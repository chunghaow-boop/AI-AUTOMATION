# CONSOLIDATION PROPOSAL — what stays, what goes
### File 39. Nothing is deleted without your explicit yes. Append-only archive, never destroy.
### Scored against ONE question: does this help produce fully-AI vlog / car review / industry
### value content at the quality level of the reference videos?

---

## THE DIAGNOSIS

**Current state:** 6,009 lines across 27 repo files + **12 files I added today** + 9 tools.

The bloat is not evenly spread. It sits in exactly two places:

**1. The judgement layer — FIVE overlapping scoring systems.**
```
RUNNER build self-score  /60      6 seats
RUNNER plan self-score   /60      6 judges
file 06 judges           /10 ea   J0 + J1-J6
file 25 debate + tournament       per-seat challenge, 3 proposals
file 26 master scorecard /100     weighted, hard gates
```
That's one opinion counted five times — and the evaluation research (file 33) says stacking
self-judgement **amplifies** bias rather than reducing it. Consolidating isn't tidying; it's a
correctness fix.

**2. My own session output — 12 analysis files.**
Several are point-in-time findings that belong in the archive once their content is merged.
Owning that: I contributed roughly 80KB of documentation to a system whose stated problem was
too much documentation.

**What is NOT bloated:** the craft layer. Camera spec, performance, emotion, banks, prompts.
With the pivot to fully-AI generation these get **more** important, because everything that was
going to be captured on camera must now be written as text in a prompt.

---

## ⬆️ THE PIVOT CHANGES THE SCORING

Fully-AI generation **promotes** files I'd otherwise have questioned:

| File | Was | Now |
|---|---|---|
| **03 physical performance** (202 ln) | "for Nev on camera" | ⬆️ **CRITICAL** — weight, hands, gestures must be *written* into the prompt. The AI actor has no instincts |
| **07 emotion engine** (151 ln) | for real performance | ⬆️ **CRITICAL** — "name the conflict, not the expression" is now prompt language |
| **05 cinematic spec** (874 ln) | cinematic only | ⬆️ **CORE** — camera body, lens, T-stop are literal prompt tokens. Biggest file, now most used |
| **23 asset pre-production** (95 ln) | optional insurance | ⬆️ **MANDATORY** — consistency IS the product for an AI persona |
| **13 asset banks** (276 ln) | reference | ⬆️ **CORE** — the prompt vocabulary |
| **17 car cinematic prompt** (99 ln) | one format | ⬆️ **the template** to fork for all three formats |

---

## THE PROPOSAL

### ✅ KEEP AS-IS — 13 files (the working system)
```
RUNNER            the spine
18 agent contract the operating rule
22 HANDOVER       state
09 learning log   memory (4 lines?! — it's been truncated, needs restoring from archive)
05 cinematic spec camera/lens/light language for prompts
03 performance    body language as prompt text
07 emotion        conflict as prompt text
13 asset banks    prompt vocabulary
17 master prompt  the fork-from template
23 asset preprod  the character sheet — now mandatory
14 avatars/series who it's for + pillar discipline
15 launch         posting + the 24h read
11 editing bank   assembly recipes
```

### 🔀 MERGE — 9 files → 3
| Merge these | Into | Why |
|---|---|---|
| 06 judges + 25 debate + 26 scorecard + RUNNER's two /60s | **ONE gate file** | five scorers = one opinion counted five times. Keep: J0 veto · hard mechanical gates · ONE weighted score · pairwise for choosing. Drop: extra debate rounds, A/B/C labels, duplicate scorecards |
| 04 foley + 12 SFX bank + 19 sound engineer | **ONE sound file** | your own audit already said 04 is superseded. And `generate_audio:true` changes the sound doctrine anyway |
| 16 master skeleton | **into RUNNER** | your own audit's verdict, never executed |
| 35 bank additions | **into 13 + 02 + 11** | it was written to be merged, not kept |

### 📦 ARCHIVE — served their purpose (append-only, never deleted)
```
00 START-HERE        superseded by 22
24 system audit      point-in-time, its verdict is now executed here
27 editing automation superseded by the actual tools
28 mastermind loop   → collapse to a README line per tool
31 capability audit  point-in-time
32 QC upgrades       → merge the surviving items into the gate file
34 douyin analysis   point-in-time; mechanics already extracted to 35
36 AI editor pipeline → collapse into RUNNER as the edit stage
37 DO THIS NOW       point-in-time action list
20 SFX list          shopping list, consumed once
21 BGM list          same
```

### ✂️ TRUE CUTS — only 2, and both are your own audit's call
```
04 foley-master      fully superseded by 12 + 19 (verdict from file 24, never executed)
00 START-HERE        replaced by 22-HANDOVER
```
*(Both go to /archive/, not deleted. Nothing is destroyed.)*

### ⚠️ KEEP BUT REWRITE — the pivot broke these
```
01 spine + Thai reversal   4-beat spine still good; check for real-footage assumptions
02 crew + swipe            swipe file good; "crew" roles need rewriting as prompt-writers
08 strategist              fine
10 the editor              rewrite around the EDL (edl.py), not manual editing
19 sound engineer          rewrite: generate_audio:true changes everything
```

---

## THE RESULT
```
BEFORE   27 repo files + 12 session files = 39 documents · ~6,000 + ~80KB
AFTER    ~16 live files + /archive/ + 9 tools + 1 gate file
```
**Roughly 60% fewer live documents, zero capability lost**, and the judgement layer stops
double-counting itself.

---

## ⚠️ THE THING CONSOLIDATION WON'T FIX

Cutting files does not get you to the quality in those reference videos. That gap is:
1. **The character sheet** — not built yet. Consistency is the entire product for an AI persona.
2. **`generate_audio: true`** — never tested. Your talking formats depend on it.
3. **A skill** — they invoke `/seedance-director-shotlist` as one command. You have the same
   process spread across 6,000 lines of documentation.
4. **One posted video.** Still zero.

**Documentation volume was never the thing standing between you and their quality.** But a
leaner system is faster to run and easier to keep correct, and the five-scorer consolidation is a
genuine accuracy fix — so it's worth doing once, now, and then not again.
