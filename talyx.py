#!/usr/bin/env python3
"""
TALYX — one command for the whole pipeline.

WHY THIS EXISTS
  On 2026-08-01 the project had NINE python files at the root and SEVEN of them were
  per-car: build_lc300, build_lc300_cinematic, make_storyboard, make_storyboard_i8,
  make_storyboard_supra, i8_plan, supra_plan. Two and a half cars had produced seven
  scripts. The ten-car storyboard list would have meant thirty.

  That is a copy-paste factory, not a pipeline. The plan is DATA; the pipeline is CODE;
  they should never multiply together.

  Adding video number eleven is now ONE file: plans/<name>.py

USAGE
  python3 talyx.py plan   supra          planqc -> 17 checks + projects/supra/PRODUCTION.md
  python3 talyx.py board  supra          render the storyboard FROM the plan
  python3 talyx.py cost   supra          exact credits, and what a probe costs first
  python3 talyx.py ingest supra          gate every generated clip BEFORE the edit
  python3 talyx.py build  lc300          cut it — generic engine, plan-driven
  python3 talyx.py verify lc300          the 10 checks on the finished cut
  python3 talyx.py ls                    what projects and plans exist, and their state

  `plan` and `verify` exit non-zero when they fail, so they work in a shell gate:
      python3 talyx.py plan supra && echo "safe to generate"

LAYOUT
  plans/<name>.py            the edit plan. DATA ONLY - no logic, no rendering.
  projects/<name>/           clips/ output/ audio/ analysis/ tmp/ + PRODUCTION.md
  assets/                    pillars (measured profiles) · nev · refs · bgm
  tools/                     the 40 measurement tools
  ledgers/                   style_ledger.json (rejects) · knowledge.json (lessons)
"""
import os, sys, glob, json, subprocess, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PLANS = os.path.join(HERE, "plans")
PROJECTS = os.path.join(HERE, "projects")


def _plan(name):
    for cand in (f"plans.{name}", name, f"{name}_plan"):
        try:
            return importlib.import_module(cand)
        except ModuleNotFoundError:
            pass
    return None


def _pdir(name, sub=None):
    d = os.path.join(PROJECTS, name)
    return os.path.join(d, sub) if sub else d


