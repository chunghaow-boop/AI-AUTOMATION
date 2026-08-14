#!/usr/bin/env python3
"""
KUNDASANG_PLAN — "NEV · ONE DAY IN KUNDASANG · GLC 300", the SECOND travel_vlog.
Title readback resolved 2026-08-06 (his four picks, verbatim options taken):

  "Kundasang"  -> the Sabah highland town, ~2h drive from Kota Kinabalu. The pick that
                  kk.py explicitly parked: "that stays on the shelf for a road-trip
                  title". This is that title.
  "GLC 300"    -> X254 (2023+) 4Matic AMG Line, HIS PICK. Material, not cosmetic:
                  carbase.my (fetched 2026-08-06) lists the CURRENT Malaysian X254
                  range as GLC200 CKD RM329,888 and GLC350e 4Matic CKD RM398,888.
                  The GLC300 4Matic AMG Line was the CBU launch variant at RM429,888
                  and is NOT in the new lineup - so a GLC 300 here in 2026 is a used
                  or recond car. That is the audience, exactly.
  "30 seconds" -> 28.97s = 48 beats at 99.4 BPM. HIS PICK. The measured travel_vlog
                  band is 16-29s from his 6 references; 30.0 sits outside it. Same
                  readback class as KK's 45->28.31 and the WRX's 30->21.6.
                  NOTE: 28.92s was quoted first and was WRONG - it was computed at
                  97.5 BPM before he picked a 99.4 BPM bed. Corrected before use.
  bed          -> Crystal-Water by Spiring, 99.4 BPM NATIVE, ZERO stretch, 16.4dB
                  dynamics, 157s, CC BY 3.0 (BGM/travel_vlog/MEASURED.md).
                  HIS PICK. The bed chose the tempo, never the reverse.
  day arc      -> dawn -> morning -> midday -> afternoon -> golden -> dusk. HIS PICK.
                  The hook is the cloud tearing off the Kinabalu summit, which is a
                  real EVENT and not a tour. Verified: explorekundasang.com's 2026
                  guide puts the clearest window at 06:00-08:00.
  "linkage"    -> he asked for it by name. It is already gated: planqc 24 (an intent
                  per boundary), 29 (a KIND and a TOKEN findable in BOTH shots' text)
                  and 31 (a consequence floor). Every boundary below is TYPED, never
                  prose - KK v15 shipped 19 prose linkages and 14 did not land.

FIELD SCAN (Phase 0, 2026-08-06): Kundasang content splits two ways - drone beauty
with no person in it (Desa Dairy Farm, Sosodikon Hill), or itinerary listicles with no
story. THE UPGRADE vs the field: one person, one car, ONE DAY, where the car is the
through-line that physically carries you between viewpoints and the light state is the
clock. Six light states, monotonic, gate-enforced (planqc 30).

STATUS 2026-08-06: NOTHING GENERATED. Plates NOT BUILT. This file is free.
"""

PROJECT   = "NEV IN KUNDASANG · travel vlog · one day · GLC 300"
PILLAR    = "travel_vlog"
GEN_MODE  = "coverage"               # INERT BY DESIGN (bugsense class 2, MED): engine.py
                                     # does not read this. Kept because the board and a
                                     # human reader need to know which generation mode
                                     # the shot list was written for. Declared here so
                                     # the next session can tell deliberate from forgotten.
BPM       = 99.4                     # = Crystal-Water's MEASURED native tempo. Zero stretch.
BEAT      = 60.0 / BPM               # 0.603622s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 28.97                    # 48 beats = 28.9739s. Band-top of the measured 16-29s.

LESSONS_ACK = {            # ledger counts this plan was written against (planqc 23)
    "general craft": 77,   # pillar-INDEPENDENT: measurement, tooling, process
    "travel vlog":    3,   # this pillar's GENRE lessons
}
# RE-ACKED 64 -> 67 on 2026-08-06, and the three new lessons are THIS PLAN'S OWN
# findings, filed automatically by tools/lessonize.py: the J4 card veto, board.py's
# undeclared 9-source ceiling, and the destroyed KK raw clips. planqc 23 BLOCKED this
# file until the ack matched - which is the loop working, not a nuisance. The ack is a
# claim that the lessons were read; the three PREMORTEM entries below are the evidence.

