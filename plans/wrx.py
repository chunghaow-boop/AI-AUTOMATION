#!/usr/bin/env python3
"""
WRX_PLAN — Subaru WRX S4 (VA) cinematic. Title: "car cinematic of subaru wrx x4 with
nev inside, 720p, 9:16, 30 seconds" — readback resolved 2026-08-03:

  "x4"      -> WRX S4, VA generation (his pick; S4 confirmed over STI/VB)
  hook      -> AWD LAUNCH, car GONE by 1.5s (the single most WRX event there is)
  30s       -> 22s band-top by his pick; 21.6s on-grid (22.0s = 55 beats, odd —
               even-beat shots cannot sum to it; 54 beats = 21.6s is the honest max)
  GEN_MODE  -> coverage (beat-cut phonk; multishot cannot hit 44.7 hard cuts/min)

FIELD SCAN (before this plan): WRX edit culture is rally heritage — AWD launches,
anti-lag, gravel/rain, boxer rumble, the hood scoop as icon. All sound-led aggression.
THE UPGRADE: nobody puts a PERSON in the story, and nobody states the S4 fact — Japan
never exported it, so every Malaysian unit is an import by definition. Face + receipt.
"""

PROJECT   = "Subaru WRX S4 (VA) · car cinematic · Nev"
PILLAR    = "car_cinematic"
GEN_MODE  = "coverage"
BPM       = 150.0
BEAT      = 60.0 / BPM              # 0.400s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 21.6                    # 54 beats. See docstring.

# ---------------------------------------------------------------- PLATES
PLATES = {
    "wrx": {"job": None, "res": "4k", "ar": "16:9", "cr": 4, "status": "TO GENERATE",
            "must_show": "VA-gen WRX S4 with FULL AERO KIT (his call 2026-08-04 - stock "
                         "was 'ugly'): deep front splitter + canards · side skirts · rear "
                         "diffuser · TALL CARBON GT WING on the boot · large hood scoop · "
                         "angular LED headlights · WR Blue · widebody stance · 18in dark alloys",
            "prompt":
            "Photograph of a 2018 Subaru WRX S4 (VA generation) sedan in WR Blue Pearl "
            "with a FULL AGGRESSIVE AERO KIT, three-quarter front, parked on wet asphalt "
            "at night under one hard overhead light. Full-frame DSLR, 35mm, f/4, ISO 400, "
            "large softbox camera left, bare rim light behind. THE CAR MUST BE "
            "UNMISTAKABLY THIS MODEL, MODIFIED: a LARGE FUNCTIONAL HOOD SCOOP dominating "
            "the bonnet with a real dark opening; angular sharp LED headlights; a DEEP "
            "GLOSS-CARBON FRONT SPLITTER low to the ground with small CANARDS on each "
            "bumper corner; CARBON SIDE SKIRTS; a lowered widebody stance over muscular "
            "flared fenders; a TALL CARBON-FIBRE GT WING on two uprights over the boot; "
            "an aggressive REAR DIFFUSER; DUAL round exhaust tips; dark grey 18-inch "
            "multi-spoke alloys. The kit fits like a professional build - tight even "
            "panel gaps, colour-matched where painted, real carbon weave where carbon. "
            "REAL PHOTOGRAPH ARTEFACTS, not a render: true specular roll-off along the "
            "creases, clear-coat orange peel visible in the blue paint, faint panel-gap "
            "shadows, fine dust catching the key light, accurate softbox reflection in "
            "the windscreen, far wheel slightly softer than the near one, neutral white "
            "balance, no HDR halos. "
            "Negative: CGI, videogame look, plastic-smooth paint, gold wheels, "
            "invented badges, cartoonish oversized kit."},

    # Multi-angle identity — the Supra probe failure fix. Upload all three, pass as
    # image_references alongside the car plate on every HUMAN/EVENT shot.
    "nev": {"job": "4c542b39-a06e-42c6-affd-2d6d3c93a392", "res": "4k", "ar": "4:5",
            "cr": 0, "status": "3-angle face set",
            "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                              "assets/nev/face/profile_right.jpeg",
                              "assets/nev/face/front_calm.jpeg"],
            "must_show": "actually him - face, hair, jawline, EARRING. Black tee.",
            "prompt": "(identity from photo references, not regenerated)"},
}

