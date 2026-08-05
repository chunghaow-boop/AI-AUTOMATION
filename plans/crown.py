#!/usr/bin/env python3
"""
CROWN_PLAN — Toyota Crown Crossover 2.4 RS Advance (S16) · chill coastal cinematic · Nev.
Title: "car cinematic video for toyota crown Hev with nev inside, 720p, 30 seconds,
cruise along kk, chill vibe" — readback resolved 2026-08-05:

  "Crown HEV"  -> Crown CROSSOVER 2.4 RS Advance turbo hybrid (HIS PICK over the 2.5 HEV
                  G/X). The recond-lot hero: 21-inch alloys, dark accents, wide bumper.
  "chill"      -> NOT car_cinematic. New declared pillar car_cinematic_chill (his pick):
                  100 BPM, 1.2s median, blends kept, hero-only edit sfx. See the profile's
                  own _not_measured note - every number in it is a CHOICE, not a measurement.
  "cruise KK"  -> Tanjung Aru -> Likas coastal road, golden hour falling into blue hour.
                  Light was MY call (he said "go with your decision"): it is the only option
                  where the ending is CAUSED. Night and morning both give a tour with a clock
                  that never runs out.
  "nev inside" -> SILHOUETTE ONLY, face never resolves (HIS PICK). Identity gate drops out
                  entirely; the persona refs still ride every human shot so his build, hair
                  and posture stay consistent across videos. Stated once and accepted: this
                  build does not grow Nev as a recognisable KOL.
  30s          -> 50 beats at 100 BPM = 30.00s exactly.

FIELD SCAN (before this plan). The five references in assets/refs/car_cinematic and the
measured profile agree on one thing: this genre is SOUND-LED AGGRESSION - drift phonk,
exhaust, launches, 0.77s cuts. Nothing in the field is chill, and the two chill-adjacent
neighbours (travel_vlog) are holiday reels with no car sound design at all.

THE UPGRADE: every car edit in the field sells NOISE. This one sells the ABSENCE of it, and
the hybrid powertrain is the only reason it can. Thirty seconds with exactly one loud moment
- the petrol engine waking on the climb - which is earned by twenty seconds of tyre hiss.
That is a thing the reference field cannot do with a combustion car, and it is the product's
own feature doing the storytelling.

STORY, AS A SENTENCE (written BEFORE the shot list, per RESUME 2026-08-05b):
  A man leaves the city with the engine off - the Crown pulls away in silence - and drives
  the coast until the light runs out; the climb wakes the petrol engine, and at the water he
  switches it back off and lets the day end.

The consequence chain is the spine: silence -> the light dies -> the climb -> THE ENGINE
WAKES -> the crest -> the water -> key off -> silence returns. Eight of nineteen boundaries
are typed "consequence" (planqc 31 floor is 4). KK v15 had ZERO, and he disliked KK.
"""

PROJECT   = "Toyota Crown Crossover 2.4 RS Advance · chill coastal cinematic · Nev"
PILLAR    = "car_cinematic_chill"
GEN_MODE  = "coverage"
BPM       = 100.0
BEAT      = 60.0 / BPM              # 0.600s
W, H, FPS = 720, 1280, 30
MODE      = "std"                   # never 'fast' to save money silently
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 30.0                    # 50 beats. See BEATS below.

# BEATS IS PER-BPM MATH, NEVER A TEMPLATE (ledger 'car cinematic chill' L3).
# The car plans use {burst:2, med:4, hold:8} at 150 BPM = 0.80 / 1.60 / 3.20s.
# Copying that here would give 1.20 / 2.40 / 4.80s - a 4.8s hold is 3.7x this
# dialect's 1.3s median and 16% of the video on ONE image. Recomputed:
BEATS = {"burst": 2, "med": 3, "hold": 5}       # 1.20 / 1.80 / 3.00s at 100 BPM

