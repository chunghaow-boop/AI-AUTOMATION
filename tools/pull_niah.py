#!/usr/bin/env python3
"""Fetch every generated niah asset to disk ON HIS BOX (the container cannot
reach the hf CDN - measured session 11, curl 56, same class as YouTube 403).

Usage:  python tools\\pull_niah.py
Writes: projects/niah/clips/niah_<SRC>.mp4 + assets/pillars/travel_vlog/plates/
        niah_*.png, from projects/niah/JOBS.json (written at generation time).
After pulling: re-run  python tools\\storyboard.py niah  - the red panels
upgrade to plates and real frames (L141)."""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = os.path.join(HERE, "projects", "niah", "JOBS.json")
jobs = json.load(open(J))
os.makedirs(os.path.join(HERE, "projects", "niah", "clips"), exist_ok=True)
plate_dir = os.path.join(HERE, "assets", "pillars", "travel_vlog", "plates")
os.makedirs(plate_dir, exist_ok=True)

for k, v in jobs.items():
    url = v.get("url")
    if not url:
        print(f"  {k}: NO URL RECORDED - fetch from Higgsfield UI, job {v.get('job_id')}")
        continue
    if v["kind"] == "plate":
        out = os.path.join(plate_dir, f"{k}.png")
    else:
        out = os.path.join(HERE, "projects", "niah", "clips", f"niah_{k}.mp4")
    if os.path.exists(out):
        print(f"  {k}: exists, skip"); continue
    print(f"  {k} -> {out}")
    urllib.request.urlretrieve(url, out)
print("done. Now: python tools\\storyboard.py niah")
