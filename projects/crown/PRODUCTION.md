# PRODUCTION DOC — Toyota Crown Crossover 2.4 RS Advance · chill coastal cinematic · Nev
### Generated from `plans/crown.py` by `planqc.py`. Do not edit by hand — edit the plan.

**20 shots · 30.00s · 720x1280 @ 30fps · car_cinematic_chill · 100 BPM · mode `std` 720p**

---

## PLATES — generate and LOOK at these first

| plate | res | cr | status | must show |
|---|---|---|---|---|
| `crown` | 4k | 4 | NOT YET BUILT - build, LOOK at it, Gavril confirms the BODY is the CROSSOVER (not Sedan, not Signia) before any video credit | Toyota Crown CROSSOVER (S16) RS Advance: raised sedan-SUV body with a coupe-like falling roofline · full-width slim LED daytime bar across the nose with a hammerhead front · body-colour upper grille and a wide dark lower intake · black wheel-arch and rocker cladding · 21-inch dark multi-spoke alloys · full-width rear light bar · CROWN wordmark across the tailgate · two-tone black roof |
| `crown_int` | 4k | 4 | NOT YET BUILT - interior geometry is a named subject too | Crown Crossover cabin: twin 12.3-inch screens - instrument cluster and a separate landscape centre display · low wide fascia · rotary drive selector · two-tone black and tan hide |
| `nev` | 4k | 0 | existing 3-angle face set, no generation needed | his head shape, hair and shoulder line ONLY - the face is deliberately never lit in this build (his pick 2026-08-05) |

---

## TIMELINE

| # | in | dur | kind | source | crop | note |
|---|---|---|---|---|---|---|
| 0 | 0.00 | 1.80 | med | `A` EVENT · out of the underpass shadow into the light | 1.00x | shadow into gold - the car comes out already moving, and silent |
| 1 | 1.80 | 1.20 | burst | `B` coastal tracking, palms strobing | 1.30x | gold on the coast road, still silent |
| 2 | 3.00 | 1.20 | burst | `C` 21-inch alloy at kerb height | 1.00x | the alloy turns, tarmac streaming, silent |
| 3 | 4.20 | 1.20 | burst | `D` cabin at golden hour, backlit driver, no face | 1.15x | his hands settle on the rim, silent, the road runs ahead |
| 4 | 5.40 | 1.80 | med | `B` coastal tracking, palms strobing | 1.00x | the coast road opens out, gold everywhere, nothing driving it |
| 5 | 7.20 | 1.20 | burst ◆ | `C` 21-inch alloy at kerb height | 1.15x | kerb line runs under the alloy at road level, low gold light |
| 6 | 8.40 | 1.20 | burst | `E` rear three-quarter, full-width light bar | 1.00x | the light bar comes on as the gold dies |
| 7 | 9.60 | 1.20 | burst | `G` wide bay, the car small in it | 1.30x | wide bay, the coast road bends away, the last gold flat on it |
| 8 | 10.80 | 1.80 | med | `F_load` EVENT · the ramp, still electric | 1.15x | the road tilts up into the ramp - still electric, still no engine |
| 9 | 12.60 | 1.20 | burst | `J` cabin at dusk, the decision | 1.00x | HIS DECISION - the silhouette commits, foot down on the ramp |
| 10 | 13.80 | 3.00 | hold | `F_wake` EVENT · the engine catches | 1.00x | THE ENGINE WAKES on the ramp because he asked for it |
| 11 | 16.80 | 1.20 | burst | `E` rear three-quarter, full-width light bar | 1.15x | the light bar climbs away from the ramp, working now |
| 12 | 18.00 | 1.20 | burst | `G` wide bay, the car small in it | 1.00x | wide - the car small, still climbing, the note carrying over the bay |
| 13 | 19.20 | 1.20 | burst | `F_wake` EVENT · the engine catches | 1.30x | over the crest the note hardens and holds, steady under load |
| 14 | 20.40 | 1.20 | burst ◆ | `E` rear three-quarter, full-width light bar | 1.30x | the light bar eases, the load falls away and it goes quiet again |
| 15 | 21.60 | 1.20 | burst | `I` parked at the seafront barrier, blue hour | 1.00x | quiet at the barrier, blue hour, nothing running |
| 16 | 22.80 | 1.20 | burst | `H` cabin at blue hour, key off | 1.30x | he sits, hand still on the rim at the barrier |
| 17 | 24.00 | 1.80 | med ◆ | `I` parked at the seafront barrier, blue hour | 1.15x | the bay from outside the barrier, the cabin still lit |
| 18 | 25.80 | 3.00 | hold | `H` cabin at blue hour, key off | 1.00x | HIS HAND KILLS IT - key off, the cabin goes dark |
| 19 | 28.80 | 1.20 | burst | `I` parked at the seafront barrier, blue hour | 1.30x | dark bay, the car parked in it, nothing running |