# ---------------------------------------------------------------- PLATES
# A named subject is NEVER generated from text alone. This car is the repo's own
# documented proof: a text-only prompt for a "2026 Toyota Crown" returned a generic
# crossover and it SHIPPED (CLAUDE.md). Plates are 4k - nano_banana_pro defaults to
# 1k and every early plate was built at that default without anyone noticing.
PLATES = {
    "crown": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
              "status": "NOT YET BUILT - build, LOOK at it, confirm the body is the "
                        "CROSSOVER (not the Sedan, not the Signia) before any video credit",
              "must_show": "Toyota Crown CROSSOVER (S16) RS Advance: raised sedan-SUV body "
                           "with a coupe-like falling roofline · full-width slim LED daytime "
                           "bar across the nose with a hammerhead front · body-colour upper "
                           "grille and a wide dark lower intake · black wheel-arch and rocker "
                           "cladding · 21-inch dark multi-spoke alloys · full-width rear light "
                           "bar · CROWN wordmark across the tailgate · two-tone black roof",
              "prompt":
              "Photograph of a 2023 Toyota Crown CROSSOVER RS Advance in dark metallic "
              "bronze-grey with a black roof, three-quarter front, parked on a coastal "
              "promenade at golden hour. Full-frame DSLR, 50mm, f/4, ISO 200, low sun as "
              "the key from camera left, sea haze behind. THE CAR MUST BE UNMISTAKABLY "
              "THIS MODEL: a RAISED SEDAN-SUV body, taller than a saloon but with a "
              "COUPE-LIKE FALLING ROOFLINE; a HAMMERHEAD nose carrying a FULL-WIDTH SLIM "
              "LED DAYTIME RUNNING BAR; a body-colour upper grille above a WIDE DARK LOWER "
              "INTAKE; BLACK PLASTIC CLADDING around the arches and along the rockers; "
              "21-INCH DARK MULTI-SPOKE ALLOYS filling the arches; a FULL-WIDTH REAR LIGHT "
              "BAR; the word CROWN spelled across the tailgate in widely spaced letters. "
              "REAL PHOTOGRAPH ARTEFACTS, not a render: true specular roll-off along the "
              "body creases, clear-coat orange peel in the paint, faint panel-gap shadows, "
              "fine dust catching the low sun, accurate reflections in the windows, the far "
              "side of the car slightly softer than the near side, neutral white balance, "
              "no HDR halos. "
              "Negative: CGI, videogame look, plastic-smooth paint, saloon proportions, "
              "boxy SUV proportions, invented badges, wrong wordmark, exaggerated flare."},

    "crown_int": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
                  "status": "NOT YET BUILT - interior geometry is a named subject too",
                  "must_show": "Crown Crossover cabin: twin 12.3-inch screens - instrument "
                               "cluster and a separate landscape centre display · low wide "
                               "fascia · rotary drive selector · two-tone black and tan hide",
                  "prompt":
              "Photograph of the interior of a 2023 Toyota Crown CROSSOVER RS Advance from "
              "the passenger side at golden hour, no people. Full-frame DSLR, 24mm, f/4, "
              "ISO 400, low sun entering from the side windows. THE CABIN MUST BE "
              "UNMISTAKABLY THIS MODEL: a LOW WIDE FASCIA carrying a 12.3-INCH DIGITAL "
              "INSTRUMENT CLUSTER and a SEPARATE 12.3-INCH LANDSCAPE CENTRE DISPLAY; a "
              "COMPACT ROTARY DRIVE SELECTOR on the console; two-tone black and tan "
              "leather; a hybrid system power meter reading in the cluster instead of a "
              "rev counter. REAL PHOTOGRAPH ARTEFACTS, not a render: real leather grain "
              "and stitch shadow, faint fingerprints on the display, dust in the low sun "
              "shaft, accurate reflections in the windows, natural depth of field, neutral "
              "white balance, no HDR halos. "
              "Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, "
              "generic dashboard, analogue rev counter, single small screen."},

    # Identity references, not lighting references (assets/nev/README.md). Passed on every
    # human shot so the BUILD stays consistent even though the face never resolves.
    "nev": {"job": None, "res": "4k", "ar": "4:5", "cr": 0,
            "status": "existing 3-angle face set, no generation needed",
            "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                              "assets/nev/face/profile_right.jpeg",
                              "assets/nev/face/front_calm.jpeg"],
            "must_show": "his head shape, hair and shoulder line ONLY - the face is "
                         "deliberately never lit in this build (his pick 2026-08-05)",
            "prompt": "(identity from photo references, not regenerated)"},
}

