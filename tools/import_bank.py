#!/usr/bin/env python3
"""
IMPORT_BANK — find downloads anywhere on the machine, sort them into assets/, never overwrite.

WHY THIS EXISTS
  Twice this session an asset was downloaded and then simply not imported: the Nev 360 images
  sat in a Drive link for hours while assets/nev stayed empty, and the KK renders sat in
  Downloads while the build reported files missing. Both were the same failure - a human step
  between "downloaded" and "usable". This removes that step.

WHAT IT SORTS
  drive-download-*.zip / NEV*.zip      -> assets/nev/          (character reference)
  <Font_Name>.zip containing .ttf/.otf -> assets/fonts/<Family>/
  SFX_* BGM_* *.wav *.mp3              -> assets/sfx/ or assets/bgm/inbox/
  BROLL_* *.mp4 *.mov                  -> assets/broll/
  KK_* / any exam asset                -> work/

SAFETY
  - NEVER overwrites. If a name is taken the source is left alone and reported.
  - Only touches files it can classify; anything unrecognised is listed, not moved.
  - --dry-run shows the plan without touching a thing.

Usage
  python tools/import_bank.py              # find, sort, report
  python tools/import_bank.py --dry-run
"""
import os, sys, shutil, zipfile, argparse, time, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A    = os.path.join(ROOT, "assets")
WORK = os.path.join(ROOT, "work")

# Registered projects. Add a prefix here when a new build starts - deliberately manual,
# because a pattern is what caused MQF_ and SLD_ brochures to be imported as build material.
PROJECTS = ("KK_", "CROWN_", "S450_")

# Font zips must name a family we actually asked for. "slenco.zip" matched a loose
# lowercase-zip pattern and became a font folder with no fonts in it.
FONT_FAMILIES = ("bebas", "anton", "montserrat", "oswald", "poppins", "inter",
                 "archivo", "barlow", "roboto", "lato", "raleway")

IMG = (".jpg", ".jpeg", ".png", ".webp")
AUD = (".wav", ".mp3", ".aif", ".aiff", ".m4a", ".ogg")
VID = (".mp4", ".mov", ".m4v", ".webm")
FNT = (".ttf", ".otf")

def log(m): print(m, flush=True)

def search_roots():
    home = os.path.expanduser("~")
    roots = [os.path.join(home, "Downloads"), r"D:\UserFolders\Downloads",
             os.path.join(home, "Desktop"), os.path.join(home, "Documents")]
    for d in ("D:\\", "E:\\"):
        if os.path.isdir(d): roots.append(d)
    return [r for r in roots if os.path.isdir(r)]

def recent_files(roots, max_age_days=14, max_depth=6, limit_seconds=120):
    """Only look at recently-modified files - an old drive full of media should not be
    trawled, and 'what I just downloaded' is always recent."""
    t0 = time.time(); cutoff = time.time() - max_age_days*86400
    found = []
    for root in roots:
        base = root.rstrip(os.sep).count(os.sep)
        for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
            if time.time() - t0 > limit_seconds: return found
            if dirpath.count(os.sep) - base >= max_depth: dirnames[:] = []
            dirnames[:] = [d for d in dirnames if d.lower() not in
                           {"$recycle.bin", "system volume information", "windows",
                            "node_modules", ".git", "appdata", "program files",
                            "program files (x86)"}]
            for f in filenames:
                p = os.path.join(dirpath, f)
                try:
                    if os.path.getmtime(p) >= cutoff: found.append(p)
                except OSError:
                    pass
    return found

def safe_copy(src, dst_dir, dry=False, rename=None):
    os.makedirs(dst_dir, exist_ok=True)
    name = rename or os.path.basename(src)
    dst = os.path.join(dst_dir, name)
    if os.path.exists(dst):
        return "exists", dst
    if dry: return "would-copy", dst
    shutil.copy2(src, dst)
    return "copied", dst

def unzip_images(zpath, dest, dry=False):
    """Drive folder downloads arrive as a zip of images (possibly nested)."""
    n = 0
    try:
        with zipfile.ZipFile(zpath) as z:
            members = [m for m in z.namelist()
                       if m.lower().endswith(IMG) and not m.startswith("__MACOSX")]
            if not members: return 0
            if dry: return len(members)
            os.makedirs(dest, exist_ok=True)
            for m in members:
                base = os.path.basename(m)
                if not base: continue
                sub = "closeup" if "closeup" in m.lower() else ""
                d = os.path.join(dest, sub) if sub else dest
                os.makedirs(d, exist_ok=True)
                out = os.path.join(d, base)
                if os.path.exists(out): continue
                with z.open(m) as s, open(out, "wb") as o:
                    shutil.copyfileobj(s, o)
                n += 1
    except zipfile.BadZipFile:
        log(f"    !! not a valid zip: {os.path.basename(zpath)}")
    return n

