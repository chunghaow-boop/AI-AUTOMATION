# READ PASS — LOT (BMW recond lot, 2026-08-04)
### File 32 PART A. 60 clips read as time-ordered strips (4 frames each) before any in-point.
### This file did not exist for V1–V5. That absence is why five versions were cut blind.

## A3 · TEXT IN FRAME — VERDICTS AT FULL RESOLUTION

**I was wrong about mirroring in every version. Settled here, at native resolution:**

| clip | earlier call | ACTUAL | evidence |
|---|---|---|---|
| 33 | mirrored | **NORMAL** | "xDrive" reads forward @2.0s |
| 34 | mirrored | **NORMAL** | "X5" reads forward |
| 38 | mirrored (fixed in V1) | **NORMAL** | plate "SJQ 2315" forward |
| 39 | mirrored | **NORMAL** | no reversed text at full res |
| 41 | mirrored | **ROTATED 180°** | whole frame inverted — roof at bottom, yellow line at top. Fix is `hflip,vflip`, NOT `hflip` |
| 42 | mirrored | **NORMAL** | plate "SJQ 2315" reads forward @2.0s AND @11.0s |
| 49 | ambiguous | **NORMAL** | bonnet roundel, low viewing angle |

> **What actually happened:** one clip was shot with the camera upside down, and I
> generalised that into a "mirrored" verdict across six clips by reading 150 px contact-sheet
> panels. `hflip` was applied to 33, 34, 39, 41, 42 in **every version V1–V5** — damaging four
> correct clips and applying the wrong correction to the fifth. L179, restated precisely.

**Plates legible:** SWH 3190 (red X4) · SJQ 2315 (white X5) · 2165 (a third car, clip 47).
No blur applied — his own dealership stock.

## A1 · SPEECH — ASR VERDICT (see TRANSCRIPT.json)

| clip | verdict |
|---|---|
| 1, 3 | **NOT SPEECH** — "one, two, three" count-ins |
| 2 | **NOT SPEECH** — "so guys, I forgot", a false start |
| 7, 12 | **NOT SPEECH** — music / singing |
| 59 | **NOT SPEECH** — bell chime |
| **47** | real take, incomplete — same pitch as 48, weaker |
| **48** | **THE COMPLETE TAKE** — the whole pitch, ending on the CTA |

## A2 + A4 · WHAT EACH CLIP CONTAINS

### The cars
- **X4** — red, plate SWH 3190. Exterior 4–13, interior 14–32.
- **X5** — white, plate SJQ 2315. Exterior 33–46.
- **X1** — white/silver. Exterior 50–53, interior 54–59.

### Clip notes (subject · what happens · usable?)
```
 1  Nev crouching at the camera, walks off        SETUP, not content
 2  same, stands and walks away                   SETUP (the "I forgot" blooper)
 3  Nev walks in, ARMS OUT presenting             usable as PICTURE only (audio is a count-in)
 4  red X4 front, push in on headlights           hero front, plate visible
 5  red bonnet roundel, camera arcs around it     clean detail
 6  red X4 front 3/4, plate SWH 3190              establishing
 7  red X4 front low, moves across grille         dynamic; AUDIO IS MUSIC
 8  red flank, M badge, slow drift                detail
 9  red wheel, BLUE CALIPERS, orbit                strongest red detail (M Sport tell)
10  "X4" badge, drifts across                     ** IDENTIFIES THE X4 **
11  red rear, taillight + X4 badge                rear detail
12  red rear, plate H 3190, exhaust tip           AUDIO IS MUSIC
13  red wheel, BMW cap centred, orbit             sharpest wheel shot (sharp 27.1)
14  interior: wheel + BMW roundel, pans up        interior hero
15  gear selector, hand operating                 interior action
16  harman/kardon speaker badge                   SPEC CALLOUT - a real selling point
17  vents + hazard, hand presses                  interior detail
18  dash controls, hand                           interior detail
19  headlight rotary switch, hand turns           interior action
20  sun visor / blown highlight                   ** UNUSABLE ** - reads as nothing
21  door panel, mirror, window controls           interior
22  interior wide, wheel + dash, red bodywork L   good interior establishing
23  centre console / vents, dark                  filler
24  wheel + cluster, roundel centre               interior
25  cluster, orange needles                       interior
26  hand on wheel + paddle                        interior action
27  iDrive screen (off), console                  interior
28  door panel, BROWN leather seat                shows the trim
29  light controls, hand                          interior
30  hand on console controls, brown leather       interior
31  gear selector illuminated, hand               interior
32  cluster + wheel, daylight                     interior
33  white X5 "xDrive" badge                       NORMAL orientation
34  white "X5" badge, red X4 behind               ** IDENTIFIES THE X5 **
35  white wheel, black alloy, orbit               detail
36  white rear, taillights + spoiler              rear
37  white rear bumper, exhaust                    rear detail
38  white bonnet roundel + plate SJQ 2315         NORMAL
39  white flank / badge                           NORMAL
40  white front, quad angel-eye headlights        strong front
41  white X5 front                                ** ROTATED 180° ** - needs hflip,vflip
42  white X5 front 3/4, plate SJQ 2315            NORMAL - clean establishing
43  white headlight, rainbow lens flare           most dramatic single frame in the set
44  white headlight, angel eyes close             detail
45  white X5 front, red X4 behind                 shows BOTH cars in one frame
46  white X5 side + wheel, low angle              best white hero
47  ** NEV PRESENTING ** beside white car          real speech (incomplete take)
48  ** NEV PRESENTING ** gestures to X5            ** THE COMPLETE TAKE - THE SPINE **
49  white bonnet roundel                          NORMAL
50  white X1 front headlight                      X1 exterior
51  white X1 wheel, orbit                         X1 detail
52  "X1" badge                                    ** IDENTIFIES THE X1 **
53  white X1 rear, roundel + plate                X1 rear
54  X1 cluster + wheel roundel                    X1 interior
55  X1 climate / console                          X1 interior
56  X1 hazard + controls                          X1 interior
57  X1 iDrive knob                                X1 interior
58  X1 gear selector, illuminated, VERY dark      usable only as a moody insert
59  X1 START button, finger presses it            strong closing action; AUDIO IS A CHIME
60  near-black, door controls                     ** UNUSABLE ** (luma 3.8)
```

## A4 · WHAT THE FOOTAGE IS

Not a car review. **A dealership inventory promo.** He walks the lot and pitches three cars
in stock — X1, X5, X4 — and asks the viewer to PM. Everything else is b-roll of those three
cars. Any cut that does not follow that sentence is decoration.
