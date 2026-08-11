#!/usr/bin/env python3
"""
DESAFARM_PLAN — "NEV · BRZ TO DESA DAIRY FARM, KUNDASANG", the FOURTH travel_vlog
and the FIRST plan written entirely against the 2026-08-07 lessons.

Title readback resolved 2026-08-07 (his picks):

  "subaru brz"   -> HIS CALL DELEGATED TO ME: "either, pick by what looks better".
                    PICKED: ZD8, second generation (2021+). Reason, stated so he can
                    overrule it: the ZD8's geometry is far more SPECIFIABLE - hexagonal
                    grille, thin swept headlamps with a C-shaped DRL, big functional
                    front-fender vent, ducktail bootlid - whereas the ZC6 is close
                    enough to a GT86/FR-S that a generator will blend them and J4 will
                    veto an invented badge. CONFIRM AT THE PLATE: if the rendered ZD8
                    looks wrong, the ZC6 prompt is one edit away and costs 4cr.
  hook           -> THE GOAT TAKES IT. His pick over the calf headbutt and the first
                    sip. An animal with AGENCY - it lunges and pulls the bottle out of
                    his grip. Nothing in this subject's field does that.
  kundasang.py   -> THIS REPLACES IT. His pick. Two films from one location shot weeks
                    apart reads as repetition. plans/kundasang.py is archived; its 20
                    premortem risks and its judge verdicts are folded in below.
  window budget  -> HYBRID, 13 sources / 20 shots / ~300cr. His pick, and it is the
                    direct answer to what he caught on mahua: a STATIC source gets ONE
                    shot, only a clip with real internal movement earns two.
  "30 seconds"   -> 28.31s = 46 beats at 97.5 BPM. The measured travel_vlog band is
                    16-29s and planqc 2 blocks 30.0. Fourth time this readback has run.
  "720p"         -> his words. std, never fast (planqc 15).
  bed            -> liqwyd-to-the-moon, 97.5 BPM NATIVE, ZERO stretch, 14.6dB, 154s,
                    CC BY 3.0 (BGM/travel_vlog/MEASURED.md). NOT Crystal-Water
                    (kundasang's) and NOT Easy-Love (mahua's). The bed chose the tempo.

FIELD SCAN (Phase 0, 2026-08-07): Desa Dairy Farm content is a PHOTO-STOP genre - the
green hills, the New Zealand comparison, a cone of ice cream, a drone over the pasture.
Almost none of it shows an animal DOING something to the visitor. THE UPGRADE: an
animal with agency. A goat that pulls. A calf that shoves. The farm acts on him instead
of posing behind him.

VERIFIED FACTS (fetched 2026-08-07, sources in CONTENT below):
  RM10 Malaysian adult with MyKad (RM20 non-Malaysian, RM7 child 7+) · 8am-5pm daily
  · ~2,000m elevation at Mesilau, Kundasang · Holstein Friesians · ~2 hours from Kota
  Kinabalu · soft-serve made from the farm's own milk · NO WALK-INS, tickets must be
  booked in advance.
That last fact is the card that turns a nice video into a plan - the same job
"GATE SHUTS AT 5PM" did on mahua.

STATUS 2026-08-07: NOTHING GENERATED. 2 plates to build (8cr); the crocker road plate
is REUSED from mahua at ZERO cost. This file is free.
"""

PROJECT   = "NEV AT DESA DAIRY FARM · travel vlog · BRZ day trip · Kundasang"
PILLAR    = "travel_vlog"
GEN_MODE  = "coverage"               # INERT BY DESIGN (bugsense class 2): engine.py
                                     # does not read it. Declared so the next session
                                     # can tell deliberate from forgotten.
BPM       = 97.5                     # = liqwyd-to-the-moon's MEASURED native tempo.
BEAT      = 60.0 / BPM               # 0.615385s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 28.31                    # 46 beats = 28.3077s. Inside the measured 16-29s.

LESSONS_ACK = {            # ledger counts this plan was written against (planqc 23)
    "general craft": 116,  # 99, 100 and 101 were all filed 2026-08-07 BY THIS PLAN'S
    "travel vlog":    6,   # OWN PROBE AND INGEST - premortem "THE OTHER FOUR SECONDS",
                           # "THE LIGHT IS A SPEC" and "EXPOSE FOR WHAT". Source A,
                           # source C and _LOOK were all rewritten against them.
                           # RE-ACKED 2026-08-11 after reading craft L102-L114 and
                           # travel vlog L5 - ALL fifteen were filed FROM THIS PLAN'S
                           # OWN v2 rejection (the nine defects his eye caught). The
                           # ones that touch the rebuild are PREMORTEM entries below;
                           # the ones already mechanised (L102 mid-action hard gate,
                           # L103/104 look-dupe gate, L107 card clock in planqc 12,
                           # L110 verify BLOCK means BLOCKED, L113 craft topic split,
                           # L114 threshold provenance = planqc 33, tv L5 = planqc 34
                           # + engine.BLEND_RESERVES_OVERLAP) are cited where the
                           # plan leans on them.
    # NEIGHBOURING PILLARS (planqc 23b, blocking since 2026-08-08; acked 2026-08-11
    # after reading all three): the transferable prior art is i8 L9-L12 (3-second
    # retention beats watch time, hooks UNDER 2s complete 23% better, a Reel rewards
    # ONE EVENT not a tour - this plan's hook IS a single sub-2s event, by design),
    # and lc300 L5 (fx.whip's xfade once applied its prep filters to the ENTIRE
    # clip, not the seam - this plan declares a whip, so that history is live here).
    # The car-identity lessons (i8 doors, S450 grille, ZX trim) do not transfer.
    "bmw i8 car cinematic": 16,
    "car cinematic": 15,
    "toyota land cruiser 300 zx car review": 8,
}
# This is the FIRST plan written after the day he actually looked at footage. Eleven
# lessons were filed on 2026-08-07 and every one of them that can touch this build is a
# PREMORTEM entry below with its mitigation - not a citation, a design change.

