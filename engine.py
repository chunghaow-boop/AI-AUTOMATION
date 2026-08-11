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
    """Bed first: music defines the grid, not the picture.

    PILLAR-AWARE + TEMPO-VERIFIED (2026-08-05, red-team find, the worst of the day).
    The old version searched `assets/bgm/**/*.wav` as a last resort and picked the
    LARGEST file. MEASURED: a travel_vlog plan at 105 BPM resolved to the WRX's
    `bed_skrrt_slide_150.wav` — a 150 BPM phonk track — and the build would have
    reported SUCCESS. Every downstream gate would then have measured a perfectly
    beat-locked, correctly mastered video that was a car edit's soundtrack laid
    under someone's holiday. Nothing anywhere compared the bed's tempo to the plan's.

    Now: search the PILLAR's own bank first, and REFUSE a bed whose measured tempo
    does not match the plan (lesson 25 — always re-measure the file, never trust
    the filename)."""
    import glob

    # 2026-08-07, found by desafarm's first real build: THE PLAN NAMES ITS BED AND
    # NOTHING READ IT. SOUND['bed'] declared BGM/travel_vlog/liqwyd-to-the-moon.mp3,
    # "97.5 BPM NATIVE, zero stretch" - and this function returned Pathway-Home.mp3,
    # the LARGEST file in the pillar bank, measured at 166.7 BPM. verify_bed_tempo
    # then refused the build, which is the gate working, but the plan had been
    # overruled by a file-size sort. Same class as the plate lesson: a spec that
    # lives only in the plan is never read by the pipeline. The DECLARED bed wins
    # when it is on disk; the glob below stays as the fallback it always was.
    declared = (getattr(P, "SOUND", {}) or {}).get("bed", "")
    if declared:
        cand = declared.split(" - ")[0].split(" \u2014 ")[0].strip()
        cand = cand.replace("\\", "/").lstrip("/")
        full = cand if os.path.isabs(cand) else os.path.join(HERE, cand)
        if os.path.exists(full):
            return full
        print(f"  !! the plan declares bed {cand!r} and it is NOT on disk - "
              f"falling back to the pillar bank, and the tempo gate will judge it")

    pil = getattr(P, "PILLAR", "")
    # 2026-08-05: the pillar banks hold MP3 (that is what a download gives you), and
    # find_bed globbed *.wav ONLY — so a correctly-stocked BGM/travel_vlog/ resolved to
    # None and the build died claiming no bed existed. Accept both; ffmpeg reads either.
    pats = [os.path.join(pdir, "audio", "*.wav"),                    # prepared for THIS project
            os.path.join(pdir, "audio", "*.mp3")]
    if pil:
        for ext in ("wav", "mp3"):                                   # the pillar's own bank
            pats += [os.path.join(HERE, "BGM", pil, f"*.{ext}"),
                     os.path.join(HERE, "assets", "bgm", pil, f"*.{ext}")]
    pats += [os.path.join(HERE, "assets", "bgm", f"*{int(P.BPM)}*.wav")]
    # NOTE: the old catch-all `assets/bgm/**/*.wav` is GONE on purpose. A bed from an
    # unknown pillar is worse than no bed: no bed fails loudly, a wrong bed ships.
    for pat in pats:
        c = [f for f in glob.glob(pat, recursive=True)
             if "sfx" not in os.path.basename(f).lower()]
        if c:
            return sorted(c, key=os.path.getsize, reverse=True)[0]
    return None


def verify_bed_tempo(bed, want_bpm, tol_pct=2.0):
    """Return (ok, measured_bpm, detail). A bed at the wrong tempo cannot be
    beat-locked to, and the failure is INVISIBLE downstream — the cuts land on a
    grid the music never plays."""
    try:
        sys.path.insert(0, TOOLS)
        import rhythm
        x = rhythm.pcm(bed)
        flux, hop = rhythm.stft_flux(x)
        r = rhythm.estimate_tempo(flux, hop)   # returns (bpm, phase); either may be None
        got = r[0] if isinstance(r, (tuple, list)) else r
        if got is None:
            return None, None, "tempo estimator found no stable grid in this file"
        got = float(got)
    except Exception as e:
        return None, None, f"could not measure bed tempo ({str(e)[:50]})"
    # half/double-time is the same grid musically — accept it, name it
    cands = [(got, "1x"), (got * 2, "2x"), (got / 2, "0.5x")]
    for c, lab in cands:
        if abs(c - want_bpm) / want_bpm * 100 <= tol_pct:
            return True, got, f"measured {got:.1f} BPM, matches plan {want_bpm:.0f} ({lab})"
    return False, got, (f"measured {got:.1f} BPM but the plan is {want_bpm:.0f} "
                        f"({abs(got-want_bpm)/want_bpm*100:.0f}% off). Cuts would land on a "
                        f"grid the music never plays. Stretch the bed to {want_bpm:.0f} "
                        f"(see lesson: asetrate, then RE-MEASURE) or pick another.")


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


