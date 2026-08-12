"""NEV · SABAH TO SARAWAK, ONE ROAD — Defender 110 SE crosses Borneo · travel vlog
His title 2026-08-11: "car review and a vlog... nev drives the car from Sabah to
Sarawak, showing all the beautiful scenery and activities in between."

HIS PICKS (readback 2026-08-11, all four answered):
  car     = LAND ROVER DEFENDER 110 SE (asked twice - the title said "Toyota Land
            Cruiser Defender SE", which mixes two vehicles; he picked the Defender)
  route   = FULL KK -> Kuching (the border-hop motif is the hook)
  chapters= the recommended five: KK dawn -> Klias wetlands -> Sindumin border ->
            Tusan Beach, Miri -> Kuching waterfront
  length  = "go with your recommendation" -> 28.97s, top of the measured 16-29s band.
            The 45s version is the FOLLOW-UP once one real retention curve exists.

FORMAT RESOLUTION - stated as a choice (hard rule 10): "car review AND a vlog" is cut
as MUSIC-LED travel_vlog grammar with the Defender as the through-line. A spoken
review would force sentence-cut grammar and the two never mix (doctrine). The review
lives in the Defender's MOMENTS (the water crossing, the cabin, the tailgate, the
cliff park) and on verified CARDS, not in VO.

REFERENCE SCAN (web, 2026-08-11): the field's road-trip shorts are drone-and-music
tours - rolling shots, map overlays, stop-count structure. THE UPGRADE: ours opens on
the film's one irreversible state change - the border barrier LIFTING - as a cold
open, then tells the day that earned it. A crossing, not a tour.

VERIFIED FACTS (fetched 2026-08-11, sources in CONTENT below):
  Pan-Borneo Highway is TOLL-FREE, AH150, Malaysian section 2,083 km · Sabah/Sarawak
  land border at Sindumin-Merapok · the full route transits Brunei (168 km Bruneian
  section) · Klias wetlands ~112 km / ~2 h drive from KK, proboscis monkeys along the
  river (sightings NOT guaranteed - amazingborneo.com says so outright) · Tusan Beach
  ~40 min from Miri.

STATUS 2026-08-11 (Phase 2, session 9): PLATES BUILT - 16cr MEASURED
(4,294.82 -> 4,278.82), all four 5504x3072, RapidOCR at 2048px: ZERO text on all
four including the Defender body. Face refs uploaded to Higgsfield (media ids in
PLATES.nev). VIDEO GENERATION BLOCKED by an account-wide moderation misfire:
7/7 seedance jobs returned status=nsfw and were REFUNDED - including a
no-reference bland-prompt control, the 2_5 model, and a silent (no-audio)
control. Not our prompts, not our plate (craft L117). Job IDs for the support
report: bc29937b, c8c5c208, 50f73f04, bc66ad08, 7f3ddb05 (2_5: f39fe81a),
659b0793 (silent). RETRY RAN 2026-08-12 01:33: the filter had recovered. G completed and passed QC; all 12 remaining sources batched with ZERO failures. THE FOOTAGE EXISTS. See CLIPS below.

DIAGNOSIS COMPLETE (same day, his ask): the culprit is SEEDANCE'S PROVIDER-SIDE
safety classifier, not our prompt, not the plate, not the account. Proof: a
no-reference bland control flagged; his own unrelated web-UI prompt flagged; and
kling3_0 with the SAME defender plate COMPLETED CLEAN (job d0cb2935, 5.04s, AAC,
luma 101.8 - MEASURED charge 8.75cr against a 10cr preflight, balance
4,278.82 -> 4,270.07). Higgsfield docs: providers run independent safety
systems, false positives acknowledged, no manual override, credits auto-refund.
HIS PICK (asked twice, 2026-08-11 evening): WAIT for Seedance. Auto-retry
armed +3h/+6h. LIKELY CAUSE of the misfire, his own theory and the timeline
supports it: Seedance 2.5 LAUNCHED AUG 7 (the day mahua ran 9/9 clean on 2.0)
with an 'unlimited Aug 7-14' promo running NOW - a shared new safety stack
and/or a promo-abuse clampdown would flag both versions exactly as observed.
Implication: may not clear until ~Aug 14.

THE FALLBACK LADDER, researched and PREFLIGHTED (models_explore + get_cost),
so the next session spends zero time rediscovering it. All three keep or
adapt the existing plan; Seedance retries stay armed on top:
  1 gemini_omni  15.0cr/5s -> 13 clips = 195cr  image_references LIKE
    SEEDANCE (zero plan rework) + native audio + 720p + 9:16. Google's
    filter, not ByteDance's. THE RECOMMENDED PIVOT if Seedance stays down.
  2 flux_3_video 27.5cr/5s -> 357.5cr  same reference design, Black Forest
    Labs provider. Backup if Gemini's look disappoints.
  3 kling3_0     8.75cr/5s MEASURED -> ~166cr with nano keyframes, but
    start/end images ONLY (no multi-references) and it FOLLOWS THE START
    IMAGE'S ASPECT (test d0cb2935 came out 1284x716 from a 16:9 plate) -
    needs a 9:16 keyframe stage + re-gate. Cheapest, most rework.
"""

PROJECT   = "NEV · SABAH TO SARAWAK, ONE ROAD · Defender 110 SE · travel vlog"
PILLAR    = "travel_vlog"
GEN_MODE  = "coverage"               # declared so deliberate reads as deliberate
BPM       = 99.4                     # PROVISIONAL: grid written at Easy-Love's tempo
                                     # class; the BED for this film is picked from
                                     # BGM/travel_vlog ON HIS BOX at its measured
                                     # native tempo, zero stretch. If the picked bed
                                     # is not ~99.4, recompute BEAT/TARGET_S from the
                                     # same 48-beat arithmetic BEFORE assembly - the
                                     # grid is derived, never typed (tv L1).
BEAT      = 60.0 / BPM               # 0.603622s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 28.97                    # 48 beats = 28.9739s. Band-top of measured 16-29s.

LESSONS_ACK = {            # ledger counts this plan was written against (planqc 23)
    "general craft": 118,  # incl. L116 (scene-blind refs - THIS plan's SOURCE_REFS
    "travel vlog":    6,   # exists because of it) and the whole desafarm-v2 set
                           # L101-L115. tv L5 (whip stole the timeline) bites here:
                           # this plan declares the same 240ms whip.
    # NEIGHBOURING PILLARS (planqc 23b): transferable prior art read 2026-08-11 -
    # i8 L9-L12 (3-second retention > watch time, hooks UNDER 2s complete 23%
    # better, one EVENT not a tour - the hook here is a 1.21s barrier-lift event),
    # lc300 L5 (fx.whip's seam bug history - live, we declare a whip), lc300 L7
    # (image_references PLURAL - every Defender+Nev shot carries both). Car
    # identity lessons (i8 doors, S450 grille) do not transfer.
    "bmw i8 car cinematic": 16,
    "car cinematic": 15,
    "toyota land cruiser 300 zx car review": 8,
}

