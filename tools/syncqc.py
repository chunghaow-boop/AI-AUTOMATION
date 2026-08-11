#!/usr/bin/env python3
"""SYNCQC — does the CUT do what the PLAN said it would?

HIS DIAGNOSIS, 2026-08-07, after watching the hook open on an empty pool:

    "the video editor must also sync with the mastermind planner, the edits and cuts
     must follow together, if not it will be like this messy, mastermind planned
     something but other agents / roles didnt follow"

He is describing a gap that is real and, until now, unowned. Every existing gate checks
ONE side:

    planqc   is the plan coherent?          (never sees a frame)
    clipqc   is this CLIP acceptable?       (never sees the plan's intent for it)
    verify   is the CUT technically sound?  (check 12 tallies shot count, window
             overlap and sources used - it never asks whether shot 0's delivered
             window contains the EVENT the plan promised)

Nothing checks the JOIN. So mahua's plan said "THE DROP IS ALREADY HAPPENING AT FRAME
ZERO", the generator delivered a 0.55s airborne run-up, the editor took the clip head,
and every gate stayed green. Three green gates, one broken hook.

    python tools/syncqc.py mahua

READS ONLY. It never edits a plan and never re-renders. It reports where the plan and
the cut disagree, and it is deliberately additive: `verify.py` is a pipeline file and
folding these in as a real check is HIS call.

INPUTS (each one degrades to a clear SKIP if absent):
    plans/<name>.py                         the intent
    projects/<name>/clips/manifest.json     ingest: action peaks, audio, duration
    projects/<name>/tmp/manifest_peaks.json engine: the tin it actually allocated
"""
import argparse
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

OK, BAD, SKIP = [], [], []


def ok(label, detail=""):
    OK.append((label, detail))


def bad(label, detail):
    BAD.append((label, detail))


