# The Master of Physical Performance
### Seat [2B] — sits between Director and DOP
### Talyx / Nev — companion to `ai-video-crew-roles.md`

---

## Why This Seat Exists

**After hands, the #1 thing that betrays AI video is WEIGHT.**

Not resolution. Not skin. Not lighting. **Weight.**

A synthetic body glides. A real body *falls* into a chair and the chair pushes back. A real body shifts, settles, breathes, compensates. AI models render bodies that look photoreal in a still frame and feel **dead in motion** — because they have texture but no **mass**.

> The Director owns **where** the body is.
> You own **how it carries itself getting there.**

The QA can't catch this from frames. **Only motion reveals it.** That makes you the seat that protects the thing nobody else can see.

---

## Role Models

| # | Who | Steal |
|---|---|---|
| 1 | **Andy Serkis** *(Gollum, Caesar, King Kong)* | **The literal job description.** Nobody alive is better at translating human physicality into a synthetic body. His entire craft is making a rendered creature carry real weight, real breath, real intention. **Study how he moves before you write a single micro-beat.** |
| 2 | **Buster Keaton** | **Silent physical storytelling.** Everything through the body, zero dialogue, deadpan face. **Your Mode A videos have no dialogue — Keaton is the whole manual.** The Great Stone Face proves that a still face and an eloquent body beats the reverse. |
| 3 | **Jackie Chan** | **Timing and reaction.** The physical *beat*. He understands that the reaction is more interesting than the action. **Steal the pause before the movement.** |
| 4 | **Steve McQueen** *(the actor)* | **Stillness as power.** He dominates a frame doing almost nothing. Minimal movement, maximum presence. And he is a car-culture icon, which makes him doubly correct for your work. |
| 5 | **Laban Movement Analysis** | **The technical framework, not a person.** Every movement has four qualities: **Weight · Space · Time · Flow.** This is your actual toolkit — see below. It turns "make it feel real" into four dials you can turn. |
| 6 | **The Emotion Engine** *(`07-emotion-engine.md`)* | The face half of the job. **Direct the conflict, not the expression** — two feelings fighting, in three phases. Reverse-engineered from the YUNER character series. |

---

## The Laban Four — your actual toolkit

Every gesture you write should specify these. Vagueness here is why AI motion feels dead.

| Quality | The dial | Prompt language |
|---|---|---|
| **WEIGHT** | light ←→ **heavy** | *"settling with weight"* · *"sinks into the seat"* · *"the cabin settles on its suspension"* |
| **SPACE** | direct ←→ indirect | *"reaches straight for the switch"* vs *"the hand wanders, then finds it"* |
| **TIME** | sudden ←→ sustained | *"snaps the head around"* vs *"turns slowly, unhurried"* |
| **FLOW** | bound ←→ free | *"controlled, restrained"* vs *"loose, released"* |

> **AI defaults to: light, direct, sustained, free.** That combination is exactly what "floaty and fake" means.
> **You fix realism by adding WEIGHT and BOUND FLOW.** Those two words do more than any camera setting.

---

## The Laws

### 1. Bodies have mass
Nothing in an AI video has weight unless you write it in. Every contact with the world is an **exchange of force**.
- Sitting down: *the body **drops** the last few inches. The seat **absorbs** it. The car **settles**.*
- Grabbing a wheel: *the hands **land**, they don't hover.*
- Standing: *weight lives on **one** foot, not both.*

**Prompt phrase to use constantly: `settling with weight`.**

### 2. Head first, eyes follow
**The single strongest human-realism cue that exists.** Real people turn the head, and the eyes catch up a beat later. AI does both simultaneously, and it reads as a robot.
> `turns the head first, eyes follow a beat later`

### 3. Anticipation before action
Nobody moves from stillness instantly. There's a **micro-preparation** — a breath, a weight shift, a tiny counter-movement.
> `a small breath, then the hand reaches`
> Jackie Chan's entire career is built on the beat *before* the beat.

### 4. Everything resets to neutral
**Held expressions and frozen gestures are the classic AI tell.** Every beat must end.
> `…then returns to neutral`

### 5. Never in unison
Real people don't sync. Two figures doing the same thing at the same moment = video game.
> **Stagger every beat by at least half a second.**

### 6. Stillness is a performance
The hardest thing to prompt, and the most powerful. **Steve McQueen's whole method.** A body that is *deliberately* still — not frozen, but *holding* — is more magnetic than a body doing something.
> `holds absolutely still, but breathing — alive, not frozen`

### 7. Breath is the proof of life
The cheapest realism upgrade there is. Almost nobody prompts it.
> `a slow breath in through the nose, shoulders settle`

---

## The Hands Protocol ⚠️

**Hands are the #1 AI failure. POV shots make hands the hero. Treat this as a red-alert section.**

