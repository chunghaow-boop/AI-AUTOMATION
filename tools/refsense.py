#!/usr/bin/env python3
"""
REFSENSE — the semantic half of a reference video, stored so it survives the chat.

THE GAP THIS FILLS
  refstudy.py already measures the MECHANICAL DNA of a reference: cuts/min, shot median,
  hard-vs-blended ratio, BPM, cuts-on-grid, LUFS, spectral balance, grade. That half is
  real, it runs, and it is how the pillar profiles were built.

  reverse.py states the other half in its own closing line: "this measures HOW they cut,
  not whether the idea was good. Pair it with a scene-by-scene analysis for the
  storytelling layer."

  That pairing never got a home. Every time a reference was read for its HOOK, its
  TWIST, its CTA, its content shape — that reading happened in a chat and died with it.
  intel.py has banks named hooks/transitions/twists/ctas, but they are filled by
  substring-matching an analysis produced elsewhere; it is a filing cabinet, not a
  record. So the repo has learned the FORM of good car edits and has never once written
  down WHY one worked.

WHAT THIS IS, AND THE LINE IT WILL NOT CROSS
  A record, with two halves that are kept visibly apart:

    MEASURED   numbers this file computed from the file itself. Never typed.
    READ       a human or LLM teardown: hook, twist, CTA, content shape, why it worked.
               This CANNOT be computed. No threshold detects a twist.

  An unfilled READ slot prints as UNFILLED, loudly, and `--brief` refuses to present a
  reference as understood until its slots are filled. A corpus that quietly showed empty
  slots as knowledge would be the SMOOTH NUMBER trap wearing a new hat: the appearance
  of understanding, with nothing behind it.

  It does NOT scrape. intel.py already records why ("any scraper here would break on
  first run"), platforms block it, and the sandbox allowlist blocks it too. Gavril
  downloads references himself into assets/refs/<pillar>/ — 23 are there — and that is
  the correct architecture, because a folder of files he CHOSE is worth more than a
  scraper's feed.

THE EVIDENCE IT MECHANISES
  --strip writes the first 3 seconds as a frame strip and the whole video as a contact
  sheet, so the hook can be SEEN rather than guessed at. Same pattern as clipqc's
  text-zoom: the tool does the fetching and cropping, a judgement does the reading.

Usage
  python3 tools/refsense.py --pillar car_cinematic --scan          measure + create slots
  python3 tools/refsense.py --pillar car_cinematic --strip         hook strips to look at
  python3 tools/refsense.py --pillar car_cinematic --fill FILE.mp4 \
        --hook "..." --twist "..." --cta "..." --shape "..." --why "..."
  python3 tools/refsense.py --pillar car_cinematic --brief         what the corpus knows
  python3 tools/refsense.py --pillar car_cinematic --gaps          what is still UNFILLED
"""
import argparse, glob, json, os, statistics as st, subprocess, sys
from datetime import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tools"))
A = os.path.join(HERE, "assets")

# The slots. Each is a QUESTION a marketer would ask, and not one is computable.
READ_SLOTS = {
    "hook":   "First 2 seconds: what EVENT is on screen, and what makes a thumb stop?",
    "twist":  "What reframes — the thing you did not expect at second 1?",
    "cta":    "What is the viewer asked to do, when, and how hard?",
    "shape":  "The content shape: tour / story / list / demo / reveal / comparison?",
    "why":    "Why did THIS work? One sentence. The thing worth stealing.",
    "steal":  "The one specific move to copy into our build.",
    "avoid":  "The one thing it does that we should NOT copy.",
}


def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def refdir(pillar):
    """Prefer the directory that actually CONTAINS videos, not the first that exists.

    Both layouts are live in this repo: assets/pillars/<p>/refs/ holds the analysis
    artefacts, assets/refs/<p>/ holds the actual downloads. The first version returned
    whichever existed first, which was the analysis folder — so it reported 'no
    reference videos' while 23 sat one directory away. Resolve, never assume: the same
    lesson verify.py's _first() docstring records."""
    cands = [os.path.join(A, "pillars", pillar, "refs"),
             os.path.join(A, "refs", pillar)]
    for d in cands:
        if os.path.isdir(d) and any(
                f.lower().endswith((".mp4", ".mov", ".webm", ".mkv"))
                for f in os.listdir(d)):
            return d
    for d in cands:
        if os.path.isdir(d):
            return d
    return cands[-1]


def store(pillar):
    return os.path.join(refdir(pillar), "refsense.json")


