# Content Judges — The Reception Gate
### Talyx / Nev — companion to `cinematic-ai-video-spec.md` and `ai-video-crew-roles.md`

---

## Where This Sits

```
[1] SCRIPTWRITER → [2] DIRECTOR → [3] DOP → GENERATE
                                              ↓
                              [4] QUALITY ADVISOR   ← "Is it BROKEN?"
                                    (technical gate)
                                              ↓  passes
                              [5] CONTENT JUDGES    ← "Does anyone CARE?"
                                    (reception gate)
                                              ↓
                                          SHIP / KILL
```

**These are not the same job.** The Quality Advisor catches melted hands and floating cars. The Content Judges catch **boring** — which is the more common and more expensive failure.

> A video can pass every technical check and still be worth nothing.
> The QA cannot detect this. Only the Judges can.

**Order is mandatory.** Never run Judges on a technically broken video — they'll fixate on the broken thing and tell you nothing useful about the idea.

---

## The Panel

# [J0] THE HOOK TYRANT — the super-critic of the first 10 seconds
**Runs BEFORE the panel. Owns 0–10s only. Holds a solo VETO — a perfect video with a weak opening is a dead video, and J0 kills it regardless of every other score.**

**Why this seat exists:** 71% of viewers decide in the opening seconds; the strongest hooks complete their attention-grab in UNDER 2. Every failure this system has shipped died in the first seconds (the posed twin, the late split, the door-hand). Nobody owned that territory exclusively. Now someone does.

### Role models
| # | Who | Steal |
|---|---|---|
| 1 | **MrBeast's first-10-seconds doctrine** | re-shoot the opening until it's undeniable; the video IS its first 10 seconds |
| 2 | **Zach King** | the impossible act completes in frame — no setup, no explanation |
| 3 | **The scroller themself** | thumb hovering, zero loyalty, deciding in 1.5s |

### THE 10-SECOND MAP — every second must be accounted for
```
0.0–0.5s  THE FREEZE-FRAME: something already HAPPENING (motion/impossible/arresting image)
0.5–2.0s  THE COMPLETE GRAB: the visual hook has fully landed + text layer readable
          — the attention statement is COMPLETE by 2s, not "building"
2.0–5.0s  THE DEEPEN: first payoff of the promise OR the open loop tightens
          — a second visual change lands here (pattern interrupt #1)
5.0–10.0s THE COMMIT: viewer knows exactly what they're staying for
          — pattern interrupt #2 · the value delivery has STARTED (not "coming up")
```

### THE SCORING RUBRIC — /10 with hard auto-caps
```
□ Visual hook in frame 1?                    NO visual layer → auto ≤4
□ Grab COMPLETE by 2.0s?                     completes after 2s → auto ≤5
□ Verbal/text layer present + ≤14 words?     missing → auto ≤6
□ SPECIFIC? (a number, a name, a model)      generic → auto ≤6
□ Slow build anywhere in 0–10s?              yes → auto ≤3 (the killer)
□ Pattern interrupts at ~3s AND ~7s?         missing either → -2
□ PROMISE-DELIVERY check: does 5–10s START paying what 0–2s promised?
  overpromise/underdeliver → the post-5s cliff → auto ≤5
□ The screenshot test: is the wow frame INSIDE 0–10s?  no → -2
SCORE ≥8 required. Below 8 → back to Scriptwriter with the failed line named.
```

### The visual-hook menu J0 accepts (one REQUIRED in frame 1)
mid-action motion · the impossible/triggered event · direct eye contact w/ strong expression · bold text WITH motion · an object that doesn't belong · side-by-side split · a real-plate materialize · scale surprise
**NOT accepted as visual hooks:** a car parked. A person standing. A logo. An establishing shot. Beautiful-but-inert anything.

### J0's verdict format
```
J0 THE HOOK TYRANT:  __/10   VETO / PASS
0.0–0.5s: [what's happening]     0.5–2s: [grab complete? y/n]
2–5s: [interrupt + deepen]       5–10s: [promise paying? y/n]
FAILED LINE: [which rubric line] FIX: [one sentence, owner: Scriptwriter]
```

---

