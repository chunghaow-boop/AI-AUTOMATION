"""NEV · UNTIL THE OIL BREAKS — kari ayam in a home kitchen · daily vlog
His title 2026-08-12: "vlog content style... Nev in a kitchen cooking curry
chicken, and then tasting it. I want the whole cooking process to be shown
inside the video. 720p, 30 seconds."

THE INTENT, READ FIRST (his adjustment 1, 2026-08-12: the title is an INTENT
brief, not a subject line):
  He is not asking for a recipe. He is asking to prove NEV IS A PERSON - a
  Malaysian doing an ordinary Malaysian thing at home - because the channel's
  whole asset is a persona the audience trusts. Kari ayam is a HOUSEHOLD dish;
  the video's job is RECOGNITION ("that is how it is done") and APPETITE. And
  "the whole cooking process" is the same note he gave on NIAH: the PROCESS is
  the content, not the finished plate. A film that shows a beautiful curry and
  skips the making has failed this title even if every frame is perfect.

HIS PICKS (readback 2026-08-12, all three = the recommendation):
  sound    = ASMR-LED. Sizzle, chop and bubbling carry the film; the bed sits
             UNDER. This DEPARTS from L128 (travel_vlog is BGM-led) as a stated
             choice - see SOUND below and the new food-vlog note in the ledger.
  the turn = PECAH MINYAK, the moment the oil separates from the rempah.
  captions = ONE Malay term per step: REMPAH · PECAH MINYAK · SANTAN.

REFERENCE SCAN — TWO SCANS (CLAUDE.md step 2, both mandatory)
  SUBJECT (kari ayam, web 2026-08-12): rempah blended from dried chilli,
    shallot, garlic, ginger, galangal, lemongrass, turmeric, coriander, cumin,
    fennel · "rempah empat beradik" = cinnamon, star anise, clove, cardamom ·
    bone-in chicken · santan · potatoes to thicken · and THE technique:
    PECAH MINYAK - fry the rempah until the OIL VISIBLY SEPARATES, the signal
    that the spices have lost their raw edge. That is the receipt no 30-second
    curry short bothers to name.
  FORM (cooking shorts, web 2026-08-12): ASMR IS THE PRODUCT - real frying,
    chopping and sizzling hold viewers with no music needed. Tight close-ups
    MATCHED to the sound (see the oil dance when you hear it). A visual hook in
    frame 1 (gloss, steam, colour). The EATING at the end is the payoff the
    audience waits for. Our own reference library has no food films yet -
    declared, and this build's own numbers become the first entry.

THE UPGRADE OVER THE FIELD, in one line: cooking shorts show STEPS; this one
names the single moment that separates a cook from someone following a recipe,
and spends its turn there.

SPINE: KISHOTENKETSU (file 31 PART E). A kitchen has no antagonist, so three-act
conflict would manufacture fake stakes.
  KI   the knife, the rempah, the pan - the world, quiet
  SHO  the paste goes in and works
  TEN  THE OIL BREAKS - what looked like stirring was a wait, and the cook knew
  KETSU santan, the simmer, and his face on the first taste
"""

PROJECT   = "NEV · UNTIL THE OIL BREAKS · kari ayam · daily vlog"
PILLAR    = "daily_vlog"             # HIS CATCH 2026-08-12: "why is this under the
                                     # travel vlog category? This is a normal vlog."
                                     # Correct - a kitchen is not a road trip, and
                                     # mislabelling means every check judges this
                                     # against travel references. The daily_vlog
                                     # pillar now exists; its NUMBERS are inherited
                                     # from travel_vlog and DECLARED as unmeasured
                                     # until real daily-vlog references are added.
PILLAR_FIT = ("daily_vlog, created after his catch that a kitchen is not a road trip. "
    "DIFFED AGAINST travel_vlog key by key: numbers (duration band, cut rate, shot "
    "median, picture_baseline) INHERITED and declared UNMEASURED until real daily-vlog "
    "references exist; sound direction INVERTED by his pick - cooking shorts are "
    "ASMR-led so the bed sits UNDER the foley, the opposite of L128, and bedcheck must "
    "be read inverted for this film; edit_sfx inherited as-is because the kitchen's own "
    "diegetic audio IS the sweetener (the sizzle is generated with the clip) - stated "
    "here so it is a decision, not an omission (L165).")

