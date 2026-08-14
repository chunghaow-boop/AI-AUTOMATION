#!/usr/bin/env python3
"""
AUTOCUT — transcript-driven editing. This is the "AI edits the video for me" mechanism.

Without a transcript an AI editor cuts blind (which is why caption timing had to fall back to
silence gaps in the sandbox). With one, the edit is decided from the TEXT:

  1. FILLER REMOVAL      cut "um", "uh", "you know", "basically", "like" + the silence around it
  2. JUMP CUTS           tighten every inter-sentence pause to a target gap
  3. RETAKE DETECTION    near-duplicate consecutive sentences -> keep the LAST take
  4. HOOK SELECTION      score every sentence; the strongest becomes the opening
  5. WORD-EXACT CAPTIONS burn-in timed to the word, not the phrase
  6. B-ROLL MARKERS      sentences making a checkable claim -> flag for cover footage

LOCAL ONLY (needs transcribe.py -> faster-whisper). Sandbox proxy blocks the weights.

Usage:
  python3 transcribe.py IN.mp4 -o t.json
  python3 autocut.py IN.mp4 t.json -o OUT.mp4 [--captions] [--hook-first] [--gap 0.25]
  python3 autocut.py IN.mp4 t.json --plan-only        # print the plan, cut nothing
"""
import argparse, json, os, re, subprocess, tempfile, difflib

FILLERS = {"um","uh","erm","ah","hmm","like","basically","actually","literally",
           "you know","i mean","sort of","kind of","right?","so yeah","okay so"}
CLAIM = re.compile(r"\b(\d[\d,\.]*\s*(k|rm|km|cc|hp|bhp|years?|ringgit)|rm\s?\d|"
                   r"cheaper|expensive|fastest|best|worst|never|always|guarantee)\b", re.I)
HOOK_WORDS = re.compile(r"\b(you|your|never|nobody|secret|mistake|stop|why|how|"
                        r"truth|actually|before you|don't)\b", re.I)


def _guard_output(out, *inputs):
    """Refuse to write over a source file. Protects original footage."""
    import os, sys
    ao = os.path.abspath(out)
    for i in inputs:
        if i and os.path.abspath(i) == ao:
            sys.exit(f"REFUSED: output '{out}' is the same file as an input. "
                     f"Source footage is never overwritten. Choose a different -o.")
    return out

def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True)

def norm(s): return re.sub(r"[^a-z0-9 ]","", s.lower()).strip()

def build_plan(tr, gap=0.25, drop_fillers=True, hook_first=False):
    words, phrases = tr.get("words",[]), tr.get("phrases",[])
    if not words and not phrases:
        return {"error":"empty transcript"}
    keep, cuts, notes = [], [], []

    # 1 · filler words -> cut ranges
    filler_ranges = []
    if drop_fillers and words:
        i = 0
        while i < len(words):
            w1 = norm(words[i]["w"])
            two = f"{w1} {norm(words[i+1]['w'])}" if i+1 < len(words) else ""
            if two in FILLERS:
                filler_ranges.append([words[i]["start"], words[i+1]["end"]]); i += 2; continue
            if w1 in FILLERS:
                filler_ranges.append([words[i]["start"], words[i]["end"]]); i += 1; continue
            i += 1
        if filler_ranges: notes.append(f"{len(filler_ranges)} filler(s) removed")

    # 2 · retakes: near-duplicate consecutive sentences -> drop the earlier one
    retake_ranges = []
    for a, b in zip(phrases, phrases[1:]):
        if a["text"] and b["text"]:
            r = difflib.SequenceMatcher(None, norm(a["text"]), norm(b["text"])).ratio()
            if r > 0.82:
                retake_ranges.append([a["start"], a["end"]])
    if retake_ranges: notes.append(f"{len(retake_ranges)} retake(s) dropped (kept last take)")

    # 3 · long inter-sentence pauses -> tighten to `gap`
    pause_ranges = []
    for a, b in zip(phrases, phrases[1:]):
        silence = b["start"] - a["end"]
        if silence > gap:
            pause_ranges.append([round(a["end"] + gap, 3), round(b["start"], 3)])
    if pause_ranges: notes.append(f"{len(pause_ranges)} pause(s) tightened to {gap}s")

    drops = sorted(filler_ranges + retake_ranges + pause_ranges)
    merged = []
    for s, e in drops:
        if merged and s <= merged[-1][1] + 0.02: merged[-1][1] = max(merged[-1][1], e)
        else: merged.append([s, e])

    dur = tr.get("duration") or (phrases[-1]["end"] if phrases else 0)
    cur = 0.0
    for s, e in merged:
        if s > cur: keep.append([round(cur,3), round(s,3)])
        cur = max(cur, e)
    if cur < dur: keep.append([round(cur,3), round(dur,3)])

    # 4 · hook: score sentences
    scored = []
    for p in phrases:
        t = p["text"]
        if not t: continue
        s = 0
        s += 3*len(HOOK_WORDS.findall(t))
        s += 2 if t.strip().endswith("?") else 0
        s += 2 if 4 <= len(t.split()) <= 14 else 0
        s -= 2 if len(t.split()) > 22 else 0
        s += 1 if CLAIM.search(t) else 0
        scored.append({"text":t,"start":p["start"],"end":p["end"],"score":s})
    scored.sort(key=lambda x:-x["score"])

    # 5 · b-roll markers
    broll = [{"start":p["start"],"end":p["end"],"claim":p["text"][:70]}
             for p in phrases if p["text"] and CLAIM.search(p["text"])]

    return {"keep":keep or [[0,dur]], "dropped":merged, "notes":notes,
            "hook_candidates":scored[:5], "broll_markers":broll,
            "saved_seconds":round(sum(e-s for s,e in merged),2),
            "original_duration":round(dur,2)}

