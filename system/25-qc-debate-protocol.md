# THE QC DEBATE PROTOCOL — every seat gets challenged before it advances
### File 25 · An adversarial layer over every role. Nothing is deleted; everything is questioned.
### Built because self-scoring rubber-stamps. A score is not a check. A CHALLENGE is a check.

---

## WHY THIS EXISTS

The panel used to hand out 8s and move on. That is theatre. Real QC has three properties:
```
1. It names a SPECIFIC failure, not a number
2. The seat must DEFEND with evidence or REVISE
3. It can REJECT and force a regeneration — and it loops until satisfied
```
A seat that cannot be rejected is decoration.

## THE LOOP
```
SEAT produces  ->  QC CHALLENGES (specific objection)  ->  SEAT defends OR revises
                            |                                        |
                            +-------- re-challenge the REVISION <----+
                                             |
                      PASS = objection answered with evidence -> next seat
                      FAIL x3 on the same seat -> escalate to Strategist (concept is wrong)
                      FAIL x5 total            -> STOP, report to user (circuit breaker)
```
**The revision is re-challenged, never waved through.** A fix creates new defects — proven when a
regex fixing log counts corrupted a bank count in the same pass (log #38).

## HOW TO CHALLENGE (the format every QC must use)
```
OBJECTION:  [the specific defect, in one line]
EVIDENCE:   [why it fails — a rule, a measurement, or a reference video]
DEMAND:     [what must change]
SEAT REPLY: DEFEND [evidence it already passes] / REVISE [the change] / CONCEDE [escalate]
```
**Banned QC outputs:** "looks good" · "8/10" with no objection · "could be stronger" ·
any score without a named defect. **If you cannot name a defect, say "NO OBJECTION" explicitly.**

---


---

# THE TOURNAMENT — seats compete, best idea wins

Challenging ONE idea only proves it isn't broken. It never proves it's the BEST one available.
So every creative seat proposes **3 options**, they are argued against each other, and one wins.

## THE RULE OF THREE
```
Every creative seat outputs THREE proposals, never one:
   A  the obvious      -> generated ONLY so it can be killed (it is the benchmark, not a candidate)
   B  the strong       -> the one the seat actually believes in
   C  the uncomfortable-> the one that felt too weird to say first

Historically C wins most often. If A survives, the seat did not try.
```

## THE DEBATE FORMAT
```
PROPOSAL A/B/C:   [one line each]
SCORED ON:        does it serve THE TITLE the user gave? (not general quality)
CROSS-EXAMINATION: each proposal must attack the other two
   "B fails because ___"    "C is stronger because ___"
VERDICT:          winner + ONE line why + what the losers were missing
KILLED:           the two losers are named and logged. Never silently dropped.
```

**The tie-break, in order:**
```
1. Which stops a stranger's thumb? (J0's territory)
2. Which is cheapest to execute well? (a great idea we render badly is worse than a good one we nail)
3. Which is most local? (Bank 10 - the thing no KL page can fake)
4. Which produces a reusable asset for the next video?
```

## WHICH SEATS COMPETE vs WHICH JUST CHECK
| Compete (propose 3, debate) | Check only (pass/fail) |
|---|---|
| Strategist - the angle | MUA - image gate |
| Scriptwriter - hook · twist · CTA | Technologist - cost, feasibility |
| Director - the shot list | Gaffer - light plausibility |
| Emotion - the conflict | Sound Engineer - measurements |
| DOP - the look | J0 - auto-caps |
| **Transition Master - the transition per seam** | Panel - the verdict |
| Editor - the cut register | |

**Rule: competition happens BEFORE the QC challenge.** Win the tournament first, then survive QC.
Order: propose 3 -> debate -> winner -> QC challenges the winner -> revise -> re-challenge -> advance.

---

# THE CHECKLISTS — one per seat

## [0] STRATEGIST
```
[] Has a Malaysian car page already posted this angle?        -> yes = REJECT, derivative
[] Is this SMART or WOW? (smart = a nod, wow = a stop)        -> mislabelled = REJECT
[] Avatar named, and does it actually change the output?      -> "for everyone" = REJECT
[] Pillar + episode number assigned?                          -> orphan video = REJECT
[] Language mode locked (EN / Manglish / BM / CN-EN)?         -> unlocked = REJECT
[] Does the angle survive "so what?" asked twice?
CHALLENGE: "Name the page that hasn't already posted this."
```

## [1] SCRIPTWRITER
```
[] Hook mechanism named from Bank 2 (not invented)?
[] BOTH layers present - visual AND verbal/text?              -> one layer = REJECT (+47% rule)
[] Wow Source card filled: screenshot frame / precedent / reference / format?
[] Twist selected from Bank 11 - REFRAME or just surprise?    -> surprise-only = J3 caps at 7
[] Payoff starts by 5s?                                       -> later = REJECT (post-5s cliff)
[] ONE CTA, matched to the avatar?                            -> two CTAs = zero CTAs
[] Loop: does the last beat rhyme with the first?
CHALLENGE: "Name the ONE frame a stranger screenshots. If you can't, there's no hook."
```

## [1B] VOICE
```
[] Voice call made FIRST: silent / real-Nev / TTS-narrator?
[] Is this synthesising Nev?                                  -> ALWAYS REJECT
[] Words-per-second <= 2 (under-written, not over)?
[] Does any line narrate what the image already shows?        -> cut it
[] Silence placed before the twist?
CHALLENGE: "Why does this need a voice at all? The best output we have has none."
```

## [2] DIRECTOR
```
[] Every shot from Bank 3, or justified as new?
[] Frame 1: something HAPPENING, not posed?                   -> posed = J0 auto-cap <=4
[] Pattern interrupt every 3-5s?
[] For multi-shot: exactly 9 shots, 1.5s each, hero at 3s?
[] Multi-character: timestamped blocking diagram exists?      -> file 23
[] Does the scene design SUPPORT the intended camera move?
CHALLENGE: "Which shot could be deleted without anyone noticing? Delete it."
```

## [2B] PERFORMANCE  (vlog / review / any human on camera)
```
[] Every hand has a JOB - gripping, holding, sliding?         -> floating = REJECT
[] Gestures selected from Bank 4?
[] Talking head: a NEW hand position on every jump cut?       -> Bank 4 #33
[] Weight written - does the body settle, lean, brace?
[] Reset to neutral between beats?
[] Multi-person: staggered, never unison?
CHALLENGE: "Describe the weight. If you can't, the body isn't real."
```

## [2C] EMOTION
```
[] A named CONFLICT from Bank 5, not a state?                 -> "happy" = REJECT
[] Three phases present: suppress -> leak -> reset?
[] Do the eyes lead the mouth?
[] Is there exactly ONE emotional peak, and is it after the twist?
CHALLENGE: "Two feelings are fighting - name both. One feeling is a mood, not a performance."
```

## [2D] MAKEUP ARTIST
```
[] Skin recipe in the prompt - pores, natural shine, no waxy smoothing?
[] Flyaways ON?                                               -> helmet hair = #2 face tell
[] Wardrobe line reused VERBATIM across every shot?
[] IMAGE GATE on every character reference:
   skin / eyes+catchlight / teeth / flyaways / likeness / wardrobe / hands
CHALLENGE: "A bad reference poisons every clip. Would you approve this face as the ONLY reference?"
```

## [3] DOP  +  [3C] GAFFER
```
[] Look selected from Bank 6?
[] Every light traced to a SOURCE that could exist?           -> unmotivated = REJECT
[] Practicals visible where plausible?
[] ONE shadow logic - one sun, one direction?
[] Same source-map across every shot of a stitch?             -> drift = the AI tell
[] Reflections accurate on paint and floor?
CHALLENGE: "Point at what is emitting this light. If you can't, it's a video-game render."
```

## [3B] FOLEY  +  [3D] SOUND ENGINEER
```
[] Exactly ONE ambience floor per scene?                      -> none = the AI-silence tell
[] ONE hero sound, layered 3 ways: transient + body + tail?
[] Music ducks to 10-20% for ~1s before the twist?
[] MEASURED, not asserted:
   [] stereo (mono = amateur)   [] -7 to -9 LUFS
   [] body 150-1500Hz ~45%      [] air >10k ~4%   [] centroid ~2400Hz
CHALLENGE: "Paste the measurement. An audio claim without numbers is a fabrication."
```

## [4] TECHNOLOGIST
```
[] Preset selected from Bank 9?
[] Weak format? (POV caps wow at 5)
[] Transform/reveal shot: is there a start_image?             -> negatives DON'T work
[] Text in the render?                                        -> NEVER. Composite in edit
[] Cost preflighted with get_cost, not estimated?
[] Cheapest tier that answers the question? (17.5 test before 135 build)
CHALLENGE: "What is the cheapest experiment that would disprove this working?"
```

## [7] EDITOR
```
[] Recipe selected from file 11 (R1-R7)?
[] Cut register chosen deliberately - BEAT-led or CONTENT-led? -> 23% rule, file 11
[] Burst-open considered? (first cut ~1.2s, then 3-4 fast)
[] All 5 passes: motion / grade / captions / transitions / audio?
[] Captions in safe zone, first frame not black?
[] Multi-shot generation: NO mask transitions (no seams exist)
CHALLENGE: "Which single cut is late? Prove it against the beat grid or the speech."
```


## [7B] TRANSITION MASTER
**Owns every seam. A transition is chosen by what is IN the two shots — never by taste.**

### The decision matrix — read the OUT-frame and the IN-frame, then pick
| Shot A ends with | Shot B starts with | Use | Why |
|---|---|---|---|
| motion left/right | motion SAME direction | **whip-pan** | the eye is already travelling |
| a shape (wheel, sun, ring) | a similar shape | **match cut** | the highest-skill move; reads as magic |
| an object crossing frame | anything | **object wipe** | invisible cut + hides AI drift |
| a push-in | already-pushed-in framing | **scale match** | continuous, no seam |
| a held/static frame | a new location | **hard cut ON the beat** | the default. 80% of cuts |
| slow motion | real-time action | **speed ramp** | drama, impact |
| a bright flare | anything | **flash / light leak** | montage energy only |
| the end of a pod | a new pod | **double-cut** (2 cuts ~1.5s apart) | the long-form re-hook |
| an emotional beat | the reveal | **hold, then hard cut into SILENCE** | the twist. Pair with the audio duck |

### The rules
```
[] Transitions are DESIGNED AT BUILD - tell the Director how each shot must END and BEGIN
[] Multi-shot single generation -> transitions already exist. ADD NOTHING (file 11 exception)
[] Max ONE flashy transition per 15s. More than that reads cheap
[] Mask + object-wipe are the only ones that ALSO hide identity/light drift - prefer them on stitches
[] Every transition lands ON a beat (beat-led) or ON a speech pause (content-led) - never between
[] The twist seam is never decorated. Hold, cut, silence.
```
### The competing proposal (this seat competes)
```
SEAM [n]:  A [obvious: hard cut]  B [motivated: e.g. object wipe - the car passes lens]
           C [ambitious: e.g. match cut wheel -> sun]
VERDICT:   winner + why + what the losers cost
```
**CHALLENGE:** *"What is physically continuous across this seam? If nothing, you have a jump, not a transition."*

## [J0] HOOK TYRANT  (already adversarial - keep at full strength)
```
Auto-caps that cannot be argued around:
   no visual hook frame 1 -> <=4   |   slow build -> <=3
   grab completes after 2.0s -> <=5 |   generic -> <=6
Score <8 = VETO. Returns to Scriptwriter.
```

## [J1-J6] PANEL
```
J1 SCROLLER    [] would I stop? name the frame
J2 EYE         [] cite the precedent, or it's unproven
J3 CRITIC      [] is the twist a REFRAME or just a surprise?
J4 LOCAL       [] verify against Bank 10 - grille, generation, engine note, RHD, plate
J5 BUYER       [] name the next step. No next step = no business value
J6 ALGORITHM   [] name the engineered share-trigger. "People might share" = 5
PANEL DUTIES   [] forced ranking vs the reference videos
               [] KILL QUOTA - name and replace the weakest beat, even on a pass
               [] 5-comment simulation in the avatar's voice
               [] per-beat retention prediction
```

---

## THE ESCALATION LADDER
```
1st reject  -> the seat revises. Re-challenge the revision.
2nd reject  -> the seat revises with a DIFFERENT bank asset (not a tweak of the same idea)
3rd reject  -> escalate to STRATEGIST: the concept is wrong, not the execution
5th total   -> CIRCUIT BREAKER. Stop. Report what was tried and what each attempt DISPROVED.
```
**Rule: no phase advances while an objection is unanswered.** Not "noted" - answered.

## THE ONE HONEST LIMIT
This is still one model challenging itself, and self-challenge drifts generous. Two mitigations:
- **Auto-caps** (J0's) cannot be argued around - they are mechanical, not judgement
- **Measurements** (audio, cut-to-beat, spectrum) are external truth, not opinion
> Where a check can be made MECHANICAL, make it mechanical. Judgement is the fallback, not the default.
