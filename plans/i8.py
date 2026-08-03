#!/usr/bin/env python3
"""
I8_PLAN — the SINGLE SOURCE OF TRUTH for the BMW i8 cinematic.

WHY THIS FILE EXISTS
  The first version of this plan lived in three places: a hand-drawn storyboard PNG, a
  prose markdown file, and the build script's MAP. Three copies of the same truth,
  maintained separately. That is the bug class that already cost us twice tonight:

    the stale output file      I measured yesterday's render and reported it as new
    planned vs actual cuts     I verified against beatplan's plan, not the real edit

  Sooner or later the board says one thing and the code does another, and I check the
  board. So: the plan is DATA, here, once. The board renders from it, the production
  doc generates from it, and planqc.py validates it. Nothing is typed twice.

  Run `python3 planqc.py` to validate, render the board, and write the doc.
"""

PROJECT   = "BMW i8 · car cinematic"
PILLAR    = "car_cinematic"
BPM       = 150.0
BEAT      = 60.0 / BPM              # 0.400s
W, H, FPS = 720, 1280, 30
MODE      = "std"                   # NOT fast - std is the higher-quality generation
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40                    # 1.9x cost 82% of sharpness. Measured.

# ---------------------------------------------------------------- PLATES
PLATES = {
    "i8":  {"job": "7a750ac0-28c9-4d1c-b36a-f533d9f33f3d",
            "res": "4k", "ar": "16:9", "cr": 4,
            "must_show": "blue laser band inside the lamp · black floating rear buttress "
                         "with an air channel · low wedge stance"},
    "nev": {"job": "4c542b39-a06e-42c6-affd-2d6d3c93a392",
            "res": "4k", "ar": "4:5", "cr": 4,
            "must_show": "is it actually him - face, hair, jawline unchanged"},
}

# ---------------------------------------------------------------- SOURCES
# key: (label, colour, act, plates_used, prompt)
_NIGHT = ("Night. Hard artificial light, deep black shadows, the car emitting its own "
          "light. Neutral white balance, no HDR halos, no oversaturation. "
          "Real footage, not a render - true specular roll-off on the body creases, "
          "clear-coat orange peel, accurate reflections in the glass.")

SOURCES = {
 "A": ("BUTTERFLY DOORS rising", "#C4562F", "EVENT", ["i8"],
       "Vertical 9:16. THE EVENT SHOT - this is frame zero and it must read inside 0.8s. "
       "The BMW i8 from the reference image, parked on wet asphalt at night. Both "
       "BUTTERFLY DOORS are already in motion as the clip opens - NO settle, NO static "
       "first frame. They sweep UP and FORWARD, hinged at the A-pillar, rising to full "
       "travel within the clip. Camera low, three-quarter front, slow push in as the "
       "doors rise. Cabin light spills out as they open. " + _NIGHT),
 "B": ("front 3/4, laser lamps", "#4A6FA5", "EXTERIOR", ["i8"],
       "Vertical 9:16. The BMW i8 from the reference image, front three-quarter, night, "
       "wet ground. Slow arc of the camera across the nose. The LASER HEADLAMPS with "
       "their passively lit BMW i BLUE BAND are the brightest thing in frame. Narrow "
       "closed kidney grilles with blue surround clearly readable. " + _NIGHT),
 "C": ("turbine wheel + carbon sill", "#5B8C5A", "EXTERIOR", ["i8"],
       "Vertical 9:16. Tight tracking move along the flank of the BMW i8 from the "
       "reference image at wheel height, holding on the 20-inch TURBINE-STYLE ALLOY with "
       "its aerodynamic covers, then rising slightly to the EXPOSED CARBON-FIBRE SILL and "
       "the BMW i blue side-skirt accent. Car stationary, camera moving. " + _NIGHT),
 "G": ("laser lamp macro, BLUE BAND", "#3E7CA8", "EXTERIOR", ["i8"],
       "Vertical 9:16. Extreme macro on ONE laser headlamp of the BMW i8 from the "
       "reference image. The passively lit BMW i BLUE BAND inside the housing ignites "
       "during the clip. Reflections crawl across the lens optics as the camera drifts. "
       "Fills the frame - no body, no background. " + _NIGHT),
 "H": ("side profile, stream-flow", "#6B8FA8", "EXTERIOR", ["i8"],
       "Vertical 9:16. Pure side profile of the BMW i8 from the reference image, camera "
       "tracking parallel. The BLACK STREAM-FLOW FLOATING REAR BUTTRESS with its OPEN AIR "
       "CHANNEL through the C-pillar is centre frame and unmistakable - roof and buttress "
       "visibly separated. Low wedge stance, sloping roofline. " + _NIGHT),
 "F": ("cockpit, blue ambient", "#B5843A", "INTERIOR", ["i8"],
       "Vertical 9:16. Interior of the BMW i8 from the reference image. Slow drift across "
       "the driver-angled cockpit: floating centre console, digital cluster glowing, BLUE "
       "AMBIENT LIGHT STRIPS along the door and console, thin sculpted sports seats. "
       "Futuristic rather than plush. Parked, night, warm screen glow against blue "
       "ambient. " + _NIGHT),
 "I": ("rear lights + diffuser", "#A9553E", "INTERIOR", ["i8"],
       "Vertical 9:16. Macro on the rear of the BMW i8 from the reference image: tail "
       "lights lit, integrated diffuser and adaptive rear spoiler visible. Slow camera "
       "arc across the tail. Red light spilling onto wet ground. " + _NIGHT),
 "D": ("rear 3/4, buttresses", "#8C6B3B", "INTERIOR", ["i8"],
       "Vertical 9:16. Rear three-quarter of the BMW i8 from the reference image, night, "
       "wet asphalt. The FLOATING REAR BUTTRESSES and the gap between roof and buttress "
       "are the subject. Adaptive rear spoiler raised. Slow arc around the rear corner. "
       + _NIGHT),
 "J": ("NEV + car, forecourt", "#7B3F6B", "HUMAN", ["nev", "i8"],
       "Vertical 9:16. The man from the FIRST reference image standing beside the BMW i8 "
       "from the SECOND reference image, on a wet forecourt at night. He is turned "
       "three-quarters to camera, one hand resting on the open butterfly door, relaxed, "
       "looking toward the lens. His face, hair and build must match the reference "
       "exactly. Real skin texture, natural asymmetry, no beauty retouching. The car's "
       "laser lamps light him from behind. " + _NIGHT),
 "K": ("NEV in cockpit", "#93507E", "HUMAN", ["nev", "i8"],
       "Vertical 9:16. The man from the FIRST reference image seated in the driver's seat "
       "of the BMW i8 from the SECOND reference image, shot from the passenger side. Blue "
       "ambient strips and cluster glow on his face. He glances toward the lens once. His "
       "face must match the reference exactly - real skin texture, pores, natural "
       "asymmetry, no smoothing. " + _NIGHT),
 "E": ("ROLLING, wet road", "#8C3B3B", "NIGHT DRIVE", ["i8"],
       "Vertical 9:16. THE PAYOFF - sustained motion, unbroken, no settle at the head. "
       "The BMW i8 from the reference image DRIVING at speed on a wet city road at night. "
       "Tracking from a parallel vehicle, holding the front three-quarter. Background "
       "streetlights and shopfronts smear into horizontal light streaks; the car stays "
       "sharp. Laser lamps and blue band are the brightest thing in frame, reflected long "
       "on the wet asphalt. Continuous camera movement first frame to last. " + _NIGHT),
}

