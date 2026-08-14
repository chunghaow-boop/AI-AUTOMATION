# 28 — THE LINKAGE MASTER
### The seat that decides whether two shots belong next to each other.
### Taught by Gavril, 2026-08-07. Written down the same hour, because a seat that is
### not written down does not exist for the next session.

---

## WHY THIS FILE EXISTS

His doctrine, from 2026-08-05, is already in the ledger:

> *"there must be a linkage that is important, when there is linkage then it feels like
> a story"*

`planqc` 24 / 29 / 31 were built from that and they enforce a real thing: a linkage must
name a **kind** and a **token findable in BOTH shots' writing**, with the shared prompt
boilerplate subtracted, so a connection cannot exist only in the planner's head.

**But the vocabulary was too thin, and it was thin in a specific way.** The original
seven kinds — motion, gaze, subject, object, light, sound, consequence — almost all
describe what a shot **CONTAINS**. On 2026-08-07, after watching the first real footage
this system ever produced, he corrected it:

> *"ok here let me teach u how to determine the linkage, other than those that we
> already have lets add on linkage determination also includes, events, actions,
> motion, activity, audio, places"*

Those describe what a shot **DOES**. That is what an editor actually cuts on.

Six kinds added. **None removed** — every existing plan still validates.

---

## THE THIRTEEN CARRIES

### The original seven — what a shot CONTAINS

| kind | the join |
|---|---|
| `motion` | something moving in A keeps moving into B |
| `gaze` | A looks off-frame, B is what A was looking at |
| `subject` | the same person or object is in both |
| `object` | a specific thing leaves A and appears in B |
| `light` | the same light state continues across the cut |
| `sound` | a transient starts in A and resolves in B |
| `consequence` | B happens **because** of A — the state of the world changed |

### His six — what a shot DOES

| kind | the join | why it is different |
|---|---|---|
| `event` | a discrete thing **happens** in A and B carries its aftermath | the splash, the cloud tearing, the door slamming. The EVENT is the join, not the subject. A `subject` carry survives a cut where nothing happened; an `event` carry cannot. |
| `action` | **match on action** — one deliberate act begins in A and completes in B | the oldest invisible cut in the craft. The cut disappears because the eye is following the movement, not the frame. |
| `activity` | an ongoing occupation continues across the cut — swimming, driving, walking the trail | **SPAN-LEVEL, not boundary-level.** The only kind that describes a *run* of shots rather than a join. It is what makes a sequence read as one continuous stretch of time instead of a list. |
| `motion` | *(already had it — he named it again, and he was right to)* | direction and vector, distinct from `action`: motion is where things travel in frame, action is what the subject intends. |
| `audio` | the **sound** carries the cut — river noise continues, an engine note answers | distinct from `sound`: that one is a transient A→B; this is a continuous bed **spanning** the join and hiding it. This is how you cut without the viewer feeling it. |
| `place` | the same geography is on both sides — same gorge, same road, same valley | cheapest carry to verify and the one that stops a film reading as a slideshow of postcards. |

---

## THE DECIDABLE TEST FOR EACH — or it is prose again

A kind that cannot be checked is a kind that will be asserted and never delivered. **KK
v15 shipped 19 prose linkages and the eye found 5 that landed.** Each kind therefore
needs a test that runs before the money moves, or a measurement that runs at ingest.

| kind | free, at plan time | measured, at ingest |
|---|---|---|
| `event` | shot A's source `act` must be `EVENT` or `PAYOFF`; B's note must name the aftermath | A's window must contain a real action peak (`clipsense`) |
| `action` | the **verb** appears in both shots' writing | **the clip must PERFORM the verb.** Craft L58: five KK boundaries were built on walking/rising/drifting and the measured optical flow on "Nev walking toward lens" was **0.50** — a man standing still. A verb without flow is a lie. |
| `activity` | the token spans **≥3 consecutive shots**, not 2 | those shots' clips share a motion signature |
| `motion` | direction token in both | exit flow vector of A vs entry flow vector of B (**the open ingest TODO — `planqc 24b` is already written and waiting for `ingest.py` to record luma and motion means**) |
| `audio` | both prompts name the same continuous source | both clips' audio share the band — `mastermind.audio_metrics` already returns this |
| `place` | both shots cite the **same plate**, or the same place token | `verify 14` already measures shots/places ≤ 2.0 |

**The two that are free and are not yet enforced are `action`-needs-flow and
`activity`-needs-a-span.** Both are cheap additions to check 29 and both are HIS CALL,
because `planqc.py` is a pipeline file.

---

## THE HONEST LIMIT — READ THIS BEFORE TRUSTING A GREEN 29

**Check 29 is a TEXT check.** It proves the *words* connect. It cannot see a pixel.

Proven on mahua, 2026-08-07: the plan passed 34/34 with 19 typed linkages and 4
consequence boundaries, four rounds of independent LLM judges read it, and the delivered
film still had the persona **wearing three different shirts**, an **invented sign board**
in shot 7, and **six duplicate framings** at up to 0.975 histogram correlation.

None of that is visible in text. All of it was visible in **one 20-panel contact sheet**.

> **A linkage is planned in words, and it is CONFIRMED in frames.**
> `tools/contact.py` at ingest, before anything is assembled. Always.

---

## THE ORDER OF OPERATIONS

```
1  write the shot list and FREEZE it
2  generate the linkage list FROM the frozen order, boundary by boundary
   (craft L59: KK's 19 linkages were authored beside an order that then changed,
    and the built cut re-used every source 2-3x, so the list described a film
    that was never built)
3  for each boundary pick the kind that is TRUE, not the kind that sounds strongest
   - a consequence you cannot see is worth less than an honest subject carry
4  the token must be a word you actually wrote into BOTH shot notes
5  planqc 29 checks the words · planqc 31 counts the causes
6  ingest -> tools/contact.py -> HIS EYE checks the frames
```

**Rule, earned twice this session:** if the cause is not visible in the writing of the
shot *before* the boundary, it is not a `consequence`, whatever the prose says. J2
killed four of five on mahua for exactly this, and it was right every time.
