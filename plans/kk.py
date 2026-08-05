#!/usr/bin/env python3
"""
KK_PLAN — "NEV IN KK", the FIRST travel_vlog. Title readback resolved 2026-08-05:

  "KK"       -> Kota Kinabalu CITY (not Kundasang - the title overrode the earlier
                highland pick; that stays on the shelf for a road-trip title)
  "45 sec"   -> 28.31s band-top BY HIS PICK (46 beats; the measured travel_vlog band
                is 16-29s from his 6 references - same readback class as WRX's 30->21.6)
  bed        -> liqwyd-to-the-moon, 97.5 BPM NATIVE, ZERO stretch (bank MEASURED.md)
                -> plan BPM = 97.5. The bed chose the tempo, never the reverse.
  car        -> ONE arrival beat (the WRX cameo, hook + callback) - keeps J5 alive
                without becoming a car video. His delegation, mastermind's call.
  wardrobe   -> 10_shirt_white_print: KK is hot + coastal; white holds against sunset
                saturation. (The navy hoodie was a Kundasang pick - wrong at sea level.)
  language   -> Manglish fragments, "bah" is home ground. Cards <= 6 words (style).

FIELD SCAN (Phase 0): KK content circulates in BM/Manglish, discovery-listicle shaped;
#OriginalSabahan is a live identity marker. Events: SABAH DAY 31.08 (26 days out) is
the timing hook. THE UPGRADE vs the field: their KK content is either drone beauty
(no person) or food lists (no story). Ours: one person, one evening, time-of-day arc
6pm -> sunset -> night, with the car as punctuation and a VERIFIED receipt.
"""

PROJECT   = "NEV IN KK · travel vlog · one evening"
PILLAR    = "travel_vlog"
GEN_MODE  = "coverage"
BPM       = 97.5                     # = the bed's MEASURED native tempo. Zero stretch.
BEAT      = 60.0 / BPM               # 0.6154s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 28.31                    # 46 beats. Band-top of the measured 16-29s.

LESSONS_ACK = {            # ledger counts this plan was written against (planqc 23)
    "general craft": 56,   # pillar-INDEPENDENT: measurement, tooling, process
    "travel vlog":    3,   # this pillar's GENRE lessons
}

PREMORTEM = [
    ("the EDIT relights what the model already lit well — HIS catch, not a gate's: 'i think the video output from higgsfield lighting is already pretty good maybe the video editor edit for the second time on the lighting' (craft L49-L56)",
     "shot_match_mode=neighbour on this pillar — never a global median pull, because his three approved raws span 45.1-92.9 luma and that spread IS his taste. Authority declared in LUMA (max_move 12), not in opaque ffmpeg units. The stage RE-MEASURES its own render and keeps the untouched original as a candidate. verify 15 and tools/lightsense.py report the source-vs-delivered diff per shot, non-blocking, with matched-scale strips. MEASURED: v14 worst relight 72.6 luma -> v15 12.2, day range kept 79%"),
    ("wrong-genre/wrong-tempo bed reaches the build (craft L-wrongbed class)",
     "bed pinned to BGM/travel_vlog/liqwyd-to-the-moon; engine verify_bed_tempo "
     "REFUSES a mismatch; plan BPM set FROM the measured bed (L8 travel vlog)"),
    ("serene shots rejected by car-tuned gates (travel vlog L7 motion floor)",
     "style-block floors live: motion 0.6, luma 35-200, both PROVISIONAL and WIDE - "
     "RE-DERIVE from these first 9 real clips at ingest, then mark MEASURED"),
    ("daylight consistency across a time-of-day arc (new risk, no lesson yet)",
     "every scenery prompt pins its LIGHT STATE (golden hour / dusk / night) "
     "explicitly; shot-match runs on rendered segments; boundaries LINKAGE-declared "
     "by light continuity so no cut jumps backwards in time"),
    ("invented text on signage/subject (craft L34 badge class)",
     "clipqc text-zoom crops run on every EXTERIOR/PAYOFF/EVENT clip; market/mosque "
     "signage is exactly where models invent script - EYE reads every legible string"),
    ("AAC true-peak overshoot on the delivered encode (craft L27)",
     "gates measure the DELIVERED file only; HP30 + relimit chain unchanged"),
    ("plate anchors FRAMING not just place -> sources collapse to one image (P1)",
     "FRAMING declared per source; planqc 28 blocks two sources sharing a plate "
     "with the same camera position. THIS BUILD'S ACTUAL FAILURE - added after."),
    ("a source used 2-3x from a LOCKED-OFF clip gives identical windows (P2)",
     "every repeated source's prompt specifies CONTINUOUS camera movement. Measured: "
     "static 0.975 self-similarity vs tracking 0.871."),
    ("gibberish signage on shopfronts - J4 absolute veto (P4)",
     "street shots framed to exclude shopfronts entirely; clipqc text-zoom READ by eye "
     "on every exterior. Cost 22.5cr to learn on this build."),
    ("hook too slow for a vlog (craft frame-zero doctrine, WRX close-out)",
     "hook is a 1.23s burst (a med = 2.46s FAILS check 9 at this BPM - measured); "
     "subject LARGE at frame zero: the car fills frame then wipes to Nev"),
]