# ---------------------------------------------------------------- SHARED LOOK
# Deliberately carries NO word used as a linkage token - planqc 29 strips boilerplate
# before searching, and a token drawn from a block appended to all nine sources would
# be present on both sides of EVERY boundary. That is a vacuous pass wearing a tick.
_LOOK = (
    "Natural light only, no artificial fill, no colour gel. REAL FOOTAGE, NOT A RENDER: "
    "true specular roll-off along the body creases, clear-coat orange peel in the paint, "
    "faint panel-gap shadows, fine dust catching the low sun, accurate reflections in the "
    "windows, the far side of the car slightly softer than the near side, natural depth of "
    "field, neutral white balance, no HDR halos, no oversaturation. Unhurried camera - "
    "nothing whips, nothing shakes. "
    "Negative: CGI, videogame look, plastic-smooth surfaces, invented badges, exaggerated "
    "lens flare, crushed blacks, frantic camera movement, drift smoke."
)

# ---------------------------------------------------------------- SOURCES  (9 × 22.5cr)
# GOLDEN block: A B C D   ·   DUSK block: E F G   ·   BLUE block: H I
# The blocks are ordered by SHOT_TIME and never interleave - planqc 30 exists because
# KK v15 ran golden -> night -> DAYLIGHT -> sunset under a "6PM" card.
SOURCES = {
 "A": ("EVENT · out of the underpass shadow into the light", "#C98A3C", "EVENT", ["crown"],
       "Vertical 9:16. THE EVENT SHOT - one action, over inside 1.5 seconds, motion already "
       "happening at frame zero, no settle. Static camera low at kerb height beside a coastal "
       "carriageway. The Toyota Crown Crossover from the reference image is ALREADY MOVING as "
       "the clip opens, emerging from the deep shade of a concrete underpass into full "
       "low-angle golden backlight, its full-width LED daytime bar lit, and sweeping past the "
       "lens. The transition from shade to blazing backlight happens ACROSS the car's body as "
       "it travels. The rest of the clip is the empty lit carriageway it left. " + _LOOK),

 "B": ("coastal tracking, palms strobing", "#4E8C7A", "PAYOFF", ["crown"],
       "Vertical 9:16. THE SUSTAINED CRUISE - continuous motion, unbroken, no settle at the "
       "head. The Toyota Crown Crossover from the reference image driving at an easy pace "
       "along a palm-lined coastal carriageway at golden hour, tracked from a parallel "
       "vehicle, front three-quarter held steady. Palm shadows sweep rhythmically across the "
       "bodywork; the open bay and distant islands sit beyond the barrier. Camera moves "
       "smoothly with the car from first frame to last. " + _LOOK),

 "C": ("21-inch alloy at kerb height", "#8C6B3B", "EXTERIOR", ["crown"],
       "Vertical 9:16. Tight tracking move at kerb height along the flank of the Toyota "
       "Crown Crossover from the reference image, holding on the 21-INCH DARK MULTI-SPOKE "
       "ALLOY turning and the black rocker cladding above it, tarmac texture streaming "
       "past underneath in the low sun. " + _LOOK),

 "D": ("cabin, backlit driver, no face", "#6E5A8C", "HUMAN", ["nev", "crown_int"],
       "Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image, "
       "shot from the passenger side. The man from the FIRST reference images is in the "
       "driver's seat but he is a PURE SILHOUETTE against a blazing golden side window - his "
       "face is NEVER lit and NEVER resolves, only the outline of his head, hair and shoulder "
       "reads. Both hands rest easily at the bottom of the steering rim. In front of him the "
       "12.3-inch cluster shows a hybrid power meter, no rev counter. Backlit, high contrast, "
       "the sun doing all the work. " + _LOOK),

 "E": ("rear three-quarter, full-width light bar", "#B5563E", "EXTERIOR", ["crown"],
       "Vertical 9:16. Rear three-quarter of the Toyota Crown Crossover from the reference "
       "image on the coastal carriageway at dusk, slow arc around the rear corner. The "
       "FULL-WIDTH REAR LIGHT BAR is lit and is the brightest thing in frame; the CROWN "
       "wordmark across the tailgate reads clearly; the sky behind has gone amber to violet. "
       + _LOOK),

 "F": ("EVENT · the climb, the petrol engine wakes", "#C44B3A", "EVENT", ["crown"],
       "Vertical 9:16. THE SECOND EVENT - a state change, not a stunt. The Toyota Crown "
       "Crossover from the reference image climbing a rising coastal ramp at dusk, tracked "
       "from a parallel vehicle in front three-quarter. The car is ALREADY under load as the "
       "clip opens: the nose lifts slightly, the body settles back on its springs, the pace "
       "picks up decisively but without drama, and a faint heat shimmer rises off the rear "
       "of the car. Unhurried but unmistakably WORKING. " + _LOOK),

 "G": ("wide bay, the car small in it", "#3F6E8C", "EXTERIOR", ["crown"],
       "Vertical 9:16. Wide static high-angle looking down over the bay at dusk, the coastal "
       "carriageway curving through the lower third of frame, the Toyota Crown Crossover from "
       "the reference image SMALL in the frame travelling along it. Mount Kinabalu's range "
       "sits in the far haze; the last sun lies flat across the bay. The car is a moving "
       "detail inside a landscape, not the subject. " + _LOOK),

 "H": ("cabin at blue hour, key off", "#3E4A6E", "HUMAN", ["nev", "crown_int"],
       "Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image "
       "at blue hour, parked and still, shot from the passenger side. The man from the FIRST "
       "reference images sits in the driver's seat as a PURE SILHOUETTE against the pale "
       "blue-grey sky through the windscreen - his face is NEVER lit and NEVER resolves. He "
       "lifts one hand off the steering rim and lets it fall to his lap. The 12.3-inch "
       "cluster glow fades down to nothing on the fascia beside him. " + _LOOK),

 "I": ("parked at the seafront barrier, blue hour", "#2F5A72", "EXTERIOR", ["crown"],
       "Vertical 9:16. The Toyota Crown Crossover from the reference image parked and "
       "stationary at a seafront barrier at blue hour, side-on and slightly behind, the bay "
       "beyond it flat and going dim. Very slow drift of the camera, nothing else moves. The "
       "full-width rear light bar and the cabin glow are the only lit things; the sky is deep "
       "blue with the last band of orange on the horizon. " + _LOOK),
}

