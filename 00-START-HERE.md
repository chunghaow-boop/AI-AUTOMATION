> **NOT AN ENTRY POINT ANY MORE (2026-08-07).** Start at `README.md` or
> `START-NEW-CHAT.txt`: CLAUDE.md -> SYSTEM-MAP.md -> newest RESUME -> LESSONS.md.
> This file is kept because it is part of the numbered doctrine series.

# 00 — START HERE

> ⚡ **BOOT: read `22-HANDOVER.md` first**, then `RUNNER.md`. The handover holds current state, open threads, credit balance, and what is already proven. Everything else is reference.

### Talyx / Nev — AI Video Production System
### Built 14 July 2026

---

## The Six Files — read in this order

| # | File | What it is | Read when |
|---|------|-----------|-----------|
| **1** | `01-4-beat-spine.md` | **THE MASTER FILE.** Hook · Value · Twist · CTA. The four free gates. The six value types. | **Always. First. Every video.** |
| **2** | `02-ai-video-crew-roles.md` | The 8 seats. Role models. The 3 modes (Hero / Review / Vlog). | Before writing anything |
| **3** | `03-physical-performance-master.md` | Weight, hands, breath. The Hands Protocol. Laban Four. | Any video with a human or a hand |
| **4** | `04-foley-master.md` | Sound. The door thunk. The drop-out. Audio ON vs OFF. | Any sound-led video |
| **5** | `05-cinematic-ai-video-spec.md` | Camera bodies, glass, LUT vs grain, lighting, reflections. Universal prompt blocks. | When writing the actual prompt |
| **6** | `06-content-judges.md` | The 5 judges. Ship or kill. | After generation |
| **7** | `07-emotion-engine.md` | Micro-expression as CONFLICT. The face-realism upgrade. Golden-hour backlit. | Any video with a face |
| **8** | `08-the-strategist.md` | **SEAT 0.** Interprets your intent → 2-3 options. Algorithm + KPI engineering. | **First, on every idea** |
---

## The Flow

```
IDEA
  ↓
[1] SCRIPTWRITER  →  four beats                     → file 02
  ↓
⚡⚡⚡⚡ THE FOUR GATES  — Hook · Value · Twist · CTA  → file 01
     FREE. Kills bad ideas at zero cost.
  ↓
[2]  DIRECTOR              — blocking                → file 02
[2B] PHYSICAL PERFORMANCE  — weight, hands, breath   → file 03
[3]  DOP                   — the image               → files 02 + 05
[3B] FOLEY MASTER          — the sound               → file 04
[4]  TECHNOLOGIST          — model, cost             → file 02
  ↓
⏸  APPROVAL — nothing generates without a yes
  ↓
     GENERATE
  ↓
[5] QUALITY ADVISOR — is it broken?                  → file 02
[6] CONTENT JUDGES  — does anyone care?              → file 06
  ↓
SHIP
```

---

## The Ten Things That Actually Matter

1. **Reference images describe WHO. The prompt describes WHAT THEY DO.** Zero appearance words, ever. This is both your realism method *and* your moderation shield.
2. **The four gates are free.** Killing a bad idea before generation costs nothing. Rerolling never fixes a bad idea.
3. **Your default failure mode is Aspiration-only.** Beautiful and forgettable. Beauty is where you start, not where you stop.
4. **One unbroken take.** Zero cuts. That's the whole trick of the reference video.
5. **Never debug at full resolution.** 5s/720p (17.5cr) → 15s/1080p (135cr). 3× cheaper than blind rerolling.
6. **Hands need a JOB.** Idle hands melt. Anchored hands survive.
7. **Weight is what separates a photograph from a person.** AI defaults to floaty. Write *weight*.
8. **Sound is 50% of realism** — and it's the half nobody prompts.
9. **Audio ON for a single sound-led clip. OFF for multi-clip stitching.**
10. **Nev's face is the product in Mode B and C.** You cannot AI-generate trust.

---

## Model Decisions (as of July 2026 — re-verify, they go stale)

| Need | Model | Cost |
|---|---|---|
| Multi-character identity lock | **Seedance 2.0** — multiple `image_references`, up to 9 | 9 cr/sec @ 1080p std |
| Cheap composition test | Seedance 2.0, 720p, `fast` | 3.5 cr/sec |
| Character reference stills | **Soul 2.0** | 0.12 cr — effectively free |
| Real performance transfer | **Kling 3.0 Motion Control** | — |

**Cost is linear in duration.** The only real lever is `fast`/720p vs `std`/1080p — a 2.6× difference.
**NSFW rejections auto-refund.** They cost time, not credits.

---

## What's Proven

| | |
|---|---|
| ✅ | Hyper-realistic humans, single unbroken 15s take, zero cuts, 24fps, 46 Mbps master |
| ✅ | Four-person identity lock in one shot via Seedance `image_references` |
| ✅ | Moderation-safe prompt construction |
| ✅ | The 5s/720p test protocol |

## What's Not

| | |
|---|---|
| ⚠️ | **Real car photos.** Still the #1 unmitigated risk. Wrong R34 grille = roasted by Malaysian car Facebook. |
| ⚠️ | **30–60s multi-clip.** Untested. Rule #1: generate silent, lay one continuous music bed in the edit. |
| ⚠️ | **Motion Control.** The biggest untapped realism lever. You're a human who can move — film yourself. |

---

## The Line

> **Beauty gets you looked at.**
> **Value gets you remembered.**
> **The twist gets you shared.**
> **The CTA gets you paid.**

You've proven the first. The other three cost thinking, not credits.
