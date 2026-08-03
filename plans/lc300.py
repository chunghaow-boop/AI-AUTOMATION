#!/usr/bin/env python3
"""
LC300 ZX — the plan for the cut that SHIPPED on 2026-07-31, reconstructed as data.

WHY THIS FILE EXISTS
  This video was built by a bespoke 530-line script. Writing it back out as a plan does
  two things: it proves `engine.py` can reproduce a known-good cut, and it lets the plan
  gate judge a video that was made BEFORE the plan gate existed.

  It does not pass. `talyx.py plan lc300` fails check 6 — crops of 1.85/1.90/1.95 against
  a 1.40 cap. That is correct and it is the point: the shipped LC300 was made before the
  punch-in measurement (1.9x costs 82% of sharpness, 234 -> 42) and would be blocked today.
  Kept faithful rather than quietly corrected, because a plan that lies about what was
  built is worse than one that fails.
"""

PROJECT   = "Toyota Land Cruiser 300 ZX · car cinematic"
PILLAR    = "car_cinematic"
BPM       = 150.0
BEAT      = 60.0 / BPM
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40          # the shipped cut breaks this. See the docstring.
TARGET_S  = 16.0

PLATES = {
    "lc300": {"job": "09c2124c", "res": "1k", "ar": "16:9", "cr": 2,
              "status": "SHIPPED at the 1k default — a rule that did not exist yet",
              "must_show": "the actual ZX, not a generic large SUV",
              "prompt": "(historic, not regenerated)"},
}

# Files in projects/lc300/clips/. The engine also falls back to glob *_<KEY>_*.mp4.
CLIPS = {
    "A": "LC300_B_front.mp4",         # exterior front 3/4        brightness 81.2  motion  8.10
    "B": "LC300_C_wheel.mp4",         # 20in alloy + flank        brightness 73.7  motion 14.58
    "C": "LC300_D_interior.mp4",      # cabin, 12.3in screen      brightness 51.9  motion 16.90
    "D": "LC300_E_rear_screens.mp4",  # rear dual 11.6in screens  brightness 46.8  motion  7.00
    "E": "LC300_F_rolling.mp4",       # DRIVING, wet road, night  brightness 53.9  motion 15.61
    "F": "LC300_G_rear_night.mp4",    # rear 3/4, taillights      brightness 51.9  motion  7.73
}

_LOOK = ("Night / showroom dusk. Crushed blacks, high contrast. Real footage, not a render.")

SOURCES = {
 "B": ("wheel + flank", "#4A6FA5", "EVENT", ["lc300"],
       "Vertical 9:16. 20-inch alloy and flank of the Toyota Land Cruiser 300 ZX from the "
       "reference image, tracking at wheel height. Highest-motion exterior material. "
       + _LOOK),
 "A": ("front 3/4, lamps ignite", "#5B8C5A", "EXTERIOR", ["lc300"],
       "Vertical 9:16. Front three-quarter of the Land Cruiser 300 ZX from the reference "
       "image, triple LED lamp cluster igniting. Slow arc across the nose. " + _LOOK),
 "D": ("rear dual screens", "#B5843A", "INTERIOR", ["lc300"],
       "Vertical 9:16. Rear cabin of the Land Cruiser 300 ZX from the reference image, "
       "dual 11.6-inch entertainment screens lit. " + _LOOK),
 "C": ("cabin, 12.3in screen", "#A9553E", "INTERIOR", ["lc300"],
       "Vertical 9:16. Front cabin of the Land Cruiser 300 ZX from the reference image, "
       "drift across the 12.3-inch centre screen and leather. " + _LOOK),
 "F": ("rear 3/4, taillights, night", "#8C6B3B", "EXTERIOR", ["lc300"],
       "Vertical 9:16. Rear three-quarter of the Land Cruiser 300 ZX from the reference "
       "image at night, taillights lit, wet ground. " + _LOOK),
 "E": ("ROLLING, wet road, night", "#8C3B3B", "PAYOFF", ["lc300"],
       "Vertical 9:16. The Land Cruiser 300 ZX from the reference image driving at speed "
       "on a wet road at night, tracked from a parallel vehicle. " + _LOOK),
}

# (source, crop, kind, note)   crop centre defaults to 0.50/0.50; overrides in CROP_XY
SHOTS = [
 ("B", 1.00, "burst", "HOOK wheel"),      ("A", 1.00, "burst", "front wide"),
 ("B", 1.90, "burst", "alloy spokes"),    ("A", 1.95, "burst", "lamp cluster"),
 ("D", 1.00, "burst", "step inside"),     ("C", 1.00, "hold",  "CABIN REVEAL"),
 ("D", 1.90, "burst", "screen detail"),   ("C", 1.85, "burst", "12.3in screen"),
 ("F", 1.00, "burst", "after dark"),      ("E", 1.90, "burst", "lamps at speed"),
 ("F", 1.85, "burst", "taillight macro"), ("E", 1.00, "hold",  "ROLLING payoff"),
 ("F", 1.90, "burst", "tail at speed"),   ("B", 1.00, "burst", "LOOP to frame 0"),
]

CROP_XY = {2: (.50, .55), 3: (.50, .36), 6: (.50, .42), 7: (.40, .45),
           9: (.50, .45), 10: (.50, .55), 12: (.50, .40)}

BEATS = {"burst": 2, "med": 4, "hold": 8}

BLEND_AFTER = [3, 5, 7, 11]     # two section boundaries + both hold exits
BLEND_KIND  = "mask_slice"
BLEND_WIDTH = 0.40

SFX_LEAD   = 0.22
IMPACT_AT  = [4, 8]     # SHOT indices - the sound lands on the cut ENTERING them
SUBDROP_AT = [5, 11]    # the two HOLDS: hit going IN, not coming out

CARD_Y = 0.72
CARDS = [   # (text, first_shot, n_shots, kind)
    ("KING",          0, 2, "cap"),
    ("LC300 ZX",      5, 1, "cap"),
    ("GRADE 5A",      8, 2, "cap"),
    ("RM400K",       11, 1, "cap"),
    ("DM FOR PRICE", 13, 1, "cta"),
]
AI_LABEL_BURNED_IN = False

GRADE_SAT, GRADE_BRI = 1.70, 0.015
TARGET_BLACK, TARGET_SAT = 2.0, 91.5

CALLBACKS = [(0, 13)]           # the loop back to frame 0 is deliberate
PROBE_FIRST = "B"


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
