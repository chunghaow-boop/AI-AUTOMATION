#!/usr/bin/env python3
"""
CROWN_PLAN v2 — Toyota Crown Crossover 2.4 RS Advance (S16) · chill coastal cinematic · Nev.

v1 passed planqc 34/34 and FAILED both pre-spend panels. v2 exists to close the P0s in
`projects/crown/QC-PANEL-2026-08-05.md`. What changed and why:

  P0-1  AUDIO DIRECTION IN EVERY PROMPT. v1 had none - not one audio word in nine prompts,
        in a video whose entire subject is a sound. FOLEY is a mix-gain table; it cannot
        remove combustion the model generated into a clip. Six prompts now carry
        "NO ENGINE, NO EXHAUST, NO COMBUSTION" verbatim.
  P0-2  F IS SPLIT into F_load and F_wake. One clip cannot be both engine-free (the ramp)
        and engine-present (the wake). This is why the build is now 11 clips, not 9.
  P0-3  F_wake OPENS IN SILENCE and stages the catch ON CAMERA. v1 said the car was
        "ALREADY under load as the clip opens" - a state change that has already happened
        cannot be heard happening. The EVENT no-settle convention is DELIBERATELY broken
        for this one shot, and that is declared, not smuggled.
  P0-4  generate_audio DECLARED on every source (wrx.py stated it; v1 did not).
  P0-5  TWO-STATE PROMPTS + declared windows for the sources reused across the silence/
        engine boundary (E, G).
  P0-6  NEV NOW CAUSES THE STORY. v1 had him acted upon in all four of his shots and the
        HILL woke the engine - the identical defect that killed KK v15. NEW source J: his
        silhouette commits, and the engine answers. NEW shot 18: his hand kills the cabin.
        Boundaries 9 and 18 are typed consequence with him as the agent.
  P0-7  350PS RETRACTED. The recorded derivation (272+83+81) sums to 436, not 350; hybrid
        output is not additive and Toyota publishes no figure. No number ships on a card
        until a JDM spec sheet confirms it. J4 holds an absolute veto on wrong specs.
  P1-1  THE HERO NOW LANDS AT 13.80s, not 17.40s. Two golden repeats deleted and the
        cruise hold demoted; the reclaimed beats went to the dusk half.
  P1-2  THE CAR IS NAMED ON SCREEN. Card 1 was "IT PULLS AWAY IN SILENCE" - four cards
        and not one noun.

Title readback (2026-08-05, unchanged): Crown CROSSOVER 2.4 RS Advance (his pick) ·
car_cinematic_chill dialect (his pick) · golden into blue hour (my call, he deferred) ·
Nev SILHOUETTE ONLY, face never resolves (his pick).

STORY, AS A SENTENCE:
  A man leaves the city with the engine off - the Crown pulls away in silence - and drives
  the coast until the light runs out; when the road tilts up HE ASKS FOR THE ENGINE and it
  answers, and at the water HIS HAND SWITCHES IT OFF and the day ends.

The difference from v1 is one word: HE. v1's spine was a car and a sunset with a passenger
in it. Both panels found the same hole independently.

THE UPGRADE OVER THE FIELD: every edit in assets/refs/car_cinematic sells NOISE. This one
sells the absence of it and spends twenty seconds of silence to buy one engine start - which
a combustion car structurally cannot do. v1 only CLAIMED that, because no prompt asked for
it. v2 writes it into the prompts, which is the only place it can be true.
"""

PROJECT   = "Toyota Crown Crossover 2.4 RS Advance · chill coastal cinematic · Nev"
PILLAR    = "car_cinematic_chill"
GEN_MODE  = "coverage"
MODE_ABC  = "hero"                  # panel D15: the Assembly Table needs this declared
BPM       = 100.0
BEAT      = 60.0 / BPM              # 0.600s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 30.0                    # 50 beats

BEATS = {"burst": 2, "med": 3, "hold": 5}       # 1.20 / 1.80 / 3.00s at 100 BPM

# Audio is the spine of this build, so it is declared once, loudly, at the top.
GENERATE_AUDIO = True               # ON for all sources. A silent clip is a dead 22.5cr.