PREMORTEM = [
    ("AN INVENTED SIGN BOARD SHIPS AT THE BORDER (the mahua defect exactly: shot 7 "
     "grew a sign on a post although 'no signage' sat in prompt AND negative block - "
     "a negative block is not sufficient protection). A BORDER is the highest "
     "signage-pressure location in this whole channel: gantries, state crests, "
     "welcome boards, painted road text",
     "Source G frames the BARRIER ARM AND THE ROAD ONLY - composition states 'the "
     "frame contains no signboard, no gantry lettering, no painted road text; the "
     "barrier arm and the tarmac carry the image'. clipqc text-zoom runs on BOTH G "
     "windows at ingest, and the contact sheet (tools/contact.py --raw) is READ for "
     "invented text before assembly. If text appears, G is one 22.5cr regeneration, "
     "never a delivered defect."),

    ("'RESOLVES INSIDE N SECONDS' WRITES THE OTHER FOUR SECONDS (craft #99, from "
     "desafarm's own probe: told a five-second generator the action lasted one, and "
     "it invented a calm drink for the rest). The barrier lift and the water splash "
     "are both sub-second events inside 5s clips",
     "Both EVENT prompts declare what fills the WHOLE clip: G is 'barrier rises, "
     "vehicle rolls under, vehicle recedes - continuous forward motion first frame "
     "to last'; A is 'approach, splash, pull-out, water streaming off - continuous. "
     "'Resolves inside N seconds' appears in NO prompt (banned when N < CLIP_S)."),

    ("THE DARK CABIN COMES BACK (craft #101: 'fully exposed' is not an instruction "
     "until you say expose for WHAT - the desafarm cabin metered the windscreen and "
     "delivered a 37.7-luma silhouette at 59.7% crushed black)",
     "Source C carries the metering target as its loudest line: EXPOSE FOR THE "
     "CABIN, NOT FOR THE WINDSCREEN - the glass may blow out and that is correct. "
     "And every clip's mean luma is compared against the other clips of THIS film "
     "at ingest, never only against the [35,200] band - the outlier test is what "
     "actually caught it last time."),

    ("THE WHIP STEALS 240ms FROM THE TIMELINE (travel vlog L5, measured on desafarm "
     "v2: 197ms gone from shot 8, 60% of the film ~170ms early against a bed that "
     "kept its tempo). This plan declares the same 240ms whip at boundary 4",
     "ONE MECHANISM since 2026-08-11: engine.py reserves and renders the blend-in "
     "shot one blend-width longer (the blend eats the OVERLAP, never the timeline) "
     "and planqc 34 reads engine.BLEND_RESERVES_OVERLAP itself. verify's beat-grid "
     "check runs on post-blend boundaries, so a regression fails the cut, not just "
     "the plan."),

    ("WILDLIFE THAT WAS NEVER GUARANTEED GETS PROMISED (J4 class: the operator "
     "itself states 'does not guarantee wildlife sightings' and 'sometimes the "
     "wildlife may be on distant trees'). A proboscis leap is the chapter-2 money "
     "shot and a generated monkey cannot be a factual claim about Klias",
     "The card says PROBOSCIS COUNTRY - a description of what Klias is known for "
     "(operator-verified), never 'you will see them'. The film shows the monkey "
     "because film grammar wants the payoff; the CLAIM on screen stays inside what "
     "amazingborneo.com states. Sighting odds are deliberately OFF screen."),

    ("THE SAME THREE FACES ON EVERY SHOT (craft L116, HIS catch on the desafarm "
     "board 2026-08-11: identity refs were scene-blind - an OTS shot got three "
     "front faces and no back of head)",
     "SOURCE_REFS below picks per scene from the 97-image library: the OTS cabin "
     "gets back_head + the navy check's BACK; the cliff walk-away gets back refs; "
     "the closing grin gets both front expressions. planqc 27b blocks the blanket."),
]

_LOOK = (
    "Equatorial Borneo daylight, true texture on skin, fabric, leaf and paint. REAL "
    "FOOTAGE, NOT A RENDER: handheld micro-shake, natural depth of field, accurate "
    "reflections, no HDR halos. Negative: CGI, videogame look, postcard "
    "oversaturation, invented signage text, signboards, gantry lettering, painted "
    "road text, legible device screens, visible registration or number plates, model "
    "badges or lettering of any kind on any vehicle, any legible slogan wordmark "
    "logo or printed graphic on clothing, any legible instrument-cluster or "
    "infotainment display, extra fingers, warped faces, drone-stock look."
)