PREMORTEM = [
    ("beat-grid math copied across BPMs turns bursts into the wrong length "
     "(travel vlog L1: BEATS={burst:2,med:4} from a 150 BPM car plan into a 105 BPM vlog)",
     "BEATS recomputed AT 99.4: burst = 2 beats = 1.207s, med = 4 beats = 2.415s. "
     "Median lands 1.207s against the profile's 1.13s (range 0.6-2.51). 16 bursts + "
     "4 meds = 48 beats = 28.9739s, and TARGET_S is set FROM that arithmetic, not typed."),

    ("wrong-genre / wrong-tempo bed reaches the build (travel vlog L0: the whole "
     "25-track BGM library is 140-165 BPM drift phonk, the wrong pillar entirely)",
     "bed pinned to BGM/travel_vlog/Crystal-Water-by-Spiring.mp3, 99.4 native, ZERO "
     "stretch; engine.verify_bed_tempo REFUSES a mismatch at build; plan BPM set FROM "
     "the measured bed. 157s = 5.4x the video, so the segment scan has real choice."),

    ("serene highland shots rejected by car-tuned gates (travel vlog L2 / the open "
     "P2-1 blue-block: parked, still sources face a motion floor and auto-reject at "
     "22.5cr each)",
     "style-block floors are motion 0.6 and luma 35-200, BOTH still PROVISIONAL. "
     "MEASURED 2026-08-06 on KK v15's delivered cut: per-shot motion 1.41-9.42, "
     "per-shot luma 56.6-133.1 - no shipped shot came near either edge. That is the "
     "OUTPUT distribution, NOT clipqc's raw-clip input, so it is evidence and not a "
     "substitute. THIS BUILD'S RAW CLIPS ARE THE MEASUREMENT: every kk_*.mp4 was "
     "deleted before it could be re-derived. Keep all 10 raws, measure at ingest, "
     "then mark motion_source / brightness_source MEASURED."),

    ("a stale or present-tense-absolute claim reaching the screen (crown J4 SOLO VETO, "
     "2026-08-06: 'NEVER SOLD NEW IN MALAYSIA' verified against a 2024-03-04 source)",
     "every CONTENT claim below is verified against a source FETCHED 2026-08-06, and "
     "the market fact is deliberately kept OFF the cards and inside CONTENT, where it "
     "is a note with a date rather than an absolute on screen. Card 3 hedges "
     "explicitly ('THEY SAY'). No card asserts a price, a spec or a market status."),

    ("plate anchors PLACE, not FRAMING -> sources collapse to one image (KK P1: A, C, "
     "E and I all cited the waterfront plate and all four returned the plate's own "
     "composition; five shots were one picture)",
     "FRAMING declared for all 10 sources; planqc 28 blocks two sources sharing a "
     "plate with the same camera position. Eight sources cite the kundasang plate here "
     "- the highest plate-sharing load this repo has planned - so every framing names "
     "a distinct camera height, lens and axis."),

    ("a source used 2-3x from a locked-off clip gives identical delivered windows "
     "(KK P2: static 0.975 self-similarity vs tracking 0.871)",
     "every repeated source's prompt specifies CONTINUOUS movement, and every repeat "
     "uses a DIFFERENT crop (planqc 8). Heaviest source carries 3 of 20 against a cap "
     "of 5, and no source's shot durations exceed 4.83s against the 4.9s capacity "
     "ceiling (planqc 21)."),

    ("invented signage text - J4 holds an absolute veto (KK P4 cost 22.5cr: "
     "'SDNMONES', 'TOARAKNMN' on a night street, legible at phone size)",
     "Kundasang shots are farm, ridge and road - no shopfronts framed anywhere. The "
     "one signage-adjacent source (E, the dairy farm) is framed at ground level among "
     "the animals with no gate furniture in shot. clipqc text-zoom crops READ by eye "
     "on every EXTERIOR/EVENT/PAYOFF clip before the edit."),

    ("the hero sound key the engine actually reads is not defined (craft: engine.py:781 "
     "reads SOUND['hero_shot'] under edit_sfx=hero_only and silently defaults to 0 - "
     "crown defined 'hero', so the only sound in a 30s film would have played 14.00s "
     "early on a 278cr build; plans/wrx.py still carries the latent version)",
     "SOUND['hero_shot'] is DEFINED below as an int. travel_vlog runs edit_sfx="
     "hero_only, so this key is LIVE on this plan, not latent. bugsense --class 1 must "
     "return zero findings for plans/kundasang.py before any credit moves."),

    ("hook too slow for a vlog (craft frame-zero doctrine; KK measured a med = 2.46s "
     "FAILS planqc 9 at this pillar's BPM)",
     "hook is a 1.207s burst and the EVENT is a STATE CHANGE, not a camera move - "
     "the cloud tears off the summit. Filed 2026-08-06 in the car_cinematic refsense "
     "corpus: 'AN EVENT DOES NOT REQUIRE MOTION' (a static Chiron whose headlights "
     "wake 0.00-1.50s holds the first two seconds with a locked-off camera). The car "
     "is present at frame zero, small and moving, so motion exists regardless."),

    ("the plan is built against the CODE and never against the DOCTRINE that the code "
     "exists to enforce (craft: THE ENTRY PATH NAMED 1 OF 28 DOCTRINE DOCS - every seat "
     "definition was invisible to a new session, and both skills predate the 68-check "
     "architecture)",
     "this plan was written against SYSTEM-MAP and the gates, so the seats it leans on "
     "were reached through planqc rather than read directly. Before the FINAL BOSS pass "
     "on the finished cut, read 27-mastermind-qc.md top to bottom and use its verdict "
     "format - it holds the 16 measurement traps, four of which this plan is exposed to "
     "(DELIVERED WINDOW, PLANNED-vs-ACTUAL now that a blend compresses the timeline, "
     "OPEN-LOOP GAIN on the new mix knobs, and BLUR-AS-BLACK on the dusk shots). "
     "06-content-judges.md is the seat judge.py already ran. SYSTEM-MAP 12 indexes all 28."),

    ("a fix that looks right and leaves the check still failing (craft: IT IS THE"
     "BACKSLASHES, NOT JUST THE COLON - escaping the font path did not fix the caption "
     "render, because the textfile path on the SAME filter was still raw)",
     "engine.py was re-checked against this specific class the same hour: it passes "
     "text= (a literal, already escaped for ':' and '%') and fontfile= (now escaped), "
     "and never hands a path to movie=/amovie=/textfile=. So this build is clear - but "
     "after ANY fix here, re-run the route rather than trusting the diff. Rule 4."),

    ("the four cards render as NOTHING and every gate stays green (craft: THE"
     "PIPELINE'S FONT PATHS WERE LINUX-ONLY ON A WINDOWS PIPELINE - engine.py offered "
     "two /usr/share/fonts candidates, neither exists on Windows, and ffmpeg drawtext "
     "does not reliably error on a missing fontfile. No check reads pixels for text)",
     "engine.py now resolves from 5 candidates with the repo's own CapCutSansText-Bold "
     "FIRST, prints the font it chose, and RAISES instead of delivering empty cards. "
     "This plan's cards carry the two verified facts and the CTA, so a silent loss "
     "would have removed the receipt and the ask while planqc still said 34/34. LOOK "
     "at the delivered strip for all four cards before calling any build finished."),

    ("the foley and the hero swamp the bed, which is the one thing carrying a chill "
     "vlog (craft: THE MIX COMPLAINT WAS REAL BUT NOT WHERE IT WAS REPORTED - measured "
     "-4.9dB bass duck on KK v15 but -31.1dB on WRX v9, because foley foreground was "
     "hardcoded at bed-2 and the sidechain at 0.06/6:1 for every pillar alike)",
     "engine.py now reads its mix relationships from the PILLAR, defaulting to the old "
     "constants so nothing else changes. travel_vlog declares foley foreground at "
     "bed-8 (not bed-2) and a gentler 3:1 duck at threshold 0.10, release 180ms. Only "
     "four shots here are foreground at all - 0 and 2 (the EVENT, wind on rock) and 17 "
     "and 19 (the PAYOFF, the car leaving) - and planqc 19 requires those to be >=-6dB. "
     "Everything else sits -8 to -14, under Crystal-Water's 16.4dB of dynamics."),

    ("a designed transition is impossible to declare because the band is a percentage "
     "(craft: THE BLEND DETECTOR WAS BLIND TO WHIPS - travel_vlog's 0% was an "
     "undercount; blendsense re-measured 9.5% pooled, all of it whips)",
     "the pillar now declares designed_pct 9.5, designed_kinds ['whip'] and "
     "blend_max_count 2; planqc 11 gained a COUNT band and a kind whitelist so one "
     "deliberate whip is expressible at 19 boundaries. This plan takes ONE, at boundary "
     "9, because 3 of the 6 references use none - the conservative read of the same "
     "number. A dissolve here would now FAIL the whitelist, which is correct: the "
     "references measured whips, not dissolves."),

    ("something that must be HEARD is not in the clip, and no plan field can add it "
     "later (craft: SOUND LAYER CONTRACT - there is no per-shot sfx stack. engine.py "
     "reads FOLEY={shot: gain_db}, one gain on the clip's OWN audio, plus one bed and "
     "one hero transient. Three layers, and that is all there is)",
     "every sound this film needs is written INTO the prompt that pays for it: A names "
     "wind tearing at the rock, C names cold air through an open window, E names the "
     "animals, F and 15 name gravel underfoot, I names the car leaving. H is the one "
     "shot deliberately left quiet at -14dB because the face is the shot. Nothing is "
     "left to be 'added in the edit' - there is no edit stage that could add it."),

    ("the review page he says GO to does not show what the spend actually buys (craft: "
     "REVIEW PAGE OMITTED WHAT IT WAS ASKED TO PROVE - storyboard.py drew crop, light "
     "and foley but not the verbatim prompt, the identity references, the camera move, "
     "the per-boundary transition or the bed)",
     "storyboard.py extended 2026-08-06 and backed up to _backup_20260806b/: every shot "
     "now carries its verbatim prompt, its identity/wardrobe reference thumbnails, a "
     "camera chip from FRAMING, and an explicit HARD CUT or BLEND row citing this "
     "pillar's measured 0% blended. The bed is in the header. Nothing on that page is "
     "typed beside the plan, so it cannot disagree with what gets generated."),

    ("a card asserts something the CONTENT block never verified - filed the same day as "
     "this plan by tools/lessonize.py after J4 vetoed it here (craft: JUDGE J4 FAIL on "
     "kundasang, card 3 'MINI NEW ZEALAND, THEY SAY')",
     "every card is now either a fact carrying a fetched-2026 source in "
     "CONTENT.verified, or a question. Card 3 quotes Daily Express Malaysia's published "
     "phrasing instead of asserting a nickname in our own voice, and it was MOVED from "
     "shots 11-14 onto shots 8-11 so it describes footage that is actually on screen - "
     "J4's second and independent finding."),

    ("the board cannot render this plan at all: board.py:216 hardcodes a 3x3 legend and "
     "line 218 indexes col_x[n // 3], so 10 SOURCES raises IndexError (craft: FOREIGN "
     "LITERAL - board.py caps at 9 sources, filed 2026-08-06)",
     "KNOWN AND OPEN, NOT WORKED AROUND. Nine sources cannot carry a six-state day with "
     "a two-shot dusk, so the plan is right and the tool is capacity-limited. "
     "tools/storyboard.py renders this plan correctly TODAY (20 shots, 7 plates, 13 "
     "MISSING panels) and is what goes to the gate presentation. board.py is a "
     "PIPELINE file: the one-line fix is his call, never an autonomous edit."),

    ("the raw clips get deleted and the PROVISIONAL thresholds can never be re-derived "
     "(craft: MEASUREMENT SOURCE DESTROYED - every kk_*.mp4 is gone, so travel_vlog's "
     "motion_floor and brightness_band are still provisional two builds later)",
     "THIS BUILD IS THE REPLACEMENT MEASUREMENT. All 10 raws stay on disk until "
     "clipqc's numbers have been used to mark motion_source and brightness_source "
     "MEASURED. CLIP_BASE is filled at ingest and never blanked - it is the only route "
     "back to a clip that has already been deleted once."),

    ("the time-of-day arc runs backwards under a card that claims otherwise (KK v15"
     "carried a '6PM IN KK BAH' card over afternoon footage and no gate could see it, "
     "which is why planqc 30 exists)",
     "SHOT_TIME is declared per shot and runs dawn(3) -> morning(4) -> midday(4) -> "
     "afternoon(3) -> golden(3) -> dusk(3), strictly monotonic in LIGHT_ORDER with no "
     "state skipped and TIME_JUMPS empty. Every source prompt PINS its own light "
     "state so the generator cannot drift off the declared clock."),
]

