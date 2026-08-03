#!/usr/bin/env python3
"""
ANIMATE — turn a still into something that reads as a SHOT, not a slideshow.

THE PROBLEM (his words: "it literally showed it with a stagnant image of fish")
  A Ken Burns zoom always reads as a still. The move is rigid - every pixel travels on the
  same transform - so the eye instantly classifies it as a photograph being panned. The old
  setting made it worse: zoom+0.0012/frame over 2.4s is a 1.00->1.086 push, i.e. 8% across
  the whole shot. Imperceptible.

WHAT ACTUALLY DEFEATS IT  (each measured by optical flow, not opinion)
  1. PARALLAX      near and far move at different rates, so the frame stops being rigid.
                   No depth map available, so depth is approximated from vertical position
                   plus local detail - good enough to break rigidity, which is the point.
  2. INTERNAL MOTION  something moves inside the frame:
                   caustics  - travelling light bands for anything underwater
                   drift     - floating particles / plankton / dust
                   glow      - a breathing sun or highlight bloom for sunsets
  3. HANDHELD      a smooth random walk on offset + rotation. Machine pans read as machine.
  4. EASED PUSH    cubic ease-in-out at 18-24%, not linear 8%.
  5. GRAIN + WEAVE both mask residual staticness and match generated footage better.

Presets: underwater · sunset · generic
Usage:
  python3 animate.py in.png out.mp4 --dur 2.4 --preset underwater
  python3 animate.py in.png out.mp4 --preset sunset --measure
"""
import argparse, os, subprocess, sys
import numpy as np

try:
    import cv2
except ImportError:
    sys.exit("needs opencv: pip install opencv-python-headless")

W, H, FPS = 720, 1280, 30

def _writer(out, w=W, h=H, fps=FPS):
    """Raw BGR frames straight into ffmpeg's stdin - no PNG per frame."""
    return subprocess.Popen(
        f'ffmpeg -y -v error -f rawvideo -pix_fmt bgr24 -s {w}x{h} -framerate {fps} '
        f'-i - -vf "setsar=1" -c:v libx264 -crf 19 -preset veryfast -pix_fmt yuv420p "{out}"',
        shell=True, stdin=subprocess.PIPE)

def ease(t):
    """Cubic ease-in-out. A move that starts and stops abruptly reads as mechanical."""
    return 4*t*t*t if t < 0.5 else 1 - pow(-2*t + 2, 3) / 2

