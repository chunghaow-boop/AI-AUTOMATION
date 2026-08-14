"""NEV · IT BROKE FROM SITTING — Audi R8 magnetic ride · car review / advice
His title 2026-08-12: "Nev fixing a car and then driving the car to test drive
it and telling audiences and giving advice about mechanical information...
I want NEV to fix an Audi R8... showing the process of Nev fixing the car, and
Nev driving the car and explaining the issue of the car and also giving some
tips and tricks. 720p, 30 seconds."

THE INTENT, READ FIRST (his adjustment 1: the title is an INTENT brief):
  This film is not about a car. IT IS ABOUT AUTHORITY. He wants a viewer to
  finish it thinking "this guy actually knows cars" - which, for a Malaysian
  recond-car audience, is the most valuable thing the persona can own and the
  thing that converts into trust in the business behind the channel. Everything
  follows from that: the fault must be REAL and VERIFIABLE, the proof must be
  VISIBLE (not described), and the advice must be something an owner can act on
  this week. A film that looks like a mechanic but says nothing checkable has
  failed this title even if every frame is beautiful.

HIS PICKS (readback 2026-08-12):
  car   = AUDI R8. He wrote "Audi R8 TT", which names two different cars (the R8
          is a mid-engine supercar, the TT a front-engine coupe) - the panborneo
          "Land Cruiser Defender" case exactly. ASKED, not guessed. He picked R8.
  voice = CARDS CARRY THE ADVICE, music-led. A deliberate departure from what the
          car_review references do (presenter to camera with karaoke captions):
          we have never shipped a speech-led film, lip-sync is the generator's
          weak class, and no VO voice has been chosen. Declared, not drifted.

REFERENCE SCAN — TWO SCANS (CLAUDE.md step 2)
  SUBJECT (Audi R8 magnetic ride, web 2026-08-12): the R8's Magnetic Ride
    dampers are a widely-reported failure point - leaks from as early as
    ~7,000 km, most between 40,000-80,000 km, and specialists accept that ALL
    magnetorheological dampers eventually leak. Audi classes them as WEAR ITEMS,
    so warranty is typically denied. AND THE DETAIL THAT MAKES THIS FILM:
    low-mileage cars that SIT for long periods are particularly vulnerable
    because the magnetic fluid settles and damages the seals. A recond supercar
    is precisely the car that sits.
  FORM (mechanic / repair shorts, web 2026-08-12): VISUAL PROOF IS THE
    CREDIBILITY - real technician, real vehicle, the actual fault visible on
    screen rather than described. Keep it symptom-focused with ONE clear
    takeaway. 72% of owners say they prefer a 60-second video explanation to a
    written estimate. Our car_review reference set backs the text register: a
    white rounded card, top-left, stating the subject in frame 1.

THE UPGRADE OVER THE FIELD, in one line: repair shorts show a part being
replaced; this one names WHY it failed - and the answer inverts what the
audience assumes about supercars.

SPINE: KISHOTENKETSU (file 31 PART E). There is no antagonist - a damper is not
a villain - so three-act conflict would manufacture fake stakes.
  KI    the wet damper: something is wrong, shown not said
  SHO   the work: wheel off, damper out, new one in
  TEN   THE DUST SHEET AND THE LOW ODOMETER - it did not break from being
        driven hard, it broke from NOT BEING DRIVEN. Everything before re-reads.
  KETSU the test drive, and the tip an owner can act on this week
"""

PROJECT   = "NEV · IT BROKE FROM SITTING · Audi R8 magnetic ride · car review"
PILLAR    = "car_advice"             # NOT car_review: that pillar is SPEECH-LED
                                     # (sound_gate=underscore, its references are
                                     # presenters to camera with karaoke captions) and
                                     # he chose CARDS + MUSIC. Renting car_review's
                                     # name would repeat the exact mistake he caught
                                     # on the kariayam board an hour earlier (L159).
                                     # car_advice inherits car_review's numbers with
                                     # the inheritance DECLARED, and its refs are
                                     # presenter-led 58-107s so a 30s music-led film
                                     # sits outside the band by design - checks 2/9
                                     # report it rather than pretending otherwise.
