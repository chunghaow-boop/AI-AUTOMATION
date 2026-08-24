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
import glob          # FIX 2026-08-06: meta_pillar() used bare glob.glob but glob was
                     # only ever imported locally as _g inside two other functions, so
                     # meta_pillar raised NameError on EVERY call. The bare `except` in
                     # check 15 swallowed it, and the relight budget silently fell back
                     # to 18.0 for every pillar. car_cinematic_chill declares 14.0.
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
# PROJECT DEFAULT REMOVED 2026-08-12 (his catch: "why are the QC running against the
# lc300 cinematic plan?"). It used to fall back to "lc300" — the first film this
# system ever made — so ANY film verified without --project was silently judged
# against an early, flawed build's plan and profile. Judging new work against our own
# past work grandfathers its defects in as normal; 11 of 16 failures in the run he
# saw were artefacts of that mismatch. There is now NO fallback: the project is taken
# from the environment, from --project, or inferred from the video's own path, and if
# none of those resolve, check 5b fails LOUDLY instead of guessing.
def _project_from_path(p):
    """projects/<name>/… anywhere in the path → <name>"""
    try:
        parts = os.path.abspath(p).replace("\\", "/").split("/")
        i = parts.index("projects")
        return parts[i + 1] if i + 1 < len(parts) else None
    except Exception:
        return None


PROJECT = os.environ.get("TALYX_PROJECT") or ""
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


def _plan_pillar():
    """Read PILLAR out of plans/<PROJECT>.py.

    FIX 2026-08-08. This line used to read `PILLAR = "car_cinematic"`, full stop.
    Every travel_vlog project - desafarm, kundasang, mahua - was verified against
    the CAR profile. Check 1 shelled out to qc.py with --pillar car_cinematic, and
    check 5's exposure budget came from car footage shot in one light state.

    That is exactly his complaint: "it keeps on happening, especially when i switch
    frm vlog content to car review". The delivery gate itself was the thing carrying
    car numbers onto a travel vlog. planqc has read P.PILLAR since day one; verify
    never did.
    """
    for p in glob.glob(os.path.join(HERE, "plans", "*.py")):
        if os.path.basename(p)[:-3] == PROJECT:
            for ln in open(p, encoding="utf-8", errors="ignore"):
                if ln.strip().startswith("PILLAR"):
                    return ln.split("=", 1)[1].strip().strip('"\'').split("#")[0].strip()
    return ""


PILLAR = _plan_pillar() or "car_cinematic"
PILLAR_FROM_PLAN = bool(_plan_pillar())

def _plan_mod():
    """Import plans/<PROJECT>.py once. REAL-FOOTAGE SCOPING PASS, 2026-08-17 audit:
    planqc learned to read the plan's own declarations (L171); half of this file still
    judged real camera footage with generated-footage rules. Each scoped check below
    names the finding from the audit that forced it."""
    try:
        import importlib
        sys.path.insert(0, HERE)
        return importlib.import_module(f"plans.{PROJECT}")
    except Exception:
        return None


_PMOD = None
def _P():
    global _PMOD
    if _PMOD is None:
        _PMOD = _plan_mod() or False
    return _PMOD or None


def _real_footage():
    P = _P()
    return bool(P and getattr(P, "REAL_FOOTAGE", False))


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
    # FIX 2026-08-06: this globbed ONLY "LC300_*.mp4", so on every project except
    # lc300 the freshness check compared the output against NOTHING and always passed.
    # The check that gates all other checks was blind on crown/kk/wrx/supra.
    # Now: inside projects/<name>/clips every .mp4 IS a source; the flat legacy dirs
    # keep a prefix filter so an OUTPUT file is never mistaken for an input.
    _clipdir = os.path.join(PDIR, "clips")
    _prefixes = ("LC300_", PROJECT.upper() + "_", PROJECT.lower() + "_")
    srcs = []
    for d in SRCDIRS:
        for x in os.listdir(d):
            if not x.endswith(".mp4"):
                continue
            if os.path.abspath(d) == os.path.abspath(_clipdir):
                srcs.append(os.path.join(d, x))          # a clips/ dir holds only sources
            elif x.startswith(_prefixes):
                srcs.append(os.path.join(d, x))
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
    if not ok and _real_footage():
        lines = [l.strip() for l in o.splitlines() if l.strip().startswith("x ")]
        only_exposure = lines and all("exposure" in l or "brightness" in l for l in lines)
        if only_exposure:
            return add("1 qc.py profile", True,
                       f"{len(lines)} deviation(s), ALL exposure-swing - REAL FOOTAGE where "
                       f"cutaways alternate between different-coloured subjects (a red car "
                       f"and a white car differ in brightness BY DESIGN, that is not "
                       f"flicker). Reported, not blocked (audit 2026-08-17).", False)
    return add("1 qc.py profile", ok, tail[0] if tail else "no output")


# ---------------------------------------------------------------- 2 BEAT LOCK
def check_beat(video, cuts):
    try:
        import rhythm
    except Exception as e:
        return add("2 cut-to-music", False, f"rhythm import failed: {e}", False)
    if not cuts:
        return add("2 cut-to-music", False,
                   "NOT MEASURED — no cuts manifest. A cut cannot PASS unexamined; "
                   "run the build on this machine or point --project at the right one.")
    x = rhythm.pcm(video)
    f, t = rhythm.stft_flux(x)
    on = np.array(rhythm.pick_onsets(f, t))
    if not len(on):
        return add("2 cut-to-music", False, "no audio transients found")
    dev = np.array([(on - c)[np.argmin(np.abs(on - c))] * 1000 for c in cuts])
    med = float(np.median(np.abs(dev)))
    within = 100 * float(np.mean(np.abs(dev) < 50))
    if _real_footage() and not (med < 50 and within >= 70):
        return add("2 cut-to-music", True,
                   f"median |dev| {med:.1f} ms, {within:.0f}% within 50 ms  [REAL FOOTAGE: "
                   f"a speech spine cuts to the SENTENCE, not the grid - only the hook and "
                   f"close ride the beat, so the aggregate is off-grid BY DESIGN. Reported, "
                   f"not blocked (audit 2026-08-17).]", False)
    return add("2 cut-to-music", med < 50 and within >= 70,
               f"median |dev| {med:.1f} ms, {within:.0f}% within 50 ms")


