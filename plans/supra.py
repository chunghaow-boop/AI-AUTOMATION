#!/usr/bin/env python3
"""
SUPRA_PLAN — the SINGLE SOURCE OF TRUTH for the Toyota GR Supra A90 Final Edition cinematic.

WHY THIS FILE EXISTS
  The plan is DATA, once. The board renders from it, the production doc generates from it,
  and planqc.py validates it. Nothing is typed twice, because the last time a plan lived in
  three places (a PNG, a markdown file and a build MAP) the board said one thing, the code
  did another, and I checked the board.

RESEARCH BEHIND THE CHOICES  (Phase 0, run 2026-08-01, BEFORE any planning)
  - A90 production ENDED March 2026. As of today the only route in is recond/used.
    That is the hook and it is true, not manufactured.
  - Toyota's own A90 Final Edition gallery leads: front 3/4 -> side profile -> rear 3/4.
  - The press text hammers, repeatedly: carbon-fibre aero (front spoiler, canards, centre
    flap, bonnet duct), the GT4-style CARBON SWAN-NECK REAR WING, matt black exclusive
    paint, RECARO Podium CF buckets in red Alcantara with red belts, Akrapovic titanium
    muffler, TGR-engraved 19in front / 20in rear wheels on Michelin Pilot Sport Cup 2,
    Brembo drilled 395mm front discs. 441 DIN hp, 571 Nm, 275 km/h. 300 WORLDWIDE.
  - Short-form: hooks under 2s = 23% higher completion. Open on an EVENT, not a tour.
    The Supra has no door theatre, so the event is HUMAN: Nev drops in, the door thumps,
    the straight-six catches and the whole car shakes on its mounts. Face at second zero -
    the LC300 opened on a wheel and had no face, no stakes, no claim.

RUN `python3 planqc.py` TO VALIDATE. Do not generate until it passes.
"""

PROJECT   = "Toyota GR Supra A90 Final Edition · car cinematic · Nev"
PILLAR    = "car_cinematic"
BPM       = 150.0
BEAT      = 60.0 / BPM              # 0.400s
W, H, FPS = 720, 1280, 30
MODE      = "std"                   # NOT fast. std = higher quality, 22.5cr/5s vs 17.5.
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40                    # 1.9x measured an 82% loss of sharpness.
TARGET_S  = 20.0

