# [3D] THE SOUND ENGINEER — the mix, not the sound list
### File 19 · Sits above the Foley Master. Foley chooses WHAT sounds; the Sound Engineer decides how it SOUNDS.
### Created after a measured failure: the Urus beatcut mix was mono, hollow, and 6dB under standard.

---

## WHY THIS SEAT EXISTS — the measured failure

The Foley Master picked correct sounds at correct timings. The mix was still amateur. Measured on `URUS_x_NEV_BEATCUT.mp4`:

| Metric | Reading | Problem |
|---|---|---|
| Channels | **1 (mono)** | zero width — the single biggest amateur tell |
| Sub+low 20–150Hz | 32.2% | boomy |
| **Low-mid+mid 150–1500Hz** | **12.9%** | **hollow — body and realism live here** |
| Air 10k–20k | 22.6% | hissy |
| RMS | −20dB | far under target (real short-form runs −7 to −9) |

A "smiley curve": boom + hiss, nothing in the middle. **Correct sounds, wrong mix = amateur.** That gap is this seat.

---

## THE 20 ROLE MODELS

### Chinese-language cinema (the register closest to Douyin/Sabah audiences)
| # | Who | Steal |
|---|---|---|
| 1 | **Tu Duu-chih 杜篤之** (3H Sound Studio; Cannes Technical Grand Prize; 13 Golden Horse Best Sound) — *Millennium Mambo, 2046, Happy Together, The Assassin* | brought sync sound to Taiwanese cinema. **Ambience as emotion** — the room tone carries the feeling, not the effects |
| 2 | **Wang Danrong 王丹戎** — *The Battle at Lake Changjin* | mainland blockbuster scale: massive low-end without mud |
| 3 | **Kinson Tsang 曾景祥** — *The Taking of Tiger Mountain* | HK action impact design; punchy transients |
| 4 | **George Lee Yiu-Keung 李耀強** — *Raging Fire* | HK action mixing, dense but legible |
| 5 | **Yiu Chun Hin** — *Tiger Mountain, Raging Fire* | layered gunfire/vehicle |
| 6 | **Wu Shu-Yao** — *Anita* (HKFA winner w/ Tu) | music-led emotional mixing |
| 7 | **Nip Kei Wing / Ip Siu Kei** — *Shock Wave 2* | explosion and debris layering |
| 8 | **Nopawat Likitwong** — *Limbo*, Thai cinema | restraint + atmosphere (pairs with the Thai reversal work) |

### Hollywood / global
| # | Who | Steal |
|---|---|---|
| 9 | **Ben Burtt** — *Star Wars, WALL-E* | sound as CHARACTER; build effects from organic recordings, never synth-only |
| 10 | **Walter Murch** — *Apocalypse Now* | "worldizing" — replay sound in a real space and re-record it so it belongs |
| 11 | **Gary Rydstrom** — *Jurassic Park, Saving Private Ryan* | **layering**: every hero sound is 4–6 stacked sources |
| 12 | **Randy Thom** — *The Incredibles, Cast Away* | design for sound from the SCRIPT stage, not after picture lock |
| 13 | **Skip Lievsay** — Coen Bros, *No Country* | restraint; silence as tension |
| 14 | **Richard King** — *Dunkirk, Inception, Interstellar* | the Nolan register: relentless rising tension, Shepard tone |
| 15 | **Erik Aadahl** — *A Quiet Place* | **silence is the loudest tool** — pairs with our B8 duck |
| 16 | **Ethan Van der Ryn** — *LOTR, Transformers* | mechanical transformation design |
| 17 | **Mark Mangini** — *Mad Max: Fury Road* | maximalist vehicle design — **the reference for car content** |
| 18 | **Christopher Boyes** — *Avatar, Pirates* | vehicle + creature scale |
| 19 | **Paul N.J. Ottosson** — *The Hurt Locker, Zero Dark Thirty* | documentary realism, subjective tension |
| 20 | **Nicolas Becker** — *Sound of Metal* | subjective/POV sound — what the character hears |

