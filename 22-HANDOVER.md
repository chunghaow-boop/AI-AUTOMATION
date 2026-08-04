# HANDOVER — session state
### File 22 · READ THIS FIRST, before any other file. Hard cap 200 lines (auto-archives above).
### File 16 = architecture (what the system IS). This = state (where we ARE).
### Last updated: 2026-08-03 (laptop sync - see RECONCILE.md for the merged architecture)

---

## ⚡ STANDING ORDER — DO THIS WITHOUT BEING ASKED

**AT SESSION START — pull, don't wait to be told:**
```bash
git clone --depth 1 https://github.com/chunghaow-boop/AI-AUTOMATION.git /home/claude/sys
cd /home/claude/sys && bash tools/setup.sh
# then read 22-HANDOVER.md -> RUNNER.md. Nothing else unless a task needs it.
```

**AT SESSION END — back everything up, unprompted:**
```
1. update 22-HANDOVER.md   (balance MEASURED, open threads, what changed, next steps)
2. append 09-learning-log.md if anything was learned
3. wc -l 22-HANDOVER.md -> if >200, roll oldest RESOLVED content to /archive/ (append-only)
4. rebuild AI-AUTOMATION-SYSTEM.zip  (all .md + archive/ + tools/)
5. present the zip and say: "commit these"
```
**The split: Claude PULLS automatically. The USER PUSHES.** Claude cannot push — it requires a
personal access token and Claude is not permitted to handle credentials. Never claim otherwise.
Trigger the end-ritual on "wrap up" / "I'm closing" / "clear chat", or unprompted after 3+ files change.

## PROJECT FACTS (stable — verify only if something breaks)
```
Model:        seedance_2_0 · 9:16 · cinematics silent; TALKING formats generate_audio:true (old rule obsolete)
Rates:        1080p std 9cr/s · 720p std 4.5cr/s · 720p fast 5s = 17.5 flat
              15s cinematic: 1080p=135 · 720p=67.5
Decline:      preset 24bae836-2c4a-48e0-89b6-49fcc0b21612  (every job)
KOL refs:     96589a64-d346-4610-992e-532ef97517e8
              e3153edb-64a0-4276-a0c2-814ef0ae5cf5
              1b59b766-f08b-44b0-aba5-0e6ead2f99f3   (Higgsfield-side, re-upload if expired)
Soul:         Nev_KOL 7b917947-a6aa-44af-b0d2-401bd45adfd0 (image refs preferred over Soul)
Credits:      **5,852.16 MEASURED 2026-08-01 (laptop). Spending since - MEASURE at session start.** was 2,073.17 on 07-24. ⚠️ NEVER estimate this — a prior estimate
              was off by 352cr. Always run Higgsfield:balance and record the real number.
Repo:         https://github.com/chunghaow-boop/AI-AUTOMATION  (public, clone verified ✅)
              git clone --depth 1 https://github.com/chunghaow-boop/AI-AUTOMATION.git /home/claude/sys
Sandbox:      resets each session. pip install --break-system-packages librosa soundfile
Skills:       /mnt/skills/user/playwright · audio-analysis · **video-editing (autojumpcut + OCR)**
Content read: tesseract+chi_sim ✅ (solid-band text) · OCR fails on outlined captions over video
              → fallback: Higgsfield video_analysis (paid, works) · ASR (blocked) · ask user
⚠️ IMAGES:    if frames render blank, run a CONTROL image test first — if a self-made image with
              known content also renders blank, it's the session display bug, not the file.
⚠️ #1 ACTION: add **huggingface.co** to network egress allowlist → proper Whisper ASR
              (multilingual, subtitle-grade). Tested: hf 403 · openaipublic 403 · github 200.
              Fallback that DOES work offline: pocketsphinx (model bundled in pypi wheel)
              but measured ~30% accuracy, English only — gist only, never quotes/subtitles.
```

## THE CONTRACT (file 18 — the one rule that governs everything)
```
User gives a TITLE. Agent derives everything else.
PHASE 1 free + autonomous → decode, roles, banks, gates, J0, Wow Test, panel
⏸ ONE GATE: show FULL prompt verbatim + scores + exact cost → WAIT for approval
PHASE 2 paid + autonomous → generate, QC, reroll, edit, deliver. No further stops.
```

---

## WHAT'S PROVEN (detail in /archive/)
- ASSET PRE-PRODUCTION (23) - build four-view/nine-grid assets FIRST. New Phase 1.5
- MULTI-SHOT single generation (17) supersedes clip-by-clip for cinematics
- Phrasing trap: only a `start_image` fixes frame 1. Negatives do nothing
- POV = weakest format. Talking head = zero credits, highest trust
- Audio target is MEASURED, not theory: -7 to -9 LUFS, body 45%, air 4%, centroid 2400Hz