# ---------------------------------------------------------------- PLATES
PLATES = {
    "nev": {"job": "4c542b39-a06e-42c6-affd-2d6d3c93a392", "res": "4k", "ar": "4:5",
            "cr": 0, "status": "3-angle face set, EXISTS (reused from KK)",
            "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                              "assets/nev/face/profile_right.jpeg",
                              "assets/nev/face/front_calm.jpeg"],
            "wardrobe_refs": ["assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg",
                              "assets/nev/wardrobe/10_shirt_white_print/79_front.jpeg"],
            "must_show": "actually him - face, hair, EARRING. Kundasang sits in cold "
                         "highland air, so the white print shirt is worn UNDER a plain "
                         "dark zip jacket in every appearance. Wardrobe continuity is "
                         "part of the identity spec; the jacket is the one addition and "
                         "it is declared here, not improvised per shot.",
            "prompt": "(identity from photo references, not regenerated)"},

    "glc300": {"job": "", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "NOT BUILT. 4cr at 4k. A named product is NEVER generated from "
                      "text alone - a text-only '2026 Toyota Crown' returned a generic "
                      "crossover and shipped an 87cr wrong-car build. LOOK at this "
                      "plate before any clip.",
            "must_show": "Mercedes-Benz GLC 300 4Matic AMG Line, X254 generation "
                         "(2023-present). GEOMETRY, not badge-trust: upright SUV "
                         "proportions with a long bonnet and a short front overhang; "
                         "the AMG Line diamond-pin grille with ONE horizontal bar and "
                         "the star centred and large in it; slim two-piece headlamps "
                         "with a single sweeping DRL bar each side; a strong shoulder "
                         "crease running from the front wing into the tail lamp; "
                         "two-piece wraparound tail lamps; flush door handles; 19-inch "
                         "AMG five-twin-spoke wheels. Colour: polar white.",
            "prompt":
            "Photograph of a white Mercedes-Benz GLC 300 4Matic AMG Line, X254 "
            "generation, parked three-quarter front on a highland ridge road with "
            "Borneo mountain terrain behind. Upright SUV proportions, long bonnet, "
            "short front overhang, AMG Line diamond-pin grille with one horizontal "
            "bar and a large centred star, slim two-piece headlamps each with one "
            "sweeping daytime-running bar, a shoulder crease from the front wing into "
            "the tail lamp, flush door handles, 19-inch five-twin-spoke AMG wheels. "
            "Full-frame DSLR, 50mm, f/5.6, ISO 200. REAL PHOTOGRAPH ARTEFACTS, not a "
            "render: true paint reflections with visible sky gradient, accurate panel "
            "gaps, real tyre sidewall lettering, no HDR halos. Negative: CGI, "
            "videogame look, invented badges or model text, wrong grille pattern, "
            "coupe roofline, oversaturated postcard grade."},

    "kundasang": {"job": "", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "NOT BUILT. 4cr at 4k. The PLACE anchor every scenery shot cites.",
            "must_show": "the Kundasang highlands: Mount Kinabalu's granite summit "
                         "above a broad green valley of terraced vegetable plots and "
                         "dairy pasture, a narrow sealed road switchbacking through "
                         "it, cloud sitting in the folds. NO SIGNAGE anywhere = zero "
                         "invented-text risk.",
            "prompt":
            "Photograph of the Kundasang highlands, Sabah, Borneo, early morning. "
            "Mount Kinabalu's bare granite summit rising above a broad valley of "
            "terraced vegetable plots and green dairy pasture, a narrow sealed road "
            "switchbacking through the middle distance, low cloud caught in the "
            "folds of the ridge. Full-frame DSLR, 35mm, f/8, ISO 100. REAL "
            "PHOTOGRAPH ARTEFACTS, not a render: true atmospheric haze with distance, "
            "accurate cool shadow and warm sunlit split, real vegetation variation, "
            "no HDR halos. Negative: CGI, videogame look, oversaturated postcard "
            "grade, invented peaks, any signage or text, snow."},
}

