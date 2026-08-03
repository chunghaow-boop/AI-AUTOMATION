# The Car Cinematic Master Prompt — fill and fire
### File 17 · Proven template (log #26). One generation = a finished 15s multi-shot film.
### Swap the [BRACKETS]. Nothing else changes.

---

## THE TEMPLATE

```
Cinematic 4K car showcase film featuring a [COLOUR/FINISH] [CAR MODEL].
Multi-shot sequence with smooth dissolve and match-cut transitions between
every shot. Golden hour late afternoon lighting, low warm backlit sun creating
strong rim light and sharp specular reflections on the bodywork. Atmospheric,
premium mood, desaturated palette with warm amber highlights, deep shadows,
high contrast. Shot on ARRI Alexa, anamorphic lens, shallow depth of field,
subtle film grain.

Shot sequence:
1. (0-1.5s) Low-angle wide shot of the stationary [CAR], front-facing, slow
   push-in, rim light catching the hood and windshield, [ROAD/GROUND] with
   [BACKGROUND] in background
2. (1.5-3s) Smooth dissolve to extreme close-up of the front left wheel with
   spinning brake disc, slow camera drift along the tire sidewall, dust
   particles in the air catching sunlight
3. (3-4.5s) Match-cut dissolve to close-up of the rear-left three-quarter
   profile, highlighting the [TAILLIGHT SIGNATURE], rear diffuser, and
   [EXHAUST DETAIL], gentle gimbal orbit
4. (4.5-7.5s) Smooth tracking medium wide shot of the [CAR] driving down
   [LOCATION], camera parallel to the car at low angle, motion blur on wheels
5. (7.5-9s) Dissolve to ECU profile of the front wheel now stationary, brake
   caliper visible, warm rim light on the alloy spokes
6. (9-10.5s) Low-angle medium shot of front-three-quarters profile, emphasis
   on the [GRILLE DESCRIPTOR] and [HEADLIGHT SIGNATURE], slight gimbal drift
7. (10.5-12s) Orbit dissolve to low-angle medium shot of the rear-three-
   quarters, [REAR FEATURE] and taillights glowing faintly
8. (12-13.5s) Side-profile wide shot of the car facing right, low ride height,
   long shadows, sun flare at frame edge
9. (13.5-15s) Slow crane pull-back high-angle wide shot overlooking the [CAR]
   on [WIDE LOCATION], long shadow stretching out, [HORIZON ELEMENTS] against
   hazy sky

Smooth seamless transitions between every shot — no hard cuts. Consistent
lighting, color grade, and car identity across all shots. Photorealistic,
ultra-detailed, cinematic quality.
```

**Settings:** `seedance_2_0` · **9:16** (specify — the reference rendered 16:9) · 1080p · std · duration 15 · silent.

---

## THE BRACKETS — Malaysian/Sabah fills

| Bracket | Sabah default | Alternatives |
|---|---|---|
| ROAD/GROUND | dry coastal asphalt road | wet showroom floor · hillside trunk road |
| BACKGROUND | coconut palms and hazy hills | Likas bay water · KK city skyline |
| LOCATION | a quiet palm-lined coastal road | a clean suburban street · esplanade at dusk |
| WIDE LOCATION | an empty coastal asphalt road | a headland overlooking the sea |
| HORIZON ELEMENTS | palm trees and power lines | distant hills and fishing boats |

**Bank 10 accuracy — fill per car, never generic:**

| Car | GRILLE | HEADLIGHT | TAILLIGHT | REAR FEATURE |
|---|---|---|---|---|
| Lamborghini Urus | hexagonal Y-motif front | Y-shaped DRLs | Y-signature bar | quad-exit exhausts |
| Toyota Vellfire | twin-bar sport grille | slim sharp LEDs | vertical light columns | lower diffuser |
| Toyota Alphard | large chrome grille | wide LED bar | full-width bar | chrome garnish |
| LC300 | broad slat grille | slim LED units | vertical wrap lamps | tow-hitch valance |
| Audi R8 | singleframe grille | sharp LED headlights | LED taillights | rear wing + dual exhaust |

⚠️ Verify the **generation** before writing (AH30 vs AH40 Alphard, LC300 vs LC200). Wrong face = the #1 roast.

---

## THE FOUR LAWS (why it works)

1. **Global spec → timestamped shots → consistency footer.** Never reorder.
2. **Every shot 1.5s except the driving hero at 3s.** Detail–detail–MOTION–detail.
3. **Name the transition inside each shot line.** Dissolves are generated, not edited.
4. **The footer is the drift fix.** *"Consistent lighting, color grade, and car identity across all shots"* — this is what holds the car together, not mask transitions.

**No negative prompt.** Nine precisely described shots leave no room to hallucinate.

---

## THE EDIT (file 11 — what's left to do)

The transitions already exist. Do **not** add mask/object-wipes. Only:
- **2–3 hard cuts on music beats** layered over the dissolve bed — the one gap in the generated version
- Text card + CTA card
- Foley: D-floor · A14 rev (match cylinder count) · A8 drive-off · one music bed
- Disclose AI on post

---

## The Line

> **Stop generating clips. Generate films.**
> One prompt, nine shots, no seams, no approval loop.
