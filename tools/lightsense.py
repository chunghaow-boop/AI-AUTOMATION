#!/usr/bin/env python3
"""
LIGHTSENSE — see what the EDIT did to the LIGHT, shot by shot, as a picture.

WHY THIS EXISTS
  2026-08-05. Gavril: "the lighting at some scenes are super dark where i can barely
  see the video... i think the video output from higgsfield lighting is already pretty
  good maybe the video editor edit for the second time on the lighting."

  He was right, and no gate in the project could have told him so, because every gate
  measured the FINISHED file against a target. None of them ever asked the only
  question that mattered: WHAT DID I CHANGE, AND BY HOW MUCH?

  That is a missing sense, not a missing threshold. This tool is the sense.

HOW TO READ IT  (this is the part worth learning — the numbers are the easy half)

  1. ALWAYS DIFF THE STAGE, NEVER ONLY THE RESULT.
     A stage is honest if you can state its effect as a number in the unit a human
     perceives. If the only way to describe what a stage did is to name its parameter
     ("brightness 0.14"), you do not know what it did. 0.14 moved shots by 41 luma in
     one clip and 73 in another. Same parameter. Different edit.

  2. TRUST THE SOURCE UNTIL HE SAYS OTHERWISE.
     The model's output is a deliberate creative act by a system he is paying for and
     approving. The edit's job is continuity, not taste. When the delivered luma is
     far from the source luma, the burden of proof is on the EDIT.

  3. HIS APPROVAL BAND IS WIDER THAN ANY TARGET.
     His three approved raws measured 45.1, 89.7 and 92.9. A 47-luma spread is fine
     by him. Any stage that pulls toward one number is not improving consistency,
     it is deleting range. Consistency between NEIGHBOURS is the real goal; sameness
     across the whole video is a defect wearing a metric's clothes.

  4. READ BOTH DIRECTIONS.
     The complaint was "too dark", so the instinct is to hunt for crushing. The same
     bug had blown a 44-luma shot to 117. A stage that is miscalibrated is wrong
     UPWARDS too, and the bright failure is easier to miss because bright reads as
     "fine" in a thumbnail.

  5. WHEN A CORRECTION AND ITS TARGET DISAGREE, SUSPECT THE TRANSFER FUNCTION.
     If corrections consistently land on the FAR side of the target, the stage is not
     "too aggressive" — its model of its own effect is wrong. Measure the response:
     apply a known gain, re-measure, divide. Here: assumed 134 luma/unit, actual
     174-519. Everything downstream of that guess was fiction, including a previous
     session's conclusion that "widening the clamp makes exposure worse".

  6. A SMOOTH METRIC IS NOT EVIDENCE OF A GOOD EDIT.
     Exposure-match scored well precisely BECAUSE it was flattening his footage.
     Ask of every passing check: what did it have to break to pass?

USAGE
  python3 tools/lightsense.py --project kk
  python3 tools/lightsense.py --project kk --ref /path/to/raw_higgsfield_clip.mp4
"""
import os, sys, glob, argparse
import numpy as np
import cv2

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def levels(path):
    """Mean luma per frame. 96x171 to match every other stage in this project — a
    different resize is a different number and the comparison silently breaks."""
    c = cv2.VideoCapture(path)
    v = []
    while True:
        ok, f = c.read()
        if not ok:
            break
        v.append(cv2.cvtColor(cv2.resize(f, (96, 171)), cv2.COLOR_BGR2GRAY).mean())
    c.release()
    return np.array(v, dtype=float)


def stat(path):
    v = levels(path)
    if not len(v):
        return None
    return dict(mean=float(v.mean()), lo=float(v.min()), hi=float(v.max()),
                p5=float(np.percentile(v, 5)), n=len(v))


