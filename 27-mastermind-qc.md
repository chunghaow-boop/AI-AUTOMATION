# [FINAL BOSS] MASTERMIND QC — the strictest gate, top to bottom
### File 27 · Created 2026-08-04 · REWRITTEN 2026-08-05 after the first travel_vlog build.
### Runs AFTER every mechanical gate passes. The mastermind is the FIRST planner and the LAST judge.
### Companion: `ledgers/knowledge.json` — this file is the PROCEDURE, the ledger is the EVIDENCE.

---

## WHY THIS SEAT IS THE FINAL BOSS

Builds that passed every mechanical gate and were still caught by his eye or ear:
duplicated footage, a softbox in frame, the hook dissolving mid-event, a bed breakdown
reading as silence, ducks stepping, whoosh sand, an inaudible Nev, an invented badge,
and — on the first vlog — **five shots that were one image**.

**Every one became a measured cause, then a permanent gate, the same day.**

```
Mechanical gates prove CONFORMANCE.  The mastermind judges whether it is
REALISTIC, SMOOTH, and ALIVE — then converts every miss into the next gate.
```

---

## PART 0 — THE PREDICTION PASS (NEW, 2026-08-05. Run this BEFORE looking at anything.)

His standing order: *predict the bug before it appears.* Every defect below was found by
eye AFTER a build. Each now has a question that would have caught it at PLAN time, free.
**Answer all of these in writing before the eye pass. An unanswered one is a miss waiting.**

| # | Ask this | Because | Gate |
|---|---|---|---|
| P1 | Does any two sources share a PLATE without declaring different framings? | A plate anchors PLACE *and* FRAMING. 4 sources cited one waterfront plate → 5 shots, one image. | planqc 28 |
| P2 | Is any source used more than once? Does its prompt say the camera KEEPS MOVING? | A locked-off clip gives every window the same picture. Measured: static sunset self-similarity 0.975 → tracking 0.871. | prompt rule |
| P3 | Does the story span more than one LIGHT STATE? | A time-of-day arc legitimately spans 60 luma; shot-match cannot close that, and reordering for luma destroys the story. Expect exposure fails and DECLARE them. | verify 5 |
| P4 | Will any shot contain SIGNAGE, BADGES or SCREENS? | Models write gibberish on every legible surface. "SDNMONES", "TOARAKNMN", an invented 'SR' badge. J4 has an ABSOLUTE veto. | clipqc text-zoom |
| P5 | Is any threshold in play tuned on a DIFFERENT pillar? | Night luma band rejected daylight; 1.5 motion floor rejected serene shots; 3-word cards blocked the vlog's own caption style. | planqc 26 |
| P6 | Does the bed come from THIS pillar's bank, and has its tempo been MEASURED? | A vlog at 105 BPM silently resolved to a 150 BPM phonk bed and would have built successfully. | engine verify_bed_tempo |
| P7 | Does every declared CALLBACK have the footage to land? | A "car leaves" callback pointed at a window with no car in it — the same image as the hook. | eye, PART A3 |
| P8 | Which constants am I about to change, and were they MEASURED? | Widening a measured clamp on a plausible argument made exposure WORSE (9→16 swings). *(That result was itself a symptom of P9 — see below.)* | ledger |
| P9 | For every stage that ADJUSTS the source: what is its authority in the UNIT HE SEES, and does it re-measure its own output? | The edit relit a shot he called "close to perfect" from 44 to 117 luma and crushed nine others by −46, because the gain formula assumed a fixed response of 134 luma/unit when the MEASURED response is 174–519. Open-loop correction on a guessed constant. | verify 15 |
| P11 | For each boundary: what is DIFFERENT on the far side of it, and does shot B inherit that difference? | His doctrine: *"there must be a linkage that is important, when there is linkage then it feels like a story."* KK v15 declared 19 linkages and 14 were descriptions of RESEMBLANCE — same warmth, same blue hour, two stillnesses. Resemblance is continuity; it stops a cut being jarring. Only CONSEQUENCE makes a story. | planqc 29, 31 |
| P12 | Does every linkage name a token that appears in the WRITING of both shots it joins? | Boundary 15→16 declared "the car returns"; the shot note for 16 said "the place, EMPTIED". The plan contradicted itself in writing and shipped — free to catch, one build after P7. | planqc 29 |
| P13 | Does every shot declare its light state, and does the sequence ever run backwards? | KK v15 ran golden → night → daylight → morning under a "6PM" card. The premortem promised "no cut jumps backwards in time" and nothing enforced it, because no shot ever said what time it was. | planqc 30 |
| P14 | Is the linkage list DERIVED from the final shot order, or authored beside it? | KK's list was written against the storyboard order; the built cut reused 9 sources 2-3× each, so boundary 12→13 was boundary 5→6 again and half the list described a video that was never assembled. | planqc 29 |
| P10 | Whose look is authoritative — the model's or the edit's? Has he ever said the raw output was good? | He did, verbatim, on 2026-08-05. His three approved raws span 45.1–92.9 mean luma; a 47-luma spread is INSIDE his approval band, so any stage pulling to one median is destroying the thing he likes. | style: shot_match_mode |

