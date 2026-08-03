# LC300 ZX — PHASE 1 PLAN (gated, awaiting approval)
### Nev reviews the Toyota Land Cruiser 300 ZX · 30s · 720p · 9:16
### Prepared 2026-07-31. Phase 0 PASSED. **Nothing in Phase 2 has been spent.**

---

## 0 · WHY THIS STOPPED AT THE GATE

Not the contract for its own sake. A specific, checkable reason:

**I cannot see any generated image from this session.** The sandbox has no network route to
Higgsfield's CDN (`cloudfront 000`, upload host `000`, web_fetch timed out at 180s), the
Chrome extension is not connected, and the desktop-access dialog timed out after you left.

The one rule that would be broken by continuing is the one that cost the most:

> **A named-product build cannot self-certify its own subject.**
> A text-only prompt for "2026 Toyota Crown" returned a generic crossover, and it shipped.

This build has **two** named subjects — Nev and the LC300 ZX. Generating 105 cr of video
against plates I have never looked at is the Crown failure with a bigger invoice.

**The plate is generated and waiting for you.** Two minutes of your eyes unblocks everything.

---

## 1 · SPEND SO FAR

| item | cr |
|---|---|
| LC300 ZX reference plate (`nano_banana_pro`, 1k, 16:9) | **2.00** |
| **total this session** | **2.00** |

Balance measured at session start: **1,445.31 cr**.

---

## 2 · PHASE 0 — RESEARCH GATE: **PASS**

8 lessons logged to `ledgers/knowledge.json`. The identity-critical ones:

- **THREE-EYE / triple LED headlamp cluster** each side — the single most recognisable J300 ZX
  signature. Three horizontal LED elements inside one slim rectangular housing.
- Grille: **four bold horizontal chrome slats**, large rectangular opening.
- **Polished 20-inch alloys**, power tailgate, 3.5L twin-turbo V6, 7-seat.
- Interior: 12.3in T-EMV, **JBL 14-speaker**, semi-aniline leather, ambient lighting,
  **dual 11.6in rear entertainment screens (ZX-only — the visual differentiator)**.
- **This is NOT the US 250-series Land Cruiser** (round retro lamps, heritage grille).
  Different vehicle. That confusion is the most likely way this build generates the wrong car.
- Malaysian recond framing: Japan **Grade 5A**, unregistered, **RM330k–400k+**. The audience
  cares about grade sheet, AP status and spec — that is the review hook, not 0–100 times.

---

## 3 · THE PROFILE THIS BUILDS AGAINST — `car_review` (n=7)

| metric | target | this build |
|---|---|---|
| median shot | **3.60s** | 3.75s |
| cuts/min | 14.3 | 14.0 |
| blended | **16%** | 12.5% (1 of 8) |
| speech share | 81–99% | speech-led, `generate_audio: true` |
| black point / saturation | 8.0 / **52.9** | `grade.py` to 52.9 — flatter than the car cinematic crush |
| duration | **58–107s** | **30s — BELOW the measured range** |

**The one honest deviation:** you asked for 30s. Every car_review reference you chose runs
58–107s. `qc.py profile` will still PASS (it gates shot median and blend %, not duration), but
30s is a format you have no measured evidence for. It is closer to a *teaser* than to the
reviews you sampled. Worth a decision, not a silent assumption.

---

## 4 · SHOT LIST — 8 shots, 30.0s

Cut to **sentence boundaries**, not a beat grid. `car_review` is speech-led.

| # | t | len | source | content | audio |
|---|---|---|---|---|---|
| 1 | 0.0 | 3.75 | GEN-A | Nev to camera, LC300 ZX behind him, hook line | speech |
| 2 | 3.75 | 3.75 | GEN-B | front 3/4 push-in, **three-eye lamps lit** | engine/amb |
| 3 | 7.5 | 3.75 | GEN-B | tight on grille slats + lamp cluster (reframe of B) | amb |
| 4 | 11.25 | 3.75 | GEN-C | 20in alloy + side profile track | tyre/amb |
| 5 | 15.0 | 3.75 | GEN-D | interior: 12.3in screen, leather, ambient light | amb |
| 6 | 18.75 | 3.75 | GEN-D | **rear dual 11.6in screens** (reframe of D) — the ZX proof | amb |
| 7 | 22.5 | 3.75 | GEN-E | Nev to camera, verdict line + price framing | speech |
| 8 | 26.25 | 3.75 | GEN-F | rear 3/4 static, CTA card overlay | bed |

**Blend:** one only — `dip` at seam 6→7 (interior → Nev). 12.5%, inside the 0–70% reference
range. Everything else hard-cut. **Do not use `whip` here**: it is fixed but unproven on a
real build, and `car_review` does not want a whip.

