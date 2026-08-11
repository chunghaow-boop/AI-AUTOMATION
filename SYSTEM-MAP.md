# SYSTEM MAP — the whole automation, top to bottom
### Read order for a NEW CHAT: `CLAUDE.md` → **this file** → the newest `RESUME-*.md`
### Written 2026-08-06 after a full read of every pipeline file. Architecture, not state.
### State lives in the RESUME. This file changes only when the ARCHITECTURE changes.

---

## 0. WHAT THIS IS IN ONE PARAGRAPH

A credit-rationed film studio where every department is a measurement. Fully-AI
short-form video for a Malaysian recond-car audience, fronted by a consistent AI KOL
(Nev). The design assumption behind every line of it: **generation is expensive and
irreversible, so the entire argument happens before the money moves.** Thirteen-plus
gates exist to make a bad build fail while it is still free.

**The one architectural rule:** THE PLAN IS DATA, THE PIPELINE IS CODE, AND THEY NEVER
MULTIPLY. A new video is one new file in `plans/`. Before `talyx.py` there were nine
root-level scripts, seven of them per-car.

---

## 1. THE FLOW

```
TITLE
 └─ readback + his picks            free, mandatory (CLAUDE.md TITLE CONTRACT)
 └─ plans/<name>.py                 the plan, as DATA
     ├─ talyx.py plan     → planqc.py     39 checks. BLOCKS. Free.
     ├─ talyx.py board    → board.py      timeline PNG from the plan
     ├─ tools/storyboard.py            per-shot image + linkage + edit flow → HTML
     ├─ tools/judge.py                 J0/J2/J4 — the gate that kills BORING
     └─ talyx.py cost     → exact credits + probe-first number
 ⏸ HE SAYS GO  ← the one gate. Everything above is free.
 └─ generate (Higgsfield MCP)       ~22.5cr per 5s 720p std clip
     ├─ talyx.py ingest   → clipqc.py     per-clip gate. One reject = 22.5cr, not a rebuild.
     ├─ talyx.py build    → engine.py     ~15 stages, one encode
     ├─ talyx.py verify   → verify.py     15 checks, freshness FIRST
     ├─ tools/cutsense.py              LRA + far-repeats + event curve (standalone)
     └─ tools/judge.py --stage cut     the panel on the finished cut
 └─ POST  ← has never happened. Zero posts, ever.
     └─ tools/retention.py             +24h curve → the loop. Zero rows.
```

`talyx.py` is the front door: `plan · board · cost · ingest · build · verify · ls`.
`plan` and `verify` exit non-zero deliberately so they compose in a shell.

---

## 2. EVERY FILE THAT MATTERS

### Root — the pipeline (CODE, invariant)
| file | what it is |
|---|---|
| `talyx.py` | CLI dispatcher. 7 verbs. No video logic. |
| `planqc.py` | **The plan gate.** 39 emitted checks. Also generates `PRODUCTION.md`. |
| `clipqc.py` | **The paid-artefact gate.** 13 checks on every generated clip. |
| `engine.py` | **The builder.** Plan + clips → finished mp4. One encode. |
| `verify.py` | **The cut gate.** 15 checks. CHECK 0 gates all others. |
| `board.py` | Timeline PNG, rendered from the plan only. |

### `plans/` — the plan (DATA, one file per video)
`crown.py` is the current format demo. Also `wrx, kk, supra, lc300, i8`.

### `assets/`
| path | what |
|---|---|
| `pillars/PILLAR-PROFILES.json` | **every genre threshold.** 5 pillars. Read by all gates. |
| `nev/` | the persona: face set, wardrobe, plates, `index.json` |
| `refs/<pillar>/` | reference videos he chose. 23 files. Gitignored. |
| `bgm/`, `BGM/<pillar>/` | music beds, per pillar (never cross-pillar) |

### `ledgers/` — the memory
| file | what |
|---|---|
| `knowledge.json` | **117 lessons, 7 topics.** planqc 23 BLOCKS a plan that doesn't ack the current count. |
| `approvals.json` | Every "he approved X" with the VERBATIM quote and exact scope. 3 approvals, 3 unverified. |
| `routing.json` | **68 checks → the seat that owns each.** New 2026-08-06. |
| `attempts.json` | Attempt counts. The 5-failure stop rule, mechanised. |
| `verdicts.json` | Every judge verdict. |
| `style_ledger.json` | His rejections, and whether each is still fixed. |

