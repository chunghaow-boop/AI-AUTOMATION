# TALYX AI VIDEO AUTOMATION — project instructions
Local Claude Code loads this automatically. Read `GATE.md` and `PROMPTS.md` before any build.

## WHAT THIS IS
Fully-AI short-form video for a Malaysian recond-car audience. Three formats — **vlog · car
review · industry value** — all generated, fronted by a consistent AI KOL persona (Nev).
Platforms: Facebook · TikTok · Instagram.

## THE CONTRACT (the one rule)
```
User gives a TITLE. Derive everything else.
PHASE 1  free + autonomous  → target, beats, gates, shot list, cost preflight
⏸ ONE GATE: full prompt verbatim + scores + exact cost → WAIT for approval
PHASE 2  paid + autonomous  → generate, edit, gate, deliver. No further stops.
```
Use the `/talyx-shotlist` skill for Phase 1.

## HARD RULES
1. **Evidence before claims.** Every audio/pacing claim cites a measurement. "Sounds good" with
   no number is fabrication. Tools exist for exactly this — use them.
2. **MEASURE the credit balance, never estimate.** A past estimate was off by 352cr.
3. **Mechanical beats judgement.** If a check can be a number, it must be. Judgement is fallback.
4. **After any fix, re-run the check.** A fix pass creates new defects (proven twice).
5. **5 failures on one problem → stop and ask.** Never loop and burn credits.
6. **Rank options, name the pick, one line why.** Never hand over a flat menu.
7. **Claude PULLS from GitHub; the USER PUSHES.** Never claim you can commit — no credentials.
8. **Frames and spectrograms ARE the work.** View them; never ask for a text summary instead.

## COST DISCIPLINE (the binding constraint)
720p std **4.5cr/s** · 1080p **9cr/s** · Seedance max clip **15s** · fast 720p/5s = 17.5 flat.
Naive 60s = 270cr. Three pillars weekly = **3,240cr/month**.
**Generate only the moments that MOVE.** Carry runtime with stills + `zoompan` + VO + captions
(≈145cr for 60s). Probe hooks at 17.5cr before committing 135. See `PROMPTS.md`.

## IDENTITY — ANY NAMED SUBJECT, not just the persona
**A named subject is never generated from text alone.** Persona OR product OR place.
Generate a REFERENCE PLATE first (`nano_banana_pro`, ~2cr), LOOK at it, confirm it is the
right thing, then pass it as `start_image` / `image_references` on every shot.

> Why this is stated explicitly: this rule existed scoped to "AI persona builds" and was not
> applied to a car. A text-only prompt for "2026 Toyota Crown" returned a generic crossover,
> and it shipped. A 2cr plate would have prevented an 87cr build from being wrong.

Character sheet is the permanent `start_image` on every shot. Past 15s, chain: last frame of
shot N becomes `start_image` of shot N+1. Verify with `tools/facecheck.py` on every seam.
`generate_audio: true` for talking formats — the old "silent always" rule is obsolete.

## PLAYWRIGHT — standing rule
**Whenever a task involves rendering, the web, or anything visual, reach for Playwright first.**
It is installed locally (blocked in the Cowork sandbox — browser binaries 403, same as Whisper).

Current uses:
- `tools/cards.py` — HTML/CSS → PNG cards at 1080×1920. **Replaces ffmpeg drawtext**, which is
  the weakest visual element in the output. Templates: punch · title · checklist · ladder ·
  cta · lower-third.
- **The Artefact Drop** (the top-performing Douyin mechanic) depends on this: a genuinely
  screenshot-able checklist people SAVE. drawtext cannot produce that quality.

Also use it for:
- reference harvesting — screenshot competitor posts/thumbnails for `reverse.py` and `intel.py`
- rendering `qc-console.html` to an image for review
- thumbnail/cover generation from HTML templates
- any future "study this page/video" task — render, screenshot, then measure

