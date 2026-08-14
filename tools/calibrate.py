#!/usr/bin/env python3
"""
CALIBRATE — turn already-paid generations into predictive power. Zero new credits.

The problem it solves: every weight in the pre-generation gates (file 26) was chosen by
REASONING, not evidence. You are using an uncalibrated scorer to decide when to spend 135
credits. This mines the ~1,500 credits of generations you have ALREADY paid for and derives
which prompt features actually predicted a good output — for YOUR model, YOUR subject, YOUR
references. Not general advice.

Inputs:
  history.json  — the show_generations dump (free, no credits)
  ratings.csv   — your verdicts: job_id,verdict  where verdict = good | mixed | bad
Output:
  per-feature lift: P(good | feature) vs base rate, with counts, plus prompt rules ranked
  by evidence. Features with too few samples are reported as INSUFFICIENT, never as a rule.

Usage:
  python3 calibrate.py history.json ratings.csv
"""
import json, sys, re, csv, math, argparse
from collections import Counter, defaultdict

FEATURES = {
 "start_image_used":      lambda p: any(m.get("role")=="image" for m in (p.get("medias") or [])),
 "multi_shot":            lambda p: bool(p.get("multi_shots")) or "shot sequence" in _t(p),
 "audio_on":              lambda p: bool(p.get("generate_audio")),
 "seamless_no_hard_cuts": lambda p: "no hard cuts" in _t(p),
 "golden_hour":           lambda p: "golden hour" in _t(p),
 "named_camera_body":     lambda p: bool(re.search(r"(sony fx|arri|red |canon|blackmagic)", _t(p))),
 "names_lens_mm":         lambda p: bool(re.search(r"\d+\s?mm", _t(p))),
 "pov":                   lambda p: "pov" in _t(p),
 "human_subject":         lambda p: any(k in _t(p) for k in ("man","woman","person","he ","she ")),
 "long_prompt_2k+":       lambda p: len(p.get("prompt","")) >= 2000,
 "short_prompt_800-":     lambda p: len(p.get("prompt","")) <= 800,
 "res_1080p":             lambda p: p.get("resolution")=="1080p",
 "mode_fast":             lambda p: p.get("mode")=="fast",
 "duration_15s":          lambda p: p.get("duration")==15,
 "duration_5s":           lambda p: p.get("duration")==5,
 "motion_in_first_shot":  lambda p: bool(re.search(r"(0-2s|0-3s)[^.]{0,80}(walk|drive|roll|run|push|pan|move|turn)", _t(p))),
 "explicit_transitions":  lambda p: any(k in _t(p) for k in ("dissolve","match-cut","match cut","whip")),
}

def _t(p): return (p.get("prompt") or "").lower()

MIN_N = 4   # below this, no rule is emitted — sample size honesty

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("history"); ap.add_argument("ratings")
    ap.add_argument("--min-n", type=int, default=MIN_N)
    a = ap.parse_args()

    hist = json.load(open(a.history))
    items = hist.get("items", hist if isinstance(hist, list) else [])
    by_id = {it.get("id"): it for it in items}

    verdicts = {}
    with open(a.ratings) as f:
        for row in csv.DictReader(f):
            v = (row.get("verdict") or "").strip().lower()
            if v in ("good","mixed","bad"):
                verdicts[row["job_id"].strip()] = v

    rated = [(by_id[j], v) for j, v in verdicts.items() if j in by_id]
    if not rated:
        print("No rated generations matched the history. Fill ratings.csv first."); return

    n = len(rated)
    good = sum(1 for _, v in rated if v == "good")
    base = good / n
    print(f"CALIBRATION SET: {n} rated generations · base rate P(good) = {base:.0%}\n")
    if n < 10:
        print(f"⚠️  SMALL SAMPLE ({n}). Treat everything below as a hypothesis to test, "
              f"not a rule. Sample size of one produces confident wrong answers.\n")

    rows = []
    for name, fn in FEATURES.items():
        withf = [(it, v) for it, v in rated if _safe(fn, it.get("params") or {})]
        without = [(it, v) for it, v in rated if not _safe(fn, it.get("params") or {})]
        if not withf: continue
        pw = sum(1 for _, v in withf if v == "good") / len(withf)
        po = (sum(1 for _, v in without if v == "good") / len(without)) if without else None
        lift = (pw - base)
        rows.append({"feature": name, "n_with": len(withf), "p_good_with": pw,
                     "p_good_without": po, "lift": lift,
                     "verdict": ("INSUFFICIENT" if len(withf) < a.min_n else
                                 "HELPS" if lift > 0.15 else
                                 "HURTS" if lift < -0.15 else "NEUTRAL")})
    rows.sort(key=lambda r: -abs(r["lift"]))

    print(f"{'feature':<24}{'n':>4}{'P(good|f)':>11}{'lift':>8}   verdict")
    print("-"*62)
    for r in rows:
        print(f"{r['feature']:<24}{r['n_with']:>4}{r['p_good_with']:>10.0%}"
              f"{r['lift']:>+8.0%}   {r['verdict']}")

    print("\nEVIDENCE-BASED PROMPT RULES (only where n >= %d):" % a.min_n)
    emitted = False
    for r in rows:
        if r["verdict"] == "HELPS":
            print(f"  ✅ DO   {r['feature']}  ({r['p_good_with']:.0%} good, n={r['n_with']})"); emitted = True
        elif r["verdict"] == "HURTS":
            print(f"  ❌ AVOID {r['feature']}  ({r['p_good_with']:.0%} good, n={r['n_with']})"); emitted = True
    if not emitted:
        print("  none yet — rate more generations, or the features genuinely don't separate.")
    print("\nNOTE: correlation on a small, non-random sample. These are priors to test with the")
    print("hook-first protocol (RUNNER 9b, ~17.5cr per probe), not laws. Log outcomes in file 09.")

def _safe(fn, p):
    try: return bool(fn(p))
    except Exception: return False

if __name__ == "__main__":
    main()
