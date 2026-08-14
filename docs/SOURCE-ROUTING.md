# SOURCE ROUTING — hybrid: AI-generated + real footage
### Decide this at Phase 1, before anything else. It changes cost, gates and tools.
### Companion to RUNNER.md. Most videos are a MIX — route per SHOT, not per video.

---

## THE MODE SWITCH — decide first, it changes everything

| | **A · AI HERO** | **B · REAL REVIEW** | **C · REAL VLOG** | **D · HYBRID ⭐** |
|---|---|---|---|---|
| Who's on camera | AI Nev | you / a real person | you | both, by shot |
| AI makes | everything | B-roll only | inserts only | the moments that move |
| Credit cost | **high** (270cr/60s naive) | **~0** | **~0** | **low** (~145cr/60s) |
| Main risk | identity drift, "AI slop" tell | dead air, rambling | dead air | **seam mismatch** |
| Killer tool | `facecheck.py` | `autocut.py` | `autocut.py` | both |

**⭐ D is the default for you.** Real footage carries trust and costs nothing; AI covers what you
can't film — a car you don't have, a location, a cutaway, a hero shot. That's how the reference
channels actually work.

---

## PER-SHOT ROUTING TABLE

| Shot need | Source | Why |
|---|---|---|
| Nev speaking to camera (trust, opinion, verdict) | **REAL** if you have him · AI if persona-only | a real face is free and converts better |
| A car you physically have | **REAL** | free, accurate, no spec risk |
| A car you do NOT have | **AI** | the whole reason generation exists |
| Location you can't reach (auction, port, Japan) | **AI** | cheap vs travel |
| Cutaway / insert / detail (badge, dial, tyre) | **REAL** first, AI if missing | phone macro is free |
| Impossible shot (crane, drone, cross-section) | **AI** | this is where AI earns its cost |
| Title cards, price ladders, checklists | **STILLS** | ~free, and they're save-bait |
| Runtime filler between talking beats | **STILLS + zoompan** | 5% of video cost |

**The economic rule:** film everything you *can*. Generate only what you *can't*. Every shot you
film instead of generate is ~67cr back in the balance.

---

## WHAT CHANGES BY SOURCE

### AI-GENERATED shots
```
GATES     character sheet as start_image (mandatory) · facecheck.py on every seam
          named camera body + lens + T-stop · ONE motivated move · motion in frame 1
COST      preflight before spend · probe hooks at 17.5cr · 720p not 1080p
FAILURE   identity drift · unmotivated camera moves · posed frame 1 · melted detail
AUDIO     generate_audio TRUE for talking (the old "silent always" rule is dead)
```

### REAL-FOOTAGE shots
```
GATES     transcribe.py → autocut.py (fillers, retakes, pause tightening)
          pacing.py cuts/min band · dead-zone detection
COST      zero credits — iterate freely, reshoot as many times as you like
FAILURE   dead air · rambling · weak hook because you didn't plan frame 1
AUDIO     real room tone · normalise to −9 LUFS · Whisper gives word-exact captions
SEATS     03 performance + 07 emotion apply to YOU now — weight, hands with a job,
          named conflict. Same doctrine, different actor.
```

### THE HYBRID SEAM — where hybrid videos actually break
Cutting between real and AI is the #1 tell. Mitigations, in order of effect:
```
1. GRADE MATCH      colour-match the AI to your real footage, never the reverse.
                    Sample your phone's look, put it in the prompt: "muted, warm amber
                    highlights, slight 35mm grain" — then ffmpeg-match on the seam.
2. CUT ON MOTION    never cut real→AI on a static frame. Cut mid-movement; motion hides
                    the mismatch. `pacing.py` flags static stretches.
3. AUDIO CONTINUITY one continuous VO or bed ACROSS the seam. Ears bridge what eyes doubt.
4. AI GOES WIDE     use AI for wide/detail/impossible shots; keep faces real where you can.
                    Faces are where the uncanny tell lives.
5. NEVER SEAM MID-SENTENCE  cut on a sentence boundary (autocut.py gives you these).
```

---

## THE HYBRID BUILD — 60s at ~90cr

```
0-3s    AI hero shot (the car you don't have, one motivated move)      ~14cr  ← the WOW
3-18s   REAL Nev talking, phone, natural light                            0cr  ← the TRUST
18-30s  STILLS + zoompan (price ladder / checklist card)                  ~4cr  ← the VALUE
30-45s  REAL cutaways you filmed + one AI impossible shot                ~14cr
45-55s  REAL Nev, the verdict                                             0cr  ← the PAYOFF
55-60s  STILL CTA card                                                    ~2cr
        ────────────────────────────────────────────────────────────────
        ≈34cr of generation + stills. vs 270cr fully-AI.
```
**Trust from the real face, spectacle from AI, runtime from stills.** That's the architecture.

---

## PIPELINE BY SOURCE

```
REAL footage:   shoot → transcribe.py → autocut.py → edl.py → GATE → launch
AI footage:     /talyx-shotlist → ⏸approve → probe → generate → edl.py → GATE → launch
HYBRID:         plan both in ONE shot list, marking each shot [REAL] or [AI]
                → film the REAL ones first (free, and they may replace planned AI shots)
                → only then generate the gaps that remain
```
**Film first, generate second.** Filming often reveals you don't need the AI shot you planned —
and that's a direct credit saving.

## GATES THAT APPLY TO BOTH
`mastermind.py` (loudness, peak, dead air, blank frames, caption sync) · `pacing.py` (cuts/min,
dead zones, hook motion) · `rhythm.py` (beat sync) · `GATE.md` stages 2–6 · launch protocol.
