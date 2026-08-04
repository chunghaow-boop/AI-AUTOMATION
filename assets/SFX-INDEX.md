# SFX + BGM INDEX — beat-type → sound
### 74 files, 100% synthesised (`tools/sfxgen.py`). No licence, no attribution, no takedown risk.
### Regenerate any time: `python3 tools/sfxgen.py --out assets`
### ⚠️ Downloads were BLOCKED: pixabay · mixkit · freesound · archive.org · freepd all 403 at
### the sandbox proxy (verified 2026-07-27). These are synthesised, not scraped.

## THE CHEAT SHEET — beat type → which file
| Beat in the edit | Use | Why |
|---|---|---|
| **Hard cut between shots** | `transition/whoosh_up` | the workhorse. 3 variations, alternate them |
| **Reveal / the twist lands** | `impact/impact_hit` + `impact/sub_drop` | body + weight under the moment |
| **Build INTO the twist** | `transition/riser` (2.0s) | start 2s before the cut |
| **Energy drop after a peak** | `transition/downlifter` | the comedown |
| **Text/caption pops on** | `ui/pop` or `ui/tick` | keep it small — this is punctuation |
| **Checklist item appears** | `ui/click` then `ui/ui_confirm` on the last one | the Artefact Drop rhythm |
| **Price / number reveal** | `ui/cash_register` | only once per video, it's loud |
| **Photo / spec card snap** | `ui/camera_shutter` | |
| **Page / section change** | `ui/page_turn` + `transition/swell` | |
| **Car starts / engine beat** | `car/engine_rev` | |
| **Getting in / out of the car** | `car/door_close` | |
| **Speed / aggression** | `car/tyre_screech` | sparingly — it reads as clickbait if overused |
| **Glitch / pattern interrupt** | `transition/glitch` | the ~30s attention reset |
| **Section end / chapter close** | `impact/stinger` or `transition/reverse_cymbal` | |
| **Under a held emotional beat** | `bgm/utility-beds/drone_tension` | duck it under the VO |

## RULES (from `system/19-sound-engineer.md`, measured)
```
Target mix: -7 to -9 LUFS integrated · true peak < -1 dBFS
Body 150-1500Hz ~45% · sub <150Hz ~8% · air >10k ~4% · centroid ~2400Hz
SFX sit 8-12 dB under the VO. If you notice the SFX, it is too loud.
ONE hero sound per video. Everything else is punctuation.
Place on the TRANSIENT, not near it — rhythm.py measures the ms deviation.
```

## FOLDERS
```
sfx/transition/  8 sounds × 3 variations   whoosh up/down/long · riser · downlifter ·
                                            reverse_cymbal · glitch · swell
sfx/impact/      4 × 3                      impact_hit · thud · sub_drop · stinger
sfx/ui/          8 × 3                      click · tick · pop · confirm · error ·
                                            page_turn · cash_register · camera_shutter
sfx/car/         3 × 3                      engine_rev · door_close · tyre_screech
bgm/utility-beds/ 5                         pulse 90/100/120/128 BPM · drone_tension
```

## ⚠️ ON THE BEDS — read this
`utility-beds` are **BPM grids, not music.** They exist so `rhythm.py` has a known tempo to
quantise cuts against while you build and test. Verified: `pulse_120bpm.wav` reads as **120.2 BPM**.

**Real music still needs sourcing by you.** Melody and performance don't synthesise
convincingly. Options, ranked:
1. **Higgsfield `generate_audio`** — you already pay for it; can produce a bed per video
2. **TikTok Commercial Music Library** — `tiktok_music_trending` (needs the account connected);
   trending + cleared for commercial use, which is the licensing-safe path
3. Download CC0 from Pixabay/Mixkit **on your machine** and drop into `assets/bgm/`

## HOW A SOUND GETS USED
```bash
python3 tools/rhythm.py final.mp4 --bed assets/bgm/utility-beds/pulse_120bpm.wav --cuts
# -> BPM + which cuts miss the grid, in milliseconds
```

---

# RELEVANCE FILTER — what was taken and what was rejected
Mixkit has 40+ SFX categories. These were selected **against your three formats**, not scraped wholesale.

## ✅ TAKEN — and the beat each one serves
| Category | Serves | Format |
|---|---|---|
| **car** | engine, doors, indicators, driving | ⭐ car review — your niche |
| **money** | price reveals, "RM50k gets you THIS" | ⭐ car review + industry value |
| whoosh · swoosh · transition | every hard cut | all three |
| riser · glitch | build into the twist · the 30s pattern interrupt | all three |
| impact · hit · punch | the reveal lands, the verdict | all three |
| click · pop · interface · notification | caption pops, checklist ticks | ⭐ the Artefact Drop |
| camera | spec-card snap, photo insert | car review |
| bell · page · logo | section change, series title card | all three |
| tech · drum · cinematic | branding, energy, hero moments | industry value + hero |
| **ambience** | garage / street / lot room tone under B-roll | vlog + review |
| **machine** | workshop, tools, lifts | car review |
| **wind** | outdoor, driving, open-lot | vlog |
| **error · alarm** | warning content — "don't buy this one" | ⭐ recond-truth pillar |
| **typing** | data on screen, research beats | industry value |

## ❌ REJECTED — and why
`magic` `horror` `explosion` `robot` `siren` `footstep` `wood` `scratch` `game` `sport` `water`
`applause` — wrong register for a car channel. Fantasy/gaming SFX on a recond review reads as
amateur and undercuts the trust the whole channel runs on.

## BGM GENRES TAKEN — mapped to your pillars
| Genre | Pillar |
|---|---|
| hip-hop · rock · funk · energetic | car review · JDM Dreamer avatar |
| electronic · technology · trailer | hero / cinematic |
| corporate · documentary | ⭐ industry value |
| chill · lo-fi · upbeat · pop | ⭐ vlog |
| ambient | tension beds, held emotional beats |

**Rule from file 19:** one bed per video, ducked 8–12dB under the VO. If you notice the music,
it is too loud.
