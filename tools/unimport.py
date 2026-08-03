#!/usr/bin/env python3
"""
UNIMPORT — pull back files the watcher filed wrongly. Moves, never deletes.

WHY THIS WAS NEEDED
  The first watcher run polluted the asset banks:
    assets/nev/       169 files instead of 50 - 119 unrelated camera photos, because
                      ANY drive-download*.zip was assumed to be Nev images
    work/             BROLL_*, MQF_*, SLD_* - my "any uppercase prefix is project material"
                      regex was far too broad AND ran before the specific BROLL_ rule
    fonts/slenco/     slenco.zip is not a font

  Everything was COPIED, not moved, so the Downloads originals are intact. This just
  un-does the AI-folder side, into a quarantine folder so nothing is destroyed.
"""
import os, re, shutil, sys, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(ROOT, "work", "quarantine", "mis-imported")

# The real Nev drop is WhatsApp exports; anything else in there arrived by mistake.
NEV_KEEP = re.compile(r"^WhatsApp Image", re.I)
# Only these prefixes are project material. An allowlist, not a pattern.
PROJECTS = ("KK_", "CROWN_", "S450_")

def pull(src, why, dry):
    rel = os.path.relpath(src, ROOT)
    dst = os.path.join(Q, rel.replace(os.sep, "__"))
    if dry: return f"would pull  {rel}   ({why})"
    os.makedirs(Q, exist_ok=True)
    if os.path.exists(dst): dst += ".dup"
    shutil.move(src, dst)
    return f"pulled  {rel}   ({why})"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(); dry = not a.apply
    out = []
    nev = os.path.join(ROOT, "assets", "nev")
    if os.path.isdir(nev):
        for f in sorted(os.listdir(nev)):
            p = os.path.join(nev, f)
            if os.path.isfile(p) and not NEV_KEEP.match(f):
                out.append(pull(p, "not a Nev reference", dry))
    w = os.path.join(ROOT, "work")
    if os.path.isdir(w):
        for f in sorted(os.listdir(w)):
            p = os.path.join(w, f)
            if not os.path.isfile(p): continue
            if f.startswith(PROJECTS): continue
            if f.lower().endswith((".mp4",".mov",".png",".jpg",".jpeg")) and \
               re.match(r"^[A-Z0-9]{2,10}_", f):
                out.append(pull(p, "not a registered project", dry))
    fdir = os.path.join(ROOT, "assets", "shared", "fonts")
    if os.path.isdir(fdir):
        for d in sorted(os.listdir(fdir)):
            dp = os.path.join(fdir, d)
            if os.path.isdir(dp) and not any(x.lower().endswith((".ttf",".otf"))
                                             for x in os.listdir(dp)):
                out.append(pull(dp, "contains no font files", dry))
    print("="*62); print("UNIMPORT" + ("  (dry run)" if dry else "  APPLYING")); print("="*62)
    for line in out[:14]: print("  " + line)
    if len(out) > 14: print(f"  ... and {len(out)-14} more")
    print(f"\n  {len(out)} item(s). Quarantine: work/quarantine/mis-imported/")
    print("  Downloads originals are untouched — the watcher copies, it does not move.")
    if dry: print("  run with --apply")
if __name__ == "__main__": sys.exit(main())