# ---------------------------------------------------------------- 3 SFX
def check_sfx(video, cuts):
    P = _P()
    if P is not None and str(getattr(P, "SFX_WAIVED", "") or "").strip():
        return add("3 sfx audible", True,
                   "WAIVED IN THE PLAN: " + str(P.SFX_WAIVED)[:110] +
                   "  [a waiver is a sentence, never a silence (L168) - and this check "
                   "now reads it]", False)
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
    if not cuts:      # 2026-08-05: "0/0 cuts (0%)" used to print OK — a vacuous pass
        return add("4 repetition", False, "NOT MEASURED — no cuts manifest")
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
    if not cuts:      # 2026-08-05: "across 1 shots" printed OK with no manifest
        return add("10 far repeats", False, "NOT MEASURED — no cuts manifest")
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
               f"no far pair reuses the same FRAMES across {len(shots)} shots "
               f"(this is a PIXEL test - two windows of one clip are different "
               f"pixels and still read as the same shot; that is check 13's job)"
               if not dup
               else f"DUPLICATED FOOTAGE: " + " · ".join(dup[:4]))


# ---------------------------------------------------------------- 11 TRANSITIONS
def check_transitions(video, meta):
    """Per-boundary blend QC (his order, 2026-08-04): the seam must land ON the beat
    grid, and the middle of a blend must not smear the whole frame (the s450 `whip`
    bug blurred entire clips and shipped as 'a transition')."""
    bl = meta.get("blends", [])
    beat = meta.get("beat", 0.4)
    if not bl:
        if not meta:      # no manifest at all vs a plan that honestly has no blends
            return add("11 transitions", False, "NOT MEASURED — no build manifest")
        return add("11 transitions", True, "build declares no blends", False)
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
def _composition(img):
    """COMPOSITION descriptor: 4x4 grid of gradient-orientation histograms.
    Deliberately blind to colour and exposure — it answers only 'where are the
    lines', which is what makes a viewer say "I've seen this shot already"."""
    import numpy as np
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(gx * gx + gy * gy)
    ang = (np.arctan2(gy, gx) + np.pi) * (8 / (2 * np.pi))
    v = []
    for r in range(4):
        for c in range(4):
            m = mag[r * 28:(r + 1) * 28, c * 16:(c + 1) * 16]
            a = ang[r * 28:(r + 1) * 28, c * 16:(c + 1) * 16]
            h = np.zeros(8)
            for b in range(8):
                h[b] = m[(a.astype(int) % 8) == b].sum()
            v.append(h / (h.sum() + 1e-9))
    v = np.concatenate(v)
    return v / (np.linalg.norm(v) + 1e-9)


def frames_color(path, w=64, h=112):
    c = cv2.VideoCapture(path); out = []
    while True:
        ok, f = c.read()
        if not ok:
            break
        out.append(cv2.resize(f, (w, h)))
    c.release()
    return out


def _place(img):
    """SAME-PLACE descriptor: hue/saturation signature. Answers the question a VIEWER
    asks — "am I somewhere new?" — which is NOT the question composition answers.
    MEASURED 2026-08-05: between v3 and v11 framing duplicates went 3 -> 0 while
    same-place repeats stayed at 7 and loose similarity went 12 -> 13. Optimising
    framing did nothing for the feeling he named: "alot of reused scenes"."""
    import numpy as np
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = cv2.calcHist([hsv], [0, 1], None, [16, 8], [0, 180, 0, 256]).flatten()
    return h / (np.linalg.norm(h) + 1e-9)


def check_place_variety(video, cuts, thresh=0.90):
    """14 PLACE VARIETY — his catch, 2026-08-05: "alot of reused scenes"."""
    import numpy as np
    if not cuts:
        return add("14 place variety", False, "NOT MEASURED — no cuts manifest")
    fr = frames_color(video)
    fps = 30.0
    bounds = [0.0] + list(cuts) + [len(fr) / fps]
    P = []
    for i in range(len(bounds) - 1):
        t = (bounds[i] + bounds[i + 1]) / 2.0
        P.append(_place(fr[min(int(t * fps), len(fr) - 1)]))
    n = len(P)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)
             if float(P[i] @ P[j]) >= thresh]
    # cluster into distinct PLACES
    par = list(range(n))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for i, j in pairs:
        par[find(i)] = find(j)
    places = len({find(i) for i in range(n)})
    ratio = n / max(1, places)
    return add("14 place variety", ratio <= 2.0,
               f"{n} shots read as ~{places} distinct PLACES ({ratio:.1f} visits each; "
               f"cap 2.0). Framing variety is NOT place variety — measured on KK, "
               f"framing dupes 3->0 while place repeats held at 7.")


def _colour_hist(img):
    """Colour/tone descriptor - the axis composition is deliberately blind to."""
    import numpy as np
    h = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256] * 3)
    h = cv2.normalize(h, h).flatten()
    return h


