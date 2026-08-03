#!/usr/bin/env python3
"""
FX — transitions that actually do something. Replaces the ones that didn't.

WHY THIS REPLACES transitions.py
  Reviewed frame-by-frame across the seam for the first time (18 consecutive frames, not
  3 stills). Findings:

      whip      read as a DEFOCUS, not a pan. boxblur is isotropic and there was almost
                no frame translation. Wrong mechanism.
      mask      produced NO visible mask. It was a straight cut.
      zoomblur  produced no visible zoom blur. Also a straight cut.

  Two of three did nothing. Wiring them into the Crown build would not have fixed his
  complaint, because there was nothing to wire.

THE PRIMITIVES THAT WORK (verified present in this ffmpeg)
  xfade   circlecrop circleopen radial wipeleft wiperight slideleft slideright
          hlslice vuslice smoothleft diagtl pixelize squeezeh
          -> this is the correct backbone for MASKING transitions
  gblur   sigma=N:sigmaV=0  -> TRUE horizontal-only blur. This is what a whip needs;
          boxblur cannot do it.
  setpts  -> speed ramps
  crop    with time-varying size -> dolly in / dolly out

  Researched car-edit vocabulary (work/knowledge.json): fast cut, cut-to-beat, masking,
  dolly in/out, speed ramp. Every one of those now exists here.

CONVENTION
  Each function joins A and B. xfade OVERLAPS, so output = durA + durB - d.
  Callers measure the real duration afterwards; nothing assumes.
"""
import os, subprocess

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def dur(p):
    _, o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"')
    try: return float(o.strip().splitlines()[0])
    except Exception: return 0.0

def _norm(src, out, W, H, fps):
    """xfade demands identical geometry, rate and pixel format on both inputs."""
    sh(f'ffmpeg -y -v error -i "{src}" -vf "scale={W}:{H}:force_original_aspect_ratio=increase,'
       f'crop={W}:{H},fps={fps},setsar=1,format=yuv420p" -an -c:v libx264 -crf 18 '
       f'-preset veryfast "{out}"')
    return out

def _xfade(a, b, out, mode, d, W, H, fps, pre_a=None, pre_b=None):
    """Shared spine. pre_a / pre_b inject per-transition processing (blur, scale, speed)."""
    tmp = out + ".n"
    na, nb = _norm(a, tmp+"a.mp4", W, H, fps), _norm(b, tmp+"b.mp4", W, H, fps)
    da = dur(na)
    off = max(0.0, da - d)
    fa = f"[0:v]{pre_a}[va];" if pre_a else "[0:v]null[va];"
    fb = f"[1:v]{pre_b}[vb];" if pre_b else "[1:v]null[vb];"
    f = f"{fa}{fb}[va][vb]xfade=transition={mode}:duration={d}:offset={off},format=yuv420p[v]"
    rc, err = sh(f'ffmpeg -y -v error -i "{na}" -i "{nb}" -filter_complex "{f}" -map "[v]" '
                 f'-c:v libx264 -crf 19 -preset veryfast -pix_fmt yuv420p "{out}"')
    for t in (na, nb):
        try: os.remove(t)
        except OSError: pass
    if rc != 0:
        raise RuntimeError(err.strip()[:160])
    _assert_not_dead(out, mode)
    return out

def _assert_not_dead(path, mode):
    """A transition that renders SOLID GREEN passed every previous check: rc=0, file exists,
    duration correct. Only looking at pixels caught it. So look at pixels, always."""
    rc, o = sh(f'ffmpeg -v error -ss 0.3 -i "{path}" -frames:v 1 -f rawvideo '
               f'-pix_fmt rgb24 -s 8x8 - 2>/dev/null | xxd -p -l 192')
    hexs = o.strip().replace("\n", "")
    if len(hexs) < 96:
        raise RuntimeError(f"{mode}: no readable frame")
    px = [int(hexs[i:i+2], 16) for i in range(0, min(len(hexs), 192), 2)]
    r = sum(px[0::3])/max(1, len(px[0::3])); g = sum(px[1::3])/max(1, len(px[1::3]))
    b = sum(px[2::3])/max(1, len(px[2::3]))
    if g > 100 and r < 25 and b < 25:
        raise RuntimeError(f"{mode}: rendered SOLID GREEN (dead frames) - filter chain invalid")