---

## PART A — THE EYE PASS (one combined evidence sheet: contact strip + spectrogram)

Look for exactly these, in order. Each has shipped or nearly shipped.

1. **Rig leaks** — softbox/light stand in ANY frame (shipped at 1.8s once).
2. **Identity** — is it HIM? Face, hair, EARRING; the car is THE car.
   ⚠️ **CLAUDE CANNOT JUDGE THIS.** On KK the verdict FLIPPED between crop scales —
   "not him" at thumbnail size, "plausibly him" at matched size, same frames, same
   session. Claude's job is to present plate-crop and delivered-window-crop side by
   side at matched scale. **The verdict is Gavril's, always.**
3. **Duplicate FEEL** — now MEASURED (verify 13), but the eye still owns the final call.
   The metric is blind to colour by design; it can miss and it can false-positive
   (a boardwalk's receding lines scored 0.913 against a grill grate — nothing alike).
4. **Hook** — frame zero is already an EVENT. Resolution ON SCREEN, never inside a blend.
5. **Action resolution** — no cut while motion is still rising.
6. **Cards** — legible, act-timed, lower third, never clipped, spelling exact.
7. **Softness** — punch-ins ≤1.4x; watch the SECOND half for drift.
8. **Grade** — coherent look, blacks not crushed, no exposure flicker at cuts.
9. **TEXT IN FRAME** (NEW) — read EVERY legible string: signage, badges, screens,
   number plates. Gibberish is the single fastest way to lose J4.
10. **INTENT vs RENDER** (NEW) — read the plan's shot note against the actual frame.
    "NEV grin" delivered no grin. "The car again" delivered no car.

## PART B — THE EAR PASS (headphones, then phone speaker)

1. **Layer balance** — read the SOUND ENGINEER table, then LISTEN.
2. **MOMENT balance, not averages** — judge the cut INSTANT. Averages lied twice.
3. **Continuity** — no dropouts ≥6dB/≥0.25s; no stepping ducks; no breakdown mid-video.
4. **Diegetic truth** — the launch sounds like a launch; the market sounds like a market.
5. **Character** — no sand, no mud, no mono, TP ≤ −1 dBTP MEASURED ON THE DELIVERED FILE.

## PART C — MEASUREMENT TRAPS (the checks themselves fail; all verified)

```
NORMALIZE-UP        scaling to peak BOOSTS what you just quieted            (x2)
AVERAGE-vs-MOMENT   layer RMS said "6dB under"; at the cut it was ON TOP
STALE CALIBRATION   a check tuned on old material fails honest new work
PLANNED-vs-ACTUAL   blends compress the timeline; verify rendered boundaries
STRETCHED AUDIO     always re-measure the stretched file (149.5 != 150)
DELIVERED WINDOW    gate what PLAYS, not the clip head            (3 false rejects)
BLUR-AS-BLACK       the blank gate measures blur; smooth leather trips it
AAC OVERSHOOT       true peak exists only in the delivered encode
GENRE-vs-REFERENCE  a bare phonk bed is 70-89% sub-low BY GENRE
FIX CREATES DEFECTS every fix pass re-runs every check
VACUOUS PASS        a check that measured NOTHING must FAIL, never OK   (8 of 13 did)
COLOUR-BLIND-METRIC NCC and pHash miss identical framing under a colour shift;
                    strip the dimension the eye is ignoring
SILENT NO-OP        a script reporting "patched 20" that changed nothing.
                    READ THE EDITED LINES BACK AND ASSERT.
OPEN-LOOP GAIN      a correction stage that APPLIES a computed gain and never
                    re-measures its own output. The luma response of ffmpeg
                    eq=brightness was assumed fixed at 134/unit; MEASURED 174-519
                    (3.0x spread, content dependent). 17 of 20 shots overshot and
                    landed on the FAR SIDE of the target. Every adjust stage must
                    RE-MEASURE, and keep the untouched original as a candidate.
SMOOTH NUMBER       a metric improved by DESTROYING the input. Exposure-match got
                    its number by relighting an approved shot +72 luma. Ask what
                    the check had to break to pass.
UNIT HE CANNOT SEE  authority declared in opaque units (ffmpeg "brightness 0.14")
                    hides its real size. State budgets in the unit he perceives -
                    luma - or nobody can tell 12 from 72.
OVER-DETERMINED     when a new constraint makes a rule-set INFEASIBLE, prove it by
                    backtracking and drop one rule at a time to name the binding one.
                    Then change the SHOT, never loosen a measured rule.
```

## PART D — CLOSE THE LOOP

For EVERY miss, all three, same day:
1. **FIX** it now, then re-run every gate (a fix pass creates new defects).
2. **LEDGER** it — craft goes in `general craft`, genre goes in its pillar topic.
3. **MECHANIZE** it — plan-time if decidable from the plan (cheapest), clip-time if
   decidable from a clip, cut-time only if it needs the finished file.

**And add its question to PART 0.** A lesson that does not become a pre-flight question
will be rediscovered by his eye on the next build. That is the whole point of this file.

## VERDICT FORMAT

```
MASTERMIND QC — <project> <version>
PREDICTION   P1-P8 answered? (any unanswered = not ready)
PRE-FLIGHT   all green? (list any red -> stop)
EYE          pass/fail per A1-A10, one line each, timestamped
             (A2 identity: EVIDENCE ONLY — verdict is Gavril's)
EAR          pass/fail per B1-B5, one line each, timestamped
TRAPS        any check suspected of lying? which, why
MISSES       each -> fix / ledger# / new-check / new PART 0 question
VERDICT      SHIP to Gavril | FIX first (ranked list, pick named)
```

> The standing gap, always: every green check still cannot measure whether anything
> HAPPENS. One posted video with a real 24-hour curve outranks everything in this file.

---

## 2026-08-17 — TIER 0, ADDED BEFORE PART 0

His order: *"make sure the QC double check or triple check before showing the final output."*

**Run `python3 tools/predeliver.py <project> --video <file>` FIRST. If it does not exit 0,
this procedure does not start and he does not see the file.**

Why a tier had to go *above* the prediction pass: every check in this file inspects a film
that EXISTS. None of them asks whether the work that should have preceded it happened at
all. LOT reached him five times with **no plan file** — so CONTENT, TURNS, twist timing,
CARDS/CTA, LINKS and PILLAR_FIT never ran. They did not fail. They were never invoked, and
nothing reported their absence (L176).

**And one rule for PART A and PART B both:** when a mechanical gate reports a finding, open
the frames it names and LOOK before deciding anything. cutsense reported 19.9% repetition on
LOT_v3; I argued the metric was mis-scoped and moved on; he watched it and saw six
near-identical shots immediately. **A finding is closed by inspection, never by an
argument** (L177). Record what you saw — predeliver TIER 3 requires it.