# ---------------------------------------------------------------- SHARED LOOK
_LOOK = (
    "Night. One hard artificial key plus the car's own light; deep shaped shadows; wet "
    "asphalt doubling every light source. WR Blue paint reads deep and saturated in the "
    "highlights, near-black in shadow. Neutral white balance, no HDR halos. REAL FOOTAGE, "
    "NOT A RENDER: true specular roll-off along the creases, clear-coat orange peel, faint "
    "panel-gap shadows, fine rain mist catching the key light, accurate glass reflections, "
    "natural depth of field. Negative: CGI, videogame look, plastic-smooth surfaces, "
    "over-bright fill, invented badges, cartoonish oversized kit."
)

# ---------------------------------------------------------------- SOURCES  (9 × 22.5cr)
SOURCES = {
 # HOOK v2 after the Judge panel (2026-08-04): v1 launched AWAY - taillights of an
 # unidentifiable car, the field's most common opening. v2 launches AT THE LENS:
 # threat-read, the car's face in frame 1, and an angle real crews can't safely shoot.
 "A": ("EVENT · LAUNCH AT THE LENS", "#C4562F", "EVENT", ["wrx"],
       "Vertical 9:16. THE EVENT SHOT - ONE action only, over inside 1.5 seconds, NO "
       "settle, motion already happening at frame zero. Static camera at knee height in "
       "the MIDDLE OF THE LANE on a wet night street. The Subaru WRX S4 from the "
       "reference image is already at full throttle COMING STRAIGHT AT THE CAMERA as the "
       "clip opens - hood scoop and angular headlights filling more of the frame every "
       "frame, all four wheels throwing spray. At about 1.2 seconds it SWERVES and rips "
       "past within inches, spray and wind shear whipping across the lens, headlight "
       "flare raking over it. The rest of the clip is the empty wet street it left, "
       "mist drifting through the streetlight. " + _LOOK),
 "B": ("front 3/4, scoop + hawk eyes", "#4A6FA5", "EXTERIOR", ["wrx"],
       "Vertical 9:16. The Subaru WRX S4 from the reference image, front three-quarter, "
       "parked, night, wet ground. Slow arc across the nose. The LARGE HOOD SCOOP is the "
       "subject - its dark opening clearly readable - with the angular LED headlights "
       "the brightest thing in frame. " + _LOOK),
 "C": ("SCOOP macro, rain + heat", "#5B8C5A", "EXTERIOR", ["wrx"],
       "Vertical 9:16. Extreme macro on the HOOD SCOOP of the Subaru WRX S4 from the "
       "reference image at night. Rain beads stream across the blue bonnet toward the "
       "scoop's dark opening; one engine rev makes heat-haze shimmer rise from it and "
       "pulls a wisp of mist inward. Fills the frame - no background. " + _LOOK),
 "D": ("wheel + brake, spray", "#B5843A", "EXTERIOR", ["wrx"],
       "Vertical 9:16. Tight tracking move at wheel height along the flank of the Subaru "
       "WRX S4 from the reference image, holding on the dark 18-inch multi-spoke alloy "
       "and the brake caliper behind it, fine road spray flicking off the tread. Car "
       "creeping slowly, camera moving with it. " + _LOOK),
 "E": ("cockpit, no person", "#A9553E", "INTERIOR", ["wrx"],
       "Vertical 9:16. Interior of the Subaru WRX S4 from the reference image, no "
       "people. Slow drift across the driver-focused cockpit: red-stitched black seats "
       "and wheel, aluminium pedals, boost gauge glow on the dash, red ambient needles. "
       "Parked, night, instrument glow against darkness. " + _LOOK),
 "F": ("NEV cockpit, launch grip", "#7B3F6B", "HUMAN", ["nev", "wrx"],
       "Vertical 9:16. The man from the FIRST reference images seated in the driver's "
       "seat of the Subaru WRX S4 from the LAST reference image, shot from the passenger "
       "side, CLOSE - head and shoulders fill the upper half of frame. Black tee. Both "
       "hands set on the wheel, he rolls his shoulders once, exhales, then his eyes flick "
       "up to the road - the face of someone about to launch. Instrument glow and one "
       "streetlight on his face. His face, hair and EARRING must match the references "
       "exactly - real skin texture, pores, natural asymmetry, no smoothing. " + _LOOK),
 "G": ("rear 3/4, wing + diffuser", "#8C6B3B", "EXTERIOR", ["wrx"],
       "Vertical 9:16. Rear three-quarter of the Subaru WRX S4 from the reference image, "
       "night, wet asphalt. The TALL CARBON GT WING, the REAR DIFFUSER, DUAL round "
       "exhaust tips breathing faint vapour, tail lights lit and doubled in the wet "
       "ground. Slow arc around the rear corner. " + _LOOK),
 "H": ("ROLLING, wet road, night", "#8C3B3B", "PAYOFF", ["wrx"],
       "Vertical 9:16. THE PAYOFF - sustained motion, unbroken, no settle at the head. "
       "The Subaru WRX S4 from the reference image driving hard on a wet city road at "
       "night, tracked from a parallel vehicle, front three-quarter held. Streetlights "
       "smear into horizontal streaks; the car stays sharp; spray trails off all four "
       "arches - unmistakably all-wheel drive. Continuous camera movement first frame to "
       "last. " + _LOOK),
 "I": ("NEV + car, street", "#93507E", "HUMAN", ["nev", "wrx"],
       "Vertical 9:16. The man from the FIRST reference images leaning back against the "
       "front fender of the Subaru WRX S4 from the LAST reference image on a wet street "
       "at night, arms crossed, relaxed, looking at the lens. Black tee. Framed close "
       "enough that his face is large and clearly readable. Headlight glow rims him from "
       "behind. Face, hair and EARRING match the references exactly - real skin, no "
       "smoothing. " + _LOOK),
}