PREMORTEM = [
    ("THE OTHER FOUR SECONDS (craft #99, filed 2026-08-07 BY THIS PLAN'S OWN PROBE, "
     "which is what the probe is for). Source A v1 ended 'Resolves inside one second.' "
     "I told a FIVE second generator my action lasted ONE and it wrote the other four: "
     "job 8f6de91a delivered motion 4-13 - a calm drink - across 0.0-2.6s, the goat "
     "disengaged at 2.8s and trotted off by 3.5s, and the LUNGE and YANK the prompt "
     "demanded appear NOWHERE in the clip. Note precisely what did and did not fail: "
     "'already in contact at frame zero' WORKED, contact was live at 0.00. The opening "
     "was never the problem. The unwritten four seconds were",
     "Source A is rewritten as a MONOTONIC escalation first frame to last with an "
     "explicit FORBIDDEN list naming the calm feed, and 'resolves inside N seconds' is "
     "banned from any prompt where N is shorter than CLIP_S. All 14 sources were then "
     "re-audited against this before the remaining spend: 13 already declared either "
     "'continuous X first frame to last' or a held state, and A was the only hole. "
     "Source H remains the pattern to copy - it declares its arc explicitly."),

    ("'FULLY EXPOSED' IS NOT AN INSTRUCTION UNTIL YOU SAY EXPOSE FOR WHAT (craft #101, "
     "filed 2026-08-07 at this plan's own ingest, one lesson after the fix for #100 "
     "shipped). Source C - the cabin - CARRIED the new exposure clause and still came "
     "back a silhouette: mean luma 37.7 against a 14-clip average near 100, and 59.7% "
     "of every frame crushed to pure black, WORSE than the source A take already "
     "rejected at 22.6%. A camera pointed through a windscreen meters the bright GLASS "
     "and the driver falls into shadow. The clause demanded a fully exposed frame and "
     "never named the subject the exposure serves",
     "Two changes, and the second is the one that generalises. (1) Any shot with a "
     "bright field behind the subject - windscreen, doorway, window, sky behind a "
     "face, backlit anything - names the METERING TARGET as the loudest line in its "
     "prompt: 'EXPOSE FOR THE CABIN, NOT FOR THE WINDSCREEN - the glass is allowed to "
     "blow out and that is correct', with silhouette, backlit subject, dark interior "
     "and dim cabin in the negative block. (2) MEASURE EVERY CLIP'S MEAN LUMA AGAINST "
     "THE OTHER CLIPS OF THE SAME FILM before assembly, never only against a fixed "
     "band: 13 of 14 landed between 81.7 and 121.6 and the outlier at 37.7 was obvious "
     "ONLY in that comparison. Any band wide enough to accept a real dawn shot is wide "
     "enough to accept a silhouette."),

    ("THE LIGHT IS A SPEC, NOT A MOOD (craft #100, filed 2026-08-07 by this plan's own "
     "probe, one clip after #99 and caused by the fix for it). Source A v2 delivered "
     "the action exactly as rewritten - motion 15.6-31.7 across the first 0.8s against "
     "v1's 5.6-11.8, the goat rearing with its front hooves off the ground by t=0.30 - "
     "and arrived 37 luma DARKER than v1: mean 65.3 against 102.7, darkest frame 49.1, "
     "22.6% of every frame crushed to black. The rewrite was all struggle and "
     "escalation in capitals and said NOTHING about light, so the model matched the "
     "drama with a moody low key. It still passed the pillar's [35,200] luma band, "
     "which is the whole point: a band does not protect a hook",
     "Two changes. (1) _LOOK now carries a TIME-AGNOSTIC exposure clause - the stated "
     "hour is a hard spec, the frame is FULLY EXPOSED at whatever hour, never low-key, "
     "never crushed - plus dusk, underexposed, low-key, crushed blacks, heavy shadow "
     "and teal-and-orange in the negative block. Time-agnostic because this film runs "
     "dawn to golden and a blanket 'bright afternoon' would break B, H, I and M. "
     "(2) AT INGEST, compare each clip's mean luma against the clips it will be CUT "
     "AGAINST, not only against the pillar band. A hook 37 luma below its neighbours "
     "is his 'way too dark' note arriving in the RAW, where the retired lighting "
     "master cannot be blamed and no grade can rescue it."),

    ("THE HOOK IS PROMPTED IN CAPITALS AND THE GENERATOR IGNORES IT (craft, filed "
     "2026-08-07 from mahua: source A's prompt demanded 'THE DROP IS ALREADY HAPPENING "
     "AT FRAME ZERO' and the delivered clip was airborne until t=0.55s - HALF a 1.2s "
     "hook was a run-up over an empty pool, and planqc, clipqc and verify all stayed "
     "green because none of them checks the JOIN between plan and cut)",
     "THREE defences, because one was not enough. (1) source A's prompt puts the goat "
     "ALREADY IN CONTACT with the bottle at frame zero and describes the pull, not the "
     "approach. (2) BAN_SPANS is left empty ON PURPOSE and is filled AT INGEST from the "
     "measured action peak - the run-up gets banned once we can see where it ends. "
     "(3) tools/syncqc.py check 1 BLOCKS if the event lands past 40% of shot 0's "
     "delivered window. Run it after build, before verify, every time."),

    ("A STATIC SOURCE RE-USED IS THE SAME PICTURE TWICE (travel vlog, filed 2026-08-07: "
     "mahua PASSED planqc 8 and delivered six duplicate framings - E 8/11 at 0.975 "
     "histogram correlation - because check 8 only forbids a repeated source+crop pair "
     "and assumes a different crop makes a different picture. It does not. The only two "
     "sources that did NOT duplicate were the two with real internal motion)",
     "HIS PICK, AND THE WHOLE REASON THIS PLAN COSTS 300cr INSTEAD OF 214: thirteen "
     "sources for twenty shots. The SEVEN that carry two shots all have real internal "
     "movement - A the goat pulling, B and I the car moving, C the drive, E the calf "
     "feeding, G the goats jostling, H a performed arc. The SIX static ones - D the "
     "parked car, F the herd, K the hills, L the walk-out, J the milk, M the car "
     "detail - carry ONE shot each and are never re-cropped."),

    ("A SPEC THAT LIVES ONLY IN THE PLATE IS NEVER READ BY THE GENERATOR (craft, filed "
     "2026-08-07: mahua declared the wardrobe in PLATES[nev].must_show, sources G and H "
     "never repeated it in their own prompts, and the delivered film had the persona in "
     "THREE different garments - white print shirt, black tee, blue-grey shirt)",
     "EVERY human source below names the garment, the hair and the state EXPLICITLY in "
     "its own prompt text: 'white print shirt under an open dark overshirt, hair dry'. "
     "Five sources carry the persona (A, C, E, H, L) and all five carry the sentence. "
     "The plate is the identity; the PROMPT is the contract with the generator."),

    ("A NEGATIVE BLOCK DOES NOT STOP INVENTED SIGNAGE (craft, filed 2026-08-07: mahua "
     "shot 7 shipped a sign board on a post with 'No railings, no boards, no signage' "
     "in the positive prompt AND 'invented signage text' in the negative block - both "
     "ignored, and it is lesson 35's class surviving both guards written for it)",
     "A WORKING FARM IS THE HIGHEST SIGNAGE RISK THIS REPO HAS PLANNED - gates, feed "
     "sacks, milk cartons, ticket booths, information boards. So the framing does the "
     "work the words could not: every source is composed on ANIMALS, HANDS, GRASS, "
     "SKY or TARMAC with no built furniture in frame, the milk is shown in a plain "
     "unbranded glass and a plain cone, and the farm buildings are never framed. "
     "clipqc text-zoom crops are READ BY EYE on all thirteen clips."),

    ("OCR IS NOT A LOOK (craft, filed 2026-08-07: mahua's plates passed RapidOCR clean "
     "of all text and the mahua plate was still WRONG - a thin two-tier cascade where "
     "its own prompt said 'one unbroken column' and its own negative list banned "
     "'tiered or fanned cascade'. Every clip citing it inherited the error)",
     "Both new plates are LOOKED AT against their own must_show line, item by item, "
     "before a single clip cites them - the BRZ for its nose, DRL shape and ducktail, "
     "the farm for black-and-white Holsteins on OPEN GREEN SLOPE with no buildings. If "
     "the sandbox cannot display an image that is a BLOCKER to report, not a step to "
     "skip. Automated checks ADD to the look; they never replace it."),

    ("SOURCE LIGHTING IS TRUSTED AND THE RELIGHT PATH IS THE DEFECT (craft, filed "
     "2026-08-07 after he said it for the SECOND time: 'the lighting in the raw "
     "footages are already good, and then our video automation lighting master edits "
     "and made it worst'. His approval band is 47 luma WIDE)",
     "travel_vlog shot_match_max_move is now 0.0 - the stage cannot move source luma at "
     "all. NOTHING in this plan grades toward a target: GRADE_SAT 1.00, GRADE_BRI 0.0. "
     "At 2,000m the light is hard and high-contrast and that is CORRECT for the place. "
     "DO NOT report an exposure spread as a defect - read the pillar's "
     "shot_match_source and craft L51-L54 first, and state his measured band next to "
     "any number before calling it a fault."),

    ("A COLD OPEN THAT REWINDS IS BECOMING A FORMULA (craft, this plan's own risk: "
     "mahua opened on the payoff and rewound to dawn, it worked, and this plan does it "
     "again. Two films with the same structural trick is a house style; three is a rut, "
     "and the field-scan advantage disappears the moment it is predictable)",
     "DECLARED, NOT HIDDEN. It is used here because the day's only real EVENTS are at "
     "the farm and planqc 9 requires shot 0 to be one - a dawn departure is a tour. "
     "TIME_JUMPS carries the reason. THE NEXT MUSIC-LED PLAN MUST NOT REWIND: build the "
     "hook from an event that genuinely happens first, e.g. a cold start, a launch, a "
     "door, a gate opening. Noted here so the next session inherits the constraint."),

    ("THE HERO SOUND KEY THE ENGINE ACTUALLY READS IS NOT DEFINED (craft: engine.py "
     "reads SOUND['hero_shot'] under edit_sfx=hero_only and silently defaults to 0; "
     "crown defined 'hero' and the only sound in a 30s film would have played 14.00s "
     "early on a 278cr build)",
     "SOUND['hero_shot'] is DEFINED below as an int. travel_vlog runs hero_only so it "
     "is LIVE, not latent. bugsense --class 1 must return zero findings for "
     "plans/desafarm.py before any credit moves."),

    ("SOMETHING THAT MUST BE HEARD IS NOT IN THE CLIP (craft L67: engine reads "
     "FOLEY={shot: gain_db}, ONE gain on that clip's OWN generated audio, plus one bed "
     "and one hero transient. Three layers, and there is no per-shot sfx stack)",
     "This is an ANIMAL film, so the sound is the content: A names the goat's grunt and "
     "the bottle scraping, E names the calf's suck and butt against the bottle, G names "
     "the herd's bleating and hooves, F names distant lowing, B/C/I name the boxer "
     "engine. generate_audio stays TRUE on every clip. syncqc check 3 verifies every "
     "foreground-FOLEY shot's clip actually HAS audio - a foreground gain on silence is "
     "silence, louder."),

    ("A CARD ASSERTS A NUMBER TWO SOURCES DISAGREE ABOUT (craft: J4's absolute veto on "
     "crown's price and on kundasang's unsourced nickname; and on mahua a card asserted "
     "the LOW END of a 1.5-2h range as fact while claiming two agreeing sources, one of "
     "which stated no drive time at all)",
     "Three cards, and every figure on them comes from ONE named source that states it "
     "outright: RM10 with MyKad, book ahead, 2,000m. The 'Little New Zealand' epithet "
     "is NOT on a card in our own voice - it was J4-vetoed once already. Prices go "
     "stale, so CONTENT.verified carries the fetch date beside every figure and the "
     "card says RM10 WITH MYKAD, which is the qualifier that makes it checkable."),

    ("THE BOARD CANNOT RENDER THIS PLAN (craft L65: board.py:216 hardcodes a 3x3 legend "
     "and indexes col_x[n // 3], so any plan above 9 SOURCES raises IndexError. This "
     "plan has THIRTEEN by his explicit instruction)",
     "KNOWN, DECLARED, NOT WORKED AROUND. The hybrid window budget is HIS PICK and it "
     "is the fix for a defect he found by eye, so the plan is right and the tool is "
     "capacity-limited. tools/storyboard.py renders it correctly TODAY and "
     "tools/contact.py covers the review that actually matters. board.py's two-line fix "
     "(rows = ceil(n/3); index col_x by n // rows) stays HIS call - it is a PIPELINE "
     "file and a plan-level fix is not available here."),

    ("THE PLAN AND THE CUT ARE NEVER CHECKED AGAINST EACH OTHER (craft, filed "
     "2026-08-07 from his diagnosis: 'the video editor must also sync with the "
     "mastermind planner... mastermind planned something but other agents / roles didnt "
     "follow'. Three green gates shipped a broken hook because each checks only one side)",
     "tools/syncqc.py runs AFTER build and BEFORE verify, every time. Five checks on "
     "the join: the hook lands in the first 40% · every EVENT/PAYOFF window contains an "
     "action peak · every foreground-FOLEY clip has audio · repeated windows sit >=1.0s "
     "apart in-clip · an ARC source is delivered in order. Source H performs an arc "
     "here, so check 5 is LIVE on this build."),

    ("THE RAW CLIPS GET DELETED AND A PROVISIONAL THRESHOLD CAN NEVER BE RE-DERIVED "
     "(craft L66: every kk_*.mp4 is gone, so travel_vlog's motion_floor 0.6 and "
     "brightness_band [35,200] are STILL provisional three builds later)",
     "mahua's nine raws plus this build's thirteen are the measurement. Keep all of "
     "them until clipqc's numbers have been used to mark motion_source and "
     "brightness_source MEASURED. This film is the better sample: a 2,000m farm in open "
     "sun is the BRIGHTEST this pillar will shoot, where mahua's gorge was the darkest."),

    # ---- added 2026-08-11 at the L102-L115 / tv-L6 re-ack ----
    ("THE MIXER'S CLAMP EATS HALF THE CORRECTION AND PRINTS THE CLAMPED VALUE AS "
     "SUCCESS (craft L105: FOL_DB = max(-8, min(8, want)) reported +8 when the foley "
     "needed +16.3, so 'the bgm covers all the sfx' shipped with a green mix line). "
     "This build's sound design leans on six foreground foley moments, so the same "
     "lie would bury the goat's grunt - the hero sound of the film",
     "Every foley pick for this build comes from the measured bank with clean_only "
     "semantics where possible: bank.pick() ranks gain_limited_db==0 files FIRST and "
     "why() prints the shortfall warning on any file the clamp may bind on. Any file "
     "carrying gain_limited_db > 1 dB is either replaced from the bank or its "
     "shortfall is stated next to the mix line - the clamp can bind, it can no "
     "longer bind SILENTLY."),

    ("A TRANSITION THAT SHORTENS THE TIMELINE KNOCKS EVERY LATER CUT OFF THE MUSIC "
     "AND NO PER-SHOT CHECK CAN SEE IT (travel vlog L5 - filed FROM this plan's own "
     "v2: the declared 240ms whip removed 197ms from shot 8 and 60% of the film sat "
     "~170ms early against a bed that kept its tempo). This plan still declares the "
     "same whip after shot 8",
     "ONE MECHANISM now, not two agreeing by hand (closed 2026-08-11): engine.py "
     "reserves and renders each blend-in shot one blend-width longer - the blend "
     "eats the OVERLAP, never the timeline - and planqc 34 reads the engine's own "
     "BLEND_RESERVES_OVERLAP contract constant instead of a hand-set plan flag. "
     "verify's beat-grid check then measures the delivered cut boundaries "
     "post-blend, so a regression cannot pass both gates."),
]

