# READ THIS FIRST

**You are about to make a video for Gavril. Read this before you touch anything.**

Written 2026-08-08, the day a film cleared **every single gate** and he rejected it
on sight in under a minute.

---

## BEFORE ANYTHING: WHAT HE IS ACTUALLY BUILDING

Read `30-what-he-actually-wants.md` first. It is short, it is in his own words, and
I got the answer wrong twice in one conversation — both times plausibly.

The one-line version: **he wants an agent that scans what is winning right now,
measures it, and builds better.** Not a video generator. His judgment is the
fastest feedback available while that agent doesn't exist yet — the bootstrap, not
the ceiling. But it is also the only source that gives you a CAUSE rather than a
correlation, and that never gets replaced.

And when he says something feels off but can't say why, that is the most valuable
report you will get. Run `python3 tools/flinch.py <project> <seconds>` and point
every instrument at that moment. Never ask him to justify it first.

## THE ONE THING TO UNDERSTAND

The video that failed was not broken in any of its parts. It was broken **between**
its parts.

- The car was fine. The road was fine. **The car was driving at 90° to the road.**
- The music was on tempo. The foley was in the mix. **The music buried the foley.**
- His face performed a real laugh. The audio was correctly mastered. **There was no laugh in it.**
- Both captions sat in the caption zone. **Both sat in it at the same time**, printed through each other, unreadable, for 2.5 seconds.

Thirty-four plan checks and fifteen delivery checks all looked at **things**.
Not one asked whether the things **agreed**.

> **If you check every element and ship, you will ship a broken film.
> Check the pairs.**

The eight pairs are in `29-relationship-master.md`. Your plan must state how it holds
each one, or `planqc 32` will refuse it. That is not bureaucracy — every pair on that
list is there because it actually failed, with a measurement.

## THE SECOND THING: YOU CANNOT SHIP PAST A GATE

On 2026-08-07 `verify` returned **BLOCK, six failing checks**. I read it, wrote him a
neat table explaining the failures, and sent him the link anyway.

His reply: *"QC did its job but the video still proceeded anyway."*

He was right. The gate fired and nothing stopped delivery, because delivery was never
a step — it was me pasting a URL.

**A video now leaves exactly one way:**

```
python talyx.py deliver <project>
```

It runs `verify`, runs the **mastermind** final scorecard, crosschecks the plan
against the cut against the file on disk, and **refuses to print the path** if
anything blocks. If you find yourself about to send him a link that `deliver` did
not print, stop. That is the exact thing that happened.

If you believe a stop is wrong: **change the check and say why in its comment.**
Never carry the film past it.

## THE THIRD THING: A PREFERENCE THAT NEVER BLOCKS IS A HOPE

`engine.py` had computed "this window ends mid-action" since 2026-08-04 — filed from
his catch *"clips cut off way too early."* It was only ever used as a **sort key**.

Three months later he wrote *"some scenes important events are cutted out"* and the
measurement had been sitting right there, computed, printed, never enforced.

If the pipeline can measure a defect, it must **block** on it. Audit anything that
looks like a ranking term for the same shape.

## WHAT HE ACTUALLY CATCHES

He finds things instruments miss, fast. Four of the nine defects in that film were
his, and I had already looked at two of them:

| he said | what it was |
|---|---|
| *"nev driving a car horizontally but the road is going vertically"* | a **side window** — wing mirror visible — with the road receding away through it |
| *"the bgm is slightly louder than everything it covers all the sfx, and foley"* | a `±8 dB` clamp ate half a `+16.3 dB` correction and printed the clamped value as success |
| *"nevs expression have no sfx or other elements to back it up"* | the shot where he's shocked has **less vocal-band energy than a shot of empty hills** |
| *"some scenes important events are cutted out"* | shot 5 ended at **96%** of its own action peak |

And when he says *why* something happened, test it — he is often more precise than
the instrument. He said the duplicate scenes were *"at the video editing side, not
the ai video generation."* Measuring every non-overlapping window pair proved him
right for source C (a clean pair existed at 0.817/0.798 and the editor picked
0.928/0.986) and wrong for source E (no pair in that clip could ever have differed).
**That split the fix into two fixes.** Neither would have been found by agreeing
with him or by dismissing him.

## HOW TO TALK TO HIM

He named the planner **"the mastermind"** on purpose. His reason, in his words:
*"because its an easier word to remember than all those other words, something more
like a human language rather than an AI understood language."*

Follow that everywhere. Name things so a person remembers them. Write gate output as
a sentence someone can act on, not a metric dump. `HELD BACK — the film is 149 ms
short of the plan` beats `assert_duration_delta_exceeded`.

## THE ORDER OF WORK

```
talyx.py plan     <name>     free. 35 checks. blocks generation.
talyx.py cost     <name>     MEASURE the balance, never estimate it
                             ... probe ONE clip, LOOK at it, then buy the rest
talyx.py ingest   <name>     per-clip gate. one bad clip = 22.5cr, not a rebuild
talyx.py build    <name>     cut it. refuses on mid-action or duplicate windows
talyx.py deliver  <name>     verify + mastermind + crosscheck. THE ONLY WAY OUT
```

**Show him the contact sheet before anything is assembled.** Standing order.
**Give him a hosted link, never an attachment.** Standing order.

## WHERE THE MEMORY LIVES

| file | what it is |
|---|---|
| `LESSONS.md` | every lesson, compiled. Generated — never edit by hand |
| `ledgers/knowledge.json` | the truth behind it. `tools/lessonize.py` is the only writer |
| `29-relationship-master.md` | the eight pairs, and why each is on the list |
| `28-linkage-master.md` | how shots connect — his taxonomy, in his words |
| `SYSTEM-MAP.md` | what each file does |

`planqc 23` blocks any plan whose `LESSONS_ACK` counts are stale. That is deliberate.
**A lesson that does not change the next build is not learned.**

And the failure mode that matters most, because it already happened: `verify 13`'s
threshold carried its own comment saying *"fitted to THREE samples… widen the sample
and re-derive before trusting it further."* Nobody did, and it passed three
duplicates by a hair. **Filing the lesson is not the job. Changing the gate is.**