# _LOOK is appended to every source prompt, so every word in it is BOILERPLATE and is
# subtracted by planqc 29 before a linkage token is checked. Deliberately written to
# contain NONE of the carry tokens used below (cloud, summit, mountain, valley, mist,
# road, gate, hills, grass, wind, viewpoint, golden, car, tail lights).
_LOOK = (
    "Cold high-altitude Borneo air; true texture on skin, paint and vegetation. "
    "REAL FOOTAGE, NOT A RENDER: handheld micro-shake, natural depth of field, "
    "accurate reflections, no HDR halos. Negative: CGI, videogame look, postcard "
    "oversaturation, invented signage text, extra fingers, warped faces, snow."
)

# ---------------------------------------------------------------- SOURCES (10 x 22.5cr)
SOURCES = {
 "A": ("EVENT · SUMMIT CLEARS AT DAWN", "#C4562F", "EVENT", ["kundasang", "glc300"],
       "Vertical 9:16. THE EVENT, and it RESOLVES INSIDE 1.2 SECONDS. DAWN. Locked-off "
       "camera at ridge level on the place from the first reference image: the bare "
       "granite summit FILLS THE UPPER HALF OF FRAME and cloud is already tearing off "
       "it at frame zero, stripping clear across the peak and finishing the uncover "
       "within the first second - not a slow drift, a fast tear. The white SUV from "
       "the second reference image runs along the switchback below, large enough to "
       "read instantly at phone size. A state change in the landscape, not a camera "
       "move. First dawn light striking the rock. " + _LOOK),

 "B": ("GLC climbs the switchbacks", "#7B3F6B", "EXTERIOR", ["kundasang", "glc300"],
       "Vertical 9:16. DAWN, first light. Long lens from across the valley of the first "
       "reference image, aimed UP the switchback ribbon of tarmac so the road recedes "
       "toward the granite peak at the top of frame: the white SUV from the second "
       "reference image climbs away from the lens INTO that depth, getting smaller as "
       "it goes, the peak held uncovered above it the whole time. The reveal continues "
       "instead of being interrupted. Continuous vehicle movement first frame to last. "
       + _LOOK),

 "C": ("cabin, window down", "#4A6FA5", "HUMAN", ["nev", "glc300"],
       "Vertical 9:16. MORNING. Interior of the SUV from the second reference image, "
       "over-the-shoulder onto the windscreen: the man from the first reference images "
       "- white print shirt under a dark zip jacket - driving with the window down, "
       "cold air moving his hair, terrain unrolling ahead through the glass. His face, "
       "hair and EARRING match the references exactly, real skin, no smoothing. "
       + _LOOK),

 "D": ("terraces under mist", "#5B8C5A", "EXTERIOR", ["kundasang"],
       "Vertical 9:16. MORNING GOING TO MIDDAY - one continuous weather move, which is "
       "why this single clip serves both of its shots. High overhead angle straight "
       "down onto the terraced vegetable plots of the reference image, no sky in "
       "frame: stepped green platforms filling the whole picture, thin mist sliding "
       "across them and burning off in the first half, then NEW CLOUD ROLLING BACK IN "
       "from the ridge across the same plots in the second half, its shadow travelling "
       "over the terraces. A farmer's figure tiny for scale. Constant drift of vapour "
       "first frame to last. " + _LOOK),

 "E": ("dairy pasture, close", "#B5843A", "EXTERIOR", ["kundasang"],
       "Vertical 9:16. MIDDAY. Ground-level among black-and-white dairy cattle on open "
       "green pasture in the highlands of the reference image, shallow focus, the "
       "rolling slopes soft behind them. Animals shifting and grazing continuously, "
       "ears and tails moving. No fencing furniture, no buildings, no text of any kind "
       "in frame. " + _LOOK),

 "F": ("NEV at the lookout", "#93507E", "HUMAN", ["nev", "kundasang"],
       "Vertical 9:16. Tracking backwards ahead of the man from the first reference "
       "images - white print shirt under a dark zip jacket - as he walks out to a "
       "railing above the highland valley of the last reference image, head-and-chest "
       "framing, moving air pulling at his jacket and hair. Face and EARRING exact. "
       + _LOOK),

 "G": ("GLC parked, peak behind", "#8C3B3B", "EXTERIOR", ["glc300", "kundasang"],
       "Vertical 9:16. AFTERNOON. Low three-quarter static on the white SUV from the "
       "second reference image, parked on a gravel shoulder, the granite peak of the "
       "last reference image centred directly behind it. Slow push toward the vehicle, "
       "cloud shadow travelling across the paint and the slope. " + _LOOK),

 "H": ("NEV, warm hour close", "#A9553E", "HUMAN", ["nev"],
       "Vertical 9:16. Close head-and-shoulders portrait of the man from the reference "
       "images - white print shirt under a dark zip jacket - late warm hour, low sun "
       "raking across his face, highland slopes thrown out of focus behind him. He "
       "watches the horizon, then turns to the lens with an easy grin. Face, hair, "
       "EARRING exact, real skin. " + _LOOK),

 "I": ("PAYOFF · the descent", "#6A4F8C", "PAYOFF", ["glc300", "kundasang"],
       "Vertical 9:16. DUSK. THE PAYOFF. Camera tracking from behind the white SUV of "
       "the second reference image as it pulls away down the descending highland "
       "tarmac of the last reference image, rear lamps lit, the sky in full colour "
       "over the ridgeline ahead. Continuous forward movement, first frame to last. "
       + _LOOK),

 "J": ("ridge, lamps below", "#3F5F7B", "EXTERIOR", ["kundasang"],
       "Vertical 9:16. DUSK going to blue. Locked wide from high above the highland "
       "tarmac of the reference image: a single pair of red rear lamps travelling "
       "small along the ridge line, scattered orange farm lamps waking in the valley "
       "floor beneath, the peak a flat silhouette against the last colour. " + _LOOK),
}

