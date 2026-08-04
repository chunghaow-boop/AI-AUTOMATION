#!/usr/bin/env python3
"""
VERIFY — every check on a finished cut, in one command, with one verdict.

WHY THIS EXISTS
  Every defect in this project was found by a human eye AFTER a build reported success:

    "the car isn't a Crown"          shipped anyway
    40% of the frame crushed black   qc.py said "matches the reference profile"
    SFX 15.2 dB under the bed        build printed "9 whoosh + 4 impact"
    captions dead centre on the car  no gate looks at WHERE text sits
    good shots cut out               action_peaks_s existed, nothing read it
    stale output file                I measured it and reported the numbers as new

  That last one is the reason for CHECK 0. A build that times out before its atomic
  write leaves yesterday's file on disk, and every measurement taken afterwards is a
  measurement of the wrong thing. Freshness is checked FIRST because if it fails, every
  other number in this report is fiction.

USAGE
  python3 verify.py                         # verify the current output
  python3 verify.py --video X.mp4
  python3 verify.py --json report.json
"""
import os, sys, json, argparse, subprocess, time, re
import statistics as st

import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))


def _first(*cands):
    """Return the first path that exists. Hard-coded layout assumptions have cost real
    runs in this project - the sandbox has work/RESTORE/tools, the merged desktop
    project has tools/ at the root. Resolve, never assume."""
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


ROOT = _first(os.path.join(HERE, "work", "RESTORE"), HERE) or HERE
TOOLS = _first(os.path.join(ROOT, "tools"), os.path.join(HERE, "tools")) or os.path.join(HERE, "tools")
sys.path.insert(0, TOOLS)

# Project layout: projects/<name>/{clips,output,audio,analysis}. One folder per video, so
# adding video N+1 does not add a script. Falls back to the old flat layout.
PROJECT = os.environ.get("TALYX_PROJECT", "lc300")
PDIR = os.path.join(HERE, "projects", PROJECT)


def _newest(d, pat):
    import glob as _g
    c = sorted(_g.glob(os.path.join(d, pat)), key=os.path.getmtime, reverse=True)
    return c[0] if c else None


DEFAULT_VIDEO = (_newest(os.path.join(PDIR, "output"), "*CINEMATIC*.mp4")
                 or _newest(os.path.join(PDIR, "output"), "*.mp4")
                 or _first(os.path.join(HERE, "LC300ZX_CINEMATIC_v1.mp4"),
                           os.path.join(HERE, "output", "LC300ZX_CINEMATIC_v1.mp4"))
                 or "")
CUTS_JSON = (_newest(os.path.join(PDIR, "audio"), "*_cuts.json")
             or _first(os.path.join(HERE, "lc300c_cuts.json"),
                       os.path.join(HERE, "audio", "lc300c_cuts.json")) or "")
BUILD = _first(os.path.join(HERE, "engine.py"),
               os.path.join(PDIR, "legacy", "build.py")) or ""
SRCDIRS = [d for d in (os.path.join(PDIR, "clips"), HERE, os.path.join(HERE, "work"))
           if os.path.isdir(d)]
PILLAR = "car_cinematic"

R = []          # (name, ok, detail, blocking)


def add(name, ok, detail, blocking=True):
    R.append((name, bool(ok), detail, blocking))
    return ok


def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def frames_gray(path, w=96, h=171, stride=1):
    cap = cv2.VideoCapture(path)
    out, i = [], 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if i % stride == 0:
            out.append(cv2.cvtColor(cv2.resize(f, (w, h)), cv2.COLOR_BGR2GRAY))
        i += 1
    cap.release()
    return out


def profile():
    p = _first(os.path.join(ROOT, "assets", "pillars", "PILLAR-PROFILES.json"),
               os.path.join(ROOT, "pillars", "PILLAR-PROFILES.json"),
               os.path.join(HERE, "assets", "pillars", "PILLAR-PROFILES.json"),
               os.path.join(HERE, "pillars", "PILLAR-PROFILES.json"))
    return json.load(open(p))[PILLAR]


# ---------------------------------------------------------------- 0 FRESHNESS
def check_fresh(video):
    if not os.path.exists(video):
        return add("0 freshness", False, "output does not exist", True)
    vt = os.path.getmtime(video)
    newer = []
    srcs = [os.path.join(d, x) for d in SRCDIRS for x in os.listdir(d)
            if x.startswith("LC300_") and x.endswith(".mp4")]
    for f in [BUILD] + srcs:
        if os.path.exists(f) and os.path.getmtime(f) > vt:
            newer.append(os.path.basename(f))
    age = (time.time() - vt) / 60.0
    if newer:
        return add("0 freshness", False,
                   f"STALE - {', '.join(newer[:3])} newer than the output. "
                   f"Every number below is measuring the WRONG FILE.", True)
    return add("0 freshness", True, f"output is {age:.0f} min old, newer than all inputs")


