"""NEV · INTO THE HOLLOW MOUNTAIN — Batu Niah, Miri · daily travel vlog
His title 2026-08-12: "Nev daily Vlog going to Batu Niah in miri sarawak hiking,
and exploring the cave" — 30 seconds, 720p, "show the process of hiking in Batu
Niah seeing caves, bats, weird insects."

HIS PICKS (readback 2026-08-12, all four = my recommendations, approved "go for it"):
  hook   = COLD OPEN IN THE DARK - headlamp beam finds a weird insect (creature
           event inside 3s, file 31 rule 1/2)
  twist  = "THOSE AREN'T STARS." - the cave ceiling's glints stir into wings,
           twist_at 11.08s = 37.5% of runtime (rule 4, <=40%)
  cliff  = the Painted Cave death-ships card (rule 5 - the open loop names
           episode 2; Wikipedia verbatim: "paintings and wooden coffin 'death
           ships'")
  voice  = BGM-led, no VO, cards carry the facts (the proven pillar; L128 mix)

REFERENCE SCAN (web, 2026-08-12): cave shorts are walk-into-the-dark POV with
creature jump-scares and ZERO facts. THE UPGRADE: a verified receipt no cave
TikTok carries - people lived in this exact darkness 40,000 years ago - and the
scale twist STAGED (ceiling stars -> wings) rather than stumbled into.

VERIFIED FACTS (fetched 2026-08-12, full citations in CONTENT):
  UNESCO WHS listed 27 July 2024 · Great Cave WEST MOUTH 150m WIDE x 75m HIGH
  (Barker 2007 via Wikipedia - the tourism newsletter's "60m high, 250m wide"
  CONFLICTS and is REJECTED; academic citation wins) · human occupation ~40,000
  years, oldest recorded settlement in East Malaysia (first activity ca.
  46,000-34,000 BP) · 3km elevated plankwalk from park HQ · Great Cave hosts
  guano-feeding cockroaches incl. Symploce strinatii, ENDEMIC to the cave; park
  holds 25 phasmid + 11 mantid species (the "weird insects" are documented) ·
  at dusk thousands of roundleaf bats spiral OUT while swiftlets stream IN ·
  Painted Cave: rock art dated 1,200 years + wooden-coffin "death ships".

STRUCTURE: 18 shots / 48 beats at the travel_vlog tempo class. Story process arc
exactly as he asked: hike (1-4) -> the door (5-6) -> cave dark + ceiling twist
(7-8) -> insects (9-11) -> bats (12-16) -> out (17). Cold open (0) is the dark
itself. Three declared time jumps carry the day: dark->morning (the rewind out),
midday->cave-dark (walking into the mountain), cave-dark->dusk (the cave ate the
afternoon).
"""

PROJECT   = "NEV · INTO THE HOLLOW MOUNTAIN · Batu Niah · daily travel vlog"
PILLAR    = "travel_vlog"
GEN_MODE  = "coverage"
BPM       = 97.5                     # PROVISIONAL tempo class (liqwyd measured);
                                     # the bed is PICKED ON HIS BOX from
                                     # BGM/travel_vlog at its native tempo, zero
                                     # stretch; recompute BEAT/TARGET_S from the
                                     # same 48-beat arithmetic if it differs.
BEAT      = 60.0 / BPM               # 0.615385s
W, H, FPS = 720, 1280, 30
MODE      = "std"                    # NEVER fast (quality defaults)
RES       = "720p"                   # HIS STANDING CALL 2026-08-12: 720p IS the
                                     # cost strategy. No upscale. Do not re-raise.
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 27.0769                  # 44 beats at 97.5 (12 burst + 5 med) -
                                     # r2: 48 beats broke the pillar's 29s ceiling

LESSONS_ACK = {                      # counts MEASURED 2026-08-12 (planqc 23)
    "general craft": 153,   # incl. L146-L154 (L150 refs were half-read;
                                     # L151 TIMESTAMPS are the journey mechanic): a rule that lives only in a RESUME
                                     # line is not in the system (this plan is the
                                     # test case - HARD RULE 0 + planqc 38 + shape)            # written against L128-L140 incl. L136
                                     # re-acked 2026-08-12 after L141-L145:
                                     # L141 storyboard=tools/storyboard.py, L142 the
                                     # Chrome bridge, L143 window arithmetic, L144
                                     # WHOLE CLIPS IS AN ORDER (this plan's shape),
                                     # L145 a declared light state is not a measured
                                     # one (V1's daylight ending - the reorder fixed it).
                                     # (calibrate gates), L137 (caption legibility
                                     # is a property of the footage - this plan's
                                     # cards ride the pill scrim), L139 (zero-
                                     # reserve fades), L140 (per-scene transition
                                     # selection - TRANSITIONS_PLAN below exists
                                     # because of it)
    "travel vlog":    9,             # incl. tvL9 THE JOURNEY IS THE PRODUCT (his
                                     # NIAH_V2 catch - this plan still owes it,
                                     # planqc 39 blocks until V3 adds the beats).
                                     # Also L5 whip timeline theft (no whip in
                                     # this film at all), L7 bed-window scan
    # NEIGHBOURING PILLARS (planqc 23b): i8 L9-L12 (3s retention > watch time,
    # hooks under 2s complete 23% better - the cold-open insect is a 1.2s
    # creature event), lc300 L7 (image_references PLURAL on every human shot),
    # car cinematic cutting doctrine (transitions must be EARNED - this film
    # plans 3, all on story turns).
    "bmw i8 car cinematic": 16,
    "car cinematic": 15,
    "toyota land cruiser 300 zx car review": 8,
}