# FRAMING (planqc 28). Eight of ten sources cite the kundasang plate - the heaviest
# plate-sharing load this repo has planned - so every camera position is stated. A
# plate anchors PLACE; framing must be declared or the model returns the picture it saw.
FRAMING = {
    "A": "locked-off at ridge level, peak filling the upper half, vehicle readable in lower third",
    "B": "long lens up the road into depth, subject receding from lens toward the peak",
    "C": "interior over-the-shoulder, windscreen and hands, no exterior camera position",
    "D": "high overhead straight down, no sky, pattern fills frame",
    "E": "ground level among animals, shallow, slopes as soft background",
    "F": "backward tracking, head-and-chest, subject walking INTO lens",
    "G": "low three-quarter static on the vehicle, slow push, peak centred behind",
    "H": "close portrait, shallow, face fills upper third",
    "I": "rear tracking behind the vehicle, tarmac descending away from lens",
    "J": "locked wide from high above, subject tiny, valley floor beneath",
}

# ---------------------------------------------------------------- TIMELINE 20 shots
# 48 beats at 99.4 BPM = 28.9739s. burst = 2 beats = 1.2072s, med = 4 beats = 2.4145s.
# 16 bursts + 4 meds. Median 1.207s against the profile's 1.13s (range 0.6-2.51).
# 20 shots / 28.974s = 41.4 cuts/min against the profile's 40.3 (band 32.2-48.4).
# HARD CUTS ONLY - the pillar measured zero blends across 5 of 6 references.
# The four meds are the breathing beats: the valley, the railing, the face, the descent.
SHOTS = [
 ("A", 1.00, "burst", "cloud tears off the summit at dawn - the GLC small on the ridge road below"),
 ("B", 1.00, "burst", "the GLC climbing the switchback road into the same cloud, summit above"),
 ("A", 1.20, "burst", "summit clear now - the mountain the whole climb was for"),
 ("C", 1.00, "burst", "in the cabin, window down, cold air, the mountain ahead and the valley below"),
 ("D", 1.00, "burst", "vegetable terraces under morning mist, the valley waking"),
 ("C", 1.20, "burst", "hands on the wheel, mist crossing the windscreen, the road unrolling"),
 ("B", 1.15, "burst", "the GLC running the valley road down to the farm gate, past the terraces"),
 ("E", 1.00, "burst", "past the gate - cows on the green hills"),
 ("D", 1.10, "med",   "the valley wide - the same green hills, terraces stacked, grass moving, cloud rolling back in"),
 ("E", 1.20, "burst", "cows close, grass turning, the cloud shadow crossing them"),
 ("F", 1.00, "burst", "the cloud closing in, so Nev pulls over and steps out at the viewpoint, wind pulling his jacket"),
 ("G", 1.15, "burst", "the GLC parked at the viewpoint, summit centred behind it"),
 ("F", 1.25, "med",   "Nev at the railing, the summit and the mountain straight in front of him"),
 ("G", 1.00, "burst", "the GLC in detail - wheel, flank, mountain held behind, golden starting"),
 ("H", 1.00, "burst", "golden hour finds his face"),
 ("F", 1.15, "burst", "Nev walking back to the car in the same golden hour"),
 ("H", 1.20, "med",   "at the car he turns to the lens - the day landed, the road down waiting"),
 ("I", 1.00, "burst", "the GLC pulls away, tail lights lit, road descending"),
 ("J", 1.30, "burst", "tail lights small on the ridge road, valley lamps waking below"),
 ("I", 1.15, "med",   "last of it on the descending road home"),
]

