# The Editing Bank — Edit Recipes for Auto-Assembly
### Companion to `10-the-editor.md`. The Editor picks a RECIPE, fills the slots, outputs the auto-edit spec.
### Talyx / Nev — every generated video flows through one of these.

---

## How This Bank Works

Generation hands you clips. **The Editor never edits from scratch — it selects a recipe by video type, fills the slots, and executes.** Each recipe is a complete timeline template: cut rhythm, transition per seam, caption slots, SFX slots, music behavior. This is what makes the edit *automatic* instead of hand-crafted every time.

```
generated clips → [pick recipe by MODE + GOAL] → fill slots → auto-edit spec → render
```

**The rule:** if a video doesn't fit any recipe, that's a signal the plan was wrong — not a reason to freestyle. Go back to the Strategist.

---

## RECIPE 1 — THE HERO SINGLE-TAKE (Mode A · 10–15s · one unbroken clip)
*For: the Douyin-style showroom piece, the transform hook. One clip IS the video.*

```
TIMELINE
0.0s      clip starts — NO fade-in (fade-in kills the hook; frame 1 must hit)
0.0–0.5s  HOOK CARD on (bold, top-third, 2 lines max)
0.5s      card holds 2.5s, then off
[climax]  music swells into the reveal moment
-1.0s     CTA CARD on (bottom band) + hold final frame 0.5s
end       fade-out 0.4s (video only, music tails 0.5s longer)

CUTS         none — the take is the take
TRANSITIONS  none
MUSIC        one cinematic bed · a RISE into the reveal · no drop-out needed
CAPTIONS     2 cards only (hook + CTA). Single-takes die from over-captioning.
SFX          1 hero sound at the reveal + ambience layer. That's it.
```

---

## RECIPE 2 — THE 4-BEAT SPINE CUT (Mode A/B · 15s · 4 clips)
*For: the standard Hook→Value→Twist→CTA build (the POV salesman structure).*

```
TIMELINE
0.0s      Beat 1 (4s) — hook card ON at 0.0 (top), off at 3.0
4.0s      ⚡ hard cut ON BEAT → Beat 2 (4s) — caption bottom band
8.0s      ⚡ transition: whip or object-wipe → Beat 3 (4s) — caption
          ★ MUSIC DUCK to 10% for 1.0s at the twist moment, SFX lands in the quiet
12.0s     ⚡ hard cut on beat → Beat 4 (3s) — CTA card + hold last frame
15.0s     fade out 0.4s

CUTS         on the beat, every 4s (matches beat clock)
TRANSITIONS  seam 1: hard-cut · seam 2: whip/object-wipe (the mid-video re-hook) · seam 3: hard-cut
MUSIC        one bed · DUCK before the twist · back full for CTA
CAPTIONS     4 cards, one per beat, timed to the cut
SFX          per-beat from the Foley Bank (see companion file) — hero sound each beat
```

---

## RECIPE 3 — THE CHAPTERED LONG-FORM (Mode B · 30–60s · 3–5 pods)
*For: multi-car features, "day in the life", listicles. From the cinematic showcase reference.*

```
TIMELINE
0.0s      HOOK POD (2s max) — the single most arresting clip, hook card on
2.0s      ⚡ DOUBLE-CUT (two cuts 1.5s apart) → POD 1 (~12s, one idea/car)
~15s      ⚡ DOUBLE-CUT → POD 2 (~12s)
~28s      ⚡ DOUBLE-CUT → POD 3 (~12s)
...       repeat to length
-3.0s     CTA pod: verdict card + comment-bait question + hold

CUTS         inside pods: standard 2–3s rhythm · between pods: the double-cut
TRANSITIONS  the double-cut IS the pod transition (rapid re-hook) — use B-roll insert + snap back
MUSIC        one bed for the WHOLE video (hides pod seams) · small lift at each pod start
CAPTIONS     pod-title card at each pod start ("Car #1: ...") + running captions
SFX          pod-start whoosh at every double-cut + per-content foley
RULE         no pod over 13s — that's where the reference's retention re-hooks fired
```

---

## RECIPE 4 — THE VELOCITY MONTAGE (Mode A · 10–20s · 6–12 clips)
*For: hype reels, car reveals, event recaps. From the fast-cut montage reference.*

```
TIMELINE
0.0s      strongest clip FIRST (0.5–1s only) — the screenshot frame opens
then      cuts every 1.0–1.5s, EVERY cut on a beat
climax    ★ BURST: 3–4 cuts at 0.3–0.5s each, stacked into the payoff
payoff    the hero shot — hold it 2s (the only long shot in the video)
end       CTA card over the held hero + fade

CUTS         1–1.5s standard → accelerate → 0.3–0.5s burst → HOLD
TRANSITIONS  hard cuts + 1–2 flash/whip max (more = cheap)
MUSIC        high-energy, beat-mapped FIRST — the cuts obey the track, not vice versa
CAPTIONS     minimal — 1 hook word + CTA. Montage speed IS the content.
SFX          whoosh on whips, impact hit on the payoff, riser into the burst
RULE         the burst must land ON the music drop. Find the drop, build backwards.
```