PREMORTEM = [
    ("A PARK SIGNBOARD SHIPS (the mahua defect: an invented sign grew on a post "
     "with 'no signage' in prompt AND negative). A national-park boardwalk is "
     "high signage-pressure: trail markers, interpretive boards, distance posts, "
     "safety rails with stencilled text",
     "Every exterior prompt states THE FRAME CONTAINS NO SIGNBOARD, NO TRAIL "
     "MARKER, NO PAINTED OR STENCILLED TEXT - planks, jungle and limestone carry "
     "the image. clipqc text-zoom runs on every exterior at ingest; the contact "
     "sheet is READ for invented text before assembly."),

    ("THE CAVE INTERIOR CRUSHES TO SILHOUETTE MUSH (craft #101: 'fully exposed' "
     "is not an instruction until you say expose for WHAT - the desafarm cabin "
     "metered the windscreen and shipped a 37.7-luma black hole). A cave is this "
     "channel's ULTIMATE dark-interior risk - five of eighteen shots live inside "
     "the mountain",
     "Every interior prompt carries its metering target as the loudest line: "
     "EXPOSE FOR THE HEADLAMP POOL - the beam's pool and what it touches carry "
     "the image; the darkness around it stays TEXTURED, never pure black. Ingest "
     "compares each clip's luma against THIS film's other interiors (the outlier "
     "test that actually catches it), and the blank-frame gate's blur-vs-black "
     "blind spot is known - interiors get eyeballed on the contact sheet."),

    ("'RESOLVES INSIDE N SECONDS' WRITES THE OTHER FOUR (craft #99): the insect "
     "find, the ceiling stir and the exodus are all sub-second events inside 5s "
     "clips",
     "Every EVENT prompt declares what fills the WHOLE clip: A is 'the beam "
     "searches, finds, holds - the insect reacts, antennae reading the air, "
     "continuous'; E is 'glints, then stirring, then motion spreading - "
     "continuous escalation'; G is 'bats pouring first frame to last, density "
     "rising'. 'Resolves inside N seconds' appears in NO prompt."),

    ("SCENE-BLIND IDENTITY REFS (craft L116, his catch): headlamp shots and the "
     "walk-in silhouette do not want three front faces",
     "SOURCE_REFS picks per scene: the walk-in (D) is back-to-camera by "
     "composition (FACE_OPTOUT declared); the sweat pause and the awe/grin get "
     "front refs; wardrobe (04_check_navy, this film's continuity: same outfit "
     "as panborneo - a daily-vlog series wears its wardrobe) repeated inside "
     "every human prompt."),

    ("THE BAT SWARM RENDERS AS NOISE OR MORPH-SOUP (many-small-objects is the "
     "generator's known weak class; the mid-action gate L102 can pass a clip "
     "whose swarm is visually mush)",
     "G IS THE PROBE (PROBE_FIRST) - one 22.5cr clip, LOOKED AT before the other "
     "nine spend a credit. The prompt anchors scale ('each bat a distinct dark "
     "wingbeat against the dusk sky, not particles, not smoke') and the judge "
     "panel's realism seat rules on the probe frame before batch."),

    ("CARDS CLASH WITH THE FOOTAGE (L137 - his own catch on V5, white on bright "
     "road; this film swings the other way: bright pill on near-black cave "
     "frames can glare",
     "Cards render via capcards.py (pill scrim + keyword highlight, the locked "
     "standard) and capcheck.py gates every span at >=4.5:1 on the FINAL frames "
     "- the gate is calibrated (fails V5's exact defect) and runs in the "
     "pipeline's final-gates step, not on faith."),
]

_LOOK = (
    "Equatorial Borneo, true texture on skin, fabric, leaf, limestone and guano. "
    "REAL FOOTAGE, NOT A RENDER: handheld micro-shake, natural depth of field, "
    "true darkness gradients around torchlight, no HDR halos. Negative: CGI, "
    "videogame look, postcard oversaturation, invented signage text, signboards, "
    "trail markers, painted or stencilled text, legible device screens, any "
    "legible slogan wordmark logo or printed graphic on clothing, extra fingers, "
    "warped faces, drone-stock look."
)