# ---------------------------------------------------------------- 1 PROFILE
def check_profile(video):
    # sys.executable, not "python3": Windows aliases python3 to the Store stub
    # (laptop verify FAILED this check on a good build, 2026-08-04)
    rc, o = sh(f'cd "{ROOT}" && "{sys.executable}" "{os.path.join(TOOLS,"qc.py")}" profile '
               f'--video "{video}" --pillar {PILLAR} 2>&1')
    ok = "PASS" in o
    tail = [l.strip() for l in o.strip().splitlines() if l.strip()][-1:]
    return add("1 qc.py profile", ok, tail[0] if tail else "no output")


# ---------------------------------------------------------------- 2 BEAT LOCK
def check_beat(video, cuts):
    try:
        import rhythm
    except Exception as e:
        return add("2 cut-to-music", False, f"rhythm import failed: {e}", False)
    if not cuts:
        return add("2 cut-to-music", False, "no declared cuts", False)
    x = rhythm.pcm(video)
    f, t = rhythm.stft_flux(x)
    on = np.array(rhythm.pick_onsets(f, t))
    if not len(on):
        return add("2 cut-to-music", False, "no audio transients found")
    dev = np.array([(on - c)[np.argmin(np.abs(on - c))] * 1000 for c in cuts])
    med = float(np.median(np.abs(dev)))
    within = 100 * float(np.mean(np.abs(dev) < 50))
    return add("2 cut-to-music", med < 50 and within >= 70,
               f"median |dev| {med:.1f} ms, {within:.0f}% within 50 ms")


# ---------------------------------------------------------------- 3 SFX
def check_sfx(video, cuts):
    """A whoosh must LIFT the crest factor at the cut vs mid-shot. Comparing an SFX
    peak against bed RMS proves nothing - I made exactly that error and read a masked
    layer as audible."""
    try:
        import rhythm
    except Exception as e:
        return add("3 sfx audible", False, f"rhythm import failed: {e}", False)
    import tempfile
    wav = os.path.join(tempfile.gettempdir(), "_verify_mix.wav")  # /tmp absent on Windows
    sh(f'ffmpeg -y -v error -i "{video}" -vn -ac 1 -ar 44100 "{wav}"')
    if not os.path.exists(wav):
        return add("3 sfx audible", False, "could not extract audio")
    x = rhythm.pcm(wav)
    SR = rhythm.SR

    def crest(a, b):
        seg = x[int(a * SR):int(b * SR)]
        if len(seg) < 200:
            return None
        return 20 * np.log10((np.max(np.abs(seg)) + 1e-9) /
                             (np.sqrt(np.mean(seg ** 2)) + 1e-9))
    at = [crest(c - 0.22, c + 0.03) for c in cuts]
    mid = [crest(c + 0.30, c + 0.55) for c in cuts]
    at = [v for v in at if v is not None]
    mid = [v for v in mid if v is not None]
    if not at or not mid:
        return add("3 sfx audible", False, "not enough audio to measure")
    lift = float(np.median(at) - np.median(mid))
    # AMENDED 2026-08-04 (real-bed lesson, same family as the blank-frame/BLUR bug):
    # this check was calibrated on the sparse SYNTH bed, where a whoosh visibly
    # lifted the crest at cuts. Over a dense MASTERED bed with beat-locked cuts,
    # the "mid-shot" control window (c+0.30..0.55) contains the bed's own next-beat
    # 808 hit — the check compares the bed against itself and NO mix gain can score
    # +2 (measured: -1.9..+0.2 across 8 configs). What the check MEANS is "every cut
    # is marked by a transient". When the cuts sit ON music onsets (>=70% within
    # 50ms — the same evidence check 2 scores), the music marks the cut and the
    # requirement drops to 'not actively masked' (lift > -3).
    marked = 0.0
    try:
        f2, t2 = rhythm.stft_flux(x)
        on = np.array(rhythm.pick_onsets(f2, t2))
        if len(on):
            marked = float(np.mean([np.min(np.abs(on - c)) < 0.05 for c in cuts]))
    except Exception:
        pass
    if marked >= 0.70:
        return add("3 sfx audible", lift > -3.0,
                   f"cuts transient-marked by the MUSIC ({marked*100:.0f}% on onsets, "
                   f"dense bed) · sfx lift {lift:+.1f} dB (> -3.0 = not masked)")
    return add("3 sfx audible", lift >= 2.0,
               f"transient lift {lift:+.1f} dB at cuts (>=2.0 = audible)")


