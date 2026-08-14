# THE RUNNER — one page, every video
### The spine. HYBRID: real footage + AI generation, routed per shot.
### Formats: vlog · car review · industry value · cinematic hero.
### Read `SOURCE-ROUTING.md` (real vs AI) · `GATE.md` (scorer) · `PROMPTS.md` (assets) · `RUN.md` (commands).

```
INTEL → DECIDE → ⏸ APPROVE → PROBE → GENERATE → EDIT → GATE → LAUNCH → RESOLVE
 free    free      you       ~52cr    paid       free   free    you      you
```

---

## PHASE 0 · INTEL — weekly, automatic, free
Runs Mondays 9am (scheduled). Or `python3 tools/intel.py brief`.
```
watchlist URLs  → scene analysis → mechanisms → banks
WebSearch       → what is working THIS week
tools/reverse.py → editing DNA of any reference video, diffed against yours
```
**You are the discovery layer.** Drop URLs you admire into `intel.py add`. The tools measure
what your eye already selected. Output: 3–5 new mechanisms + the one ranked action for the week.

---

## PHASE 1 · DECIDE — free, autonomous
**You give a TITLE. Nothing else.** Run `/talyx-shotlist`.

### 1.0 SOURCE ROUTING — decide before anything else
**You shoot real footage AND generate.** Route per SHOT, not per video — see `SOURCE-ROUTING.md`.
```
FILM everything you CAN.  GENERATE only what you CAN'T.
Every shot filmed instead of generated = ~67cr back.
Default = HYBRID: real face (trust) + AI spectacle + stills (runtime) ≈ 90cr per 60s
```
Mark every line of the shot list `[REAL]` or `[AI]`. **Film the REAL ones first** — filming
often removes an AI shot you planned, which is a direct saving.
Hybrid seam rules (grade match · cut on motion · audio across the seam · AI goes wide ·
never seam mid-sentence) are in `SOURCE-ROUTING.md`.

### 1.1 Target — never "for everyone"
`AVATAR` (1 First-Car Kid · 2 Family Upgrader · 3 Resale Uncle · 4 JDM Dreamer · 5 Silent
Businessman) · `PILLAR + episode #` · `LANGUAGE` (Clean EN · **Manglish ⭐default** · BM lead ·
CN/EN mix) · `FORMAT` · `PLATFORM` (decides the CTA — see 1.5).

### 1.2 The four beats — fork, never start blank
```
HOOK   type + WOW/TWIST inside 2s · 10-14 words · a SPECIFIC nameable promise
VALUE  which of the 6? (knowledge/comedy/relatable/aspiration/utility/identity)
TWIST  what makes them SEND it
CTA    ONE ask (see 1.5)
LOOP   last frame → first frame
```
**Declare the remix.** "Borrowed this format from X" reads as craft literacy, not theft — and
pre-empts the copied-comment by owning it first.

### 1.3 The free gates — rewrite until all pass, costs nothing
```
□ frame 1 = something HAPPENING, not someone POSED   ← the #1 killer
□ idea detonates ≤1.5s   □ WOW or TWIST in frame 1   □ delivers ≥1 value type
□ twist makes the sharer look good   □ CTA loops to the hook   □ legible SOUND OFF
□ AI disclosure planned              □ every factual claim is checkable (Bank 10)
```

### 1.4 The shot list — banks before invention
Per shot, written literally into the prompt:
```
CAMERA      body + lens + T-stop        "Sony FX3, 35mm, T2.8"
MOVE        ONE, motivated              "slow push-in — the verdict landing"
PERFORM     weight · hands have a JOB · head-first-eyes-follow · reset to neutral
EMOTION     the CONFLICT, not the expression (suppress → leak → reset)
LIGHT       every source named · practicals visible · one shadow logic
TRANSITION  what is physically continuous across the seam — if nothing, it's a jump
SOUND       generate_audio TRUE for talking · hero sound named
IDENTITY    character sheet as start_image, every shot, no exceptions
```
**Pacing target:** vlog 15–25 cuts/min (max 3s shots) · review 8–15 (max 6s) · industry 6–12
(max 8s). **Hard cuts, not dissolves** — dissolves don't interrupt a scroller.

### 1.5 CTA routing — the platform decides
| Platform | Weighted signal | CTA type |
|---|---|---|
| FB Reels | comments between people | war-starter / opinion split |
| **IG Reels** | **DM sends per reach** | **"send this to the friend who…"** |
| TikTok | completion + rewatch | loop / "watch the hands again" |