# ------------------------------------------------------------- SOURCES (10 x 22.5cr)
SOURCES = {
 "A": ("EVENT · THE THING IN THE BEAM", "#3B2F2F", "EVENT", ["niah_interior"],
       "Vertical 9:16. INSIDE A DARK CAVE, near-black. Inside the dark chamber of the reference image, a headlamp beam - the only "
       "light - sweeps slowly across wet limestone and dark guano, ITS POOL "
       "CARRYING THE IMAGE: EXPOSE FOR THE HEADLAMP POOL, the darkness around it "
       "textured, never pure black. The beam finds a LARGE CAVE INSECT - a "
       "long-legged cave cricket, whip-thin antennae longer than its body - "
       "frozen on the rock. The antennae MOVE, reading the air, the insect "
       "shifting one leg at a time. The beam searches, finds, holds; the insect "
       "reacts - continuous first frame to last, never settling. Real chitin "
       "gloss in the beam, real rock wetness. AUDIO: cave silence made of drips "
       "and space, the faint dry tick of the insect's legs on stone - no music, "
       "no voice. " + _LOOK),

 "B": ("the plankwalk - boots and sweat", "#4C6B45", "HUMAN", ["nev"],
       "Vertical 9:16. MORNING, hot equatorial light in shafts through high "
       "canopy. An elevated wooden plankwalk runs single-file through dense "
       "Borneo rainforest. The man from the reference images (navy check shirt "
       "open over a black tee, dark trousers, small day-pack; face, hair and "
       "EARRING match the references exactly) hikes TOWARD the lens along the "
       "planks - boots landing on old timber, sweat already darkening the tee's "
       "collar - then in the clip's second half he STOPS, wipes his forehead "
       "with a forearm and LOOKS UP AND PAST the camera at something enormous "
       "off-frame, chest moving from the climb. Continuous movement first frame "
       "to last. THE FRAME CONTAINS NO SIGNBOARD, NO TRAIL MARKER, NO PAINTED "
       "TEXT - planks, jungle and light carry the image. AUDIO: boots on "
       "timber, insect drone, birds high up, his breathing - no music, no "
       "voice. " + _LOOK),

 "I": ("the boardwalk ribbon", "#2E5339", "PLACE", ["niah_mouth"],
       "Vertical 9:16. MORNING. From above the canopy edge, looking down a "
       "long diagonal: the wooden plankwalk a thin pale ribbon threading "
       "unbroken dark-green Borneo rainforest toward the limestone massif of "
       "the reference image rising in the far haze, one small figure moving along "
       "it, heat haze over the trees. The camera drifts slowly forward along "
       "the ribbon's line - continuous glide first frame to last. No signage, "
       "no structures beyond the plankwalk. AUDIO: the forest wide - cicada "
       "wall, distant hornbill wingbeats - no music, no voice. " + _LOOK),

 "C": ("the limestone wall", "#6E6A5E", "PLACE", ["niah_mouth"],
       "Vertical 9:16. TWO DECLARED LOOKS IN ONE LIGHT MOVE, morning to dusk "
       "impossible in one clip - so THIS clip is MORNING ONLY on the first "
       "look and its second use is windowed late: the camera tilts up from "
       "dense green canopy to the sheer grey limestone massif above the cave "
       "mouth of the reference image rising out of the "
       "jungle - Gunung Subis - vine-streaked rock climbing until it fills the "
       "frame, swifts wheeling as specks against it. Continuous tilt first "
       "frame to last. No signage. AUDIO: wind against rock, swift cries thin "
       "and high - no music, no voice. " + _LOOK),

 "D": ("THE DOOR - the west mouth", "#4A4239", "HUMAN", ["niah_mouth", "nev"],
       "Vertical 9:16. MIDDAY, flat bright. From inside the shadow line of the "
       "Great Cave's west mouth looking out: the opening a vast ragged arch of "
       "daylight - 150 metres wide, 75 high, jungle burning green beyond - and "
       "the man from the reference images (navy check shirt over black tee, "
       "day-pack) walks INTO frame from behind the camera and AWAY toward the "
       "light, back to camera the whole clip, his figure shrinking against the "
       "scale of the arch until he is a small dark silhouette on the guano "
       "floor. Continuous walk first frame to last. Stalactite fringe on the "
       "arch, swiftlets crossing as flecks. AUDIO: the acoustic OPENING - "
       "outside jungle hiss arriving through cave reverb, wingbeats echoing - "
       "no music, no voice. " + _LOOK),

 "E": ("THE CEILING OF STARS", "#1C2333", "EVENT", ["niah_interior"],
       "Vertical 9:16. DEEP CAVE DARK. Inside the dark chamber of the reference image, camera low, tilted up at its vast unseen "
       "ceiling: hundreds of tiny glints hang in the blackness like a star "
       "field - points of reflected torchlight high above, dense and still. "
       "EXPOSE FOR THE GLINTS AND THE BEAM: darkness textured, never pure "
       "black. A headlamp beam sweeps up across them - and the stars STIR: "
       "first a few points shivering, then patches of the 'sky' rippling as "
       "wings unfold, motion spreading across the ceiling - continuous "
       "escalation first frame to last, glints becoming movement. AUDIO: "
       "drips, then a dry leathery rustle building overhead, a first thin "
       "chitter - no music, no voice. " + _LOOK),

 "F": ("the floor is alive", "#3A3226", "WILDLIFE", ["niah_interior"],
       "Vertical 9:16. CAVE DARK inside the chamber of the reference image, headlamp pool on its sloping bank of guano. "
       "EXPOSE FOR THE POOL. The surface is MOVING: dark glossy cockroaches "
       "and long-limbed cave insects working the guano, dozens in the beam's "
       "circle, antennae and legs in constant motion; when the beam shifts, "
       "the edge of the pool SCATTERS - insects pouring away from the light "
       "into the dark. Continuous movement first frame to last, macro-real "
       "chitin and texture, unsettling and true. AUDIO: a fine dry rustle "
       "like paper moving, drips behind it - no music, no voice. " + _LOOK),

 "G": ("EVENT · THE EXODUS", "#2B2B3A", "EVENT", ["niah_mouth"],
       "Vertical 9:16. DUSK, the sky over the jungle gone orange-grey. From "
       "below the dark cave mouth of the reference image: BATS POUR OUT - first ropes, then a "
       "continuous spiralling column twisting out of the arch and bending over "
       "the canopy, EACH BAT A DISTINCT DARK WINGBEAT AGAINST THE DUSK SKY, "
       "not particles, not smoke, not static - density rising first frame to "
       "last, the column alive and turning. Swiftlets cut the opposite way, "
       "streaming IN under the bats. Continuous, never settling. AUDIO: the "
       "wing-thunder - thousands of leathery wingbeats layered into a soft "
       "roar, chittering through it, jungle dusk below - no music, no voice. "
       + _LOOK),

 "H": ("he watches the sky empty the mountain", "#40342C", "HUMAN", ["nev", "niah_mouth"],
       "Vertical 9:16. DUSK. Close-medium on the man from the reference images "
       "(navy check shirt over black tee, headlamp pushed up on his hair, off; "
       "face, hair and EARRING match the references exactly) standing at the "
       "cave mouth's rim, lit by the last warm sky: he looks UP, following "
       "movement across the sky, mouth opening slightly - pure awe - then the "
       "awe breaks into a slow disbelieving grin, head shaking once. "
       "Continuous performance first frame to last, facing the lens, eyes "
       "above it. AUDIO: wing-rush and chitter passing overhead, dusk insects "
       "starting - no music, no voice. " + _LOOK),

 "J": ("ribbons over the black jungle", "#232B2B", "PLACE", ["niah_mouth"],
       "Vertical 9:16. LAST LIGHT, the sky a dying orange band over silhouette "
       "jungle. Long ribbons of bats stream from the direction of the reference image's black massif, crossing the frame high up - loose "
       "winding lines of distinct wingbeats crossing the afterglow, thinning "
       "and thickening, unhurried and endless. Continuous drift first frame "
       "to last, no ground detail, just sky, ribbons and the black canopy "
       "line. AUDIO: far wing-rush almost gone, dusk insects rising from "
       "below - no music, no voice. " + _LOOK),
}

# FRAMING (planqc 28) - every camera position stated.
FRAMING = {
    "A": "macro-low inside the beam pool, insect on rock, darkness around",
    "B": "eye-level on the planks, subject toward lens then the stop-and-look-up",
    "I": "high oblique above the canopy edge, boardwalk ribbon receding",
    "C": "tilt up from canopy to the massif face filling frame",
    "D": "from inside the shadow line looking OUT through the arch, subject away",
    "E": "low tilt-up at the ceiling star-field, beam entering frame",
    "F": "macro-down on the guano bank inside the beam pool",
    "G": "low outside the mouth, column spiralling up and over the canopy",
    "H": "close-medium at the rim, subject facing lens, eyes above it",
    "J": "sky-only wide, ribbons crossing the afterglow band",
}

# ------------------------------------------------------------- SCENE REFS (L116)
SOURCE_REFS = {
    # B: toward-lens hike + the look-up -> both fronts + shirt front.
    "B": ["assets/nev/face/front_neutral.jpeg",
          "assets/nev/face/front_calm.jpeg",
          "assets/nev/wardrobe/04_check_navy/21_front.jpeg"],
    # D: back to camera the whole clip -> back of head + shirt back.
    "D": ["assets/nev/face/back_head.jpeg",
          "assets/nev/wardrobe/04_check_navy/23_back.jpeg"],
    # H: awe -> grin facing lens -> smile + calm fronts + shirt front.
    "H": ["assets/nev/face/front_smile.jpeg",
          "assets/nev/face/front_calm.jpeg",
          "assets/nev/wardrobe/04_check_navy/24_front.jpeg"],
}

FACE_OPTOUT = {"D": "back to camera against the arch for the whole clip - the "
                    "composition is the SCALE, a figure against a 75m door; "
                    "identity carried by wardrobe back + build + the series' "
                    "continuity, refs above"}