# ---------------------------------------------------------------- PLATES
# A named subject is NEVER generated from text alone. 4k always - nano_banana_pro
# defaults to 1k and every early plate was built at that floor without anyone noticing.
PLATES = {
    # v1 `13492da3` FAILED subject verification and was discarded - 4cr wasted, logged.
    #   The wing came back on STRAIGHT PEDESTALS FROM BELOW; a swan-neck hangs from curved
    #   arms ABOVE. Canards were absent entirely. Naming the part ("swan-neck", "canards")
    #   did not work; DESCRIBING THE GEOMETRY did. That is the transferable lesson.
    # v2 `813de734` APPROVED: arm arcs over the top with open space under the element,
    #   three stacked fins on each bumper corner, matt black reads matt.
    #   WATCH: wing hardware reads polished metal, not carbon weave. Softbox visible top-left.
    "supra": {"job": "813de734-e499-4269-b8d9-8eeaefe33efe",
              "res": "4k", "ar": "16:9", "cr": 8, "status": "APPROVED v2 (2 attempts)",
              "must_show": "MATT BLACK paint reading as matt, not gloss · carbon swan-neck "
                           "rear wing on twin uprights · front canards + carbon front "
                           "spoiler · double-bubble roof · ducktail deck · six-lens LED "
                           "headlights behind an L-shaped DRL · wide rear haunches",
              "prompt":
              "Photograph of a 2026 Toyota GR Supra A90 Final Edition, three-quarter front, "
              "parked on wet asphalt at night under a single hard overhead key light. "
              "Shot on a full-frame DSLR, 35mm lens, f/4, ISO 400, one large softbox camera "
              "left plus a bare rim light behind. "
              "THE CAR MUST BE UNMISTAKABLY THIS MODEL: exclusive MATT BLACK paint that "
              "ABSORBS light and shows its form through soft sheen and edge highlights, NOT "
              "glossy reflections; a GT4-style CARBON-FIBRE SWAN-NECK REAR WING mounted on "
              "two curved uprights over the ducktail deck; carbon-fibre front spoiler with "
              "CANARDS either side; a carbon duct on the bonnet; the DOUBLE-BUBBLE ROOF with "
              "its twin raised sections clearly visible; six-lens LED headlights sitting "
              "behind an L-shaped LED daytime running light; very wide rear haunches over a "
              "short wheelbase; forged wheels, 19-inch front and 20-inch rear, on Michelin "
              "Pilot Sport Cup 2 tyres; large drilled Brembo front discs visible through the "
              "spokes. "
              "REAL PHOTOGRAPH ARTEFACTS, not a render: true specular roll-off travelling "
              "along the body creases, faint panel-gap shadows, fine dust and micro-scratches "
              "catching the key light, an accurate softbox reflection in the windscreen "
              "glass, the far wheel slightly softer than the near one, neutral white balance, "
              "no HDR halos, no oversaturation. "
              "Negative: CGI, videogame look, plastic-smooth surfaces, glossy black paint, "
              "invented badges, wrong wing shape."},

    # UPGRADED 2026-08-03: multi-angle identity from the organised nev360 set.
    # The failed probe was generated from ONE plate; the face came back small and
    # unreadable. assets/nev/face/ is a proper head turnaround - front, both profiles,
    # calm/smile - shot close in soft light, black tee, earring visible. Multi-angle
    # references lock a face far harder than one frame. Upload these three and pass
    # them as image_references ALONGSIDE the car plate on every HUMAN/EVENT shot.
    "nev":   {"job": "4c542b39-a06e-42c6-affd-2d6d3c93a392", "res": "4k", "ar": "4:5",
              "cr": 0, "status": "UPGRADE - use the 3-angle face set below",
              "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                                "assets/nev/face/profile_right.jpeg",
                                "assets/nev/face/front_calm.jpeg"],
              "must_show": "is it actually him - face, hair, jawline, EARRING. "
                           "Wardrobe: the black tee from the face set (night palette).",
              "prompt": "(identity from photo references, not regenerated)"},
}

# ---------------------------------------------------------------- SHARED LOOK
_LOOK = (
    "Night. One hard artificial key plus practical light from the car itself; deep, shaped "
    "shadows. The paint is MATT BLACK - it absorbs light and reads through soft sheen and "
    "bright edge highlights, never as a glossy mirror. Neutral white balance, no HDR halos, "
    "no oversaturation. REAL FOOTAGE, NOT A RENDER: true specular roll-off along the body "
    "creases, faint panel-gap shadows, fine dust catching the key light, accurate reflections "
    "in the glass, natural depth of field with the far side slightly softer. "
    "Negative: CGI, videogame look, plastic-smooth surfaces, glossy black paint, "
    "over-bright fill, invented badges."
)