### `tools/` — ~50 measurers. The ones that matter:
| tool | what |
|---|---|
| `mastermind_loop.py` | **The conductor.** Routing, seat dispatch, 5-failure stop, `--audit`. |
| `judge.py` | **The LLM loop.** file-06 judges. API mode or paste-packet mode. |
| `storyboard.py` | Per-shot reference image + linkage + edit flow → self-contained HTML. |
| `bugsense.py` | Predicts structural bugs. 4 classes, all learned from real ones. |
| `refsense.py` | Reference DNA (measured) + semantic teardown (read). Two halves, kept apart. |
| `reffetch.py` | Fetch references by URL (yt-dlp), auto-study. |
| `refstudy.py` | Reference → target profile. How PILLAR-PROFILES was built. |
| `reverse.py` | Diff our cut against the reference DNA. |
| `cutsense.py` | Standalone: LRA floor, far-repeat matrix, event curve. |
| `syncqc.py` | **NEW 2026-08-07. Does the CUT do what the PLAN said? The only check on the JOIN — every other gate checks one side. Run after build, before verify.** |
| `contact.py` | **NEW 2026-08-07. 20-panel contact sheet at ingest and on the cut. His standing order: he sees it before anything is assembled.** |
| `lessons_book.py` | **NEW 2026-08-07. Compiles `knowledge.json` into `LESSONS.md` — one file, 150 lessons. Generated, never hand-edited.** |
| `smoketest.py` | 9 routes on synthetic inputs. Baseline **79 pass / 0 fail** (2026-08-06; was 74/5 — 4 were one bad bed glob, 1 was an unescaped Windows path). |
| `fx.py` | Transition bank: dissolve, whip, speedramp, zoomblur, masks, dolly, glitch, flash, dip. |
| `cards.py` | HTML/CSS → PNG cards via Playwright. Replaces ffmpeg drawtext. |
| `retention.py` | Post → +24h curve → attribution. **Zero rows. MIN_N=8.** |
| `lessonize.py` | **The learning loop, mechanised.** Failing gate check / judge seat → a dated lesson → planqc 23 BLOCKS the next plan. `--brief` PRINTS the unread ones. Never fixes anything. |
| `blendsense.py` | Whip-sensitive transition detector. Separates WHIP (sharpness trench + scene change) from HARD CUT and DISSOLVE. |
| `mastermind.py` | Frame/audio METRICS module. `audio_metrics` feeds verify 8. Not the seat. |

**Two different things share the name "mastermind":** `tools/mastermind.py` is a metrics
module that enforces nothing. THE MASTERMIND is a seat defined in `27-mastermind-qc.md`,
executed by a human + LLM. They share a name and almost nothing else.

---

## 3. THE GATES, WITH THE NUMBERS THAT MATTER

### planqc.py — 39 checks, free, blocks generation
Highlights (`--audit` in mastermind_loop lists all 39 with owners):

- **1 duration** `|timeline() − TARGET_S| < 0.05`
- **2 pillar band** duration + median shot in profile band, cuts/min within ±20%
- **3 coverage** distinct sources ≥ `ceil(shots / 2.5)`
- **4 source balance** no source > `max(2, ceil(n×0.25))`; every source used
- **5 adjacency** zero neighbouring shots from one clip
- **6/7 crop** ≤ `MAX_CROP`; runs ≤2, halves within 30pp, shot 0 uncropped
- **8 repeat framing** no duplicate (source, crop) unless in `CALLBACKS`
- **9 hook is an EVENT** shot 0 act == EVENT **and** ≤ 2.00s
- **11 blends** % in profile band, width 240–560ms, `dip` auto-fails (fades through black)
- **12 caption zone** `CARD_Y` NOT in 0.34–0.60; ≤ pillar's `card_max_words`
- **13 plates** every plate 4k; humans must cite the persona plate
- **14 prompt quality** every prompt contains `not a render` + `negative:` + `reference image`
- **17 cost** total ≤ MEASURED balance
- **19 sound design** FOLEY + SOUND complete; EVENT/PAYOFF foley ≥ −6dB
- **20 transitions** no blend touches an EVENT shot
- **21 source capacity** Σ shot durations ≤ `CLIP_S − banned − 0.1`
- **22/23 premortem + lessons** ≥3 ledger-cited risks; ack must EQUAL current count
- **24/29/31 linkage** intent per boundary; token must appear in BOTH shots' text; ≥ consequence floor
- **26 style declared** pillar must declare a style block (anti-inheritance)
- **28 framing diversity** two sources sharing a plate may not share a framing
- **30 time monotonic** light state never runs backwards or jumps ≥3