# ---------------------------------------------------------------- SOURCES (12 x 22.5cr)
SOURCES = {
 "G": ("EVENT · THE BARRIER LIFTS", "#B0413E", "EVENT", ["defender"],
       "Vertical 9:16. THE EVENT. MIDDAY, hard equatorial light. Camera low beside a plain red-and-white "
       "striped border barrier arm across a two-lane tarmac road, jungle green behind. "
       "AT FRAME ZERO THE ARM IS ALREADY RISING - never at rest. It swings up in the "
       "first second and the deep green Defender 110 from the reference image rolls "
       "under it and past the lens, then recedes up the road - continuous forward "
       "motion first frame to last, never settling. THE FRAME CONTAINS NO SIGNBOARD, "
       "NO GANTRY LETTERING, NO PAINTED ROAD TEXT: the barrier arm and the tarmac "
       "carry the image - and the arm itself is PLAIN striped metal, no lettering on its surface. Real tarmac texture, heat shimmer allowed. AUDIO: the mechanical rise and CLANK of the barrier arm - the hero sound of the film - then the diesel rolling under and away; no music, no voice. " + _LOOK),

 "B": ("KK rolls out at dawn", "#4A6FA5", "PLACE", ["defender"],
       "Vertical 9:16. DAWN, first light, sky grading orange to blue. Camera low at "
       "kerb height on an empty coastal boulevard in Kota Kinabalu, the sea flat and "
       "pale beyond: the deep green Defender 110 from the reference image SWEEPS PAST "
       "CLOSE - headlamps on, its boxy flank filling the frame for an instant, round "
       "lamps in square surrounds - then recedes fast down the tarmac, tail lamps "
       "going away small and bright. One continuous pass, energy front-loaded, never "
       "settling. THE FRAME CONTAINS NO SHOP SIGNS, NO ROAD-NAME BOARDS, NO PAINTED "
       "ROAD TEXT - kerb, tarmac, sea and sky carry the image. AUDIO: the diesel "
       "swelling in and whipping past, dawn birds behind it - no music, no voice. "
       + _LOOK),

 "C": ("cabin, window down, dawn", "#7A8B5C", "HUMAN", ["nev", "defender"],
       "Vertical 9:16. DAWN turning to MORNING - one continuous light move, which is "
       "why this single clip serves both of its shots. EXPOSE FOR THE CABIN, NOT FOR "
       "THE WINDSCREEN - the glass may blow out and that is correct; the driver, his "
       "hands and the upright dashboard are fully lit and readable at all times, "
       "never a silhouette, never a dim interior. Interior of the Defender 110 from "
       "the second reference image, over-the-shoulder onto the windscreen: the man "
       "from the first reference images (navy check shirt over a black tee, hair "
       "dry, no cap, no sunglasses) drives with the window down, morning air moving "
       "his hair, the upright Defender bonnet visible ahead, the road feeding under "
       "it. No legible instrument display, and the steering-wheel hub is PLAIN - no "
       "badge, no emblem. Face partial, back of head and right side "
       "to the lens. AUDIO: steady diesel, wind rushing the open window, tyres on "
       "tarmac - no music, no voice. " + _LOOK),

 "A": ("EVENT · THE WATER CROSSING", "#2E6F8E", "EVENT", ["defender"],
       "Vertical 9:16. MORNING. THIS CLIP IS ONE CONTINUOUS ACTION FIRST FRAME TO "
       "LAST. Camera low at water level beside a shallow flooded stretch of kampung "
       "road. AT FRAME ZERO THE SPLASH IS ALREADY BEGINNING: the deep green Defender "
       "110 from the reference image is entering the water, bow wave rising, and in "
       "the first half second the spray bursts white over the bonnet and past the "
       "lens; it pulls through and out, water streaming off the squared wheel "
       "arches, wake settling behind. Approach, splash, pull-out - continuous, the "
       "clip never settles. A vehicle event, not a camera move. THE FRAME "
       "CONTAINS NO HOUSE BOARDS, NO HAZARD SIGNS, NO PAINTED TEXT - water, "
       "road and vehicle carry the image. AUDIO: the bow wave BURSTING over the "
       "bonnet, water hammering the arches, the engine pulling through - no "
       "music, no voice. " + _LOOK),

 "D": ("Klias jetty - he boards", "#C88A3D", "HUMAN", ["klias", "nev"],
       "Vertical 9:16. MORNING, soft bright overcast. Waist-height camera on a "
       "plain wooden jetty over the brown Klias river of the first reference image, "
       "mangrove walls green on both banks. The man from the second reference "
       "images (navy check shirt over a black tee, hair dry; face, hair and EARRING "
       "match the references exactly) steps down into a plain open longboat, "
       "steadies himself on the gunwale and sits, the boat dipping under his "
       "weight, water ringing out - and as he settles he LOOKS UP at movement in "
       "the mangrove canopy across the water. Continuous movement first frame to "
       "last, facing the lens as he boards. No signage on the jetty. AUDIO: boots "
       "on wet planks, the hull taking his weight, jungle and water close - no "
       "music, no voice. " + _LOOK),

 "F": ("the river bend, boat POV", "#5B8A72", "PLACE", ["klias"],
       "Vertical 9:16. LATE MORNING. Low POV from the bow of a moving longboat on "
       "the brown Klias river of the reference image: the bow line cutting the "
       "frame low, the river bending ahead, mangrove walls sliding past both sides, "
       "small wake chevrons running off the bow. THE HULL AND BOW ARE PLAIN "
       "UNPAINTED TIMBER - no registration numbers, no painted name, no "
       "lettering on any surface. Continuous forward glide first frame to "
       "last, engine-speed steady, no people in frame. AUDIO: the "
       "outboard drone, water running on the hull, jungle wide behind - no "
       "music, no voice. " + _LOOK),

 "E": ("proboscis in the canopy", "#8C6239", "WILDLIFE", ["klias"],
       "Vertical 9:16. LATE MORNING, bright overcast. Long lens up into the "
       "mangrove canopy beside the Klias river of the reference image: a male "
       "proboscis monkey - pot belly, long pale nose, rust-orange back, grey limbs "
       "- moves along a branch, pauses, then LEAPS to the next tree in one heavy "
       "committed arc, branches whipping on the landing, leaves falling. The leap "
       "completes INSIDE the clip with the landing held - continuous animal "
       "movement first frame to last. Real fur texture, real branch physics. AUDIO: "
       "close jungle - insects, the branch CREAKING under its weight, then the "
       "whip and crash of leaves as it lands; no music, no voice. " + _LOOK),

 "I": ("the Pan Borneo, rolling", "#6A4F8C", "PLACE", ["defender"],
       "Vertical 9:16. AFTERNOON, high sun gone slightly warm. ONE CONTINUOUS "
       "CAMERA MOVE WITH TWO DECLARED LOOKS: the first half runs CLOSE ALONGSIDE "
       "the deep green Defender 110 from the reference image - its boxy flank "
       "filling the frame, centreline feeding past - and in the second half the "
       "camera FALLS BEHIND AND RISES, the vehicle pulling ahead until the "
       "two-lane straight reads as a long ribbon into the low green hills of the "
       "valley. Continuous highway speed first frame to last. No gantries, no "
       "signboards, no painted road text. AUDIO: close tyre roar and diesel in "
       "the first half, falling away to wind and distant hum as the camera "
       "drops back - no music, no voice. " + _LOOK),

 "H": ("EVENT · the pour at the turnout", "#A9553E", "EVENT", ["nev", "defender"],
       "Vertical 9:16. AFTERNOON. Medium shot from the road edge: the Defender 110 "
       "from the second reference image parked on a gravel turnout, its "
       "side-hinged tailgate open, external spare wheel on the door; the man from "
       "the first reference images (navy check shirt over a black tee; face, hair "
       "and EARRING match the references exactly) stands at the open tailgate, "
       "uncaps a plain UNLABELLED bottle - no label, no lettering on it - and "
       "TIPS IT OVER HIS OWN HEAD against the heat, water sheeting off his hair "
       "and shoulders as he shakes it away laughing, a green valley falling away "
       "behind him in afternoon haze. One continuous action first frame to last: "
       "uncap, pour, shake, grin. Facing the lens. HIS HAIR IS WET ONLY IN THIS "
       "CLIP - by the golden-hour shots, hours later, he is dry again. AUDIO: "
       "water splattering on gravel, his gasp and laugh, ticking engine, valley "
       "birds - no music, no voice. " + _LOOK),

 "J": ("Tusan clifftop, golden", "#C2703D", "HUMAN", ["tusan", "nev", "defender"],
       "Vertical 9:16. GOLDEN hour. Camera behind and low: the deep green Defender "
       "110 from the third reference image stands parked at the grassy cliff edge "
       "of Tusan Beach from the first reference image, and the man from the second "
       "reference images (navy check shirt over a black tee) walks AWAY from the "
       "lens toward the cliff edge, back to camera the whole clip, stopping at the "
       "rim with the low gold sun flaring past him, the long sand and surf line "
       "far below. Continuous walk first frame to last, no turn to camera. "
       "AUDIO: cliff-top wind, grass moving, the surf faint and far below - no "
       "music, no voice. " + _LOOK),

 "K": ("the cliff face and the surf", "#B8860B", "PLACE", ["tusan"],
       "Vertical 9:16. GOLDEN hour, sun low over the South China Sea. From the "
       "sand at Tusan Beach of the reference image: the tall sandstone cliff face "
       "glowing orange, long shallow waves sliding in flat gold sheets across the "
       "sand toward the lens in the FIRST HALF; in the SECOND HALF one LARGER "
       "SET ARRIVES and breaks against the cliff base, spray flung up backlit. "
       "Continuous wave movement first frame to last, no people. AUDIO: the surf "
       "ARRIVING - the slide, the break, the spray hiss - the coast made audible; "
       "no music, no voice. " + _LOOK),

 "L": ("Kuching waterfront, arrival", "#4F7CAC", "HUMAN", ["kuching", "nev", "defender"],
       "Vertical 9:16. DUSK, blue hour just beginning, the sky still holding warm "
       "light low in the west. The Kuching riverfront promenade of the second "
       "reference image, lamps coming on, the river dark and calm. The man from "
       "the first reference images (navy check shirt over a black tee; face, hair "
       "and EARRING match the references exactly) leans back against the parked "
       "deep green Defender 110 of the third reference image, arms loosely "
       "crossed, then breaks into a slow grin and tips his head back, done, the "
       "day's distance behind him. Warm lamp light on his face, city glow behind. "
       "Continuous, facing the lens. No legible signage anywhere. AUDIO: evening "
       "promenade - water lapping the wall, far voices, lamp buzz, the ticking "
       "cooling engine beside him; no music, no voice. " + _LOOK),

 "M": ("PAYOFF · the lamps hand over", "#37474F", "PAYOFF", ["defender", "kuching"],
       "Vertical 9:16. DUSK, deeper than the arrival - blue hour proper. From the "
       "Kuching promenade of the second reference image, its warm lamps lit: the "
       "deep green Defender 110 from the first reference image pulls away along "
       "the riverfront road, its small squared tail lamps bright red in the blue, "
       "receding under the run of promenade lamps until the road curves it out of "
       "sight. Continuous departure first frame to last, camera static, axis along "
       "the road. No legible signage anywhere. AUDIO: the diesel pulling away and "
       "fading under the promenade quiet, the river lapping after it - the engine "
       "leaves last; no music, no voice. " + _LOOK),
}