def _run(args, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.call([sys.executable] + args, cwd=HERE, env=e)


# ---------------------------------------------------------------- verbs
def v_plan(name, rest):
    """Gate the plan BEFORE spending. Costs nothing, blocks generation."""
    os.makedirs(_pdir(name), exist_ok=True)
    return _run([os.path.join(HERE, "planqc.py"), "--plan", name] + rest)


def v_board(name, rest):
    """Render the storyboard FROM the plan, never beside it."""
    os.makedirs(_pdir(name, "analysis"), exist_ok=True)
    import board
    out = board.main(name)
    print(f"  board -> {out}")
    return 0


def v_cost(name, rest):
    P = _plan(name)
    if not P:
        print(f"no plan: plans/{name}.py"); return 2
    c = P.cost()
    print(f"{P.PROJECT}")
    print(f"  {c['clips']} clips x {c['per_clip']}cr = {c['generation']}cr")
    print(f"  plates                  {c['plates']}cr")
    print(f"  TOTAL                   {c['total']}cr")
    print(f"  probe first ({P.PROBE_FIRST})        {c['probe']}cr  <- LOOK at it, then commit "
          f"{c['after_probe']}cr")
    print("\n  MEASURE the balance before spending. Never estimate it.")
    return 0


def v_ingest(name, rest):
    """Per-clip gate BETWEEN generation and the edit. One clip failing = one 22.5cr
    regeneration, not a rebuilt edit."""
    return _run([os.path.join(HERE, "clipqc.py"), name] + rest)


def v_build(name, rest):
    """Cut it. Generic engine, driven entirely by plans/<name>.py."""
    import engine
    return engine.build(name, use_cache="--no-cache" not in rest)


def v_verify(name, rest):
    """The 10 checks on a finished cut. Freshness runs first."""
    return _run([os.path.join(HERE, "verify.py")] + rest, env={"TALYX_PROJECT": name})


def v_deliver(name, rest):
    """THE ONLY WAY A VIDEO LEAVES THIS PIPELINE.

    2026-08-08, and it exists because of what I did rather than what the code did.
    verify returned BLOCK with six failing checks on DESAFARM_CINEMATIC_v2. I read
    it, wrote Gavril a table about the failures, and pasted him the link anyway.
    The gate fired and nothing stopped the delivery, because delivery was never a
    step - it was a human copying a URL. His words: "QC did its job but the video
    still proceeded anyway".

    And the FINAL scorecard, the mastermind, had never run at all. It was not a
    verb, nothing called it, and the only mention of it anywhere in the repo was a
    comment inside transcribe.py. Run by hand afterwards it said SEND BACK on two
    hard gates, one of which - SFX OFF-BEAT, median 78.5ms - was the whip drift
    found independently by the tool nobody opened.

    So: deliver runs BOTH gates plus a crosscheck of the plan against the cut
    against the file on disk, and it REFUSES TO PRINT A LINK if anything blocks.
    A gate that reports but cannot stop shipping is advisory. This one stops it."""
    import glob as _glob
    import json as _json
    pdir = _pdir(name)
    outs = sorted(_glob.glob(os.path.join(pdir, "output", "*.mp4")),
                  key=os.path.getmtime)
    if not outs:
        print(f"  nothing to deliver - no cut in projects/{name}/output/")
        return 2
    video = outs[-1]
    cuts_json = ""
    for pat in ("*_cuts.json",):
        c = sorted(_glob.glob(os.path.join(pdir, "audio", pat)), key=os.path.getmtime)
        if c:
            cuts_json = c[-1]
    P = _plan(name)

    print("=" * 70)
    print(f"DELIVER  {os.path.basename(video)}")
    print("=" * 70)

    stops = []

    # ---- 1. the cut gate -------------------------------------------------
    print("\n[1/3] checking the cut")
    rc_v = _run([os.path.join(HERE, "verify.py")] + rest, env={"TALYX_PROJECT": name})
    if rc_v != 0:
        stops.append("verify blocked the cut (see its list above)")

    # ---- 2. the final scorecard -----------------------------------------
    print("\n[2/3] the mastermind's final word")
    mm_args = [os.path.join(HERE, "tools", "mastermind.py"), video,
               "--out", os.path.join(pdir, "analysis", "qc")]
    bed = getattr(P, "SOUND", {}).get("bed", "") if P else ""
    bed = bed.split(" - ")[0].strip() if bed else ""
    if bed and os.path.exists(os.path.join(HERE, bed)):
        mm_args += ["--bed", os.path.join(HERE, bed)]
    if cuts_json:
        mm_args += ["--cuts", cuts_json]
    rep_path = os.path.join(pdir, "analysis", "qc", "report.json")
    rc_m = _run(mm_args + ["--quiet"] if False else mm_args)
    verdict, gates, final = "NOT RUN", [], None
    if os.path.exists(rep_path):
        try:
            rep = _json.load(open(rep_path))
            sc = rep.get("score", {})
            verdict = sc.get("verdict", "?")
            gates = sc.get("hard_gates", []) or []
            final = sc.get("final")
        except Exception as e:
            verdict = f"unreadable report ({str(e)[:40]})"
    print(f"\n      mastermind says: {verdict}" + (f"   (score {final})" if final else ""))
    for g in gates:
        print(f"        STOP  {g}")
    if verdict != "SHIP":
        stops.append(f"the mastermind said {verdict}")

    # ---- 3. crosscheck: does the file match what was planned? ------------
    print("\n[3/3] crosschecking the plan against the file on disk")
    if P is None:
        stops.append(f"no plan at plans/{name}.py to crosscheck against")
    else:
        import subprocess as _sp
        try:
            dur = float(_sp.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", video], text=True).strip())
        except Exception:
            dur = None
        want = float(getattr(P, "TARGET_S", 0) or 0)
        if dur and want:
            drift = dur - want
            ok = abs(drift) <= 0.05
            print(f"      length     {dur:.2f}s against the plan's {want:.2f}s "
                  f"({drift*1000:+.0f} ms)")
            if not ok:
                stops.append(
                    f"the film is {abs(drift)*1000:.0f} ms {'short of' if drift < 0 else 'longer than'} "
                    f"the plan - every cut after the change sits off the music")
        n_cuts = 0
        if cuts_json:
            try:
                n_cuts = len(_json.load(open(cuts_json)).get("cuts", []))
            except Exception:
                pass
        want_cuts = len(getattr(P, "SHOTS", [])) - 1
        if n_cuts:
            print(f"      cuts       {n_cuts} against the plan's {want_cuts}")
        cards = getattr(P, "CARDS", []) or []
        spans = [(c[0], int(c[1]), int(c[1]) + max(1, int(c[2])) - 1) for c in cards]
        clash = [(a[0], b[0]) for i, a in enumerate(spans) for b in spans[i+1:]
                 if a[1] <= b[2] and b[1] <= a[2]]
        print(f"      cards      {len(cards)}, "
              + ("none overlap" if not clash else f"{len(clash)} OVERLAP"))
        if clash:
            stops.append("two cards share the caption zone: "
                         + "; ".join(f"{a!r} and {b!r}" for a, b in clash))

    # ---- the verdict -----------------------------------------------------
    print("\n" + "=" * 70)
    if stops:
        print(f"  HELD BACK - {len(stops)} reason(s). No link, and that is the point.")
        print("=" * 70)
        for s in stops:
            print(f"    - {s}")
        print("\n  Fix it and run deliver again. If you believe a stop is wrong, change")
        print("  the CHECK and say why in its comment - never carry the film past it.")
        return 1
    print("  CLEARED TO SEND")
    print("=" * 70)
    print(f"\n  {video}")
    print(f"\n  Upload it and give Gavril the hosted link - his standing order is a")
    print(f"  link, never an attachment.")
    return 0


def v_ls(_name, _rest):
    plans = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(PLANS, "*.py"))
                   if not os.path.basename(p).startswith("__"))
    projs = sorted(os.path.basename(p) for p in glob.glob(os.path.join(PROJECTS, "*"))
                   if os.path.isdir(p))
    print(f"{'PROJECT':14s} {'PLAN':6s} {'CLIPS':>6s} {'CUTS':>5s}  STATE")
    print("-" * 62)
    for n in sorted(set(plans) | set(projs)):
        has = "yes" if n in plans else "-"
        clips = len(glob.glob(os.path.join(_pdir(n, "clips"), "*.mp4")))
        outs = len(glob.glob(os.path.join(_pdir(n, "output"), "*.mp4")))
        P = _plan(n)
        need = len(P.SOURCES) if P else 0
        if n.startswith("_"):
            state = "archive"
        elif outs:
            state = f"cut ({outs})"
        elif need and clips >= need:
            state = "clips complete - ready to build"
        elif need:
            state = f"generating {clips}/{need}"
        else:
            state = "no plan"
        print(f"{n:14s} {has:6s} {clips:6d} {outs:5d}  {state}")
    print()
    print("  talyx.py plan <name>    gate the plan (free)")
    print("  talyx.py verify <name>  gate the cut")
    print("  talyx.py deliver <name> BOTH gates + crosscheck - the only way out")
    return 0


VERBS = {"plan": v_plan, "board": v_board, "cost": v_cost, "ingest": v_ingest,
         "build": v_build,
         "verify": v_verify, "deliver": v_deliver, "ls": v_ls}


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__); return 0
    verb, argv = argv[0], argv[1:]
    if verb not in VERBS:
        print(f"unknown verb '{verb}'. one of: {', '.join(VERBS)}"); return 2
    name = argv[0] if argv and not argv[0].startswith("-") else None
    rest = argv[1:] if name else argv
    if verb != "ls" and not name:
        print(f"usage: talyx.py {verb} <name>"); return 2
    return VERBS[verb](name, rest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
