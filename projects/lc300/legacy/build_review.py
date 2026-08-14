#!/usr/bin/env python3
"""
BUILD_LC300 — Toyota Land Cruiser 300 ZX review, 720p 9:16.

TWO STAGES, ON PURPOSE (his call, 2026-07-31):
    "analyze which is the visual hook, which is the content and cta, categorise them,
     stitch them in order first then fix it that way, then only start the editing for
     the effects, sound, transitions and other stuff"

That is the right order and it is not how build_kk / build_crown / build_s450 work. Those
are hand-typed timelines - clipsense.py's own docstring calls that out: "Nothing in the
footage influenced a single cut. A renderer, not an editor." This script chooses the order
from MEASURED features instead.

    python3 build_lc300.py structure    -> ordered spine, no effects. LOOK AT IT.
    python3 build_lc300.py polish       -> transitions, grade, gates

CLASSIFICATION IS MECHANICAL, NOT TASTE
    hook     highest motion_mean, penalised by stillness_head_s
             (dead time at the head is what makes AI clips feel slow - clipsense docstring)
    cta      lowest motion_mean = the calmest frame, the one that can carry text
    content  everything else, ordered WIDE -> CLOSE, which is review grammar:
             establish the car, then earn the detail

TARGETS - car_review, n=7, measured from his references
    median shot 3.60s | cuts/min 14.3 | blended 16% | black 8.0 | saturation 52.9
    NOTE 30s is BELOW the measured 58-107s range. qc.py profile gates shot median and
    blend %, not duration, so it will pass - but there is no measured evidence for a 30s
    review. It is a teaser. Flagged, not hidden.
"""
import os, sys, subprocess, json, glob

HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.join(HERE, "work", "RESTORE")
TOOLS = os.path.join(ROOT, "tools")
TMP   = os.path.join(HERE, "_lc300_tmp")
SPINE = os.path.join(HERE, "LC300ZX_SPINE.mp4")
FINAL = os.path.join(HERE, "LC300ZX_30S_v1.mp4")
PLATE = os.path.join(HERE, "lc300zx.png")
sys.path.insert(0, TOOLS)

W, H, FPS = 720, 1280, 30
TARGET_TOTAL = 30.0
SIZE_RANK = {"wide": 0, "medium": 1, "close": 2}


def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def dur(p):
    _, o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"')
    try:
        return float(o.strip().splitlines()[0])
    except Exception:
        return 0.0


def sources():
    return sorted(glob.glob(os.path.join(HERE, "LC300_*.mp4")))


# ---------------------------------------------------------------- STAGE 1
def classify(clips):
    """hook / content / cta.

    THE FIRST VERSION OF THIS RANKED THE HOOK BY motion_mean AND WAS WRONG.
    It elected the INTERIOR as the hook (motion 2.791) and demoted the exterior
    establishing shot to CTA. That is backwards for a review - you establish the car,
    then earn the inside. The number was real; the inference was not.

    His own ledger already says this, E3:
        "optical flow was the wrong proxy for 'looks alive'
         -> stopped optimising it; view frames instead"

    In a tight cabin the camera sweeps past close geometry, so flow is huge while the
    shot is doing very little. Flow measures pixel displacement, not arrest.

    So ordering is now REVIEW GRAMMAR, declared in the filename role, not inferred from
    a proxy that has already failed once. Mechanical where mechanics work (in-points,
    lengths, blend placement); declared where it is a structural choice. Saying
    "measured" about a judgement call is how the 27%-blended over-read happened.
    """
    ROLE_ORDER = {"B": ("hook", 0),      # exterior front 3/4 - establish the car
                  "C": ("content", 1),   # wheel / flank detail
                  "D": ("content", 2),   # front cabin - the move inside
                  "E": ("cta", 3)}       # rear screens - the ZX proof, holds the end card
    out = []
    for c in clips:
        key = c["file"].split("_")[1][:1]
        role, rank = ROLE_ORDER.get(key, ("content", 9))
        out.append((rank, role, c))
    out.sort(key=lambda x: x[0])
    return [(role, c) for _rank, role, c in out]