# FRAMING (planqc 28) - every camera position stated; a plate anchors PLACE only.
FRAMING = {
    "G": "low beside the barrier arm, road receding past it, vehicle through and away",
    "B": "long lens along the dawn boulevard, vehicle receding in its own lane",
    "C": "interior over-the-shoulder onto the windscreen, no exterior position",
    "A": "low at water level beside the flooded stretch, vehicle crossing left to right",
    "D": "waist height on the jetty, subject stepping down toward the lens",
    "F": "bow POV, river bending ahead, banks sliding past both sides",
    "E": "long lens up into the canopy, branch line crossing the upper third",
    "I": "close alongside (first half) then risen far behind (second half) - two looks, one move",
    "H": "static medium from the road edge, tailgate and valley in one frame",
    "J": "behind and low, subject walking away to the cliff rim, sun past him",
    "K": "from the sand, cliff face right, waves sliding in toward the lens",
    "L": "static medium on the promenade, subject against the parked vehicle",
    "M": "static on the promenade, vehicle receding away under the lamp run",
}

# ---------------------------------------------------------------- SCENE REFS
# Craft L116 (his correction, 2026-08-11): refs chosen PER SCENE from assets/nev/
# (97 measured images, index.json). Wardrobe THIS film: 04_check_navy - navy check
# over a black tee, the darkest full outfit in the set (README finding 4), right for
# a road film that ends at dusk. Declared here AND repeated inside every human
# prompt - a spec that lives in one place is never read (the mahua wardrobe bug).
SOURCE_REFS = {
    # C: OTS onto the windscreen -> back of head + right side + the shirt's BACK.
    "C": ["assets/nev/face/back_head.jpeg",
          "assets/nev/face/profile_right.jpeg",
          "assets/nev/wardrobe/04_check_navy/23_back.jpeg"],
    # D: steps down toward the lens -> both fronts + shirt front on a full body.
    "D": ["assets/nev/face/front_neutral.jpeg",
          "assets/nev/face/front_calm.jpeg",
          "assets/nev/wardrobe/04_check_navy/21_front.jpeg"],
    # H: medium, facing lens, the pour + shake + grin -> neutral front + shirt front.
    "H": ["assets/nev/face/front_neutral.jpeg",
          "assets/nev/wardrobe/04_check_navy/21_front.jpeg"],
    # J: walks AWAY, back to camera the whole clip -> back of head + shirt BACK.
    "J": ["assets/nev/face/back_head.jpeg",
          "assets/nev/wardrobe/04_check_navy/26_back.jpeg"],
    # L: the closing grin, facing lens under lamp light -> both front expressions
    # (the arc ends warm) + shirt front.
    "L": ["assets/nev/face/front_smile.jpeg",
          "assets/nev/face/front_calm.jpeg",
          "assets/nev/wardrobe/04_check_navy/24_front.jpeg"],
}

# J is back-to-camera BY COMPOSITION - the gaze at the drop is the shot.
FACE_OPTOUT = {"J": "back to camera at the cliff rim for the whole clip - the "
                    "composition is the gaze at the drop, not the face; identity "
                    "is carried by wardrobe back + build, refs above"}

# ---------------------------------------------------------------- SHOTS (20 = 48 beats)
# chapters: [0] cold open border | [1-4] KK dawn | [5-9] Klias | [10-13] border+highway
# | [14-16] Tusan golden | [17-19] Kuching dusk
SHOTS = [
 ("G", 1.00, "burst", "COLD OPEN - the barrier already rising off the tarmac, the Defender rolls under"),
 ("B", 1.00, "burst", "rewind to dawn: the SWEEP past on the KK boulevard - flank fills the frame, tail lamps away down the tarmac as the exit"),
 ("C", 1.00, "burst", "cabin, window down, dawn light filling the windscreen over the bonnet"),
 ("A", 1.00, "med",   "the water crossing - spray bursts over the bonnet"),
 ("C", 1.20, "burst", "back in the cabin, full morning now on the glass - the Klias turnoff coming"),
 ("D", 1.00, "burst", "Klias jetty - he steps down into the boat off the mangrove bank"),
 ("E", 1.00, "burst", "the proboscis on the branch above the river, nose unmistakable"),
 ("F", 1.25, "burst", "bow POV, the brown Klias river bending ahead"),
 ("E", 1.20, "med",   "the LEAP - one committed arc over the river, branches whipping"),
 ("F", 1.00, "burst", "the river opening out, the jetty run done - the border ahead"),
 ("G", 1.20, "burst", "the border again - through the barrier and away up the far lane"),
 ("I", 1.00, "burst", "the Pan Borneo straight, centreline feeding past - until the turnout"),
 ("H", 1.00, "burst", "the pour - the bottle over his head at the turnout, the valley in haze"),
 ("I", 1.25, "med",   "long lens: the road a ribbon threading the valley, running for the coast cliffs"),
 ("J", 1.00, "burst", "Tusan - the Defender parked at the cliff edge above the sand"),
 ("K", 1.00, "burst", "the cliff face orange, waves in gold sheets on the sand"),
 ("J", 1.20, "burst", "he walks out to the rim, back to us, sun flaring past him"),
 ("K", 1.25, "burst", "the break ARRIVES - the wave concussion flung backlit below the rim, the gold going"),
 ("L", 1.00, "med",   "Kuching lamps on - the lean, the slow grin, the last gold gone to lamplight"),
 ("M", 1.00, "burst", "the tail lamps answer the promenade lamps and the Defender pulls away"),
]

