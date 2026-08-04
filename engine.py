#!/usr/bin/env python3
"""
ENGINE — build any music-led cut from any plan. One file, no per-car copies.

WHY THIS EXISTS
  `projects/lc300/legacy/build.py` is 530 lines and every line of it is specific to one video:
  the source filenames, the shot map, the caption text, the output path. Building the
  Supra the same way meant copying it and changing eleven things, which is how two and a
  half cars produced seven scripts.

  Everything that varies lives in `plans/<name>.py` as DATA. Everything that is TRUE OF
  EVERY CUT lives here as code — and every one of those truths was paid for:

    music defines the grid          measure PHASE, not just tempo (163ms offset)
    cut on an action peak           clipsense returned them; nothing read them
    match exposure BEFORE blending  matching after only sees merged segments
    frame-exact cuts                -t drifts +34ms/shot on a 24fps source
    never double-grade              7.7% -> 40.0% of pixels crushed
    SFX leads the cut               a whoosh RESOLVES on the cut
    the bed ducks under the SFX     otherwise it is mixed to inaudible
    captions in the lower third     the subject is always centre
    write atomically                a killed run left a file with no moov atom
    declare ACTUAL post-blend cuts  blending moves every boundary after it

USAGE
  python3 talyx.py build lc300
  python3 engine.py lc300 [--out FILE] [--no-cache]
"""
import os, sys, json, argparse, subprocess, importlib
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "tools")
sys.path.insert(0, HERE)
sys.path.insert(0, TOOLS)


def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def dur(p):
    _, o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"')
    try:
        return float(o.strip().splitlines()[0])
    except Exception:
        return 0.0


def load_plan(name):
    for cand in (f"plans.{name}", name, f"{name}_plan"):
        try:
            return importlib.import_module(cand)
        except ModuleNotFoundError:
            pass
    return None


def find_bed(P, pdir):
    """Bed first: music defines the grid, not the picture."""
    import glob
    for pat in (os.path.join(pdir, "audio", "*.wav"),
                os.path.join(HERE, "assets", "bgm", f"*{int(P.BPM)}*.wav"),
                os.path.join(TOOLS, "BGM_phonk_*.wav", "*.wav"),
                os.path.join(HERE, "assets", "bgm", "**", "*.wav")):
        c = [f for f in glob.glob(pat, recursive=True) if "sfx" not in os.path.basename(f).lower()]
        if c:
            return sorted(c, key=os.path.getsize, reverse=True)[0]
    return None


def find_clip(P, pdir, key):
    import glob
    named = getattr(P, "CLIPS", {}).get(key)
    if named:
        p = os.path.join(pdir, "clips", named)
        if os.path.exists(p):
            return p
    c = glob.glob(os.path.join(pdir, "clips", f"*_{key}_*.mp4"))
    return c[0] if c else None


# ---------------------------------------------------------------- exposure
def _level(p):
    import cv2, numpy as np
    c = cv2.VideoCapture(p); v = []
    while True:
        ok, f = c.read()
        if not ok:
            break
        v.append(cv2.cvtColor(cv2.resize(f, (96, 171)), cv2.COLOR_BGR2GRAY).mean())
    c.release()
    return float(np.mean(v)) if v else None


def shot_match(segs, W, H, FPS, tmp, tol=10.0, max_gain=0.14):
    # clamp 0.10 -> 0.14 (2026-08-04): WRX v1 measured 4/15 cuts swinging >18, worst 32.
    # 32/255*1.9 = 0.24 needed; 0.14 halves the worst swing without relighting.
    """Pull each RENDERED segment toward the running level. Never the source clip: a
    1.90x punch crops into the dark part of frame, so source B averages 73.7 while its
    punch renders at 50. The source average is the wrong statistic.

    The gain is a LEVEL DIFFERENCE scaled into ffmpeg's brightness units
    (d/255 * 1.9), clamped to +/-0.085 so it matches rather than relights.
    A ratio-based approximation was tried instead and under-corrected badly:
    it left one cut swinging 22 where this leaves zero.
    """
    import numpy as np
    lv = [_level(s) for s in segs]
    if any(x is None for x in lv):
        print("  !! could not measure a segment - SKIPPING shot match")
        return segs
    target = float(np.median(lv))
    out, fixed = [], 0
    for i, (p, l) in enumerate(zip(segs, lv)):
        d = target - l
        if abs(d) <= tol:
            out.append(p); continue
        gain = max(-max_gain, min(max_gain, d / 255.0 * 1.9))
        o = p.replace(".mp4", "_m.mp4")
        spec, sf = f"{gain:.4f}", o + ".spec"
        if os.path.exists(o) and os.path.exists(sf) and open(sf).read() == spec:
            out.append(o); fixed += 1; continue
        rc, err = sh(f'ffmpeg -y -v error -i "{p}" -vf "eq=brightness={gain:.4f},setsar=1" '
                     f'-an -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p "{o}"')
        if rc != 0 or not os.path.exists(o):
            print(f"  !! shot {i} match FAILED - keeping unmatched: {err.strip()[:60]}")
            out.append(p); continue
        open(sf, "w").write(spec)
        out.append(o); fixed += 1
    print(f"  target level {target:.1f} - {fixed}/{len(segs)} shots matched "
          f"(tol {tol}, clamp {max_gain:+.3f})")
    return out


def adjacent_check(segs, thresh=0.95):
    """HISTOGRAM CORRELATION, not pixel difference. A punch-in moves every pixel while
    showing nothing new — mean |diff| flagged 0 of 13 cuts; hist-corr flagged 7."""
    import cv2, numpy as np
    last, bad = None, 0
    for i, s in enumerate(segs):
        cap = cv2.VideoCapture(s); ok, f = cap.read(); cap.release()
        if not ok:
            continue
        g = cv2.cvtColor(cv2.resize(f, (96, 171)), cv2.COLOR_BGR2GRAY)
        h = cv2.calcHist([g], [0], None, [64], [0, 256]); cv2.normalize(h, h)
        if last is not None:
            c = float(cv2.compareHist(last, h, cv2.HISTCMP_CORREL))
            if c > thresh:
                bad += 1
                print(f"  !! shot {i} barely changes the image (hist-corr {c:.3f})")
        last = h
    print(f"  {bad}/{max(1,len(segs)-1)} adjacent pairs show no new information")
    return bad


