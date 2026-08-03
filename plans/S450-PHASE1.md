# PHASE 1 — Mercedes-Benz S450 · car cinematic
### Free and autonomous. Stops at ONE gate.
### Built against MEASURED targets from your 5 car-cinematic references, not my assumptions.

---

## 0 · RESEARCH GATE — passed before planning

`qc.py phase0` requires ≥5 references studied. **22 lessons on file, last researched today.**
New research for this build:

- The S450's signature is **illumination**: the radiator grille lights up (enlarged 20% on
  W223) and the **hood star lights up**. Three LED light accents. Chrome twin louvres over
  gloss-black vertical bars.
- **This is the single luckiest fact about this brief.** Your references' strongest common
  trait is *the car emitting light* — headlights, taillights, glowing brakes, cluster. The
  S450 does that from the factory. We're not faking a look; we're shooting the actual car.
- It is an **executive limousine, not a sports car.** Weighty and expensive, not aggressive
  drift. Sources at the end.

---

## 1 · TARGET

| | |
|---|---|
| Avatar | **5 — Silent Businessman.** The S-Class is the definitional car for this avatar. |
| Pillar | **car_cinematic** |
| Language | none. **Zero VO.** No spoken claim = no factual risk. |
| Platform | TikTok primary |

---

## 2 · THE MEASURED TARGETS THIS BUILD MUST HIT

Straight from `PILLAR-PROFILES.json`, n=5:

| metric | target | our Crown scored |
|---|---|---|
| duration | 10–22s | 14.8 ✓ |
| **median shot** | **0.77s** | 2.00s ✗ 2.6× too slow |
| cuts/min | 44.7 | 28.4 ✗ |
| blended cuts | 20% (6–33) | 0% ✗ |
| blend width | 240–560ms | n/a |
| BPM | 140–165 | 90 ✗ |
| sub-bass | 60–92% | 48% ✗ |
| black point / sat | 2.0 / 91.5 | 1.0 / 109 (over-saturated) |

**Every one of those is a gate.** `qc.py profile` blocks the build if it misses.

---

## 3 · THE EDIT — 18 shots in 15.0s at 150 BPM

Beat = **0.400s**. Cut grammar taken from the frame-level study of your references:

> Most cuts are **HARD** (33–67ms). Blends are **rare and wide** (240–560ms), used as section
> punctuation. Cuts arrive in **bursts one beat apart, then hold.**

```
BURST A  0.0-2.4    6 shots x 0.40s   grille light-up, star, louvres, badge, DRL, air intake
HOLD     2.4-4.0    1 shot  x 1.60s   full car reveal, wide
BURST B  4.0-6.0    5 shots x 0.40s   wheel, brake, sill, door handle, mirror
BLEND    6.0-6.4    ---- 400ms blend ---- (section punctuation, 1 of 3)
HOLD     6.4-8.4    1 shot  x 2.00s   interior wide, ambient light strips
BURST C  8.4-10.8   6 shots x 0.40s   cluster, vents, seat stitch, wheel(int), star(int), screen
BLEND    10.8-11.2  ---- 400ms blend ---- (2 of 3)
HOLD     11.2-13.2  1 shot  x 2.00s   rear 3/4, taillights lit
BURST D  13.2-14.6  3 shots x ~0.47s  star macro, grille macro, badge — loops to shot 1
BLEND    14.6-15.0  ---- 400ms blend ---- (3 of 3)
```

**Resulting numbers:** 18 shots · 17 cuts · **68 cuts/min** · **median shot 0.40s** ·
**3 blends = 18%** · longest 2.00s.

Median 0.40s is *below* the 0.77s reference median — deliberately. Their median is pulled up
by a few long holds; their burst sections run at exactly one beat. Ours has the same shape.
If the gate reads it as too fast I'll lengthen the holds, not the bursts.

**Shot mix vs the measured reference mix:**

| class | reference | this build |
|---|---|---|
| exterior | 30% | 5 shots (28%) |
| wheel/brake | 15% | 3 (17%) |
| light macro | 15% | 3 (17%) |
| **interior** | **25%** | **5 (28%)** |
| badge | 10% | 2 (11%) |
| human | 5% | 0 — *see risk* |

---

## 4 · GENERATION — 5 clips → 18 shots

