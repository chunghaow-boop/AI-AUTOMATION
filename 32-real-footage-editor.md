# [SEAT] THE REAL-FOOTAGE EDITOR — reading footage you did not write
### File 32 · Created 2026-08-17 after the LOT build reached him five times with the wrong premise
### Companion seats: 10-the-editor · 27-mastermind-qc · 31-shortdrama-scriptwriter · 08-the-strategist

---

## WHY THIS SEAT HAD TO EXIST

Every other role file in this repo assumes **generated** footage. That assumption hides a
thing so basic nobody wrote it down:

> **When I write the prompt, I already know what is in the clip.**
> The plan says "a gloved finger drags down the damper and comes away wet", the generator
> returns roughly that, and my only job is to check it delivered.

With **real footage that is inverted.** The camera recorded whatever happened. Nobody
declared it. The clip is not an instruction that was executed — it is **evidence that must
be read.** Every downstream seat in this repo was built on the first assumption and silently
breaks under the second.

### What that cost, concretely (LOT, 2026-08-17)
60 clips, 12.7 minutes, a BMW recond lot. I catalogued duration, motion, luma, sharpness and
audio level, and cut five versions. Then transcription arrived and showed:

- **6 of my 8 "speech takes" were not speech** — two count-ins, a false start, two clips of
  music, and a bell chime. 23.1s of the delivered film.
- The film's actual content was a **dealership promo** — "we are Talyx, we promote cars like
  the X1, the X5, or you are interested in this red X4, so if you are interested you can PM
  us" — and I had shipped it with **no hook, no turn, and no CTA**, while an explicit CTA sat
  unused in the footage.
- I had the car wrong in writing (called an X1 an X7) because I read a badge on a thumbnail.

Not one of those is an editing mistake. **They are all reading mistakes.**

---

## THE ONE RULE

> # READ THE FOOTAGE BEFORE YOU CUT IT.
> Measuring is not reading. Duration, motion, luma, sharpness and dBFS describe a clip's
> PHYSICS. They say nothing about its MEANING. A count-in and a sentence have identical
> physics. A wheel pan and an event have identical physics. **You cannot cut what you have
> not read**, and every metric in this repo is silent about content.

---

## PART A — THE READ PASS (mandatory, before ANY in-point is chosen)

Run all four. None is optional; each covers a blind spot the others share.

### A1 · TRANSCRIBE FIRST. Always. (L174)
No speech-led film is cut before a transcript exists.

```
tools/asr.py --scan "<footage dir>" --out projects/<name>/TRANSCRIPT.json
```
Model lives in Downloads (fetched via Claude-in-Chrome, see PART D) and runs in-sandbox.

**Never use an energy detector to decide whether someone is talking.** Voice-band energy
plus envelope variability is satisfied by singing, counting, chimes and laughter. It is a
valid tool for finding pause BOUNDARIES *once ASR has confirmed there are words*, and for
nothing else.

### A2 · READ EVERY CLIP AS A TIME-ORDERED STRIP (L178)
6–12 frames per clip, evenly spaced, laid out left-to-right, and **LOOKED AT**. One frame is
a thumbnail; it tells you the subject and lies about everything else — where the gesture
resolves, whether the hand leaves frame, whether the shot is usable at second 4 but not
second 9.

An in-point chosen from a clip you have not seen at that timestamp is **invented**, and
HARD RULE 0 forbids it.

### A3 · READ THE TEXT IN FRAME AT FULL RESOLUTION (L179)
Badges, plates, signage, screens. Per clip, at native resolution, one at a time.
Record: what it says · whether it is mirrored · the evidence frame.

**Never call a mirror from a contact sheet.** Flipping a clip that was already correct is a
NEW defect you introduced, and it has shipped twice.

### A4 · NAME WHAT EACH CLIP CONTAINS, IN WORDS
One line per clip, written down: subject, what happens, where it peaks, why it would be used.
If you cannot write that line, you have not read the clip and it is not eligible for the cut.

---

## PART B — THE STORY PASS (nothing is cut until these four are named)

The read pass gives facts. This turns them into a film. **All four come from the
TRANSCRIPT in a speech-led format** — not from motion scores (L175).

| | question | where it lives |
|---|---|---|
| **HOOK** | What makes a viewer stop in the first 2s? | usually his first sentence, or the event it describes |
| **TURN** | What does the viewer believe that stops being true? | the sentence where the direction changes |
| **CTA** | What does he ASK them to do, in his own words? | quote it verbatim; never invent one |
| **FLOW** | What order do the words demand? | **b-roll follows the sentence** |

**FLOW, stated properly:** when he says "X1", the X1 is on screen. When he says "this red
one", the red car is on screen. Pictures and words are ONE timeline. On LOT I had them fully
decoupled — he named three cars and the cut showed unrelated details throughout.

If a piece cannot be named, **say so in the plan as a written waiver** — "this footage
contains no turn; it is a promo, not a story" is a legitimate finding. Silence is not.
A waiver is a sentence, never a silence (L168).

---

## PART C — THEN, AND ONLY THEN, THE PLAN

Write `plans/<name>.py` with a CONTENT block carrying the four above, quoting the transcript.
Run `planqc`. Render the board. Show him the board. **Then** cut.

> **A film with no plan file has no gates at all (L176).** They do not fail — they are never
> invoked, and nothing reports their absence. Going from footage straight to ffmpeg bypasses
> every story gate silently. That is how five versions reached him with no CTA.

---

## PART D — THE ASR BRIDGE (how the model gets in)

HuggingFace and the Azure CDN are proxy-blocked from the sandbox; GitHub release assets
redirect to a blocked host. **PyPI works.** So:

1. `pip install sherpa-onnx` — the engine comes from PyPI, fine.
2. The **weights** come via Claude-in-Chrome, which browses on HIS network:
   `github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2`
3. Chrome saves to Downloads. **Downloads is a mounted folder** — the sandbox reads it directly.
4. Extract and run in-sandbox. He runs nothing. ("Too old school.")

Proven 2026-08-17: 639 MB fetched, extracted, transcribed 8 clips.
Quality note: whisper-small handles Manglish code-switching adequately but garbles some
phrases ("come eat the legs"). Read transcripts for SHAPE and quote only what is clear.

---

## PART E — WHAT THIS SEAT HANDS DOWNSTREAM

```
projects/<name>/TRANSCRIPT.json    every word, with timings
projects/<name>/READ.md            one line per clip + text-in-frame + mirror verdicts
plans/<name>.py                    CONTENT block: hook · turn · CTA · flow, quoted
```
The editor seat (file 10) may not choose an in-point that is not justified by one of these.