# ---------------------------------------------------------------- SOURCES
# key: (label, colour, act, plates_used, prompt)
SOURCES = {
 "A": ("EVENT · Nev in, door shut, START", "#C4562F", "EVENT", ["nev", "supra"],
       "Vertical 9:16. THE EVENT SHOT - this is frame zero and the whole event must be OVER "
       "inside 2 seconds. NO settle, NO static first frame; motion is already happening as "
       "the clip opens. "
       "The man from the FIRST reference image is dropping into the driver's seat of the "
       "Toyota GR Supra A90 Final Edition from the SECOND reference image. Camera low and "
       "close at the open driver's door, three-quarter front. His face is clearly visible for "
       "the first beat as he swings in. He pulls the door and it THUMPS shut. Immediately the "
       "straight-six fires: the whole car shakes once on its suspension, the rear settles, "
       "exhaust haze puffs from the twin Akrapovic tips. "
       "His face, hair and build must match the reference exactly - real skin texture, pores, "
       "natural asymmetry, no beauty retouching, no smoothing. " + _LOOK),

 "B": ("front 3/4, canards + spoiler", "#4A6FA5", "EXTERIOR", ["supra"],
       "Vertical 9:16. The Toyota GR Supra A90 Final Edition from the reference image, front "
       "three-quarter, night, wet ground. Slow arc of the camera across the nose. The "
       "CARBON-FIBRE FRONT SPOILER and the CANARDS either side of it are the subject and "
       "clearly readable, with the carbon bonnet duct behind them. Six-lens LED headlights "
       "behind their L-shaped daytime running light are the brightest thing in frame. "
       + _LOOK),

 "C": ("CARBON SWAN-NECK WING", "#5B8C5A", "EXTERIOR", ["supra"],
       "Vertical 9:16. Tight tracking move across the GT4-style CARBON-FIBRE SWAN-NECK REAR "
       "WING of the Toyota GR Supra A90 Final Edition from the reference image. The two "
       "curved uprights that hang the wing from ABOVE are unmistakable, the carbon weave "
       "visible in the raking key light, the ducktail deck and double-bubble roof behind it. "
       "Car stationary, camera moving. " + _LOOK),

 "D": ("20in TGR wheel + Brembo", "#B5843A", "EXTERIOR", ["supra"],
       "Vertical 9:16. Tight tracking move along the flank of the Toyota GR Supra A90 Final "
       "Edition from the reference image at wheel height, holding on the rear 20-inch forged "
       "wheel with the TGR logo engraved on the spoke, then pushing through to the large "
       "DRILLED BREMBO DISC and red caliper behind it. Michelin Pilot Sport Cup 2 sidewall "
       "lettering readable. Car stationary, camera moving. " + _LOOK),

 "E": ("RECARO buckets, red Alcantara", "#A9553E", "INTERIOR", ["supra"],
       "Vertical 9:16. Interior of the Toyota GR Supra A90 Final Edition from the reference "
       "image, no people. Slow drift across the two RECARO PODIUM CF FULL-BUCKET SEATS in "
       "RACY RED with Alcantara pads and exposed carbon shells, the RED SEAT BELTS, the "
       "carbon-fibre scuff plates and the Alcantara-wrapped steering wheel. Digital cluster "
       "glowing. Parked, night, warm screen glow against the red trim. " + _LOOK),

 "F": ("NEV cockpit, manual shift", "#7B3F6B", "HUMAN", ["nev", "supra"],
       "Vertical 9:16. The man from the FIRST reference image seated in the driver's seat of "
       "the Toyota GR Supra A90 Final Edition from the SECOND reference image, shot from the "
       "passenger side. He is held in the RECARO Podium bucket by a RED harness belt. His "
       "right hand takes the short bespoke MANUAL gear lever and pulls a shift; his eyes stay "
       "up on the road, then flick to the lens once. Cluster glow and passing streetlight on "
       "his face. His face must match the reference exactly - real skin texture, pores, "
       "natural asymmetry, no smoothing. " + _LOOK),

 "G": ("rear 3/4, ducktail + Akrapovic", "#8C6B3B", "EXTERIOR", ["supra"],
       "Vertical 9:16. Rear three-quarter of the Toyota GR Supra A90 Final Edition from the "
       "reference image, night, wet asphalt. The DUCKTAIL DECK, the carbon swan-neck wing "
       "above it, the rear diffuser and the TWIN AKRAPOVIC TITANIUM EXHAUST TIPS are the "
       "subject. LED tail lights lit, red light spilling long on the wet ground. Slow arc "
       "around the rear corner. " + _LOOK),

 "H": ("ROLLING, wet road, night", "#8C3B3B", "PAYOFF", ["supra"],
       "Vertical 9:16. THE PAYOFF - sustained motion, unbroken, no settle at the head. "
       "The Toyota GR Supra A90 Final Edition from the reference image DRIVING at speed on a "
       "wet city road at night. Tracking from a parallel vehicle, holding the front "
       "three-quarter. Background streetlights and shopfronts smear into horizontal light "
       "streaks; the car stays sharp. The headlights and the wet reflection under the car are "
       "the brightest things in frame. Continuous camera movement first frame to last. "
       + _LOOK),
}

