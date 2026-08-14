# THE PIPELINE
### Every stage, what it measures, what it cost to learn, and where it can still bite.
### Written after running the whole thing end-to-end on 2026-08-01. Numbers are measured.

---

## THE SHAPE

```
  IDEA ─► PLAN ─► ⏸ GATE 1 ─► GENERATE ─► ⏸ probe ─► BUILD ─► ⏸ GATE 2 ─► POST ─► MEASURE
          data     planqc      Higgsfield   look      engine    verify      human   retention
          FREE     FREE        CREDITS      22.5cr    FREE      FREE        FREE    ← the gap
```

**Two gates, and only one of them costs anything to fail.** `planqc` runs before a single
credit is spent; `verify` runs before anything is posted. Everything expensive sits between
two free checks, on purpose.

```
python3 talyx.py plan   supra      17 checks · FREE · blocks generation
python3 talyx.py board  supra      draw it — the picture catches what numbers do not
python3 talyx.py cost   supra      exact credits, probe-first
                ⏸ approve, then generate
python3 talyx.py build  supra      cut it
python3 talyx.py verify supra      10 checks · blocks delivery
```

Both gates exit non-zero, so they chain: `talyx.py plan supra && talyx.py build supra`.

---

## STAGE 0 · IDEA — the only stage with no tool

**RULE ZERO: idea before edit plan, edit plan before generation.**

The LC300 passes ten mechanical checks and would not stop a scroll, because nothing happens
in it. Every check measures conformance to a profile; none measures whether anything
*occurs*. That is not fixable downstream.

What the research says the idea has to be:

| finding | source |
|---|---|
| TikTok Q2 2026 ranks **3-second retention above watch time** | hookmafia |
| hooks **under 2s** = 23% higher completion than 4–5s (n=10,000) | storycut |
| car edits: **start with immediate motion** | fluxnote |
| Reels reward a **SINGLE EVENT**, not a tour | roadspy |

So the plan gate has a check for it — **check 9 blocks any plan whose shot 0 is not an
`EVENT` act completing inside 2.00s**. It is the only creative rule that is mechanically
enforced, and it exists because "the hook is a static wheel" was decidable from the plan.

---

## STAGE 1 · PLAN — `plans/<name>.py`, data only

One file per video. No logic, no rendering, nothing typed twice. The board renders **from**
it, the production doc generates **from** it, `planqc` validates it, the engine builds from
it. When a plan lived in three places once — a PNG, a markdown file and a build MAP — the
board said one thing, the code did another, and I checked the board.

```python
BPM, BEAT, W, H, FPS, MODE, MAX_CROP, TARGET_S
PLATES   = {...}          reference plates + the must_show list they are checked against
SOURCES  = {...}          one generation each: label, colour, act, plates, VERBATIM prompt
CLIPS    = {...}          key -> filename in projects/<name>/clips/
SHOTS    = [...]          (source, crop, kind, note) — the timeline
CROP_XY  = {...}          crop centre per shot, defaults 0.50/0.50
BLEND_AFTER · SFX_LEAD · IMPACT_AT · SUBDROP_AT · CARDS · CARD_Y · GRADE_*
```

**Adding video eleven is this one file.** On 2026-08-01 the project had seven per-car
scripts for two and a half cars; the ten-car list would have meant thirty.

---

## STAGE 2 · GATE 1 — `planqc.py`, 17 checks, free

Every other gate in this project runs *after* the money is gone. These defects were all
decidable from the plan alone:

```
7 of 13 cuts showed the same image      4 sources under 14 shots — countable
1.9x punch-ins destroyed 82% sharpness  a number in the plan, not in the footage
captions dead centre on the car         a y-coordinate in the plan
the hook was a static wheel             shot 0's source, in the plan
a generic crossover, not a Crown        a missing reference plate, in the plan
```

| # | check | blocks on |
|---|---|---|
| 1 | duration | timeline ≠ target |
| 2 | pillar band | duration / median shot / cuts-min outside the measured profile ±20% |
| 3 | **coverage** | `distinct sources < shots / 2.5` |
| 4 | source balance | one clip carrying >25% of shots |
| 5 | adjacency | neighbouring shots from the same clip |
| 6 | crop cap | any crop > 1.40 |
| 7 | **crop distribution** | >2 crops in a row · halves differing >30 pts · cropped hook or hold |
| 8 | **repeat framing** | same source at the same crop, undeclared |
| 9 | **hook is an EVENT** | shot 0 not act=EVENT, or longer than 2.00s |
| 10 | hold placement | a 3.2s hold on a low-energy act |
| 11 | blends | outside 6–33%, or width outside 240–560ms, or `dip` (fades through black) |
| 12 | caption zone | any card y in 0.34–0.60 — where the subject lives |
| 13 | reference plates | plate below 4k, missing, or a human shot with no persona plate |
| 14 | prompt quality | prompt missing the realism block or never citing the plate |
| 15 | quality defaults | `fast` mode, burned-in AI label |
| 16 | shot mix | **WARN only** — deviation from profile, printed with its reason |
| 17 | cost | total against a **measured** balance |