◆ = blend after this shot (`dissolve`, 400ms)

---

## CARDS — y=0.72 lower third, never centre

| text | shots | kind |
|---|---|---|
| **CROWN. PULLING AWAY IN SILENCE** | 0–3 | cap |
| **HE ASKS. IT WAKES.** | 9–11 | cap |
| **NEVER SOLD NEW IN MALAYSIA** | 14–16 | cap |
| **RECOND UNIT. ASK THE PRICE** | 17–19 | cta |

---

## PREVIZ — sketch-grade, never enters generation

![previz](None)

_Nev appears in D, J and H, so the sheet MUST carry the identity reference even though he is a silhouette. Not built - Gavril declined the ~2cr spend until the plan is unblocked._

**LIMIT:** a still sheet CANNOT depict shot 0 (a car crossing a light boundary while moving) or shot 10 (an engine waking). Both are judged at the PROBE.

Timeline board (real frames appear here automatically once clips exist):

![board](analysis/STORYBOARD.png)

---

## GENERATION PROMPTS — verbatim, as they will be sent

### `A` · EVENT · out of the underpass shadow into the light  ·  act: EVENT  ·  plates: crown

```
Vertical 9:16. THE EVENT SHOT - one action, over inside 1.5 seconds, motion already happening at frame zero, no settle. Static camera low at kerb height beside a coastal carriageway. The Toyota Crown Crossover from the reference image is ALREADY MOVING as the clip opens, emerging from the deep shade of a concrete underpass into full low-angle golden backlight, its full-width LED daytime bar lit, and sweeping past the lens. The transition from shade to blazing backlight happens ACROSS the car's body as it travels. The rest of the clip is the empty lit carriageway it left. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO: NO ENGINE, NO EXHAUST, NO COMBUSTION OF ANY KIND - the car is running on electric drive and is silent. No music, no voiceover, no dialogue. Only the hiss of tyres on warm tarmac, the rush of displaced air as the body passes the lens, and the change in room tone as it leaves the concrete underpass for open coastal air. Ambience: distant surf, faint.
```

### `B` · coastal tracking, palms strobing  ·  act: PAYOFF  ·  plates: crown

```
Vertical 9:16. THE SUSTAINED CRUISE - continuous motion, unbroken, no settle at the head. The Toyota Crown Crossover from the reference image driving at an easy pace along a palm-lined coastal carriageway at golden hour, tracked from a parallel vehicle, front three-quarter held steady. Palm shadows sweep rhythmically across the bodywork; the open bay and distant islands sit beyond the barrier. Camera moves smoothly with the car from first frame to last. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO: NO ENGINE, NO EXHAUST, NO COMBUSTION OF ANY KIND - the car is running on electric drive and is silent. No music, no voiceover, no dialogue. A steady, unchanging tyre hiss on open tarmac and a soft wind wash along the body for the whole clip. Ambience: open bay air and faint surf.
```

### `C` · 21-inch alloy at kerb height  ·  act: EXTERIOR  ·  plates: crown

