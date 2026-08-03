#!/usr/bin/env python3
"""
RETENTION — the missing arm of the loop. Predict before posting, resolve after, attribute.

WHY THIS IS THE MOST IMPORTANT FILE IN THE REPO RIGHT NOW
  His framing: editing sense tracks virality, virality drifts, so the system must keep
  updating against a retention target of 30-50%.

  That is a closed feedback loop:
      current meta -> edit choices -> POST -> retention curve -> attribute -> update weights

  Audit of the arms, 2026-07-30:
      edit arm          strong   (clipsense + editsense + build_kk)
      trend arm         partial  (intel.py is a ledger; it must be fed)
      MEASUREMENT ARM   ABSENT   zero measured curves exist anywhere in this repo
      attribution arm   absent   (needs N posts before signal beats noise)

  Every retention number this system has ever produced is a structural heuristic. pacing.py
  says so itself: "NOT a measurement and NOT a promise". So the editing rules built today -
  J/L cuts, beat snapping, foley density - are HYPOTHESES. Plausible, evidence-informed,
  entirely unvalidated on this audience.

  This file makes them falsifiable.

HOW IT WORKS
  1. log_build()   at render time: capture every edit feature + the predicted retention
  2. resolve()     at +24h: paste the real numbers from TikTok/Meta analytics
  3. attribute()   once N is enough: which features actually moved retention, with honest
                   confidence. Under-powered features are reported as INSUFFICIENT, never
                   as a rule. That is the same discipline calibrate.py uses.

WHAT IT WILL NOT DO
  Claim a feature works from one post. With N<8 nothing is reported as causal.

Usage
  python3 retention.py log      --video output/KK_3SPOTS_v3.mp4 --predict 44
  python3 retention.py resolve  --id kk_v3 --views 12000 --avg-pct 38 --3s-pct 62 --full-pct 21
  python3 retention.py report
"""
import argparse, json, os, sys, csv, math
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

LEDGER = _ledger_path("retention_ledger.json")
sys.path.insert(0, os.path.join(ROOT, "tools"))

MIN_N = 8          # below this, no attribution is reported. Ever.

def _load():
    if os.path.exists(LEDGER):
        try: return json.load(open(LEDGER))
        except Exception: pass
    return {"entries": []}

def _save(d):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(d, open(LEDGER, "w"), indent=2)

def extract_features(video):
    """Every edit feature the system can already measure. These are the candidate causes;
    the retention curve is the effect. Anything not measurable here cannot be attributed."""
    f = {"file": os.path.basename(video)}
    try:
        import pacing
        p = pacing.analyse(video, "vlog")
        f.update({"duration": p["duration"], "cuts": p["cuts"],
                  "cuts_per_min": p["cuts_per_min"],
                  "hook_motion": p["hook"]["motion"],
                  "shot_len_median": p["shot_len_median"],
                  "shot_len_max": p["shot_len_max"],
                  "cut_rate_variation": p["cut_rate_variation"],
                  "dead_zones": len(p["dead_zones"]),
                  "heuristic_estimate": p["retention_estimate_pct"]})
    except Exception as e:
        f["pacing_error"] = str(e)[:60]
    try:
        import mastermind
        a = mastermind.audio_metrics(video)
        f.update({"lufs": a.get("lufs"), "true_peak": a.get("peak")})
    except Exception:
        pass
    return f

def log_build(video, predict=None, ident=None, notes="", extra=None, shots=None):
    d = _load()
    ident = ident or os.path.splitext(os.path.basename(video))[0]
    e = {"id": ident,
         "logged": datetime.now().isoformat(timespec="seconds"),
         "features": extract_features(video),
         "predicted_avg_pct": predict,
         "notes": notes,
         "shots": shots or {},
         "actual": None}
    if extra: e["features"].update(extra)
    d["entries"] = [x for x in d["entries"] if x["id"] != ident] + [e]
    _save(d)
    print(f"logged '{ident}'  predicted avg-viewed {predict}%")
    for k, v in e["features"].items(): print(f"    {k:22s} {v}")
    print(f"\n  -> POST IT, then at +24h run:\n     python3 retention.py resolve --id {ident} "
          f"--views N --avg-pct N --3s-pct N --full-pct N")
    return e