GEN_MODE  = "coverage"
BPM       = 97.5
BEAT      = 60.0 / BPM               # 0.615385s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"                   # his standing call - 720p IS the cost strategy
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 29.5385                  # 48 beats = 6 whole clips x 8 beats.
                                     # His 30s request and HARD RULE 0 agree here.

LESSONS_ACK = {
    "general craft": 168,            # incl. L167-L169 (QC is the final boss · layers
                                     # owe a decision · gates ship with negative
                                     # controls) · L161 BOARD QC, L162 prove the field a
                                     # gate reads · L159 create the pillar, never rent the
                                     # name · L160 the board shows what will be SENT ·
                                     # L144 whole clips are an order, L147
                                     # scan the FORM not just the subject, L148
                                     # kishotenketsu is our native spine, L149 the
                                     # triple link, L151 process mechanics, L158
                                     # his three pipeline adjustments.
    "travel vlog":    9,             # nearest ledger topic; daily_vlog has no
                                     # lessons yet and this build starts it.
                                     # tvL9 THE JOURNEY IS THE PRODUCT - here the
                                     # journey is the COOK: prep -> transform ->
                                     # serve. planqc 39 is answered by JOURNEY.
    "bmw i8 car cinematic": 16,
    "car cinematic": 15,
    "toyota land cruiser 300 zx car review": 8,
}

PREMORTEM = [
    ("HANDS AND FOOD ARE THE GENERATOR'S WORST CLASS - warped fingers, six-finger "
     "hands, chicken that morphs mid-shot. This film is ALL hands and food, and "
     "craft L102's mid-action gate can pass a clip whose hands are wrong",
     "Every prompt names REAL HANDS, five fingers, natural knuckles and nails, and "
     "the negative block carries extra-fingers/warped-hands FIRST. The PROBE is A "
     "(the rempah close-up, hands + knife + texture): one 22.5cr clip LOOKED AT "
     "before the other five spend anything, and per his adjustment 2 EVERY clip is "
     "then judged individually before assembly - hands checked on each."),

    ("THE FOOD READS AS PLASTIC (the CGI tell): uniform colour, no steam, no "
     "specular wetness, glossy videogame surfaces. An unappetising curry fails the "
     "film's whole intent even if the story lands",
     "Every food prompt states REAL FOOD PHOTOGRAPHY artefacts: visible steam, oil "
     "sheen catching light, uneven browning, sauce clinging unevenly, real "
     "condensation on the pot rim. Negative: CGI, plastic food, uniform colour, "
     "stock-photo gloss. Judged on the probe frame BEFORE the batch."),

    ("A KITCHEN IS FULL OF LEGIBLE TEXT (the mahua invented-signage defect): "
     "packet labels, brand names on bottles, a rice-cooker display, sachet print. "
     "Any of it invents a brand we do not own",
     "Every prompt: NO PACKAGING, NO LABELS, NO BRAND MARKS, no legible text on any "
     "surface - ingredients sit in plain bowls and on plain boards. clipqc text-zoom "
     "runs on EVERY clip at ingest (his adjustment 2), not just the probe."),

    ("'RESOLVES INSIDE N SECONDS' WRITES THE OTHER FOUR (craft #99). The oil "
     "breaking, the chicken searing and the first taste are all sub-second events "
     "inside 5s clips, and this film plays WHOLE CLIPS - every second is on screen",
     "Every prompt declares what fills the WHOLE clip: C is 'the paste darkens, "
     "the oil pools and separates, the spoon drags through it - continuous "
     "transformation first frame to last'. 'Resolves inside N seconds' appears "
     "nowhere."),

    ("SCENE-BLIND IDENTITY REFS (craft L116, his catch on desafarm): a hands-only "
     "macro does not want three front faces, and the taste shot needs the smile",
     "SOURCE_REFS picks per scene: the taste (F) gets front_smile + front_calm; the "
     "wide kitchen (E) gets front_neutral; the hands-only shots (A, C, D) declare "
     "FACE_OPTOUT and carry no face refs at all - identity there is wardrobe, "
     "forearms and continuity."),
]

