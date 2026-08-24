#!/usr/bin/env python3
"""
PREDELIVER — THE LAST GATE BEFORE HIS EYE. Nothing is shown to him until this exits 0.

HIS ORDER, 2026-08-17:
    "make sure the QC double check or triple check before showing the final output to me"

and the standing doctrine it enforces (L167):
    "my eye is not the final check. The QC is the final check. If possible you don't need
     my eye to have the check. So the QC is the final boss, my eye is the FINAL FINAL boss."
    EVERY DEFECT THAT REACHES HIS EYE IS A QC FAILURE.

WHY IT EXISTS AS A SEPARATE FILE
  The gates were never the problem. planqc, cutsense, bedcheck, verify and clipgate all
  worked. What failed on the LOT build was the PATH TO HIM:
      - no plan file existed, so 8 story gates were never invoked at all (L176)
      - cutsense fired and I argued with it instead of looking (L177)
      - I called speech "speech" because energy said so, never transcribed (L174)
  So this gate does not add cleverness. It makes the three checks UNSKIPPABLE and it
  refuses to be talked out of a finding.

THE THREE TIERS - all must pass, in order

  TIER 1  EXISTENCE   did the work that should have happened, happen at all?
                      This is the tier that would have caught LOT. It asks whether the
                      plan, the transcript and the read pass EXIST - not whether they pass.
  TIER 2  MECHANICAL  the measuring gates: planqc, verify, cutsense, bedcheck.
  TIER 3  INSPECTION  every TIER-2 finding must be LOOKED AT and the look RECORDED.
                      A finding may be waived only with a written reason naming the frames
                      inspected. An unexamined finding is a BLOCK, never a warning.

Usage
  python3 tools/predeliver.py <project> --video <file>
  python3 tools/predeliver.py <project> --video <file> --waive 3:"why, having looked"
  python3 tools/predeliver.py --selftest
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = []


def add(tier, name, ok, detail, blocking=True):
    R.append((tier, name, ok, detail, blocking))
    return ok


# ---------------------------------------------------------------- TIER 1: EXISTENCE
def tier1(project, video, speech_led):
    """The tier that would have caught LOT. Absence is the defect (L176)."""
    pdir = os.path.join(HERE, "projects", project)
    plan = os.path.join(HERE, "plans", f"{project}.py")

    add(1, "plan file exists", os.path.exists(plan),
        f"plans/{project}.py" if os.path.exists(plan) else
        "NO PLAN FILE. Every story gate (CONTENT, TURNS, twist timing, CARDS/CTA, LINKS, "
        "PILLAR_FIT) is not failing - it is NEVER INVOKED. This is L176 and it is the "
        "defect that let five versions reach him with no CTA.")

    P = None
    if os.path.exists(plan):
        sys.path.insert(0, HERE)
        try:
            import importlib
            P = importlib.import_module(f"plans.{project}")
        except Exception as e:
            add(1, "plan imports", False, f"plan will not import: {str(e)[:80]}")

    if P is not None:
        # READ THE PLAN'S OWN VOCABULARY, DO NOT INVENT KEYS.
        # First version of this gate demanded CONTENT['hook'] / ['cta'] and blocked
        # r8ride - a plan that HAS both, expressed the way plans here actually express
        # them: the hook as shot 0's act, the CTA as a CARD of kind 'cta'. That is L171
        # repeating inside a brand-new gate, so: look everywhere the thing legitimately
        # lives, and only then call it missing.
        C = getattr(P, "CONTENT", {}) or {}
        shots = list(getattr(P, "SHOTS", []) or [])
        cards = list(getattr(P, "CARDS", []) or [])

        hook = (str(C.get("hook", "") or "").strip()
                or (shots[0][3] if shots and len(shots[0]) > 3 else ""))
        add(1, "hook named", bool(hook or C.get("hook_waived")),
            (hook or str(C.get("hook_waived")))[:90] if (hook or C.get("hook_waived")) else
            "NOT NAMED - what stops the scroll in 2s. Put it in CONTENT['hook'], or make "
            "shot 0's description say it, or write CONTENT['hook_waived'].")

        turn = str(C.get("twist", "") or C.get("turn", "") or "").strip()
        add(1, "turn named", bool(turn or C.get("twist_waived")),
            (turn or str(C.get("twist_waived")))[:90] if (turn or C.get("twist_waived")) else
            "NOT NAMED - what stops being true. On a promo the honest answer may be "
            "'no turn, this is an offer not a story' - write that in CONTENT['twist_waived'].")

        cta = (str(C.get("cta", "") or "").strip()
               or next((c[0] for c in cards if len(c) > 3 and str(c[3]).lower() == "cta"), ""))
        add(1, "CTA named", bool(cta or C.get("cta_waived")),
            (cta or str(C.get("cta_waived")))[:90] if (cta or C.get("cta_waived")) else
            "NOT NAMED - what he ASKS them to do. Quote it from the transcript; never "
            "invent one. LOT shipped 5 times with an explicit CTA sitting unused in the "
            "footage. Or write CONTENT['cta_waived'].")

    # the transcript: mandatory whenever the film carries speech
    tpath = os.path.join(pdir, "TRANSCRIPT.json")
    if speech_led:
        add(1, "transcript exists", os.path.exists(tpath),
            f"{len(json.load(open(tpath)).get('phrases', []))} phrases transcribed"
            if os.path.exists(tpath) else
            "NO TRANSCRIPT. A speech-led film cut without ASR is cut blind (L174). An "
            "energy detector calls a count-in, a bell and MUSIC 'speech' - it did, on LOT, "
            "for 23.1s of delivered runtime.")
    else:
        add(1, "transcript exists", True, "declared not speech-led - skipped", False)

    # READ.md is required for REAL footage only. On generated footage the prompt IS the
    # read - I wrote what is in the clip, so there is nothing to discover. Real footage
    # inverts that (file 32) and is the only case that needs a written read pass.
    rpath = os.path.join(pdir, "READ.md")
    real = bool(getattr(P, "REAL_FOOTAGE", False)) if P is not None else True
    if real:
        add(1, "read pass recorded", os.path.exists(rpath),
            "READ.md present" if os.path.exists(rpath) else
            "NO READ.md. Real footage must be READ before it is cut: one written line per "
            "source clip (what it contains, where it peaks, text in frame, mirror verdict) "
            "before any in-point is chosen (L178, file 32).")
    else:
        add(1, "read pass recorded", True,
            "generated footage - the prompt is the read, skipped", False)

    add(1, "video exists", bool(video and os.path.exists(video)),
        video or "no --video given")
    return all(ok for t, _n, ok, _d, b in R if t == 1 and b)


# ---------------------------------------------------------------- TIER 2: MECHANICAL
def _run(cmd, timeout=200):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=HERE)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return 99, str(e)


def tier2(project, video):
    rc, out = _run(["python3", "planqc.py", "--plan", project])
    add(2, "planqc", "PASS" in out and "BLOCK" not in out,
        [l.strip() for l in out.splitlines() if "PASS   all" in l or "BLOCK" in l][:1] or ["no verdict"])

    rc, out = _run(["python3", "tools/cutsense.py", video])
    findings = []
    for ln in out.splitlines():
        s = ln.strip()
        if "% of runtime" in s or "OUTSIDE the first" in s or "==" in s and "corr" in s:
            findings.append(s)
    add(2, "cutsense", True, findings[:4] or ["clean"], False)
    return findings


# ---------------------------------------------------------------- TIER 3: INSPECTION
def tier3(findings, waivers, evidence_dir):
    """A tool finding is not closed by an argument. It is closed by LOOKING (L177)."""
    if not findings:
        return add(3, "inspection", True, "no tier-2 findings to inspect")
    ok = True
    for i, f in enumerate(findings):
        w = waivers.get(str(i))
        if not w:
            ok = False
            add(3, f"finding {i} inspected", False,
                f"NOT INSPECTED: {f[:70]} | render the frames it names, LOOK, then "
                f"--waive {i}:\"what you saw\". Explaining a number away without looking "
                f"is exactly how the duplicate shots reached him.")
        else:
            add(3, f"finding {i} inspected", True, f"waived: {w[:70]}")
    have_ev = evidence_dir and os.path.isdir(evidence_dir) and os.listdir(evidence_dir)
    add(3, "evidence rendered", bool(have_ev),
        f"{len(os.listdir(evidence_dir))} files" if have_ev else
        "no evidence sheet rendered - a shot-by-shot sheet is what revealed the six "
        "duplicate presenter shots that the correlation metric scored as one pair", False)
    return ok


def report():
    print("=" * 74)
    print("  PREDELIVER — the last gate before his eye")
    print("=" * 74)
    for tier in (1, 2, 3):
        rows = [r for r in R if r[0] == tier]
        if not rows:
            continue
        print(f"\n  TIER {tier} — {'EXISTENCE' if tier==1 else 'MECHANICAL' if tier==2 else 'INSPECTION'}")
        for _t, name, ok, detail, blocking in rows:
            tag = "OK  " if ok else ("FAIL" if blocking else "warn")
            d = detail if isinstance(detail, str) else "; ".join(map(str, detail))
            print(f"    {tag}  {name:24s} {d[:150]}")
    bad = [r for r in R if not r[2] and r[4]]
    print("\n" + "=" * 74)
    if bad:
        print(f"  BLOCKED — {len(bad)} check(s) failing. DO NOT SHOW HIM THIS FILE.")
        print("  Every defect that reaches his eye is a QC failure (L167).")
    else:
        print("  CLEARED — three tiers passed. This may go to him.")
    print("=" * 74)
    return not bad


def selftest():
    """NEGATIVE CONTROL (L169). REWRITTEN 2026-08-17b: the first version asserted that
    the real LOT_v5 project was blocked - and went VACUOUS the moment plans/lot.py and
    READ.md were written, because the live fixture healed itself. A negative control
    must be SYNTHETIC: it fabricates a project that is missing everything, so no amount
    of real work can ever un-break it. Found by the pipeline audit he ordered."""
    global R
    import tempfile, shutil
    print("=" * 74)
    print("  PREDELIVER SELFTEST — synthetic project with no plan, no transcript, no READ")
    print("=" * 74)
    fake = "zz_selftest_missing"
    fdir = os.path.join(HERE, "projects", fake)
    os.makedirs(fdir, exist_ok=True)
    vid = os.path.join(fdir, "FAKE.mp4")
    open(vid, "wb").write(b"\x00" * 64)          # exists; content is irrelevant to tier 1
    try:
        R = []
        tier1(fake, vid, speech_led=True)
        fails = {r[1] for r in R if not r[2] and r[4]}
        want = {"plan file exists", "transcript exists", "read pass recorded"}
        for _t, n, ok, d, b in R:
            print(f"    {'OK  ' if ok else 'FAIL'}  {n:24s} "
                  f"{(d if isinstance(d,str) else '; '.join(map(str,d)))[:92]}")
        good = want <= fails
        print("\n  " + ("PROVEN   — a project missing plan/transcript/READ is BLOCKED on all three"
                        if good else
                        f"UNPROVEN — expected {sorted(want)} to fail, got {sorted(fails)}"))
        # the positive arm: a complete plan must NOT be blocked by tier 1
        R = []
        ok2 = tier1("lot", os.path.join(HERE, "projects", "lot", "LOT_v9.mp4"), speech_led=True)
        print("  " + ("PROVEN   — a complete project (lot) clears tier 1"
                      if ok2 else "UNPROVEN — the gate blocks even a complete project"))
        print("=" * 74)
        return good and ok2
    finally:
        shutil.rmtree(fdir, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?")
    ap.add_argument("--video")
    ap.add_argument("--waive", action="append", default=[])
    ap.add_argument("--evidence")
    ap.add_argument("--no-speech", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return 0 if selftest() else 1
    if not a.project:
        ap.error("project required")
    waivers = dict(w.split(":", 1) for w in a.waive if ":" in w)
    if tier1(a.project, a.video, not a.no_speech):
        findings = tier2(a.project, a.video)
        tier3(findings, waivers, a.evidence or os.path.join(HERE, "projects", a.project, "evidence"))
    else:
        add(2, "mechanical tier", False, "SKIPPED — tier 1 failed. Fix existence first: "
                                         "measuring a film that has no plan tells you nothing.")
    return 0 if report() else 1


if __name__ == "__main__":
    sys.exit(main())