def captions_from_words(words, max_chars=28):
    """Group words into short burn-in cards, word-exact."""
    cards, cur, start = [], [], None
    for w in words:
        if start is None: start = w["start"]
        cur.append(w["w"])
        if len(" ".join(cur)) >= max_chars or w["w"].endswith((".","?","!")):
            cards.append({"text":" ".join(cur), "start":start, "end":w["end"]})
            cur, start = [], None
    if cur: cards.append({"text":" ".join(cur), "start":start, "end":words[-1]["end"]})
    return cards

def render(src, plan, out, caps=None):
    tmp = tempfile.mkdtemp(); parts = []
    for i,(a,b) in enumerate(plan["keep"]):
        if b - a < 0.05: continue
        p = os.path.join(tmp, f"p{i}.mp4")
        sh(f'ffmpeg -y -v error -ss {a} -to {b} -i "{src}" -c:v libx264 -crf 20 '
           f'-preset veryfast -pix_fmt yuv420p -c:a aac "{p}"')
        if os.path.exists(p): parts.append(p)
    if not parts: return None
    lst = os.path.join(tmp,"l.txt"); open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
    stitched = os.path.join(tmp,"s.mp4")
    sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c copy "{stitched}"')
    if not caps:
        sh(f'cp "{stitched}" "{out}"'); return out
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font):
        for c in ["/System/Library/Fonts/Helvetica.ttc","/Library/Fonts/Arial.ttf"]:
            if os.path.exists(c): font = c; break
    vf = []
    for i,c in enumerate(caps[:80]):
        tf = os.path.join(tmp,f"c{i}.txt"); open(tf,"w",encoding="utf-8").write(c["text"])
        vf.append(f"drawtext=fontfile={font}:textfile={tf}:"
                  f"enable='between(t,{c['start']},{c['end']})':fontsize=44:fontcolor=white:"
                  f"box=1:boxcolor=black@0.55:boxborderw=16:x=(w-tw)/2:y=h*0.78")
    sh(f'ffmpeg -y -v error -i "{stitched}" -vf "{",".join(vf)}" -c:v libx264 -crf 20 '
       f'-preset veryfast -pix_fmt yuv420p -c:a copy "{out}"')
    return out if os.path.exists(out) else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("transcript")
    ap.add_argument("-o", default="autocut.mp4"); ap.add_argument("--gap", type=float, default=0.25)
    ap.add_argument("--captions", action="store_true"); ap.add_argument("--keep-fillers", action="store_true")
    ap.add_argument("--plan-only", action="store_true")
    a = ap.parse_args()

    tr = json.load(open(a.transcript))
    if tr.get("tier") in ("missing","none"):
        print("!!", tr.get("error","no transcript")); return
    plan = build_plan(tr, a.gap, not a.keep_fillers)
    if plan.get("error"): print("!!", plan["error"]); return

    print(f"original {plan['original_duration']}s -> saves {plan['saved_seconds']}s "
          f"({len(plan['keep'])} kept ranges)")
    for n in plan["notes"]: print("  -", n)
    print("\nHOOK CANDIDATES (strongest first):")
    for h in plan["hook_candidates"]:
        print(f"  [{h['score']:>2}] {h['start']:>6.2f}  {h['text'][:66]}")
    if plan["broll_markers"]:
        print(f"\nB-ROLL needed on {len(plan['broll_markers'])} claim(s):")
        for b in plan["broll_markers"][:5]: print(f"  {b['start']:>6.2f}  {b['claim']}")
    json.dump(plan, open(a.o.replace(".mp4",".plan.json"),"w"), indent=2)
    if a.plan_only: return

    caps = captions_from_words(tr["words"]) if (a.captions and tr.get("words")) else None
    _guard_output(a.o, a.video)
    got = render(a.video, plan, a.o, caps)
    print("\nrendered ->", got or "FAILED")

if __name__ == "__main__":
    main()