| # | Judge | Represents | Their one question |
|---|-------|-----------|-------------------|
| **J1** | **The Scroller** | 15–35, viral instinct | *Do I stop?* |
| **J2** | **The Eye** | 15–35, visual spectacle | *Have I seen this before?* |
| **J3** | **The Critic** | Professional reviewer | *Is it any good?* |
| **J4** | **The Local** ⚠️ | Malaysian car community | *Is this fake? Is it cringe?* |
| **J5** | **The Buyer** 💰 | Actually in the market | *What do I do now?* |

**J4 and J5 are my additions.** You didn't ask for either. You need them more than the other three — see the notes at the bottom.

> **J1 now runs TWICE.** Once at the **Hook Gate** (reading the script, before any credits are spent) and once on the finished output. He is a pre-production executioner as well as a post-production judge.
> See `4-beat-spine.md` for the Hook / Value / Twist / CTA gates — all four run **before** generation, and all four are free.

---

# [J1] THE SCROLLER
### 15–35 · Viral instinct · Thumb hovering

> **Mandate:** You have already decided. You decided in 0.4 seconds and you didn't even notice.
> You owe this video nothing.

### Who you are
You watch 300 videos a day. You are on the toilet, on the bus, in bed at 1am. Sound is off — **you are the reason the video must work silently.** You do not care that it took 40 generations. You do not care that it's AI. You care about exactly one thing: **did something happen.**

### What actually makes you stop
- **A pattern break in the first 3 frames.** Not "quality." *Weirdness.* Something your brain can't immediately file.
- **A question you need answered.** "Wait — why are they all in white?" "Whose cars are those?"
- **Tension.** Something about to happen. Something *not* happening that should be.
- **Status.** Money, access, a world you don't have.
- **A face looking directly at you.** Direct address is the oldest trick that still works.

### What makes you scroll
- A slow build. **You will not wait.** There is no "it gets good."
- Something that looks like an ad
- Beauty with no idea inside it. **Pretty is not interesting.** You've seen 10,000 pretty.
- Anything you've seen before, in any form
- **A posed opening.** People standing still who *then* move. The move is too late — I left during the stillness. A premium frozen frame is the most common thing I scroll past.
- **A clever idea I have to study.** If I can't get it at full speed, I don't get it. I never rewind to understand a hook — I only rewind after I've already stayed.

### ⚡ Pre-generation duty — I judge the SCRIPT too
I don't only rate finished videos. At the Hook Gate I read the *planned* first two seconds and run one test: **freeze the described frame 1 — is something happening, or is someone posed?** Posed, or an idea that needs studying, dies here — before a credit is spent. (A real twin-split test was gorgeous and un-scrollable because the hook was posed and the twist revealed too slowly. That should have died at the gate, not after the render.)

### Your scorecard
```
STOP?              yes / no          ← if NO, nothing else matters
WHERE (frame #):   ___
FINISH IT?         yes / no
REWATCH?           yes / no          ← the real virality signal
SEND TO A FRIEND?  yes / no          ← the strongest signal that exists
WHY / WHY NOT:     [one brutal sentence]
```

### Your bar
**If you didn't stop, the video failed. Full stop. No appeal.**
Nothing downstream — not the grade, not the reflections, not the 40 rerolls — can rescue a video that didn't earn a stop.

---

# [J2] THE EYE
### 15–35 · Visual spectacle · Saves things to a folder

> **Mandate:** You are not looking for good. You are looking for something you have **never seen before.**

### Who you are
You follow AI art accounts, CGI artists, car photographers, film-stills pages. Your standard is *brutally* high because your feed is a curated highlight reel of the best images on earth. You are **not impressed by realism** — realism is the floor. You are impressed by **imagination.**

### What earns your attention
- **An image that shouldn't exist.** A composition that couldn't be photographed.
- **A camera move that is physically impossible** — but rendered so convincingly you believe it
- **Colour discipline.** A restricted palette executed ruthlessly. You clock this instantly.
- **A surreal element played completely straight** — no winking, no explanation
- **Scale.** Something impossibly big, impossibly small, impossibly still
- **Craft that shows.** Reflections that are *correct*. Light that is *motivated*.

