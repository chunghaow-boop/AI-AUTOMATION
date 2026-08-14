#!/usr/bin/env python3
"""
MASTERMIND LOOP — the conductor. Runs the gates, routes every failure to the seat that
owns it, keeps an attempt ledger, and refuses to spin.

WHAT WAS MISSING, EXACTLY
  This repo has thirteen gates and they all work. Not one of them can say WHO FIXES IT.
  planqc exits 1. clipqc prints REJECT. verify exits 1. Every one stops dead, and a
  person reads the output, decides what broke, decides who fixes it, fixes it, and
  remembers to re-run. That person was Claude, in a chat window, and the chat is
  disposable — so the routing died every session while the measurements survived.

  Gavril, 2026-08-06: "if one fails it redirects to respect parts or seats or agent to
  refix it again and again until it passes through the master mind QC."

  This is that redirect, and only that. Read the honesty section before trusting it.

HONESTY — WHAT THIS DOES NOT DO
  IT DOES NOT FIX ANYTHING BY ITSELF, and it never will. Fixing means rewriting a
  prompt, moving a shot, choosing a bed — judgement, not mechanism. A loop that edited
  plans on its own would be a claimed capability, which is the one thing this repo
  forbids outright (plans/crown.py v2 shipped two inert flags and that lesson cost a
  whole panel round).

  What it does: RUN the gates, COLLECT every failure, ROUTE each to its owning seat with
  the concrete fix, COUNT attempts so the 5-failure rule is enforced by a machine and
  not by memory, and RE-RUN to prove the fix worked. The seat does the work. The loop
  makes sure nothing is dropped, nobody spins, and the state survives the chat.

  It also cannot judge whether anything is GOOD. Every gate it drives measures
  conformance. `ledgers/routing.json` names that in _not_routed, deliberately.

THE ONE THING IT ENFORCES THAT NOTHING ELSE DID
  --audit re-extracts every check name from planqc.py, clipqc.py and verify.py and
  compares them to the routing table. If a check is renamed and the table is not, that
  check silently loses its owner and the loop reports "no route" for something that has
  one. That is the same shape as every bug fixed on 2026-08-06, so it is checked, and
  the audit runs automatically before every dispatch.

Usage
  python3 tools/mastermind_loop.py --audit                  routing table vs source
  python3 tools/mastermind_loop.py crown --stage plan       run planqc, route failures
  python3 tools/mastermind_loop.py crown --stage clips
  python3 tools/mastermind_loop.py crown --stage verify
  python3 tools/mastermind_loop.py crown --status           the attempt ledger
  python3 tools/mastermind_loop.py crown --resolve "9 hook is an EVENT" --note "..."

Exit codes
  0  stage passed, or audit clean
  1  stage failed — a routed work order was printed
  2  could not run (bad plan, missing file)
  3  STOP — a check hit the attempt limit. Do not loop further; ask.
"""
import argparse, json, os, re, subprocess, sys
from datetime import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTING = os.path.join(HERE, "ledgers", "routing.json")
LEDGER = os.path.join(HERE, "ledgers", "attempts.json")

# His rule, from CLAUDE.md: "5 failures on one problem -> stop and ask. Never loop and
# burn credits." Enforced here by a counter instead of by whoever remembers it.
ATTEMPT_LIMIT = 5


def load_routing():
    if not os.path.exists(ROUTING):
        print(f"  no routing table at {os.path.relpath(ROUTING, HERE)}")
        return None
    return json.load(open(ROUTING, encoding="utf-8"))


def load_ledger():
    if os.path.exists(LEDGER):
        try:
            return json.load(open(LEDGER, encoding="utf-8"))
        except Exception:
            pass
    return {"_what": "Attempt counts per project per check. The 5-failure stop rule, "
                     "enforced mechanically. Written by tools/mastermind_loop.py.",
            "projects": {}}


def save_ledger(d):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(d, open(LEDGER, "w", encoding="utf-8"), indent=1)


# ---------------------------------------------------------------- AUDIT
# Extract the check names the gates ACTUALLY emit. If these drift from the routing
# table, routing silently misses. Same shape as the LC300_ and hero_shot bugs.
# NOTE: planqc emits through BOTH add() and warn(). The first version of this matched
# only add( and reported five real routes as "stale" — the audit caught its own drift
# on its first run, which is the behaviour wanted, but the extractor was the thing
# that was wrong. Both emitters are matched now.
_EMITTERS = re.compile(r'\b(?:add|warn)\("([^"]+)"')
EMIT = {
    "planqc": (os.path.join(HERE, "planqc.py"), _EMITTERS),
    "clipqc": (os.path.join(HERE, "clipqc.py"), _EMITTERS),
    "verify": (os.path.join(HERE, "verify.py"), _EMITTERS),
}