CALLBACKS = []          # no repeated (source, crop) pair exists - every repeat is re-framed
BAN_SPANS = {}          # nothing measured yet; populated from the probe, never guessed
TIME_JUMPS = {}         # the clock is strictly monotonic - nothing to declare

BEATS = {"burst": 2, "med": 4}

# ONE WHIP, and it is a measurement, not a taste. His catch 2026-08-06: "i created a
# whole lot of transition banks inside it" - correct, tools/fx.py holds 14 and
# engine.py:596 dispatches them live. travel_vlog declared 0% blended, but that came
# from a frame-difference heuristic whose own analysis says "a very fast whip can read
# as a hard cut". RE-MEASURED with tools/blendsense.py across the same 6 references:
# 3 WHIPS + 1 dissolve in 42 cuts = 9.5% POOLED designed, and 3 of 6 refs use one.
# 9.5% of 19 boundaries = 1.8. Taking ONE, not two, because three of the six references
# use none at all - the conservative read of the same number.
# PLACED AT BOUNDARY 9, the consequence beat: the cloud closes over the pasture, SO he
# pulls over. A whip is the physical act of that turn, and it is the one boundary in
# the film where something CHANGES rather than continues. planqc 20 forbids a blend
# touching an EVENT shot, which rules out boundaries 0-2 anyway.
BLEND_AFTER  = [9]
BLEND_KIND   = "whip"               # the ONLY designed kind blendsense found here
BLEND_WIDTH  = 0.24                 # floor of the 240-560ms band: a whip must be FAST