PILLAR_FIT = ("car_advice, created for this film rather than renting car_review's "
    "name: car_review is SPEECH-LED (a presenter carries it) and this is CARDS + "
    "MUSIC. DIFFED AGAINST car_review, key by key, after his sound catch (L165): "
    "sound_gate underscore -> diegetic (no VO here); edit_sfx 'none' -> 'hero_only' "
    "(a talking-head format needs no sweeteners, a WORKSHOP film's ratchet, torque "
    "click and engine ARE the content); duration band 58-107s INHERITED and NOT "
    "diffed - a 30s film sits outside it by design and checks 2/9 report that; "
    "picture_baseline INHERITED from presenter-led refs and flagged as a placeholder, "
    "not a standard, until music-led advice references exist.")

GEN_MODE  = "coverage"
BPM       = 97.5
BEAT      = 60.0 / BPM
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"                   # his standing call: 720p IS the cost strategy
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 29.5385                  # 48 beats = 6 whole clips x 8 beats

LESSONS_ACK = {
    "general craft": 169,            # incl. L170 THE GENERATOR DOES NOT ALWAYS RETURN
                                     # ONE TAKE — this batch produced it: 2 of 6 clips
                                     # came back two-shot, and the far side of C's cut
                                     # held a floating torque wrench. clipgate now
                                     # detects internal cuts (full-rate, never
                                     # subsampled — the subsample missed a real cut)
                                     # · L167 QC is the final boss (his eye is the
                                     # final FINAL boss) · L168 every layer owes a
                                     # decision or a written waiver · L169 a gate ships
                                     # with its negative control · L165 a pillar sound
                                     # POLICY is inherited
                                     # too (this plan found it) · L166 sound must be
                                     # visible on the board · L163 a new plan field
                                     # must reach EVERY
                                     # reader (this plan found it) · L161 BOARD QC ·
                                     # L159 create the pillar,
                                     # never rent the name · L144 whole clips are an
                                     # ORDER · L147 scan the FORM too · L148
                                     # kishotenketsu · L149 the triple link · L158
                                     # his three pipeline adjustments.
    "toyota land cruiser 300 zx car review": 8,   # the review-pillar lessons
    "car cinematic": 15,
    "bmw i8 car cinematic": 16,
    "travel vlog": 9,
}

PREMORTEM = [
    ("AN INVENTED BADGE OR MODEL NAME SHIPS (lesson 35: the WRX grew an 'SR' badge "
     "that does not exist, and the Crown shipped as a generic crossover because a "
     "text-only prompt was trusted). An R8 is one of the most badge-and-grille "
     "recognisable cars on earth and a wrong one destroys the credibility this "
     "film exists to build",
     "THE R8 PLATE IS MANDATORY AND IS BUILT FIRST (identity rule: a named subject "
     "is never generated from text alone), OCR'd, and LOOKED AT before any clip. "
     "Every prompt describes GEOMETRY - mid-engine proportions, the side blade, "
     "the wide low nose - and BANS badges, model lettering and number plates. "
     "clipqc text-zoom runs on EVERY clip (his adjustment 2), not just the probe."),

    ("THE MECHANICAL DETAIL IS WRONG AND A REAL MECHANIC SEES IT INSTANTLY. This "
     "film's whole intent is authority; one implausible shot - a damper coming off "
     "with the wheel still on, a torque wrench used backwards - costs more than a "
     "soft frame ever could",
     "Every work prompt states the ACTUAL SEQUENCE in the order a shop does it: "
     "car on the ramp and wheel OFF before the damper is touched; the damper "
     "unbolted top and bottom; the new unit offered up and torqued. The visible "
     "fault is the one the sources describe - an OIL FILM WEEPING DOWN THE DAMPER "
     "BODY - not a puddle, not smoke, not a broken spring."),

    ("HANDS AND TOOLS ARE THE GENERATOR'S WORST CLASS (the same risk as the kari "
     "ayam board): six fingers, a spanner fused to a hand, a socket that morphs "
     "between frames. Four of six shots here are hands-on-metal",
     "Every prompt names REAL HANDS in nitrile gloves, five fingers, correct "
     "anatomy, and the negative block leads with extra-fingers/warped-hands. The "
     "PROBE is A (the leak macro: gloved fingers, fluid, machined metal in one "
     "frame) - one 22.5cr clip LOOKED AT before the other five spend anything."),

    ("'RESOLVES INSIDE N SECONDS' WRITES THE OTHER FOUR (craft #99), and this film "
     "plays WHOLE CLIPS so every second is on screen",
     "Every prompt declares what fills the WHOLE clip: A is 'the finger drags "
     "through the film, comes away wet, turns in the light - continuous'. The "
     "phrase 'resolves inside N seconds' appears nowhere."),

    ("A WORKSHOP IS FULL OF LEGIBLE TEXT - tool brands, oil bottles, wall posters, "
     "a diagnostic screen. Any of it invents a brand we do not own (the mahua "
     "signage defect)",
     "Every prompt: NO BRAND MARKS, NO LABELS, NO LEGIBLE TEXT on tools, bottles, "
     "walls or screens; no number plate on the car. Plain tools, plain surfaces."),
]