### clipqc.py — 13 checks, per clip, before the edit
**Central principle: measure the DELIVERED WINDOW, not the clip head.** The engine
centres every shot on its action peak; head measurement caused three false rejects.

Blocking: `readable · specs · delivered window (motion_floor) · brightness (band) ·
sharpness ≥25 · foley source audible >−45dB · face READS (≥2 detections, ≥3.5% frame)`
Non-blocking: `0 role resolved · no-settle open · alive after 2s · EVENT window
(PROVISIONAL, approvals UNV-1) · EVENT is loudest · on-subject text → EYE`

### verify.py — 15 checks on the finished cut
**CHECK 0 is freshness and NOTHING ELSE RUNS IF IT FAILS.** A build that times out
before its atomic write leaves yesterday's file on disk; every later number would be
fiction.

`2 cut-to-music` median dev <50ms & ≥70% within 50ms · `3 sfx audible` crest lift ≥2dB
(or >−3dB on a dense bed) · `4 repetition` ≤25% cuts hist-corr >0.95 · `5 exposure`
zero swings >18 luma · `8 audio` −9.6..−6.5 LUFS, peak ≤−1.0 dBTP, silence <0.45 ·
`9 black` zero frames mean<4 · `10 far repeats` non-adjacent pairs · `11 transitions`
on-grid ±40ms, no smear · `13 composition dupes` cosine ≥0.93 · `14 place variety`
shots/places ≤2.0 · `15 relight audit` NON-BLOCKING by instruction

---

## 4. THE CONTRACT — WHICH PLAN FIELD IS READ BY WHAT

**This is the single most important table in the repo, and it is NOT reproduced here on
purpose.** A hand-typed copy goes stale, and a stale contract table is exactly the bug
class that has cost the most (see §6). Get the live answer:

```
python tools/bugsense.py --class 1     # keys a pipeline file reads with a SILENT DEFAULT
                                       # that a plan does not define  ← the expensive one
python tools/bugsense.py --class 2     # names a plan declares that NO file reads
```

What you must know structurally:

- `engine.py` reads only ~30 plan fields. It does **NOT** read `GEN_MODE`, `MODE`, `RES`,
  `CLIP_S`, `MAX_CROP`, `TARGET_S`, `DELIVERED_S`, `GENERATION`, `PLATES`, `FRAMING`,
  `WINDOWS`, `SHOT_TIME`, `LINKAGE`, `CALLBACKS`, `MIX`, `CONTENT`, `PREMORTEM`, `cost()`.
- `SOURCES` — engine uses only the KEYS. The tuple payload is for planqc/board.
- `SOUND` — engine reads **only `SOUND["hero_shot"]`**, and only under `edit_sfx=hero_only`.
  Everything else in that dict is prose for a human. `bed_map` and `duck_shots` are INERT.
- Pillar `style` drives clipqc and planqc thresholds; engine reads only `edit_sfx` and the
  four `shot_match_*` values.

**THE RULE, EARNED THE HARD WAY:** *if a declaration changes behaviour, name the file and
line that READS it, or call it a note.*

---

## 5. COST MODEL

```
720p std   4.5cr/s     →  5s clip = 22.5cr      ← the unit that matters
1080p std  9cr/s       →  15s cinematic = 135cr
720p fast  17.5 flat   →  NEVER chosen silently to save money (planqc 15 blocks it)
plate      4cr at 4k   →  nano_banana_pro defaults to 1k. ALWAYS 4k.
```

**PROBE FIRST.** Buy the plates + ONE clip, LOOK at it, then commit the rest.
Crown: 278.0cr total, 30.5cr probe. A 2cr plate would have prevented an 87cr wrong-car build.

**MEASURE the balance, never estimate.** A past estimate was off by 352cr.

---

## 6. THE BUG CLASSES THAT HAVE ACTUALLY COST MONEY

All four are the same shape: **a declaration and its reader disagreed, and nothing said
so.** `tools/bugsense.py` scans for new instances of each.

1. **UNMET CONTRACT** — a file reads a plan key with a silent default the plan doesn't
   define. `engine.py:781` read `SOUND["hero_shot"]`; crown defined `"hero"`. The only
   sound in a 30s silent film would have played at t=0.00s, 14.00s early, on a 278cr build.
2. **INERT DECLARATION** — a plan declares something no file reads. `BLEND_AS_OVERLAP`
   and `GENERATE_AUDIO` were committed *inside the plan written to fix a defect list*.
