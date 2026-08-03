#!/usr/bin/env python3
"""
RUN_KK — locate everything, import the assets, then build.

WHY THIS IS PYTHON AND NOT BATCH
  The batch version failed twice. Embedding PowerShell inside .bat means cmd parses the
  string first, so a path containing parentheses - "C:\\Program Files (x86)" - closes the
  enclosing IF block early and corrupts the script. Batch quoting cannot be made reliable
  here. Python is already installed, so all the logic lives here and the .bat just calls it.

WHAT IT DOES
  1. find ffmpeg + ffprobe (PATH, then package-manager install roots, then a zip it extracts)
  2. find the KK_* assets anywhere on the machine, by looking for KK_VO.wav
  3. move them into work/ - never overwriting anything
  4. verify the 11-file manifest
  5. hand off to build_kk.py

Usage:  python tools/run_kk.py [--dry-run] [--src FOLDER] [--ffmpeg FOLDER]
"""
import os, sys, shutil, zipfile, argparse, subprocess, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work")
sys.path.insert(0, os.path.join(ROOT, "tools"))

MANIFEST = ["KK_01_hook_sunset.mp4", "KK_02_market_wide.mp4", "KK_03_grill.mp4",
            "KK_04_nev_eating.mp4", "KK_05_boat.mp4", "KK_07_beach_nev.mp4",
            "KK_08_sunset_hero.mp4", "KK_10_cta_silhouette.mp4",
            "KK_S6_coral.png", "KK_S9_silhouettes.png", "KK_VO.wav"]

EXE = ".exe" if os.name == "nt" else ""

class Tee:
    """Everything printed also lands in work/last-run.txt, so a failed run can be read
    back without anyone having to retype a console window."""
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.f = open(path, "w", encoding="utf-8", errors="replace")
        self.out = sys.__stdout__
    def write(self, s):
        self.out.write(s); self.out.flush()
        self.f.write(s); self.f.flush()
    def flush(self):
        self.out.flush(); self.f.flush()

def hr(t=""):
    print("=" * 58) if not t else print("=" * 58 + f"\n{t}\n" + "=" * 58)

def find_file(roots, names, max_depth=None, limit_seconds=90, need_all=False,
              collect=None):
    """Walk roots looking for `names`. Returns the containing directory, or None.

    need_all=True requires EVERY name in the same folder. That matters: CapCut bundles
    ffmpeg.exe with no ffprobe.exe, so matching on ffmpeg alone finds a partial install
    that cannot probe durations. Near-misses go into `collect` for diagnostics.

    No depth cap on targeted roots - package managers bury ffmpeg 7-8 levels down, and a
    depth-6 limit is exactly what made an earlier version miss a real install.
    """
    t0 = time.time()
    want = {n.lower() for n in names}
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        base = root.rstrip(os.sep).count(os.sep)
        for dirpath, dirnames, filenames in os.walk(root, topdown=True, onerror=lambda e: None):
            if time.time() - t0 > limit_seconds:
                return None
            if max_depth is not None and dirpath.count(os.sep) - base >= max_depth:
                dirnames[:] = []
            dirnames[:] = [d for d in dirnames if d.lower() not in
                           {"$recycle.bin", "system volume information", "windows",
                            "node_modules", ".git", "onedrivetemp"}]
            here = {f.lower() for f in filenames}
            hit = want & here
            if need_all:
                if want <= here:
                    return dirpath
                if hit and collect is not None:
                    collect.append((dirpath, sorted(hit), sorted(want - here)))
            elif hit:
                return dirpath
    return None

