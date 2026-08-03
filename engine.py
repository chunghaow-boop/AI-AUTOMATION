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


def shot_match(segs, W, H, FPS, tmp, tol=10.0, max_gain=0.10):
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
    try:
        _x = rhythm.pcm(BED); _f, _t = rhythm.stft_flux(_x)
        _on = rhythm.pick_onsets(_f, _t)
        BED_OFFSET = float(_on[0]) if len(_on) else 0.0
    except Exception as e:
        BED_OFFSET = 0.0
        print(f"  !! could not measure bed phase ({str(e)[:40]}) — assuming 0. "
              f"Cuts may sit off the hits.")
    print(f"\n[1/7] phase   first transient at {BED_OFFSET*1000:.0f}ms -> bed trimmed to it")
    print(f"      grid    {len(P.SHOTS)} shots @ {P.BPM:.0f} BPM, beat {P.BEAT*1000:.0f}ms, "
          f"{TOTAL:.2f}s")

    # ---- 2 segments, cut on action ----
    print(f"\n[2/7] segments  centred on unused action peaks, frame-exact")
    sense = {k: clipsense.analyse(v) for k, v in clips.items()}
    xy = getattr(P, "CROP_XY", {})
    used = {k: set() for k in clips}
    rep = {k: 0 for k in clips}
    shot_tin, segs, cuts, t = {}, [], [], 0.0
    for i, ((key, cs, kind, note), (start, d, _k)) in enumerate(zip(P.SHOTS, tl)):
        c = sense[key]
        peaks = [pk for pk in c["action_peaks_s"] if pk not in used[key]] or list(c["action_peaks_s"])
        want = c["best_in_s"] + rep[key] * 1.25
        pk = min(peaks, key=lambda x: abs(x - want)) if peaks else c["best_in_s"]
        used[key].add(pk); rep[key] += 1
        tin = max(0.0, pk - d * 0.42)
        if c["duration"] < tin + d:
            tin = max(0.0, c["duration"] - d - 0.05)
        shot_tin[i] = tin
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
    for i in sorted(set(P.BLEND_AFTER)):
        if i + 1 >= len(out) or out[i] is None or out[i + 1] is None:
            continue
        o = os.path.join(tmp, f"bx{i:02d}.mp4")
        bspec = f"{os.path.basename(out[i])}|{os.path.basename(out[i+1])}|{P.BLEND_KIND}|{P.BLEND_WIDTH}"
        bsf = o + ".spec"
        if use_cache and os.path.exists(o) and os.path.exists(bsf) and open(bsf).read() == bspec:
            out[i] = o; out[i + 1] = None; n += 1
            continue
        try:
            fx.FX[P.BLEND_KIND](out[i], out[i + 1], o, d=P.BLEND_WIDTH, W=W, H=H, fps=FPS)
            open(bsf, "w").write(bspec)
            if os.path.exists(o) and dur(o) > 0.3:
                out[i] = o; out[i + 1] = None; n += 1
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
            if im is None or im.shape[2] != 4:      # no alpha = full-frame fallback = unusable as overlay
                cards_png = []; break
            cards_png.append(o)
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
            size = 56 if kind == "cta" else max(56, min(78, int(560 / max(4, len(txt)))))
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
                place(sfxgen.whoosh(0.30, up=True), max(0.0, c - P.SFX_LEAD), 0.34); nw += 1
        pk = float(np.max(np.abs(track))) or 1.0
        sfxgen._w(sfx_path, track / pk * 0.72)
        HAVE_SFX = os.path.exists(sfx_path)
        print(f"\n[7/7] sfx    {nw} whoosh + {ni} impact/drop, leading each cut by "
              f"{P.SFX_LEAD*1000:.0f}ms")
    except Exception as e:
        print(f"\n[7/7] !! SFX FAILED: {str(e)[:80]} — cuts have NO transient design")

    OUT = out_path or os.path.join(pdir, "output", f"{name.upper()}_CINEMATIC_v1.mp4")
    A = "aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo"
    if HAVE_SFX:
        f = (f"[1:a]atrim={BED_OFFSET:.4f}:{vd+BED_OFFSET:.2f},asetpts=N/SR/TB,{A},"
             f"volume=12.0dB[bedraw];"
             f"[2:a]atrim=0:{vd:.2f},asetpts=N/SR/TB,{A},volume=13.5dB,asplit=2[sfx][key];"
             f"[bedraw][key]sidechaincompress=threshold=0.05:ratio=8:attack=4:"
             f"release=180:makeup=1[bed];"
             f"[bed][sfx]amix=inputs=2:duration=first:normalize=0,"
             f"alimiter=limit=0.76:level=disabled:attack=5:release=50[aout]")
        cmd = (f'ffmpeg -y -v error -i "{graded}" -stream_loop -1 -i "{BED}" -i "{sfx_path}" '
               f'-filter_complex "{f}" -map 0:v -map "[aout]" -c:v copy -c:a aac '
               f'-b:a 192k -t {vd:.2f} "{OUT}.part.mp4"')
    else:
        f = (f"[1:a]atrim={BED_OFFSET:.4f}:{vd+BED_OFFSET:.2f},asetpts=N/SR/TB,{A},"
             f"volume=11.0dB,alimiter=limit=0.76:level=disabled:attack=5:release=50[aout]")
        cmd = (f'ffmpeg -y -v error -i "{graded}" -stream_loop -1 -i "{BED}" '
               f'-filter_complex "{f}" -map 0:v -map "[aout]" -c:v copy -c:a aac '
               f'-b:a 192k -t {vd:.2f} "{OUT}.part.mp4"')
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
    json.dump({"cuts": actual, "planned": cuts, "bpm": P.BPM, "beat": P.BEAT},
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
