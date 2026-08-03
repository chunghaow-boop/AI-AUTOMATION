# NEV 360 — the persona reference set
### 97 images · organised 2026-08-01 · `index.json` carries measured metadata for every file

This is a **wardrobe turnaround shoot**: one person, eleven outfits, photographed front /
profile / back against a plain wall in flat overcast daylight, plus a six-frame head
turnaround.

---

## THE HEADLINE FINDINGS

**1 · `face/` is the identity gold, and it was sitting in a subfolder.**
Six frames — front neutral, front calm, front smiling, both profiles, back of head — shot
close, in soft window light. This is a *proper* head turnaround. Every previous Nev plate was
built from a single wide body shot; multi-angle references lock a face far harder than one
frame ever can.

**2 · In `face/` he is wearing a BLACK TEE.**
I recommended a dark wardrobe for the Supra edit before I had seen this set. It turns out the
dark reference already exists — and it is attached to the sharpest, closest, best-lit frames
in the whole collection. The recommendation and the best available reference agree.

**3 · The beige sweater in the failed Supra probe came from here.**
`wardrobe/07_sweater_tan/`. The old plate was built from this outfit, so the tan mock-neck
propagated into the video — the brightest object in a matt-black night frame. Diagnosis
confirmed against the source, not guessed.

**4 · There is no black or charcoal OUTFIT in the body set.**
The closest are `04_check_navy` (navy check over a black tee) and `09_hoodie_navy`. For a
night car shoot, drive wardrobe from `face/` (black tee) and use `04_check_navy` if a jacket
is wanted.

**5 · He wears an earring.** Clearly visible in `face/profile_right` and `face/front_calm`.
No previous plate carried it. It is a real identity marker and should be in the prompt.

**6 · These are IDENTITY references, not LIGHTING references.**
Flat overcast daylight, plain white wall, full-length framing. Perfect for "who is this
person", useless for "how is this scene lit". The lighting always comes from the plate prompt.

---

## THE FOLDER

```
face/                  6   THE IDENTITY SET — use these first
  front_neutral · front_calm · front_smile · profile_left · profile_right · back_head

wardrobe/              88  eleven outfits, front / profile / back each
  01_tiedye_orange   05_denim            09_hoodie_navy
  02_gradient_mint   06_sweat_white      10_shirt_white_print
  03_jacket_yellow   07_sweater_tan      11_fleece_brown
  04_check_navy      08_knit_oatmeal        <- darkest options: 04, 09

accessories/           3   wrist / watch detail shots (not persona references)
_contact/              2   the contact sheets — look at these before picking anything
index.json                 every file: source name, angle, dimensions, sharpness, face area
```

---

## HOW THE LABELS WERE MADE — and how far to trust them

| field | method | trust |
|---|---|---|
| `angle` | OpenCV Haar frontal + profile cascade | **measured.** But `back` really means *no face detected* — a few hard profiles land there. |
| `sharp` | variance of Laplacian | measured |
| `face_area` | largest detected face box, scaled to full res | measured |
| `score` | `face_area × sharp` | measured — this is how the best frame gets picked |
| **outfit group** | **read off the contact sheet by eye** | **judgement.** Three mechanical attempts failed — see below. |

Three automated attempts at outfit segmentation were made and all three failed: mean torso
colour, HSV histogram, and full-body histogram. The plain wall dominates every histogram and
the front/back of one outfit differ more than two adjacent outfits do. Judgement is the
documented fallback when a mechanical check fails — but it is labelled as judgement here
rather than quietly presented as a measurement. **Boundaries between adjacent outfit folders
may be off by one or two frames.**

---

## MEASURED SUMMARY

```
97 files, 6.9 MB, all JPEG
dimensions   810x1080 (80)   960x1280 (17)
sharpness    min 33   median 165   max 486
brightness   min 140  median 174   max 205     flat daylight, no deep shadow anywhere
face found   34 frontal · 10 profile · 53 none (backs + missed profiles)
```

**Top 5 by `face_area × sharpness`:**

```
26.5   face/front_neutral        area 181,476  sharp 146
17.8   wardrobe/02 idx 05        area  68,121  sharp 261
17.1   face/front_smile          area 150,544  sharp 114
16.8   face/front_calm           area 148,225  sharp 113
16.4   wardrobe/01 idx 00        area  33,856  sharp 486   <- sharpest frame in the set
```

The face folder takes three of the top four on face area; a body shot takes the sharpness
crown. For a plate, **area beats raw sharpness** — a big slightly-soft face carries identity
better than a tiny crisp one.

---

## HOW TO USE THIS FOR GENERATION

**Plate build — pass three angles, not one:**

```
face/front_neutral      primary — largest, sharpest face in the set
face/profile_right      gives the model the jawline and the earring
face/front_calm         a second frontal at a different expression stops one frame dominating
```

Then let the **plate prompt** supply the scene: night, hard key, matt-black car, wet asphalt.
Never take lighting from these images — there is none to take.

**Wardrobe:** default to the black tee from `face/`. It matches the night palette and it is
what he is actually wearing in the best references.

**Do not use `accessories/`** as persona references — they are hands and a watch, and they
will confuse an identity lock.