BEATS = {"burst": 2, "med": 4}       # at 99.4: burst 1.2072s, med 2.4145s
                                     # 16 bursts + 4 meds = 48 beats = 28.9739s

# planqc 30: every shot names its light state; boundary 0 is the ONE declared jump.
SHOT_TIME = ["midday",                                 # 0  the cold open
             "dawn", "dawn", "morning", "morning",     # 1-4   KK out
             "morning", "morning", "morning",          # 5-7   Klias
             "morning", "morning",                     # 8-9   Klias
             "midday",                                 # 10 the border, forward this time
             "afternoon", "afternoon", "afternoon",    # 11-13 the Pan Borneo
             "golden", "golden", "golden", "golden",   # 14-17 Tusan
             "dusk", "dusk"]                           # 18-19 Kuching

# THE ONE DECLARED BACKWARDS BOUNDARY (planqc 30 reads this; mahua precedent).
TIME_JUMPS = {
    0: "COLD OPEN. Shot 0 is midday - the barrier lifting, the film's one "
       "irreversible change, Sabah becoming Sarawak - and shot 1 rewinds to dawn in "
       "KK. The field opens road-trip films on a rolling shot; we spend the crossing "
       "at frame zero and then tell the road that earned it. Every boundary from 1 "
       "onward is strictly monotonic: dawn -> morning -> midday -> afternoon -> "
       "golden -> dusk.",
}

LINKAGE = [
    ("subject",     "tarmac",   "the tarmac under the lifting barrier -> the same tarmac rewound to dawn in KK"),
    ("light",       "dawn",     "the dawn boulevard outside -> the same dawn filling the windscreen"),
    ("object",      "bonnet",   "the bonnet the dawn light lands on -> the bonnet the spray bursts over"),
    ("light",       "morning",  "the crossing throws morning light around -> the same morning filling the cabin"),
    # boundary 4 - the whip: the one mode-of-travel change, wheel to hull
    ("consequence", "klias",    "the road reaches the Klias turnoff, SO the wheel stops and the boat takes over"),
    ("place",       "mangrove", "the mangrove bank at the jetty -> the mangrove canopy over the water"),
    ("subject",     "river",    "the branch hanging over the river -> the river itself, bending ahead"),
    ("place",       "klias",    "the Klias bend the bow is cutting -> the Klias air the leap crosses"),
    ("subject",     "river",    "the leap over the river -> the river opening out under the bow"),
    # boundary 9 - the cruise ends, back to the wheel
    ("consequence", "border",   "the jetty run is done, SO back to the road - and the border, forward this time"),
    ("motion",      "lane",     "through the barrier into the far lane -> holding the lane at highway speed"),
    ("motion",      "turnout",  "the straight runs until the turnout -> the turnout stop itself"),
    ("gaze",        "valley",   "the valley behind the pour -> the ribbon of road threading it"),
    # boundary 13 - the coast earns the detour
    ("consequence", "cliff",    "the road runs for the coast cliffs, SO Tusan - the day's last-light stop"),
    ("place",       "cliff",    "the Defender at the cliff edge -> the cliff face itself, glowing"),
    ("gaze",        "sand",     "the sand far below the parked car -> him walking out to look down at it"),
    ("subject",     "rim",      "stopped at the rim, sun past him -> the spray breaking below the same rim"),
    # boundary 17 - the light decides the last leg
    ("consequence", "gold",     "the gold is off the water, SO the last leg runs - and ends under lamplight"),
    ("subject",     "lamps",    "the lamps he leans under -> the tail lamps answering them as he pulls away"),
]

BLEND_AFTER  = [4]                   # the one mode-of-travel change: wheel -> hull
BLEND_KIND   = "whip"
BLEND_WIDTH  = 0.24                  # floor of the 240-560ms band

SFX_LEAD     = 0.0                   # INERT here: hero sits at t=0 (no timeline
                                     # before frame zero) and IMPACT/SUBDROP are
                                     # empty. Declared, not forgotten (sound QC 4).
IMPACT_AT    = []                    # hero_only: no whoosh/impact layer on a vlog
SUBDROP_AT   = []

SOUND = {
    "bed":       "PICK ON HIS BOX from BGM/travel_vlog at native tempo, zero "
                 "stretch - NOT Easy-Love (mahua's bed) and NOT Crystal-Water "
                 "(kundasang's). The 99.4 grid above is the tempo CLASS; recompute "
                 "BEAT/TARGET_S from 48 beats at the picked bed's measured BPM.",
    "hero":      "the barrier arm's mechanical rise-and-clank on shot 0 - the "
                 "border made audible. After that the film's places carry it: "
                 "engine, water, jungle, surf, evening promenade.",
    "hero_shot": 0,
    "duck_shots": [0, 3, 6, 8, 12, 15, 17, 19],  # EVERY foreground line (>= -6) ducks the bed
                                      # (sound QC 3: a hero against an un-ducked
                                      # bed is the WRX mix bug shape)
    "silence":   "the quiet point is shot 13 (-11, the lowest line in the FOLEY "
                 "map - the camera risen far behind, the road a ribbon; shot 1 was "
                 "rescored -7 when its pin chose the sweep, r3). Doctrine's 'near-silence before "
                 "the twist' is IMPOSSIBLE here because the twist sits at frame 0 "
                 "(cold open) - waived as a stated choice, hard rule 10. The road "
                 "hum is continuous except the Klias chapter, shots 5-9, where the "
                 "DIESEL hands over to outboard, water and jungle - engine-band "
                 "sound persists on 7 and 9 by design (the boat has a motor).",
}

FOLEY = {   # every shot lays its own clip audio (generate_audio=true), mostly under
            # the bed; foreground (>= -6) where the moment IS the sound (planqc 19)
     0:  -3.0,   # G  EVENT - barrier clank + the Defender rolling under. HEARD.
     1:  -7.0,   # B  the diesel swells in and whips PAST (the pinned sweep), dawn
                 #    birds after - energy at the decision second, never a dropout
                 #    (was -11 scoring the recede: three documents, two shots - r3)
     2:  -9.0,   # C  cabin: engine, wind through the open window
     3:  -3.0,   # A  EVENT - the splash. The Defender review moment. HEARD.
     4:  -9.0,   # C  cabin again - the same cabin, later in the clip's one
                 #    declared change (dawn -> morning). Nothing new is promised.
     5:  -8.0,   # D  boots on the jetty, the boat taking his weight
     6:  -6.0,   # E  jungle close: insects, the branch creaking. Forward.
     7:  -7.0,   # F  outboard drone, water on the hull
     8:  -5.0,   # E  the LEAP - branches whip and crash. The chapter's hero.
     9:  -8.0,   # F  wake and engine fading as the river opens
    10:  -8.0,   # G  engine-through ONLY: the clank lives at 0-1.0s of the clip,
                 #    inside shot 0's pinned window - shot 10's late window (3.30s)
                 #    physically cannot contain it (sound QC finding 2). The border
                 #    lands here on the CARD, not on a sound the window does not have.
    11:  -9.0,   # I  highway hum, tyre roar on coarse tarmac
    12:  -6.0,   # H  EVENT - the pour: water on gravel, the gasp-laugh. HEARD.
    13: -11.0,   # I  the ribbon - road noise pulled far back under the bed
    14:  -9.0,   # J  wind at the cliff edge, grass - only what J's AUDIO line asks for
    15:  -6.0,   # K  the surf on the sand - the coast made audible. Forward.
    16:  -9.0,   # J  wind and waves below as he walks out
    17:  -6.0,   # K  the break-line, spray. Forward.
    18:  -9.0,   # L  evening promenade under the med - lapping water, far voices
    19:  -6.0,   # M  PAYOFF - the departure. The engine leaves last. HEARD.
}