_LOOK = (
    "An independent workshop, real practical light. REAL PHOTOGRAPHY, NOT A "
    "RENDER: machined metal with real specular highlights, fine dust and "
    "fingerprints, oil sheen, natural handheld micro-shake, shallow depth of "
    "field. REAL HANDS in dark nitrile gloves: five fingers, correct anatomy at "
    "all times. Negative: CGI, videogame look, plastic or waxy surfaces, "
    "stock-photo gloss, extra fingers, warped or merged hands, floating tools, "
    "NO BRAND MARKS, NO LABELS, no legible text on tools, bottles, walls or "
    "screens, no visible number plate, no model badges or lettering on the car, "
    "no showroom, no crowds."
)

# ------------------------------------------------------------- SOURCES (6 x 22.5cr)
SOURCES = {
 "A": ("THE LEAK — proof, not opinion", "#6E7A82", "EVENT", ["r8", "workshop"],
       "Vertical 9:16. Macro, low, under the front corner of the silver Audi R8 from "
       "the reference image, raised on a two-post ramp in the workshop of the second "
       "reference image; the wheel is already off and the brake disc catches the light "
       "behind. A gloved finger reaches in and drags slowly down the damper body: the "
       "metal is wet with a thin film of oil, and the finger comes away glistening, "
       "turning in the light so the wet sheen is unmistakable. Dust clings to the "
       "damper everywhere the oil has run. Continuous movement first frame to last - "
       "reach, drag, turn, hold. Real machined aluminium, real oil viscosity. AUDIO: "
       "the low hum of a workshop, a distant compressor, the small squeak of a nitrile "
       "glove on metal - no music, no voice. " + _LOOK),

 "B": ("the damper comes out", "#5A646B", "HUMAN", ["r8", "workshop", "nev"],
       "Vertical 9:16. Medium at wheel height on the raised silver Audi R8 from "
       "the reference image, and THE MAN FROM THE REFERENCE IMAGES IS IN FRAME AND "
       "WORKING - navy check shirt open over a black tee, sleeves pushed up, dark "
       "nitrile gloves; face, hair and EARRING match the references exactly, three-"
       "quarter to the lens, eyes down on the job. His two gloved hands work a long socket bar onto the damper's "
       "lower bolt and break it loose - the bar moves, the bolt turns, the thread comes "
       "clear - then the upper mount is freed and the damper unit is drawn down and out "
       "of the arch, hanging heavy in one hand, its lower half dark with the oil that "
       "was on it. Continuous work first frame to last, no cutaway. Plain unbranded "
       "tools. AUDIO: the ratchet's mechanical clatter, the crack as the bolt breaks "
       "loose, metal settling - no music, no voice. " + _LOOK),

 "C": ("the new one goes in", "#4F5A60", "EVENT", ["r8", "workshop"],
       "Vertical 9:16. Close over the arch of the silver Audi R8 from the reference "
       "image: a clean new damper - dry, unmarked, its body evenly machined - is "
       "offered up into the arch, lined up, and the lower bolt started by hand, then a "
       "torque wrench is fitted and pulled through in one smooth arc until it CLICKS. "
       "Gloved hands, deliberate and unhurried. Continuous action first frame to last: "
       "offer up, thread, torque, click. The contrast with the wet unit is visible - "
       "this one is bone dry. AUDIO: the thread running, the torque wrench's single "
       "sharp click, workshop hum behind - no music, no voice. " + _LOOK),

 "D": ("THE REASON — the sheet comes off", "#7C7168", "PLACE", ["r8", "workshop"],
       "Vertical 9:16. THE TURN OF THE FILM. Wider in the workshop of the second "
       "reference image: a soft dust sheet is drawn back off the silver Audi R8 from "
       "the first reference image in one continuous pull, and a slow drift of dust "
       "lifts into a shaft of light behind it - and the empty ARCH where the damper "
       "came out is visible on the near side, the old wet damper lying on the floor "
       "beside the wheel. The car underneath is spotless and "
       "clearly unused - tyres clean, a fine settled film on the glass. The pull "
       "continues across the whole clip, revealing the low wide body from nose to "
       "haunch. Continuous movement first frame to last. AUDIO: the soft drag of "
       "fabric over paint, the room's quiet, no engine - no music, no voice. " + _LOOK),

 "E": ("the test drive", "#3F4A55", "EVENT", ["r8"],
       "Vertical 9:16. Low tracking shot alongside the silver Audi R8 from the "
       "reference image at speed on an empty stretch of Malaysian road, warm late "
       "afternoon light: the car runs level and settled, the body barely moving over "
       "an undulation that would have unsettled it before, the wheel and tyre "
       "compressing and rebounding cleanly in the arch. The camera holds beside it, "
       "the road blurring past underneath. Continuous motion first frame to last, the "
       "car never leaving frame. No number plate. AUDIO: the V-engine's hard flat "
       "note under load, tyre roar on coarse tarmac, wind - no music, no voice. "
       + _LOOK),

 "F": ("the verdict at the wheel", "#4A5560", "PAYOFF", ["nev", "r8"],
       "Vertical 9:16. THE PAYOFF. Close-medium from the passenger side onto the man "
       "from the reference images (navy check shirt open over a black tee; face, hair "
       "and EARRING match the references exactly) driving the silver Audi R8 of the "
       "third reference image, both hands on the wheel, late afternoon light crossing "
       "his face through the side glass. He listens to the car for a moment, feels the "
       "road through the wheel, then gives a single satisfied nod and a small closed "
       "smile - the verdict of someone who has just proved his own diagnosis. "
       "Continuous performance first frame to last, three-quarter to the lens, eyes on "
       "the road. No legible instrument display. AUDIO: the engine settled at cruise, "
       "tyre hum, the small creak of the wheel under his hands - no music, no voice. "
       + _LOOK),
}