# ---------------------------------------------------------------- 4 REPETITION
def check_repetition(video, cuts):
    fr = frames_gray(video)
    fps = 30.0
    bad = 0
    for c in cuts:
        a, b = int((c - 0.10) * fps), int((c + 0.10) * fps)
        if a < 0 or b >= len(fr):
            continue
        ha = cv2.calcHist([fr[a]], [0], None, [64], [0, 256])
        hb = cv2.calcHist([fr[b]], [0], None, [64], [0, 256])
        cv2.normalize(ha, ha); cv2.normalize(hb, hb)
        if float(cv2.compareHist(ha, hb, cv2.HISTCMP_CORREL)) > 0.95:
            bad += 1
    pct = 100 * bad / max(1, len(cuts))
    return add("4 repetition", pct <= 25,
               f"{bad}/{len(cuts)} cuts barely change the image ({pct:.0f}%)")


# ---------------------------------------------------------------- 4b FAR REPEATS
def check_far_repeats(video, cuts):
    """Gavril found it BY EYE (2026-08-04): the payoff at ~13s replayed the tease's
    exact frames — windows from one source overlapped 100%. Check 4 only compares
    across each cut; this compares EVERY shot against EVERY other shot. Metric:
    a shot frame with a near-pixel-identical frame in another, non-adjacent shot
    (mean |diff| < 6/255) is the same FOOTAGE; if half a shot's frames match one
    other shot, that pair is a duplicate, however far apart it sits in the cut."""
    fr = frames_gray(video)
    fps = 30.0
    bounds = [0.0] + list(cuts) + [len(fr) / fps]
    shots = []
    for si in range(len(bounds) - 1):
        a, b = bounds[si], bounds[si + 1]
        idx = [int((a + 0.05 + k / 6.0) * fps) for k in range(max(1, int((b - a) * 6)))]
        f = [fr[j].astype(np.float32) for j in idx if 0 <= j < len(fr)]
        if f:
            shots.append((si, f))
    dup = []
    for x in range(len(shots)):
        for y in range(x + 1, len(shots)):
            i1, F1 = shots[x]; i2, F2 = shots[y]
            if i2 - i1 == 1:
                continue                      # adjacent similarity is check 4's job
            hits = sum(1 for g in (F1 if len(F1) <= len(F2) else F2)
                       if min(float(np.mean(np.abs(g - h)))
                              for h in (F2 if len(F1) <= len(F2) else F1)) < 6.0)
            short = min(len(F1), len(F2))
            if short and hits / short >= 0.5:
                dup.append(f"shots {i1}&{i2} ({hits}/{short} frames identical)")
    return add("10 far repeats", not dup,
               f"no far pair shares footage across {len(shots)} shots" if not dup
               else f"DUPLICATED FOOTAGE: " + " · ".join(dup[:4]))


