#!/usr/bin/env python3
"""
WATCHER — sits on your Downloads folder and files things into the AI folder automatically.

WHY
  His words: "its quite annoying if i have to manually move everything on my own into the
  AI folder". Correct, and it is also a failure point - twice this session an asset was
  downloaded and then simply not imported (the Nev images sat in Drive for hours; the KK
  renders sat in Downloads while the build reported files missing).

  Every manual step between "downloaded" and "usable" is a place the pipeline stalls.

WHAT IT DOES
  Polls Downloads every few seconds. When a file appears that this system recognises, it
  waits for the download to FINISH (size stable for two polls - a partial .mp4 imported
  mid-download is worse than no file), then classifies and moves it using the exact same
  rules as import_bank.py. Nothing is ever overwritten.

  hf_<date>_<jobid>.mp4   -> work/ renamed via work/ledgers/rename_manifest.json
  KK_* / CROWN_*          -> work/
  drive-download*.zip     -> assets/nev/          (unzipped)
  <Font>.zip              -> assets/shared/fonts/ (unzipped)
  SFX_* BGM_* BROLL_*     -> their banks

SAFETY
  - never overwrites; a name clash leaves the source alone and logs it
  - never deletes anything from Downloads that it did not successfully copy
  - only touches files matching known patterns; everything else is ignored
  - Ctrl+C to stop

Usage
  python tools/watcher.py                # watch until stopped
  python tools/watcher.py --once         # single sweep, then exit
  python tools/watcher.py --interval 3
"""
import argparse, os, sys, time, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import import_bank as IB


def downloads_dir():
    home = os.path.expanduser("~")
    for c in (os.path.join(home, "Downloads"), r"D:\UserFolders\Downloads",
              r"D:\USER FOLDER IMPORTANT\Downloads", os.path.join(home, "Desktop")):
        if os.path.isdir(c):
            return c
    return None


def settled(path, seen, min_stable=2, age_settled=30.0):
    """A file is only safe to move once its size has stopped changing. Importing a partial
    mp4 produces a file that looks present and plays as garbage - worse than absent.

    BUT: a file last modified more than `age_settled` seconds ago is finished by definition.
    Without this, every pre-existing file in Downloads reported "still downloading" forever,
    because the stability counter starts at zero on first sight."""
    try:
        sz = os.path.getsize(path)
        if time.time() - os.path.getmtime(path) > age_settled:
            return sz > 0          # old file: definitely not mid-download
    except OSError:
        return False
    prev, count = seen.get(path, (None, 0))
    if prev == sz and sz > 0:
        count += 1
    else:
        count = 0
    seen[path] = (sz, count)
    return count >= min_stable


def handle(p, dry=False):
    kind = IB.classify(p)
    if not kind:
        return None
    n = os.path.basename(p)
    A, W = IB.A, IB.WORK
    if kind == "zip_nev":
        c = IB.unzip_images(p, os.path.join(A, "nev"), dry)
        return f"{n} -> assets/nev/ ({c} images)" if c else None
    if kind == "zip_font":
        c, fam = IB.unzip_fonts(p, os.path.join(A, "shared", "fonts"), dry)
        return f"{n} -> assets/shared/fonts/{fam}/ ({c})" if c else None
    if kind == "work_named":
        tgt = IB.manifest_name(p)
        st, _ = IB.safe_copy(p, W, dry, rename=tgt)
        return f"{n} -> work/{tgt}" if st in ("copied", "would-copy") else None
    if kind == "work":
        st, _ = IB.safe_copy(p, W, dry)
        return f"{n} -> work/" if st in ("copied", "would-copy") else None
    if kind == "font_loose":
        st, _ = IB.safe_copy(p, os.path.join(A, "shared", "fonts", "loose"), dry)
        return f"{n} -> assets/shared/fonts/loose/" if st in ("copied", "would-copy") else None
    if kind in ("sfx", "bgm", "broll"):
        sub = {"sfx": os.path.join(A, "sfx", "inbox"),
               "bgm": os.path.join(A, "bgm", "inbox"),
               "broll": os.path.join(A, "broll")}[kind]
        st, _ = IB.safe_copy(p, sub, dry)
        return f"{n} -> {os.path.relpath(sub, ROOT)}/" if st in ("copied", "would-copy") else None
    return None


def sweep(d, seen, done, dry=False, quiet=False):
    moved = 0
    try:
        entries = sorted(os.listdir(d))
    except OSError:
        return 0
    for f in entries:
        p = os.path.join(d, f)
        if not os.path.isfile(p) or p in done:
            continue
        if f.endswith((".crdownload", ".part", ".tmp")):
            continue
        if not IB.classify(p):
            continue
        if not settled(p, seen):
            continue          # genuinely mid-download; silently retry next sweep
        msg = handle(p, dry)
        done.add(p)          # examined once, never again - copied OR already present
        if msg:
            moved += 1
            print(f"  [{time.strftime('%H:%M:%S')}] {msg}", flush=True)
    return moved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=float, default=4.0)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dir")
    a = ap.parse_args()
    d = a.dir or downloads_dir()
    if not d:
        print("could not find a Downloads folder"); return 2
    print("=" * 60)
    print("WATCHER — auto-filing downloads into the AI folder")
    print("=" * 60)
    print(f"  watching : {d}")
    print(f"  into     : {ROOT}")
    print(f"  manifest : {len(IB.MANIFEST)} job-id rename rule(s) loaded")
    if a.dry_run: print("  DRY RUN — nothing will actually move")
    print("  Ctrl+C to stop\n")
    seen, done = {}, set()
    print("  first sweep (existing files are examined once, then ignored)...", flush=True)
    total = sweep(d, seen, done, a.dry_run)
    print(f"  first sweep done: {len(done)} file(s) examined, {total} filed\n", flush=True)
    if a.once:
        print(f"\n  {total} file(s) filed."); return 0
    try:
        while True:
            time.sleep(a.interval)
            total += sweep(d, seen, done, a.dry_run, quiet=True)
    except KeyboardInterrupt:
        print(f"\n  stopped. {total} file(s) filed this session.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
