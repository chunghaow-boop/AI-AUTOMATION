# Cinematic AI Video — Master Spec & Prompt Template
### Talyx / Nev — reusable format for hyper-realistic AI video

---

## 0. The Core Principle

Realism does **not** come from the video model. It comes from three separate layers, and most people collapse them into one prompt and fail.

| Layer | Carried by | Never do this |
|---|---|---|
| **IDENTITY** — who they are | Reference images | Never describe faces in the prompt |
| **STAGING** — what they do | Prompt: blocking, camera, gestures | Never leave blocking to the model |
| **LOOK** — how it's shot | Prompt: the spec block below | Never say "make it cinematic" |

**Rule:** Reference images describe WHO. The prompt describes WHAT THEY DO and HOW IT'S SHOT.

This is also your moderation shield — see §12.

---

## 1. LUT vs Film Grain vs Film Stock

| Term | Definition | What it changes | Example prompt line |
|---|---|---|---|
| **LUT / Grade** | A colour transformation. Maps input colour → output colour. | Hue, contrast, saturation, tint, black level | `cool-white neutral grade, lifted blacks, low saturation` |
| **Film grain** | Physical noise texture. | Texture only. No colour effect. | `fine 35mm film grain` |
| **Film stock** | Shorthand that implies a grade **and** a grain structure. | Both at once. Most efficient. | `Kodak Vision3 500T aesthetic` |

**Stock cheat-sheet:**

| Stock | Look | Use for |
|---|---|---|
| **Kodak Vision3 500T** | Tungsten-balanced, soft highlight rolloff, clean shadows, gentle grain | Showroom, interior, premium commercial ← *the Douyin video* |
| **Kodak Vision3 250D** | Daylight, punchy, clean | Exterior car, golden hour |
| **Kodak Portra 400** | Warm skin, low contrast, creamy | Lifestyle, people-first |
| **Fuji Eterna 250D** | Muted, low-sat, green-leaning | Moody, restrained, editorial |
| **Cinestill 800T** | Halated red highlights, neon bloom | Night city, wet neon, JDM night |
| **Bleach bypass** | Crushed blacks, desaturated, silver | Aggressive, hard, performance |

**Grade families** (pick one, never mix):
- `neutral clean` — premium, corporate, showroom
- `teal and amber` — blockbuster, over-used, still works on cars
- `cool desaturated` — Nordic, tech, restrained luxury
- `warm nostalgic` — kampung, heritage, retro JDM
- `high-contrast monochrome with one accent colour` — dramatic hero shots

---

## 2. Focal Length

Focal length is the single most under-used realism lever. It controls **compression** — how near and far objects relate.

| Focal | Effect | Use for |
|---|---|---|
| **18–24mm** | Extreme wide. Edge distortion. Exaggerated depth. | Interior of car, tight spaces. **Never on faces.** |
| **28–35mm** | Natural documentary. Slight environmental feel. | Walk-throughs, showroom moves, group wides ← *the Douyin video* |
| **50mm** | Neutral. Approximates human eye. | Safe default. Mid shots. |
| **85mm** | Portrait compression. Background melts. Flattering. | Hero close-ups, face beats |
| **100–135mm** | Heavy compression. Subject isolated, background stacked. | Car detail, dramatic isolation |
| **Anamorphic** | Oval bokeh, horizontal flares, widescreen squeeze | Premium hero, night neon |

**Aperture** (say it explicitly):
- `T1.4–T2.0` — very shallow, one plane sharp. Hero faces.
- `T2.8–T4` — shallow but controlled. **Default for people + car.**
- `T5.6–T8` — deep focus. Group tableau where everyone must be sharp.

> **Trap:** if the prompt says "shallow depth of field" on a four-person wide, the back two go soft and become uncountable. For group tableaus use **T5.6, deep focus.**

---

## 2B. Camera Bodies — Name the Sensor

The camera body name is a **compression token**. It carries dynamic range, colour science, highlight rolloff and noise character in two words. Models are trained on millions of images tagged with these bodies, so naming one is far more efficient than describing the look longhand.

| Body | Colour science / signature | Use for |
|---|---|---|
| **ARRI Alexa 35** | The safest choice. Gentle highlight rolloff, forgiving skin, 17 stops. Reads as "expensive film." | **Default. Showroom, people, premium commercial.** ← *what we use* |
| **ARRI Alexa Mini LF** | Same science, large format. Shallower, wider, more "cinema." | Hero wides, large-format feel |
| **ARRI Alexa 65** | Huge sensor. Epic scale, extreme separation. | Landscape hero, Mt Kinabalu scope |
| **RED V-Raptor 8K VV** | Sharper, more clinical, crunchier highlights. | Hard, aggressive, performance car |
| **RED Komodo 6K** | Compact, punchy, contrasty. | Run-and-gun, action, in-car |
| **Sony Venice 2** | Beautiful low light, dual-ISO, creamy. | **Night, neon, wet street.** |
| **Blackmagic URSA 12K** | Clean, neutral, slightly digital. | Product, technical, catalogue |
| **Phantom Flex4K** | High-speed. | Slow motion only — dust, water, rubber |
| **Canon C500 II** | Warm, natural skin, documentary. | Talking head, UGC-adjacent, Nev on camera |

**Format modifier** (optional, adds a lot):
- `Super 35` — classic, tighter, more depth
- `Large format / full frame` — shallower, wider, modern premium
- `65mm / IMAX` — enormous scale

---


