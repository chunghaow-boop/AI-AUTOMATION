---
name: "talyx-cinematic"
description: "Cut a Talyx car-cinematic edit to the measured pillar profile. Use whenever planning, generating for, assembling or re-cutting short-form music-led car footage (car_cinematic or travel_vlog) — it enforces EDIT PLAN BEFORE GENERATION, max-quality reference plates, music-first beat-grid cutting via editsense, burst/rest patterning, shot-matching, and a reverse.py DNA diff before delivery. Trigger on \"cut this\", \"edit the clips\", \"build the cinematic\", \"make it cut to beat\", or any car edit assembly or shot-planning."
---

# TALYX CINEMATIC — the edit, not the render

## RULE ZERO — PLAN THE EDIT BEFORE YOU GENERATE ANYTHING

**The edit plan comes first. Generation fills its slots. Never the reverse.**

Measured cost of getting it backwards: 4 clips generated from a content brief, then asked
what edit they could support. **7 of 13 cuts had histogram correlation > 0.95.** The timing
was correct and the video still failed, because **cut rate must be earned by coverage.**

```
1 PILLAR + duration   2 MUSIC (BPM *and PHASE*)   3 BEAT GRID
4 SLOT TABLE          5 COVERAGE CHECK            6 GENERATE  <- credits
7 ASSEMBLE            8 PROVE
```
Steps 1–5 are free. **Draw the plan as an image** (`make_storyboard.py`) — it caught a source
carrying 4 of 14 shots, and a lighting arc that jumped instead of progressing.

```
distinct sources >= shots / 2.5        punch-ins <= 1.4x   (see QUALITY)
```
14 shots needs 6 sources; 26 shots needs 11. A 30s cinematic needs roughly double a 16s one.

---

## QUALITY FIRST — HIS STANDING RULE

> *"all the reference images needed for image-to-video generations, make sure it's
> highest quality and most realistic"*

**REFERENCE PLATES: ALWAYS `resolution: "4k"`.** `nano_banana_pro` defaults to **1k** and
every early plate was built at that default without anyone noticing. 4k costs **4 cr vs 2 cr**
— two credits, against a 150–200 cr build that inherits the plate's quality on every shot.

**Write the plate prompt as a PHOTOGRAPH, not a description.** Name the camera, lens,
aperture, ISO and lighting setup. Then ask explicitly for the artefacts that only real photos
have, because their absence is what reads as AI:

```
true specular highlights that roll along a crease, not painted-on glints
clear-coat orange peel, faint panel-gap shadows
fine dust and micro-scratches catching the key light
accurate softbox reflection in the glass
far wheel slightly softer than the near one
neutral white balance, no HDR halos, no oversaturation
negative: CGI, videogame look, plastic-smooth surfaces
```

**VIDEO: `mode: "std"`, not `fast`.** Higgsfield's own text — *"'std' = higher quality;
'fast' = cheaper/faster."* std is 22.5 cr/5s vs 17.5. On a 9-clip build realism costs **+45 cr**.
Never choose `fast` silently to save the user money; say what the tradeoff buys.

**PUNCH-INS DESTROY RESOLUTION. Cap at 1.4x.** Measured on 720p source:

```
source clip        sharpness 234
1.00x segment                228
1.90x punch                   42     -82%
1.95x punch                   36     -85%
```
A 1.95x crop on 720p is **369x656 upscaled to 720x1280**. That mush IS the "AI look".
When punch-ins stop reading as new shots, the answer is **more coverage, not deeper crops** —
raising them from 1.3x to 1.9x fixed a repetition metric and wrecked the picture.

**GRADE GENTLY.** Saturation was pushed to 1.70 chasing the profile's `saturation 91.5`,
taking source 44.6 to 91.7. That target was measured from *finished, compressed reference
exports*, not raw generations — matching a downstream number with a blunt `eq` is not grading
to it. Start at ~1.15 and measure toward the target.

---

## THE GATES DO NOT CHECK WHAT YOU THINK

`PILLAR-PROFILES.json` stores **16 measured fields**; `qc.py profile` originally read **two**.
`black_point`, `saturation`, `sub_bass_pct`, `blend_width_ms`, `shot_mix` and `lighting` were
measured from 23 references and **never checked by any gate**. A build shipped with 40% of
every frame crushed black and qc.py printed *"matches the reference profile."*

`mastermind.score` is a **frame-quality** inspector, not an **edit** inspector:

| it asks | it never asks |
|---|---|
| is this frame blank / soft / dark? | do adjacent shots match exposure? |
| is the file too loud / clipping? | does this cut deliver a new image? |
| are captions synced to speech? | is the grade near the pillar's black point? |
| | **has a punch-in destroyed the resolution?** |

`"exposure floor" · brightness_min >= 18` is one number for the whole file and is **weighted,
not blocking**. It cannot see a shot-to-shot swing.

**Every defect found by eye has been RELATIONAL.** When adding a check, ask whether it inspects
a frame or a *relationship between shots*. Run `verify.py` — 10 checks, one verdict.

---

## THE MEASURED TARGETS

| | car_cinematic (n=5) | travel_vlog (n=6) |
|---|---|---|
| median shot | **0.77s** | **1.13s** |
| cuts/min | 44.7 | 40.3 |
| blended | **20%** (range 6–33) | **0%** |
| blend width | 240–560ms | — |
| BPM | 140–170 drift phonk | 83–176 |
| sub-bass | **60–92%** | — |
| black point / saturation | **2.0 / 91.5** | 10.0 / 74.5 |

Read the JSON at run time. **Two families**: short/music-led cuts to the beat, long/speech-led
cuts to the sentence. A 30s "review" is cinematic grammar whatever it's called.