FRAMING = {
    "A": "macro under the front arch, wheel already off, finger entering frame right",
    "B": "medium at wheel height, HIM working three-quarter to lens, damper drawn down",
    "C": "close over the arch looking down, torque wrench swinging through frame",
    "D": "wide in the bay, sheet pulled left to right off the whole car",
    "E": "low tracking alongside at road speed, car filling the right of frame",
    "F": "close-medium from the passenger side, subject three-quarter, road beyond",
}

SOURCE_REFS = {
    # the technician's face IS the credibility (FORM scan) - B carries it too
    "B": ["assets/nev/face/front_neutral.jpeg",
          "assets/nev/wardrobe/04_check_navy/21_front.jpeg"],
    "F": ["assets/nev/face/front_calm.jpeg",
          "assets/nev/face/profile_right.jpeg",
          "assets/nev/wardrobe/04_check_navy/21_front.jpeg"],
}
FACE_OPTOUT = {
    "A": "gloved hands and the damper only - the evidence is the subject",
    "C": "hands and the torque wrench only - the fix is the subject",
    "D": "no person in frame - the car and the dust are the subject",
    "E": "no person visible - the car's behaviour on the road is the subject",
}

# ------------------------------------------------------------- SHOTS (6 = 48 beats)
# WHOLE CLIPS, REORDER ONLY (HARD RULE 0). Six sources, one appearance each, t_in=0.
# REORDERED 2026-08-12 after planqc 36: the twist sat at 14.77s = 50% of runtime,
# past the 40% cap, and a late reversal is a scroll already gone. Revealing the CAUSE
# before the repair is also the better story - find it, remove it, UNDERSTAND it, fix
# it, prove it, judge it - and it puts the turn at 9.85s = 33%.
SHOTS = [
 ("A", 1.00, "whole", "KI - the wet damper: the fault shown, not claimed"),
 ("B", 1.00, "whole", "the damper comes out, and he is the one taking it out"),
 ("D", 1.00, "whole", "TEN - the dust sheet comes off: this car had been SITTING"),
 ("C", 1.00, "whole", "the new one torqued in, bone dry against the wet one"),
 ("E", 1.00, "whole", "the test drive - the car settled and level at speed"),
 ("F", 1.00, "whole", "KETSU - the nod at the wheel, and the tip that follows"),
]
BEATS = {"whole": 8}

SHOT_TIME = ["morning", "morning", "morning", "morning", "afternoon", "afternoon"]
TIME_JUMPS = {}

TURNS = [
    (4.92,  "the fault stops being a symptom and becomes a job - the tools come out"),
    (9.85,  "THE SHEET COMES OFF - the cause was never hard driving, it was stillness"),
    (14.77, "the new damper goes in, dry against the wet one"),
    (19.69, "the car goes back on the road and behaves"),
    (24.62, "the verdict lands on his face, and the advice follows from it"),
]

