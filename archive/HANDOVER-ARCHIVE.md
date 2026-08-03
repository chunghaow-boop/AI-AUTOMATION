# HANDOVER ARCHIVE — append-only
### Rolled-off state from 22-HANDOVER.md. Never deleted, never rewritten.
### Claude appends here when the handover exceeds 200 lines. Read only when history is needed.

---

## 2026-07-21 — first archive entry (system build sessions)

**Resolved threads (closed, kept for reference)**
- POV recond salesman — 4 beats generated, assembled 3× (v1 raw / styled / V2 with 5 passes).
  Verdict: system test passed, video was average. Root cause = POV is the model's weakest format.
- Urus "Summoning" hook test (17.5cr) — FAILED. Frame 1 rendered empty despite the prompt
  saying "ALREADY half-materialized" AND negatives listing `empty starting frame`.
  → produced the phrasing-trap law: **only a start_image guarantees frame 1**.
- Urus × Nev cinematic (67.5cr) — PASSED. 9 shots, correct Urus, wardrobe held. RHD unverified.
- Audio v1 → v2 — mono→stereo, −20→−14.8 LUFS, boom fixed. Midrange REGRESSED 12.8%→10.9%.

**Superseded approaches (do not repeat)**
- Clip-by-clip generation for cinematic work → superseded by the file-17 multi-shot template.
- Long negative-prompt lists on multi-shot → they cause failures; specificity replaces them.
- Synthesised SFX from sine/noise → measured hollow. Real library is the fix.
- Mask/object-wipe transitions on multi-shot output → seams don't exist, nothing to hide.

**Credit history**
Session start ~2,990 → cameraman 135 → Urus test 17.5 → Urus×Nev 67.5 → ~2,425 at handoff.


## 2026-07-23 — auto-archived from handover (cap exceeded at 207 lines)

## DELIVERABLES ON DISK (re-upload only if you want to keep working on them)
```
URUS_x_NEV_FINAL.mp4        15s · dissolve register · captions + foley   ← the polished one
URUS_x_NEV_BEATCUT.mp4      15s · beat-cut v1 · MONO audio (superseded)
URUS_x_NEV_BEATCUT_v2.mp4   15s · beat-cut · stereo, -14.8 LUFS          ← best beat-cut
POV_recond_salesman_V2.mp4  14.1s · all 5 edit passes, synthesised audio
urus_hero_startframe.png    best car render this project produced — use as a start_image
caption_card_demo.png       Playwright styled-caption proof
```



## 2026-07-24 — auto-archived (handover hit 211 lines)

### WHAT'S PROVEN (full detail)
- ✓ **Multi-shot single generation** (file 17) — 1 prompt = 9 shots/15s, in-model dissolves.
  **Supersedes clip-by-clip for all cinematic work.** Cheaper, seamless, no drift.
- ✓ **No negative prompts** on multi-shot. Specificity crowds out failure; negatives broke Urus v1.
- ✓ **Phrasing trap: negatives DO NOT fix it.** Only a `start_image` guarantees frame 1.
- ✓ POV/first-person = **weakest format**. Wow capped at 5. Use real footage or Motion Control.
- ✓ Talking head (Recipe 7) = **zero credits, highest trust**. Check this preset FIRST.
- ✓ Playwright renders styled caption cards (transparent PNG → FFmpeg overlay). Beats drawtext.
- ✓ Beat-cut edit works — 450 frames = exactly 15.000s, librosa confirms 119.7 BPM.
- ✗ **My synthesised audio is bad** — measured mono, body 15.8% (target 35-45%), centroid 3383Hz.
  Real SFX/BGM library is the fix, not more synthesis.



## 2026-07-24b - archived (handover 221 lines)

## WHAT'S PROVEN (full detail in /archive/)
- ✓ **ASSET PRE-PRODUCTION (file 23)** — build a four-view/expression/nine-grid **scene asset
  library FIRST**, generate video FROM it. Fixes identity + scene drift at the root. New Phase 1.5.