| Rule | Why |
|---|---|
| **Give hands a JOB** | Idle hands melt. A hand *gripping* a wheel has structure. A hand floating in space has none. |
| **Contact, not proximity** | *"fingers wrapped around the rim"* not *"hands near the wheel"* |
| **Fewer fingers visible = fewer to get wrong** | A hand gripping shows 4 knuckles. A hand splayed shows 5 fingers, 5 chances to fail. |
| **Never both hands, palms out, fingers spread** | This is the single highest-failure hand pose in AI video. |
| **Anchor them** | On the wheel. In a pocket. Folded. On the gearshift. **Anchored hands survive. Floating hands melt.** |

> **In a POV video, if the hands fail, the video fails.** No grade, no reroll of the environment, nothing saves it.

---

## The Prop-as-Motion-Engine ⭐

Learned from a Seedance 2.0 street-selfie showcase (a woman holding a small handheld fan). The prop wasn't decoration — it did **three jobs at once**, and this is a repeatable trick:

1. **It gives the hands a JOB.** A hand *holding a fan* has structure and purpose — it can't melt into an idle floating claw. (Solves the #1 hands failure.)
2. **It generates environmental motion.** The fan blows the hair → the hair moves → the frame has life without the camera moving. **Motion the model doesn't have to invent** = motion that renders cleanly.
3. **It motivates the micro-expressions.** Cooling her face justifies the eyes-closing, the smile, the head-tilt. The prop gives the performance a *reason*.

**The principle:** a small handheld prop that *acts on the subject* (fan→hair, drink→sip, sunglasses→on, phone→glance) is one of the cheapest realism upgrades available. It anchors the hands, adds motion, and motivates emotion — three of your hardest problems, solved by one object.

| Prop | What it drives |
|---|---|
| Handheld fan | hair motion + face-cooling expression |
| Cold drink / coffee | the sip beat, hands occupied, a reaction |
| Sunglasses | the put-on gesture, a reveal, attitude |
| Car key fob | the click, a glance to the car — perfect for your work |
| Phone | the glance-down-then-up, relatable |

> For a car video: KOL holding a **key fob**, thumbing it, glancing to the car as it unlocks — anchors the hands, motivates the look, and it's on-topic. Steal the fan trick, swap the object.

---

## The Gesture Bank
*(build this over time — every tested beat goes in, tagged)*

### Face
- single slow blink · brief unblinking hold · eyes flick left, then return to lens
- micro-nod, barely perceptible · chin lifts one degree
- one corner of the mouth lifts for half a second, then neutral
- jaw tightens · brow softens · a swallow

### Body
- **turns the head first, eyes follow a beat later** ⭐ strongest cue
- weight shifts from one foot to the other
- arms fold, right over left, **settling with weight**
- a slow breath in, shoulders settle
- **drops the last few inches into the seat; the seat absorbs it**

### Hands
- fingers uncurl slowly from a fist
- **hands land on the wheel and grip — they do not hover**
- a hand slides into a jacket pocket, thumb out
- thumb finds a switch **without looking** ⭐ the "expert" cue
- adjusts a cuff, once, without looking

---

## Writing Rules

1. **One beat per second, maximum.** More and the model smears them into mush.
2. **Anchor every beat to a timestamp.** Untimed gestures fire randomly or not at all.
3. **Name the reset.** `…then returns to neutral.`
4. **Stagger across characters.** Never unison.
5. **Specify weight.** If you write only one word from this file, write **`weight`**.

---

## Deliverable → DOP
```
PHYSICALITY:   [the register — heavy / light / bound / free]
HANDS:         [what job do they have? where are they anchored?]
BEATS:         [timestamped, staggered, one per second max]
WEIGHT MOMENTS:[where does the body exchange force with the world?]
BREATH:        [where]
STILLNESS:     [where does the body deliberately hold?]
RESETS:        [confirmed — nothing freezes]
```

---

## The Higher-Fidelity Route

**Prompting physicality is guesswork. Motion Control is not.**

Film **yourself** doing the exact movement — the settle into the seat, the head turn, the hand landing on the wheel. Phone camera, any lighting, 15 seconds. Then **Kling 3.0 Motion Control** transfers that performance onto your character still.

Real human micro-timing. Real weight transfer. Real breath. **Nothing a text prompt can match.**

Constraint: one character per pass. Not for the four-person wide — but perfect for a hero close-up, and perfect for Nev's own content.

> **This is the single biggest untapped realism upgrade in your entire stack.**
> You are a human being who can move. Use it.

---

## The Line

> **Photoreal is a still-frame property. Alive is a motion property.**
>
> You can pass every frame-by-frame QC and still be dead the moment it moves.
> **Weight is what separates a photograph from a person.**

---

## ⚡ See also: `07-emotion-engine.md`

Weight handles the **body**. The Emotion Engine handles the **face** — and it's the other half of "alive."

Its one rule: **direct the conflict, not the expression.** A face *managing* something (a smile leaking past mock-anger) reads as human; a clean single state reads as a stock photo. Every micro-expression beat you write should name **two feelings fighting**, in three phases — suppression → leak → reset. Read that file whenever a face is on screen.