# ---------------------------------------------------------------- PLATES
PLATES = {
    "nev": {"job": "4c542b39-a06e-42c6-affd-2d6d3c93a392", "res": "4k", "ar": "4:5",
            "cr": 0, "status": "3-angle face set, EXISTS",
            "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                              "assets/nev/face/profile_right.jpeg",
                              "assets/nev/face/front_calm.jpeg"],
            "wardrobe_refs": ["assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg",
                              "assets/nev/wardrobe/10_shirt_white_print/79_front.jpeg"],
            "must_show": "actually him - face, hair, EARRING. WHITE PRINT SHIRT "
                         "(wardrobe set 10) in EVERY appearance - wardrobe continuity "
                         "is now part of the identity spec.",
            "prompt": "(identity from photo references, not regenerated)"},

    "wrx": {"job": "42c29a3e-f348-4549-bcb5-61cdc23c8a3d", "res": "4k", "ar": "16:9",
            "cr": 0, "status": "EXISTS - the WRX plate, PASS by eye 2026-08-04",
            "must_show": "the SAME WR Blue aero-kitted S4 from the first video - "
                         "channel continuity, one cameo",
            "prompt": "(existing plate, reused)"},

    "kk": {"job": "99474a92-1860-45c0-92eb-5a4bda583b58", "res": "4k", "ar": "16:9", "cr": 4,
           "status": "PASS by Claude eye 2026-08-05 (5504x3072): golden hour holds, boardwalk/"
                     "boats/ridge read plausibly KK, haze real, crowd natural, NO SIGNAGE anywhere "
                     "= zero invented-text risk. 2cr previz + 4cr plate spent; balance ~5,197.8. "
                     "GAVRIL EYE still pending at probe review.",
           "must_show": "KK waterfront at GOLDEN HOUR: Jesselton-style jetty boardwalk, "
                        "boats, the city ridge behind, South China Sea light - the "
                        "place anchor every scenery shot cites",
           "prompt":
           "Photograph of the Kota Kinabalu waterfront promenade at golden hour, "
           "Sabah, Borneo. Wooden boardwalk in the foreground, small boats on calm "
           "water, the low city skyline and Signal Hill ridge behind, warm tropical "
           "light with towering cumulus offshore. Full-frame DSLR, 35mm, f/5.6, "
           "ISO 200. REAL PHOTOGRAPH ARTEFACTS, not a render: true haze over the "
           "water, salt-air softness at the horizon, accurate warm/cool split "
           "between sunlit and shaded faces, natural crowd sparseness, no HDR "
           "halos. Negative: CGI, videogame look, oversaturated postcard grade, "
           "invented landmarks, English signage that reads as gibberish."},
}

_LOOK = (
    "Tropical golden-hour light unless the shot names another light state; warm key, "
    "soft haze, real skin and surface texture. REAL FOOTAGE, NOT A RENDER: handheld "
    "micro-shake, natural depth of field, accurate reflections, no HDR halos. "
    "Negative: CGI, videogame look, postcard oversaturation, invented signage text, "
    "extra fingers, warped faces in crowds."
)