**Additions (user-specified role models):**
| Body | Signature | Prompt use |
|---|---|---|
| **Hasselblad (medium format)** | huge sensor, creamy falloff, editorial stills look | `shot on Hasselblad medium format` — hero STILLS, poster frames, the premium print look |
| **Sony FX3** | full-frame run-and-gun cine, superb low light | `Sony FX3, handheld documentary energy` — vlog/Mode C, night shoots, real-plate footage |
| **Sony FX6** | pro doc/commercial workhorse, clean 4K S-Cinetone | `Sony FX6, S-Cinetone` — interviews, Mode B reviews, honest commercial look |

## 2C. Lens Systems — Name the Glass

Body = sensor. **Glass = character.** This is where "cinematic" actually lives.

| Lens system | Character | Use for |
|---|---|---|
| **Cooke S7/i** | "Cooke Look" — warm, soft rolloff, flattering skin, gentle bokeh | **People. Default for faces.** |
| **Cooke Anamorphic/i** | Cooke warmth + oval bokeh + horizontal flare | Hero, premium, night |
| **ARRI Signature Prime** | Clean, modern, natural, slight warmth. Very neutral. | Corporate, showroom, safe |
| **Zeiss Supreme Prime** | Sharp, clinical, high contrast, precise | Product, technical, detail |
| **Zeiss Master Prime** | Extremely sharp, neutral, "no character" | Car detail macro |
| **Panavision C-Series Anamorphic** | Vintage, dreamy, heavy flare, soft edges | Retro JDM, nostalgic |
| **Panavision E-Series Anamorphic** | Cleaner anamorphic, controlled flare | Modern hero |
| **Leica Summilux-C** | Crisp centre, beautiful falloff, rich | Luxury, editorial |
| **Angénieux Optimo zoom** | Smooth zooms, consistent | Moves that zoom |
| **Vintage Canon K35** | Warm, flarey, soft, golden | Kampung, heritage, warmth |

**Anamorphic vs spherical — pick deliberately:**
- **Spherical** — round bokeh, no flare, clean. Corporate, showroom, product. *(The Douyin video is spherical.)*
- **Anamorphic** — oval bokeh, blue horizontal flares, widescreen squeeze. Hero, night, drama. Costs realism, buys drama.

**Full camera line — the format:**
```
Shot on [BODY], [LENS SYSTEM] [FOCAL]mm, [T-STOP], [FORMAT].
```
Example:
```
Shot on ARRI Alexa 35, ARRI Signature Prime 35mm, T5.6, Super 35.
```

---

## 2D. Camera Modes — POV / Selfie (the native short-form format)

