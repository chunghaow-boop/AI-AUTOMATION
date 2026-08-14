#!/usr/bin/env python3
"""
CROWN_PLAN v3 — Toyota Crown Crossover 2.4 RS Advance (S16) · chill coastal cinematic · Nev.

v1 passed planqc 34/34 and failed both panels. v2 closed most P0s and failed the re-walk.
v3 closes the re-walk register `projects/crown/QC-PANEL-v2-2026-08-05.md`.

**v3 IS PLAN-ONLY, BY GAVRIL'S INSTRUCTION 2026-08-05: "the pipeline and the flow i already
built i think is good already, please do not adjust or make too much of a adjustments inside
the pipeline."** Every v2 defect that the register proposed to fix by editing planqc.py or
engine.py is instead solved inside this file, in arithmetic the existing tools already
measure. Where that is impossible, the item is declared OPEN rather than papered over.

WHAT CHANGED FROM v2

  A0  THE TWO INERT FLAGS ARE GONE. v2 declared BLEND_AS_OVERLAP and GENERATE_AUDIO as if
      they changed behaviour; grep planqc.py returns 0 hits for both. That is a claimed
      capability, which is the one thing this repo forbids outright. Replaced by:
        - the timeline now carries the blend cost IN BEATS (see TARGET_S), so no tool has to
          learn a new flag for the delivered cut to be 30.00s;
        - GENERATION{} states the API parameters the operator must pass at spend time. It is
          labelled as an instruction to a human, not as a switch.
  A1  "HYBRID" IS ON CARD 1. The mechanism that makes the silence possible was never stated,
      so on a muted autoplay feed the whole video was a car driving at sunset.
  A2  Card "HE ASKS. IT WAKES." moved from shot 9 to shot 11 - v2 announced the twist 1.20s
      before it happened.
  A3  E and G no longer over-subscribe their engine halves. E is now used ONCE per state
      (7 silent / 12 engine). G's two engine windows are 1.20s each against ~2.5s.
  A4  The engine shots are now LOUDER than the silence block. v2 had shots 11/12/14 at
      -8/-10/-14 while the silence sat at -6: the engine was quieter than the silence.
      Fixed by raising the engine, NOT by dropping the gated shots below planqc 19's floor -
      that floor exists so a payoff is heard, and in this dialect the tyre hiss IS the
      payoff's sound. No gate was loosened.
  A5  HERO_SYNC is no longer an asserted 0.00. It is MEASURED at ingest off F_wake's own
      onset, and WINDOWS[11] is derived from it.
  A6  One owner for the duck. bed_map no longer contradicts SOUND["duck"].
  A7  Shot 12 is E's decay state, matching what E's prompt actually stages.
  A8  The 5.40-12.60s textless dead zone is filled - new source K and a second card.
  A9  LINKAGE regenerated from the v3 order; the two reversed/tautological entries are gone
      and the docstring no longer miscounts.
  A11 Local nouns exist now: Sabah on a card, Sabah/Kota Kinabalu in K and G.

STILL OPEN, DECLARED NOT HIDDEN
  - P2-1 blue-block motion floor (~112cr of possible auto-rejects). Needs a decision before
    ingest, and the decision belongs in the profile, which is a pipeline file - so it is
    Gavril's call, not mine.
  - WINDOWS below is read by NO tool. It is written as an instruction for the build step and
    labelled as such. Calling it a fix would repeat v2's mistake.
  - planqc's PRODUCTION.md generator still prints WRX boilerplate (whoosh on every cut, a
    150 BPM phonk bed). Pipeline file. NOT touched. Read the board, not that doc's sfx rows.

STORY, AS A SENTENCE
  A man leaves the city with the engine off - the Crown pulls away in silence - and drives
  the Sabah coast until the light runs out; when the road tilts up HE ASKS FOR THE ENGINE and
  it answers, and at the water HIS HAND SWITCHES IT OFF and the day ends.
"""

PROJECT   = "Toyota Crown Crossover 2.4 RS Advance · chill coastal cinematic · Nev"
PILLAR    = "car_cinematic_chill"
GEN_MODE  = "coverage"
MODE_ABC  = "hero"
BPM       = 100.0
BEAT      = 60.0 / BPM              # 0.600s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40