### 1.6 Cost preflight — the binding constraint
720p std **4.5cr/s** · max clip **15s** · fast 720p/5s = 17.5 flat.
**Generate only the moments that MOVE:**
```
0-15s  TALKING clip (audio ON, char sheet)      67.5cr
15-35s STILLS + zoompan + VO + captions           ~8cr
35-50s TALKING clip #2 (the payoff)             67.5cr
50-60s STILL CTA card                             ~2cr
       ≈145cr for 60s   vs 270cr naive
```
State per-clip cost, total, and **the measured balance after** (never estimate it).

### 1.7 Score the plan — `GATE.md` stages 2–4
J0 ≥8 or back to the hook. Weighted /100. Choose between options **pairwise, anonymised,
order swapped** — never by absolute score.

---

## ⏸ PHASE 1.5 · THE SINGLE APPROVAL — the only spend authorization
You see: locked script · full shot list · **every prompt verbatim** · scores · exact cost ·
balance after · the probe plan. **Everything stops here until you say go.**

---

## PHASE 2 · PROBE — ~52cr, mandatory above 100cr
Paper gates are blind to execution. Every hook this system shipped passed its paper gates and
died in the render.
```
3 competing hooks × 5s × 720p fast ≈ 52cr
→ qc-console.html blind A/B, order randomised
→ YOUR thumb picks. Not a score.
→ winner is rebuilt at full quality; losers logged
```
Your pick is the only genuinely external signal in the system — everything else is one model
judging itself.

---

## PHASE 3 · GENERATE — paid, autonomous
```
identity   character sheet = start_image on EVERY shot
past 15s   chain: last frame of shot N → start_image of shot N+1
routing    review/UGC → Marketing Studio (Product Review preset + avatar_ids)
           talking    → Seedance 2.0 + refs, generate_audio TRUE
           lip-sync   → Wan 2.7 (accepts audio_references)
           B-roll     → Seedance 2.0 Mini (budget)
           stills     → image models, then zoompan for motion
```
Reroll max 2 per shot. 5 failures on one problem → **stop and ask**, never loop.

---

## PHASE 4 · EDIT — free, mechanical
```
tools/transcribe.py   word-level transcript  (local only — REAL footage esp.)
tools/autocut.py      fillers · retakes · pause tighten · hook pick · word-exact captions
tools/cards.py        designed HTML/CSS cards (Playwright) — NOT ffmpeg drawtext
tools/edl.py auto     build EDL → render → gate → auto-amend (max 3 loops)
```
The edit is **data** (an EDL), not a one-off command — diffable, re-renderable, and amendable
by the gate without a human. Cuts and SFX quantised to the beat grid.

---

## PHASE 5 · GATE — nothing reaches you on a fail
`GATE.md` stage 1, all mechanical:
```
blank frames · LUFS −7..−9 (measured target, file 19) · true peak < −1 · dead air <45% · captions within 0.6s of the word
SFX/cuts within 50ms of the beat · cuts/min in band · frame-1 motion ≥0.35
face similarity across every seam · AI disclosed · Bank 10 accuracy
```
FAIL → route to the seat → fix → **re-measure** (a fix pass creates new defects — proven twice).
Max 3 loops, then stop and report.

---

## PHASE 6 · LAUNCH — yours
```
timing    TikTok 6-11pm MY (Sat is its best day, FB's worst) · FB Reels weekday 9pm · IG after
pre       caption ADDS (never repeats the hook) · 3-5 specific tags · pinned comment DRAFTED
          · AI disclosed · 2-3 groups ready · reply hour blocked out
0-60min   reply to EVERY comment with a QUESTION. Never "thanks". Comments-between-people is
          the strongest distribution signal, and you are one of the people.
```

## PHASE 7 · RESOLVE — the only real score
At +24h: pull 3s rate · avg % viewed · shares · comments. Overlay **predicted vs actual per
beat**. Log the gap. After ~10 resolutions the gate weights stop being opinion and become
measured.

> **Everything above Phase 7 is informed opinion until a real curve lands.**
> Nothing has been posted yet. That remains the single largest gap in this system.

---

## THE 5 THINGS THAT ACTUALLY DECIDE IT
1. **Frame 1 = WOW or TWIST, and it MOVES.** No exceptions.
2. **The character sheet.** For an AI persona, consistency IS the product.
3. **Generate only what moves.** Stills + VO + captions carry the rest at 5% of the cost.
4. **Cut hard, on the beat.** Dissolves are cinematic grammar; they lose scrollers.
5. **The free gates are free. The generator is not.** Kill bad ideas before you pay.