**6 generations → 8 shots.** Shots 3 and 6 are reframes of B and D, the `build_s450` pattern
(18 shots from 4 generations). This is what keeps it at 105 cr instead of 135.

---

## 5 · COST — PREFLIGHTED WITH THE LITERAL PARAMS

Measured via `get_cost`, not estimated:

| params | cr |
|---|---|
| `seedance_2_0` 720p **std** 5s 9:16 | 22.50 |
| `seedance_2_0` 720p **fast** 5s 9:16 | **17.50** |
| `seedance_2_0` 720p fast 10s | 35.00 |
| `nano_banana_pro` plate | 2.00 |

> **D1 is still live.** `std` is the model default and quotes **22.5**, not 17.5. Quoting
> "17.5/clip" without passing `mode: fast` explicitly reproduces the original error exactly.

**Quote: 6 × 17.50 = 105.00 cr** (`mode: fast`, 720p, 9:16, 5s, `generate_audio: true`)

| | cr |
|---|---|
| plates (1 spent, 1 pending — Nev) | 4.00 |
| generation | 105.00 |
| **total** | **109.00** |
| balance after | **~1,336.31** |

Contingency: 1 reshoot = +17.50. Hard ceiling before I stop and ask: **145 cr**.

---

## 6 · BLOCKER — THE NEV PLATE

`s450.png` is the only locked plate that exists. Nev has 49 photos and **no plate** (open
item #6 in HANDOVER).

Best source frame selected by inspection of all 49: **`nev/WhatsApp Image 2026-06-11 at
2.23.15 AM (1).jpeg`** — front-facing, head-and-shoulders, clear face, neutral background.
Copied to the outputs folder as `NEV_PLATE_SOURCE_21.jpeg`.

**It could not be uploaded.** Presigned PUT to `upload.higgsfield.ai` returned HTTP 000 —
the sandbox has no route. Three ways through, in order of preference:

1. **`media_import_url`** — needs a *direct file* URL. Your Drive link is a folder and renders
   client-side, so I could not enumerate file IDs without Chrome. Share a single file link
   (or make one file public) and Higgsfield fetches it server-side. Cleanest.
2. **`media_upload_widget`** — you pick the file in the Higgsfield widget, browser uploads
   direct. One click, needs you present.
3. **Connect the Chrome extension** — then I can read the Drive folder myself.

**`seedance_2_0` accepts `image_references` (plural)** — so once the Nev plate exists, a
single shot can carry *both* Nev and the car plate. That is the correct fix for a
two-named-subject review, and the single-`start_image` pattern in CLAUDE.md cannot do it.
Worth writing into the doc.

---

## 7 · WHAT I NEED FROM YOU — IN ORDER

1. **Look at the LC300 ZX plate** in your Higgsfield gallery (job
   `09c2124c-467f-4f9c-9402-dda606f8af41`). Check exactly one thing: **three stacked LED
   elements per headlamp, four horizontal grille slats, big square SUV.** If it is a rounded
   crossover or has round retro lamps, say so and I regenerate for 2 cr.
2. **Get Nev in** — one of the three routes in §6.
3. **Rule on 30s** vs the 58–107s your references actually run.
4. Say go, and Phase 2 runs unattended: generate → ingest → assemble → sound → captions →
   `verdict.py` → `qc.py profile` → deliver with the numbers.

---

## 8 · ALSO DONE THIS SESSION (free)

- **`fx.whip` fixed.** `pre_a`/`pre_b` were injected as `[0:v]<filter>` — the blur applied to
  the *entire* clip, not the seam. Now gated to the transition window in 3 ramped steps.
  Measured on sharp inputs (Laplacian 407/503): output median **2.6 → 457.2**, frames under
  the blank threshold **80% → 2%**. `smoketest transitions` still 45/45.
- **`S450_15S_v1` is BLOCKED by `verdict.py`** on 7 "blank frames" — it passes `qc.py profile`
  but the blocking gate had never been run on it. Root cause was the whip bug above:
  2.4s of a 10.1s cut smeared. Cannot rebuild here — `work/S450_*.mp4` sources are not in the
  RESTORE package.
- **Two gate defects logged** to `style_ledger.json` (now 22 rejects): `verdict.py` calls a
  Laplacian-sharpness test "blank frames" when 0 frames are actually black; and
  `mastermind.video_metrics` samples ~6 fps, under-counting 30 affected frames as 7.
- **Path drift bridged** — tools read `assets/pillars/`, `work/ledgers/`,
  `assets/bgm/utility-beds/`; the package ships `pillars/`, `ledgers/`, `bgm/`. Symlinked.
  Before that, 3 audio smoketest checks failed for no real reason.
- **Smoketest: 78 passed, 1 failed** (whisper weights, known sandbox limit).