# THE BLEND COST IS CARRIED IN THE TIMELINE, NOT IN A FLAG (A0).
# 52 beats = 31.20s cut end-to-end. Three 0.40s dissolves compress it by 1.20s - which is
# exactly 2 beats - so the DELIVERED file is 30.00s and every surviving cut stays on the
# 0.600s grid. v2 tried to fix this by declaring BLEND_AS_OVERLAP=True, a flag nothing reads.
# planqc check 1 compares timeline() against TARGET_S, so TARGET_S is the PRE-blend number
# and the delivered number is stated here in writing.
TARGET_S   = 31.2                   # pre-blend
DELIVERED_S = 30.0                  # 31.2 - 3 * 0.40. This is the file Gavril receives.

BEATS = {"burst": 2, "med": 3, "hold": 5}       # 1.20 / 1.80 / 3.00s at 100 BPM

# GENERATION — parameters the operator passes at spend time. NOT a flag any tool reads;
# this is a written instruction to whoever spends the credits (A0).
GENERATION = {
    "generate_audio": "TRUE on every source. The diegetic spine IS the clip audio. A silent "
                      "clip is a dead 22.5cr and the concept dies with it.",
    "model_note":     "pass the plate as start_image / image_references on every shot; "
                      "human shots take the nev refs FIRST, then crown_int.",
    "resolution":     "720p, mode std. Never fast.",
}