## PIPELINE
```
/talyx-shotlist  →  ⏸ approve  →  generate (Higgsfield)
  →  tools/transcribe.py      word-level transcript      (local only)
  →  tools/autocut.py         filler/retake/pause cuts, hook pick, word-exact captions
  →  tools/edl.py auto        build → render → gate → auto-amend (max 3 loops)
  →  GATE.md stage 1          mechanical gates, all must pass
  →  deliver WITH the numbers →  predict retention  →  resolve at +24h
```

## THE STANDING GAP
Nothing has ever been posted. Every retention figure is engineered-for, not measured.
`pacing.py`'s estimate is a structural heuristic and says so in its own output.
**One posted video with a real 24-hour curve is worth more than any prediction in this repo.**

## DISCLOSURE
AI content must be labelled on TikTok/Meta. An undisclosed AI persona risks both a platform
penalty and the trust the whole channel depends on. Non-negotiable.

---

## SESSION PROTOCOL — added 2026-08-04
The chat is disposable; the repo is the memory. Session end: Claude updates the
newest RESUME-*.md + commits, Gavril pushes, chat cleared. Session start: pull,
read CLAUDE.md + the NEWEST RESUME-*.md, continue. Claude keeps token cost down:
one combined evidence sheet per review, logs tailed to verdicts, minimum LOOKs.

AUTO-SAVE RULE (his standing order): Claude commits after EVERY meaningful state
change without being asked (already habit), and — because Claude cannot push or
clear the chat — Claude WATCHES THE SESSION WEIGHT and, whenever a milestone
lands (gate passed, build delivered, ~10+ images accumulated, or the limit
banner appears), proactively says: "RESUME updated + committed — run PUSH.bat
and clear the chat now." Gavril's whole job is those two clicks. Claude never
waits to be asked for a handover.

## ADDED 2026-07-31 / 08-01 — READ THE NEWEST `RESUME-*.md` FIRST (08-04 latest)

The balance line above ("1,850.68cr") is stale. **Measured 2026-08-01: 5,967.02 cr, plan
`team`.** Measure it again before spending; hard rule 2 was broken once by estimating.

### RULE ZERO
**Edit plan before generation. IDEA before edit plan.** The plan lives as DATA in one file
(`i8_plan.py`), never duplicated across a board, a doc and a build MAP.

### THE CINEMATIC PILLAR
`build_lc300_cinematic.py` is the working reference implementation; read its comments.
Short/music-led cuts to the BEAT; long/speech-led cuts to the SENTENCE. Never mix.
`car_cinematic` = 0.77s median shot, 44.7 cuts/min, 20% blended, 140-170 BPM drift phonk.

### QUALITY DEFAULTS — never accept the API's
```
PLATES ALWAYS 4k         nano_banana_pro defaults to 1k. 4cr vs 2cr.
VIDEO IN std, NEVER fast never chosen silently to save money
PUNCH-INS <= 1.4x        1.9x measured an 82% loss of sharpness
GRADE ~1.15 THEN MEASURE never double-grade; the prompt may already crush blacks
COVERAGE >= shots / 2.5  cut rate must be EARNED
FRAME-EXACT CUTS         -frames:v N, never -t seconds
CAPTIONS y=0.72          lower third. Never centre - the subject lives there.
```

### GATE BLIND SPOTS — proven, do not trust these alone
- `mastermind` is a **frame** inspector, not an **edit** inspector. Every defect found by
  eye was RELATIONAL — it never asks whether two shots belong together.
- A build that times out before its atomic write leaves the PREVIOUS render on disk.
  **Check freshness first** (`verify.py` CHECK 0) or every number is fiction.
- Verify against ACTUAL post-blend cut boundaries, never the plan. Blending merges segments.
- SFX audibility = crest-factor LIFT at the cut (>=2 dB), never peak-vs-bed-RMS.
- The blank-frame gate measures BLUR and calls it black. Smooth leather trips it.