# ---------------------------------------------------------------- PLATES
PLATES = {
    "nev": {"job": "4c542b39-a06e-42c6-affd-2d6d3c93a392", "res": "4k", "ar": "4:5",
            "cr": 0, "status": "3-angle face set, EXISTS (reused from KK/kundasang/mahua)",
            "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                              "assets/nev/face/profile_right.jpeg",
                              "assets/nev/face/front_calm.jpeg"],
            "must_show": "actually him - face, hair, EARRING. WARDROBE FOR THIS FILM, "
                         "and it is repeated inside every human source prompt because "
                         "a spec that lives only here is never read by the generator "
                         "(craft, 2026-08-07): white print shirt under an OPEN dark "
                         "overshirt, hair dry, no cap, no sunglasses. Kundasang sits at "
                         "2,000m and is genuinely cold, so the overshirt stays on all "
                         "day - there is no wet/dry state to track in this film, which "
                         "is one continuity risk fewer than mahua had.",
            "prompt": "(identity from photo references, not regenerated)"},

    "brz": {"job": "99f6a417-a806-41da-beb6-36a7f9931992", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-07, 5504x3072. VERIFIED BY EYE against every line of "
                      "must_show, not just OCR'd (craft, 2026-08-07: OCR IS NOT A LOOK): "
                      "low wide coupe, power-bulge bonnet, hexagonal lower grille between "
                      "two intakes, functional fender vent, hard character line into the "
                      "haunch, dark multi-spoke wheels, World Rally Blue, NO PLATE FITTED "
                      "and no badge lettering. RapidOCR at 2048px: zero text. NOTE FOR THE "
                      "NEXT SESSION: the plate's BACKGROUND reads temperate/European "
                      "rather than Bornean - it anchors the CAR only, and the desa plate "
                      "anchors the place. Was: 4cr at 4k. A named product is NEVER generated from "
                      "text alone - a text-only '2026 Toyota Crown' returned a generic "
                      "crossover and shipped an 87cr wrong-car build. LOOK AT THIS "
                      "PLATE against every line of must_show before any clip cites it.",
            "must_show": "Subaru BRZ, ZD8 second generation (2021+). GEOMETRY, not "
                         "badge-trust: low wide coupe, long bonnet with a pronounced "
                         "power bulge, HEXAGONAL lower grille flanked by two large "
                         "functional intakes; slim swept headlamps each carrying a "
                         "C-SHAPED daytime-running signature; a big functional vent "
                         "behind each front wheel arch; a hard character line running "
                         "from that vent into the rear haunch; a DUCKTAIL lip moulded "
                         "into the bootlid, not a bolted wing; twin round exhaust tips; "
                         "18-inch multi-spoke wheels. Colour: World Rally Blue.",
            "prompt":
            "Photograph of a World Rally Blue Subaru BRZ, ZD8 second generation, parked "
            "three-quarter front on a narrow highland road with green pasture and "
            "layered blue ridges behind it. Low wide coupe proportions, long bonnet "
            "with a power bulge, hexagonal lower grille between two large functional "
            "intakes, slim swept headlamps each with a C-shaped daytime-running "
            "signature, a functional vent behind each front wheel arch, a hard "
            "character line into the rear haunch, a ducktail lip moulded into the "
            "bootlid, twin round exhaust tips, 18-inch multi-spoke wheels. THE "
            "NUMBER-PLATE RECESS IS EMPTY - no plate is fitted, front or rear, and no "
            "lettering of any kind appears on the body. Full-frame DSLR, 50mm, f/5.6, "
            "ISO 200. REAL PHOTOGRAPH ARTEFACTS, not a render: true paint reflections "
            "with a visible sky gradient, accurate panel gaps, correct tyre sidewall "
            "relief, no HDR halos. Negative: CGI, videogame look, any visible "
            "registration or number plate, plate lettering, dealer sticker, model badge "
            "text, invented badges, tyre brand lettering, bolted rear wing, SUV or "
            "sedan proportions, oversaturated postcard grade.",
            "_look_note": "J4 ROUND 2 on mahua: _LOOK is appended to every SOURCE "
                          "prompt and to NO PLATE prompt, so a plate framed "
                          "three-quarter FRONT with no plate ban is how an invented "
                          "registration gets baked into a 4cr image and carried into "
                          "six shots. This plate carries its own ban."},

    "desa": {"job": "da216e46-883a-4e7a-9709-d82db0fa8fe9", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-07, 5504x3072. VERIFIED BY EYE: black-and-white "
                      "Holsteins on open rolling green pasture, bare granite ridge above "
                      "the far treeline, hard highland light and crisp shadow, and - the "
                      "risk this plan called its highest - NO BUILDINGS, NO SHEDS, NO "
                      "GATES, NO TICKET BOOTHS, NO SIGNAGE. RapidOCR returned one "
                      "0.52-confidence artefact on grass texture and nothing legible. "
                      "Was: 4cr at 4k. The PLACE anchor for seven of thirteen "
                      "sources - the heaviest single-plate load this repo has planned, "
                      "so FRAMING below states a distinct camera position for every one "
                      "of them (planqc 28).",
            "must_show": "Desa Dairy Farm, Kundasang at 2,000m: black-and-white "
                         "Holstein Friesian cattle grazing on OPEN ROLLING GREEN "
                         "PASTURE, the bare granite ridge of Mount Kinabalu standing "
                         "above the far treeline, cool highland light, a plain wire "
                         "fence line at most. NO BUILDINGS, NO SHEDS, NO GATES, NO "
                         "TICKET BOOTHS, NO FEED SACKS AND NO SIGNAGE ANYWHERE - a "
                         "working farm is the highest invented-text risk this repo has "
                         "planned and the framing is the guard, not the wording.",
            "prompt":
            "Photograph of a highland dairy pasture at two thousand metres in "
            "Kundasang, Sabah, Borneo. Black-and-white Holstein Friesian cattle grazing "
            "on open rolling green slopes, the bare granite ridge of Mount Kinabalu "
            "rising above the far treeline, cool clear highland light with hard "
            "sunlight and crisp shadow, a plain wire fence line low in the frame. "
            "Full-frame DSLR, 35mm, f/8, ISO 100. REAL PHOTOGRAPH ARTEFACTS, not a "
            "render: true atmospheric haze with distance, accurate grass texture and "
            "variation, real hide markings, no HDR halos. Negative: CGI, videogame "
            "look, oversaturated postcard grade, any buildings sheds barns gates or "
            "ticket booths, any signage or text, feed sacks, milk cartons, crowds, "
            "snow, drone-stock look.",
            "_reuse_note": "This plate REPLACES kundasang.py's 'kundasang' plate, which "
                           "was planned and never built. That plan is archived."},

    "crocker": {"job": "014b8022-5d1b-4b5b-8c46-6ac8bdd3166f", "res": "4k", "ar": "16:9",
            "cr": 0,
            "status": "BUILT 2026-08-07 FOR MAHUA AND REUSED HERE AT ZERO COST. "
                      "5504x3072, OCR clean (zero text detected). The road to Kundasang "
                      "and the road to Tambunan are the same Crocker Range tarmac, so "
                      "the plate is correct for both and the 4cr is already spent. "
                      "ASSET HYGIENE: check ledgers and prior plans for an existing "
                      "plate before budgeting a new one.",
            "must_show": "a narrow sealed two-lane mountain road switchbacking along a "
                         "forested ridge, layered blue ridges receding, low cloud in "
                         "the valleys, no buildings and no signage.",
            "prompt": "(already built — see plans/mahua.py PLATE_JOBS['crocker'])"},
}