# ---------------------------------------------------------------- PLATES
PLATES = {
    "crown": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
              "status": "NOT YET BUILT - build, LOOK at it, Gavril confirms the BODY is the "
                        "CROSSOVER (not Sedan, not Signia) before any video credit",
              "must_show": "Toyota Crown CROSSOVER (S16) RS Advance: raised sedan-SUV body "
                           "with a coupe-like falling roofline · full-width slim LED daytime "
                           "bar with a hammerhead front · body-colour upper grille and a wide "
                           "dark lower intake · black wheel-arch and rocker cladding · "
                           "21-inch dark multi-spoke alloys · full-width rear light bar · "
                           "CROWN wordmark across the tailgate · two-tone black roof",
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

# The silence contract. Six sources carry it VERBATIM. Without it the model's prior for
# "car on a coastal road" is an engine note and it supplies one at 22.5cr a time.
_SILENT = (" AUDIO: NO ENGINE, NO EXHAUST, NO COMBUSTION OF ANY KIND - the car is running "
           "on electric drive and is silent. No music, no voiceover, no dialogue.")

# ---------------------------------------------------------------- SOURCES  (12 × 22.5cr)
# GOLDEN: A B C D K   ·   DUSK: E G F_load J F_wake   ·   BLUE: H I
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
       "tread, the surface note changing under the wheel."),

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

 "K": ("the Sabah shoreline past the barrier", "#5C9A86", "EXTERIOR", ["crown"],
       "Vertical 9:16. Low slow tracking shot looking PAST the Toyota Crown Crossover from "
       "the reference image and out to sea - the car occupies the near edge of frame as a "
       "moving dark mass, and the subject is the SABAH shoreline beyond it: the Kota Kinabalu "
       "seafront promenade, coconut palms, the offshore island ridgelines low on the water, "
       "a small local fishing boat on the bay. Golden hour, the sun laying flat gold across "
       "the water. The camera travels with the car but is looking away from it. " + _LOOK +
       _SILENT + " Tyre hiss close and constant, wind, and distant surf and gulls beyond it."),

 "E": ("rear three-quarter, full-width light bar", "#B5563E", "EXTERIOR", ["crown"],
       "Vertical 9:16. Rear three-quarter of the Toyota Crown Crossover from the reference "
       "image on the coastal carriageway at dusk, slow arc around the rear corner. The "
       "FULL-WIDTH REAR LIGHT BAR is lit and is the brightest thing in frame; the CROWN "
       "wordmark across the tailgate reads clearly; the sky behind has gone amber to violet. "
       + _LOOK +
       " AUDIO, TWO STATES, SPLIT AT THE MIDPOINT. FIRST HALF: NO ENGINE, NO EXHAUST, NO "
       "COMBUSTION OF ANY KIND - only tyre note and wind. SECOND HALF: a petrol engine is "
       "running and pulling away from the camera, its note receding with distance. No music, "
       "no voiceover, no dialogue."),

 "G": ("wide bay, the car small in it", "#3F6E8C", "EXTERIOR", ["crown"],
       "Vertical 9:16. Wide static high-angle looking down over the Kota Kinabalu bay at "
       "dusk, the coastal carriageway curving through the lower third of frame AND RISING TO "
       "A CREST at the far side, the Toyota Crown Crossover from the reference image SMALL in "
       "the frame travelling along it. Offshore island ridgelines sit low in the haze; the "
       "last sun lies flat across the water. The car is a moving detail inside a landscape, "
       "not the subject. " + _LOOK +
       " AUDIO, TWO STATES, SPLIT AT THE MIDPOINT. FIRST HALF: NO ENGINE, NO EXHAUST, NO "
       "COMBUSTION OF ANY KIND - only wind over open water and distant surf. SECOND HALF: a "
       "petrol engine is faintly audible at long distance, thin and small inside the "
       "landscape, then easing off. No music, no voiceover, no dialogue."),

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
       " AUDIO: the deepest near-silence in the film - faint cloth, a thin electric whine, "
       "nothing else. NO ENGINE, NO EXHAUST, NO COMBUSTION ANYWHERE IN THIS CLIP, not at the "
       "start, not at the end. The engine must NOT be heard starting here; it starts in the "
       "NEXT shot. No music, no voiceover, no dialogue."),

 "F_wake": ("EVENT · the engine catches", "#C44B3A", "EVENT", ["crown"],
       "Vertical 9:16. THE HERO. The Toyota Crown Crossover from the reference image climbing "
       "the rising coastal ramp at dusk, tracked from a parallel vehicle in front "
       "three-quarter. THE CLIP OPENS STILL SILENT AND STILL ON ELECTRIC DRIVE for a beat - "
       "then the petrol engine CATCHES and the car takes load: the nose lifts, the body "
       "settles back on its springs, the pace hardens decisively but without drama, and heat "
       "shimmer rises off the rear. THE TRANSITION FROM SILENT TO RUNNING HAPPENS ON CAMERA, "
       "inside this clip, and it happens EARLY - within the first second. Unhurried but "
       "unmistakably WORKING. " + _LOOK +
       " AUDIO - THIS IS THE ONLY COMBUSTION SOUND IN THE ENTIRE FILM: the clip opens in near "
       "silence with tyre roll and wind alone, then the petrol engine CATCHES - a brief crank, "
       "the four-cylinder fires, and the note rises and hardens under load as the ramp "
       "steepens, with turbo spool behind it. The catch must happen EARLY in the clip. "
       "Ambience: open coastal air. No music, no voiceover, no dialogue."),

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
       "promenade and the bay beyond it going dim. Very slow drift of the camera; THE WATER "
       "AND THE PALMS MOVE, the car does not. The full-width rear light bar and the cabin "
       "glow are the only lit things; the sky is deep blue with the last band of orange on "
       "the horizon. " + _LOOK +
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
    "K":      "low tracking looking PAST the car out to sea, car at the near edge",
    "E":      "slow arc around the rear corner, exterior",
    "G":      "wide static high angle, car small inside a landscape",
    "F_load": "parallel-vehicle tracking onto an incline, front three-quarter, level",
    "J":      "interior from passenger side, TIGHT on shoulder and forearm, silhouette",
    "F_wake": "parallel-vehicle tracking on the incline, front three-quarter, car loading",
    "H":      "interior from passenger side, parked, silhouette, hand to console",
    "I":      "exterior side-and-behind, static, very slow drift",
}

