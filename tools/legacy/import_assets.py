#!/usr/bin/env python3
"""
IMPORT_ASSETS — sort the browser downloads into the AI folder, then measure everything.

Chrome drops everything into ~/Downloads. This moves each file to the right place, converts
mp3 → wav where useful, unzips the Nev reference set, and writes a measured index so the
Sound Engineer seat has real numbers instead of filenames.

Naming produced by the download step:
  SFX_<category>_<id>.mp3   ->  assets/sfx/<category>/
  BGM_<Name>.mp3            ->  assets/bgm/mixkit/
  drive-download*.zip       ->  assets/nev/           (unzipped)

SAFETY CONTRACT
  · ONLY touches files whose names match SFX_* / BGM_* / BROLL_* / *drive*.zip
    Your own footage in Downloads is INVISIBLE to this script unless you named it that way.
  · NEVER overwrites. If a destination file exists, it writes name_1.ext, name_2.ext ...
  · Only ever MOVES INTO assets/. It never writes to work/, output/, or anywhere you keep source.
  · --dry-run shows exactly what would move, and touches nothing.

Usage:
  python3 tools/import_assets.py --dry-run              # ALWAYS run this first
  python3 tools/import_assets.py                       # auto-detect ~/Downloads
  python3 tools/import_assets.py --src "C:/Users/User/Downloads"
  python3 tools/import_assets.py --measure-only        # re-index what's already imported
"""
import argparse, json, os, re, shutil, subprocess, sys, zipfile, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True)

def safe_move(src, dst):
    """NEVER overwrite. If dst exists, append _1, _2 ... Returns the path actually written."""
    if not os.path.exists(dst):
        shutil.move(src, dst); return dst
    base, ext = os.path.splitext(dst); i = 1
    while os.path.exists(f"{base}_{i}{ext}"): i += 1
    shutil.move(src, f"{base}_{i}{ext}"); return f"{base}_{i}{ext}"

def default_downloads():
    for p in [os.path.expanduser("~/Downloads"), os.path.expanduser("~/downloads"),
              "C:/Users/User/Downloads"]:
        if os.path.isdir(p): return p
    return None

def measure(path):
    """duration + integrated LUFS + rough BPM for beds."""
    d = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{path}"').stdout.strip()
    try: dur = round(float(d.splitlines()[0]), 2)
    except Exception: dur = None
    out = sh(f'ffmpeg -hide_banner -nostats -i "{path}" -af ebur128 -f null - 2>&1').stdout
    m = re.findall(r"I:\s*(-?\d+\.?\d*)\s*LUFS", out)
    lufs = float(m[-1]) if m else None
    return dur, lufs

