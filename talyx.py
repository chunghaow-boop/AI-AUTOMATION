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
    return 0


VERBS = {"plan": v_plan, "board": v_board, "cost": v_cost, "ingest": v_ingest,
         "build": v_build,
         "verify": v_verify, "ls": v_ls}


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