# ------------------------------------------------------------- SHOTS (10 = 80 beats)
# WHOLE CLIPS, REORDER ONLY — his standing order, restated 2026-08-12 on V1:
# "do not simply cut unless analyzed fully then cut. if not, just piece all the
# scene together fully." V1's 17-shot version chopped 5.04s sources into 1.23s
# bursts and used each source twice to hit the 30s title spec; he judged the RAW
# FOOTAGE GOOD and the CUT wrong. The title's duration is a REQUEST, this is an
# ORDER, so the film got LONGER (49.23s) rather than choppier. planqc 38 now
# blocks any unjustified cut or reuse. ORDER IS THE ONLY EDIT DECISION - and this
# order also fixed V1's ending defect for free (ends on dusk ribbons, not C's
# bright daylight cliff; see L145 - a declared light state is not a measured one).
SHOTS = [
 ("A", 1.00, "whole", "COLD OPEN - the beam finds the cricket in the dark, antennae first"),
 ("B", 1.00, "whole", "morning: the plankwalk, boots and sweat - the walk back to the dark"),
 ("I", 1.00, "whole", "the plankwalk from above - a ribbon through unbroken jungle, the mouth visible in the canopy"),
 ("C", 1.00, "whole", "the wall arrives - the limestone massif out of the canopy"),
 ("D", 1.00, "whole", "THE DOOR in that wall - he walks into the arch, shrinking against 75 metres"),
 ("E", 1.00, "whole", "THE TWIST - the ceiling star field STIRS into wings"),
 ("F", 1.00, "whole", "the floor is alive - the guano bank the wings feed on, working and scattering from the beam"),
 ("G", 1.00, "whole", "THE EXODUS - the mountain exhales wings, the column bends over the canopy"),
 ("H", 1.00, "whole", "the spiral lands on his face - awe breaks into the grin"),
 ("J", 1.00, "whole", "the sky he sees: ribbons of wingbeats on the last orange band"),
]
BEATS = {"whole": 8}                 # 8 beats = 4.923s of each 5.04s clip
                                     # 10 x 8 = 80 beats = 49.2308s
SHOT_TIME = ["night", "morning", "morning", "morning", "midday",
             "night", "night", "dusk", "dusk", "dusk"]
TIME_JUMPS = {
    0: "COLD OPEN. Shot 0 is the cave dark - the destination shown first - and "
       "shot 1 rewinds to the morning trail that walks back to it. The flash "
       "punctuates the jump.",
    4: "WALKING INTO THE MOUNTAIN. Midday dies at the drip line; inside is its "
       "own night. The dip IS that boundary - geography, not clock.",
    6: "THE CAVE ATE THE AFTERNOON. He turns for the mouth and the light has gone "
       "to dusk - which is WHEN the exodus happens (verified). Flash bookends it.",
}
TURNS = [
    (4.92,  "the dark -> the morning trail that walks back to it"),
    (14.77, "the jungle ends at a wall - the hike becomes a descent"),
    (19.69, "the door: daylight dies, the mountain takes him"),
    (24.62, "the ceiling STIRS - those aren't stars (the twist detonates)"),
    (34.46, "the mountain empties - exodus at dusk, the emotion event"),
    (44.31, "the awe lands on a human face, then on the sky he sees"),
]
TRANSITIONS_PLAN = {
    0: {"kind": "flash", "why": "the one backwards jump - beam OFF the insect INTO "
        "morning; flash is time-jump grammar and works from a static macro frame"},
    4: {"kind": "dip",   "why": "walking into the mountain - the chapter change; "
        "daylight dies at the drip line and the dip IS that death"},
    6: {"kind": "flash", "why": "the second time jump - cave dark snaps to dusk, "
        "bookending the descent"},
}
CARDS = [
    ("GUA NIAH. 3KM TO THE DOOR.",          1, 1, "cap"),
    ("A DOOR 75 METRES HIGH",               4, 1, "cap"),
    ("THOSE AREN'T STARS.",                 5, 1, "cap"),
    ("PEOPLE SLEPT HERE 40,000 YEARS AGO",  6, 1, "cap"),
    ("DEATH SHIPS. NEXT CAVE.",             8, 1, "cta"),
]
FOLEY = {0:-5.0, 1:-7.0, 2:-9.0, 3:-8.0, 4:-4.0,
         5:-4.0, 6:-6.0, 7:-3.0, 8:-6.0, 9:-8.0}
SHOT_WINDOW = {}                     # WHOLE CLIPS: every shot starts at t_in=0.
                                     # A window IS a cut - planqc 38 territory.
TARGET_S = 49.2308                   # 80 beats at 97.5. Longer than the title's
                                     # "30 seconds" BY ORDER: whole-clip beats the
                                     # duration request when they conflict (L144).

# ---- V1 ARCHIVE (superseded 2026-08-12, kept as the record of the wrong cut) --
# _V1_SHOTS_SUPERSEDED = [
# process arc: [0] cold open dark | [1-4] the hike | [5] the door | [6-10] inside:
# ceiling twist + insects | [11-15] the exodus | [16] out.
# r2: fully interleaved (zero adjacent same-source pairs), every pair of shots
# from one source carries DISTINCT crops (repeat-framing), twist at 36.4%.
# SHOTS = [
#  ("A", 1.00, "burst", "COLD OPEN - the beam finds the cricket in the dark, antennae first"),
#  ("B", 1.00, "burst", "morning: boots hit the plankwalk - the walk that leads back to the dark"),
#  ("I", 1.00, "burst", "the plankwalk a ribbon through unbroken jungle - the scale of the walk"),
#  ("B", 1.15, "burst", "the walk stops: sweat wiped, and he looks UP at the wall"),
#  ("C", 1.20, "burst", "the wall arrives - the limestone massif rising out of the canopy"),
#  ("D", 1.00, "burst", "the wall opens: THE DOOR - he walks into the arch's dark, shrinking"),
#  ("E", 1.12, "burst", "the dark holds a star field - the ceiling glints under the beam"),
#  ("F", 1.15, "burst", "the beam drops to the floor - the guano is moving"),
#  ("E", 1.00, "med",   "back up the beam: THE STIR - the ceiling is alive, stars into wings"),
#  ("F", 1.00, "burst", "the floor is alive too - it scatters from the beam"),
#  ("A", 1.25, "med",   "one tenant does not run from the beam: the cricket, closer - the mountain's smallest, his breath held"),
#  ("G", 1.15, "burst", "the mountain exhales - first ropes of bats out of the mouth"),
#  ("H", 1.00, "burst", "at the rim he follows the ropes up, mouth open"),
#  ("G", 1.00, "med",   "the ropes braid into THE COLUMN - the exodus spirals over the canopy"),
#  ("H", 1.15, "med",   "the spiral lands on his face - awe breaks into the grin, head tipping back to the sky"),
#  ("J", 1.00, "med",   "the sky he sees: ribbons of wingbeats on the afterglow"),
#  ("C", 1.00, "burst", "the massif black against the same afterglow, still bleeding bats"),
# ]

# BEATS = {"burst": 2, "med": 4}       # at 97.5: burst 1.2308s, med 2.4615s
                                     # 12 bursts + 5 meds = 44 beats = 27.0769s