**Checks 7 and 8 are the ones that matter most**, because they are *relational*. Every
defect ever found by eye in this project was a relationship between shots, not a bad shot.
The first Supra plan passed all fifteen original checks and still had 12% of its punch-ins
in the first half and 67% in the second — a video that gets visibly softer as it plays.
A per-shot cap cannot see that.

**Check 16 warns rather than blocks** on purpose. The profile came from references that do
not necessarily stop a scroll either. A deviation may be the point — but it must be
*declared*, never silently passed.

> Run it on the LC300 and it **fails**: crops of 1.85/1.90/1.95 against a 1.40 cap. That
> video shipped before the punch-in measurement existed. The plan was kept faithful rather
> than quietly corrected — a plan that lies about what was built is worse than one that fails.

---

## STAGE 3 · BOARD — `board.py`, rendered FROM the plan

Numbers do not catch everything. Drawing the LC300 board caught one clip carrying 4 of 14
shots and a lighting arc that contradicted the comment above it. Drawing the Supra board
caught the punch-in drift that fifteen numeric checks had passed.

The board has no content of its own — every label, colour, length and note is read out of
the plan module, so the picture **cannot** disagree with the code.

---

## STAGE 4 · GENERATE — the only stage that costs money

```
PLATES ALWAYS 4k          nano_banana_pro defaults to 1k. 4cr vs 2cr, against a 180cr build.
PLATE PROMPTS AS PHOTOS   camera, lens, aperture, ISO, lighting + the artefacts only real
                          photos have: clear-coat orange peel, pores, panel-gap shadows
NAME NOTHING, DESCRIBE IT "swan-neck wing" returned a generic GT wing on straight pedestals.
                          "two curved arms rise from the deck, arch UP and OVER the wing,
                          bolt to its UPPER surface, NOTHING underneath" returned the right
                          part. Jargon is not a spec. Cost: 4cr and one wasted plate.
VIDEO IN std, NEVER fast  22.5cr/5s vs 17.5. Never chosen silently to save money.
PROBE THE HOOK FIRST      generate shot 0 alone, LOOK at it, then commit the rest.
                          22.5cr told us the Supra event was half-missing instead of 180cr.
LOOK AT EVERY PLATE       against the plan's own must_show list, at native resolution.
```

**The probe is the highest-leverage habit in the whole pipeline.** It has already paid for
itself twice.

---

## STAGE 5 · BUILD — `engine.py`, one file for every video

Everything that varies is in the plan. Everything true of *every* cut is here, and every
one of those truths was paid for:

```
[1/7] PHASE, not just tempo   the bed's first transient is at 163ms — there is NO downbeat
                              at t=0. Trimming to it took cut-to-music 31.8ms -> 3.3ms.
[2/7] CUT ON ACTION           clipsense returns action_peaks_s, "the moments a pro cuts on
                              or into". Nothing read it for weeks; shots 0/1/9 contained no
                              peak at all — and shot 0 is the hook. Now 14/14 land on one.
      FRAME-EXACT             -frames:v N, never -t. `-t 0.80` on 24fps source yields
                              0.834s at 30fps — +34ms/shot, ~130ms adrift by 15s.
      CACHE ON FULL SPEC      keyed on file|tin|dur|crop|cx|cy. A duration-only key once
                              silently reused untreated segments.
[3/7] SHOT MATCH FIRST        on the RENDERED segment, never the source: a 1.9x punch crops
                              into the dark part of frame, so source B averages 73.7 while
                              its punch renders at 50. Gain = Δlevel/255 × 1.9, clamped
                              ±0.085 — match, never relight.
[4/7] BLENDS                  section punctuation only, 240–560ms. Never `dip` — it fades
                              through black and legitimately trips the blank-frame gate.
[5/7] COVERAGE                HISTOGRAM CORRELATION, not pixel difference. A punch-in moves
                              every pixel while showing nothing new: mean |diff| flagged
                              0 of 13 cuts, hist-corr flagged 7.
[6/7] GRADE                   saturation ONLY. The prompts already ask for crushed blacks,
                              so the footage ARRIVES graded — adding contrast took pixels
                              below value 4 from 7.7% to 40.0%.
      CAPTIONS                y=0.72 lower third. The subject is always centre.
[7/7] SFX                     whoosh LEADS the cut by 220ms — a whoosh RESOLVES on the cut.
                              The bed SIDECHAIN-DUCKS under it, or the layer is mixed to
                              inaudible while the build prints "9 whoosh + 4 impact".
      ATOMIC WRITE            .part.mp4 then os.replace. A killed run left a 532KB file
                              with no moov atom that ffprobe refused entirely.
      DECLARE ACTUAL CUTS     post-blend, never planned. Blending merges pairs, so 13
                              planned became 9 actual and verifying against the plan
                              compared two frames INSIDE the same shot.
```

