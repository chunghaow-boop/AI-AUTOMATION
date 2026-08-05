# PRODUCTION DOC — Toyota Crown Crossover 2.4 RS Advance · chill coastal cinematic · Nev
### Generated from `plans/crown.py` by `planqc.py`. Do not edit by hand — edit the plan.

**20 shots · 30.00s · 720x1280 @ 30fps · car_cinematic_chill · 100 BPM · mode `std` 720p**

---

## PLATES — generate and LOOK at these first

| plate | res | cr | status | must show |
|---|---|---|---|---|
| `crown` | 4k | 4 | NOT YET BUILT - build, LOOK at it, confirm the body is the CROSSOVER (not the Sedan, not the Signia) before any video credit | Toyota Crown CROSSOVER (S16) RS Advance: raised sedan-SUV body with a coupe-like falling roofline · full-width slim LED daytime bar across the nose with a hammerhead front · body-colour upper grille and a wide dark lower intake · black wheel-arch and rocker cladding · 21-inch dark multi-spoke alloys · full-width rear light bar · CROWN wordmark across the tailgate · two-tone black roof |
| `crown_int` | 4k | 4 | NOT YET BUILT - interior geometry is a named subject too | Crown Crossover cabin: twin 12.3-inch screens - instrument cluster and a separate landscape centre display · low wide fascia · rotary drive selector · two-tone black and tan hide |
| `nev` | 4k | 0 | existing 3-angle face set, no generation needed | his head shape, hair and shoulder line ONLY - the face is deliberately never lit in this build (his pick 2026-08-05) |

---

## TIMELINE

| # | in | dur | kind | source | crop | note |
|---|---|---|---|---|---|---|
| 0 | 0.00 | 1.80 | med | `A` EVENT · out of the underpass shadow into the light | 1.00x | shadow into gold - the car comes out already moving, and silent |
| 1 | 1.80 | 1.20 | burst | `B` coastal tracking, palms strobing | 1.30x | gold on the coast road, still silent |
| 2 | 3.00 | 1.20 | burst | `C` 21-inch alloy at kerb height | 1.00x | the alloy turns, tarmac streaming, silent |
| 3 | 4.20 | 1.20 | burst | `D` cabin, backlit driver, no face | 1.15x | his hands settle on the rim, silent, the road runs ahead |
| 4 | 5.40 | 3.00 | hold ◆ | `B` coastal tracking, palms strobing | 1.00x | THE CRUISE - the coast road opens out, gold everywhere |
| 5 | 8.40 | 1.20 | burst | `C` 21-inch alloy at kerb height | 1.15x | kerb line runs under the alloy at road level, low gold light |
| 6 | 9.60 | 1.20 | burst | `A` EVENT · out of the underpass shadow into the light | 1.30x | gold at its peak, flare raking across the glass |
| 7 | 10.80 | 1.20 | burst ◆ | `D` cabin, backlit driver, no face | 1.00x | the cluster reads hybrid, no revs - glass holding the last gold |
| 8 | 12.00 | 1.20 | burst | `E` rear three-quarter, full-width light bar | 1.30x | the light bar comes on as the gold dies |
| 9 | 13.20 | 1.20 | burst | `G` wide bay, the car small in it | 1.00x | wide bay, the coast road bends away, the last gold flat on it |
| 10 | 14.40 | 1.80 | med | `F` EVENT · the climb, the petrol engine wakes | 1.15x | the road tilts up - the climb begins |
| 11 | 16.20 | 1.20 | burst | `E` rear three-quarter, full-width light bar | 1.00x | the light bar climbs away from the lens |
| 12 | 17.40 | 3.00 | hold | `F` EVENT · the climb, the petrol engine wakes | 1.00x | THE ENGINE WAKES on the climb - the one loud moment |
| 13 | 20.40 | 1.20 | burst | `G` wide bay, the car small in it | 1.30x | wide - the car tops the rise, engine still working |
| 14 | 21.60 | 1.20 | burst ◆ | `E` rear three-quarter, full-width light bar | 1.15x | the light bar settles, engine falls quiet again |
| 15 | 22.80 | 1.20 | burst | `I` parked at the seafront barrier, blue hour | 1.00x | quiet at the barrier, blue hour, the rim straightens |
| 16 | 24.00 | 1.20 | burst | `H` cabin at blue hour, key off | 1.30x | he lifts his hand off the rim at the barrier |
| 17 | 25.20 | 1.80 | med | `I` parked at the seafront barrier, blue hour | 1.15x | still at the barrier, the bay going dark |
| 18 | 27.00 | 1.20 | burst | `H` cabin at blue hour, key off | 1.00x | the cluster fades out - key off, the cabin goes dark |
| 19 | 28.20 | 1.80 | med | `I` parked at the seafront barrier, blue hour | 1.30x | dark bay, the car parked in it, nothing moves |

◆ = blend after this shot (`dissolve`, 400ms)

---

## CARDS — y=0.72 lower third, never centre