TRANSITIONS_PLAN = {
    3: {"kind": "dip", "why": "the film's one chapter change - the workshop closes and "
        "the road opens; a breath between the fix and the proof, landing on the turn"},
}

LINKS = {
 0: {"picture": "the oil film glistening on the damper body -> the same wet body swinging free in his hand",
     "sound":   "the glove's small squeak on metal gives way to the ratchet's clatter - the room gets busy",
     "story":   "the damper is proven wet, SO it comes out"},
 1: {"picture": "the wet unit hanging heavy and dark -> the new unit offered up, dry and unmarked",
     "sound":   "the ratchet's clatter resolves into one clean torque-wrench click",
     "story":   "the old one is out, SO the new one goes in"},
 2: {"picture": "the torque wrench settling on a finished joint -> a dust sheet still lying over the same car",
     "sound":   "the workshop hum drops to room quiet - work stops, and something is about to be shown",
     "story":   "the repair is done, SO the question is what caused it - and the answer is in the bay"},
 3: {"picture": "dust lifting off the paint in a shaft of light -> the same paint moving at road speed",
     "sound":   "the room's quiet is broken by the engine taking load",
     "story":   "the car had been standing still, SO the fix is to DRIVE it - and that is what happens next"},
 4: {"picture": "the wheel compressing cleanly in the arch -> his hands settled on the steering wheel",
     "sound":   "tyre roar eases to a cruise under the creak of the wheel in his hands",
     "story":   "the car behaves, SO he can give the verdict he came to give"},
}

LINKAGE = [
    ("consequence", "damper",  "the damper is proven wet, SO it comes out of the car"),
    ("subject",     "arch",    "the empty arch he has just worked in -> the same arch seen as the sheet comes off"),
    ("subject",     "damper",  "the old wet damper on the floor -> the clean dry one going in to replace it"),
    ("subject",     "arch",    "the new damper torqued into the arch -> that arch working at road speed"),
    ("gaze",        "wheel",   "the front wheel working in the arch -> his hands on the steering wheel"),
]

BLEND_AFTER  = []
BLEND_KIND   = ""
BLEND_WIDTH  = 0.0
SFX_LEAD     = 0.0
IMPACT_AT    = []            # no whoosh-on-every-cut layer: hard cuts stay clean
SUBDROP_AT   = []            # no sub-drops: this is a workshop, not a phonk edit

# SFX SWEETENERS — HIS CATCH 2026-08-12: "are you sure there is no sound effects?
# When Nev is fixing the car, shouldn't there be a sound effect? And the car driving?"
# He was right, and the root cause was one level below the plan: car_advice INHERITED
# edit_sfx='none' from car_review, a PRESENTER format where a voice carries everything.
# In a workshop film the ratchet, the torque click and the engine ARE the content, and
# trusting the generator to produce a crisp mechanical click is a bet, not a plan.
# The pillar policy is now hero_only, and these three moments get a bank sweetener
# LAYERED ON the clip's own diegetic audio - never replacing it.
#   (source_key, clip_time, duration, video_time)
SFX_OVERLAYS = [
    ("B", 1.20, 0.60,  6.10),   # the bolt CRACKING loose - the sound of a seized
                                # fastener letting go, the moment a mechanic knows
                                # the job is real. Bank: sfx/impact, low band, clean.
    ("C", 2.40, 0.45, 17.20),   # THE TORQUE WRENCH CLICK - the film's hero sound and
                                # the sound of a job done properly. Bank: sfx/impact,
                                # short tail, cut_safe. If ONE sweetener survives the
                                # mix, it is this one.
    ("E", 0.80, 1.20, 20.30),   # the engine TAKING LOAD as the road opens - lands on
                                # the dip transition so the picture and the sound
                                # change state together. Bank: sfx/transition, rise.
]
SFX_BANK_QUERY = {   # queries, not filenames: a filename rots, a query does not
    "B": {"bucket": "sfx/impact",     "band": "low",  "cut_safe": True, "clean_only": True},
    "C": {"bucket": "sfx/impact",     "band": "mid",  "cut_safe": True, "clean_only": True,
          "max_tail_ms": 300},
    "E": {"bucket": "sfx/transition", "band": "rise", "cut_safe": True, "clean_only": True},
}