LUMA_RESPONSE = 296.0
# MEASURED 2026-08-05 on KK v14, 18 corrected shots: ffmpeg eq=brightness moves mean
# luma by 174-519 per unit (mean 296, spread 3.0x, content dependent).
# The old code assumed a FIXED 255/1.9 = 134. Every correction was therefore ~2.2x too
# strong and 17 of 20 shots CROSSED the target and landed on the far side.
# 296 is only the FIRST GUESS of a closed loop below - never trusted as a constant.


def shot_match(segs, W, H, FPS, tmp, tol=10.0, max_gain=0.14,
               max_move=18.0, mode="neighbour", passes=2):
    """Reduce JARRING CUT-BOUNDARY SWINGS. It does not relight, and it does not pull
    the video to one level.

    Measured on his source clips 2026-08-05: the three raw Higgsfield clips he called
    "close to perfect" span 45.1 to 92.9 mean luma. A 47-luma spread is INSIDE his
    approval band. Any stage that pulls that to a single median is destroying the
    thing he likes. kk_I measured 45.1 at source (his word: perfect) and the old
    median-pull rendered it at 116.9 - a +72 relight of an approved shot.

    Two modes:
      neighbour  (default) - a shot is touched ONLY if it differs from the shot before
                 it by more than `tol`, and is then moved just inside that boundary,
                 never to a global level. Preserves a time-of-day arc.
      median     - legacy global pull, for pillars whose look is authored in the edit.

    `max_move` is stated in LUMA, not in opaque ffmpeg units, and is capped by
    `max_gain` as a second belt.

    CLOSED LOOP: apply, RE-MEASURE the rendered file, correct once more using the
    response actually observed on THAT shot. Keeps whichever candidate lands closest,
    including the untouched original. A pass that makes the boundary worse is reverted.
    """
    import numpy as np
    lv = [_level(s) for s in segs]
    if any(x is None for x in lv):
        print("  !! could not measure a segment - SKIPPING shot match")
        return segs

    def swings(levels):
        return [abs(levels[i] - levels[i - 1]) for i in range(1, len(levels))]

    before = swings(lv)
    # ---- targets -------------------------------------------------------------
    if mode == "median":
        med = float(np.median(lv))
        targets = [med] * len(lv)
    else:
        targets, prev = [], lv[0]
        for i, l in enumerate(lv):
            if i == 0:
                targets.append(l); prev = l; continue
            d = l - prev
            # only the EXCESS over tol is a defect; the rest is the arc, keep it
            t = l - (d - tol) if d > tol else (l - (d + tol) if d < -tol else l)
            t = max(l - max_move, min(l + max_move, t))
            targets.append(t)
            prev = t
        del prev

    out, fixed, delivered = [], 0, []
    for i, (p, l, t) in enumerate(zip(segs, lv, targets)):
        need = t - l
        if abs(need) <= 1.0:
            out.append(p); delivered.append(l); continue
        best, best_lv, best_err = p, l, abs(l - t)
        resp = LUMA_RESPONSE
        gain = 0.0
        for k in range(passes):
            step = (t - best_lv) / max(resp, 60.0)
            g = max(-max_gain, min(max_gain, gain + step))
            # never authorise more luma authority than the style allows
            g = max(-max_move / resp, min(max_move / resp, g))
            if abs(g - gain) < 1e-4:
                break
            o = p.replace(".mp4", f"_m{k}.mp4" if k else "_m.mp4")
            spec, sf = f"{g:.4f}", o + ".spec"
            if not (os.path.exists(o) and os.path.exists(sf)
                    and open(sf).read() == spec):
                rc, err = sh(f'ffmpeg -y -v error -i "{p}" '
                             f'-vf "eq=brightness={g:.4f},setsar=1" -an -c:v libx264 '
                             f'-crf 18 -preset veryfast -pix_fmt yuv420p "{o}"')
                if rc != 0 or not os.path.exists(o):
                    print(f"  !! shot {i} match FAILED - keeping unmatched: "
                          f"{err.strip()[:60]}")
                    break
                open(sf, "w").write(spec)
            m = _level(o)
            if m is None:
                break
            if abs(g) > 1e-6:                      # learn THIS shot's real response
                r = abs(m - l) / abs(g)
                if r > 40.0:
                    resp = r
            gain = g
            if abs(m - t) < best_err:
                best, best_lv, best_err = o, m, abs(m - t)
            if best_err <= max(1.5, tol * 0.15):
                break
        if best is not p:
            fixed += 1
        out.append(best); delivered.append(best_lv)

    after = swings(delivered)
    b_mean = float(np.mean(before)) if before else 0.0
    a_mean = float(np.mean(after)) if after else 0.0
    b_max = max(before) if before else 0.0
    a_max = max(after) if after else 0.0
    print(f"  mode {mode}  tol {tol}  max_move {max_move:.0f} luma  clamp {max_gain:+.3f}")
    print(f"  boundary swing  mean {b_mean:.1f} -> {a_mean:.1f}   worst "
          f"{b_max:.1f} -> {a_max:.1f}   ({fixed}/{len(segs)} shots touched)")
    moved = max((abs(d - o) for d, o in zip(delivered, lv)), default=0.0)
    print(f"  largest single shot relight: {moved:.1f} luma "
          f"(budget {max_move:.0f})")
    # A FIX THAT MAKES IT WORSE MUST NOT SHIP.
    if a_mean > b_mean + 0.5:
        print("  !! shot match made boundaries WORSE - REVERTING to unmatched segments")
        return segs
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
def _profile(pillar):
    """Read a pillar's measured profile (and its declared style). 2026-08-05."""
    for c in (os.path.join(HERE, "assets", "pillars", "PILLAR-PROFILES.json"),
              os.path.join(HERE, "pillars", "PILLAR-PROFILES.json")):
        if os.path.exists(c):
            try:
                return json.load(open(c, encoding="utf-8")).get(pillar) or {}
            except Exception:
                return {}
    return {}


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
        print(f"!! NO MUSIC BED for pillar '{getattr(P,'PILLAR','?')}' at {P.BPM:.0f} BPM.")
        print(f"   Looked in: projects/{name}/audio/ · BGM/{getattr(P,'PILLAR','?')}/ "
              f"· assets/bgm/*{int(P.BPM)}*")
        print(f"   Drop an in-band track in BGM/{getattr(P,'PILLAR','?')}/ and run "
              f"tools/bedqc.py. Failing loudly beats bedding the wrong genre.")
        return 1
    print(f"  bed: {os.path.relpath(BED, HERE)}")
    _ok, _got, _why = verify_bed_tempo(BED, P.BPM)
    if _ok is None:
        print(f"  !! bed tempo UNVERIFIED — {_why}. Proceeding, but beat-lock is unproven.")
    elif not _ok:
        print(f"  !! BED TEMPO MISMATCH — {_why}")
        print(f"     REFUSING to build: a wrong-tempo bed produces a video that passes "
              f"every downstream gate and is still wrong.")
        return 1
    else:
        print(f"  bed tempo OK — {_why}")

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
    mid_action, look_dupes = [], []
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

        # LOOK DIVERSITY (2026-08-07, HIS CALL: "i think the duplicated scenes are
        # not something wrong with the ai video generation, its at the video editing
        # side"). He was right, and measuring it split the blame exactly:
        # searching EVERY non-overlapping window pair of the three duplicated
        # sources for the most different pair available -
        #   source C (cabin)  best available comp 0.817 / col 0.798  DELIVERED 0.928 / 0.986
        #   source G (goats)  best available comp 0.868 / col 0.872  DELIVERED 0.866 / 0.933
        #   source E (calf)   best available comp 0.911 / col 0.973  DELIVERED 0.878 / 0.984
        # For C a clean pair EXISTED and this allocator threw it away, because it
        # ranked candidates on action peak alone and never asked whether the two
        # windows LOOK different. For E nothing in the clip could have worked - that
        # one is a plan error and ingest_gate() catches it before assembly.
        chosen_looks = []

        def _look(ts):
            """composition + colour of the frame at ts, for window comparison."""
            try:
                import cv2 as _cv, numpy as _np
                cap = _cv.VideoCapture(clips[key])
                cap.set(_cv.CAP_PROP_POS_MSEC, max(0.0, ts) * 1000.0)
                ok, fr = cap.read(); cap.release()
                if not ok:
                    return None
                sm = _cv.resize(fr, (64, 112))
                g = _cv.cvtColor(sm, _cv.COLOR_BGR2GRAY).astype(_np.float32)
                gx = _cv.Sobel(g, _cv.CV_32F, 1, 0, ksize=3)
                gy = _cv.Sobel(g, _cv.CV_32F, 0, 1, ksize=3)
                mag = _np.sqrt(gx * gx + gy * gy)
                ang = (_np.arctan2(gy, gx) + _np.pi) * (8 / (2 * _np.pi))
                v = []
                for r_ in range(4):
                    for c_ in range(4):
                        m = mag[r_ * 28:(r_ + 1) * 28, c_ * 16:(c_ + 1) * 16]
                        a_ = ang[r_ * 28:(r_ + 1) * 28, c_ * 16:(c_ + 1) * 16]
                        hh = _np.zeros(8)
                        for b_ in range(8):
                            hh[b_] = m[(a_.astype(int) % 8) == b_].sum()
                        v.append(hh / (hh.sum() + 1e-9))
                v = _np.concatenate(v); v = v / (_np.linalg.norm(v) + 1e-9)
                ch = _cv.calcHist([sm], [0, 1, 2], None, [8, 8, 8], [0, 256] * 3)
                ch = _cv.normalize(ch, ch).flatten()
                return (v, ch)
            except Exception:
                return None

        def _dupe_penalty(tin_, d2_):
            """max similarity of this window to the ones already taken from THIS
            source. 0 when nothing is taken yet or the frame cannot be read."""
            if not chosen_looks:
                return 0.0
            import cv2 as _cv
            L = _look(tin_ + d2_ / 2.0)
            if L is None:
                return 0.0
            worst = 0.0
            for P0 in chosen_looks:
                cs = float(L[0] @ P0[0])
                ks = float(_cv.compareHist(L[1], P0[1], _cv.HISTCMP_CORREL))
                worst = max(worst, min(cs, ks))   # both axes must agree to be a dupe
            return worst

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
                        # is still >=80% of its peak cuts MID-action.
                        mp, me = _mot(pk), _mot(tin_ + d_)
                        unresolved = 1 if (mp and me and me > 0.8 * mp) else 0
                        dup = _dupe_penalty(tin_, d_) if len(shots_of) > 1 else 0.0
                        # rank: never cut mid-action, then never repeat the look,
                        # then sit nearest the clip's best moment.
                        cands.append((unresolved, round(dup, 2),
                                      abs(pk - c["best_in_s"]), tin_))
            if cands:
                cands.sort()
                tin_ = cands[0][3]
                if len(shots_of) > 1:
                    L = _look(tin_ + d_ / 2.0)
                    if L is not None:
                        chosen_looks.append(L)
                if cands[0][0]:
                    mid_action.append(f"{key}: shot {i} ends while motion is still "
                                      f">=80% of its peak - the event is cut off")
                if cands[0][1] >= 0.80:
                    look_dupes.append(f"{key}: shots share a look at {cands[0][1]:.2f} "
                                      f"(best window available was no better)")
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
    # HARD GATES, 2026-08-07. Both of these were already COMPUTED and both were
    # only ever used as sort keys, so the build shipped with the defect and every
    # downstream gate passed it:
    #   - "unresolved" (window ends above 80% of its own action peak) existed since
    #     2026-08-04 and desafarm still delivered shot 5 at 96% and shot 14 at 83%.
    #     His words: "some scenes important events are cutted out".
    #   - look duplication was not measured at all until he said the duplicates were
    #     an EDITING problem, not a generation one. He was right.
    # A preference that never blocks is not a rule, it is a hope.
    if mid_action:
        print("!! EVENTS CUT BEFORE THEY FINISH:")
        for m in mid_action:
            print(f"   {m}")
        print("   Fix the PLAN (lengthen the shot or re-source it). REFUSING to cut "
              "an event in half.")
        return 1
    if look_dupes:
        print("!! TWO SHOTS FROM ONE SOURCE READ AS THE SAME PICTURE:")
        for m in look_dupes:
            print(f"   {m}")
        print("   This clip cannot carry two shots. Drop it to one in the plan, or "
              "generate a second angle. REFUSING to show the same shot twice.")
        return 1
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
        # DELOGO (2026-08-04, lesson 35): an invented red 'SR' badge in G's plate
        # recess shipped through 8 builds. plan DELOGO = {shot: (x,y,w,h)} in OUTPUT
        # frame coords patches it at SEGMENT render — before the single final encode,
        # so the fix costs zero extra compression generations and zero credits.
        dl = (getattr(P, "DELOGO", {}) or {}).get(i)
        o = os.path.join(tmp, f"c{i:02d}.mp4")
        # spec carries the SOURCE FILE's identity too (2026-08-05, red-team): a
        # re-downloaded clip keeps its basename — without mtime+size a stale
        # segment of the OLD content serves silently.
        _cst = os.stat(clips[key])
        spec = (f"{os.path.basename(clips[key])}|{_cst.st_size}|{int(_cst.st_mtime)}|"
                f"{tin:.3f}|{d:.3f}|{cs}|{cx}|{cy}|frames|dl={dl}")
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
        if dl:
            x_, y_, w_, h_ = [int(v) for v in dl]
            if w_ <= 0 or h_ <= 0 or x_ < 0 or y_ < 0 or x_ + w_ > W or y_ + h_ > H:
                print(f"  !! shot {i}: DELOGO ({x_},{y_},{w_},{h_}) outside {W}x{H} "
                      f"— REFUSING to render a corrupt patch. Fix the plan.")
                return 1
            vf += f",delogo=x={x_}:y={y_}:w={w_}:h={h_}"
            print(f"  shot {i} ({key}): DELOGO patch {w_}x{h_} at ({x_},{y_})")
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
    # CLAMP FROM THE STYLE BLOCK (2026-08-05). 0.14 was tuned on a NIGHT car edit,
    # one light state end to end. KK v1 measured 9/19 cuts swinging >18 (worst 52)
    # because a travel vlog spans golden hour -> night by design: the segments really
    # are that far apart, and 0.14 could not close the gap (15/20 matched). The arc is
    # the STORY (the card clock), so the fix is grading authority, not reordering.
    # 2026-08-05, ROOT CAUSE: the gain formula assumed a fixed 134 luma per unit of
    # eq=brightness; MEASURED response is 174-519. Every correction ran ~2.2x hot and
    # 17/20 shots crossed the target. Widening the clamp to 0.26 "making things worse"
    # was a SYMPTOM of that miscalibration, not a fact about the clamp.
    _st = ((_profile(getattr(P, "PILLAR", "")) or {}).get("style") or {})
    _clamp = float(_st.get("shot_match_clamp", 0.14))
    _mode = str(_st.get("shot_match_mode", "neighbour"))
    _move = float(_st.get("shot_match_max_move", 18.0))
    _tol = float(_st.get("shot_match_tol", 10.0))
    segs = shot_match(segs, W, H, FPS, tmp, tol=_tol, max_gain=_clamp,
                      max_move=_move, mode=_mode)

    # ---- 4 blends ----
    print(f"\n[4/7] blends  {P.BLEND_KIND} {P.BLEND_WIDTH*1000:.0f}ms at declared boundaries")
    out, n = list(segs), 0
    blend_ok = []      # successful boundaries — the foley layer needs the ACTUAL timeline
    for i in sorted(set(P.BLEND_AFTER)):
        if i + 1 >= len(out) or out[i] is None or out[i + 1] is None:
            continue
        o = os.path.join(tmp, f"bx{i:02d}.mp4")
        # STALE BLEND (2026-08-05, red-team find): basenames alone matched even when
        # a segment was RE-RENDERED with new content (c06.mp4 overwritten in place) —
        # the cached blend then ships the OLD pixels inside the seam. The delogo
        # build dodged this only because shot 15 touches no blend. Content identity
        # (size+mtime of both inputs) now invalidates the blend cache.
        _sa, _sb = os.stat(out[i]), os.stat(out[i + 1])
        bspec = (f"{os.path.basename(out[i])}|{_sa.st_size}|{int(_sa.st_mtime)}|"
                 f"{os.path.basename(out[i+1])}|{_sb.st_size}|{int(_sb.st_mtime)}|"
                 f"{P.BLEND_KIND}|{P.BLEND_WIDTH}")
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
    # FONT RESOLUTION (2026-08-06). Both original candidates were LINUX paths. On
    # WINDOWS - the machine this pipeline actually runs on - neither exists, so FONT was
    # set to a file that is not there and drawtext rendered NOTHING. Silently: ffmpeg
    # does not reliably fail on a missing fontfile, so a card could vanish from a
    # DELIVERED video and no gate would ever see it. Surfaced by smoketest on Windows.
    # The REPO font goes first on purpose: it ships with the project, so the cards look
    # identical on every machine instead of depending on what the OS happens to have.
    _FONT_CANDIDATES = [
        os.path.join(HERE, "assets", "fonts", "loose", "CapCutSansText-Bold.otf"),
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    FONT = next((f for f in _FONT_CANDIDATES if os.path.exists(f)), None)
    if FONT is None:
        # LOUD, not silent - but not fatal here, because a build whose cards came from
        # cards.py (Playwright) never touches drawtext and must not be stopped by this.
        print("      !! NO USABLE FONT FOUND for the drawtext fallback. Tried:")
        for _c in _FONT_CANDIDATES:
            print(f"           {_c}")
        print("      !! If this build needs the drawtext fallback it will STOP rather "
              "than deliver empty cards.")
    else:
        # ffmpeg's drawtext parses ':' as its option separator, so a Windows drive
        # letter must be escaped or the filter silently reads the path as just 'C'.
        # Backslashes are normalised for the same reason.
        FONT = FONT.replace("\\", "/").replace(":", r"\:")
        print(f"      card font: {FONT}")
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
            if FONT is None:
                raise RuntimeError(
                    "drawtext card fallback needed but NO USABLE FONT was found - "
                    "see the candidate list printed above. Refusing to render cards "
                    "that would come out EMPTY: a silently missing card on a delivered "
                    "video is worse than a stopped build.")
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
    # STYLE GATE (2026-08-05). Everything ABOVE this line is CRAFT — the window
    # allocator, action-centering, shot-match, bed segment scan, phase fit, beat
    # lock, sound-engineer calibration, master chain — and it transfers to any
    # music-led pillar unchanged. THIS stage is the car's SIGNATURE: noise sweeps
    # and sub-drops on cuts. travel_vlog measured HARD CUTS ONLY; laying phonk
    # whooshes over vlog footage would be a car edit wearing someone else's
    # holiday. edit_sfx is declared per pillar in PILLAR-PROFILES.json.
    _style = (_profile(getattr(P, "PILLAR", "")) or {}).get("style", {})
    _sfx_policy = _style.get("edit_sfx", "full")
    if _sfx_policy == "none":
        print(f"      edit-sfx SKIPPED — pillar '{getattr(P,'PILLAR','?')}' declares "
              f"edit_sfx=none (hard cuts carry themselves). Bed + diegetic only.")
    elif _sfx_policy == "hero_only":
        print(f"      edit-sfx HERO ONLY — no transient design on cuts, but the plan's "
              f"hero moment keeps its sound (his catch: the car pass was the QUIETEST "
              f"instant in the video, measured -2.8dB vs a random moment).")
    try:
        if _sfx_policy == "none":
            raise RuntimeError("edit_sfx=none")
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
        if _sfx_policy == "hero_only":
            # ONE sound, at the hero shot's own boundary. No whooshes anywhere.
            _hero = (getattr(P, "SOUND", {}) or {}).get("hero_shot", 0)
            _ht = 0.0 if _hero == 0 else (cuts[_hero - 1] if 0 < _hero <= len(cuts) else 0.0)
            place(sfxgen.impact(0.9), max(0.0, _ht - 0.02), 0.62); ni += 1
            print(f"      hero impact placed at {_ht:.2f}s (shot {_hero})")
            cuts_iter = []
        else:
            cuts_iter = cuts
        for c in cuts_iter:
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

    # VERSION MONOTONIC (2026-08-05, red-team find): the default was hardcoded _v1
    # and OVERWROTE the approved v1 the night the delogo build ran. History is
    # evidence; a build may never clobber it. Default = next free version number.
    if out_path:
        OUT = out_path
    else:
        odir = os.path.join(pdir, "output")
        os.makedirs(odir, exist_ok=True)
        import re as _re
        vs = [int(m.group(1)) for f_ in os.listdir(odir)
              for m in [_re.match(rf"{name.upper()}_CINEMATIC_v(\d+)\.mp4$", f_)] if m]
        OUT = os.path.join(odir, f"{name.upper()}_CINEMATIC_v{max(vs, default=0) + 1}.mp4")
        print(f"  output -> {os.path.basename(OUT)} (next free version, never overwrite)")
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
    # ---- MIX RELATIONSHIPS, NOW PER PILLAR (2026-08-06, his catch: "the sfx and
    # foley are too loud it covers the whole bgm").
    # MEASURED before changing anything, on the delivered files:
    #   KK v15 (travel_vlog, hero_only): during the loudest 10% of broadband moments
    #     the bed's 40-160Hz band drops  -4.9 dB  -> ordinary musical ducking.
    #   WRX v9 (car_cinematic, edit_sfx=full): the same measurement reads -31.1 dB.
    #     That is not ducking, that is the music being removed under every whoosh.
    # The old constants (-6 for sfx, -2 for foley foreground, duck 0.06/6:1) are kept
    # as the DEFAULTS, so every existing pillar builds byte-identically unless its
    # profile says otherwise. A pillar can now state its own balance.
    _mx = _style if isinstance(_style, dict) else {}
    SFX_TGT = float(_mx.get("mix_sfx_target_db", -6.0))    # edit-sfx active RMS vs bed
    FOL_TGT = float(_mx.get("mix_foley_fg_target_db", -2.0))  # foley FOREGROUND vs bed
    DUCK_THR = float(_mx.get("mix_duck_threshold", 0.06))
    DUCK_RAT = float(_mx.get("mix_duck_ratio", 6.0))
    DUCK_REL = float(_mx.get("mix_duck_release", 120.0))
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
                trim = max(-8.0, min(8.0, (bl + SFX_TGT) - sl))
                SFX_DB += trim
                rows.append(("edit-sfx", sl, bl + SFX_TGT, trim))
        if bl is not None and HAVE_FOLEY and fg_spans:
            flv = _active_rms(foley_path, 0.0, spans=fg_spans)
            if flv is not None:
                want = (bl + FOL_TGT) - flv
                FOL_DB = max(-8.0, min(8.0, want))
                rows.append(("foley (foreground)", flv, bl + FOL_TGT, FOL_DB))
                # HIS CATCH, 2026-08-07: "the bgm is slightly louder than everything
                # it covers all the sfx, and foley which is not balanced".
                # ROOT CAUSE, and it is this clamp. On desafarm the mixer measured
                # foley at -22.5dB against a -6.2dB target, computed the correct
                # +16.3dB, applied the +8.0dB the clamp allows, and PRINTED "+8.0dB"
                # as though it had succeeded. Foley shipped 8.3dB under its own
                # target and verify's soundscape median came out 0.935 - cuts sounded
                # no different from mid-shot. Seedance ambience is always this quiet,
                # so the clamp binds on every travel_vlog build.
                # A limiter that silently eats half the correction is a lie. Say so.
                FOLEY_SHORT = round(want - FOL_DB, 1)
                if FOLEY_SHORT > 1.0:
                    print(f"      !! FOLEY CLAMPED: needed {want:+.1f}dB, the +/-8dB "
                          f"limit allowed {FOL_DB:+.1f}dB - foley lands "
                          f"{FOLEY_SHORT:.1f}dB UNDER target and the bed will cover it.")
                    print(f"         The clip audio is too quiet to lift by gain alone. "
                          f"Fix at the SOURCE (generate_audio louder / normalise the "
                          f"foley stem before mixing), not by widening this clamp.")
                    globals()["_FOLEY_SHORTFALL"] = FOLEY_SHORT
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
        fp.append(f"[bedraw][key]sidechaincompress=threshold={DUCK_THR}:"
                  f"ratio={DUCK_RAT:g}:attack=4:release={DUCK_REL:g}:makeup=1[bed]")
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
