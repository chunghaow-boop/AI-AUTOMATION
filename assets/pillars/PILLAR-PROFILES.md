# PILLAR PROFILES — the master reference
### Measured from 23 reference videos he selected. Snapshot 2026-07-30, expires 2026-09-28.
### **When lost, start here.** Machine-readable twin: `PILLAR-PROFILES.json`

---

## ALL FOUR PILLARS

| pillar | n | duration | median shot | cuts/min | blended | black pt | saturation |
|---|---|---|---|---|---|---|---|
| **car_cinematic** | 5 | 10–22s | **0.77s** | 44.7 | 20% | 2.0 | 91.5 |
| **travel_vlog** | 6 | 16–29s | **1.13s** | 40.3 | 0% | 10.0 | 74.5 |
| **car_review** | 7 | 58–107s | **3.60s** | 14.3 | 16% | 8.0 | 52.9 |
| **industry** | 5 | 35–181s | **2.52s** | 17.9 | 0% | 3.0 | 81.3 |

---

## THE TAXONOMY I HAD WRONG

I treated all four as one craft with different footage. They are **two families**:

```
SHORT-FORM, MUSIC-LED           LONG-FORM, SPEECH-LED
  car_cinematic  10-22s           car_review   58-107s
  travel_vlog    16-29s           industry     35-181s
  sub-bass 60-92%                 speech 63-99% of the signal
  no voice                        speech IS the signal
  cut to the beat                 cut to the sentence
  shots 0.77-1.13s                shots 2.52-3.60s
```

**Shots are 3–5× longer in the speech-led pillars.** A car cinematic and a car review share
almost nothing — not length, not sound, not edit grammar.

---

## 1 · CAR CINEMATIC (n=5) — short, music-led

| metric | median | range |
|---|---|---|
| median shot | **0.77s** | 0.70 – 4.50 |
| cuts/min | 44.7 | 11.5 – 58.3 |
| blended cuts | **20%** | 6 – 33 |
| blend width | **240–560ms** | |
| BPM | 100.5 | 78 – **163** |
| sub-bass share | **60–92%** | |
| black point / saturation | 2.0 / 91.5 | crushed, punchy |

**Frame-level correction.** My first pass reported 27% blended from a heuristic. Studying
every cut frame-by-frame gives the real picture:

```
azmiedtz    1/16 blended (6%)   — 14 hard cuts at 33-67ms
d2_shots    5/15 blended (33%)  — blends 240-560ms wide
```

**Most cuts are HARD and instantaneous (33–67ms).** Blends are rare, deliberate and *wide* —
used as section punctuation, not as a default transition. Chasing "27% blended" would have
been wrong.

**Burst pattern.** Cuts arrive in clusters one beat apart, then hold:
`8.27 / 8.63 / 9.03s` and `14.80 / 15.20 / 15.60s` — that's **0.40s apart at 145.8 BPM,
exactly one beat.** The cut rate is not uniform; it bursts and rests.

- Fastest shot: **0.28s**
- Captions: **lyric-synced** — 1–2 words, huge, centre-frame, on the beat
- Lighting: **night, hard artificial, the car emits light** (headlights, taillights, glowing
  brakes, cluster). Not dusk, not a studio void.
- Shot mix ≈ 30% exterior · 15% wheel/brake · 15% light macro · **25% interior** · 10% badge · 5% human

## 2 · TRAVEL VLOG (n=6) — short, music-led

| metric | median | range |
|---|---|---|
| median shot | **1.13s** | 0.60 – 2.51 |
| cuts/min | 40.3 | 18.5 – 63.9 |
| blended cuts | **0%** | 0 – 28 |
| BPM | 104.6 | 83 – 176 |
| black point / saturation | **10.0 / 74.5** | lifted, flatter |

**Five of six use ZERO blended transitions.** Hard cuts only. Energy comes from cut rate and
content. The grade is the *inverse* of car cinematic — open blacks, lower saturation.

Fastest shot seen: **0.03s**.

## 3 · CAR REVIEW (n=7) — long, speech-led

| metric | median | range |
|---|---|---|
| duration | ~80s | 58 – 107 |
| median shot | **3.60s** | 2.35 – 7.30 |
| cuts/min | 14.3 | 5.0 – 22.5 |
| blended | 16% | 0 – 70 |
| **speech share** | **81–99%** | |
| body band (150–1500Hz) | 72–97% | |
| sub-bass | 0–12% | |

Music is a bed under speech, not the driver. Cut to sentence boundaries, not a beat grid.
Wide spread on cut rate (5–22/min) suggests two sub-styles: talking-head vs b-roll-led.

## 4 · INDUSTRY VALUE (n=5) — long, speech-led

| metric | median | range |
|---|---|---|
| duration | ~62s | 35 – **181** |
| median shot | **2.52s** | 1.60 – 9.95 |
| cuts/min | 17.9 | 5.0 – 23.2 |
| blended | 0% | 0 – 17 |
| speech share | 63–96% | |
| sub-bass | 1–33% | |

Longest format. One reference at 63% speech / 33% sub is a music-led variant — worth asking
whether that belongs here.

---

## WHERE OUR OUTPUT SITS

| | target | ours | gap |
|---|---|---|---|
| car cinematic — median shot | **0.77s** | 2.00s | **2.6× too slow** |
| car cinematic — blended | 20% | **0%** | no transitions at all |
| car cinematic — sub-bass | **60–92%** | 48% | not bass-heavy enough |
| travel vlog — median shot | **1.13s** | ~2.00s | **~2× too slow** |
| travel vlog — blended | 0% | 0% | correct |

**The most consistent failure across both short-form pillars: our shots are 2–3× too long.**

---

## CORRECTIONS TO MY EARLIER ASSUMPTIONS

1. **"body ~45%, air ~4%"** (file 19) came from a *viral reel* and I applied it to a car edit.
   Car cinematic runs **60–92% sub-bass**. That target is pillar-specific and was misapplied.
2. **My phonk build** measured sub 30% / body 42% — **still not bass-heavy enough.**
3. **"27% blended"** was my own over-read. Frame-level says **20% median, and mostly hard
   cuts with rare wide blends.**
4. **Transitions are not universal**: 20% for car cinematic, **0% for vlog and industry.**
5. **The grade is not universal**: car crushes (2.0 / 91.5), vlog lifts (10.0 / 74.5).
6. **Cut rate is not uniform** — it bursts on the beat, then rests.

---

## CAVEATS — do not over-trust

- n = 5, 6, 7, 5. Medians are indicative; **ranges matter as much**, and several are very wide
  (car_review cuts/min spans 5.0–22.5).
- All re-downloaded via snaptik/ssstik, which re-encode. **LUFS and air-band figures are
  unreliable.** Cut timing, shot length, grade and relative band balance survive; absolute
  loudness does not.
- Long clips (>25s) analysed with frame-stride decimation — cut resolution ~0.12–0.2s.
- Blend detection on the long pillars is still the heuristic, not the frame-level study.
  Only car_cinematic has been verified frame-by-frame.
- One vlog reference (`7178823736408280325`) is an outlier on every axis.

---

## FILES

```
assets/pillars/PILLAR-PROFILES.md     <- start here
assets/pillars/PILLAR-PROFILES.json   <- the gate reads this
assets/pillars/<pillar>/refs/         reference videos + ANALYSIS.md
work/ledgers/knowledge.json           researched lessons, dated, expire at 45 days
work/ledgers/style_ledger.json        19 of his critiques
```
