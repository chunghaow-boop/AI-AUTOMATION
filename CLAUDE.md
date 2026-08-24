# TALYX AI VIDEO AUTOMATION — project instructions
Local Claude Code loads this automatically.

> ## READ THESE THREE, IN THIS ORDER, BEFORE ANYTHING ELSE
> ```
> 1. this file              the rules and the contract
> 2. SYSTEM-MAP.md          the whole pipeline top to bottom - every file, every
>                           gate, every threshold, the plan->engine contract, the
>                           bug classes, the seats, the cost model.
>                           WRITTEN SO A NEW SESSION NEVER STARTS FROM ZERO.
> 3. the NEWEST RESUME-*.md where we actually are right now
> 4. 32-real-footage-editor.md   IF the job involves footage HE shot rather than
>                           generated clips. Every other seat assumes I wrote the
>                           prompt and therefore know the content. Real footage
>                           inverts that and breaks them silently.
> ```
> Then state where we are in ONE line and wait.
>
> **Do not re-derive the architecture by reading source.** It is already written
> down. Re-deriving it burns a third of a session before any work happens.
> If SYSTEM-MAP.md disagrees with the code, the CODE is right and the map is
> stale - fix the map and say so in the RESUME.
>
> Corrected 2026-08-06: this line used to read "Read `GATE.md` and `PROMPTS.md`
> before any build." **Neither file exists.** The first instruction every session
> read was a dead pointer - a large part of why every session started cold.

## MODEL
Sessions run on **Claude Fable 5** (renewed 2026-08-11). Earlier commit footers
that name a different model are historical artifacts of the tooling, not a
record of what is in use. Do not add model names to commit footers.

## WHAT THIS IS
Fully-AI short-form video for a Malaysian recond-car audience. Three formats — **vlog · car
review · industry value** — all generated, fronted by a consistent AI KOL persona (Nev).
Platforms: Facebook · TikTok · Instagram.

## THE QC IS THE FINAL BOSS. HIS EYE IS THE FINAL FINAL BOSS.
### His correction, 2026-08-12, and it sets the target for every gate in this repo:
```
"my eye is not the final check. The QC is the final check. If possible you don't
 need my eye to have the check. So the QC is the final boss, my eye is the FINAL
 FINAL boss."
```
The goal is NOT that his eye catches things. The goal is that his eye finds NOTHING,
because everything it would have caught was caught upstream. **EVERY DEFECT THAT
REACHES HIS EYE IS A QC FAILURE.** When one does, the fix is always the same shape:
name the layer that was never decided or never shown, add the check, calibrate it
against the defect, and ledger it. Never "I will look more carefully next time."

### NOTHING REACHES HIS EYE UNTIL PREDELIVER EXITS 0 — his order, 2026-08-17
```
python3 tools/predeliver.py <project> --video <file>     # three tiers, all must pass
python3 tools/predeliver.py --selftest                   # proves it blocks LOT_v5
```
His words: *"make sure the QC double check or triple check before showing the final output."*
```
TIER 1 EXISTENCE    did the work happen AT ALL? plan file · hook/turn/CTA named ·
                    transcript (if speech) · READ.md (if real footage). THIS is the tier
                    that catches the LOT failure - 5 versions shipped with NO plan file,
                    so 8 story gates were never invoked and nothing reported it (L176).
TIER 2 MECHANICAL   planqc · cutsense · verify · bedcheck.
TIER 3 INSPECTION   every tier-2 finding must be LOOKED AT and the look RECORDED.
                    An unexamined finding BLOCKS. Explaining a number away without
                    opening the frames it named is how six duplicate shots reached him
                    after cutsense had already reported them (L177).
```

