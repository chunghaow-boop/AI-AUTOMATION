#!/usr/bin/env python3
"""CONTACT SHEET — the LOOK that has to happen before anything is assembled.

HIS STANDING ORDER, 2026-08-07, after the mahua preview:
    "yes this should be the first thing you show me in the preview just now
     before generating"

Rule 8 has always said frames ARE the work, but nothing in the pipeline ever put
20 frames in front of a human in one image. A contact sheet costs zero credits and
zero seconds, and on mahua it surfaced in one glance what four rounds of judges on
prose could not: three different shirts, an invented sign board, and a two-tier
waterfall where the plate specified one unbroken column.

    python tools/contact.py mahua                 # from the delivered cut
    python tools/contact.py mahua --raw           # from the raw clips, at ingest
    python tools/contact.py mahua --video path.mp4

--raw is the important one: it runs BEFORE a single frame is assembled, so a bad
clip is caught while it is still one 22.5cr regeneration and not a rebuilt edit.
"""
import argparse
import importlib
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

PANEL_W, PANEL_H, LABEL_H = 216, 384, 26


def _grab(path, t):
    cap = cv2.VideoCapture(path)
    cap.set(cv2.CAP_PROP_POS_MSEC, max(0.0, t) * 1000)
    ok, fr = cap.read()
    cap.release()
    return fr if ok else None


def _stats(fr):
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    return g.mean(), np.percentile(g, 5), np.percentile(g, 95)


def sheet(panels, out, cols=5):
    rows = (len(panels) + cols - 1) // cols
    im = Image.new("RGB", (cols * PANEL_W, rows * (PANEL_H + LABEL_H)), (12, 12, 14))
    d = ImageDraw.Draw(im)
    for n, (frame, label, warn) in enumerate(panels):
        x, y = (n % cols) * PANEL_W, (n // cols) * (PANEL_H + LABEL_H)
        im.paste(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                 .resize((PANEL_W, PANEL_H)), (x, y))
        d.text((x + 5, y + PANEL_H + 3), label, fill=(235, 235, 235))
        if warn:
            d.text((x + 5, y + PANEL_H + 14), warn, fill=(255, 150, 90))
            d.rectangle([x, y, x + PANEL_W - 2, y + PANEL_H - 2], outline=(255, 150, 90))
    im.save(out)
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--raw", action="store_true", help="sample the raw clips, not the cut")
    ap.add_argument("--video", default=None)
    a = ap.parse_args()

    P = importlib.import_module(f"plans.{a.plan}")
    pdir = os.path.join(HERE, "projects", a.plan)
    band = ((P.__dict__.get("_band") or {}) or {})
    lo, hi = 35.0, 200.0
    panels = []

    if a.raw:
        for key in P.SOURCES:
            fn = getattr(P, "CLIPS", {}).get(key)
            path = os.path.join(pdir, "clips", fn) if fn else None
            if not path or not os.path.exists(path):
                print(f"  MISSING clip for source {key}")
                continue
            for frac, tag in ((0.15, "head"), (0.5, "mid"), (0.85, "tail")):
                cap = cv2.VideoCapture(path)
                dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / max(1.0, cap.get(cv2.CAP_PROP_FPS))
                cap.release()
                fr = _grab(path, dur * frac)
                if fr is None:
                    continue
                mean, p5, p95 = _stats(fr)
                warn = ""
                if mean < lo:
                    warn = f"luma {mean:.0f} BELOW {lo:.0f}"
                elif p95 < 150:
                    warn = f"no highlight p95 {p95:.0f}"
                panels.append((fr, f"{key} {tag}  luma {mean:.0f}", warn))
        out = os.path.join(pdir, "analysis", "CONTACT_RAW.png")
    else:
        video = a.video or os.path.join(pdir, f"{a.plan}_v1.mp4")
        if not os.path.exists(video):
            print(f"no video at {video}")
            return 1
        tl, total = P.timeline()
        cap = cv2.VideoCapture(video)
        real = cap.get(cv2.CAP_PROP_FRAME_COUNT) / max(1.0, cap.get(cv2.CAP_PROP_FPS))
        cap.release()
        drift = real / total if total else 1.0
        for i, ((src, crop, kind, _n), (st, d, _k)) in enumerate(zip(P.SHOTS, tl)):
            fr = _grab(video, (st + d * 0.45) * drift)
            if fr is None:
                continue
            mean, p5, p95 = _stats(fr)
            warn = f"luma {mean:.0f} BELOW {lo:.0f}" if mean < lo else ""
            panels.append((fr, f"{i:02d} {src} {crop:.2f}x  luma {mean:.0f}", warn))
        out = os.path.join(pdir, "analysis", "CONTACT.png")

    os.makedirs(os.path.dirname(out), exist_ok=True)
    size = sheet(panels, out)
    print(f"  {len(panels)} panels -> {out}  {size[0]}x{size[1]}")
    print("  LOOK AT IT. Wardrobe, signage, repeated framings and identity all read "
          "in one glance and no mechanical gate sees any of them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
