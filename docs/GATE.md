# THE GATE — one scorer, replacing five
### Replaces: RUNNER build /60 · RUNNER plan /60 · file 06 J1-J6 · file 25 debate · file 26 /100
### Why: five self-scorers = one opinion counted five times. Research (reference/33) shows
### stacked self-judgement AMPLIFIES bias. This is an accuracy fix, not tidying.

## STAGE 1 — MECHANICAL (no judgement; a fail = no ship, no score)
Run `tools/mastermind.py`, `tools/pacing.py`, `tools/facecheck.py`, `tools/rhythm.py`.
```
□ no blank frames (frame variance >8)
□ loudness −7..−9 LUFS (MEASURED from a real viral reel) · true peak < −1 dBFS
□ dead air < 45%
□ every caption within 0.6s of its spoken phrase
□ SFX/cuts within 50ms of the beat grid   (only when a music bed exists)
□ cuts/min inside the format band          vlog 15-25 · review 8-15 · industry 6-12
□ frame-1 motion ≥0.35                     posed opening = the #1 killer
□ face similarity across every seam        AI persona: consistency IS the product
□ AI disclosed                             platform requirement, non-negotiable
□ Bank 10 factual accuracy                 an AI persona stating a wrong spec is indefensible
```

## STAGE 2 — J0, THE HOOK TYRANT (solo veto, kept)
The only seat that keeps a standalone veto, because hooks decide whether anything else happened.
Grab complete by 2.0s · specific nameable promise · 10-14 words · interrupts at ~3s and ~7s.
Auto-caps: no visual hook ≤4 · slow build ≤3 · generic ≤6. **Score ≥8 or it goes back.**

## STAGE 3 — ONE WEIGHTED SCORE /100
```
J0 hook          ×3.0      Strategist/idea   ×2.0      twist/share-trigger ×2.0
execution seats  ×1.0      transitions/tech  ×0.75
```
**Any single seat ≤4 caps the final at 69.** One broken link kills the video.

## STAGE 4 — CHOOSING BETWEEN OPTIONS: PAIRWISE, NOT SCORES
Absolute /10 scales drift; pairwise is stable for *choosing*.
```
□ candidates ANONYMISED — no A/B/C labels, no "the obvious one must lose"
□ order RANDOMISED, then run again with the order SWAPPED
□ if the winner flips on swap, the comparison carried no signal
□ reasoning BEFORE the verdict, never score-then-justify
```
> The old tournament pre-committed its verdict ("A is generated only to be killed"). If the
> obvious option is genuinely best, the protocol must be able to select it.

## STAGE 5 — EXECUTION PROBE (the only test of pixels)
**Mandatory above 100cr.** Paper gates are blind to execution — every hook failure this system
shipped passed its paper gates and died in the render.
```
3 competing hooks × 5s × 720p fast ≈ 52cr   →  YOUR blind pick decides  →  build the winner
```
Your thumb is the only genuinely external signal in the system. Use `qc-console.html` A/B tab.

## STAGE 6 — PREDICT, THEN RESOLVE
Every gate emits a falsifiable prediction (3s rate · avg % viewed · shares). At +24h, log
predicted vs actual in the learning log. After ~10 resolutions the weights above stop being
opinion and become measured. **This is the only step that makes the system learn.**

## WHAT WAS DELIBERATELY DROPPED
- multi-round debate → bias amplifies with rounds; use one meta-judgement pass
- A/B/C tournament labels → identity bias, pre-committed verdict
- duplicate /60 scorecards → same opinion, counted twice

---


## SOUND DESIGN GATE — from the Arena Zero measurement (reference/ARENA-ZERO-ANALYSIS.md)
Machine analysis of a 1.9M-view reference confirmed four techniques absent from most AI content.
These are now checks, not suggestions:
```
□ SILENCE BEFORE IMPACT     bed muted 0.3-0.5s before the reveal, then impact_hit + sub_drop
                            (their scene 5: "tense silence followed by a sudden punch sound")
□ AMBIENCE BED PRESENT      every scene, -30 to -35dB. If you consciously hear it, too loud.
                            Absence of room tone is why AI video sounds dry.
□ MUSIC CHANGES BY ACT      3-4 states in 60s minimum. They used SIX in ten minutes.
                            One bed start-to-finish = the amateur tell.
□ HOOK IS A SEQUENCE        escalation, not one shot: situation -> problem -> turn.
                            They spend 22% of runtime on it. Your 60s video = ~13s.
```

## SEAT COVERAGE MAP — every seat still gets checked
Merging the five scorecards removed DUPLICATION, not COVERAGE. Each seat below is still
challenged. What changed: where a check can be a NUMBER it now is one, and each seat is
scored ONCE instead of three times in three documents.

