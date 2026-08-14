# PIPELINE V2 — rebuilt from what actually went wrong
### Every rule below is traced to a specific failure in this session. No rule without a cause.

---

## THE ONE STRUCTURAL CHANGE

**Before:** gates *printed*. Delivery happened regardless. I was the gate, and I overrode myself.

> The Crown build generated a crossover instead of a Crown liftback. I saw it, wrote
> *"the car isn't a Crown"* in the delivery message, and shipped the file anyway.

**After:** delivery is a *return value*, not a decision.

```
verdict.run() -> PASS   file is written to output/
              -> BLOCK  file goes to work/quarantine/ + a .WHY.txt
                        output/ is left empty. There is nothing to hand over.
```

Re-run against the shipped Crown file, `verdict.py` blocks it on three hard gates —
including **2 blank frames** that no human or tool had noticed.

---

## THE FAILURE LEDGER — 23 failures, grouped by root cause

### A · The gate did not gate  (6)

| # | what happened | fix |
|---|---|---|
| A1 | wrong car shipped after I noticed it | `verdict.py` blocks; subject gate added |
| A2 | `gate()` returned nothing — could not block | verdict returns bool; delivery depends on it |
| A3 | `build_crown` never called mastermind at all | verdict is mandatory in every build's tail |
| A4 | no gate anywhere verified the **subject** | reference-plate similarity, or human sign-off |
| A5 | 2 blank frames never caught | blank-frame count is now a hard gate |
| A6 | v1 scored 66.7 "SEND BACK" — I delivered it | a SEND BACK verdict now quarantines the file |

### B · Silent failures — the worst class  (5)

Every one of these produced a *plausible* output while being wrong.

| # | what happened | fix |
|---|---|---|
| B1 | `drawtext` failed on the Windows path → shipped a clean video **reporting success** | prints `DO NOT POST THIS FILE`; verdict blocks when text was planned but absent |
| B2 | segment cache keyed on duration only → untreated segments silently reused | cache key includes the full treatment spec |
| B3 | `-shortest` deleted 8s of video silently | mix duration asserted against video duration |
| B4 | `alimiter` auto-level defeated `limit` — peak stayed at −0.0 dBFS | `level=disabled`; smoketest asserts default≠disabled |
| B5 | Chrome blocked multi-downloads; fetches "succeeded" | download one at a time, verify arrival by import |

**Standing rule:** a fallback that produces output must SHOUT. Silent degradation is the
single most expensive failure mode in this system — it cost four rounds of review.

### C · Untested code shipped  (4)

| # | what happened | fix |
|---|---|---|
| C1 | .bat shipped twice without ever being run | logic moved to Python; `.bat` is 9 lines |
| C2 | 16 tools syntax-checked, never executed | `smoketest.py` — 9 routes, real resolution |
| C3 | `transitions.py` crashed at 720×1280 (SAR mismatch) | `setsar=1` everywhere; all 9 regression-tested |
| C4 | `zoompan` frame-multiply bug in 3 places (hangs, +1.0s) | clamped; kept as an explicit smoketest case |

**Standing rule:** syntax-checking is not testing. Nothing is "working" until it has run.

### D · Planning gaps  (4)

| # | what happened | fix |
|---|---|---|
| D1 | quoted 17.5 cr/clip; default mode was 22.5 | `get_cost` preflight **before** every gate quote |
| D2 | **the Crown timeline had no transition field at all** — 8 hard cuts | transitions are a required column; verdict counts them |
| D3 | coverage crops produced repetition, not variety | adjacent-shot visual-difference check |
| D4 | prompted the car, not the *place* → studio void | location is a required prompt element |

### E · Measurement gaps  (4)

| # | what happened | fix |
|---|---|---|
| E1 | zero retention data; every target unvalidated | `retention.py` — predict, resolve, attribute |
| E2 | `ratings.csv` empty; `calibrate.py` never run | `styleref.py` captures every critique as a check |
| E3 | optical flow was the wrong proxy for "looks alive" | stopped optimising it; view frames instead |
| E4 | cut detector blind to same-palette cuts (3 of 14 found) | build reports KNOWN cuts; detector is cross-check only |

---

## THE PIPELINE

```
0  BRIEF        title in
1  RESEARCH     verify facts + the SUBJECT's real appearance          free
2  PLAN         shot list · transitions column · edit rules · foley   free
3  PREFLIGHT    get_cost on the EXACT params to be used               free
   ⏸ GATE       verbatim plan + measured cost + balance -> WAIT
4  GENERATE     locked reference plate on every named-subject shot
5  INGEST       one download at a time; import_bank sorts + renames
6  ASSEMBLE     segments -> transitions -> concat
7  SOUND        foley (content) -> bed (arranged) -> mix -> normalise
8  TEXT         captionmgr; fails LOUD
9  VERDICT      blocking. PASS -> output/   BLOCK -> quarantine/
10 LOG          retention.py logs features + prediction
11 POST         the only source of truth
12 RESOLVE      +24h curve -> attribute drops to shots
```

### Stage gates — all blocking

```
after 3   cost preflighted with the literal params        else no gate quote
after 6   duration == EDL   transitions rendered > 0      else stop
after 7   peak <= -1.0   loudness in band   gap present   else stop
after 8   text present if planned                         else stop
after 9   subject verified (plate OR human sign-off)      else quarantine
```

---

## THE SUBJECT GATE — and an honest limit

I cannot reliably tell a Toyota Crown from a Lexus RX by pixels. Pretending otherwise would
rebuild the same failure with extra steps. So:

- **with a reference plate** → similarity measured; below 0.45 blocks
- **without one** → the build blocks pending explicit human sign-off

**A named-product build cannot self-certify its own subject.** That is the whole point.
`assets/nev/` (50 images) now serves this for Nev. A car needs the same: a locked plate per
model, generated once, reused forever.

---

## WHAT THE MACHINE CANNOT CHECK — stated plainly

`styleref.py` holds 16 of his rejections. **8 are machine-checkable. 8 are not:**

```
machine-checkable   peak · captions present · bed present · foley present · blank
                    frames · duration · static shots · transitions rendered
NOT checkable       "doesn't match the feeling" · "stale and boring" · "needs design"
                    · "looks completely ugly" · composition · whether a shot is beautiful
```

Every round of this session, **his eyes caught what the metrics missed**. The gate's job is
to make sure he never has to report the same defect twice — not to replace him.

---

## THE THREE STANDING RULES

1. **Silent degradation is banned.** Any fallback that still produces a file must print a
   refusal loud enough to stop a post. B1 cost four review rounds.
2. **Syntax-checking is not testing.** `smoketest.py` runs before anything is called done.
3. **The verdict is not advisory.** If it blocks, there is no file in `output/` to argue with.

---

## STILL OPEN

| item | status |
|---|---|
| Crown build | **quarantined** — 3 hard gate failures |
| wrong subject (crossover ≠ Crown) | needs a locked plate + regeneration |
| **no transitions in the Crown edit** | timeline column added; needs rebuild |
| KK islands are karst, not Sabah | needs regeneration, ~17.5 cr |
| retention data | **zero posts. Every target in this repo is still a hypothesis.** |