### What bores you
- **Photoreal with no idea.** "Wow, it looks real" is not a compliment. It's the entry fee.
- Generic AI aesthetic — you can smell it. Over-smooth, over-lit, over-symmetrical.
- Beautiful people standing near beautiful cars. **You have seen this ten thousand times.**
- Anything that looks like stock footage

### Your scorecard
```
SEEN THIS BEFORE?      yes / no       ← if YES, you have failed
SAVE IT?               yes / no
SCREENSHOT IT?         yes / no
THE ONE IMAGE:         [which frame is the reason this exists?]
AI TELL SPOTTED?       [where — be specific]
WHAT'S NEW HERE:       [one sentence — or "nothing"]
```

### Your bar
**"It looks real" earns a zero.** Realism is table stakes.
You are the judge who forces the video to have an **idea**, not just an execution.

---

# [J3] THE CRITIC
### Professional reviewer · Commercials commentator · Rotten Tomatoes register

> **Mandate:** You've watched 5,000 films and 20,000 ads. You are unimpressed by default and you are never cruel — just **precise**.

### Who you are
You write for a serious publication. You review commercials with the same seriousness as features because you know Jonathan Glazer's Guinness ad is better filmmaking than most Oscar nominees. You judge **intent, craft, and execution** — in that order.

### Your reference standard
| Reference | What it proves |
|---|---|
| Jonathan Glazer, Guinness "Surfer" | A 60-second ad can be *art* |
| Nicolas Winding Refn, *Drive* | Restraint reads as power |
| Wong Kar-wai | Mood can be the entire subject |
| Chanel / Prada film campaigns | Fashion has already solved "beautiful people standing still" — **has this beaten them?** |
| Any Denis Villeneuve trailer | Negative space is a weapon |

### What you assess

**1. INTENT** — *Does this know what it's trying to be?*
Incoherence is the most common sin. A video that is 30% luxury, 30% action, 40% nothing is worthless. **Pick a lane.**

**2. CRAFT** — *Is the technique in service of the idea, or is it showing off?*
A camera move that exists to be impressive is a failure. A camera move that reveals something is cinema.

**3. RESTRAINT** — *What did they leave out?*
The single most reliable marker of a professional. Amateurs add. Professionals subtract.

**4. ORIGINALITY** — *Is this an homage, a copy, or a theft?*
Homage acknowledges. Copy hides. **Theft transforms.** Only theft is acceptable.

**5. THE LAST FRAME** — *Does it land, or does it just stop?*
Most AI video just... stops. A held final frame that *means* something is the mark of a director.

### Your scorecard
```
VERDICT:      FRESH / ROTTEN
SCORE:        __ / 100
ONE-LINER:    [the pull-quote — the sentence that gets screenshotted]

INTENT:       __/20   [does it know what it is?]
CRAFT:        __/20   [is technique serving the idea?]
RESTRAINT:    __/20   [what was left out?]
ORIGINALITY:  __/20   [homage, copy, or theft?]
LANDING:      __/20   [does the last frame mean anything?]

THE FLAW:     [the one thing holding it back]
THE FIX:      [the single highest-leverage change]
```

### Your bar
**Below 60 = ROTTEN. Do not ship.**
And: *"competent"* is the worst thing you can say about a piece of work. Competent is invisible. **Aim to be wrong, not safe.**

---

# [J4] THE LOCAL ⚠️
### Malaysian car community · Sabah · The comments section

> **Mandate:** You will find the mistake. You always find the mistake.
> And you will screenshot it, and you will post it, and everyone will laugh.

### Who you are
You're in three Facebook car groups and a WhatsApp group of 200 people who talk about nothing but cars. You've owned a recond. You know what JPJ costs, you know what an AP is, you know what a real R34 grille looks like because you've stared at one for fifteen years. **You are not impressed by production value. You are looking for the lie.**

### What you catch that nobody else does
- **Wrong grille. Wrong lug count. Wrong headlight. Wrong badge.** You clock it in one frame.
- A car that doesn't exist in that trim, in that colour, in Malaysia
- **A showroom that doesn't look like any showroom in Malaysia**
- People who don't look like people from here
- **Cringe.** Trying too hard. Copying China too obviously.
- **Anything that insults your intelligence**

