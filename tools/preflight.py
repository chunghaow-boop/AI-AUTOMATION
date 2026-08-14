#!/usr/bin/env python3
"""PREFLIGHT — one command, tells you exactly what will and won't work right now."""
import os, sys, subprocess, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = lambda b: "OK " if b else "-- "
print("TALYX PREFLIGHT\n" + "="*46)
# whisper
wdir = os.path.join(ROOT, "models", "faster-whisper-base")
has_w = os.path.exists(os.path.join(wdir, "model.bin"))
try:
    import faster_whisper; pkg = True
except Exception: pkg = False
print(f"{ok(pkg and has_w)} Whisper       pkg={'y' if pkg else 'n'} weights={'local' if has_w else 'MISSING'}")
if pkg and not has_w:
    print("     -> see models/PUT-WHISPER-FILES-HERE.txt (4 files, one drag)")
# playwright
try:
    import playwright; pw = True
except Exception: pw = False
print(f"{ok(pw)} Playwright    {'ready' if pw else 'unavailable -> cards use ffmpeg fallback'}")
# binaries
for b in ("ffmpeg", "ffprobe"):
    print(f"{ok(subprocess.run(['which',b],capture_output=True).returncode==0)} {b}")
try:
    import cv2, numpy; print(f"{ok(True)} cv2 + numpy")
except Exception: print(f"{ok(False)} cv2 + numpy")
# assets
sfx = len(glob.glob(os.path.join(ROOT,"assets","sfx","*","*.*")))
bgm = len(glob.glob(os.path.join(ROOT,"assets","bgm","*","*.*")))
bro = len(glob.glob(os.path.join(ROOT,"assets","broll","*","*.*")))
nev = len(glob.glob(os.path.join(ROOT,"assets","nev","**","*.*"), recursive=True))
print(f"{ok(sfx>0)} SFX {sfx} · BGM {bgm} · B-roll {bro} · Nev refs {nev}")
# tools
bad = [os.path.basename(f) for f in glob.glob(os.path.join(ROOT,"tools","*.py"))
       if subprocess.run([sys.executable,"-c",f"import ast;ast.parse(open(r'{f}').read())"],
                         capture_output=True).returncode != 0]
print(f"{ok(not bad)} tools {len(glob.glob(os.path.join(ROOT,'tools','*.py')))} files"
      + (f"  BROKEN: {bad}" if bad else ""))
print("="*46)
print("EXAM READY" if (sfx>0 and not bad) else "NOT READY")
if not has_w: print("(degraded: caption timing via silence-map, not word-exact)")