# ---------------------------------------------------------------- TIMELINE  19 shots · 54 beats = 21.60s
# First draft had 50 beats against a 21.6 target and a 3-crop run - planqc caught its
# own author. Rebuilt: crop halves 44%/50%, longest run 2, hook and holds uncropped.
SHOTS = [
 ("A", 1.00, "med",   "LAUNCH AT LENS"),         # EVENT, 1.6s
 ("B", 1.00, "burst", "front 3/4"),
 ("C", 1.35, "burst", "scoop macro"),
 ("D", 1.00, "burst", "wheel spray"),
 ("G", 1.35, "burst", "rear 3/4"),
 ("E", 1.00, "burst", "cockpit empty"),
 ("F", 1.00, "hold",  "NEV - about to launch"),  # human hold, uncropped
 ("H", 1.35, "burst", "rolling tease"),
 ("B", 1.35, "burst", "hawk eyes"),
 ("I", 1.00, "burst", "NEV + car"),
 ("D", 1.35, "burst", "caliper"),
 ("H", 1.00, "hold",  "ROLLING PAYOFF"),         # highest motion, uncropped
 ("C", 1.00, "burst", "scoop breathes"),
 ("E", 1.35, "burst", "boost gauge"),
 ("F", 1.35, "burst", "NEV grin"),
 ("G", 1.00, "burst", "dual tips"),
 ("A", 1.35, "burst", "lens-pass replay"),
 ("I", 1.35, "burst", "NEV punch-in"),
 ("B", 1.00, "med",   "FRONT - CTA"),
]

CALLBACKS = [(1, 18)]       # front 3/4 opens the montage and closes it

BEATS = {"burst": 2, "med": 4, "hold": 8}

BLEND_AFTER  = [0, 6, 11]           # event exit + both hold exits = 3/18 cuts = 17%
BLEND_KIND   = "mask_slice"
BLEND_WIDTH  = 0.40