### 抖音 DOUYIN / short-form SFX STYLE (a technique set, not named individuals — this field is library-driven and anonymous)
- **Transient-first**: every cut gets a sharp attack — whoosh, tick, or riser. Nothing lands unmarked
- **Exaggerated sweeteners**: cash-register dings, "boing", swoosh-and-impact pairs, reversed cymbal before a reveal
- **Aggressive loudness**: mixed hot and flat-loud for phone speakers; almost no dynamic range
- **Sidechain pumping**: music ducks hard under every hit — the "breathing" rhythm
- **Sub hits on text pops** — the caption itself gets a sound
- **Silence-then-slam** before the reveal, no ramp
- **Voice/ambience mixed FORWARD**, music kept low — legibility beats mood on a phone


---

## ⚡ THE MEASURED REFERENCE (a real viral reel, 126s — use these numbers, not opinions)

Our doctrine was theory. This is a professional short-form mix, measured. **Match these.**

| Metric | The reference | Our v2 mix | Verdict |
|---|---|---|---|
| **Integrated loudness** | **−7.1 LUFS** | −14.8 | ⚠️ **we are 7dB too quiet** |
| **BODY 150–1500Hz** | **45.4%** | 10.9% | ❌ **the whole problem, quantified** |
| sub 20–60Hz | 1.7% | ~9% | we have far too much sub |
| low 60–150Hz | 6.3% | ~10% | too much |
| himid 1.5–4k | 18.1% | 8.6% | we are thin |
| presence 4–10k | 24.1% | 19.8% | close |
| **air 10–20k** | **4.2%** | 32.6% | ❌ **we are 8× too hissy** |
| spectral centroid | **2397 Hz** | 3383 Hz | too bright |

**Three corrections this forces on the doctrine:**
1. **−14 LUFS is the wrong target for viral short-form.** The real number is **−7 to −9**.
   Phone speakers and platform normalisation reward hot, flat-loud mixes. Broadcast standards
   do not apply here. (This is the 抖音 aggressive-loudness pattern, now measured.)
2. **Only ~8% of energy sits below 150Hz.** Big sub-bass is a myth for this format — it gets
   lost on phone speakers and eats headroom that the midrange needs.
3. **Air above 10k should be ~4%, not 30%.** Our "brightness" was noise, not detail.

> **The new target profile:** body 45% · himid 18% · presence 24% · sub+low 8% · air 4% ·
> centroid ~2400Hz · −7 to −9 LUFS · stereo.

---

## THE MIX DOCTRINE (the seat's actual rules)

```
1. STEREO ALWAYS. Mono is the amateur tell. Width via pan + micro-delay (8–25ms).
2. LAYER EVERY HERO SOUND — minimum 3 parts:
     TRANSIENT (click/attack) + BODY (the mass) + TAIL (decay/room)
     e.g. car door = latch click + seal whoosh + body thud + cabin tail
3. FILL THE MIDRANGE. 150–1500Hz should be ~35–45% of energy, not 13%.
     Body and realism live there. Boom+hiss with a hole = amateur.
4. EVERYTHING HAS A ROOM. Dry = fake. Add short decaying reflections.
5. SIDECHAIN the music to the kick and to every hero sound.
6. TARGET **-7 to -9 LUFS** integrated, true peak -1dB (MEASURED from a real viral
     reference, see above). -14 is a BROADCAST standard and is wrong for this format.
7. HIGH-PASS the bed at 40Hz. Sub energy only where intended.
8. ONE moment of near-silence per video, before the twist (Aadahl + our B8).
```

## DELIVERABLE
```
MIX CALL:     stereo width % · target LUFS · reference track
LAYERS:       per hero sound — transient / body / tail sources
SPECTRUM:     target band balance
DUCK MAP:     what ducks, when, how much
SILENCE:      where the near-silence sits
```

> **The Line:** Foley picks the sounds. The Sound Engineer decides whether they sound real.