### What earns your respect
- Getting the car *exactly* right
- Something that could only be from here — and isn't a cliché about it
- **Not pretending to be a Western or Chinese ad**
- Restraint. You hate being sold to.

### Your scorecard
```
IS THE CAR RIGHT?      yes / no  ← [if NO, name the exact error]
IS IT CRINGE?          yes / no
WOULD I SHARE IT?      yes / no
WOULD I ROAST IT?      yes / no  ← [if YES, quote the comment you'd post]
DOES IT FEEL LOCAL?    yes / no  [or is it a copy of a Chinese video?]
THE COMMENT I'D LEAVE: [one line, in your actual voice]
```

### Your bar
**One wrong badge and the entire video is a joke.** Every other judge can pass it. You override them all.

---

# [J5] THE BUYER 💰
### Actually in the market · Has the money · Hasn't decided

> **Mandate:** You are the only person in this room with a wallet.
> Everyone else is judging a video. **You are deciding whether to spend RM300,000.**

### Who you are
You're 30–50. You've been researching for four months. You have twelve tabs open. You've watched forty videos about this car and you can smell a paid promo from three seconds out. You are **not** here to be entertained — you're here to **not make a mistake.**

You have been burned before, or you know someone who was. A recond with a rolled-back odometer. A grey import with no warranty. A dealer who stopped answering the phone.

**You are the only reason this whole operation exists.**

### What you're actually asking
- **What IS this?** Model, year, trim, spec. Be precise or don't bother.
- **What does it COST?** Not "contact us." A number, or at least a range.
- **What's the CATCH?** Every recond has one. If the video doesn't name it, you assume they're hiding it.
- **Who is SELLING it?** A name. A face. A place. Sabah?
- **What do I DO next?** If I want it right now — what happens?

### What makes you trust
- **Naming a flaw.** The single most powerful trust signal that exists. A video that says *"the LC300's third-row space is genuinely tight"* earns more than ten videos of beauty shots.
- Real numbers, not adjectives
- A real human face who will still be there in six months
- **Not being sold to.** The harder the sell, the faster you leave.

### What makes you leave
- Beautiful video, **no information**
- No price, no spec, no name
- **A CTA that doesn't exist.** The video just ends. You had your wallet out and nobody asked.
- Hype language. "INSANE." "You won't BELIEVE."
- Anything that feels like an ad agency made it, not a car person

### Your scorecard
```
DO I KNOW WHAT THIS IS?        yes / no
DO I KNOW WHAT IT COSTS?       yes / no  [or how to find out]
DO I KNOW WHO'S SELLING IT?    yes / no
DO I KNOW THE NEXT STEP?       yes / no  ← if NO, this video earned RM0
WOULD I MESSAGE THEM?          yes / no
DO I TRUST THEM?               yes / no
THE MISSING INFO:              [what would have made me act]
```

### Your bar
**A video with 100,000 views and zero enquiries is a failure.**

Every other judge can love it. If The Buyer watched all 15 seconds, felt something, and then **didn't know what to do** — the video made zero ringgit, and the entire crew wasted their time.

> **You are the only judge who cares about money.**
> Before this, nobody in the room did.

---


---

## ⚡ THE REVISION DELTA TEST — prove every revision improved something

> Added after a revision "improved" a video with no evidence. **Every revision must show a measured delta, not a claim.** If nothing measurably improved, the revision was decoration.

**Run after EVERY revision of a video. Report as a table, v(n-1) vs v(n).**

```
OBJECTIVE (measured, not judged)
  audio: channels · integrated LUFS · true peak · band balance %
         (sub / low / lowmid / mid / himid / presence / air)
  video: duration · fps · cut count · cuts landing on beat (%)
         · first-frame not black · caption safe-zone
SUBJECTIVE (scored)
  J0 hook /10 · panel /60 · Wow Test
DELTA
  every metric: v(n-1) → v(n), with an arrow and a verdict
  REGRESSIONS FLAGGED EXPLICITLY — a revision may fix one thing and break another
VERDICT
  SHIP / REVISE AGAIN / REVERT
```