SFX_LEAD     = 0.22
IMPACT_AT    = [1, 7, 12]           # SHOT indices - sound lands on the cut ENTERING them
SUBDROP_AT   = [6, 11]              # the two HOLDS: hit going IN

CARD_Y       = 0.72
# NARRATIVE CARDS (2026-08-04, after "the story is too common"): the field's cards are
# labels; ours read as a SENTENCE across the video - a forbidden-fruit story with a
# resolution. This is the improvise-above move at STORY level, not just hook level.
CARD_STYLE = "narrative"   # DECLARED deviation from the profile's 1-2 word label style.
                           # The deviation IS the improvisation: cards read as a sentence.
CARDS = [   # (text, first_shot, n_shots, kind)
    ("JAPAN KEPT IT",       0, 4, "cap"),   # Act 1 FORBIDDEN
    ("NEVER SOLD HERE",     6, 2, "cap"),   # Act 2 THE PROOF
    ("HE FOUND ONE",       11, 2, "cap"),   # Act 3 THE TAKE
    ("DM BEFORE IT'S GONE",16, 3, "cta"),
]
AI_LABEL_BURNED_IN = False

GRADE_SAT    = 1.15
GRADE_BRI    = 0.015
TARGET_BLACK = 2.0
TARGET_SAT   = 91.5

# ---------------------------------------------------------------- CONTENT
CONTENT = {
    "claim":    "The WRX S4 was JAPAN-ONLY - never officially sold outside Japan. Every "
                "unit in Malaysia is a JDM import by definition.",
    "verified": "Subaru JDM lineup / Wikipedia VA-series S4 (JDM-only trim, 300PS FA20, "
                "CVT), cross-checked BeForward JDM export listings - 2026-08-03 Phase 0",
    "twist":    "the cards ARE the story - four lines that read as a sentence "
                "(KEPT / NEVER SOLD / FOUND ANYWAY / GONE) over a forbidden-fruit arc. "
                "The payoff still lands FIRST and AT the viewer.",
    "why_stop": "threat-read: a car at full throttle AT the viewer, identity visible "
                "(scoop + hawk eyes), swerve at 1.2s + receipt card (JAPAN ONLY) - "
                "no reference edit opens toward-camera because real crews cannot",

    # Judge panel verdict, recorded (the Wow Test the merge had dropped):
    "judged":   "2026-08-04 panel, twice. HOOK v1: weak-pass/novelty-FAIL -> v2 "
                "toward-camera. STORY v1 (Gavril: 'too common'): montage skeleton same "
                "as every field edit -> narrative cards adopted, cards form a sentence. "
                "Lesson: the panel must judge HOOK and ARC separately.",
}

PREVIZ = {  # sketch-grade, NEVER enters generation. v2 carries the Nev identity ref.
    "sheet_v3": "https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/hf_20260804_043249_35fadfd8-8a81-4f91-b7e7-f3f9d0883ffa.png",
    "limit":    "STILL PREVIZ CANNOT DEPICT THE v2 HOOK - a static frame cannot show "
                "'charging at the lens'; the model rendered a parked front view. The "
                "hook is judged at the PROBE, never at previz. Do not reroll sketches.",
    "note": "panel letters partly scrambled by the model; CONTENT mapping: "
            "launch=A front=B scoopmacro=C wheel=D cockpit=E nev-seat=F rear=G rolling=H nev-lean=I",
}

PROBE_FIRST  = "A"      # the launch is the riskiest generation - probe it alone


def timeline():
    out, t = [], 0.0
    for _s, _c, kind, _n in SHOTS:
        d = BEATS[kind] * BEAT
        out.append((round(t, 4), round(d, 4), kind))
        t += d
    return out, round(t, 4)


def cost():
    per = 22.5 if MODE == "std" else 17.5
    gen = len(SOURCES) * per
    plates = sum(p["cr"] for p in PLATES.values())
    return {"per_clip": per, "clips": len(SOURCES), "generation": gen,
            "plates": plates, "total": gen + plates,
            "probe": plates + per, "after_probe": gen - per}