Learned from a Seedance 2.0 showcase (arm's-length street selfie). This is a **format**, not just a shot — and it's the single most native short-form framing there is. The camera *is* the subject's own hand. It reads as authentic and un-produced, which is exactly why it converts on FYP feeds.

| Element | Prompt language |
|---|---|
| **The framing** | `POV selfie, arm's-length distance, the subject holds the camera themselves` |
| **The distance** | one bent-arm length — close, intimate, face fills the upper frame |
| **Natural sway** | `subtle handheld sway, as if held in one hand` — never a locked tripod |
| **Direct address** | subject looks INTO the lens — it's the "main character talking to you" format |
| **Best for** | Nev-to-camera, lifestyle, relatable/vlog, product-in-hand |

**Structure it as timed micro-beats** (like the YUNER reference): front-facing → side profile → turn/back → tight face beat. Each 2–2.5s, one expression each. The prompt names each beat with its own timestamp and its own micro-expression.

> **Why it works:** it's the opposite of the polished showroom look, and that's the point. For Mode B/C where trust matters, POV selfie reads as *real person*, not *ad*. Pair it with §7B (prop-as-motion) and the Emotion Engine (07) and you have a complete relatable-format toolkit.

---

## 2E. Cinematic Mode — the "AI movie" look (learned from a Seedance showcase)

A 61-second cinematic showcase revealed how the hyper-real *film* look is prompted — it's a different register from the clean commercial look. The recurring ingredients:

| Element | What drives the cinematic feel |
|---|---|
| **Extreme dynamic camera** | `FPV drone move` · `whip-pan` · `crash-zoom` · `360 orbit` · `camera barrels through the space` — motion that a real crew *couldn't* do is what reads as "epic AI film" |
| **Surreal-but-physical** | one impossible thing (time freezes, gravity flips) rendered with *rigorous* real physics everywhere else |
| **Backlit silhouette / lens flare** | `low-angle orbit, backlit silhouette, anamorphic flare` — the single most "movie" lighting cue |
| **Scale & speed** | tiny-to-huge reveals, speed ramps (slow-mo → real-time snap) |
| **Heavy atmosphere** | `dust, haze, volumetric light shafts, floating particles` — atmosphere hides AI flaws AND reads as cinema |
| **Desaturated filmic grade** | crushed blacks, teal shadows, bleach-bypass — never clean/bright |

> **The cinematic prompt formula:** `[impossible camera move] through [atmospheric environment], [backlit/flare lighting], [film stock + grade], [one surreal element], photoreal physics, anamorphic, 24fps.`
> This is the register for a **hero brand film** — not the showroom clean look. Reach for it when the goal is *awe*, not *clarity*.

---

## 2F. The Chaptered Long-Form Structure (the 30–60s answer)

The same showcase solved the **30s+ retention problem** the log flagged. Its cut map (measured): hook at 1.8s → then **~13-second content pods, each separated by a rapid DOUBLE-CUT transition** (two cuts ~1.5s apart).

```
0–2s     HOOK          (one arresting shot)
2–15s    POD 1         (one idea / one location)
15–17s   ⚡ double-cut  (rapid re-hook transition)
17–26s   POD 2
26–28s   ⚡ double-cut
28–40s   POD 3
40–42s   ⚡ double-cut
...       repeat
```

**Why it works:** the double-cut every ~13s is a *scheduled pattern interrupt* — it re-grabs attention right when a pod would start to sag. This is the automatable template for long-form: **fixed pod length + a fixed rapid-transition between pods + one music bed over the whole thing.** The Editor seat can execute this as a timeline.

> **For a multi-car or "day in the life" video:** each pod = one car / one moment, the double-cut = the beat-synced transition between them. Solves both the 30s stitch AND keeps retention from decaying.

---

## 2G. The Real-Plate Technique — shoot the environment, generate only the impossible

*From the "vault on the desk" tutorial reference. The highest-realism workflow available — and the direct fix for POV unnaturalness (log #8).*

1. **Shoot a real plate** — phone photo/short clip of the ACTUAL environment (desk, showroom floor, car bonnet). 0.5x wide, natural light, your real hand in frame if needed.
2. **Feed it as the start frame / image reference.**
3. **Prompt ONLY the impossible EVENT into it** — "a miniature glowing [car/structure] materializes on the desk, volumetric fog, loading ring." Environment, lighting, hand are already real; the model renders only the magic.

**Why it wins:** realism is *inherited, not generated*. AI's weakest jobs (environment coherence, hand physics, camera motion) are handled by reality; its strongest (an impossible object + light interaction) is all it does.
**The tutorial's cut pattern (Recipe 6 in file 11):** result-first hook ("How to do this" + arrow) → ~5s process pods → a LONG 20s payoff hold of the finished result → fast 3-cut CTA outro. A long hold works when it IS the promised payoff.

---

## 2H. The Talking-Head Setup — the zero-credit authority look

*From the 2:40 knowledge-creator reference. No AI, no render risk — the format that wins on trust.*

| Element | Spec |
|---|---|
| Framing | static **medium close-up**, chest up, subject centred-ish, never moves |
| Lens feel | ~50–85mm equivalent, shallow DOF, background softly blurred |
| Light | soft front key, neutral, even on the face; a gentle rim on the hair |
| Background | **personality set-dressing** — a shelf of objects that say WHO you are (her figurines = the persona). For Nev: die-cast models, a workshop wall, keys on hooks |
| Mic | lapel mic **visible**, and left in when she adjusts it on camera — authenticity beats polish |
| Grade | natural, slightly high saturation. No filmic crush |
| Camera | static with faint handheld life. Zero moves, zero reframes |

**The insight:** production value here is near-zero and it doesn't matter. Authority comes from density (Recipe 7's jump-cut rule), gesture, and eye contact — not from cameras. This is the cheapest high-trust format available to Talyx.

---

## 2I. ⚡ THE MULTI-SHOT SINGLE-GENERATION TEMPLATE — the car cinematic master prompt

*Proven on a user-generated 15s Audi R8 film (log #26). **This supersedes clip-by-clip generation for cinematic work.** One prompt produced 9 shots, 15 seconds, with dissolves and match-cuts generated IN-MODEL. No stitching, no identity drift, no per-clip approval loop.*

**Why it wins:** clip-by-clip cost ~45-54cr per 5s clip plus assembly plus drift-hiding transitions. This delivers a finished 15s multi-shot film in ONE job. Fewer credits, zero seams, consistent car identity.

### The architecture — three blocks, always in this order
```
BLOCK 1 — GLOBAL SPEC (one paragraph, sets everything)
   subject + "Multi-shot sequence with [transition style] between every shot"
   + lighting + mood + palette + camera body + lens + DOF + grain

BLOCK 2 — TIMESTAMPED SHOT LIST (numbered, each with its own time window)
   N. (start-end s) [shot size] [angle] of [subject detail],
      [camera move], [light behaviour], [background element]

BLOCK 3 — CONSISTENCY FOOTER (the drift killer)
   "Smooth seamless transitions between every shot — no hard cuts.
    Consistent lighting, color grade, and car identity across all shots.
    Photorealistic, ultra-detailed, cinematic quality."
```

### The proven shot rhythm (9 shots / 15s)
| # | Window | Shot | Purpose |
|---|---|---|---|
| 1 | 0–1.5s | low wide, front, slow push-in | establish + hook |
| 2 | 1.5–3s | ECU wheel / brake disc, drift along sidewall | texture |
| 3 | 3–4.5s | rear 3/4 close, taillights + diffuser, gimbal orbit | detail |
| 4 | **4.5–7.5s** | **tracking medium-wide, car DRIVING, parallel, low** | **the hero — longest shot, 2× the others** |
| 5 | 7.5–9s | ECU wheel stationary, caliper, rim light on spokes | breath |
| 6 | 9–10.5s | low front 3/4, grille + headlights, gimbal drift | face |
| 7 | 10.5–12s | orbit to rear 3/4, wing + taillights | turn |
| 8 | 12–13.5s | side profile wide, long shadows, sun flare at edge | silhouette |
| 9 | 13.5–15s | **slow crane pull-back high wide**, long shadow, sky | resolve |

> **The law: every shot 1.5s EXCEPT the driving hero at 3s.** Detail-detail-MOTION-detail is the rhythm. Open static, close with a crane pull-back — the pull-back is what makes it feel like a film instead of a reel.

### Locked look (proven)
`golden hour, low warm backlit sun, strong rim light, sharp specular reflections, desaturated palette with warm amber highlights, deep shadows, high contrast, ARRI Alexa, anamorphic lens, shallow DOF, subtle film grain`

### Rules learned
- **Transitions are GENERATED, not edited.** Name them per shot: *smooth dissolve · match-cut dissolve · orbit dissolve*. Measured: most shot changes were so soft they didn't trip scene-detection at all.
- **No negative prompt needed.** Specificity crowds out failure — 9 precisely described shots leave no room to hallucinate.
- **The consistency footer is mandatory.** It's what holds car identity + grade across all 9 shots. This replaces mask/object-wipe transitions as the primary drift fix.
- **Aspect:** the reference rendered 1280×720 landscape. **For FB/TikTok/IG, specify 9:16 explicitly** or the deliverable needs reframing.
- **Known gap (user-noted):** no cut-to-beat. Fix in edit — layer 2–3 hard cuts on music beats over the dissolve bed, or add `two sharp hard cuts on the beat at [t]` to Block 2.

---

## 3. Environment Setting

Specify in this order — the model reads it hierarchically:

1. **Space type** — `modern minimalist car showroom`
2. **Scale** — `spacious, high ceiling, open volume`
3. **Architecture** — `white walls, clean lines, glass frontage`
4. **Floor** — `mirror-polished concrete` ← *huge realism driver, see §6*
5. **Contents & placement** — `three cars staggered: red left, blue centre, black right`
6. **Condition** — `pristine, showroom-clean, no clutter`

**Sabah/Malaysia environment bank:**
| Environment | Signature detail |
|---|---|
| KK coastal road, blue hour | Wet asphalt, South China Sea, palm silhouettes |
| Mt Kinabalu highland | Mist, cool light, laterite red soil |
| Wet KL night street | Neon shoplot signage, standing water, halation |
| Kampung road / plantation | Dappled light through palms, red dust |
| Underground carpark | Hard overhead strips, concrete, deep shadow |
| White showroom | Polished floor, skylights, clean reflections |

---

## 4. Lighting — Environment vs Character

These are **two separate blocks**. Most prompts only write one and the result looks flat and fake.

### 4A. Environment Lighting (the SPACE)
- **Source** — `overhead skylights` / `LED strip ceiling` / `floor-to-ceiling windows` / `sodium streetlights`
- **Quality** — `soft, diffused` (large source) vs `hard, directional` (small source)
- **Direction** — `top-down` / `side-window` / `wraparound`
- **Level** — `high-key, bright, even` vs `low-key, pooled, deep shadow`
- **Spill** — `light bouncing off the polished floor back up onto the subjects`

### 4B. Character Lighting (the FACE)
- **Key** — `soft key from camera-left, 45 degrees, large source`
- **Fill ratio** — `2:1` (commercial, gentle) / `4:1` (dramatic) / `8:1` (hard, moody)
- **Rim / backlight** — `subtle rim light separating hair and shoulder from the background`
- **Catchlight** — `a soft catchlight in the eyes` ← **the single strongest "alive" cue**
- **Practicals** — light sources visible in frame (headlights, signage, ceiling strips)

**Ratio guide:**
| Ratio | Feel | Use |
|---|---|---|
| 1:1 | Flat, clean, commercial | Corporate, showroom |
| 2:1 | Gentle modelling | **Default. Premium and safe.** |
| 4:1 | Dramatic, sculpted | Hero, aggressive |
| 8:1+ | Noir, hard | Night, tension |

---

## 5. Colour Control

- **Palette discipline** — `limited palette: white, red, blue, black only`. A restrained palette reads as *expensive*. This is the #1 thing amateurs miss.
- **White balance** — `cool-white (5600K)` / `tungsten (3200K)` / `mixed: tungsten interior, blue exterior spill`
- **Saturation** — `low saturation with one saturated accent (the red car)`
- **Black level** — `lifted blacks, no crush` (filmic) vs `deep crushed blacks` (contrasty)
- **Skin protection** — `natural, accurate skin tone, not orange, not waxy`

---

## 6. Reflections — Your Highest-Leverage Line

For car content, reflections are the difference between real and CGI. **Always specify. Never assume.**

```
Physically accurate reflections: mirror-polished floor throwing clean
inverted reflections of the cars and figures; environment reflected in
the paintwork with correct curvature; accurate specular highlights on
chrome and glass; no floating or detached shadows.
```

**Reflection surfaces to name:**
- Polished floor (showroom) — inverted mirror image
- Car paint — the *environment* curving across the panels
- Glass / windscreen — sky and ceiling
- Chrome / grille — sharp, distorted specular
- Wet asphalt (exterior) — the cheapest cinematic upgrade available in Malaysia
- Eyes — catchlight (§4B)

**Anti-CGI phrase:** `contact shadows where tyres meet the floor` — stops the car "floating," which is the #1 AI tell.

---

## 7. Frame & Composition

- **Aspect** — `9:16 vertical` (FB/TikTok) or `16:9`
- **Shot size** — ECU / CU / MCU / MS / MW / WS / EWS
- **Depth layers** — **name all three.** `foreground: defocused figure crossing; midground: hero subject; background: cars and architecture`
- **Foreground occlusion** — someone/something passing close to the lens. **Massive realism cue.** The Douyin video uses this at 1–3s as a wipe.
- **Headroom / lead room** — `slight headroom, subject looking into frame space`
- **Symmetry** — `symmetrical composition, centre-weighted` (formal, powerful) vs `rule of thirds` (natural)
- **Countability** — if N people must be visible, say `all N clearly visible and countable at a glance, no occlusion`

---

## 8. Camera Movement

| Move | Prompt phrase | Feel |
|---|---|---|
| Orbit | `smooth horizontal orbit around the subject` | Reveal, premium |
| Dolly back | `camera retreats smoothly` | Expanding, revelatory |
| Arc | `arcs to the left while retreating` | Elegant, complex |
| Push in | `slow push in on the subject` | Intensity |
| Crane up/down | `slow crane rise` | Scale, scope |
| Rack focus | `focus racks from foreground to background` | Directs attention |
| Locked off | `static locked-off frame` | Formality, tension |

**The single-take rule:** if you want the Douyin look, this line is non-negotiable —

```
ONE SINGLE UNBROKEN CONTINUOUS TAKE. No cuts, no flicker,
no post-production transitions of any kind.
```

A montage of stitched 5s clips reads as AI slop. One unbroken 15s move reads as a film crew.

---

## 9. Mood

One line, three words maximum. Vague mood words get ignored; concrete ones land.

Good: `professionalism, confidence, team power` · `restrained luxury` · `quiet menace` · `nostalgic warmth`
Bad: `cinematic` · `epic` · `amazing` · `high quality`

---

## 10. Micro-Expressions & Gestures

**Write verbs, not adjectives.** Behaviour is safe; appearance gets you flagged (§12).

### Face bank
- single slow blink · brief unblinking hold · eyes flick left, then return to lens
- micro-nod, barely perceptible · chin lifts one degree
- one corner of the mouth lifts for half a second, then returns to neutral
- jaw tightens · brow softens · a swallow · breath in through the nose

### Body bank
- turns the head first, eyes follow a beat later ← **strongest realism cue there is**
- weight shifts from one foot to the other
- arms fold, right over left, settling with weight
- fingers uncurl slowly from a fist
- a hand slides into a jacket pocket, thumb out
- adjusts a cuff once, without looking

### Three hard rules
1. **One beat per second, maximum.** More and the model smears them together.
2. **Anchor every beat to a timestamp.** Untimed gestures fire randomly or not at all.
3. **Name the reset.** `…then returns to neutral.` Without it, expressions freeze and hold — the classic AI tell.
4. **Stagger across characters.** Real people don't move in unison.

```
3-8s: Camera retreats and arcs left.
  · Staff 3 turns the head first, eyes follow a beat later.
  · At 4s: one slow blink, gaze stays on the lens.
  · At 5s: arms fold, right over left, settling with weight.
  · At 6s: barely perceptible chin lift, then neutral.
  · Staff 4, behind: shifts weight to the back foot at 6s.
```

---

## 11. Realism Anchors & Negative Bank

**Anchors — paste every time:**
```
Shot on ARRI Alexa 35, [FOCAL]mm [LENS TYPE], [T-STOP].
[FILM STOCK] aesthetic, [GRAIN] film grain.
Natural motion blur. Photoreal skin texture with visible pores.
Accurate panel gaps, accurate wheel geometry, correct badging.
Physically accurate reflections. Contact shadows.
24fps.
```

**Negative bank — paste every time:**
```
Negative: cuts, jump cuts, flicker, post transitions, CGI plastic look,
warped rims, floating car, extra wheels, melting badge, deformed hands,
extra fingers, text artifacts, oversaturated HDR, cartoon, waxy skin,
frozen expression, missing person, duplicated person.
```

---

## 12. Moderation — The Rules That Cost Us a Failed Job

Seedance/ByteDance moderation flags **appearance**, not behaviour. A job flagged `nsfw` **auto-refunds** — it costs time, not credits — but it kills your momentum.

| ❌ Triggers a flag | ✅ Passes clean |
|---|---|
| "four young women" | "four professional staff members" |
| ethnicity tags (Malay, Chinese, Kadazan-Dusun…) | *(omit entirely — refs carry it)* |
| "delicate refined features", "flawless skin" | *(omit entirely — refs carry it)* |
| "fashion-model energy", "alluring", "charisma" | *(omit entirely)* |
| "a sensual, confident smile" | "one corner of the mouth lifts, then neutral" |
| framing as beauty/model content | framing as **"corporate brand film"** |

**Iron rule:** the prompt must contain **zero** words describing what a person *looks like*. Only what they *do*.

If it still flags with a clean prompt, the **reference images** are the trigger — regenerate them more corporate-neutral (plain business headshots, less editorial).

---

## 12B. UNIVERSAL BLOCKS — paste these into anything

These are **model-agnostic**. They work in Seedance, Kling, Veo, Sora. Build every prompt by stacking blocks.

### U1 — Universal Realism Block *(paste in EVERY prompt, no exceptions)*
```
Shot on ARRI Alexa 35, ARRI Signature Prime 35mm, T4, Super 35.
Kodak Vision3 500T aesthetic, fine 35mm film grain, 24fps.
Natural motion blur. Photoreal skin texture with visible pores and fine
flyaway hairs. Natural fabric drape and weight.
Physically accurate reflections and specular highlights.
Contact shadows where every object meets the ground.
Accurate panel gaps, accurate wheel geometry, correct badging.
```

### U2 — Universal Negative Block *(paste in EVERY prompt)*
```
Negative: cuts, jump cuts, flicker, post-production transitions, CGI plastic
look, waxy skin, warped rims, floating object, extra wheels, melting badge,
deformed hands, extra fingers, text artifacts, watermark, oversaturated HDR,
cartoon, frozen expression, missing person, duplicated person, distorted face.
```

### U3 — Universal Single-Take Block *(for the Douyin look)*
```
ONE SINGLE UNBROKEN CONTINUOUS TAKE from start to finish. The camera move
and the subjects' blocking must lock to the music rhythm. Absolutely no
mid-shot cuts, no frame flicker, no post-production transitions of any kind.
```

### U4 — Universal Lighting Blocks *(pick one)*

**L1 — Clean Commercial** *(showroom, corporate, product)*
```
Environment lighting: overhead skylights and diffused ceiling panels, soft,
top-down, high-key and even. Light bounces off the polished floor back up
onto the subjects.
Character lighting: soft key from camera-left at 45 degrees, large source.
2:1 fill ratio. Subtle rim light separating hair and shoulder from the
background. Soft catchlight in the eyes.
```

**L2 — Blue Hour Exterior** *(coastal, road, hero car)*
```
Environment lighting: blue-hour ambient sky as the key, warm sodium
streetlights as practicals. Soft, wraparound, low level.
Character lighting: cool ambient key, warm practical rim from behind.
4:1 fill ratio. Strong rim separation. Catchlight in the eyes.
```

**L3 — Night Neon Wet** *(KL/KK street, JDM night)*
```
Environment lighting: neon shoplot signage as coloured practicals, hard and
directional. Low-key, pooled light, deep shadow between pools. Standing water
on the asphalt doubling every light source.
Character lighting: motivated by the neon — magenta from camera-left, cyan
rim from behind. 8:1 fill ratio. Hard, sculpted. Bright catchlight.
```

### U5 — Universal Colour Blocks *(pick one)*

**C1 — Neutral Clean** *(premium, showroom)*
```
Grade: neutral clean, no colour cast. White balance 5600K cool-white.
Limited palette: white, [ACCENT 1], [ACCENT 2], black only.
Low saturation with one saturated accent. Lifted blacks, no crush.
Natural accurate skin tone, not orange, not waxy.
```

**C2 — Teal & Amber** *(hero car, commercial)*
```
Grade: teal and amber. Cool shadows, warm highlights.
White balance mixed: 3200K practicals against 5600K ambient.
Medium saturation. Deep but detailed blacks.
Skin tone protected and natural despite the grade.
```

**C3 — Cinestill Night** *(neon, wet, JDM)*
```
Grade: Cinestill 800T aesthetic. Halated red highlights, neon bloom.
White balance tungsten 3200K with cool exterior spill.
High saturation in the practicals, desaturated in the shadows.
Crushed blacks. Skin tone protected.
```

### U6 — Universal Reflection Block *(car content — always)*
```
Physically accurate reflections: the environment curving correctly across the
paintwork with proper surface curvature; sharp distorted specular highlights
on chrome and the grille; sky and ceiling reflected in the glass; a clean
inverted mirror image on the polished floor / wet asphalt.
Contact shadows where the tyres meet the ground. The car is grounded, not
floating.
```

### U7 — Universal Micro-Expression Block *(timestamped — edit the times)*
```
Micro-performance, staggered, never in unison:
· At [T]s: turns the head first, eyes follow a beat later.
· At [T]s: one slow blink, gaze stays on the lens.
· At [T]s: arms fold, right over left, settling with weight.
· At [T]s: a barely perceptible chin lift, then returns to neutral.
· At [T]s: weight shifts to the back foot.
Expressions always return to neutral. Nothing freezes or holds.
```

### U8 — Universal Moderation-Safe Subject Block
```
[N] professional staff members, matching the [N] reference images exactly.
All wear [WARDROBE]. Formal, composed, corporate.
Reference image 1 = Staff 1. Reference image 2 = Staff 2. [etc.]
```
> Contains **zero** appearance words. That is the whole point. §12.

### U9 — Universal Audio Block
```
Rhythmic, driving, premium commercial music bed. Supported by faint air
movement during the camera move, crisp footsteps on the hard floor, and the
subtle rustle of fabric. No voiceover and no dialogue at any point.
```

### U10 — Universal Count-Lock Block *(for multi-person shots)*
```
Exactly [N] people visible. Not [N-1]. Not [N+1]. All [N] fully visible and
countable at a glance in the final wide frame, no occlusion by any object or
any other person. Do not merge, duplicate or omit anyone.
```

---

## 12C. FOUR READY-TO-RUN UNIVERSAL PROMPTS

Fill the brackets and go. Each is a complete, moderation-safe prompt.

### P1 — Showroom Group Tableau *(the Douyin format)*
```
Corporate brand film for a car dealership. ONE SINGLE UNBROKEN CONTINUOUS
TAKE. No cuts, no flicker, no post-production transitions.

SETTING: Modern minimalist performance-car showroom. Spacious, high ceiling,
white architecture. Mirror-polished floor. Three cars staggered: [CAR 1,
COLOUR] at far left, [CAR 2, COLOUR] centre, [CAR 3, COLOUR] at right.
Pristine, showroom-clean.

SUBJECTS: Four professional staff members, matching the four reference images
exactly. All wear crisp white tailored business suits. Formal, composed.
Reference image 1 = Staff 1. Image 2 = Staff 2. Image 3 = Staff 3 (centre).
Image 4 = Staff 4.

CAMERA: Shot on ARRI Alexa 35, ARRI Signature Prime 35mm, T5.6, Super 35.
Deep focus — all four subjects sharp.
Movement: smooth horizontal orbit, then retreat, then arc left, settling into
a locked symmetrical wide.
Frame: 9:16 vertical. Depth: defocused foreground figure crossing; midground
hero subject; background cars and architecture.

CHOREOGRAPHY:
0-1s:  Medium-close. Camera orbits horizontally. Staff 1 centred, head
       lowered, focused. At 1s: a single slow blink.
1-3s:  Staff 2 crosses the extreme foreground, creating a defocused wipe.
       Focus racks to Staff 3 behind. Staff 3 turns the head first, eyes
       follow a beat later, then holds the lens.
3-8s:  Camera retreats and arcs left. The centre car enters frame behind
       Staff 3. At 5s: Staff 3 folds arms, right over left, settling with
       weight. At 6s: a barely perceptible chin lift, then neutral. Staff 4
       becomes visible behind-left, shifting weight to the back foot at 7s.
8-15s: Camera retreats and pans left, locking to a wide symmetrical frame.
       Staff 2 beside the left car, Staff 1 on the right, Staff 3 centred in
       front of the centre car, Staff 4 behind-left of Staff 3 but fully
       visible.

[PASTE L1] [PASTE C1] [PASTE U6] [PASTE U9] [PASTE U10] [PASTE U1] [PASTE U2]

MOOD: Professionalism, confidence, team power.
```

### P2 — Hero Car Exterior *(blue hour, single unbroken orbit)*
```
Automotive brand film. ONE SINGLE UNBROKEN CONTINUOUS TAKE.

SUBJECT: A [YEAR] [CAR] in [COLOUR], stationary on wet asphalt.
Pristine bodywork, accurate panel gaps, accurate wheel geometry, correct
badging.

SETTING: [ENVIRONMENT — e.g. empty Kota Kinabalu coastal road], blue hour,
just after tropical rain. Standing water on the road. [BACKDROP] in soft haze.
Humid air.

CAMERA: Shot on ARRI Alexa Mini LF, Cooke Anamorphic/i 40mm, T2.8, large
format.
Movement: starts on a macro detail of the front badge, cranes back and orbits
left around the car, finishing on a low three-quarter hero angle.
Frame: 9:16 vertical. Low camera height, at bumper level.

[PASTE L2] [PASTE C2] [PASTE U6] [PASTE U1] [PASTE U2]

MOOD: Restrained luxury, stillness, weight.
```

### P3 — Night Neon Street *(JDM, wet, dramatic)*
```
Automotive brand film. ONE SINGLE UNBROKEN CONTINUOUS TAKE.

SUBJECT: A [YEAR] [CAR] in [COLOUR], rolling slowly through the frame.

SETTING: Rain-soaked [CITY] street at night. Neon shoplot signage. Standing
water doubling every light source. Wet asphalt. Empty, late.

CAMERA: Shot on Sony Venice 2, Panavision E-Series Anamorphic 50mm, T2.0.
Movement: low gimbal dolly tracking parallel to the car at bumper height,
continuous, no cuts.
Frame: 9:16 vertical. Depth: foreground rain streaks; midground car;
background neon bokeh.

[PASTE L3] [PASTE C3] [PASTE U6] [PASTE U1] [PASTE U2]

MOOD: Quiet menace, isolation, control.
```

### P4 — Presenter Walkaround *(for Nev on camera)*
```
Automotive presenter piece. ONE SINGLE UNBROKEN CONTINUOUS TAKE.

SUBJECT: One professional presenter, matching the reference image exactly.
Wearing [WARDROBE]. Composed, confident, addressing the lens directly.

SETTING: [ENVIRONMENT]. A [YEAR] [CAR] in [COLOUR] behind and to the side.

CAMERA: Shot on Canon C500 II, Cooke S7/i 50mm, T2.8.
Movement: slow steadicam arc, following the presenter as they walk the length
of the car, keeping them at frame-left with the car revealed behind.
Frame: 9:16 vertical, medium shot, slight headroom, lead room ahead of the walk.

PERFORMANCE:
· Presenter walks at an unhurried pace, one hand gesturing open-palm toward
  the car, the other relaxed.
· At 3s: turns the head to the car, then back to the lens a beat later.
· At 6s: a single slow blink, then a small nod.
· At 9s: one hand slides into a jacket pocket, thumb out.
· Expressions always return to neutral. Nothing freezes.

[PASTE L1 or L2] [PASTE C1] [PASTE U6] [PASTE U1] [PASTE U2]

MOOD: Trustworthy, knowledgeable, relaxed.
```

---

## 13. THE TEMPLATE — copy, fill, ship

```
[GENRE FRAME]: Corporate brand film for [CLIENT].
ONE SINGLE UNBROKEN CONTINUOUS TAKE. No cuts, no flicker, no transitions.

[SETTING]
[SPACE TYPE], [SCALE], [ARCHITECTURE].
Floor: [FLOOR SURFACE].
Contents: [OBJECT 1] at [POSITION], [OBJECT 2] at [POSITION], [OBJECT 3] at [POSITION].
Condition: pristine, accurate panel gaps, accurate wheel geometry, correct badging.

[SUBJECTS]
[N] professional [ROLE] staff members, matching the [N] reference images exactly.
All wear [WARDROBE]. Formal, composed.
Reference image 1 = Staff 1. Reference image 2 = Staff 2. [etc.]

[CAMERA]
Body: [CAMERA BODY]. Glass: [LENS SYSTEM] [FOCAL]mm, [T-STOP], [FORMAT].
Movement: [MOVE GRAMMAR].
Frame: [ASPECT], [SHOT SIZE], [SYMMETRY].
Depth: foreground [X], midground [Y], background [Z].

[CHOREOGRAPHY — timestamped]
0-1s:  [BLOCKING] + [MICRO-BEAT]
1-3s:  [BLOCKING] + [MICRO-BEAT]
3-8s:  [BLOCKING] + [MICRO-BEAT]
8-15s: [FINAL TABLEAU]. All [N] clearly visible and countable at a glance,
       no occlusion by any object or any other person.

[ENVIRONMENT LIGHTING]
Source: [SOURCE]. Quality: [soft/hard]. Direction: [DIR]. Level: [high-key/low-key].
Spill: [BOUNCE].

[CHARACTER LIGHTING]
Key: [DIRECTION + SIZE]. Fill ratio: [X:1]. Rim: [YES/NO].
Soft catchlight in the eyes.

[COLOUR]
Grade: [GRADE FAMILY]. White balance: [K].
Palette: limited — [COLOUR 1], [COLOUR 2], [COLOUR 3] only.
Saturation: [LEVEL]. Blacks: [lifted/crushed].
Natural accurate skin tone.

[REFLECTIONS]
Physically accurate reflections: [FLOOR], [PAINTWORK], [GLASS], [CHROME].
Contact shadows where tyres meet the floor.

[MOOD]
[THREE WORDS].

[LOOK]
Shot on ARRI Alexa 35, [FILM STOCK] aesthetic, [GRAIN] film grain.
Natural motion blur, photoreal skin texture. 24fps.

[AUDIO]
[MUSIC BED]. [DIEGETIC SFX]. No voiceover, no dialogue.

[CONSTRAINTS]
Exactly [N] staff members visible. Not [N-1]. Not [N+1].
All [N] fully visible in the final wide frame.
Do not merge, duplicate or omit anyone.

[NEGATIVE]
cuts, jump cuts, flicker, post transitions, CGI plastic look, warped rims,
floating car, extra wheels, melting badge, deformed hands, extra fingers,
text artifacts, oversaturated HDR, cartoon, waxy skin, frozen expression.
```

---

## 14. Step-by-Step Pipeline (Higgsfield)

| # | Step | Tool | Cost | Notes |
|---|---|---|---|---|
| 1 | Generate character references | **Soul 2.0**, 9:16, 2k | ~0.12 cr each | Neutral, corporate, well-lit. Reuse forever. |
| 2 | Source car references | Real photos | free | **Non-negotiable for JDM.** Wrong grille = roasted in comments. |
| 3 | *(optional)* Save as Reference Elements | Elements | free | Makes them reusable across all models |
| 4 | *(optional)* Build the group start frame | Nano Banana Pro | low | Locks blocking **in a still** before spending on video. 10× cheaper reroll. |
| 5 | Preflight cost | `get_cost: true` | free | Always |
| 6 | Generate the take | **Seedance 2.0**, 15s, 1080p, std, high bitrate | ~135 cr | `image_references` = your character refs |
| 7 | Decline any auto-preset | — | — | Presets override your whole look |
| 8 | QC (see §15) | — | — | |
| 9 | Upscale if keeping | Upscale Video, `aigc` preset | — | 2K/4K |

**Model choice, settled:**
- **Seedance 2.0** — *multiple* `image_references` (up to 9). Identity lock. **This is why it wins for people.**
- **Kling 3.0** — only accepts `start_image`. Better for motion transfer / multi-shot. Not for multi-character identity.
- **Kling 3.0 Motion Control** — film yourself doing the gesture, transfer it onto a character still. Real human micro-timing. **One character per pass.**

---

## 15. QC Checklist — run on every output

- [ ] Correct number of people? All visible in the final wide?
- [ ] Wardrobe colour held? (no drift to grey/black)
- [ ] Any hard cut mid-take? (kills the single-take illusion)
- [ ] Car badges, grille, panel gaps, lug nuts correct?
- [ ] Wheels round, not warped? Contact shadows present?
- [ ] Hands — five fingers, no melting?
- [ ] Expressions reset, or frozen in place?
- [ ] Reflections physically plausible?
- [ ] Skin — pores and texture, or waxy plastic?

---

## 16. Failure Playbook

| Symptom | Fix |
|---|---|
| `nsfw` / refunded | Strip **all** appearance language. Reframe as corporate. §12 |
| Person missing from the wide | Reduce headcount. Or lock blocking in a still first (§14 step 4) |
| Faces drift over 15s | More/better reference images. Shorten to 10s. |
| Car looks wrong | Real car photos as references. Non-negotiable. |
| Looks like CGI | Add: reflections, contact shadows, film grain, motion blur, skin texture |
| Feels stiff / dead | Add timestamped micro-beats (§10). Stagger them. |
| Frozen smile | Add `…then returns to neutral` |
| Cheap-looking | Restrict the palette. Limited colour = expensive. |
| Back of group out of focus | Deep focus, T5.6. Not shallow. |

---

## 17. Worked Example — the JDM Showroom (our actual build)

- **Genre frame:** Corporate brand film for a car dealership
- **Setting:** Modern minimalist performance-car showroom, spacious, white, mirror-polished floor. Red Toyota Supra A80 left, blue Nissan Skyline GT-R R34 centre, gloss black Nissan GT-R R35 right.
- **Subjects:** 4 staff, white tailored business suits, from 4 reference images
- **Lens:** 35mm spherical, T5.6 (deep — all four must be countable)
- **Movement:** Orbit → retreat → arc left → lock to symmetrical wide
- **Env lighting:** Overhead skylights, soft, top-down, high-key. Floor bounce back up onto subjects.
- **Character lighting:** Soft key camera-left 45°, 2:1 fill, subtle rim, catchlight in eyes
- **Colour:** Neutral clean grade, 5600K cool-white. Palette: white, red, blue, black only. Low sat, lifted blacks.
- **Reflections:** Mirror floor inversion, environment curving across paintwork, chrome specular, contact shadows at tyres
- **Mood:** Professionalism, confidence, team power
- **Look:** ARRI Alexa 35, Kodak Vision3 500T, fine 35mm grain, 24fps
- **Audio:** Rhythmic premium commercial bed, footsteps on polished floor, fabric rustle. No VO.
- **Constraint:** Exactly four. Not three. All four in the final wide.

---

## 18. Build These Once, Reuse Forever

1. **Character bank** — 4 locked staff references. Same faces every video = brand asset.
2. **Car bank** — real reference photos of every unit in inventory.
3. **Gesture bank** — 30–40 tested micro-beats, tagged by emotion and body part.
4. **Environment bank** — 6 Sabah/Malaysia settings, pre-written.
5. **The template above** — with `[CAR]`, `[COLOUR]`, `[ENVIRONMENT]` as the only variables.

New stock arrives → new hero video, same crew, same 15s take, 10 minutes of work.

That's the system. Everything else is assembly.
