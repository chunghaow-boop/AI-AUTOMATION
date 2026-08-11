#!/usr/bin/env python3
"""Fetch the PAID artefacts for plans/mahua.py onto this machine.

Written 2026-08-07 because the remote Cowork sandbox is BLOCKED from the Higgsfield
CDN (curl returns `CONNECT tunnel failed, response 403`), so the session that paid the
214.50cr could not put the files on disk itself. The URLs are recorded in the plan
(CLIP_BASE + CLIP_JOBS + PLATE_JOBS), which is exactly what CLIP_BASE exists for.

    python tools\\pull_mahua.py

Then, on this machine:

    python talyx.py ingest mahua      clipqc, 13 checks per clip
    python tools\\ingest.py mahua      the manifest the engine reads
    python talyx.py build mahua       the cut
    python talyx.py verify mahua      15 checks, freshness first

KEEP THE RAWS. travel_vlog's motion_floor and brightness_band are still PROVISIONAL
and every kk_*.mp4 was deleted before they could be re-derived. These nine are the
replacement measurement.
"""
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

import plans.mahua as P  # noqa: E402

CLIPS = os.path.join(HERE, "projects", "mahua", "clips")
PLATES = os.path.join(HERE, "projects", "mahua", "plates")


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        print(f"  have  {os.path.basename(dest)}")
        return True
    try:
        with urllib.request.urlopen(url, timeout=120) as r, open(dest, "wb") as f:
            f.write(r.read())
    except Exception as e:
        print(f"  FAIL  {os.path.basename(dest)}  {str(e)[:60]}")
        return False
    print(f"  got   {os.path.basename(dest)}  {os.path.getsize(dest)/1e6:.1f} MB")
    return True


def main():
    os.makedirs(CLIPS, exist_ok=True)
    os.makedirs(PLATES, exist_ok=True)
    ok = True

    print("PLATES  (4k reference images — LOOK at glc300 before trusting any clip)")
    for name, fn in P.PLATE_JOBS.items():
        ok &= fetch(P.CLIP_BASE + fn, os.path.join(PLATES, name + ".png"))

    print("\nCLIPS  (the 202.5cr — keep every one of them)")
    for key, fn in P.CLIP_JOBS.items():
        ok &= fetch(P.CLIP_BASE + fn, os.path.join(CLIPS, P.CLIPS[key]))

    print("\n" + "=" * 70)
    if ok:
        print("  ALL ARTEFACTS ON DISK.  Next:")
        print("    python talyx.py ingest mahua      clipqc, 13 checks per clip")
        print("    python tools\\ingest.py mahua      the manifest the engine reads")
        print("    python talyx.py build mahua       the cut")
        print("    python talyx.py verify mahua      15 checks, freshness first")
    else:
        print("  SOMETHING DID NOT ARRIVE. The URLs expire; re-run soon, and if a clip")
        print("  is gone for good it is 22.5cr to regenerate from the plan's prompt.")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