| text | shots | kind |
|---|---|---|
| **IT PULLS AWAY IN SILENCE** | 0–3 | cap |
| **2.4 TURBO HYBRID. 350PS.** | 11–13 | cap |
| **TOYOTA NEVER SOLD IT HERE** | 14–16 | cap |
| **PRICE IN THE DM** | 17–19 | cta |

---

## PREVIZ — sketch-grade, never enters generation

![previz](None)

_previz is sketch-grade and NEVER enters generation. Nev appears in panels D and H, so the sheet MUST carry the identity reference even though he is a silhouette - a text-only previz once invented a stranger and was correctly rejected ('the man is not nev')._

**LIMIT:** a still sheet CANNOT depict shot 0 (a car crossing a light boundary while moving) or shot 12 (an engine waking). Both are judged at the PROBE, never at previz. Do not reroll sketches to chase them.

Timeline board (real frames appear here automatically once clips exist):

![board](analysis/STORYBOARD.png)

---

## GENERATION PROMPTS — verbatim, as they will be sent

### `A` · EVENT · out of the underpass shadow into the light  ·  act: EVENT  ·  plates: crown

```
Vertical 9:16. THE EVENT SHOT - one action, over inside 1.5 seconds, motion already happening at frame zero, no settle. Static camera low at kerb height beside a coastal carriageway. The Toyota Crown Crossover from the reference image is ALREADY MOVING as the clip opens, emerging from the deep shade of a concrete underpass into full low-angle golden backlight, its full-width LED daytime bar lit, and sweeping past the lens. The transition from shade to blazing backlight happens ACROSS the car's body as it travels. The rest of the clip is the empty lit carriageway it left. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

### `B` · coastal tracking, palms strobing  ·  act: PAYOFF  ·  plates: crown

```
Vertical 9:16. THE SUSTAINED CRUISE - continuous motion, unbroken, no settle at the head. The Toyota Crown Crossover from the reference image driving at an easy pace along a palm-lined coastal carriageway at golden hour, tracked from a parallel vehicle, front three-quarter held steady. Palm shadows sweep rhythmically across the bodywork; the open bay and distant islands sit beyond the barrier. Camera moves smoothly with the car from first frame to last. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

### `C` · 21-inch alloy at kerb height  ·  act: EXTERIOR  ·  plates: crown

```
Vertical 9:16. Tight tracking move at kerb height along the flank of the Toyota Crown Crossover from the reference image, holding on the 21-INCH DARK MULTI-SPOKE ALLOY turning and the black rocker cladding above it, tarmac texture streaming past underneath in the low sun. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

### `D` · cabin, backlit driver, no face  ·  act: HUMAN  ·  plates: nev, crown_int

```
Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image, shot from the passenger side. The man from the FIRST reference images is in the driver's seat but he is a PURE SILHOUETTE against a blazing golden side window - his face is NEVER lit and NEVER resolves, only the outline of his head, hair and shoulder reads. Both hands rest easily at the bottom of the steering rim. In front of him the 12.3-inch cluster shows a hybrid power meter, no rev counter. Backlit, high contrast, the sun doing all the work. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

### `E` · rear three-quarter, full-width light bar  ·  act: EXTERIOR  ·  plates: crown

```
Vertical 9:16. Rear three-quarter of the Toyota Crown Crossover from the reference image on the coastal carriageway at dusk, slow arc around the rear corner. The FULL-WIDTH REAR LIGHT BAR is lit and is the brightest thing in frame; the CROWN wordmark across the tailgate reads clearly; the sky behind has gone amber to violet. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

### `F` · EVENT · the climb, the petrol engine wakes  ·  act: EVENT  ·  plates: crown

```
Vertical 9:16. THE SECOND EVENT - a state change, not a stunt. The Toyota Crown Crossover from the reference image climbing a rising coastal ramp at dusk, tracked from a parallel vehicle in front three-quarter. The car is ALREADY under load as the clip opens: the nose lifts slightly, the body settles back on its springs, the pace picks up decisively but without drama, and a faint heat shimmer rises off the rear of the car. Unhurried but unmistakably WORKING. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

### `G` · wide bay, the car small in it  ·  act: EXTERIOR  ·  plates: crown

```
Vertical 9:16. Wide static high-angle looking down over the bay at dusk, the coastal carriageway curving through the lower third of frame, the Toyota Crown Crossover from the reference image SMALL in the frame travelling along it. Mount Kinabalu's range sits in the far haze; the last sun lies flat across the bay. The car is a moving detail inside a landscape, not the subject. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

### `H` · cabin at blue hour, key off  ·  act: HUMAN  ·  plates: nev, crown_int

```
Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image at blue hour, parked and still, shot from the passenger side. The man from the FIRST reference images sits in the driver's seat as a PURE SILHOUETTE against the pale blue-grey sky through the windscreen - his face is NEVER lit and NEVER resolves. He lifts one hand off the steering rim and lets it fall to his lap. The 12.3-inch cluster glow fades down to nothing on the fascia beside him. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

### `I` · parked at the seafront barrier, blue hour  ·  act: EXTERIOR  ·  plates: crown

