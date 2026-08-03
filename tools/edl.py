#!/usr/bin/env python3
"""
EDL — the AI video editor. Generation -> Edit Decision List -> render -> gate -> auto-amend.

The edit becomes DATA, not a one-off ffmpeg command: diffable, versionable, re-renderable, and
amendable by the QC gate without a human. That is the difference between "Claude ran ffmpeg" and
an actual AI editor.

TRANSCRIPTION TIERS (auto-detected, degrades gracefully, always reports which tier was used):
  1. faster-whisper   word-level timings          <- best; needs local Claude Code (unrestricted net)
  2. openai-whisper   segment-level timings
  3. vosk             word-level, lower accuracy
  4. silence-map      phrase boundaries only      <- works offline in the Cowork sandbox
Tier 4 is what runs here today. Tiers 1-3 need model weights, which the sandbox proxy blocks.

Usage:
  python3 edl.py build  IN.mp4 --format vlog [--bed bed.wav] [--cards cards.json] -o edit.json
  python3 edl.py render IN.mp4 edit.json -o OUT.mp4
  python3 edl.py auto   IN.mp4 --format vlog [--bed bed.wav] -o OUT.mp4     # build+render+gate+amend
"""
import argparse, json, os, subprocess, sys, shutil, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _guard_output(out, *inputs):
    """Refuse to write over a source file. Protects original footage."""
    import os, sys
    ao = os.path.abspath(out)
    for i in inputs:
        if i and os.path.abspath(i) == ao:
            sys.exit(f"REFUSED: output '{out}' is the same file as an input. "
                     f"Source footage is never overwritten. Choose a different -o.")
    return out

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout + r.stderr

def dur_of(p):
    o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"').strip()
    try: return float(o.splitlines()[0])
    except Exception: return 0.0

# ---------------- 1. TRANSCRIPTION (tiered) ----------------
def transcribe(path):
    """Returns {tier, words:[{w,start,end}], phrases:[{text,start,end}]}"""
    wav = os.path.join(tempfile.gettempdir(), "edl_audio.wav")
    sh(f'ffmpeg -y -v error -i "{path}" -ac 1 -ar 16000 "{wav}"')
    if not os.path.exists(wav):
        return {"tier": "none", "words": [], "phrases": [], "note": "no audio track"}

    # tier 1
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel("base", device="cpu", compute_type="int8")
        segs, _ = m.transcribe(wav, word_timestamps=True)
        words, phrases = [], []
        for s in segs:
            phrases.append({"text": s.text.strip(), "start": round(s.start,3), "end": round(s.end,3)})
            for w in (s.words or []):
                words.append({"w": w.word.strip(), "start": round(w.start,3), "end": round(w.end,3)})
        return {"tier": "faster-whisper", "words": words, "phrases": phrases}
    except Exception: pass

    # tier 2
    try:
        import whisper
        m = whisper.load_model("base")
        r = m.transcribe(wav)
        phrases = [{"text": s["text"].strip(), "start": round(s["start"],3), "end": round(s["end"],3)}
                   for s in r.get("segments", [])]
        return {"tier": "openai-whisper", "words": [], "phrases": phrases}
    except Exception: pass

    # tier 3
    try:
        from vosk import Model, KaldiRecognizer
        import wave, json as _j
        mdir = os.environ.get("VOSK_MODEL", "model")
        wf = wave.open(wav, "rb"); m = Model(mdir)
        rec = KaldiRecognizer(m, wf.getframerate()); rec.SetWords(True)
        words = []
        while True:
            d = wf.readframes(4000)
            if not d: break
            if rec.AcceptWaveform(d):
                for w in _j.loads(rec.Result()).get("result", []):
                    words.append({"w": w["word"], "start": w["start"], "end": w["end"]})
        for w in _j.loads(rec.FinalResult()).get("result", []):
            words.append({"w": w["word"], "start": w["start"], "end": w["end"]})
        return {"tier": "vosk", "words": words, "phrases": []}
    except Exception: pass

    # tier 4 — offline fallback: silence map gives phrase boundaries
    out = sh(f'ffmpeg -hide_banner -nostats -i "{wav}" -af silencedetect=noise=-30dB:d=0.35 -f null - 2>&1')
    import re
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?\d+\.?\d*)", out)]
    ends   = [float(x) for x in re.findall(r"silence_end:\s*(-?\d+\.?\d*)", out)]
    total  = dur_of(wav)
    onsets = ([0.0] if (not starts or starts[0] > 0.25) else []) + ends
    phrases = []
    for s in sorted(onsets):
        nxt = [x for x in starts if x > s]
        phrases.append({"text": "", "start": round(s,3), "end": round(nxt[0] if nxt else total,3)})
    return {"tier": "silence-map", "words": [], "phrases": phrases,
            "note": "no ASR weights available — phrase boundaries only, no text. "
                    "Run locally with faster-whisper for word-level editing."}