| clip | content | yields |
|---|---|---|
| **A** | front end at night, grille + hood star **igniting**, slow push | shots 1,2,3,4 + loop 16,17,18 |
| **B** | full car wide, low, wet asphalt, underground carpark | 7 + 11 |
| **C** | wheel + brake caliper + sill, hard raking light | 8,9,10 |
| **D** | interior: cluster, ambient light strips, vents, seat stitching | 12,13,14,15 + hold 6.4-8.4 |
| **E** | rear 3/4, taillights lit, reflections on wet ground | 5 + 17 |

Coverage does the rest — the technique that turned 4 clips into 8 shots on the Crown, now
pushed harder because sub-second shots need less source each.

**Every clip prompted for: night · underground carpark or wet street · hard artificial key ·
deep black shadows · the car's own lights as practical sources.** No dusk. No studio void.
That was the Crown's biggest visual failure.

---

## 5 · SOUND

- **Bed:** `phonk.py` at **150 BPM** — inside the 140–165 measured band.
- **Sub-bass target 65%.** My last phonk build measured 30%; the references run 60–92%.
  I will measure and iterate before it goes near the video.
- **Foley:** door close, low engine idle, a single indicator tick, tyre-on-wet. All from
  `assets/pillars/car_cinematic/sfx/` — pillar-scoped, so a travel bed cannot be reached.
- **Silence gap** 0.35s before the grille ignition at 0.0s? No — the ignition IS the opening.
  Gap goes before the **rear taillight reveal at 11.2s** instead.

## 6 · CAPTIONS

**Lyric-synced style**, per the references — 1–2 words, huge, centre-frame, on the beat.
Not sentences. No VO to sync to, so they punctuate the music:

```
0.8s   "S450"        2.4s   "FOUR FIFTY"      6.4s   "INSIDE"
11.2s  "AFTER DARK"  14.0s  "MERCEDES"
```

Five cards in 15s. `captionmgr` punch style, outline stroke. **No AI watermark** — platform
toggle instead.

## 7 · GRADE

Match the measured reference grade: **black point 2.0, saturation 91.5.** Our Crown came out
at saturation 109 — ~20% too punchy. `grade.py` will pull it down and crush the blacks.

---

## 8 · COST PREFLIGHT

**Measured with the literal params** (`mode:fast`, `720p`, `generate_audio:false`) — not
assumed. This is the check that caught the 17.5-vs-22.5 error last time.

```
per clip        17.5 cr   (preflighted, not quoted from memory)
5 clips         87.5 cr
balance now  1,519.31
after          1,431.81
```

Alternative considered: 4 clips at 70.0 cr. Rejected — the interior is 25% of the reference
shot mix and needs its own generation; cropping it out of an exterior clip is what produced
the Crown's repetition.

---

## 9 · RISKS, STATED BEFORE SPENDING

1. **Subject drift.** The Crown came back as a crossover. **There is still no locked plate.**
   `clipgate` will run on all 5 clips but cannot verify the subject without a reference — it
   passed two crossovers last time and said so. **Mitigation: I will look at every clip
   before editing, and `verdict` will block delivery pending your sign-off.**
2. **No human in frame** — references average 5%. At 15s with 18 shots there's no room
   without cutting a light macro. Accepting the miss deliberately.
3. **0.40s bursts may read as chaotic** on a limousine rather than a sports car. If it does,
   the fix is lengthening holds, not slowing bursts.

---

## ⏸ 10 · THE GATE

```
SPEND       87.5 cr      5 x Seedance 720p fast, 5s, no audio
BALANCE     1,519.31  ->  1,431.81
DELIVERS    15.0s · 720x1280 · 18 shots · 17 cuts · 68 cuts/min
            median shot 0.40s · 3 blends at 400ms · 150 BPM phonk
            night/hard-light throughout · lyric captions · no VO · no watermark
GATED BY    qc.py profile against the measured car_cinematic targets
```

Your GO is the only spend authorisation.

---

### Sources
- [Mercedes-Benz S-Class W223 — MENA](https://www.mercedes-benz-mena.com/oman/en/models/s-class-w223-805/)
- [Illuminated grille — Motor1](https://www.motor1.com/news/775593/mercedes-big-light-up-grille-teaser/)
- [S-Class press kit — MBUSA](https://media.mbusa.com/releases/release-2ed377f30bb0cb9da6ae59a4040057c7-the-mercedes-benz-s-class)
