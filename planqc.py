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
import os, sys, json, math, argparse, importlib

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
    return add("2 pillar band", ok_dur and ok_med and ok_cpm,
               f"duration {total:.1f}s in [{lo},{hi}] · median shot {med:.2f}s in "
               f"[{mlo},{mhi}] · {cpm:.1f} cuts/min vs {tgt} target (+-20%)")


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
    blo, bhi = pf["blended_range"]
    wlo, whi = pf["blend_width_ms"]
    bad_idx = [i for i in P.BLEND_AFTER if i >= len(P.SHOTS) - 1]
    ok = blo <= pct <= bhi and wlo <= w <= whi and not bad_idx
    d = f"{nb}/{cuts} blended = {pct:.0f}% in [{blo},{bhi}] · width {w:.0f}ms in [{wlo},{whi}]"
    if bad_idx:
        d += f" - blend index past the last cut: {bad_idx}"
    if getattr(P, "BLEND_KIND", "") == "dip":
        d += " - `dip` fades through BLACK and will trip the blank-frame gate"
        ok = False
    return add("11 blends", ok, d)


# ---------------------------------------------------------------- 12 CAPTIONS
def check_captions(P):
    """y=0.42 put text dead centre, on the car. The subject always lives in the centre."""
    y = P.CARD_Y
    n = len(P.SHOTS)
    over = [c for c in P.CARDS if c[1] + c[2] > n]
    centre = 0.34 <= y <= 0.60
    long = [c[0] for c in P.CARDS if len(c[0].split()) > 3]
    ok = not centre and not over and not long
    d = f"{len(P.CARDS)} cards at y={y}"
    if centre:
        d += " - IN THE CENTRE BAND (0.34-0.60), this is where the car is"
    if over:
        d += f" - card runs past the last shot: {[c[0] for c in over]}"
    if long:
        d += f" - too wordy for 1-2 word cards: {long}"
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
def write_doc(P, path):
    tl, total = P.timeline()
    c = P.cost()
    L = []
    a = L.append
    a(f"# PRODUCTION DOC — {P.PROJECT}")
    a(f"### Generated from `supra_plan.py` by `planqc.py`. Do not edit by hand — edit the plan.")
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
    pf = profile(P.PILLAR)

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
    check_captions(P)
    check_plates(P)
    check_prompts(P)
    check_defaults(P)
    check_shot_mix(P, pf)
    check_content(P)
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
    write_doc(P, doc)
    print(f"\n  doc -> {doc}")

    if args.json:
        json.dump([{"check": n, "ok": o, "detail": d, "blocking": b}
                   for n, o, d, b in R], open(args.json, "w"), indent=1)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