# ---------------------------------------------------------------- SOURCES (9 x 22.5cr)
SOURCES = {
 "A": ("EVENT · ARRIVAL WIPE", "#C4562F", "EVENT", ["wrx", "kk"],
       "Vertical 9:16. THE EVENT - over inside 1.2 seconds, motion at frame zero. "
       "Static camera on the waterfront promenade from the LAST reference image at "
       "golden hour. The WR Blue Subaru from the FIRST reference image is ALREADY "
       "crossing the frame close to the lens as the clip opens, filling most of the "
       "frame, and sweeps out of shot like a wipe - revealing the man's silhouette "
       "further down the boardwalk against the sea light, walking toward camera. "
       "The car exits, the place remains. " + _LOOK),
 "B": ("NEV walks Gaya Street", "#7B3F6B", "HUMAN", ["nev"],
       "Vertical 9:16. The man from the reference images - WHITE PRINT SHIRT - "
       "walking toward camera through a busy Kota Kinabalu street market, late "
       "afternoon. Tracking backwards ahead of him, head-and-chest framing, stalls "
       "and awnings flanking, locals passing naturally. His face, hair and EARRING "
       "match the references exactly - real skin, no smoothing. " + _LOOK),
 "C": ("waterfront boats, gold", "#4A6FA5", "EXTERIOR", ["kk"],
       "Vertical 9:16. The waterfront from the reference image at golden hour: "
       "small boats rocking on bright water, boardwalk leading the eye, gulls "
       "crossing, constant gentle motion of water and light. " + _LOOK),
 "D": ("floating mosque reflection", "#5B8C5A", "EXTERIOR", ["kk"],
       "Vertical 9:16. The Kota Kinabalu City Mosque appearing to float on its "
       "still lagoon at DUSK - blue hour, minaret and dome doubled in the water, "
       "a slow drift across the reflection, warm lamps just coming on. Same city, "
       "later light than the reference image. " + _LOOK),
 "E": ("market food, smoke + sizzle", "#B5843A", "EXTERIOR", ["kk"],
       "Vertical 9:16. Extreme close-up at a Kota Kinabalu night-market grill near "
       "the waterfront of the reference image: skewers of seafood over charcoal, "
       "real smoke rolling through a shaft of low sun, oil sizzling, tongs turning "
       "the food. Fills the frame. " + _LOOK),
 "F": ("NEV at the viewpoint", "#93507E", "HUMAN", ["nev", "kk"],
       "Vertical 9:16. The man from the reference images - WHITE PRINT SHIRT - at a "
       "hilltop viewpoint railing overlooking the city and sea of the LAST "
       "reference image, late golden hour, wind moving his hair and shirt. Shot "
       "from beside him, then he turns to the view. Face and EARRING match the "
       "references exactly. " + _LOOK),
 "G": ("SUNSET, Tanjung Aru", "#8C3B3B", "PAYOFF", ["kk"],
       "Vertical 9:16. THE PAYOFF - the famous sunset of the city in the reference "
       "image, from a beach "
       "with leaning coconut palms in silhouette: the sky in full colour, clouds "
       "burning, small waves catching the last light, silhouettes of people at the "
       "waterline. Continuous slow motion of waves and birds, first frame to last. "
       + _LOOK),
 "H": ("NEV golden close", "#A9553E", "HUMAN", ["nev"],
       "Vertical 9:16. The man from the reference images - WHITE PRINT SHIRT - "
       "close head-and-shoulders on the beach at sunset, the burning sky behind "
       "him, warm light raking his face. He watches the horizon, then turns to "
       "the lens with an easy grin. Face, hair, EARRING exact - real skin. " + _LOOK),
 "I": ("city lights come on", "#8C6B3B", "EXTERIOR", ["kk"],
       "Vertical 9:16. The city of the reference image tipping from dusk into "
       "NIGHT: streetlights and shop signs flickering on along the waterfront "
       "road, headlight streaks, the ridge behind going indigo. Constant motion "
       "of traffic and light. " + _LOOK),
}

# FRAMING (planqc 28, added 2026-08-05 after his catch on v1). Every source declares
# its CAMERA POSITION. Two sources citing the same plate may not share one — measured
# root cause: A, C, E and I all cited the kk waterfront plate with no framing declared,
# and all four returned the PLATE'S OWN composition (boardwalk receding to sea). Shots
# 0/1/5/12/16 were one image five times, from three different sources.
# A plate anchors PLACE. Framing must be stated or the model reuses the picture it saw.
FRAMING = {
    "A": "low static, lane level, subject crossing frame",
    "B": "backward tracking, head-and-chest, subject walking INTO lens",
    "C": "high angle down onto water, boats filling frame, NO boardwalk leading line",
    "D": "locked wide, architecture centred, reflection symmetry",
    "E": "extreme macro, shallow, fills frame, no horizon",
    "F": "profile two-shot at railing, city as background bokeh",
    "G": "low beach level, palms as foreground silhouette frame",
    "H": "close portrait, shallow, face fills upper third",
    "I": "street level ACROSS the road, traffic crossing laterally, NO jetty",
}