_LOOK = (
    "A real Malaysian home kitchen, warm practical light. REAL FOOD PHOTOGRAPHY, "
    "NOT A RENDER: visible steam, oil sheen catching the light, uneven browning, "
    "sauce clinging unevenly, condensation on metal, natural handheld micro-shake, "
    "shallow depth of field. REAL HANDS: five fingers, natural knuckles and nails, "
    "correct anatomy at all times. Negative: CGI, plastic or waxy food, uniform "
    "colour, stock-photo gloss, videogame look, extra fingers, warped or merged "
    "hands, NO PACKAGING, NO LABELS, NO BRAND MARKS, no legible text on any "
    "surface, no on-screen graphics, no chef whites, no restaurant kitchen."
)

# ------------------------------------------------------------- SOURCES (6 x 22.5cr)
SOURCES = {
 "A": ("THE REMPAH — hands, knife, colour", "#B8562A", "EVENT", ["kitchen"],
       "Vertical 9:16. Macro, top-down over a worn wooden board in the home kitchen "
       "of the reference image, warm window light from the left. A man's hands - "
       "sleeves pushed up, no watch - slice a stalk of lemongrass and sweep it into "
       "a small mound of blended rempah: deep brick-red, coarse, glistening. Beside "
       "it, plain white bowls of sliced shallot, garlic, a knob of ginger, dried "
       "chillies, and a small dish of cinnamon, star anise and cloves waiting to one side. The hands work continuously first frame to last - slice, sweep, "
       "press the paste with the flat of the knife so it shines. INGREDIENTS SIT IN "
       "PLAIN BOWLS ON A PLAIN BOARD: no packets, no labels, no lettering anywhere. "
       "AUDIO: the knife's rhythm on wood, the dry rustle of chilli, a shallot's "
       "wet crunch - close, dry, no music, no voice. " + _LOOK),

 "B": ("the pan takes the heat", "#8C3B1E", "PLACE", ["kitchen"],
       "Vertical 9:16. Low three-quarter view of a battered steel pan on a gas ring "
       "in the kitchen of the reference image, blue flame licking its base. Oil goes "
       "in and spreads, thinning as it heats, the surface beginning to shimmer and "
       "move; a cinnamon stick, two star anise and a few cloves drop in and swell, "
       "turning slowly in the oil, releasing thin ribbons of steam. Continuous "
       "movement first frame to last - the oil never sits still. AUDIO: the gas ring's "
       "low roar, oil ticking as it heats, the small crackle as the whole spices go "
       "in - no music, no voice. " + _LOOK),

 "C": ("PECAH MINYAK — the oil breaks", "#A8431F", "EVENT", ["kitchen"],
       "Vertical 9:16. THE TURN OF THE FILM. Tight macro straight down into the pan "
       "from the reference image: the brick-red rempah is frying hard around the cinnamon stick from before, a wooden spoon "
       "dragging through it in slow continuous circles. Across the clip the paste "
       "DARKENS from bright red to deep rust, and OIL VISIBLY SEPARATES OUT OF IT - "
       "first a few clear orange beads at the edge of the spoon's trail, then pools "
       "of glistening red-gold oil standing clear of the paste, sliding back into the "
       "channel the spoon leaves. Continuous transformation first frame to last, "
       "steam rising through the light. Real chilli-oil colour, real bubbling at the "
       "edges. AUDIO: a hard, wet, continuous sizzle that thickens as the paste "
       "dries, the spoon scraping the pan - the loudest sound in the film; no music, "
       "no voice. " + _LOOK),

 "D": ("chicken in, santan follows", "#C4763A", "EVENT", ["kitchen"],
       "Vertical 9:16. Close over the pan of the reference image: bone-in chicken "
       "pieces go into the dark fried rempah and are turned with the wooden spoon, "
       "each piece taking on the red-brown coat, the surfaces tightening and browning "
       "where they touch the metal. Then thick white coconut milk pours in from a "
       "plain jug in a slow steady stream, blooming white through the red and "
       "marbling as it is stirred, the whole pan turning a warm orange; potato "
       "chunks slide in after it. Continuous action first frame to last: turn, pour, "
       "stir. Plain jug, no label. AUDIO: the sear when the chicken meets the pan, "
       "the pour, the sizzle dropping to a lower rolling bubble as the santan lands "
       "- no music, no voice. " + _LOOK),

 "E": ("the simmer, and him waiting", "#7A5230", "HUMAN", ["kitchen", "nev"],
       "Vertical 9:16. Wider, waist-height: the man from the reference images (navy "
       "check shirt open over a black tee, sleeves pushed up; face, hair and EARRING "
       "match the references exactly) stands at the stove in the home kitchen of the "
       "second reference image, one hand on the pan handle, watching the curry move, a potato surfacing and sinking in the sauce. "
       "The pot breathes: thick orange sauce rising in slow domes and collapsing, oil "
       "beading gold on the surface, steam curling past his face into the window "
       "light. He lifts the lid, leans in, and the steam hits him - he blinks and "
       "grins at it. Continuous first frame to last, three-quarter to the lens. "
       "AUDIO: the fat rolling bubble of a curry at simmer, the lid's small clink, "
       "his breath in the steam - no music, no voice. " + _LOOK),

 "F": ("THE FIRST TASTE", "#B5603B", "PAYOFF", ["nev", "kitchen"],
       "Vertical 9:16. THE PAYOFF. Close-medium on the man from the reference images "
       "(navy check over black tee; face, hair and EARRING match exactly) in the "
       "kitchen of the third reference image: he lifts a wooden spoon of orange curry "
       "to his mouth, blows once across it, and tastes. The reaction runs across the "
       "whole clip - eyes widening slightly, a pause while it lands, then a slow nod "
       "and a grin he cannot hold back; he goes back for a second taste. Continuous "
       "performance first frame to last, facing the lens. Real steam off the spoon, "
       "real sheen on the sauce. AUDIO: the small breath blown across the spoon, the "
       "taste, his quiet laugh, the pot still bubbling behind him - no music, no "
       "voice. " + _LOOK),
}

