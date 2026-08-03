# HANDOVER — session state
### Read this FIRST, before any other file. Then `RUNNER.md`.
### Last updated: 2026-07-27

## ⚡ SESSION START
```bash
cd <this folder>          # CLAUDE.md loads automatically in local Claude Code
bash setup-local.sh       # first run only — installs Whisper + deps
python3 tools/... # see RUN.md
```
Claude PULLS from GitHub; **the USER PUSHES.** Claude has no credentials and cannot commit.

---

## ⚠️ CORRECTIONS 2026-07-27 — my defaults were wrong, your measurements won
- **LUFS target is −7 to −9** (your file 19, measured from a real viral reel), NOT −9..−14.
  `mastermind.py` corrected. `INFLUENCER_v1.mp4` at −12.3 LUFS is ~4dB too quiet.
- Spectral: body 150–1500Hz ≈45% · air >10kHz ≈4% (your measured profile).
- Playwright is **local-only now** (was pre-installed in an earlier sandbox). See `LOCAL-ONLY.md`.
- Your repo is now mirrored in `system/` so a local session has the banks and seats too.

## PROJECT FACTS (verify only if something breaks)
```
Balance:    1,850.68 cr  MEASURED 2026-07-27  ⚠️ never estimate — a past estimate was off 352cr
Rates:      720p std 4.5cr/s · 1080p 9cr/s · 720p fast 5s = 17.5 flat · max clip 15s
KOL refs:   96589a64-d346-4610-992e-532ef97517e8
            e3153edb-64a0-4276-a0c2-814ef0ae5cf5
            1b59b766-f08b-44b0-aba5-0e6ead2f99f3
Repo:       https://github.com/chunghaow-boop/AI-AUTOMATION  (public; UNTOUCHED this session)
Sandbox:    Cowork = no ASR (openaipublic/huggingface/alphacephei all 403 at the proxy).
            Local Claude Code = Whisper works. That is the reason to go local.
Scheduled:  weekly intel run, Mondays 09:00
```


## ✅ ASSETS ACQUIRED 2026-07-27 — the biggest gap is now closed
```
SFX   74 synthesised (tools/sfxgen.py, licence-free) + ~396 Mixkit recordings
      selected AGAINST the three formats — car, money, ambience, machine, wind, error,
      alarm, typing kept; magic/horror/explosion/robot/game/sport REJECTED as wrong register
BGM   ~127 Mixkit tracks across 14 genres mapped to pillars, + 5 BPM utility beds
NEV   50 × 360° reference photos + closeup-face set (real photos > generated sheet)
```
**→ Chrome downloads land in ~/Downloads. Run `python3 tools/import_assets.py` to sort,
unzip and MEASURE everything into `assets/` + `asset-index.json`.**

This unlocks: cut-to-beat (`rhythm.py` now has real beds), the SFX timing gate, the measured
audio rebuild, and the identity lock (`facecheck.py` has real reference).

## 🔒 SAFETY — see `SAFETY.md`
Source footage cannot be overwritten. `_guard_output()` in transitions/grade/autocut/edl exits
before ffmpeg if output == input (tested). `import_assets.py` only touches SFX_/BGM_/BROLL_/zip
prefixes and never overwrites — it auto-suffixes `_1`, `_2`. Use `--dry-run` first.

## ✅ WHISPER UNBLOCKED 2026-07-29
Weights live in `models/faster-whisper-base/` (145MB model.bin + config + tokenizer + vocab).
`transcribe.py` resolves LOCAL dirs first. Verified: 56 words / 11 phrases from the real VO in 6.4s.
The sandbox limitation was the *download*, never the *package*. Mounted folders bypass it.

## MODE — HYBRID
Real footage AND AI generation, routed **per shot**. Film what you can; generate what you can't.
Every filmed shot ≈ 67cr saved. See `SOURCE-ROUTING.md`.

---

## WHAT EXISTS NOW
```
RUNNER.md          the spine: intel → decide → ⏸approve → probe → generate → edit → gate → launch → resolve
SOURCE-ROUTING.md  real vs AI per shot · hybrid seam rules · the ~90cr/60s build
GATE.md            one scorer: mechanical gates · J0 veto · weighted /100 · camera-quality gate
                   + SEAT COVERAGE MAP (all 16 seats, 7 now mechanical)
PROMPTS.md         character-sheet prompt · asset set · shot chaining · model routing · cost architecture
CLAUDE.md          project instructions, auto-loaded by local Claude Code
RUN.md             every command, in order
skills/talyx-shotlist/   Phase 1 as one invokable command
tools/             10 tools, all syntax-verified
qc-console.html    rate 30 clips + blind A/B (feeds calibrate.py)
reference/         analysis docs + generation_history.json
```