| Seat | What it owns | Checked by | Type |
|---|---|---|---|
| **0 Strategist** | angle, avatar, pillar, is the idea worth making | Stage 3 weighted ×2.0 | judgement |
| **1 Scriptwriter** | beats, hook line, twist | Stage 2 J0 veto + Stage 3 ×2.0 | judgement |
| **1B Voice** | register, script, language mode | Stage 3, + `mastermind.py` loudness/dead-air | both |
| **2 Director** | blocking, shot clarity, occlusion | `pacing.py` shot lengths + Stage 3 | both |
| **2B Performance** | weight, hands have a job, staggered motion | Stage 3 (prompt text review) | judgement |
| **2C Emotion** | named conflict, 3 phases | Stage 3 (prompt text review) | judgement |
| **2D MUA / identity** | wardrobe lock, face consistency | **`facecheck.py`** similarity across seams | **mechanical** |
| **3 DOP** | motivated light, DOF, sharpness | **`mastermind.py`** sharpness + exposure floors | **mechanical** |
| **3B Foley** | hero sound named, foley per beat | **`rhythm.py`** onset vs beat grid (ms) | **mechanical** |
| **3C Gaffer** | every light named to a source | `mastermind.py` brightness floor + Stage 3 | both |
| **3D Sound Engineer** | LUFS, body/air balance, ducking | **`mastermind.py`** ebur128 + spectral bands | **mechanical** |
| **4 Technologist** | model fit, settings, cost sanity | cost preflight in `/talyx-shotlist` | mechanical |
| **7 Editor** | pace, dead air, cut rhythm | **`pacing.py`** cuts/min, dead zones, variation | **mechanical** |
| **7B Transitions** | what is physically continuous across each seam | `rhythm.py` cuts-vs-beat + Stage 3 | both |
| **J0 Hook Tyrant** | the first 3 seconds | **Stage 2 SOLO VETO** (unchanged) | judgement |
| **J1-J6 panel** | scroller, novelty, quality, local, buyer, algorithm | folded into Stage 3 weighted /100 | judgement |

**What each seat gained:** 7 of 16 seats moved from opinion to measurement. A sound engineer
that says "sounds good" was never a check. `ebur128` printing -12.3 LUFS is.

**What each seat lost:** being scored in `06`, then again in the build /60, then again in the
master /100 — three numbers for one judgement, which felt like rigour and was actually
triple-counting a single opinion.

**Prompt QC before generation** (your specific concern) lives in `/talyx-shotlist` steps 4-7:
each shot's CAMERA / PERFORM / EMOTION / LIGHT / TRANSITION / SOUND line is written, then run
through Stage 2 (J0) and Stage 3 (weighted /100) BEFORE any credits are spent, with the full
prompt shown verbatim at the approval gate.


## VIDEO QUALITY + CAMERA MOVEMENT — the generation-side gate
Everything above judges the EDIT. These judge the GENERATION itself — the thing that decides
whether it looks like the reference videos or looks like AI slop.

### PRE-GENERATION (free — written into the prompt, checked before spend)
```
□ CAMERA BODY named          "Shot on Sony FX3" / ARRI / RED — a real body anchors the look
□ LENS + T-STOP named        "35mm, T2.8" — controls DOF explicitly. T5.6 if bodies must be countable
□ MOVEMENT named + MOTIVATED not "cinematic camera move" but WHICH move and WHY:
                             slow push-in (rising tension) · handheld follow (documentary)
                             locked-off (authority) · low tracking (speed) · orbit (reveal)
□ ONE move per shot          two moves in one 5s clip = mush. Pick one, commit
□ MOTION IN FRAME 1          something HAPPENING, not someone POSED  ← the #1 killer
□ LIGHT sourced              every light named to a source; practicals visible; one shadow logic
□ GRADE named                "muted, warm amber highlights, deep shadows, subtle 35mm grain"
□ NEGATIVES ARE USELESS      only a start_image fixes frame 1. Proven, twice
□ RESOLUTION honest          720p 9:16 is enough for phone. 1080p doubles cost — hero only
```

### POST-GENERATION (mechanical, on the rendered clip)
```
□ sharpness floor      Laplacian var ≥25        mastermind.py   catches melt / soft frames
□ exposure floor       min brightness ≥18       mastermind.py   catches crushed blacks
□ blank-render check   frame variance >8        mastermind.py   the known display bug
□ hook motion 0-2s     optical flow ≥0.35       pacing.py       catches the posed opening
□ motion continuity    no dead static stretches pacing.py       dead zones by timestamp
□ identity across cuts face similarity          facecheck.py    the AI-persona killer
```

### THE CAMERA-MOVE BANK (name one per shot — never "cinematic")
| Move | Use it for | Prompt phrasing |
|---|---|---|
| slow push-in | rising tension, a verdict landing | "slow dolly push toward the subject" |
| handheld follow | documentary honesty, vlog | "handheld follow, subtle sway, natural" |
| locked-off tripod | authority, industry-value talking | "locked-off tripod, static frame" |
| low tracking | speed, machinery, arrival | "low-angle tracking alongside, wheel height" |
| orbit / arc | product reveal, the car | "slow arc around the subject, 90 degrees" |
| rack focus | shifting attention within a shot | "rack focus from foreground badge to face" |
| crane down | scale into intimacy | "crane descends from wide to eye level" |
| whip pan | energy transition INTO the next shot | "fast whip pan left, motion blur" |

**Rule:** the move must be *motivated* — name the emotional reason in the same line. An
unmotivated move is the single clearest tell of AI-generated video.

### WHY THE REFERENCE VIDEOS LOOK BETTER (the honest list)
1. They name a **real camera + lens + stop**. Generic prompts give generic optics.
2. **One move per shot**, motivated. AI slop stacks three moves and dissolves between them.
3. **Hard cuts, not dissolves.** Your Seedance prompt asked for "no hard cuts" — that is
   cinematic grammar fighting short-form retention.
4. **Character sheet locked** before any shot. Consistency reads as production value.
5. **They cut on the beat.** `rhythm.py` measures this in milliseconds.
