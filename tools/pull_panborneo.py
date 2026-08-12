#!/usr/bin/env python3
"""Fetch the 13 panborneo artefacts (13 clips; plates optional) onto disk.

Run ON HIS WINDOWS BOX - the Cowork sandbox is blocked from the Higgsfield CDN
(403), which is exactly why this file exists (same division as pull_mahua.py:
a remote session plans and generates; he builds).

    python tools\pull_panborneo.py            clips -> projects/panborneo/clips/
    python tools\pull_panborneo.py --plates   also fetch the 4 plates
"""
import os, sys, urllib.request

BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/"
CLIPS = {
 "G": "hf_20260812_013352_6ea04155-c2eb-4bd0-a5fd-be012eefeab6.mp4",
 "B": "hf_20260812_013945_a0ea9c0e-03c5-4ba2-9c22-07431803ac88.mp4",
 "C": "hf_20260812_013944_2ff0e9b5-29cc-4966-90e5-e26610710094.mp4",
 "A": "hf_20260812_013944_bae2cbc1-8efb-4c36-9d52-86f842c6a8a6.mp4",
 "D": "hf_20260812_013944_fc725a80-05cb-447c-b3c4-81235209be76.mp4",
 "F": "hf_20260812_013945_565611be-cec7-4968-8c69-9c8c33a6db47.mp4",
 "E": "hf_20260812_013944_52cf20ff-d1c5-4242-8adf-a02e41cdc00a.mp4",
 "I": "hf_20260812_014031_b0463077-a1b0-4f0b-9275-d42de489fa4c.mp4",
 "H": "hf_20260812_014031_bc8b6f76-a54e-4a17-8d4e-6d12a725bb8c.mp4",
 "J": "hf_20260812_014031_a0a80cfc-0870-44d2-87dd-83884d2a5e6c.mp4",
 "K": "hf_20260812_014031_3427b1bb-c182-4362-a988-38e9e38c41b4.mp4",
 "L": "hf_20260812_014031_39f52888-1814-4784-9fe5-6f5f2bb66b0c.mp4",
 "M": "hf_20260812_014031_6008c272-94b4-46af-97f1-e1c6befa2587.mp4",
}
PLATES = {
 "defender": "hf_20260811_132543_ac20b2f6-e69a-4d99-9d7e-0427bfc78b45.png",
 "klias":    "hf_20260811_132543_fb748a80-7151-4469-befc-20ccc8d42a8e.png",
 "tusan":    "hf_20260811_132543_8926debd-3b50-46f0-8c13-cc52f2b56d14.png",
 "kuching":  "hf_20260811_132543_038e32ad-8c9b-4cfe-82c5-6289df3678a4.png",
}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fetch(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        print("  have", os.path.basename(dst)); return
    print("  <-", os.path.basename(dst), flush=True)
    tmp = dst + ".part"
    urllib.request.urlretrieve(url, tmp)
    os.replace(tmp, dst)          # atomic - a killed run never leaves a stub

def main():
    cdir = os.path.join(ROOT, "projects", "panborneo", "clips")
    os.makedirs(cdir, exist_ok=True)
    for k, f in CLIPS.items():
        fetch(BASE + f, os.path.join(cdir, f"panborneo_{k}.mp4"))
    if "--plates" in sys.argv:
        pdir = os.path.join(ROOT, "projects", "panborneo", "plates")
        os.makedirs(pdir, exist_ok=True)
        for k, f in PLATES.items():
            fetch(BASE + f, os.path.join(pdir, f"{k}.png"))
    print("DONE. Next: python talyx.py ingest panborneo")

if __name__ == "__main__":
    main()