# ---------------- 2. ANALYSIS ----------------
def analyse(path, fmt, bed=None):
    import pacing
    p = pacing.analyse(path, fmt)
    grid, bpm = None, None
    try:
        import rhythm
        src = bed or path
        flux, hop = rhythm.stft_flux(rhythm.pcm(src))
        on = rhythm.pick_onsets(flux, hop)
        bpm, grid = rhythm.estimate_tempo(flux, hop, onsets=on)
    except Exception: pass
    return p, (grid if grid is not None else None), bpm

def snap(t, grid, max_shift=0.12):
    if grid is None or len(grid) == 0: return t
    n = float(grid[int(np.argmin(np.abs(np.asarray(grid) - t)))])
    return round(n, 3) if abs(n - t) <= max_shift else round(t, 3)

# ---------------- 3. BUILD THE EDL ----------------
def build(path, fmt="vlog", bed=None, cards=None):
    import pacing
    p, grid, bpm = analyse(path, fmt, bed)
    tr = transcribe(path)
    total = p["duration"]
    T = pacing.FORMATS[fmt]

    edl = {"source": os.path.basename(path), "format": fmt, "duration": total,
           "bpm": bpm, "transcription_tier": tr["tier"],
           "keep": [], "captions": [], "sfx": [], "transitions": [], "notes": []}
    if tr.get("note"): edl["notes"].append(tr["note"])

    # --- keep-ranges: drop dead zones (long + low motion) ---
    dead = [d for d in p["dead_zones"] if d["severity"] == "HIGH"]
    cuts = [0.0] + list(p["shot_cuts"] if "shot_cuts" in p else []) + [total]
    drops = []
    for d in dead:
        # trim the quiet tail of an over-long static shot, keep its first max_shot seconds
        s = d["start"] + T["max_shot"]
        e = min(total, d["start"] + d["len"])
        if e - s > 0.4: drops.append([round(s,3), round(e,3)])
    keep, cur = [], 0.0
    for s, e in sorted(drops):
        if s > cur: keep.append([round(cur,3), round(s,3)])
        cur = max(cur, e)
    if cur < total: keep.append([round(cur,3), round(total,3)])
    edl["keep"] = keep or [[0.0, round(total,3)]]
    if drops: edl["notes"].append(f"dropped {len(drops)} dead zone(s): {drops}")

    # --- captions: on the spoken phrase, snapped to the beat when close ---
    if cards:
        cardlist = json.load(open(cards)) if isinstance(cards, str) else cards
        onsets = [ph["start"] for ph in tr["phrases"]] or [0.5]
        for c in cardlist:
            want = c.get("start", 0.5)
            near = min(onsets, key=lambda o: abs(o - want))
            st = near if abs(near - want) < 2.0 else want
            edl["captions"].append({"text": c["text"], "start": round(st,3),
                                    "end": round(c.get("end", st + 3.0),3)})
    elif tr["phrases"] and tr["tier"] in ("faster-whisper","openai-whisper"):
        for ph in tr["phrases"][:8]:
            if ph["text"]:
                edl["captions"].append({"text": ph["text"][:42], "start": ph["start"], "end": ph["end"]})

    # --- sfx: one accent on each retained cut, snapped to the grid ---
    for c in (p.get("shot_cuts") or []):
        if any(a <= c <= b for a, b in edl["keep"]):
            edl["sfx"].append({"id": "whoosh", "t": snap(c, grid)})

    # --- transitions: hard cut by default (short-form), per file 30 ---
    for c in (p.get("shot_cuts") or []):
        edl["transitions"].append({"type": "hard", "at": snap(c, grid)})

    edl["diagnostics"] = {
        "cuts_per_min": p["cuts_per_min"], "target_cpm": list(T["cpm"]),
        "hook_motion": p["hook"]["motion"], "dead_zones": len(p["dead_zones"]),
        "retention_estimate_pct": p["retention_estimate_pct"],
    }
    return edl

