#!/usr/bin/env python3
"""
BLENDSENSE — does this reference actually use designed transitions, or did the
frame-difference heuristic just miss them?

WHY THIS EXISTS. assets/pillars/travel_vlog_ANALYSIS.md line 86, written by the tool
that set the profile, against itself:

    "Blended-transition detection is a frame-difference heuristic - it catches wipes
     and fades reliably, but A VERY FAST WHIP CAN READ AS A HARD CUT."

A fast whip is exactly the transition a vlog uses. So travel_vlog's blended_pct = 0
may be an editorial fact about the genre, or it may be a blind spot in the detector -
and the difference decides whether tools/fx.py's 14-transition bank is switched off
for a good reason on this pillar. That question cannot be answered by re-reading the
same number. It needs a detector that separates the two cases.

HOW A WHIP DIFFERS FROM A CUT, MEASURABLY
  A HARD CUT is instantaneous: one frame is sharp, the next frame is sharp, and the
  histogram falls off a cliff between them. Sharpness never drops.
  A WHIP is a camera move used as a transition: for 2-5 frames the image SMEARS. That
  smear is measurable as a collapse in Laplacian variance (focus energy) with a
  simultaneous spike in inter-frame displacement. The scene changes THROUGH the smear.
  A DISSOLVE/FADE is neither: the histogram drifts across 4+ frames while sharpness
  stays roughly intact, because two sharp images are being cross-faded.

So: at every scene change, look at the sharpness trench around it.
  no trench                      -> HARD CUT
  trench 1-6 frames + motion     -> WHIP  (a DESIGNED transition, and fx.FX has one)
  sustained mid-correlation      -> DISSOLVE / FADE (what the old heuristic caught)

THE TRAP THIS TOOL IS ITSELF EXPOSED TO
  A genuinely fast handheld pan that is NOT a transition also smears. That is why a
  whip is only counted when the scene ALSO changes across the smear (histogram
  correlation before-vs-after below the cut threshold). A smear with no scene change
  is camera movement, and it is reported separately as `smear_no_cut` so the number
  is visible rather than silently folded in either direction.

USAGE
  python3 tools/blendsense.py assets/refs/travel_vlog          whole folder
  python3 tools/blendsense.py <file.mp4> [...]                 named files
  python3 tools/blendsense.py <dir> --json out.json            machine-readable
"""

import argparse
import glob
import json
import os
import sys

import cv2
import numpy as np

# Thresholds. Every one of these is a CHOICE, stated here so it can be argued with,
# and the raw per-boundary numbers are printed so a verdict can be re-derived.
CUT_CORR = 0.62      # histogram correlation below this across a boundary = scene change
SHARP_DROP = 0.55    # frame sharpness below 55% of local median = smeared frame
WHIP_MAX_FRAMES = 6  # a smear longer than this is not a whip, it is a bad shot
DISSOLVE_MIN = 4     # frames of sustained mid-correlation to call it a dissolve


def read(path, w=160, h=284, cap_frames=None):
    c = cv2.VideoCapture(path)
    fps = c.get(cv2.CAP_PROP_FPS) or 30.0
    gray, hists, sharp = [], [], []
    while True:
        ok, f = c.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        # sharpness on the FULL frame - downscaling destroys the very focus energy
        # a whip removes, which would make every frame look smeared.
        sharp.append(float(cv2.Laplacian(g, cv2.CV_64F).var()))
        s = cv2.resize(g, (w, h))
        gray.append(s.astype(np.float32))
        hh = cv2.calcHist([s], [0], None, [64], [0, 256])
        hists.append(hh / (hh.sum() + 1e-9))
        if cap_frames and len(gray) >= cap_frames:
            break
    c.release()
    return fps, gray, hists, np.array(sharp)