SOUND = {
    "bed":       "PICK from BGM/car_review (or travel_vlog if that bank is thin) at "
                 "native tempo, zero stretch. This film is MUSIC-LED with the "
                 "workshop forward: the bed carries the pacing, the metal carries "
                 "the credibility.",
    "sfx_policy": "hero_only (pillar) - three bank sweeteners on the sound-critical "
                  "moments (SFX_OVERLAYS), each LAYERED ON the clip's own audio. No "
                  "whoosh layer, no sub-drops: the hard cuts stay clean.",
    "hero":      "THE TORQUE WRENCH CLICK on shot 3 - one sharp mechanical click, the "
                 "sound of a job done properly, and the only percussive event in the "
                 "film. Second: the ratchet break-loose crack on shot 1.",
    "hero_shot": 3,   # C sits at index 3 after the reorder
    "duck_shots": [0, 1, 3, 4, 5],
    "silence":   "the quiet point is shot 2 (the dust sheet, -9): the room goes still "
                 "exactly where the film reveals its reason. Quiet before the turn, "
                 "which doctrine wants and this film can actually deliver.",
}
FOLEY = {   # re-mapped to the reordered cut
     0: -6.0,   # A  glove squeak, workshop hum, compressor far off. Forward.
     1: -5.0,   # B  ratchet clatter, the bolt cracking loose. HEARD.
     2: -9.0,   # D  fabric over paint, room quiet - the film's SILENCE, on the turn
     3: -4.0,   # C  the torque wrench CLICK - the hero sound.
     4: -5.0,   # E  engine under load, tyre roar. HEARD.
     5: -6.0,   # F  PAYOFF - the verdict must be HEARD (planqc 19): cruise,
                #    wheel creak, his breath as he nods
}

MIX = {
    "lufs_i_target":  -11.0,     # the level his ear approved on V5 / NIAH_V3
    "true_peak_max":   -1.0,
    "master_limit":    0.631,    # -4.0 dBFS linear: NIAH proved AAC needs the headroom
                                 # (0.891 -> +1.22 dBTP; 0.631 -> -2.10 dBTP)
    "stereo":         "workshop wide, foley centred - never mono",
    "duck_depth_db":  -6,
    "duck_shape":     "sidechain, 50ms attack / 300ms release",
    "loudnorm":       "TWO-PASS, never single",
    "bed_under":      -4.0,      # NEGATIVE = bed sits ABOVE foley (L128 direction,
                                 # the proven travel/car standard - this is NOT the
                                 # ASMR inversion the kitchen film declared)
    "source":         "19-sound-engineer.md + L128 measured flags",
}

CROP_XY   = {}
BAN_SPANS = {}
DELOGO    = {}
CALLBACKS = ["the DAMPER BODY is the film's one object: wet in shot 0, out in his "
             "hand in shot 1, replaced dry in shot 2, and working silently in the "
             "arch in shot 4. One part, four states (file 31 PART G rule 6)."]
SHOT_WINDOW = {}

CARD_Y       = 0.72
CARD_STYLE   = "fragment"
CARD_REGISTER = "card"               # PLANNING DECISION. The car_review references
                                     # measured 2026-08-12 state their subject on a
                                     # white rounded card, top-left, in frame 1 -
                                     # this pillar's own grammar, so the plan adopts
                                     # it and capcards merely obeys.
# NO MONEY FIGURE ON ANY CARD, deliberately: the sources quote 1,500-1,600 per damper
# and ~6,000-6,400 for four, but in an unstated currency on owner forums. A number we
# cannot source in RM is exactly the range-endpoint trap - the film shows the fault
# and gives the advice, and the price stays off screen.
CARDS = [
    ("AUDI R8 MAGNETIC RIDE",          0, 1, "cap"),   # ASCII only: planqc 25 refuses
                                                       # a middot - fallback fonts
                                                       # render TOFU boxes
    ("IT LEAKS FROM SITTING",          2, 1, "cap"),   # ON the turn, now shot 2
    ("DRIVE IT EVERY WEEK",            5, 1, "cta"),
]
AI_LABEL_BURNED_IN = False

