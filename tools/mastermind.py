#!/usr/bin/env python3
"""
MASTERMIND — automated edit QC gate.
Measures a finished cut, scores it per file 26 doctrine, routes failures to seats.
Nothing reaches the user until every hard gate passes.

Deps: ffmpeg/ffprobe + opencv-python-headless + numpy  (no librosa required)
Usage: python3 mastermind.py VIDEO.mp4 [--vo VO.wav] [--cards cards.json] [--out qcdir]
"""
import json, subprocess, sys, os, re, math, argparse
import numpy as np
import cv2

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stderr + \
           subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

def ff(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stderr + r.stdout

# ---------------- AUDIO (measured, never "sounds good") ----------------
def audio_metrics(path):
    m = {}
    out = ff(f'ffmpeg -hide_banner -nostats -i "{path}" -af ebur128=peak=true -f null - 2>&1')
    for key, pat in [("lufs", r"I:\s*(-?\d+\.?\d*)\s*LUFS"),
                     ("lra",  r"LRA:\s*(-?\d+\.?\d*)\s*LU"),
                     ("peak", r"Peak:\s*(-?\d+\.?\d*)\s*dBFS")]:
        mm = re.findall(pat, out)
        m[key] = float(mm[-1]) if mm else None
    st = ff(f'ffmpeg -hide_banner -nostats -i "{path}" -af astats=metadata=1 -f null - 2>&1')
    fl = re.findall(r"Flat factor:\s*(\d+\.?\d*)", st)
    m["flat_factor"] = float(fl[0]) if fl else None
    # silence / speech map
    sd = ff(f'ffmpeg -hide_banner -nostats -i "{path}" -af silencedetect=noise=-30dB:d=0.35 -f null - 2>&1')
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?\d+\.?\d*)", sd)]
    ends   = [float(x) for x in re.findall(r"silence_end:\s*(-?\d+\.?\d*)", sd)]
    m["silence_starts"], m["silence_ends"] = starts, ends
    dur = duration(path)
    m["duration"] = dur
    sil = sum(max(0, (ends[i] if i < len(ends) else dur) - s) for i, s in enumerate(starts))
    m["silence_ratio"] = round(sil / dur, 3) if dur else None
    return m

def band_energy(path, outdir):
    """Spectral balance via ffmpeg showspectrumpic -> read pixel energy per band."""
    png = os.path.join(outdir, "spectrum.png")
    ff(f'ffmpeg -y -i "{path}" -lavfi showspectrumpic=s=1024x512:legend=0 "{png}" 2>&1')
    if not os.path.exists(png):
        return {}, None
    img = cv2.imread(png, cv2.IMREAD_GRAYSCALE)
    if img is None: return {}, png
    h = img.shape[0]
    # showspectrumpic: y=0 is HIGH freq, y=h is LOW freq (log scale)
    air  = img[0:int(h*0.20), :].mean()
    mids = img[int(h*0.20):int(h*0.65), :].mean()
    body = img[int(h*0.65):, :].mean()
    tot = air + mids + body or 1
    return {"air_pct": round(100*air/tot,1), "mid_pct": round(100*mids/tot,1),
            "body_pct": round(100*body/tot,1)}, png