# ---------------------------------------------------------------- MIX (file 19)
# Sound QC r2 finding 8: FOLEY gives per-clip offsets and SOUND gives a duck
# list, but nothing bound assembly to the measured reference profile - which is
# exactly how a mix once shipped mono at -20dB with the right sounds in it.
MIX = {
    "lufs_i_target":  -8.0,      # file 19: deliver inside -7..-9 LUFS integrated
    "band_body_pct":   45,       # measured reference band balance
    "band_air_pct":     4,
    "stereo":         "wide bed, foley centred - never mono",
    "hero_layers":    "the shot-0 clank = G's native clip audio PLUS bank "
                      "sweeteners (bank.pick role=hit, cut_safe) layered "
                      "transient/body/tail in post - the measured bank is the "
                      "stated source, not an unnamed library",
    "duck_depth_db":  -6,        # bed drops 6dB under every duck_shots entry
    "duck_shape":     "sidechain, 50ms attack / 250ms release - no stepping",
    "loudnorm":       "TWO-PASS, never single (undershot twice); alimiter "
                      "level=disabled",
    "source":         "19-sound-engineer.md measured reference profile",
}

CROP_XY   = {}          # populated only from a probe
BAN_SPANS = {}          # filled AT INGEST from measured clips, never guessed
DELOGO    = {}          # border + city shots carry the signage ban in the PROMPT;
                        # boxes come from measured clips at clipqc, never invented
CALLBACKS = []

# ORDER IS STORY in five sources, so all five are pinned (panel r2: G got a pin,
# every same-dependency source deserves the same discipline). Pins allocate
# first; a pin that does not fit fails LOUDLY (engine, 2026-08-11). ALL values
# are conservative head/tail picks - REFINE AT INGEST from the motion curve.
# INGEST CHECKS owed with them: G's 3.30s window must still CONTAIN the barrier
# arm in frame (else the rewind structure never visibly closes - re-pin); H's
# window must contain the pour-to-shake transition, not the uncap.
SHOT_WINDOW = {
    0: 0.30, 10: 3.30,    # G: arm rising | through-and-away
    3: 0.00,              # A: the burst lives in the first half second - a late
                          #    window would pass the mid-action gate with only
                          #    streaming-off audio under a -3 HEARD line (r3)
    2: 0.30,  4: 3.30,    # C: dawn early | morning late - the light move is the
                          #    clip's one arc and SHOT_TIME depends on its order
    11: 0.30, 13: 3.30,   # I: close alongside | risen-behind ribbon
    1: 0.20,              # B: the SWEEP - energy in the scroll-decision second;
                          #    the recede is the shot's exit, never its body
    6: 0.30,  8: 2.40,    # E: perch | the LEAP - the mini-arc cannot reverse
    7: 0.40,  9: 3.50,    # F: the bend | the river opening out
   12: 1.20,              # H: pour-to-shake, not the uncap
   15: 0.30, 17: 3.30,    # K: gold sheets | the break arriving
}

CARD_Y       = 0.72
CARD_STYLE   = "fragment"
# Three facts and one ask, every figure from a named fetched source; spans disjoint
# by construction (0-3 · 5-7 · 10-12 · 16-19), craft L107.
# FIVE cards, spans 0-0 · 1-2 · 5-7 · 10-12 · 16-17, disjoint by construction;
# ZERO figures on any card - deliberate (a figure invites the range-endpoint trap).
# J0 ROUND 1 (2026-08-11) rewired these: the cold open was ILLEGIBLE as a border
# (the anti-signage rule strips every visual cue, so the CARD must say what the
# frame lawfully cannot) and the rewind was unsignalled (the film's one structural
# idea was invisible - a midday->dawn cut with no cue reads as a continuity error).
# Cards are rendered by cards.py, not generated, so this carries ZERO invented-text
# risk. "ALL OF IT" also dropped (J4: hardened an unqualified adjective into a
# totality claim) - the Sarawak card is specific AND inside the wikipedia quote.
CARDS = [
    ("SABAH ENDS HERE",           0, 1, "cap"),   # the border made legible, shot 0 only
    ("REWIND TO DAWN",            1, 2, "cap"),   # the structure, said out loud
    ("KLIAS: PROBOSCIS COUNTRY",  5, 3, "cap"),   # operator-verified; odds off screen
    ("SARAWAK. STILL TOLL-FREE.", 10, 3, "cap"),  # the crossing lands + verified toll-free
    # J0 r2: the CTA ends at shot 17 so the cut to the lamps ANSWERS it - a card
    # still asking while Kuching is on screen is decoration, not an open loop.
    # AND: shot 0's card is STRUCTURAL - a cards.py fallback to drawtext on it is
    # a BUILD FAILURE, not a warning (J0 r2 finding 5).
    ("KUCHING BY DUSK?",         16, 2, "cta"),   # a question, answered by the cut
]
AI_LABEL_BURNED_IN = False           # platform AI toggle at upload - a HUMAN step

# ---------------------------------------------------------------- RELATIONSHIPS
RELATIONSHIPS = {
    "subject_vs_background":
        "Three driving sources (B, I, and C's windscreen) each state the camera "
        "axis relative to travel and what the glass shows - the desafarm "
        "sideways-road defect is a stated axis here, and window-and-road geometry "
        "is read on the raw contact sheet at ingest before any assembly.",
    "performance_vs_sound":
        "Nev's moments each carry their own audio at the declared level: the "
        "jetty boarding has the boat taking his weight (-8), the "
        "pour its own water-and-laugh (-6), the closing grin its lapping evening "
        "promenade (-9, agreeing with FOLEY[18]) - performed emotion is backed by place sound, and syncqc refuses a "
        "foreground-FOLEY clip whose audio lane is empty.",
    "bed_vs_foley":
        "The bed holds the 48-beat grid; the places speak over it at declared "
        "levels - barrier clank -3, splash -3, leap -5, surf -6. The desafarm "
        "soundscape measurement (cuts changed place, sound did not) is re-run on "
        "this cut: a film that crosses road, river, jungle, coast and city MUST "
        "change sound at those cuts or this pair has failed.",
    "card_vs_card":
        "Five cards, spans 0-0, 1-2, 5-7, 10-12, 16-17 - disjoint by "
        "construction (craft L107), zero figures on any of them, and planqc 12's "
        "clock check blocks any edit that reintroduces an overlap at y=0.72.",
    "event_vs_window":
        "All three EVENTs (barrier lift, water splash, the pour) declare one "
        "continuous action filling the whole clip - no 'resolves inside N "
        "seconds' anywhere - and the engine's mid-action hard gate (craft L102) "
        "refuses any window ending above 80% of its own peak.",
    "arc_vs_shot_order":
        "The order that matters is G's: the arm RISES at shot 0 and the vehicle "
        "is THROUGH at shot 10. SHOT_WINDOW = {0: 0.30, 10: 3.30} pins it "
        "mechanically; syncqc's arc-order check and the eye on the strip are the "
        "second and third belts.",
    "picture_grid_vs_music_grid":
        "One 240ms whip at boundary 4 (wheel -> hull, the film's only "
        "mode-of-travel change). The engine reserves the overlap by contract "
        "(engine.BLEND_RESERVES_OVERLAP, planqc 34, one mechanism since "
        "2026-08-11) and verify measures post-blend boundaries against the same "
        "48-beat grid TARGET_S was computed from.",
    "clip_variety_vs_shot_count":
        "Seven of thirteen sources carry two shots, and every pair is two DECLARED "
        "states (C: dawn -> morning light move; E: branch -> leap; G: rise -> "
        "through; J: parked -> walk-out; K: cliff -> break-line; F: bend -> "
        "opening; I: alongside -> ribbon). The allocator's "
        "look-dupe gate refuses same-look pairs at >=0.80 and ingest_gate "
        "measures each source's best window pair before assembly - a source that "
        "cannot supply two looks loses its second shot at plan level (L103/104).",
}