---

## RECIPE 5 — THE POV / RELATABLE CUT (Mode C · 15–30s)
*For: vlog-style, day-in-life, selfie-format. Softer rhythm, authenticity over polish.*

```
CUTS         2.5–4s, slightly OFF-perfect (too-clean cutting kills the authentic feel)
TRANSITIONS  hard cuts only — fancy transitions break the "real person" illusion
MUSIC        lofi/chill bed at ~30% volume — ambience and foley sit ON TOP (reversed mix!)
CAPTIONS     conversational, lowercase, small — like the creator typed them
SFX          heavy: this format lives on foley (doors, cloth, keys, footsteps)
RULE         imperfection is the aesthetic. One handheld wobble > stabilized glide.
```

---

## ⚡ WHEN SEAMS DON'T EXIST — the multi-shot generation exception

If the film was made as a **single multi-shot generation** (file 05 §2I), the transitions were generated in-model and there are no seams to hide. The Editor's job shrinks to: captions, music, SFX, and **layering 2–3 hard cuts on the beat** over the dissolve bed — which is the one thing the generated version lacks. Do NOT add mask/object-wipe transitions to a multi-shot generation; you'd be solving a problem that isn't there.

---


## ⚡ THE BURST-OPEN (measured on a viral 126s reel)

The reference's **first cut lands at 1.17s, then 3 more inside 0.73s.** It opens on a burst.
```
0.0-1.2s   one held frame  (the hook lands)
1.2-1.9s   4 CUTS          (0.24s each — the pattern interrupt, immediately)
then       settle to ~0.9s median cutting
```
This weaponises J0's "grab complete by 2.0s": the hook is visual, then the *edit itself* becomes
the second interrupt before the viewer can decide to leave. **Bursts recur every 20-40s**
(measured at 1.2s, 3.7s, 17.9s, 35.2s, 60.5s) — one was **7 cuts in 1.17s**.

## ⚡ BEAT-LOCK IS A STYLE CHOICE, NOT A LAW

Measured on the reference: tempo 119.7 BPM, but **only 23% of cuts land within 60ms of a beat**
(mean error 185ms). **This professional viral video is NOT beat-locked.** It cuts to *content* —
speech beats, reveals, reactions.

| Cut to | Use for |
|---|---|
| **the BEAT** | montage, hype, product reveals, music-led (our Urus beatcut) |
| **the CONTENT** | talking head, story, tutorial, any video where words carry meaning |

Cutting a talking-head to a music grid fights the speech. Cutting a montage to speech wastes the drop.
**Pick one deliberately** — the reference proves the content-led register is fully viable at scale.

## Cut-pace reference (measured, real viral short-form)
```
median interval 0.93s  ·  mean 1.90s  ·  fastest 0.066s (2 frames)  ·  longest hold 12.5s
```
The mean/median gap is the lesson: **mostly fast, with a few long holds.** Not uniform pacing.

---

## THE SEAM-HIDING RULES (all recipes — AI-specific)

Stitched AI clips expose themselves at the seams (lighting/identity drift). Hide every seam with one of:
1. **Cut on motion** — both sides of the cut have movement in the same direction
2. **Object-wipe** — something crosses the lens at the cut (designed at BUILD)
3. **The music bed** — one continuous track makes 5 clips feel like 1 film (mandatory, every recipe)
4. **Caption bridge** — a card that stays on across the cut pulls the eye to the text, not the seam
5. **The audio J-cut** — next clip's sound starts 0.3s BEFORE its picture (pro move, huge)

---

## CAPTION STYLE GUIDE (all recipes)

| Slot | Style | Rules |
|---|---|---|
| HOOK card | bold · top third · 2 lines max | on at 0.0s (not delayed) · off by 3s |
| Running caption | bottom band · 1 line | changes ON the cut, never mid-shot |
| The TWIST card | can break style — bigger/colored | the one allowed style-break per video |
| CTA card | bottom · with the 👇 | holds to the end, never fades early |

**Font: one family per video. Sizes: hook > twist > captions > CTA. Never more than 2 caption elements on screen at once.**

---

## THE EXPORT STANDARD (every video)

```
1080×1920 · 30fps · H.264 · CRF 18–20 · audio AAC 192k stereo
loudness: master -7 to -9 LUFS (measured viral standard, file 19) · SFX peaks -6dB · no clipping
safe zones: keep text inside center 80% width, above bottom 15% (UI covers it)
first frame: NEVER black (thumbnails pull frame 1)
disclose AI on posting
```

---