```
Vertical 9:16. Tight tracking move at kerb height along the flank of the Toyota Crown Crossover from the reference image, holding on the 21-INCH DARK MULTI-SPOKE ALLOY turning and the black rocker cladding above it, tarmac texture streaming past underneath in the low sun. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO: NO ENGINE, NO EXHAUST, NO COMBUSTION OF ANY KIND - the car is running on electric drive and is silent. No music, no voiceover, no dialogue. Close tyre contact - tread pattern rolling on coarse tarmac, grit ticking in the tread, the note changing as the surface changes under the wheel.
```

### `D` · cabin at golden hour, backlit driver, no face  ·  act: HUMAN  ·  plates: nev, crown_int

```
Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image, shot from the passenger side. The man from the FIRST reference images is in the driver's seat but he is a PURE SILHOUETTE against a blazing golden side window - his face is NEVER lit and NEVER resolves, only the outline of his head, hair and shoulder reads. Both hands rest easily at the bottom of the steering rim. In front of him the 12.3-inch cluster shows a hybrid power meter, no rev counter. Backlit, high contrast, the sun doing all the work. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO: NO ENGINE, NO EXHAUST, NO COMBUSTION OF ANY KIND - the car is running on electric drive and is silent. No music, no voiceover, no dialogue. The cabin drop-out: outside noise distant and damped, the cabin still. Faint seat-cloth and leather movement as his hands settle on the rim, one quiet breath, a muted tyre rumble through the floor, a faint high electric whine rising with speed.
```

### `E` · rear three-quarter, full-width light bar  ·  act: EXTERIOR  ·  plates: crown

```
Vertical 9:16. Rear three-quarter of the Toyota Crown Crossover from the reference image on the coastal carriageway at dusk, slow arc around the rear corner. The FULL-WIDTH REAR LIGHT BAR is lit and is the brightest thing in frame; the CROWN wordmark across the tailgate reads clearly; the sky behind has gone amber to violet. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO, TWO STATES: for the FIRST HALF of the clip there is NO ENGINE, NO EXHAUST, NO COMBUSTION - only tyre note and wind. In the SECOND HALF a petrol engine is heard receding into the distance, backing off and handing back to tyre roll. No music, no voiceover, no dialogue.
```

### `G` · wide bay, the car small in it  ·  act: EXTERIOR  ·  plates: crown

```
Vertical 9:16. Wide static high-angle looking down over the bay at dusk, the coastal carriageway curving through the lower third of frame AND RISING TO A CREST at the far side, the Toyota Crown Crossover from the reference image SMALL in the frame travelling along it. Offshore island ridgelines sit low in the haze; the last sun lies flat across the water. The car is a moving detail inside a landscape, not the subject. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO, TWO STATES: heard from far away across open water - wind and distant surf dominate throughout. In the FIRST HALF no combustion is present at all. In the SECOND HALF a petrol engine is faintly audible at long distance, thin and small inside the landscape. No music, no voiceover, no dialogue.
```

### `F_load` · EVENT · the ramp, still electric  ·  act: EVENT  ·  plates: crown

```
Vertical 9:16. The Toyota Crown Crossover from the reference image approaching and starting a rising coastal ramp at dusk, tracked from a parallel vehicle, front three-quarter. The road visibly tilts upward through the shot and the car keeps its easy pace onto it - no acceleration yet, no drama, the body level. This clip is the SETUP for the shot that follows and must not contain the event itself. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO: NO ENGINE, NO EXHAUST, NO COMBUSTION OF ANY KIND - the car is running on electric drive and is silent. No music, no voiceover, no dialogue. Tyre note and wind only, with a faint electric whine holding steady. The quiet immediately before something happens.
```

### `J` · cabin at dusk, the decision  ·  act: HUMAN  ·  plates: nev, crown_int

