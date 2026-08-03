# CAR CINEMATIC — analysis of your 5 references
### Measured, not eyeballed. Every number is from the files you gave me.
### Snapshot dated 2026-07-30. References date — treat as calibration, not a standard.

---

## THE HEADLINE: we cut ~3× too slow and blend 0% of our cuts

| | your references (n=5) | our Crown | verdict |
|---|---|---|---|
| **median shot length** | **0.77s** (range 0.70–4.50) | 2.00s | **~3× too slow** |
| fastest shot | **0.28s** | 1.30s | we have no fast cuts at all |
| cuts/min | 44.7 (11.5–58.3) | 28.4 | too slow |
| **blended transitions** | **27%** (8–60%) | **0%** | every cut of ours is hard |
| shots ≤1.0s | **7–14 per video** | **0** | we never cut fast, once |

Shot-length distribution, which is the clearest single picture:

```
                              <=1.0s   1-2.5s   >2.5s   fastest
snaptik_7631962430926523668      14        0       2      0.70s
snaptik_7446071634366057760       7        5       1      0.73s
ssstik @azmiedtz03                7       10       0      0.37s
ssstik @d2_shots                 10        5       1      0.28s
snaptik_7541916507043925279       1        0       2      0.87s   <- the outlier
OUR CROWN                         0        7       1      1.30s
```

Four of five are built on sub-second shots. **We produced zero.**

---

## 1 · TRANSITIONS

**27% of their cuts are blended** — a masked/wiped/ramped transition rather than a straight
cut. Range 8% to 60%. Ours: **0%**, because `build_crown` had no transition column and the
library was broken anyway.

At ~45 cuts/min with 27% blended, that's roughly **one designed transition every 5 seconds**.

Visible in the frames: hard white/orange **flash frames** (light-leak wipes) in the azmiedtz
reference at two points, plus speed-ramped whips into detail shots.

**What our rebuilt `fx.py` now covers:** whip, speedramp, zoomblur, dolly_in/out,
mask_circle/crop/wipe/slice/radial, glitch, flash, dip — 13 verified working.

---

## 2 · VIDEO / GRADE

| | references | our Crown |
|---|---|---|
| black point | **2.0** /255 | 1.0 |
| saturation | **91.5** | 109.2 |
| resolution | 1080×1920 (2 of 5) | 720×1280 |
| frame rate | 30, one at **60** | 30 |

Both crush blacks similarly. **Ours is ~20% more saturated than theirs** — they're more
desaturated and colder, which reads as expensive; ours is punchier and cheaper-looking.

**The bigger difference is lighting, and it's not a grade fix.** Both strong references are
shot at **night with artificial light**:

- **azmiedtz** — underground carpark. Concrete pillars, hard overhead fluorescents, real
  architecture. The car sits in a *place*.
- **d2_shots** — near-black frames where **the car is the light source**: headlights blazing,
  taillights, a glowing brake disc, the instrument cluster, the tachometer needle.

Our Crown is **even blue dusk on an infinite reflective floor**. No environment, no hard
light, nothing emitting. That's a *prompt* failure, not a grading one.

---

## 3 · SHOT VOCABULARY

Counted across both strong references:

```
exterior wide / rolling      ~30%
wheel + brake detail         ~15%
headlight / taillight macro  ~15%
INTERIOR: gauges, cluster,
  hands on wheel, tacho      ~25%   <- we had ONE interior shot, buried
badge / logo                 ~10%
human presence                ~5%   <- a person walks through frame in d2_shots
```

**A quarter of their runtime is interior.** The tachometer needle sweeping through 3–4k is a
genre staple we didn't shoot at all.

---

## 4 · AUDIO — the finding that surprised me most

Spectral energy distribution:

| | sub (<150Hz) | body | presence | air |
|---|---|---|---|---|
| snaptik_7541916507043925279 | **92%** | 8% | 0% | 0% |
| snaptik_7446071634366057760 | **81%** | 18% | 1% | 0% |
| ssstik @d2_shots | **80%** | 14% | 2% | 0% |
| ssstik @azmiedtz03 | 60% | 34% | 5% | 0% |
| snaptik_7631962430926523668 | 61% | 34% | 4% | 1% |
| **our Crown** | **48%** | 31% | 13% | 4% |

**Their audio is 60–92% sub-bass. Ours is 48%.** Car-edit sound is far more bass-dominant
than anything I built.

This also invalidates a target I'd been applying: the "body ~45%, air ~4%" figures came from
your file 19 — measured off a **viral reel**, a different genre. I applied travel-vlog
spectral targets to a car edit. My phonk build measured sub 30%, body 42% — **still not
bass-heavy enough by a wide margin.**

*Caveat:* these came through snaptik/ssstik re-encoders, which may roll off highs. The 0% air
readings are suspect. The 60–92% sub figures are too consistent to be an artifact.

**Transient density** (proxy for SFX + percussion hits): references 158–357/min, median ~318.
Ours 373/min — we're comparable, so the *density* of events is fine. It's the *spectrum*
that's wrong.

**Loudness:** references −24.7 to −8.5 LUFS, median −14. Ours −9.7. Wide spread because
TikTok normalises on playback, so the upload level matters less than I'd assumed.

**Tempo:** 78–163 BPM, median 100. The two strongest references sit at **145.8 and 163.0** —
squarely drift-phonk. My 145 BPM phonk build is right on target.

---

## 5 · CAPTIONS — completely different from ours

The azmiedtz reference uses **lyric-synced captions**: single words or short fragments, very
large, centre-frame, in time with the song —

> YOU · SO PRE · TELL · I WISH THAT · LIE · BUT MY MIND · THINK · AWARE

Not sentences. Not narration. **The song's lyrics, one beat at a time.** Ours were VO-derived
sentence fragments placed low in frame. Different instrument entirely.

There's also a branded end/interstitial card — a logo on solid black.

---

## 6 · WHAT TO CHANGE, RANKED

| # | change | evidence |
|---|---|---|
| 1 | **shot length 2.0s → 0.7–0.8s** | their median is 0.77s; four of five are built on sub-second shots |
| 2 | **blend 25–30% of cuts** | theirs 27%; ours 0% |
| 3 | **shoot night + hard artificial light, car emitting** | both strong refs; ours is flat dusk in a void |
| 4 | **~25% interior** — gauges, tacho, hands | a whole shot class we skipped |
| 5 | **push sub to 60–80%** | ours 48%, phonk build 30% |
| 6 | **lyric-style captions, not sentences** | their captions are one word, huge, centre |
| 7 | desaturate ~20% | 91.5 vs our 109.2 |

---

### Written to `target_profile.json` alongside this. Expires 2026-09-28.