## RECIPE 6 — THE TUTORIAL / RESULT-FIRST (Mode C · 45–60s)
*From the "vault on the desk" reference. For "how I made this" meta-content.*

```
0–2s     RESULT-FIRST HOOK — the finished effect + "How to do this" + arrow
2–30s    PROCESS PODS (~5s each): the plate shot → the prompt → the build steps
30–52s   ★ THE PAYOFF HOLD — the finished result plays UNBROKEN ~20s
          (a long hold WORKS when it is the promised payoff — earn it, then hold it)
52–60s   fast 3-cut outro + CTA ("full prompt in comments / follow for part 2")
```

---

## RECIPE 7 — THE TALKING-HEAD AUTHORITY CUT (Mode B/C · 60–180s · ZERO AI credits)
*From the 2:40 Chinese knowledge-creator reference. One chair, one camera, 34 jump cuts. The highest-trust, lowest-cost format in the system.*

```
SETUP        static medium close-up · soft front key · shallow DOF ·
             personality background (shelf/objects that say WHO you are) ·
             lapel mic VISIBLE and left in — authenticity beats polish

TIMELINE
0:00–~50%    FAST HALF — jump cut every 2–4s. Cut out EVERY pause, breath,
             "um", and dead frame. The jump cut IS the pattern interrupt.
~50%–end     SLOW HALF — holds of 8–12s. Let the emotional payoff breathe.

CUTS         jump cuts only, same framing, no reframe
TRANSITIONS  NONE. A transition here reads as amateur.
MUSIC        none, or a near-silent bed. The voice is the track.
CAPTIONS     burned in, every line, high-contrast — most viewers read before they hear
SFX          none. Room tone only.
```

**⚡ THE PACING INVERSION (contradicts Recipe 4 — read carefully):**
> Recipe 4 accelerates into the climax. This one DECELERATES. The rule that reconciles them:
> **visual payoffs accelerate · verbal/emotional payoffs decelerate.**
> Measured on the reference: 26 cuts in the first 82s (3.1s avg) → 8 cuts in the last 80s (10.0s avg). A 3× slowdown into the feeling.

**⚡ AUTOMATE THE FAST HALF — the auto jump-cut tool**
```bash
python3 /mnt/skills/user/video-editing/autojumpcut.py raw.mp4 tight.mp4 --db -35 --min 0.25
```
Detects every pause, cuts it, re-concats. Verified: 39% tightening on a test with 5 gaps.
**This is what makes Recipe 7 economically viable** — the reference's 3.1s cut density came from
removing every breath and "um" by hand. One command replaces that. Run it FIRST, then caption.

**⚡ THE GESTURE-PER-CUT LAW:** a NEW hand position on every single jump cut — pinch, point-to-chest, clasp, chop, splay, tap-the-collar. This is what stops 34 identical framings from reading as static. Performance seat owns it (Bank 4 #33).

**Why this recipe matters for Talyx:** it needs no AI, no credits, and no render risk — and for "Recond Truth" content it beats any generated clip on trust. The only skill required is ruthless cutting.

---

## THE FFMPEG AUTO-EDIT TEMPLATE (v2 — learned from the v1 failure)

*v1 shipped flat: no audio, hard cuts, static clips, debug captions on black bands. v2 fixes each, fully scripted — this is the actual automation layer that runs after generation.*

**The 5 automated passes (per video, in order):**
1. **Motion pass** — every clip gets a slow lateral drift (scale 110% → crop 1080×1920 with x moving over the clip; alternate direction per clip). Flat AI clips read static; 8% drift reads filmed.
2. **Grade pass** — one `eq=contrast=1.04:saturation=1.06` on every clip = unified look across generations.
3. **Caption pass** — outline text (borderw=4), NO background band, at y=72% (safe zone), **pop-in via alpha fade 0.25s, fade-out 0.4s before the cut.** Captions breathe with the edit instead of sitting static.
4. **Transition pass** — `xfade`: slide between beats, **fadewhite on the twist**, 0.3s each. Cuts stop being raw jumps.
5. **Audio pass (the v1 killer fixed)** — even with no music library, the layer is synthesized:
   - ambience floor: low pink noise (the D-floor — silence is the AI tell)
   - whoosh at every cut: filtered white-noise burst (B1)
   - impact at the twist: 55Hz sine thump (B5)
   - **the duck: floor drops to 25% for 1.2s around the twist** (B8)
   - master fade-out
   These are placeholder-grade SFX — swap with real bank sounds (file 12) in CapCut for the ship version — but the *structure* (what plays when, the duck, the floor) is fully automated.

**Rule: no video leaves the pipeline without all 5 passes.** v1 skipped 4 of them; that's exactly why it read as AI slop despite good clips.

---

## The Line

> **A recipe is taste, written down once, executed forever.**
> The edit stops being a craft you perform every time and becomes a system that performs it for you —
> while the 20% you keep (the duck before the twist, the burst on the drop) stays yours.