# ---------------------------------------------------------------- TIMELINE
# (source, crop, kind, note)
#   burst = 2 beats (0.80s) · med = 4 beats (1.60s) · hold = 8 beats (3.20s)
#   hold=5 measured 60 cuts/min against a 44.7 target; hold=8 measured 48.7. Use 8.
#   CROP PLACEMENT IS A RELATIONAL PROBLEM, not a per-shot one. The first draft passed
#   every numeric check and still put 12% of its punch-ins in the first half and 67% in
#   the second - the picture got visibly softer as it played. Drawing the board caught it.
#   Rules now enforced by planqc: never crop shot 0 or a hold, max 2 crops in a row,
#   halves within 30 points of each other, and a reused source must change crop.
SHOTS = [
 ("A", 1.00, "med",   "DOOR SHUT + START"),   # EVENT. Over by 1.6s. NEVER cropped.
 ("B", 1.00, "burst", "front 3/4"),
 ("C", 1.35, "burst", "swan-neck wing"),
 ("D", 1.00, "burst", "TGR wheel"),
 ("G", 1.35, "burst", "rear 3/4"),
 ("E", 1.00, "burst", "RECARO red"),
 ("F", 1.00, "hold",  "NEV SHIFTS"),          # human hold. Holds are NEVER cropped -
 ("B", 1.35, "burst", "canards"),             # 3.2s is the most visible place for softness.
 ("H", 1.35, "burst", "rolling tease"),
 ("C", 1.00, "burst", "carbon weave"),
 ("D", 1.35, "burst", "Brembo disc"),
 ("A", 1.35, "burst", "Nev face"),
 ("H", 1.00, "hold",  "ROLLING PAYOFF"),      # highest motion on the hold, wide and sharp
 ("G", 1.00, "burst", "Akrapovic tips"),
 ("E", 1.35, "burst", "red belts"),
 ("F", 1.35, "burst", "Nev cockpit"),
 ("B", 1.00, "med",   "FRONT · CTA"),
]

# A reused source at the SAME crop is a repeated image. Declared exceptions only.
CALLBACKS = [(1, 16)]   # front 3/4 opens the montage and closes it - a deliberate loop

BEATS = {"burst": 2, "med": 4, "hold": 8}

BLEND_AFTER  = [0, 6, 12]               # event exit + both hold exits. ~19% of cuts.
BLEND_KIND   = "mask_slice"             # never `dip` - it fades through black
BLEND_WIDTH  = 0.40                     # profile band 240-560ms

# SFX. A whoosh RESOLVES on the cut - it never starts there.
SFX_LEAD     = 0.22
IMPACT_AT    = [1, 7, 13]               # SHOT indices; sound lands on the cut ENTERING
SUBDROP_AT   = [6, 12]                  # the two HOLDS: hit going IN, not coming out
# everything else gets a whoosh

# TEXT. y=0.72 lower third. NEVER centre - the car lives there.
CARD_Y       = 0.72
CARDS = [   # (text, first_shot, n_shots, kind)
    ("THE LAST ONE",   0,  4, "cap"),   # production ended March 2026 - true, not invented
    ("300 MADE",       6,  2, "cap"),
    ("441 HP",        12,  2, "cap"),
    ("DM FOR PRICE",  15,  2, "cta"),
]
AI_LABEL_BURNED_IN = False              # platform toggle at upload - a HUMAN step

# GRADE. Saturation only, then MEASURE toward the target. NEVER double-grade:
# the prompts already ask for deep night shadows, so contrast on top crushed the LC300
# from 7.7% to 40.0% of pixels below value 4.
GRADE_SAT    = 1.15
GRADE_BRI    = 0.015
TARGET_BLACK = 2.0
TARGET_SAT   = 91.5
# KNOWN RISK: matt black paint at night is legitimately dark. Watch the black-point and
# clipping gates rather than assuming a failure means the grade is wrong.

# ---------------------------------------------------------------- CONTENT
# What the video SAYS. planqc check 18 blocks any plan without this, and any claim
# without a verification source - a confident false claim in a sales video is worse
# than a dull true one.
CONTENT = {
    "claim":    "A90 Supra production ENDED March 2026 - recond is now the only way in",
    "verified": "Toyota press / netcarshow / Autoblog, checked 2026-08-01 (Phase 0)",
    "twist":    "he doesn't tour it - he gets in and takes it. THE LAST ONE isn't a "
                "museum piece, it's leaving",
    "why_stop": "a face at second zero + a dated, checkable fact (THE LAST ONE / "
                "300 MADE) in the first cards - not adjectives, receipts",
}

# ---------------------------------------------------------------- COST
PROBE_FIRST  = "A"      # generate the EVENT shot alone, LOOK at it, then commit the rest


def timeline():
    """[(start, dur, kind)] - the ONLY place shot lengths are computed."""
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
