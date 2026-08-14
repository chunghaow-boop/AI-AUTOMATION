#!/usr/bin/env python3
"""
BUILD_LC300_CINEMATIC — the SAME 4 clips, re-cut as car_cinematic instead of car_review.

WHY A SECOND BUILD OF THE SAME FOOTAGE
  The first cut applied car_review grammar (median 3.60s, cut to sentence) to footage that
  was always cinematic. Measured against the real references, with DECLARED cuts so the
  same-palette-blind detector could not flatter it:

      cuts_per_min      21.4  vs  30.7      -30%
      shot_median       2.47  vs   1.32     +87%
      rate_variation    0.01  vs   1.50     -99%   <- a perfect metronome
      cuts_on_beat       0.0%

  Against the car_cinematic profile proper the median target is 0.77s, so 2.47s is 3.2x
  too slow - the exact failure PILLAR-PROFILES names as the project's most consistent.

THE ORDER THAT MATTERS: MUSIC FIRST.
  Cut-to-beat means the grid exists BEFORE any picture is placed. The first build made
  picture and laid a bed under it afterwards, which is why cuts_on_beat was 0.0%.

      phonk.py   --bpm 150 --dur 16      bed, measured sub 57.0% / cowbell 6.0%
      beatplan.py --bpm 150 --dur 16     17 shots, burst-hold-burst-hold-burst
      -> every boundary is ON the grid by construction

Usage
  python3 build_lc300_cinematic.py
"""
import os, sys, subprocess, json
import statistics as st

HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.join(HERE, "work", "RESTORE")
TOOLS = os.path.join(ROOT, "tools")
TMP   = os.path.join(HERE, "_lc300c_tmp")
OUT   = os.path.join(HERE, "LC300ZX_CINEMATIC_v1.mp4")
BED   = os.path.join(TOOLS, "BGM_phonk_150.wav", "BGM_phonk_150.wav")  # phonk.py treats --out as a DIRECTORY and names the file itself
sys.path.insert(0, TOOLS)

W, H, FPS = 720, 1280, 30
BPM, TOTAL = 150.0, 16.0

SRC = {"A": "LC300_B_front.mp4",        # exterior front 3/4, lamps ignite   showroom
       "B": "LC300_C_wheel.mp4",        # 20in alloy + flank                 showroom
       "C": "LC300_D_interior.mp4",     # front cabin, 12.3in screen         interior
       "D": "LC300_E_rear_screens.mp4", # rear dual 11.6in screens           interior
       "E": "LC300_F_rolling.mp4",      # DRIVING, wet road, night           NIGHT
       "F": "LC300_G_rear_night.mp4"}   # rear 3/4, taillights lit, night    NIGHT

# COVERAGE RULE: distinct sources >= shots / 2.5.  14 / 2.5 = 6.
# The 4-source version put 5 of 14 shots on one clip and 7 of 13 cuts had histogram
# correlation > 0.95 - the image barely changed, so the cutting read as a stutter.
# Cut rate has to be EARNED by coverage.