# ---------------------------------------------------------------- PLATES
PLATES = {
    "crown": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
              "status": "NOT YET BUILT - build, LOOK at it, Gavril confirms the BODY is the "
                        "CROSSOVER (not Sedan, not Signia) before any video credit",
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
# Carries NO word used as a linkage token, and NO audio word - the audio direction is
# per-source on purpose, because six sources must forbid combustion and three must stage it.
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

# The silence contract, appended verbatim to every source that must arrive engine-free.
# Without this the model's prior for "car on a coastal road" is an engine note and it will
# supply one at 22.5cr a time, with no free way back.
_SILENT = (" AUDIO: NO ENGINE, NO EXHAUST, NO COMBUSTION OF ANY KIND - the car is running "
           "on electric drive and is silent. No music, no voiceover, no dialogue.")

# ---------------------------------------------------------------- SOURCES  (11 × 22.5cr)
# GOLDEN: A B C D   ·   DUSK: E G F_load J F_wake   ·   BLUE: H I
SOURCES = {
 "A": ("EVENT · out of the underpass shadow into the light", "#C98A3C", "EVENT", ["crown"],
       "Vertical 9:16. THE EVENT SHOT - one action, over inside 1.5 seconds, motion already "
       "happening at frame zero, no settle. Static camera low at kerb height beside a coastal "
       "carriageway. The Toyota Crown Crossover from the reference image is ALREADY MOVING as "
       "the clip opens, emerging from the deep shade of a concrete underpass into full "
       "low-angle golden backlight, its full-width LED daytime bar lit, and sweeping past the "
       "lens. The transition from shade to blazing backlight happens ACROSS the car's body as "
       "it travels. The rest of the clip is the empty lit carriageway it left. " + _LOOK +
       _SILENT + " Only the hiss of tyres on warm tarmac, the rush of displaced air as the "
       "body passes the lens, and the change in room tone as it leaves the concrete underpass "
       "for open coastal air. Ambience: distant surf, faint."),

 "B": ("coastal tracking, palms strobing", "#4E8C7A", "PAYOFF", ["crown"],
       "Vertical 9:16. THE SUSTAINED CRUISE - continuous motion, unbroken, no settle at the "
       "head. The Toyota Crown Crossover from the reference image driving at an easy pace "
       "along a palm-lined coastal carriageway at golden hour, tracked from a parallel "
       "vehicle, front three-quarter held steady. Palm shadows sweep rhythmically across the "
       "bodywork; the open bay and distant islands sit beyond the barrier. Camera moves "
       "smoothly with the car from first frame to last. " + _LOOK + _SILENT +
       " A steady, unchanging tyre hiss on open tarmac and a soft wind wash along the body "
       "for the whole clip. Ambience: open bay air and faint surf."),

 "C": ("21-inch alloy at kerb height", "#8C6B3B", "EXTERIOR", ["crown"],
       "Vertical 9:16. Tight tracking move at kerb height along the flank of the Toyota "
       "Crown Crossover from the reference image, holding on the 21-INCH DARK MULTI-SPOKE "
       "ALLOY turning and the black rocker cladding above it, tarmac texture streaming "
       "past underneath in the low sun. " + _LOOK + _SILENT +
       " Close tyre contact - tread pattern rolling on coarse tarmac, grit ticking in the "
       "tread, the note changing as the surface changes under the wheel."),

 "D": ("cabin at golden hour, backlit driver, no face", "#6E5A8C", "HUMAN",
       ["nev", "crown_int"],
       "Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image, "
       "shot from the passenger side. The man from the FIRST reference images is in the "
       "driver's seat but he is a PURE SILHOUETTE against a blazing golden side window - his "
       "face is NEVER lit and NEVER resolves, only the outline of his head, hair and shoulder "
       "reads. Both hands rest easily at the bottom of the steering rim. In front of him the "
       "12.3-inch cluster shows a hybrid power meter, no rev counter. Backlit, high contrast, "
       "the sun doing all the work. " + _LOOK + _SILENT +
       " The cabin drop-out: outside noise distant and damped, the cabin still. Faint "
       "seat-cloth and leather movement as his hands settle on the rim, one quiet breath, a "
       "muted tyre rumble through the floor, a faint high electric whine rising with speed."),

 "E": ("rear three-quarter, full-width light bar", "#B5563E", "EXTERIOR", ["crown"],
       "Vertical 9:16. Rear three-quarter of the Toyota Crown Crossover from the reference "
       "image on the coastal carriageway at dusk, slow arc around the rear corner. The "
       "FULL-WIDTH REAR LIGHT BAR is lit and is the brightest thing in frame; the CROWN "
       "wordmark across the tailgate reads clearly; the sky behind has gone amber to violet. "
       + _LOOK +
       " AUDIO, TWO STATES: for the FIRST HALF of the clip there is NO ENGINE, NO EXHAUST, "
       "NO COMBUSTION - only tyre note and wind. In the SECOND HALF a petrol engine is heard "
       "receding into the distance, backing off and handing back to tyre roll. No music, no "
       "voiceover, no dialogue."),

 "G": ("wide bay, the car small in it", "#3F6E8C", "EXTERIOR", ["crown"],
       "Vertical 9:16. Wide static high-angle looking down over the bay at dusk, the coastal "
       "carriageway curving through the lower third of frame AND RISING TO A CREST at the far "
       "side, the Toyota Crown Crossover from the reference image SMALL in the frame "
       "travelling along it. Offshore island ridgelines sit low in the haze; the last sun "
       "lies flat across the water. The car is a moving detail inside a landscape, not the "
       "subject. " + _LOOK +
       " AUDIO, TWO STATES: heard from far away across open water - wind and distant surf "
       "dominate throughout. In the FIRST HALF no combustion is present at all. In the SECOND "
       "HALF a petrol engine is faintly audible at long distance, thin and small inside the "
       "landscape. No music, no voiceover, no dialogue."),

 "F_load": ("EVENT · the ramp, still electric", "#D0763A", "EVENT", ["crown"],
       "Vertical 9:16. The Toyota Crown Crossover from the reference image approaching and "
       "starting a rising coastal ramp at dusk, tracked from a parallel vehicle, front "
       "three-quarter. The road visibly tilts upward through the shot and the car keeps its "
       "easy pace onto it - no acceleration yet, no drama, the body level. This clip is the "
       "SETUP for the shot that follows and must not contain the event itself. " + _LOOK +
       _SILENT + " Tyre note and wind only, with a faint electric whine holding steady. The "
       "quiet immediately before something happens."),

 "J": ("cabin at dusk, the decision", "#7C4F8C", "HUMAN", ["nev", "crown_int"],
       "Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image "
       "at dusk, shot from the passenger side, tight. The man from the FIRST reference images "
       "is a PURE SILHOUETTE against the violet windscreen - his face is NEVER lit and NEVER "
       "resolves. He is still for a beat, then his forearm and shoulder drop and set as he "
       "commits weight through his right foot, and the 12.3-inch cluster's power meter needle "
       "swings hard across into its power band. HIS MOVEMENT COMES FIRST, the meter answers "
       "it. Nothing else in frame moves. " + _LOOK +
       " AUDIO: near silence - the cabin drop-out at its deepest, only faint cloth and a "
       "thin electric whine. In the last third the whine begins to rise. NO PETROL ENGINE "
       "YET - it must not have started inside this clip. No music, no voiceover, no dialogue."),

 "F_wake": ("EVENT · the engine catches", "#C44B3A", "EVENT", ["crown"],
       "Vertical 9:16. THE HERO. The Toyota Crown Crossover from the reference image climbing "
       "the rising coastal ramp at dusk, tracked from a parallel vehicle in front "
       "three-quarter. THE CLIP OPENS STILL SILENT AND STILL ON ELECTRIC DRIVE for the first "
       "half-second - then the petrol engine CATCHES and the car takes load: the nose lifts, "
       "the body settles back on its springs, the pace hardens decisively but without drama, "
       "and heat shimmer rises off the rear. THE TRANSITION FROM SILENT TO RUNNING HAPPENS ON "
       "CAMERA, inside this clip. Unhurried but unmistakably WORKING. " + _LOOK +
       " AUDIO - THIS IS THE ONLY COMBUSTION SOUND IN THE ENTIRE FILM: the clip opens in near "
       "silence with tyre roll and wind alone, then the petrol engine CATCHES - a brief crank, "
       "the four-cylinder fires, and the note rises and hardens under load as the ramp "
       "steepens, with turbo spool behind it. The transition from silent to running is the "
       "loudest event in the clip. Ambience: open coastal air. No music, no voiceover, no "
       "dialogue."),

 "H": ("cabin at blue hour, key off", "#3E4A6E", "HUMAN", ["nev", "crown_int"],
       "Vertical 9:16. Interior of the Toyota Crown Crossover from the LAST reference image "
       "at blue hour, parked and still, shot from the passenger side. The man from the FIRST "
       "reference images sits in the driver's seat as a PURE SILHOUETTE against the pale "
       "blue-grey sky through the windscreen - his face is NEVER lit and NEVER resolves. His "
       "hand leaves the steering rim, reaches, and PRESSES the start-stop button; the "
       "12.3-inch cluster and the fascia lighting die out in the same movement. HIS ACTION "
       "CAUSES THE DARKNESS - the lights do not simply fade on their own. " + _LOOK +
       " AUDIO: a parked, still cabin. Seat-cloth and leather as he moves. The car's "
       "electronics power down - a single soft shutdown chime, then the last relay settles "
       "and the cabin goes completely quiet. Outside, faint water and wind, far away and "
       "damped. NO ENGINE, NO IDLE. No music, no voiceover, no dialogue."),

 "I": ("parked at the seafront barrier, blue hour", "#2F5A72", "EXTERIOR", ["crown"],
       "Vertical 9:16. The Toyota Crown Crossover from the reference image parked and "
       "stationary at a seafront barrier at blue hour, side-on and slightly behind, the flat "
       "seafront promenade and the bay beyond it going dim. Very slow drift of the camera; "
       "the water moves, the car does not. The full-width rear light bar and the cabin glow "
       "are the only lit things; the sky is deep blue with the last band of orange on the "
       "horizon. " + _LOOK +
       " AUDIO: a stopped car - nothing mechanical, nothing running. Only water against the "
       "seawall and a low steady wind. The quietest sound in the whole piece. NO ENGINE, NO "
       "IDLE. No music, no voiceover, no dialogue."),
}

# ---------------------------------------------------------------- FRAMING (planqc 28)
FRAMING = {
    "A":      "static low at kerb height, subject crossing the lens",
    "B":      "parallel-vehicle tracking, front three-quarter held",
    "C":      "tight tracking at wheel height along the flank",
    "D":      "interior from passenger side, backlit silhouette, mid-close",
    "E":      "slow arc around the rear corner, exterior",
    "G":      "wide static high angle, car small inside a landscape",
    "F_load": "parallel-vehicle tracking onto an incline, front three-quarter, level",
    "J":      "interior from passenger side, TIGHT on shoulder and forearm, silhouette",
    "F_wake": "parallel-vehicle tracking on the incline, front three-quarter, car loading",
    "H":      "interior from passenger side, parked, silhouette, hand to console",
    "I":      "exterior side-and-behind, static, very slow drift",
}

# ---------------------------------------------------------------- TIMELINE
# 20 shots · 50 beats = 30.00s · 14 burst / 4 med / 2 hold
# THE HERO NOW LANDS AT 13.80s (v1: 17.40s). Deleted v1's two golden repeats and demoted
# the cruise hold; the six reclaimed beats went to the dusk half where the story is.
SHOTS = [
 ("A",      1.00, "med",   "shadow into gold - the car comes out already moving, and silent"),
 ("B",      1.30, "burst", "gold on the coast road, still silent"),
 ("C",      1.00, "burst", "the alloy turns, tarmac streaming, silent"),
 ("D",      1.15, "burst", "his hands settle on the rim, silent, the road runs ahead"),
 ("B",      1.00, "med",   "the coast road opens out, gold everywhere, nothing driving it"),
 ("C",      1.15, "burst", "kerb line runs under the alloy at road level, low gold light"),
 ("E",      1.00, "burst", "the light bar comes on as the gold dies"),
 ("G",      1.30, "burst", "wide bay, the coast road bends away, the last gold flat on it"),
 ("F_load", 1.15, "med",   "the road tilts up into the ramp - still electric, still no engine"),
 ("J",      1.00, "burst", "HIS DECISION - the silhouette commits, foot down on the ramp"),
 ("F_wake", 1.00, "hold",  "THE ENGINE WAKES on the ramp because he asked for it"),
 ("E",      1.15, "burst", "the light bar climbs away from the ramp, working now"),
 ("G",      1.00, "burst", "wide - the car small, still climbing, the note carrying over the bay"),
 ("F_wake", 1.30, "burst", "over the crest the note hardens and holds, steady under load"),
 ("E",      1.30, "burst", "the light bar eases, the load falls away and it goes quiet again"),
 ("I",      1.00, "burst", "quiet at the barrier, blue hour, nothing running"),
 ("H",      1.30, "burst", "he sits, hand still on the rim at the barrier"),
 ("I",      1.15, "med",   "the bay from outside the barrier, the cabin still lit"),
 ("H",      1.00, "hold",  "HIS HAND KILLS IT - key off, the cabin goes dark"),
 ("I",      1.30, "burst", "dark bay, the car parked in it, nothing running"),
]

# ---------------------------------------------------------------- THE CLOCK (planqc 30)
SHOT_TIME = (["golden"] * 6) + (["dusk"] * 9) + (["blue"] * 5)
TIME_JUMPS = {}

# ---------------------------------------------------------------- LINKAGE (24/29/31)
# GENERATED FROM THE FINAL SHOT ORDER after the v2 re-cut, never carried over from v1.
# 8 of 19 are CONSEQUENCE, and the two that matter - boundary 9 (he asks, the engine
# answers) and boundary 18 (his hand kills the cabin) - now have THE MAN as the agent.
# v1's spine was a car and a sunset; both panels found the same hole.
LINKAGE = [
 ("light",       "gold",   "the car breaks into the gold -> the gold is the whole road"),
 ("sound",       "silent", "silent at speed -> still silent, the absence is established"),
 ("sound",       "silent", "the alloy turns in silence -> his hands rest in the same silence"),
 ("consequence", "road",   "his hands settle -> the road opens out in front of that decision"),
 ("motion",      "road",   "the road opening -> the same road running under the alloy"),
 ("consequence", "gold",   "the gold is dying -> so the light bar comes on"),
 ("light",       "gold",   "the light bar against the dying gold -> the bay holding the last of it"),
 ("motion",      "road",   "the road bending away -> the road tilting up into the ramp"),
 ("consequence", "ramp",   "the ramp arrives -> HE COMMITS to it, foot down"),
 ("consequence", "ramp",   "he asked for it on the ramp -> THE ENGINE ANSWERS. the hero"),
 # 'engine' is UNUSABLE as a carry token here and the gate was right to say so: the word
 # appears in all eleven prompts, because six of them forbid it and three stage it. A token
 # present on both sides of every boundary proves nothing. Retyped against what is actually
 # written into these four shots.
 ("consequence", "ramp",  "the engine woke on the ramp -> the car climbs away from it"),
 ("motion",      "climb", "climbing away -> still climbing, seen small across the bay"),
 ("sound",       "note",  "the note carrying at distance -> the note close and hardened"),
 ("consequence", "load",  "the load ends at the crest -> so it goes quiet again"),
 ("consequence", "quiet",  "the engine goes quiet -> arrival, quiet at the barrier"),
 ("subject",     "barrier","the car at the barrier -> him inside it at the same barrier"),
 ("object",      "cabin",  "his hand on the rim -> the lit cabin seen from outside"),
 ("consequence", "cabin",  "the cabin is still lit -> HIS HAND KILLS IT"),
 ("consequence", "dark",   "he switched it off -> the whole frame dark, nothing left running"),
]

CALLBACKS = [(0, 4), (15, 19)]      # the cruise opens+re-hits; the barrier opens+closes blue

BAN_SPANS = {}
DELOGO    = {}

# ---------------------------------------------------------------- TRANSITIONS
# 3 of 19 = 15.8%, inside [6,33]. NONE touches an EVENT shot (0, 8, 10, 13).
# P1-8: the dissolve is declared as an OVERLAP, not a subtraction - v1's three 400ms blends
# silently made the deliverable 28.80s and pushed the hero 0.80s (1.33 beats) off the music
# grid, while planqc checked the pre-blend total and passed.
BLEND_AFTER    = [5, 14, 17]        # golden->dusk seam · dusk->blue seam · into the key-off hold
BLEND_KIND     = "dissolve"
BLEND_WIDTH    = 0.40
BLEND_AS_OVERLAP = True             # segments extend BLEND_WIDTH into the transition so the
                                    # delivered total stays 30.00s and every cut stays on the
                                    # 0.600s grid. If the engine can only subtract, add 0.40s
                                    # of source window at shots 5, 14 and 17 instead.

SFX_LEAD   = 0.22                   # DESIGNED transients only - a whoosh resolves on the cut
HERO_SYNC  = 0.00                   # the DIEGETIC engine lands ON the cut. 220ms of lead on
                                    # an engine catching is a mis-sync, not anticipation.
IMPACT_AT  = [10]                   # hero_only: the one designed cut in the video
SUBDROP_AT = []                     # P2-8: v1 put IMPACT and SUBDROP on the same index and
                                    # the doc generator's if/elif silently swallowed the sub.
                                    # Folded into the hero's body layer instead.

# ---------------------------------------------------------------- SOUND
SOUND = {
    "generate_audio": "ON for all 11 sources. The diegetic spine IS the clip audio; a silent "
                      "clip is a dead 22.5cr. v1 never declared this.",
    "bed":        "NOT YET SOURCED - and it CANNOT come from the library. All 25 tracks in "
                  "assets/bgm + assets/pillars/car_cinematic/bgm are 140-165 BPM drift phonk. "
                  "Required: 100.00 BPM measured, warm, half-time, no cowbell, no distorted "
                  "808. Generate via tools/bgmgen.py, then rhythm.py for BPM + grid OFFSET "
                  "and trim so hit 1 lands at t=0.",
    "bed_map":    {"in": "shot 1 @1.80s, fading up over one beat from -inf - the video OPENS "
                         "with no bed at all, because the card says SILENCE and a bed under "
                         "it makes the card a lie",
                   "level_silence_block": "-9dB under nominal through shots 1-9",
                   "duck": "to -inf across shot 9, the near-silence",
                   "hero": "nominal from shot 10",
                   "out": "fade to -inf across shot 18, fully silent from 28.80s",
                   "tail": "shot 19 is diegetic sea only - no bed"},
    "hero":       "THE PETROL ENGINE CATCHING on the ramp (shot 10, 13.80s), CAUSED by his "
                  "commit in shot 9. ONE hero sound per video (file 04, law 4).",
    "hero_layers": {"transient": "the crank/catch from F_wake's own audio",
                    "body":      "the 2.4T load note, 150-1500Hz, from F_wake - the sub "
                                 "energy folded in here rather than as a separate drop",
                    "tail":      "exhaust decay carried under shot 11"},
    "near_silence": "shot 9 (12.60-13.80s) - the diegetic floor drops to -24dB and the bed "
                    "ducks to -inf over the last 0.40s. THIS is the drop-out the engine "
                    "breaks. v1 had no near-silence at all and called the opening block the "
                    "silence instead (file 19 doctrine 8 / file 04 law 5).",
    "duck_shots": [10],          # the key planqc 19 reads. Detail below, not instead.
    "duck":       {"shots": [10], "mode": "sidechain", "thr": 0.06, "ratio": 6,
                   "release_ms": 120, "depth_db": -18,
                   "starts_at": "0.40s BEFORE the shot-10 cut, i.e. before SFX_LEAD",
                   "recovers": "over shot 11",
                   "why": "binary hard-duck windows STEP 12dB in/out and he heard it as "
                          "'music breaks at cuts'. One smooth sidechain only."},
    "silence":    "shots 0-9 (0.00-13.80s) carry NO COMBUSTION - written into the prompts, "
                  "not just the gain map. Shot 19 returns to it with the engine off. The "
                  "video opens and closes on the same absence and the middle breaks it.",
    "layers":     "diegetic (per-shot gains below) + bed (one smooth sidechain, mapped above) "
                  "+ edit-sfx HERO ONLY - no whoosh on ordinary cuts.",
}

MIX = {   # P1-10: v1 had no mix call at all. File 19's required deliverable.
    "target_lufs":   "-7 to -9 integrated",
    "true_peak":     "-1.0 dBTP",
    "channels":      2,          # MONO is the measured failure that created seat 19
    "spectrum":      "body 150-1500Hz ~45% · himid ~18% · presence ~24% · sub+low ~8% · "
                     "air 10-20k ~4% · centroid ~2400Hz",
    "room":          "cabin shots (D, J, H) damped, short tail. Coast shots open.",
    "bed_highpass":  "40Hz",
    "note":          "sub_bass_pct [25,65] is INHERITED PHONK TASTE and is wrong for this "
                     "dialect - a 2.4 turbo four lives at 200-800Hz and 1-3k. Measure "
                     "against the file 19 spectrum, not the inherited band, and re-derive "
                     "the profile field at first ingest.",
}

SFX_OVERLAYS = []   # under edit_sfx=hero_only this list may ONLY contain entries at shot 10

# FOLEY, P1-5. v1 gave the hero 3dB over the hook and called it "the loudest instant in 30
# seconds". Perceived doubling needs ~10dB. The gated shots sit AT the -6 floor, everything
# else descends, and the hero is +12 over the floor.
# PROVISIONAL - re-derive every value against the generated bed's measured RMS before
# assembly (craft L16: when the bed changes, re-calibrate every layer gain against it).
FOLEY = {
     0:  -6.0,   # A       tyre roll + displaced air. NO ENGINE.
     1:  -6.0,   # B       tyre hiss on open tarmac
     2: -12.0,   # C       tread and tarmac texture
     3: -18.0,   # D       cabin drop-out: cloth, a breath, floor rumble
     4:  -6.0,   # B       the cruise, road and wind carry it
     5: -13.0,   # C       kerb passing
     6: -15.0,   # E       tyre note easing, first half of E (no combustion)
     7: -18.0,   # G       distant surf and wind, car barely audible
     8:  -6.0,   # F_load  tyre note under load-free climb - still no combustion
     9: -24.0,   # J       NEAR-SILENCE. The floor before the twist.
    10:  +6.0,   # F_wake  HERO - the catch. +12 over the gated floor.
    11:  -8.0,   # E       second half of E: engine climbing away
    12: -10.0,   # G       second half of G: engine thin at distance
    13:  -6.0,   # F_wake  the note hardened, held under load
    14: -14.0,   # E       engine backing off, tyre returning
    15: -18.0,   # I       stillness - water and wind at a stopped car
    16: -20.0,   # H       cabin, cloth, the hand on the rim
    17: -21.0,   # I       water and wind outside a stopped car
    18: -22.0,   # H       the shutdown chime and the last relay
    19: -26.0,   # I       the global floor - sea only
}

# ---------------------------------------------------------------- CARDS
CARD_Y     = 0.72
CARD_STYLE = "fragment"
CARDS = [   # (text, first_shot, n_shots, kind) - card_max_words = 5
    ("CROWN. PULLING AWAY IN SILENCE", 0, 4, "cap"),   # P1-2: v1 named the car on ZERO cards
    ("HE ASKS. IT WAKES.",             9, 3, "cap"),   # lands ON the decision and the hero
    ("NEVER SOLD NEW IN MALAYSIA",    14, 3, "cap"),   # P1-3: matches CONTENT["claim"] exactly
    ("RECOND UNIT. ASK THE PRICE",    17, 3, "cta"),   # gives the fact AND the ask
]
AI_LABEL_BURNED_IN = False

# ---------------------------------------------------------------- GRADE
GRADE_SAT    = 1.10
GRADE_BRI    = 0.0
TARGET_BLACK = 6.0
TARGET_SAT   = 80.0

# ---------------------------------------------------------------- CONTENT
CONTENT = {
    "claim":    "The Crown Crossover has never been sold new in Malaysia by UMW Toyota - "
                "every unit here is a Japan-market import through the recond channel.",
    "verified": "paultan.org 2024-03-04 covers a Crown Hybrid SPOTTED in Malaysia and asks "
                "whether it is coming at all; Malaysian availability is recond/used listings "
                "only (motortrader recond index, carlist). Card 3 says NEVER SOLD NEW IN "
                "MALAYSIA, which is exactly this claim and not the wider 'Toyota never sold "
                "it here' - Toyota has sold Crown-nameplate cars here historically and J4 "
                "would roast the wider version. "
                "POWER FIGURE RETRACTED 2026-08-05: v1 shipped a card reading 350PS on a "
                "derivation (272+83+81) that sums to 436. Hybrid system output is not "
                "additive and Toyota's own release states no figure. NO NUMBER SHIPS until a "
                "JDM spec sheet confirms one.",
    "twist":    "the product feature IS the story device, and the MAN operates it. The video "
                "withholds combustion for 13.8 seconds so that one engine start becomes the "
                "loudest thing in it - and he causes that start, and later causes the "
                "darkness. A non-hybrid car has no silence to spend. Cards read as a "
                "sentence: CROWN, in silence -> he asks, it wakes -> you cannot buy it new "
                "here -> ask me.",
    "why_stop": "shot 0 is a light EVENT, not a tour - the car crosses from black shade into "
                "blazing backlight inside 1.8s - and card 1 NAMES THE CAR while promising "
                "the thing the ear is already noticing. Under-2s hooks measured 23% higher "
                "completion. The payoff arrives at 13.80s, inside the 15s line v1 missed.",
    "judged":   "v1 panel 2026-08-05: HOOK FAIL / ARC FAIL / REDESIGN, and SOUND QC FAIL. "
                "Full register: projects/crown/QC-PANEL-2026-08-05.md. v2 closes all 7 P0 "
                "and P1-1/2/3/5/6/7/8/10. **BOTH PANELS MUST BE RE-WALKED ON v2 BEFORE "
                "SPEND** - a changed CONTENT block always re-runs the panel, and this is a "
                "changed everything. Open from the register: P2-1 (blue-block motion floor), "
                "P2-5 (linkage kinds re-audited here but not re-judged), P2-9 (no loop).",
    "judged_cut": "N/A - nothing generated.",
}

PREVIZ = {
    "sheet": None,
    "note":  "Nev appears in D, J and H, so the sheet MUST carry the identity reference even "
             "though he is a silhouette. Not built - Gavril declined the ~2cr spend until "
             "the plan is unblocked.",
    "limit": "a still sheet CANNOT depict shot 0 (a car crossing a light boundary while "
             "moving) or shot 10 (an engine waking). Both are judged at the PROBE.",
}

# ---------------------------------------------------------------- THE MASTERMIND LOOP
LESSONS_ACK = {
    "general craft":       64,
    "car cinematic chill":  5,
    "car cinematic":       15,
}

PREMORTEM = [
    ("THE SOUND IS NEVER GENERATED. v1's fatal defect, caught by the sound panel at zero "
     "cost: nine prompts, not one audio word, and source F said the car was ALREADY under "
     "load - a state change that has already happened cannot be heard happening. FOLEY is a "
     "mix table; it cannot remove combustion the model invented.",
     "GENERATE_AUDIO declared; _SILENT appended verbatim to A/B/C/D/F_load; two-state audio "
     "written into E and G; F_wake stages the catch ON CAMERA and is the only clip permitted "
     "combustion. Probe A is now an AUDIO test - if it returns with an engine in it the "
     "concept dies at 22.5cr instead of 247.5cr."),

    ("WRONG CAR FROM A TEXT-ONLY PROMPT. This exact model is the repo's documented failure - "
     "'2026 Toyota Crown' returned a generic crossover and shipped an 87cr build.",
     "4k plate built FIRST and LOOKED AT, Crossover geometry spelled out in must_show, "
     "Gavril confirms the body before any video credit, every source cites the plate."),

    ("NOTHING HAPPENS TO THE PERSON. KK v15 measured 0 consequence boundaries and nothing "
     "happened to the man in 28 seconds; v1 repeated it in a better costume, with the HILL "
     "waking the engine while Nev was acted upon in all four of his shots.",
     "source J exists solely so he CAUSES the hero, and H is rewritten so his hand causes the "
     "darkness. Boundaries 9 and 18 are typed consequence with him as agent. If the ingest "
     "clip for J shows no decisive movement, that clip is rejected - the story is in it."),

    ("THE PAYOFF LANDS TOO LATE. v1 put the hero at 17.40s of 30s and left 10.8s with no text "
     "layer across the commit window.",
     "two golden repeats deleted, the cruise hold demoted, six beats moved into the dusk "
     "half. Hero at 13.80s, card 2 at 12.60s."),

    ("THE BED COMES FROM THE PHONK LIBRARY. All 25 tracks are 140-165 BPM drift phonk "
     "(ledger 'travel vlog' L0 / 'car cinematic chill' L2).",
     "SOUND['bed'] states the library is unusable and names the requirement; bed_map declares "
     "the video OPENS with no bed at all, because a bed under the word SILENCE is a lie."),

    ("THE BLUE BLOCK FAILS THE PLAN'S OWN MOTION FLOOR. Sources I and H are written parked "
     "and still, supply 5 of 20 shots, and face a delivered-window floor of 0.6 - roughly "
     "112cr of auto-rejects waiting at ingest (register P2-1).",
     "STILL OPEN. Declare a stillness exemption scoped to SHOT_TIME=='blue' in the profile "
     "BEFORE ingest, or restate the floor as block-scoped. I's prompt now specifies that the "
     "WATER moves even though the car does not, which may carry it - but that is a hope, not "
     "a measurement. Do not discover this after paying."),

    ("CLIPQC REJECTS THE GOLDEN-HOUR CLIPS. car_cinematic's band is [18,90], a MEASURED NIGHT "
     "band; daylight measures 142-165 and a golden/dusk frame measured 51.3.",
     "car_cinematic_chill declares [35,190], labelled PROVISIONAL. Deliberately wide because "
     "a wrong reject burns 22.5cr and a wrong accept costs one eye pass."),

    ("DOUBLE-GRADING THE GOLDEN HOUR. Footage arrives graded; a past build pushed saturation "
     "to 1.70 and took source 44.6 to 91.7, and shot_match once moved a shot 72.6 luma.",
     "GRADE_SAT 1.10 as a starting point to measure from, TARGET_BLACK 6.0 not 2.0, "
     "shot_match_max_move 14.0 luma in neighbour mode so the golden->blue arc survives."),
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


PROBE_FIRST = "A"   # tests the plate, the light break, the motion floor AND the silence
CLIPS = {}
CLIP_BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/"

# =====================================================================================
# ** STILL BLOCKED - DO NOT GENERATE **
# v2 closes every P0 and most P1s, but BOTH panels must be RE-WALKED on this version
# before a credit is spent, and P2-1 (blue-block motion floor) is open by name above.
# =====================================================================================
BLOCKED = ("v2 RE-WALKED 2026-08-05: judge REDESIGN (scoped to shots 1-8 + the card map), "
           "sound FAIL. See projects/crown/QC-PANEL-v2-2026-08-05.md. "
           "TWO OF MY OWN P0 'FIXES' WERE INERT: BLEND_AS_OVERLAP and GENERATE_AUDIO are "
           "read by NO tool (grep planqc.py = 0 hits each), so the deliverable is still "
           "28.80s and nothing guarantees the clips carry audio. A declaration no tool reads "
           "is not a fix. Highest-value open line: the word HYBRID appears on zero cards, so "
           "on a muted feed this is a car driving at sunset.")
