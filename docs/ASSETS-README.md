# ASSETS — what's here and how it got here

## THE LIBRARY
```
assets/
├── sfx/
│   ├── <synthesised>        74 files · tools/sfxgen.py · zero licence risk
│   └── <mixkit categories>  ~249 real recordings · Mixkit Free License
├── bgm/
│   ├── utility-beds/        5 BPM grids (90/100/120/128 + drone) — for cut-to-beat testing
│   └── mixkit/              ~127 real tracks across 14 genres
├── nev/                     50 × 360° reference photos + closeup face set
├── cards/                   rendered PNG cards (tools/cards.py output)
├── SFX-INDEX.md             beat-type → which sound (the cheat sheet)
└── asset-index.json         measured duration/LUFS/BPM for every file
```

## AFTER THE DOWNLOADS FINISH — one command sorts everything
```bash
python3 tools/import_assets.py
```
It moves `SFX_*` and `BGM_*` from Downloads into the right folders, unzips the Nev set,
then measures duration + LUFS for every file and BPM for every bed → `asset-index.json`.
Add `--to-wav` if you want wav copies of the SFX for frame-accurate editing.

## LICENCE — know what you're shipping
| Source | Terms |
|---|---|
| **Synthesised** (`tools/sfxgen.py`) | 100% original output. No attribution, no restrictions. Safest for monetised content. |
| **Mixkit Free** | free for commercial use, no attribution required, **but** you may not redistribute the files themselves or use them in a product where the audio IS the product. Fine for video content. Verify current terms at mixkit.co/license before a paid campaign. |

## NEV REFERENCE SET — the identity lock
50 photos: front · left profile · right profile · back · three-quarter, across several wardrobe
states, plus a `closeup face` subfolder. **This replaces the generated character sheet** — real
reference beats synthetic every time.

Use as `start_image` / `image_references` on every generation. Pick the angle that matches the
shot you're generating. Verify consistency after with `tools/facecheck.py`.

> ⚠️ These are photographs of a real person. Generating video of a real identity requires their
> consent, and AI content must be disclosed on TikTok/Meta — both already in `GATE.md` stage 1.

---

## B-ROLL — licensed stock, usable in videos AND as tool test material
```
assets/broll/{car,driving,highway,road,street,sunset,city-night,traffic,workshop}/
41 clips · 1080p/720p · Mixkit Free License · no watermark
```
**Two jobs:** real B-roll for the `[AI]` shots you'd otherwise pay ~67cr to generate, and real
footage for `reverse.py` / `grade.py` / `transitions.py` to be tested against.

**Every one of these replaces a generation.** A highway shot you drop in free is 67cr you keep.

---

## ⚠️ ON REFERENCE VIDEOS — what I will and won't do

You offered browser access to fetch reference videos. Two things I won't do, stated plainly:

**I won't rip videos from TikTok / YouTube / Douyin** via downloader sites. It breaches those
platforms' terms and the content is copyrighted. Measuring someone's edit for private study is
defensible; downloading their file to do it is not the way to get there.

**The clean paths to the same data:**

| Path | Gets you | Cost |
|---|---|---|
| **Higgsfield `video_analysis_create`** | scene-by-scene breakdown from a **YouTube URL directly** — sanctioned API, no download | small |
| **Your own screen recording** | if you can watch it, you can record your screen. Your recording, your file. | free |
| **`assets/broll/`** (done) | licensed footage for tool calibration | free |
| **Your own phone footage** | the real grade anchor — nothing substitutes for it | free |

**What still can't be substituted:** your phone's colour profile. `grade.py` needs one raw clip
off your actual camera to build the look every AI shot gets matched to. Until then the hybrid
seam stays the weakest point in the pipeline.

### MEASURED PROOF THAT THIS MATTERS
Ran `grade.py compare` on your own two AI clips — same model, same session, same prompt family:
```
colour distance 12.77   ->  ">10 = obvious mismatch, this is the AI tell"
```
They don't even match each other. `INFLUENCER_v1.mp4` carries that mismatch right now.
Fix: `python3 tools/grade.py match part2.mp4 --ref part1.mp4 -o part2_graded.mp4`