FRAMING = {
    "A": "macro top-down on the board, hands entering frame left, no face",
    "B": "low three-quarter on the pan, flame visible under it, no hands",
    "C": "tight macro straight down into the pan, spoon crossing frame, no face",
    "D": "close over the pan at 45 degrees, jug entering high, no face",
    "E": "waist-height wide, subject three-quarter at the stove, pot in foreground",
    "F": "close-medium, subject facing lens, spoon entering from below frame",
}

# ------------------------------------------------------------- SCENE REFS (L116)
SOURCE_REFS = {
    "E": ["assets/nev/face/front_neutral.jpeg",
          "assets/nev/wardrobe/04_check_navy/21_front.jpeg"],
    "F": ["assets/nev/face/front_smile.jpeg",
          "assets/nev/face/front_calm.jpeg",
          "assets/nev/wardrobe/04_check_navy/24_front.jpeg"],
}
FACE_OPTOUT = {
    "A": "hands and board only by composition - the rempah is the subject",
    "B": "no person in frame at all - the pan is the subject",
    "C": "hands and pan only - the oil breaking is the subject",
    "D": "hands and pan only - the santan bloom is the subject",
}

# ------------------------------------------------------------- SHOTS (6 = 48 beats)
# WHOLE CLIPS, REORDER ONLY (HARD RULE 0). Six sources, one appearance each,
# t_in=0, 8 beats each = 4.923s of every 5.04s clip. ORDER IS THE ONLY EDIT.
SHOTS = [
 ("A", 1.00, "whole", "KI - hands, knife, the rempah: the world of the film, quiet"),
 ("B", 1.00, "whole", "the pan takes the heat, whole spices swell in the oil"),
 ("C", 1.00, "whole", "TEN - PECAH MINYAK: the oil separates and the wait pays"),
 ("D", 1.00, "whole", "chicken in, then santan blooms white through the red"),
 ("E", 1.00, "whole", "the simmer, and him waiting in the steam"),
 ("F", 1.00, "whole", "KETSU - the first taste, and the grin he cannot hold back"),
]
BEATS = {"whole": 8}                 # 4.9231s each · 6 x 8 = 48 beats = 29.5385s

SHOT_TIME = ["morning"] * 6          # one continuous cook in one light state
TIME_JUMPS = {}