def analyse(path):
    fps, gray, hists, sharp = read(path)
    n = len(gray)
    if n < 12:
        return {"file": os.path.basename(path), "error": "too short / unreadable"}

    corr = np.array([cv2.compareHist(hists[i - 1], hists[i], cv2.HISTCMP_CORREL)
                     for i in range(1, n)])
    diff = np.array([float(np.mean(np.abs(gray[i] - gray[i - 1]))) for i in range(1, n)])

    # local sharpness baseline: median over a +-15 frame window, so a genuinely dark or
    # soft SHOT is not read as a permanent smear.
    med = np.array([np.median(sharp[max(0, i - 15):i + 16]) for i in range(n)])
    smeared = sharp < (SHARP_DROP * np.maximum(med, 1e-6))

    boundaries = [i for i in range(1, n) if corr[i - 1] < CUT_CORR]
    # collapse boundaries 1 frame apart (a whip produces a run of them)
    groups, cur = [], []
    for b in boundaries:
        if cur and b - cur[-1] <= 2:
            cur.append(b)
        else:
            if cur:
                groups.append(cur)
            cur = [b]
    if cur:
        groups.append(cur)

    hard, whip, dissolve, rows = 0, 0, 0, []
    for g in groups:
        a, b = g[0], g[-1]
        lo, hi = max(0, a - 4), min(n, b + 5)
        trench = int(smeared[lo:hi].sum())
        span = b - a + 1
        # dissolve: correlation sits in the mid band for several consecutive frames
        mid = int(np.sum((corr[max(0, a - 6):min(len(corr), b + 6)] > CUT_CORR) &
                         (corr[max(0, a - 6):min(len(corr), b + 6)] < 0.95)))
        if trench >= 2 and span <= WHIP_MAX_FRAMES:
            kind = "WHIP"; whip += 1
        elif mid >= DISSOLVE_MIN:
            kind = "DISSOLVE"; dissolve += 1
        else:
            kind = "HARD"; hard += 1
        rows.append({"t": round(a / fps, 2), "kind": kind, "smear_frames": trench,
                     "span": span, "corr": round(float(corr[a - 1]), 3),
                     "diff": round(float(diff[a - 1]), 1)})

    # smears that are NOT at a scene change = camera movement, not a transition.
    sm_runs, run = 0, 0
    for i in range(n):
        if smeared[i]:
            run += 1
        else:
            if 2 <= run <= WHIP_MAX_FRAMES:
                sm_runs += 1
            run = 0
    cuts = hard + whip + dissolve
    designed = whip + dissolve
    return {
        "file": os.path.basename(path), "fps": round(fps, 2), "frames": n,
        "dur_s": round(n / fps, 2), "cuts": cuts, "hard": hard, "whip": whip,
        "dissolve": dissolve, "designed": designed,
        "designed_pct": round(100.0 * designed / max(1, cuts), 1),
        "old_heuristic_pct": round(100.0 * dissolve / max(1, cuts), 1),
        "smear_no_cut": sm_runs, "rows": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    files = []
    for p in a.paths:
        if os.path.isdir(p):
            for e in ("*.mp4", "*.mov", "*.webm", "*.mkv"):
                files += sorted(glob.glob(os.path.join(p, e)))
        else:
            files.append(p)
    if not files:
        print("  no video files found"); return 2

    out = [analyse(f) for f in files]
    ok = [r for r in out if "error" not in r]

    print("=" * 86)
    print("BLENDSENSE — designed transitions vs hard cuts, whip-sensitive")
    print("=" * 86)
    print(f"  {'file':<40}{'cuts':>6}{'hard':>6}{'whip':>6}{'diss':>6}"
          f"{'designed%':>11}{'oldheur%':>10}")
    for r in out:
        if "error" in r:
            print(f"  {r['file']:<40}  {r['error']}"); continue
        print(f"  {r['file']:<40}{r['cuts']:>6}{r['hard']:>6}{r['whip']:>6}"
              f"{r['dissolve']:>6}{r['designed_pct']:>10.1f}%{r['old_heuristic_pct']:>9.1f}%")
    if ok:
        d = [r["designed_pct"] for r in ok]
        o = [r["old_heuristic_pct"] for r in ok]
        print("-" * 86)
        print(f"  MEDIAN designed {np.median(d):.1f}%   (old dissolve-only heuristic: "
              f"{np.median(o):.1f}%)   range {min(d):.1f}-{max(d):.1f}%")
        print(f"  refs using ANY designed transition: "
              f"{sum(1 for x in d if x > 0)}/{len(ok)}")
        print(f"  whips found: {sum(r['whip'] for r in ok)} across {len(ok)} references")
        print(f"  smears NOT at a cut (camera movement, not transitions): "
              f"{sum(r['smear_no_cut'] for r in ok)}")
    if not a.quiet:
        print()
        for r in ok:
            marks = [x for x in r["rows"] if x["kind"] != "HARD"]
            if marks:
                print(f"  {r['file']}")
                for m in marks[:12]:
                    print(f"     {m['t']:>6.2f}s  {m['kind']:<9} smear {m['smear_frames']}f "
                          f"span {m['span']}f  corr {m['corr']}")
    if a.json:
        json.dump(out, open(a.json, "w", encoding="utf-8"), indent=1)
        print(f"\n  json -> {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