# EXPOSURE-ORDERED. Measured source brightness / motion:
#   A 81.2 / 8.10   B 73.7 / 14.58   C 51.9 / 16.90
#   D 46.8 / 7.00   E 53.9 / 15.61   F 51.9 / 7.73
#
# THREE FIXES FROM THE GRADED v1, all measured, none by taste:
#  1 EXPOSURE FLICKER - v1 alternated A(65)/B(41)/A(68)/B(40) at 0.8s and read as a
#    strobe. 6 of 12 cuts swung >18. Shots are now grouped by brightness tier, so the
#    only jumps >18 are the section boundary at 3->4 (which carries a blend) and the
#    loop at 12->13 (which is the reset, and inherent to the arc).
#    clipsense.py measures brightness[] with the docstring "for matching exposure across
#    a cut". Nothing had ever read it.
#  2 THE HOOK WAS THE QUIETEST SHOT - A at motion 8.10 opened, while the highest-motion
#    material sat third. B (14.58) now opens.
#  3 THE FIRST HOLD DIED - D (motion 7.00) was on a 3.2s hold, so the music carried on
#    while the picture stopped. C (16.90) takes it; E (15.61) keeps the second hold.
MAP = [
    ("B", 1.00, .50, .50),  # 0  BURST A  SHOWROOM  HOOK - wheel, highest exterior motion
    ("A", 1.00, .50, .50),  # 1                     front wide
    ("B", 1.90, .50, .55),  # 2                     punch: alloy spokes
    ("A", 1.95, .50, .36),  # 3                     punch: triple lamp cluster
    ("D", 1.00, .50, .50),  # 4            INTERIOR step inside, rear screens
    ("C", 1.00, .50, .50),  # 5  HOLD 3.2s          CABIN REVEAL - motion 16.9, sustains
    ("D", 1.90, .50, .42),  # 6  BURST B            punch: screen detail
    ("C", 1.85, .40, .45),  # 7                     punch: 12.3in screen
    ("F", 1.00, .50, .50),  # 8            NIGHT    out after dark, rear 3/4
    ("E", 1.90, .50, .45),  # 9                     punch: lamps at speed
    ("F", 1.85, .50, .55),  # 10                    punch: taillight macro
    ("E", 1.00, .50, .50),  # 11 HOLD 3.2s          ROLLING - motion 15.6, the payoff
    ("F", 1.90, .50, .40),  # 12 BURST C            punch: tail at speed
    ("B", 1.00, .50, .50),  # 13           SHOWROOM LOOP back to frame 0
]


def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def dur(p):
    _, o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"')
    try:
        return float(o.strip().splitlines()[0])
    except Exception:
        return 0.0


def adjacent_check(segs, thresh=0.95):
    """LEDGER D3 - 'coverage crops produced repetition, not variety', fix never built.

    USE HISTOGRAM CORRELATION, NOT PIXEL DIFFERENCE. A punch-in of the same shot moves
    every pixel, so mean|diff| scores it 23-62 and calls it fine, while the viewer sees
    the same image twice. Measured on the 4-source cut: mean|diff| flagged 0 of 13 cuts;
    hist-corr flagged 7. Same trap as ledger E3 - optical flow was the wrong proxy for
    'looks alive'.
    """
    import cv2, numpy as np
    def firstframe(p):
        c = cv2.VideoCapture(p)
        ok, f = c.read()
        c.release()
        return cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (96, 171)) if ok else None
    frames = [firstframe(s) for s in segs]
    bad = []
    for i in range(len(frames) - 1):
        a, b = frames[i], frames[i + 1]
        if a is None or b is None:
            continue
        ha = cv2.calcHist([a], [0], None, [64], [0, 256])
        hb = cv2.calcHist([b], [0], None, [64], [0, 256])
        cv2.normalize(ha, ha); cv2.normalize(hb, hb)
        corr = float(cv2.compareHist(ha, hb, cv2.HISTCMP_CORREL))
        if corr > thresh:
            bad.append((i, i + 1, corr))
    pct = 100 * len(bad) / max(1, len(frames) - 1)
    print(f"  adjacent-shot check: {len(bad)}/{len(frames)-1} cuts barely change "
          f"the image ({pct:.0f}%)")
    for i, j, c in bad:
        print(f"    x shot {i} -> {j}  hist-corr {c:.2f}")
    if pct > 25:
        print(f"  !! {pct:.0f}% of cuts deliver no new image. The cut rate is not EARNED")
        print(f"  !! by the coverage. Generate more distinct sources or cut less.")
        return False
    return True