# ---------------------------------------------------------------- TIMELINE
# 21 shots · 52 beats = 31.20s pre-blend · 30.00s delivered · 15 burst / 4 med / 2 hold
# HERO at 14.40s pre-blend, 14.00s delivered - inside the 15s line.
SHOTS = [
 ("A",      1.00, "med",   "shadow into gold - already moving, and silent"),
 ("B",      1.30, "burst", "gold on the coast road, still silent"),
 ("C",      1.00, "burst", "the alloy turns, tarmac streaming, silent"),
 ("D",      1.15, "burst", "his hands settle on the rim, silent, the road runs ahead"),
 ("B",      1.00, "med",   "the coast road opens out, gold everywhere, nothing driving it"),
 ("K",      1.15, "burst", "the Sabah shoreline past the barrier, gold flat on the water"),
 ("C",      1.30, "burst", "kerb line under the alloy at road level, the last of the gold"),
 ("E",      1.00, "burst", "the light bar comes on as the gold dies"),
 ("G",      1.30, "burst", "wide bay, the coast road bends away, the last gold flat on it"),
 ("F_load", 1.15, "burst", "the road tilts up into the ramp - still electric, nothing running"),
 ("J",      1.00, "burst", "HIS DECISION - the silhouette commits, foot down on the ramp"),
 ("F_wake", 1.00, "hold",  "IT WAKES on the ramp because he asked for it"),
 ("E",      1.15, "burst", "the light bar pulls away from the ramp, climbing now"),
 ("G",      1.00, "burst", "wide - the car small, climbing toward the crest"),
 ("F_wake", 1.30, "burst", "at the crest it hardens and holds, steady under load"),
 ("G",      1.15, "burst", "the load falls away past the crest, it goes quiet again"),
 ("I",      1.00, "burst", "quiet at the barrier, blue hour, nothing running"),
 ("H",      1.30, "burst", "he sits, hand still on the rim at the barrier"),
 ("I",      1.15, "med",   "the bay from outside the barrier, the cabin still lit"),
 ("H",      1.00, "hold",  "HIS HAND KILLS IT - key off, the cabin goes dark"),
 ("I",      1.30, "med",   "dark bay, the car parked in it, nothing running"),
]

# WINDOWS — which second of each 5s clip a shot is cut from.
# HONESTY: NO TOOL READS THIS. It is an instruction for the build step and for the eye at
# ingest, written down so the two-state clips cannot be cut from the wrong half by accident.
# v2's mistake was declaring things like this as if they were switches. This is not a switch.
WINDOWS = {
    # shot: (in_s, out_s) within its source clip
    7:  (0.00, 1.20),   # E  FIRST half  - the silent state
    12: (2.60, 3.80),   # E  SECOND half - the engine state
    8:  (0.00, 1.20),   # G  FIRST half  - silent
    13: (2.60, 3.80),   # G  SECOND half - engine at distance
    15: (3.80, 5.00),   # G  SECOND half tail - easing off. 13+15 = 2.40s of a ~2.5s half.
    11: ("AT THE CATCH", "MEASURED AT INGEST - see HERO_SYNC. The window opens ON the "
         "onset, not at the clip head, because F_wake spends its first beat silent."),
    14: (3.20, 4.40),   # F_wake tail - the hardened note, after the hold's window
}

# ---------------------------------------------------------------- THE CLOCK (planqc 30)
SHOT_TIME = (["golden"] * 7) + (["dusk"] * 9) + (["blue"] * 5)
TIME_JUMPS = {}