### RUN BEFORE ANY DELIVERY
```
python3 verify.py     10 checks, one verdict, freshness first
```

### THE STANDING GAP, RESTATED
Ten mechanical checks pass and the output still would not stop a scroll. Every check
measures conformance to a profile; none measures whether anything HAPPENS. TikTok Q2 2026
ranks 3-second retention above watch time; hooks under 2s show 23% higher completion. Open
on an EVENT, not a tour. Still 0 posts.

---

## THE TITLE CONTRACT — added 2026-08-03, agreed with Gavril

A title is a COMPRESSED brief. The mastermind never goes title → plan directly. The
sequence, mandatory, all steps before any credit:

```
1 TITLE          "car cinematic of toyota supra with nev inside it"
2 REFERENCE SCAN web-search the title's genre: what do the top edits for this exact
                 subject actually do — opening move, hero feature, event vocabulary?
                 PLUS reverse.py on assets/refs/ for the measured cutting DNA.
                 Scraped references are for UNDERSTANDING, never for generation input.
                 The job is: see the field standard, then IMPROVISE ABOVE it — name
                 explicitly what ours does that the references do not.
3 READBACK       show Gavril: (a) what the title LOCKS (pillar, subject, persona),
                 (b) the 2-4 decisions it leaves OPEN as fixed choices with a
                 recommended pick, (c) the upgrade-over-references in one line.
                 Proven necessary: "toyota supra" alone → I would have guessed
                 standard A90; he meant Final Edition. A wrong guess here poisons
                 every downstream artefact.
4 HIS PICKS      30 seconds of his time. Cheapest disambiguation in the pipeline.
5 PLAN           plans/<name>.py, with a CONTENT block (claim + verification source,
                 twist, why_stop) that planqc REQUIRES.
6 GATES          planqc -> JUDGE PANEL ON HOOK **AND STORY ARC** (file 01/06, FREE, verdict
                 recorded in the plan's CONTENT block - restored 2026-08-04 after Gavril
                 caught that the merge had dropped the pre-spend J0/Wow step) -> board
                 -> approve -> probe -> generate -> clipqc -> build -> verify -> JUDGES
                 on the cut.
```

Two failure modes, kept separate on purpose:
- MISREADING THE TITLE — fixed by steps 2-4 (readback + picks + board).
- CRAFT ERRORS — a correctly-understood title can still produce an overloaded 5s clip
  (shot A: door + engine in one clip, 22.5cr). Fixed by the probe, never by more questions.

## MERGED WITH THE DESKTOP SYSTEM — 2026-08-03
Read `RECONCILE.md`. One flow now: Strategist readback (file 08) -> Four Gates as CONTENT
block (file 01 / planqc 18) -> probe -> clipqc -> engine -> verify 10 -> JUDGES (file 06,
LLM reception gate - kills boring, which no mechanical check can) -> Gavril. Plans may set
GEN_MODE = "coverage" (beat-cut phonk pillar) or "multishot" (file 17, 67.5cr dissolve film).
Persona = references only; product = describe the geometry.

### STORYBOARD RULE — added 2026-08-04, his standing order
"I want the storyboard to be full and detailed with images as reference." Every gate
presentation ships the FULL PRODUCTION.md, generated from the plan (never typed beside
it), containing: previz image sheet (identity-ref'd) + timeline board + every verbatim
generation prompt + the complete edit treatment (cut grid, blends, SFX map, cards,
grade, mix) with computed times + cost. The timeline board upgrades itself to REAL
frames as clips arrive.

### PREVIZ RULE — added 2026-08-04
Storyboard previz (the cheap 1cr nine-panel sheet) is sketch-grade and NEVER enters
generation. But if the persona appears in ANY panel, the sheet MUST carry the identity
reference — a text-only previz invented a stranger and was correctly rejected ("the man
is not nev"). Persona = references, always, even in sketches.