- ✓ **Multi-shot single generation** (file 17) supersedes clip-by-clip for ALL cinematic work
- ✓ **No negative prompts** on multi-shot — specificity replaces them
- ✓ **Phrasing trap: only a `start_image` fixes frame 1.** Negatives do nothing
- ✓ POV = weakest format (wow capped 5) · Talking head = zero credits, highest trust
- ✓ Playwright caption cards · beat-cut lock (450 frames = 15.000s exactly)
- ✗ **Synthesised audio measured bad** — real SFX/BGM library is the fix, not more synthesis



## 2026-07-24c - archived (handover 221 lines)

## GITHUB SYNC + AUTO-ARCHIVE PROTOCOL

**Repo layout**
```
/                     RUNNER.md · 00 … 22 (the live system)
/archive/             HANDOVER-ARCHIVE.md  (rolled-off history, append-only)
/outputs/             finished mp4s, start-frames  (optional, large)
```

**Reading — automatic, Claude does this**
```
git clone --depth 1 https://github.com/<user>/<repo>.git /home/claude/sys
```
✅ verified: clone works · raw.githubusercontent.com 200 · **api.github.com is 403-blocked**

**Writing — the user does this. Claude CANNOT push** (pushing needs a personal access token,
and Claude is not permitted to handle credentials/tokens). Claude prepares files; user commits.

**⚡ THE 200-LINE AUTO-ARCHIVE RULE**
This file is capped at **200 lines**. Claude checks the count at the END of every session:
```
1. wc -l 22-HANDOVER.md
2. If > 200:
     a. Move the OLDEST RESOLVED content (closed threads, superseded facts, old deliverables)
        into /archive/HANDOVER-ARCHIVE.md — APPEND, with a date header. Never delete.
     b. Keep in 22: project facts · contract · what's proven · the NEXT SESSION steps ·
        file index · session rules. These never get archived.
     c. Re-check the count. Repeat until under 200.
3. Report the new line count and hand the user both files to commit.
```
**Never trim by deleting facts.** Archive is append-only and permanent; the handover is a
working surface. A fact that survived one archive round is load-bearing — keep it.

**⚠️ WHAT SURVIVES WHAT**
```
Chat compaction  → files SURVIVE (they live on disk, not in the conversation). No action needed.
Ending the chat  → sandbox RESETS, all files GONE unless committed. ← the real deadline
```
Claude cannot detect either event and does not run between messages. **The user must trigger
the ritual by saying "wrap up" / "I'm closing" before ending a session.**

**End-of-session ritual — Claude runs this whenever the user signals wrap-up, or unprompted
after any session where 3+ files changed**
```
□ update 22-HANDOVER: balance · open threads · what changed · next steps
□ append to 09-learning-log if anything was learned
□ wc -l 22-HANDOVER.md → archive to /archive/ if >200 lines
□ rebuild AI-AUTOMATION-SYSTEM.zip  (all .md + archive/ in one file)
□ present the zip and say: "download this, drag into GitHub, commit"
```
**The zip is the whole system in one drag-and-drop** — GitHub's web upload accepts it unzipped
into the repo root, or the user unzips locally and commits the folder. One action, not 26.



## 2026-07-24d - archived (handover 232 lines)

## SELF-QC - run before any handoff (catches drift)
```
[] Higgsfield:balance      -> record the REAL number, never estimate (was once off 352cr)
[] grep stale counts       -> log entries / file counts / bank sizes vs actual
[] grep contradictions     -> a doctrine arguing with its own measured finding (-14 vs -7)
[] grep gate values        -> /50 vs /60 drift after a rule change
[] grep deps on cut files  -> anything still referencing a file marked for removal?
[] RE-WALK after fixing    -> a fix pass CREATES defects. Proven: a regex corrupted a bank count
```