# _LOOK is appended to every source prompt, so every word in it is BOILERPLATE and is
# subtracted by planqc 29 before a linkage token is checked. Written to contain NONE of
# the carry tokens used below (goat, bottle, calf, milk, road, herd, hills, grass,
# wheel, engine, sun).
# EXPOSURE CLAUSE ADDED 2026-08-07 mid-probe, craft #100. Source A v2 fixed the action
# exactly as written and arrived 37 luma darker than v1 - mean 65.3 against 102.7, 22.6%
# of every frame crushed to black - because the rewrite was all struggle in capitals and
# said NOTHING about light, so the model matched the drama with a moody key. It still sat
# inside the pillar's [35,200] band, which is exactly why a band does not protect a hook.
# The clause is deliberately TIME-AGNOSTIC: this film runs dawn -> golden and a blanket
# "bright afternoon" would break B, I, H and M. It demands EXPOSURE, not brightness.
_LOOK = (
    "The stated time of day is a hard specification, not a mood: whatever the hour, the "
    "frame is FULLY EXPOSED and every subject in it is clearly readable - never "
    "underexposed, never a low-key or moody treatment, never crushed black shadows. "
    "Cold clear highland air at two thousand metres; true texture on skin, hide, cloth "
    "and paint. REAL FOOTAGE, NOT A RENDER: handheld micro-shake, natural depth of "
    "field, accurate reflections, no HDR halos. Negative: underexposed, low-key "
    "lighting, moody darkness, crushed blacks, heavy shadow, teal-and-orange grade, "
    "CGI, videogame look, postcard "
    "oversaturation, invented signage text, legible device screens, visible "
    "registration plates, model badges or lettering of any kind, any legible slogan "
    "wordmark logo or printed graphic on clothing, buildings sheds or ticket booths in "
    "frame, extra fingers, warped faces, drone-stock look."
)

_WARDROBE = ("white print shirt under an open dark overshirt, hair dry, no cap, no "
             "sunglasses; face, hair and EARRING match the references exactly")

