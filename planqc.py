#!/usr/bin/env python3
"""
PLANQC — gate the EDIT PLAN before a single credit is spent.

WHY THIS EXISTS
  Every gate in this project runs AFTER the money is gone. `verify.py` inspects a finished
  cut; `qc.py` inspects a rendered file; `mastermind` inspects frames. By the time any of
  them speak, the clips are generated and the credits are burned.

  The defects that cost the most were all decidable from the PLAN alone:

    7 of 13 cuts showed the same image     4 sources carrying 14 shots - countable
    1.9x punch-ins destroyed 82% sharpness a number in the plan, not in the footage
    captions dead centre on the car        a y-coordinate in the plan
    the hook was a static wheel            shot 0's source, in the plan
    a generic crossover, not a Crown       a missing reference plate, in the plan

  So this runs FIRST, costs nothing, and blocks generation. It is the cheapest gate in
  the project and it should have existed before the other three.

  It also refuses to flatter the plan: deliberate deviations from the pillar profile are
  printed as WARN with the reason, never silently passed.

USAGE
  python3 planqc.py                 validate + write the production doc
  python3 planqc.py --plan i8_plan  validate a different plan module
  python3 planqc.py --json r.json
"""
import os, re, sys, json, math, argparse, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

R = []          # (name, ok, detail, blocking)


def add(name, ok, detail, blocking=True):
    R.append((name, bool(ok), detail, blocking))
    return ok


def warn(name, detail):
    return add(name, False, detail, False)


def _first(*c):
    for p in c:
        if p and os.path.exists(p):
            return p
    return None


def profile(pillar):
    p = _first(os.path.join(HERE, "assets", "pillars", "PILLAR-PROFILES.json"),
               os.path.join(HERE, "pillars", "PILLAR-PROFILES.json"),
               os.path.join(HERE, "work", "RESTORE", "pillars", "PILLAR-PROFILES.json"))
    if not p:
        return None
    return json.load(open(p))[pillar]


# ---------------------------------------------------------------- 1 STRUCTURE
def check_structure(P):
    tl, total = P.timeline()
    n = len(P.SHOTS)
    ok = abs(total - P.TARGET_S) < 0.05
    return add("1 duration", ok,
               f"{n} shots, {total:.2f}s against a {P.TARGET_S:.0f}s target "
               f"({len(tl)} entries, beat {P.BEAT:.3f}s)")