def bpm_of(path):
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import rhythm
        x = rhythm.pcm(path)
        if x.size == 0: return None
        flux, hop = rhythm.stft_flux(x)
        b, _ = rhythm.estimate_tempo(flux, hop, onsets=rhythm.pick_onsets(flux, hop))
        return b
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src"); ap.add_argument("--measure-only", action="store_true")
    ap.add_argument("--to-wav", action="store_true", help="also convert SFX mp3 -> wav")
    ap.add_argument("--dry-run", action="store_true", help="show what WOULD move, touch nothing")
    a = ap.parse_args()

    moved = {"sfx": 0, "bgm": 0, "nev": 0, "broll": 0, "skipped": 0}

    if not a.measure_only:
        src = a.src or default_downloads()
        if not src or not os.path.isdir(src):
            print("!! could not find Downloads. Pass --src <path>"); return
        print(f"scanning {src}")

        if a.dry_run:
            print("DRY RUN — nothing will be moved\n")
        for f in sorted(os.listdir(src)):
            p = os.path.join(src, f)
            if not os.path.isfile(p): continue

            m = re.match(r"SFX_([a-z]+)_(\d+)\.mp3$", f, re.I)
            if m:
                d = os.path.join(ASSETS, "sfx", m.group(1).lower())
                os.makedirs(d, exist_ok=True)
                (print(f"  would move {f} -> {os.path.relpath(d, ROOT)}/") if a.dry_run
                 else safe_move(p, os.path.join(d, f))); moved["sfx"] = moved.get("sfx",0)+1; continue

            if f.startswith("BROLL_") and f.lower().endswith((".mp4",".mov")):
                cat = f.split("_")[1] if "_" in f else "misc"
                d = os.path.join(ASSETS, "broll", cat); os.makedirs(d, exist_ok=True)
                (print(f"  would move {f} -> {os.path.relpath(d, ROOT)}/") if a.dry_run
                 else safe_move(p, os.path.join(d, f))); moved["broll"] = moved.get("broll",0)+1; continue

            if f.startswith("BGM_") and f.lower().endswith((".mp3", ".wav")):
                d = os.path.join(ASSETS, "bgm", "mixkit"); os.makedirs(d, exist_ok=True)
                (print(f"  would move {f} -> {os.path.relpath(d, ROOT)}/") if a.dry_run
                 else safe_move(p, os.path.join(d, f))); moved["bgm"] = moved.get("bgm",0)+1; continue

            if f.lower().endswith(".zip") and ("drive" in f.lower() or "nev" in f.lower()) and not a.dry_run:
                d = os.path.join(ASSETS, "nev"); os.makedirs(d, exist_ok=True)
                try:
                    with zipfile.ZipFile(p) as z:
                        for member in z.namelist():
                            if member.endswith("/"): continue
                            target = os.path.join(d, os.path.basename(member))
                            if os.path.exists(target):
                                b_, e_ = os.path.splitext(target); k = 1
                                while os.path.exists(f"{b_}_{k}{e_}"): k += 1
                                target = f"{b_}_{k}{e_}"
                            with z.open(member) as srcf, open(target, "wb") as dstf:
                                shutil.copyfileobj(srcf, dstf)
                    n = len([x for x in z.namelist() if not x.endswith("/")])
                    moved["nev"] += n
                    os.remove(p)
                    print(f"  unzipped {n} Nev reference images")
                except Exception as e:
                    print("  !! zip failed:", str(e)[:80]); moved["skipped"] += 1
                continue

        print(f"moved -> sfx {moved['sfx']} · bgm {moved['bgm']} · broll {moved.get('broll',0)} "
              f"· nev images {moved['nev']}")

    if a.to_wav:
        for p in glob.glob(os.path.join(ASSETS, "sfx", "*", "*.mp3")):
            w = p[:-4] + ".wav"
            if not os.path.exists(w):
                sh(f'ffmpeg -y -v error -i "{p}" -ar 48000 -ac 1 "{w}"')
        print("converted sfx mp3 -> wav")

    # ---- measure + index ----
    index = {"sfx": [], "bgm": [], "broll": [], "nev_images": 0}
    for p in sorted(glob.glob(os.path.join(ASSETS, "sfx", "*", "*.*"))):
        if not p.lower().endswith((".mp3", ".wav")): continue
        dur, lufs = measure(p)
        index["sfx"].append({"file": os.path.relpath(p, ROOT),
                             "cat": os.path.basename(os.path.dirname(p)),
                             "dur": dur, "lufs": lufs})
    for p in sorted(glob.glob(os.path.join(ASSETS, "bgm", "*", "*.*"))):
        if not p.lower().endswith((".mp3", ".wav")): continue
        dur, lufs = measure(p); bpm = bpm_of(p)
        index["bgm"].append({"file": os.path.relpath(p, ROOT), "dur": dur,
                             "lufs": lufs, "bpm": bpm})
    for p in sorted(glob.glob(os.path.join(ASSETS, "broll", "*", "*.mp4"))):
        d = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"').stdout.strip()
        try: dd = round(float(d.splitlines()[0]),2)
        except Exception: dd = None
        index["broll"].append({"file": os.path.relpath(p, ROOT),
                               "cat": os.path.basename(os.path.dirname(p)), "dur": dd})

    nev = os.path.join(ASSETS, "nev")
    if os.path.isdir(nev):
        index["nev_images"] = sum(1 for _, _, fs in os.walk(nev)
                                  for f in fs if f.lower().endswith((".jpg",".jpeg",".png",".webp")))

    json.dump(index, open(os.path.join(ASSETS, "asset-index.json"), "w"), indent=1)
    print(f"\nINDEX: {len(index['sfx'])} sfx · {len(index['bgm'])} bgm · "
          f"{len(index['broll'])} b-roll · {index['nev_images']} Nev images "
          f"-> assets/asset-index.json")
    if index["bgm"]:
        print("\nBGM with detected tempo (feed these to rhythm.py as --bed):")
        for b in index["bgm"][:12]:
            print(f"  {os.path.basename(b['file']):<38} {str(b['dur']):>6}s  "
                  f"{str(b['lufs']):>6} LUFS  {str(b['bpm']):>6} bpm")

if __name__ == "__main__":
    main()