# ---------------------------------------------------------------- SOURCES (13 x 22.5cr)
SOURCES = {
 # REWRITTEN 2026-08-07 AFTER THE PROBE, and the old text is quoted in the comment
 # because the defect IS the lesson. v1 ended with "Resolves inside one second." -
 # I told a FIVE second generator that my action lasted ONE, and it wrote the other
 # four. Measured on job 8f6de91a: motion 4-13 (a calm drink) across 0.0-2.6s, the
 # goat disengaged at 2.8s and trotted off by 3.5s. There was no lunge and no yank
 # anywhere in the delivered clip. CAPITALS did not save it. "Already in contact"
 # DID work - contact was live at frame 0.00, so keep that device.
 # THE LAW: script all five seconds or the model scripts them for you. An action
 # verb is not a clip; a clip is a state that must hold for the whole window.
 # Source H is the pattern to copy - it declares a MONOTONIC arc first to last.
 "A": ("EVENT · THE GOAT TAKES IT", "#C4562F", "EVENT", ["desa", "nev"],
       "Vertical 9:16. THE EVENT. THIS CLIP IS ONE CONTINUOUS ESCALATION FROM ITS "
       "FIRST FRAME TO ITS LAST AND IT NEVER SETTLES - there is no calm second "
       "anywhere in it. AFTERNOON. Camera close and low beside the man from the "
       "second reference images (" + _WARDROBE + "), crouched on the open green "
       "slope of the first reference image with a plain white feeding bottle in his "
       "hand. AT FRAME ZERO THE TAKE IS ALREADY IN PROGRESS, MID-STRUGGLE, NEVER "
       "BEGINNING: the brown-and-white goat's mouth is already CLAMPED on the "
       "bottle, its head already wrenched hard sideways, its front hooves already "
       "off the ground, his wrist already bent over by the pull and his elbow "
       "already dragged forward. Nothing approaches, nothing starts, the first "
       "frame is already the middle of it. From there it ONLY escalates and never "
       "reverses: the goat twists further and DOWN, the bottle tears out of his "
       "grip, his hand snatches after it and closes on air, he rocks back on his "
       "heels, and the goat carries the bottle away past the lens with its head "
       "high while he is still reaching after it. The last frame is the emptiest "
       "his hand ever is. FORBIDDEN - these are exactly the failures this shot "
       "exists to avoid: the goat calmly drinking or nursing, the goat standing "
       "still with the bottle in its mouth, all four hooves planted on the ground, "
       "a settled peaceful feed, any second of this clip in which nothing is being "
       "pulled. " + _LOOK.replace(
           "Negative: ",
           "Negative: calm feeding, peaceful nursing, static animal, ")),

 "B": ("BRZ on the highland road", "#7B3F6B", "EXTERIOR", ["crocker", "brz"],
       "Vertical 9:16. DAWN going to full MORNING - one continuous light move, which "
       "is why this single clip serves both of its shots. Long lens from across a "
       "valley onto the switchbacking mountain road of the first reference image: the "
       "blue coupe from the second reference image climbing away from the lens into "
       "layered ridges, open green slope falling away below the road, low cloud lying under it and burning off the tarmac as "
       "the sun reaches it. Continuous vehicle movement first frame to last. " + _LOOK),

 # REWRITTEN 2026-08-07, craft #101. v1 carried the new _LOOK exposure clause and
 # STILL came back a silhouette: mean luma 37.7 against a 14-clip average near 100,
 # 59.7% of every frame crushed to pure black - worse than the source A take already
 # rejected at 22.6%. A camera pointed through a windscreen meters the bright GLASS
 # and the driver falls into shadow. "FULLY EXPOSED" was not an instruction until it
 # named what the exposure serves. Any shot with a bright field behind the subject -
 # windscreen, doorway, window, sky behind a face - must name the metering target as
 # the loudest line in the prompt.
 "C": ("cabin, low in the seat", "#4A6FA5", "HUMAN", ["nev", "brz"],
       "Vertical 9:16. MORNING. EXPOSE FOR THE CABIN, NOT FOR THE WINDSCREEN - this "
       "is the single most important instruction in this shot. Bright morning "
       "daylight FLOODS the interior and fills it; the driver's face, hands and "
       "clothing are fully lit and clearly readable at all times; the windscreen is "
       "allowed to be bright, even blown out, and that is correct. NEVER a "
       "silhouette, NEVER a dark cabin against a bright window, NEVER a dim moody "
       "interior, NEVER crushed black shadows anywhere in the frame. Interior of the "
       "low blue coupe from the second "
       "reference image, over-the-shoulder onto the windscreen: the man from the first "
       "reference images (" + _WARDROBE + ") driving, sitting LOW the way a sports car "
       "seats you, one hand on the wheel, the highland road unrolling ahead through "
       "the glass and green pasture opening on both sides. Continuous forward "
       "movement of the road through the glass, first frame to last. "
       "Real skin, no smoothing. "
       "No legible instrument display of any kind. " + _LOOK.replace(
           "Negative: ",
           "Negative: silhouette, backlit subject, dark interior, dim cabin, ")),

 "D": ("BRZ at the pasture edge", "#8C3B3B", "EXTERIOR", ["brz", "desa"],
       "Vertical 9:16. MORNING. Low three-quarter static on the blue coupe from the "
       "first reference image, stopped on grass at the edge of the open pasture of the "
       "second reference image, the granite ridge standing behind it. Slow push toward "
       "the car, cloud shadow travelling across the paint and the slope. No buildings, "
       "no fencing furniture, no signage in frame. " + _LOOK),

 "E": ("the calf takes the bottle", "#B5843A", "HUMAN", ["nev", "desa"],
       "Vertical 9:16. MIDDAY going to AFTERNOON. Close, camera at crouching height "
       "beside the man from the first reference images (" + _WARDROBE + ") holding a "
       "plain white bottle to a black-and-white Holstein calf on the pasture of the "
       "second reference image. The calf SHOVES the bottle upward with its head the "
       "way calves actually feed, tongue working, froth at the corner of its mouth, "
       "his arm absorbing each butt. Continuous animal movement first frame to last. "
       + _LOOK),

 "F": ("the herd on the slope", "#5B8C5A", "EXTERIOR", ["desa"],
       "Vertical 9:16. MIDDAY. Ground level among black-and-white Holstein cattle on "
       "the open green slope of the reference image, shallow focus, the granite ridge "
       "soft behind them. Animals shifting and grazing continuously, ears and tails "
       "moving, one lifting its head toward the lens. No buildings, no fencing "
       "furniture, no text of any kind in frame. " + _LOOK),

 "G": ("goats at the rail", "#93507E", "EXTERIOR", ["desa"],
       "Vertical 9:16. MIDDAY going to AFTERNOON. Camera close at goat height on the "
       "pasture of the reference image: five or six brown-and-white goats crowding and "
       "jostling toward the lens, climbing over each other, heads pushing through a "
       "plain wire fence line, mouths working. Constant animal motion and collision "
       "first frame to last. No feed sacks, no buckets, no signage. " + _LOOK),

 "H": ("NEV · THE LAUGH", "#A9553E", "HUMAN", ["nev"],
       "Vertical 9:16. AFTERNOON going to GOLDEN. THIS CLIP PERFORMS A CHANGE OF STATE "
       "FROM ITS FIRST FRAME TO ITS LAST AND THAT ARC IS THE POINT OF IT - it must be "
       "MONOTONIC, never a loop. Medium-close on the man from the reference images "
       "(" + _WARDROBE + "), chest up, the jostling goats over one shoulder and the switchback road dropping away below the green slope over the other, both thrown soft. HE "
       "STARTS STARTLED: eyes wide, mouth open, head pulled back, hands still up where "
       "the bottle was. Then it TURNS across the second half of the clip - the shoulders "
       "drop, he shakes his head once and breaks into a real laugh, looking off toward "
       "the animals. Real skin, no smoothing. " + _LOOK),

 "I": ("PAYOFF · the road down", "#6A4F8C", "PAYOFF", ["brz", "crocker"],
       "Vertical 9:16. THE PAYOFF. GOLDEN hour. Camera tracking from behind the blue "
       "coupe of the first reference image as it pulls away and runs down the "
       "switchbacking mountain road of the second reference image, low sun coming "
       "through the trees and raking along its flank in bars, ridges going blue and long behind "
       "it. Continuous forward movement, first frame to last. " + _LOOK),

 "J": ("the milk, cold", "#3F7BA8", "EXTERIOR", ["desa"],
       "Vertical 9:16. AFTERNOON. Macro-close, held in a hand: a plain unbranded glass "
       "of cold fresh milk with condensation running down it, the open green slope of "
       "the reference image thrown far out of focus behind. Light coming through the "
       "top edge of the milk. Nothing else in frame - no label, no packaging, no "
       "printing of any kind on the glass. " + _LOOK),

 "K": ("the hills, wide", "#1F6E63", "EXTERIOR", ["desa"],
       "Vertical 9:16. MIDDAY. Static wide on the rolling green pasture of the "
       "reference image, cattle scattered small across two ridgelines, the granite peak "
       "above the far treeline, cloud shadow moving across the whole slope. The only "
       "motion is the shadow and the grass. No buildings and no signage anywhere. "
       + _LOOK),

 "L": ("NEV walks out with the bottle", "#4F7B5F", "HUMAN", ["nev", "desa"],
       "Vertical 9:16. MIDDAY. Tracking backwards ahead of the man from the first "
       "reference images (" + _WARDROBE + ") as he walks out across the open pasture of "
       "the second reference image carrying a plain white feeding bottle, cattle in the "
       "middle distance turning toward him, wind pulling at the open overshirt. "
       "Head-and-chest framing, continuous walking movement. " + _LOOK),

 "N": ("the goat walks off with it", "#C77A3F", "EVENT", ["desa", "nev"],
       "Vertical 9:16. AFTERNOON. Camera low at goat height on the open green slope of "
       "the first reference image: the brown-and-white goat TROTS AWAY from the lens "
       "with the plain white bottle of milk gripped sideways in its mouth, head high, "
       "other goats turning to follow it; the man from the second reference images ("
       + _WARDROBE + ") is out of focus behind, half-risen from his crouch with both "
       # PROMPT HYGIENE, 2026-08-07: the rationale for this source used to be written
       # INSIDE the prompt string - "source A already spends the take and its own
       # prompt says it resolves inside one second... J2 round 1, 2026-08-07" - which
       # the generator reads as CONTENT, not as a note to me. It also shipped the exact
       # phrase craft #99 just banned. Rationale belongs in a comment; the prompt says
       # only what the camera sees. WHY THIS SOURCE EXISTS: A spends the take, so a
       # second window of A could only replay frames the film has already used (J2 R1).
       "hands still open. This is the AFTERMATH: the bottle is already gone and the "
       "goat is already leaving, never the moment of taking it. Continuous animal "
       "movement first frame to last. " + _LOOK),

 "M": ("BRZ detail, ridge behind", "#6E5B3A", "EXTERIOR", ["brz", "desa"],
       "Vertical 9:16. GOLDEN hour. Tight low detail on the blue coupe of the first "
       "reference image - front wheel arch vent, the hard character line, the ducktail "
       "lip - with the green slope and granite ridge of the second reference image "
       "held soft behind it, the road dropping away below. Slow lateral drift along the flank, low sun raking the "
       "paint. No badges and no lettering anywhere on the body. " + _LOOK),
}