# planqc 30 - light states with three declared jumps.
# SHOT_TIME = ["night",                                  # 0  the cold open dark
#              "morning", "morning", "morning", "morning",  # 1-4 the hike
#              "midday",                                 # 5  the door
#              "night", "night", "night", "night", "night", # 6-10 inside the mountain
#              "dusk", "dusk", "dusk", "dusk", "dusk", "dusk"]  # 11-16 the exodus

# TIME_JUMPS = {
#     0:  "COLD OPEN. Shot 0 is the cave dark itself - the film's destination shown "
#         "first - and shot 1 rewinds to the morning trail that walks back to it. "
#         "The flash transition at this boundary punctuates the jump.",
#     5:  "WALKING INTO THE MOUNTAIN. Midday dies at the drip line - inside is its "
#         "own night. The dip transition IS this boundary: geography, not clock.",
#     10: "THE CAVE ATE THE AFTERNOON. He turns for the mouth and outside the light "
#         "has gone to dusk - the honest cave-day compression, and dusk is WHEN the "
#         "exodus happens (verified changeover). Flash punctuates the second jump.",
# }

# ------------------------------------------------------------- STORY (planqc 35/36)
# TURNS = [
#     (1.2308,  "the dark -> the morning trail that walks back to it (cold open pays off at shot 6)"),
#     (6.1538,  "the jungle ends at a wall with a DOOR - the hike becomes a descent"),
#     (7.3846,  "daylight dies - inside the mountain, the ceiling reads as a star field"),
#     (9.8462,  "the stars STIR - the ceiling is alive (the twist detonates)"),
#     (16.0000, "the mountain empties - exodus at dusk, the film's emotion event"),
#     (20.9231, "the awe lands on a human face - the day gets its meaning"),
# ]

# per-scene transitions, LIVE kinds only (planqc 37); each on a TURN, each with
# its own sound bucket - no whoosh anywhere in this film, nothing whips.
# TRANSITIONS_PLAN = {
#     0:  {"kind": "flash", "why": "the film's one backwards jump - beam OFF the "
#          "insect INTO morning; a flash is time-jump grammar and works from the "
#          "static macro frame (whip cannot)"},
#     5:  {"kind": "dip",   "why": "walking into the mountain - the geography/chapter "
#          "change; daylight dies at the drip line and the dip IS that death"},
#     10: {"kind": "flash", "why": "the second time jump - cave dark snaps to dusk "
#          "outside; same grammar as the cold-open exit, bookending the descent"},
# }

LINKAGE = [
    ("consequence","dark",      "the dark holds tenants, SO the film rewinds to the walk back into the dark"),
    ("motion",     "plankwalk", "boots on the plankwalk -> the same plankwalk read as a ribbon from above"),
    ("place",      "jungle",    "the plankwalk's jungle from above -> the jungle the limestone wall rises out of"),
    ("subject",    "wall",      "the wall of limestone -> the wall opening: the door in that same wall"),
    ("light",      "dark",      "the arch's dark swallows his silhouette -> the dark his beam now owns, starred"),
    ("subject",    "beam",      "the beam on the stirring ceiling -> the beam dropped to the floor it feeds"),
    ("motion",     "wings",     "wings unfolding off the floor's edge -> wings pouring out of the mouth"),
    ("gaze",       "sky",       "the column bending across the sky -> his face turned up into that sky"),
    ("subject",    "sky",       "the sky on his face -> the sky itself, ribboned, holding the last light"),
]


# ---- THE TRIPLE LINK (file 31 PART F, his order 2026-08-12) -------------------
# Every boundary declares what the EYE carries, what the EAR carries, and what the
# next shot MEANS because of this one. One link is a transition; three is a story
# beat. Rendered per boundary by tools/storyboard.py and gated by planqc 40, so
# the whole chain is inspectable BEFORE generation.
# READ-ALOUD TEST: the 'story' column, in order, must read as one paragraph.
LINKS = {
 0: {"picture": "the headlamp flare blows to white -> the same white arriving as morning sun shafts through canopy",
     "sound":   "the cave's enclosed drip-and-space cuts to an open cicada wall - the room becomes a forest",
     "story":   "the dark has tenants, SO the film rewinds to the walk that leads back into it"},
 1: {"picture": "his boots landing on the planks -> the same plank line read from above as a ribbon",
     "sound":   "boots and breath fall back into a wide forest bed - human scale to map scale",
     "story":   "the walk at body height becomes the walk at map height: how far there still is to go"},
 2: {"picture": "the ribbon points at rising ground -> the rock it was always aiming at",
     "sound":   "the canopy hiss narrows to wind moving over stone",
     "story":   "the walk has a destination, and the destination is a wall"},
 3: {"picture": "grey limestone fills the frame -> the same limestone read as the arch's edge",
     "sound":   "wind on rock becomes cave reverb - the room changes size around the mic",
     "story":   "a wall that big has to open somewhere, and it does"},
 4: {"picture": "his silhouette swallowed by the arch's shadow -> that shadow itself, starred",
     "sound":   "the reverb tail carries through and drips enter under it",
     "story":   "inside, the dark turns out not to be empty"},
 5: {"picture": "the beam leaves the ceiling and lands on the floor",
     "sound":   "the leathery rustle overhead hands over to a dry paper rustle below",
     "story":   "what hangs above feeds on what moves below - the cave is one animal"},
 6: {"picture": "wings scattering from the beam -> wings pouring out of the arch",
     "sound":   "the close dry rustle opens into distant wing-thunder",
     "story":   "the mountain has been holding all of this, and now it lets go"},
 7: {"picture": "the column bending across the dusk sky -> his face turned up into that same sky",
     "sound":   "the wing-thunder passes overhead and thins to dusk insects",
     "story":   "the event needs a witness before it means anything"},
 8: {"picture": "his head tipping back -> the sky he is looking at, ribboned",
     "sound":   "the last wing-rush recedes under a rising evening floor",
     "story":   "the day ends inside the thing he came for, and it is still going without him"},
}

BLEND_AFTER  = []                    # legacy path empty - TRANSITIONS_PLAN carries
BLEND_KIND   = ""                    # this film's transitions (flash/dip, L139
BLEND_WIDTH  = 0.0                   # zero-reserve fades inside each shot's own
                                     # frames; executor = the proven v6 mechanism)

SFX_LEAD     = 0.0
IMPACT_AT    = []                    # no whoosh, no impact layer - HIS CATCH
SUBDROP_AT   = []                    # 2026-08-12 ("mostly whoosh") honoured: each
                                     # transition brings its own bucket per bank.

