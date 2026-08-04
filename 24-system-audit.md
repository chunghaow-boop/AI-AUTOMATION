# SYSTEM AUDIT — every file scored against the four real formats
### File 24 · Audit v2. **v1 was wrong** — it was scored on cinematics alone, when the actual
### roadmap is vlog · car review · industry value · cinematic. Three of four are TALKING formats.

---

## THE FOUR FORMATS
```
CIN  cinematic hero        file 17 multi-shot · AI-generated · proven (Urus, R8)
VLG  vlog / day-in-life    Recipe 5 · REAL footage + AI inserts · unproven
REV  car review            Recipe 7 talking head · REAL footage · ZERO credits · unproven
IND  industry value        Recipe 7 or R3 chaptered · REAL footage · unproven
```
> **Three of four need no video generation at all.** The credit-heavy path is the minority.
> That inverts the system's centre of gravity — the edit layer and the human seats now matter most.

---

## THE MATRIX  (✅ core · ○ used · – not used)

| File | CIN | VLG | REV | IND | Verdict |
|---|:--:|:--:|:--:|:--:|---|
| **RUNNER** | ✅ | ✅ | ✅ | ✅ | **KEEP** — spine |
| **18 agent contract** | ✅ | ✅ | ✅ | ✅ | **KEEP** — the spec |
| **22 HANDOVER** | ✅ | ✅ | ✅ | ✅ | **KEEP** — state |
| **09 learning log** | ✅ | ✅ | ✅ | ✅ | **KEEP** — memory |
| **13 asset banks** | ✅ | ✅ | ✅ | ✅ | **KEEP** — Bank 9/10 used every run |
| **06 judges (J0)** | ✅ | ✅ | ✅ | ✅ | **KEEP** — J0 has real teeth |
| **06 judges (J1-J6)** | ○ | ○ | ✅ | ✅ | **KEEP** — J4/J5 only bite on real reviews |
| **11 editing bank** | ✅ | ✅ | ✅ | ✅ | **KEEP** — R5/R7 are the new workhorses |
| **19 sound engineer** | ✅ | ✅ | ✅ | ✅ | **KEEP** — now has measured targets |
| **12 SFX bank** | ✅ | ✅ | ✅ | ✅ | **KEEP** |
| **10 editor** | ✅ | ✅ | ✅ | ✅ | **KEEP** |
| **05 cinematic spec** | ✅ | ○ | ○ | – | **KEEP** — §2H talking-head look now matters |
| **02 crew + hooks + swipe** | ✅ | ✅ | ✅ | ✅ | **KEEP** — S1-S7 ARE vlog/review formats |
| **03 physical performance** | – | ✅ | ✅ | ✅ | **KEEP** ⚠️ *v1 said archive — wrong.* Nev on camera = gestures are the performance |
| **07 emotion engine** | – | ✅ | ✅ | ○ | **KEEP** ⚠️ *v1 said archive — wrong.* A review's credibility is micro-expression |
| **14 avatars/voice/series** | ○ | ✅ | ✅ | ✅ | **KEEP** ⚠️ IND lives or dies on who it's for |
| **08 strategist** | ✅ | ✅ | ✅ | ✅ | **KEEP** |
| **01 spine + Thai reversal** | ○ | ○ | ○ | ✅ | **KEEP** — reframe twists are IND's edge |
| **15 launch protocol** | ✅ | ✅ | ✅ | ✅ | **KEEP** — unproven only because nothing is posted |
| **17 car cinematic prompt** | ✅ | – | – | – | **KEEP** — the one proven generator |
| **23 asset pre-production** | ✅ | ○ | – | – | **KEEP** — cheap insurance on any AI shot |
| **16 master skeleton** | ○ | ○ | ○ | ○ | **MERGE** → fold into RUNNER |
| **00 START-HERE** | – | – | – | – | **CUT** — 22 replaced it |
| **04 foley master** | – | – | – | – | **CUT** — fully superseded by 12 + 19 |
| **20 SFX list** | – | – | – | – | **→ /reference/** — a shopping list, consumed once |
| **21 BGM list** | – | – | – | – | **→ /reference/** — same |

## THE VERDICT
```
KEEP        21 files   (was going to cut 7 of these — v1 audit was scored on the wrong sample)
MERGE        1 file    16 -> RUNNER
CUT          2 files   00, 04
REFERENCE    2 files   20, 21
```
**Net: 26 → 22 live + 2 reference.** Far less pruning than v1 proposed, and that is the correct answer.

---

## ⚠️ WHAT THE AUDIT ACTUALLY EXPOSED (more useful than the cut list)

**1. The system is built for the format we're about to stop leading with.**
File 17 + 23 serve CIN. Everything for VLG/REV/IND is *unproven* — not weak, just untested.

**2. Three of four formats need ZERO credits.** The bottleneck stops being Higgsfield and becomes:
```
□ huggingface.co allowlist  → auto-subtitles.  BLOCKING for REV and IND
□ autojumpcut.py            → goes from curiosity to most-used tool
□ seat 1B Voice             → finally exercised (real Nev voice, never TTS)
□ real SFX/BGM library      → talking formats live on foley, not synthesis
```

**3. The judges finally get teeth.** J4 Local and J5 Buyer were rubber-stamps on cinematics
(no real car, no real claim). On a REAL car review they have something to actually check:
wrong grille, wrong engine note, a claim you can't back = a real fail.

**4. Bank 10 stops being trivia and becomes the roast shield.** Reviewing real units in KK means
every generation/spec/price claim is checkable by your audience.

---

## THE HONEST RANKING OF WHAT TO DO NEXT
```
1. Add huggingface.co to the allowlist        — unblocks REV + IND entirely
2. Shoot ONE car review (Recipe 7, zero cost) — tests 03, 07, 14, J4, J5, 1B, autojumpcut at once
3. Launch it through file 15                  — the loop has still never run
4. Only then: build the format->pipeline map from real evidence, not theory
```
> **v1 of this audit tried to prune a system that had only ever been tested one way.**
> Sample size of one produces confident wrong answers. That lesson matters more than the cut list.