GRADE_SAT    = 1.00                  # SOURCE LIGHT IS TRUSTED (his instruction, twice)
GRADE_BRI    = 0.0
TARGET_BLACK = 10.0                  # profile values, reported not enforced
TARGET_SAT   = 74.5

# ---------------------------------------------------------------- CONTENT
CONTENT = {
    "claim":    "The toll-free Pan-Borneo Highway links Kota Kinabalu to Kuching, "
                "crossing from Sabah into Sarawak at the Sindumin-Merapok border; "
                "the Klias wetlands - proboscis monkey country - sit about two "
                "hours' drive from KK; Tusan Beach's sandstone cliffs are about 40 "
                "minutes from Miri; the film compresses the crossing into one "
                "told-forward day, dawn KK to dusk Kuching.",
    "verified": "THREE sources, all fetched 2026-08-11. (1) Wikipedia, Pan-Borneo "
                "Highway: 'toll-free', designated AH150, Malaysian section '2,083 "
                "kilometres', Bruneian section '168 kilometres', and the "
                "'Lawas-Merapok-Sindumin section' marking the Sabah-Sarawak "
                "transition. (2) amazingborneo.com, Klias Wildlife Safari River "
                "Cruise: 'approximately 112km from Kota Kinabalu city', 'a scenic "
                "2 hours ride', proboscis monkeys along the Klias river - AND the "
                "operator's own caveat, quoted: 'Amazing Borneo Tours does not "
                "guarantee wildlife sightings'. That caveat is why the card says "
                "PROBOSCIS COUNTRY and never promises a sighting. (3) "
                "southeastasiabackpacker.com, Sarawak itinerary: Tusan Beach "
                "'about 40 minutes from Miri'; its Blue Tears bioluminescence is "
                "stated for 'September-December' - TODAY IS AUGUST, so Blue Tears "
                "is DELIBERATELY ABSENT from film and cards both. DELIBERATELY "
                "OFF SCREEN: exact KK-Kuching distance and drive time (no single "
                "fetched source states one figure for the full leg - a number "
                "nobody states does not go on a card), border document formality "
                "(process detail, goes stale), any Defender price or spec (not "
                "yet verified against a source - the review here is visual), and "
                "the SE trim (unverifiable on film with all badges banned - it "
                "stays out of every on-screen text; J4 2026-08-11). HUMAN STEP AT "
                "PUBLISH, recorded here because J4 asked for it: the caption/"
                "description must acknowledge the compression - the real drive is "
                "1,000+ km over multiple days and the full land route transits "
                "Brunei; this film compresses it to one told-forward day and "
                "shows one crossing. The card asks a question (KUCHING BY DUSK?) "
                "precisely so the film never asserts the timeline as fact.",
    "twist":    "The border is the hook, not the scenery: the film spends its one "
                "irreversible change - the barrier lifting, Sabah becoming "
                "Sarawak - at frame zero as a cold open, then rewinds to dawn and "
                "tells the road that earned it. Nobody in this genre opens on the "
                "crossing.",
    "why_stop": "A striped barrier arm already rising over an empty jungle road "
                "answers 'where is this going?' before the viewer can ask it - "
                "and the rewind to dawn makes the question personal: how far back "
                "does this road start?",
}