SOUND = {
    "bed":       "PICK ON HIS BOX from BGM/travel_vlog at native tempo, zero "
                 "stretch. Tempo class 97.5 provisional; recompute the 48-beat "
                 "grid if the picked bed differs. Mood: warm/organic morning -> "
                 "held-breath sparse in the cave -> swelling for the exodus.",
    "hero":      "THE WING-THUNDER on shot 13 - thousands of layered wingbeats, "
                 "the film's one irreplaceable sound, generated in G's own clip "
                 "audio and paid for. Second hero: the ceiling rustle at shot 8 "
                 "(the twist heard before it is understood).",
    "hero_shot": 7,   # G, the exodus (whole-clip order)
    "duck_shots": [0, 4, 5, 6, 7, 8],   # every foreground line (>= -6) in the
                                        # 10-shot whole-clip order
    "silence":   "the near-silence sits at shot 6 (the star field, drips at -9): "
                 "doctrine's quiet-before-the-twist, PRESENT in this film "
                 "(unlike panborneo's waived one) because the twist lives "
                 "mid-film where quiet can precede it.",
}

# SUPERSEDED by the whole-clip block above (2026-08-12) — kept for the record
# FOLEY = {   # per-shot clip audio (generate_audio=true), foreground >= -6
#      0:  -5.0,   # A  the insect tick + cave space. Forward - it IS the hook.
#      1:  -7.0,   # B  boots on timber, jungle
#      2:  -9.0,   # I  cicada wall wide under the bed
#      3:  -6.0,   # B  his breathing after the climb - the effort heard
#      4:  -8.0,   # C  wind on rock, swift cries
#      5:  -4.0,   # D  the acoustic OPENING - reverb arrives. HEARD.
#      6:  -9.0,   # E  drips and space - the quiet before the twist
#      7:  -7.0,   # F  the fine dry paper-rustle of the floor
#      8:  -4.0,   # E  THE RUSTLE builds overhead. The twist heard. HEARD.
#      9:  -6.0,   # F  the scatter - legs on guano, forward
#     10:  -6.0,   # A  the cricket close, his held breath audible
#     11:  -5.0,   # G  first ropes - wing-rush arriving
#     12:  -7.0,   # H  wing-rush passing overhead at the rim
#     13:  -3.0,   # G  THE EXODUS wing-thunder. The film's hero sound. HEARD.
#     14:  -6.0,   # H  the grin - dusk insects rising under it
#     15:  -8.0,   # J  far wing-rush thinning, evening floor
#     16:  -8.0,   # C  wind on the black rock, the last chitter
# }

MIX = {
    "lufs_i_target":  -8.0,
    "band_body_pct":   45,
    "band_air_pct":     4,
    "stereo":         "wide bed, foley centred - never mono",
    "hero_layers":    "shot 13's wing-thunder = G's native clip audio PLUS bank "
                      "sweeteners (bank.pick role=hit/texture, cut_safe) layered "
                      "transient/body/tail; shot 8's rustle likewise from G/E "
                      "audio + bank texture - named sources, no unnamed library",
    "duck_depth_db":  -6,
    "duck_shape":     "sidechain, 50ms attack / 250ms release - no stepping",
    "loudnorm":       "TWO-PASS, never single; alimiter level=disabled",
    "source":         "19-sound-engineer.md measured reference profile + L128 "
                      "finalmix flags (--foley-target -22 --bed-under -4 "
                      "--duck-ratio 2 --duck-release 300) - the travel_vlog "
                      "standard, bedcheck-gated",
}

CROP_XY   = {}
BAN_SPANS = {}          # filled AT INGEST from measured clips
DELOGO    = {}
CALLBACKS = ["shot 11 answers shot 0 - the same species, closer; the cold open "
             "was a promise and the film keeps it"]

# Pins - conservative head/tail picks, REFINE AT INGEST from motion curves.
# SUPERSEDED by the whole-clip block above (2026-08-12) — kept for the record
# SHOT_WINDOW = {
#     0: 0.30, 10: 2.50,    # A: the find | the closer read
#     1: 0.30,  3: 3.30,    # B: boots toward | the stop-and-look-up
#     5: 0.30,              # D: the walk-in - arch + shrinking silhouette in one
#     6: 0.30,  8: 2.50,    # E: still stars | the stir - the mini-arc cannot reverse.
                          # r2 2026-08-12: glints rise 53->172, stir peaks late ->
                          # window pushed as late as a MED PHYSICALLY FITS: a 2.46s
                          # med + 0.08 tail in a 5.04s clip caps the window at 2.50
                          # (build r1 measured the 3.40 pin overrunning the source -
                          # audio 2.04s short, NaN median. Windows obey arithmetic.)
#     7: 0.40,  9: 3.40,    # F: working floor | the scatter
#    11: 0.30, 13: 2.30,    # G: first ropes | full column (density must RISE)
#    12: 0.50, 14: 2.50,    # H: the up-follow | the grin
#     4: 0.30, 16: 3.30,    # C: morning tilt | late-window black-against-afterglow
# }

# CARD REGISTER — A PLANNING DECISION, NOT A RENDERER DEFAULT (2026-08-12).
# The reference read (file 31 PART H) showed text register is per-pillar; the
# PLAN chooses it here and tools/capcards.py merely obeys. Keeping the decision
# in the planning phase is his explicit instruction - the build phase executes,
# it never decides. Options: quiet (vlog whisper) · punch (industry/default) ·
# display (cinematic) · card (review) · time (the journey clock chip).
# THIS FILM: 'punch' is retained deliberately - the delivered V2 shipped with it
# and his eye approved those cards. 'quiet' is what the travel_vlog references
# actually do and is the candidate for V3, HIS CALL at the gate.
# CLIP PACKAGE (added 2026-08-12, field research): name the standalone moments
# BEFORE generating - the editor gets a map, and one paid batch carries more than
# one post. 233cr / 3 posts = 77.7cr per post instead of 233. Directly attacks the
# standing gap: the cheapest post is the one already paid for.
CLIP_PACKAGE = {
    "the film (49s)":            [0,1,2,3,4,5,6,7,8,9],
    "THOSE AREN'T STARS (12s)":  [5, 6],      # the twist, standalone
    "the exodus + the face (15s)": [7, 8, 9], # the emotion event, standalone
}