## REAL FOOTAGE IS READ, NOT MEASURED — file 32, added 2026-08-17
Every other seat in this repo assumes GENERATED footage, where I wrote the prompt so I
already know what is in the clip. **Real footage inverts that**: the camera recorded
whatever happened, nobody declared it, and the clip is evidence that must be READ.
```
1 TRANSCRIBE FIRST     ASR IS THE ONLY SPEECH DETECTOR (L174). An energy detector called
                       a count-in, a false start, TWO MUSIC CLIPS and a bell "speech" -
                       23.1s of a delivered film. Model via Chrome -> Downloads (mounted)
                       -> sherpa-onnx in-sandbox. He runs nothing.
2 READ EVERY CLIP      6-12 frames as a time-ordered strip. ONE FRAME IS A THUMBNAIL, NOT
                       ANALYSIS (L178). An in-point chosen from a moment never seen is
                       invented, and HARD RULE 0 forbids it.
3 TEXT AT FULL RES     badges/plates/screens, one clip at a time. NEVER call a mirror from
                       a contact sheet - flipping a correct clip is a NEW defect and it
                       shipped twice (L179).
4 THEN NAME            hook · turn · CTA · flow - ALL FOUR COME FROM THE TRANSCRIPT in a
                       speech-led format. Motion metrics rank shots; they cannot read
                       intent (L175). B-ROLL FOLLOWS THE SENTENCE: when he says "X1", the
                       X1 is on screen.
5 THEN plans/<n>.py    with REAL_FOOTAGE = True, then planqc, then the board, then cut.
```
> His verdict on the version that skipped all five: *"you cannot see the meaning behind
> the motion."* He was right. Duration, motion, luma and dBFS describe a clip's PHYSICS.
> A count-in and a sentence have identical physics.

BULLETPROOFING IS NOT MORE CHECKS - IT IS PROVEN CHECKS (L169). Three gates written
in one session were VACUOUS and passed injected defects until they were tested. So:
```
python3 planqc.py --selftest <plan>     # injects known defects, proves each check FAILS
```
It prints PROVEN / UNPROVEN per defect, and the UNPROVEN list IS the untested surface.
A NEW GATE SHIPS WITH ITS NEGATIVE CONTROL IN planqc.DEFECTS, OR IT IS NOT SHIPPED.
Its own first run found two bugs inside the harness - that is the mechanism working.

THE LAYERS A PLAN MUST DECIDE (planqc 41, file 31 PART I):
  PILLAR_FIT · TRANSITIONS_PLAN or ALL_HARD_CUTS · CARD_REGISTER · FOLEY ·
  SFX_OVERLAYS or SFX_WAIVED · SOURCE_REFS/FACE_OPTOUT · LINKS
A waiver is a sentence, never a silence. And when a pillar is INHERITED, diff EVERY
style key against the film you are actually making — numbers inherit, style inherits,
and SOUND POLICY inherits (a talking-head format's edit_sfx='none' reached a workshop
film and left it with no sound effects at all).

## THREE ADJUSTMENTS HE MADE TO THE PIPELINE — 2026-08-12, binding
```
1 THE TITLE IS AN INTENT BRIEF, NOT A SUBJECT LINE
  Do not stop at what the video is ABOUT. Analyse what HE WANTS OUT OF IT.
  The title carries a wanted OUTCOME - what the viewer should feel, what the
  video is for, what it must achieve - and that reading goes in the readback
  and into the plan's CONTENT block. A plan that nails the subject and misses
  the intent has failed the title. ("nev daily vlog... hiking, exploring the
  cave" wanted THE PROCESS - and the first build gave the destination.)

2 JUDGE EVERY CLIP, NOT JUST THE PROBE
  The probe still goes first and alone (it protects the batch). But after the
  batch lands, EVERY clip is QC'd on its own merits - measured and LOOKED at -
  and each one passes or fails individually. A clip that fails is named, and
  the decision to regenerate or work around it is made before assembly, never
  discovered in the cut.

3 THE EDIT LOOP, AND THE THREE QC TIERS
  Automation runs ffmpeg rough cut -> sound -> polish -> EDIT QC GATE.
    · FAIL  -> the gate hands its ADJUSTMENTS back to step 1 (ffmpeg), then
               sound, then polish, then the gate again. Loop until it passes.
    · PASS  -> the file goes to MASTERMIND FINAL BOSS QC (file 27).
    · MASTERMIND FAIL -> back to step 1 again, same loop.
    · MASTERMIND PASS -> and only then -> HIM. THE FINAL FINAL BOSS QC, his eye.
               Then WAIT for his feedback, and feed it into the next adjustment.
  SCOPE, HIS WORDS: "this is only applicable for the video editing automation
  part." The loop re-EDITS. It never regenerates. If a defect cannot be fixed
  by editing, sound or polish, the loop STOPS and says so - regeneration costs
  credits and belongs back at the plan and his gate, not inside an automatic
  loop. Hard rule 5 still binds: five failed attempts on one problem -> stop
  and ask, never spin.
```