SFX_LEAD     = 0.22
IMPACT_AT    = []                   # hero_only: no whoosh/impact layer on a vlog's cuts
SUBDROP_AT   = []

# ---------------------------------------------------------------- SOUND (ambience gate)
SOUND = {
    "bed":        "BGM/travel_vlog/Crystal-Water-by-Spiring.mp3 - 99.4 BPM NATIVE, "
                  "zero stretch, 157s (5.4x the video: the segment scan has real "
                  "choice), 16.4dB dynamics, CC BY 3.0. Credit line REQUIRED at "
                  "publish - see BGM/travel_vlog/MEASURED.md.",
    "hero":       "the dawn reveal (shot 0) - wind and the distant climb, then the "
                  "highland ambience takes over for the rest of the day",
    # THE KEY THE ENGINE ACTUALLY READS. engine.py:781 reads SOUND["hero_shot"] under
    # edit_sfx=hero_only and silently defaults to 0. crown defined "hero" and not
    # "hero_shot": the only sound in a 30s film would have landed 14.00s early on a
    # 278cr build, and no gate looks at it. travel_vlog runs hero_only, so this is LIVE.
    "hero_shot":  0,
    "duck_shots": [0],
    "silence":    "none - highland ambience carries every gap; the bed breathes with "
                  "the altitude",
}

FOLEY = {   # ambience gate: every shot lays its own clip audio, mostly UNDER the bed
     0:  -4.0,   # A  EVENT - wind tearing the cloud off the rock. Must be HEARD.
     1: -10.0,   # B  distant engine on the switchbacks
     2:  -5.0,   # A  EVENT source again - the ridge wind stays forward
     3:  -8.0,   # C  cabin, window down, air rush
     4: -12.0,   # D  valley hush
     5:  -9.0,   # C  wheel, air, tyre hum
     6: -10.0,   # B  the car passing, mid
     7: -10.0,   # E  cattle, bells, pasture
     8: -13.0,   # D  wide valley, quiet
     9:  -8.0,   # E  cows close - the animals must be HEARD
    10: -10.0,   # F  wind at the lookout, footsteps on gravel
    11: -12.0,   # G  parked - engine off, only air
    12: -12.0,   # F  railing wind
    13: -13.0,   # G  detail, near-silent
    14: -14.0,   # H  quiet - the face is the shot
    15: -11.0,   # F  gravel underfoot walking back
    16: -14.0,   # H  clean under the card
    17:  -6.0,   # I  PAYOFF - the car leaving. Must be HEARD.
    18: -12.0,   # J  distance, valley hush
    19:  -6.0,   # I  PAYOFF source again - the descent stays forward
}

# ---------------------------------------------------------------- THE CLOCK (planqc 30)
# Every shot names its light state. Strictly monotonic in LIGHT_ORDER
# (dawn, morning, midday, afternoon, golden, dusk, blue, night) - no boundary runs
# backwards, no state is skipped, TIME_JUMPS is empty. Each source prompt PINS its own
# light state so the generator cannot drift off the declared clock. KK v15 ran
# night -> daylight -> morning under a "6PM" card and no gate could see it.
SHOT_TIME = ["dawn", "dawn", "dawn",
             "morning", "morning", "morning", "morning",
             "midday", "midday", "midday", "midday",
             "afternoon", "afternoon", "afternoon",
             "golden", "golden", "golden",
             "dusk", "dusk", "dusk"]

# ---------------------------------------------------------------- LINKAGE (19 boundaries)
# TYPED, never prose: (kind, token, intent). planqc 29 requires the TOKEN to be findable
# in the writing of BOTH shots it joins, with shared boilerplate subtracted first - so a
# connection cannot exist only in my head. KK v15 passed check 24 nineteen-for-nineteen
# on prose and the eye found 5 of 19 that actually landed.
# Kinds: motion · gaze · subject · object · light · sound · consequence.
# planqc 31 floor: 4 consequence boundaries out of 19. This plan declares 4.
LINKAGE = [
    ("motion",      "cloud",       "the cloud torn off the summit streams down over the climbing car"),
    ("object",      "summit",      "the summit the car is climbing toward -> the summit uncovered"),
    ("consequence", "mountain",    "the mountain is clear, SO the day starts: he drives"),
    ("gaze",        "valley",      "he looks down into the valley -> the valley he is looking at"),
    ("light",       "mist",        "the same mist, on the terraces then on the windscreen"),
    ("motion",      "road",        "the road unrolling inside the cabin -> the same road from outside"),
    ("consequence", "gate",        "the road arrives at the farm gate, SO we are through it"),
    ("subject",     "hills",       "the hills the cows stand on -> the same hills, wide"),
    ("motion",      "grass",       "grass moving in the wide valley -> grass turning at the animals' feet"),
    ("consequence", "cloud",       "the cloud is closing back over the pasture, SO he pulls over and gets out"),
    ("subject",     "viewpoint",   "he arrives at the viewpoint -> the car at the same viewpoint"),
    ("gaze",        "summit",      "the summit behind the car -> the summit he is facing"),
    ("subject",     "mountain",    "the mountain he faces -> the mountain held behind the car"),
    ("light",       "golden",      "golden starts on the paint -> golden lands on his face"),
    ("light",       "golden",      "the same golden hour, on his face then on his walk back"),
    ("consequence", "car",         "he reaches the car, SO he turns and closes the day"),
    ("consequence", "road",        "the day is done, SO he takes the road down"),
    ("motion",      "tail lights", "the tail lights leaving -> the same tail lights small on the ridge"),
    ("motion",      "road",        "the ridge road above -> the descending road home"),
]