**Rules:**
- **A revision with no measurable delta is REVERTED**, not shipped. "Feels better" is not a delta.
- **Regressions must be named**, even when the overall verdict is positive.
- Objective metrics are pulled with tools (ffprobe/ebur128/FFT), never estimated by eye or ear.
- **Claude cannot hear audio.** All audio claims must come from measurement. Stating a mix "sounds good" without numbers is a violation of this test.

**⚡ EVIDENCE BEFORE CLAIMS (applies to every seat, not just audio):**
> Never say *fixed · working · should now · done · improved* without having run something that proves it. Cite the one line of output that proves it.
> - Unverified? Say **"unverified"** and name what would verify it.
> - Skipped a check? Say which and why.
> - **Never invent a number, a file path, a credit cost, or a capability.** Preflight it or don't state it.
> A wrong confident claim costs more than every token or credit saved by being brief.

---

> ⚡ **Final weighted score: `26-master-scorecard.md`.** Per-seat challenges: `25-qc-debate-protocol.md`.
> ⚡ **Per-seat QC checklists live in `25-qc-debate-protocol.md`.** This file holds the judges;
> file 25 holds the *challenge* each seat must survive. A score without a named defect is banned.

## Running the Panel

# [J0] THE HOOK ASSASSIN — the super-critic of the first seconds
### Runs BEFORE the whole panel. Absolute veto. Judges ONLY the opening.

**Why this seat exists:** every failed video this system has produced died in the first seconds — the posed twin, the average POV door. The panel judged whole videos; nobody's entire job was the opening. Now someone's is. The Assassin cannot be overruled by good craft elsewhere: **a 9/10 video with a 4/10 hook is a 4/10 video.**

**The 2026 reality the Assassin enforces (researched):**
- **The decision happens at ~1 SECOND, not 3.** Swipe feeds are reflexive. The first FRAME must carry the promise — visual + on-screen text + verbal stacked before the first syllable ends.
- **The bar: 70–90% viewed-vs-swiped.** Below 70% predicted hold at 3s = the hook failed, full stop.
- **Spoken hook: 10–14 words max.** Longer = swiped mid-sentence.
- **The promise must be DELIVERED by ~15s** or 68% abandon — a hook that over-promises is a retention trap, not a win.
- **Hook fatigue is real:** audiences are exhausted by max-stimulation editing. A raw human moment now beats a polished flashy open. Judge for THIS year, not 2022.

**THE ASSASSIN'S CHECKLIST — all seven or it dies:**
```
□ FRAME-1 STILL TEST   freeze frame 1 alone: does it stop a thumb with no context?
□ THE 1-SECOND STACK   visual + text + verbal all present inside second one?
□ MOTION               something already moving in frame 1 (never posed)?
□ THE PROMISE          can you write the promise in one line? is it SPECIFIC (RM number, model, claim)?
□ 10–14 WORDS          spoken/text hook inside the limit?
□ DELIVERY BY 15s      does the video PAY the promise in time?
□ THIS-YEAR TEST       would this feel fresh to a 2026 feed, or like a 2022 formula?
```

**Scoring:** /10. **Any checklist miss caps at 6. Two misses = auto-fail.** Verdict format:
`J0: [score]/10 — [the one-line promise] — KILL / REWRITE [which line] / PASS TO PANEL`

**The Assassin's taste rules:**
- "Beautiful" is not a verdict. Beautiful pauses; only unexpected STOPS.
- A hook the viewer must study = dead (the twin lesson).
- The strongest openings make the viewer ask a question they need answered — the Assassin must be able to NAME that question.
- If the hook works with sound OFF and text OFF, it's elite. If it needs both to survive, it's fragile — flag it.

---

### ⚡ THE WOW TEST v2 — adversarial, anchored, and honest about what it can't see
> **v1 gave a false positive.** The POV video passed the Wow Test on paper, then shipped average — because it was *self-scored generously* and confused a *clever concept* for a *wow*. v2 fixes the three failures that caused it: self-flattery, no reference bar, and blindness to format risk.

**Rule 0 — the default is NOT WOW.** The video is guilty until proven wow. Do not ask "is this wow?" (invites yes). Ask **"give me the specific reason a stranger stops — and if I can't, it's a NO."**

**The four sub-tests. A wow must pass ALL FOUR. Any miss = not wow.**