def locate_ffmpeg(override=None):
    PAIR = ["ffmpeg" + EXE, "ffprobe" + EXE]
    partial = []
    if override:
        if all(os.path.isfile(os.path.join(override, x)) for x in PAIR):
            return override
        have = [x for x in PAIR if os.path.isfile(os.path.join(override, x))]
        print(f"  !! --ffmpeg {override}: has {have or 'neither binary'}, "
              f"needs both ffmpeg{EXE} and ffprobe{EXE}")
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        d = os.path.dirname(shutil.which("ffmpeg"))
        print(f"  OK  both on PATH: {d}")
        return d

    home = os.path.expanduser("~")
    la = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
    targeted = [
        ROOT, os.path.join(ROOT, "bin"), os.path.join(ROOT, "ffmpeg-extracted"),
        os.path.join(la, "Microsoft", "WinGet", "Packages"),   # winget
        os.path.join(home, "scoop", "apps"),                    # scoop
        r"C:\ProgramData\chocolatey",                           # chocolatey
        os.path.join(la, "Programs"),
        r"C:\ffmpeg", r"C:\Tools",
        r"C:\Program Files", r"C:\Program Files (x86)",         # parens are fine in Python
        os.environ.get("APPDATA", ""),
    ]
    print("  .. checking install locations (no depth limit)")
    d = find_file(targeted, PAIR, limit_seconds=75, need_all=True, collect=partial)
    if d:
        print(f"  OK  found: {d}")
        return d

    print("  .. widening to your user folder and other drives")
    broad = [home]
    for drv in ("D:\\", "E:\\", "C:\\Users\\Public"):
        if os.path.isdir(drv):
            broad.append(drv)
    d = find_file(broad, PAIR, max_depth=10, limit_seconds=150,
                  need_all=True, collect=partial)
    if d:
        print(f"  OK  found: {d}")
        return d

    print("  .. looking for a still-zipped ffmpeg archive")
    zpath = None
    for root in [home] + [x for x in ("D:\\",) if os.path.isdir(x)]:
        for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
            if dirpath.count(os.sep) - root.rstrip(os.sep).count(os.sep) >= 8:
                dirnames[:] = []
            dirnames[:] = [x for x in dirnames if x.lower() not in
                           {"$recycle.bin", "system volume information", "windows"}]
            for f in filenames:
                if "ffmpeg" in f.lower() and f.lower().endswith(".zip"):
                    c = os.path.join(dirpath, f)
                    if zpath is None or os.path.getsize(c) > os.path.getsize(zpath):
                        zpath = c
            if zpath:
                break
        if zpath:
            break
    if zpath:
        out = os.path.join(ROOT, "ffmpeg-extracted")
        print(f"  .. extracting {os.path.basename(zpath)}")
        try:
            with zipfile.ZipFile(zpath) as z:
                z.extractall(out)
            d = find_file([out], PAIR, need_all=True)
            if d:
                print(f"  OK  extracted to: {d}")
                return d
        except Exception as e:
            print(f"  !! extract failed: {e}")
    # Authorised by the user: "quickly reinstall it and continue".
    # winget is Microsoft's own package manager; Gyan.FFmpeg is the standard full build.
    if os.name == "nt" and shutil.which("winget"):
        print("  .. no full build found. Installing via winget (authorised)")
        try:
            subprocess.run("winget install Gyan.FFmpeg --accept-source-agreements "
                           "--accept-package-agreements --disable-interactivity",
                           shell=True, timeout=900)
        except Exception as e:
            print(f"  !! winget failed: {e}")
        # winget does not update THIS process's PATH, so look in its package root
        la2 = os.environ.get("LOCALAPPDATA", os.path.join(os.path.expanduser("~"), "AppData", "Local"))
        d = find_file([os.path.join(la2, "Microsoft", "WinGet", "Packages"),
                       r"C:\Program Files", os.path.join(la2, "Programs")],
                      PAIR, need_all=True, limit_seconds=90)
        if d:
            print(f"  OK  installed: {d}")
            return d
        print("  !! installed but the binaries were not located; "
              "close this window, open a new one, and re-run")
    if partial:
        print("\n  Partial installs found (these bundle ffmpeg but not ffprobe,")
        print("  so they cannot be used - a full build ships both):")
        seen = set()
        for d, have, miss in partial:
            if d in seen: continue
            seen.add(d)
            print(f"    {d}\n        has {have}, missing {miss}")
    return None

def locate_assets(override=None):
    if override:
        if os.path.isfile(os.path.join(override, "KK_VO.wav")):
            return override
        print(f"  !! --src {override} has no KK_VO.wav")
    if os.path.isfile(os.path.join(WORK, "KK_VO.wav")):
        print("  OK  already imported into work/")
        return None
    home = os.path.expanduser("~")
    roots = [os.path.join(home, "Downloads"), r"D:\UserFolders\Downloads",
             os.path.join(home, "Desktop"), home]
    for drv in ("D:\\", "E:\\"):
        if os.path.isdir(drv):
            roots.append(drv)
    roots = [r for r in roots if os.path.isdir(r)]
    print("  .. searching for KK_VO.wav")
    d = find_file(roots, ["KK_VO.wav"], max_depth=8, limit_seconds=120)
    if d:
        print(f"  OK  source folder: {d}")
    return d

