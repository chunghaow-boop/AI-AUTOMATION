# REACHING ARENA-ZERO QUALITY — what it actually takes
### Reference: "Arena Zero Ep.1" — Higgsfield AI, 10:03, 1.9M views, 31K likes.
### Their own showcase series. 16:9 narrative sci-fi, creature VFX, burned-in subtitles.

---

## ⚠️ FIRST — THE ARITHMETIC

| | 720p std | 1080p std |
|---|---|---|
| one 10-min episode, single pass, **zero rerolls** | 2,714 cr | 5,427 cr |
| realistic, 2.5× reroll factor | **6,784 cr** | **13,568 cr** |

**Your balance: 1,850.68 cr.** One episode at 720p, realistically, is ~4,900 cr short.
Your whole balance buys **6.9 minutes of 720p with no rerolls at all** — and rerolls are not
optional in AI filmmaking, they're most of the work.

Higgsfield made Arena Zero as a **marketing showcase for their own platform**, with a team and
presumably uncapped internal credits. The "$100M saved in 4 days" line is advertising, not a
budget you can copy.

---

## ⚠️ SECOND — IT IS A DIFFERENT PRODUCT FROM YOURS

| | Arena Zero | Your three formats |
|---|---|---|
| aspect | 16:9 | **9:16** |
| platform | YouTube long-form | FB / TikTok / IG |
| genre | narrative sci-fi fiction | vlog · car review · industry value |
| audience | anyone who likes AI film | Malaysian recond car buyers |
| goal | showcase a tool | build trust → sell cars |
| pacing | long takes, atmosphere, slow build | 8–25 cuts/min, hook in 2s |

**The editing craft that makes Arena Zero good would damage your retention.** Its held wide
shots, atmospheric pauses and slow reveals are correct for a 10-minute story on a TV. On a
9:16 feed they read as dead air — `pacing.py` would flag most of it as a dead zone.

> Copying its *look* is worth doing. Copying its *editing grammar* would cost you scrollers.

---

## WHAT GENUINELY TRANSFERS — and how to get it

### 1 · GRADE CONSISTENCY ⭐ the single biggest visual-quality lever
Arena Zero holds one colour identity across every shot. That consistency is 80% of why it reads
as "cinema" rather than "AI clips stitched together."

**You already have the tool.** `grade.py` — and it already proved the point: your own two AI
clips measured **12.77 apart** ("obvious mismatch, this is the AI tell"). Fix that and your
output jumps a tier before you spend a single extra credit.
```bash
python3 tools/grade.py profile hero.mp4 -o assets/look.json     # define ONE look
python3 tools/grade.py match clipN.mp4 --profile assets/look.json -o clipN_graded.mp4
```
**Free. Do this today.**

### 2 · SOUND DESIGN DEPTH ⭐ second biggest, also free
Arena Zero layers dialogue + foley + ambience + score, each at its own level. Most AI content
has one music bed and nothing else — that flatness is instantly readable as amateur.

**You now have 470 SFX and 127 tracks.** The layers you're missing are ambience beds under
everything (`sfx/ambience`, `sfx/wind`, `sfx/machine`) and per-beat foley. Not a credit cost —
an assembly discipline. `SFX-INDEX.md` maps beat-type → file.

### 3 · SHOT VARIETY AND CAMERA LANGUAGE
Wide → medium → close → insert, each with ONE motivated move. Already specified in `GATE.md`'s
camera gate. Costs nothing extra; it's a prompt-writing habit.

### 4 · THE HERO INSERT — the realistic way to buy cinema
Don't make a 10-minute film. **Buy 5 seconds of Arena-Zero-grade footage and put it in frame 1
of a 60-second car video.**
```
5s @ 1080p std = 45cr  ·  reroll twice = 135cr
```
One genuinely cinematic hook shot, then cut to your real face. That's the hybrid architecture
already in `SOURCE-ROUTING.md` — spectacle where it earns attention, trust where it converts.

---

## WHAT I'D NEED TO BUILD FOR TRUE CINEMATIC TIER
Only worth building if you actually commit to a hero/cinematic pillar. Ranked:

| # | Tool | Does | Why it's missing |
|---|---|---|---|
| 1 | `lut.py` | film-emulation LUTs (Kodak/Fuji curves), halation, bloom, grain | `grade.py` matches clips to each other; it does not impose a *filmic* look |
| 2 | `soundmix.py` | 4-track mixer: dialogue / foley / ambience / score with auto-ducking + per-track LUFS | current mixing is single-track |
| 3 | `continuity.py` | track wardrobe, props, light direction across many shots; flag breaks | `facecheck.py` only does faces |
| 4 | `composite.py` | multi-layer: fog, dust, light rays, lens flares over a plate | no compositing layer exists |
| 5 | `subs.py` | cinematic burned-in subtitles (their exact style) | `cards.py` does cards, not dialogue subs |

**1 and 2 are the high-value pair** — they're what separates "AI clips" from "a film," and
neither costs credits to run.

---

## WHAT I NEED FROM YOU
```
1. A DECISION: is cinematic a real pillar, or a hero-insert technique?
   → pillar        = needs a credit budget ~5,000cr/episode. Say so and I'll plan for it.
   → hero insert   = 135cr per video, works inside your current balance. ⭐ my recommendation
2. Your phone clip  → the grade anchor. Everything colour-related is blocked on this.
3. Nothing else.    The tools for 1-3 above I can build without input.
```

## THE HONEST VERDICT
> You can reach Arena Zero's **look** — grade consistency and sound depth get you most of the
> way, and both are free. You cannot reach its **scale** on 1,850 credits, and its **editing
> grammar** would hurt the formats you actually named.
>
> The move is: cinematic *quality* in a 5-second hook, short-form *pacing* everywhere else.