def depth_map(img):
    """Approximate depth: lower in frame = nearer, high local detail = nearer.
    Not metric depth - just enough spatial variation to break a rigid transform."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)/255.0
    detail = cv2.GaussianBlur(np.abs(cv2.Laplacian(g, cv2.CV_32F)), (0,0), 9)
    detail = detail/(detail.max() or 1)
    h = img.shape[0]
    vert = np.repeat(np.linspace(0.15, 1.0, h, dtype=np.float32)[:, None], img.shape[1], axis=1)
    d = 0.65*vert + 0.35*detail
    return cv2.GaussianBlur(d.astype(np.float32), (0,0), 15)

_GRID = {}
def grid(shape):
    if shape not in _GRID:
        h, w = shape
        _GRID[shape] = np.mgrid[0:h, 0:w].astype(np.float32)
    return _GRID[shape]

_RIP = {}
def ripple(shape, t, amp=6.0, rate=1.0):
    """Quarter-resolution ripple, upsampled. Full-res cost 5.5M sin/frame and dominated
    runtime; the field is smooth so decimating it changes nothing visible."""
    h, w = shape
    qh, qw = max(8, h//4), max(8, w//4)
    key = (qh, qw)
    if key not in _RIP:
        yy, xx = np.mgrid[0:qh, 0:qw].astype(np.float32)
        _RIP[key] = (yy*0.064, yy*0.164, xx*0.044, xx*0.076, xx*0.148, yy*0.036)
    a1, a2, a3, a4, a5, a6 = _RIP[key]
    dx = (np.sin(a1 + t*2.7*rate)*0.6 + np.sin(a2 - t*4.1*rate + 1.2)*0.3
          + np.sin(a3 + t*1.9*rate)*0.35)
    dy = (np.sin(a4 - t*3.1*rate + 0.7)*0.6 + np.sin(a5 + t*4.6*rate)*0.28
          + np.sin(a6 - t*2.2*rate)*0.3)
    dx = cv2.resize(dx*amp, (w, h), interpolation=cv2.INTER_LINEAR)
    dy = cv2.resize(dy*amp, (w, h), interpolation=cv2.INTER_LINEAR)
    return dx, dy

def _ripple_old(shape, t, amp=6.0, rate=1.0):
    """Time-varying local warp. Returns (dx, dy) offset fields in pixels.
    This is the single most effective anti-still measure: content moves non-rigidly."""
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = (np.sin(yy*0.016 + t*2.7*rate) * 0.6 +
          np.sin(yy*0.041 - t*4.1*rate + 1.2) * 0.3 +
          np.sin(xx*0.011 + t*1.9*rate) * 0.35)
    dy = (np.sin(xx*0.019 - t*3.1*rate + 0.7) * 0.6 +
          np.sin(xx*0.037 + t*4.6*rate) * 0.28 +
          np.sin(yy*0.009 - t*2.2*rate) * 0.3)
    return dx*amp, dy*amp

_CAU = {}
def caustics(shape, t, strength=7.0, seed=0):
    """Travelling interference bands - the light pattern on a shallow reef floor.
    Quarter-res + upsample: full res was ~5M sin/frame and dominated runtime."""
    h, w = shape
    qh, qw = max(8, h//4), max(8, w//4)
    key = (qh, qw)
    if key not in _CAU:
        yy, xx = np.mgrid[0:qh, 0:qw].astype(np.float32)
        _CAU[key] = (xx*0.052 + yy*0.032, xx*0.028 - yy*0.068, xx*0.084 + yy*0.076)
    p1, p2, p3 = _CAU[key]
    v = (np.sin(p1 + t*7.5) + np.sin(p2 - t*5.4 + 1.7) + 0.6*np.sin(p3 + t*10.4 + 0.4)) / 2.6
    return cv2.resize(v*strength, (w, h), interpolation=cv2.INTER_LINEAR)

def animate(src, out, dur=2.4, preset="generic", zoom=0.20, seed=11, quiet=False):
    img = cv2.imread(src, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"cannot read {src}")
    # work oversized so parallax + handheld never expose an edge
    OW, OH = int(W*1.35), int(H*1.35)
    ih, iw = img.shape[:2]
    s = max(OW/iw, OH/ih)
    img = cv2.resize(img, (int(iw*s)+1, int(ih*s)+1), interpolation=cv2.INTER_LANCZOS4)
    ih, iw = img.shape[:2]
    cx, cy = iw//2, ih//2
    img = img[max(0,cy-OH//2):cy-OH//2+OH, max(0,cx-OW//2):cx-OW//2+OW]
    d = depth_map(img)

    rng = np.random.default_rng(seed)
    n = int(dur*FPS)
    # handheld: smoothed random walk, so it drifts like a held camera
    hx = np.cumsum(rng.normal(0, 1.0, n)); hy = np.cumsum(rng.normal(0, 1.0, n))
    hr = np.cumsum(rng.normal(0, 0.02, n))
    k = max(3, n//5)
    sm = lambda v: np.convolve(v, np.ones(k)/k, mode="same")
    hx, hy, hr = sm(hx)*2.2, sm(hy)*2.2, sm(hr)*0.35

    parts = None
    if preset in ("underwater", "generic"):
        m = 46 if preset == "underwater" else 22
        parts = np.stack([rng.uniform(0, OW, m), rng.uniform(0, OH, m),
                          rng.uniform(0.7, 2.6, m), rng.uniform(28, 105, m)], 1)

    sunfall = None
    proc = _writer(out)
    for i in range(n):
        p = i/max(1, n-1); e = ease(p); t = i/FPS
        f = img.astype(np.float32)

        if preset == "underwater":
            f += caustics(f.shape[:2], t, 8.0)[..., None] * np.array([1.25, 1.05, 0.55])
        if preset == "sunset":
            if sunfall is None:
                g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, _, _, loc = cv2.minMaxLoc(cv2.GaussianBlur(g, (0,0), 21))
                yy2, xx2 = grid(f.shape[:2])
                r = np.sqrt((xx2-loc[0])**2 + (yy2-loc[1])**2)
                sunfall = np.exp(-(r/(f.shape[0]*0.30))**2)
            puls = 0.5 + 0.5*np.sin(t*1.5)
            f += (sunfall*(16 + 12*puls))[..., None] * np.array([0.35, 0.72, 1.0])
        if parts is not None:
            for px, py, pr, sp in parts:
                y = int((py - t*sp) % f.shape[0]); x = int((px + np.sin(t*0.8+py)*7) % f.shape[1])
                cv2.circle(f, (x, y), int(pr), (235, 245, 250), -1, cv2.LINE_AA)

        # PARALLAX: near pixels get a bigger push than far pixels
        z = 1.0 + zoom*e
        near, far = z, 1.0 + zoom*e*0.45
        mapx = np.empty(f.shape[:2], np.float32); mapy = np.empty(f.shape[:2], np.float32)
        yy, xx = np.mgrid[0:f.shape[0], 0:f.shape[1]].astype(np.float32)
        zz = far + (near-far)*d
        ccx, ccy = f.shape[1]/2, f.shape[0]/2
        th = np.deg2rad(hr[i])
        dx = (xx-ccx)/zz; dy = (yy-ccy)/zz
        RIP = {"underwater": (7.0, 1.0), "sunset": (2.6, 0.45), "generic": (3.4, 0.7)}
        ramp, rrate = RIP[preset]
        rdx, rdy = ripple(f.shape[:2], t, ramp, rrate)
        mapx[:] = ccx + dx*np.cos(th) - dy*np.sin(th) + hx[i] + rdx
        mapy[:] = ccy + dx*np.sin(th) + dy*np.cos(th) + hy[i] + rdy
        warped = cv2.remap(f, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

        y0 = (warped.shape[0]-H)//2; x0 = (warped.shape[1]-W)//2
        fr = warped[y0:y0+H, x0:x0+W]
        fr += rng.normal(0, 2.6, fr.shape)          # grain
        proc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    proc.stdin.close(); proc.wait()
    if not quiet: print(f"  animated {os.path.basename(src)} -> {os.path.basename(out)} "
                        f"({n} frames, preset={preset})")
    return out

def measure(path, cap_frames=70):
    """Mean optical flow. Generated video measures ~1.5-2.0; the old Ken Burns stills
    measured ~0.65 and pacing.py flagged them as dead zones."""
    c = cv2.VideoCapture(path); prev = None; vals = []
    while len(vals) < cap_frames:
        ok, fr = c.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), (160, 284))
        if prev is not None:
            fl = cv2.calcOpticalFlowFarneback(prev, g, None, .5,3,15,3,5,1.2,0)
            vals.append(float(np.linalg.norm(fl, axis=2).mean()))
        prev = g
    c.release()
    return float(np.mean(vals)) if vals else 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--dur", type=float, default=2.4)
    ap.add_argument("--preset", default="generic", choices=["underwater","sunset","generic"])
    ap.add_argument("--zoom", type=float, default=0.20)
    ap.add_argument("--measure", action="store_true")
    a = ap.parse_args()
    animate(a.src, a.out, a.dur, a.preset, a.zoom)
    if a.measure:
        print(f"  motion {measure(a.out):.3f}   (Ken Burns still ~0.65, real video 1.5-2.0)")

if __name__ == "__main__":
    main()


# ==================================================================== video paths
def enliven(src, out, dur=None, preset="sunset", zoom=0.10, crop=None, seed=5, quiet=False):
    """Add life to a STATIC VIDEO clip. Measured: KK_08_sunset_hero.mp4 scores 0.149 mean
    optical flow - the generated sunset is nearly frozen, and it occupies the last third of
    the video. His note: "just shows a sunset and the sea waves, not attractive enough...
    stale and boring". This applies a slow eased push, a gentle ripple and grain to real
    frames, and can reframe (crop) so ONE clip yields several distinct shots.

    crop = (scale, cx, cy) with scale 1.0 = full frame, 2.0 = 2x tighter, cx/cy in 0..1.
    """
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or FPS
    frames = []
    want = int((dur or 1e9) * fps)
    while len(frames) < want:
        ok, fr = cap.read()
        if not ok: break
        frames.append(fr)
    cap.release()
    if not frames:
        raise SystemExit(f"no frames read from {src}")
    n = len(frames)
    rng = np.random.default_rng(seed)
    hx = np.cumsum(rng.normal(0, .8, n)); hy = np.cumsum(rng.normal(0, .8, n))
    k = max(3, n//5); sm = lambda v: np.convolve(v, np.ones(k)/k, mode="same")
    hx, hy = sm(hx)*1.6, sm(hy)*1.6
    sunfall = None

    proc = _writer(out)
    for i, fr in enumerate(frames):
        p = i/max(1, n-1); e = ease(p); t = i/fps
        f = fr.astype(np.float32)
        h, w = f.shape[:2]
        # reframe first, so a tighter shot really is a different shot
        if crop:
            cs, ccx, ccy = crop
            cw, ch = int(w/cs), int(h/cs)
            x0 = int(np.clip(ccx*w - cw/2, 0, w-cw)); y0 = int(np.clip(ccy*h - ch/2, 0, h-ch))
            f = f[y0:y0+ch, x0:x0+cw]
            h, w = f.shape[:2]
        z = 1.0 + zoom*e
        yy, xx = grid((h, w))
        ccx2, ccy2 = w/2, h/2
        ramp, rrate = {"underwater": (5.0, 1.0), "sunset": (2.2, 0.4),
                       "generic": (2.8, 0.6)}[preset]
        rdx, rdy = ripple((h, w), t, ramp, rrate)
        mapx = ccx2 + (xx-ccx2)/z + hx[i] + rdx
        mapy = ccy2 + (yy-ccy2)/z + hy[i] + rdy
        f = cv2.remap(f, mapx.astype(np.float32), mapy.astype(np.float32),
                      cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if preset == "sunset":
            if sunfall is None or sunfall.shape != f.shape[:2]:
                g = cv2.cvtColor(np.clip(f,0,255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
                _, _, _, loc = cv2.minMaxLoc(cv2.GaussianBlur(g, (0,0), 21))
                yy2, xx2 = grid(f.shape[:2])
                sunfall = np.exp(-(np.sqrt((xx2-loc[0])**2+(yy2-loc[1])**2)/(h*0.26))**2)
            puls = 0.5 + 0.5*np.sin(t*1.6)
            f += (sunfall*(10 + 9*puls))[..., None] * np.array([0.3,0.7,1.0])
        f = cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4)
        f += rng.normal(0, 2.2, f.shape)
        proc.stdin.write(np.clip(f,0,255).astype(np.uint8).tobytes())
    proc.stdin.close(); proc.wait()
    if not quiet:
        print(f"  enlivened {os.path.basename(src)} -> {os.path.basename(out)}"
              + (f"  crop x{crop[0]:.2f}" if crop else ""))
    return out