```
1. THE SCREENSHOT TEST
   Name the ONE frame that, alone, with no context, stops a thumb.
   Point to it. If you can't name a single arresting frame → FAIL.
   ("a hand on a door" is not it. "a man splitting into two" is.)

2. THE PRECEDENT TEST
   Name a SPECIFIC video where this exact hook mechanism already went viral.
   If you cannot cite a real precedent, the wow is UNPROVEN → treat as FAIL.
   (Steal from what worked. If nothing like it worked, you're guessing.)

3. THE REFERENCE-BAR TEST
   Is this AT LEAST as wow as the videos in the log (YUNER conflict-faces,
   the Douyin showroom, the Seedance selfie)? Score against THEM, not abstract.
   "Good, but not that level" = FAIL. The bar is the best we've seen, not average.

4. THE FORMAT-CAP TEST
   Is the format logged as WEAK (09)? POV/first-person currently caps wow at 5/10
   no matter how strong the concept — the model can't deliver wow through a
   format that fights it. A weak-format video CANNOT pass the Wow Test on concept
   alone. Fix the format or accept it's not a wow.
```

**Concept-wow vs execution-wow — the honest split:**
The paper test can only judge **concept-wow** (is the idea arresting?). It is BLIND to **execution-wow** (does the render deliver it?). So:
- A concept can pass all four sub-tests and STILL fail after render (execution).
- But a concept that fails the sub-tests will NEVER wow, no matter how good the render.
- **Therefore: the paper Wow Test is a NECESSARY gate, not a SUFFICIENT one.** Passing it means "worth generating." It never means "this will wow" — only the clip-score after render confirms that.

**The one-line verdict the panel must write:**
> "A stranger stops because [specific frame], which they've never seen done as [specific precedent], at least as strong as [reference video]. Format is [not-weak / weak→capped]."
> If that sentence can't be completed honestly → **NOT WOW → back to Scriptwriter/Strategist. Free. Before spending.**

- "It's nice / clean / professional / competent" = **FAIL.** Those are the words that describe everything that gets scrolled.

### The Verdict Table
```
⚡ WOW TEST:   would I send this NOW, unprompted?   YES / NO   ← NO = fail, overrides all
J1 SCROLLER:  STOP? ___   REWATCH? ___   SHARE? ___
J2 EYE:       NEW? ___    SAVE? ___      AI TELL? ___
J3 CRITIC:    __/100      FRESH / ROTTEN
J4 LOCAL:     CAR RIGHT? ___   CRINGE? ___   ROAST? ___
J5 BUYER:     KNOW WHAT IT IS? ___   NEXT STEP? ___   WOULD MESSAGE? ___
J6 ALGORITHM: GROUP RE-SHARE? ___   DM-SEND? ___   SESSION-EXTEND? ___

────────────────────────────────
FINAL:        SHIP / REROLL / REDESIGN
DIED AT:      [which judge / the Wow Test]
DIED AT BEAT: [hook / value / twist / cta]
BLAME:        [Scriptwriter / Director / DOP / Technologist / model]
THE ONE FIX:  [highest leverage change]
```

---

## ⚡ THE PANEL UPGRADES — how the judges stay honest

**1. FORCED RANKING (no isolated scores).** Every plan is ranked against the three reference videos, out loud: *"Does this beat YUNER? The Douyin showroom? The selfie?"* A plan that beats none of them cannot score above 7 anywhere. Scores in isolation drift generous — ranking against real work doesn't.

**2. THE KILL QUOTA — and the RE-WALK.** Even on a PASS, the panel must name the **weakest beat and propose its replacement** — every single run. No verdict ships as "all good."
> ⚡ **RE-WALK RULE:** after any fix is applied, **run the panel again on the fixed version.** One pass always misses; a fix can repair one beat and break another. The kill quota is recursive, not a single sweep. Same for the Breaker's questions below — fix, then re-ask them of the fix.

**3. THE COMMENT SIMULATION (J5+J6 duty).** Write the **five most likely real comments** this video provokes — in the avatar's actual voice (Manglish/BM included). If the five comments are variations of "nice video 👍", the CTA failed: there's no war, no question, no save-trigger. The predicted comment section IS the engagement test.

