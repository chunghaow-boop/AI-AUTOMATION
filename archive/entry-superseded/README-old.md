# TALYX — AI VIDEO AUTOMATION
### This folder is the whole project: pipeline, tools, media, lessons, skills.

> Not a car channel. **An autonomous video editor** — one engine, two inputs:
> AI-generated footage, or his own raw clips. The cars are the proving ground.

---

## ONE COMMAND

```
python3 talyx.py ls                what exists and what state it is in
python3 talyx.py plan   supra      gate the plan — 17 checks, FREE, blocks generation
python3 talyx.py board  supra      render the storyboard FROM the plan
python3 talyx.py cost   supra      exact credits, and what a probe costs first
python3 talyx.py build  lc300      cut it — one generic engine, plan-driven
python3 talyx.py verify lc300      gate the finished cut — 10 checks
```

Both gates exit non-zero on failure, so they chain: `talyx.py plan supra && ...`

**Adding video number eleven is ONE file: `plans/<name>.py`.** On 2026-08-01 this project
had nine python files at the root and seven were per-car — two and a half cars had produced
seven scripts. The ten-car list would have meant thirty. The plan is DATA, the pipeline is
CODE, and they must never multiply together.

## READ IN THIS ORDER

```
1  RESUME-2026-08-01.md      ← START HERE. Whole project in one read. Paste into a fresh chat.
2  docs/HANDOVER-2026-07-31.md   the detail: what broke, what changed, every lesson
3  CLAUDE.md                 project instructions. Claude Code loads this automatically.
4  docs/GATE.md              the mechanical gates
5  plans/supra.py            the live build, as data. Verbatim generation prompts inside.
```

---

## STATE — MEASURED 2026-08-01

| | |
|---|---|
| balance | **5,967.02 cr** (plan: team) — measured, never estimated |
| posts | **0.** The #1 gap. Every retention target here is a hypothesis. |
| working deliverable | `projects/lc300/output/LC300ZX_CINEMATIC_v1.mp4` — 14.67s, passes 10/10 in `verify.py`, **not posted** |
| next build | BMW i8 — plates approved, 11 clips × 22.5 = **~248 cr** (~4% of balance) |

---

## THE FOLDER

```
talyx.py                   <- THE ENTRY POINT. Every verb goes through here.
planqc.py                  gates the PLAN, before any credit is spent
verify.py                  gates the CUT, 10 checks, freshness first
board.py                   renders any storyboard from any plan

plans/                     ONE FILE PER VIDEO. Data only - no logic, no rendering.
  supra.py                 live: GR Supra A90 Final Edition
  i8.py                    planned: BMW i8

projects/                  ONE FOLDER PER VIDEO
  lc300/   clips/ output/ audio/ analysis/ legacy/   (superseded per-car scripts)
  supra/   clips/ analysis/ PRODUCTION.md
  i8/
  _archive/  older builds: Crown, S450, KK, influencer

assets/
  pillars/   PILLAR-PROFILES.json - measured targets from 23 reference videos
  refs/      those 23 reference videos. The evidence base. Do not delete.
  nev/       the organised 360 set + plates. See assets/nev/README.md
  bgm/       music beds

tools/       40 measurement tools. beatplan.py NEW; qc.py fx.py reverse.py PATCHED.
ledgers/     style_ledger.json (22 rejects) . knowledge.json (lessons, 4 topics)
docs/        documentation + docs/archive/ for anything superseded
skills/      talyx-cinematic . talyx-shotlist
```

**Restructured 2026-08-01** from 458 files / 390 MB to 269 / 329 MB. Removed a 43 MB zip of
files already present, a duplicate copy of the Nev photo set, 49 byte-identical images, and
three of the five competing "start here" documents. Nothing that works was touched: the
LC300 still passes 10/10 and the Supra plan still passes 17/17 through the new CLI.

## THE PIPELINE, AS BUILT