# ---------------------------------------------------------------- LINKAGE (24/29/31)
# Generated from the v3 order. 9 of 20 are CONSEQUENCE (planqc floor is 4), and the two that
# carry the story - boundary 10 (he asks, the engine answers) and boundary 18 (his hand kills
# the cabin) - have THE MAN as the agent. v2's reversed entry ("the engine goes quiet ->
# arrival", when arrival causes the quiet) and its tautological one ("the cabin dark -> the
# frame dark") are both gone rather than re-worded.
# 'engine' is NOT usable as a token: the word appears in all twelve prompts, because six
# forbid it and three stage it. A token on both sides of every boundary proves nothing.
LINKAGE = [
 ("light",       "gold",    "the car breaks into the gold -> the gold is the whole road"),
 ("sound",       "silent",  "silent at speed -> still silent, the absence is established"),
 ("sound",       "silent",  "the alloy turns in silence -> his hands rest in the same silence"),
 ("consequence", "road",    "his hands settle -> the road opens out in front of that decision"),
 ("light",       "gold",    "the gold on the road -> the same gold laid flat on the water"),
 ("light",       "gold",    "gold on the water -> the last of the gold down at ground level"),
 ("consequence", "gold",    "the gold is dying -> so the light bar comes on"),
 ("light",       "gold",    "the light bar against the dying gold -> the bay holding the last of it"),
 ("motion",      "road",    "the road bending away -> the road tilting up into the ramp"),
 ("consequence", "ramp",    "the ramp arrives -> HE COMMITS to it, foot down"),
 ("consequence", "ramp",    "he asked for it on the ramp -> THE ENGINE ANSWERS. the hero"),
 ("consequence", "ramp",    "it woke on the ramp -> the car pulls away from it"),
 ("motion",      "climb",   "climbing away -> still climbing, seen small across the bay"),
 ("motion",      "crest",   "climbing toward the crest -> arriving at the crest"),
 ("consequence", "crest",   "the crest is reached -> so the load falls away past it"),
 ("consequence", "quiet",   "it goes quiet -> arrival, quiet at the barrier"),
 ("subject",     "barrier", "the car at the barrier -> him inside it at the same barrier"),
 ("object",      "barrier", "him at the barrier -> the same barrier seen from outside"),
 ("consequence", "cabin",   "the cabin is still lit -> HIS HAND KILLS IT"),
 ("consequence", "dark",    "he switched it off -> the whole frame dark, nothing left running"),
]

CALLBACKS = [(0, 4), (16, 20)]
BAN_SPANS = {}
DELOGO    = {}

# ---------------------------------------------------------------- TRANSITIONS
# 3 of 20 = 15%, inside [6,33]. NONE touches an EVENT shot (0, 9, 11, 14).
# Their 1.20s of compression is carried in the beat count, not in a flag - see TARGET_S.
BLEND_AFTER = [6, 15, 18]           # golden->dusk seam · dusk->blue seam · into the key-off
BLEND_KIND  = "dissolve"
BLEND_WIDTH = 0.40

SFX_LEAD   = 0.22                   # designed transients only
HERO_SYNC  = "MEASURED AT INGEST"   # v2 asserted 0.00 while F_wake's own prompt puts the
                                    # catch a beat inside the clip. Run onset detection on
                                    # the ingested F_wake; that number sets WINDOWS[11]'s
                                    # in-point AND the IMPACT placement. Until it is
                                    # measured it is NOT a number.
IMPACT_AT  = [11]                   # hero_only: the one designed cut in the video
SUBDROP_AT = []                     # folded into the hero's body layer

# ---------------------------------------------------------------- SOUND
SOUND = {
    "bed":        "NOT YET SOURCED, and it CANNOT come from the library - all 25 tracks in "
                  "assets/bgm + assets/pillars/car_cinematic/bgm are 140-165 BPM drift phonk. "
                  "Required: 100.00 BPM measured, warm, half-time, no cowbell, no distorted "
                  "808. tools/bgmgen.py, then rhythm.py for BPM + grid OFFSET, trimmed so "
                  "hit 1 lands at t=0.",
    "bed_map":    {"in": "shot 4 @6.00s, up over one beat from -inf. The video opens with NO "
                         "BED AT ALL: card 1 says NO ENGINE YET and music under it makes the "
                         "card a lie. v2 brought the bed in at 1.80s and defeated its own "
                         "stated reason for 3.6 of 5.4 seconds.",
                   "level_silence_block": "-9dB under nominal through shots 4-10",
                   "hero": "nominal from shot 11",
                   "out": "fade to -inf across shot 19, fully silent from 28.80s delivered",
                   "tail": "shot 20 is diegetic sea only - no bed",
                   "duck": "OWNED BY SOUND['duck'] BELOW. Not restated here - v2 declared the "
                           "duck in two places with different values."},
    "hero":       "THE PETROL ENGINE CATCHING (shot 11, 14.00s delivered), CAUSED by his "
                  "commit in shot 10. ONE hero sound per video (file 04, law 4).",
    "hero_layers": {"transient": "the crank/catch from F_wake's own audio",
                    "body":      "the 2.4T load note, 150-1500Hz, from F_wake - sub energy "
                                 "folded in here, not as a separate drop",
                    "tail":      "exhaust decay carried under shot 12",
                    "honesty":   "all three come from ONE recording, F_wake's clip audio. "
                                 "File 19 asks for layered construction; this is layered "
                                 "PLACEMENT of one source. Stated as what it is."},
    "near_silence": "shot 10 (13.20-14.40s pre-blend) - diegetic floor at -24dB and the bed "
                    "ducked out over its last 0.40s. THIS is the drop-out the engine breaks.",
    "duck_shots": [11],          # the key planqc 19 reads. Detail below, one owner.
    "duck":       {"shots": [11], "mode": "sidechain", "thr": 0.06, "ratio": 6,
                   "release_ms": 120, "depth_db": -18,
                   "starts_at": "0.40s before the shot-11 cut",
                   "recovers": "over shot 12",
                   "why": "binary hard-duck windows STEP 12dB in/out and he heard it as "
                          "'music breaks at cuts'. One smooth sidechain, one owner."},
    "silence":    "shots 0-10 (0.00-14.40s pre-blend) carry NO COMBUSTION - written into "
                  "eleven prompts, not just into the gain map. Shot 20 returns to it.",
    "layers":     "diegetic (gains below) + bed (one sidechain, mapped above) + edit-sfx "
                  "HERO ONLY. The IMPACT at shot 11 is the single declared non-diegetic "
                  "element in a diegetic-gated pillar, and it sits on the hero.",
}