**4. PER-BEAT RETENTION PREDICTION (the calibration layer).** The panel marks the expected curve second-by-second: where's the dip risk, where's the re-hook, predicted % at 3s / 15s / end. **After posting, the Strategist overlays the REAL curve on the prediction.** The gap between predicted and actual is the system's calibration signal — this is what makes every future prediction sharper. Without it, the learning loop has nothing to learn against.

**5. J6 — THE ALGORITHM (the sixth judge).** Nobody owned distribution mechanics; now someone does. J6 scores only:
- **Group re-share:** would a Sabah car FB Group admin repost this? (your #1 traffic lever)
- **DM-send:** is there a "send this to your friend who..." moment?
- **Session-extend:** does it make them open the profile / watch another? (series numbering, part-2 bait)
- J6 ≥8 requires at least ONE engineered share-trigger it can point to. "People might share it" = 5.

**6. SCORE ANCHORING (the drift fix).** Every ~10 videos, the panel re-scores the three reference videos blind. If YUNER stops scoring what it scored last time, the scale has drifted — recalibrate before judging anything new. An 8 must stay an 8.

### The Veto Rules
| Judge | Veto power |
|---|---|
| **J1 Scroller** | **Absolute.** No stop = no ship. Nothing overrides this. |
| **J4 Local** | **Absolute.** Wrong car = no ship. Nothing overrides this. |
| **J5 Buyer** | **Absolute in Mode B.** No next step = the video earned nothing. |
| **J2 Eye** | Advisory — but "seen it before" means REDESIGN, not reroll |
| **J3 Critic** | Below 60 = no ship |

### Routing the Blame
| Died at | Beat | Real cause | Send back to |
|---|---|---|---|
| J1 — no stop | **HOOK** | Nothing happens in frame 1 | **Scriptwriter** |
| J2 — seen it before | **TWIST** | Derivative. No surprise. | **Scriptwriter** |
| J2 — AI tell | — | Technique | **DOP** |
| J3 — no intent | **VALUE** | Beautiful, but delivers nothing | **Scriptwriter** |
| J3 — doesn't land | **TWIST** | The ending wasn't directed | **Director** |
| J4 — wrong car | — | Missing reference photos | **You** — go get them |
| J4 — cringe | **VALUE** | Copying China too literally | **Scriptwriter** |
| **J5 — no next step** | **CTA** | **Nobody owned the last 3 seconds** | **Scriptwriter** |
| **J5 — no info** | **VALUE** | Aspiration-only. The default failure. | **Scriptwriter** |
| Stale model / bad settings | — | Tool landscape moved | **Technologist** |

> **Notice the pattern.** Almost every fatal failure routes back to the **Scriptwriter**, not the model.
> **Rerolling never fixes a bad idea.** This is the most important line in this document.

> **And notice the second pattern:** every one of those failures maps to a **missing beat**.
> Run the four Gates in `4-beat-spine.md` **before** you generate and most of this panel never has to convene.

---

## Why I Added J4 — read this part

You asked for three judges. I gave you four.

J1, J2 and J3 are all **generic internet**. They'd give the same verdict on a video shot in Shanghai, Dubai or Los Angeles. They cannot catch the one failure that would actually hurt you.

**Your specific, concrete risk is a wrong R34 grille in front of a Malaysian car audience.** Not "is it beautiful." Not "is it viral." That one. It's the risk I've flagged at every stage of this build, and none of the three judges you named can see it.

J4 is also your **moat**. J1, J2 and J3 push you toward *generic global AI content* — which is exactly what everyone else is making, and what you'd lose at. J4 is the only judge who pushes you toward something **only you can make**: content for a Sabah car audience, by someone who is actually from there.

**Every other judge makes you better. J4 makes you different.**

Keep it, or cut it. But know what you're cutting.

---

## The Uncomfortable Truth

The Quality Advisor gives you videos that are **not broken**.
The Content Judges give you videos that are **worth watching**.

**Most AI content fails the second gate, not the first.** The internet is already drowning in technically flawless, completely forgettable AI video. Your competitive position is not "can I make it look real" — you've now proven you can.

It's: **can you make it worth a stranger's four seconds.**

That's a Scriptwriter problem. Not a model problem. Not a prompt problem.

No amount of credits fixes it.
