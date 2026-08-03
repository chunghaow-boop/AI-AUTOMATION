#!/usr/bin/env python3
"""
INTEL — the trend intelligence ledger.

What it does NOT do: scrape Douyin/TikTok. Those platforms block automated access and the
sandbox network is allowlisted. Any scraper here would break on first run. Instead this is
the ledger + synthesiser; the *fetching* is done by tools that legitimately can:
  - Higgsfield `video_analysis_create`  (accepts YouTube URLs -> scene-by-scene breakdown)
  - Higgsfield `virality_predictor`     (hook strength, retention risk)
  - Higgsfield `tiktok_music_trending`  (trending commercial tracks by country/genre)
  - WebSearch                            (what's working this week, benchmarks)
Claude runs those in-session and pipes the JSON in here with `--ingest`.

Usage:
  python3 intel.py add "https://youtube.com/..." --note "great 3s hook"
  python3 intel.py pending                  # URLs awaiting analysis
  python3 intel.py ingest analysis.json --url "..."   # store a scene analysis
  python3 intel.py brief                    # weekly brief + bank deltas
  python3 intel.py banks                    # dump learned mechanisms
"""
import json, os, sys, argparse, datetime, re, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(ROOT, "intel_db.json")

# 2026 benchmarks (source: retention benchmark research, logged 2026-07-26).
# NOTE: a 30-50% target is BELOW par for short-form in 2026. Gate at benchmark.
BENCH = {
    "tiktok":   {"<30s": (50,60), "30-60s": (40,50), ">60s": (30,40), "viral": 70},
    "reels":    {"<30s": (45,65), "viral": 70},
    "shorts":   {"<30s": (40,55), "viral": 70},
}

def load():
    if os.path.exists(DB):
        return json.load(open(DB))
    return {"watchlist": [], "analyses": [], "banks": {"hooks": [], "transitions": [],
            "twists": [], "ctas": [], "sfx_moments": []}, "log": []}

def save(d):
    json.dump(d, open(DB, "w"), indent=2)

def uid(s): return hashlib.md5(s.encode()).hexdigest()[:10]

def cmd_add(a):
    d = load()
    if any(w["url"] == a.url for w in d["watchlist"]):
        print("already on watchlist"); return
    d["watchlist"].append({"id": uid(a.url), "url": a.url, "note": a.note or "",
                           "added": datetime.date.today().isoformat(), "analyzed": False})
    save(d); print(f"added {a.url}")

def cmd_pending(a):
    d = load()
    p = [w for w in d["watchlist"] if not w["analyzed"]]
    print(json.dumps(p, indent=2))
    if p:
        print(f"\n{len(p)} pending. Claude: run video_analysis_create on each, "
              f"then `intel.py ingest <json> --url <url>`", file=sys.stderr)

def extract_mechanisms(scenes):
    """Pull reusable mechanisms out of a scene-by-scene analysis."""
    out = {"hooks": [], "transitions": [], "twists": [], "ctas": [], "sfx_moments": []}
    if not scenes: return out
    txt_all = " ".join(json.dumps(s).lower() for s in scenes)
    first = json.dumps(scenes[0]).lower() if scenes else ""
    last  = json.dumps(scenes[-1]).lower() if scenes else ""
    # hook mechanism = what happens in scene 1
    if first:
        out["hooks"].append({"scene": scenes[0],
            "motion_open": any(k in first for k in ("move","walk","drive","run","pan","push","reveal")),
            "static_open": any(k in first for k in ("pose","stand still","static","portrait"))})
    for k in ("cut","dissolve","match","whip","mask","speed ramp","zoom","transition","jump cut"):
        if k in txt_all: out["transitions"].append(k)
    for k in ("reveal","twist","turns out","actually","but then","surprise"):
        if k in txt_all: out["twists"].append(k)
    if last: out["ctas"].append({"closing_scene": scenes[-1]})
    for k in ("whoosh","impact","riser","bass drop","click","swoosh","thud"):
        if k in txt_all: out["sfx_moments"].append(k)
    return out

def cmd_ingest(a):
    d = load()
    payload = json.load(open(a.file))
    scenes = payload.get("scenes") or payload.get("result") or payload
    if isinstance(scenes, dict): scenes = scenes.get("scenes", [])
    mech = extract_mechanisms(scenes if isinstance(scenes, list) else [])
    d["analyses"].append({"url": a.url, "date": datetime.date.today().isoformat(),
                          "scene_count": len(scenes) if isinstance(scenes,list) else 0,
                          "mechanisms": mech, "raw": payload})
    for k, v in mech.items():
        for item in v:
            if item not in d["banks"][k]:
                d["banks"][k].append(item)
    for w in d["watchlist"]:
        if w["url"] == a.url: w["analyzed"] = True
    d["log"].append(f"{datetime.date.today()} ingested {a.url}")
    save(d)
    print(json.dumps({"ingested": a.url, "new_mechanisms": mech}, indent=2)[:2000])

def cmd_brief(a):
    d = load()
    pend = [w for w in d["watchlist"] if not w["analyzed"]]
    print("="*60); print("WEEKLY INTEL BRIEF", datetime.date.today().isoformat()); print("="*60)
    print(f"watchlist: {len(d['watchlist'])} total, {len(pend)} awaiting analysis")
    print(f"analysed : {len(d['analyses'])} videos")
    print("\nBANKS (learned mechanisms):")
    for k, v in d["banks"].items():
        flat = [x if isinstance(x,str) else "(scene)" for x in v]
        print(f"  {k:<14} {len(v):>3}  {', '.join(sorted(set(flat))[:8])}")
    print("\n2026 RETENTION BENCHMARKS — gate here, not at 30-50%:")
    for plat, b in BENCH.items():
        print(f"  {plat:<8} " + " · ".join(f"{k}:{v}" for k,v in b.items()))
    print("\nNEXT: analyse pending URLs, then feed banks into Phase 1 (file 13/02/11).")

def cmd_banks(a):
    print(json.dumps(load()["banks"], indent=2))

def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add");     s.add_argument("url"); s.add_argument("--note"); s.set_defaults(f=cmd_add)
    s = sub.add_parser("pending"); s.set_defaults(f=cmd_pending)
    s = sub.add_parser("ingest");  s.add_argument("file"); s.add_argument("--url", required=True); s.set_defaults(f=cmd_ingest)
    s = sub.add_parser("brief");   s.set_defaults(f=cmd_brief)
    s = sub.add_parser("banks");   s.set_defaults(f=cmd_banks)
    a = p.parse_args(); a.f(a)

if __name__ == "__main__":
    main()