# MASTER + BED, decided here (2026-08-12, both defects PROVEN by measurement):
#  MASTER_LIMIT 0.794 (-2.0 dBFS) not 0.891: a mix limited to -1.0 decodes from AAC
#    at -0.09 dBFS - the encoder adds ~+0.75 dB and we left it no headroom, which is
#    why the delivered V2 measured +1.2 dBTP against a -1.0 spec. Tested: 0.794 lands
#    SOLVED BY ITERATION, not assumption: 0.794 gave TP -0.04 (still over), 0.708
#    gave -0.66, 0.631 (-4.0 dBFS) lands TRUE PEAK -2.10 dBTP. TRUE peak is
#    oversampled and always exceeds sample peak - measuring sample peak fooled me
#    once today. The limiter was never at fault (it clamps a +6 dBFS test tone
#    to exactly -1.00); the gain staging was.
#  BED_SS 89.9862s sits ON THE TRACK-S OWN BEAT. First attempt used 89.8462 (an
#    integer multiple of the beat from ZERO) and made it WORSE - 81.6ms vs 60.5ms -
#    because the track-s first beat is NOT at t=0. MEASURED phase: 140ms. The old 90.0 was 146.25 beats,
#    so the bed started a quarter-beat late and every cut inherited it: verify
#    check 2 measured cuts a median 60.5 ms off the grid with only 33% inside 50 ms.
MASTER_LIMIT = 0.631
BED_SS       = 89.9862

CARD_REGISTER = "punch"
CARD_Y       = 0.72
CARD_STYLE   = "fragment"
# Five cards, spans 1-2 · 5 · 8 · 9-10 · 14-15, disjoint by construction; CTA
# ends at shot 15 so the cut to the black massif ANSWERS it (J0 doctrine).
# Rendered by capcards.py (pill + keyword), gated by capcheck >= 4.5:1.
# Figures: 3KM and 75 METRES both carry named fetched sources (below); 40,000
# carries Wikipedia's own wording class ("human remains from 40,000 years ago").
# SUPERSEDED by the whole-clip block above (2026-08-12) — kept for the record
# CARDS = [
#     ("GUA NIAH. 3KM TO THE DOOR.",          1, 2, "cap"),   # the hike, named + measured
#     ("A DOOR 75 METRES HIGH",               5, 1, "cap"),   # the arch, academic figure
#     ("THOSE AREN'T STARS.",                 8, 1, "cap"),   # THE TWIST, said at detonation
#     ("PEOPLE SLEPT HERE 40,000 YEARS AGO",  9, 2, "cap"),   # the receipt no cave TikTok has
#     ("DEATH SHIPS. NEXT CAVE.",            14, 2, "cta"),   # the cliff - ep 2 named,
                                                            # answered by the cut to
                                                            # the black massif
# ]
AI_LABEL_BURNED_IN = False           # platform AI toggle at upload - HUMAN step

RELATIONSHIPS = {
    "subject_vs_background":
        "Interior shots live or die on beam-vs-dark: every interior prompt "
        "states EXPOSE FOR THE POOL and 'darkness textured, never pure black', "
        "and ingest compares interior lumas against THIS film's other interiors "
        "- the outlier test, not the [35,200] band, is the working gate.",
    "performance_vs_sound":
        "Nev's three performance beats each carry their own audio at the "
        "declared level: the climb breathing (-6), the held breath at the "
        "cricket (-6), the grin under dusk insects (-6) - performed emotion "
        "backed by place sound, syncqc refuses an empty foreground lane.",
    "bed_vs_foley":
        "The bed holds the 48-beat grid and DUCKS -6 under every foreground "
        "line; the film's sound arc (jungle -> reverb -> drips -> rustle -> "
        "wing-thunder) must change at the cuts that change place - the "
        "desafarm soundscape measurement re-runs on this cut.",
    "card_vs_card":
        "Five cards, spans 1-2, 5-6, 7-8, 9-10, 15-16 - disjoint by "
        "construction, one figure per card maximum, every figure carrying a "
        "named fetched source; planqc 12's clock check blocks reintroduced "
        "overlaps at y=0.72.",
    "event_vs_window":
        "All three EVENTs (the find, the stir, the exodus) declare continuous "
        "whole-clip action with escalation stated ('density rising', 'motion "
        "spreading') - no 'resolves inside N seconds' anywhere; the mid-action "
        "gate refuses windows ending above 80% of their own peak.",
    "arc_vs_shot_order":
        "Two mini-arcs cannot reverse: E's stars-then-stir (windows 0.30 -> "
        "2.60) and G's ropes-then-column (0.30 -> 2.30, density must RISE). "
        "SHOT_WINDOW pins both; syncqc's arc-order check and the contact-sheet "
        "eye are the second and third belts.",
    "picture_grid_vs_music_grid":
        "ZERO overlap transitions: both flashes and the dip are L139 zero- "
        "reserve fades inside each shot's own frames - the timeline cannot "
        "drift by construction (v6 proved the mechanism at 1536/1536 frames). "
        "verify still measures post-build boundaries against the 48-beat grid.",
    "clip_variety_vs_shot_count":
        "Eight of ten sources carry two shots and every pair is two DECLARED "
        "states (A: find -> closer read; B: walk -> stop; D: arch -> walk-in; "
        "E: still -> stir; F: work -> scatter; G: ropes -> column; H: follow "
        "-> grin; C: morning tilt -> dusk silhouette via late window). The "
        "look-dupe gate refuses same-look pairs >= 0.80 at ingest.",
}

GRADE_SAT    = 1.00                  # source light trusted (his instruction)
GRADE_BRI    = 0.0
TARGET_BLACK = 10.0
TARGET_SAT   = 74.5