# ---------------------------------------------------------------- FRAMING (planqc 28)
# Two sources sharing a plate may not share a framing, or the model returns the plate's
# own composition. MEASURED on KK v1: five shots from three sources were one image.
FRAMING = {
    "A": "static low at kerb height, subject crossing the lens",
    "B": "parallel-vehicle tracking, front three-quarter held",
    "C": "tight tracking at wheel height along the flank",
    "D": "interior from passenger side, backlit silhouette, mid-close",
    "E": "slow arc around the rear corner, exterior",
    "F": "parallel-vehicle tracking on an incline, front three-quarter",
    "G": "wide static high angle, car small inside a landscape",
    "H": "interior from passenger side, parked, silhouette against windscreen",
    "I": "exterior side-and-behind, static, very slow drift",
}

# ---------------------------------------------------------------- TIMELINE
# 20 shots · 50 beats = 30.00s · 14 burst / 4 med / 2 hold
# Crops alternate 1.00 / 1.30 with a longest run of ONE. Hook and both holds are
# UNCROPPED - a 1.9x punch on 720p measured an 82% loss of sharpness, and the answer
# to repetition is more coverage, never deeper crops.
SHOTS = [
 ("A", 1.00, "med",   "shadow into gold - the car comes out already moving, and silent"),
 ("B", 1.30, "burst", "gold on the coast road, still silent"),
 ("C", 1.00, "burst", "the alloy turns, tarmac streaming, silent"),
 ("D", 1.15, "burst", "his hands settle on the rim, silent, the road runs ahead"),
 ("B", 1.00, "hold",  "THE CRUISE - the coast road opens out, gold everywhere"),
 ("C", 1.15, "burst", "kerb line runs under the alloy at road level, low gold light"),
 ("A", 1.30, "burst", "gold at its peak, flare raking across the glass"),
 ("D", 1.00, "burst", "the cluster reads hybrid, no revs - glass holding the last gold"),
 ("E", 1.30, "burst", "the light bar comes on as the gold dies"),
 ("G", 1.00, "burst", "wide bay, the coast road bends away, the last gold flat on it"),
 ("F", 1.15, "med",   "the road tilts up - the climb begins"),
 ("E", 1.00, "burst", "the light bar climbs away from the lens"),
 ("F", 1.00, "hold",  "THE ENGINE WAKES on the climb - the one loud moment"),
 ("G", 1.30, "burst", "wide - the car tops the rise, engine still working"),
 ("E", 1.15, "burst", "the light bar settles, engine falls quiet again"),
 ("I", 1.00, "burst", "quiet at the barrier, blue hour, the rim straightens"),
 ("H", 1.30, "burst", "he lifts his hand off the rim at the barrier"),
 ("I", 1.15, "med",   "still at the barrier, the bay going dark"),
 ("H", 1.00, "burst", "the cluster fades out - key off, the cabin goes dark"),
 ("I", 1.30, "med",   "dark bay, the car parked in it, nothing moves"),
]

