# FULLY-AI VLOG / CAR REVIEW / INDUSTRY VALUE
### File 38. Strategic pivot: all three formats generated, using the KOL reference.
### ⚠️ This SUPERSEDES several standing rules. Read the "what changes" section before building.

---

## 1 · MY EARLIER ADVICE WAS BUILT ON A WRONG ASSUMPTION

I argued repeatedly this session: *"You cannot AI-generate trust — in Mode B and C, Nev's face
is the product."* That came from file 22 and I assumed Nev was a real person to be filmed.

**If Nev is an AI persona built from your reference images, that argument doesn't apply as
stated.** The trust question becomes about *consistency and disclosure*, not about a camera.
Correcting it here so the record is clean.

## 2 · WHAT THIS CHANGES IN THE EXISTING SYSTEM

| Standing rule | Status now |
|---|---|
| `generate_audio: false` — **"silent always"** | ❌ **OBSOLETE for talking formats.** Seedance 2.0 supports native audio. Correct for multi-clip cinematic stitches; wrong for a talking head |
| "3 of 4 formats need ZERO credits" (file 24) | ❌ **REVERSED.** All four now cost credits. The bottleneck returns to Higgsfield |
| "Mode B/C: AI serves Nev, never replaces him" | ❌ rewrite — AI *is* Nev |
| File 23 asset sheet | ⬆️ **PROMOTED from optional to mandatory.** Consistency is now the entire product |
| AI disclosure | ⬆️ **CRITICAL.** TikTok/Meta require it; your own file 15 already lists it. An AI persona that gets caught undisclosed loses the trust the whole channel runs on |

## 3 · ⚠️ THE COST MATH — this is the binding constraint

**Balance: 1,850.68 cr (measured).** Rates: 720p std **4.5cr/s** · 1080p std **9cr/s** ·
720p fast 5s = 17.5 flat. Seedance max clip length = **15s**, so longer videos = multiple clips.

| Video length | 720p std | 1080p std |
|---|---|---|
| 30s | 135cr | 270cr |
| 60s | **270cr** | 540cr |
| 90s | 405cr | 810cr |
| 2 min | 540cr | 1,080cr |

**Weekly cadence across three pillars, 60s each, 720p:**
```
3 × 270cr = 810 cr / week   →   3,240 cr / month
Your balance covers ~2.3 weeks.
```
**That is the real blocker — not capability. Fully-generated talking content at weekly cadence
is a subscription-scale spend, and naive generation burns the balance in under a month.**

## 4 · THE COST-EFFICIENT ARCHITECTURE (this is the actual answer)

Don't generate 60 seconds of video. Generate **the moments that must move**, and carry the rest
with assets that are nearly free.

```
60-SECOND VIDEO — the cheap build
  0-15s   TALKING clip (Seedance, generate_audio ON, KOL ref)      67.5cr
  15-35s  STILLS with Ken Burns push/pan + VO + captions            ~8cr  (images only)
  35-50s  TALKING clip #2 (the payoff / verdict)                    67.5cr
  50-60s  STILL card + CTA (the Artefact Drop, file 35)             ~2cr
  ────────────────────────────────────────────────────────────────
  TOTAL ≈ 145cr  vs 270cr naive        →  ~46% saving, same runtime
```
**Why it works:** images cost a fraction of video, and `ffmpeg zoompan` gives them motion for
free. My `pacing.py` already enforces the cut rate so the still sections don't read as dead air.
Speech + captions carry comprehension; the face only needs to appear where it earns trust.

**Further levers, in order of savings:**
1. **`seedance_2_0_mini`** — budget variant, 480p/720p. Use for B-roll and non-hero shots.
2. **`fast` mode** — 720p/5s flat 17.5cr (≈3.5cr/s vs 4.5). Use for all tests and probes.
3. **Hook-first probe (RUNNER 9b)** — 3 hooks × 17.5 ≈ 52cr before committing.
4. **Reuse ruthlessly.** One character sheet, one location set, one wardrobe — forever.
5. **9:16 720p is enough.** 1080p doubles cost for a phone screen. Reserve for hero only.

## 5 · THE MODEL ROUTING (from `models_explore`, verified this session)

| Need | Model | Why |
|---|---|---|
| **Car review / UGC / tutorial** | **Marketing Studio** | purpose-built presets: **Product Review, UGC, Tutorial, Unboxing**, takes `avatar_ids` + `hook_id` + `setting_id`. 12–15s. Closest thing to a one-click review format |
| **Talking head, identity-locked** | **Seedance 2.0** + KOL refs, `generate_audio: true` | reference-driven identity consistency, native audio |
| **Lip-sync accuracy** | **Wan 2.7** | "synchronized audio, character-consistent", accepts `audio_references` — feed it your VO |
| **Multi-shot in one gen** | **Kling v3.0** | multi-shot + audio sync + motion transfer |
| **Cheap B-roll** | **Seedance 2.0 Mini** | budget variant |
| **Stills for Ken Burns** | image models | cheapest runtime per second, by far |

## 6 · THE FOUNDATION — build this ONCE, before anything else

**The four-view character sheet** (prompt in file 37, adapted from Tao Prompts). Without it,
every generation drifts and the persona stops being a persona. With it, every future build has a
locked `start_image`.

**Then build a locked asset set, reused forever:**
```
□ character sheet (4 views + portraits)      ← the identity
□ 3 wardrobe states                          ← "episodes" feel distinct without re-drifting
□ 3 locations (garage / lot / desk-office)   ← one per pillar
□ 1 title-card template per pillar           ← file 14 says series title cards are fixed assets
```
Cost: image generations only. This is the highest-leverage spend available.

## 7 · THE HONEST RISKS

1. **Consistency is the whole product.** A persona whose face shifts between episodes reads as
   fake and loses trust faster than no persona at all. `facecheck.py` now measures this.
2. **Disclosure is mandatory**, and your own launch protocol already says so. Undisclosed AI
   personas are a platform-penalty risk and a credibility risk.
3. **Douyin's own 2026 data:** authentic ordinary-person content gets **+40% engagement**.
   An AI KOL can absolutely work — but it starts from behind on trust, and it must win on
   consistency, usefulness and format instead.
4. **Claims need a human backstop.** A car review makes checkable claims (spec, price,
   generation). Your Bank 10 accuracy gate matters *more* now, not less — an AI persona stating
   a wrong figure is indefensible.
5. **Burn rate.** At naive generation you have under a month. The architecture in §4 roughly
   doubles that; discipline does the rest.

## 8 · WHAT I'D DO, IN ORDER
```
1. Build the 4-view character sheet                    images only · the foundation
2. Build the locked asset set (wardrobe/locations)     images only
3. ONE 30s car review at 720p, cheap architecture      ~145cr · proves the whole chain
4. Run it through the gate (mastermind + pacing + facecheck)
5. POST IT. Read the 24h curve.                        the only real score
6. Only then scale to weekly across three pillars
```
**Do not start weekly cadence before step 5.** Committing 3,240cr/month to a format whose
retention you have never measured is the exact mistake the gates exist to prevent.