# ------------------------------------------------------------- CONTENT (file 31)
CONTENT = {
    "claim":    "Niah National Park (Miri Division, Sarawak) is a UNESCO World "
                "Heritage Site (listed 27 July 2024) reached by a 3km elevated "
                "plankwalk; the Great Cave's west mouth measures ~150m wide by "
                "~75m high; the caves preserve ~40,000 years of human "
                "occupation - the oldest recorded settlement in East Malaysia; "
                "the Great Cave floor hosts guano-feeding cave insects "
                "including a cockroach endemic to the cave; at dusk thousands "
                "of bats stream out while swiftlets stream in; the nearby "
                "Painted Cave holds 1,200-year-old rock art and wooden-coffin "
                "'death ships'.",
    "verified": "Sources fetched 2026-08-12. (1) Wikipedia, Niah National "
                "Park (fetched in full): UNESCO listing '27 July 2024'; west "
                "mouth '150 m wide and 75 m high' citing Barker et al. 2007, "
                "Journal of Human Evolution; 'human remains from 40,000 years "
                "ago... the oldest recorded human settlement in East "
                "Malaysia'; first activity 'ca. 46,000 to 34,000 years ago'; "
                "Great Cave home to three guano-feeding cockroach species, "
                "'Symploce strinatii, endemic to the cave'; Painted Cave "
                "'paintings and wooden coffin death ships', rock art 'dated "
                "as 1,200 years old'. (2) Sarawak Forestry Corporation: '3km "
                "trek along an elevated plank walk'. (3) Tourism Malaysia "
                "blog: the dusk changeover - roundleaf bats spiral out while "
                "swiftlets return to roost. CONFLICT RESOLVED AND RECORDED: "
                "the Sarawak Tourism newsletter claims the mouth is '60 "
                "meters high and 250 meters wide' - REJECTED in favour of the "
                "academically-cited 150x75 (a conflicted number ships on the "
                "academic citation or not at all). DELIBERATELY OFF SCREEN: "
                "'oldest modern human remains in SOUTHEAST ASIA' (tourism "
                "superlative; Wikipedia's defensible claim is East Malaysia "
                "and the film says the humbler true thing by showing, not "
                "superlative-ing), Deep Skull re-dating nuance (37k vs 40k - "
                "the card says PEOPLE SLEPT HERE 40,000 YEARS AGO, which the "
                "'human remains from 40,000 years ago' and '46,000-34,000' "
                "site record both support without resting on the skull "
                "alone), birds'-nest economics, sighting guarantees. HUMAN "
                "STEP AT PUBLISH: platform AI label + the daily-vlog caption "
                "notes the compression (one visit, one cut).",
    "twist":    "THOSE AREN'T STARS. The interior is framed so its ceiling "
                "reads as a night-sky star field - hundreds of still glints - "
                "and at 9.85s the beam sweep turns the star field into a "
                "living ceiling: the glints stir into wings. The scale twist "
                "is STAGED (E's two pinned windows), not stumbled into.",
    "twist_at": 9.8462,
    # THE PROMISE (added 2026-08-12 from the field's retention frameworks): the
    # viewer is told what they will get by ~4s and the film pays it at the exodus.
    "promise":    "the card GUA NIAH. 3KM TO THE DOOR. tells the viewer there is a "
                  "DOOR at the end of a 3km walk - a destination worth the hike, "
                  "named and measured, arriving while he is still on the plankwalk",
    "promise_at": 4.9,
    "payoff_at":  34.5,
    "why_stop": "Card 5 plants the next door: THE NEXT CAVE KEEPS SHIPS FOR "
                "THE DEAD - a true, unexplained image (Painted Cave's "
                "wooden-coffin death ships, verified verbatim) that the film "
                "deliberately does not show. The open loop is the question it "
                "forces - what does a ship for the dead look like? - and the "
                "cut answers only with ribbons of bats and the black massif: "
                "the mountain keeps its second secret for episode 2. Series "
                "thinking: every video ends aimed at the next.",
}

# ------------------------------------------------------------- PLATES
PLATES = {
    "nev": {"job": None, "res": "4k", "ar": "4:5", "cr": 0,
            "status": "EXISTS - the measured 97-image library. Higgsfield media "
                      "ids already uploaded (see plans/panborneo.py PLATES.nev): "
                      "front_neutral efdb9f44 · front_calm 44009a35 · "
                      "front_smile 66e529c7 · profile_right 1bdbaed4 · "
                      "back_head 451cdf9d. Wardrobe refs prompt-text + repo "
                      "files per SOURCE_REFS.",
            "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                              "assets/nev/face/profile_right.jpeg",
                              "assets/nev/face/front_calm.jpeg"],
            "wardrobe_refs": ["assets/nev/wardrobe/04_check_navy/21_front.jpeg",
                              "assets/nev/wardrobe/04_check_navy/23_back.jpeg"],
            "must_show": "actually him - face, hair, EARRING. Wardrobe: NAVY "
                         "CHECK SHIRT open over BLACK TEE, dark trousers, small "
                         "day-pack this film (stated in every human prompt). "
                         "Headlamp worn pushed-up in H only. Sweat is DECLARED "
                         "continuity on the hike shots.",
            "prompt": "(identity from photo references, not regenerated)"},

    "niah_mouth": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
            "status": "TO BUILD at approval - nano_banana_pro 4k, OCR before use "
                      "(glc300 protocol). LOOK at it: the arch must read as a "
                      "RAGGED LIMESTONE ARCH, not a smooth tunnel portal.",
            "must_show": "the Great Cave west mouth from just inside the shadow "
                         "line: a vast ragged limestone arch of daylight, "
                         "stalactite fringe, jungle green beyond, guano floor "
                         "sloping down, swiftlets as flecks. Scale legible: "
                         "the arch dwarfs everything. NO signage, no railings "
                         "with text, no people.",
            "prompt":
            "Photograph from inside the shadow line of an immense limestone "
            "cave mouth in Borneo - the Great Cave of Niah - looking out: a "
            "ragged arch of daylight roughly 150 metres wide and 75 metres "
            "high, fringed with stalactites, dense green rainforest burning "
            "bright beyond the opening, the cave floor a dark sloping bank of "
            "guano, small swiftlets crossing the opening as flecks. Natural "
            "hard contrast between the dark interior and the bright mouth, "
            "interior rock still textured in the shadow. No people, no "
            "boardwalk railings, no signage of any kind. Full-frame DSLR, "
            "24mm, f/8, ISO 400. Real photograph artefacts: true dynamic-range "
            "rolloff at the bright arch, damp rock sheen, no HDR halos. "
            "Negative: CGI, videogame look, smooth tunnel portal, postcard "
            "oversaturation, any signboard or lettering, people, handrails."},

    "niah_interior": {"job": None, "res": "4k", "ar": "16:9", "cr": 4,
            "status": "TO BUILD at approval - nano_banana_pro 4k, OCR + LOOK: "
                      "darkness must be TEXTURED (premortem 2), never a black "
                      "void; the ceiling must carry glint points.",
            "must_show": "deep cave interior lit only by a single torch pool: "
                         "wet limestone, a guano bank, and HIGH ABOVE a "
                         "ceiling holding hundreds of tiny reflective glints "
                         "like a star field. Darkness textured throughout.",
            "prompt":
            "Photograph deep inside a vast dark limestone cave chamber in "
            "Borneo, lit only by a single headlamp pool on wet rock and a "
            "dark guano bank: the beam's pool carries the image, the darkness "
            "around it textured and readable, never pure black - and far "
            "above, a high ceiling holds hundreds of tiny points of "
            "reflected light like a star field hanging in blackness. "
            "Full-frame DSLR, 24mm, f/2.8, ISO 3200, real high-ISO grain. "
            "Real photograph artefacts: beam falloff, damp rock sheen, "
            "floating dust motes in the beam, no HDR halos. Negative: CGI, "
            "videogame look, pure black voids, artificial floodlight, "
            "postcard grade, any lettering, people."},
}

PROBE_FIRST  = "G"     # the exodus: the climax, the emotion event, and the
                       # generator's weakest class (many small objects). If G
                       # fails, the film does not exist - probe it alone
                       # (mouth plate 4cr + 22.5cr), LOOK, judge, then batch.

CLIPS = {}             # filled at generation

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
            "probe": 4 + per, "after_probe": gen - per + 4}