# ---------------------------------------------------------------- TIMELINE 20 shots · 46 beats = 28.31s
# HARD CUTS ONLY (profile: 5 of 6 references, zero blends). Bursts carry the pace at
# the genre median (1.23s = measured 1.13 median's beat-grid neighbour); three MEDs
# are the breathing beats: the viewpoint, the face, the close.
SHOTS = [
 ("A", 1.00, "burst", "ARRIVAL WIPE - car sweeps, Nev revealed"),   # EVENT 1.23s
 ("C", 1.00, "burst", "waterfront gold, boats"),
 ("B", 1.15, "burst", "Gaya Street walk-in"),
 ("E", 1.00, "burst", "grill smoke macro"),
 ("F", 1.00, "med",   "viewpoint - the city breathes"),             # 2.46s
 ("I", 1.15, "med",   "first lights flicker - the turn"),   # 2.46s breath
 ("D", 1.00, "burst", "mosque on glass water"),
 ("B", 1.20, "burst", "market detail, hands + stalls"),
 ("G", 1.15, "burst", "sunset ignites - tease"),
 ("H", 1.00, "med",   "NEV golden face"),                            # 2.46s
 ("C", 1.15, "burst", "boats in last gold"),
 ("E", 1.15, "burst", "sizzle close 2"),
 ("I", 1.00, "burst", "streetlight streaks"),
 ("D", 1.15, "burst", "mosque, lamps on"),
 ("F", 1.15, "burst", "viewpoint wind, shirt moving"),
 ("G", 1.00, "burst", "sunset holds - the card lands here"),
 ("A", 1.35, "burst", "boardwalk at dusk - the place, emptied"),  # see CALLBACK note
 ("B", 1.00, "burst", "walking off into the market glow"),
 ("G", 1.20, "burst", "last light on the water"),
 ("H", 1.15, "burst", "NEV to lens - CTA"),
]

# CALLBACK REMOVED (0,16) 2026-08-05. It never landed: MEASURED, clip A carries the
# car only to ~2.5s and BAN_SPANS bans the static head to 1.5s, leaving ~1.0s of car
# footage that shot 0 consumes entirely. Shot 16's window was empty boardwalk, so the
# "car leaves" beat was the SAME IMAGE as the hook with no car in it - verify 13 caught
# it at 0.947. Shot 16 is now the night street. The car is a hook-only appearance,
# which is what "punctuation, not subject" meant anyway.
# TO RESTORE THE BOOKEND: regenerate A with the car present across the whole 5s (22.5cr).
CALLBACKS = [(2, 17), (9, 19)]   # Nev walks in/out · face opens and closes the video
BAN_SPANS  = {"A": [(0.0, 1.5)]}   # PROBE MEASURED: near-static head; sweep starts ~1.5s

BEATS = {"burst": 2, "med": 4}

BLEND_AFTER  = []                   # HARD CUTS ONLY - the pillar measured zero blends
BLEND_KIND   = "mask_slice"
BLEND_WIDTH  = 0.40

SFX_LEAD     = 0.22
IMPACT_AT    = []                   # edit_sfx=none for this pillar - no whoosh/impact layer
SUBDROP_AT   = []