def stage_structure():
    srcs = sources()
    if not srcs:
        print("!! no LC300_*.mp4 in this folder. See DOWNLOAD-THESE.md")
        return 1
    if not os.path.isdir(TOOLS):
        print(f"!! tools not found at {TOOLS}")
        return 1

    import clipsense
    os.makedirs(TMP, exist_ok=True)

    print("=" * 66)
    print("STAGE 1 - STRUCTURE   measure -> classify -> order -> stitch")
    print("=" * 66)

    clips = []
    for p in srcs:
        r = clipsense.analyse(p)
        if not r:
            print(f"  !! could not analyse {os.path.basename(p)}")
            continue
        r["path"] = p
        clips.append(r)

    print(f"\n{'clip':26s} {'dur':>5s} {'size':>6s} {'motion':>7s} {'bestIn':>7s} {'still':>6s}")
    for c in clips:
        print(f"{c['file']:26s} {c['duration']:5.1f} {c['shot_size']:>6s} "
              f"{c['motion_mean']:7.3f} {c['best_in_s']:7.2f} {c['stillness_head_s']:6.2f}")

    order = classify(clips)

    # TWO shots per clip: the front half, then a REFRAMED tighter second half.
    # This is the build_s450 pattern (18 shots from 4 generations) and it is the only
    # way to get 8 shots out of 4 clips without inventing footage.
    SHOTS = len(order) * 2
    per = round(min(TARGET_TOTAL / SHOTS, (min(c["duration"] for c in clips) - 0.1) / 2), 2)
    total = SHOTS * per

    print(f"\n  ROLE ASSIGNMENT (grammar-declared, see classify() docstring)")
    for role, c in order:
        print(f"    {role:8s} {c['file']:26s} motion {c['motion_mean']:6.3f} "
              f"in @ {c['best_in_s']:.2f}s")

    print(f"\n  {SHOTS} shots x {per:.2f}s = {total:.2f}s")
    if total < TARGET_TOTAL - 0.5:
        print()
        print("  " + "!" * 62)
        print(f"  !! CANNOT REACH {TARGET_TOTAL:.0f}s. Sources give {total:.2f}s.")
        print(f"  !! {len(clips)} clips x {min(c['duration'] for c in clips):.2f}s is all the")
        print(f"  !! footage that exists. Reaching {TARGET_TOTAL:.0f}s needs "
              f"{int((TARGET_TOTAL-total)/5)+1} more generation(s).")
        print(f"  !! NOT silently shipping a short file and calling it done.")
        print("  " + "!" * 62)
    print(f"     median shot {per:.2f}s | target 3.60s | his measured range 2.35-7.30s")
    print(f"     cuts/min {(SHOTS-1)/(total/60):.1f} | target 14.3 | range 5.0-22.5")

    # (scale, cx, cy) - second pass on each clip is punched in.
    #
    # REFRAME IN SPACE, NOT IN TIME. The first version advanced tin by `per` for the
    # second pass, which walked clip C off the wheel and onto 2.5s of blank white door
    # panel - measured sharpness 4.3-7.4 across f378-f453, which tripped the gate AND
    # was simply a boring shot. Seedance clips settle: the content is front-loaded and
    # the tail drifts. So both passes sit near best_in and differ by CROP.
    CROPS = [(1.00, 0.50, 0.50), (1.50, 0.50, 0.42)]
    segs = []
    for i, (role, c) in enumerate(order):
        for j, (cs, cx, cy) in enumerate(CROPS):
            o = os.path.join(TMP, f"sp{i}{j}_{role}.mp4")
            tin = c["best_in_s"] + (j * per * 0.35)   # small nudge, not a full shot
            if c["duration"] < tin + per:
                tin = max(0.0, c["duration"] - per - 0.05)
            if cs > 1.05:
                vf = (f"crop=iw/{cs}:ih/{cs}:(iw-iw/{cs})*{cx}:(ih-ih/{cs})*{cy},"
                      f"scale={W}:{H},fps={FPS},setsar=1")
            else:
                vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},fps={FPS},setsar=1")
            # KEEP the audio. Seedance generated ambient on every clip; the first pass
            # stripped it with -an and verdict came back true peak None / loudness None.
            rc, err = sh(f'ffmpeg -y -v error -ss {tin} -t {per} -i "{c["path"]}" '
                         f'-vf "{vf}" -c:v libx264 -crf 19 -preset veryfast '
                         f'-pix_fmt yuv420p -c:a aac -b:a 192k -ac 2 -ar 44100 "{o}"')
            if rc != 0 or not os.path.exists(o):
                print(f"  !! segment {i}{j} FAILED: {err.strip()[:80]}")
                return 1
            got = dur(o)
            if abs(got - per) > 0.15:
                print(f"  !! {os.path.basename(o)} is {got:.2f}s, asked {per:.2f}s "
                      f"- SHORT SEGMENT, not silently accepted")
            segs.append(o)

    lst = os.path.join(TMP, "spine.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    rc, _ = sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c copy -an "{SPINE}"')
    if rc != 0 or dur(SPINE) < 1:
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c:v libx264 -crf 19 '
           f'-preset veryfast -pix_fmt yuv420p -an "{SPINE}"')

    # MANIFEST, not a glob. Globbing _lc300_tmp picked up segments from a PREVIOUS run
    # and polish concatenated 12 segments into a 39.93s file from a 20.17s spine.
    # An explicit list cannot drift.
    json.dump({"segments": segs,
               "per": per,
               "order": [{"role": r, **{k: v for k, v in c.items() if k != "motion_curve"}}
                         for r, c in order]},
              open(os.path.join(TMP, "manifest.json"), "w"), indent=1)

    print(f"\n  -> {SPINE}   {dur(SPINE):.2f}s")
    print("\n  NO effects, NO sound, NO transitions, NO grade. That is deliberate.")
    print("  LOOK AT IT. If the order is wrong, say so - reordering is free.")
    print("  If it is right:  python3 build_lc300.py polish")
    return 0