## THE PLANNING PHASE PLANS EVERYTHING — his statement, 2026-08-12, verbatim intent
```
1 RESEARCH   the relevant content, ANALYSE it, and say how it implements into OUR video
             (two scans: SUBJECT and FORM · the reference library is read, not just
              measured · assets/refs/<pillar>/refsense.json READ slots + PILLAR-PROFILES
              measured_spread carry open_grammar and text_register per pillar)
2 PLAN EVERY  prompts · the edit · effects · transitions · foley · BGM · captions and
  SINGLE      their REGISTER · the triple link at every boundary · the journey beats ·
  THING       the spine (three-act or kishotenketsu) · the promise and its payoff ·
              the clip package (which shots also stand alone as their own posts)
3 STORYBOARD  tools/storyboard.py → **BOARD QC runs automatically on the render**
              (his idea, 2026-08-12): deep-analyses the board itself - order,
              timing continuity, panel provenance, prompt fidelity against the
              plan, refs actually shown vs refs the plan names, pillar sanity,
              cards, triple links, cost arithmetic. A FAILING BOARD IS NEVER
              SHOWN TO HIM: it redirects to REPLAN → fix → planqc → regenerate
              the board → BOARD QC again. Only a passing board reaches his eye.
              WHY: both defects he caught on the kariayam board (a borrowed
              pillar name, a persona plate showing the wrong wardrobe) were
              found BY HIM, after all 45 PLAN checks passed - planqc reads the
              plan as DATA and nothing inspected the ARTEFACT he reads.
4 HE APPROVES the single gate
5 EVERYTHING  generation, editing, sound, polish, gates — they EXECUTE the plan.
  DOWNSTREAM  They never decide. If a downstream stage has to make a choice, that
              choice was missing from the plan and the plan is what gets fixed.
```
**Consequence, and it is architectural:** a decision belongs in `plans/<name>.py`, not
in a tool. CARD_REGISTER is the worked example — the plan names the caption register,
`tools/capcards.py` merely obeys. Any tool that decides something is a bug.

## THE CONTRACT (the one rule)
```
User gives a TITLE. Derive everything else.
PHASE 1  free + autonomous  → target, beats, gates, shot list, cost preflight
⏸ ONE GATE: full prompt verbatim + scores + exact cost → WAIT for approval
PHASE 2  paid + autonomous  → generate, edit, gate, deliver. No further stops.
```
Use the `/talyx-shotlist` skill for Phase 1.

## HARD RULES
0. **WHOLE CLIPS. THE EDIT IS THE ORDER.** His words, 2026-08-12: *"do not simply
   cut unless analyzed fully then cut. If not, just piece all the scene together
   fully and just add a simple transition."* The generated footage is GOOD; the
   editor is what breaks it. So: every scene plays whole, in an order that tells
   the story, joined by simple declared transitions. A cut is EARNED by written
   per-window analysis naming what the discarded seconds contain — never assumed,
   never to hit a runtime. **The title's duration is a REQUEST; this is an ORDER —
   when they conflict the film gets LONGER, not choppier.** Enforced by planqc 38
   (CUT_JUSTIFICATION / REUSE_JUSTIFICATION); profile-conformance checks 2 and 9
   report instead of block on a whole-clip film. Broken once on NIAH_V1 (5.04s
   sources chopped to 1.23s bursts, every source used twice) — he caught it, V2
   rebuilt whole-clip and the reorder fixed the ending defect for free.
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
and clear the chat now" AND NAMES THE EXACT FILE for the next chat (the newest
RESUME-*.md, also kept current in START-NEW-CHAT.txt). Gavril's whole job is those two clicks. Claude never
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
2 REFERENCE SCAN **TWO scans, both mandatory — SUBJECT and FORM.**
                 (a) SUBJECT: what do the top edits for this exact subject do —
                     opening move, hero feature, event vocabulary?
                 (b) FORM: what does this CONTENT TYPE structurally owe its
                     audience? Added 2026-08-12 after NIAH_V2: the subject scan
                     was done (Niah facts, cave shorts) and the form scan was
                     NOT, so a VLOG shipped with no journey — it cold-opened
                     inside the destination and never showed how he got there.
                     His words: *"people like to see videos that have process in
                     it."* A vlog's content IS the process: pack → travel →
                     arrive → the thing → the return. Skipping it deletes the
                     format's reason to exist. planqc 39 now blocks it.
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
                 twist, why_stop) that planqc REQUIRES. The CONTENT block is written
                 AGAINST file 31 (31-shortdrama-scriptwriter.md, added 2026-08-12 on
                 his order): K/J short-drama grammar, 7 rules + a 6-question
                 checklist the SCRIPTWRITER seat runs FREE at plan review.
