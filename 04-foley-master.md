# The Foley Master
### Seat [3B] — sits alongside the DOP. Owns everything you hear.
### Talyx / Nev — companion to `ai-video-crew-roles.md`

---

## ⚠️ Read This First — I Got This Wrong

**I have been telling you to generate videos with the audio OFF.**

For multi-clip stitching, that advice is correct — mismatched native audio exposes every seam.

**For a POV interior video, it is catastrophically wrong.**

> **In "POV: First Time Sitting Inside," the sound IS the content.**
> The door thunk. The leather creak. The seatbelt click. The switch that goes *chunk*.
>
> Take the sound away and you have a nice-looking interior shot. Add it, and the viewer *feels* the car.

**Sound is 50% of realism, and it is the half nobody prompts.** That's the gap this seat closes.

---

## Role Models

| # | Who | Steal |
|---|---|---|
| 1 | **Ben Burtt** *(Star Wars, WALL-E)* | **Master of making sounds that don't exist feel inevitable.** The lightsaber. R2-D2. WALL-E — a feature-length film where the lead character has **no dialogue and you understand every emotion through sound.** That is Mode A. |
| 2 | **Nicolas Becker** *(Sound of Metal)* | **The best modern reference for subjective, first-person sound.** The entire film puts you *inside someone's head*. **POV video is a sound problem before it's a picture problem — Becker is the manual.** |
| 3 | **Gary Rydstrom** *(Jurassic Park, Saving Private Ryan)* | Physical impact. **Weight through sound.** He makes you feel mass — the same job the Performance Master does with bodies, done with ears. |
| 4 | **Erik Aadahl & Ethan Van der Ryn** *(A Quiet Place)* | **Silence as an instrument.** They prove the loudest moment is the one *before* the sound. **Restraint. Space. The drop-out.** |
| 5 | **Jack Foley** *(the man the craft is named after)* | The original. **Sound performed by a human body in real time** — footsteps, fabric, props. Every foley artist since is doing his job. |

---

## The Automotive Sound Bible

Car brands spend **millions** engineering these sounds. They are not accidents. They are the product.

| Sound | What it signals | Prompt phrase |
|---|---|---|
| **The door thunk** ⭐ | **The single most engineered sound in the car industry.** Germans obsess over it. A cheap car goes *clang*. A premium car goes **thunk** — deep, damped, final. | `a deep, damped door thunk — solid, final, expensive` |
| **Leather creak** | Realness. Materiality. Nobody fakes leather creak. | `the soft creak of leather taking weight` |
| **Seatbelt** | The ritual. Two sounds: the *reel* and the *click*. | `the smooth reel of the seatbelt, then a firm metallic click` |
| **Switchgear** | **Quality is audible.** A cheap switch is silent mush. A good one goes *chunk*. | `a solid mechanical chunk as the switch throws` |
| **Start-up** | The reveal. The character of the engine. | `the twin-turbo V6 catches, settles into a low idle` |
| **The cabin drop-out** ⭐ | **The luxury cue.** When the door closes, the *world goes quiet*. That contrast is the entire premium sell. | `outside noise drops away, the cabin goes still and quiet` |
| **Suspension settle** | Weight. Mass. | `the suspension compresses and settles as the body lands` |
| **Indicator tick** | Familiarity. Intimacy. | `a soft, precise indicator tick` |

> ⭐ **The two that matter most: the DOOR THUNK and the CABIN DROP-OUT.**
> Those two sounds *are* the feeling of sitting in an expensive car. Everything else is decoration.

---

## The Four Layers

Every video has four. Miss one and it feels thin.

| Layer | What it is | Example |
|---|---|---|
| **1. AMBIENCE** | The room tone. The floor of the mix. | Showroom hum · road noise · rain on a roof |
| **2. FOLEY** | Bodies and objects. **The realism layer.** | Footsteps · leather · fabric · switches |
| **3. HERO SFX** | The one sound that IS the moment. | The door thunk. The engine catching. |
| **4. MUSIC** | The emotional bed. | The rhythmic commercial track |

**Amateurs write only layer 4.** Music over pretty pictures. That's why it feels like a template.

---

## The Laws

### 1. The drop-out is louder than the sound
**A Quiet Place's core lesson.** The most powerful moment is the *absence*. In a POV interior video: the door closes and **the world disappears.** That silence is the luxury.
> `outside noise drops abruptly away — the cabin is still`

### 2. Sound sells weight better than picture
You *see* a car settle. You **feel** it when you hear the suspension compress. **This seat and the Performance Master are doing the same job with different tools.**

### 3. In short-form, sound is the hook
**People watch with sound on far more than the industry admits** — and ASMR-style tactile sound is one of the most reliable retention mechanics on TikTok and Reels. A crisp *click* in the first second holds a thumb.

### 4. One hero sound per video
Not five. **One.** Everything else supports it.

### 5. Silence is a tool, not an absence
Cut the music for one second before the twist. It's the cheapest, most effective dramatic device that exists.

---

## Native Audio vs Post — the decision table

| Situation | Generate audio? | Why |
|---|---|---|
| **Single hero clip, sound-led** *(POV interior)* | ✅ **ON** | Seedance's native audio is synced to the picture. Foley timing is *impossible* to fake in post without frame-perfect work. |
| **Multi-clip 30–60s stitch** | ❌ **OFF** | Native audio will never match across clips. **It exposes every seam.** Lay one continuous bed in the edit. |
| **Music-driven brand film** | ❌ **OFF** | You want *your* track, not a generated one. |
| **Dialogue** | ❌ **OFF, always** | AI lip-sync is still the weakest link in the entire stack. **Nev talks. Do not synthesise him.** |

> **Revised rule:** *Generate silent for multi-clip. Generate WITH audio for a single sound-led hero clip.*
> My earlier blanket "always off" was wrong. This table replaces it.

---

## The Audio Prompt Block — paste into any sound-led generation

```
AUDIO:
Hero sound: [the ONE sound that IS this video]
Foley: [bodies, objects, materials — be specific about the material]
Ambience: [room tone — the floor of the mix]
Music: [the bed, or "none"]
Drop-out: [where does sound fall away?]
No voiceover, no dialogue.
```

### Worked example — "POV: First Time Sitting Inside"
```
AUDIO:
Hero sound: a deep, damped door thunk — solid, final, expensive.
Foley: the soft creak of leather taking weight as the body lands; the
       suspension compressing and settling; the smooth reel of a seatbelt
       and a firm metallic click; a solid mechanical chunk as a switch throws.
Ambience: showroom air, faint and clean.
Music: a low, restrained bass pulse, entering only after the door closes.
Drop-out: at the door thunk, all outside noise falls abruptly away. The
          cabin goes still and quiet. That silence is the moment.
No voiceover, no dialogue.
```

---

## Deliverable → Technologist
```
SOUND-LED?     yes / no    → decides generate_audio ON or OFF
HERO SOUND:    [the one]
FOLEY:         [materials, contacts]
AMBIENCE:      [room tone]
MUSIC:         [bed or none]
DROP-OUT:      [where]
POST WORK:     [what gets added in the edit]
```

---

## The Line

> **The picture makes them believe it's real.**
> **The sound makes them believe they're there.**

You have spent this entire build solving for the picture.
**The other half has been silent.**