# FRAMING (planqc 28). SEVEN sources cite the desa plate - the heaviest single-plate
# load this repo has planned - so every camera position is stated. A plate anchors
# PLACE; framing must be declared or the model returns the picture it was given.
FRAMING = {
    "A": "close and low beside the crouching subject, animal head filling one side",
    "B": "long lens across the valley, vehicle receding up the road into ridges",
    "C": "interior over-the-shoulder, windscreen and wheel, low seating position",
    "D": "low three-quarter static on the vehicle, slow push, ridge centred behind",
    "E": "crouching height, tight two-shot of hand, bottle and calf's head",
    "F": "ground level among the herd, shallow, ridge as soft background",
    "G": "close at goat height, animals crowding INTO the lens",
    "H": "medium-close static, chest up, the subject changing state inside the frame",
    "I": "rear tracking behind the vehicle, road descending away from the lens",
    "J": "macro in-hand on the glass, everything else thrown far out of focus",
    "K": "static wide, two ridgelines, subjects tiny, shadow the only movement",
    "L": "backward tracking, head-and-chest, subject walking INTO lens",
    "N": "low at goat height BEHIND the animal, subject trotting AWAY from lens",
    "M": "tight low detail on the flank, slow lateral drift",
}

# ---------------------------------------------------------------- TIMELINE 20 shots
# 46 beats at 97.5 BPM = 28.3077s. burst = 2 beats = 1.2308s, med = 4 beats = 2.4615s.
# 17 bursts + 3 meds. Median 1.2308s against the profile's 1.13s (range 0.6-2.51).
# 20 shots / 28.308s = 42.4 cuts/min against the profile's 40.3 (band 32.2-48.4).
# THE WINDOW BUDGET IS THE POINT OF THIS PLAN: seven sources with real internal motion
# carry two shots each; the six static ones carry one and are never re-cropped.
# The three meds sit on clips that CHANGE inside themselves - the calf feeding, the
# laugh turning, the road running out - never on a static frame.
SHOTS = [
 ("A", 1.00, "burst", "the goat takes it - lunges and yanks the bottle clean out of his hand on the open green slope"),
 ("B", 1.20, "burst", "rewind to first light: the blue BRZ climbing the road toward that same green slope"),
 ("C", 1.00, "burst", "low in the seat, one hand on the wheel, the road unrolling ahead"),
 ("B", 1.15, "burst", "the road opening out, pasture on both sides, the ridge ahead"),
 ("C", 1.15, "burst", "hands on the wheel, the road now running straight through open pasture - he is here"),
 ("D", 1.00, "burst", "the BRZ stopped on the grass at the edge of the pasture"),
 ("F", 1.00, "burst", "the herd on the slope, one lifting its head at him"),
 ("K", 1.20, "burst", "the hills wide - the whole green slope and the granite ridge"),
 ("L", 1.00, "burst", "he walks out across the grass with the bottle, cattle turning"),
 ("E", 1.15, "med",   "the calf takes the bottle and shoves it upward, froth, his arm absorbing it"),
 ("G", 1.00, "burst", "the goats crowd the rail, climbing over each other, mouths working"),
 ("N", 1.00, "burst", "the goat walks off with the bottle, the others turning to follow"),
 ("H", 1.00, "burst", "the laugh: startled first, hands still up where the bottle was, the goats still going behind him"),
 ("G", 1.20, "burst", "the goats still pushing, unbothered, while the calf feeds on behind them"),
 ("E", 1.30, "burst", "back to the calf, calmer now, draining the last of the milk out of the bottle"),
 ("J", 1.00, "burst", "the milk itself - a plain cold glass of it, condensation running, the animals behind"),
 ("H", 1.20, "med",   "the laugh lands - shoulders down, still looking at the animals, the road down waiting"),
 ("I", 1.00, "burst", "the BRZ pulls away down the road, low sun in bars across its flank"),
 ("M", 1.00, "burst", "last look at the car - the flank, the ducktail, the ridge behind, the road below"),
 ("I", 1.15, "med",   "the last of it: the road down, ridges going blue and long"),
]

CALLBACKS = []          # no repeated (source, crop) pair exists
DELOGO    = {}          # EMPTY ON PURPOSE. The signage risk is handled by FRAMING, not
                        # by a box guessed before a clip exists. Populate from the
                        # measured clip at ingest, then re-run.

# RESOLVED AT INGEST, 2026-08-07, AND THE ANSWER IS "NOTHING TO BAN".
# It was left empty on purpose because mahua proved a frame-zero instruction is a
# request, not a guarantee - mahua's hook was airborne until t=0.55s and the first HALF
# of the shot was a run-up over an empty pool. So A was probed three times and MEASURED,
# not assumed:
#     A v1  motion 5.6 -> 11.8 over the first 0.8s, floor 3.9   NO EVENT AT ALL
#     A v2  motion 15.6 -> 31.7, floor 10.0                     event live, light dead
#     A v3  motion 29.1 -> 43.6, floor 16.8                     KEPT
# v3 never drops below 16.8 anywhere in five seconds - there is no run-up, no settle and
# no dead span to ban, so this stays empty on the evidence rather than on hope. If the
# delivered cut still reads late, the fault is the ALLOCATOR, not the clip: measure
# again before adding a span here. tools/syncqc.py check 1 blocks if the event lands
# past 40% of shot 0's window.
# ---------------------------------------------------------------- SCENE REFS
# HIS CORRECTION 2026-08-11, looking at the storyboard: "it uses the same three
# reference picture... analyze the scene and choose which reference picture is the
# best to use... you got a front face, side face, back face, zoom in, zoom out,
# close-up". The library is assets/nev/ - 97 measured images (index.json): a 6-frame
# face turnaround, closeups, 11 wardrobe sets shot front/profile/back. This film's
# wardrobe is 10_shirt_white_print. 1-3 refs per scene - the BEST match, never the
# blanket. profile_right and front_calm carry the EARRING (README finding 5).
# planqc 27b enforces: entry per human source, <=3, not all identical, back ref on
# any shot from behind.
SOURCE_REFS = {
    # A: camera close and low BESIDE him, crouched mid-struggle -> his side to the
    # lens: right profile (earring) + front anchor + the shirt worn on a body.
    "A": ["assets/nev/face/profile_right.jpeg",
          "assets/nev/face/front_neutral.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg"],
    # C: OVER-THE-SHOULDER onto the windscreen -> the camera sees the back of his
    # head and the right side of his face, never a full front. Back of head + right
    # profile + the overshirt's BACK.
    "C": ["assets/nev/face/back_head.jpeg",
          "assets/nev/face/profile_right.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/76_back.jpeg"],
    # E: crouching height BESIDE him feeding the calf -> side-on again: right
    # profile + front anchor + shirt front.
    "E": ["assets/nev/face/profile_right.jpeg",
          "assets/nev/face/front_neutral.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg"],
    # H: THE LAUGH - medium-close, chest up, INTO the lens, startled -> laugh.
    # Both endpoint expressions, plus the shirt front for the chest-up frame.
    "H": ["assets/nev/face/front_neutral.jpeg",
          "assets/nev/face/front_smile.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg"],
    # L: tracking backwards AHEAD of him -> full frontal walk: calm front (earring)
    # + neutral front + shirt front on a full body.
    "L": ["assets/nev/face/front_calm.jpeg",
          "assets/nev/face/front_neutral.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg"],
    # N: out of focus BEHIND the leaving goat, half-risen, facing the lens at
    # distance -> identity is soft here by design: one front + the shirt is enough.
    "N": ["assets/nev/face/front_neutral.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg"],
}

BAN_SPANS = {}

# THE ONE DECLARED BACKWARDS BOUNDARY (planqc 30). Boundary 0 only.
TIME_JUMPS = {
    0: "COLD OPEN. Shot 0 is afternoon - the goat taking the bottle - and shot 1 "
       "rewinds to dawn on the road. The day's only real EVENTS happen at the farm and "
       "planqc 9 requires shot 0 to be one; a dawn departure is a tour. DECLARED RISK, "
       "see the premortem: this is the SECOND film to open on the payoff and rewind. "
       "The next music-led plan must find a hook that genuinely happens first.",
}

BEATS = {"burst": 2, "med": 4}

# ONE WHIP. travel_vlog measured 9.5% designed across six references, ALL of them whips
# (tools/blendsense.py), so the profile declares designed_kinds ['whip'] and
# blend_max_count 2. Taking ONE, at boundary 8 - he walks out with the bottle, SO the
# calf takes it. That is the first consequence beat and the only boundary in the first
# half where the mode of the scene changes. planqc 20 forbids a blend touching an EVENT
# shot, which rules out boundaries 0, 10 and 11 (either side of shots 0 and 11).
BLEND_AFTER  = [8]
BLEND_KIND   = "whip"
BLEND_WIDTH  = 0.24                 # floor of the 240-560ms band: a whip must be FAST