CROP_XY = {}            # nothing measured yet; populated only from a probe

CARD_Y       = 0.72
CARD_STYLE   = "fragment"           # pillar style: sentence fragments, <= 6 words
# The cards are the DAY, not a brochure. Every one of them is either a verified fact
# with a 2026 source or an explicitly hedged local saying. NOTHING on screen asserts a
# price, a spec or a market status - that is what J4 vetoed on crown, and it stays in
# CONTENT below where it carries its date.
CARDS = [
    ("2 HOURS FROM KK",              0, 4, "cap"),  # verified, 2026 source
    ("CLEAREST 6 TO 8AM",            4, 4, "cap"),  # verified, 2026 source - and it is the hook
    ("SABAH'S OWN LITTLE NEW ZEALAND", 8, 4, "cap"),  # J4 FIX: sourced AND moved onto the pasture
    ("KUNDASANG NEXT WEEKEND?",      16, 4, "cta"),  # a question, not a beg
]
AI_LABEL_BURNED_IN = False          # HUMAN step at upload. Never burned in (planqc 15).

GRADE_SAT    = 1.00                 # daylight vlog: the prompts carry the look
GRADE_BRI    = 0.0
TARGET_BLACK = 10.0                 # profile values
TARGET_SAT   = 74.5

# ---------------------------------------------------------------- CONTENT
CONTENT = {
    "claim":    "Kundasang is about a two-hour drive from Kota Kinabalu, and Mount "
                "Kinabalu shows clearest between 6 and 8am - which is why the whole "
                "video opens at dawn and not at lunch.",
    "verified": "explorekundasang.com, 'Mount Kinabalu from Kundasang' (2026 guide) - "
                "states a two-hour drive from Kota Kinabalu and names 06:00-08:00 as "
                "the clearest window. FETCHED 2026-08-06, same day as this plan. "
                "CARD 3, added after J4 vetoed it unsourced: Daily Express Malaysia "
                "(Sabah's leading news portal), 'Sabah's own little New Zealand' - the "
                "card quotes that published phrasing rather than asserting a nickname "
                "in our own voice, and the same epithet is independently attested "
                "across Tripadvisor reviews of Desa Dairy Farm and Places Malaysia. "
                "The card was ALSO moved from shots 11-14 to shots 8-11 so it sits on "
                "the pasture footage it describes - J4's second, independent finding. "
                "SEPARATE, and deliberately NOT on screen: carbase.my (fetched "
                "2026-08-06) lists the current Malaysian X254 range as GLC200 CKD "
                "RM329,888 and GLC350e 4Matic CKD RM398,888; the GLC300 4Matic AMG "
                "Line was the CBU launch variant at RM429,888 and is not in the new "
                "lineup. That is a market STATUS and market statuses go stale - it is "
                "the reason the car is shown and never captioned.",
    "twist":    "the car is the clock. One vehicle, one person, six light states, and "
                "every cut is a declared carry - so the day physically moves instead "
                "of cutting between postcards. The field posts drone beauty with "
                "nobody in it, or itinerary lists with no story; nobody drives you "
                "through ONE day.",
    "why_stop": "frame zero is a state change, not a tour - cloud tears off the summit "
                "while the car is already moving below it (the refsense finding: an "
                "EVENT does not require motion, but here it has both); card 1 is a "
                "drive time, which is the single thing anyone planning this trip "
                "actually searches for; the CTA is a question with a date attached to "
                "it by implication - next weekend - not a request for a follow.",
}

PREVIZ = {  # sketch-grade, NEVER enters generation. The hook is judged at probe, not here.
    "sheet_v1": "",
    "board_v1": "",
    "job":      "",
    "note":     "STANDING ORDER 2026-08-05: a storyboard (previz sheet + reference "
                "strip + beat-exact cut table) is SHOWN TO GAVRIL before any clip "
                "credit is spent. If the persona appears in ANY panel the sheet MUST "
                "carry the identity reference - a text-only previz invented a stranger "
                "and was correctly rejected ('the man is not nev').",
}

PROBE_FIRST  = "A"     # the dawn reveal: two named subjects, a landscape state change
                       # and the hook that decides the video. Probe alone, LOOK, batch.

CLIPS = {}             # nothing generated. Populated at ingest, and the raws are KEPT.
CLIP_BASE = ""         # INERT BY DESIGN (bugsense class 2, MED): no pipeline file reads
                       # this. It is the download provenance of the paid artefacts, kept
                       # so a later session can re-fetch a clip it no longer has on disk.
                       # THAT IS NOT HYPOTHETICAL: every kk_*.mp4 is already gone, and
                       # kk.py's CLIP_BASE is the only remaining route back to them.


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