# ------------------------------------------------------------- STORY (planqc 35/36)
TURNS = [
    (4.92,  "the board becomes the fire - preparation ends, cooking begins"),
    (9.85,  "THE OIL BREAKS - stirring turns out to have been waiting, and he knew"),
    (14.77, "the pan stops being spice and becomes a curry: chicken and santan"),
    (19.69, "the work ends and the WAIT begins - he stands in his own steam"),
    (24.62, "the wait pays on his face"),
]

# JOURNEY (planqc 39). A cooking vlog's journey is the COOK itself - his note on
# NIAH applies: the process IS the content, so the beats are prep -> transform ->
# serve, and the audience never joins late.
JOURNEY = {"depart": 0, "transit": 1, "arrive": 3}   # prep -> heat -> the
                                                    # dish EXISTS (chicken+santan)
                                                    # by 60%, leaving the simmer
                                                    # and the taste to pay it off

TRANSITIONS_PLAN = {
    2: {"kind": "dip", "why": "the film's one chapter change: the rempah stops "
        "being ingredients and becomes the base - a breath between the making and "
        "the cooking, on the turn"},
}

LINKS = {
 0: {"picture": "the red rempah pressed on the board -> the same red waiting to meet oil in the pan",
     "sound":   "the dry knife-on-wood rhythm gives way to the gas ring's low roar - the room gets hotter",
     "story":   "the paste is finished, SO the fire is lit"},
 1: {"picture": "oil shimmering in the empty pan -> that same oil already carrying the paste",
     "sound":   "the ticking of heating oil thickens into a hard continuous sizzle",
     "story":   "the pan is ready, SO the rempah goes in and the work begins"},
 2: {"picture": "clear orange oil standing free of the darkened paste -> the same oil coating chicken skin",
     "sound":   "the dry sizzle drops as cold chicken hits the heat",
     "story":   "the oil has broken, SO the base is ready and the chicken can go in"},
 3: {"picture": "white santan marbling through the red -> the same orange sauce breathing in the pot",
     "sound":   "the sear falls to a fat rolling bubble - the pan changes state",
     "story":   "the curry exists now, SO there is nothing left to do but wait"},
 4: {"picture": "steam curling past his face at the pot -> the same steam rising off the spoon at his mouth",
     "sound":   "the simmer stays under while his breath crosses the spoon",
     "story":   "the wait is over, SO he finds out whether it worked"},
}

LINKAGE = [
    ("consequence", "star anise", "the whole spices waiting beside the board -> the same star anise swelling in the hot oil"),
    ("subject",     "cinnamon",   "the cinnamon stick turning in clean oil -> the same stick riding the paste as it breaks"),
    ("subject",     "wooden spoon","the spoon dragging through broken oil -> the same spoon turning chicken in it"),
    ("subject",     "potato",     "the potato chunks settling in -> the same potato surfacing in the simmer"),
    ("gaze",        "grin",       "the grin the steam pulls out of him -> the grin the taste confirms"),
]

BLEND_AFTER  = []
BLEND_KIND   = ""
BLEND_WIDTH  = 0.0
SFX_LEAD     = 0.0
IMPACT_AT    = []            # no whoosh layer: an ASMR film's cuts stay clean
SUBDROP_AT   = []

# SFX SWEETENERS — added 2026-08-12 after planqc 41 caught the same gap here that
# he caught by ear on the R8 film. This is an ASMR-LED film: the sizzle IS the
# product, which makes it the WORST thing to leave entirely to the generator.
# Two sweeteners, layered ON the clip's own audio, never replacing it.
#   (source_key, clip_time, duration, video_time)
SFX_OVERLAYS = [
    ("A", 0.90, 0.35,  1.10),   # the knife's first strike on the board - the sound
                                # that tells a viewer in the scroll-decision second
                                # that this film is going to sound GOOD
    ("C", 1.60, 1.40, 11.40),   # PECAH MINYAK - the hard wet fry as the paste dries
                                # and the oil breaks. The hero sound of the film; if
                                # one sweetener survives the mix, it is this one.
]
SFX_BANK_QUERY = {
    "A": {"bucket": "sfx/impact", "band": "mid",  "cut_safe": True, "clean_only": True,
          "max_tail_ms": 200},
    "C": {"bucket": "sfx/texture", "band": "high", "cut_safe": True, "clean_only": True},
}

