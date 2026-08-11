# 29 · RELATIONSHIP MASTER

**The doctrine that exists because of how everything else passed.**

Filed 2026-08-07, from `DESAFARM_CINEMATIC_v2.mp4` — a build that cleared
34 plan checks and 15 verify checks and was rejected on sight.

---

## THE LAW

> **Every element passed. Nothing checked whether they agreed.**

Nine defects were found in that film. Not one of them was a broken element.
Every single one was a **relationship between two elements that were each
individually correct.**

| the element | verdict alone | the element | verdict alone | together |
|---|---|---|---|---|
| the car | fine | the road | fine | driving at 90° to each other |
| the music | on tempo | the foley | present in the mix | music buried the foley |
| his face | a real laugh | the audio | correctly mastered | he performed into silence |
| card 3 | in the zone | card 4 | in the zone | both in it at once, unreadable |
| the event | a real event | the shot length | on the beat grid | event cut in half |
| the clip | one clean arc | the shot order | on the grid | arc played backwards |
| the whip | 240 ms, as declared | the beat grid | 97.5 BPM, verified | picture 170 ms early for 60% of the film |
| the clip | generated fine | the shot count | 2, as planned | same picture twice |

A checklist of elements cannot see any of these. That is not a gap in the
checklist — it is the wrong shape of checklist.

## WHY IT KEPT HAPPENING

Both the plan gate and the delivery gate are lists of *nouns*. Is the hook an
EVENT? Is the bed on tempo? Are the cards in the zone? Is the luma in band?

Every question is about one thing. A film is made of **pairs**.

The failure is structural and it repeats, so it gets its own gate rather than
another lesson: `planqc 32 relationships`.

## THE EIGHT PAIRS

Each one is on this list because it *actually failed*, with a measurement.
Nothing here is hypothetical. Add a ninth only when a ninth is measured.

### 1 · subject_vs_background
A subject's implied geometry must agree with the world behind it.

> **His catch:** *"nev driving a car horizontally but the road is going vertically."*
> A side window — wing mirror visible, no steering wheel in frame — with the road
> receding straight away through it. The car is driving perpendicular to its own road.

### 2 · performance_vs_sound
A performed emotion must be carried by audio, not mimed.

> **His catch:** *"nevs expression have no sfx or other elements to back it up."*
> Measured: voice-band ratio 0.25 where he laughs out loud, 0.16 where he is
> shocked, against **0.19 for a shot of empty hills.**

### 3 · bed_vs_foley
Music must not cover the diegetic sound of the place.

> **His catch:** *"the bgm is slightly louder than everything it covers all the sfx,
> and foley."* Measured: soundscape similarity across cuts **0.935** against a
> mid-shot control of **0.947** — a goat pen and a car interior sounded identical.
> Root cause: a `±8 dB` clamp ate half a `+16.3 dB` correction and printed the
> clamped value as if it had worked.

### 4 · card_vs_card
No two cards may occupy the caption zone at the same time.

> Two captions printed through each other for 2.5 s. `planqc 12` checked the
> **zone**, `verify 6` checked the **zone**. Neither checked the **clock**.

### 5 · event_vs_window
The shot must be long enough to contain the whole event.

> **His catch:** *"some scenes important events are cutted out."* Shot 5 ended at
> **96%** of its own action peak, shot 14 at **83%**, and the hook ended with the
> bottle still in his hand — the goat takes it thirteen seconds later.
> The engine had computed `unresolved` since 2026-08-04 and used it only as a
> **sort key**. *A preference that never blocks is not a rule, it is a hope.*

### 6 · arc_vs_shot_order
A clip with an internal arc must be used in that arc's order.

> Source H was written `startled → laugh`, explicitly MONOTONIC. Delivered as
> laugh at 15.8 s and startled at 20.9 s. He reacts after he has already laughed.

### 7 · picture_grid_vs_music_grid
A transition must not shift the picture off the music.

> The 240 ms whip **shortened** shot 8 by 197 ms instead of overlapping it.
> Internal spacing stayed perfect, so the error is invisible to any per-shot
> check — the whole back 60% of the film simply sits ~170 ms early.

### 8 · clip_variety_vs_shot_count
A source may carry N shots only if it can supply N distinct looks.

> **His call:** the duplicates were *"at the video editing side."* He was right,
> and measuring it split the blame exactly — searching every non-overlapping
> window pair for the most different available:
>
> | source | best available | delivered | whose fault |
> |---|---|---|---|
> | C cabin | 0.817 / 0.798 | 0.928 / 0.986 | **the editor** — it had a clean option |
> | G goats | 0.868 / 0.872 | 0.866 / 0.933 | marginal |
> | E calf | 0.911 / 0.973 | 0.878 / 0.984 | **the plan** — no pair could ever have worked |

## HOW A PLAN SATISFIES THIS

`RELATIONSHIPS` is a required dict. One key per pair, and the answer must be a
**mechanism**, not a promise. Under 40 characters is rejected as too thin to be
a plan.

```python
RELATIONSHIPS = {
    "subject_vs_background":
        "Every interior prompt names the window it shoots through and what the "
        "view does: a SIDE window sweeps across, a WINDSCREEN recedes. Checked "
        "on the delivered frame at ingest, not on the prompt.",
    ...
}
```

Wrong: *"we will be careful about the car and the road."* That is a promise.
Right: the sentence above — it says what the prompt contains and where it is
verified.

## THE TEST THAT MATTERS

A gate written from a defect must **fail the film it was written for.** All six
built on 2026-08-07 were run against `DESAFARM_CINEMATIC_v2` and all six failed
it. A gate that passes the video that produced it is decoration.
