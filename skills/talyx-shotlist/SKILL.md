---
name: talyx-shotlist
description: Turn one title into a gated, generation-ready shotlist for a Talyx AI video (vlog, car review, industry value, or cinematic). Use when the user gives a video title or topic and wants the full Phase 1 worked through — angle, avatar, pillar, hook, beats, shot list, cost preflight — stopping at the single approval gate before any credits are spent.
---

# TALYX SHOTLIST

Their `/seedance-director-shotlist` in one command — but gated, costed, and format-aware.

## THE CONTRACT
User gives a TITLE. Derive everything else. **Phase 1 is free and autonomous. Stop at ONE gate.**

## RUN

### 1 · TARGET (never "for everyone")
Name: **AVATAR** (1 First-Car Kid · 2 Family Upgrader · 3 Resale Uncle · 4 JDM Dreamer ·
5 Silent Businessman) · **PILLAR + episode #** · **LANGUAGE MODE** (Clean EN · Manglish ⭐default ·
BM lead · CN/EN mix) · **FORMAT** (vlog · review · industry · cinematic).

### 2 · THE FOUR BEATS + LOOP
Fork from the nearest swipe exemplar — never start blank. Name the source out loud
("borrowed from X") — declared remix reads as craft literacy, not theft.
```
HOOK   type + WOW/TWIST inside 2s        VALUE  which of the 6?
TWIST  what makes them SEND it            CTA    one ask
LOOP   last frame → first frame
```
**CTA routing by platform:** FB → comment war · IG/Reels → **DM send** (most weighted signal) ·
TikTok → completion/rewatch loop.

### 3 · FREE GATES (rewrite until all pass — costs nothing)
```
□ frame 1 = something HAPPENING, not someone POSED   ← #1 killer
□ idea detonates ≤1.5s   □ WOW or TWIST in frame 1   □ ≥1 value type
□ twist makes the sharer look good   □ CTA loops to hook   □ legible SOUND OFF
```

### 4 · SHOT LIST — banks before invention
Per shot: CAMERA (body + lens + T-stop, written literally) · PERFORM (weight, hands have a job) ·
EMOTION (the *conflict*, not the expression) · LIGHT (every source named) · TRANSITION (what is
physically continuous across the seam — if nothing, it's a jump not a transition) · SOUND.
**Pacing target:** vlog 15-25 cuts/min · review 8-15 · industry 6-12 · max shot 3/6/8s.
**Hard cuts, not dissolves** — dissolves don't interrupt a scroller.

### 5 · IDENTITY LOCK — persona AND named products/places
**Never generate a named subject from text alone.** Plate first (`nano_banana_pro` ~2cr),
view it, confirm, then `start_image` / `image_references` on every shot.
Plates live in `assets/pillars/<pillar>/plates/`. `clipgate` cannot verify a subject without
one — it passed two crossovers as a Toyota Crown and reported that it could not check.
Character sheet as `start_image` on every shot. Over 15s → chain: last frame of N = start of N+1.

### 6 · COST PREFLIGHT — use the cheap architecture
720p std 4.5cr/s · 15s max per clip. Generate only the moments that must MOVE; carry the rest
with stills + zoompan + VO + captions (see PROMPTS.md §cost architecture).
State: per-clip cost, total, and the balance after.

### 7 · J0 + THE GATE
Run `GATE.md` stages 2-4 on the plan. J0 ≥8 or back to the hook.

### ⏸ 8 · STOP HERE — THE SINGLE APPROVAL
Present: locked script · shot list · scores · **exact preflighted cost** · the hook-probe plan
(3 hooks × 17.5cr). **Wait.** The user's GO is the only spend authorization.

## AFTER APPROVAL
Generate → `tools/edl.py auto` (build → render → gate → auto-amend) → `GATE.md` stage 1
mechanical checks → deliver with the numbers → predict retention → resolve at +24h.

## RULES
- Evidence before claims. Never "should work" / "sounds good" without a measurement.
- Rank options, name the pick, one-line reason. Never a flat menu.
- 5 failures on one problem → stop and ask. Don't loop.
- Measure the balance, never estimate it.