def load(pillar):
    p = store(pillar)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    return {"_what": "Per-reference record. MEASURED numbers were computed from the "
                     "file; READ slots are a human/LLM teardown and cannot be computed.",
            "_rule": "An UNFILLED slot is not knowledge. --brief will say so.",
            "pillar": pillar, "refs": {}}


def save(pillar, d):
    p = store(pillar)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1)
    return p


def videos(pillar):
    d = refdir(pillar)
    return sorted(p for p in glob.glob(os.path.join(d, "*"))
                  if p.lower().endswith((".mp4", ".mov", ".webm", ".mkv")))


# ---------------------------------------------------------------- MEASURED half
def measure(path):
    """Delegates to refstudy — the measurement stack already exists and is already how
    the pillar profiles were derived. Duplicating it would create a second set of
    numbers with different field names, which the repo already has three of."""
    try:
        import refstudy
    except Exception as e:
        return {"_not_measured": f"refstudy unavailable: {e}"}
    try:
        r = refstudy.study(path)
    except Exception as e:
        return {"_not_measured": f"refstudy.study failed: {e}"}
    keep = ("duration", "cuts_per_min", "shot_median", "shot_max", "hard_cut_pct",
            "blended_pct", "bpm", "cuts_on_grid_pct", "lufs", "lra", "true_peak",
            "black_point", "saturation")
    return {k: r.get(k) for k in keep if r.get(k) is not None}


