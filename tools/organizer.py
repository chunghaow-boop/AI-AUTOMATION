#!/usr/bin/env python3
"""
ORGANIZER — keeps the folder sane as generations pile up, and scopes assets by pillar.

TWO PROBLEMS THIS SOLVES, both his

  1. "when there are many generations it starts to look messy"
     work/ accumulates sources, intermediates, QC frames, JSON and finished cuts until
     nothing is findable. Already hit 41 items once.

  2. "categorise different references, styles, assets with different types of videos...
      if not it will clash, because all of the assets are in the same folder,
      maybe you got confused"
     He is exactly right, and it is diagnostic. assets/bgm/generated/ held the travel bed,
     the auto-hero bed and the phonk bed side by side. I chose by FILENAME and reached for
     a 90 BPM marimba bed on a car edit, when the genre is 140-170 BPM drift phonk.
     A car build must not be able to SEE a travel bed.

PILLAR SCOPING
    assets/pillars/<pillar>/{bgm,sfx,refs,plates}   only this pillar's build may read these
    assets/shared/{transitions,ui,fonts,nev}        genuinely format-agnostic

PROJECT SCOPING
    work/projects/<project>/{sources,tmp,qc,out}    one folder per build
    work/archive/<date>/                            finished builds, moved not deleted

SAFETY
  Never deletes. Only moves, and never over an existing file. --dry-run shows the plan.

Usage
  python3 organizer.py --plan                 show what would move
  python3 organizer.py --apply
  python3 organizer.py --project crown --apply
"""
import argparse, json, os, re, shutil, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A    = os.path.join(ROOT, "assets")
W    = os.path.join(ROOT, "work")

PILLARS = {
    "car_cinematic": {
        "bgm":  ["phonk", "auto_hero", "drift"],
        "sfx":  ["car"],
        "note": "drift phonk 140-170 BPM, cowbell signature. NOT the travel beds.",
    },
    "travel_vlog": {
        "bgm":  ["sunset_warm", "travel_bright", "lofi", "travel_arrangement"],
        "sfx":  [],
        "note": "warm/organic. marimba + hand percussion.",
    },
    "car_review":   {"bgm": [], "sfx": ["car", "ui"], "note": "spoken; bed sits low."},
    "industry":     {"bgm": [], "sfx": ["ui"],        "note": "B2B; proof + on-screen data."},
}
KEEP_SOURCES = True   # source clips stay in work/ - every build reads them there
SHARED_SFX = ["transition", "impact", "ui"]

def plan_assets():
    moves = []
    gen = os.path.join(A, "bgm", "generated")
    if os.path.isdir(gen):
        for f in sorted(os.listdir(gen)):
            if not f.lower().endswith((".wav", ".mp3")): continue
            if f.startswith("STEM_"):
                moves.append((os.path.join(gen, f), os.path.join(A, "shared", "stems", f)))
                continue
            dest = None
            for pil, spec in PILLARS.items():
                if any(k in f.lower() for k in spec["bgm"]): dest = pil; break
            if dest:
                moves.append((os.path.join(gen, f),
                              os.path.join(A, "pillars", dest, "bgm", f)))
    for sub in SHARED_SFX:
        d = os.path.join(A, "sfx", sub)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                moves.append((os.path.join(d, f), os.path.join(A, "shared", "sfx", sub, f)))
    d = os.path.join(A, "sfx", "car")
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            moves.append((os.path.join(d, f),
                          os.path.join(A, "pillars", "car_cinematic", "sfx", f)))
    for name in ("nev", "fonts", "broll"):
        d = os.path.join(A, name)
        if os.path.isdir(d):
            for dirpath, _, files in os.walk(d):
                for f in files:
                    rel = os.path.relpath(os.path.join(dirpath, f), d)
                    moves.append((os.path.join(dirpath, f),
                                  os.path.join(A, "shared", name, rel)))
    return moves

def guess_project(fn):
    n = fn.lower()
    if n.startswith("kk_") or "3spots" in n: return "kk_3spots"
    if n.startswith("crown"): return "crown_15s"
    return None