def skip(label, why):
    SKIP.append((label, why))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    P = importlib.import_module(f"plans.{a.plan}")
    pdir = os.path.join(HERE, "projects", a.plan)
    tl, total = P.timeline()

    man_p = os.path.join(pdir, "clips", "manifest.json")
    peaks_p = os.path.join(pdir, "tmp", "manifest_peaks.json")
    man = json.load(open(man_p)) if os.path.exists(man_p) else None
    alloc = None
    if os.path.exists(peaks_p):
        alloc = {e["shot"]: e for e in json.load(open(peaks_p))}

    print("=" * 78)
    print(f"SYNCQC  {P.PROJECT}")
    print("  does the CUT do what the PLAN said it would?")
    print("=" * 78)

    if man is None:
        skip("ingest manifest", f"no {os.path.relpath(man_p, HERE)} — run tools/ingest.py first")
    if alloc is None:
        skip("engine allocation", f"no {os.path.relpath(peaks_p, HERE)} — run talyx.py build first")

    style = {}
    try:
        from planqc import profile
        style = (profile(P.PILLAR) or {}).get("style") or {}
    except Exception:
        pass
    ev_floor = float(style.get("event_motion_floor", 2.5))

    # ---------------------------------------------------------------- 1 THE HOOK
    s0, _c0, _k0, note0 = P.SHOTS[0]
    act0 = P.SOURCES[s0][2].upper()
    d0 = tl[0][1]
    if alloc and man and s0 in man:
        tin = alloc.get(0, {}).get("tin")
        pks = man[s0].get("action_peaks_s") or []
        inside = [p for p in pks if tin is not None and tin <= p <= tin + d0]
        if tin is None:
            bad("1 THE HOOK LANDS", "shot 0 got no allocated window at all")
        elif not inside:
            bad("1 THE HOOK LANDS",
                f"shot 0 is act={act0} and its delivered window {tin:.2f}-{tin+d0:.2f}s "
                f"contains NO action peak (clip peaks at {[round(p,2) for p in pks]}). "
                f"THE HOOK IS A RUN-UP. Ban the head in BAN_SPANS and re-cut — free.")
        else:
            first = min(inside) - tin
            frac = first / d0
            if frac > 0.40:
                bad("1 THE HOOK LANDS",
                    f"the event lands {first:.2f}s into a {d0:.2f}s hook ({frac*100:.0f}% "
                    f"through). Everything before it is a run-up over an empty frame — "
                    f"mahua opened on 0.55s of airborne and every gate stayed green. "
                    f"Ban {tin:.2f}-{min(inside)-0.05:.2f}s on source {s0}.")
            else:
                ok("1 THE HOOK LANDS",
                   f"event at {first:.2f}s = {frac*100:.0f}% into the hook (needs <=40%)")
    else:
        skip("1 THE HOOK LANDS", "needs the ingest manifest AND the engine allocation")

    # ---------------------------------------------- 2 EVENT / PAYOFF SHOTS CARRY EVENTS
    if alloc and man:
        weak = []
        for i, (src, _c, kind, _n) in enumerate(P.SHOTS):
            act = P.SOURCES[src][2].upper()
            if act not in ("EVENT", "PAYOFF"):
                continue
            e = alloc.get(i) or {}
            if not e.get("has_peak"):
                weak.append(f"shot {i} ({src}, {act}) window carries no action peak")
        if weak:
            bad("2 EVENT SHOTS CARRY EVENTS", " · ".join(weak) +
                f"  [event_motion_floor for this pillar is {ev_floor}]")
        else:
            ok("2 EVENT SHOTS CARRY EVENTS", "every EVENT/PAYOFF window contains a peak")
    else:
        skip("2 EVENT SHOTS CARRY EVENTS", "needs the engine allocation")

    # ------------------------------------------- 3 FOREGROUND SOUND HAS SOMETHING IN IT
    fg = sorted(i for i, g in (getattr(P, "FOLEY", {}) or {}).items() if g >= -6.0)
    if man:
        silent = []
        for i in fg:
            src = P.SHOTS[i][0]
            au = (man.get(src) or {}).get("audio") or {}
            if not au.get("present"):
                silent.append(f"shot {i} ({src})")
        if silent:
            bad("3 FOREGROUND SOUND EXISTS",
                f"mixed to the FRONT but the clip has no audio: {', '.join(silent)}. "
                f"engine lays each shot's OWN clip audio — a foreground gain on silence "
                f"is silence, louder.")
        else:
            ok("3 FOREGROUND SOUND EXISTS",
               f"{len(fg)} foreground shots ({fg}), all carry clip audio")
    else:
        skip("3 FOREGROUND SOUND EXISTS", "needs the ingest manifest")

    # ------------------------------------------------ 4 REPEATED SOURCES SIT FAR APART
    if alloc:
        bysrc = {}
        for i, (src, _c, _k, _n) in enumerate(P.SHOTS):
            t = (alloc.get(i) or {}).get("tin")
            if t is not None:
                bysrc.setdefault(src, []).append((i, t))
        tight = []
        for src, uses in bysrc.items():
            uses.sort(key=lambda x: x[1])
            for (ia, ta), (ib, tb) in zip(uses, uses[1:]):
                if tb - ta < 1.0:
                    tight.append(f"{src} shots {ia}/{ib} start {tb-ta:.2f}s apart in-clip")
        if tight:
            bad("4 REPEATS SIT FAR APART", " · ".join(tight) +
                "  — MEASURED on mahua: two windows of one static clip hit 0.975 "
                "histogram correlation. A different crop is not a different picture.")
        else:
            ok("4 REPEATS SIT FAR APART", "every repeated source's windows are >=1.0s apart")
    else:
        skip("4 REPEATS SIT FAR APART", "needs the engine allocation")

    # ------------------------------------------------------- 5 THE PLAN'S OWN ARC ORDER
    # A source whose prompt performs an ARC must have its windows delivered IN ORDER.
    arcs = [k for k, v in P.SOURCES.items()
            if any(w in str(v[4]).upper() for w in ("CHANGE OF STATE", "MONOTONIC", "ARC"))]
    if alloc and arcs:
        wrong = []
        for src in arcs:
            uses = sorted(((i, (alloc.get(i) or {}).get("tin"))
                           for i, s in enumerate(P.SHOTS) if s[0] == src
                           and (alloc.get(i) or {}).get("tin") is not None),
                          key=lambda x: x[0])
            if [u[1] for u in uses] != sorted(u[1] for u in uses):
                wrong.append(f"source {src}: shots {[u[0] for u in uses]} take in-clip "
                             f"windows {[round(u[1],2) for u in uses]} — OUT OF ORDER")
        if wrong:
            bad("5 ARC RUNS FORWARD", " · ".join(wrong) +
                "  — the clip performs a one-way change and the cut plays it backwards. "
                "There is no per-shot window field; swap which shot is the burst, or ask "
                "for SHOT_WINDOW in the engine.")
        else:
            ok("5 ARC RUNS FORWARD", f"arc sources {arcs} delivered in order")
    elif arcs:
        skip("5 ARC RUNS FORWARD", "needs the engine allocation")

    print()
    for label, detail in OK:
        print(f"  OK    {label:32s} {detail}")
    for label, why in SKIP:
        print(f"  skip  {label:32s} {why}")
    for label, detail in BAD:
        print(f"  FAIL  {label:32s} {detail}")
    print()
    print("=" * 78)
    if BAD:
        print(f"  {len(BAD)} DISAGREEMENT(S) BETWEEN THE PLAN AND THE CUT")
        print("  The plan is not wrong and the clips are not wrong — they were never")
        print("  checked against each other. Fix at plan level (BAN_SPANS, shot order)")
        print("  and re-cut: no credits move.")
    elif OK:
        print("  THE CUT DOES WHAT THE PLAN SAID IT WOULD.")
    else:
        print("  NOTHING COULD BE CHECKED — run ingest and build first.")
    print("=" * 78)
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