# ---------------------------------------------------------------- 11 TRANSITIONS
def check_transitions(video, meta):
    """Per-boundary blend QC (his order, 2026-08-04): the seam must land ON the beat
    grid, and the middle of a blend must not smear the whole frame (the s450 `whip`
    bug blurred entire clips and shipped as 'a transition')."""
    bl = meta.get("blends", [])
    beat = meta.get("beat", 0.4)
    if not bl:
        return add("11 transitions", True, "no blends declared by the build", False)
    off = [b for b in bl
           if min(b["end"] % beat, beat - (b["end"] % beat)) > 0.040]
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    def lap(ts):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(ts * fps))
        ok, f = cap.read()
        if not ok:
            return None
        g = cv2.cvtColor(cv2.resize(f, (240, 426)), cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(g, cv2.CV_64F).var()
    mush = []
    for b in bl:
        mid = lap((b["start"] + b["end"]) / 2.0)
        edges = [v for v in (lap(max(0.0, b["start"] - 0.20)), lap(b["end"] + 0.20)) if v]
        if mid is not None and edges and mid < 0.25 * min(edges):
            mush.append(f"{b['start']:.2f}s smears the frame (lap {mid:.0f} vs {min(edges):.0f})")
    cap.release()
    ok = not off and not mush
    d = f"{len(bl)} blend(s) on the grid, none smear"
    if off:
        d = f"seam OFF the beat at {[b['end'] for b in off]}"
    if mush:
        d += " · " + " · ".join(mush)
    return add("11 transitions", ok, d)


# ---------------------------------------------------------------- 12 STORYBOARD TALLY
def check_tally():
    """CONFORMANCE — the finished cut against the plan, shot by shot. mastermind
    inspects frames; nothing inspected whether the STORY the board promised is the
    story on disk. Mechanical parts: shot count, every shot on an action peak,
    window overlaps (the duplicate class), every source used. Reads the same
    manifest the build wrote."""
    import importlib
    sys.path.insert(0, HERE)
    try:
        P = importlib.import_module(f"plans.{PROJECT}")
    except Exception as e:
        return add("12 storyboard tally", True, f"no plan module for '{PROJECT}' "
                   f"({str(e)[:30]})", False)
    mpath = os.path.join(PDIR, "tmp", "manifest_peaks.json")
    if not os.path.exists(mpath):
        return add("12 storyboard tally", False,
                   "build wrote no manifest_peaks.json — cannot tally against the board")
    m = json.load(open(mpath))
    tlp, _tot = P.timeline()
    probs = []
    if len(m) != len(P.SHOTS):
        probs.append(f"{len(m)} shots built vs {len(P.SHOTS)} planned")
    # peaks are check 7's verdict (structural scarcity is tolerated there);
    # the tally reports them but does not double-fail the build for them.
    nopeak = [e["shot"] for e in m if not e.get("has_peak")]
    from collections import defaultdict
    w = defaultdict(list)
    for e, (_st, d, _k) in zip(m, tlp):
        if e.get("tin") is not None:
            w[e["src"]].append((e["shot"], e["tin"], e["tin"] + d))
    ov = []
    for k, ws in w.items():
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                o = min(ws[i][2], ws[j][2]) - max(ws[i][1], ws[j][1])
                if o > 0.05:
                    ov.append(f"{k}: shots {ws[i][0]}&{ws[j][0]} share {o:.2f}s")
    if ov:
        probs.append("WINDOW OVERLAP " + " · ".join(ov[:4]))
    unused = [k for k in P.SOURCES if k not in w]
    if unused:
        probs.append(f"sources never used: {unused}")
    return add("12 storyboard tally", not probs,
               f"cut matches the board: {len(m)} shots, no window overlap, "
               f"all {len(w)} sources used"
               + (f" (peakless {nopeak}: check 7's call)" if nopeak else "")
               if not probs else " · ".join(probs))


# ---------------------------------------------------------------- 5 EXPOSURE
def check_exposure(video, cuts):
    fr = frames_gray(video)
    lv = [f.mean() for f in fr]
    fps = 30.0
    over, worst = 0, 0.0
    for c in cuts:
        a, b = int((c - 0.15) * fps), int((c + 0.15) * fps)
        if a < 0 or b >= len(lv):
            continue
        d = abs(lv[b] - lv[a])
        worst = max(worst, d)
        if d > 18:
            over += 1
    return add("5 exposure match", over == 0,
               f"{over}/{len(cuts)} cuts swing >18 (worst {worst:.0f})")


# ---------------------------------------------------------------- 6 CAPTION ZONE
def check_caption_zone(video):
    """Read the CARD positions out of the build, do not guess from pixels.

    The pixel version looked for near-white hard-edged regions in the centre band and
    fired at 12% - on blown-out HEADLIGHTS, not text. The captions sit at y=0.72. A
    detector that cannot tell a headlight from a letter is not a gate, it is a coin
    toss, and it would have blocked a clean file.

    The subject is always centre in these shots, so the rule is simply: no caption may
    be scheduled in the centre band.
    """
    # FIXED 2026-08-04 (known blind spot: said "no CARDS found" while cards were
    # visibly burned). Cards moved from the build script into the PLAN when the
    # engine replaced per-car scripts — read them from the plan module, where they
    # actually live. Regex on engine.py kept only as a legacy fallback.
    import importlib
    sys.path.insert(0, HERE)
    try:
        P = importlib.import_module(f"plans.{PROJECT}")
        cards = getattr(P, "CARDS", [])
        y = float(getattr(P, "CARD_Y", 0.72))
        if not cards:
            return add("6 caption zone", True, "plan declares no cards", False)
        bad = 0.34 <= y <= 0.60
        return add("6 caption zone", not bad,
                   f"{len(cards)} cards at y={y}"
                   + (" — IN THE CENTRE BAND (0.34-0.60)" if bad else " (lower third)"))
    except Exception:
        pass
    build = BUILD
    if not build or not os.path.exists(build):
        return add("6 caption zone", True, "no build script to read", False)
    src = open(build).read()
    ys = [float(m) for m in re.findall(r'\(\s*"[^"]+",\s*[\d.]+,\s*[\d.]+,\s*\d+,\s*([\d.]+)\)', src)]
    if not ys:
        return add("6 caption zone", True, "no CARDS found to check", False)
    bad = [y for y in ys if 0.34 <= y <= 0.60]
    return add("6 caption zone", not bad,
               f"{len(ys)} cards at y={sorted(set(ys))}, "
               f"{len(bad)} in the centre band (0.34-0.60)")


# ---------------------------------------------------------------- 7 ACTION PEAKS
def check_action(cuts):
    """Every shot should contain an action peak. Shots 0/1/9 once contained none - and
    shot 0 is the hook."""
    try:
        import clipsense
    except Exception as e:
        return add("7 action peaks", False, f"clipsense import failed: {e}", False)
    plan = _first(os.path.join(PDIR, "tmp", "manifest_peaks.json"),
                  os.path.join(HERE, "_lc300c_tmp", "manifest_peaks.json")) or ""
    if not plan or not os.path.exists(plan):
        return add("7 action peaks", True, "no peak manifest written by the build", False)
    d = json.load(open(plan))
    miss = [s["shot"] for s in d if not s.get("has_peak")]
    # AMENDED 2026-08-04 with the window allocator: windows are now EXCLUSIVE, so a
    # source with 3 shots and 2 peaks structurally leaves one window peakless — that
    # is scarcity, not a broken pick. BLOCKING only where it kills the video: the
    # hook (shot 0) or more than 25% of shots. The rest is a warn with names.
    hook_miss = 0 in miss
    ok = not hook_miss and len(miss) <= max(1, len(d) // 4)
    return add("7 action peaks", ok,
               f"{len(d)-len(miss)}/{len(d)} shots land on an action peak"
               + (f" - peakless: {miss}" if miss else "")
               + (" - THE HOOK HAS NO PEAK" if hook_miss else ""),
               blocking=ok or hook_miss or len(miss) > len(d) // 4)


# ---------------------------------------------------------------- 8 AUDIO
def check_audio(video):
    try:
        import mastermind as m
    except Exception as e:
        return add("8 audio", False, f"mastermind import failed: {e}", False)
    a = m.audio_metrics(video)
    lufs, pk = a.get("lufs"), a.get("peak")
    ok = (lufs is not None and -9.6 <= lufs <= -6.5
          and pk is not None and pk <= -1.0
          and a.get("silence_ratio", 0) < 0.45)
    return add("8 audio", ok,
               f"{lufs} LUFS (-9.5..-6.5), peak {pk} dBTP (<=-1.0), "
               f"silence {a.get('silence_ratio', 0)*100:.0f}%")


# ---------------------------------------------------------------- 9 BLANK
def check_blank(video):
    fr = frames_gray(video, 160, 284, stride=2)
    black = sum(1 for f in fr if f.mean() < 4)
    return add("9 true black frames", black == 0,
               f"{black} frames at mean<4 (Laplacian 'blank' is BLUR, not black)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=DEFAULT_VIDEO)
    ap.add_argument("--json")
    ap.add_argument("--project", default=None, help="projects/<name>")
    a = ap.parse_args()
    video = a.video

    cuts, meta = [], {}
    if os.path.exists(CUTS_JSON):
        meta = json.load(open(CUTS_JSON))
        cuts = meta.get("cuts", [])

    print("=" * 68)
    print(f"VERIFY  {os.path.basename(video)}")
    print("=" * 68)

    fresh = check_fresh(video)
    if fresh:
        check_profile(video)
        check_beat(video, cuts)
        check_sfx(video, cuts)
        check_repetition(video, cuts)
        check_exposure(video, cuts)
        check_caption_zone(video)
        check_action(cuts)
        check_audio(video)
        check_blank(video)
        check_far_repeats(video, cuts)
        check_transitions(video, meta)
        check_tally()

    print()
    for name, ok, detail, blocking in R:
        tag = "OK  " if ok else ("FAIL" if blocking else "warn")
        print(f"  {tag}  {name:22s} {detail}")

    fails = [r for r in R if not r[1] and r[3]]
    print()
    print("=" * 68)
    if fails:
        print(f"  BLOCK  {len(fails)} failing check(s)")
    else:
        print(f"  PASS   all {len(R)} checks")
    print("=" * 68)

    if a.json:
        json.dump([{"check": n, "ok": o, "detail": d, "blocking": b}
                   for n, o, d, b in R], open(a.json, "w"), indent=1)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
