# The Emotion Engine — Micro-Expression as Conflict
### Module for Seat [2B] Physical Performance · companion to `03-physical-performance-master.md`
### Reverse-engineered from the YUNER "AI Comic Series" reference (July 2026)

---

## The One Insight

**A state is dead. A conflict is alive.**

Your beats so far have been *states*: "confident smile," "slow blink," "arms fold." A state is a single thing the face is doing. The viewer's brain reads it as a pose and moves on.

The reference video is built entirely on **conflict**: two feelings fighting on one face. Suppress vs leak. Hold vs spill. Look away vs look back. **The struggle is what reads as human** — because that is what a real face actually does. Real people are never one clean emotion. They're always managing one while another leaks through.

> Stop directing expressions. Start directing **the thing the person is trying not to show.**

---

## Proof, from the reference

The creator baked the acting note into each clip as on-screen text. Every single one is a compound, not a state:

| Clip | Label | The conflict |
|---|---|---|
| 1 | 笑骂 *smiling-scold* | Wants to scold — but is smiling instead. Affection leaking through mock anger. |
| 2 | 心疼 *heartache* | Grief rising — but held back. Won't let it spill. |
| 3 | 娇嗔 *playful-sulk* | Pretend-annoyed — secretly pleased. |
| 4 | 委屈 *wronged* | Hurt — but too proud to say it. Holding it in. |
| 5 | *(resolve)* | The feeling finally lands, released. |

**Not one of these is a single emotion.** That is the whole technique.

---

## The Structure of a Living Expression

Every real expression has **three phases**. AI defaults to skipping straight to phase 2 and holding it — which is exactly why it looks fake and frozen.

```
1. SUPPRESSION   the face resists the feeling      (0.0–0.5s)
2. LEAK          the feeling breaks through         (0.5–1.5s)
3. RESET         the face reasserts control         (1.5s+)
```

**Write all three. Every time.**

Bad (state):  `she smiles confidently at the lens`
Good (conflict): `her mouth presses flat, holding it — then the smile breaks through against her will — then she reins it back to composed`

Same 2 seconds. One reads as a stock photo. The other reads as a person.

---

## The Emotion Bank — conflict recipes

Each is written in the three-phase format. Timestamp and drop into any prompt.

### 笑骂 — Smiling-scold (affection as mock-anger)
```
The mouth presses flat first, brows tense as if to scold — then a smile
leaks through against her will, breaking the composure. The head tilts
back a degree. Eyes soften before the mouth does. Then she reins it back.
```

### 心疼 — Heartache (grief, held)
```
The inner corners of the brows lift and draw together. The eyes gloss
but do NOT spill. A slow, heavy blink. The chin dips. The effort of not
crying is visible in the jaw. Then a slow breath, and she holds.
```

### 娇嗔 — Playful-sulk (pretend-annoyed, secretly pleased)
```
She looks away with a small huff, chin up, mock-offended — but the
corner of the mouth twitches upward, betraying that she's pleased. Eyes
flick back to the lens once. Then away again, fighting the smile.
```

### 委屈 — Wronged (hurt, too proud to show)
```
The lower lip tightens. The eyes widen slightly and shine. She lifts her
chin to stay composed, but the vulnerability shows in a single slow
blink. She swallows. Holds her dignity. Does not look away.
```

### Contempt / cool dismissal
```
One eyebrow rises a fraction. The eyes narrow briefly. A single side of
the mouth lifts — not a smile, a verdict. Then flat neutral. Cold.
```

### The slow win (satisfaction landing)
```
The eyes catch first — a flicker of recognition. Then the mouth follows,
slow, earned. Not a grin. A quiet certainty settling in. Chin lifts a
degree. Holds.
```

### Suppressed laugh
```
The lips clamp. The cheeks lift and fight it. A breath escapes through
the nose. The shoulders shake once before she gets it under control.
Eyes bright and wet with the effort.
```

---

## The Direction Rules

1. **Name the conflict, not the expression.** "Smiling-scold," not "smile." If you can't name two feelings, you don't have a beat yet.
2. **Always three phases.** Suppression → leak → reset. Never hold a single state.
3. **The eyes lead the mouth.** Real emotion reaches the eyes *first*. AI does the mouth first. Force the order: `eyes soften before the mouth does`.
4. **Glossy, never spilling.** Emotion rising and *held* beats emotion released. The restraint is the realism. (Also: actual tears break AI faces — don't.)
5. **Asymmetry.** One side of the face moves before the other. `one corner of the mouth` beats `a smile`.
6. **One conflict per clip.** At 5 seconds you have room for exactly one emotional arc. Don't stack.

---

## The Lighting That Sells It ⚠️ (DOP note)

The reference is **not studio-lit.** The realism leans hard on a specific setup your studio work doesn't have:

| Element | Why it matters |
|---|---|
| **Golden-hour backlight** | Warm key from *behind*, low angle. Not flat frontal studio light. |
| **Rim-lit loose hair** | Every stray strand catches light → a halo of flyaways. **This is a massive realism cue.** AI usually renders helmet-hair; loose lit strands read as real. |
| **Soft-blurred natural background** | A real place, thrown fully out of focus — not a seamless cyclorama. |
| **Long lens, shallow DOF** | 85mm+. Portrait compression. Background melted. |

> **This is a different lighting problem from your showroom work.** If you want *this* quality, the DOP has to switch from white-cyclorama high-key to **golden-hour backlit portrait.** Add to the prompt:
> `warm golden-hour key from behind and to one side, rim-lighting the loose strands of hair, soft-blurred natural background, 85mm, shallow depth of field`

---

## Deliverable → DOP (extends the Physical Performance handoff)
```
EMOTION:        [the named conflict — e.g. smiling-scold]
THREE PHASES:   [suppression → leak → reset, timestamped]
EYE-LEAD:       [confirmed — eyes move before mouth]
ASYMMETRY:      [which side leads]
LIGHTING REQ:   [golden-hour backlit? studio? — tell the DOP]
```

---

## The Line

> **AI can render a perfect face. It cannot, by default, render a face that is *managing* something.**
>
> Give it something to manage — one feeling leaking past another — and the mask becomes a person.
> That is the entire gap between your showroom video and this one. Not the model. The direction.