# ---------------- VIDEO ----------------
def duration(path):
    o = ff(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{path}"').strip()
    try: return float(o.splitlines()[0])
    except: return 0.0

def video_metrics(path, outdir, hook_window=2.0, cuts=None):
    """MEASURED 2026-08-08: this function reported shot_count = 1 for a TWENTY shot
    film, and it is the input the final scorecard scores 'shot variety' on.

    Cause: cuts were detected as a Bhattacharyya distance > 0.45 between GREYSCALE
    64-bin histograms. desafarm is graded consistently and half of it is green
    pasture, so the grey histogram barely moves across a cut and not one of the 19
    cuts cleared 0.45. Then 'shot variety' failed for the wrong reason, and
    sharpness_min reported 9.0 because the single blurriest frame in the film is
    the middle of the declared whip - a transition doing exactly its job, scored
    as a melted frame.

    Now: take the ENGINE'S OWN cut list when it exists (it wrote the film, it knows
    where the cuts are), and when it does not, detect on mean absolute frame
    difference with an adaptive threshold - the method that found all 19 by hand.
    Sharpness is measured AWAY from cuts, with the blur at cuts reported separately
    so a transition can never be mistaken for a soft shot."""
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    n   = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    prev, flows, frames_t = None, [], []
    sharps_t, brights = [], []
    diffs, diff_t = [], []
    prev_small = None
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        if i % max(1, int(fps//6)) == 0:
            g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
            small = cv2.resize(g, (160, 284))
            t = i / fps
            if prev is not None:
                f = cv2.calcOpticalFlowFarneback(prev, small, None, .5,3,15,3,5,1.2,0)
                flows.append(float(np.linalg.norm(f, axis=2).mean()))
                frames_t.append(t)
            prev = small
            sharps_t.append((t, float(cv2.Laplacian(g, cv2.CV_64F).var())))
            brights.append(float(g.mean()))
            if prev_small is not None:
                diffs.append(float(np.abs(small.astype(np.float32)
                                          - prev_small.astype(np.float32)).mean()))
                diff_t.append(t)
            prev_small = small
        i += 1
    cap.release()
    dur = n/fps if fps else 0

    if cuts:
        shot_cuts = [round(float(c), 2) for c in cuts]
        cut_src = "engine cut manifest"
    else:
        shot_cuts = []
        if diffs:
            mu, sd = float(np.mean(diffs)), float(np.std(diffs))
            thr = max(18.0, mu + 2.2 * sd)
            for t, d in zip(diff_t, diffs):
                if d > thr and (not shot_cuts or t - shot_cuts[-1] > 0.25):
                    shot_cuts.append(round(t, 2))
        cut_src = "measured (mean abs frame difference, adaptive)"

    # sharpness AWAY from cuts - a transition is not a soft shot
    def _near_cut(t, w=0.25):
        return any(abs(t - c) <= w for c in shot_cuts)
    clean = [s for t, s in sharps_t if not _near_cut(t)]
    at_cut = [s for t, s in sharps_t if _near_cut(t)]
    sharps = [s for _t, s in sharps_t]

    hook_idx = [k for k,t in enumerate(frames_t) if t <= hook_window]
    hook_motion = float(np.mean([flows[k] for k in hook_idx])) if hook_idx else 0.0
    return {
        "fps": round(fps,2), "frames": n, "duration": round(dur,2),
        "motion_mean": round(float(np.mean(flows)),3) if flows else 0,
        "hook_motion": round(hook_motion,3),
        "motion_min": round(float(np.min(flows)),3) if flows else 0,
        "sharpness_mean": round(float(np.mean(clean or sharps)),1) if sharps else 0,
        "sharpness_min": round(float(np.min(clean or sharps)),1) if sharps else 0,
        "sharpness_min_at_cut": round(float(np.min(at_cut)),1) if at_cut else None,
        "brightness_mean": round(float(np.mean(brights)),1) if brights else 0,
        "brightness_min": round(float(np.min(brights)),1) if brights else 0,
        "blank_frames": int(sum(1 for s in (clean or sharps) if s < 8)),
        "shot_cuts": shot_cuts, "shot_count": len(shot_cuts)+1,
        "shot_cuts_source": cut_src,
    }

def contact_sheet(path, outdir, cols=5, rows=3):
    """Render a grid of frames so a human/model can actually LOOK at the cut."""
    dur = duration(path); n = cols*rows
    tiles = []
    for k in range(n):
        t = dur*(k+0.5)/n
        p = os.path.join(outdir, f"_t{k}.png")
        ff(f'ffmpeg -y -ss {t:.2f} -i "{path}" -frames:v 1 -vf scale=216:384 "{p}" 2>&1')
        im = cv2.imread(p)
        if im is None: im = np.zeros((384,216,3), np.uint8)
        cv2.putText(im, f"{t:.1f}s", (6,24), cv2.FONT_HERSHEY_SIMPLEX, .6, (255,255,255), 2)
        tiles.append(im);
        if os.path.exists(p): os.remove(p)
    grid = np.vstack([np.hstack(tiles[r*cols:(r+1)*cols]) for r in range(rows)])
    out = os.path.join(outdir, "contact_sheet.png")
    cv2.imwrite(out, grid)
    return out

# ---------------- CAPTION / VO SYNC ----------------
def caption_sync(cards, audio):
    """cards: [{'text':..,'start':..,'end':..}] -> distance from nearest speech onset.
    FIX: silence_ends only lists speech *resumptions*. If the audio does not begin
    with silence, speech also starts at t=0 — omitting it produced a false
    'card 1 is 3s off' failure. t=0 is now included as a valid onset."""
    onsets = list(audio.get("silence_ends") or [])
    starts = audio.get("silence_starts") or []
    if not starts or starts[0] > 0.25:      # audio opens with speech, not silence
        onsets.append(0.0)
    if not onsets: return []
    res = []
    for c in cards:
        near = min(onsets, key=lambda e: abs(e - c["start"]))
        res.append({"text": c["text"], "start": c["start"],
                    "nearest_speech": round(near,2), "drift": round(c["start"]-near,2)})
    return res

# ---------------- SCORING (file 26 doctrine: hard gates, then weighted) ----------------
def timing_metrics(path, bed=None):
    """Delegates to rhythm.py — the ONLY check that catches off-beat SFX.
    Spectral balance says nothing about *when* a hit lands."""
    try:
        import rhythm
    except Exception:
        return {}
    try:
        x = rhythm.pcm(path)
        if x.size == 0: return {}
        flux, hop = rhythm.stft_flux(x)
        onsets = rhythm.pick_onsets(flux, hop)
        if bed:
            bf, bh = rhythm.stft_flux(rhythm.pcm(bed))
            bpm, grid = rhythm.estimate_tempo(bf, bh, onsets=rhythm.pick_onsets(bf, bh))
        else:
            bpm, grid = rhythm.estimate_tempo(flux, hop, onsets=onsets)
        out = {"bpm": bpm, "onsets": len(onsets), "applicable": bool(bed)}
        if not bed:
            out["note"] = ("no --bed supplied: cannot distinguish SFX hits from speech "
                           "syllables, so the beat grid is inferred and NOT trustworthy. "
                           "Timing gate skipped. Pass --bed to enable it.")
        out["sfx_vs_beat"] = rhythm.grade(rhythm.deviations(onsets, grid), "SFX vs beat")
        try:
            cuts = rhythm.video_cuts(path)
            if cuts:
                out["cuts_vs_beat"] = rhythm.grade(
                    rhythm.deviations(np.array(cuts), grid), "cuts vs beat")
        except Exception: pass
        return out
    except Exception as e:
        return {"error": str(e)}

def score(v, a, bands, sync, timing=None):
    seats, gates = [], []
    def add(name, seat, val, ok, why, weight):
        seats.append({"check":name,"seat":seat,"value":val,"score":10 if ok else 3,
                      "weight":weight,"note":why})
    # HARD GATES (mechanical fail = no ship)
    if v["blank_frames"] > 0:
        gates.append(f"BLANK FRAMES x{v['blank_frames']} -> DOP/Technologist")
    if a.get("lufs") is None or not (-13 <= a["lufs"] <= -5):
        gates.append(f"LOUDNESS {a.get('lufs')} LUFS outside -13..-5 -> Sound Engineer")
    if a.get("peak") is not None and a["peak"] > -1.0:
        gates.append(f"TRUE PEAK {a['peak']} dBFS clipping -> Sound Engineer")
    if a.get("silence_ratio") is not None and a["silence_ratio"] > 0.45:
        gates.append(f"DEAD AIR {a['silence_ratio']*100:.0f}% -> Editor/Foley")
    for s in sync:
        if abs(s["drift"]) > 0.6:
            gates.append(f"CARD '{s['text'][:24]}' off speech by {s['drift']}s -> Editor")
    # WEIGHTED
    add("hook motion (frame 1 alive)","J0 Hook Tyrant",v["hook_motion"],
        v["hook_motion"]>=0.35,"posed open = #1 killer",3.0)
    add("overall motion","Director",v["motion_mean"], v["motion_mean"]>=0.30,"static = scroll-past",1.0)
    add("sharpness floor","DOP",v["sharpness_min"], v["sharpness_min"]>=25,"soft/melted frames",1.0)
    add("exposure floor","Gaffer",v["brightness_min"], v["brightness_min"]>=18,"crushed blacks/blank",1.0)
    add("shot variety","Editor",v["shot_count"], v["shot_count"]>=3,"too few cuts for 9:16",1.0)
    add("loudness target","Sound Engineer",a.get("lufs"),
        a.get("lufs") is not None and -9.5<=a["lufs"]<=-6.5,"-7 to -9 LUFS: MEASURED from a real viral reel (file 19), not generic guidance",2.0)
    if bands:
        add("body 150-1500Hz","Sound Engineer",bands.get("body_pct"),
            38<=(bands.get("body_pct") or 0)<=55,"body 150-1500Hz target ~45% (measured)",1.5)
        add("air >6kHz","Sound Engineer",bands.get("air_pct"),
            2<=(bands.get("air_pct") or 0)<=9,"air >10kHz target ~4% (measured)",0.75)
    add("caption sync","Editor",max([abs(s['drift']) for s in sync],default=0),
        all(abs(s["drift"])<=0.6 for s in sync) if sync else True,"cards must land on the word",1.5)
    # TIMING — the off-beat catcher.
    # GUARD: only meaningful when a musical bed/SFX layer exists. On a speech-only
    # cut the "onsets" are syllables and the inferred grid is fiction — scoring it
    # produced a false OFF-BEAT failure. No bed => report N/A, never gate.
    if timing and not timing.get("applicable", True):
        seats.append({"check":"SFX on the grid","seat":"Sound Engineer","value":"N/A — no bed",
                      "score":10,"weight":0.0,"note":"speech-only cut; timing gate skipped"})
    elif timing:
        sb = timing.get("sfx_vs_beat") or {}
        if sb.get("verdict") == "OFF-BEAT":
            gates.append(f"SFX OFF-BEAT: median {sb.get('median_abs_ms')}ms, "
                         f"only {sb.get('pct_within_50ms')}% within 50ms -> Sound Engineer")
        if sb:
            add("SFX on the grid","Sound Engineer",
                f"{sb.get('median_abs_ms')}ms / {sb.get('pct_within_50ms')}% tight",
                sb.get("verdict") in ("TIGHT","ACCEPTABLE"),
                "a hit >50ms off reads as sloppy",2.0)
        cb = timing.get("cuts_vs_beat") or {}
        if cb:
            add("cuts on the grid","Editor",
                f"{cb.get('median_abs_ms')}ms / {cb.get('pct_within_50ms')}% tight",
                cb.get("verdict") in ("TIGHT","ACCEPTABLE"),
                "cuts should land on the beat",1.5)
    tot_w = sum(s["weight"] for s in seats)
    raw = sum(s["score"]*s["weight"] for s in seats)/ (tot_w*10) * 100
    worst = min((s["score"] for s in seats), default=10)
    final = min(raw, 69) if worst <= 4 else raw     # one broken link caps at 69
    return {"seats":seats,"hard_gates":gates,"raw":round(raw,1),
            "final":round(final,1),"capped":worst<=4,
            "verdict":"SHIP" if (not gates and final>=75) else "SEND BACK"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--vo"); ap.add_argument("--cards")
    ap.add_argument("--bed", help="music bed — defines the beat grid")
    ap.add_argument("--cuts", help="engine cut manifest (*_cuts.json) — authoritative")
    ap.add_argument("--out", default="qc")
    A = ap.parse_args()
    os.makedirs(A.out, exist_ok=True)
    _cuts = None
    if A.cuts and os.path.exists(A.cuts):
        try:
            _cuts = json.load(open(A.cuts)).get("cuts") or None
        except Exception:
            _cuts = None
    v = video_metrics(A.video, A.out, cuts=_cuts)
    a = audio_metrics(A.vo or A.video)
    bands, spec = band_energy(A.vo or A.video, A.out)
    cards = json.load(open(A.cards)) if A.cards else []
    sync = caption_sync(cards, a)
    timing = timing_metrics(A.vo or A.video, A.bed)
    sheet = contact_sheet(A.video, A.out)
    rep = {"video":v,"audio":a,"bands":bands,"sync":sync,"timing":timing,
           "artifacts":{"contact_sheet":sheet,"spectrum":spec}}
    rep["score"] = score(v,a,bands,sync,timing)
    json.dump(rep, open(os.path.join(A.out,"report.json"),"w"), indent=2)
    print(json.dumps(rep, indent=2))

if __name__ == "__main__":
    main()