def check_composition_dupes(video, cuts, comp_thresh=0.80, col_thresh=0.80):
    """13 COMPOSITION DUPLICATES - TWO AXES, because one was never enough.

    HISTORY. Gavril caught duplicate shots on KK v1 while checks 4 and 10 said
    clean, so this check was written on a COMPOSITION descriptor at threshold 0.93,
    fitted to THREE samples. Its own comment said: "a starting point, not a measured
    constant - widen the sample and re-derive before trusting it further." Nobody did.

    2026-08-07, desafarm: he caught three duplicate pairs BY EYE and this check
    passed all three, printing "no pair shares a composition (>= 0.93)":

        shots  2 & 4  (source C, the cabin)   composition 0.920   colour 0.984
        shots  9 & 14 (source E, the calf)    composition 0.885   colour 0.985
        shots 10 & 13 (source G, the goats)   composition 0.871   colour 0.930

    All three sat just under 0.93. But LOWERING the threshold cannot fix it, and
    this is the whole lesson: the highest composition score in that film was

        shots 5 & 15  (the BRZ on grass vs a glass of milk)  composition 0.916

    - a pair with nothing in common, scoring HIGHER than a real duplicate at 0.871.
    Gradient orientation alone cannot separate "same shot twice" from "two shots
    that happen to have lines in the same places". No single threshold exists.

    So the check now requires BOTH axes to agree: composition (where the lines are)
    AND colour/tone (what it is made of). On the 190 pairs of desafarm, comp >= 0.80
    AND colour >= 0.80 reproduces his eye EXACTLY - all three real pairs flagged,
    every other pair clear, worst true margin 0.071, worst false margin 0.060
    (shots 6 & 10 at colour 0.740). Fitted to 6 eye-confirmed samples across two
    films; re-derive as more accumulate, and record the samples when you do."""
    import numpy as np
    if not cuts:
        return add("13 composition dupes", False, "NOT MEASURED - no cuts manifest")
    fr = frames_color(video)
    fps = 30.0
    bounds = [0.0] + list(cuts) + [len(fr) / fps]
    comp, col = [], []
    for i in range(len(bounds) - 1):
        t = (bounds[i] + bounds[i + 1]) / 2.0
        idx = min(int(t * fps), len(fr) - 1)
        comp.append(_composition(fr[idx]))
        col.append(_colour_hist(fr[idx]))
    hits = []
    for i in range(len(comp)):
        for j in range(i + 1, len(comp)):
            c = float(comp[i] @ comp[j])
            k = float(cv2.compareHist(col[i], col[j], cv2.HISTCMP_CORREL))
            if c >= comp_thresh and k >= col_thresh:
                hits.append((round(c, 3), round(k, 3), i, j))
    hits.sort(reverse=True)
    n = len(comp)
    if _real_footage() and hits:
        return add("13 composition dupes", True,
                   f"{len(hits)} recurring pair(s) - REAL FOOTAGE with a speech spine: "
                   f"the presenter re-appearing between cutaways is the FORMAT, not reuse "
                   f"(audit 2026-08-17). Reported for the eye, not blocked.", False)
    return add("13 composition dupes", not hits,
               f"{n} shots, no pair matches on BOTH composition (>= {comp_thresh}) "
               f"and colour (>= {col_thresh})" if not hits
               else f"{len(hits)} pair(s) READ AS THE SAME SHOT: "
                    + " \u00b7 ".join(f"{i}&{j} comp {c} col {k}" for c, k, i, j in hits[:6])
                    + f" - {n} shots collapse to ~{n - len(hits)} distinct images")

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
        return add("12 storyboard tally", False, f"NOT MEASURED — no plan module for '{PROJECT}' "
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
    if _P() is not None and getattr(_P(), "CUTAWAYS", None) and probs:
        return add("12 storyboard tally", True,
                   f"{len(probs)} finding(s) - plan declares CUTAWAYS: physical segments "
                   f"legitimately outnumber logical SHOTS and the spine source repeats "
                   f"(audit 2026-08-17). Reported: " + "; ".join(map(str, probs))[:150], False)
    return add("12 storyboard tally", not probs,
               f"cut matches the board: {len(m)} shots, no window overlap, "
               f"all {len(w)} sources used"
               + (f" (peakless {nopeak}: check 7's call)" if nopeak else "")
               if not probs else " · ".join(probs))


# ---------------------------------------------------------------- 5 EXPOSURE
def check_exposure(video, cuts):
    """FIX 2026-08-08: the 18 was hard-coded in the comparison.

    A travel vlog runs golden hour to night BY DESIGN. A car cinematic is shot in
    one light state. Judging both against the same luma swing is the same mistake
    as shot_match_clamp, which was fitted on night car footage and quietly carried
    into travel_vlog until it stopped working.

    The budget now comes from the pillar's own style block, and the message says
    WHERE the number came from. A threshold you cannot trace is a guess wearing a
    lab coat.
    """
    if not cuts:
        return add("5 exposure match", False, "NOT MEASURED — no cuts manifest")
    try:
        _st = (profile().get("style") or {})
        budget = float(_st.get("exposure_max_swing", 18.0))
        src = f"{PILLAR}.exposure_max_swing"
        gate = str(_st.get("exposure_gate", "block"))
    except Exception:
        budget, src = 18.0, "FALLBACK 18.0 — the pillar declares no exposure_max_swing"
        gate = "block"
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
        if d > budget:
            over += 1
    note = ""
    if over:
        note = (" | a multi-light-state arc swings by design (P3). DO NOT close this "
                "by relighting: v14 bought a smooth number by moving one of his "
                "'close to perfect' shots +72 luma. Check 15 is the harder limit.")
    # REPORT-ONLY PILLARS (2026-08-11). travel_vlog's style block declares
    # exposure_gate="report": its budget was never derived (thresholds.json calls
    # 18 a guess), and a multi-light-state arc swings by design. The measurement
    # still prints in full - what changes is only whether it can BLOCK. Blocking
    # resumes the day a real budget lands (PENDING 2.1) and the style block says
    # "block" again.
    if gate == "report" and over:
        note += (f" | REPORT-ONLY for '{PILLAR}' (style.exposure_gate) - budget "
                 f"never derived for this pillar; not blocking")
    ok = (over == 0) or gate == "report"
    if _real_footage() and not ok:
        return add("5 exposure match", True,
                   "swings are between DIFFERENT SUBJECTS (red/white car cutaways) - by "
                   "design on real footage, not flicker (audit 2026-08-17). Reported.", False)
    return add("5 exposure match", ok,
               f"{over}/{len(cuts)} cuts swing >{budget:.0f} (worst {worst:.0f}) "
               f"[budget from {src}]{note}")


# --------------------------------------------------- 5b WHICH PILLAR ARE WE JUDGING
def check_pillar_source():
    """A gate that judges a travel vlog by car numbers is worse than no gate.

    Blocking, because the failure is silent: every downstream number simply comes
    from the wrong profile and every one of them still prints as if it were fine.
    """
    if not PILLAR_FROM_PLAN:
        return add("5b pillar source", False,
                   f"plans/{PROJECT}.py declares no PILLAR, so every check below is "
                   f"judging this film as '{PILLAR}'. Declare it in the plan.")
    return add("5b pillar source", True,
               f"judging as '{PILLAR}', read from plans/{PROJECT}.py")


# ---------------------------------------------------------------- 15 RELIGHT AUDIT
def check_relight():
    if _real_footage():
        return add("15 relight audit", True,
                   "N/A - real footage has no relight step: nothing between the camera "
                   "file and the cut can move a shot's luma (audit 2026-08-17)", False)
    """HIS CATCH, 2026-08-05: "the video output from higgsfield lighting is already
    pretty good maybe the video editor edit for the second time on the lighting".

    He was right, in BOTH directions. MEASURED on v14: shot 12 arrived at 44.4 mean
    luma — one of the three raw clips he called "close to perfect" — and the edit
    delivered it at 116.9, a +72 relight. Nine other shots were crushed by up to -46.
    Root cause: the gain formula assumed ffmpeg eq=brightness moves 134 luma per unit;
    the MEASURED response is 174-519. Every correction ran ~2.2x hot and 17 of 20 shots
    crossed the target and landed on the far side.

    This check compares what the model DELIVERED against what the edit SHIPPED, shot by
    shot, and fails if the edit exceeded its declared luma budget. It cannot run from
    the finished file alone, so a missing segment cache FAILS — never a vacuous pass.
    """
    import glob as _g
    tmp = os.path.join(PDIR, "tmp")
    srcs = sorted(_g.glob(os.path.join(tmp, "c[0-9][0-9].mp4")))
    if not srcs:
        return add("15 relight audit", False,
                   "NOT MEASURED — no segment cache in tmp/; rebuild before verifying")
    budget = 18.0
    try:
        prof = json.load(open(os.path.join(HERE, "assets", "pillars",
                                           "PILLAR-PROFILES.json"), encoding="utf-8"))
        pil = (meta_pillar() or "")
        budget = float(((prof.get(pil) or {}).get("style") or {})
                       .get("shot_match_max_move", 18.0))
    except Exception:
        pass

    def lev(p):
        c = cv2.VideoCapture(p); v = []
        while True:
            ok, f = c.read()
            if not ok:
                break
            v.append(cv2.cvtColor(cv2.resize(f, (96, 171)), cv2.COLOR_BGR2GRAY).mean())
        c.release()
        return float(np.mean(v)) if v else None

    over, worst, n = [], 0.0, 0
    for s in srcs:
        stem = s[:-4]
        cand = sorted(_g.glob(stem + "_m*.mp4"))
        a = lev(s)
        b = lev(cand[-1]) if cand else a
        if a is None or b is None:
            return add("15 relight audit", False,
                       f"NOT MEASURED — could not read {os.path.basename(s)}")
        n += 1
        d = abs(b - a)
        worst = max(worst, d)
        if d > budget + 0.5:
            over.append((os.path.basename(s), b - a))
    detail = (f"{n} shots audited, worst relight {worst:.1f} luma "
              f"(budget {budget:.0f})")
    if over:
        detail += " | OVER: " + ", ".join(f"{k}{v:+.0f}" for k, v in over[:4])
    # NON-BLOCKING BY INTENT (his instruction, 2026-08-05: "dont lock it i want you to
    # learn from it... these are to upgrade your senses"). A number that blocks gets
    # obeyed and stops being thought about. This one reports, and `lightsense` renders
    # the same measurement as a picture so the judgement stays with an eye.
    return add("15 relight audit", not over, detail, False)


def meta_pillar():
    for p in glob.glob(os.path.join(HERE, "plans", "*.py")):
        if os.path.basename(p)[:-3] == PROJECT:
            for ln in open(p, encoding="utf-8", errors="ignore"):
                if ln.strip().startswith("PILLAR"):
                    return ln.split("=", 1)[1].strip().strip('"\'').split("#")[0].strip()
    return ""


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
        return add("6 caption zone", False, "NOT MEASURED — plan unreadable and no build script")
    src = open(build).read()
    ys = [float(m) for m in re.findall(r'\(\s*"[^"]+",\s*[\d.]+,\s*[\d.]+,\s*\d+,\s*([\d.]+)\)', src)]
    if not ys:
        return add("6 caption zone", False, "NOT MEASURED — no CARDS found anywhere to check")
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
        return add("7 action peaks", False, "NOT MEASURED — no peak manifest written by the build")
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
def check_reference_baseline(video):
    """20 REFERENCE BASELINE — PICTURE ONLY. His instruction 2026-08-12: "the QC
    should run based on the reference video I have provided… that is the baseline",
    scoped by him to "the planning phase and the rough cut phase before Remotion".

    WHY IT EXISTS: this file used to fall back to judging every film against
    plans/lc300.py — our own first build. Measuring new work against old work
    grandfathers our defects in as the standard. The reference films are the
    standard instead, and the numbers below are derived from them
    (assets/refs/<pillar>/*.mp4 → PILLAR-PROFILES.json.measured_spread.picture_baseline).

    AUDIO IS DELIBERATELY NOT JUDGED HERE. The reference files are platform
    re-encodes — two of the six travel_vlog refs peak above 0 dBFS — so baselining
    loudness on them would bless clipping. His mix tuning stands; checks 8/16 and
    bedcheck own audio.

    ONE-SIDED WHERE ONLY ONE DIRECTION IS A DEFECT (caught in test: PANBORNEO_V5,
    the film his ear approved, carries MORE palette across its cuts than the
    references — 0.83 vs a 0.66-0.80 range — and a two-sided bound called that a
    failure. Too much continuity is a different defect and check 13 owns it.)

    PACING METRICS REPORT, NEVER BLOCK, ON A WHOLE-CLIP FILM (hard rule 0): such a
    film is longer and slower by his standing order. Palette carry always counts —
    that is LINKAGE, and nothing he has asked for wants less of it."""
    pil = meta_pillar() or PILLAR
    try:
        prof = json.load(open(os.path.join(HERE, "assets", "pillars",
                                           "PILLAR-PROFILES.json"), encoding="utf-8"))
        base = prof[pil]["measured_spread"]["picture_baseline"]
    except Exception:
        return add("20 reference baseline", True,
                   f"no picture_baseline for '{pil}' - run tools/refsense.py --pillar "
                   f"{pil} --scan and derive it from that pillar's references", False)
    # MEASURE EXACTLY AS THE BASELINE WAS DERIVED (L136): the picture_baseline in
    # PILLAR-PROFILES came from ffmpeg fps=15, scale=64x114 on each reference film.
    # Sampling this film any other way (frames_gray uses a stride) changes the cut
    # count and makes the comparison meaningless - measured 2026-08-12: the same
    # file read 17.8 cuts/min one way and 32.8 the other.
    try:
        dur = float(json.loads(sh(f'ffprobe -v quiet -print_format json -show_format '
                                  f'"{video}"')[1])["format"]["duration"])
    except Exception:
        dur = None
    raw = subprocess.run(f'ffmpeg -v quiet -i "{video}" -vf fps=15,scale=64:114 '
                         f'-f rawvideo -pix_fmt gray -', shell=True,
                         capture_output=True).stdout
    if not raw or dur is None:
        return add("20 reference baseline", True, "could not sample the film", False)
    F = np.frombuffer(raw, np.uint8).reshape(-1, 114, 64).astype(float)
    if len(F) < 8:
        return add("20 reference baseline", True, "too few frames to measure", False)
    FPS_S = 15.0
    d = np.array([np.abs(F[i + 1] - F[i]).mean() for i in range(len(F) - 1)])
    thr = max(18, d.mean() + 2.2 * d.std())
    cuts_m = sorted(set((np.where(d > thr)[0] / FPS_S).tolist()))
    total = dur
    shots = len(cuts_m) + 1
    def hist(fr):
        h = np.histogram(fr, bins=16, range=(0, 255))[0].astype(float)
        return h / (h.sum() + 1e-9)
    inters = []
    for c in cuts_m:
        i = int(c * FPS_S)
        if 1 <= i < len(F) - 1:
            inters.append(float(np.minimum(hist(F[i - 1]), hist(F[i + 1])).sum()))
    mine = {"cpm": shots / total * 60.0, "med": total / shots,
            "first_cut": (cuts_m[0] if cuts_m else total)}
    if inters:
        mine["palette_continuity"] = float(np.median(inters))
    # whole-clip detection straight from the plan (hard rule 0)
    clip_s = 0.0
    try:
        import importlib.util as _il
        _s = _il.spec_from_file_location("_p", os.path.join(HERE, "plans", PROJECT + ".py"))
        _m = _il.module_from_spec(_s); _s.loader.exec_module(_m)
        clip_s = float(getattr(_m, "CLIP_S", 0) or 0)
    except Exception:
        pass
    # WHOLE-CLIP: DECLARED BY THE PLAN **AND** MEASURED IN THE OUTPUT (his catch,
    # 2026-08-12: "the whole clip needs to be measured from the plan AND measured
    # from the output video as well"). Reading the plan alone repeats L145 exactly -
    # a DECLARED property is not a MEASURED one, and a build that quietly chopped a
    # scene would still be granted the whole-clip waiver. So the waiver now requires
    # BOTH, and a disagreement is a FAILURE, not a shrug: the plan said play the
    # scene whole and the file on disk did something else.
    #   plan side   : every shot's declared duration >= 90% of CLIP_S
    #   output side : NO hard cut inside any declared shot span. A hard cut is a big
    #                 luma jump AND a palette break - the same discriminator check 20
    #                 uses at boundaries, which is what separates a real cut from a
    #                 motion spike inside a long take (the thing that made the naive
    #                 detector read 20 segments in a 10-shot film).
    # the auto cut-detector over-segments a whole-clip film - it found 20 segments
    # in a 10-shot NIAH because motion spikes inside a long shot look like cuts -
    # so a measured median can never prove whole-clip. The plan knows: a shot whose
    # declared duration is >= 90% of CLIP_S is the whole scene (hard rule 0).
    whole_plan, whole_out, betrayed = False, None, []
    try:
        _b = getattr(_m, "BEATS", {}) or {}
        _beat = float(getattr(_m, "BEAT", 0) or 0)
        _sh = list(getattr(_m, "SHOTS", []) or [])
        if clip_s and _b and _beat and _sh:
            whole_plan = all(_b.get(s[2], 0) * _beat >= 0.9 * clip_s for s in _sh)
            if whole_plan:
                # MEASURE THE OUTPUT: walk each declared span, look for an interior
                # hard cut (luma jump AND palette break).
                spans, t0 = [], 0.0
                for s in _sh:
                    d_ = _b.get(s[2], 0) * _beat
                    spans.append((t0, t0 + d_)); t0 += d_
                whole_out = True
                for si, (a_, b_) in enumerate(spans):
                    # 0.4s guard band each side: a 2-frame margin at 15fps let the
                    # shot BOUNDARY itself read as an interior cut (false positive
                    # caught in test 2026-08-12 - shot 7 'cut' at 34.53s was the
                    # 34.46s boundary plus sampling jitter).
                    GUARD = 6
                    i0 = int(a_ * FPS_S) + GUARD
                    i1 = min(len(F) - 2, int(b_ * FPS_S) - GUARD)
                    for i in range(i0, i1):
                        if abs(float(F[i + 1].mean()) - float(F[i].mean())) > 28 and \
                           float(np.minimum(hist(F[i]), hist(F[i + 1])).sum()) < 0.45:
                            betrayed.append(f"shot {si} cut at {i / FPS_S:.2f}s")
                            whole_out = False
                            break
    except Exception:
        pass
    whole = bool(whole_plan and whole_out)
    lines, fails = [], []
    for k, b in base.get("metrics", {}).items():
        if k not in mine:
            continue
        lo, hi = b["p10"], b["p90"]
        v = mine[k]
        if k == "palette_continuity":
            ok = v >= lo
        else:
            ok = lo <= v <= hi
            if not ok and whole:
                lines.append(f"{k} {v:.2f} (refs {lo:.2f}-{hi:.2f}) REPORT-whole-clip")
                continue
        lines.append(f"{k} {v:.2f} (refs {lo:.2f}-{hi:.2f}) {'ok' if ok else 'FAIL'}")
        if not ok:
            fails.append(k)
    if whole_plan and whole_out is False:
        fails.append("whole_clip_betrayed")
        lines.append("PLAN SAYS WHOLE CLIPS BUT THE OUTPUT IS CUT: " +
                     "; ".join(betrayed[:3]) + "  <- the build did not honour the plan")
    elif whole_plan and whole_out:
        lines.append("whole-clip CONFIRMED in the output (no interior cuts) - pacing waived")
    return add("20 reference baseline", not fails,
               f"vs {base.get('refs','?')} {pil} references · " + " · ".join(lines) +
               "  [PICTURE ONLY - audio is not baselined on re-encoded refs]")


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
    # THE PLAN'S MIX TARGET OUTRANKS THE PILLAR BAND (audit 2026-08-17). The band
    # (-9.5..-6.5) was measured on loud phonk edits; a speech-led plan deliberately
    # targets quieter. Peak and silence rules still apply unchanged.
    P = _P()
    mix = getattr(P, "MIX", None) if P is not None else None
    if isinstance(mix, dict) and mix.get("lufs_i_target") is not None and lufs is not None:
        want = float(mix["lufs_i_target"])
        ok2 = (abs(lufs - want) <= 1.5 and pk is not None and pk <= -1.0
               and a.get("silence_ratio", 0) < 0.45)
        return add("8 audio", ok2,
                   f"{lufs} LUFS vs the PLAN's own MIX target {want} (±1.5), peak {pk} dBTP "
                   f"(<=-1.0) - the plan decides the level, not the pillar band")
    return add("8 audio", ok,
               f"{lufs} LUFS (-9.5..-6.5), peak {pk} dBTP (<=-1.0), "
               f"silence {a.get('silence_ratio', 0)*100:.0f}%")


# ---------------------------------------------------------------- 9 BLANK
def check_blank(video):
    fr = frames_gray(video, 160, 284, stride=2)
    black = sum(1 for f in fr if f.mean() < 4)
    # A DECLARED dip-to-black or closing fade OWNS its black frames (audit 2026-08-17:
    # LOT_v9's one black frame was the planned dip). Budget: ~5 sampled frames per
    # declared dip/fade at stride=2; undeclared black stays a hard fail.
    P = _P()
    dips = 0
    if P is not None:
        tp = getattr(P, "TRANSITIONS_PLAN", {}) or {}
        dips = sum(1 for v in tp.values() if "dip" in str(v.get("kind", "")).lower())
        dips += 1                                    # every film may fade out once
    budget = dips * 5
    if black and black <= budget:
        return add("9 true black frames", True,
                   f"{black} black frame(s), within the {budget}-frame budget of "
                   f"{dips} DECLARED dip/fade(s) - the plan owns them", False)
    return add("9 true black frames", black == 0,
               f"{black} frames at mean<4 (Laplacian 'blank' is BLUR, not black)"
               + (f" - budget was {budget}" if budget else ""))


# ---------------------------------------------------------------- 16 SOUNDSCAPE
def check_soundscape(video, cuts):
    """16 SOUNDSCAPE CHANGE - does the sound know a cut happened?

    HIS CATCH, 2026-08-07, and nothing in the pipeline was asking it: "the bgm is
    slightly louder than everything it covers all the sfx, and foley which is not
    balanced". Measured on DESAFARM_CINEMATIC_v2:

        median spectral similarity ACROSS the 19 cuts      0.935
        median at random mid-shot control points            0.947

    Cutting from a goat pen to a car interior changed the soundscape NO MORE than a
    random moment inside one shot. The bed was carrying the entire film. Every audio
    check passed anyway: check 8 measures loudness, check 3 measures the transient at
    a cut - neither asks whether the world SOUNDS different on the other side.

    A cut is a change of place. If the sound does not change, there is no foley in
    the mix, whatever the mixer's log claims it applied."""
    import numpy as np, wave, subprocess, tempfile
    if not cuts:
        return add("16 soundscape", False, "NOT MEASURED - no cuts manifest")
    wav = os.path.join(tempfile.gettempdir(), "verify_sound.wav")
    rc, _ = sh(f'ffmpeg -y -v error -i "{video}" -vn -ac 1 -ar 22050 "{wav}"')
    if rc or not os.path.exists(wav):
        return add("16 soundscape", False, "could not extract audio")
    w = wave.open(wav); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    w.close()
    hop, win = 256, 1024
    F = max(0, int((len(x) - win) / hop))
    if F < 32:
        return add("16 soundscape", False, "audio too short to measure")
    S = np.zeros((F, win // 2 + 1))
    hann = np.hanning(win)
    for i in range(F):
        S[i] = np.abs(np.fft.rfft(x[i * hop:i * hop + win] * hann))

    def prof(a, b):
        i, j = int(a * sr / hop), int(b * sr / hop)
        i, j = max(0, i), min(F, j)
        if j - i < 2:
            return None
        v = S[i:j].mean(0)
        return v / (np.linalg.norm(v) + 1e-9)

    sims = []
    for c in cuts:
        a, b = prof(c - 0.30, c - 0.05), prof(c + 0.05, c + 0.30)
        if a is not None and b is not None:
            sims.append(float(a @ b))
    if not sims:
        return add("16 soundscape", False, "no measurable cut boundaries")
    rng = np.random.default_rng(0)
    ctrl = []
    dur = len(x) / sr
    for _ in range(max(12, len(sims))):
        t = float(rng.uniform(0.6, max(0.7, dur - 0.6)))
        a, b = prof(t - 0.30, t - 0.05), prof(t + 0.05, t + 0.30)
        if a is not None and b is not None:
            ctrl.append(float(a @ b))
    med = float(np.median(sims))
    cm = float(np.median(ctrl)) if ctrl else 1.0
    # A cut must change the sound MORE than a random moment inside a shot does.
    # Threshold measured on desafarm (0.935 vs 0.947 control = failure) and set with
    # margin: the cut median must sit at least 0.03 BELOW the control median.
    ok = med <= cm - 0.03
    return add("16 soundscape", ok,
               f"cut similarity {med:.3f} vs mid-shot control {cm:.3f} "
               + ("- the sound changes at cuts" if ok else
                  "- THE BED IS CARRYING THE FILM: cuts sound the same as "
                  "mid-shot, so the foley is not audible in the mix"))


# ---------------------------------------------------------------- 17 CARD COLLISION
def check_card_presence(video):
    """21 CARD PRESENCE - the plan declared a caption; is it ACTUALLY ON SCREEN?

    2026-08-14, r8ride (L173). THE WORST BUG OF THE SESSION, because it is perfectly
    silent. Card PNGs were passed to ffmpeg as bare '-i card.png' - a ONE-FRAME stream
    whose only frame sits at pts=0. capcards then applies fade=t=in:st=<start>:alpha=1,
    and a fade-in evaluated at pts=0 is FULLY TRANSPARENT. overlay's default
    eof_action=repeat holds that transparent frame for the entire film. Result:

        PNGs on disk correct (456x62, alpha 255)      manifest correct
        filtergraph correct                            enable= windows correct
        ffmpeg exit code 0, no error, no warning       ZERO captions in the output

    Every existing caption check passed it: check_caption_zone asks whether cards are
    in the right ZONE, check_card_overlap asks whether two collide. Neither asks the
    prior question - IS ANYTHING THERE AT ALL. A check that only ever runs on frames
    that HAVE a caption cannot report its absence.

    So this measures the built frame against its OWN SOURCE CLIP inside the declared
    card band: a composited card must move that band and leave the rest of the frame
    alone. Self-referencing, so it needs no absolute threshold and no OCR.

        r8ride, cards invisible:  band-diff 0.0 / 0.0 / 0.0   (identical frames)
        r8ride, after the fix:    band-diff 54.4 / 32.0 / 54.5 vs 1.1 elsewhere

    THE RULE: A DECLARED LAYER MUST BE MEASURED IN THE OUTPUT, NEVER ASSUMED FROM A
    CLEAN EXIT CODE. Exit 0 means ffmpeg understood you, not that it did what you meant.
    """
    import numpy as np, importlib
    sys.path.insert(0, HERE)
    try:
        P = importlib.import_module(f"plans.{PROJECT}")
    except Exception as e:
        return add("21 card presence", True,
                   f"NOT MEASURED — no plan module for '{PROJECT}' ({str(e)[:30]})", False)
    cards = list(getattr(P, "CARDS", []) or [])
    if not cards:
        return add("21 card presence", True, "plan declares no cards", False)
    clipdir = os.path.join(PDIR, "clips")
    shots = list(getattr(P, "SHOTS", []) or [])
    beats, beat = getattr(P, "BEATS", {}) or {}, float(getattr(P, "BEAT", 0) or 0)
    if not (shots and beats and beat and os.path.isdir(clipdir)):
        return add("21 card presence", True,
                   "NOT MEASURED - needs SHOTS/BEATS and the source clips on disk", False)

    bound, t = [0.0], 0.0
    for s in shots:
        t += beats.get(s[2], 0) * beat
        bound.append(t)
    y = float(getattr(P, "CARD_Y", 0.72))

    def grab(path, ts):
        c = cv2.VideoCapture(path)
        c.set(cv2.CAP_PROP_POS_MSEC, ts * 1000.0)
        ok, fr = c.read()
        c.release()
        if not ok:
            return None
        g = cv2.cvtColor(cv2.resize(fr, (720, 1280)), cv2.COLOR_BGR2GRAY)
        return g.astype(np.int16)

    bad, seen = [], []
    for text, shot, _span, _kind in cards:
        if shot >= len(shots):
            continue
        srcf = os.path.join(clipdir, f"{PROJECT}_{shots[shot][0]}.mp4")
        if not os.path.exists(srcf):
            continue
        off = 1.0
        a = grab(video, bound[shot] + off)
        b = grab(srcf, off)
        if a is None or b is None:
            continue
        d = np.abs(a - b)
        # the card band, generous either side of the declared y
        lo, hi = max(0, int(1280 * y) - 40), min(1280, int(1280 * y) + 110)
        # FOOTPRINT-AWARE, not band-average. Calibrated 2026-08-17 on LOT: a 149px-wide
        # "PM US" pill inside a 1080px-wide band averages to 3.67 and would be reported
        # NOT ON SCREEN while being plainly visible. The card only occupies the columns
        # it occupies, so measure the columns it actually lit, not the empty ones either
        # side. Found by LOOKING at the frame after the number said no (L177).
        strip = d[lo:hi]
        cols = strip.mean(axis=0)
        band = float(np.percentile(cols, 92)) if cols.size else 0.0
        rest = float(np.delete(d, np.s_[lo:hi], axis=0).mean())
        seen.append(f"{text[:18]} {band:.0f}/{rest:.0f}")
        if not (band > 6.0 and band > rest * 2):
            bad.append(f"'{text[:28]}' at {bound[shot]+off:.1f}s: card band differs "
                       f"from the source by only {band:.1f} (rest {rest:.1f}) - "
                       f"THE CARD IS NOT ON SCREEN")
    if not seen:
        return add("21 card presence", True, "NOT MEASURED - no source clips matched", False)
    return add("21 card presence", not bad,
               "; ".join(bad) if bad else f"all {len(seen)} cards visible ({', '.join(seen)})")


def check_caption_contrast(video):
    """22 CAPTION CONTRAST - his complaint, finally wired (audit 2026-08-17).
    capcheck.py was built 2026-08-12 after 'the caption is what color, it clashes with
    the environment color' - validated once against PANBORNEO_V5, then NEVER connected
    to any gate. Every film since shipped with nobody checking caption legibility.
    It now feeds itself from the plan (capcheck --plan) and this check shells to it."""
    P = _P()
    if P is None or not getattr(P, "CARDS", None):
        return add("22 caption contrast", True, "no plan cards to check", False)
    r = subprocess.run(["python3", os.path.join(TOOLS, "capcheck.py"), video,
                        "--plan", PROJECT], capture_output=True, text=True, timeout=180)
    tail = [l for l in (r.stdout or "").splitlines() if l.strip()][-1:] or ["no output"]
    return add("22 caption contrast", r.returncode == 0, tail[0].strip())


def check_card_overlap(video):
    """17 CARD COLLISION - two captions printed on top of each other.

    2026-08-07, desafarm: 'KUNDASANG NEXT WEEKEND?' rendered OVER 'TWO THOUSAND
    METRES UP' from 20.9s to 23.4s - unreadable overlapping letters for 2.5s, the
    most visible defect in the film. planqc 12 passed it and verify 6 passed it:
    both validate the caption ZONE (are the cards at y=0.72?) and neither asks
    whether two of them are in it AT THE SAME TIME.

    The two captions land on the SAME baseline, so counting text ROWS cannot see it.
    What double-printing does is shatter the glyphs: strokes cross strokes and the
    line breaks into far more connected fragments than any single line of text.
    MEASURED on this film, caption line component counts:

        clean captions   17, 17, 23, 23, 25, 29, 29   (ink density 0.202 - 0.221)
        the collision    59, 59, 59                   (ink density 0.251)

    Self-calibrating on the film's own clean captions rather than an absolute
    constant, because component count scales with the font and the caption length."""
    import numpy as np
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    samples = []
    t = 0.3
    while t * fps < n:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        ok, f = cap.read()
        if not ok:
            break
        h, w = f.shape[:2]
        strip = cv2.cvtColor(f[int(h * 0.63):int(h * 0.80)], cv2.COLOR_BGR2GRAY)
        ink = (strip > 230).astype(np.uint8)
        rows = ink.sum(1)
        if rows.max() >= 8:
            r = int(np.argmax(rows))
            line = ink[max(0, r - 14):min(strip.shape[0], r + 14)]
            ncomp, _ = cv2.connectedComponents(line)
            samples.append((round(t, 2), ncomp - 1, float(line.mean())))
        t += 0.3
    cap.release()
    if len(samples) < 4:
        return add("17 card collision", True,
                   f"{len(samples)} captioned frames - too few to calibrate", blocking=False)
    comps = sorted(s[1] for s in samples)
    med = comps[len(comps) // 2]
    # a caption line with >= 1.6x the median fragment count is two texts superimposed
    bad = [s for s in samples if s[1] >= max(med * 1.6, med + 8)]
    spans = []
    for tt, c, d in bad:
        if spans and tt - spans[-1][1] <= 0.7:
            spans[-1][1] = tt
        else:
            spans.append([tt, tt])
    long = [s for s in spans if s[1] - s[0] >= 0.5]
    if _real_footage() and long:
        return add("17 card collision", True,
                   f"glyph-fragment spike at {long} - REAL FOOTAGE: busy textures (LED "
                   f"strips, chrome) fragment like superimposed glyphs; verified false "
                   f"positive on LOT_v9 by opening the frames (L177). Reported - LOOK at "
                   f"the span before shipping.", False)
    return add("17 card collision", not long,
               f"{len(samples)} captioned frames, median {med} glyph fragments, "
               f"no line above {max(int(med*1.6), med+8)}" if not long
               else "TWO CAPTIONS SUPERIMPOSED (glyph fragments "
                    f"{max(s[1] for s in bad)} vs median {med}): "
                    + " \u00b7 ".join(f"{a:.1f}-{b:.1f}s" for a, b in long))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=DEFAULT_VIDEO)
    ap.add_argument("--json")
    ap.add_argument("--project", default=None, help="projects/<name>")
    a = ap.parse_args()
    # --project was parsed but NEVER USED (2026-08-05 red-team find: --project wrx
    # still verified against the lc300 defaults computed at import). Recompute every
    # project-derived path here, where the argument actually exists.
    global PROJECT, PDIR, CUTS_JSON, PILLAR, PILLAR_FROM_PLAN
    # 2026-08-12: infer the project from the video's own path when not told, and
    # RECOMPUTE the pillar — it is read at import time, before --project exists.
    if not a.project:
        guess = _project_from_path(a.video)
        if guess and os.path.exists(os.path.join(HERE, "plans", guess + ".py")):
            a.project = guess
            print(f"  (project inferred from the video path: {guess})")
    if a.project:
        PROJECT = a.project
        _p = _plan_pillar()
        if _p:
            PILLAR, PILLAR_FROM_PLAN = _p, True
        PDIR = os.path.join(HERE, "projects", PROJECT)
        CUTS_JSON = _newest(os.path.join(PDIR, "audio"), "*_cuts.json") or ""
        if a.video == DEFAULT_VIDEO:
            a.video = (_newest(os.path.join(PDIR, "output"), "*CINEMATIC*.mp4")
                       or _newest(os.path.join(PDIR, "output"), "*.mp4") or a.video)
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
        check_pillar_source()   # FIRST: everything below reads this pillar's numbers
        check_profile(video)
        check_beat(video, cuts)
        check_sfx(video, cuts)
        check_repetition(video, cuts)
        check_exposure(video, cuts)
        check_caption_zone(video)
        check_action(cuts)
        check_audio(video)
        check_reference_baseline(video)
        check_blank(video)
        check_far_repeats(video, cuts)
        check_transitions(video, meta)
        check_composition_dupes(video, cuts)
        check_place_variety(video, cuts)
        check_soundscape(video, cuts)
        check_card_overlap(video)
        check_card_presence(video)
        check_caption_contrast(video)
        check_relight()
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