def strip(src, dst, out_png, label):
    """Side-by-side middle frame, source LEFT and delivered RIGHT, at MATCHED SCALE.
    Matched scale matters: the identity verdict on KK flipped between crop sizes in one
    session. Never present two crops of different sizes and call it a comparison."""
    a = cv2.VideoCapture(src); b = cv2.VideoCapture(dst)
    na = int(a.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    a.set(cv2.CAP_PROP_POS_FRAMES, na // 2); b.set(cv2.CAP_PROP_POS_FRAMES, na // 2)
    oka, fa = a.read(); okb, fb = b.read()
    a.release(); b.release()
    if not (oka and okb):
        return None
    h = 260
    fa = cv2.resize(fa, (int(fa.shape[1] * h / fa.shape[0]), h))
    fb = cv2.resize(fb, (int(fb.shape[1] * h / fb.shape[0]), h))
    pad = np.full((h, 8, 3), 40, np.uint8)
    img = np.hstack([fa, pad, fb])
    bar = np.full((26, img.shape[1], 3), 20, np.uint8)
    cv2.putText(bar, label, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (235, 235, 235), 1)
    cv2.imwrite(out_png, np.vstack([bar, img]))
    return out_png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--ref", action="append", default=[],
                    help="a RAW model clip he has approved; sets the reference band")
    ap.add_argument("--sheet", default=None, help="write contact strips to this dir")
    a = ap.parse_args()

    pdir = os.path.join(HERE, "projects", a.project)
    tmp = os.path.join(pdir, "tmp")
    srcs = sorted(glob.glob(os.path.join(tmp, "c[0-9][0-9].mp4")))
    if not srcs:
        print("NOT MEASURED — no segment cache in tmp/. Build first; a lighting claim "
              "with no before-file is an opinion.")
        return 2

    if a.ref:
        rs = [stat(p) for p in a.ref]
        rs = [r for r in rs if r]
        if rs:
            print(f"APPROVED REFERENCE BAND  {min(r['mean'] for r in rs):.1f} – "
                  f"{max(r['mean'] for r in rs):.1f} mean luma   ({len(rs)} raw clips)")
            print("  Anything the edit delivers outside this band is a CHOICE the edit "
                  "made, and it needs a reason.\n")

    print(f"{'sh':>3} {'MODEL GAVE':>11} {'EDIT SHIPPED':>13} {'the edit did':>13}   what to look at")
    rows = []
    for s in srcs:
        i = int(os.path.basename(s)[1:3])
        cand = sorted(glob.glob(s[:-4] + "_m*.mp4"))
        d = cand[-1] if cand else s
        sa, sb = stat(s), stat(d)
        if not (sa and sb):
            print(f"{i:>3}   UNREADABLE — do not average around it")
            continue
        mv = sb["mean"] - sa["mean"]
        rows.append((i, sa, sb, mv, s, d))
        note = ""
        if abs(mv) >= 25:
            note = "RELIT, not matched — this is a second grade"
        elif abs(mv) >= 12:
            note = "large for a continuity fix; confirm by eye"
        if sb["p5"] < 18 and sa["p5"] >= 18:
            note = (note + " | " if note else "") + "shadows crushed BY THE EDIT"
        print(f"{i:>3} {sa['mean']:>11.1f} {sb['mean']:>13.1f} {mv:>+13.1f}   {note}")

    if not rows:
        return 2
    mvs = [abs(r[3]) for r in rows]
    print(f"\nworst single relight {max(mvs):.1f} luma · mean {np.mean(mvs):.1f} · "
          f"{sum(1 for m in mvs if m >= 25)} shot(s) relit ≥25")
    print(f"delivered band {min(r[2]['mean'] for r in rows):.1f} – "
          f"{max(r[2]['mean'] for r in rows):.1f}   "
          f"(model gave {min(r[1]['mean'] for r in rows):.1f} – "
          f"{max(r[1]['mean'] for r in rows):.1f})")

    rng_in = max(r[1]['mean'] for r in rows) - min(r[1]['mean'] for r in rows)
    rng_out = max(r[2]['mean'] for r in rows) - min(r[2]['mean'] for r in rows)
    if rng_in > 1:
        print(f"RANGE KEPT {100*rng_out/rng_in:.0f}%  — under ~70% the edit is "
              f"flattening the day into one light state.")

    if a.sheet:
        os.makedirs(a.sheet, exist_ok=True)
        worst = sorted(rows, key=lambda r: -abs(r[3]))[:6]
        for i, sa, sb, mv, s, d in worst:
            strip(s, d, os.path.join(a.sheet, f"light_{i:02d}.png"),
                  f"shot {i}   MODEL {sa['mean']:.0f}  ->  EDIT {sb['mean']:.0f}   ({mv:+.0f} luma)")
        print(f"\ncontact strips -> {a.sheet}  (LOOK at them; the number is only the pointer)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
