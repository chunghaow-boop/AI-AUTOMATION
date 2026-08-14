# ROUND 2 — THE TWO NIGHT CLIPS (download these next)

These fill the two 3.2s HOLD slots in `STORYBOARD-FLOW.png`. Save into this folder with
**exactly these names**, then say go.

| save as | link |
|---|---|
| `LC300_F_rolling.mp4` | https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/hf_20260731_084900_1783f400-8969-45b6-b75a-cb12640a3aa2.mp4 |
| `LC300_G_rear_night.mp4` | https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/hf_20260731_084904_5f0b9852-b1c4-4b62-ac0e-aee878cf396d.mp4 |

Then: `python3 build_lc300_cinematic.py`

---

# ROUND 1 — the original 4 clips (already downloaded)

Save each one into the same folder this file is in, with **exactly these names**.
`build_lc300.py` looks for these filenames and will refuse to run if they are missing.

| save as | link |
|---|---|
| `LC300_B_front.mp4` | https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/hf_20260731_050402_c5114ae0-a2c7-4307-9bd3-ad32051f0dec.mp4 |
| `LC300_C_wheel.mp4` | https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/hf_20260731_050405_585254f4-7612-43d3-bdd4-3522d4767c76.mp4 |
| `LC300_D_interior.mp4` | https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/hf_20260731_050414_e5385255-7274-44e9-9e7e-ffa9835cd78d.mp4 |
| `LC300_E_rear_screens.mp4` | https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/hf_20260731_050417_818f31db-b2ce-4c1f-9e96-87990dbd87d4.mp4 |

Reference plate (optional, but `verdict.py` uses it for the subject gate — save as `lc300zx.png`):

https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/hf_20260731_031810_09c2124c-467f-4f9c-9402-dda606f8af41.png

---

## THEN SAY "GO"

I run:

```
python3 build_lc300.py
```

which does: segments → 1 blend → concat → grade to the car_review numbers → `verdict.py`
→ `qc.py profile --pillar car_review`, and hands you the file **with the measurements**.

---

## WHY YOU HAVE TO DO THE DOWNLOADING

This sandbox has no outbound network — every fetch returns `000`, including Higgsfield's own
CDN. I can generate (MCP tools work) and I can edit (ffmpeg + the 41 tools are extracted here),
but I cannot move bytes between the two. Your browser is the bridge.

## WHAT THIS BUILD IS AND IS NOT

**Is:** a 30s car_review-grammar cut of the Land Cruiser 300 ZX — 8 shots from 4 generations,
median 3.75s, one blend, graded to saturation 52.9 / black point 8.0.

**Is not:** a review with Nev in it. No Nev plate exists and the upload path is blocked by the
same network wall. To add him, send a **single-file** Google Drive share link (not the folder)
— Higgsfield fetches server-side, and `seedance_2_0` takes `image_references` plural, so one
shot can carry Nev *and* the car.

**Unverified:** I have never seen the plate or these clips. Check shot B for three stacked LED
elements per headlamp and four horizontal grille slats. If it's a rounded crossover, that's the
Crown failure again and the fix is 2 cr, not 70.