def unzip_fonts(zpath, dest_root, dry=False):
    fam = re.sub(r"[^A-Za-z0-9]+", "", os.path.splitext(os.path.basename(zpath))[0]) or "Font"
    n = 0
    try:
        with zipfile.ZipFile(zpath) as z:
            members = [m for m in z.namelist()
                       if m.lower().endswith(FNT) and not m.startswith("__MACOSX")]
            if not members: return 0, fam
            if dry: return len(members), fam
            # prefer static weights over variable when both ship
            dest = os.path.join(dest_root, fam); os.makedirs(dest, exist_ok=True)
            for m in members:
                base = os.path.basename(m)
                out = os.path.join(dest, base)
                if os.path.exists(out): continue
                with z.open(m) as s, open(out, "wb") as o:
                    shutil.copyfileobj(s, o)
                n += 1
    except zipfile.BadZipFile:
        log(f"    !! not a valid zip: {os.path.basename(zpath)}")
    return n, fam

def _manifest():
    # organizer.py moves ledgers into work/ledgers/ - look in both, same fix as the
    # other ledgers. "0 rename rules loaded" was this, silently.
    cands = [os.path.join(ROOT, "work", "ledgers", "rename_manifest.json"),
             os.path.join(ROOT, "work", "rename_manifest.json")]
    mp = next((c for c in cands if os.path.exists(c)), cands[0])
    if os.path.exists(mp):
        try:
            import json as _j; return _j.load(open(mp))
        except Exception: pass
    return {}

MANIFEST = _manifest()

def manifest_name(p):
    """Higgsfield names renders hf_<date>_<jobid>.mp4. Map the job id to the build's name."""
    n = os.path.basename(p).lower()
    for jid, target in MANIFEST.items():
        if jid.lower() in n: return target
    return None

def classify(p):
    n = os.path.basename(p); low = n.lower()
    ext = os.path.splitext(low)[1]
    if ext == ".zip":
        # ANY drive-download*.zip was being treated as Nev references. That dumped 119
        # unrelated camera photos into assets/nev/. A Drive zip must SAY it is Nev.
        if "nev" in low:                                       return "zip_nev"
        if low.startswith("drive-download"):                   return "zip_unknown"
        if any(f in low for f in FONT_FAMILIES) or "font" in low: return "zip_font"
        return None
    if manifest_name(p):                                       return "work_named"
    if low.startswith("sfx_") and ext in AUD:                  return "sfx"
    if low.startswith("bgm_") and ext in AUD:                  return "bgm"
    if low.startswith("broll_") and ext in VID:                return "broll"
    if n.startswith(PROJECTS):                                 return "work"
    if ext in FNT:                                             return "font_loose"
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--days", type=int, default=14)
    a = ap.parse_args()

    log("="*58); log("IMPORT BANK   find -> classify -> sort -> never overwrite"); log("="*58)
    roots = search_roots()
    log("searching: " + ", ".join(roots))
    files = recent_files(roots, a.days)
    log(f"  {len(files)} file(s) modified in the last {a.days} days\n")

    tally = {}
    def bump(k, n=1): tally[k] = tally.get(k, 0) + n

    for p in sorted(files):
        kind = classify(p)
        if not kind: continue
        n = os.path.basename(p)
        if kind == "zip_nev":
            c = unzip_images(p, os.path.join(A, "nev"), a.dry_run)
            if c: log(f"  NEV      {n} -> assets/nev/  ({c} images)"); bump("nev", c)
        elif kind == "zip_unknown":
            log(f"  ??       {n} -> NOT imported. A Drive zip is not assumed to be anything. "
                f"Rename it to include 'nev' if it is Nev references.")
            bump("skipped")
        elif kind == "zip_font":
            c, fam = unzip_fonts(p, os.path.join(A, "fonts"), a.dry_run)
            if c: log(f"  FONT     {n} -> assets/fonts/{fam}/  ({c} files)"); bump("fonts", c)
        elif kind == "font_loose":
            st, _ = safe_copy(p, os.path.join(A, "fonts", "loose"), a.dry_run)
            if st in ("copied","would-copy"): log(f"  FONT     {n}"); bump("fonts")
        elif kind == "work_named":
            tgt = manifest_name(p)
            st, _ = safe_copy(p, WORK, a.dry_run, rename=tgt)
            if st in ("copied","would-copy"):
                log(f"  WORK     {n}  ->  {tgt}"); bump("work")
            elif st == "exists": log(f"  --       {tgt} already present, source left alone")
        elif kind == "work":
            st, _ = safe_copy(p, WORK, a.dry_run)
            if st in ("copied","would-copy"): log(f"  WORK     {n}"); bump("work")
        elif kind in ("sfx","bgm","broll"):
            sub = {"sfx": os.path.join(A,"sfx","inbox"),
                   "bgm": os.path.join(A,"bgm","inbox"),
                   "broll": os.path.join(A,"broll")}[kind]
            st, _ = safe_copy(p, sub, a.dry_run)
            if st in ("copied","would-copy"): log(f"  {kind.upper():8s} {n}"); bump(kind)

    log("\n" + "="*58)
    if not tally:
        log("  nothing new to import (or nothing matched the patterns)")
    for k, v in sorted(tally.items()):
        log(f"  {k:8s} {v}")
    log("="*58)
    log("\nassets/ now holds:")
    for d in ("nev", "fonts", "broll", "sfx", "bgm"):
        pth = os.path.join(A, d)
        c = sum(len(fs) for _,_,fs in os.walk(pth)) if os.path.isdir(pth) else 0
        log(f"  {d:8s} {c}")
    if a.dry_run: log("\n(--dry-run: nothing was actually moved)")

if __name__ == "__main__":
    main()