RELATIONSHIPS = {
    "subject_vs_background":
        "Four of six shots are macro or medium on metal in a workshop, so the "
        "background is a bay out of focus - stated in every prompt as an "
        "independent shop, never a showroom and never a dealer service line. The "
        "two road shots carry the only daylight, and ingest compares their luma "
        "against the four workshop shots of THIS film rather than against a band.",
    "performance_vs_sound":
        "The single performance beat - the nod at the wheel - carries its own audio "
        "at -8 (cruise, wheel creak, breathing). syncqc refuses a foreground FOLEY "
        "clip with an empty audio lane, and this film's credibility depends on the "
        "mechanical sound being real rather than sweetened.",
    "bed_vs_foley":
        "L128 direction, UNCHANGED (bed above foley): this is a car film, not the "
        "kitchen ASMR case, and the reference pillar is music-led. The torque "
        "wrench click must still cut THROUGH the bed - bedcheck measures the bed, "
        "and the crest-lift at the click is the number that proves the hero sound "
        "survived the mix.",
    "card_vs_card":
        "Three cards on shots 0, 3 and 5 - disjoint by construction, no figures, "
        "white-card register per this pillar's measured references. planqc 12's "
        "clock check blocks any edit that reintroduces an overlap.",
    "event_vs_window":
        "Five of six shots are EVENTs and each declares continuous whole-clip "
        "action stated as a sequence (reach-drag-turn-hold; break-loose-draw-out; "
        "offer-thread-torque-click; pull-reveal; run-compress-rebound). No "
        "'resolves inside N seconds' anywhere - doubly important on whole clips.",
    "arc_vs_shot_order":
        "The repair is irreversible and the order encodes a real shop's sequence: "
        "wheel already off before the damper is touched, old unit out before the "
        "new one goes in, torque before the car comes down, road only after that. "
        "A mechanic in the audience is the harshest reviewer this film has, and "
        "the order is what he checks first.",
    "picture_grid_vs_music_grid":
        "One transition, a zero-reserve dip after shot 3 (L139), inside that shot's "
        "own frames - the timeline cannot drift. verify measures post-build "
        "boundaries against the same 48-beat grid TARGET_S came from.",
    "clip_variety_vs_shot_count":
        "Six sources, six shots, one appearance each. The risk is the inverse of "
        "repetition: four workshop shots could read as one image, so FRAMING "
        "declares four distinct positions (macro under the arch, medium at wheel "
        "height, close over the arch looking down, wide across the bay) and check "
        "13 is the gate that proves they are distinct.",
}

GRADE_SAT    = 1.00
GRADE_BRI    = 0.0
TARGET_BLACK = 10.0
TARGET_SAT   = 74.5

CONTENT = {
    "claim":    "The Audi R8's Magnetic Ride dampers are a widely-reported failure "
                "point: they weep magnetorheological fluid, leaks have been reported "
                "from as little as ~7,000 km with most between 40,000-80,000 km, and "
                "specialists accept that every magnetic damper eventually leaks. Audi "
                "classes them as WEAR ITEMS, so warranty is typically declined. The "
                "cars most at risk are the ones that SIT: when a car stands for long "
                "periods the magnetic fluid settles and damages the seals - which is "
                "why a low-mileage garage-kept R8 is a worse bet than a driven one.",
    "verified": "Fetched 2026-08-12 from Audi R8 owner communities and a reliability "
                "report (r8talk.com threads on magnetic ride failure; audizine thread "
                "on replacing leaking OEM shocks; carchecker.pro Audi R8 V10 Type 42 "
                "reliability report). Consistent across sources: premature leaking "
                "(reports from ~7,000 km, cluster 40,000-80,000 km), 'all magnetic "
                "ride dampers will eventually leak', classified by Audi as wear items "
                "with warranty typically denied, and low-mileage cars that sit are "
                "particularly vulnerable because the fluid settles and damages seals. "
                "DELIBERATELY OFF SCREEN: any PRICE (sources quote per-damper and "
                "four-corner figures in an unstated currency on owner forums - a "
                "number we cannot state in RM does not go on a card), any claim about "
                "a specific model year being worse, any claim that this fault is "
                "unique to the R8 (magnetic dampers across several marques share it), "
                "and any suggestion the repair is DIY - the film shows a workshop.",
    "promise":  "The white card AUDI R8 MAGNETIC RIDE over a finger coming away wet "
                "promises the viewer a specific named fault on a specific named car, "
                "proven on screen in the first seconds rather than asserted.",
    "promise_at": 3.5,
    "payoff_at":  27.0,
    "twist":    "IT LEAKS FROM SITTING. For three shots this reads as a repair film "
                "about a hard-driven supercar; at 9.85s the dust sheet comes off a "
                "spotless, clearly unused car and the cause inverts - the damage came "
                "from stillness, not from driving. Every earlier shot re-reads: the "
                "dust stuck in the oil film, the clean tyres, the untouched brakes. "
                "For a recond audience whose cars sit in garages, this is the most "
                "useful thing the film could tell them.",
    "twist_at": 9.8462,
    "why_stop": "The last card is an instruction an owner can act on this week - "
                "DRIVE IT EVERY WEEK - delivered off a nod rather than a lecture. The "
                "open loop is the viewer's own garage: what else is quietly dying "
                "while it sits? Series thinking: the workshop is now a set we own, "
                "and the next fault is the next video.",
}