MIX = {
    "target_lufs":   "-7 to -9 integrated",
    "true_peak":     "-1.0 dBTP",
    "channels":      2,
    "stereo_width":  "bed wide, diegetic near-centre; the hero centred so it reads on a phone",
    "reference":     "NONE YET - file 19 wants a reference track and no chill car reference "
                     "exists in this repo. OPEN.",
    "spectrum":      "body 150-1500Hz ~45% · himid ~18% · presence ~24% · sub+low ~8% · "
                     "air 10-20k ~4% · centroid ~2400Hz",
    "room":          "cabin shots (D, J, H) damped, short tail. Coast shots open.",
    "bed_highpass":  "40Hz",
    "note":          "the profile's sub_bass_pct [25,65] is INHERITED PHONK TASTE and is "
                     "wrong here - a 2.4 turbo four lives at 200-800Hz and 1-3k. Measure "
                     "against the file 19 spectrum. Re-derive the profile field at ingest "
                     "(profile edit = pipeline, so that is Gavril's call).",
}

SFX_OVERLAYS = []   # under hero_only this list may only ever hold entries at shot 11

# FOLEY. v2's incoherence: the engine shots sat at -8/-10/-14 while the silence sat at -6,
# so the engine was QUIETER than the silence. Fixed by raising the engine, NOT by dropping
# the gated shots under planqc 19's -6 floor. That floor exists so a payoff is HEARD, and in
# this dialect the tyre hiss IS the payoff's sound. No gate loosened.
# PROVISIONAL - re-derive every value against the generated bed's measured RMS.
FOLEY = {
     0:  -6.0,   # A       tyre roll + displaced air. NO ENGINE. gated.
     1:  -6.0,   # B       tyre hiss on open tarmac. gated.
     2: -14.0,   # C       tread and tarmac texture
     3: -20.0,   # D       cabin drop-out: cloth, a breath, floor rumble
     4:  -6.0,   # B       the cruise - road and wind carry it. gated.
     5: -15.0,   # K       tyre close, surf and gulls beyond
     6: -15.0,   # C       kerb passing
     7: -16.0,   # E       first half: tyre note easing, no combustion
     8: -20.0,   # G       first half: wind over water, car barely audible
     9:  -6.0,   # F_load  the quiet immediately before. gated, and it must be HEARD.
    10: -24.0,   # J       NEAR-SILENCE. the floor before the twist.
    11:  +6.0,   # F_wake  HERO - the catch. +12 over the gated floor, +30 over shot 10.
    12:  -2.0,   # E       second half: engine pulling away. LOUDER than any silent shot.
    13:  -5.0,   # G       second half: engine thin at distance
    14:  -3.0,   # F_wake  hardened under load at the crest. gated.
    15: -10.0,   # G       the load falling away
    16: -18.0,   # I       stillness - water and wind at a stopped car
    17: -20.0,   # H       cabin, cloth, the hand on the rim
    18: -21.0,   # I       water and wind outside a stopped car
    19: -22.0,   # H       the shutdown chime and the last relay
    20: -26.0,   # I       the global floor - sea only
}