def resolve(ident, **actual):
    d = _load()
    for e in d["entries"]:
        if e["id"] == ident:
            e["actual"] = {k: v for k, v in actual.items() if v is not None}
            e["resolved"] = datetime.now().isoformat(timespec="seconds")
            _save(d)
            pred = e.get("predicted_avg_pct")
            act = e["actual"].get("avg_pct")
            print(f"resolved '{ident}'")
            if pred is not None and act is not None:
                err = act - pred
                print(f"  predicted {pred}%  actual {act}%   error {err:+.1f} pts")
                print(f"  -> the heuristic was {'OPTIMISTIC' if err < 0 else 'PESSIMISTIC'} "
                      f"by {abs(err):.1f} points on this one")
            n = sum(1 for x in d["entries"] if x.get("actual"))
            print(f"  resolved posts: {n}/{MIN_N} needed before attribution means anything")
            return e
    print(f"no entry '{ident}'")

def curve_attribution(ident=None, curve=None, shots=None):
    """Map a retention CURVE onto the shot list, so a single post is already informative.

    This is the answer to the attribution problem in his thesis. He is right that retention
    is the aggregate quality signal - flow, hooks, transitions, editing, foley, all of it.
    But the AGGREGATE cannot tell you which lever moved: one scalar over fifteen variables.

    The CURVE can. Retention is monotonic, so the steepest drops are where viewers left, and
    the build knows which shot occupies every second. That turns "38%" into "you lost 22% of
    viewers during shot 06" - actionable from post number one, no statistics required.

    curve: list of (second, pct_still_watching) straight off TikTok/Meta analytics
    shots: {tag: start_seconds} from the build
    """
    d = _load()
    if ident and not curve:
        e = next((x for x in d["entries"] if x["id"] == ident), None)
        curve = (e or {}).get("actual", {}).get("curve")
        shots = shots or (e or {}).get("shots")
    if not curve:
        print("  no curve on file. Paste one from analytics:")
        print("    python3 retention.py curve --id kk_v3 --points 0:100,1:94,2:88,3:71,...")
        return
    curve = sorted(curve)
    drops = []
    for i in range(1, len(curve)):
        (t0, p0), (t1, p1) = curve[i-1], curve[i]
        span = max(1e-6, t1-t0)
        drops.append((round((p0-p1)/span, 2), t0, t1, p0-p1))
    drops.sort(reverse=True)
    order = sorted((shots or {}).items(), key=lambda kv: kv[1])
    def shot_at(t):
        cur = None
        for tag, st in order:
            if st <= t: cur = tag
            else: break
        return cur or "?"
    print("")
    print("  WHERE VIEWERS LEFT  (steepest first)")
    for rate, t0, t1, lost in drops[:6]:
        tag = shot_at(t0)
        print(f"    {t0:5.1f}-{t1:4.1f}s  -{lost:5.1f} pts  ({rate:5.2f}/s)  shot {tag}")
    hook = next((p for t, p in curve if t >= 3), None)
    if hook is not None:
        print("")
        print(f"  3-second hold: {hook:.0f}%")
        if hook < 70:
            print("    -> BELOW 70%. Fix the opening before anything else; nothing")
            print("       downstream matters if most viewers never reach it.")
        else:
            print("    -> healthy. The losses below are body/payoff problems, not hook problems.")
    return drops