def shot_match(segs, tol=10.0, max_gain=0.10):
    """Pull each segment's exposure toward the running level. This is shot matching -
    what a colourist does before anything else.

    WHY REORDERING BY SOURCE BRIGHTNESS WAS NOT ENOUGH
      v2 grouped shots by the SOURCE clip's average brightness. Measured at the actual
      cuts, the first four still swung 28/35/34/35. The reason: a 1.90x punch-in crops
      into the DARK part of the frame - tyre, lamp housing - so source B averages 73.7
      while its punch renders at 50. The source average is the wrong statistic; only the
      rendered segment tells the truth.

    Correction is clamped to +/-0.085 so it matches, never relights.
    """
    import cv2, numpy as np

    def level(p):
        c = cv2.VideoCapture(p); v = []
        while True:
            ok, f = c.read()
            if not ok: break
            v.append(cv2.cvtColor(cv2.resize(f, (96, 171)), cv2.COLOR_BGR2GRAY).mean())
        c.release()
        return float(np.mean(v)) if v else None

    lv = [level(s) for s in segs]
    if any(x is None for x in lv):
        print("  !! could not measure a segment - SKIPPING shot match")
        return segs
    target = float(np.median(lv))
    print(f"  target level {target:.1f}  (median of {len(segs)} shots)")
    out = []
    fixed = 0
    for i, (p, l) in enumerate(zip(segs, lv)):
        d = target - l
        if abs(d) <= tol:
            out.append(p); continue
        gain = max(-max_gain, min(max_gain, d / 255.0 * 1.9))
        o = p.replace(".mp4", "_m.mp4")
        spec = f"{gain:.4f}"
        sf = o + ".spec"
        if os.path.exists(o) and os.path.exists(sf) and open(sf).read() == spec:
            out.append(o); fixed += 1; continue
        rc, err = sh(f'ffmpeg -y -v error -i "{p}" -vf "eq=brightness={gain:.4f},setsar=1" '
                     f'-an -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p "{o}"')
        if rc == 0 and os.path.exists(o):
            open(sf, "w").write(spec)
        if rc != 0 or not os.path.exists(o):
            print(f"  !! shot {i} match FAILED - keeping unmatched: {err.strip()[:60]}")
            out.append(p); continue
        nl = level(o)
        print(f"  shot {i:2d}  {l:5.1f} -> {nl:5.1f}  (gain {gain:+.3f})")
        out.append(o); fixed += 1
    print(f"  {fixed}/{len(segs)} shots matched")
    return out