## HOW I "HEAR" (I cannot — this is the workaround)
`showspectrumpic` → PNG → **view it** · `ebur128` → real LUFS · librosa → BPM/onset/centroid (wav only)
**Every audio claim must cite a measurement. "Sounds good" without numbers = fabrication.**

---

## THE BIGGEST GAP
**Nothing has been posted. Ever.** Every retention target is engineered-for, not measured.
The outer loop (post → read 24h curve → calibrate) is the one part of the system with zero data.
Until one video ships, the whole thing is a simulator.

---

## DELIVERABLES
Best: `URUS_x_NEV_BEATCUT_v3.mp4` (mix rebuilt to the measured reference) ·
`urus_hero_startframe.png` (use as `start_image`). Full inventory in `/archive/`.

## ⚠️ IN FLIGHT WHEN LAST SESSION ENDED (2026-07-24)
```
VIDEO: "How to become a successful car influencer" - 30s = 2x15s stitch, 720p, Nev refs
  Part 1  a1c600fb-760c-4c51-8dd0-9dc1d2dc5791   fantasy->reveal   was STILL RENDERING
  Part 2  8a3e5989-60f5-44c6-91fa-54863fa3813c   method->CTA       DONE
  VO Marcus  8da286f2-3043-4576-9860-9dcc970b3c84  DONE
  VO Cillian c43f67b6-2fa8-4c97-813a-5f4201b6a9e1  unchecked
  Spent 139cr. Balance was ~1,934 (VERIFY with Higgsfield:balance, never estimate).
NOT DONE: QC, stitch, VO mix, caption cards, 5 passes, delivery.
USER MUST: download all 4 from higgsfield.ai and re-upload, then say "finish the influencer video".
VO SCRIPT (55 words): "Everyone thinks you need a supercar. You don't. The biggest car pages here
started with a phone and a second-hand Myvi. What they had wasn't money. It was one thing they
could say that nobody else could. Find yours. Say it every week. For a year. That's the whole
secret. What's yours? Tell me below."
CAPTION CARDS: 0.5s "everyone thinks you need a supercar" | 6s "you don't" |
  15s "it was never the car" | 26s "what's your one thing? tell me below"
KNOWN RISK: Parts 1+2 are separate generations -> Nev's face may DRIFT between halves.
  This is exactly what file 23 Phase 1.5 (four-view asset sheet) exists to prevent. It was
  SKIPPED on this run. If drift shows, that is the evidence - build the asset sheet first next time.
```

## ⚠️ HIGGSFIELD WIDGET FAILURE (seen 2026-07-24)
Widgets showed "Unable to reach Higgsfield" while jobs SUCCEEDED. Display-layer failure only.
**Workaround: call `job_display` and read the CloudFront URL out of the tool result, then give the
user the raw URL to download.** Do not assume a job failed because its widget is blank.

## ▶ NEXT SESSION — RUN THIS, IN ORDER

**STEP 0 · BOOT (30 sec)**
```
bash tools/setup.sh     <- ONE COMMAND. Restores librosa/OCR/ASR-check/espeak every session.
                           The sandbox wipes each time; this is the only install step needed.
tools/QUICKREF.md       <- the commands that do the work + measured audio targets
```

**GitHub pull**
```
FASTEST — user pastes the repo URL, Claude pulls everything itself:
    git clone --depth 1 https://github.com/<user>/<repo>.git /home/claude/sys
    (verified working: clone ✅ · raw.githubusercontent ✅ · api.github.com ✗ blocked)
FALLBACK — user uploads all .md files manually (works, just slower)

Claude reads:  22-HANDOVER.md → RUNNER.md.  Nothing else unless a task needs it.
Claude runs:   Higgsfield:balance          → confirm real credit number
               pip install --break-system-packages librosa soundfile   (audio work only)
Claude says:   one-line state + the 3 options below. No re-explaining the system.
```

**STEP 1 · CLOSE THE BIGGEST GAP — launch a video (highest value, ~0 credits)**
```
1a. User eyeballs URUS_x_NEV_BEATCUT_v2.mp4 at ~3.8s and ~7s → is the driver on the RIGHT?
       RHD correct → go to 1b
       LHD wrong   → reroll that clip only (67.5cr), or cut shots 3+5 and ship 7 shots
1b. Claude builds the launch package from file 15:
       caption · 3-5 hashtags · pinned comment (war-starter) · posting window (FB Reels 9pm MY)
1c. USER POSTS IT. Claude cannot post — this step is yours.
1d. +24h: user pastes the analytics (3s rate · avg % viewed · shares · comments)
1e. Claude overlays predicted vs actual per beat → logs the gap in 09 → THE LOOP FINALLY RUNS
```
> This is the only step that turns the simulator into a system. Everything else is more building.