# ---------------------------------------------------------------- STAGE 2
def stage_polish():
    if not os.path.exists(SPINE):
        print("!! no spine. Run:  python3 build_lc300.py structure")
        return 1
    import fx

    print("=" * 66)
    print("STAGE 2 - POLISH   transitions -> grade -> gates")
    print("=" * 66)

    mf = os.path.join(TMP, "manifest.json")
    if not os.path.exists(mf):
        print("!! no manifest. Run:  python3 build_lc300.py structure")
        return 1
    man = json.load(open(mf))
    segs = [s for s in man["segments"] if os.path.exists(s)]
    if len(segs) != len(man["segments"]):
        print(f"!! manifest lists {len(man['segments'])} segments, {len(segs)} on disk. STOP.")
        return 1
    spine_total = sum(dur(s) for s in segs)
    print(f"  {len(segs)} segments from manifest, {spine_total:.2f}s")

    # ONE blend, at the last seam before the CTA = section punctuation, not decoration.
    # 1 of N seams lands near the 16% target for this pillar.
    # NOT whip: fixed today but unproven on a real build, and a review does not want one.
    out = list(segs)
    i = max(0, len(out) - 2)
    o = os.path.join(TMP, "blend.mp4")
    n = 0
    # NOT dip. dip fades THROUGH BLACK - measured f519-f524 at mean 0.0, which is a
    # genuine blank-frame gate failure, not a false positive. mask_slice is an xfade
    # wipe: no black midpoint, and masking is in the researched car-edit vocabulary.
    try:
        fx.FX["mask_slice"](out[i], out[i + 1], o, d=0.40, W=W, H=H, fps=FPS)
        if os.path.exists(o) and dur(o) > 0.5:
            out[i] = o
            out[i + 1] = None
            n = 1
            print(f"  blend mask_slice at seam {i} -> {dur(o):.2f}s")
    except Exception as e:
        print(f"  !! dip: {str(e)[:70]}")
    segs = [x for x in out if x]
    print(f"  {n} blend(s) = {100*n//max(1,len(segs))}%   target 16%")

    lst = os.path.join(TMP, "poly.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    cut = os.path.join(TMP, "cut.mp4")
    rc, _ = sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c copy "{cut}"')
    if rc != 0 or dur(cut) < 1:
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c:v libx264 -crf 19 '
           f'-preset veryfast -pix_fmt yuv420p -an "{cut}"')

    print("\n  grade -> car_review (black 8.0 / saturation 52.9, NOT the cinematic crush)")
    graded = os.path.join(TMP, "graded.mp4")
    rc, _ = sh(f'ffmpeg -y -v error -i "{cut}" -vf "eq=saturation=0.88:brightness=0.02,'
               f'setsar=1" -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -an '
               f'"{graded}"')
    if rc != 0 or not os.path.exists(graded):
        print("  !! GRADE FAILED - shipping ungraded. DO NOT POST WITHOUT LOOKING.")
        graded = cut

    # ---- SOUND -------------------------------------------------------------
    # The first pass built video-only (-an) and verdict returned true peak None /
    # loudness None - two hard gate failures caused by there being no audio track at
    # all. The Seedance clips DO carry ambient aac; stripping it was the error.
    # Bed under ambient, ducked, normalised to his band.
    print("\n  sound: source ambient + bed -> measured gain 7.2dB + limiter 0.62")
    amb = os.path.join(TMP, "amb.wav")
    ins, fl, k = [], [], 0
    for s in segs:
        rc, _ = sh(f'ffprobe -v error -select_streams a:0 -show_entries stream=codec_name '
                   f'-of csv=p=0 "{s}"')
        ins.append(f'-i "{s}"')
        fl.append(f"[{k}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a{k}]")
        k += 1
    cc = "".join(f"[a{x}]" for x in range(k))
    sh(f'ffmpeg -y -v error {" ".join(ins)} -filter_complex '
       f'"{";".join(fl)};{cc}concat=n={k}:v=0:a=1[out]" -map "[out]" "{amb}"')

    bed = None
    for cand in ("BGM_auto_hero.wav", "BGM_full_loop.wav"):
        p = os.path.join(ROOT, "bgm", cand)
        if os.path.exists(p):
            bed = p
            break

    vdur = dur(graded)
    mixed = os.path.join(TMP, "mixed.mp4")
    if bed and os.path.exists(amb):
        print(f"    bed: {os.path.basename(bed)}")
        f = (f"[1:a]atrim=0:{vdur:.2f},asetpts=N/SR/TB,volume=0.85,"
             f"aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[amb];"
             f"[2:a]atrim=0:{vdur:.2f},asetpts=N/SR/TB,volume=0.30,"
             f"aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[bed];"
             f"[amb][bed]amix=inputs=2:duration=first:normalize=0,"
             f"volume=7.2dB,alimiter=limit=0.62:level=disabled:attack=5:release=50[aout]")
        # MEASURED, not trusted: single-pass loudnorm undershot twice (-10.2 then
        # -10.4 LUFS against a -9.5..-6.5 band) and left true peak at -0.9. Swept
        # gain/limit and measured each: 6.0dB/0.62 -> -9.6/-1.7 (still 0.1 low),
        # 7.2dB/0.62 -> -9.4 LUFS / -1.7 dBTP. Both gates pass. B4 applies here:
        # level=disabled is what makes alimiter actually limit.
        rc, err = sh(f'ffmpeg -y -v error -i "{graded}" -i "{amb}" -stream_loop -1 -i "{bed}" '
                     f'-filter_complex "{f}" -map 0:v -map "[aout]" -c:v copy -c:a aac '
                     f'-b:a 192k -t {vdur:.2f} "{mixed}"')
        if rc != 0 or not os.path.exists(mixed):
            print(f"    !! MIX FAILED: {err.strip()[:110]}")
            print("    !! DO NOT POST - this file has no sound")
            mixed = graded
    else:
        print("    !! no bed found in work/RESTORE/bgm - SHIPPING WITHOUT SOUND")
        mixed = graded

    graded = mixed
    sh(f'ffmpeg -y -v error -i "{graded}" -c copy "{FINAL}"')
    got = dur(FINAL)
    print(f"\n  -> {FINAL}   {got:.2f}s")
    if abs(got - spine_total) > 1.0:
        print(f"  !! FINAL is {got:.2f}s but the spine was {spine_total:.2f}s. "
              f"Something added footage. STOP AND LOOK.")

    print("\n" + "=" * 66)
    print("GATES")
    print("=" * 66)
    ref = f' --reference "{PLATE}"' if os.path.exists(PLATE) else ""
    if not ref:
        print("  (no lc300zx.png - subject gate falls back to human sign-off)\n")
    rc, o = sh(f'cd "{ROOT}" && python3 "{os.path.join(TOOLS, "verdict.py")}" '
               f'--video "{FINAL}"{ref} --no-quarantine 2>&1')
    print(o.strip() or f"  !! verdict.py produced NO OUTPUT (rc={rc}) - gate did not run")
    rc, o = sh(f'cd "{ROOT}" && python3 "{os.path.join(TOOLS, "qc.py")}" profile '
               f'--video "{FINAL}" --pillar car_review 2>&1')
    print(o.strip() or f"  !! qc.py produced NO OUTPUT (rc={rc}) - gate did not run")

    print("\n  STILL MISSING, and the gate cannot catch it: no VO, no bed, no foley,")
    print("  no captions, no CTA card. Those need Nev, or a decision to go VO-less.")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "structure"
    sys.exit(stage_structure() if cmd == "structure" else stage_polish())