def emitted_names(gate):
    path, rx = EMIT[gate]
    if not os.path.exists(path):
        return None
    names = set()
    for ln in open(path, encoding="utf-8", errors="ignore"):
        s = ln.strip()
        if s.startswith("#"):
            continue
        for m in rx.finditer(ln):
            names.add(m.group(1))
    return names


def audit(R, quiet=False):
    """Returns (n_unrouted, n_stale). Never silently passes."""
    unrouted, stale = [], []
    for gate in ("planqc", "clipqc", "verify"):
        emitted = emitted_names(gate)
        if emitted is None:
            stale.append((gate, "SOURCE MISSING", f"{gate}.py not found — cannot audit"))
            continue
        routed = set((R.get("routes", {}).get(gate) or {}).keys())
        for nm in sorted(emitted - routed):
            unrouted.append((gate, nm))
        for nm in sorted(routed - emitted):
            stale.append((gate, nm, "routed but the gate no longer emits it"))
    if not quiet:
        print("=" * 78)
        print("ROUTING AUDIT — every check the gates emit must have an owner")
        print("=" * 78)
        for gate in ("planqc", "clipqc", "verify"):
            em = emitted_names(gate)
            rt = len((R.get("routes", {}).get(gate) or {}))
            print(f"  {gate:8s} emits {len(em) if em is not None else '?':>3} "
                  f"· routed {rt:>3}")
        if unrouted:
            print(f"\n  {len(unrouted)} check(s) WITH NO OWNER — these would fail and "
                  f"nobody would be dispatched:")
            for g, nm in unrouted:
                print(f"    {g:8s} {nm}")
        if stale:
            print(f"\n  {len(stale)} stale route(s) — table names a check the gate no "
                  f"longer emits:")
            for g, nm, why in stale:
                print(f"    {g:8s} {nm}   ({why})")
        if not unrouted and not stale:
            print("\n  clean — every emitted check has exactly one owner.")
        print()
    return len(unrouted), len(stale)


# ---------------------------------------------------------------- STAGES
def run(cmd):
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# The gates print `  OK  `/`FAIL`/`warn` then a padded name then a detail. Parse that,
# rather than re-implementing any gate's logic here — one source of truth per fact.
LINE = re.compile(r"^\s*(OK|FAIL|warn)\s{2,}(\S.*?)\s{2,}(.*)$")


def parse_gate(out):
    rows = []
    for ln in out.splitlines():
        m = LINE.match(ln.rstrip())
        if not m:
            continue
        rows.append({"status": m.group(1), "check": m.group(2).strip(),
                     "detail": m.group(3).strip()})
    return rows


STAGES = {
    "plan":   lambda name: [sys.executable, "planqc.py", "--plan", name],
    "clips":  lambda name: [sys.executable, "clipqc.py", name],
    "verify": lambda name: [sys.executable, "verify.py", "--project", name],
}