# ---------------------------------------------------------------- THE CLOCK (planqc 30)
# Declared BEFORE the order was fixed, not retrofitted. Three contiguous blocks,
# monotonic through the ordered vocabulary, no jumps: golden(4) -> dusk(5) -> blue(6).
SHOT_TIME = (["golden"] * 8) + (["dusk"] * 7) + (["blue"] * 5)
TIME_JUMPS = {}

# ---------------------------------------------------------------- LINKAGE (planqc 24/29/31)
# GENERATED FROM THE FINAL SHOT ORDER, never authored beside it (craft ledger, 2026-08-05:
# KK's list described a video that was never assembled). Each entry is (kind, token, prose)
# and the TOKEN is present in the shot notes on BOTH sides of the boundary.
# 8 of 19 boundaries are CONSEQUENCE - B happens BECAUSE of A. Floor is 4.
LINKAGE = [
 ("light",       "gold",   "the car breaks into the gold -> the gold is the whole road"),
 ("sound",       "silent", "silent at speed -> still silent, the absence is established"),
 ("sound",       "silent", "the alloy turns in silence -> his hands rest in the same silence"),
 ("consequence", "road",   "his hands settle -> THE CRUISE: intent becomes the open road"),
 ("motion",      "road",   "the road opening -> the same road running under the alloy"),
 ("light",       "gold",   "low gold at ground level -> gold at its peak overhead"),
 ("object",      "glass",  "flare on the glass -> through that glass, the cluster reading"),
 ("consequence", "gold",   "the gold is going -> so the light bar comes on"),
 ("light",       "gold",   "the light bar against the dying gold -> the bay holding the last of it"),
 ("motion",      "road",   "the road bending away -> the road tilting up"),
 ("motion",      "climb",  "the climb begins -> the car climbing away from the lens"),
 ("consequence", "climb",  "the climb loads the car -> THE ENGINE WAKES because of it"),
 ("consequence", "engine", "the engine woke -> the car tops the rise on it"),
 ("sound",       "engine", "engine still working -> engine falling quiet"),
 ("consequence", "quiet",  "the engine goes quiet -> arrival, quiet at the barrier"),
 ("consequence", "rim",    "the car is stopped, rim straight -> he takes his hand off it"),
 ("subject",     "barrier","his hand leaves the rim -> the car still sitting at the barrier"),
 ("consequence", "dark",   "the bay going dark -> so he switches it off, the cabin goes dark"),
 ("consequence", "dark",   "the cabin dark -> the whole frame dark and still: nothing left running"),
]

CALLBACKS = [(0, 6), (15, 19)]      # the light-break re-hits; the barrier opens+closes blue

BAN_SPANS = {}                      # nothing measured yet - populate at ingest
DELOGO    = {}                      # nothing invented yet - populate if clipqc finds text

# ---------------------------------------------------------------- TRANSITIONS
# Blends KEPT at car level (18% declared) because a dissolve is how a cruise flows - the
# one piece of car grammar chill actively needs. travel_vlog's 0% would make this a
# holiday reel. 3 of 19 cuts = 15.8%, inside the [6,33] band, 400ms inside [240,560].
# NONE touches an EVENT shot (0, 6, 10, 12) - planqc 20 blocks that, and the WRX proved
# why: a blend on the hook dissolved the event itself.
BLEND_AFTER  = [4, 7, 14]           # cruise-hold exit · golden->dusk seam · dusk->blue seam
BLEND_KIND   = "dissolve"           # ADDED to tools/fx.py for this pillar: a true xfade
                                    # "fade". Every existing blend is a graphic wipe or
                                    # goes through BLACK (dip), which trips the blank-frame
                                    # gate legitimately. Neither is a chill transition.
