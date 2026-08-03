# PRODUCTION DOC — Toyota Land Cruiser 300 ZX · car cinematic
### Generated from `supra_plan.py` by `planqc.py`. Do not edit by hand — edit the plan.

**14 shots · 16.00s · 720x1280 @ 30fps · car_cinematic · 150 BPM · mode `std` 720p**

---

## PLATES — generate and LOOK at these first

| plate | res | cr | status | must show |
|---|---|---|---|---|
| `lc300` | 1k | 2 | SHIPPED at the 1k default — a rule that did not exist yet | the actual ZX, not a generic large SUV |

---

## TIMELINE

| # | in | dur | kind | source | crop | note |
|---|---|---|---|---|---|---|
| 0 | 0.00 | 0.80 | burst | `B` wheel + flank | 1.00x | HOOK wheel |
| 1 | 0.80 | 0.80 | burst | `A` front 3/4, lamps ignite | 1.00x | front wide |
| 2 | 1.60 | 0.80 | burst | `B` wheel + flank | 1.90x | alloy spokes |
| 3 | 2.40 | 0.80 | burst ◆ | `A` front 3/4, lamps ignite | 1.95x | lamp cluster |
| 4 | 3.20 | 0.80 | burst | `D` rear dual screens | 1.00x | step inside |
| 5 | 4.00 | 3.20 | hold ◆ | `C` cabin, 12.3in screen | 1.00x | CABIN REVEAL |
| 6 | 7.20 | 0.80 | burst | `D` rear dual screens | 1.90x | screen detail |
| 7 | 8.00 | 0.80 | burst ◆ | `C` cabin, 12.3in screen | 1.85x | 12.3in screen |
| 8 | 8.80 | 0.80 | burst | `F` rear 3/4, taillights, night | 1.00x | after dark |
| 9 | 9.60 | 0.80 | burst | `E` ROLLING, wet road, night | 1.90x | lamps at speed |
| 10 | 10.40 | 0.80 | burst | `F` rear 3/4, taillights, night | 1.85x | taillight macro |
| 11 | 11.20 | 3.20 | hold ◆ | `E` ROLLING, wet road, night | 1.00x | ROLLING payoff |
| 12 | 14.40 | 0.80 | burst | `F` rear 3/4, taillights, night | 1.90x | tail at speed |
| 13 | 15.20 | 0.80 | burst | `B` wheel + flank | 1.00x | LOOP to frame 0 |

◆ = blend after this shot (`mask_slice`, 400ms)

---

## CARDS — y=0.72 lower third, never centre

| text | shots | kind |
|---|---|---|
| **KING** | 0–1 | cap |
| **LC300 ZX** | 5–5 | cap |
| **GRADE 5A** | 8–9 | cap |
| **RM400K** | 11–11 | cap |
| **DM FOR PRICE** | 13–13 | cta |

---

## GENERATION PROMPTS — verbatim, as they will be sent

### `B` · wheel + flank  ·  act: EVENT  ·  plates: lc300

```
Vertical 9:16. 20-inch alloy and flank of the Toyota Land Cruiser 300 ZX from the reference image, tracking at wheel height. Highest-motion exterior material. Night / showroom dusk. Crushed blacks, high contrast. Real footage, not a render.
```

### `A` · front 3/4, lamps ignite  ·  act: EXTERIOR  ·  plates: lc300

```
Vertical 9:16. Front three-quarter of the Land Cruiser 300 ZX from the reference image, triple LED lamp cluster igniting. Slow arc across the nose. Night / showroom dusk. Crushed blacks, high contrast. Real footage, not a render.
```

### `D` · rear dual screens  ·  act: INTERIOR  ·  plates: lc300

```
Vertical 9:16. Rear cabin of the Land Cruiser 300 ZX from the reference image, dual 11.6-inch entertainment screens lit. Night / showroom dusk. Crushed blacks, high contrast. Real footage, not a render.
```

### `C` · cabin, 12.3in screen  ·  act: INTERIOR  ·  plates: lc300

```
Vertical 9:16. Front cabin of the Land Cruiser 300 ZX from the reference image, drift across the 12.3-inch centre screen and leather. Night / showroom dusk. Crushed blacks, high contrast. Real footage, not a render.
```

### `F` · rear 3/4, taillights, night  ·  act: EXTERIOR  ·  plates: lc300

```
Vertical 9:16. Rear three-quarter of the Land Cruiser 300 ZX from the reference image at night, taillights lit, wet ground. Night / showroom dusk. Crushed blacks, high contrast. Real footage, not a render.
```

### `E` · ROLLING, wet road, night  ·  act: PAYOFF  ·  plates: lc300

```
Vertical 9:16. The Land Cruiser 300 ZX from the reference image driving at speed on a wet road at night, tracked from a parallel vehicle. Night / showroom dusk. Crushed blacks, high contrast. Real footage, not a render.
```

---

## COST

- probe first: plates + shot `B` = **24.5 cr**, then LOOK
- remaining 5 clips = **112.5 cr**
- **total 137.0 cr**