SFX_LEAD     = 0.22
IMPACT_AT    = []                   # hero_only: no whoosh layer on a vlog's cuts
SUBDROP_AT   = []

# ---------------------------------------------------------------- SOUND (ambience gate)
SOUND = {
    "bed":        "BGM/travel_vlog/liqwyd-to-the-moon.mp3 - 97.5 BPM NATIVE, zero "
                  "stretch, 154s (5.4x the video), 14.6dB dynamics, CC BY 3.0. Credit "
                  "line REQUIRED at publish - see BGM/travel_vlog/MEASURED.md. NOT "
                  "Crystal-Water (kundasang's) and NOT Easy-Love (mahua's): three "
                  "Sabah vlogs must not share a track.",
    "hero":       "the goat's grunt and the bottle scraping out of his hand on shot 0. "
                  "After that the farm carries it - hooves, bleating, distant lowing, "
                  "then the boxer engine on the road down.",
    # THE KEY THE ENGINE ACTUALLY READS. engine.py reads SOUND["hero_shot"] under
    # edit_sfx=hero_only and silently defaults to 0. crown defined "hero" and not
    # "hero_shot", which would have put the only sound in a 30s film 14.00s early.
    "hero_shot":  0,
    "duck_shots": [0],
    "silence":    "none - animals are continuous from shot 6 to shot 15; the two quiet "
                  "shots are the wide and the milk, where the bed comes forward",
}

FOLEY = {   # ambience gate: every shot lays its own clip audio, mostly UNDER the bed.
     0:  -3.0,   # A  EVENT - the grunt and the scrape. Must be HEARD. (planqc 19 >= -6)
     1: -11.0,   # B  distant boxer engine on the switchbacks
     2:  -8.0,   # C  cabin, engine note, air
     3: -11.0,   # B  the road, mid distance
     4:  -8.0,   # C  wheel, engine, tyre hum
     5: -12.0,   # D  parked - engine off, only wind
     6:  -7.0,   # F  the herd - lowing, hooves in grass. Forward.
     7: -13.0,   # K  wide, wind only, near-silent
     8: -10.0,   # L  footsteps in grass, cattle shifting
     9:  -5.0,   # E  the calf feeding - suck, butt, froth. The reason the shot exists.
    10:  -6.0,   # G  goats jostling, bleating, hooves on the rail
    11:  -3.0,   # A  EVENT source again - the goat stays forward (planqc 19 >= -6)
    12: -11.0,   # H  his breath and the laugh starting
    13:  -7.0,   # G  goats still pushing
    14:  -8.0,   # E  the calf, calmer
    15: -13.0,   # J  the glass - near-silent, the bed comes forward
    16: -10.0,   # H  the laugh, clean
    17:  -6.0,   # I  PAYOFF - the car leaving. Must be HEARD. (planqc 19 >= -6)
    18: -12.0,   # M  detail, wind only
    19:  -6.0,   # I  PAYOFF source again - the descent stays forward
}

# ---------------------------------------------------------------- THE CLOCK (planqc 30)
# Shot 0 is the COLD OPEN at afternoon; boundary 0 is declared in TIME_JUMPS. From shot
# 1 the clock is strictly monotonic: dawn -> morning -> midday -> afternoon -> golden,
# no state skipped. THERE IS NO DUSK STATE: the farm gate shuts at 5pm
# (explorekundasang.com, fetched 2026-08-07), so a dusk shot at the pasture would be a
# lie a local viewer can catch. Each source prompt PINS its own light state.
SHOT_TIME = ["afternoon",
             "dawn", "dawn",
             "morning", "morning", "morning",
             "midday", "midday", "midday", "midday", "midday",
             "afternoon", "afternoon", "afternoon", "afternoon", "afternoon",
             "golden", "golden", "golden", "golden"]

# ---------------------------------------------------------------- LINKAGE (19 boundaries)
# TYPED, never prose: (kind, token, intent). planqc 29 requires the TOKEN to be findable
# in the writing of BOTH shots it joins, with the shared _LOOK boilerplate subtracted -
# so a connection cannot exist only in my head. Written AFTER the shot order was frozen.
# HIS TAXONOMY, taught 2026-08-07 and now in planqc.CARRY_KINDS: the original seven
# describe what a shot CONTAINS; his six - event, action, activity, motion, audio,
# place - describe what a shot DOES. Definitions in 28-linkage-master.md. This is the
# FIRST plan written with the full thirteen, and it uses ten of them.
# planqc 31 floor: 4 consequence boundaries out of 19. This plan declares 5.
LINKAGE = [
    ("place",       "slope",    "the green slope where the goat took it -> the road climbing toward that same slope, hours earlier"),
    ("place",       "road",     "the highland road from across the valley -> the same road through the windscreen"),
    ("motion",      "road",     "the road climbing away -> the road opening out ahead"),
    ("activity",    "road",     "the drive continues - the same road outside the car, then through the windscreen"),
    ("consequence", "pasture",  "the pasture fills the windscreen, SO he stops the car on the grass"),
    ("place",       "slope",    "the car at the edge of the slope -> the herd standing on the same slope"),
    ("subject",     "ridge",    "the granite ridge behind the herd -> the same ridge above the wide hills"),
    ("place",       "pasture",  "the wide pasture -> the same pasture at walking height as he crosses it"),
    ("consequence", "bottle",   "he carries the bottle out to them, SO the calf takes it"),
    ("place",       "pasture",  "the calf on the pasture -> the goats at the fence line of the same pasture"),
    ("consequence", "goat",     "the goats are crowding and shoving, SO one of them gets the bottle"),
    ("event",       "bottle",   "the bottle is yanked out of his hand -> his hands are still up where it was"),
    ("activity",    "goats",    "the goats carry on regardless - going behind him as he reacts, still going after"),
    ("motion",      "animal",   "constant animal movement carries the cut - goats jostling, then the calf working"),
    ("consequence", "milk",     "the calf drains the bottle, SO the milk is what he goes and drinks"),
    ("place",       "slope",    "the milk held against the green slope -> the same slope soft behind his face"),
    ("consequence", "road",     "the day is done, SO he takes the road down"),
    ("object",      "flank",    "the car pulling away -> the same flank, close, in the last light"),
    ("motion",      "road",     "the car leaving the frame -> the road running down and away"),
]

CROP_XY = {}            # nothing measured yet; populated only from a probe

# SHOT_WINDOW (engine, 2026-08-11): per-shot window pins, allocated BEFORE the free
# search so a free-choice shot cannot steal a pinned window. Source H performs this
# film's only two-window arc (startled -> laugh lands) and the allocator otherwise
# guarantees non-overlap but NOT ORDER - mahua's open risk 1, now closed. Shot 12
# takes the EARLY window (the startle), shot 16 the LATE one (the laugh landing).
# Values are conservative head/tail picks inside the 5.04s clip; REFINE AT INGEST
# from the measured motion curve if the startle sits later than 0.2s. A pin that
# does not fit the free space is an ALLOCATION FAILURE, never a silent fallback.
SHOT_WINDOW = {12: 0.20, 16: 3.60}

CARD_Y       = 0.72
CARD_STYLE   = "fragment"           # pillar style: sentence fragments, <= 6 words
# Three facts and one ask. Every figure comes from ONE named source that states it
# outright, and each carries its fetch date in CONTENT.verified. "Little New Zealand"
# is deliberately NOT on a card - J4 vetoed that epithet once already on kundasang.
CARDS = [
    ("RM10 WITH MYKAD",           4, 4, "cap"),   # verified. The qualifier is the point.
    ("BOOK AHEAD, NO WALK-INS",   9, 4, "cap"),   # verified - and it is the useful one
    # WAS (14, 4) -> shots 14-17, colliding with the CTA on 16-17: two captions
    # printed through each other for 2.5s, the most visible defect in the v2 film
    # (craft L107, and planqc 12 now checks the CLOCK, not just the zone).
    # 2 shots =~ 2.8s is plenty for four words; the zone is CLEAR before the CTA.
    ("TWO THOUSAND METRES UP",   14, 2, "cap"),   # verified
    ("KUNDASANG NEXT WEEKEND?",  16, 4, "cta"),   # a question, not a beg
]
AI_LABEL_BURNED_IN = False          # HUMAN step at upload. Never burned in (planqc 15).