BLEND_WIDTH  = 0.40

SFX_LEAD     = 0.22
IMPACT_AT    = [12]                 # hero_only: the ONE designed cut is into the engine wake
SUBDROP_AT   = [12]

# ---------------------------------------------------------------- SOUND
# sound_gate = diegetic. The powertrain IS the story, so the car's own audio is the spine
# and file 19 + 04 judge it BEFORE spend. Clip audio is generated and PAID FOR.
SOUND = {
    "bed":        "NOT YET SOURCED - and it CANNOT come from the library. All 25 tracks in "
                  "assets/bgm + assets/pillars/car_cinematic/bgm are 140-165 BPM drift phonk "
                  "(ledger 'travel vlog' L0 / 'car cinematic chill' L2). Required: 100.00 BPM "
                  "measured, warm, half-time, no cowbell, no distorted 808. Generate via "
                  "tools/bgmgen.py, then rhythm.py for BPM + grid OFFSET and trim so hit 1 "
                  "lands at t=0 (a generated bed once put its first transient at 163ms; "
                  "trimming took cut-to-music from ~34ms to a median 2.5ms).",
    "hero":       "THE PETROL ENGINE WAKING on the climb (shot 12). ONE hero sound per video "
                  "(file 04, law 4). Everything before it is tyre, wind and hybrid whine, so "
                  "the hero is earned by 20 seconds of its own absence rather than by volume.",
    "duck_shots": [12],
    "silence":    "shots 0-7 are the SILENCE - no combustion anywhere in the golden block, "
                  "only tyre roll, wind and a faint hybrid whine. Shot 19 returns to it with "
                  "the engine off: sea and nothing else. The video opens and closes on the "
                  "same absence, and the middle is what breaks it.",
    "layers":     "diegetic (per-shot gains below) + bed (sidechain-ducked under the hero, "
                  "hard-ducked at shot 12) + edit-sfx HERO ONLY - no whoosh on ordinary cuts. "
                  "A whoosh on every cut is the phonk signature and it is exactly what makes "
                  "a chill edit feel anxious.",
}

SFX_OVERLAYS = []                   # placement must be MEASURED off the real bed's gaps

FOLEY = {   # shot: gain_db. EVENT/PAYOFF must sit >= -6dB or the hero moments are not heard.
     0:  -3.0,   # A  tyre roll + wind + the shade-to-light whoosh of air. NO ENGINE.
     1:  -6.0,   # B  tyre hiss on open tarmac, the cruise's own sound
     2:  -8.0,   # C  tread and tarmac texture close up
     3: -14.0,   # D  cabin: cloth, a breath, hybrid whine floor
     4:  -4.0,   # B  THE CRUISE hold - road and wind carry the whole beat
     5: -10.0,   # C  kerb passing, tyre note
     6:  -6.0,   # A  wind swell on the light break
     7: -14.0,   # D  cabin quiet, faint inverter whine as the cluster reads
     8: -10.0,   # E  relay click, tyre note dropping as pace eases
     9: -12.0,   # G  distant surf and wind, the car barely audible
    10:  -6.0,   # F  load building - tyre note rises, no combustion YET
    11: -10.0,   # E  road note under the climb
    12:   0.0,   # F  HERO - the petrol engine wakes. The loudest instant in 30 seconds.
    13:  -6.0,   # G  engine carrying across the wide, heard at distance
    14: -10.0,   # E  engine backing off, returning to tyre
    15: -12.0,   # I  arrival - tyres on grit, then stillness
    16: -16.0,   # H  cabin, cloth, the hand leaving the rim
    17: -14.0,   # I  water and wind outside a stopped car
    18: -12.0,   # H  key off: the shutdown chime and the fade to nothing
    19: -18.0,   # I  the floor of the whole video - sea only
}