# ---------------------------------------------------------------- motion
def whip(a, b, out, d=0.22, direction="left", W=720, H=1280, fps=30):
    """A real whip pan: HORIZONTAL-only blur that ramps up on the outgoing shot and decays
    on the incoming one, plus a hard directional slide. gblur sigmaV=0 is the key - it
    smears along one axis only, which is what a fast pan physically does."""
    mode = "slideleft" if direction == "left" else "slideright"
    # constant sigma: gblur takes a number, not an expression. The xfade slide supplies the
    # movement, the horizontal-only blur supplies the smear. Together they read as a whip.
    # gblur with sigmaV=0 EXACTLY renders solid green in this ffmpeg (verified: whole file
    # green at every timestamp, while gblur alone on a testsrc was fine). avgblur with
    # sizeY=0 is the correct primitive for a horizontal-only smear - cheaper too.
    #
    # THE BUG THIS FIXES (measured 2026-07-31, S450_15S_v1)
    #   pre_a / pre_b are injected as [0:v]<filter> - they apply to the WHOLE clip, not to
    #   the seam. xfade's `duration` governs the blend only; it does not gate the pre-filter.
    #   So a 0.40s whip joining a 0.40s shot to a 2.00s shot smeared all 2.40s. Measured on
    #   sharp inputs (Laplacian median 407 and 503) the output came back at median 2.6 with
    #   80% of frames under the blank-frame threshold. `dip` on the same pair: median 456.
    #   In S450_15S_v1 that is 2.4s of 10.1s - 24% of the runtime - permanently unreadable.
    #   _assert_not_dead did not catch it: it only tests for solid green.
    #
    # THE FIX: gate the blur to the seam with avgblur's timeline `enable`, in three steps so
    # it ramps up through the tail of A and decays through the head of B - which is what the
    # docstring above always claimed and never did. Commas inside enable= must be escaped.
    da = dur(a)
    step = d / 3.0
    t0 = max(0.0, da - d)
    def _g(size, lo, hi):
        return f"avgblur=sizeX={size}:sizeY=0:enable='between(t\\,{lo:.4f}\\,{hi:.4f})'"
    pre_a = ",".join([_g(16, t0, t0 + step),
                      _g(32, t0 + step, t0 + 2 * step),
                      _g(56, t0 + 2 * step, da + 1.0)])
    pre_b = ",".join([_g(56, 0.0, step),
                      _g(32, step, 2 * step),
                      _g(16, 2 * step, d)])
    return _xfade(a, b, out, mode, d, W, H, fps, pre_a=pre_a, pre_b=pre_b)

def speedramp(a, b, out, d=0.30, W=720, H=1280, fps=30, factor=0.62):
    """Slow-then-snap. The tail of A accelerates into the cut - the most common car-edit
    move after the beat cut itself.

    setpts inline fought xfade's timebase check ("First input link main timebase 1/10..."),
    so the sped-up copy is RENDERED FIRST and fed in as a clean input. Pre-rendering beats
    arguing with a filtergraph."""
    tmp = out + ".fast.mp4"
    sh(f'ffmpeg -y -v error -i "{a}" -vf "setpts={factor}*PTS,fps={fps},'
       f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1" '
       f'-an -c:v libx264 -crf 18 -preset veryfast "{tmp}"')
    try:
        r = _xfade(tmp, b, out, "smoothleft", d, W, H, fps)
    finally:
        try: os.remove(tmp)
        except OSError: pass
    return r