# ---------------------------------------------------------------- build
def build(name, out_path=None, use_cache=True):
    P = load_plan(name)
    if not P:
        print(f"!! no plan: plans/{name}.py"); return 1
    pdir = os.path.join(HERE, "projects", name)
    tmp = os.path.join(pdir, "tmp")
    for d in ("clips", "output", "audio", "analysis", "tmp"):
        os.makedirs(os.path.join(pdir, d), exist_ok=True)

    W, H, FPS = P.W, P.H, P.FPS
    tl, TOTAL = P.timeline()
    print("=" * 66); print(f"ENGINE  {P.PROJECT}"); print("=" * 66)

    # ---- inputs ----
    clips = {k: find_clip(P, pdir, k) for k in P.SOURCES}
    miss = [k for k, v in clips.items() if not v]
    if miss:
        print(f"!! MISSING CLIPS for sources {miss} in projects/{name}/clips/")
        print(f"   have: {sorted(os.path.basename(f) for f in __import__('glob').glob(os.path.join(pdir,'clips','*.mp4')))}")
        return 1
    BED = find_bed(P, pdir)
    if not BED:
        print(f"!! no music bed. Run: python3 tools/phonk.py --bpm {P.BPM:.0f} --dur {TOTAL:.0f}")
        return 1
    print(f"  bed: {os.path.relpath(BED, HERE)}")

    import clipsense, fx, rhythm

    # ---- 1 PHASE, not just tempo ----
    BED_TRIM = 0.0        # per-segment level compensation, set by the segment scan
    try:
        import math
        _x = rhythm.pcm(BED); _f, _t = rhythm.stft_flux(_x)
        _on = rhythm.pick_onsets(_f, _t)
        BED_OFFSET = float(_on[0]) if len(_on) else 0.0
        # PHASE UPGRADE (2026-08-04, real-bed lesson): the first transient is not
        # necessarily ON the beat grid - a swung phonk intro starts off-grid and
        # every cut inherits the error (measured: 69% on-grid trimming to first
        # onset). Fit the grid phase over ALL onsets instead, then trim at the
        # grid line nearest the first transient so the drop still opens the video.
        if len(_on) > 4:
            import numpy as _np
            _dur = len(_f) * _t / rhythm.SR
            _sc, _off = rhythm._fit_grid(P.BEAT, _np.array(_on), _dur, tol=0.035)
            k = round((BED_OFFSET - _off) / P.BEAT)
            cand = _off + k * P.BEAT
            if cand >= -1e-3:
                BED_OFFSET = max(0.0, float(cand))
            # SEGMENT SCAN (2026-08-04, his ear: "silent 1-2s, track keeps
            # switching"). A real track has an ARRANGEMENT - intro, drop,
            # breakdown - and starting at the head dropped Skrrt Slide's
            # breakdown into the middle of the video (measured: 1.4s of
            # beat-gone at 6.6-8.0s). Scan beat-aligned start offsets and keep
            # the one whose WEAKEST 0.8s of bed energy is strongest - the
            # video rides the most continuous stretch the track has.
            bed_dur = len(_x) / rhythm.SR
            if bed_dur > TOTAL + 2 * P.BEAT:
                hopw = int(0.2 * rhythm.SR)
                env = _np.array([20 * _np.log10(float(_np.sqrt(_np.mean(
                    _x[i:i + hopw] ** 2))) + 1e-9)
                    for i in range(0, len(_x) - hopw, hopw)])
                best = (-1e9, BED_OFFSET)
                off = BED_OFFSET
                while off + TOTAL + 0.2 <= bed_dur:
                    a, b = int(off / 0.2), int((off + TOTAL) / 0.2)
                    win = env[a:b]
                    if len(win) >= 4:
                        roll = _np.convolve(win, _np.ones(4) / 4, "valid")
                        score = float(roll.min())
                        if score > best[0] + 1e-9:
                            best = (score, off)
                    off += 2 * P.BEAT          # 2-beat steps keep the phase
                head = env[int(BED_OFFSET / 0.2):int((BED_OFFSET + TOTAL) / 0.2)]
                if best[1] != BED_OFFSET:
                    print(f"      bed segment: start {best[1]:.2f}s (weakest 0.8s "
                          f"{best[0]:.1f}dB vs {head.min():.1f}dB at the head)")
                # LEVEL COMPENSATION: the mix gains were calibrated at one segment
                # level; a hotter segment re-broke true-peak (+0.8 measured).
                # Gain rides the segment's mean level so the bed hits the mix at
                # a CONSTANT level whichever segment wins. Reference = -15.7dB
                # mean (the calibration segment of bed_skrrt_slide_150).
                seg = env[int(best[1] / 0.2):int((best[1] + TOTAL) / 0.2)]
                if len(seg):
                    BED_TRIM = max(-6.0, min(6.0, -15.7 - float(seg.mean())))
                BED_OFFSET = best[1]
    except Exception as e:
        BED_OFFSET = 0.0
        print(f"  !! could not measure bed phase ({str(e)[:40]}) — assuming 0. "
              f"Cuts may sit off the hits.")
    print(f"\n[1/7] phase   first transient at {BED_OFFSET*1000:.0f}ms -> bed trimmed to it")
    print(f"      grid    {len(P.SHOTS)} shots @ {P.BPM:.0f} BPM, beat {P.BEAT*1000:.0f}ms, "
          f"{TOTAL:.2f}s")

    # ---- 2 segments, cut on action ----
    print(f"\n[2/7] segments  NON-OVERLAPPING windows centred on action peaks, frame-exact")
    sense = {k: clipsense.analyse(v) for k, v in clips.items()}
    xy = getattr(P, "CROP_XY", {})

    # WINDOW ALLOCATOR (2026-08-04, after Gavril caught duplicates BY EYE that every
    # gate missed): the old picker deduped PEAKS, not WINDOWS — a hold consumed the
    # whole clip head and a later burst from the same source landed INSIDE it. Measured
    # on the v1 build: 9 overlapping pairs, three 100% contained (payoff replayed the
    # tease frame-for-frame). Now each source hands out non-overlapping windows, minus
    # BAN_SPANS from the plan and ban_spans from clips/manifest.json (ingest.py — e.g.
    # the softbox in B's head, measured out at 2.0s). A source that cannot fit its
    # shots FAILS THE BUILD LOUDLY: that is a plan overcommit (planqc 21 catches it
    # pre-spend), never something to paper over with a repeat.
    bans = {k: [tuple(b) for b in (getattr(P, "BAN_SPANS", {}) or {}).get(k, [])]
            for k in clips}
    mpath = os.path.join(pdir, "clips", "manifest.json")
    if os.path.exists(mpath):
        try:
            mf = json.load(open(mpath))
            for k in clips:
                for sp in mf.get(k, {}).get("ban_spans", []):
                    if tuple(sp) not in bans[k]:
                        bans[k].append(tuple(sp))
        except Exception as e:
            print(f"  !! manifest.json unreadable ({str(e)[:40]}) — plan bans only")

    def _sub(free, a, b):
        out = []
        for lo, hi in free:
            if b <= lo or a >= hi:
                out.append((lo, hi)); continue
            if a - lo > 0.05:
                out.append((lo, a))
            if hi - b > 0.05:
                out.append((b, hi))
        return out

    by_src = {}
    for i, ((key, _c2, _kind2, _n2), (_s2, d2, _k2)) in enumerate(zip(P.SHOTS, tl)):
        by_src.setdefault(key, []).append((i, d2))
    shot_tin, alloc_fail = {}, []
    for key, shots_of in by_src.items():
        c = sense[key]
        free = [(0.0, max(0.1, c["duration"] - 0.05))]
        for a_, b_ in bans[key]:
            free = _sub(free, a_, b_)
        mc = c.get("motion_curve") or []
        cfps = c.get("fps", 24.0)

        def _mot(ts):
            if not mc:
                return None
            return mc[min(len(mc) - 1, max(0, int(ts * cfps / 2)))]

        for i, d_ in sorted(shots_of, key=lambda s: (-s[1], s[0])):   # longest first
            cands = []
            for pk in c["action_peaks_s"]:
                for lo, hi in free:
                    if not (lo <= pk <= hi) or hi - lo < d_:
                        continue
                    tin_ = min(max(pk - d_ * 0.42, lo), hi - d_)
                    if tin_ <= pk <= tin_ + d_:
                        # ACTION RESOLUTION (2026-08-04, his catch: "clips cut
                        # off way too early"). A window that ends while motion
                        # is still >=80% of its peak cuts MID-action; prefer
                        # windows whose end is past the action, then nearest
                        # the clip's best moment.
                        mp, me = _mot(pk), _mot(tin_ + d_)
                        unresolved = 1 if (mp and me and me > 0.8 * mp) else 0
                        cands.append((unresolved, abs(pk - c["best_in_s"]), tin_))
            if cands:
                tin_ = sorted(cands)[0][2]
            else:
                gaps = sorted(((hi - lo, lo) for lo, hi in free if hi - lo >= d_),
                              reverse=True)
                if not gaps:
                    alloc_fail.append(f"{key}: shot {i} needs {d_:.2f}s, free "
                                      f"{[(round(a_,2),round(b_,2)) for a_,b_ in free]}")
                    continue
                tin_ = gaps[0][1]
                print(f"  !! shot {i} ({key}): window carries NO action peak "
                      f"(free space, not choice)")
            shot_tin[i] = tin_
            free = _sub(free, tin_, tin_ + d_)
    if alloc_fail:
        print("!! SOURCE OVERCOMMITTED — the plan wants more footage than the clip has:")
        for f_ in alloc_fail:
            print(f"   {f_}")
        print("   Fix the PLAN (re-source or shorten a shot). REFUSING to duplicate.")
        return 1

    segs, cuts, t = [], [], 0.0
    for i, ((key, cs, kind, note), (start, d, _k)) in enumerate(zip(P.SHOTS, tl)):
        c = sense[key]
        tin = shot_tin[i]
        cx, cy = xy.get(i, (0.50, 0.50))
        o = os.path.join(tmp, f"c{i:02d}.mp4")
        spec = f"{os.path.basename(clips[key])}|{tin:.3f}|{d:.3f}|{cs}|{cx}|{cy}|frames"
        sf = o + ".spec"
        if (use_cache and os.path.exists(o) and os.path.exists(sf)
                and open(sf).read() == spec and abs(dur(o) - d) < 0.10):
            segs.append(o)
            if i:
                cuts.append(round(t, 3))
            t += d
            continue
        if cs > 1.05:
            vf = (f"crop=iw/{cs}:ih/{cs}:(iw-iw/{cs})*{cx}:(ih-ih/{cs})*{cy},"
                  f"scale={W}:{H},fps={FPS},setsar=1")
        else:
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H},fps={FPS},setsar=1")
        nfr = int(round(d * FPS))          # FRAME-EXACT. -t drifts +34ms/shot at 24fps.
        rc, err = sh(f'ffmpeg -y -v error -ss {tin:.3f} -i "{clips[key]}" -vf "{vf}" '
                     f'-frames:v {nfr} -an -c:v libx264 -crf 18 -preset veryfast '
                     f'-pix_fmt yuv420p "{o}"')
        if rc != 0 or not os.path.exists(o):
            print(f"  !! shot {i} FAILED: {err.strip()[:90]}"); return 1
        got = dur(o)
        if abs(got - d) > 0.10:
            print(f"  !! shot {i} is {got:.2f}s, asked {d:.2f}s — SHORT, not silently kept")
        open(sf, "w").write(spec)
        segs.append(o)
        if i:
            cuts.append(round(t, 3))
        t += d
    print(f"  {len(segs)} shots, {t:.2f}s, {len(cuts)} cuts — all on the grid")

    # ---- 3 exposure BEFORE blends ----
    print(f"\n[3/7] shot match")
    segs = shot_match(segs, W, H, FPS, tmp)

    # ---- 4 blends ----
    print(f"\n[4/7] blends  {P.BLEND_KIND} {P.BLEND_WIDTH*1000:.0f}ms at declared boundaries")
    out, n = list(segs), 0
    blend_ok = []      # successful boundaries — the foley layer needs the ACTUAL timeline
    for i in sorted(set(P.BLEND_AFTER)):
        if i + 1 >= len(out) or out[i] is None or out[i + 1] is None:
            continue
        o = os.path.join(tmp, f"bx{i:02d}.mp4")
        bspec = f"{os.path.basename(out[i])}|{os.path.basename(out[i+1])}|{P.BLEND_KIND}|{P.BLEND_WIDTH}"
        bsf = o + ".spec"
        if use_cache and os.path.exists(o) and os.path.exists(bsf) and open(bsf).read() == bspec:
            out[i] = o; out[i + 1] = None; n += 1; blend_ok.append(i)
            continue
        try:
            fx.FX[P.BLEND_KIND](out[i], out[i + 1], o, d=P.BLEND_WIDTH, W=W, H=H, fps=FPS)
            open(bsf, "w").write(bspec)
            if os.path.exists(o) and dur(o) > 0.3:
                out[i] = o; out[i + 1] = None; n += 1; blend_ok.append(i)
        except Exception as e:
            print(f"  !! {P.BLEND_KIND}@{i}: {str(e)[:70]}")
    segs = [x for x in out if x]
    print(f"  {n} blend(s) = {100*n//max(1,len(P.SHOTS)-1)}%  (profile 6-33%)")

    print(f"\n[5/7] coverage")
    adjacent_check(segs)

    # ---- concat ----
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    cut = os.path.join(tmp, "cut.mp4")
    rc, _ = sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c copy -an "{cut}"')
    if rc != 0 or dur(cut) < 1:
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c:v libx264 -crf 18 '
           f'-preset veryfast -pix_fmt yuv420p -an "{cut}"')

    # ---- 6 grade: saturation only, NEVER double-grade ----
    print(f"\n[6/7] grade  saturation {P.GRADE_SAT}, brightness {P.GRADE_BRI:+.3f} "
          f"(target black {P.TARGET_BLACK} / sat {P.TARGET_SAT})")
    graded = os.path.join(tmp, "graded.mp4")
    rc, _ = sh(f'ffmpeg -y -v error -i "{cut}" -vf '
               f'"eq=saturation={P.GRADE_SAT}:brightness={P.GRADE_BRI},setsar=1" '
               f'-c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -an "{graded}"')
    if rc != 0 or not os.path.exists(graded):
        print("  !! GRADE FAILED — DO NOT POST WITHOUT LOOKING"); graded = cut

    # ---- captions: shot indices -> times, lower third ----
    # QUALITY LADDER (his standing rule: drawtext is the weakest visual element):
    #   1. tools/cards.py 'lower' via Playwright (DESKTOP ONLY - real typography, alpha)
    #   2. ffmpeg drawtext (sandbox fallback) - flagged loudly so it is never mistaken
    #      for the good path.
    cards_png = []
    try:
        import subprocess as _sp
        for ci, (txt, first, ncards, kind) in enumerate(P.CARDS):
            o = os.path.join(tmp, f"card{ci}.png")
            r = _sp.run([sys.executable, os.path.join(TOOLS, "cards.py"), "lower",
                         "--text", txt, "-o", o], capture_output=True, text=True, timeout=30)
            import cv2 as _cv
            im = _cv.imread(o, _cv.IMREAD_UNCHANGED)
            # a usable card is a CHIP with alpha. A full-frame canvas (cards.py's own
            # ffmpeg fallback, 1920x1080) scales into a letterbox and CLIPS long text -
            # measured on WRX v1, which shipped "RU WON'T SELL YOU". Reject portrait/
            # full-frame outputs, not just missing alpha.
            if im is None or im.shape[2] != 4 or im.shape[0] >= im.shape[1] // 2:
                cards_png = []; break
            cards_png.append(o)
    except Exception:
        cards_png = []
    if not cards_png:
        # PIL CHIP RENDERER - the middle rung of the quality ladder (added 2026-08-04
        # after WRX v1): cards.py/Playwright > PIL chip > drawtext. Measured type
        # (textlength), AUTO-FIT so five-word narrative cards can never clip, real
        # alpha, CapCut font from the repo. Runs anywhere Pillow exists.
        try:
            from PIL import Image as _Im, ImageDraw as _Dr, ImageFont as _Ft
            _fd = os.path.join(HERE, "assets", "fonts", "loose")
            _fp = next(os.path.join(_fd, f) for f in
                       ("CapCutSansText-Bold.otf", "NotoSans-Regular.ttf")
                       if os.path.exists(os.path.join(_fd, f)))
            cards_png = []
            for ci, (txt, first, ncards, kind) in enumerate(P.CARDS):
                size = 84
                while size > 34:
                    _f = _Ft.truetype(_fp, size)
                    if _Dr.Draw(_Im.new("RGBA", (8, 8))).textlength(txt, font=_f) <= 980:
                        break
                    size -= 2
                _f = _Ft.truetype(_fp, size)
                _w = int(_Dr.Draw(_Im.new("RGBA", (8, 8))).textlength(txt, font=_f))
                _h = int(size * 2.0)
                _im = _Im.new("RGBA", (1080, _h), (0, 0, 0, 0))
                _d = _Dr.Draw(_im)
                _x, _y = (1080 - _w) // 2, (_h - size) // 2 - size // 6
                _d.text((_x + 3, _y + 4), txt, font=_f, fill=(0, 0, 0, 140))
                _d.text((_x, _y), txt, font=_f, fill=(255, 255, 255, 255),
                        stroke_width=max(3, size // 14), stroke_fill=(0, 0, 0, 220))
                o = os.path.join(tmp, f"card{ci}.png")
                _im.save(o)
                cards_png.append(o)
            print("      cards: PIL chip renderer (auto-fit, CapCut font)")
        except Exception:
            cards_png = []
    if not cards_png:
        print("      cards.py unusable here (Playwright blocked) -> drawtext FALLBACK. "
              "On the DESKTOP this build upgrades itself automatically.")
    FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
    if not os.path.exists(FONT):
        FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    # PLANNED vs ACTUAL, again: blends compress the timeline (16.00s planned -> 14.40s
    # actual on the LC300), so spans from the plan put the CTA PAST THE END OF THE FILE
    # and it never rendered. Caught by LOOKING at the strip, not by any gate. Scale all
    # card times by actual/planned so the last card always lands inside the video.
    vd_now = dur(graded)
    scale = vd_now / TOTAL if TOTAL else 1.0
    spans = []
    for txt, first, ncards, kind in P.CARDS:
        st_ = tl[first][0] * scale
        en = tl[min(first + ncards - 1, len(tl) - 1)]
        spans.append((txt, st_, ((en[0] + en[1]) - tl[first][0]) * scale, kind))
    capped = os.path.join(tmp, "capped.mp4")
    if cards_png:
        # PNG overlay path - same geometry contract as drawtext: centred, y=CARD_Y.
        ins = "".join(f' -i "{c}"' for c in cards_png)
        fc, prev = [], "0:v"
        for i, (txt, st_, ln, kind) in enumerate(spans):
            fc.append(f"[{i+1}:v]scale={W}:-1[c{i}]")
            out = f"v{i}"
            fc.append(f"[{prev}][c{i}]overlay=x=0:y=(H*{P.CARD_Y})-(h/2):"
                      f"enable='between(t,{st_:.2f},{st_+ln:.2f})'[{out}]")
            prev = out
        rc, err = sh(f'ffmpeg -y -v error -i "{graded}"{ins} '
                     f'-filter_complex "{";".join(fc)}" -map "[{prev}]" '
                     f'-c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -an "{capped}"')
        mode = "cards.py overlay"
    else:
        dt = []
        for txt, st_, ln, kind in spans:
            # drawtext ESCAPING (found 2026-08-04): the apostrophe in "WON'T" closed
            # the text quote and ffmpeg read the enable timestamps as filter names.
            # Typographic apostrophe renders correctly AND cannot break the parser.
            txt = txt.replace("'", "’").replace(":", r"\:").replace("%", r"\%")
            # AUTO-FIT (WRX v1 lesson): the old max(56,...) FLOOR guaranteed overflow on
            # long text. Bound ~0.58*size px/char to <=0.92 of frame width, no floor.
            size = min(56 if kind == "cta" else 78, max(30, int(1100 / max(8, len(txt)))))
            dt.append(f"drawtext=fontfile='{FONT}':text='{txt}':fontcolor=white:fontsize={size}:"
                      f"borderw=6:bordercolor=black@0.85:x=(w-text_w)/2:y=(h*{P.CARD_Y}):"
                      f"enable='between(t,{st_:.2f},{st_+ln:.2f})'")
        rc, err = sh(f'ffmpeg -y -v error -i "{graded}" -vf "{",".join(dt)}" '
                     f'-c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -an "{capped}"')
        mode = "drawtext FALLBACK"
    if rc == 0 and os.path.exists(capped) and dur(capped) > 1:
        graded = capped
        print(f"      {len(P.CARDS)} cards at y={P.CARD_Y} (lower third) via {mode}")
        if not P.AI_LABEL_BURNED_IN:
            print(f"      NO burned-in AI label — SET THE PLATFORM TOGGLE AT UPLOAD (human step)")
    else:
        print(f"  !! CAPTIONS FAILED: {err.strip()[:100]} — DO NOT POST, no captions/CTA")

    # ---- 7 sound ----
    vd = dur(graded)
    sfx_path = os.path.join(tmp, "sfx.wav")
    HAVE_SFX = False
    try:
        import sfxgen, numpy as np
        SR = sfxgen.SR
        track = np.zeros(int(vd * SR) + SR)

        def place(x, at, gain):
            a = int(at * SR); b = min(a + len(x), len(track))
            if a >= 0 and b > a:
                track[a:b] += x[:b - a] * gain

        # CONVENTION: IMPACT_AT / SUBDROP_AT are SHOT indices, and the sound lands on the
        # cut ENTERING that shot -> cut index i-1. Stated explicitly because translating
        # the LC300 build put its sub-drops on the hold EXITS instead of the entries,
        # which cost 2.5 dB of transient lift (+4.6 -> +2.1 against a 2.0 floor).
        sec = {cuts[i - 1] for i in P.IMPACT_AT if 0 < i <= len(cuts)}
        hold = {cuts[i - 1] for i in P.SUBDROP_AT if 0 < i <= len(cuts)}
        nw = ni = 0
        for c in cuts:
            if c in sec:
                place(sfxgen.impact(0.7), c - 0.02, 0.55); ni += 1
            elif c in hold:
                place(sfxgen.sub_drop(1.4), c - 0.05, 0.42); ni += 1
            else:
                # whoosh 0.34 -> 0.15 (2026-08-04, his ear v5+v6: the noise sweep
                # dominates the CUT MOMENT because the sidechain ducks the bed at
                # exactly that instant - average level comparisons miss this.
                # Impacts/sub-drops keep full weight; only the sand gets cut.)
                place(sfxgen.whoosh(0.30, up=True), max(0.0, c - P.SFX_LEAD), 0.15); nw += 1
        # SAFETY ONLY, never normalize UP (2026-08-04): dividing by the peak
        # BOOSTED the impacts +2.3dB the moment the whooshes got quieter —
        # the placement gains ARE the design; the peak scale only protects.
        pk = float(np.max(np.abs(track))) or 1.0
        sfxgen._w(sfx_path, track * min(1.0, 0.72 / pk))
        HAVE_SFX = os.path.exists(sfx_path)
        print(f"\n[7/7] sfx    {nw} whoosh + {ni} impact/drop, leading each cut by "
              f"{P.SFX_LEAD*1000:.0f}ms")
    except Exception as e:
        print(f"\n[7/7] !! SFX FAILED: {str(e)[:80]} — cuts have NO transient design")

    # ---- 7b DIEGETIC / FOLEY (added 2026-08-04, Gavril's catch) ----
    # Whoosh/impact on cuts is EDIT sound, not foley. In a sound-led genre the launch
    # had no engine, the rolling shot no spray, the cockpit no boxer idle. The clips
    # were generated WITH audio (probe A measured -12.8 LUFS of real engine/spray) and
    # the obsolete "silent" rule stripped it all with -an. 0 credits to fix: extract
    # each shot's audio from its OWN clip window (same trim as the video) and lay it
    # on the ACTUAL post-blend timeline. The plan decides the mix: FOLEY={shot: gain_db}
    # (foreground on EVENT/PAYOFF, low under HUMAN/stills) + SOUND{hero, duck_shots,
    # silence}. planqc check 19 blocks a car_cinematic plan that never decided.
    FOLEY = getattr(P, "FOLEY", {}) or {}
    SOUND = getattr(P, "SOUND", {}) or {}
    foley_path = os.path.join(tmp, "foley.wav")
    HAVE_FOLEY = False
    fg_spans = []          # video-time spans where foley is FOREGROUND (>= -6dB)
    # each successful blend pulls every LATER shot forward by BLEND_WIDTH
    # (measured: 3 x 0.4s took 21.6s -> 20.4s). Place foley on the shifted grid.
    shift = [P.BLEND_WIDTH * sum(1 for b in blend_ok if b < j) for j in range(len(P.SHOTS))]
    if FOLEY:
        try:
            import numpy as np, wave
            SRF = 44100
            ftr = np.zeros(int(vd * SRF) + SRF)
            n_laid = 0
            for i, ((key, _cs, _kind, _note), (start, d, _k)) in enumerate(zip(P.SHOTS, tl)):
                if i not in FOLEY or shot_tin.get(i) is None:
                    continue
                aw = os.path.join(tmp, f"a{i:02d}.wav")
                rc2, _ = sh(f'ffmpeg -y -v error -ss {shot_tin[i]:.3f} -i "{clips[key]}" '
                            f'-t {d:.3f} -vn -ac 1 -ar {SRF} -c:a pcm_s16le "{aw}"')
                if rc2 != 0 or not os.path.exists(aw) or os.path.getsize(aw) < 1000:
                    continue        # a clip with no audio stream is skipped, not fatal
                wv = wave.open(aw)
                x = np.frombuffer(wv.readframes(wv.getnframes()),
                                  dtype=np.int16).astype(float) / 32768.0
                wv.close()
                if not len(x):
                    continue
                e = int(0.015 * SRF)        # 15ms edge fades — no clicks at the cuts
                if len(x) > 2 * e:
                    x = x.copy()
                    x[:e] *= np.linspace(0, 1, e)
                    x[-e:] *= np.linspace(1, 0, e)
                at = int(max(0.0, start - shift[i]) * SRF)
                b = min(at + len(x), len(ftr))
                if b > at:
                    ftr[at:b] += x[:b - at] * (10.0 ** (FOLEY[i] / 20.0))
                    n_laid += 1
                    if FOLEY[i] >= -6.0:
                        fg_spans.append((at / SRF, b / SRF))
            # SFX_OVERLAYS (2026-08-04, his idea): plan-declared snippets from the
            # clips' own audio, covering the bed's arrangement gaps with something
            # DIEGETIC (idle swell under Nev, spray under the payoff). 0 credits.
            for ov in getattr(P, "SFX_OVERLAYS", []) or []:
                skey, ct, dv, vt, gdb = ov[0], ov[1], ov[2], ov[3], ov[4]
                if skey not in clips:
                    continue
                aw = os.path.join(tmp, f"ov_{skey}_{int(vt*100)}.wav")
                rc2, _ = sh(f'ffmpeg -y -v error -ss {ct:.3f} -i "{clips[skey]}" '
                            f'-t {dv:.3f} -vn -ac 1 -ar {SRF} -c:a pcm_s16le "{aw}"')
                if rc2 != 0 or not os.path.exists(aw) or os.path.getsize(aw) < 1000:
                    print(f"      !! overlay {skey}@{vt:.2f}s: no audio - skipped")
                    continue
                wv = wave.open(aw)
                x = np.frombuffer(wv.readframes(wv.getnframes()),
                                  dtype=np.int16).astype(float) / 32768.0
                wv.close()
                e = int(0.06 * SRF)              # slow 60ms fades - a swell, not a cut
                if len(x) > 2 * e:
                    x = x.copy()
                    x[:e] *= np.linspace(0, 1, e)
                    x[-e:] *= np.linspace(1, 0, e)
                at = int(vt * SRF)
                b = min(at + len(x), len(ftr))
                if b > at:
                    ftr[at:b] += x[:b - at] * (10.0 ** (gdb / 20.0))
                    n_laid += 1
                    fg_spans.append((at / SRF, b / SRF))
                    print(f"      overlay {skey} {ct:.1f}s -> video {vt:.2f}s "
                          f"({gdb:+.0f}dB): {ov[5] if len(ov) > 5 else ''}")
            if n_laid:
                pk = float(np.max(np.abs(ftr)))
                if pk > 0.98:               # safety clip only — never normalize UP:
                    ftr *= 0.98 / pk        # the plan's relative gains ARE the mix
                y = (np.clip(ftr, -1, 1) * 32767).astype("<i2")
                wv = wave.open(foley_path, "w")
                wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SRF)
                wv.writeframes(y.tobytes()); wv.close()
                HAVE_FOLEY = os.path.exists(foley_path)
                print(f"      foley  {n_laid}/{len(P.SHOTS)} shots carry their own clip "
                      f"audio (diegetic, plan-gained)")
            else:
                print("      !! FOLEY planned but NO clip carried audio — diegetic skipped")
        except Exception as e:
            print(f"      !! FOLEY FAILED: {str(e)[:70]} — diegetic layer skipped")
    else:
        print("      NO FOLEY block in plan — edit-sfx only (pre-2026-08-04 plan)")

    OUT = out_path or os.path.join(pdir, "output", f"{name.upper()}_CINEMATIC_v1.mp4")
    A = "aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo"
    # MIX TUNING LOG (2026-08-04, WRX, both MEASURED - do not re-try blind):
    #   original (12/13.5, thr .05, limit .76): lift -0.5dB FAIL, -8.3 LUFS OK, peak +0.2dBTP FAIL
    #   experiment (9/16.5, thr .03, limit .62): lift -2.8dB WORSE, -10.4 LUFS FAIL, peak -0.6 ok
    # Lesson: a LOWER limiter ceiling squashes the very transients the lift check
    # measures. Keep original balance; trim only the ceiling slightly for true-peak.
    # Next lever if lift still fails: raise impact/sub-drop amplitudes in sfxgen
    # placement (0.55/0.42), NOT the master gains.
    #
    # 3-LAYER MIX (2026-08-04, REVISED same day): diegetic + bed + edit-sfx.
    # v4 lesson (his ear: "music breaks ~1s at every cut then continues"): the
    # binary hard-duck windows STEPPED 12dB in and out, and thr .03 / ratio 8 /
    # release 180 punched holes under every whoosh. Replaced with ONE smooth
    # sidechain whose KEY is edit-sfx + foley summed: the loud launch foley ducks
    # the bed by itself (no windows, no steps), quiet HUMAN foley leaves it alone,
    # and gentler settings (thr .06, ratio 6, release 120) pump musically instead
    # of gating. SOUND.duck_shots is now legacy — kept in plans as documentation.
    # ---- 7c SOUND ENGINEER — automatic layer calibration (file 19, AUTOMATED;
    # his order 2026-08-04: "analyze and calibrate all the decibels so bgm/sfx/
    # foley are balanced — the bgm was so loud you can't hear Nev"). Hand-tuned
    # constants broke three times today the moment any one layer changed
    # (lessons 32/33). Now the BED is the anchor and every layer is MEASURED at
    # its mix gain, then trimmed to a target RELATIONSHIP before the master:
    #     edit-sfx active RMS      -> bed - 6 dB  (marks the cut, never sand)
    #     foley FOREGROUND moments -> bed - 2 dB  (hero/Nev moments read over
    #                                              the music; per-shot design
    #                                              inside the layer is preserved)
    SFX_DB, FOL_DB = 13.5, 0.0
    bed_gain_num = (17.0 if HAVE_SFX else 11.0) + BED_TRIM

    def _active_rms(path, gain_db=0.0, spans=None):
        try:
            import numpy as np, wave
            wv = wave.open(path)
            sr_ = wv.getframerate()
            xx = np.frombuffer(wv.readframes(wv.getnframes()),
                               dtype=np.int16).astype(float) / 32768.0
            wv.close()
            if spans:
                xx = np.concatenate([xx[int(a1*sr_):int(b1*sr_)] for a1, b1 in spans]
                                    ) if spans else xx
            a2 = xx[np.abs(xx) > 10 ** (-45 / 20.0)]
            if not len(a2):
                return None
            return 20.0 * float(np.log10(float(np.sqrt(np.mean(a2 ** 2))) + 1e-12)) + gain_db
        except Exception:
            return None
    try:
        seg_wav = os.path.join(tmp, "bedseg.wav")
        sh(f'ffmpeg -y -v error -ss {BED_OFFSET:.3f} -t {vd:.2f} -i "{BED}" '
           f'-ac 1 -ar 44100 -c:a pcm_s16le "{seg_wav}"')
        bl = _active_rms(seg_wav, bed_gain_num)
        rows = [("bed (anchor)", bl, bl, 0.0)]
        if bl is not None and HAVE_SFX:
            sl = _active_rms(sfx_path, SFX_DB)
            if sl is not None:
                trim = max(-8.0, min(8.0, (bl - 6.0) - sl))
                SFX_DB += trim
                rows.append(("edit-sfx", sl, bl - 6.0, trim))
        if bl is not None and HAVE_FOLEY and fg_spans:
            flv = _active_rms(foley_path, 0.0, spans=fg_spans)
            if flv is not None:
                FOL_DB = max(-8.0, min(8.0, (bl - 2.0) - flv))
                rows.append(("foley (foreground)", flv, bl - 2.0, FOL_DB))
        print("      SOUND ENGINEER calibration (active RMS at mix gain):")
        for nm, meas, tgt, tr in rows:
            print(f"        {nm:20s} measured {meas:6.1f}dB  target {tgt:6.1f}dB  "
                  f"trim {tr:+.1f}dB")
    except Exception as e:
        print(f"      !! calibration failed ({str(e)[:50]}) — falling back to constants")

    ins = f'-i "{graded}" -stream_loop -1 -i "{BED}"'
    bed_db = f"{bed_gain_num:.1f}"
    if abs(BED_TRIM) > 0.05:
        print(f"      bed level: {BED_TRIM:+.1f}dB segment compensation -> {bed_db}dB")
    fp = [f"[1:a]atrim={BED_OFFSET:.4f}:{vd+BED_OFFSET:.2f},asetpts=N/SR/TB,{A},"
          f"volume={bed_db}dB[bedraw]"]
    nxt = 2
    if HAVE_SFX:
        ins += f' -i "{sfx_path}"'
        # volume comes from the SOUND ENGINEER calibration above (target: bed-6).
        fp.append(f"[{nxt}:a]atrim=0:{vd:.2f},asetpts=N/SR/TB,{A},volume={SFX_DB:.1f}dB,"
                  f"asplit=2[sfx][sk]")
        nxt += 1
    if HAVE_FOLEY:
        ins += f' -i "{foley_path}"'
        # volume comes from the SOUND ENGINEER calibration (target: foreground bed-2)
        fp.append(f"[{nxt}:a]atrim=0:{vd:.2f},asetpts=N/SR/TB,{A},"
                  f"volume={FOL_DB:.1f}dB,asplit=2[fol][fk]")
        nxt += 1
    if HAVE_SFX and HAVE_FOLEY:
        fp.append("[sk][fk]amix=inputs=2:duration=first:normalize=0[key]")
    elif HAVE_SFX:
        fp.append("[sk]anull[key]")
    elif HAVE_FOLEY:
        fp.append("[fk]anull[key]")
    if HAVE_SFX or HAVE_FOLEY:
        fp.append("[bedraw][key]sidechaincompress=threshold=0.06:ratio=6:attack=4:"
                  "release=120:makeup=1[bed]")
    else:
        fp.append("[bedraw]anull[bed]")
    mix_in = ["[bed]"]
    if HAVE_SFX:
        mix_in.append("[sfx]")
    if HAVE_FOLEY:
        mix_in.append("[fol]")
    lim = "0.72" if HAVE_SFX else "0.76"
    # MASTER STAGE (2026-08-04, ~20 combos MEASURED across BOTH beds - the log):
    #   synth bed era: aac overshot +2..3.4dB on 81% sub-low energy; TP/LUFS/lift
    #     were jointly infeasible at ANY ceiling. Root cause was the bed.
    #   real bed era (bed_skrrt_slide_150, mastered stereo phonk): codec overshoot
    #     collapsed as predicted. Locked, all MEASURED on the delivered aac:
    #     bed +17 / sfx +18 / duck thr .03 / HP30 / relimit 0.70
    #     -> -9.5 LUFS (in band) and -1.5 dBTP (passes) simultaneously.
    #   A mastered bed is ~5dB hotter than the synth was quiet - hence bed 12->17,
    #   sfx 13.5->18 (whoosh must sit over real 808s), duck .05->.03 (deeper hole
    #   for the transient). HP30 stays: subsonics only feed codec overshoot.
    safety = (",highpass=f=30:poles=2"
              ",alimiter=limit=0.70:level=disabled:attack=3:release=30")
    if len(mix_in) == 1:
        fp.append(f"[bed]alimiter=limit={lim}:level=disabled:attack=5:release=50"
                  f"{safety}[aout]")
    else:
        fp.append(f"{''.join(mix_in)}amix=inputs={len(mix_in)}:duration=first:normalize=0,"
                  f"alimiter=limit={lim}:level=disabled:attack=5:release=50"
                  f"{safety}[aout]")
    layers = "bed" + ("+sfx" if HAVE_SFX else "") + ("+diegetic" if HAVE_FOLEY else "")
    print(f"      mix    {layers}, bed smooth-ducked by sfx+foley key")
    cmd = (f'ffmpeg -y -v error {ins} -filter_complex "{";".join(fp)}" '
           f'-map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 256k -t {vd:.2f} "{OUT}.part.mp4"')
    rc, err = sh(cmd)
    if rc == 0 and os.path.exists(OUT + ".part.mp4") and dur(OUT + ".part.mp4") > 1:
        os.replace(OUT + ".part.mp4", OUT)      # ATOMIC — never publish a partial file
    else:
        print(f"  !! MIX FAILED: {err.strip()[:110]} — SHIPPING SILENT, DO NOT POST")
        sh(f'ffmpeg -y -v error -i "{graded}" -c copy "{OUT}"')

    # ---- declare ACTUAL post-blend boundaries, never the plan ----
    actual, tt = [], 0.0
    for s in segs:
        tt += dur(s); actual.append(round(tt, 3))
    actual = actual[:-1]
    # blends declared for verify's transition QC: seam END = planned shot end minus
    # the shift from earlier blends; seam START = end - width. With width == beat,
    # both sit on the grid by construction — verify measures it anyway.
    blends_meta = [{"after_shot": i,
                    "start": round(tl[i][0] + tl[i][1] - shift[i] - P.BLEND_WIDTH, 3),
                    "end": round(tl[i][0] + tl[i][1] - shift[i], 3)} for i in blend_ok]
    json.dump({"cuts": actual, "planned": cuts, "bpm": P.BPM, "beat": P.BEAT,
               "blends": blends_meta, "blend_width": P.BLEND_WIDTH},
              open(os.path.join(pdir, "audio", f"{name}_cuts.json"), "w"), indent=1)

    pm = []
    for i, (key, _cs, kind, _n) in enumerate(P.SHOTS):
        d_ = P.BEATS[kind] * P.BEAT
        ti = shot_tin.get(i)
        pm.append({"shot": i, "src": key, "tin": ti,
                   "has_peak": bool(ti is not None and any(
                       ti <= pk <= ti + d_ for pk in sense[key]["action_peaks_s"]))})
    json.dump(pm, open(os.path.join(tmp, "manifest_peaks.json"), "w"), indent=1)

    lens = [d for _s, d, _k in tl]
    print(f"\n  -> {os.path.relpath(OUT, HERE)}   {dur(OUT):.2f}s")
    print(f"     median shot {st.median(lens):.2f}s   cuts/min {len(actual)/(t/60):.1f}")
    print(f"     {len(actual)} ACTUAL post-blend cuts declared ({len(cuts)} planned)")
    print(f"\n  NEXT: python3 talyx.py verify {name}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--out")
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()
    sys.exit(build(a.name, a.out, not a.no_cache))