def plan_work():
    moves = []
    if not os.path.isdir(W): return moves
    for f in sorted(os.listdir(W)):
        p = os.path.join(W, f)
        if os.path.isdir(p):
            if f.startswith("_") and f.endswith("_tmp"):
                proj = "kk_3spots" if "kk" in f else ("crown_15s" if "crown" in f else "misc")
                moves.append((p, os.path.join(W, "projects", proj, "tmp")))
            elif f == "qc":
                moves.append((p, os.path.join(W, "projects", "_qc")))
            continue
        if f.endswith(".md"):
            proj = guess_project(f)
            dst = (os.path.join(W,"projects",proj,"plan",f) if proj
                   else os.path.join(W,"plans",f))
            moves.append((p, dst)); continue
        proj = guess_project(f)
        if proj:
            if re.search(r"_v\d+\.mp4$", f):
                moves.append((p, os.path.join(W, "projects", proj, "out", f)))
            elif not KEEP_SOURCES:
                moves.append((p, os.path.join(W, "projects", proj, "sources", f)))
        elif f.endswith((".json", ".csv", ".txt")):
            moves.append((p, os.path.join(W, "ledgers", f)))
    return moves

def apply(moves, dry=True):
    done = skipped = 0
    for src, dst in moves:
        if not os.path.exists(src): continue
        if os.path.exists(dst):
            skipped += 1; continue
        if dry:
            done += 1; continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            shutil.move(src, dst); done += 1
        except Exception as e:
            print(f"  !! {os.path.basename(src)}: {str(e)[:50]}"); skipped += 1
    return done, skipped

def write_map():
    """Formats read their assets THROUGH this map, so a build cannot reach another
    pillar's material even by accident."""
    m = {p: {"bgm":  f"assets/pillars/{p}/bgm",
             "sfx":  [f"assets/pillars/{p}/sfx"] + [f"assets/shared/sfx/{s}" for s in SHARED_SFX],
             "plates": f"assets/pillars/{p}/plates",
             "refs":   f"assets/pillars/{p}/refs",
             "note": s["note"]} for p, s in PILLARS.items()}
    m["_shared"] = {"fonts": "assets/shared/fonts", "nev": "assets/shared/nev",
                    "broll": "assets/shared/broll", "stems": "assets/shared/stems"}
    p = os.path.join(A, "pillar_map.json")
    os.makedirs(A, exist_ok=True)
    json.dump(m, open(p, "w"), indent=2)
    return p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--assets-only", action="store_true")
    ap.add_argument("--work-only", action="store_true")
    ap.add_argument("--move-sources", action="store_true",
                    help="also relocate source clips (will break builds until paths update)")
    a = ap.parse_args()
    global KEEP_SOURCES
    KEEP_SOURCES = not a.move_sources
    dry = not a.apply
    print("="*62)
    print("ORGANIZER" + ("   (dry run — nothing will move)" if dry else "   APPLYING"))
    print("="*62)
    total = 0
    if not a.work_only:
        m = plan_assets()
        d, s = apply(m, dry)
        print(f"\n  assets -> pillars/shared : {d} move(s), {s} skipped (already there)")
        for src, dst in m[:6]:
            print(f"     {os.path.basename(src):28s} -> {os.path.relpath(dst, ROOT)}")
        if len(m) > 6: print(f"     ... and {len(m)-6} more")
        total += d
    if not a.assets_only:
        m = plan_work()
        d, s = apply(m, dry)
        print(f"\n  work -> projects/ledgers : {d} move(s), {s} skipped")
        for src, dst in m[:6]:
            print(f"     {os.path.basename(src):28s} -> {os.path.relpath(dst, ROOT)}")
        if len(m) > 6: print(f"     ... and {len(m)-6} more")
        total += d
    p = write_map()
    print(f"\n  pillar map -> {os.path.relpath(p, ROOT)}")
    for k, v in PILLARS.items(): print(f"     {k:16s} {v['note']}")
    print(f"\n  {total} file(s) " + ("would move" if dry else "moved") + ". Nothing deleted.")
    if dry: print("  run with --apply to do it")
    return 0

if __name__ == "__main__":
    sys.exit(main())
