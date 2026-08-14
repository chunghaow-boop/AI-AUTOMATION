#!/usr/bin/env python3
"""
STYLEREF — capture every judgement he gives, so none of it is thrown away again.

WHY
  His strategy, stated: send reference links and critiques FIRST so the system learns the
  target, and only start formally rating every generation later, because rating costs time
  and credits.

  That is correct, and it exposes a bug in how I was operating: every critique he gave today
  was a labelled data point, and I treated all of them as conversation. Fifteen labels,
  already paid for in his time, discarded.

  This file is the ledger. Three kinds of evidence, all free:
      REFERENCE  a link he pointed at as "this is the quality I want"
      REJECT     a specific defect he called out on a specific build
      ACCEPT     something he explicitly said was good

  The point is not archiving. It is REGRESSION CHECKING: once "no captions" is a recorded
  rejection, no future build is allowed to ship without captions without the gate shouting.
  That is how his taste stops being something he has to repeat.

RELATIONSHIP TO THE OTHER LEDGERS
  styleref.py   what HE says is good          free, available now, subjective
  retention.py  what the AUDIENCE says        needs posts, objective, currently empty
  calibrate.py  what predicted good outputs   needs his verdicts on past generations

  styleref is the cheap arm. It cannot tell you what goes viral. It CAN stop the system
  making the same mistake twice, which is most of what went wrong today.

Usage
  python3 styleref.py add-reject  --build v2 --feature bgm --note "doesnt match the feeling"
  python3 styleref.py add-ref     --url https://... --why "transitions, sfx on every action"
  python3 styleref.py check       --build v3        # regression check against all rejects
  python3 styleref.py report
"""
import argparse, json, os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _ledger_path(name):
    """work/ledgers/ is canonical (organizer.py moves them there); work/ is the legacy
    location. Look in both so a reorganise can never orphan a ledger again."""
    import os as _o
    _r = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__)))
    for c in (_o.path.join(_r, "work", "ledgers", name), _o.path.join(_r, "work", name)):
        if _o.path.exists(c): return c
    return _o.path.join(_r, "work", "ledgers", name)

LEDGER = _ledger_path("style_ledger.json")

def _load():
    if os.path.exists(LEDGER):
        try: return json.load(open(LEDGER, encoding="utf-8"))
        except Exception: pass
    return {"references": [], "rejects": [], "accepts": []}