# ---------------------------------------------------------------- SOUND (ambience gate)
SOUND = {
    "bed":        "BGM/travel_vlog/liqwyd-to-the-moon.mp3 - 97.5 BPM NATIVE, zero "
                  "stretch, 154s (5x the video: segment scan has real choice), "
                  "14.6dB dynamics, CC BY 3.0. Credit line REQUIRED at publish - "
                  "see BGM/travel_vlog/MEASURED.md.",
    "hero":       "the arrival pass (shot 0) - one hero sound, then the city takes over",
    # HIS CATCH 2026-08-05: "the car without any sfx and foley". MEASURED - the car pass
    # was 2.8dB QUIETER than a random mid-video moment. The one EVENT in the video was
    # its quietest instant, because edit_sfx=none (right for a vlog's cuts) also killed
    # the hero. Pillar now declares edit_sfx=hero_only and the plan names WHICH shot.
    "hero_shot":  0,
    "duck_shots": [0],
    "silence":    "none - ambience carries every gap; the bed breathes with the market",
}
FOLEY = {   # ambience gate: every shot lays its own clip audio, mostly UNDER the bed
     0:  -4.0,   # A  car pass - the one loud diegetic moment
     1: -12.0,   # C  water, gulls
     2: -10.0,   # B  market voices, footsteps
     3:  -6.0,   # E  sizzle FOREGROUND - food must be HEARD
     4: -12.0,   # F  wind at the railing
     5: -12.0,   # I  traffic hum
     6: -14.0,   # D  dusk hush
     7: -10.0,   # B  market hands/stalls
     8: -12.0,   # G  waves
     9: -14.0,   # H  quiet - the face is the shot
    10: -12.0,   # C  boats
    11:  -6.0,   # E  sizzle 2 foreground
    12: -12.0,   # I  streets
    13: -14.0,   # D  lamps on
    14: -12.0,   # F  wind 2
    15: -12.0,   # G  waves 2
    16:  -8.0,   # A  car cameo, quieter than the hook
    17: -10.0,   # B  market glow walk
    18: -12.0,   # G  last light
    19: -14.0,   # H  CTA - clean under the card
}

# ---------------------------------------------------------------- LINKAGE (19 boundaries)

# THE CLOCK, DECLARED HONESTLY (planqc 30, 2026-08-05).
# Read off each source's own prompt. This is the CURRENT order and it is WRONG - it is
# written down so the gate can prove it, not because it is defensible. v15 carried a
# "6PM IN KK BAH" card over afternoon market footage and no gate could see it, because
# no shot had ever been asked what time it was.
#   A golden (arrival, golden hour)      F golden (viewpoint)
#   B afternoon (Gaya St, late aft.)     G dusk   (sunset ignites)
#   C golden (waterfront boats)          H golden (NEV golden face)
#   D blue   (mosque, dusk/blue hour)    I night  (streetlight streaks, rain)
#   E dusk   (grill, low sun)
SHOT_TIME = ["golden", "golden", "afternoon", "dusk", "golden", "night",
             "blue", "afternoon", "dusk", "golden", "golden", "dusk",
             "night", "blue", "golden", "dusk", "golden", "afternoon",
             "dusk", "golden"]


LINKAGE = [
    "car exits frame right -> boats drift same direction: motion handoff",
    "water gold -> market warmth: same light temperature, place shift",
    "Nev walking toward lens -> food he is walking toward: implied approach",
    "smoke rising -> city wide from above: scale jump on a rising motif",
    "viewpoint stillness -> first lights flicker: time advances on a med exit",
    "lights on -> mosque lamps: the same dusk state, new subject",
    "mosque calm -> market hands: quiet-to-busy contrast cut",
    "market detail -> sunset ignition: the evening's turn, light jumps DECLARED",
    "sky colour -> the same colour on Nev's face: light continuity to the human",
    "his eyeline to horizon -> boats on that horizon: eyeline match",
    "boats -> sizzle: gold water to gold oil, texture rhyme",
    "sizzle -> street streaks: heat motion to light motion",
    "streets -> mosque night: dusk completes, same blue hour",
    "mosque -> viewpoint wind: two stillnesses, human returns",
    "wind -> sky at full burn: the view he faces, reverse implied",
    "full burn -> the car returns: callback in the same gold light",
    "car glow -> market glow walk: same artificial warmth, Nev departing",
    "his walk direction -> last light on water: exit toward the sea",
    "water dims -> NEV to lens: the evening hands him the close",
]

# FACE_OPTOUT (his call 2026-08-05 after clipqc rejected F): declared, never fudged.
# planqc 27 enforces that >=2 human sources still carry a readable face.
FACE_OPTOUT = {
    "F": "PRESENCE shot by design — the prompt turns him toward the view, and the "
         "back/profile 'looking out' composition is the better image and real vlog "
         "language. Face measured 1.3% across the WHOLE clip (floor 3.5%). Identity "
         "is carried by B (9.4%) and H (19.4%), 5 shots between them.",
}