# ---------------------------------------------------------------- CARDS
CARD_Y     = 0.72                   # lower third. Never centre - the subject lives there.
CARD_STYLE = "fragment"             # profile style; card_max_words = 5
CARDS = [   # (text, first_shot, n_shots, kind)
    ("IT PULLS AWAY IN SILENCE", 0, 4, "cap"),      # the concept, stated over the silence
    ("2.4 TURBO HYBRID. 350PS.", 11, 3, "cap"),     # the receipt, landing ON the wake
    ("TOYOTA NEVER SOLD IT HERE", 14, 3, "cap"),    # the recond fact
    ("PRICE IN THE DM", 17, 3, "cta"),              # the withheld number is the engine
]
AI_LABEL_BURNED_IN = False          # platform AI toggle at upload - a HUMAN step, every time

# ---------------------------------------------------------------- GRADE
# Golden hour arrives graded. The prompt already asks for low natural sun, so applying a
# heavy curve on top is DOUBLE-GRADING: a past build pushed saturation to 1.70 chasing a
# number measured off finished compressed exports and took source 44.6 to 91.7.
GRADE_SAT    = 1.10
GRADE_BRI    = 0.0
TARGET_BLACK = 6.0                  # chill profile - NOT the car pillar's 2.0 crush
TARGET_SAT   = 80.0

# ---------------------------------------------------------------- CONTENT
CONTENT = {
    "claim":    "The Crown Crossover has never been sold new in Malaysia by UMW Toyota - "
                "every unit here is a Japan-market import through the recond channel. The "
                "2.4 RS Advance runs a turbocharged hybrid with a 350PS system output.",
    "verified": "NOT-SOLD-HERE: paultan.org 2024-03-04 covers a Crown Hybrid SPOTTED in "
                "Malaysia and asks whether it is coming at all; Malaysian availability is "
                "recond/used listings only (motortrader recond index, carlist). "
                "350PS: Carscoops 2022-07 JDM launch detail, broken down as 272PS engine + "
                "83PS + 81PS motors = 350PS / 261kW. SECONDARY SOURCE, not Toyota's own "
                "sheet - Toyota's global newsroom release describes the Dual Boost system "
                "but states NO output figure. Re-verify against a JDM spec sheet before "
                "this card ships if the number is challenged.",
    "twist":    "the product feature IS the story device. The video withholds combustion for "
                "20 seconds so that one engine start becomes the loudest thing in it. Nobody "
                "in the reference field can do this - a non-hybrid car has no silence to "
                "spend. The cards run as a sentence: SILENCE -> here is the number -> you "
                "cannot buy it here -> ask me.",
    "why_stop": "shot 0 is a light EVENT, not a tour - the car crosses from black shade into "
                "blazing backlight inside 1.8s, and the first card names the thing the ear "
                "is already noticing (silence) instead of describing the car. Under-2s hooks "
                "measured 23% higher completion. The stop-scroll bet is CONTRAST, not speed.",
    "judged":   "PENDING - hook AND story-arc panel (file 01/06) has NOT been run. This plan "
                "may not reach spend until it has, and a changed CONTENT block ALWAYS "
                "re-runs the panel (WRX lesson: planqc passing is NOT the panel passing).",
    "judged_cut": "PENDING - judges run on the finished cut, after verify.",
}

PREVIZ = {
    "sheet": None,
    "note":  "previz is sketch-grade and NEVER enters generation. Nev appears in panels D "
             "and H, so the sheet MUST carry the identity reference even though he is a "
             "silhouette - a text-only previz once invented a stranger and was correctly "
             "rejected ('the man is not nev').",
    "limit": "a still sheet CANNOT depict shot 0 (a car crossing a light boundary while "
             "moving) or shot 12 (an engine waking). Both are judged at the PROBE, never "
             "at previz. Do not reroll sketches to chase them.",
}

# ---------------------------------------------------------------- THE MASTERMIND LOOP
LESSONS_ACK = {
    "general craft":       64,      # pillar-independent: measurement, tooling, process
    "car cinematic chill":  5,      # this dialect's genre lessons (created with this plan)
    "car cinematic":       15,      # the parent pillar - not required by planqc, read anyway
}