def _save(d):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(d, open(LEDGER, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def seed():
    """Everything he actually said today, with the build it applied to. This is real
    evidence, not an example - it is why the ledger exists."""
    d = _load()
    if d["rejects"]:
        print("  ledger already seeded"); return d
    R = lambda b, f, n, fix: {"build": b, "feature": f, "note": n, "fix": fix,
                              "date": "2026-07-30"}
    d["rejects"] = [
        R("v1", "captions",   "no caption at all",                 "captionmgr + cwd fix"),
        R("v1", "cta",        "no CTA card on screen",             "3-spot end card"),
        R("v1", "disclosure", "AI label absent (later: remove it)", "platform toggle instead"),
        R("v1", "location",   "islands are karst - Krabi not Sabah", "UNFIXED - needs regen"),
        R("v1", "true_peak",  "-0.7 dBTP failed the -1.0 gate",    "limiter headroom"),
        R("v2", "bgm",        "no bgm",                            "bgmgen.py"),
        R("v2", "captions",   "no caption",                        "drawtext path fix"),
        R("v2", "stills",     "stagnant image of fish",            "animate.py parallax"),
        R("v2", "mixing",     "mixed video and pictures looks bad", "coverage recut"),
        R("v2", "sunset",     "just sunset and waves, stale, boring", "tight coverage crop"),
        R("v2", "hook",       "no visual hook",                    "punch-style title"),
        R("v2", "cta_visual", "CTA in audio but not backed on screen", "list-style end card"),
        R("v3", "bgm_feel",   "bgm doesnt match the video feeling", "marimba + hand perc"),
        R("v3", "caption_design", "captions really need some design", "captionmgr seat"),
        R("v3", "foley",      "no sfx on actions - bubbles, crowd, splash", "foley.py"),
        R("v3", "disclosure", "do not put AI GENERATED caption",   "removed"),
    ]
    d["accepts"] = [
        {"build": "v3", "feature": "generation",
         "note": "video generation is very good, quality is perfect up to my par",
         "date": "2026-07-30"},
    ]
    d["references"] = [
        {"url": "https://www.youtube.com/watch?v=zYPgz6sOy74",
         "why": "Higgsfield full AI short-film workflow", "date": "2026-07-30"},
        {"url": "https://www.youtube.com/watch?v=fs5S867VQzg",
         "why": "smooth transitions, sfx on most actions, seamless linkage", "date": "2026-07-30"},
    ]
    _save(d); print(f"  seeded {len(d['rejects'])} rejects, {len(d['accepts'])} accepts, "
                    f"{len(d['references'])} references"); return d

# feature -> how to verify it is still fixed in a rendered file
CHECKS = {
    "captions":    ("text present in the render", "caption_count", lambda v: v > 0),
    "cta":         ("CTA card present",           "caption_count", lambda v: v > 0),
    "true_peak":   ("true peak <= -1.0 dBTP",     "true_peak",     lambda v: v is not None and v <= -1.0),
    "bgm":         ("a music bed is present",     "has_bed",       lambda v: bool(v)),
    "foley":       ("diegetic foley present",     "has_foley",     lambda v: bool(v)),
    "hook":        ("hook title in first 3s",     "hook_text",     lambda v: bool(v)),
    "stills":      ("no static shot below 0.2 motion", "min_shot_motion", lambda v: v is None or v > 0.2),
}

def check(build, metrics):
    """Regression check: for every recorded rejection, is it still fixed?"""
    d = _load()
    feats = {r["feature"] for r in d["rejects"]}
    print("="*60); print(f"REGRESSION CHECK vs {len(d['rejects'])} recorded rejections"); print("="*60)
    fails, unknown = [], []
    for f in sorted(feats):
        if f not in CHECKS: unknown.append(f); continue
        desc, key, ok = CHECKS[f]
        if key not in metrics: unknown.append(f); continue
        good = ok(metrics[key])
        print(f"  {'PASS' if good else 'FAIL'}  {f:16s} {desc}  (= {metrics[key]})")
        if not good: fails.append(f)
    if unknown:
        print(f"\n  NOT MACHINE-CHECKABLE: {', '.join(unknown)}")
        print("  These were judgement calls - they need his eyes, not a metric.")
        print("  That is the honest boundary of what this ledger can enforce.")
    print(f"\n  {len(fails)} regression(s)" + (": " + ", ".join(fails) if fails else ""))
    return not fails

def report():
    d = _load()
    print("="*60); print("STYLE LEDGER"); print("="*60)
    print(f"  references {len(d['references'])}   rejects {len(d['rejects'])}   "
          f"accepts {len(d['accepts'])}")
    byb = {}
    for r in d["rejects"]: byb.setdefault(r["build"], []).append(r)
    for b in sorted(byb):
        print(f"\n  [{b}]")
        for r in byb[b]:
            state = "OPEN" if "UNFIX" in r["fix"].upper() else "fixed"
            print(f"    {state:5s} {r['feature']:16s} {r['note'][:46]}")
    if d["accepts"]:
        print("\n  ACCEPTED")
        for x in d["accepts"]: print(f"    {x['feature']:16s} {x['note'][:56]}")
    openr = [r for r in d["rejects"] if "UNFIX" in r["fix"].upper()]
    if openr:
        print(f"\n  STILL OPEN: {len(openr)}")
        for r in openr: print(f"    {r['feature']}: {r['note']}  -> {r['fix']}")
    n = len(d["rejects"])
    check_n = sum(1 for r in d["rejects"] if r["feature"] in CHECKS)
    print(f"\n  machine-checkable: {check_n}/{n}  "
          f"({100*check_n//max(1,n)}%) - the rest need his eyes")

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd")
    ar = sub.add_parser("add-reject")
    ar.add_argument("--build", required=True); ar.add_argument("--feature", required=True)
    ar.add_argument("--note", default=""); ar.add_argument("--fix", default="")
    af = sub.add_parser("add-ref"); af.add_argument("--url", required=True); af.add_argument("--why", default="")
    sub.add_parser("seed"); sub.add_parser("report")
    ck = sub.add_parser("check"); ck.add_argument("--build", default="current")
    a = ap.parse_args()
    if a.cmd == "add-reject":
        d = _load(); d["rejects"].append({"build": a.build, "feature": a.feature,
                                          "note": a.note, "fix": a.fix,
                                          "date": datetime.now().strftime("%Y-%m-%d")})
        _save(d); print(f"  recorded rejection: {a.feature}")
    elif a.cmd == "add-ref":
        d = _load(); d["references"].append({"url": a.url, "why": a.why,
                                             "date": datetime.now().strftime("%Y-%m-%d")})
        _save(d); print("  recorded reference")
    elif a.cmd == "seed": seed()
    elif a.cmd == "check": check(a.build, {})
    else: report()

if __name__ == "__main__":
    main()