# ---------------------------------------------------------------- RELATIONSHIPS
# planqc 32. Every defect Gavril found in v2 was a RELATIONSHIP between two elements
# that each passed alone (craft L101). For each known pair: how THIS plan holds it.
RELATIONSHIPS = {
    "subject_vs_background":
        "The v2 sin was THIS FILM'S: a side window with the road receding straight "
        "through it - nev driving at 90 degrees to his own road. Every in-car prompt "
        "now states the camera axis AND what the window shows relative to travel "
        "('through the WINDSCREEN, road receding AWAY'; side glass shows the fence "
        "line PASSING, never receding), and the ingest contact sheet is checked for "
        "window-geometry agreement before a single frame is assembled.",
    "performance_vs_sound":
        "Nev performed into silence in v2 (voice-band ratio 0.16-0.25, no better "
        "than empty hills). Every human shot in this plan carries a FOLEY line with "
        "its emotion's sound - the laugh has the laugh, the flinch at the goat has "
        "the grunt AND his breath - at foreground level (>=-6dB), and syncqc's "
        "foreground-foley check refuses a human clip whose audio lane is empty.",
    "bed_vs_foley":
        "The bed sat on top of the place in v2 - a goat pen and a car interior "
        "sounded identical across the cut (0.935 vs 0.947 control). The bed is "
        "ambience-class from the measured bank (target -20 LUFS), foreground foley "
        "sits >=-6dB, and the six hero moments duck the bed; cut-adjacent SFX are "
        "cut_safe picks so the place CHANGES SOUND when the picture changes place.",
    "card_vs_card":
        "v2 printed two captions through each other for 2.5s (craft L107). The "
        "altitude card is now 2 shots (14-15) and the CTA holds 16-19: spans are "
        "disjoint BY CONSTRUCTION, and planqc 12's clock check blocks any edit "
        "that reintroduces an overlap in the y=0.72 zone.",
    "event_vs_window":
        "v2 cut the bottle-snatch at 96% of its own action peak ('important events "
        "are cutted out'). Every EVENT shot here declares a monotonic action that "
        "COMPLETES inside CLIP_S (source A's rewrite is the template), and the "
        "engine's mid-action gate now REFUSES a window ending above 80% of its "
        "peak - it stopped being a sort key and became a wall (craft L102).",
    "arc_vs_shot_order":
        "Source H performs the film's only two-window arc (startled -> laugh). "
        "SHOT_WINDOW = {12: 0.20, 16: 3.60} pins shot 12 to the clip's head (the "
        "startle) and shot 16 to its tail (the laugh landing), so the allocator "
        "cannot deliver the reaction after the laugh - mahua's open risk 1, closed "
        "2026-08-11; syncqc check 5 (arc order) stays LIVE as the second belt.",
    "picture_grid_vs_music_grid":
        "The 240ms whip after shot 8 is timing='overlap': the engine RESERVES a "
        "blend-width on the outgoing shot and the blend eats the overlap, never "
        "the timeline (engine.BLEND_RESERVES_OVERLAP, planqc 34 - one mechanism "
        "since 2026-08-11). The 97.5 BPM grid survives the transition by contract, "
        "and verify measures the post-blend boundaries against it.",
    "clip_variety_vs_shot_count":
        "v2's duplicates split the blame: the editor threw away source C's clean "
        "pair, and source E could never have carried two shots at all (best pair "
        "0.911/0.973). Multi-shot sources here were re-audited for two DECLARED "
        "states per window, the allocator's look-dupe gate REFUSES same-look pairs "
        "at >=0.80, and ingest_gate kills a clip whose best available pair is "
        "already a duplicate before any credit is spent on assembly.",
}

GRADE_SAT    = 1.00                 # SOURCE LIGHT IS TRUSTED. Nothing grades toward a
GRADE_BRI    = 0.0                  # target - his instruction, twice given.
TARGET_BLACK = 10.0                 # profile values, reported not enforced
TARGET_SAT   = 74.5

# ---------------------------------------------------------------- CONTENT
CONTENT = {
    "claim":    "Desa Dairy Farm sits at about two thousand metres in Kundasang, costs "
                "RM10 for a Malaysian adult with MyKad, opens 8am to 5pm - and you "
                "cannot just turn up, tickets have to be booked in advance.",
    "verified": "explorekundasang.com, 'Desa Dairy Farm Kundasang Guide', FETCHED "
                "2026-08-07, states each figure outright: 'Malaysian adults with "
                "MyKad: RM10', non-Malaysians RM20, Malaysian children 7+ RM7, under 7 "
                "free; 'No walk-ins; tickets must be booked in advance'; '8:00 AM - "
                "5:00 PM daily'; Mesilau village, Kundasang, Ranau at approximately "
                "2,000 metres elevation; 'roughly a two-hour drive from Kota Kinabalu'; "
                "the cattle are Holstein Friesians, brought in for milk yield and "
                "highland tolerance; soft-serve ice cream is made from the farm's own "
                "milk. A PRICE IS A MARKET STATUS AND MARKET STATUSES GO STALE - that "
                "is what J4 vetoed on crown - so the card says RM10 WITH MYKAD, which "
                "names the exact qualifier the source names and is checkable at the "
                "gate. DELIBERATELY OFF SCREEN: the 'Little New Zealand' epithet, "
                "which J4 vetoed on kundasang when it was asserted in our own voice. "
                "ALSO OFF SCREEN: the BRZ's market position. Subaru Malaysia lists the "
                "current ZD8 and paultan.org lists the previous ZC6 from RM232,869; a "
                "BRZ at this price point is a recond or used buy, which is the "
                "audience exactly - and it is a status, so it stays in this block "
                "with its date and never on a card.",
    "twist":    "the animals act on HIM. The whole field posts this farm as a "
                "photo-stop - green hills, a cone of ice cream, a drone over the "
                "pasture, the New Zealand line - and in almost none of it does an "
                "animal do anything. Here a goat takes the bottle out of his hand in "
                "the first second and he is still laughing about it four shots later. "
                "A sports car parked on a cow pasture at 2,000m is the second joke, "
                "and neither is explained.",
    "why_stop": "frame zero is an ANIMAL DOING SOMETHING TO A PERSON - it reads at "
                "phone size, it resolves inside a second, and it is funny before it is "
                "pretty; card 2 is the single most useful fact about this place (you "
                "cannot walk in) and it is the one every other post leaves out; the "
                "BRZ gives the recond audience a reason to watch a farm video at all; "
                "and the CTA is a question with a date implied rather than a request "
                "for a follow.",
}

PREVIZ = {  # sketch-grade, NEVER enters generation. The hook is judged at probe.
    "sheet_v1": "",
    "board_v1": "",
    "job":      "",
    "note":     "STANDING ORDER 2026-08-05: a storyboard is SHOWN TO GAVRIL before any "
                "clip credit is spent, and if the persona appears in ANY panel the "
                "sheet MUST carry the identity reference. ADDED 2026-08-07, his "
                "standing order: tools/contact.py --raw runs at INGEST and the contact "
                "sheet reaches him BEFORE anything is assembled. board.py cannot render "
                "13 sources; tools/storyboard.py can.",
}

PROBE_FIRST  = "A"     # the goat taking the bottle. It is the hook, it is the only shot
                       # with an animal acting on a person, and mahua proved the probe
                       # is exactly where a frame-zero instruction gets checked. Buy the
                       # two plates, LOOK, buy A alone, LOOK, then batch the other 12.

# DELIVERED 2026-08-07. tools/pull_desafarm.py writes exactly these filenames into
# projects/desafarm/clips/, so engine.find_clip resolves every source by name and never
# falls through to its glob. 14 sources, 17 generations, 382.5cr - A took three takes
# and C took two, and both re-shoots are recorded in pull_desafarm.py with the measured
# numbers that condemned them. Measured luma band across the delivered 14: 81.7 - 121.6.
CLIPS = {
    "A": "desa_A.mp4", "B": "desa_B.mp4", "C": "desa_C.mp4", "D": "desa_D.mp4",
    "E": "desa_E.mp4", "F": "desa_F.mp4", "G": "desa_G.mp4", "H": "desa_H.mp4",
    "I": "desa_I.mp4", "J": "desa_J.mp4", "K": "desa_K.mp4", "L": "desa_L.mp4",
    "M": "desa_M.mp4", "N": "desa_N.mp4",
}
PLATE_JOBS = {
 "brz":     "hf_20260807_065614_99f6a417-a806-41da-beb6-36a7f9931992.png",
 "desa":    "hf_20260807_065614_da216e46-883a-4e7a-9709-d82db0fa8fe9.png",
 "crocker": "hf_20260807_044021_014b8022-5d1b-4b5b-8c46-6ac8bdd3166f.png",  # reused, mahua
}
CLIP_BASE = ""         # INERT BY DESIGN (bugsense class 2): no pipeline file reads it.
                       # It is the download provenance of the paid artefacts - and on
                       # 2026-08-07 it was the ONLY route by which a remote session that
                       # could not reach the CDN handed nine clips to the machine that
                       # could. Fill it at ingest and never blank it.


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
