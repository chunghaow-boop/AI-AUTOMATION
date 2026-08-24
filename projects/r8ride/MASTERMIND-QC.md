# MASTERMIND FINAL BOSS QC — R8RIDE picture-lock
### File 27 procedure, run 2026-08-14 · build `projects/r8ride/r8ride_rough.mp4`
### 720x1280 · 24fps · 664 frames · 27.667s · h264 crf16 + aac 256k

---

## PART 0 — THE PREDICTION PASS (written before looking)
From the plan's PREMORTEM and the ledger, this build's likely small mistakes:
1. the C trim lands mid-action and reads as a yank — **partly true, see A/5**
2. A and C are both macro-on-suspension and will feel like the same shot — **TRUE, the one real eye finding**
3. the foley spread will collapse in the mix — **false, it survived (B/2)**
4. blacks crushed by the generator's own grade — **false once measured properly (C)**

---

## PART A — THE EYE PASS

| # | check | verdict |
|---|-------|---------|
| 1 | Rig leaks | **CLEAN** — no light stands, softboxes or crew in 21 frames sampled |
| 2 | Identity | **CLEAN** — Nev in B and F: face, centre-part, navy pixel-check over black tee. Car is the R8 (side blade) in all five car shots |
| 3 | Duplicate feel | **FINDING — see below** |
| 4 | Hook | frame 0 is A, a gloved hand already on the damper. An EVENT, but the oil reveal resolves at ~2.5s, not at 0 |
| 5 | Action resolution | 5 of 6 cuts land at a clip's natural end. **C cuts at 3.077s mid-thread** — a consequence of the earned trim, accepted |
| 6 | Cards | **CLEAN** — 3/3 on screen, spelling exact, white pill / dark text at y=0.13 (the car_review register the plan declared), never clipped, act-timed to shots 0/2/5 |
| 7 | Softness | **N/A** — no punch-ins in this build |
| 8 | Grade | **CLEAN** — luma arc 98.6 → 106.3 → 100.8 → 93.9 → **112.9** → 86.9. Workshop, then the road as the brightest point, then the cabin as the darkest. Reads as one day |
| 9 | Text in frame | **CLEAN** — no plates, badges, signage or screen text legible anywhere |

### A/3 — THE ONE REAL EYE FINDING
**Shots A (0.00–4.92s) and C (14.75–17.83s) are near-identical framings** — both macro
into the wheel arch, both a gloved hand on a damper, same lens, same light, same angle.
The entire point of the pair is the contrast **wet vs dry**, and at a glance they read as
the same shot returning. The film's central claim is carried by a difference the framing
actively hides.

Not fixable by editing — it is a framing decision made at generation. Options, ranked:
1. **Accept for V1** (pick) — the cards and the sound carry the distinction, and D sits
   between them so they never touch. 0cr.
2. Regenerate C from a different angle (side-on, damper vertical) — 22.5cr, and it would
   genuinely fix it.
3. Reorder so they sit further apart — impossible, the story order is already correct.

---

## PART B — THE EAR PASS *(measured; not listened to — no audio monitoring in this environment)*

| # | check | measured |
|---|-------|----------|
| 1 | Layer balance | per-shot RMS −18.11 / −19.98 / −19.72 / −17.61 / −17.63 / −18.09 dBFS. Plan targets hit within ±0.6 dB on 5 of 6; **B is 2.4 dB under** its target |
| 2 | Moment balance at the cut | −4.0 dB into D and +4.4 dB into C — these are the plan's design (D = the silence on the turn at −9, C = the hero at −4), not drift |
| 3 | Continuity | **CLEAN** — 17/553 windows ≥6 dB under median, **0 sustained runs ≥0.25s**. No dropouts, no stepping ducks |
| 4 | Diegetic truth | **NOT JUDGED** — requires listening |
| 5 | Character | **True peak −3.7 dBTP**, spec ≤ −1.0 → passes with 2.7 dB margin. LRA 2.8 LU |

### B — THE BLOCKING PROBLEM
**Integrated loudness −19.4 LUFS against a plan target of −11.0. The film is 8.4 LU quiet
because it has no music bed and no SFX sweeteners.** The plan declares this film
MUSIC-LED (`SOUND['bed']`) with three bank one-shots on the sound-critical moments —
the bolt crack, the torque click, the engine taking load. None of them are in this file.

Cause is environmental, not editorial: `assets/bank` (6.4 MB) and `assets/bgm` (20 MB) are
binary and gitignored, so they exist only on the local machine, and the two sandboxes that
can reach the clips and the assets respectively have no route to each other.

---

## PART C — MEASUREMENT TRAPS HIT THIS RUN
**One, and it would have been a false alarm.** The 1st-percentile luma reads 1.0–2.0 on
four of six shots, which looks exactly like crushed blacks against the plan's
`TARGET_BLACK = 10.0`. Measuring the actual distribution instead of the percentile:
only **0.4–1.5 % of pixels sit at ≤2**, and ≤16 covers 3–9 %. That is ordinary deep
shadow in a workshop macro, not clipping. **p1 answers "where is the floor", never "how
much is on it"** — and reporting the first number as the second would have sent a
correct film back for a grade it does not need.

---

## VERDICT

```
PICTURE      PASS   — order, cards, grade arc, identity, text all clean
SOUND        FAIL   — -19.4 LUFS vs -11.0 target: the bed and 3 sweeteners are absent
EDIT         PASS   — one earned cut, justified; 5 of 6 shots whole; transitions as planned

VERDICT      FIX FIRST — do not treat this as the deliverable.
             It is PICTURE-LOCKED and one command from finished.
```

**The fix is not an edit-loop iteration.** Per his own scope rule the loop re-edits and
never regenerates — but this defect is neither: the edit is correct and the assets are
simply not reachable from here. So the loop stops and says so, which is what it is for.

### One command, on the machine that has the assets
```
python3 tools/build_r8ride.py --stage full
```
It will find `assets/bank` and `assets/bgm`, lay in the bed and the three sweeteners at
the video times the plan now carries (6.12 / 17.62 / 18.65), and write the real mix.
If the assets are missing it refuses to pretend — it prints why and writes the rough cut
instead, because a silent downgrade is how a defect reaches his eye.

### Then, before it goes to him
```
TALYX_PROJECT=r8ride python3 verify.py
```
Check 21 CARD PRESENCE is new this session and has been proven in isolation
(band 40.70 visible vs 0.91 invisible) but has **never executed against a real build** —
its measuring branch needs the clips and the film in one place. Treat its first green as
unproven until it has run once here.