def safe_move(src, dst_dir, dry=False):
    """Never overwrite. If the name is taken, leave the source alone and report it."""
    dst = os.path.join(dst_dir, os.path.basename(src))
    if os.path.exists(dst):
        return "skip"
    if dry:
        return "would-move"
    os.makedirs(dst_dir, exist_ok=True)
    shutil.move(src, dst)
    return "moved"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, move nothing")
    ap.add_argument("--src", help="folder holding the KK_* files")
    ap.add_argument("--ffmpeg", help="folder holding ffmpeg.exe")
    a = ap.parse_args()

    sys.stdout = sys.stderr = Tee(os.path.join(WORK, "last-run.txt"))
    print("python", sys.version.split()[0], "|", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("repo  ", ROOT)
    hr("TALYX AUTO-BUILD\n3 Best Spots in Kota Kinabalu Sabah  |  30s  |  9:16")
    os.makedirs(WORK, exist_ok=True)

    print("\n[1/4] ffmpeg")
    ffdir = locate_ffmpeg(a.ffmpeg)
    if not ffdir:
        print("""
  !! ffmpeg not found, and no ffmpeg zip either.

     Fastest fix - open a NEW terminal and run one of these yourself:
         winget install Gyan.FFmpeg
         choco install ffmpeg

     Or download the "full" build from https://www.gyan.dev/ffmpeg/builds/,
     unzip it, and copy ffmpeg.exe + ffprobe.exe into:
         %s

     Then run this again. I can't install software for you.

     NOTE if you believe it IS installed: winget updates PATH, but an
     already-running explorer.exe keeps the old environment, so anything you
     double-click inherits a stale PATH. Sign out and back in, or pass the
     folder directly:  python tools/run_kk.py --ffmpeg "C:\\path\\to\\bin"
""" % ROOT)
        return 2
    os.environ["PATH"] = ffdir + os.pathsep + os.environ.get("PATH", "")
    if not shutil.which("ffprobe"):
        print(f"  !! ffprobe{EXE} is missing from {ffdir} (it ships beside ffmpeg)")
        return 2
    print("  OK  ffprobe")

    print("\n[1b/4] Python packages")
    for mod, pkg in (("cv2", "opencv-python-headless"), ("numpy", "numpy"),
                     ("faster_whisper", "faster-whisper")):
        try:
            __import__(mod); print(f"  OK  {mod}")
        except ImportError:
            print(f"  .. installing {pkg} (one time)")
            subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", pkg])
            try:
                __import__(mod); print(f"  OK  {mod}")
            except ImportError:
                print(f"  !! {mod} still unavailable - the gate will not report numbers")

    print("\n[2/4] KK assets")
    src = locate_assets(a.src)
    if src:
        moved = skipped = 0
        for f in sorted(os.listdir(src)):
            if not f.startswith("KK_"):
                continue
            if not f.lower().endswith((".mp4", ".wav", ".png", ".jpg", ".mov")):
                continue
            r = safe_move(os.path.join(src, f), WORK, a.dry_run)
            if r == "skip":
                skipped += 1
            else:
                moved += 1
                print(f"  ++ {r}: {f}")
        print(f"  imported {moved} | already present {skipped}")

    print("\n[3/4] Manifest")
    missing = [m for m in MANIFEST if not os.path.isfile(os.path.join(WORK, m))]
    for m in MANIFEST:
        print(f"  {'ok      ' if m not in missing else 'MISSING '} {m}")
    if missing:
        print(f"\n  !! {len(missing)} missing. Put them in:\n     {WORK}\n  then run again.")
        return 3
    print("  OK  all 11 present")

    if a.dry_run:
        print("\n[4/4] --dry-run: stopping before the build.")
        return 0

    print("\n[4/4] Build\n")
    import build_kk
    build_kk.main()
    out = os.path.join(ROOT, "output", "KK_3SPOTS_v1.mp4")
    if os.path.isfile(out):
        print(f"\nFINAL: {out}")
        if os.name == "nt":
            subprocess.run(f'explorer "{os.path.dirname(out)}"', shell=True)
    else:
        print("\n  !! no output produced - read the errors above")
        return 4
    return 0

if __name__ == "__main__":
    sys.exit(main())