# ------------------------------------------------------------- SOUND
# HIS PICK 2026-08-12: ASMR-LED. This is a STATED DEPARTURE from L128 (travel_vlog
# is BGM-led, bed OVER foley) and the reason is measured, not preference: the FORM
# scan found cooking shorts are carried by real frying/chopping sound, often with
# no music at all - "the sound IS the product". The bed becomes a floor, not the
# anchor. bedcheck.py's PASS condition (bed >= foley) MUST THEREFORE BE INVERTED
# for this film - run it expecting FAIL and read the number, or the gate is
# measuring the wrong doctrine (L136: calibrate the gate against what is true here).
SOUND = {
    "bed":       "PICK from BGM/travel_vlog at native tempo, zero stretch, and sit "
                 "it 6-8 dB UNDER the foley - a warm floor under the kitchen, never "
                 "the anchor. If a bed fights the sizzle, the bed loses.",
    "hero":      "THE SIZZLE AT PECAH MINYAK (shot 2) - a hard, wet, continuous fry "
                 "that thickens as the paste dries. It is the loudest thing in the "
                 "film and the sound the whole video is built around.",
    "hero_shot": 2,
    "duck_shots": [0, 1, 2, 3, 5],
    "silence":   "the quiet point is shot 4 (the simmer, -8): the fat slow bubble "
                 "after the work stops. It is the breath before the taste.",
}
FOLEY = {   # per-shot clip audio, ASMR-forward: five of six sit at or above -6
     0: -5.0,   # A  knife on wood, chilli rustle, shallot crunch. HEARD.
     1: -6.0,   # B  gas roar, oil ticking, whole spices crackling in. HEARD.
     2: -3.0,   # C  PECAH MINYAK - the hero sizzle. LOUDEST.
     3: -4.0,   # D  the sear, the pour, the drop to a rolling bubble. HEARD.
     4: -8.0,   # E  the simmer under him - the film's quiet point
     5: -5.0,   # F  the breath across the spoon, the taste, his laugh. HEARD.
}

MIX = {
    "lufs_i_target":  -11.0,     # the level HIS EAR approved on PANBORNEO_V5/NIAH_V3
    "true_peak_max":   -1.0,     # measured spec; NIAH proved the codec needs headroom
    "master_limit":    0.631,    # LINEAR, -4.0 dBFS. NIAH_V3 solved this by iteration:
                                 # 0.891 -> +1.22 dBTP, 0.794 -> -0.04, 0.708 -> -0.66,
                                 # 0.631 -> -2.10 dBTP. TRUE peak is oversampled and
                                 # always exceeds sample peak.
    "stereo":         "kitchen wide, foley centred - never mono",
    "duck_depth_db":  -6,
    "duck_shape":     "sidechain, 50ms attack / 300ms release",
    "loudnorm":       "TWO-PASS, never single",
    "bed_under":       6.0,      # POSITIVE = bed sits UNDER foley (the ASMR read)
    "source":         "19-sound-engineer.md + the FORM scan (cooking shorts are "
                      "carried by diegetic sound). Departure from L128 is DECLARED.",
}

CROP_XY   = {}
BAN_SPANS = {}
DELOGO    = {}
CALLBACKS = ["the wooden spoon appears in shots 2, 3 and 5 - it stirs the oil that "
             "breaks, folds in the santan, and finally carries the taste to his "
             "mouth. One object, three jobs, whole film (file 31 PART G rule 6)."]
SHOT_WINDOW = {}                     # WHOLE CLIPS: every shot starts at t_in=0

CARD_Y       = 0.72
CARD_STYLE   = "fragment"
CARD_REGISTER = "quiet"              # PLANNING DECISION (the plan decides, capcards
                                     # obeys): the vlog reference read says this
                                     # pillar WHISPERS - small lowercase on a
                                     # barely-there scrim, not the industry punch.
# One Malay term per step - his pick. Teaches while it shows, and the words are the
# recognition hook for a Malaysian audience. Spans disjoint by construction.
CARDS = [
    ("rempah",            0, 1, "cap"),
    ("pecah minyak",      2, 1, "cap"),
    ("santan",            3, 1, "cap"),
    ("the wait",          4, 1, "cap"),
]
AI_LABEL_BURNED_IN = False