# ---------------------------------------------------------------- CARDS
CARD_Y     = 0.72
CARD_STYLE = "fragment"
CARDS = [   # (text, first_shot, n_shots, kind) - card_max_words = 5
    ("CROWN. HYBRID. NO ENGINE YET",     0, 4, "cap"),   # A1: names the car AND the mechanism
    ("SABAH COAST. STILL NOTHING RUNNING", 5, 4, "cap"), # A8+A11: fills the dead zone, local
    ("HE ASKS. IT WAKES.",              11, 3, "cap"),   # A2: ON the hero, not before it
    ("NEVER SOLD NEW IN MALAYSIA",      15, 3, "cap"),   # matches CONTENT["claim"] exactly
    ("RECOND. DM FOR THE PRICE",        18, 3, "cta"),   # names the channel
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
                "only (motortrader recond index, carlist). Card 4 says NEVER SOLD NEW IN "
                "MALAYSIA, exactly this claim - not the wider 'Toyota never sold it here', "
                "which is false and which J4 would roast. "
                "POWER FIGURE RETRACTED 2026-08-05: v1 shipped 350PS on a derivation "
                "(272+83+81) that sums to 436. Hybrid output is not additive and Toyota's "
                "own release states no figure. NO NUMBER SHIPS until a JDM spec sheet "
                "confirms one.",
    "twist":    "the product feature is the story device AND the man operates it. Combustion "
                "is withheld for 14 seconds so one engine start is the loudest thing in the "
                "film - he causes that start, and later causes the darkness. A non-hybrid car "
                "has no silence to spend. Cards read as a sentence: CROWN, hybrid, no engine "
                "yet -> Sabah coast, still nothing running -> he asks, it wakes -> you cannot "
                "buy it new here -> DM me.",
    "why_stop": "shot 0 is a light EVENT, not a tour - the car crosses from black shade into "
                "blazing backlight inside 1.8s - and card 1 names the car AND the mechanism, "
                "so a MUTED viewer is told what to notice. v2's fatal weakness was that its "
                "differentiator was inaudible and unstated; sound-off, it was a car at "
                "sunset. Payoff at 14.00s delivered, inside the 15s line.",
    "judged":   "v1 panel: HOOK FAIL / ARC FAIL / REDESIGN + SOUND FAIL. v2 re-walk: judge "
                "REDESIGN (scoped to shots 1-8 + the card map), sound FAIL - registers at "
                "projects/crown/QC-PANEL-2026-08-05.md and QC-PANEL-v2-2026-08-05.md. "
                "v3 addresses A0-A11 of the v2 register. **BOTH PANELS MUST BE RE-WALKED ON "
                "v3 BEFORE SPEND.** Open by name: P2-1 blue-block motion floor (needs a "
                "profile decision, which is Gavril's), MIX reference track, and the fact "
                "that WINDOWS is read by no tool.",
    "judged_cut": "N/A - nothing generated.",
}

PREVIZ = {
    "sheet": None,
    "note":  "Nev appears in D, J and H - the sheet MUST carry the identity reference even "
             "though he is a silhouette. Not built; Gavril declined the ~2cr until unblocked.",
    "limit": "a still sheet CANNOT depict shot 0 (a car crossing a light boundary while "
             "moving) or shot 11 (an engine waking). Both are judged at the PROBE.",
}

# ---------------------------------------------------------------- THE MASTERMIND LOOP
LESSONS_ACK = {
    "general craft":       64,
    "car cinematic chill":  5,
    "car cinematic":       15,
}

