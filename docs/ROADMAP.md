# ROADMAP — making the automation smoother, cheaper, faster
### Deep analysis 2026-08-03. Every claim below is measured from the LC300 + Supra builds
### or verified against the tools actually available. Ranked by impact ÷ effort.

---

## WHERE THE TIME ACTUALLY GOES (measured)

| sink | measured cost | fix |
|---|---|---|
| **Serial generation waits** | ~7 min per clip submit→poll→complete. 8 clips serial ≈ 45–55 min of waiting | **#1 below** |
| **Manual clip ferrying** | cost the whole of 07-31; still one manual upload batch per build (browser can't decode video, sandbox has no network) | batch it: ONE upload of all clips, not per-clip loops |
| Regeneration iterations | each retry = another full wait cycle | clipqc + tighter per-clip briefs shrink retries |
| 45s sandbox call limit | build needs 2–3 resumable passes | cache already mitigates; not fully solvable |

## WHERE THE CREDITS ACTUALLY GO (measured)

Supra so far: 30.5 cr spent, of which 26.5 cr (87%) was "learning spend" — the discarded
plate v1 and the diagnosed shot-A probe. **That ratio is the system working**: the same two
failures at full batch would have burned 184 cr. Credits do not leak at the gates; they leak
in **retries**, and retries shrink when the prompt asks for less per clip (the shot-A lesson:
one action per 5s clip, never two).

---

## THE RANKED ADJUSTMENTS

### 1 · PARALLEL GENERATION AFTER THE PROBE  — biggest wall-clock win, zero risk
Today clips are submitted one at a time and polled serially. After the probe passes, the
remaining clips share no dependencies — submit ALL of them, then poll once.
**8 clips: ~50 min → one ~8-min wait window.** No code needed; it is an operating habit of
the generation step.

### 2 · `clipqc.py` — per-clip gate at ingest  — biggest credit win
The gap between GATE 1 and GATE 2: today only shot 0 gets looked at; clips 2–8 enter the
edit unexamined. A bad wheel on clip D is currently caught by Gavril, after edit time is
spent. Per-clip, all mechanical:
duration/fps/resolution · opening-settle (motion in first 0.4s — AI clips settle) ·
event-resolves-by-2s for the hook clip · brightness vs plan palette · sharpness floor ·
face check via existing `facecheck.py` on persona shots.
**One clip failing = one 22.5 cr regen instead of a rebuilt edit.**
New verb: `talyx.py ingest <name>` — runs clipqc on everything in `clips/`, PASS/BLOCK per file.

### 3 · CARDS VIA PLAYWRIGHT, NOT drawtext  — biggest visible quality win, desktop only
`engine.py` line 306 uses ffmpeg drawtext. The project's own CLAUDE.md standing rule says
drawtext is "the weakest visual element in the output" and `tools/cards.py` (HTML/CSS →
PNG at 1080×1920) replaces it. Playwright is blocked in this sandbox but installed on the
desktop — so the engine should try cards.py and fall back to drawtext with a loud warning.
This is also what the Artefact Drop mechanic depends on.

### 4 · CLOSE THE 0-POST GAP WITH THE TOOLS THAT ALREADY EXIST  — biggest strategic win
Discovered in the connected Higgsfield MCP, unused:
- `tiktok_connect / tiktok_prepare_publish / tiktok_publish` — posting can run through the
  pipeline. Per-post approval stays with Gavril (and the AI-content toggle stays a human step).
- `tiktok_music_trending / tiktok_music_tune` — cut to a REAL trending sound instead of the
  synthesized phonk bed. Retention research says sound choice matters; the synthesized bed
  exists because nothing else was reachable. Use platform audio at publish; keep the bed for
  edit timing.
- A scheduled task can fire at +24h after posting: fetch the retention curve, write it to
  `ledgers/retention.json`, resolve prediction vs reality. **This is stage 9, automated.**

### 5 · UPSCALE THE FINAL CUT, GENERATE AT 720p  — quality per credit
`upscale_video` exists in the MCP. Preflight its cost before relying on it, but the shape is
right: generating at 1080p costs 2× (9 cr/s vs 4.5); upscaling ONE 20s final cut is a single
operation on the only file that ships. Same credits at generation, sharper delivery.
**Action: preflight `upscale_video` cost on the next finished cut, decide with the number.**

### 6 · `talyx.py ship <name>`  — one verb for the back half
Chain: `ingest → build → verify → strip render` and stop. Removes the human from the middle
of the mechanical section entirely; the human gates stay at plan-approval, probe review, and
final review. (`plan` and `verify` already exit non-zero, so the chain self-blocks.)

### 7 · RETENTION SCORECARD, HONESTLY NAMED  — the 30–50% goal, without fabrication
`retention_check` in verify: hook-under-2s ✓/✗ · event-resolves ✓/✗ · face-at-zero ✓/✗ ·
single-event-not-tour ✓/✗ · pause-point count · cut-rate vs profile. Labelled
**"conformance to retention research"**, never "predicted retention" — until real curves
from #4 start calibrating it. With 3–5 posted videos the same scorecard becomes a genuine
predictor fitted to HIS audience. There is no shortcut to that; anyone selling one is
selling a random number.

---

## WHAT NOT TO BUILD

- **A retention-percentage dial before any video has posted.** It would be a fabricated
  number, and optimising toward it is worse than having none.
- **More gates.** Two free gates + probe + final boss is the right shape; a third automated
  gate between build and verify would re-check the same measurements.
- **Auto-regeneration loops.** Hard rule 5: five failures on one problem → stop and ask.
  A loop that silently retries generation is a credit incinerator with good intentions.

## SEQUENCE

```
this week   #2 clipqc  →  #1 parallel gen on the Supra rebuild  →  #4 tiktok_connect + POST the LC300
next        #6 ship verb  →  #3 cards.py on desktop  →  #5 upscale preflight  →  #7 scorecard
```