RELATIONSHIPS = {
    "subject_vs_background":
        "Four of six shots are macro on the pan or board, so the background is the "
        "kitchen out of focus - stated in every prompt as warm practical light, "
        "never a restaurant kitchen and never chef whites. Ingest compares the two "
        "human shots' luma against the four macro shots of THIS film, not against a "
        "band, because a macro over a dark pan is legitimately darker.",
    "performance_vs_sound":
        "His two performance beats each carry their own audio at the declared level: "
        "the steam-blink at the simmer (-8, the quiet point) and the taste (-5, "
        "breath + laugh over the bubbling). Performed emotion is backed by place "
        "sound; syncqc refuses an empty foreground lane.",
    "bed_vs_foley":
        "INVERTED FOR THIS FILM BY HIS PICK: the bed sits 6-8 dB UNDER the foley "
        "because cooking content is ASMR-led. bedcheck.py's PASS condition assumes "
        "the L128 direction and MUST be read inverted here - the number still gets "
        "measured and recorded, but a 'FAIL' that shows foley above bed is this "
        "film's PASS. Declared so nobody 'fixes' it later.",
    "card_vs_card":
        "Four cards, one per step, spans 0 · 2 · 3 · 4 - disjoint by construction, "
        "no figures, lowercase quiet register at y=0.72. planqc 12's clock check "
        "blocks any edit that reintroduces an overlap.",
    "event_vs_window":
        "Three EVENTs (the rempah work, the oil breaking, the chicken+santan) each "
        "declare continuous whole-clip action with the transformation stated "
        "('darkens', 'separates', 'blooms') - no 'resolves inside N seconds' "
        "anywhere, which matters doubly because every clip plays whole.",
    "arc_vs_shot_order":
        "The cook is irreversible and the order encodes it: paste -> heat -> oil "
        "breaks -> chicken+santan -> simmer -> taste. A viewer who cooks would catch "
        "any swap instantly, which is the point - the recognition IS the content.",
    "picture_grid_vs_music_grid":
        "One transition, a zero-reserve dip after shot 2 (L139), inside the shot's "
        "own frames - the timeline cannot drift. verify measures post-build "
        "boundaries against the same 48-beat grid TARGET_S came from.",
    "clip_variety_vs_shot_count":
        "Six sources, six shots, ONE appearance each - the strictest possible "
        "answer to the repeat-framing and composition-dupe checks. The risk is the "
        "opposite one: four macro pan shots could read as the same image, so FRAMING "
        "declares four distinct camera positions (top-down board, low three-quarter "
        "with flame, straight-down macro, 45-degree over the pan) and check 13 is "
        "the gate that proves it.",
}

GRADE_SAT    = 1.00
GRADE_BRI    = 0.0
TARGET_BLACK = 10.0
TARGET_SAT   = 74.5

CONTENT = {
    "claim":    "Malaysian kari ayam is built on a rempah of dried chilli, shallot, "
                "garlic, ginger, galangal, lemongrass and ground spice, fried in oil "
                "with cinnamon, star anise, clove and cardamom - the 'rempah empat "
                "beradik' - until PECAH MINYAK, the point at which the oil visibly "
                "separates from the paste and the spices lose their raw edge; only "
                "then do the chicken, the santan and the potatoes go in.",
    "verified": "Fetched 2026-08-12. Method and ingredient order cross-checked "
                "across four independent kari ayam sources (dailylifestyleguide, "
                "hankerie, glebekitchen, farahjeats): rempah composition (6-8 dried "
                "chilli, shallot, garlic, ginger, galangal, lemongrass, turmeric, "
                "coriander, cumin, fennel); whole spices named as 'rempah empat "
                "beradik' = cinnamon, star anise, clove, cardamom; bone-in chicken; "
                "thin santan; potatoes added to thicken; and the technique stated "
                "explicitly - 'cook the spice paste until the oil separates, a stage "
                "known as PECAH MINYAK'. DELIBERATELY OFF SCREEN: exact quantities "
                "and timings (a 30s film that states a 40-minute simmer invites a "
                "correction it cannot defend), any regional claim about whose recipe "
                "this is (Malay, Nyonya and Indian-Malaysian versions differ and the "
                "film does not adjudicate), and any health or origin claim.",
    "promise":  "The card 'rempah' over a board of hand-cut aromatics promises the "
                "viewer this is made from scratch, not from a packet - the thing that "
                "separates a home cook from a shortcut, stated in the first shot.",
    "promise_at": 4.0,
    "payoff_at":  27.0,
    "twist":    "PECAH MINYAK. For half the film he appears to be stirring; at 9.85s "
                "the oil visibly separates out of the paste and the shot re-frames "
                "everything before it - he was not stirring, he was WAITING for a "
                "signal, and he knew it was coming. A viewer who cooks recognises it "
                "instantly; a viewer who does not has just learned the one thing that "
                "makes the dish work.",
    "twist_at": 9.8462,
    "why_stop": "The last frame is his face deciding, then going back for a second "
                "spoon - the film ends on appetite rather than on a plated dish, so "
                "the open loop is the viewer's own hunger and the question the "
                "caption asks: what would you have put in it? Series thinking: the "
                "kitchen is a set we now own, and the next dish is a video.",
}