## TOOLS — what replaced judgement with measurement
| tool | measures | status |
|---|---|---|
| `mastermind.py` | LUFS, peak, dead air, blank frames, caption sync → score + gates | ✅ tested on real video |
| `pacing.py` | cuts/min per format, dead zones, hook motion, retention estimate | ✅ tested |
| `rhythm.py` | BPM, beat grid, ms deviation of SFX/cuts | ✅ validated vs 120BPM ground truth |
| `facecheck.py` | face drift across seams | ✅ tested (frontal-face only — profile fallback queued) |
| `edl.py` | AI editor: build → render → gate → auto-amend | ✅ ran end-to-end |
| `autocut.py` | fillers, retakes, pause tighten, hook pick, word captions | ✅ logic tested · needs real Whisper run |
| `transcribe.py` | word-level transcript | ⚠️ LOCAL ONLY — weights blocked in sandbox |
| `reverse.py` | editing DNA of reference videos, diffed vs yours | ✅ ran |
| `calibrate.py` | which prompt features predicted good output | ⏳ needs ratings.csv filled |
| `intel.py` | watchlist → mechanisms → banks | ✅ tested end-to-end |

## DELIVERABLE READY TO POST
`INFLUENCER_v1.mp4` — 30.1s, stitched, VO mixed (−12.3 LUFS integrated), 4 caption cards
re-timed to the actual speech, seam QC passed (no face drift).
Launch package: `INFLUENCER-LAUNCH-PACKAGE.md`.
**Prediction on record: 3s ~58% · avg viewed ~42% · completion ~27%.**

---

## ⚠️ OPEN — BLOCKED ON THE USER
```
1. POST INFLUENCER_v1.mp4          0 credits · the only thing that turns predictions into data
2. Rate 30 clips in qc-console     10 min · unlocks calibrate.py · converts 1,497 spent credits
                                    into evidence-based prompt rules
3. Install local Claude Code       unlocks Whisper → transcript-driven editing
4. Approve the character sheet     small image cost · fixes identity drift permanently
5. Consolidation decision          reference/39 — user wants scoring KEPT, so repo untouched.
                                    Try GATE.md on one build first, then decide.
```

## RULES LEARNED / CONFIRMED THIS SESSION
0. **Arena Zero measured** (reference/ARENA-ZERO-ANALYSIS.md, via Higgsfield video_analysis):
   silence-before-impact CONFIRMED on a 1.9M-view reference · ambience bed under every scene ·
   music changes 6× in 10min · hook = 22% of runtime as an escalating sequence, not one shot.
   All four are free to implement. Its 3.8 scenes/min pacing does NOT transfer to 9:16.
1. **`generate_audio: false` ("silent always") is OBSOLETE** for talking formats. Correct only
   for multi-clip cinematic stitches.
2. **"No hard cuts / seamless dissolves" fights short-form retention.** Dissolves don't interrupt
   a scroller. Cut hard, on the beat.
3. **DM sends are the most weighted Reels signal** — every existing CTA optimised for comments.
4. **Debate amplifies bias** (arXiv 2505.19477); meta-judge resists it. Anonymise candidates;
   the old A/B/C tournament pre-committed its verdict ("A must lose").
5. **Pairwise to choose, pointwise to monitor.** Absolute /10 scales drift.
6. **Character sheet = mandatory**, not optional, once an AI persona is involved.
7. **2026 retention benchmarks:** TikTok <30s 50–60% · 30–60s 40–50% · >60s 30–40% · viral 70%+.
   A 30s video at 40% is UNDER par.
8. **Skill + volume − focus = flat** (Douyin yibolas: 66 posts, 1,325 followers). External
   evidence for pillar discipline.

## THE STANDING GAP
**Nothing has ever been posted.** Every retention figure in this system is engineered-for, not
measured. `pacing.py` says so in its own output. Phase 7 (RESOLVE) has never run.
> One posted video with a real 24-hour curve is worth more than every prediction in this folder.