# ---------------------------------------------------------------- PLATES
PLATES = {
    "nev": {"job": None, "res": "4k", "ar": "4:5", "cr": 0,
            "status": "EXISTS - the measured 97-image library, no generation. "
                      "UPLOADED to Higgsfield 2026-08-11, media ids: "
                      "front_neutral efdb9f44-cd50-4976-86c8-ca4afa395a00 · "
                      "front_calm 44009a35-52c5-4fb4-92c8-e3f1763b7af8 · "
                      "front_smile 66e529c7-d40e-4508-a242-103d68b59e1b · "
                      "profile_right 1bdbaed4-3297-488f-9373-ec9885027f2a · "
                      "back_head 451cdf9d-ac99-435d-adf3-693b87e1161c. "
                      "Wardrobe refs are PROMPT-TEXT ONLY this build - the "
                      "container cannot reach upload.higgsfield.ai (403, "
                      "measured again 2026-08-11) and the wardrobe files are "
                      "not in the public repo; declared per-prompt instead, "
                      "a stated choice.",
            "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                              "assets/nev/face/profile_right.jpeg",
                              "assets/nev/face/front_calm.jpeg"],
            "wardrobe_refs": ["assets/nev/wardrobe/04_check_navy/21_front.jpeg",
                              "assets/nev/wardrobe/04_check_navy/23_back.jpeg"],
            "must_show": "actually him - face, hair, EARRING. WARDROBE FOR THIS "
                         "FILM, repeated inside every human source prompt because "
                         "a spec that lives only here is never read (mahua's "
                         "wardrobe bug): NAVY CHECK SHIRT worn open over a BLACK "
                         "TEE (04_check_navy), dark trousers. Dry EXCEPT the "
                         "declared pour at shot 12 (hair wet in that clip only; "
                         "by the golden-hour shots, hours later, he is dry again "
                         "- stated continuity, not drift). The splash stays "
                         "outside the cabin.",
            "prompt": "(identity from photo references, not regenerated)"},

    "defender": {"job": "ac20b2f6-e69a-4d99-9d7e-0427bfc78b45", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-11, 5504x3072. OCR CLEAN at 2048px: zero "
                      "text, no plate, no badges, no tyre lettering (glc300 "
                      "protocol, run in the Higgsfield sandbox).",
            "must_show": "Land Rover Defender 110 SE, L663 generation. GEOMETRY, "
                         "not badge-trust: boxy two-box silhouette with short "
                         "front and rear overhangs; upright windscreen; flat "
                         "roof; squared wheel arches; round LED headlamps set in "
                         "square surrounds; small squared rear lamps in a black "
                         "rear panel; SIDE-HINGED tailgate carrying an EXTERNAL "
                         "SPARE WHEEL - the signature; flush glazing; five-door "
                         "110 body. Colour: deep gloss green, body-colour roof. "
                         "EMPTY licence-plate recess front and rear, no badges, "
                         "no lettering anywhere.",
            "prompt":
            "Photograph of a deep green Land Rover Defender 110, L663 generation, "
            "parked three-quarter rear on red laterite ground against a wall of "
            "Borneo rainforest, bright equatorial daylight. Boxy two-box "
            "silhouette, short overhangs, upright windscreen, flat roof, squared "
            "wheel arches, round LED headlamps in square surrounds, small squared "
            "rear lamps in a black rear panel, side-hinged tailgate with an "
            "external full-size spare wheel, flush glazing, five-door body. THE "
            "LICENCE-PLATE RECESS IS EMPTY front and rear - no plate fitted, no "
            "lettering of any kind on the body, no badges. Full-frame DSLR, 35mm, "
            "f/5.6, ISO 100. REAL PHOTOGRAPH ARTEFACTS, not a render: true paint "
            "reflections with sky gradient rolling along the panel creases, "
            "clear-coat orange peel, faint panel-gap shadows, fine red dust on "
            "the lower panels catching the light, correct tyre sidewall relief, "
            "no HDR halos. Negative: CGI, videogame look, any visible "
            "registration or number plate, badge or model lettering, tyre brand "
            "lettering, dealer sticker, wrong proportions, sloped modern "
            "crossover roofline, oversaturated postcard grade."},
            # THE THREE-QUARTER REAR IS DELIBERATE: it puts the Defender's one
            # unfakeable signature - the side-hinged tailgate and external spare -
            # dead centre, and it is the angle most of the film's tracking shots
            # see. J4 protocol: LOOK at the render, OCR it, THEN reference it.

    "klias": {"job": "fb748a80-7151-4469-befc-20ccc8d42a8e", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-11, 5504x3072, OCR CLEAN",
            "must_show": "the Klias river: broad, slow, tea-brown water between "
                         "unbroken walls of mangrove and nipah palm, flat bright "
                         "overcast sky, a plain wooden jetty low over the water. "
                         "NO signage, no buildings beyond the jetty.",
            "prompt":
            "Photograph of a wide slow tea-brown river in Sabah, Borneo - the "
            "Klias wetlands - dense unbroken walls of mangrove and nipah palm on "
            "both banks, a plain weathered wooden jetty standing low over the "
            "near bank, flat bright overcast tropical sky, still water carrying "
            "soft reflections of the green. No boats, no people, no signage of "
            "any kind. Full-frame DSLR, 35mm, f/8, ISO 200. Real photograph "
            "artefacts: true water reflections, haze in the far bend, no HDR "
            "halos. Negative: CGI, videogame look, postcard oversaturation, any "
            "signboard or lettering, buildings, power lines."},

    "tusan": {"job": "8926debd-3b50-46f0-8c13-cc52f2b56d14", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-11, 5504x3072, OCR CLEAN",
            "must_show": "Tusan Beach near Miri at golden hour: tall layered "
                         "sandstone cliffs glowing orange, a long flat sand "
                         "shelf, shallow gold-lit surf sheets, grassy clifftop "
                         "in the foreground. NO horse-shaped arch claim - the "
                         "cliff line is generic Tusan strata, not a named "
                         "formation.",
            "prompt":
            "Photograph from the grassy clifftop at Tusan Beach near Miri, "
            "Sarawak, golden hour: tall layered sandstone cliffs glowing deep "
            "orange in low sun, a long flat sand shelf far below, shallow surf "
            "sliding in as flat gold-lit sheets, the South China Sea burning to "
            "the horizon. Empty - no people, no vehicles, no signage. Full-frame "
            "DSLR, 24mm, f/8, ISO 100, low sun flaring softly at frame edge. "
            "Real photograph artefacts: true backlit spray, long soft shadows on "
            "the grass, no HDR halos. Negative: CGI, videogame look, postcard "
            "oversaturation, any signboard or lettering, horse-shaped rock arch, "
            "people, buildings."},

    "kuching": {"job": "038e32ad-8c9b-4cfe-82c5-6289df3678a4", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-11, 5504x3072, OCR CLEAN",
            "must_show": "Kuching waterfront at dusk: the riverfront promenade "
                         "with lamps just lit, the Sarawak river dark and calm, "
                         "warm western afterglow low in the sky, city glow "
                         "across the water. ALL SIGNAGE ILLEGIBLE OR ABSENT.",
            "prompt":
            "Photograph of the Kuching riverfront promenade in Sarawak at dusk, "
            "blue hour beginning: ornate promenade lamps just lit and warm, the "
            "wide river dark and calm with lamp reflections standing in it, a "
            "warm orange afterglow dying low in the western sky, soft city glow "
            "and rooflines across the water. The promenade is nearly empty. NO "
            "legible signage anywhere - any signboard is distant, dark or turned "
            "away. Full-frame DSLR, 35mm, f/2.8, ISO 800, true mixed colour "
            "temperature - warm lamps against blue sky. Real photograph "
            "artefacts: lamp flare, reflection shimmer on the water, no HDR "
            "halos. Negative: CGI, videogame look, postcard oversaturation, "
            "legible signboards or lettering, crowds, daylight."},
}

PROBE_FIRST  = "G"     # the barrier lift. It is the hook, it is the highest
                       # signage-pressure frame in the film (premortem 1), and it is
                       # the one clip whose failure means the film does not exist.
                       # Probe alone (defender plate 4cr + 22.5cr), LOOK + OCR, then
                       # batch the other 11.

# GENERATED 2026-08-12 (session 9, scheduled retry). seedance_2_0, 720p, std, 5s,
# 9:16, generate_audio=true. ALL THIRTEEN returned 720x1280, 5.062s, AAC. ZERO
# failures. MEASURED SPEND: 4,270.07 -> 3,977.57 = 292.50cr, exactly 13 x 22.5;
# total with plates 308.5cr = the gated figure to the credit. Remote batch QC:
# OCR clean (3 sub-glyph noise hits, no legible text - border, boulevard and city
# all sign-free), luma median 104 with ZERO outliers (cabin C = 89.8; the
# desafarm 37.7 silhouette did not recur), dawn->dusk arc visible in the means.
# Job ids in projects/panborneo/JOBS.json. Fetch: python tools\pull_panborneo.py
CLIPS = {"G": "panborneo_G.mp4", "B": "panborneo_B.mp4", "C": "panborneo_C.mp4",
         "A": "panborneo_A.mp4", "D": "panborneo_D.mp4", "F": "panborneo_F.mp4",
         "E": "panborneo_E.mp4", "I": "panborneo_I.mp4", "H": "panborneo_H.mp4",
         "J": "panborneo_J.mp4", "K": "panborneo_K.mp4", "L": "panborneo_L.mp4",
         "M": "panborneo_M.mp4"}


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