# ---------------------------------------------------------------- TIMELINE
# (source, crop, kind, note)
SHOTS = [
 ("A", 1.00, "burst", "DOORS RISE"),     ("G", 1.00, "burst", "lamp ignites"),
 ("C", 1.00, "burst", "turbine wheel"),  ("H", 1.00, "burst", "side profile"),
 ("B", 1.00, "burst", "front 3/4"),      ("A", 1.00, "hold",  "DOORS FULLY UP"),
 ("F", 1.00, "burst", "step inside"),    ("I", 1.00, "burst", "rear light macro"),
 ("F", 1.35, "burst", "blue ambient"),   ("D", 1.00, "burst", "rear 3/4"),
 ("G", 1.35, "burst", "blue band"),      ("J", 1.00, "hold",  "NEV + CAR"),
 ("C", 1.35, "burst", "carbon sill"),    ("B", 1.35, "burst", "kidney + blue"),
 ("K", 1.00, "burst", "Nev cockpit"),    ("H", 1.35, "burst", "buttress channel"),
 ("I", 1.35, "burst", "tail light"),     ("E", 1.00, "hold",  "ROLLING NIGHT"),
 ("D", 1.35, "burst", "spoiler"),        ("E", 1.35, "burst", "lamps at speed"),
 ("J", 1.35, "burst", "Nev punch"),      ("K", 1.35, "burst", "Nev cockpit"),
 ("C", 1.00, "burst", "wheel rolling"),  ("B", 1.00, "hold",  "FRONT, NIGHT"),
 ("G", 1.00, "burst", "lamp"),           ("A", 1.00, "burst", "LOOP to doors"),
]

BLEND_AFTER  = [5, 11, 17, 23]          # HOLD exits only. mask_slice 0.40s, never dip.
BLEND_KIND   = "mask_slice"
BLEND_WIDTH  = 0.40

# SFX. whoosh LEADS the cut by 220ms - it RESOLVES on the cut, never starts there.
SFX_LEAD     = 0.22
IMPACT_AT    = [5, 11, 17, 23]          # section boundaries
SUBDROP_AT   = [6, 12, 18]              # first shot after a hold
# everything else gets a whoosh

# TEXT. y=0.72 lower third. Never centre - the car lives there.
CARD_Y       = 0.72
CARDS = [   # (text, first_shot, n_shots, kind)
    ("DOORS UP",     0,  4, "cap"),
    ("i8",           5,  1, "cap"),
    ("LASER LIGHT", 10,  2, "cap"),
    ("RECOND",      17,  1, "cap"),
    ("DM FOR PRICE",23,  3, "cta"),
]
AI_LABEL_BURNED_IN = False              # platform toggle at upload instead

# GRADE. saturation only, then MEASURE toward the target. Never double-grade.
GRADE_SAT    = 1.15
GRADE_BRI    = 0.015
TARGET_BLACK = 2.0
TARGET_SAT   = 91.5


def timeline():
    """[(start, dur, kind)] - the only place shot lengths are computed."""
    out, t = [], 0.0
    for _s, _c, kind, _n in SHOTS:
        d = 8 * BEAT if kind == "hold" else 2 * BEAT
        out.append((round(t, 4), round(d, 4), kind))
        t += d
    return out, round(t, 4)


def cost():
    per = 22.5 if MODE == "std" else 17.5
    gen = len(SOURCES) * per
    plates = sum(p["cr"] for p in PLATES.values())
    return {"per_clip": per, "clips": len(SOURCES), "generation": gen,
            "plates": plates, "total": gen + plates}
