# TALYX AI VIDEO AUTOMATION — the lean system
Fully-AI vlog · car review · industry value, built on a consistent KOL persona.

## RUN ORDER
0. `HANDOVER.md` → **read first.** state, balance, what's open, what's blocked on you.
1. `RUNNER.md`   → **the spine.** intel → decide → ⏸approve → probe → generate → edit → gate → launch → resolve
2. `SOURCE-ROUTING.md` → **real vs AI per shot.** Film what you can, generate what you can't.
3. `PROMPTS.md`  → build the character sheet FIRST. Every generation depends on it.
4. `GATE.md`     → the scorer: mechanical gates, J0 veto, weighted /100, camera-quality gate
5. `tools/`      → mechanical checks; judgement is the fallback, never the default

## SETUP
Cowork sandbox: ffmpeg + numpy + opencv already present. No ASR (weights blocked).
Local Claude Code: run `bash setup-local.sh` → unlocks Whisper (word-level editing).

## THE TOOLS
| tool | does | replaces |
|---|---|---|
| `mastermind.py` | loudness, peak, dead air, blank frames, caption sync → score + gates | "sounds good" |
| `rhythm.py` | BPM, beat grid, ms deviation of SFX/cuts | "feels off-beat" |
| `pacing.py` | cuts/min per format, dead zones, hook motion, retention estimate | guesswork |
| `facecheck.py` | face drift across a seam | eyeballing |
| `edl.py` | AI editor: build → render → gate → auto-amend | manual ffmpeg |
| `reverse.py` | editing DNA of reference videos, diffed vs yours | "study their style" |
| `calibrate.py` | which prompt features predicted good output | reasoned weights |
| `intel.py` | trend watchlist → mechanisms → banks | ad-hoc research |

## STATE
Balance measured 1,850.68cr. Nothing posted yet — that is still the #1 gap.
