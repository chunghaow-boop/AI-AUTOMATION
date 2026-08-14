"""pull_desafarm.py - fetch the 14 delivered desafarm clips to projects/desafarm/clips/

WHY THIS EXISTS: generation and assembly are on SEPARATE MACHINES. The chat session
that buys the clips runs in a sandbox that is 403-blocked from the Higgsfield CDN, so
it can measure clips only through Higgsfield's own sandbox and can never write them to
your disk. This script is the bridge. Run it on the Windows box, then build.

    python tools\\pull_desafarm.py
    python talyx.py build desafarm
    python tools\\contact.py desafarm --raw          (contact sheet BEFORE assembly)
    python tools\\syncqc.py desafarm                 (plan<->cut join, 5 checks)
    python verify.py desafarm

EVERY URL BELOW IS A CLIP THAT WAS PAID FOR AND MEASURED ON 2026-08-07. Three of them
are re-shoots and the superseded takes are listed at the bottom so the record is
honest - do not delete them from this file, they are the evidence for lessons 99-101.
"""
import os
import sys
import urllib.request

BASE = ("https://d8j0ntlcm91z4.cloudfront.net/"
        "user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/")

# key -> (filename on the CDN, mean luma measured 2026-08-07, black% measured)
CLIPS = {
    "A": ("hf_20260807_081208_f93e41dc-8cb2-49d7-b69b-2b0f6b8b8cf3.mp4", 107.1, 2.8),
    "B": ("hf_20260807_083119_9b52f8b5-68b2-4f53-ba86-5c4caf5f8778.mp4",  93.5, 9.2),
    "C": ("hf_20260807_084437_c3e58748-390a-425a-bc80-0f4241ba5c8f.mp4",  95.1, 4.1),
    "D": ("hf_20260807_083119_bec7b58b-596a-4102-8cfd-4c94d90e10d1.mp4",  91.6, 3.3),
    "E": ("hf_20260807_083118_25f4cd1d-1992-466f-8e2e-073edb62f387.mp4", 104.7, 7.3),
    "F": ("hf_20260807_083118_b68d235a-4721-4991-b18a-189201aa1f7c.mp4", 108.2, 6.6),
    "G": ("hf_20260807_083118_e8b81994-2360-456d-86ad-bbd89f8cb932.mp4",  93.3, 10.2),
    "H": ("hf_20260807_083118_29ec644d-ac7b-4da9-be3a-567e4fbfa0f2.mp4", 113.4, 2.0),
    "I": ("hf_20260807_083118_16d06e1e-64a7-4d0b-820e-5100d65fb49a.mp4",  93.1, 16.5),
    "J": ("hf_20260807_083118_6184e760-f50d-40c2-94bb-45bb24c8102b.mp4", 116.7, 0.2),
    "K": ("hf_20260807_083118_27d7961a-b224-4a14-922e-46cc7175af38.mp4", 121.6, 0.6),
    "L": ("hf_20260807_083140_98ebcc20-ba2a-474c-afd7-ccb4fa5f3b88.mp4", 100.1, 11.0),
    "M": ("hf_20260807_083118_3608f380-a511-4070-ac51-47c3fa72bb7b.mp4",  81.7, 7.4),
    "N": ("hf_20260807_083140_9335ccb0-99d0-4d74-bf57-fe8fc9e7ca9b.mp4", 116.8, 0.7),
}

# SUPERSEDED, kept as the record behind lessons 99, 100 and 101. Not downloaded.
#   A v1  8f6de91a-3191-4c94-af2d-46ce60554bbc  luma 102.7  - NO YANK: calm drink to
#         2.6s then the goat left. "Resolves inside one second" let the model write
#         the other four seconds.                                      (craft #99)
#   A v2  b9b46684-0ad4-461a-838c-953e77d79288  luma  65.3  - action FIXED, but 22.6%
#         crushed black. All struggle, no light spec.                  (craft #100)
#   C v1  60da09fa-2b98-4ed7-a4bb-f9fe3d4e2fb1  luma  37.7  - SILHOUETTE, 59.7% black.
#         Carried the new exposure clause and still failed: the clause never named
#         the metering target.                                         (craft #101)

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "projects", "desafarm", "clips")


def main():
    os.makedirs(DEST, exist_ok=True)
    bad = 0
    for key in sorted(CLIPS):
        name, luma, black = CLIPS[key]
        out = os.path.join(DEST, "desa_%s.mp4" % key)
        if os.path.exists(out) and os.path.getsize(out) > 100000:
            print("  have  %s  %s" % (key, os.path.basename(out)))
            continue
        print("  pull  %s  luma %5.1f  black %4.1f%%" % (key, luma, black), end=" ")
        sys.stdout.flush()
        try:
            urllib.request.urlretrieve(BASE + name, out)
            print("-> %.1f MB" % (os.path.getsize(out) / 1e6))
        except Exception as exc:
            bad += 1
            print("FAILED %s" % str(exc)[:60])
    if bad:
        print("\n!! %d clip(s) did not download. The CDN links are signed-free but the "
              "host can rate-limit; re-run this script, it skips what it already has."
              % bad)
        return 1
    lum = [v[1] for v in CLIPS.values()]
    print("\n  14/14 in projects/desafarm/clips/")
    print("  luma band %.1f - %.1f (spread %.1f). Craft #101: the outlier is only ever "
          "visible in THIS comparison, never against a fixed band."
          % (min(lum), max(lum), max(lum) - min(lum)))
    print("\n  next:  python talyx.py build desafarm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
