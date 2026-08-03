# THE AGENT CONTRACT — title in, finished video out
### File 18 · The actual spec. Read with RUNNER.md and 16-master-skeleton.md.
### This is what the whole 17-file system exists to execute.

---

## THE SPEC

```
/goal  INPUT:   one video title idea from the user. Nothing else.
                e.g. "the best recond car in the world"

       OUTPUT:  ONE finished, postable 9:16 video file —
                generated, edited, subtitled, transitioned, sound-designed.
                Not clips. Not a storyboard. A finished video.

       STANDARD: matches the proven reference tier (the Audi R8 cinematic,
                 file 17) — photoreal, cinematic, seamless transitions,
                 consistent subject identity across all shots.

       MUST CONTAIN: a visual hook that stops the scroll · a wow factor ·
                     a twist · a CTA · attractive subtitles · SFX · music bed

       RUN MODE: PHASE 1 (free) fully autonomous — decode, roles, banks, gates,
                 J0, Wow Test, panel, rewrites. No permission stops, no progress
                 narration. Output of this phase is a FINAL PROMPT.

                 ⏸ THE ONE GATE: show the FULL prompt (verbatim, complete) plus
                 the QC/inspector results and the exact credit cost. WAIT for the
                 user's explicit approval. This is the only stop in the run.

                 PHASE 2 (paid) autonomous after approval — generate, QC, reroll,
                 edit, assemble, deliver. Report credits as spent. No further stops.
```

**The user supplies a title. The agent supplies everything else.** Avatar, pillar, language, angle, hook, twist, CTA, shot list, prompt, edit, sound — all derived, not asked.

---

## THE CREW → TASK MAP (who does what when a title arrives)

| Task | Seat | Pulls from |
|---|---|---|
| Decode the title's real meaning | **Strategist** | Bank 1 (30 angles), kill-the-obvious |
| Pick who it's for | **Strategist** | file 14 — 5 avatars, 6 pillars, language modes |
| **Design the hook** | **Scriptwriter** | Bank 2 (35 hooks), two-layer rule, swipe S1–S7 |
| **Design the twist** | **Scriptwriter** | Bank 11 (24 patterns — Thai reframe + comedy) |
| Design the CTA | **Scriptwriter** | Bank 7 (31 CTAs) |
| Shot list + camera | **Director** | Bank 3 (30 moves) |
| Look, light, grade | **DOP + Gaffer** | Bank 6 (30 looks) |
| Human beats | **Performance + Emotion + MUA** | Banks 4, 5 + the 7-line image gate |
| Model, settings, cost, risk | **Technologist** | Bank 9 (27 presets) |
| **Write the generation prompt** | **Technologist** | **file 17 master template** |
| **Edit to final output** | **Editor** | file 11 (R1–R7) + file 10 (9 transitions) |
| **Subtitles** | **Editor** | file 11 caption style guide |
| **SFX + music** | **Foley** | file 12 (44 sounds) + beat→sound cheat |
| **QC + scoring** | **J0 + J1–J6** | file 06, Bank 8 (30 failure patterns) |
| Local accuracy | **J4** | Bank 10 (30 Malaysia/Sabah ground truths) |
| Launch | **Strategist** | file 15 |

---

## THE CHECKLIST — what "done" means

**Pre-generation (free, unlimited retries):**
- [ ] Angle is not derivative (kill-the-obvious)
- [ ] Free gates pass: frame 1 happening not posed · detonates ≤1.5s · two-layer hook · loop <12s · one CTA · moderation clean
- [ ] **BUILD /60 ≥48**, no seat under 8
- [ ] **J0 ≥8** — no visual hook in frame 1 = auto ≤4 = VETO
- [ ] **Wow Test v2** — screenshot frame named · precedent cited · ranked vs references · weak format capped
- [ ] **PLAN /60 ≥48**, no judge under 8

**Post-generation:**
- [ ] Clip score — no merge, melt, drift, warped subject, rendered text
- [ ] Frame 1 contains the subject (phrasing-trap check)
- [ ] Bank 10 accuracy — correct grille/lights/generation, RHD, engine note matches cylinder count

**Post-edit — the deliverable is not done without all five:**
- [ ] motion pass · [ ] unified grade · [ ] pop-in captions, no bands
- [ ] transitions · [ ] audio layer (ambience floor + hits + duck)

**Ship:** 9:16 · first frame never black · captions in safe zone · AI disclosed.

---

## THE INSPECTOR

```
J0 HOOK TYRANT   → 0–10s only. SOLO VETO. Runs before everything.
SIX-JUDGE PANEL  → the plan, /60. Forced ranking vs references. Kill quota.
CLIP SCORE       → the pixels, after render. Catches what paper can't.
```

⚠️ **Known weakness: the inspector is not independent.** Every judge is the same model that wrote the plan. That is why the Wow Test passed a video that shipped average — self-grading drifts generous.

**The fix available now:** Higgsfield **Virality Predictor** as an independent pre-launch gate — scores hook strength, attention, retention risk without the author's bias. Wire it in after assembly, before launch.

---

## THE BUDGET — the loop must terminate

```
PER VIDEO CAP:        150 credits
HOOK TEST:            1 round max (17.5)
REROLLS:              2 per clip max
ON EXCEEDING:         stop, deliver best available, report the overrun

⚡ THE CIRCUIT BREAKER — 5 consecutive failures on the SAME problem = STOP.
   Write down: what was tried, what each attempt DISPROVED, what's left untested.
   Then ask. Do not keep re-rolling the same failure with cosmetic variations —
   that is how credits die. Three failed rerolls of one clip is already a signal
   the PROMPT is wrong, not the render.

Cinematic (file 17, 15s/9 shots/one job) ....... ~135
Hero clip 5s / 8s .............................. 45 / 72
Hook test 720p fast ............................ 17.5
Talking head (Recipe 7) ........................ 0
```

---

## THE RUN SEQUENCE (what actually happens on a title)

```
1. DECODE      title → meaning → 2–3 angles → kill the obvious → pick
2. TARGET      avatar · pillar · language · recipe
3. WRITE       hook (Bank 2) + twist (Bank 11) + CTA (Bank 7) + shot list
4. GATE        free gates → BUILD /60 → J0 → Wow Test → PLAN /60
               fail = rewrite free, no credits, loop until clear
5. PROMPT      file 17 template, filled, 9:16
   ⏸ GATE      show the FULL prompt verbatim + J0/Wow/panel scores + exact cost
               → WAIT for the user's credit approval. The only stop in the run.
6. GENERATE    one multi-shot job where possible; clip-by-clip only if needed
7. QC          clip score → reroll on failure (max 2)
8. EDIT        recipe + 5 passes: motion · grade · captions · transitions · audio
9. DELIVER     one finished MP4 + the launch package (caption, hashtags,
               pinned comment, posting window)
```

---

## HONEST LIMITS (what the agent cannot do, stated up front)

1. **Seedance generates silent.** Audio is added in the edit. In-sandbox that means *synthesized* placeholders (shaped noise, tone hits) — structurally correct timing, but a real library SFX swap in CapCut still beats it.
2. **Music.** No licensed library available in-sandbox. The bed is the one element that must be added on the user's side.
3. **Paper gates can't predict render quality.** J0 and the Wow Test judge concept only; execution is only known after pixels exist.
4. **Nothing is proven until posted.** The retention targets are engineered-for, not guaranteed. The outer loop (post → read curve → calibrate) has never run.

---

## The Line

> **One title in. One finished video out. Everything between is the agent's job, not the user's.**