def attribute():
    """Correlate each edit feature with measured retention. Honest about power."""
    d = _load()
    done = [e for e in d["entries"] if e.get("actual", {}).get("avg_pct") is not None]
    n = len(done)
    print("="*62); print(f"ATTRIBUTION   resolved posts: {n}"); print("="*62)
    if n == 0:
        print("\n  NOTHING TO ATTRIBUTE. Zero posts have a measured curve.")
        print("  Every editing rule in this repo is currently an untested hypothesis:")
        print("    - J/L cuts improve retention          UNTESTED")
        print("    - cuts on the beat improve retention  UNTESTED")
        print("    - diegetic foley improves retention   UNTESTED")
        print("    - 25 cuts/min beats 10 cuts/min       UNTESTED")
        print("    - the heuristic's own 44% estimate    UNVALIDATED")
        print("\n  The loop cannot close without the first data point.")
        return
    if n < MIN_N:
        print(f"\n  UNDER-POWERED. {n} post(s); {MIN_N} needed before a correlation is")
        print("  distinguishable from noise. Showing raw rows only - no rules inferred.\n")
        for e in done:
            print(f"   {e['id']:22s} pred {e.get('predicted_avg_pct')}%  "
                  f"actual {e['actual']['avg_pct']}%")
        return
    keys = [k for k in done[0]["features"]
            if isinstance(done[0]["features"].get(k), (int, float))]
    ys = [e["actual"]["avg_pct"] for e in done]
    my = sum(ys)/len(ys)
    rows = []
    for k in keys:
        xs = [e["features"].get(k) for e in done]
        if any(v is None for v in xs): continue
        mx = sum(xs)/len(xs)
        sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
        sxx = math.sqrt(sum((x-mx)**2 for x in xs)); syy = math.sqrt(sum((y-my)**2 for y in ys))
        if sxx*syy == 0: continue
        rows.append((sxy/(sxx*syy), k))
    rows.sort(key=lambda r: -abs(r[0]))
    print(f"\n  feature correlation with average-viewed %  (n={n})\n")
    for r, k in rows:
        strength = "strong" if abs(r) > 0.6 else ("moderate" if abs(r) > 0.35 else "weak")
        print(f"    {k:24s} r={r:+.2f}  {strength}")
    print("\n  NOTE correlation on a small n is not causation. Treat the top rows as the next")
    print("  thing to A/B deliberately, not as settled rules.")

def report():
    d = _load(); es = d["entries"]
    done = [e for e in es if e.get("actual")]
    print("="*62); print("RETENTION LEDGER"); print("="*62)
    print(f"  builds logged : {len(es)}")
    print(f"  posts resolved: {len(done)}")
    print(f"  target band   : 30-50% average-viewed")
    if not es:
        print("\n  Ledger empty. Log a build:")
        print("    python3 retention.py log --video output/KK_3SPOTS_v3.mp4 --predict 44")
        return
    for e in es:
        a = e.get("actual")
        state = f"actual {a['avg_pct']}%" if a and a.get("avg_pct") is not None else "AWAITING POST"
        print(f"   {e['id']:24s} pred {str(e.get('predicted_avg_pct')):>4}%   {state}")
    print()
    attribute()

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    lg = sub.add_parser("log");  lg.add_argument("--video", required=True)
    lg.add_argument("--predict", type=float); lg.add_argument("--id"); lg.add_argument("--notes", default="")
    rs = sub.add_parser("resolve"); rs.add_argument("--id", required=True)
    for k in ("views", "avg-pct", "3s-pct", "full-pct", "likes", "shares", "comments"):
        rs.add_argument(f"--{k}", type=float)
    cv = sub.add_parser("curve"); cv.add_argument("--id", required=True)
    cv.add_argument("--points", required=True,
                    help="second:pct pairs, e.g. 0:100,1:95,3:71,5:64,10:52")
    sub.add_parser("report"); sub.add_parser("attribute")
    a = ap.parse_args()
    if a.cmd == "log": log_build(a.video, a.predict, a.id, a.notes)
    elif a.cmd == "resolve":
        resolve(a.id, views=a.views, avg_pct=getattr(a, "avg_pct"),
                three_s_pct=getattr(a, "3s_pct", None), full_pct=getattr(a, "full_pct"),
                likes=a.likes, shares=a.shares, comments=a.comments)
    elif a.cmd == "curve":
        d = _load()
        pts = []
        for tok in a.points.split(","):
            t, _, p = tok.partition(":")
            pts.append((float(t), float(p)))
        for e in d["entries"]:
            if e["id"] == a.id:
                e.setdefault("actual", {})
                if e["actual"] is None: e["actual"] = {}
                e["actual"]["curve"] = pts
                _save(d)
                curve_attribution(a.id, pts, e.get("shots"))
                return
        print(f"no entry '{a.id}' - log the build first")
    elif a.cmd == "attribute": attribute()
    else: report()

if __name__ == "__main__":
    main()