PLATES = {
    "nev": {"job": None, "res": "4k", "ar": "4:5", "cr": 0,
            "status": "EXISTS - the measured library; Higgsfield media ids already "
                      "uploaded (see plans/panborneo.py PLATES.nev): front_neutral "
                      "efdb9f44 · front_calm 44009a35 · front_smile 66e529c7 · "
                      "profile_right 1bdbaed4 · back_head 451cdf9d.",
            "identity_refs": ["assets/nev/face/front_smile.jpeg",
                              "assets/nev/face/front_calm.jpeg",
                              "assets/nev/face/front_neutral.jpeg"],
            "wardrobe_refs": ["assets/nev/wardrobe/04_check_navy/21_front.jpeg"],
            "must_show": "actually him - face, hair, EARRING. Wardrobe: NAVY CHECK "
                         "SHIRT open over a BLACK TEE, SLEEVES PUSHED UP (he is "
                         "cooking), no watch, no apron, no chef whites.",
            "prompt": "(identity from photo references, not regenerated)"},

    "kitchen": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
            "status": "TO BUILD at approval - nano_banana_pro 4k, OCR before use "
                      "(glc300 protocol). LOOK at it: it must read as a HOME "
                      "kitchen, lived-in, not a showroom and not a restaurant line.",
            "must_show": "a Malaysian home kitchen: worn laminate counter, a gas "
                         "hob with a battered steel pan, a wooden board, plain "
                         "white bowls, a window throwing warm light across the "
                         "counter, a tiled splashback. Lived-in: a tea towel, a "
                         "spoon rest, faint use-marks. NO packaging, NO labels, NO "
                         "brand marks, no legible text anywhere, no people.",
            "prompt":
            "Photograph of a modest Malaysian home kitchen in warm late-morning "
            "light: a worn laminate counter beside a gas hob carrying a battered "
            "steel pan, a scratched wooden chopping board, plain white ceramic "
            "bowls holding shallots and dried chillies, a tiled splashback, a "
            "window to the left throwing soft warm light across the counter, a "
            "cotton tea towel hanging over the oven rail. Lived-in and ordinary, "
            "not styled, not a showroom, not a restaurant kitchen. NO packaging, "
            "no jars with labels, no brand marks, no legible text of any kind, no "
            "people. Full-frame DSLR, 35mm, f/2.8, ISO 400. Real photograph "
            "artefacts: soft window falloff, faint scratches on the counter, "
            "true metal reflections on the pan, no HDR halos. Negative: CGI, "
            "videogame look, showroom kitchen, chef whites, stainless restaurant "
            "surfaces, product packaging, legible labels, oversaturated food-blog "
            "grade, people."},
}

PROBE_FIRST  = "A"   # the rempah macro: HANDS + KNIFE + FOOD TEXTURE in one frame,
                     # which is every risk in this film at once (premortem 1 and 2).
                     # If A's hands and food read real, the batch is safe. Probe it
                     # alone (kitchen plate 4cr + 22.5cr), LOOK, judge - and then per
                     # HIS ADJUSTMENT 2 judge EVERY clip of the batch individually
                     # before assembly.

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
