# [FINAL BOSS] MASTERMIND QC — the strictest gate, top to bottom
### File 27 · Created 2026-08-04 from one day of his catches (8 builds, 34 ledger lessons).
### Runs AFTER every mechanical gate passes. The mastermind is the FIRST planner and the LAST judge.
### Companion: `ledgers/knowledge.json` (the living memory — this file is the PROCEDURE, the ledger is the EVIDENCE. When the ledger grows, extend this file.)

---

## WHY THIS SEAT IS THE FINAL BOSS

Eight consecutive builds today passed every mechanical gate and were still caught by
his eye or ear: duplicated footage, a softbox in frame, the hook dissolving mid-event,
a bed breakdown reading as silence, ducks stepping, whoosh sand, an inaudible Nev.
**Every one became a measured cause, then a permanent gate — same day.** That cadence
is the job: the mastermind finds what the numbers missed, then TURNS IT INTO NUMBERS.

```
Mechanical gates prove CONFORMANCE.  The mastermind judges whether it is
REALISTIC, SMOOTH, and ALIVE — then converts every miss into the next gate.
```

---

## PART 0 — PRE-FLIGHT (all must already be green; do not re-derive, READ them)

| gate | what it proves | what it CANNOT see |
|---|---|---|
| planqc 22 checks | plan-level craft + CONTENT + SOUND/FOLEY + transitions + capacity | taste, feel, whether anything HAPPENS |
| clipqc (delivered-window) | each clip usable in its USED window | relations between clips |
| verify 0 freshness | measuring the right file | — |
| verify 2 beat lock | cuts on the music grid (≤50ms, ≥70%) | whether the grid FEELS right |
| verify 3 sfx | cut marked (music-marked path on dense beds) | sand/character of the sfx |
| verify 10 far repeats | no duplicated footage windows | visually-similar-but-distinct shots |
| verify 11 transitions | seam on beat, no whole-frame smear | whether the cut point serves the action |
| verify 12 storyboard tally | cut == board (shots/windows/sources) | whether the board itself was good |
| SOUND ENGINEER table (build log) | layer balance vs bed anchor | moment balance the averages hide |

**If any is red, STOP — you are not the final boss yet, you are debugging.**

---

## PART A — THE EYE PASS (one combined evidence sheet: frame strip + spectrogram)

Look for exactly these, in order (each has shipped or nearly shipped):

1. **Rig leaks** — softbox/light stand in ANY frame (shipped at 1.8s once; ingest flags
   SUSPECT spans, but the eye confirms — the detector cannot tell a rig from a highlight).
2. **Identity** — Nev is Nev in EVERY appearance (face, hair, EARRING); the car is THE car
   (aero kit, scoop, wing). A text-only generation shipped a wrong car once.
3. **Duplicate FEEL** — windows may be provably distinct yet read as the same image
   (same source, static composition). Far-repeat check is pixel-level; the eye judges feel.
4. **Hook** — frame zero is already an EVENT in motion. No settle, no tour. The event's
   resolution must be ON SCREEN, never inside a blend (a blend dissolved the swerve once).
5. **Action resolution** — no cut while motion is still rising (allocator prefers resolved
   windows, but only ~80% enforceable; the eye owns the rest).
6. **Cards** — legible, act-timed, lower third, never clipped (a fallback once shipped
   "RU WON'T SELL YOU"), spelling exact, arc reads as a sentence.
7. **Softness** — punch-ins ≤1.4x; blend middles must not smear the whole frame; watch
   the SECOND half (drift of cropped shots was once 12%/67%).
8. **Grade** — night look coherent, blacks not crushed (>12% pure black = double-grade
   suspicion), no exposure flicker at cuts (worst offenders go to plan sequencing).

## PART B — THE EAR PASS (headphones, then phone speaker — the audience uses the phone)

1. **Layer balance** — read the build's SOUND ENGINEER table first, then LISTEN:
   bed anchor · edit-sfx at bed−6 · foreground foley at bed−2. His three catches in one
   day: foley 19dB under (inaudible Nev), whoosh sand at +18, bed drowning everything.
2. **MOMENT balance, not averages** — at each cut the duck lowers the bed WHILE the sfx
   plays: judge the cut INSTANT. Averages lied twice today.
3. **Continuity** — no dropouts ≥6dB/≥0.25s (engine covers arrangement gaps with
   SFX_OVERLAYS from the clips' own audio); no stepping ducks (smooth sidechain only);
   the bed segment must not contain a breakdown mid-video (segment scan chooses, ear confirms).
4. **Diegetic truth** — the launch SOUNDS like a launch (engine+spray foreground),
   idle under Nev, spray on rolling. Foley exists because it was PAID FOR at generation.
5. **Character** — no sand (noise sweeps sat too hot twice), no mud (77% sub-low shipped
   once), no mono, true peak ≤ −1 dBTP MEASURED ON THE DELIVERED FILE (AAC overshoots
   +1..3.4dB after the limiter — the pre-encode number is a lie).

## PART C — MEASUREMENT TRAPS (the checks themselves fail; verified today, do not relearn)

```
NORMALIZE-UP        scaling a track to peak BOOSTS what you just quieted (x2 today)
AVERAGE-vs-MOMENT   layer RMS said "6dB under"; at the cut instant it was ON TOP
STALE CALIBRATION   a check tuned on old material (sparse synth bed) fails honest
                    work on new material (dense real bed) - amend the CHECK
PLANNED-vs-ACTUAL   blends compress the timeline; verify against rendered boundaries
STRETCHED AUDIO     always re-measure the stretched file's tempo (149.5 != 150)
DELIVERED WINDOW    gate what plays, not the clip head (2 false rejects in one day)
BLUR-AS-BLACK       the blank gate measures blur; smooth leather trips it
AAC OVERSHOOT       true peak exists only in the delivered encode
GENRE-vs-REFERENCE  a bare phonk bed is 70-89% sub-low BY GENRE; the 45%-body
                    reference profile applies to the FULL MIX only
FIX CREATES DEFECTS every fix pass re-runs every check (proven repeatedly)
```

## PART D — CLOSE THE LOOP (this is the entire point)

For EVERY miss found, all three, same day:
1. **FIX** it now, then re-run every gate (a fix pass creates new defects).
2. **LEDGER** it — `ledgers/knowledge.json`, same day it is learned. Chat is disposable.
3. **MECHANIZE** it — if the miss can become a number, it MUST become a check
   (planqc if decidable from the plan; verify if from the file; engine if behaviour).
   Today produced 9 new checks this way. Judgement is only for what numbers cannot hold.

Then: the NEXT plan's PREMORTEM must read the ledger and predict this build's likely
misses with mitigations planned in. planqc will enforce (PREMORTEM / LINKAGE /
LESSONS_ACK — speced in RESUME, build next session).

## VERDICT FORMAT

```
MASTERMIND QC — <project> <version>
PRE-FLIGHT   all green? (list any red -> stop)
EYE          pass/fail per A1-A8, one line each, timestamped
EAR          pass/fail per B1-B5, one line each, timestamped
TRAPS        any check suspected of lying? which, why
MISSES       each -> fix / ledger# / new-check(or "judgement-only, why")
VERDICT      SHIP to Gavril | FIX first (ranked list, pick named)
```

> The standing gap, always: ten green checks still cannot measure whether anything
> HAPPENS. One posted video with a real 24-hour curve outranks everything in this file.