3. **NAME SHADOW** — `verify.py` called `glob.glob` with `glob` imported only locally as
   `_g`. NameError on every call, swallowed by a bare `except`, relight budget stuck at
   18.0 forever.
4. **FOREIGN LITERAL** — `verify.py` CHECK 0 globbed only `LC300_*.mp4`, so the check
   that gates all fourteen others was inert on five of six projects.

### And the traps that make the CHECKS lie (file 27 PART C, 16 of them)
`VACUOUS PASS` (a check measuring nothing printing OK — 8 of 13 did) · `SMOOTH NUMBER`
(a metric improved by destroying the input — exposure closed by relighting an approved
shot +72 luma) · `OPEN-LOOP GAIN` (applying a computed gain and never re-measuring;
`eq=brightness` was assumed 134 luma/unit, MEASURED 174–519) · `DELIVERED WINDOW`
(gate what plays, not the head — 3 false rejects) · `AVERAGE-vs-MOMENT` · `PLANNED-vs-
ACTUAL` (blends compress the timeline) · `BLUR-AS-BLACK` · `COLOUR-BLIND-METRIC`.

---

## 7. THE SEATS AND THE ROUTING

Every check has an owner. `ledgers/routing.json` is the table; `MASTERMIND` /
`STRATEGIST` / `SCRIPTWRITER` / `DIRECTOR` / `DOP` / `GAFFER` / `FOLEY` /
`SOUND_ENGINEER` / `EDITOR` / `TRANSITION_MASTER` / `TECHNOLOGIST` / `J0` / `PANEL` /
`OPERATOR` (= Gavril).

```
python tools/mastermind_loop.py --audit              MUST say CLEAN before trusting dispatch
python tools/mastermind_loop.py <plan> --stage plan  run + route + count attempts
python tools/mastermind_loop.py <plan> --status      the attempt ledger
```

Work orders sort **cheapest fix first** (plan = free, clip = 22.5cr). At 5 attempts on
one check it exits 3 and says STOP — his rule, mechanised.

**The loop does not fix anything by itself and never will.** Fixing is judgement.

### What NO routing table can own (`_not_routed`)
- **IDENTITY** — is it really Nev. The verdict FLIPPED between crop scales on KK: "not
  him" at thumbnail, "plausibly him" at matched size, same frames, same session.
  **Claude presents evidence at matched scale. Gavril rules. Always.**
- **IS IT GOOD** — no gate measures whether anything HAPPENS.
- **DOES IT PERFORM** — zero posts, so nobody can be held to it.

---

## 8. THE PILLARS

| | car_cinematic | car_cinematic_chill | travel_vlog | car_review | industry |
|---|---|---|---|---|---|
| duration | 10–22s | 20–34s | 16–29s | 58–107s | 35–181s |
| shot median | 0.77s | 1.3s | 1.13s | 3.6s | 2.52s |
| cuts/min | 44.7 | 38 | 40.3 | 14.3 | 17.9 |
| bpm | 140–165 | 88–112 | 95–115 | — | — |
| edit_sfx | full | hero_only | hero_only | none | none |
| cut_spine | beat_grid | beat_grid | beat_grid | **sentence** | **sentence** |

**`cut_spine = "sentence"` means the editor DOES NOT EXIST.** `car_review` and
`industry` can be PLANNED but NOT BUILT. planqc `26c` warns. Never promise a
talking-format build.

`car_cinematic_chill` has **n=0** — every number is a structural CHOICE interpolated
between two measured neighbours. It says so in its own `_not_measured` field.
Re-derive at first ingest. **Never cite a choice as a measurement.**

Profiles expire **2026-09-28** (measured 2026-07-30 from 23 references).

---

## 9. HARD RULES THAT OVERRIDE EVERYTHING

1. **Evidence before claims.** Every audio/pacing claim cites a measurement.
2. **MEASURE the credit balance.** Never estimate.
3. **Mechanical beats judgement.** If a check can be a number, it must be.
4. **After any fix, re-run the check.** A fix pass creates new defects. Proven twice.
5. **5 failures on one problem → STOP and ask.** Never loop and burn credits.
6. **Rank options, name the pick, one line why.** Never a flat menu.
7. **Claude PULLS from GitHub; the USER PUSHES.** Claude has no credentials. Never claim otherwise.
8. **Frames and spectrograms ARE the work.** View them. Never ask for a text summary instead.
9. **Claude cannot hear audio.** Every audio claim comes from a measurement.
10. **Never invent a number, path, credit cost or capability.**
11. **A named subject is NEVER generated from text alone.** Plate first, LOOK at it, then
    pass it as `start_image` on every shot.