---

## THE SEQUENCE

### 1 · MUSIC FIRST — PHASE, NOT JUST TEMPO
```
phonk.py --bpm 150 --dur 30     (--out is a DIRECTORY; it names the file itself)
rhythm.py BED.wav               BPM + grid + OFFSET
```
A generated bed put its first transient at **163ms** — no downbeat at t=0. Trimming the bed so
hit 1 lands on t=0 took cut-to-music from ~34ms to a **median 2.5ms**.

> A *constant* deviation is a phase error, not sloppiness. `editsense.beat_grid()` takes
> `offset` — pass it.

### 2 · PERCEPTION
`clipsense.py` — `best_in_s` is where the shot starts MOVING; AI clips open with a settle.
**Reframe in space, not time.**

### 3 · BURST / REST
```
BURST 4-6 cuts at 2 beats  ->  HOLD 8 beats  ->  BURST  ->  HOLD  ->  BURST
```
`hold=5` gave 60 cuts/min vs 44.7 target; **`hold=8` gives 48.7**. Flat lengths measure
`rate_variation ≈ 0` — one build scored **0.01**, a perfect metronome.

**Highest-motion clip on the HOLD** — a 3.2s hold on a motion-7.0 clip is dead air.
**Highest-motion clip on shot 0** — one build opened on its quietest shot.

### 4 · CUT ON ACTION — `action_peaks_s`
clipsense returns *"the moments a pro cuts on or into"* and nothing had ever read it. Anchoring
near `best_in` never reached past ~1.3s of a 5.04s clip, throwing away every peak from 2–4.5s.
Shots 0/1/9 contained **no peak at all** — and shot 0 is the hook. Centre each shot on its
nearest unused peak.

### 5 · SHOT MATCH — BEFORE the blends
Measure the **rendered segment**, never the source clip. A 1.4x punch crops into the dark part
of frame, so source averages lie. Reordering by source brightness left 5 of 13 cuts swinging
>18; matching on rendered levels took it to **0 of 12**. Clamp to ±0.085 — match, never relight.

### 6 · FRAME-EXACT CUTS
`-t 0.80` on a 24fps source yields **0.834s** at 30fps — an extra frame per shot, accumulating
to ~130ms (a third of a beat) by 15s. Use **`-frames:v round(d*FPS)`**.

**Record ACTUAL post-blend boundaries, not planned ones.** Blending merges pairs, so 13 planned
became 9 actual; verifying against the plan compared two frames *inside the same shot*.

### 7 · TRANSITIONS
Most cuts HARD (33–67ms). Blends rare, wide (240–560ms), as section punctuation.
- **`dip` fades through BLACK** — trips the blank-frame gate legitimately.
- **`whip`** — `_xfade` injects `pre_a`/`pre_b` as `[0:v]`, applying to the WHOLE clip. Must be
  time-gated with `enable='between(t,..)'`.
- A blend between two near-identical images is **invisible** — it reads as a glitch line.

### 8 · GRADE — NEVER DOUBLE-GRADE
If the generation prompt asked for a look, the footage **arrives** with it. Prompts said
"crushed blacks, high contrast"; applying `contrast=1.16, brightness=-0.035` on top took pixels
at value <4 from 7.7% to **40.0%**. `black_point 2.0` is where the darkest pixel should SIT —
a target to measure toward, not a filter to apply.

### 9 · SOUND
Sub-bass 60–92%. **Foley on cuts** — one build mixed SFX **15.2 dB under the bed**, fully
masked, while printing "9 whoosh + 4 impact". Whooshes **lead** the cut by ~220ms (a whoosh
*resolves* on the cut); the bed **sidechain-ducks** under them. **Don't trust single-pass
`loudnorm`** — it undershot twice. `alimiter` needs **`level=disabled`**.

### 10 · PROVE IT
`reverse.py ... --mine-cuts plan.json` — **always** pass declared cuts. The detector found
**2 of 7** cuts in one file and **0 of 13** in another. It measures the *references* with the
same blind detector, so trust PILLAR-PROFILES over the DNA table.

**Adjacent-shot check: HISTOGRAM CORRELATION, not pixel difference.** A punch-in moves every
pixel while showing nothing new — mean |diff| flagged 0 of 13, hist-corr flagged 7. Same trap
as ledger E3.

**Known false positive:** `blank_frames` counts Laplacian sharpness < 8 — that is BLUR, not
black. Check `mean ≈ 0` first. `mastermind.video_metrics` samples ~6fps, under-counts ~4x.

---

## HARD RULES

1. **Evidence before claims.** Every audio/pacing claim cites a measurement.
2. **Preflight `get_cost` with the LITERAL params.** `std` defaults to 4.5cr/s; `fast` is 3.5.
3. **A named subject is never generated from text alone.** 4k plate first, LOOK at it.
   `seedance_2_0` takes `image_references` **plural** — one shot carries persona AND product.
4. **A fallback that still produces a file must SHOUT.**
5. **Write output atomically** (`.part.mp4` then `os.replace`) — a killed run left a 532KB mp4
   with no moov atom.
6. **Cache keys include the full treatment spec**, not just duration.
7. **After any fix, re-run the check.**
8. **5 failures on one problem → stop and ask.**
9. **Frames and spectrograms ARE the work.** View them.
10. **Say "measured" only about measurements.** Declare structural choices as choices.
11. **No burned-in AI label** — use the platform's AI toggle at upload. It is a human step now,
    so it must be stated on every delivery.

## THE STANDING GAP
Zero posts. Every retention figure is a hypothesis until one real 24-hour curve exists.