PLATES = {
    "nev": {"job": None, "res": "4k", "ar": "4:5", "cr": 0,
            "status": "EXISTS - the measured library; Higgsfield media ids uploaded "
                      "(see plans/panborneo.py PLATES.nev).",
            "identity_refs": ["assets/nev/face/front_calm.jpeg",
                              "assets/nev/face/profile_right.jpeg"],
            "wardrobe_refs": ["assets/nev/wardrobe/04_check_navy/21_front.jpeg"],
            "must_show": "actually him - face, hair, EARRING. Wardrobe: NAVY CHECK "
                         "SHIRT open over a BLACK TEE. No overalls, no branded "
                         "workwear, no cap.",
            "prompt": "(identity from photo references, not regenerated)"},

    "r8": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
            "status": "TO BUILD FIRST at approval - nano_banana_pro 4k, OCR, and "
                      "LOOKED AT before any clip. MANDATORY: a named car is never "
                      "generated from text alone (the Crown lesson - a text-only "
                      "prompt returned a generic crossover and an 87cr build shipped "
                      "wrong for want of a 2cr plate).",
            "must_show": "Audi R8, first-generation Type 42 proportions: mid-engine "
                         "two-seat coupe, very low wide stance, long flat nose with "
                         "a wide single-frame grille, THE SIDE BLADE panel behind the "
                         "door in contrasting finish, wide rear haunches, quad round "
                         "tail pipes, engine visible under a rear glass cover. "
                         "Silver. EMPTY number-plate recess, NO badges, NO model "
                         "lettering anywhere on the body.",
            "prompt":
            "Photograph of a silver Audi R8, first generation, parked three-quarter "
            "front in an independent workshop bay under practical overhead light. "
            "Mid-engine two-seat coupe proportions: very low and wide, long flat "
            "nose with a wide single-frame grille, the signature contrasting SIDE "
            "BLADE panel behind the door, broad rear haunches, quad round exhaust "
            "tips, engine visible beneath a rear glass cover. THE NUMBER-PLATE "
            "RECESS IS EMPTY front and rear - no plate fitted, no badges, no model "
            "lettering of any kind on the body. Full-frame DSLR, 35mm, f/5.6, ISO "
            "400. REAL PHOTOGRAPH ARTEFACTS, not a render: true paint reflections "
            "with the roof lights rolling along the creases, clear-coat orange "
            "peel, faint panel-gap shadows, fine dust on the lower sills, correct "
            "tyre sidewall relief, no HDR halos. Negative: CGI, videogame look, "
            "showroom floor, crowds, any visible registration plate, badge or model "
            "lettering, brand marks on walls or tools, oversaturated poster grade.",
            },

    "workshop": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
            "status": "TO BUILD at approval - nano_banana_pro 4k, OCR before use. "
                      "LOOK at it: it must read as an INDEPENDENT shop, working and "
                      "lived-in, never a dealer service centre.",
            "must_show": "an independent workshop bay: a two-post ramp, a concrete "
                         "floor with old oil marks, a plain tool trolley, coiled air "
                         "line overhead, daylight from a roller door to one side. "
                         "NO brand marks, NO posters, NO legible text anywhere, no "
                         "people.",
            "prompt":
            "Photograph of an independent car workshop bay in daylight: a two-post "
            "ramp standing empty over a concrete floor marked with old oil stains, "
            "a plain steel tool trolley to one side, a coiled air line hanging "
            "overhead, a roller door open at the end of the bay throwing warm "
            "daylight across the floor. Working and lived-in, not a dealer service "
            "centre and not a showroom. NO brand marks, no posters, no signage, no "
            "legible text of any kind, no people. Full-frame DSLR, 24mm, f/5.6, ISO "
            "800. Real photograph artefacts: true metal reflections on the ramp "
            "posts, dust in the daylight shaft, no HDR halos. Negative: CGI, "
            "videogame look, showroom, dealer branding, posters, legible labels, "
            "people, oversaturated grade.",
            },
}

PROBE_FIRST  = "A"   # gloved fingers + fluid + machined metal in one macro frame:
                     # every risk in this film at once (premortem 1 and 3). If A
                     # reads real, the batch is safe. Probe alone (2 plates 8cr +
                     # 22.5cr), LOOK, judge - then per HIS ADJUSTMENT 2 judge EVERY
                     # clip of the batch individually before assembly.

CLIPS = {}

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