12. **AI content must be labelled** on TikTok/Meta. Non-negotiable. It is a HUMAN step at
    upload — never burned in (planqc 15 blocks that).

### Working with his files
- **ADDITIVE ONLY unless he says otherwise.** *"the pipeline and the flow i already built
  i think is good already"* / *"we must respect each other work, those stuff are my days
  and night effort adjustments."* If a defect can only be fixed inside a pipeline file,
  DECLARE IT OPEN and hand him the decision. **A plan-level fix beats a pipeline-level fix
  even when the pipeline fix is cleaner.**
- Back up before editing: `_backup_<date>/`, and say so.
- **Prove it.** Before/after diff on every plan, every generated doc, and smoketest.

### The Cowork bridge
- `device_bash` **cannot delete.** `rm` and cross-mount `mv` both fail — but `mv`'s COPY
  half succeeds first, so files look "stuck" in Downloads when they already arrived.
  **Downloads → AI is always `cp`. He deletes the original.**
- `device_commit_files` caps at 20MB/file. Several reference videos exceed it. `cp` doesn't.
- Git leaves stale `.git/*.lock` the bridge can't remove. `PUSH.bat` clears them.

---

## 10. THE STANDING GAP

**Zero posts. Ever.** WRX and KK finished and unposted. Crown planned, gated four times,
ungenerated. Thirteen gates optimise toward numbers scraped from 23 strangers' videos
that expire 2026-09-28. `retention.py` is built and holds zero rows.

23 references are MEASURED. **Zero are READ** — not one line anywhere explains WHY any
of them worked. `tools/refsense.py --strip` then `--fill` costs zero credits and is the
highest-value work available.

**One posted video with a real 24-hour curve outranks everything in this repo.**

---

## 11. THE LEARNING LOOP — how a finding becomes permanent (2026-08-06)

**THE MASTERMIND IS NOT A PROGRAM.** It is a seat (`27-mastermind-qc.md`) executed by a
human plus an LLM, so **its entire memory is these files**. Anything not written down
here does not exist for the next session. That is the whole reason this section exists.

```
a gate FAILS / a judge seat FAILS
   └─ tools/lessonize.py <project> --from-gate | --from-judge
        └─ dated lesson appended to ledgers/knowledge.json  (deduped on a signature)
             └─ that topic's COUNT rises
                  └─ planqc 23 BLOCKS every plan whose LESSONS_ACK is lower
                       └─ tools/lessonize.py <plan> --brief   PRINTS the unread ones
                            └─ read → put them in the plan's PREMORTEM → re-ack
```

**It captures and blocks automatically. It never fixes.** A loop that edited a plan to
clear its own gate would be optimising the CHECK instead of the FILM — the SMOOTH NUMBER
trap from file 27 PART C, automated and unattended.

**The honest limit:** planqc 23 checks a NUMBER, not comprehension. A session can ack 76
without reading one line. `--brief` exists so the ack can be earned; nothing can force it.

`--status` lists every topic count and every plan the ledger currently blocks.
Backs up `knowledge.json` to `_backup_lessonize/` before each write.

### Per-pillar mix, added the same day
`engine.py` reads five relationships from the PILLAR's style block, defaulting to the old
hardcoded constants so untouched pillars build byte-identically:
`mix_sfx_target_db` (−6) · `mix_foley_fg_target_db` (−2) · `mix_duck_threshold` (0.06) ·
`mix_duck_ratio` (6) · `mix_duck_release` (120).
**MEASURED:** during the loudest 10% of broadband moments the bed's 40–160 Hz band drops
**−4.9 dB on KK v15** (travel_vlog) but **−31.1 dB on WRX v9** (car_cinematic,
edit_sfx=full). travel_vlog now declares foley foreground at **bed−8** and a **3:1** duck.
**car_cinematic is UNCHANGED and OPEN** — retuning it changes the approved WRX look.

### Blend bands can be COUNTS
planqc 11 accepts `blend_max_count` and a `designed_kinds` whitelist. A percentage
quantises to zero on a short cut: at 19 boundaries ONE blend is 5.3%, over a [0,5] cap.
travel_vlog measures **9.5% designed pooled across 6 references, all whips**
(`blendsense.py`), so it declares `blend_max_count 2` and `designed_kinds ["whip"]`.