6 GATES          planqc -> JUDGE PANEL ON HOOK **AND STORY ARC** -> SOUND ENGINEER QC
                 (file 19+04: foley/diegetic design judged BEFORE spend - added 2026-08-04
                 after the WRX shipped with edit-sfx only and Gavril caught it; clip audio
                 is generated and PAID FOR, the plan must decide how it is used)
                 (file 01/06, FREE, verdict
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

### STORYBOARD RULE — added 2026-08-04; RESTATED AND HARDENED 2026-08-12 (L141)
"I want the storyboard to be full and detailed with images as reference." / "Every
time after the planning phase, I want to see the storyboard."

**THE STORYBOARD IS `tools/storyboard.py`. Run it at EVERY gate. No substitutes.**
```
python3 tools/storyboard.py <plan>   →  projects/<plan>/analysis/STORYBOARD.html
```
Per-shot cards with timing/foley/camera/card + verbatim prompts + edit flow + cost.
Its honesty rule is binding: every image is a REAL FRAME, a PLATE on disk, or a red
MISSING panel — **an AI-sketch previz is NOT a storyboard and never ships at a gate**
(session 11 burned 2cr learning this; the tool already existed, built to his
2026-08-06 spec, verbatim in its header). Re-run after plates and after every clip
batch — panels upgrade themselves to real frames. The gate also ships PRODUCTION.md
(planqc-generated) beside it. Search the repo's tools BEFORE building anything new.

### PREVIZ RULE — added 2026-08-04
Storyboard previz (the cheap 1cr nine-panel sheet) is sketch-grade and NEVER enters
generation. But if the persona appears in ANY panel, the sheet MUST carry the identity
reference — a text-only previz invented a stranger and was correctly rejected ("the man
is not nev"). Persona = references, always, even in sketches.

## THE MASTERMIND LOOP — his doctrine, stated 2026-08-04, codified same day
The mastermind is the FIRST planner and the FINAL BOSS of QC, and the whole
system is a loop that must get better every generation:

```
1 PLAN      full detailed storyboard BEFORE any generation - including a
            PREMORTEM: predict the small mistakes this exact build will make
            (from ledgers/knowledge.json - 31 lessons and counting) and plan
            the fix INTO the plan. Sound (FOLEY/SOUND), overlays, ban spans,
            linkage - all decided pre-spend. planqc enforces what it can.
2 LINKAGE   every shot is planned to CONNECT to its neighbours - exit motion
            into entry motion, lighting continuity, direction - so the
            organizer (ingest.py manifest) hands the editor footage that
            already wants to join. Relational, planned, not discovered.
3 EXECUTE   organizer catalogs -> engine cuts/sounds/transitions to the
            declared mood -> mechanical gates (planqc 22 / verify 13) all pass.
4 FINAL BOSS mastermind cross-checks the FINISHED cut against the board and
            against realism/smoothness - strictest gate, after all others.
            THE PROCEDURE IS FILE `27-mastermind-qc.md` - read it, run it
            top to bottom, use its verdict format. Every miss it finds
            becomes (a) a fix now, (b) a LESSON in ledgers/knowledge.json,
            (c) where possible a NEW MECHANICAL CHECK.
5 LOOP      the next plan's premortem READS the ledger. A lesson that does not
            change the next build is not learned.
```

Proven today, five times over: every defect his eye/ear caught (duplicates,
softbox, blend-killed hook, bed breakdown, duck stepping) became a measured
cause, then a permanent gate or engine behaviour the same day. That cadence IS
the loop. BUILT 2026-08-04 (remote session 6): planqc 22 PREMORTEM (>=3 ledger-
cited risks w/ mitigations) / 23 LESSONS_ACK (plan blocks unless it acks the
ledger's exact current lesson count for its pillar topic) / 24 LINKAGE (an
intent per boundary; 24b measures brightness continuity once ingest.py records
luma/motion means — that ingest extension is the open TODO). plans/wrx.py is
the format demo. Same session: file 27 QC ran first time on v8 and caught an
invented 'SR' badge (lesson 35) → clipqc text-zoom crops + plan DELOGO +
engine delogo-at-segment-render, all live.