---

## STAGE 6 · GATE 2 — `verify.py`, 10 checks

**Check 0 is freshness and it runs first**, because a build that times out before its atomic
write leaves the previous render on disk — and every number measured afterwards is fiction.
That happened, and the numbers were reported as new.

```
0 freshness        output newer than the build script and every source clip
1 qc.py profile    all 16 profile fields, not the 2 it used to read
2 cut-to-music     median |deviation| from the nearest onset
3 sfx audible      crest-factor LIFT at the cut (≥2 dB) — never peak-vs-bed-RMS
4 repetition       histogram correlation across each cut
5 exposure match   level swing across each cut (>18 fails)
6 caption zone     CARD positions read from the build, not guessed from pixels
7 action peaks     every shot lands on a real motion peak
8 audio            LUFS · true peak · silence ratio
9 true black       mean<4, because the "blank" gate measures BLUR and calls it black
```

---

## MEASURED: THE GENERIC ENGINE vs THE 530-LINE SCRIPT IT REPLACED

Same six clips, same plan, run end-to-end on 2026-08-01:

| | bespoke `build.py` | generic `engine.py` |
|---|---|---|
| cut-to-music | 31.8 ms median · 78% within 50ms | **3.3 ms · 100%** |
| SFX transient lift | +4.6 dB | **+5.7 dB** |
| exposure | 0/9 cuts >18, worst 15 | 0/9, worst 15 |
| repetition | 1/9 | 1/9 |
| qc profile | PASS | PASS |
| **verdict** | 10/10 | **10/10** |
| lines of per-car code | 530 | **0** |

**Three bugs the end-to-end run found, that reading the code did not:**

1. **`shot_match` gain formula rewritten from memory.** I used a ratio approximation instead
   of the original Δlevel/255 × 1.9. Under-corrected badly: one cut still swung 22, and the
   qc profile check failed downstream of it. *Ported faithfully, re-ran, both cleared.*
2. **Sub-drops landed on hold EXITS, not entries.** The original indexed the cut list
   directly; I translated to shot indices without stating the convention. Cost 2.5 dB of
   transient lift (+4.6 → +2.1, against a 2.0 floor). *Convention now stated in the engine
   and both plans: `IMPACT_AT`/`SUBDROP_AT` are SHOT indices, the sound lands on the cut
   ENTERING that shot.* Result: **+5.7 dB, better than the original.*
3. **Blends re-rendered on every run.** No cache. *Added a spec-keyed cache; a no-change
   rebuild is now 27s.*

---

## WHERE IT CAN STILL BITE

| risk | status |
|---|---|
| **0 posts.** Every retention target is a hypothesis. | **the #1 gap, unchanged** |
| No check measures whether anything *happens* — only conformance | check 9 is a proxy, not a solution |
| A full build exceeds a single 45s sandbox call | mitigated by the cache; not solved |
| `qc.py`'s blend detector disagrees with the engine's own count (30% vs 10%) | two different definitions of "blended" — unreconciled |
| I deleted `manifest_peaks.json` during a cleanup and lost the evidence | regenerated by the engine now |
| Video decoding is unavailable in the browser automation context | clips must be uploaded manually to reach the sandbox |

---

## THE ONE-LINE VERSION

Everything expensive is fenced by something free. The plan gate costs nothing and blocks
generation; the probe costs 22.5cr and blocks the other 157.5; the verify gate costs nothing
and blocks delivery. What is still missing is at the end of the chain, not the middle:
**one real 24-hour retention curve is worth more than every number in this document.**