# ---------------- 4. RENDER ----------------
def render(src, edl, out):
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font):
        font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    tmp = tempfile.mkdtemp()
    # keep-ranges -> trim + concat
    parts = []
    for i, (a, b) in enumerate(edl["keep"]):
        p = os.path.join(tmp, f"p{i}.mp4")
        sh(f'ffmpeg -y -v error -ss {a} -to {b} -i "{src}" -c:v libx264 -crf 20 -preset veryfast '
           f'-pix_fmt yuv420p -c:a aac "{p}"')
        if os.path.exists(p): parts.append(p)
    if not parts: return None
    if len(parts) == 1:
        stitched = parts[0]
    else:
        lst = os.path.join(tmp, "l.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        stitched = os.path.join(tmp, "s.mp4")
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c copy "{stitched}"')
    # captions
    if edl.get("captions"):
        vf = []
        for i, c in enumerate(edl["captions"]):
            tf = os.path.join(tmp, f"c{i}.txt")
            open(tf, "w", encoding="utf-8").write(c["text"])
            y = "h*0.10" if i % 2 == 0 else "h*0.78"
            vf.append(f"drawtext=fontfile={font}:textfile={tf}:"
                      f"enable='between(t,{c['start']},{c['end']})':fontsize=46:fontcolor=white:"
                      f"box=1:boxcolor=black@0.55:boxborderw=18:x=(w-tw)/2:y={y}")
        sh(f'ffmpeg -y -v error -i "{stitched}" -vf "{",".join(vf)}" -c:v libx264 -crf 20 '
           f'-preset veryfast -pix_fmt yuv420p -c:a copy "{out}"')
    else:
        shutil.copy(stitched, out)
    return out if os.path.exists(out) else None

# ---------------- 5. GATE + AUTO-AMEND ----------------
def gate(path, fmt, cards=None):
    import mastermind, pacing
    v = mastermind.video_metrics(path, tempfile.mkdtemp())
    a = mastermind.audio_metrics(path)
    sync = mastermind.caption_sync(cards or [], a)
    s = mastermind.score(v, a, {}, sync, None)
    p = pacing.analyse(path, fmt)
    return {"score": s["final"], "verdict": s["verdict"], "gates": s["hard_gates"],
            "pacing_findings": p["findings"], "cuts_per_min": p["cuts_per_min"],
            "retention_estimate": p["retention_estimate_pct"]}

def amend(edl, g, fmt):
    """Adjust the EDL in response to gate findings. Returns (edl, changed)."""
    import pacing
    T = pacing.FORMATS[fmt]; changed = False
    for f in g.get("pacing_findings", []):
        if "CUTS TOO SLOW" in f and edl["keep"]:
            # tighten: shave the tail of the longest kept range
            longest = max(range(len(edl["keep"])), key=lambda i: edl["keep"][i][1]-edl["keep"][i][0])
            a, b = edl["keep"][longest]
            if b - a > T["max_shot"] + 0.5:
                edl["keep"][longest] = [a, round(b - min(1.5, (b-a)*0.25), 3)]
                edl.setdefault("amendments", []).append(f"tightened range {longest} for pace")
                changed = True
    for gate_msg in g.get("gates", []):
        if "LOUDNESS" in gate_msg:
            edl["normalize_audio"] = True
            edl.setdefault("amendments", []).append("audio normalisation enabled")
            changed = True
    return edl, changed

# ---------------- CLI ----------------
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build");  b.add_argument("video"); b.add_argument("--format", default="vlog")
    b.add_argument("--bed"); b.add_argument("--cards"); b.add_argument("-o", default="edit.json")
    r = sub.add_parser("render"); r.add_argument("video"); r.add_argument("edl"); r.add_argument("-o", default="out.mp4")
    a = sub.add_parser("auto");   a.add_argument("video"); a.add_argument("--format", default="vlog")
    a.add_argument("--bed"); a.add_argument("--cards"); a.add_argument("-o", default="out.mp4")
    a.add_argument("--max-loops", type=int, default=3)
    A = ap.parse_args()

    if A.cmd == "build":
        e = build(A.video, A.format, A.bed, A.cards)
        json.dump(e, open(A.o, "w"), indent=2)
        print(json.dumps({k: e[k] for k in ("transcription_tier","bpm","keep","diagnostics","notes")}, indent=2))
        print(f"\nEDL -> {A.o}")

    elif A.cmd == "render":
        e = json.load(open(A.edl))
        _guard_output(A.o, A.video)
        o = render(A.video, e, A.o)
        print("rendered ->", o or "FAILED")

    elif A.cmd == "auto":
        cards = json.load(open(A.cards)) if A.cards else None
        e = build(A.video, A.format, A.bed, A.cards)
        print(f"[build] tier={e['transcription_tier']} bpm={e['bpm']} keep={len(e['keep'])} ranges")
        cur = A.video
        for loop in range(1, A.max_loops + 1):
            out = A.o if loop == 1 else A.o.replace(".mp4", f"_v{loop}.mp4")
            got = render(A.video, e, out)
            if not got: print("[render] FAILED"); return
            g = gate(got, A.format, cards)
            print(f"[gate {loop}] score={g['score']} verdict={g['verdict']} "
                  f"cpm={g['cuts_per_min']} est_ret={g['retention_estimate']}%")
            for x in (g["gates"] + g["pacing_findings"]): print("    -", x)
            cur = got
            if g["verdict"] == "SHIP" and not g["pacing_findings"]:
                print(f"\nPASS on loop {loop} -> {cur}"); break
            e, changed = amend(e, g, A.format)
            if not changed:
                print(f"\nSTOPPING: gate still failing but no automatic amendment applies.")
                print("Escalate to a human seat — do not loop blindly (session rule 2).")
                break
        json.dump(e, open(A.o.replace(".mp4", ".edl.json"), "w"), indent=2)
        print("final EDL ->", A.o.replace(".mp4", ".edl.json"))

if __name__ == "__main__":
    main()