### CORRECTION to RESUME-2026-08-06
That file states `GATE.md` and `PROMPTS.md` "do not exist". **They do** — at
`docs/GATE.md` and `docs/PROMPTS.md`. The old CLAUDE.md pointer had the wrong PATH, not
a missing file. Every other referenced doc (27, 06, 19, 01, 08, 14, 17, RECONCILE) is
present and was verified 2026-08-06.

---

## 12. THE DOCTRINE DOCS — 29 files the entry path never named

**MEASURED 2026-08-06, in answer to "does the mastermind know this in detail?":** the
three entry files name **6/6 root pipeline files**, **32/53 tools**, and **1 of these 28**.
CLAUDE.md cites 27, 06, 19, 01, 08, 14 and 17 by number in prose, but nothing ever told a
new session the other twenty-one existed. This index is that missing line.

**These are the SEATS.** The pipeline is code; these are the judgement it is meant to
encode. A gate can only measure what one of these decided.

| file | what it is |
|---|---|
| `00-START-HERE.md` | entry orientation |
| `01-4-beat-spine.md` | the 4-beat spine — the CONTENT block's four gates |
| `02-ai-video-crew-roles.md` | the crew — every role agent |
| `03-physical-performance-master.md` | physical performance |
| `04-foley-master.md` | the Foley Master |
| `05-cinematic-ai-video-spec.md` | master spec + prompt template |
| `06-content-judges.md` | **the reception gate — J0/J2/J4. `tools/judge.py` runs this.** |
| `07-emotion-engine.md` | micro-expression as conflict |
| `08-the-strategist.md` | Seat [0] — the title readback |
| `09-learning-log.md` | learning log (predates `ledgers/knowledge.json`) |
| `10-the-editor.md` | Seat [7] — the assembly layer |
| `11-editing-bank.md` | edit recipes for auto-assembly |
| `12-sfx-foley-bank.md` | the SFX / foley bank |
| `13-role-asset-banks.md` | 20+ assets per seat |
| `14-audience-voice-series.md` | audience + voice — who we talk to |
| `15-launch-protocol.md` | what happens after "ship" — **the unused half, 0 posts** |
| `16-master-skeleton.md` | full pipeline, all seats |
| `17-car-cinematic-master-prompt.md` | the car cinematic master prompt |
| `18-agent-contract.md` | title in, finished video out |
| `19-sound-engineer.md` | **[3D] the mix, not the sound list.** The seat behind the per-pillar mix knobs. |
| `20-sfx-download-list.md` | 50-SFX starter library |
| `21-bgm-library.md` | BGM library — 80 tracks |
| `22-HANDOVER.md` | session state (superseded by `RESUME-*.md`) |
| `23-asset-preproduction.md` | build assets BEFORE the video — the PLATE rule |
| `24-system-audit.md` | every file scored against the four formats |
| `25-qc-debate-protocol.md` | every seat gets challenged before it advances |
| `26-master-scorecard.md` | one number per video, comparable across all |
| `27-mastermind-qc.md` | **[FINAL BOSS] the strictest gate. THE MASTERMIND'S PROCEDURE.** |
| `28-linkage-master.md` | **THE LINKAGE MASTER — his taxonomy, taught 2026-08-07. 13 carry kinds and the decidable test for each. NEW.** |

### The three that a mastermind must read before it acts
`27-mastermind-qc.md` (its own procedure + the 16 measurement traps) ·
`06-content-judges.md` (the seats `judge.py` executes) ·
`08-the-strategist.md` (the title readback that starts everything).

### KNOWN STALE — the skills predate the gates
`skills/talyx-cinematic/SKILL.md` (1,687 words) and `skills/talyx-shotlist/SKILL.md`
(645 words) mention **planqc 0 times, clipqc 0, judge 0, lessonize 0**. CLAUDE.md still
says "Use the `/talyx-shotlist` skill for Phase 1", so a session that obeys that gets
Phase-1 guidance written before the 68-check architecture existed. **HIS CALL:** rewrite
them against the current gates, or delete the pointer. Do not leave both.

### Tools not named anywhere in the entry path (21 of 53)
Mostly per-car legacy builders and one-off measurers. Two matter:
`tools/build_kk.py` — **`smoketest.py` imports it** for the loudness route, so it is live
infrastructure, not legacy. `tools/facecheck.py` — CLAUDE.md tells you to run it on every
identity seam. Get the current list with `ls tools/*.py`; do not trust a typed copy.