def check_profile_band(P, pf):
    if not pf:
        return warn("2 pillar band", "PILLAR-PROFILES.json not found")
    tl, total = P.timeline()
    lo, hi = pf["duration_s"]
    durs = sorted(d for _s, d, _k in tl)
    med = durs[len(durs) // 2]
    cuts = len(P.SHOTS) - 1
    cpm = cuts / total * 60.0
    mlo, mhi = pf["shot_median_range"]
    tgt = pf["cuts_per_min"]

    ok_dur = lo <= total <= hi
    ok_med = mlo <= med <= mhi
    ok_cpm = tgt * 0.8 <= cpm <= tgt * 1.2
    r = add("2 pillar band", ok_dur and ok_med and ok_cpm,
            f"duration {total:.1f}s in [{lo},{hi}] · median shot {med:.2f}s in "
            f"[{mlo},{mhi}] · {cpm:.1f} cuts/min vs {tgt} target (+-20%)")
    # 2b SHOT EXTREMES (2026-08-05). The median hides the longest shot, and the
    # plan's BEATS dict is written per-plan — copy a car plan's {burst:2,med:4,hold:8}
    # into a 105 BPM vlog and a "hold" silently becomes 4.57s (4x that genre's median,
    # ~20% of the video on one image). The car's own hold was 4.2x ITS median and his
    # eye did not object to it (NOT an approval - approvals.json UNV-2), so this is NOT a rule — it is a number that must be SEEN, not
    # discovered in the finished cut.
    longest = max(d for _s, d, _k in tl)
    ratio = longest / max(1e-6, pf["shot_median_s"])
    share = 100.0 * longest / total
    msg = (f"longest shot {longest:.2f}s = {ratio:.1f}x the genre median "
           f"({pf['shot_median_s']}s), {share:.0f}% of the video")
    if ratio > 3.0 or share > 15.0:
        warn("2b shot extremes", msg + " — deliberate? a hold this long is a bet on ONE image")
    else:
        add("2b shot extremes", True, msg, False)
    return r


# ---------------------------------------------------------------- 3 COVERAGE
def check_coverage(P):
    """The rule that the LC300 broke. 4 sources under 14 shots produced 7 repeated cuts."""
    n = len(P.SHOTS)
    need = math.ceil(n / 2.5)
    have = len({s for s, _c, _k, _t in P.SHOTS})
    return add("3 coverage", have >= need,
               f"{have} distinct sources for {n} shots (need >= {need} = shots/2.5)")


def check_source_balance(P):
    """The storyboard image caught ONE clip carrying 4 of 14 shots. Count it instead."""
    n = len(P.SHOTS)
    use = {}
    for s, _c, _k, _t in P.SHOTS:
        use[s] = use.get(s, 0) + 1
    cap = max(2, math.ceil(n * 0.25))
    worst = max(use.values())
    hogs = [k for k, v in use.items() if v > cap]
    unused = [k for k in P.SOURCES if k not in use]
    ok = not hogs and not unused
    d = f"heaviest source carries {worst}/{n} (cap {cap})"
    if hogs:
        d += f" - OVER: {hogs}"
    if unused:
        d += f" - UNUSED sources: {unused}"
    return add("4 source balance", ok, d)


def check_adjacency(P):
    """Two neighbouring shots from one clip is a repeat no matter how it is cropped."""
    bad = [i for i in range(1, len(P.SHOTS))
           if P.SHOTS[i][0] == P.SHOTS[i - 1][0]]
    return add("5 adjacency", not bad,
               f"{len(bad)} adjacent pairs share a source"
               + (f" at shots {bad}" if bad else ""))


# ---------------------------------------------------------------- 6 CROP
def check_crop(P):
    """1.90x measured a sharpness collapse from 234 to 42. That is the AI look."""
    over = [(i, c) for i, (_s, c, _k, _t) in enumerate(P.SHOTS) if c > P.MAX_CROP + 1e-9]
    crops = sorted({c for _s, c, _k, _t in P.SHOTS})
    return add("6 crop cap", not over,
               f"crops {crops}, cap {P.MAX_CROP}"
               + (f" - OVER at {over}" if over else ""))


def check_crop_distribution(P):
    """RELATIONAL. The per-shot cap in check 6 passed a plan with 12% of its punch-ins in
    the first half and 67% in the second - a video that gets visibly softer as it plays,
    plus a run of three cropped shots back to back. A cap cannot see either. Every defect
    found by eye in this project has been a relationship between shots, not a shot."""
    crops = [c for _s, c, _k, _t in P.SHOTS]
    n = len(crops)
    bad = []

    run = best = 0
    for c in crops:
        run = run + 1 if c > 1.0 else 0
        best = max(best, run)
    if best > 2:
        bad.append(f"{best} cropped shots in a row (max 2)")

    h = n // 2
    f = 100.0 * sum(1 for c in crops[:h] if c > 1.0) / max(1, h)
    s = 100.0 * sum(1 for c in crops[h:] if c > 1.0) / max(1, n - h)
    if abs(f - s) > 30:
        bad.append(f"sharpness drift: {f:.0f}% cropped in the first half vs {s:.0f}% in the second")

    if crops[0] > 1.0:
        bad.append("shot 0 is cropped - never soften the hook")
    holds = [i for i, sh in enumerate(P.SHOTS) if sh[2] == "hold" and sh[1] > 1.0]
    if holds:
        bad.append(f"cropped HOLD at {holds} - the longest shots are where softness shows most")

    return add("7 crop distribution", not bad,
               f"longest run {best}, halves {f:.0f}%/{s:.0f}%, hook and holds uncropped"
               if not bad else " · ".join(bad))


def check_repeat_framing(P):
    """RELATIONAL. Same source at the same crop is the same image twice, however far
    apart. This is the plan-time version of the histogram-correlation check that found
    7 of 13 cuts showing no new information."""
    seen, dup = {}, []
    cb = {tuple(sorted(p)) for p in getattr(P, "CALLBACKS", [])}
    for i, (s, c, _k, _t) in enumerate(P.SHOTS):
        key = (s, c)
        if key in seen:
            pair = tuple(sorted((seen[key], i)))
            if pair not in cb:
                dup.append(f"{s}@{c:.2f}x at shots {pair[0]} and {pair[1]}")
        seen[key] = i
    return add("8 repeat framing", not dup,
               f"no source repeats a crop ({len(cb)} declared callback(s))"
               if not dup else " · ".join(dup))


# ---------------------------------------------------------------- 9 THE HOOK
def check_event(P):
    """The LC300 opened on a static wheel because it measured highest motion. Highest
    motion is not most arresting. Shot 0 must be an EVENT and it must be OVER fast."""
    s0, _c0, k0, _t0 = P.SHOTS[0]
    act = P.SOURCES[s0][2]
    tl, _ = P.timeline()
    d0 = tl[0][1]
    is_event = act.upper() == "EVENT"
    fast = d0 <= 2.0
    return add("9 hook is an EVENT", is_event and fast,
               f"shot 0 = source {s0} ({act}), {d0:.2f}s "
               f"[needs act=EVENT and <= 2.00s: hooks under 2s measured 23% higher completion]")


def check_hold_placement(P):
    """A 3.2s hold on a low-motion clip is dead air. Holds go to PAYOFF or HUMAN acts."""
    holds = [(i, P.SHOTS[i][0], P.SOURCES[P.SHOTS[i][0]][2])
             for i, s in enumerate(P.SHOTS) if s[2] == "hold"]
    weak = [h for h in holds if h[2].upper() not in ("PAYOFF", "HUMAN", "EVENT")]
    if not holds:
        return warn("10 hold placement", "no holds - flat lengths measure rate_variation ~0")
    return add("10 hold placement", not weak,
               f"{len(holds)} holds on {[h[2] for h in holds]}"
               + (f" - WEAK: {weak}" if weak else ""))


# ---------------------------------------------------------------- 11 BLENDS
def check_blends(P, pf):
    cuts = len(P.SHOTS) - 1
    nb = len(P.BLEND_AFTER)
    pct = 100.0 * nb / max(1, cuts)
    w = P.BLEND_WIDTH * 1000
    if not pf:
        return warn("11 blends", f"{pct:.0f}% blended, no profile to compare")
    # PILLAR PORTABILITY (2026-08-05, red-team: the first non-car plan CRASHED here
    # with KeyError 'blended_range'). Only car_cinematic was ever measured for blend
    # RANGES; travel_vlog carries blended_pct 0 + "HARD CUTS ONLY - 5 of 6 references
    # use zero blended transitions", industry carries blended_range but no width.
    # Derive an honest band from what the profile DOES hold, never assume car values.
    if "blended_range" in pf:
        blo, bhi = pf["blended_range"]
    else:
        base = float(pf.get("blended_pct", 0))
        # a measured 0% is an editorial RULE for this pillar, not a missing number
        blo, bhi = (0.0, 5.0) if base == 0 else (base * 0.5, base * 1.5)
    wlo, whi = pf.get("blend_width_ms", (240, 560))
    bad_idx = [i for i in P.BLEND_AFTER if i >= len(P.SHOTS) - 1]
    no_width = (nb == 0)   # zero blends cannot violate a width band

    # COUNT BAND (2026-08-06). A percentage quantises to zero on a short cut: with 19
    # boundaries ONE blend is 5.3%, so a [0,5] band made a single deliberate whip
    # impossible — an artifact of the unit, not a decision anyone made. A pillar whose
    # designed transitions are RARE can now say so as a COUNT. travel_vlog measures 9.5%
    # designed pooled across 6 references (tools/blendsense.py, whip-sensitive) = 0-2 at
    # this length, so it declares blend_max_count 2.
    _maxn = pf.get("blend_max_count")
    if _maxn is not None:
        ok_band = nb <= int(_maxn)
        band_txt = f"{nb}/{cuts} blended, cap {int(_maxn)} by COUNT (pillar measures " \
                   f"{pf.get('designed_pct', pct):g}% designed, rare by nature)"
    else:
        ok_band = blo <= pct <= bhi
        band_txt = f"{nb}/{cuts} blended = {pct:.0f}% in [{blo:g},{bhi:g}]"

    # KIND WHITELIST. A pillar that measures only whips should not silently accept a
    # dissolve: the count can be right and the vocabulary still wrong.
    _kinds = pf.get("designed_kinds")
    bad_kind = (nb and _kinds and getattr(P, "BLEND_KIND", "") not in _kinds)

    ok = ok_band and (no_width or wlo <= w <= whi) and not bad_idx and not bad_kind
    d = (band_txt
         + ("  (no blends — width not judged)" if no_width
            else f" · width {w:.0f}ms in [{wlo},{whi}]"))
    if bad_kind:
        d += (f" — BLEND_KIND '{getattr(P, 'BLEND_KIND', '')}' is not in this pillar's "
              f"measured vocabulary {_kinds}")
    if _maxn is None and bhi <= 5.0 and nb:
        d += f" — this pillar measured HARD CUTS ONLY; {nb} blend(s) is a declared deviation"
    if bad_idx:
        d += f" - blend index past the last cut: {bad_idx}"
    if getattr(P, "BLEND_KIND", "") == "dip":
        d += " - `dip` fades through BLACK and will trip the blank-frame gate"
        ok = False
    return add("11 blends", ok, d)


# ---------------------------------------------------------------- 12 CAPTIONS
def check_captions(P, pf=None):
    """y=0.42 put text dead centre, on the car. The subject always lives in the centre."""
    y = P.CARD_Y
    n = len(P.SHOTS)
    over = [c for c in P.CARDS if c[1] + c[2] > n]
    centre = 0.34 <= y <= 0.60
    # WORD LIMIT FROM THE STYLE BLOCK (2026-08-05). Was hardcoded 3 / 5-if-narrative —
    # car-label taste. travel_vlog's measured caption style is "sentence fragments", and
    # a real fragment ("SABAH, 1500 METRES UP") is 4 words: the car limit BLOCKED the
    # vlog genre's own caption form. Another silent-inheritance leftover, same class as
    # the night brightness band and the 1.5 motion floor.
    # The style block sets the PILLAR DEFAULT; a plan's declared CARD_STYLE="narrative"
    # is a DELIVERATE deviation (the WRX cards read as a sentence — that IS the
    # improvisation) and must be able to raise the ceiling, never be silently capped
    # by it. Caught immediately: adding the style default alone broke the WRX, which
    # has shipped 5-word narrative cards since 2026-08-04.
    _st = (pf or {}).get("style") or {}
    limit = _st.get("card_max_words", 3)
    if getattr(P, "CARD_STYLE", "") == "narrative":
        limit = max(limit, 5)
    long = [c[0] for c in P.CARDS if len(c[0].split()) > limit]
    # CARD COLLISION, 2026-08-07. This check validated the ZONE - are the cards at
    # y=0.72, do they fit, are they short enough - and never asked whether two of
    # them are IN that zone at the same time. desafarm shipped
    #   ('TWO THOUSAND METRES UP', shot 14, 4 shots)  -> shots 14,15,16,17
    #   ('KUNDASANG NEXT WEEKEND?', shot 16, 4 shots) -> shots 16,17,18,19
    # and cards.py drew both on the same baseline. From 20.9s to 23.4s the lower
    # third was two captions printed through each other, unreadable. This check
    # said OK, and so did verify 6. The most visible defect in the film passed
    # every gate that was supposed to be looking straight at it.
    spans = []
    for c in P.CARDS:
        s0 = int(c[1]); n0 = int(c[2]) if len(c) > 2 else 1
        spans.append((c[0], s0, s0 + max(1, n0) - 1))
    collide = []
    for a in range(len(spans)):
        for b in range(a + 1, len(spans)):
            t1, a0, a1 = spans[a]; t2, b0, b1 = spans[b]
            if a0 <= b1 and b0 <= a1:
                lo, hi = max(a0, b0), min(a1, b1)
                collide.append(f"{t1!r} and {t2!r} both on shots {lo}-{hi}")
    ok = not centre and not over and not long and not collide
    d = f"{len(P.CARDS)} cards at y={y}"
    if collide:
        d += " - TWO CARDS IN THE SAME ZONE AT THE SAME TIME: " + " · ".join(collide)
    if centre:
        d += " - IN THE CENTRE BAND (0.34-0.60), this is where the car is"
    if over:
        d += f" - card runs past the last shot: {[c[0] for c in over]}"
    if long:
        d += f" - too wordy even for {getattr(P,'CARD_STYLE','label')} style: {long}"
    if ok and getattr(P, "CARD_STYLE", "") == "narrative":
        # deviation from the measured 1-2 word profile: DECLARED, never silent
        warn("12b card style", f"NARRATIVE cards ({max(len(c[0].split()) for c in P.CARDS)} "
             f"words max) vs profile's 1-2 word labels - DELIBERATE: the cards form a "
             f"sentence, the field's cards are labels")
    return add("12 caption zone", ok, d)


# ---------------------------------------------------------------- 13 IDENTITY
def check_plates(P):
    """A text-only prompt for a '2026 Toyota Crown' returned a generic crossover and it
    SHIPPED. A named subject is never generated from text alone."""
    missing, low, human_no_plate = [], [], []
    for k, v in P.PLATES.items():
        if v.get("res") != "4k":
            low.append(f"{k}={v.get('res')}")
    for key, (_lab, _col, act, plates, prompt) in P.SOURCES.items():
        for p in plates:
            if p not in P.PLATES:
                missing.append(f"{key}->{p}")
        # HUMAN always needs the persona plate. EVENT needs it only when the prompt
        # actually STAGES the persona ("the man from the ... reference") - a car-only
        # event (AWD launch, doors) is legitimate and has no face to lock. The WRX
        # launch shot exposed this: the act said EVENT, the frame contains no human.
        stages_persona = "man from the" in prompt.lower()
        if (act.upper() == "HUMAN" or (act.upper() == "EVENT" and stages_persona)) \
                and "nev" not in plates:
            human_no_plate.append(key)
    ok = not missing and not low and not human_no_plate
    d = f"{len(P.PLATES)} plates, all 4k" if not low else f"PLATES BELOW 4k: {low}"
    if missing:
        d += f" - source references a plate that does not exist: {missing}"
    if human_no_plate:
        d += f" - human shot with no persona plate: {human_no_plate}"
    return add("13 reference plates", ok, d)


def check_prompts(P):
    """Absence of real-photo artefacts is what reads as AI. Every prompt must ask for them
    and must name the subject explicitly."""
    need = ["not a render", "negative:"]
    thin, generic = [], []
    for key, (_l, _c, _a, _p, prompt) in P.SOURCES.items():
        low = prompt.lower()
        if not all(t in low for t in need):
            thin.append(key)
        if "reference image" not in low:
            generic.append(key)
    ok = not thin and not generic
    d = f"{len(P.SOURCES)} prompts carry the realism block and cite the plate"
    if thin:
        d = f"prompts missing realism/negative language: {thin}"
    if generic:
        d += f" - prompts that never cite the reference plate: {generic}"
    return add("14 prompt quality", ok, d)


# ---------------------------------------------------------------- 15 DEFAULTS
def check_defaults(P):
    """Every default was accepted silently once: 1k plates, `fast` video."""
    bad = []
    if P.MODE != "std":
        bad.append(f"MODE={P.MODE} (std is the higher-quality generation)")
    if getattr(P, "AI_LABEL_BURNED_IN", False):
        bad.append("AI label burned in - use the platform toggle at upload")
    return add("15 quality defaults", not bad,
               f"mode={P.MODE}, res={P.RES}, {P.FPS}fps, AI label = platform toggle"
               + (f" - {bad}" if bad else ""))


# ---------------------------------------------------------------- 16 SHOT MIX
def check_shot_mix(P, pf):
    """WARN only. The profile was measured from references that also do not necessarily
    stop a scroll - a deviation may be the point. But it must be DECLARED, not silent."""
    if not pf or "shot_mix" not in pf:
        return warn("16 shot mix", "no shot_mix in profile")
    tl, total = P.timeline()
    acts = {}
    for (s, _c, _k, _t), (_st, d, _kk) in zip(P.SHOTS, tl):
        a = P.SOURCES[s][2].lower()
        acts[a] = acts.get(a, 0.0) + d
    mine = {k: 100.0 * v / total for k, v in sorted(acts.items(), key=lambda x: -x[1])}
    got = ", ".join(f"{k} {v:.0f}%" for k, v in mine.items())
    human = mine.get("human", 0) + mine.get("event", 0)
    ref_h = pf["shot_mix"].get("human", 0)
    if human > ref_h * 2:
        return warn("16 shot mix",
                    f"{got} - HUMAN+EVENT is {human:.0f}% against the profile's {ref_h}%. "
                    f"DELIBERATE: the LC300 had no face, no stakes and no claim.")
    return add("16 shot mix", True, got)


def check_content(P):
    """CONTENT QUALITY, made mechanical where it can be. The LC300 passed every craft
    check and said NOTHING - no claim, no stakes, no reason to care. A plan must now
    carry a CONTENT block, and its claim must cite a verification source, because a
    confident false claim in a sales video is worse than a dull true one."""
    c = getattr(P, "CONTENT", None)
    if not c:
        return add("18 content", False,
                   "NO CONTENT BLOCK - the plan says how to cut but not what the video "
                   "SAYS. Required: claim, verified, twist, why_stop.")
    missing = [k for k in ("claim", "verified", "twist", "why_stop") if not c.get(k)]
    if missing:
        return add("18 content", False, f"CONTENT block missing {missing}")
    return add("18 content", True,
               f"claim: \"{c['claim'][:58]}...\" verified: {c['verified'][:40]}")


def check_sound(P):
    """SOUND DESIGN, made blocking (2026-08-04, Gavril's catch: the WRX shipped with
    whoosh/impact only — EDIT sound, not foley — in a genre that is sound-led. No
    engine under the launch, no spray, no boxer idle). Clip audio is generated and
    PAID FOR; a car_cinematic plan without a diegetic decision NEVER reaches spend.
    File 19 (sound engineer) judges the mix; file 04 (foley) picks the sounds; this
    check only verifies the DECISION exists and is coherent — mechanical, not taste."""
    # SCOPED BY DECLARED STYLE, not by a hardcoded pillar name (2026-08-05).
    # The old `!= "car_cinematic"` meant a vlog plan got a WARN and could reach
    # SPEND with no sound decision at all — the gate that made foley mandatory
    # silently switched itself off for every pillar that came after the car.
    pil = getattr(P, "PILLAR", "")
    gate = ((profile(pil) or {}).get("style") or {}).get("sound_gate", "diegetic")
    if gate == "underscore":
        # speech-led: the spine is the VOICE, so that is what must be declared.
        v = getattr(P, "VOICE", None)
        if not v or not v.get("voice_id"):
            return add("19 sound design", False,
                       f"pillar '{pil}' is speech-led (sound_gate=underscore): the plan must "
                       f"declare VOICE={{name, voice_id, voice_type}} + language mode. "
                       f"See assets/nev/voice/VOICE.md.")
        return add("19 sound design", True,
                   f"speech-led: voice '{v.get('name')}' declared, bed is underscore")
    foley = getattr(P, "FOLEY", None)
    snd = getattr(P, "SOUND", None)
    n = len(P.SHOTS)
    if not foley or not snd:
        return add("19 sound design", False,
                   "NO SOUND/FOLEY BLOCK — the plan says how to cut but not what the "
                   "video SOUNDS like. Required: FOLEY={shot: gain_db} for every shot "
                   "+ SOUND{hero, duck_shots, silence}.")
    missing = [i for i in range(n) if i not in foley]
    mkeys = [k for k in ("hero", "duck_shots", "silence") if snd.get(k) is None]
    quiet = []
    if gate == "diegetic":
        # HERO DOCTRINE is car-genre taste (file 04 law 4: one hero sound). A travel
        # vlog has ambience, not a hero — demanding a foreground EVENT there would be
        # importing the car's signature. Only the diegetic gate enforces it.
        for i, (s, _c, _k, _t) in enumerate(P.SHOTS):
            act = P.SOURCES[s][2].upper()
            if act in ("EVENT", "PAYOFF") and foley.get(i, -99) < -6:
                quiet.append(f"shot {i} ({act.lower()}) at {foley.get(i)}dB")
    bad_duck = [si for si in (snd.get("duck_shots") or []) if not 0 <= si < n]
    ok = not missing and not mkeys and not quiet and not bad_duck
    d = (f"FOLEY covers {n-len(missing)}/{n} shots, "
         f"{sum(1 for g in foley.values() if g >= -6)} foreground (>=-6dB), "
         f"hero: {str(snd.get('hero'))[:45]}")
    if missing:
        d += f" — shots with NO diegetic decision: {missing}"
    if mkeys:
        d += f" — SOUND block missing {mkeys}"
    if quiet:
        d += f" — EVENT/PAYOFF mixed to background: {quiet} (the hero moments must be HEARD)"
    if bad_duck:
        d += f" — duck_shots out of range: {bad_duck}"
    return add("19 sound design", ok, d)


def check_transitions_plan(P):
    """Gavril: 'it cuts the first clip way too early' (2026-08-04). The v1 blend after
    shot 0 dissolved the last 0.4s of a 1.6s EVENT — the swerve-pass resolved INSIDE
    the fade. Mechanical rule: a blend never touches an EVENT. Its resolution is its
    last frames (exiting side); its onset must be frame zero (entering side)."""
    bad = []
    for i in sorted(set(P.BLEND_AFTER)):
        if i >= len(P.SHOTS) - 1:
            continue                            # out-of-range is check 11's job
        for j, side in ((i, "EXITS"), (i + 1, "ENTERS")):
            act = P.SOURCES[P.SHOTS[j][0]][2].upper()
            if act == "EVENT":
                bad.append(f"blend after shot {i} {side} EVENT shot {j} — "
                           f"the event dissolves instead of landing")
    return add("20 transitions", not bad,
               f"{len(P.BLEND_AFTER)} blend(s), none touching an EVENT boundary"
               if not bad else " · ".join(bad))


def check_capacity(P):
    """Duplicates are a plan OVERCOMMIT before they are an engine bug: B carried 3.2s
    of shots against ~3.0s of usable clip once the softbox head (measured out at
    2.0s) was banned. Windows may not overlap — so the demand must FIT the clip."""
    bans = getattr(P, "BAN_SPANS", {}) or {}
    tl, _ = P.timeline()
    need = {}
    for (s, _c, _k, _t), (_st, d, _kk) in zip(P.SHOTS, tl):
        need[s] = need.get(s, 0.0) + d
    bad, det = [], []
    for s in sorted(need):
        banned = sum(b - a for a, b in bans.get(s, []))
        have = P.CLIP_S - banned - 0.1
        det.append(f"{s} {need[s]:.1f}/{have:.1f}")
        if need[s] > have + 1e-6:
            bad.append(f"source {s} needs {need[s]:.1f}s but has {have:.1f}s usable "
                       f"(clip {P.CLIP_S}s - {banned:.1f}s banned)")
    return add("21 source capacity", not bad,
               "every source fits its windows (need/have s): " + " · ".join(det)
               if not bad else " · ".join(bad))


# ------------------------------------------------------- 22-24 THE MASTERMIND LOOP
# His doctrine, stated 2026-08-04: the mastermind is the FIRST planner and the FINAL
# BOSS of QC, and the whole system is a loop that must get better every generation.
# A lesson that does not change the next build is not learned. These three checks
# make the loop mechanical: the plan must READ the ledger (23), PREDICT its own
# likely failures from it (22), and PLAN every join, not discover it (24).

def _ledger_topics():
    p = _first(os.path.join(HERE, "ledgers", "knowledge.json"))
    if not p:
        return None
    try:
        return json.load(open(p, encoding="utf-8")).get("topics", {})
    except Exception:
        return None


def _ledger_lessons(pillar):
    topics = _ledger_topics()
    if topics is None:
        return None, None
    key = str(pillar).replace("_", " ")
    t = topics.get(key)
    if t is None:
        return None, key
    return t.get("lessons", []), key


def check_premortem(P):
    """The plan predicts THIS build's likely mistakes from the ledger and plans the
    fix IN — before any credit. Free, and it is where the loop closes."""
    pm = getattr(P, "PREMORTEM", None)
    if not pm:
        return add("22 premortem", False,
                   "NO PREMORTEM — the plan must predict this build's likely mistakes "
                   "from ledgers/knowledge.json and plan the mitigation in. Required: "
                   "PREMORTEM = [(risk, mitigation), ...], >= 3 entries.")
    bad = []
    if len(pm) < 3:
        bad.append(f"only {len(pm)} entries (need >= 3)")
    for i, e in enumerate(pm):
        if len(e) < 2 or not str(e[0]).strip() or not str(e[1]).strip():
            bad.append(f"entry {i} lacks a risk or a mitigation")
    ok = not bad
    cited = sum(1 for e in pm if re.search(r"L\d+", str(e[0]) + " " + str(e[1])))
    r = add("22 premortem", ok,
            f"{len(pm)} predicted risks, {cited} citing ledger lessons (L<n>)"
            if ok else " · ".join(bad))
    if ok and cited == 0:
        warn("22b premortem cites", "no entry cites a ledger lesson (L<n>) — a premortem "
             "must READ the ledger, not free-associate")
    return r


CRAFT_TOPIC = "general craft"


def check_lessons_ack(P):
    """A plan cannot pass planqc without having read the NEWEST ledger state — for its
    own GENRE **and** for the pillar-independent CRAFT topic.

    2026-08-05: this check used to read only the plan's own pillar topic, so a
    travel_vlog plan acknowledged 11 lessons while ignoring 25 lessons of measurement
    and tooling craft that were filed under 'car cinematic' purely because that is
    where the work happened first. The ledger has since been refactored: craft moved
    to '<CRAFT_TOPIC>', genre stayed put. Every plan must now ack BOTH.

    LESSONS_ACK = {"general craft": N, "<pillar topic>": M}   (dict, preferred)
    A bare int is still accepted as the GENRE count, but the craft ack is mandatory —
    silence about craft is what this refactor exists to end."""
    genre_lessons, key = _ledger_lessons(getattr(P, "PILLAR", ""))
    craft_lessons, _ = _ledger_lessons(CRAFT_TOPIC.replace(" ", "_"))
    if craft_lessons is None:
        craft_lessons = (_ledger_topics() or {}).get(CRAFT_TOPIC, {}).get("lessons")
    ack = getattr(P, "LESSONS_ACK", None)

    need = {}
    if genre_lessons is not None:
        need[key] = len(genre_lessons)
    if craft_lessons is not None:
        need[CRAFT_TOPIC] = len(craft_lessons)
    if not need:
        return warn("23 lessons ack", "no ledger topics found — nothing to ack")

    if ack is None:
        return add("23 lessons ack", False,
                   "NO LESSONS_ACK — declare the counts this plan was written against: "
                   f"LESSONS_ACK = {{{', '.join(repr(k)+': '+str(v) for k,v in need.items())}}}")
    if isinstance(ack, int):
        ack = {key: ack}
    if not isinstance(ack, dict):
        return add("23 lessons ack", False, f"LESSONS_ACK must be a dict, got {type(ack).__name__}")

    bad, okd = [], []
    for t, n in need.items():
        got = ack.get(t)
        if got is None:
            bad.append(f"'{t}' NOT ACKNOWLEDGED (holds {n})"
                       + (" — this is the pillar-independent craft topic; every plan reads it"
                          if t == CRAFT_TOPIC else ""))
        elif got < n:
            bad.append(f"'{t}' STALE: acked {got}, ledger holds {n} — read {got}..{n-1}, "
                       f"update the premortem, re-ack")
        elif got > n:
            bad.append(f"'{t}' acked {got} but ledger holds {n} — an invented count is "
                       f"worse than none. Hard rule 2 applies to lessons too.")
        else:
            okd.append(f"{t} {n}")
    if bad:
        return add("23 lessons ack", False, " · ".join(bad))
    r = add("23 lessons ack", True, "plan written against " + " + ".join(okd))
    # OTHER PILLARS' genre lessons are not required reading, but a neighbouring pillar
    # often holds the closest prior art — surfaced, never blocking.
    others = {k: len(v.get("lessons", [])) for k, v in (_ledger_topics() or {}).items()
              if k not in need and v.get("lessons")}
    if others:
        big = sorted(others.items(), key=lambda x: -x[1])[:3]
        # BLOCKS since 2026-08-08. This was a WARNING, and it is the single
        # mechanism behind his loudest complaint: "it keeps on happening,
        # especially when i switch frm vlog content to car review then switch to
        # car cinematic there turns out to be more and more problem".
        # planqc 23 only blocks on the topics a plan DECLARES, so a lesson filed
        # under another genre was invisible - not deprioritised, invisible. The
        # neighbouring pillar is almost always the closest prior art there is.
        # Reading it is now required, exactly like your own genre's.
        stale_n = [f"{k} {n}" for k, n in sorted(big)
                   if int(ack.get(k, -1)) != n]
        if stale_n:
            add("23b neighbouring genres", False,
                "the closest prior art is in another pillar and this plan has not "
                "read it - ack these too: " + " · ".join(stale_n)
                + "  (a lesson filed under another genre is INVISIBLE to check 23, "
                  "which is why switching format keeps surfacing old problems)")
        else:
            add("23b neighbouring genres", True,
                "neighbouring pillars' lessons acked: "
                + " · ".join(f"{k} {n}" for k, n in sorted(big)))
    return r


LIGHT_ORDER = ["dawn", "morning", "midday", "afternoon", "golden",
               "dusk", "blue", "night"]

# HIS TAXONOMY, 2026-08-07, taught verbatim: "lets add on linkage determination also
# includes, events, actions, motion, activity, audio, places". The first seven kinds
# were mine and they were thin - they described what a shot CONTAINS. His six describe
# what a shot DOES, which is what an editor actually cuts on. Six added, none removed;
# every existing plan still validates. Full definitions and the decidable test for each
# are in 28-linkage-master.md. ADDITIVE ONLY - his standing rule.
CARRY_KINDS = {
    # --- the original seven: what a shot CONTAINS
    "motion":      "something moving in A keeps moving into B",
    "gaze":        "A looks off-frame, B is what A was looking at",
    "subject":     "the same person/object is in both",
    "object":      "a specific thing leaves A and appears in B",
    "light":       "the same light state continues across the cut",
    "sound":       "a sound starts in A and resolves in B",
    "consequence": "B happens BECAUSE of A — the state of the world changed",
    # --- HIS SIX, 2026-08-07: what a shot DOES
    "event":       "a discrete thing HAPPENS in A and B carries its aftermath - the "
                   "splash, the tear, the slam. The event is the join, not the subject.",
    "action":      "MATCH ON ACTION: one deliberate act begins in A and completes in B. "
                   "The oldest invisible cut there is. Needs a clip that PERFORMS the "
                   "verb (craft L58: five KK boundaries were built on verbs their clips "
                   "never performed - measured flow 0.50 on 'walking toward lens').",
    "activity":    "an ongoing occupation continues across the cut - swimming, driving, "
                   "walking the trail. SPAN-LEVEL, not boundary-level: it is the only "
                   "kind that describes a run of shots rather than a join, and it is "
                   "what makes a sequence read as ONE stretch of time.",
    "audio":       "the SOUND carries the cut - river noise continues, an engine note "
                   "answers, the bed breathes through. Distinct from 'sound': that one "
                   "is a transient starting in A and resolving in B; this one is a "
                   "continuous audio bed spanning the join and hiding it.",
    "place":       "the same GEOGRAPHY is on both sides - same gorge, same road, same "
                   "valley. Cheapest carry to verify (both shots cite the same plate) "
                   "and the one that stops a film reading as a slideshow of postcards. "
                   "verify 14 already measures shots/places <= 2.0.",
}


def _boilerplate(P):
    """Words present in EVERY source prompt — the shared realism/look block.

    CAUGHT BEFORE SHIPPING, 2026-08-05: the first version of check 29 searched the whole
    source prompt, and every WRX boundary offered the same 14 shared words
    ('specular', 'cartoonish', 'videogame'...) because _LOOK is appended to all nine
    sources. A token drawn from boilerplate is present on BOTH sides of EVERY boundary,
    so the check would have passed on any plan — a VACUOUS PASS wearing a green tick.
    Boilerplate is subtracted so a carry must be SHOT-SPECIFIC."""
    sets = []
    for s in (getattr(P, "SOURCES", {}) or {}).values():
        if isinstance(s, (list, tuple)):
            txt = " ".join(x for x in s if isinstance(x, str)).lower()
            sets.append(set(re.findall(r"[a-z]{3,}", txt)))
    if len(sets) < 2:
        return set()
    common = set.intersection(*sets)
    return common


def _shot_text(P, i, boiler=frozenset()):
    """What the plan says about shot i ALONE: its note, plus the part of its source
    prompt that is not shared with every other source."""
    sh = P.SHOTS[i]
    note = " ".join(str(x) for x in sh[3:]) if len(sh) > 3 else ""
    s = getattr(P, "SOURCES", {}).get(sh[0])
    src = ""
    if isinstance(s, (list, tuple)):
        src = " ".join(x for x in s if isinstance(x, str))
    words = [w for w in re.findall(r"[a-z]{3,}", src.lower()) if w not in boiler]
    return (note.lower() + " " + " ".join(words)).strip()


def check_linkage_carry(P):
    """HIS DOCTRINE, 2026-08-05: "there must be a linkage that is important, when there
    is linkage then it feels like a story".

    Check 24 only proves a linkage STRING EXISTS. KK v15 passed it 19/19 and the eye
    found 5 of 19 that actually land. Two failures were decidable from the plan text
    alone, for free:

      boundary 15->16 declared  "the car returns: callback in the same gold light"
      the shot note for 16 says "boardwalk at dusk - THE PLACE, EMPTIED"

    The plan contradicted itself IN WRITING and shipped. That is the P7 callback
    failure, one build after P7 was written.

    So a linkage stops being prose and becomes a CARRY: a kind, and a TOKEN that must
    be findable in the writing of BOTH shots it joins. If the token is not on both
    sides, the connection exists only in my head.

        LINKAGE = [("object", "car", "car exits right -> boats drift the same way"),
                   ("gaze", "horizon", "his eyeline -> the boats on it"), ...]

    Legacy prose entries still parse and are reported UNVERIFIABLE, never OK - a
    linkage nobody can check is not evidence of a story.
    """
    lk = getattr(P, "LINKAGE", None)
    n_b = len(P.SHOTS) - 1
    if not lk:
        return add("29 linkage carry", False, "NOT MEASURED - no LINKAGE to read")
    if isinstance(lk, dict):
        lk = [lk.get(i, "") for i in range(n_b)]
    boiler = _boilerplate(P)
    prose, typed, bad_kind, missing, vac = [], [], [], [], []
    for i in range(min(n_b, len(lk))):
        e = lk[i]
        if not isinstance(e, (list, tuple)) or len(e) < 2:
            prose.append(i); continue
        kind, token = str(e[0]).lower().strip(), str(e[1]).lower().strip()
        typed.append(i)
        if kind not in CARRY_KINDS:
            bad_kind.append((i, kind)); continue
        a, b = _shot_text(P, i, boiler), _shot_text(P, i + 1, boiler)
        if token and token in boiler:
            vac.append((i, token)); continue
        if token and not (token in a and token in b):
            side = "shot %d" % (i if token not in a else i + 1)
            missing.append((i, token, side))
    if prose and not typed:
        return add("29 linkage carry", False,
                   f"all {len(prose)} linkages are PROSE - UNVERIFIABLE. KK v15 shipped "
                   f"19 prose linkages and 14 did not land. Convert to (kind, token, "
                   f"prose); kinds: {', '.join(sorted(CARRY_KINDS))}")
    detail = f"{len(typed)} typed / {len(prose)} prose"
    if bad_kind:
        detail += " | unknown kind: " + ", ".join(f"{i}:{k}" for i, k in bad_kind[:3])
    if missing:
        detail += " | TOKEN NOT ON BOTH SIDES: " + ", ".join(
            f"boundary {i} '{t}' absent from {s}" for i, t, s in missing[:3])
    if vac:
        detail += " | BOILERPLATE TOKEN (present in every source, proves nothing): " \
                  + ", ".join(f"{i}:'{t}'" for i, t in vac[:3])
    ok = not bad_kind and not missing and not prose and not vac
    r = add("29 linkage carry", ok, detail)
    if prose and typed:
        warn("29b prose linkages", f"boundaries {prose[:8]} are prose - not checkable")
    return r


def check_time_monotonic(P):
    """MEASURED on KK v15: the cut runs golden -> night -> DAYLIGHT -> sunset ->
    morning -> night -> golden, with a "6PM IN KK BAH" card on screen over the noon
    footage. The plan's own premortem promised "no cut jumps backwards in time" and
    nothing enforced it, because no shot ever declared what time it was.

    Declare SHOT_TIME per shot. Backwards is a FAIL unless the boundary is listed in
    TIME_JUMPS with a reason: a declared jump is a choice, an undeclared one is the
    continuity break he reads as "no story"."""
    n = len(P.SHOTS)
    tl = getattr(P, "SHOT_TIME", None)
    if not tl:
        return add("30 time monotonic", False,
                   "NOT DECLARED - every shot must name its light state ("
                   + "/".join(LIGHT_ORDER) + "). KK v15 ran night->daylight->morning "
                   "under a '6PM' card and no gate could see it.")
    if isinstance(tl, dict):
        tl = [tl.get(i) for i in range(n)]
    unknown = [(i, t) for i, t in enumerate(tl) if t not in LIGHT_ORDER]
    if unknown:
        return add("30 time monotonic", False,
                   "unknown light state: " + ", ".join(f"{i}:{t}" for i, t in unknown[:4]))
    jumps = set(getattr(P, "TIME_JUMPS", {}) or {})
    idx = [LIGHT_ORDER.index(t) for t in tl]
    back = [i for i in range(n - 1) if idx[i + 1] < idx[i] and i not in jumps]
    skip = [i for i in range(n - 1) if idx[i + 1] - idx[i] >= 3 and i not in jumps]
    detail = f"{tl[0]} -> {tl[-1]} across {n} shots"
    if back:
        detail += f" | RUNS BACKWARDS at boundaries {back[:5]}"
    if skip:
        detail += f" | skips >=3 light states at {skip[:5]}"
    return add("30 time monotonic", not back and not skip, detail)


def check_consequence_spine(P):
    """The thing underneath every note he has given me: "no story no linkage from 1st
    starting visual hook then leads to another scene then connect it with a twist".

    A boundary can carry motion, light or a subject and still change NOTHING. Measured
    on KK v15: 9 of 20 shots had optical flow under 0.6 and nothing happened to the
    person in 28 seconds. A story needs boundaries where B occurs BECAUSE of A.

    Floor: one consequence per ~6 boundaries, minimum 2. NON-BLOCKING on purpose - I am
    not qualified to score whether a story works, only to COUNT the boundaries that
    even attempt it and put the number in front of him."""
    lk = getattr(P, "LINKAGE", None) or []
    n_b = len(P.SHOTS) - 1
    if isinstance(lk, dict):
        lk = [lk.get(i, "") for i in range(n_b)]
    cons = [i for i, e in enumerate(lk)
            if isinstance(e, (list, tuple)) and str(e[0]).lower().strip() == "consequence"]
    need = max(2, -(-n_b // 6))
    tail = (f"at {cons}" if cons else
            "- NOTHING HAPPENS BECAUSE OF ANYTHING; this is a slideshow with captions")
    return add("31 consequence spine", len(cons) >= need,
               f"{len(cons)} consequence boundaries, floor {need} {tail}", False)



# ---------------------------------------------------------------- 32 RELATIONSHIPS
_REL_PAIRS = {
    # key: (what must agree, the failure that put it on this list)
    "subject_vs_background":
        ("a subject's implied geometry must agree with the world behind it",
         "desafarm 2026-08-07, HIS CATCH: 'nev driving a car horizontally but the "
         "road is going vertically'. A SIDE window (wing mirror visible, no steering "
         "wheel in frame) with the road receding straight away through it = the car "
         "is driving at 90 degrees to its own road. Both halves were fine alone."),
    "performance_vs_sound":
        ("a performed emotion must be carried by audio, not mime",
         "desafarm, HIS CATCH: 'nevs expression have no sfx or other elements to back "
         "it up'. MEASURED: the shot where he laughs out loud has a voice-band ratio "
         "of 0.25 and the shot where he is shocked 0.16, against 0.19 for a shot of "
         "EMPTY HILLS. He performed into silence."),
    "bed_vs_foley":
        ("music must not cover the diegetic sound of the place",
         "desafarm, HIS CATCH: 'the bgm is slightly louder than everything it covers "
         "all the sfx, and foley'. MEASURED: soundscape similarity across cuts 0.935 "
         "vs 0.947 mid-shot control - a goat pen and a car interior sounded the same."),
    "card_vs_card":
        ("no two cards may occupy the caption zone at the same time",
         "desafarm: two captions printed through each other for 2.5s, 20.9-23.4s. "
         "planqc 12 and verify 6 both checked the ZONE and neither checked the CLOCK."),
    "event_vs_window":
        ("the shot must be long enough to contain the whole event",
         "desafarm, HIS CATCH: 'some scenes important events are cutted out'. Shot 5 "
         "ended at 96% of its own action peak, shot 14 at 83%, and the hook ended with "
         "the bottle still in his hand - the goat takes it 13 seconds later."),
    "arc_vs_shot_order":
        ("a clip with an internal arc must be used in that arc's order",
         "desafarm: source H was written startled -> laugh, MONOTONIC. Delivered as "
         "laugh at 15.8s and startled at 20.9s. He reacts after he has already laughed."),
    "picture_grid_vs_music_grid":
        ("a transition must not shift the picture off the music",
         "desafarm: the 240ms whip SHORTENED shot 8 by 197ms instead of overlapping, "
         "so every cut after it sits ~170ms early against a bed that kept its tempo."),
    "clip_variety_vs_shot_count":
        ("a source may carry N shots only if it can supply N distinct looks",
         "desafarm, HIS CALL: the duplicates were 'at the video editing side'. Measured "
         "over every non-overlapping window pair: source C could have delivered "
         "0.817/0.798 and the editor chose 0.928/0.986 - the editor's fault. Source E's "
         "BEST available pair was 0.911/0.973 - that one is a PLAN error, the clip "
         "could never have carried two shots."),
}


def check_threshold_provenance(P):
    """33 THRESHOLD PROVENANCE - a number tuned on one format is not a constant.

    2026-08-08, from his sharpest complaint: "it keeps on happening, especially
    when i switch frm vlog content to car review then switch to car cinematic
    there turns out to be more and more problem".

    Two mechanisms cause that. Lessons not travelling is one, and check 23b now
    blocks on it. This is the other, and it is the silent one: numbers DO travel,
    when they should not. engine.py's shot_match_clamp carries a comment saying it
    was "tuned on a NIGHT car edit, one light state end to end" - then travel_vlog
    runs golden hour to night by design and the same 0.14 quietly stopped working.
    Nobody changed it. It just started being wrong.

    ledgers/thresholds.json now records what every tuned number was fitted on, how
    many samples, and which pillars it is allowed to run on. This check refuses a
    plan whose pillar inherits a threshold that was never derived for it.

    And it reports what is PROVISIONAL, because that is the list the future
    scanning agent exists to replace. His words: his judgment is the fastest
    feedback available, not the ceiling - the standard is meant to come from
    measuring what actually wins."""
    path = os.path.join(HERE, "ledgers", "thresholds.json")
    if not os.path.exists(path):
        return warn("33 thresholds", "no ledgers/thresholds.json - every tuned "
                                     "number in this build is unprovenanced")
    try:
        T = json.load(open(path, encoding="utf-8")).get("thresholds", [])
    except Exception as e:
        return add("33 thresholds", False, f"thresholds.json unreadable: {str(e)[:60]}")
    pil = getattr(P, "PILLAR", "")
    borrowed = [t for t in T
                if "*" not in (t.get("pillars") or [])
                and pil not in (t.get("pillars") or [])
                and t.get("where", "").startswith(("engine", "assets"))]
    prov = [t["id"] for t in T if t.get("status") in ("provisional", "guess")
            and ("*" in (t.get("pillars") or []) or pil in (t.get("pillars") or []))]
    if borrowed:
        return add("33 thresholds", False,
                   f"'{pil}' would inherit {len(borrowed)} number(s) never derived "
                   f"for it: " + " · ".join(f"{t['id']} (fitted on {t['fitted_on']})"
                                            for t in borrowed[:3]))
    r = add("33 thresholds", True,
            f"no borrowed numbers for '{pil}'; {len(prov)} of its thresholds are "
            f"PROVISIONAL and awaiting real measurement")
    if prov:
        warn("33b provisional", "these are placeholders, not constants - the "
                                "scanning agent replaces them: " + ", ".join(prov[:6]))
    return r


def check_transition_contract(P):
    """34 TRANSITION CONTRACT - does the plan's transition agree with its own timeline?

    THE FAILURE THIS IS BUILT FROM. desafarm declared a 240 ms whip after shot 8.
    The engine SHORTENED shot 8 by 197 ms instead of OVERLAPPING it. Spacing between
    every other shot stayed perfect, so no per-shot check could see anything wrong -
    the back 60% of the film just sat ~170 ms early against a verified 97.5 BPM grid.

    The bug was never in the whoosh. It was that nothing in the system stated whether
    a transition CONSUMES time or OVERLAPS it. assets/transitions/TRANSITIONS.json
    states it now, and this check refuses a plan that contradicts it.
    """
    import json as _j
    bank = _first(os.path.join(HERE, "assets", "transitions", "TRANSITIONS.json"))
    if not bank:
        return warn("34 transition contract",
                    "assets/transitions/TRANSITIONS.json not found - transitions are "
                    "running on whatever the plan happens to say")
    T = {t["kind"]: t for t in _j.load(open(bank, encoding="utf-8"))["transitions"]}

    after = list(getattr(P, "BLEND_AFTER", []) or [])
    if not after:
        return add("34 transition contract", True,
                   "no transitions declared - every cut is hard")

    kind = str(getattr(P, "BLEND_KIND", "") or "").strip()
    width_ms = float(getattr(P, "BLEND_WIDTH", 0.0) or 0.0) * 1000.0
    spec = T.get(kind)
    if not spec:
        return add("34 transition contract", False,
                   f"BLEND_KIND '{kind}' is not in the transition bank. Known kinds: "
                   f"{', '.join(sorted(T))}. An undeclared transition is an undeclared "
                   f"timing rule, and that is exactly how the whip drifted.")

    bad = []
    if abs(width_ms - spec["duration_ms"]) > 1.0:
        bad.append(f"BLEND_WIDTH is {width_ms:.0f} ms but the bank defines '{kind}' as "
                   f"{spec['duration_ms']} ms")

    # the whip bug, made un-shippable
    tgt = float(getattr(P, "TARGET_S", 0) or 0)
    shots = list(getattr(P, "SHOTS", []) or [])
    if spec["timing"] == "overlap":
        # ONE MECHANISM (2026-08-11, closes PENDING 2.3). The engine has reserved
        # blend-width on overlap transitions since 2026-08-08; requiring every plan
        # to ALSO hand-declare BLEND_RESERVES_OVERLAP made two mechanisms that
        # agree by hand. The engine's contract constant is now the source of
        # truth; a plan flag still wins if declared (a plan may opt OUT with
        # False to document a deliberate deviation).
        _reserved = getattr(P, "BLEND_RESERVES_OVERLAP", None)
        if _reserved is None:
            try:
                from engine import BLEND_RESERVES_OVERLAP as _reserved
            except Exception:
                _reserved = False
        if not _reserved:
            bad.append(
                f"'{kind}' is timing='overlap': the engine must RESERVE {spec['duration_ms']} ms "
                f"of extra source on each of the {len(after)} blended shots, or the timeline "
                f"pulls {spec['duration_ms'] * len(after):.0f} ms early - the desafarm whip "
                f"exactly. engine.BLEND_RESERVES_OVERLAP is False/absent and the plan does "
                f"not declare it either.")
    else:
        eaten = spec["duration_ms"] * len(after) / 1000.0
        if tgt and eaten > 0.05:
            bad.append(f"'{kind}' is timing='consume': {len(after)} transitions eat "
                       f"{eaten:.2f}s. TARGET_S={tgt:.2f} must already include that loss.")

    # a transition that needs motion cannot sit on a shot too short to have any
    mn = float(spec.get("min_shot_len_s") or 0)
    if mn and shots:
        try:
            lens = [float(s[1]) for s in shots]
            for i in after:
                if 0 <= i < len(lens) and lens[i] < mn:
                    bad.append(f"shot {i} is {lens[i]:.2f}s but '{kind}' needs >= {mn}s")
        except Exception:
            pass

    cap = spec.get("max_per_film")
    if cap and len(after) > cap:
        bad.append(f"{len(after)} '{kind}' transitions, the bank caps it at {cap} "
                   f"({spec['why'].split('.')[0]})")

    if bad:
        return add("34 transition contract", False, " | ".join(bad[:4]))
    return add("34 transition contract", True,
               f"{len(after)}x '{kind}' {spec['duration_ms']}ms timing={spec['timing']} "
               f"- matches assets/transitions/TRANSITIONS.json")


def check_relationships(P):
    """32 RELATIONSHIPS - the check that exists because of how the others failed.

    Every defect Gavril found in DESAFARM_CINEMATIC_v2 was a RELATIONSHIP between
    two elements that each passed on its own. The car passed. The road passed. The
    music passed. The foley passed. The cards each sat in the zone. The shot lengths
    matched the beat grid. Thirty-four plan checks and fifteen verify checks all
    looked at elements, and not one asked whether the elements AGREED.

    So the plan must now name, for each pair below, how it holds that pair together.
    This does not measure the film - it forces the mastermind to predict the failure
    at planning time, which is the only place it is free to fix."""
    rel = getattr(P, "RELATIONSHIPS", None)
    if not isinstance(rel, dict):
        return add("32 relationships", False,
                   "NO RELATIONSHIPS block - the plan does not say how it keeps "
                   f"{len(_REL_PAIRS)} known element-pairs in agreement: "
                   + ", ".join(sorted(_REL_PAIRS)))
    missing = [k for k in _REL_PAIRS if not str(rel.get(k, "")).strip()]
    thin = [k for k, v in rel.items()
            if k in _REL_PAIRS and 0 < len(str(v).strip()) < 40]
    if missing:
        return add("32 relationships", False,
                   f"{len(missing)} pair(s) unaddressed: " + ", ".join(sorted(missing)))
    if thin:
        return add("32 relationships", False,
                   "answer is too thin to be a plan (under 40 chars): "
                   + ", ".join(sorted(thin)))
    return add("32 relationships", True,
               f"all {len(_REL_PAIRS)} element-pairs have a stated mitigation")


def check_linkage(P, name):
    """Every shot is planned to CONNECT to its neighbours — exit motion into entry
    motion, lighting, direction — so the editor gets footage that already wants to
    join. Relational, planned, not discovered (his doctrine, 2026-08-04)."""
    n_b = len(P.SHOTS) - 1
    lk = getattr(P, "LINKAGE", None)
    if not lk:
        return add("24 linkage", False,
                   f"NO LINKAGE — the plan must declare a connection intent for each of "
                   f"its {n_b} boundaries (LINKAGE = [intent, ...] or {{i: intent}}).")
    if isinstance(lk, dict):
        lk = [lk.get(i, "") for i in range(n_b)]
    empty = [i for i in range(n_b) if i >= len(lk) or not str(lk[i]).strip()]
    ok = not empty
    r = add("24 linkage", ok,
            f"all {n_b} boundaries carry a connection intent" if ok
            else f"boundaries with NO declared connection: {empty}")
    # relational measurement, free at plan time, when ingest data exists
    mp = os.path.join(HERE, "projects", name, "clips", "manifest.json")
    if ok and os.path.exists(mp):
        man = json.load(open(mp, encoding="utf-8"))
        have = any("luma_mean" in v or "motion_mean" in v for v in man.values())
        if not have:
            warn("24b linkage measured", "manifest carries no luma/motion means yet — "
                 "extend ingest.py to record them; declared intents stay UNVERIFIED")
        else:
            jumps = []
            for i in range(n_b):
                a, b = P.SHOTS[i][0], P.SHOTS[i + 1][0]
                la = man.get(a, {}).get("luma_mean")
                lb = man.get(b, {}).get("luma_mean")
                if la is not None and lb is not None and abs(la - lb) > 60:
                    jumps.append(f"{i}({a}->{b}: {la:.0f}->{lb:.0f})")
            if jumps:
                warn("24b linkage measured",
                     f"brightness jump > 60 luma at boundaries {jumps} — declared "
                     "continuity vs measured light disagree, LOOK before build")
            else:
                add("24b linkage measured", True,
                    "no boundary joins clips more than 60 luma apart", False)
    return r


def check_field_sanity(P):
    """25 FIELD SANITY (2026-08-05, red-team wave 1). Three holes found by feeding
    hostile plans: DELOGO fully out of frame PASSED (engine dies mid-render on a
    cryptic ffmpeg error); SFX_OVERLAYS reading past clip EOF PASSED (ffmpeg
    extracts SHORT silently - the dip the overlay covers ships uncovered); CJK/
    emoji cards PASSED word count and render as identical TOFU boxes in fallback
    fonts. Every plan literal the engine consumes must be provably consumable."""
    bad = []
    n = len(P.SHOTS)
    tl, total = P.timeline()

    for i, box in (getattr(P, "DELOGO", {}) or {}).items():
        if not 0 <= i < n:
            bad.append(f"DELOGO shot {i} out of range 0..{n-1}")
            continue
        try:
            x, y, w, h = [int(v) for v in box]
            if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > P.W or y + h > P.H:
                bad.append(f"DELOGO {i}=({x},{y},{w},{h}) outside {P.W}x{P.H} or empty")
        except Exception:
            bad.append(f"DELOGO {i}={box!r} not (x,y,w,h)")

    fit = total - len(set(P.BLEND_AFTER)) * P.BLEND_WIDTH   # blends COMPRESS the timeline
    for ov in (getattr(P, "SFX_OVERLAYS", []) or []):
        src, ct, dur_, vt = ov[0], float(ov[1]), float(ov[2]), float(ov[3])
        if src not in P.SOURCES:
            bad.append(f"SFX_OVERLAY src {src!r} not a source")
        if ct < 0 or dur_ <= 0 or ct + dur_ > P.CLIP_S:
            bad.append(f"SFX_OVERLAY {src}@{ct}+{dur_}s reads past the {P.CLIP_S}s clip "
                       f"- ffmpeg extracts SHORT silently, the overlay ships thin")
        if vt + dur_ > fit + 0.05:
            bad.append(f"SFX_OVERLAY at video {vt}+{dur_}s past the post-blend end "
                       f"({fit:.2f}s) - placed audio would be truncated")

    orphans = [k for k in (getattr(P, "FOLEY", {}) or {}) if not 0 <= k < n]
    if orphans:
        bad.append(f"FOLEY gains for nonexistent shots: {orphans}")

    if not getattr(P, "CARDS_NON_ASCII_OK", False):
        for c in P.CARDS:
            odd = sorted({ch for ch in c[0] if ord(ch) > 126})
            if odd:
                bad.append(f"card {c[0]!r} carries non-ASCII {odd} - fallback fonts "
                           f"render TOFU boxes; transliterate or declare "
                           f"CARDS_NON_ASCII_OK=True after a MEASURED glyph test")

    return add("25 field sanity", not bad,
               "DELOGO in-frame · overlays fit clip and post-blend timeline · "
               "no orphan FOLEY keys · cards ASCII-safe"
               if not bad else " · ".join(bad))


def check_style_declared(P, pf):
    """26 STYLE DECLARED (2026-08-05). THE ANTI-INHERITANCE GATE.

    Everything this system learned was learned on ONE pillar. The car's look and
    signature were written as CONSTANTS, so a new pillar did not start with no
    style — it silently INHERITED the car's, and nothing said so. Measured that
    day: clipqc's night band (18-90) would REJECT daylight vlog footage at 142-165
    ('regenerate this clip, 22.5cr'); engine laid a phonk whoosh on every cut
    regardless of genre; check 19 switched itself off for non-car pillars.

    A pillar must now DECLARE its style, and a PROVISIONAL band must say so out
    loud. Silence is never a style."""
    pil = getattr(P, "PILLAR", "")
    if not pf:
        return warn("26 style declared", "no profile — cannot verify style")
    st = pf.get("style")
    if not st:
        return add("26 style declared", False,
                   f"pillar '{pil}' declares NO style block in PILLAR-PROFILES.json — it "
                   f"would silently inherit car_cinematic's night band, whoosh-on-every-cut "
                   f"and hero-foley doctrine. Add a style block before planning this pillar.")
    need = ["brightness_band", "brightness_source", "edit_sfx", "sound_gate", "cut_spine"]
    missing = [k for k in need if not st.get(k)]
    if missing:
        return add("26 style declared", False, f"pillar '{pil}' style missing {missing}")
    prov = not str(st["brightness_source"]).startswith("MEASURED")
    fam = pf.get("family", "?")
    r = add("26 style declared", True,
            f"family={fam} · spine={st['cut_spine']} · sfx={st['edit_sfx']} · "
            f"sound={st['sound_gate']} · luma{st['brightness_band']}")
    if prov:
        warn("26b style provisional",
             f"'{pil}' brightness band is PROVISIONAL, not measured — no footage exists for "
             f"this pillar yet. It is deliberately WIDE (a wrong reject costs 22.5cr). "
             f"RE-DERIVE from the first 9 real clips at ingest, then mark it MEASURED.")
    if st["cut_spine"] == "sentence":
        warn("26c editor exists?", f"'{pil}' declares a SENTENCE spine — the speech-led "
             f"editor is NOT BUILT. engine.py cuts to a beat grid only. This plan cannot "
             f"be rendered yet, however well it gates.")
    return r


def check_framing_diversity(P):
    """28 FRAMING DIVERSITY (2026-08-05, Gavril's catch on KK v1: "a few duplicated
    images / scenes and shots").

    Root cause, MEASURED: sources A, C, E and I all cited the same waterfront plate,
    and every one of them generated the plate's own composition — a boardwalk receding
    to the sea. Shots 0, 1, 5, 12 and 16 were one image seen five times, from THREE
    different sources. A reference plate anchors PLACE; left unqualified it also
    anchors FRAMING, and the model returns the picture it was given.

    Nothing downstream could prevent this: the clips were already paid for. So each
    source must DECLARE its camera position, and two sources sharing a plate may not
    share a framing. Free, decidable from the plan, before a credit is spent."""
    fr = getattr(P, "FRAMING", None)
    if not fr:
        return add("28 framing diversity", False,
                   "NO FRAMING — every source must declare its camera position "
                   "(FRAMING = {src: 'wide static' | 'low tracking' | 'macro' | "
                   "'high angle' | 'close handheld' | ...}). Sources that cite the same "
                   "plate and do not declare DIFFERENT framings will return that plate's "
                   "own composition — measured on KK v1: 5 shots, one image.")
    missing = [k for k in P.SOURCES if k not in fr]
    if missing:
        return add("28 framing diversity", False, f"sources with no declared framing: {missing}")
    # group by shared plate; within a group, framings must be distinct
    clash = []
    byplate = {}
    for k, v in P.SOURCES.items():
        for pl in v[3]:
            byplate.setdefault(pl, []).append(k)
    for pl, keys in byplate.items():
        seen = {}
        for k in keys:
            f = str(fr[k]).strip().lower()
            if f in seen:
                clash.append(f"plate '{pl}': {seen[f]} and {k} both '{f}'")
            seen[f] = k
    return add("28 framing diversity", not clash,
               f"{len(fr)} sources, all framings distinct within each shared plate"
               if not clash else " · ".join(clash))


def check_identity_coverage(P):
    """27 IDENTITY COVERAGE (2026-08-05). FACE_OPTOUT lets a plan declare a human shot
    as PRESENCE rather than a face beat — the back/profile "looking out at the view"
    composition is real vlog language and KK's viewpoint shot deliberately turns away.
    But identity is J4's ABSOLUTE veto, so it must never be possible to opt out of it
    everywhere: at least two human sources must still be expected to carry a readable
    face, and every opt-out must state a reason."""
    humans = [k for k, v in P.SOURCES.items()
              if v[2].upper() == "HUMAN" or "man from the" in v[4].lower()]
    if not humans:
        return warn("27 identity coverage", "no human sources — nothing to verify")
    opt = getattr(P, "FACE_OPTOUT", {}) or {}
    blank = [k for k, v in opt.items() if not str(v).strip()]
    unknown = [k for k in opt if k not in P.SOURCES]
    carrying = [k for k in humans if k not in opt]
    n_shots = sum(1 for s, _c, _k, _t in P.SHOTS if s in carrying)
    bad = []
    if blank:
        bad.append(f"FACE_OPTOUT entries with no stated reason: {blank}")
    if unknown:
        bad.append(f"FACE_OPTOUT names sources that do not exist: {unknown}")
    if len(carrying) < 2:
        bad.append(f"only {len(carrying)} human source(s) still carry a readable face "
                   f"({carrying}) — identity is J4's ABSOLUTE veto and cannot be waived "
                   f"across the board; keep at least 2")
    return add("27 identity coverage", not bad,
               f"{len(humans)} human sources, {len(opt)} declared presence-only, "
               f"{len(carrying)} carrying identity ({carrying}) across {n_shots} shots"
               if not bad else " · ".join(bad))


# ---------------------------------------------------------------- 17 COST
def check_cost(P, balance):
    c = P.cost()
    d = (f"{c['clips']} clips x {c['per_clip']}cr = {c['generation']}cr "
         f"+ {c['plates']}cr plates = {c['total']}cr")
    if balance is None:
        return warn("17 cost", d + " - balance NOT MEASURED, measure before spending")
    pct = 100.0 * c["total"] / balance
    return add("17 cost", c["total"] <= balance,
               d + f" = {pct:.1f}% of a MEASURED {balance:.2f}cr")


# ---------------------------------------------------------------- DOC
def write_doc(P, path, name="?"):
    tl, total = P.timeline()
    c = P.cost()
    L = []
    a = L.append
    a(f"# PRODUCTION DOC — {P.PROJECT}")
    a(f"### Generated from `plans/{name}.py` by `planqc.py`. Do not edit by hand — edit the plan.")
    a("")
    a(f"**{len(P.SHOTS)} shots · {total:.2f}s · {P.W}x{P.H} @ {P.FPS}fps · "
      f"{P.PILLAR} · {P.BPM:.0f} BPM · mode `{P.MODE}` {P.RES}**")
    a("")
    a("---")
    a("")
    a("## PLATES — generate and LOOK at these first")
    a("")
    a("| plate | res | cr | status | must show |")
    a("|---|---|---|---|---|")
    for k, v in P.PLATES.items():
        a(f"| `{k}` | {v['res']} | {v['cr']} | {v['status']} | {v['must_show']} |")
    a("")
    a("---")
    a("")
    a("## TIMELINE")
    a("")
    a("| # | in | dur | kind | source | crop | note |")
    a("|---|---|---|---|---|---|---|")
    for i, ((s, cr, k, note), (st, d, _k)) in enumerate(zip(P.SHOTS, tl)):
        b = " ◆" if i in P.BLEND_AFTER else ""
        a(f"| {i} | {st:.2f} | {d:.2f} | {k}{b} | `{s}` {P.SOURCES[s][0]} | {cr:.2f}x | {note} |")
    a("")
    a("◆ = blend after this shot (`%s`, %.0fms)" % (P.BLEND_KIND, P.BLEND_WIDTH * 1000))
    a("")
    a("---")
    a("")
    a("## CARDS — y=%.2f lower third, never centre" % P.CARD_Y)
    a("")
    a("| text | shots | kind |")
    a("|---|---|---|")
    for t, f, n, kind in P.CARDS:
        a(f"| **{t}** | {f}–{f+n-1} | {kind} |")
    a("")
    a("---")
    a("")
    pv = getattr(P, "PREVIZ", None)
    if pv:
        a("## PREVIZ — sketch-grade, never enters generation")
        a("")
        sheet = pv[sorted(k for k in pv if k.startswith("sheet"))[-1]]
        a(f"![previz]({sheet})")
        a("")
        a(f"_{pv['note']}_")
        if pv.get("limit"):
            a("")
            a(f"**LIMIT:** {pv['limit']}")
        a("")
        a("Timeline board (real frames appear here automatically once clips exist):")
        a("")
        a("![board](analysis/STORYBOARD.png)")
        a("")
        a("---")
        a("")
    a("## GENERATION PROMPTS — verbatim, as they will be sent")
    a("")
    for k, (lab, _col, act, plates, prompt) in P.SOURCES.items():
        a(f"### `{k}` · {lab}  ·  act: {act}  ·  plates: {', '.join(plates)}")
        a("")
        a("```")
        a(prompt)
        a("```")
        a("")
    a("---")
    a("")
    a("## THE EDIT — what the engine will do, with computed times")
    a("")
    scale_note = "times below are PLANNED; blends compress them - the engine re-times "\
                 "cards and declares ACTUAL cut boundaries after building."
    a(f"_{scale_note}_")
    a("")
    # FIX 2026-08-06: everything below used to print WRX numbers — "150 BPM", "0.400s",
    # "profile 6-33%", "drift-phonk", "whoosh" on every cut — no matter what plan
    # generated it. For a 100 BPM hero_only chill plan the doc CONTRADICTED the plan it
    # was generated from, and this is the doc a human reads before spending. Now every
    # number is read from the plan or the pillar profile.
    try:
        _pf = profile(P.PILLAR)
    except Exception:
        _pf = {}
    _sty = (_pf.get("style") or {})
    _sfx_policy = str(_sty.get("edit_sfx", "full")).lower()
    _br = _pf.get("blended_range") or [6, 33]
    a(f"**Cut grid** — every boundary on the {P.BPM:g} BPM beat ({P.BEAT:.3f}s), "
      "frame-exact (`-frames:v`), each shot centred on a measured action peak, exposure "
      "matched on rendered segments BEFORE blending.")
    a("")
    a("| after shot | t (planned) | treatment |")
    a("|---|---|---|")
    for i in sorted(P.BLEND_AFTER):
        t_end = tl[i][0] + tl[i][1]
        a(f"| {i} ({P.SHOTS[i][3]}) | {t_end:.2f}s | {P.BLEND_KIND} {P.BLEND_WIDTH*1000:.0f}ms |")
    a("")
    a(f"All other cuts HARD (33-67ms). Blends {len(P.BLEND_AFTER)}/{len(P.SHOTS)-1} "
      f"= {100*len(P.BLEND_AFTER)//(len(P.SHOTS)-1)}% (profile {_br[0]}-{_br[1]}%).")
    a("")
    _bpm_band = _pf.get("bpm") or []
    _bedline = (f"bed at {P.BPM:g} BPM"
                + (f" (profile band {_bpm_band[0]}-{_bpm_band[1]})" if len(_bpm_band) == 2 else "")
                + ", first transient trimmed to t=0 (phase, not just tempo).")
    if _sfx_policy == "none":
        a(f"**Sound** — {_bedline} `edit_sfx = NONE` for this pillar: the engine lays "
          "NO transient design on any cut. All sound is diegetic or bed.")
    elif _sfx_policy == "hero_only":
        _h = (getattr(P, "SOUND", {}) or {}).get("hero_shot")
        a(f"**Sound** — {_bedline} `edit_sfx = HERO_ONLY`: ONE impact, at the hero "
          f"shot's own entry cut" + (f" (shot {_h})" if _h is not None else
          " — WARNING: SOUND['hero_shot'] is NOT SET, so engine.py:781 defaults to "
          "shot 0 and the impact lands at t=0.00s") + ". No whooshes anywhere. The bed "
          "SIDECHAIN-DUCKS under the sfx+foley key.")
    else:
        a(f"**Sound** — {_bedline} `edit_sfx = FULL`: SFX layer auto-calibrated to "
          f"bed-6dB with the bed SIDECHAIN-DUCKING under it; every whoosh LEADS its cut "
          f"by {getattr(P, 'SFX_LEAD', 0.22)*1000:.0f}ms and resolves ON it.")
    a("")
    fo = getattr(P, "FOLEY", None)
    sn = getattr(P, "SOUND", {}) or {}
    if fo:
        fg = sorted(i for i, g in fo.items() if g >= -6)
        a(f"**Diegetic** — every shot lays its OWN clip audio (generated and paid for) "
          f"on the actual timeline, plan-gained. Foreground (>=-6dB): shots {fg}. "
          f"Bed HARD-ducks during shots {sn.get('duck_shots', [])}. "
          f"Hero: {sn.get('hero', '?')}")
        a("")
    a("| t (planned) | cut entering | sound |")
    a("|---|---|---|")
    # FIX 2026-08-06: this printed "whoosh" on EVERY cut regardless of the pillar's
    # edit_sfx policy. On a hero_only plan whose whole subject is silence, the doc
    # described 20 whooshes the engine will never make. engine.py:756-806 is the
    # authority: `none` -> nothing, `hero_only` -> ONE impact at the hero entry cut
    # (IMPACT_AT is NOT consulted on that branch), `full` -> IMPACT/SUBDROP/whoosh.
    _hero_shot = (getattr(P, "SOUND", {}) or {}).get("hero_shot", 0)
    for i in range(1, len(P.SHOTS)):
        t = tl[i][0]
        if _sfx_policy == "none":
            snd = "— (edit_sfx=none)"
        elif _sfx_policy == "hero_only":
            snd = "**IMPACT (hero)**" if i == _hero_shot else "— (hero_only)"
        elif i in P.IMPACT_AT:
            snd = "IMPACT (section)"
        elif i in P.SUBDROP_AT:
            snd = "SUB-DROP (into hold)"
        else:
            snd = "whoosh"
        a(f"| {t:.2f}s | shot {i} · {P.SHOTS[i][3]} | {snd} |")
    a("")
    a("**Captions** — cards.py PNGs on desktop (drawtext fallback flagged loudly), "
      f"lower third y={P.CARD_Y}, re-timed to actual duration:")
    a("")
    a("| card | shots | planned window |")
    a("|---|---|---|")
    for t_, f_, n_, kind in P.CARDS:
        st_ = tl[f_][0]; en = tl[min(f_+n_-1, len(tl)-1)]
        a(f"| **{t_}** ({kind}) | {f_}-{f_+n_-1} | {st_:.2f}-{en[0]+en[1]:.2f}s |")
    a("")
    a(f"**Grade** — saturation {P.GRADE_SAT} ONLY (never double-grade; prompts already "
      f"carry the night look), measured toward black_point {P.TARGET_BLACK} / "
      f"saturation {P.TARGET_SAT}. Mix: engine auto-calibrates the sfx and foley layers "
      f"against the bed (sfx -> bed-6dB, foley foreground -> bed-2dB, each clamped +/-8dB), "
      f"then limiter 0.72 level=disabled -> highpass 30Hz -> limiter 0.70. "
      f"verify.py gates -9.6..-6.5 LUFS and <=-1.0 dBTP. Output written atomically.")
    a("")
    a("**Then the gates:** clipqc per clip -> engine build -> verify (15 checks, "
      "freshness FIRST — if it fails nothing else runs) -> JUDGES (kill-boring) -> Gavril.")
    a("")
    a("---")
    a("")
    a("## COST")
    a("")
    a(f"- probe first: plates + shot `{P.PROBE_FIRST}` = **{c['probe']} cr**, then LOOK")
    a(f"- remaining {c['clips']-1} clips = **{c['after_probe']} cr**")
    a(f"- **total {c['total']} cr**")
    a("")
    open(path, "w", encoding="utf-8").write("\n".join(L))
    return path


# ---------------------------------------------------------------- MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default="supra")
    ap.add_argument("--balance", type=float, default=None,
                    help="MEASURED balance. Never pass an estimate.")
    ap.add_argument("--doc", default=None)
    ap.add_argument("--json")
    args = ap.parse_args()

    name = args.plan
    for cand in (f"plans.{name}", name, f"{name}_plan"):
        try:
            P = importlib.import_module(cand); break
        except ModuleNotFoundError:
            P = None
    if P is None:
        print(f"no plan module for '{name}' (looked for plans/{name}.py)"); return 2

    # ---- FIX 2026-08-06: PREFLIGHT, before any check touches the plan ----------
    # `python3 planqc.py --plan i8` used to die with a raw traceback
    #   AttributeError: module 'plans.i8' has no attribute 'TARGET_S'
    # A gate that crashes is worse than a gate that fails: there is no verdict, no
    # doc, and the exit code is indistinguishable from an interpreter error. Worse,
    # it reports only the FIRST missing field, so fixing an old plan is one
    # traceback per field. This names every missing field at once and returns a
    # clean BLOCK. Nothing about the 31 checks changes.
    _REQ = ["PROJECT", "PILLAR", "TARGET_S", "BEAT", "BPM", "W", "H", "FPS", "MODE",
            "RES", "CLIP_S", "MAX_CROP", "SHOTS", "SOURCES", "PLATES", "BLEND_AFTER",
            "BLEND_WIDTH", "CARD_Y", "CARDS", "GRADE_SAT", "TARGET_BLACK",
            "TARGET_SAT", "IMPACT_AT", "SUBDROP_AT", "PROBE_FIRST",
            "timeline", "cost"]
    _missing = [f for f in _REQ if not hasattr(P, f)]
    if _missing:
        print("=" * 74)
        print(f"PLANQC  {getattr(P, 'PROJECT', name)}")
        print("=" * 74)
        print(f"\n  FAIL  plan structure       missing {len(_missing)} required field(s):")
        for f in _missing:
            print(f"          - {f}")
        print(f"\n{'=' * 74}")
        print(f"  BLOCK  plan is missing required fields — DO NOT GENERATE")
        print(f"{'=' * 74}\n")
        print(f"  plans/{name}.py predates the current plan format. Add the fields")
        print(f"  above (copy the shape from plans/crown.py) or retire the plan.")
        return 1

    try:
        pf = profile(P.PILLAR)
    except KeyError:
        print(f"\n  BLOCK  pillar '{P.PILLAR}' is not in assets/pillars/PILLAR-PROFILES.json")
        print(f"         planqc 26 exists to stop a plan inheriting another pillar's")
        print(f"         style silently. Declare the pillar before gating this plan.\n")
        return 1

    print("=" * 74)
    print(f"PLANQC  {P.PROJECT}")
    print("=" * 74)

    check_structure(P)
    check_profile_band(P, pf)
    check_coverage(P)
    check_source_balance(P)
    check_adjacency(P)
    check_crop(P)
    check_crop_distribution(P)
    check_repeat_framing(P)
    check_event(P)
    check_hold_placement(P)
    check_blends(P, pf)
    check_captions(P, pf)
    check_plates(P)
    check_prompts(P)
    check_defaults(P)
    check_shot_mix(P, pf)
    check_content(P)
    check_sound(P)
    check_transitions_plan(P)
    check_capacity(P)
    check_premortem(P)
    check_lessons_ack(P)
    check_linkage(P, name)
    check_linkage_carry(P)
    check_time_monotonic(P)
    check_consequence_spine(P)
    check_field_sanity(P)
    check_style_declared(P, pf)
    check_identity_coverage(P)
    check_framing_diversity(P)
    check_relationships(P)
    check_threshold_provenance(P)
    check_transition_contract(P)
    check_cost(P, args.balance)

    print()
    for cname, ok, detail, blocking in R:
        tag = "OK  " if ok else ("FAIL" if blocking else "warn")
        print(f"  {tag}  {cname:22s} {detail}")

    fails = [r for r in R if not r[1] and r[3]]
    print()
    print("=" * 74)
    if fails:
        print(f"  BLOCK  {len(fails)} failing check(s) — DO NOT GENERATE")
    else:
        print(f"  PASS   all {len(R)} checks — the plan is safe to generate")
    print("=" * 74)

    doc = args.doc or os.path.join(HERE, "projects", name, "PRODUCTION.md")
    os.makedirs(os.path.dirname(doc), exist_ok=True)
    write_doc(P, doc, name)
    print(f"\n  doc -> {doc}")

    if args.json:
        json.dump([{"check": n, "ok": o, "detail": d, "blocking": b}
                   for n, o, d, b in R], open(args.json, "w"), indent=1)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
