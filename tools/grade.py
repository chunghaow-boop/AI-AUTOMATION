#!/usr/bin/env python3
"""
GRADE — colour-match AI footage to YOUR phone footage. The hybrid-seam fix.

THE PROBLEM: cutting between real and AI is the #1 tell. Not because the AI looks fake — because
the COLOUR doesn't match. Your phone has a look (white balance, contrast curve, saturation,
black level). Seedance has a different one. The eye reads the mismatch instantly, even when it
can't say why.

THE RULE: always match AI **to** the real footage, never the reverse. Real is the anchor —
it's what the audience accepts as true.

HOW: measures per-channel mean/std and black/white points in Lab-ish space on both clips, then
builds an ffmpeg colour correction that moves the AI toward the reference. Prints the numbers so
the match is auditable, not a vibe.

Usage:
  python3 grade.py profile REAL.mp4                     # measure and save a look profile
  python3 grade.py match AI.mp4 --ref REAL.mp4 -o graded.mp4
  python3 grade.py match AI.mp4 --profile look.json -o graded.mp4
  python3 grade.py compare A.mp4 B.mp4                  # how far apart are they?
"""
import argparse, json, os, subprocess, tempfile
import numpy as np
import cv2


def _guard_output(out, *inputs):
    """Refuse to write over a source file. Protects original footage."""
    import os, sys
    ao = os.path.abspath(out)
    for i in inputs:
        if i and os.path.abspath(i) == ao:
            sys.exit(f"REFUSED: output '{out}' is the same file as an input. "
                     f"Source footage is never overwritten. Choose a different -o.")
    return out

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True); return r.stdout + r.stderr

def sample_frames(path, n=12):
    cap = cv2.VideoCapture(path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    if total <= 0: cap.release(); return []
    idxs = np.linspace(total*0.05, total*0.95, n).astype(int)
    out = []
    for i in idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i))
        ok, fr = cap.read()
        if ok: out.append(fr)
    cap.release(); return out

def profile_of(path, n=12):
    frames = sample_frames(path, n)
    if not frames: return None
    stats = {"b": [], "g": [], "r": [], "l_mean": [], "l_std": [], "sat": [],
             "black": [], "white": []}
    for f in frames:
        for i, k in enumerate(("b", "g", "r")):
            stats[k].append(float(f[:, :, i].mean()))
        lab = cv2.cvtColor(f, cv2.COLOR_BGR2LAB)
        stats["l_mean"].append(float(lab[:, :, 0].mean()))
        stats["l_std"].append(float(lab[:, :, 0].std()))
        hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        stats["sat"].append(float(hsv[:, :, 1].mean()))
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        stats["black"].append(float(np.percentile(g, 1)))
        stats["white"].append(float(np.percentile(g, 99)))
    return {k: round(float(np.mean(v)), 2) for k, v in stats.items()}

def build_filter(src, ref):
    """Derive an ffmpeg eq/colorbalance chain moving src toward ref."""
    # exposure / contrast from L channel
    bright = (ref["l_mean"] - src["l_mean"]) / 255.0
    contrast = (ref["l_std"] / src["l_std"]) if src["l_std"] > 1 else 1.0
    contrast = float(np.clip(contrast, 0.75, 1.35))
    sat = (ref["sat"] / src["sat"]) if src["sat"] > 1 else 1.0
    sat = float(np.clip(sat, 0.7, 1.4))
    # white balance: per-channel deltas normalised
    def bal(ch):
        d = (ref[ch] - src[ch]) / 255.0
        return float(np.clip(d, -0.3, 0.3))
    rs, gs, bs = bal("r"), bal("g"), bal("b")
    f = (f"eq=brightness={bright:.4f}:contrast={contrast:.4f}:saturation={sat:.4f},"
         f"colorbalance=rm={rs:.4f}:gm={gs:.4f}:bm={bs:.4f}")
    return f, {"brightness": round(bright,4), "contrast": round(contrast,4),
               "saturation": round(sat,4), "r_shift": round(rs,4),
               "g_shift": round(gs,4), "b_shift": round(bs,4)}

def distance(a, b):
    keys = ["b","g","r","l_mean","sat"]
    return round(float(np.mean([abs(a[k]-b[k]) for k in keys])), 2)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("profile"); p1.add_argument("video"); p1.add_argument("-o", default="look.json")
    p2 = sub.add_parser("match"); p2.add_argument("video"); p2.add_argument("--ref")
    p2.add_argument("--profile"); p2.add_argument("-o", default="graded.mp4")
    p2.add_argument("--strength", type=float, default=1.0, help="0-1, dial the match back")
    p3 = sub.add_parser("compare"); p3.add_argument("a"); p3.add_argument("b")
    a = ap.parse_args()

    if a.cmd == "profile":
        pr = profile_of(a.video)
        if not pr: print("!! could not read frames"); return
        json.dump(pr, open(a.o, "w"), indent=1)
        print(json.dumps(pr, indent=1)); print(f"\nlook profile -> {a.o}")
        print("Use this as the anchor for every AI clip in the same video.")
        return

    if a.cmd == "compare":
        pa, pb = profile_of(a.a), profile_of(a.b)
        if not pa or not pb: print("!! could not read"); return
        d = distance(pa, pb)
        print(f"A: {json.dumps(pa)}\nB: {json.dumps(pb)}")
        print(f"\ncolour distance: {d}")
        print("  <4   = matched, the seam will be invisible")
        print("  4-10 = noticeable on a cut — run `match`")
        print("  >10  = obvious mismatch, this is the AI tell")
        return

    if a.cmd == "match":
        if a.profile: ref = json.load(open(a.profile))
        elif a.ref:   ref = profile_of(a.ref)
        else: print("!! need --ref or --profile"); return
        src = profile_of(a.video)
        if not src or not ref: print("!! could not read frames"); return
        before = distance(src, ref)
        f, params = build_filter(src, ref)
        if a.strength != 1.0:
            s = float(np.clip(a.strength, 0, 1))
            f = (f"eq=brightness={params['brightness']*s:.4f}:"
                 f"contrast={1+(params['contrast']-1)*s:.4f}:"
                 f"saturation={1+(params['saturation']-1)*s:.4f},"
                 f"colorbalance=rm={params['r_shift']*s:.4f}:"
                 f"gm={params['g_shift']*s:.4f}:bm={params['b_shift']*s:.4f}")
        _guard_output(a.o, a.video)
        sh(f'ffmpeg -y -v error -i "{a.video}" -vf "{f}" -c:v libx264 -crf 18 '
           f'-preset veryfast -pix_fmt yuv420p -c:a copy "{a.o}"')
        after_p = profile_of(a.o)
        after = distance(after_p, ref) if after_p else None
        print(json.dumps(params, indent=1))
        print(f"\ncolour distance  before {before}  ->  after {after}")
        if after is not None and after < before:
            print(f"improved by {round(before-after,2)} -> {a.o}")
        else:
            print("!! no improvement — clips may differ in content, not grade. "
                  "Try --strength 0.6, or match on similar shots.")

if __name__ == "__main__":
    main()