def zoomblur(a, b, out, d=0.20, W=720, H=1280, fps=30):
    """Punch in on A while blurring, then reveal B. Radial-ish: scale up + blur both axes."""
    z = f"scale=iw*1.28:-1,crop={W}:{H},avgblur=sizeX=16:sizeY=16"
    return _xfade(a, b, out, "radial", d, W, H, fps, pre_a=z)

# ---------------------------------------------------------------- masking
def mask_circle(a, b, out, d=0.35, W=720, H=1280, fps=30):
    return _xfade(a, b, out, "circleopen", d, W, H, fps)

def mask_crop(a, b, out, d=0.35, W=720, H=1280, fps=30):
    return _xfade(a, b, out, "circlecrop", d, W, H, fps)

def mask_wipe(a, b, out, d=0.30, direction="left", W=720, H=1280, fps=30):
    return _xfade(a, b, out, "wipeleft" if direction == "left" else "wiperight",
                  d, W, H, fps)

def mask_slice(a, b, out, d=0.30, W=720, H=1280, fps=30):
    """Horizontal slices march across. Very CapCut, reads as deliberate design."""
    return _xfade(a, b, out, "hlslice", d, W, H, fps)

def mask_radial(a, b, out, d=0.35, W=720, H=1280, fps=30):
    return _xfade(a, b, out, "radial", d, W, H, fps)

# ---------------------------------------------------------------- camera
def dolly_in(a, b, out, d=0.30, W=720, H=1280, fps=30):
    """Push the outgoing shot into the cut. crop with a time-varying window - never
    zoompan, which multiplies frames on a video input and hangs."""
    push = (f"crop=w='iw/(1+0.30*min(t,1))':h='ih/(1+0.30*min(t,1))':"
            f"x='(iw-ow)/2':y='(ih-oh)/2',scale={W}:{H}")
    return _xfade(a, b, out, "smoothleft", d, W, H, fps, pre_a=push)

def dolly_out(a, b, out, d=0.30, W=720, H=1280, fps=30):
    pull = (f"crop=w='iw/(1.30-0.30*min(t,1))':h='ih/(1.30-0.30*min(t,1))':"
            f"x='(iw-ow)/2':y='(ih-oh)/2',scale={W}:{H}")
    return _xfade(a, b, out, "smoothleft", d, W, H, fps, pre_a=pull)

def glitch(a, b, out, d=0.18, W=720, H=1280, fps=30):
    return _xfade(a, b, out, "pixelize", d, W, H, fps)

def flash(a, b, out, d=0.12, W=720, H=1280, fps=30):
    return _xfade(a, b, out, "fadewhite", d, W, H, fps)

def dip(a, b, out, d=0.20, W=720, H=1280, fps=30):
    return _xfade(a, b, out, "fadeblack", d, W, H, fps)

FX = {
    "whip": whip, "speedramp": speedramp, "zoomblur": zoomblur,
    "mask_circle": mask_circle, "mask_crop": mask_crop, "mask_wipe": mask_wipe,
    "mask_slice": mask_slice, "mask_radial": mask_radial,
    "dolly_in": dolly_in, "dolly_out": dolly_out,
    "glitch": glitch, "flash": flash, "dip": dip,
}

# what a car edit actually reaches for, in rough order of frequency
CAR_EDIT_SET = ["whip", "speedramp", "mask_slice", "dolly_in", "mask_circle", "zoomblur"]

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("a"); ap.add_argument("b"); ap.add_argument("--outdir", default="/tmp/fx")
    ap.add_argument("--only")
    x = ap.parse_args()
    os.makedirs(x.outdir, exist_ok=True)
    names = [x.only] if x.only else list(FX)
    for n in names:
        o = os.path.join(x.outdir, f"fx_{n}.mp4")
        try:
            FX[n](x.a, x.b, o)
            print(f"  {n:12s} {dur(o):.2f}s")
        except Exception as e:
            print(f"  {n:12s} FAIL {str(e)[:70]}")
