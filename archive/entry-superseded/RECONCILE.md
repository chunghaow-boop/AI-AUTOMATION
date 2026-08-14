# RECONCILE — one system out of two
### Written 2026-08-03 after the first two-way sync. The desktop docs (built 14 Jul) and
### the laptop engine (built 30 Jul–3 Aug) are PARENT and CHILD, not rivals — CLAUDE.md's
### contract IS file 18, the hard rules match, and both independently found the same gap:
### the desktop calls it "the Judges catch BORING"; the laptop calls it "conformance is
### not interest". Same scar, two vocabularies. This file makes them one.

---

## WHO OWNS WHAT — single source of truth per concern

| concern | OWNER (canonical) | the other side's role |
|---|---|---|
| Doctrine: beats, roles, foley, camera, emotion | **files 01–21** (root) | talyx encodes the mechanical subset |
| Current state | **22-HANDOVER.md** (desktop) + RESUME (laptop) → merge into 22 | keep 22's 200-line cap |
| The contract | **18-agent-contract.md** = CLAUDE.md TITLE CONTRACT | identical intent; CLAUDE.md adds the readback step — port it back to 18 |
| Plan-time gate | **planqc.py** (18 checks) | file 01's Four Gates map onto CONTENT block + CARDS (see below) |
| Per-clip gate | **clipqc.py** | file 06's Quality Advisor, mechanised |
| Cut gate | **verify.py** (10 checks) | file 26's Part 1 hard gates, mechanised |
| Reception / "does anyone care" | **file 06 Judges + file 25 debate** — LLM judgement | NOT mechanisable; runs after verify, before Gavril |
| One number per video | **26-master-scorecard.md** | verify feeds its hard-gate section |
| Editing mechanics | **engine.py** | files 10/11 are its doctrine; bank entries → future plan fields |
| Sound doctrine | **files 04/19/12** | sfxgen + engine sidechain implement it; audio targets AGREE (-7..-9 LUFS both sides) |
| Persona identity | **assets/nev/face/** (3-angle set) | 22's Higgsfield ref IDs may be EXPIRED — re-upload from face/ |

**The merged flow (both vocabularies):**

```
TITLE → SEAT 0 Strategist = READBACK (2-3 options, his pick)
      → Four Gates (Hook·Value·Twist·CTA) = CONTENT block + CARDS   [planqc 18]
      → board → ⏸ approve → probe → generate → clipqc [per clip]
      → engine build → verify [10] → JUDGES (file 06, LLM, kill-boring) → ⏸ Gavril → post
```

---

## CONFLICTS — verdicts, with reasons

**1. Multi-shot single generation (file 17) vs coverage model (8 clips). BOTH LIVE, as modes.**
File 17: one 15s multi-shot prompt, 9 shots, dissolves baked in — 720p = **67.5cr**, proven
(log #26). Coverage: 8×5s = **180cr**. File 17 is 2.7× cheaper — but its dissolves are baked
where the model put them, so it can never hit the measured phonk pillar (44.7 cuts/min, most
cuts HARD 33–67ms, blends rare). Verdict: **plans declare `GEN_MODE`** —
`"multishot"` for dissolve-led golden-hour films (17's aesthetic), `"coverage"` for beat-cut
phonk (the pillar). Wrong tool for the wrong pillar is how 67.5cr becomes unusable.

**2. "silent always" (22) vs `generate_audio: true` (CLAUDE.md).** CLAUDE.md wins — it is
newer and explicit that the old rule is obsolete for talking formats. Cinematics stay silent
(the bed replaces everything). 22 updated.

**3. Stale facts in 22-HANDOVER:** balance 2,073.17 (07-24) → **5,852.16 measured 08-01**,
and spending happened since — MEASURE at next session start. Higgsfield KOL ref IDs are
probably expired; the durable identity is `assets/nev/face/` in git. 22 updated.

**4. "Zero appearance words in prompts" (file 00, rule 1) vs our detailed must-show prompts.**
Scope difference, not conflict: the rule is for the PERSONA (realism + moderation shield);
cars need their signatures described — that is how the wrong swan-neck got caught. Rule
restated: **persona = references only; product = describe the geometry.**

**5. Duplication: 28 numbered docs byte-identical in root and `system/`.** Root is canonical
(RUNNER references root names). `system/` duplicates deleted; `system/tools-legacy/` kept.

---

## WHAT EACH SIDE GAINS

Laptop engine gains from desktop docs: the **Judges layer** (the missing reception gate),
Four-Gate idea vocabulary, the Hands Protocol + weight doctrine for Nev shots, file 23's
asset pre-production (four-view/nine-grid) — adopt for the Supra rebuild, file 17 as a
cheap second GEN_MODE, and the 25-debate protocol for contested calls.

Desktop docs gain from laptop engine: planqc/clipqc/verify as the mechanical enforcement
of files 01/06/26, the generic engine replacing per-car builds, the probe discipline,
relational checks (crop drift, repeat framing), and PUSH/PULL sync replacing zip rituals.

## OPEN (needs Gavril)
- Post something. Both handovers, all three weeks, same #1 gap, still true.
- Judges are an LLM step: run them as a fixed prompt over the verified cut (file 06 §format)
  each build, before final review. Adopt as standing step?