def main():
    print("=" * 66)
    print("BUILD: LC300 ZX - CINEMATIC re-cut (music first)")
    print("=" * 66)

    miss = [f for f in SRC.values() if not os.path.exists(os.path.join(HERE, f))]
    if miss:
        print("!! MISSING:", ", ".join(miss))
        return 1
    if not os.path.exists(BED):
        print(f"!! no bed at {BED}. Run: python3 tools/phonk.py --bpm 150 --dur 16")
        return 1
    os.makedirs(TMP, exist_ok=True)

    import beatplan, clipsense, fx, rhythm
    # PHASE, not just tempo. The bed's first transient is at ~163ms - there is NO
    # downbeat at t=0. rhythm.py returned OFF-BEAT with a CONSTANT -171.2ms deviation,
    # which is the signature of two grids, not of sloppy cutting. Trim the bed so its
    # first hit lands on t=0 and the picture grid becomes the music grid.
    try:
        _x = rhythm.pcm(BED)
        _f, _t = rhythm.stft_flux(_x)
        _on = rhythm.pick_onsets(_f, _t)
        BED_OFFSET = float(_on[0]) if len(_on) else 0.0
    except Exception as e:
        BED_OFFSET = 0.0
        print(f"  !! could not measure bed phase ({str(e)[:40]}) - assuming 0. "
              f"Cuts may sit off the hits.")
    print(f"  bed phase: first transient at {BED_OFFSET*1000:.0f}ms -> trimming the bed")

    shots, beat = beatplan.plan(BPM, TOTAL, hold_beats=8)   # hold=5 gave 60 cuts/min
                                                        # vs a 44.7 target; 8 gives 48.7
    print(f"\n[1/5] grid   {len(shots)} shots @ {BPM:.0f} BPM, beat {beat*1000:.0f}ms")
    if len(shots) != len(MAP):
        print(f"  !! plan has {len(shots)} shots but MAP has {len(MAP)}. STOP.")
        return 1

    sense = {}
    for k, f in SRC.items():
        sense[k] = clipsense.analyse(os.path.join(HERE, f))

    print(f"\n[2/5] segments  (best_in from clipsense, reframe in SPACE not time)")
    shot_tin = {}
    used_peaks = {k: set() for k in SRC}
    rep_span = {k: 0 for k in SRC}
    segs, cuts, t = [], [], 0.0
    for i, ((start, d, kind), (key, cs, cx, cy)) in enumerate(zip(shots, MAP)):
        src = os.path.join(HERE, SRC[key])
        c = sense[key]
        # CUT ON ACTION (editsense R4). clipsense returns action_peaks_s - local maxima
        # of motion, "the moments a pro cuts on or into" - and NOTHING had ever read it.
        #
        # The old rule (best_in + rep*0.45) never reached past ~1.3s into a 5.04s clip, so
        # every peak from 2-4.5s was thrown away: the lamps igniting late in A, the car
        # passing streetlights late in E. Measured, shots 0 / 1 / 9 contained NO peak at
        # all - and shot 0 is the HOOK.
        #
        # Now each shot is centred on the nearest UNUSED peak, so the good moment lands
        # inside the window instead of just outside it.
        peaks = [pk for pk in c["action_peaks_s"] if pk not in used_peaks[key]]
        if not peaks:
            peaks = list(c["action_peaks_s"])
        want = c["best_in_s"] + rep_span[key] * 1.25
        pk = min(peaks, key=lambda x: abs(x - want))
        used_peaks[key].add(pk)
        rep_span[key] += 1
        tin = max(0.0, pk - d * 0.42)          # peak sits ~40% into the shot
        shot_tin[i] = tin
        if c["duration"] < tin + d:
            tin = max(0.0, c["duration"] - d - 0.05)
        o = os.path.join(TMP, f"c{i:02d}.mp4")
        # CACHE keyed on the FULL spec, not just duration. A duration-only key silently
        # reused untreated segments once (ledger B2) - the crop is part of the identity.
        spec = f"{SRC[key]}|{tin:.3f}|{d:.3f}|{cs}|{cx}|{cy}|frames"
        sf = o + ".spec"
        if (os.path.exists(o) and os.path.exists(sf)
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
        # FRAME-EXACT, not time-approximate. `-t 0.80` on a 24fps source yields 0.834s
        # once resampled to 30fps - a whole extra frame per shot. Measured, the actual
        # cut times drifted +34ms per shot: planned 0.8/1.6/2.4 rendered as
        # 0.867/1.701/2.535. By the end the picture is ~130ms behind the music, a third
        # of a beat at 150 BPM. -frames:v pins it exactly.
        nfr = int(round(d * FPS))
        rc, err = sh(f'ffmpeg -y -v error -ss {tin:.3f} -i "{src}" -vf "{vf}" '
                     f'-frames:v {nfr} -an -c:v libx264 -crf 18 -preset veryfast '
                     f'-pix_fmt yuv420p "{o}"')
        if rc != 0 or not os.path.exists(o):
            print(f"  !! shot {i} FAILED: {err.strip()[:80]}")
            return 1
        got = dur(o)
        if abs(got - d) > 0.10:
            print(f"  !! shot {i} is {got:.2f}s, asked {d:.2f}s - SHORT, not silently kept")
        open(sf, "w").write(spec)
        segs.append(o)
        if i:
            cuts.append(round(t, 3))
        t += d
    print(f"  {len(segs)} shots, {t:.2f}s, {len(cuts)} cuts - ALL on the grid")

    # SHOT MATCH FIRST, then blend. Matching after the blend only sees merged segments
    # (10 instead of 14) and the averages hide the swings it is meant to catch.
    print(f"\n[2b/5] shot match  (exposure)")
    segs = shot_match(segs)

    # blends only at the two HOLD exits = section punctuation, 240-560ms band.
    # mask_slice, never dip: dip fades through black and trips the blank-frame gate.
    print(f"\n[3/5] blends  mask_slice at the HOLD exits only")
    # 2 blends read as 9% to the DETECTOR (qc.py measures, it does not take my word) and
    # the gate wants >=10% against a 20% target. Reference range is 6-33%, and the study
    # says blends are WIDE section punctuation - so add two more at section boundaries,
    # not sprinkled through the bursts.
    hold_idx = [i for i, (_s, _d, k) in enumerate(shots) if k == "hold"]
    hold_idx += [3, 7]   # the two SECTION boundaries: showroom->interior, interior->night
    hold_idx = sorted(set(hold_idx))
    out, n = list(segs), 0
    for i in hold_idx:
        if i + 1 >= len(out) or out[i] is None or out[i + 1] is None:
            continue
        o = os.path.join(TMP, f"bx{i:02d}.mp4")
        try:
            fx.FX["mask_slice"](out[i], out[i + 1], o, d=0.40, W=W, H=H, fps=FPS)
            if os.path.exists(o) and dur(o) > 0.3:
                out[i] = o
                out[i + 1] = None
                n += 1
                print(f"  blend mask_slice at shot {i} -> {dur(o):.2f}s")
        except Exception as e:
            print(f"  !! mask_slice@{i}: {str(e)[:70]}")
    segs = [x for x in out if x]
    print(f"  {n} blend(s) = {100*n//max(1,len(MAP)-1)}%   target 20% (range 6-33%)")

    print(f"\n[3b/5] coverage")
    adjacent_check(segs)

    lst = os.path.join(TMP, "list.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    cut = os.path.join(TMP, "cut.mp4")
    rc, _ = sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c copy -an "{cut}"')
    if rc != 0 or dur(cut) < 1:
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c:v libx264 -crf 18 '
           f'-preset veryfast -pix_fmt yuv420p -an "{cut}"')

    # CRUSHED, not the review's flat grade. black 2.0 / saturation 91.5.
    # DO NOT DOUBLE-GRADE. The Seedance prompts asked for "crushed blacks, deep black
    # shadows, high contrast", so the footage ARRIVES graded. v1 then applied
    # contrast=1.16 + brightness=-0.035 on top and took pixels at value <4 from 7.7%
    # (ungraded cut) to 40.0%. Two fifths of every frame was destroyed detail, and it
    # bands badly after platform compression.
    #
    # black_point 2.0 is where the DARKEST PIXEL should sit. It is a target to measure
    # toward, not a filter to apply. Saturation only here; exposure is left alone.
    SAT, BRI = 1.70, 0.015
    print(f"\n[4/5] grade  saturation {SAT} only, brightness {BRI:+.3f} "
          f"(v1 double-graded to 40% clipped)")
    graded = os.path.join(TMP, "graded.mp4")
    rc, _ = sh(f'ffmpeg -y -v error -i "{cut}" -vf '
               f'"eq=saturation={SAT}:brightness={BRI},setsar=1" '
               f'-c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -an "{graded}"')
    if rc != 0 or not os.path.exists(graded):
        print("  !! GRADE FAILED - DO NOT POST WITHOUT LOOKING")
        graded = cut

    # ---- CAPTIONS + CTA + AI DISCLOSURE ----------------------------------
    # Profile says captions are "lyric-synced, 1-2 words, huge, centre". Not sentences.
    # Every caption START is a declared cut, so text lands ON the grid with the picture.
    # "no CTA card on screen" is a recorded rejection - TWICE. So is caption design.
    # AI disclosure is non-negotiable on TikTok/Meta: an undisclosed AI persona risks a
    # platform penalty AND the trust the channel depends on.
    print(f"\n[4b/5] captions  1-2 words, on the grid, + CTA + AI label")
    FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
    if not os.path.exists(FONT):
        FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    # HIS NOTE: "the caption is literally blocking the whole video at the middle,
    # can't see the cars". Correct - 92-108px type at y=0.42 sits dead centre of a
    # 720x1280 frame, right where the car is. The subject is ALWAYS centre in these
    # shots, so centre is the one place text must never go.
    #
    # Moved to the LOWER THIRD at y=0.72 and cut ~30% in size. Still inside the 9:16
    # safe zone: TikTok/Reels UI eats roughly the bottom 20% (y>0.80) and top 15%.
    CARDS = [
        ("KING",         0.00, 1.60, 76, 0.72),
        ("LC300 ZX",     4.00, 3.20, 68, 0.72),
        ("GRADE 5A",     8.00, 1.60, 66, 0.72),
        ("RM400K",      11.20, 3.20, 74, 0.72),
        ("DM FOR PRICE", 14.40, 0.55, 56, 0.72),
    ]
    dt = []
    for txt, st_, ln, size, ypos in CARDS:
        dt.append(
            f"drawtext=fontfile='{FONT}':text='{txt}':fontcolor=white:fontsize={size}:"
            f"borderw=6:bordercolor=black@0.85:x=(w-text_w)/2:y=(h*{ypos}):"
            f"enable='between(t,{st_:.2f},{st_ + ln:.2f})'")
    # AI DISCLOSURE - his call: not burned into the frame any more.
    # Disclosure still HAPPENS, at the platform layer instead of the pixel layer:
    # TikTok and Meta both carry an "AI-generated content" toggle in the upload flow,
    # which labels the post natively. That satisfies the requirement without covering
    # the image, and it is what most AI creators actually use.
    # REMEMBER TO SET THAT TOGGLE ON EVERY UPLOAD - it is now a human step, not an
    # automatic one, which is exactly the kind of step that gets forgotten.
    capped = os.path.join(TMP, "capped.mp4")
    rc, err = sh(f'ffmpeg -y -v error -i "{graded}" -vf "{",".join(dt)}" '
                 f'-c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -an "{capped}"')
    if rc == 0 and os.path.exists(capped) and dur(capped) > 1:
        graded = capped
        print(f"  {len(CARDS)} cards, lower third y=0.72 (was 0.42, centre)")
        print(f"  NO burned-in AI label - set the platform AI toggle at upload")
    else:
        # B1: a drawtext path failure once shipped a caption-less video REPORTING SUCCESS
        print(f"  !! CAPTIONS FAILED: {err.strip()[:100]}")
        print(f"  !! DO NOT POST THIS FILE - no captions, no CTA")

    # ---- SFX LAYER -------------------------------------------------------
    # "no sfx on actions" is a recorded rejection. A bed alone means ZERO transient
    # design on cuts, which is core phonk car-edit vocabulary, not decoration.
    # sfxgen synthesises whoosh/impact/sub_drop - no assets, no licence risk.
    print(f"\n[5a/5] sfx  whoosh on burst cuts, impact at section boundaries")
    vd = dur(graded)
    sfx_path = os.path.join(TMP, "sfx.wav")
    HAVE_SFX = False
    try:
        import sfxgen, numpy as _np
        SR = sfxgen.SR
        n = int(vd * SR) + SR
        track = _np.zeros(n)

        def place(x, at, gain):
            a = int(at * SR); b = min(a + len(x), n)
            if a < 0 or b <= a: return
            track[a:b] += x[:b - a] * gain

        section = {cuts[i] for i in (3, 7) if i < len(cuts)}
        holds   = {cuts[i] for i in (4, 10) if i < len(cuts)}
        nw = ni = 0
        for c in cuts:
            if c in section:
                place(sfxgen.impact(0.7), c - 0.02, 0.55); ni += 1
            elif c in holds:
                place(sfxgen.sub_drop(1.4), c - 0.05, 0.42); ni += 1
            else:
                # LEAD the cut - a whoosh RESOLVES on the cut, it does not start there
                place(sfxgen.whoosh(0.30, up=True), max(0.0, c - 0.22), 0.34); nw += 1
        pk = float(_np.max(_np.abs(track))) or 1.0
        sfxgen._w(sfx_path, track / pk * 0.72)
        HAVE_SFX = os.path.exists(sfx_path)
        print(f"  {nw} whoosh + {ni} impact/drop across {len(cuts)} cuts")
    except Exception as e:
        print(f"  !! SFX FAILED: {str(e)[:80]}")
        print(f"  !! SHIPPING WITH BED ONLY - cuts have NO transient design")

    print(f"\n[5/5] sound  phonk bed 150 BPM" + ("  + sfx" if HAVE_SFX else ""))
    A = "aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo"
    if HAVE_SFX:
        f = (f"[1:a]atrim={BED_OFFSET:.4f}:{vd + BED_OFFSET:.2f},asetpts=N/SR/TB,{A},"
             f"volume=12.0dB[bedraw];"
             f"[2:a]atrim=0:{vd:.2f},asetpts=N/SR/TB,{A},volume=13.5dB,asplit=2[sfx][key];"
             # HIS NOTE: "i dont see any foley in it". Measured: the SFX sat 15.2 dB
             # under the bed and 11-16 dB down at every cut - completely masked. It was
             # rendered and mixed to inaudible, which is worse than absent because the
             # build reported success. Now +13.5 dB, and the BED DUCKS under it via
             # sidechain, which is how a whoosh is supposed to make room for itself.
             f"[bedraw][key]sidechaincompress=threshold=0.05:ratio=8:attack=4:"
             f"release=180:makeup=1[bed];"
             f"[bed][sfx]amix=inputs=2:duration=first:normalize=0,"
             f"alimiter=limit=0.76:level=disabled:attack=5:release=50[aout]")
        cmd = (f'ffmpeg -y -v error -i "{graded}" -stream_loop -1 -i "{BED}" -i "{sfx_path}" '
               f'-filter_complex "{f}" -map 0:v -map "[aout]" -c:v copy -c:a aac '
               f'-b:a 192k -t {vd:.2f} "{OUT}.part.mp4"')
    else:
        f = (f"[1:a]atrim={BED_OFFSET:.4f}:{vd + BED_OFFSET:.2f},asetpts=N/SR/TB,{A},"
             f"volume=11.0dB,alimiter=limit=0.76:level=disabled:attack=5:release=50[aout]")
        cmd = (f'ffmpeg -y -v error -i "{graded}" -stream_loop -1 -i "{BED}" '
               f'-filter_complex "{f}" -map 0:v -map "[aout]" -c:v copy -c:a aac '
               f'-b:a 192k -t {vd:.2f} "{OUT}.part.mp4"')
    rc, err = sh(cmd)
    # atomic: a run killed mid-write left a 532KB file with no moov atom,
    # which ffprobe then refused entirely. Never publish a partial file.
    if rc == 0 and os.path.exists(OUT + ".part.mp4") and dur(OUT + ".part.mp4") > 1:
        os.replace(OUT + ".part.mp4", OUT)
    if rc != 0:
        print(f"  !! MIX FAILED: {err.strip()[:110]}  - SHIPPING SILENT, DO NOT POST")
        sh(f'ffmpeg -y -v error -i "{graded}" -c copy "{OUT}"')

    # ACTUAL cut times, measured from the rendered segments AFTER blending.
    #
    # THE BUG THIS FIXES: `cuts` came from beatplan - the PLAN. Blending merges each
    # pair into one segment, so every boundary after a blend shifts, and the planned
    # times stop pointing at real cuts. Verifying against them compared two frames
    # INSIDE the same shot and called it a repeat (hist-corr 0.999 at 14.40s), and the
    # cut-to-music figures were measured at positions that no longer existed.
    #
    # Same disease as the stale-file trap: measuring the wrong thing precisely.
    actual, tt = [], 0.0
    for sgi in segs:
        tt += dur(sgi)
        actual.append(round(tt, 3))
    actual = actual[:-1]                      # last boundary is the end of the file
    json.dump({"cuts": actual, "planned": cuts, "bpm": BPM, "beat": beat},
              open(os.path.join(HERE, "lc300c_cuts.json"), "w"), indent=1)
    print(f"  declared cuts: {len(actual)} ACTUAL post-blend boundaries "
          f"({len(cuts)} were planned)")

    # peak manifest for verify.py check 7
    try:
        pm = []
        for i, (key, _cs, _cx, _cy) in enumerate(MAP):
            c = sense[key]
            d_ = 3.2 if shots[i][2] == "hold" else 0.8
            tin_ = shot_tin.get(i)
            has = any(tin_ <= pk <= tin_ + d_ for pk in c["action_peaks_s"]) if tin_ is not None else False
            pm.append({"shot": i, "src": key, "tin": tin_, "has_peak": has})
        json.dump(pm, open(os.path.join(TMP, "manifest_peaks.json"), "w"), indent=1)
    except Exception as e:
        print(f"  !! peak manifest failed: {str(e)[:60]}")

    print(f"\n  -> {OUT}   {dur(OUT):.2f}s")
    lens = [d for _s, d, _k in shots]
    print(f"     median shot {st.median(lens):.2f}s  target 0.77")
    print(f"     cuts/min    {len(cuts)/(t/60):.1f}  target 44.7")
    print(f"     declared cuts written to lc300c_cuts.json for reverse.py --mine-cuts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