```
Vertical 9:16. The Toyota Crown Crossover from the reference image parked and stationary at a seafront barrier at blue hour, side-on and slightly behind, the bay beyond it flat and going dim. Very slow drift of the camera, nothing else moves. The full-width rear light bar and the cabin glow are the only lit things; the sky is deep blue with the last band of orange on the horizon. Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body creases, clear-coat orange peel in the paint, faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the windows, the far side of the car slightly softer than the near side, natural depth of field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - nothing whips, nothing shakes. Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated lens flare, crushed blacks, frantic camera movement, drift smoke.
```

---

## THE EDIT — what the engine will do, with computed times

_times below are PLANNED; blends compress them - the engine re-times cards and declares ACTUAL cut boundaries after building._

**Cut grid** — every boundary on the 150 BPM beat (0.400s), frame-exact (`-frames:v`), each shot centred on a measured action peak, exposure matched on rendered segments BEFORE blending.

| after shot | t (planned) | treatment |
|---|---|---|
| 4 (THE CRUISE - the coast road opens out, gold everywhere) | 8.40s | dissolve 400ms |
| 7 (the cluster reads hybrid, no revs - glass holding the last gold) | 12.00s | dissolve 400ms |
| 14 (the light bar settles, engine falls quiet again) | 22.80s | dissolve 400ms |

All other cuts HARD (33-67ms). Blends 3/19 = 15% (profile 6-33%).

**Sound** — synthesized drift-phonk bed at 150 BPM, first transient trimmed to t=0 (phase, not just tempo). SFX layer at +13.5dB with the bed SIDECHAIN-DUCKING under it; every whoosh LEADS its cut by 220ms and resolves ON it.

**Diegetic** — every shot lays its OWN clip audio (generated and paid for) on the actual timeline, plan-gained. Foreground (>=-6dB): shots [0, 1, 4, 6, 10, 12, 13]. Bed HARD-ducks during shots [12]. Hero: THE PETROL ENGINE WAKING on the climb (shot 12). ONE hero sound per video (file 04, law 4). Everything before it is tyre, wind and hybrid whine, so the hero is earned by 20 seconds of its own absence rather than by volume.

| t (planned) | cut entering | sound |
|---|---|---|
| 1.80s | shot 1 · gold on the coast road, still silent | whoosh |
| 3.00s | shot 2 · the alloy turns, tarmac streaming, silent | whoosh |
| 4.20s | shot 3 · his hands settle on the rim, silent, the road runs ahead | whoosh |
| 5.40s | shot 4 · THE CRUISE - the coast road opens out, gold everywhere | whoosh |
| 8.40s | shot 5 · kerb line runs under the alloy at road level, low gold light | whoosh |
| 9.60s | shot 6 · gold at its peak, flare raking across the glass | whoosh |
| 10.80s | shot 7 · the cluster reads hybrid, no revs - glass holding the last gold | whoosh |
| 12.00s | shot 8 · the light bar comes on as the gold dies | whoosh |
| 13.20s | shot 9 · wide bay, the coast road bends away, the last gold flat on it | whoosh |
| 14.40s | shot 10 · the road tilts up - the climb begins | whoosh |
| 16.20s | shot 11 · the light bar climbs away from the lens | whoosh |
| 17.40s | shot 12 · THE ENGINE WAKES on the climb - the one loud moment | IMPACT (section) |
| 20.40s | shot 13 · wide - the car tops the rise, engine still working | whoosh |
| 21.60s | shot 14 · the light bar settles, engine falls quiet again | whoosh |
| 22.80s | shot 15 · quiet at the barrier, blue hour, the rim straightens | whoosh |
| 24.00s | shot 16 · he lifts his hand off the rim at the barrier | whoosh |
| 25.20s | shot 17 · still at the barrier, the bay going dark | whoosh |
| 27.00s | shot 18 · the cluster fades out - key off, the cabin goes dark | whoosh |
| 28.20s | shot 19 · dark bay, the car parked in it, nothing moves | whoosh |

**Captions** — cards.py PNGs on desktop (drawtext fallback flagged loudly), lower third y=0.72, re-timed to actual duration:

| card | shots | planned window |
|---|---|---|
| **IT PULLS AWAY IN SILENCE** (cap) | 0-3 | 0.00-5.40s |
| **2.4 TURBO HYBRID. 350PS.** (cap) | 11-13 | 16.20-21.60s |
| **TOYOTA NEVER SOLD IT HERE** (cap) | 14-16 | 21.60-25.20s |
| **PRICE IN THE DM** (cta) | 17-19 | 25.20-30.00s |

**Grade** — saturation 1.1 ONLY (never double-grade; prompts already carry the night look), measured toward black_point 6.0 / saturation 80.0. Mix: bed +12dB, limiter 0.76 level=disabled, target -7..-9 LUFS. Output written atomically.

**Then the gates:** clipqc per clip -> engine build -> verify (10 checks, freshness first) -> JUDGES (kill-boring) -> Gavril.

---

## COST

- probe first: plates + shot `A` = **30.5 cr**, then LOOK
- remaining 8 clips = **180.0 cr**
- **total 210.5 cr**