PREMORTEM = [
    ("WRONG CAR FROM A TEXT-ONLY PROMPT. This exact model is the repo's documented failure "
     "- '2026 Toyota Crown' returned a generic crossover and shipped an 87cr build "
     "(CLAUDE.md). The Crown name covers four different bodies (Crossover / Sedan / Sport / "
     "Signia) and the wrong one poisons all nine sources.",
     "4k plate built FIRST and LOOKED AT, with the Crossover's specific geometry spelled out "
     "in must_show (raised body + falling roofline + hammerhead DRL bar + arch cladding + "
     "21-inch alloys + full-width rear bar). Gavril confirms the body before any video "
     "credit. Every source prompt cites the plate."),

    ("CHILL BECOMES A SLIDESHOW. The first Crown build already failed this way - 90 BPM "
     "marimba under 1.33-2.67s shots (ledger 'car cinematic' L6/L9), and KK v15 measured 9 "
     "of 20 shots under 0.6 optical flow with 0 consequence boundaries.",
     "the dialect declares its own numbers instead of drifting: 1.2s median, 38 cuts/min, "
     "two holds only, both on a PAYOFF/EVENT. The spine is a consequence chain with 8 typed "
     "consequence boundaries, and the one event is a STATE CHANGE inside the car "
     "(ledger 'car cinematic chill' L4) rather than a stunt chill cannot host."),

    ("THE BED COMES FROM THE PHONK LIBRARY. Every one of the 25 tracks is 140-165 BPM drift "
     "phonk (ledger 'travel vlog' L0). Reaching for it here repeats the original Crown's "
     "'90 BPM marimba under a car edit' error in the opposite direction.",
     "SOUND['bed'] states outright that the library is unusable and names the requirement "
     "(100.00 BPM measured, warm, half-time, no cowbell). rhythm.py measures BPM and grid "
     "OFFSET and the bed is trimmed so hit 1 lands at t=0 before any cut is placed."),

    ("BEAT MATH COPIED FROM A CAR PLAN. {burst:2, med:4, hold:8} at 100 BPM makes a 4.8s "
     "hold - 3.7x this dialect's median and 16% of the video on one image (ledger 'car "
     "cinematic chill' L3, measured first on the travel_vlog plan).",
     "BEATS recomputed for 100 BPM as {2,3,5} = 1.20/1.80/3.00s. planqc 2b prints the "
     "longest shot as a multiple of the genre median so the bet is SEEN, not discovered "
     "in the finished cut."),

    ("CLIPQC REJECTS THE GOLDEN-HOUR CLIPS AT 22.5cr EACH. car_cinematic's brightness band "
     "is [18,90] - a MEASURED NIGHT band. Daylight footage measures 142-165 and a "
     "golden/dusk frame measured 51.3 on 2026-08-05.",
     "car_cinematic_chill declares its own band [35,190] and labels it PROVISIONAL out loud. "
     "Deliberately wide because the costs are asymmetric: a wrong reject burns 22.5cr, a "
     "wrong accept costs one eye pass. RE-DERIVE from the first 9 real clips at ingest."),

    ("MOTION-KIND LINKAGES ON CLIPS THAT DO NOT MOVE. Five KK boundaries were built on verbs "
     "(walking, rising, drifting) and the clips measured 0.40-0.51 optical flow - neither "
     "side moved (craft ledger 2026-08-05).",
     "only 3 of 19 boundaries are kind 'motion' and all three join shots whose prompts "
     "specify continuous camera or vehicle travel. clipqc's delivered-window motion floor "
     "(0.6 for this dialect, PROVISIONAL) is checked per clip at ingest, before assembly."),

    ("DOUBLE-GRADING THE GOLDEN HOUR. The prompts ask for low natural sun, so the footage "
     "ARRIVES graded; a past build pushed saturation to 1.70 and took source 44.6 to 91.7, "
     "and shot_match once moved a shot by 72.6 luma on an open-loop gain formula.",
     "GRADE_SAT 1.10 as a starting point to MEASURE from, TARGET_BLACK 6.0 not the car's "
     "2.0 crush, shot_match_max_move 14.0 luma in neighbour mode so the intended "
     "golden->blue arc is never flattened toward a global median."),
]


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


PROBE_FIRST = "A"   # the hook tests the plate, the light break and the motion floor at once
CLIPS = {}
CLIP_BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/"