PREMORTEM = [
    ("I DECLARE A FIX THAT NO TOOL READS. Proven on v2, twice in one file: "
     "BLEND_AS_OVERLAP and GENERATE_AUDIO were written as if they changed behaviour and "
     "grep planqc.py returns 0 hits for both. A claimed capability is the one thing this "
     "repo forbids outright, and I did it inside the plan written to fix a defect list.",
     "v3 carries the blend cost in BEATS, which the existing timeline() already computes, so "
     "no tool has to learn anything. GENERATION and WINDOWS are labelled IN THE PLAIN TEXT "
     "as instructions to a human, not switches. Rule for the next plan: if a declaration "
     "changes behaviour, name the file and line that reads it, or call it a note."),

    ("THE SOUND IS NEVER GENERATED. v1's fatal defect - nine prompts, not one audio word, in "
     "a video whose subject is a sound. FOLEY is a mix table; it cannot remove combustion "
     "the model invented.",
     "the verbatim silence contract is in A, B, C, D, K, F_load and in E and G's first-half "
     "clauses; J forbids the start explicitly; F_wake is the only clip permitted combustion "
     "and stages the catch early and on camera. Probe A is an AUDIO test - if it returns "
     "with an engine, the concept dies at 22.5cr instead of 270cr."),

    ("WRONG CAR FROM A TEXT-ONLY PROMPT. This exact model is the repo's documented failure: "
     "'2026 Toyota Crown' returned a generic crossover and shipped an 87cr build.",
     "4k plate built FIRST and LOOKED AT, Crossover geometry in must_show, Gavril confirms "
     "the body before any video credit, every source cites the plate."),

    ("NOTHING HAPPENS TO THE PERSON. KK v15 measured 0 consequence boundaries; v1 repeated "
     "it with the HILL waking the engine while Nev was acted upon in all four of his shots.",
     "source J exists so he CAUSES the hero; H is written so his hand causes the darkness. "
     "Boundaries 10 and 18 are typed consequence with him as agent. If J's clip shows no "
     "decisive movement it is rejected - the story is inside that clip."),

    ("THE DIFFERENTIATOR IS INAUDIBLE ON A MUTED FEED. The v2 panel's sharpest line: "
     "sound-off, this is a car driving at sunset, and the word HYBRID appeared on zero cards.",
     "card 1 is CROWN. HYBRID. NO ENGINE YET - the mechanism stated in the first 2.4s to a "
     "viewer who cannot hear it. Card 2 restates it at 6.00s. The concept now survives mute."),

    ("A GREEN NUMBER ON A CHECK THAT CANNOT SEE THE CONSTRAINT. planqc 21 reported "
     "'E 3.6/4.9 - fits' on v2 while E's engine HALF was oversubscribed by 0.30s. The check "
     "measures the whole clip; the two-state prompt splits it.",
     "v3 uses E once per state and keeps G's two engine windows to 2.40s of a ~2.5s half. "
     "WINDOWS states every in-point so the arithmetic is visible to the eye even though no "
     "tool checks it. This is a NEW blind-spot class and belongs in the ledger."),

    ("THE BED COMES FROM THE PHONK LIBRARY. All 25 tracks are 140-165 BPM drift phonk.",
     "SOUND['bed'] states the library is unusable and names the requirement; bed_map keeps "
     "the bed OUT of the opening entirely, because music under 'NO ENGINE YET' is a lie."),

    ("THE BLUE BLOCK FAILS THE MOTION FLOOR. I and H are parked and still, supply 5 of 21 "
     "shots, and face a delivered-window floor of 0.6 - roughly 112cr of auto-rejects.",
     "STILL OPEN AND NOT MINE TO CLOSE. The fix is a stillness exemption in the profile, "
     "which is a pipeline file. I's prompt now specifies that THE WATER AND PALMS MOVE while "
     "the car does not, which may carry it - but that is a hope, not a measurement. Decide "
     "before ingest, not after paying."),

    ("DOUBLE-GRADING THE GOLDEN HOUR. Footage arrives graded; a past build pushed saturation "
     "to 1.70 and took source 44.6 to 91.7.",
     "GRADE_SAT 1.10 as a point to measure from, TARGET_BLACK 6.0 not 2.0, "
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
# ** BLOCKED UNTIL THE v3 PANEL RE-WALK **
# =====================================================================================
BLOCKED = ("v3 written 2026-08-05, PLAN-ONLY by his instruction. Awaiting: panel re-walk on "
           "v3, the P2-1 blue-block motion-floor decision (profile = his call), and his "
           "approval of 12 clips = 278.0cr.")
