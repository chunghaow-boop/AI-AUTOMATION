# 30 · WHAT HE ACTUALLY WANTS

**Read this before you decide what to build. I got it wrong twice in one
conversation, and both wrong answers sounded reasonable.**

Recorded 2026-08-08, from him directly.

---

## THE GOAL, IN HIS WORDS

> "I want to create an AI agent that automatically scans the whole web, every
> social media platform, for the viral video and the highest retention rate video,
> and recreate something even better than that video."

That is the thing. Not a video generator. Not a quality checklist. **A system that
finds what is winning right now, takes it apart, and builds better in the same
shape** — so that Urban Auto Hub posts 4–7 times a week, grows, and turns into
leads for recond cars and paid promo work.

## THE TWO ANSWERS I GOT WRONG

**Wrong answer 1: "you want fewer hours of work."**

I read *minimal supervision* as tiredness. It isn't. He said:

> "I want minimal supervision because I want the automation to automatically
> analyze what is the trending video right now and what is the most viral video
> right now so that it can generate an even better video."

He wants to step back because **his taste is slower than the feed**, not because
he's tired. One person can watch a few dozen videos a week. The platform sees
millions. He wants the system doing the watching too.

**Wrong answer 2: "you want your judgment written down in a form that executes."**

He said *no* three times. Then:

> "My judgment is only a part that assists in reaching that final goal. Because my
> judgment is the most direct and the most easy way and the fastest way to give you
> a feedback so you can improve."

His eye is the **bootstrap**, not the ceiling. Encode it as the spec and you cap
the system at one person's taste forever. The standard is meant to come from
measuring what actually wins.

## BUT DO NOT DEMOTE HIS JUDGMENT EITHER

The correction that makes this whole document worth reading:

> "Retention is private. That's why I'm here giving you my judgment. Because
> retention is based on human interaction — human watches the video, human likes
> the video, that creates the retention. And I am a human, and I'm giving you the
> judgment."

A retention curve **is** human reaction, aggregated and delayed. He is one of those
humans, handing over the decision directly instead of as a statistic a week later.

And the part no dataset gives you: **cause**. Retention tells you *where* people
left. It never tells you *why*. If the goat video had lost 40% at second four, the
analytics would show a cliff and nothing else. He said *"it's boring, nothing
happens between the hook and the payoff"* — right, in one sentence, immediately.

So he is not a stand-in for missing data. He is the only source in the system that
gives cause instead of correlation, and that stays true after the scanning agent
exists.

## HOW HE FINDS THINGS — AND WHAT TO DO ABOUT IT

> "Usually I know the moment it happens. And then I have a feeling even if there is
> nothing wrong with the video — I have the feeling or the urge when I see this
> video is not right or it's a little bit weird, then I will directly tell you. I
> would not go and find it somewhere else."

**The flinch comes first. The explanation is reverse-engineered afterwards.**

*"The car is going horizontally but the road is going vertically"* was him putting
words to something he had already felt in half a second — and that half-second is
the same half-second the audience gets.

Which means the vague notes are worth **more** than the precise ones. A precise note
tells you about one shot. *"Second nine feels weird, I don't know why"* tells you
something is wrong in a place nobody has thought to look — that is how all eight
pairs in `29-relationship-master.md` were found.

So the division of labour is:

> **HE SUPPLIES THE FLINCH AND THE TIMESTAMP.
> THE PIPELINE SUPPLIES THE MICROSCOPE.**

```
python3 tools/flinch.py <project> <seconds>
```

Never ask him to justify a reaction before you act on it. Point the instruments at
the timestamp. If nothing explains it, **that is the finding** — build the
instrument that would have seen it.

## WHY SWITCHING FORMAT KEEPS HURTING

> "I thought I had tuned all of my QC layers to predict and prevent these kinds of
> things, but it keeps on happening — especially when I switch from vlog content to
> car review then switch to car cinematic, there turns out to be more and more
> problem."

Three mechanisms, two of them now fixed:

1. **Lessons did not travel.** `lessonize` filed to the *genre* by default and
   `planqc 23` only blocks on topics a plan declares — so a lesson under
   "travel vlog" was **invisible** to a car review plan. *Fixed: craft is now the
   default bucket, and check 23b blocks on neighbouring genres.*
2. **Numbers travelled when they shouldn't.** A clamp fitted on night car footage
   ran on a golden-hour travel vlog and quietly stopped working. *Fixed:
   `ledgers/thresholds.json` records provenance and `planqc 33` refuses borrowed
   numbers.*
3. **Every new format brings pairs that have never failed before.** Irreducible.
   Mukbang puts eating sound against a face; car review puts a spoken claim against
   what's on screen. Nothing can predict those until that format is shot.

## WHAT IS ACTUALLY BUILDABLE, AND WHAT ISN'T

| the piece | reality |
|---|---|
| Find what's winning in a niche | Yes. YouTube has a real API; TikTok and Instagram are locked down and scraping breaks their terms. Expect "a good sample," not "the whole web." |
| Measure a winner's structure | **Yes, and this is the strong part.** Cut times, shot lengths, motion curve, luma arc, hook timing, audio bands, caption timing — all from the file. `flinch.py` and `verify.py` already do exactly this. |
| Read a competitor's retention | **No.** Views, likes, comments and shares are public; average watch time and the retention curve belong to the account owner. Proxy it (views against follower count, comment ratio, rewatch language) and know you are proxying. |
| Read HIS retention | Yes — he owns Urban Auto Hub. Needs a Meta Graph page token. **This is the only legitimate retention data in the system.** |

## THE SEQUENCING THAT FOLLOWS

He made the correction himself and it is the right one:

> "What makes you think the retention rate will be good if the video doesn't even
> pass my own quality check? Do you think others would watch if I myself wouldn't
> even watch finish the video?"

**His gate comes first.** Analytics on a video that fails him teach nothing — the
data just says "this was bad," which he already knew, and it costs a post on a page
he is trying to grow. Real numbers only start meaning something once videos clear
him consistently. Then they answer the question his eye can't: *of two cuts I would
both accept, which one held people longer.*

## THE STANDING ORDERS

- Show him the contact sheet **before** anything is assembled.
- Deliver a **hosted link**, never an attachment.
- Never send a link `talyx.py deliver` did not print.
- Name things in human language. His reason for "mastermind": *"because it's an
  easier word to remember than all those other words — something more like a human
  language rather than an AI understood language."* Write gate output as a sentence
  someone can act on.