```
Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image at dusk, shot from the passenger side, tight. The man from the FIRST reference images is a PURE SILHOUETTE against the violet windscreen - his face is NEVER lit and NEVER resolves. He is still for a beat, then his forearm and shoulder drop and set as he commits weight through his right foot, and the 12.3-inch cluster's power meter needle swings hard across into its power band. HIS MOVEMENT COMES FIRST, the meter answers it. Nothing else in frame moves. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO: near silence - the cabin drop-out at its deepest, only faint cloth and a thin electric whine. In the last third the whine begins to rise. NO PETROL ENGINE YET - it must not have started inside this clip. No music, no voiceover, no dialogue.
```

### `F_wake` · EVENT · the engine catches  ·  act: EVENT  ·  plates: crown

```
Vertical 9:16. THE HERO. The Toyota Crown Crossover from the reference image climbing the rising coastal ramp at dusk, tracked from a parallel vehicle in front three-quarter. THE CLIP OPENS STILL SILENT AND STILL ON ELECTRIC DRIVE for the first half-second - then the petrol engine CATCHES and the car takes load: the nose lifts, the body settles back on its springs, the pace hardens decisively but without drama, and heat shimmer rises off the rear. THE TRANSITION FROM SILENT TO RUNNING HAPPENS ON CAMERA, inside this clip. Unhurried but unmistakably WORKING. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO - THIS IS THE ONLY COMBUSTION SOUND IN THE ENTIRE FILM: the clip opens in near silence with tyre roll and wind alone, then the petrol engine CATCHES - a brief crank, the four-cylinder fires, and the note rises and hardens under load as the ramp steepens, with turbo spool behind it. The transition from silent to running is the loudest event in the clip. Ambience: open coastal air. No music, no voiceover, no dialogue.
```

### `H` · cabin at blue hour, key off  ·  act: HUMAN  ·  plates: nev, crown_int

```
Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image at blue hour, parked and still, shot from the passenger side. The man from the FIRST reference images sits in the driver's seat as a PURE SILHOUETTE against the pale blue-grey sky through the windscreen - his face is NEVER lit and NEVER resolves. His hand leaves the steering rim, reaches, and PRESSES the start-stop button; the 12.3-inch cluster and the fascia lighting die out in the same movement. HIS ACTION CAUSES THE DARKNESS - the lights do not simply fade on their own. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO: a parked, still cabin. Seat-cloth and leather as he moves. The car's electronics power down - a single soft shutdown chime, then the last relay settles and the cabin goes completely quiet. Outside, faint water and wind, far away and damped. NO ENGINE, NO IDLE. No music, no voiceover, no dialogue.
```

### `I` · parked at the seafront barrier, blue hour  ·  act: EXTERIOR  ·  plates: crown

```
Vertical 9:16. The Toyota Crown Crossover from the reference image parked and stationary at a seafront barrier at blue hour, side-on and slightly behind, the flat seafront promenade and the bay beyond it going dim. Very slow drift of the camera; the water moves, the car does not. The full-width rear light bar and the cabin glow are the only lit things; the sky is deep blue with the last band of orange on the horizon. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke. AUDIO: a stopped car - nothing mechanical, nothing running. Only water against the seawall and a low steady wind. The quietest sound in the whole piece. NO ENGINE, NO IDLE. No music, no voiceover, no dialogue.
```

---

## THE EDIT — what the engine will do, with computed times

_times below are PLANNED; blends compress them - the engine re-times cards and declares ACTUAL cut boundaries after building._

**Cut grid** — every boundary on the 150 BPM beat (0.400s), frame-exact (`-frames:v`), each shot centred on a measured action peak, exposure matched on rendered segments BEFORE blending.

| after shot | t (planned) | treatment |
|---|---|---|
| 5 (kerb line runs under the alloy at road level, low gold light) | 8.40s | dissolve 400ms |
| 14 (the light bar eases, the load falls away and it goes quiet again) | 21.60s | dissolve 400ms |
| 17 (the bay from outside the barrier, the cabin still lit) | 25.80s | dissolve 400ms |