def dispatch(R, gate, rows, project, ledger):
    """Route every failing row to its seat. Returns (work_orders, stopped)."""
    table = (R.get("routes", {}).get(gate) or {})
    seats = R.get("seats", {})
    decid = R.get("_decidable_at", {})
    proj = ledger["projects"].setdefault(project, {})
    orders, stopped = [], []

    for row in rows:
        if row["status"] == "OK":
            continue
        key = row["check"]
        route = table.get(key)
        if route is None:
            # Never guess an owner. An unrouted failure is itself a finding.
            orders.append({"check": key, "status": row["status"], "seat": None,
                           "detail": row["detail"], "fix": None, "attempts": 0,
                           "unrouted": True})
            continue
        rec = proj.setdefault(key, {"attempts": 0, "history": []})
        if row["status"] == "FAIL":
            rec["attempts"] += 1
            rec["history"].append({"at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                   "gate": gate, "detail": row["detail"][:200]})
            if rec["attempts"] >= ATTEMPT_LIMIT:
                stopped.append(key)
        orders.append({"check": key, "status": row["status"],
                       "seat": route.get("seat"),
                       "seat_file": seats.get(route.get("seat"), {}).get("file", "?"),
                       "where": route.get("decidable_at"),
                       "where_note": decid.get(route.get("decidable_at"), ""),
                       "fix": route.get("fix"), "regate": route.get("regate"),
                       "detail": row["detail"], "attempts": rec["attempts"],
                       "unrouted": False})
    return orders, stopped


COST_ORDER = {"plan": 0, "cut": 1, "clip": 2, "eye": 3}


def report(orders, stopped, gate, project, stage=None):
    # `gate` is the emitter name (planqc/clipqc/verify); `stage` is the CLI flag
    # (plan/clips/verify). The first version printed the gate in the re-run hint, so
    # the copy-pasteable command was `--stage planqc`, which argparse rejects. Two
    # names for one thing is how the LC300_ and hero_shot bugs happened; keep them apart.
    stage = stage or gate
    fails = [o for o in orders if o["status"] == "FAIL"]
    warns = [o for o in orders if o["status"] == "warn"]
    print("=" * 78)
    print(f"MASTERMIND LOOP — {project} · stage {gate}")
    print("=" * 78)
    if not fails and not warns:
        print("\n  stage clean. Nothing to route.\n")
        return
    # cheapest fixes first: a plan fix is free, a clip fix is 22.5cr
    fails.sort(key=lambda o: COST_ORDER.get(o.get("where"), 9))
    if fails:
        print(f"\n  WORK ORDER — {len(fails)} blocking failure(s), cheapest fix first\n")
        for i, o in enumerate(fails, 1):
            if o["unrouted"]:
                print(f"  {i}. {o['check']}")
                print(f"     SEAT: *** NO ROUTE *** — this check has no owner in "
                      f"ledgers/routing.json.")
                print(f"     Add it, or the next failure here is dropped again.")
                print(f"     said: {o['detail'][:150]}")
                print()
                continue
            print(f"  {i}. {o['check']}   [attempt {o['attempts']}/{ATTEMPT_LIMIT}]")
            print(f"     SEAT  {o['seat']}  ->  {o['seat_file']}")
            print(f"     WHERE {o['where']} — {o['where_note']}")
            print(f"     FIX   {o['fix']}")
            print(f"     SAID  {o['detail'][:170]}")
            print(f"     THEN  re-run: python3 tools/mastermind_loop.py {project} "
                  f"--stage {stage}")
            print()
    if warns:
        print(f"  {len(warns)} warning(s), not blocking:")
        for o in warns:
            s = o["seat"] or "(no route)"
            print(f"    {o['check']:28s} -> {s}")
        print()
    if stopped:
        print("=" * 78)
        print(f"  STOP. {len(stopped)} check(s) have failed {ATTEMPT_LIMIT} times:")
        for k in stopped:
            print(f"    {k}")
        print()
        print("  His standing rule: 5 failures on one problem -> stop and ask.")
        print("  Do not attempt another fix. The problem is upstream of the check —")
        print("  usually the plan is asking for something the pillar cannot give.")
        print("=" * 78)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?")
    ap.add_argument("--stage", choices=list(STAGES))
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--resolve"); ap.add_argument("--note", default="")
    ap.add_argument("--json")
    a = ap.parse_args()

    R = load_routing()
    if R is None:
        return 2

    if a.audit:
        un, st = audit(R)
        return 1 if (un or st) else 0

    if not a.project:
        ap.print_help(); return 2
    ledger = load_ledger()

    if a.status:
        proj = ledger["projects"].get(a.project, {})
        print(f"\n  ATTEMPT LEDGER — {a.project}\n")
        if not proj:
            print("    no attempts recorded.\n"); return 0
        for k, v in sorted(proj.items(), key=lambda x: -x[1]["attempts"]):
            flag = "  <== AT LIMIT" if v["attempts"] >= ATTEMPT_LIMIT else ""
            print(f"    {v['attempts']}x  {k}{flag}")
            if v.get("resolved"):
                print(f"          RESOLVED {v['resolved']['at']}: "
                      f"{v['resolved']['note']}")
        print()
        return 0

    if a.resolve:
        proj = ledger["projects"].setdefault(a.project, {})
        rec = proj.setdefault(a.resolve, {"attempts": 0, "history": []})
        rec["resolved"] = {"at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                           "note": a.note or "(no note)"}
        rec["attempts"] = 0
        save_ledger(ledger)
        print(f"  resolved and attempt count reset: {a.resolve}")
        return 0

    if not a.stage:
        ap.print_help(); return 2

    # The audit runs before EVERY dispatch, not just on demand. A routing table that
    # has drifted would send this whole run to the wrong seats, silently.
    un, st = audit(R, quiet=True)
    if un:
        print(f"\n  ROUTING DRIFT — {un} check(s) have no owner. Run --audit.")
        print("  Dispatching anyway; unrouted failures will be flagged individually.\n")

    rc, out = run(STAGES[a.stage](a.project))
    rows = parse_gate(out)
    if not rows:
        print(f"\n  the {a.stage} gate produced no parseable check lines. Raw output:\n")
        print("\n".join("    " + l for l in out.splitlines()[-25:]))
        print("\n  NOT MEASURED — routing cannot run on this. Fix the gate first.\n")
        return 2

    gate = {"plan": "planqc", "clips": "clipqc", "verify": "verify"}[a.stage]
    orders, stopped = dispatch(R, gate, rows, a.project, ledger)
    save_ledger(ledger)
    report(orders, stopped, gate, a.project, a.stage)

    if a.json:
        json.dump({"project": a.project, "stage": a.stage, "orders": orders,
                   "stopped": stopped}, open(a.json, "w"), indent=1)
        print(f"  wrote {a.json}\n")

    if stopped:
        return 3
    return 1 if any(o["status"] == "FAIL" for o in orders) else 0


if __name__ == "__main__":
    sys.exit(main())