def hook_strip(path, out_png, secs=3.0, n=6):
    """The first `secs` as a horizontal strip. The hook is a thing you LOOK at."""
    try:
        import cv2, numpy as np
    except Exception:
        return None
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    tiles = []
    for k in range(n):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(k * secs / n * fps))
        ok, fr = cap.read()
        if not ok:
            break
        fr = cv2.resize(fr, (216, 384))
        cv2.putText(fr, f"{k*secs/n:.2f}s", (7, 24), cv2.FONT_HERSHEY_SIMPLEX,
                    0.55, (0, 0, 0), 3)
        cv2.putText(fr, f"{k*secs/n:.2f}s", (7, 24), cv2.FONT_HERSHEY_SIMPLEX,
                    0.55, (255, 255, 255), 1)
        tiles.append(fr)
    cap.release()
    if not tiles:
        return None
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    cv2.imwrite(out_png, np.hstack(tiles))
    return out_png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pillar", required=True)
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--strip", action="store_true")
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--fill")
    for s in READ_SLOTS:
        ap.add_argument(f"--{s}")
    a = ap.parse_args()

    d = load(a.pillar)
    vids = videos(a.pillar)

    # -------------------------------------------------------------- scan
    if a.scan:
        if not vids:
            print(f"\n  no reference videos in {os.path.relpath(refdir(a.pillar), HERE)}")
            print(f"  Download 3-5 you consider GOOD for this pillar and put them there.")
            print(f"  Nothing here scrapes — see the docstring for why.\n")
            return 2
        print(f"\n  measuring {len(vids)} reference(s) for {a.pillar}\n")
        for v in vids:
            b = os.path.basename(v)
            print(f"    {b} ...", flush=True)
            rec = d["refs"].setdefault(b, {})
            rec["measured"] = measure(v)
            rec["measured_at"] = datetime.now().strftime("%Y-%m-%d")
            rec.setdefault("read", {k: None for k in READ_SLOTS})
            for k in READ_SLOTS:
                rec["read"].setdefault(k, None)
        p = save(a.pillar, d)
        filled = sum(1 for r in d["refs"].values()
                     if all(r.get("read", {}).get(k) for k in READ_SLOTS))
        print(f"\n  wrote {os.path.relpath(p, HERE)}")
        print(f"  {len(d['refs'])} reference(s) MEASURED · {filled} fully READ")
        print(f"\n  The measured half is done. The READ half is empty and cannot be")
        print(f"  computed — run --strip, look at the hooks, then --fill each one.\n")
        return 0

    # -------------------------------------------------------------- strip
    if a.strip:
        if not vids:
            print(f"  no reference videos in {refdir(a.pillar)}"); return 2
        odir = os.path.join(refdir(a.pillar), "_strips")
        made = 0
        for v in vids:
            b = os.path.splitext(os.path.basename(v))[0]
            r = hook_strip(v, os.path.join(odir, f"hook_{b}.png"))
            if r:
                made += 1
                print(f"    {os.path.relpath(r, HERE)}")
        print(f"\n  {made} hook strip(s) — first 3 seconds, 6 frames, timestamped.")
        print(f"  LOOK at them. The hook is not a number; this only mechanises the")
        print(f"  fetching so the judgement has something to judge.\n")
        return 0 if made else 2

    # -------------------------------------------------------------- fill
    if a.fill:
        key = os.path.basename(a.fill)
        if key not in d["refs"]:
            near = [k for k in d["refs"] if key.lower() in k.lower()]
            if len(near) == 1:
                key = near[0]
            else:
                print(f"\n  '{key}' is not in the record. Run --scan first.")
                if near:
                    print(f"  did you mean: {near}")
                print()
                return 2
        rec = d["refs"][key].setdefault("read", {})
        wrote = []
        for s in READ_SLOTS:
            v = getattr(a, s, None)
            if v:
                rec[s] = v
                wrote.append(s)
        d["refs"][key]["read_at"] = datetime.now().strftime("%Y-%m-%d")
        save(a.pillar, d)
        miss = [s for s in READ_SLOTS if not rec.get(s)]
        print(f"\n  {key}")
        print(f"    filled: {', '.join(wrote) if wrote else '(nothing passed)'}")
        print(f"    still UNFILLED: {', '.join(miss) if miss else 'none — complete'}\n")
        return 0

    # -------------------------------------------------------------- gaps
    if a.gaps:
        print(f"\n  UNFILLED READ SLOTS — {a.pillar}\n")
        if not d["refs"]:
            print("    nothing scanned yet.\n"); return 2
        total = 0
        for b, rec in sorted(d["refs"].items()):
            miss = [s for s in READ_SLOTS if not (rec.get("read") or {}).get(s)]
            total += len(miss)
            mark = "COMPLETE" if not miss else f"{len(miss)}/{len(READ_SLOTS)} missing"
            print(f"    {b}")
            print(f"        {mark}" + (f": {', '.join(miss)}" if miss else ""))
        print(f"\n    {total} slot(s) unfilled across {len(d['refs'])} reference(s).")
        print(f"    Each one is a question no measurement can answer:")
        for k, q in READ_SLOTS.items():
            print(f"      {k:7s} {q}")
        print()
        return 1 if total else 0

    # -------------------------------------------------------------- brief
    if a.brief:
        print("=" * 78)
        print(f"REFSENSE BRIEF — {a.pillar}")
        print("=" * 78)
        if not d["refs"]:
            print("\n  nothing scanned. Run --scan.\n"); return 2
        meas = [r["measured"] for r in d["refs"].values()
                if isinstance(r.get("measured"), dict) and "_not_measured" not in r["measured"]]

        def med(k):
            v = [m[k] for m in meas if isinstance(m.get(k), (int, float))]
            return round(st.median(v), 2) if v else None

        print(f"\n  MEASURED — computed from {len(meas)} file(s), never typed\n")
        for k in ("cuts_per_min", "shot_median", "blended_pct", "bpm",
                  "cuts_on_grid_pct", "lufs", "lra", "black_point", "saturation"):
            v = med(k)
            print(f"    {k:18s} median {v}")

        full = {b: r for b, r in d["refs"].items()
                if all((r.get("read") or {}).get(k) for k in READ_SLOTS)}
        part = {b: r for b, r in d["refs"].items() if b not in full
                and any((r.get("read") or {}).get(k) for k in READ_SLOTS)}
        empty = [b for b in d["refs"] if b not in full and b not in part]

        print(f"\n  READ — {len(full)} complete · {len(part)} partial · "
              f"{len(empty)} UNREAD\n")
        for b, r in list(full.items()) + list(part.items()):
            print(f"    {b}")
            for k in READ_SLOTS:
                v = (r.get("read") or {}).get(k)
                print(f"      {k:7s} {v if v else '*** UNFILLED ***'}")
            print()
        if empty:
            print(f"    {len(empty)} reference(s) have NO teardown at all:")
            for b in empty:
                print(f"      {b}")
        print("\n" + "=" * 78)
        if not full:
            print("  THIS CORPUS KNOWS NOTHING SEMANTIC YET.")
            print("  Every number above is HOW these videos cut. Not one line explains")
            print("  WHY any of them worked. Do not plan from this and call it research.")
        else:
            print(f"  {len(full)} reference(s) are fully read and may be cited in a plan's")
            print(f"  CONTENT block. The rest are measurements only.")
        print("=" * 78 + "\n")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