All other cuts HARD (33-67ms). Blends 3/19 = 15% (profile 6-33%).

**Sound** — synthesized drift-phonk bed at 150 BPM, first transient trimmed to t=0 (phase, not just tempo). SFX layer at +13.5dB with the bed SIDECHAIN-DUCKING under it; every whoosh LEADS its cut by 220ms and resolves ON it.

**Diegetic** — every shot lays its OWN clip audio (generated and paid for) on the actual timeline, plan-gained. Foreground (>=-6dB): shots [0, 1, 4, 8, 10, 13]. Bed HARD-ducks during shots [10]. Hero: THE PETROL ENGINE CATCHING on the ramp (shot 10, 13.80s), CAUSED by his commit in shot 9. ONE hero sound per video (file 04, law 4).

| t (planned) | cut entering | sound |
|---|---|---|
| 1.80s | shot 1 · gold on the coast road, still silent | whoosh |
| 3.00s | shot 2 · the alloy turns, tarmac streaming, silent | whoosh |
| 4.20s | shot 3 · his hands settle on the rim, silent, the road runs ahead | whoosh |
| 5.40s | shot 4 · the coast road opens out, gold everywhere, nothing driving it | whoosh |
| 7.20s | shot 5 · kerb line runs under the alloy at road level, low gold light | whoosh |
| 8.40s | shot 6 · the light bar comes on as the gold dies | whoosh |
| 9.60s | shot 7 · wide bay, the coast road bends away, the last gold flat on it | whoosh |
| 10.80s | shot 8 · the road tilts up into the ramp - still electric, still no engine | whoosh |
| 12.60s | shot 9 · HIS DECISION - the silhouette commits, foot down on the ramp | whoosh |
| 13.80s | shot 10 · THE ENGINE WAKES on the ramp because he asked for it | IMPACT (section) |
| 16.80s | shot 11 · the light bar climbs away from the ramp, working now | whoosh |
| 18.00s | shot 12 · wide - the car small, still climbing, the note carrying over the bay | whoosh |
| 19.20s | shot 13 · over the crest the note hardens and holds, steady under load | whoosh |
| 20.40s | shot 14 · the light bar eases, the load falls away and it goes quiet again | whoosh |
| 21.60s | shot 15 · quiet at the barrier, blue hour, nothing running | whoosh |
| 22.80s | shot 16 · he sits, hand still on the rim at the barrier | whoosh |
| 24.00s | shot 17 · the bay from outside the barrier, the cabin still lit | whoosh |
| 25.80s | shot 18 · HIS HAND KILLS IT - key off, the cabin goes dark | whoosh |
| 28.80s | shot 19 · dark bay, the car parked in it, nothing running | whoosh |

**Captions** — cards.py PNGs on desktop (drawtext fallback flagged loudly), lower third y=0.72, re-timed to actual duration:

| card | shots | planned window |
|---|---|---|
| **CROWN. PULLING AWAY IN SILENCE** (cap) | 0-3 | 0.00-5.40s |
| **HE ASKS. IT WAKES.** (cap) | 9-11 | 12.60-18.00s |
| **NEVER SOLD NEW IN MALAYSIA** (cap) | 14-16 | 20.40-24.00s |
| **RECOND UNIT. ASK THE PRICE** (cta) | 17-19 | 24.00-30.00s |

**Grade** — saturation 1.1 ONLY (never double-grade; prompts already carry the night look), measured toward black_point 6.0 / saturation 80.0. Mix: bed +12dB, limiter 0.76 level=disabled, target -7..-9 LUFS. Output written atomically.

**Then the gates:** clipqc per clip -> engine build -> verify (10 checks, freshness first) -> JUDGES (kill-boring) -> Gavril.

---

## COST

- probe first: plates + shot `A` = **30.5 cr**, then LOOK
- remaining 10 clips = **225.0 cr**
- **total 255.5 cr**