`engine.py` builds ANY video from ANY plan — proven by rebuilding the LC300 from
`plans/lc300.py` and passing 10/10 (beat lock 3.3ms vs the bespoke script's 31.8ms).
The 530-line per-car original is kept at `projects/lc300/legacy/build.py` for its comments.

```
1  phonk.py --bpm 150        bed FIRST. Music defines the grid, not the picture.
2  rhythm.py                 measure BPM *and PHASE*. Trim so hit 1 sits at t=0.
3  beatplan.py --hold 8      burst/rest grid. Every boundary on the beat by construction.
4  clipsense action_peaks_s  centre each shot on a real action peak.
5  shot_match()              exposure matched on RENDERED segments, BEFORE blends.
6  fx.mask_slice             blends at section boundaries only. Never dip.
7  grade                     saturation only. NEVER double-grade.
8  sfxgen                    whoosh LEADS the cut by 220ms; bed sidechain-ducks under it.
9  captions                  1–2 words, y=0.72 lower third. Never centre.
10 verify.py                 10 checks. One verdict. Freshness runs FIRST.
```

**Two families, never mixed:**

| | short / music-led | long / speech-led |
|---|---|---|
| cut to | the beat | the sentence |
| pillar | `car_cinematic` | `car_review` |
| median shot | 0.77s · 44.7 cuts/min · 20% blended | 3.60s · 14.3 cuts/min |
| grade | black_point 2.0 · saturation 91.5 | — |
| music | 140–170 BPM drift phonk | bed under VO |
| duration | 15–20s | 58–107s |

---

## THE RULES EARNED THE HARD WAY

```
RULE ZERO                  edit plan before generation. IDEA before edit plan.
COVERAGE >= shots / 2.5    cut rate must be EARNED, not faked with punch-ins
PLATES ALWAYS 4k           nano_banana_pro defaults to 1k. 4cr vs 2cr. Never accept the floor.
PLATE PROMPTS AS PHOTOS    camera, lens, aperture, ISO + the artefacts only real photos have:
                           clear-coat orange peel, skin pores, stray hairs
VIDEO IN std, NEVER fast   22.5cr/5s vs 17.5. Never chosen silently to save money.
PUNCH-INS <= 1.4x          1.9x measured an 82% loss of sharpness (234 → 42)
GRADE ~1.15 THEN MEASURE   profile targets came from FINISHED exports, not sources
FRAME-EXACT CUTS           -frames:v N, never -t seconds (24fps source drifts +34ms/shot)
NO BURNED-IN AI LABEL      platform toggle at upload — a HUMAN step, state it on delivery
MEASURE THE BALANCE        never estimate. A past estimate was off by 500cr.
CHECK THE FILE IS FRESH    a timed-out build leaves yesterday's render on disk
```

---

## projects/*/analysis/ — EACH IMAGE PROVES ONE THING

| image | what it proves |
|---|---|
| `lc300/analysis/STORYBOARD-FLOW.png` | Drawing the board caught one clip carrying 4 of 14 shots, and a lighting arc that contradicted my own comment. |
| `i8/STORYBOARD-I8.png` | The i8 board — doors-first, 3-second hook window marked. |
| `_archive/s450_softframes.png` | **The `whip` bug, frame by frame.** 0.5s of unreadable mush — `_xfade` blurred the WHOLE clip, not the seam. |
| `final_strip.png` | **Captions at y=0.42, dead centre, on the car.** The mistake, visible. |
| `v3_strip.png` | **Captions at y=0.72, lower third.** The fix. Same edit, one variable changed. |
| `night_check.png` | The two night clips — the best footage of the day, and why. |
| `repeat_check.png` | Four "repeat" cuts that were a **measurement bug** — timestamps that no longer existed after blending. |
| `lc300_contact.png` | Subject verification. How the car got checked BEFORE 70 cr was spent. |
| `lc300_soft_check.png` | Beige leather tripping the blank-frame gate. The gate measures BLUR and calls it black. |
| `assets/nev/_contact/nev_contact.png` | 49 photos indexed; plate chosen by face-area × sharpness. |
| `lc300_cinematic_strip.png` | The finished cut, sampled across its length. |

---

## THE HONEST PART

The engine cuts properly now — 3 ms beat lock, exposure matched, no repeated frames, audible
SFX, captions clear of the subject, ten checks passing.

**It still would not stop a scroll.** Every check measures *conformance to a profile*; none
measures *whether anything happens*. The LC300 is a walkaround tour — a car being looked at,
nothing happening to it.

The structural version: `mastermind` is a **frame**-quality inspector, not an **edit**
inspector. It asks "is this frame bad?" and never "do these two shots belong together?"
Every defect found by eye was RELATIONAL.

That is a creative problem, not a tooling one, and it is where the work goes next.

**Before anything else: post something.** One real 24-hour retention curve is worth more
than another 250 credits of generation.

---

## FIRST COMMANDS

```
balance                                       measure it. Never assume.
python3 verify.py                             confirm the LC300 still passes 10/10
python3 tools/smoketest.py                    9 routes, real resolution
python3 tools/qc.py phase0 --topic "<topic>"  research gate — DO NOT SKIP
python3 tools/styleref.py report              22 rejects. What he has turned down.
python3 tools/retention.py report             still empty. That emptiness is the gap.
```