**STEP 2 · REAL AUDIO (fixes the measured failure)**
```
2a. User downloads from file 20 (15 P1 SFX) + file 21 (16 priority BGM). Pixabay/Mixkit = CC0.
2b. User uploads them here (zip or batches). Save with the exact filenames in those files.
2c. Claude measures every file: duration · LUFS · spectral profile · true BPM (librosa)
2d. Claude rewrites file 12 from search-terms → real file paths
2e. Claude rebuilds the Urus mix as v3 with real sounds
2f. Claude runs the REVISION DELTA TEST v2 → v3
       PREDICTION ON RECORD: body 150-1500Hz rises 10.9% → 35%+
       If it does NOT, my diagnosis was wrong and the doctrine in file 19 needs revising.
```

**STEP 3 · NEW VIDEO (the contract, end to end)**
```
User gives ONE TITLE. Nothing else.
Claude: PHASE 1 free+silent → decode · avatar/pillar/language · hook (Bank 2) · twist (Bank 11)
        · CTA (Bank 7) · shot list · free gates · BUILD /60 · J0 veto · Wow Test · PANEL /60
        ⏸ GATE → full prompt verbatim + all scores + exact preflighted cost → WAIT
        PHASE 2 paid+silent → generate · QC · reroll (max 2) · Playwright cards · 5 passes · deliver
Defaults: file 17 template · 9:16 · 720p (67.5cr) unless hero · silent · KOL refs if humans
```

**PARKED (only if user asks — do not volunteer)**
```
Zach King trigger clip eca436a5 — never QC'd, needs the mp4
Cameraman video 253ea09f       — never QC'd, needs the mp4
Vellfire-vs-Alphard C build    — paused at clips 3-5, decide resume or drop
Cowork SFX-folder integration  — only after Step 2 proves real audio beats synthesis
```

## GITHUB + ARCHIVE (detail in /archive/)
```
Pull:  git clone --depth 1 https://github.com/chunghaow-boop/AI-AUTOMATION.git /home/claude/sys
Push:  USER ONLY - Claude cannot handle tokens. Claude prepares, user commits.
Cap:   this file 200 lines. Over -> roll OLDEST RESOLVED content to /archive/ (append-only).
       NEVER archive: project facts / contract / next-session steps / file index / session rules.
Ritual at session end: update handover -> append log -> check cap -> rebuild zip -> "commit these"
```

## FILE INDEX (26 + this one — `git clone` the repo, don't upload manually)
```
RUNNER  front door, the 12 steps        16  master skeleton (architecture map)
00  index          01  spine + Thai      17  car cinematic master prompt ⭐
02  crew + swipe   03  performance       18  agent contract ⭐
04  foley          05  cinematic spec    19  sound engineer
06  judges + J0    07  emotion           20  SFX download list
08  strategist     09  learning log (36) 21  BGM library list
10  editor         11  edit recipes      22  THIS FILE — read first
12  SFX bank       13  asset banks (~320)
14  audience/voice 15  launch protocol   23  asset pre-production ⭐
                                          24  system audit (keep/cut verdict)
                                          25  QC DEBATE + TOURNAMENT + [7B] Transition Master
                                          26  MASTER SCORECARD - weighted /100 ⭐ NEW
**HOW SEATS WORK NOW:** propose 3 (obvious/strong/uncomfortable) -> cross-examine -> winner ->
QC challenges the winner -> revise -> RE-challenge -> advance. 3 rejects = concept wrong. 5 = stop.
```
**FORMAT ROADMAP:** cinematic (proven) · **vlog · car review · industry value (all NEW, all
talking formats, all zero-credit).** 3 of 4 need no generation — see file 24.
**Seats:** 0 Strategist · 1 Scriptwriter · 1B Voice · 2 Director · 2B Performance · 2C Emotion · 2D MUA
(+image QC) · 3 DOP · 3B Foley · 3C Gaffer · **3D Sound Engineer** · 4 Technologist · 7 Editor ·
**J0 Hook Tyrant (solo veto)** · J1-J6 panel

## SELF-QC before handoff (full checklist in /archive/)
```
[] Higgsfield:balance - MEASURE, never estimate (was once off 352cr)
[] grep stale counts / contradictions / gate values / deps on cut files
[] RE-WALK after fixing - a fix pass CREATES defects (proven twice)
```

## SESSION RULES (learned the hard way)
1. **Evidence before claims.** Measure, then state. Never "should work" / "sounds good".
2. **5 consecutive failures on the same problem → STOP and ask.** Don't burn credits looping.
3. **After any fix, re-run the check on the fixed version.** One pass always misses.
4. **Rank options, name the pick, one-line reason.** Never hand over a flat menu.
5. **Frames and spectrograms ARE the work** — always view them, never ask for a text summary.
6. Don't declare a tool dead without testing it. (Called the sandbox dead once; it was alive.)

## ARCHIVE
`09-learning-log.md` (36 entries) = what was LEARNED. `/archive/HANDOVER-ARCHIVE.md` = what was
STATE. Both append-only, never deleted. See the 200-line rule above.