# CROP_XY (2026-08-05, invented-signage catch on v7). The regenerated night-street
# clip put SHOP SIGNS across the upper third and the model wrote gibberish on them —
# "SDNMONES", "TOARAKNMN", "WELASHAF ANDIK". Legible at phone size, and J4 holds an
# ABSOLUTE veto on exactly this (one wrong sign and the video is a joke). The clip is
# otherwise good: the traffic, the wet road and the light are all correct. So crop LOW
# on I's shots — push the sign band out of frame and keep the street. Free, no reroll.
# {shot: (cx, cy)} as a fraction of the crop travel; cy=0.90 sits near the bottom.
CROP_XY = {5: (0.50, 0.92),   # crop LOW: pushes the gibberish shop signs out
           16: (0.50, 0.85)}  # crop LOW+TIGHT: breaks the rhyme with shot 0

CARD_Y       = 0.72
CARD_STYLE   = "fragment"           # pillar style: sentence fragments, <= 6 words
# CARDS read as one evening in four lines - time-of-day IS the story arc.
CARDS = [   # (text, first_shot, n_shots, kind)
    ("6PM IN KK BAH",              0, 4, "cap"),   # place + hour + home marker
    ("TOURISTS DON'T SEE THIS ONE",  5, 3, "cap"), # insider claim, market/dusk beats
    ("WORLD-CLASS SUNSET. FREE.",  9, 4, "cap"),   # the VERIFIED receipt, on the payoff
    ("COMING HOME FOR SABAH DAY?", 16, 4, "cta"),  # 31.08 - the date is the engine
]
AI_LABEL_BURNED_IN = False

GRADE_SAT    = 1.00                 # daylight vlog: prompts carry the look, no night grade
GRADE_BRI    = 0.0
TARGET_BLACK = 10.0                 # profile values, not the car's
TARGET_SAT   = 74.5

# ---------------------------------------------------------------- CONTENT
CONTENT = {
    "claim":    "Kota Kinabalu's sunsets are nationally reported as among the world's "
                "best - and watching one at Tanjung Aru costs nothing.",
    "verified": "The Star (2022-03-13, 'Among the world's best sunsets') + sustained "
                "Tripadvisor sentiment for Tanjung Aru - Phase 0, 2026-08-05",
    "twist":    "the cards are a CLOCK: 6PM -> dusk -> sunset -> night. One person, "
                "one evening, and the car is punctuation, not the subject. The field "
                "posts drone beauty with nobody in it or food lists with no story; "
                "nobody walks you through ONE evening as a local.",
    "why_stop": "a face at frame zero behind a moving car wipe; 'BAH' in card 1 is "
                "a home-ground flag no KL page can fake (J4's cheat code, file 14); "
                "receipt with a source; CTA is a date 26 days out, not a beg",
}

PREVIZ = {  # sketch-grade, NEVER enters generation. Judged the HOOK at probe, not here.
    "sheet_v1": "projects/kk/analysis/kk_previz_v1.png",
    "board_v1": "projects/kk/analysis/storyboard_kk_v1.png",
    "job":      "d5370102-075d-44f6-9114-ae6fb8448346",   # nano_banana 2k, 2cr, MEASURED
    "note":     "STANDING ORDER 2026-08-05: a storyboard (previz sheet + reference strip "
                "+ beat-exact cut table) is SHOWN TO GAVRIL before any clip credit is "
                "spent - this title and every future one.",
}

PROBE_FIRST  = "A"     # the arrival wipe: two named subjects + a camera-adjacent pass
                       # = the riskiest generation. Probe alone, LOOK, then batch.

CLIPS = {   # batch 2026-08-05: probe A + 8. D/F/G needed one resubmit each
    "A": "kk_A.mp4", "B": "kk_B.mp4", "C": "kk_C.mp4",
    "D": "kk_D.mp4", "E": "kk_E.mp4", "F": "kk_F.mp4",
    "G": "kk_G.mp4", "H": "kk_H.mp4", "I": "kk_I.mp4",
}
CLIP_BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/"
# PROBE VERDICT 2026-08-05: job fcea85a8, 22.5cr. clipqc 9/9 ACCEPT on vlog floors
# (window 7.12@1.62s, EVENT 7.88@1.67s, luma 97.5, audio -15dB, no invented text).
# Claude eye: frame zero = car FILLS frame; sweep-wipe 1.7-2.5s; place continuity
# with plate excellent. Head 0-1.5s near-static -> BAN_SPAN + shot 16 med->burst
# (beats moved to shot 5 I med). Reveal figure wears BLACK (Nev locked WHITE) ->
# reads as a stranger; Nev enters at B. GAVRIL EYE PENDING before batch.


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
