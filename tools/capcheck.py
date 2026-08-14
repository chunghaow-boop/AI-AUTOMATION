#!/usr/bin/env python3
"""
CAPCHECK — the caption-legibility gate (L137 candidate).

WHY THIS EXISTS (2026-08-12, session 11)
  His eye on PANBORNEO_V5: "sometimes the caption is white, so it clashes with the
  environment color." Frame 48 proved it: white SABAH ENDS HERE on sun-bleached
  asphalt. captionmgr.contrast_ok() only ever checked the BOXED style against an
  assumed mid-grey — the actual footage was never consulted. This gate consults it.

METHOD (calibrated per L136: against the real signal, not a proxy)
  For each caption span: sample 5 frames, crop the caption band (y..y+h, central
  88% width), take the MEDIAN luma as the background (text pixels are a minority,
  median ignores them). Convert text colour and band luma to WCAG relative
  luminance; effective bg under a scrim of opacity a is bg*(1-a). Ratio floor 4.5:1
  (arm's-length phone in daylight). A stroke does NOT raise the ratio — V5 had a
  3px stroke and still clashed; strokes rescue edges, not fill legibility.

EXIT 0 all spans pass · EXIT 1 any span below floor (prints the worst offender).

Usage
  python3 tools/capcheck.py VIDEO --cards cards.json
    cards.json: [{"text","start","end","y":0.70,"h":0.09,"color":[255,255,255],
                  "scrim":0.0}, ...]   y/h are fractions of frame height.
  python3 tools/capcheck.py PANBORNEO_V5.mp4 --v5   # built-in V5 card table
"""
import subprocess, sys, json, argparse
import numpy as np

FLOOR = 4.5
V5_CARDS = [  # from build_panborneo_v4.py: FS=44 at y=908/1280, white, no scrim
    dict(text="SABAH ENDS HERE",          start=0.15, end=3.0),
    dict(text="REWIND TO DAWN",           start=4.92, end=8.5),
    dict(text="KLIAS: PROBOSCIS COUNTRY", start=20.0, end=23.6),
    dict(text="SARAWAK. STILL TOLL-FREE.",start=34.6, end=38.2),
    dict(text="KUCHING BY DUSK?",         start=54.3, end=57.9),
]
for c in V5_CARDS: c.update(y=908/1280, h=60/1280, color=[255,255,255], scrim=0.0)

def band_luma(video, t, y, h, W, H):
    cw = int(W*0.88); cx = (W-cw)//2
    cy, ch = int(H*y), max(8, int(H*h))
    r = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",video,
        "-frames:v","1","-vf",f"crop={cw}:{ch}:{cx}:{cy}","-f","rawvideo",
        "-pix_fmt","gray","-"], capture_output=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    return float(np.median(a)) if a.size else None

def rel_lum(rgb):
    s = [(v/255) for v in rgb]
    s = [(v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4) for v in s]
    return 0.2126*s[0] + 0.7152*s[1] + 0.0722*s[2]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--cards"); ap.add_argument("--v5", action="store_true")
    ap.add_argument("--floor", type=float, default=FLOOR)
    a = ap.parse_args()
    cards = V5_CARDS if a.v5 else json.load(open(a.cards))
    probe = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","json",a.video],
        capture_output=True, text=True)
    st = json.loads(probe.stdout)["streams"][0]; W, H = st["width"], st["height"]
    worst, results = None, []
    for c in cards:
        ts = np.linspace(c["start"]+0.1, c["end"]-0.1, 5)
        lumas = [band_luma(a.video, t, c["y"], c["h"], W, H) for t in ts]
        lumas = [l for l in lumas if l is not None]
        bg = max(lumas)                      # worst frame in the span governs
        bg_eff = bg * (1 - c.get("scrim", 0.0))
        Lt, Lb = rel_lum(c["color"]), rel_lum([bg_eff]*3)
        hi, lo = max(Lt, Lb), min(Lt, Lb)
        ratio = (hi+0.05)/(lo+0.05)
        ok = ratio >= a.floor
        results.append((c["text"][:28], round(bg,1), round(ratio,2), "PASS" if ok else "FAIL"))
        if not ok and (worst is None or ratio < worst[1]): worst = (c["text"], ratio)
    for t, bg, r, v in results:
        print(f"  {v}  {r:>6.2f}:1  band-luma {bg:>5.1f}  {t}")
    if worst:
        print(f"CAPCHECK FAIL — worst: \"{worst[0]}\" at {worst[1]:.2f}:1 (floor {a.floor}:1)")
        sys.exit(1)
    print(f"CAPCHECK PASS — {len(results)} spans ≥ {a.floor}:1")
    sys.exit(0)

if __name__ == "__main__":
    main()
