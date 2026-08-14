#!/usr/bin/env python3
"""
MAHUA_PLAN — "NEV · DAY TRIP TO MAHUA WATERFALL, TAMBUNAN", the THIRD travel_vlog.
Title readback resolved 2026-08-07 (his four picks, all four the recommended option):

  "Mahua Waterfall, Tambunan" -> Crocker Range Park, Mahua substation. Sabah.
  "30 second video"  -> 28.97s = 48 beats at 99.4 BPM. HIS PICK. The measured
                  travel_vlog band is 16-29s from his 6 references; 30.0 sits outside
                  it and planqc 2 blocks it. Same readback class as KK's 45->28.31,
                  the WRX's 30->21.6 and kundasang's 30->28.97.
  hook         -> THE COLD HIT. He picked the cold-water shock at the pool over the
                  waterfall reveal. Material: every Mahua reel on the field opens on
                  the trail-reveal (green tunnel, part the leaves, the falls appear) -
                  a TOUR, and planqc 9 would reject it anyway. Ours opens on the
                  CONSEQUENCE and rewinds. TIME_JUMPS declares the rewind (below).
  car          -> the same GLC 300 as kundasang. HIS PICK. A KOL keeps one car; the
                  plate is planned-but-unbuilt on kundasang, so the 4cr spent here
                  serves both films.
  kundasang    -> QUEUES BEHIND this build. HIS PICK. That plan stays gated at 34/34
                  and untouched; nothing here edits it.
  "720p"       -> his words. std, never fast (planqc 15).
  bed          -> Easy-Love by Hotham, 99.4 BPM NATIVE, ZERO stretch, 15.5dB dynamics,
                  199s, CC BY 3.0 (BGM/travel_vlog/MEASURED.md). NOT Crystal-Water:
                  that bed is kundasang's, and two Sabah vlogs must not share a track.
                  199s = 6.9x the video, the widest segment choice in the usable bank.
                  The bed chose the tempo, never the reverse.

FIELD SCAN (Phase 0, 2026-08-07): Mahua content is a trail-reveal genre. Instagram and
YouTube posts for this exact waterfall walk the 500m concrete walkway, part the green,
and land on the 17m curtain - the money shot arrives at 8-15 seconds. THE UPGRADE vs
the field: the money shot is spent at frame zero as a BODY EVENT (cold water taking
him), and the rest of the film is the day that earned it, told forward. Nobody in this
subject's field opens on the consequence.

VERIFIED FACTS (fetched 2026-08-07, both sources in CONTENT below):
  17m fall into a 1.3m pool · Crocker Range Park 139,919ha, Mahua substation at 1,000m
  · 8am-5pm daily · ~1.5h drive from Kota Kinabalu · 500m flat concrete trail
  · water around 23C.
The gate closing at 5pm is why this film ends in GOLDEN and has no dusk state. The
clock is bounded by a published opening hour, not by taste.

STATUS 2026-08-07: GENERATED. 3 plates + 9 clips built, 214.50cr MEASURED spend
(4927.82 -> 4713.32), zero failures. NOT YET CUT - the build runs on his Windows box
(the remote sandbox cannot reach the CDN the clips live on). See RESUME-2026-08-07.md.
"""

PROJECT   = "NEV AT MAHUA WATERFALL · travel vlog · day trip · Tambunan"
PILLAR    = "travel_vlog"
GEN_MODE  = "coverage"               # INERT BY DESIGN (bugsense class 2, MED): engine.py
                                     # does not read this. Declared so the next session
                                     # can tell deliberate from forgotten.
BPM       = 99.4                     # = Easy-Love's MEASURED native tempo. Zero stretch.
BEAT      = 60.0 / BPM               # 0.603622s
W, H, FPS = 720, 1280, 30
MODE      = "std"
RES       = "720p"
CLIP_S    = 5
MAX_CROP  = 1.40
TARGET_S  = 28.97                    # 48 beats = 28.9739s. Band-top of the measured 16-29s.

LESSONS_ACK = {            # ledger counts this plan was written against (planqc 23)
    "general craft": 116,  # pillar-INDEPENDENT: measurement, tooling, process
    "travel vlog":    6,   # this pillar's GENRE lessons
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
# RE-ACKED 2026-08-11 after reading craft L96-L114 and travel vlog L5 - all filed
# 2026-08-08 from the desafarm v2 rejection. The two that BITE this build directly:
# tv L5 (the whip that shortened the timeline - mahua declares the same 240ms whip
# after shot 4; the engine now RESERVES the overlap by contract and planqc 34 reads
# engine.BLEND_RESERVES_OVERLAP, one mechanism) and craft L102 (mid-action became a
# HARD gate - every window that ends above 80% of its own action peak is refused,
# which protects the cold-water hook this film opens on). L107's card clock: this
# plan's four card spans (0-3, 8-11, 12-15, 16-19) are disjoint by construction.
# RE-ACKED TWICE on 2026-08-07: 77->78 and 3->4 after judge round 1, then 78->81 after
# judge round 2, 81->83 after round 3, 83->84 after round 4, and 84->92 / 4->5 after HE
# LOOKED AT THE FOOTAGE on 2026-08-07 and nine more lessons were filed from what his
# eye caught that four judge rounds on prose did not. All SEVEN new lessons are THIS PLAN'S OWN
# failures, filed automatically by tools/lessonize.py from the round-1 judge panel:
# J4's veto on the drive-time card and J2's refusal of four of five declared
# consequences. planqc 23 BLOCKED this file until the ack matched - the loop working,
# not a nuisance. The last two PREMORTEM entries are the evidence that they were read.
# READ, not just counted: craft L64-L77 (the J4 card veto, board.py's 9-source ceiling,
# the destroyed KK raws, the sound-layer contract, the omitted review page, the
# whip-blind detector, the percent-quantised blend band, the two-pillar mix measurement,
# the Linux-only font, the four-failures-one-glob smoketest, the backslash filter path,
# the 1-of-28 doctrine gap) and travel vlog L0-L2 (bed band mismatch, per-BPM beat math,
# the free-music genre trough). Each one that can touch THIS build is a PREMORTEM entry
# below with its mitigation; the ack is the claim, the premortem is the evidence.

PREMORTEM = [
    ("beat-grid math copied across BPMs turns bursts into the wrong length "
     "(travel vlog L1: BEATS={burst:2,med:4} carried from a 150 BPM car plan into a "
     "105 BPM vlog, where a 'med' hook is 2.29s and FAILS planqc 9's 2.00s rule)",
     "BEATS recomputed AT 99.4: burst = 2 beats = 1.2072s, med = 4 beats = 2.4145s. "
     "16 bursts + 4 meds = 48 beats = 28.9739s and TARGET_S is set FROM that arithmetic, "
     "never typed. The hook is a BURST at 1.21s, half the 2.00s ceiling. Median shot "
     "1.207s against the profile's 1.13s (range 0.6-2.51)."),

    ("a wrong-tempo or wrong-genre bed reaches the build (travel vlog L0: the 25-track "
     "BGM library is 140-165 BPM drift phonk, the wrong pillar entirely; travel vlog L2: "
     "the free-vlog-music market clusters at 90-99 and 117-140, and 95-115 is the TROUGH "
     "between them)",
     "bed pinned to BGM/travel_vlog/Easy-Love-by-Hotham.mp3 - 99.4 BPM NATIVE, ZERO "
     "stretch, 15.5dB dynamics, 199s, CC BY 3.0, from the 14 tracks MEASURED usable in "
     "BGM/travel_vlog/MEASURED.md. Plan BPM is set FROM the bed. "
     "engine.verify_bed_tempo REFUSES a mismatch at build. Deliberately NOT "
     "Crystal-Water: that is kundasang's bed and these two films must not sound alike."),

    ("the clock runs backwards and no gate can see it (travel vlog / craft L60: KK v15 "
     "ran golden -> night -> DAYLIGHT -> sunset -> morning under a '6PM IN KK BAH' card, "
     "which is why planqc 30 exists)",
     "SHOT_TIME is declared per shot: midday(1, the cold open) then dawn(3) -> "
     "morning(4) -> midday(4) -> afternoon(4) -> golden(4), strictly monotonic from shot "
     "1 onward. The ONE backwards boundary is boundary 0 and it is DECLARED in "
     "TIME_JUMPS with its reason - a declared jump is a choice, an undeclared one is the "
     "bug. There is no dusk state because the park GATE SHUTS AT 5PM (Sabah Parks, "
     "fetched 2026-08-07): the clock is bounded by a published fact."),

    ("a plate anchors PLACE and silently anchors FRAMING too, so sources collapse into "
     "one image (craft: KK P1 - A, C, E and I all cited the waterfront plate and five "
     "shots were one picture; planqc 28 was built from it)",
     "FIVE of nine sources cite the mahua plate - A, D, E, F, G - which is a heavier "
     "single-plate load than kundasang's four. Every one declares a distinct camera "
     "position in FRAMING: water level, walkway level, cross-gorge long lens, "
     "ground-level at the pool, and handheld behind a raised arm. planqc 28 blocks a "
     "repeat within a plate group."),

    ("invented on-screen text - J4 holds an ABSOLUTE veto (craft, lesson 35: an invented "
     "'SR' badge shipped through 8 builds; KK P4 cost 22.5cr on 'SDNMONES' signage)",
     "FOUR text surfaces exist in this film and all four are handled pre-spend - the "
     "count went 2 -> 3 -> 4 across three judge rounds, which is the point of running "
     "them. (1) PARK SIGNAGE: every prompt frames trail, gorge, water and rock with no "
     "gate furniture, no interpretive boards, no shopfronts. (2) THE PHONE SCREEN, new "
     "to this plan because he asked for selfies and recording: 'legible device screens' "
     "is in the negative block of every prompt and source G is written so the phone is "
     "seen from BEHIND with its blank back to lens. (3) THE VEHICLE - registration "
     "plate, model badge, tyre lettering - which J4 found living only on the SOURCE "
     "prompts and NOT on the plate they all cite (round 2). (4) THE GARMENT: the "
     "persona wears a 'white PRINT shirt' and a print is a text surface - J4 round 3 "
     "caught that nothing banned legible words inside it, on the hook shot's chest, "
     "centre frame at frame zero. _LOOK now bans clothing wordmarks and instrument "
     "displays as well. CLIPQC TEXT-ZOOM CROPS ARE READ BY EYE ON ALL NINE CLIPS, not "
     "just the EXTERIOR/EVENT/PAYOFF ones - the HUMAN clips are exactly where surfaces "
     "(2) and (4) live. DELOGO stays EMPTY until a "
     "clip exists - a guessed box is an invented number (planqc 25 checks the box is "
     "in-frame, it cannot check that it is on the right pixels)."),

    ("the hero sound key the engine actually reads is not defined (craft: engine.py:781 "
     "reads SOUND['hero_shot'] under edit_sfx=hero_only and silently defaults to 0; "
     "crown defined 'hero' instead, so the only sound in a 30s film would have played "
     "14.00s early on a 278cr build)",
     "SOUND['hero_shot'] is DEFINED below as an int and it is 0, which is also where the "
     "hero belongs here - the water impact IS the hook. travel_vlog runs "
     "edit_sfx=hero_only so this key is LIVE, not latent. bugsense --class 1 must return "
     "zero findings for plans/mahua.py before any credit moves."),

    ("something that must be HEARD is not in the clip, and no plan field can add it "
     "later (craft L67: SOUND LAYER CONTRACT - engine.py reads FOLEY={shot: gain_db}, "
     "ONE gain on that clip's OWN generated audio, plus one bed and one hero transient. "
     "Three layers, and there is no per-shot sfx stack)",
     "this is a WATER film, so the sound is the whole point and every sound is written "
     "INTO the prompt that pays for it: F names the river over boulders, E names the "
     "curtain hitting the pool, A names the impact and the gasp, D names feet on wet "
     "concrete, B and C name engine and moving air, I names the car leaving. H is "
     "deliberately quiet at -12dB because the face is the shot. Nothing is left to be "
     "'added in the edit' - there is no edit stage that could add it."),

    ("the foley and the hero swamp the bed (craft L72: MEASURED -4.9dB bass duck on KK "
     "v15 but -31.1dB on WRX v9, because foley foreground was hardcoded at bed-2 and the "
     "sidechain at 0.06/6:1 for every pillar alike)",
     "engine.py now reads the five mix relationships from the PILLAR style block; "
     "travel_vlog declares foley foreground at bed-8 and a 3:1 duck at threshold 0.10, "
     "release 180ms. FOUR shots are foreground here and no more: 0 and 10 (the EVENT, "
     "the water taking him) and 17 and 19 (the PAYOFF, the car leaving). planqc 19 "
     "requires exactly those to be >= -6dB. A waterfall bed is BROADBAND and will duck "
     "harder than kundasang's wind did, so the -31.1dB class is live on this build: "
     "MEASURE the bed's 40-160Hz band under shots 8-11 at verify, do not assume."),

    ("a designed transition cannot be declared because the band is a percentage (craft "
     "L70/L71: planqc 11 derived [0,5]% from blended_pct 0, so ONE blend at 19 "
     "boundaries is 5.3% and BLOCKS; and the detector that produced that 0 was blind to "
     "whips - blendsense re-measured 9.5% pooled, all whips)",
     "the pillar declares designed_pct 9.5, designed_kinds ['whip'] and "
     "blend_max_count 2. This plan takes ONE whip, at boundary 4 - the road runs out, SO "
     "he walks in - because 3 of the 6 references use none. A dissolve would now FAIL "
     "the whitelist, correctly. planqc 20 forbids a blend touching an EVENT shot, which "
     "rules out boundaries 9 and 10 (either side of shot 10) and 0 anyway."),

    ("the cards render as NOTHING and every gate stays green (craft L73: engine.py "
     "resolved the drawtext font from two /usr/share/fonts candidates, neither of which "
     "exists on Windows, and ffmpeg does not reliably error on a missing fontfile - no "
     "check reads pixels for text)",
     "engine.py now resolves from 5 candidates with the repo's own CapCutSansText-Bold "
     "FIRST, prints the chosen font and RAISES rather than shipping empty cards. Both "
     "verified facts and the CTA live on cards here, so a silent loss removes the "
     "receipt AND the ask while planqc says 34/34. LOOK at the delivered strip for all "
     "four cards before calling this build finished."),

    ("a card asserts something the CONTENT block never verified, or asserts a number two "
     "sources disagree about (craft L64: J4's ABSOLUTE VETO on kundasang card 3)",
     "the two card facts are the ones BOTH fetched sources agree on: the 17m drop and "
     "the 8am-5pm gate. THE ENTRANCE FEE IS DELIBERATELY OFF SCREEN - sabahparks.org.my "
     "states RM6 for a Malaysian adult and mysabah.com states RM3, and a fee is a "
     "market status that goes stale exactly like the crown's price did. Both figures and "
     "their disagreement are recorded in CONTENT.verified, where they carry a date."),

    ("the raw clips are deleted and a PROVISIONAL threshold can never be re-derived "
     "(craft L66: every kk_*.mp4 is gone, so travel_vlog's motion_floor 0.6 and "
     "brightness_band [35,200] are still PROVISIONAL two builds later)",
     "this build is the second chance at that measurement and a better one: a gorge "
     "is the DARKEST place this pillar will ever shoot (shots 5-15 sit under canopy at "
     "1,000m) and moving water is the HIGHEST motion. All 9 raws stay on disk until "
     "clipqc's numbers have been used to mark motion_source and brightness_source "
     "MEASURED. CLIP_BASE is filled at ingest and never blanked."),

    ("a shot is rejected at 22.5cr by a car-tuned gate (travel vlog L2 / the open P2-1 "
     "blue-block: the brightness band was widened to [35,200] only after a golden-hour "
     "frame measured 51.3 and would have been wrongly rejected)",
     "the risk here is the OTHER edge and it is structural: deep gorge shade under a "
     "canopy can land BELOW 35 mean luma, and clipqc's brightness check BLOCKS. Sources "
     "D, E, F and G are written to keep sky or bright spray inside the frame so the "
     "histogram has a top. If a raw still measures under 35 it is EVIDENCE the "
     "provisional band is wrong for shade, not automatically a bad clip - measure, show "
     "him the frame, and decide. Do not silently re-generate."),

    ("a linkage exists only in my head (craft L56-L59: KK v15 shipped 19 PROSE linkages "
     "and the eye found 5 that landed; a carry needs a TOKEN findable in BOTH shots' "
     "writing, and the list must be generated from the FINAL shot order)",
     "all 19 boundaries are TYPED (kind, token, prose) and every token is a word written "
     "into BOTH adjacent shot notes - cold, mist, road, river, spray, pool, falls, "
     "phone, walkway, suv, trailhead. planqc 29 subtracts the shared _LOOK boilerplate "
     "first, so a carry cannot be satisfied by a word every prompt contains. The list "
     "was written AFTER the shot order was frozen, boundary by boundary. FIVE "
     "boundaries are consequence against planqc 31's floor of 4."),

    ("the board he approves is not the thing that gets built, or does not render at all "
     "(craft L65: board.py:216 hardcodes a 3x3 legend and IndexErrors at 10 SOURCES - "
     "kundasang cannot board; craft L68: storyboard.py omitted the verbatim prompt, the "
     "identity references and the transitions it was asked to prove)",
     "NINE sources, not ten. That is a PLAN-LEVEL fit to a known pipeline limit rather "
     "than an autonomous edit of a pipeline file - his standing rule - so board.py "
     "renders this plan today and board.py's one-line fix stays HIS call. "
     "tools/storyboard.py carries the verbatim prompts, the identity thumbnails, the "
     "camera chips and the per-boundary transition rows since 2026-08-06, and both go to "
     "the gate presentation."),

    ("the plan is built against the CODE and never against the DOCTRINE the code exists "
     "to enforce (craft L76: the entry path named 1 of 28 doctrine docs, and both skills "
     "predate the 68-check architecture)",
     "before the FINAL BOSS pass on the finished cut, read 27-mastermind-qc.md top to "
     "bottom and use its verdict format. Four of its 16 measurement traps are live on "
     "this build: DELIVERED WINDOW (clipqc measures the centred window, never the clip "
     "head), PLANNED-vs-ACTUAL (the one whip compresses the timeline, so verify against "
     "post-blend boundaries), OPEN-LOOP GAIN (the new per-pillar mix knobs are applied "
     "and must be re-MEASURED, not assumed) and BLUR-AS-BLACK (moving water and wet rock "
     "read as blur to the blank-frame gate). 06-content-judges.md is the seat judge.py "
     "runs; 08-the-strategist.md is the readback that produced this file."),

    ("A NUMBER THAT IS REALLY A RANGE GETS PUT ON A CARD AS A FACT, AND THE CITATION "
     "IS CHECKED LESS CAREFULLY THAN THE NUMBER (general craft, filed 2026-08-07 from "
     "THIS PLAN's round-1 J4 veto: card 1 read '90 MINUTES FROM KK' and CONTENT claimed "
     "two agreeing sources - sabahparks.org.my in fact states no drive time at all, and "
     "the 1.5h figure was one source's low end of a 1.5-2h range)",
     "the card now reads ABOUT 2 HOURS FROM KK - a hedge plus the upper bound, which no "
     "fetched source contradicts - and CONTENT.verified now states per-fact WHICH source "
     "carries it, names the range, and records the second disagreement J4 surfaced (the "
     "Tambunan leg: 14km on sabahparks vs 26km on mysabah), which is why no distance "
     "appears on screen at all. STANDING RULE FROM THIS: before a card ships, name the "
     "source for THAT card, not for the CONTENT block."),

    ("THE WORD 'SO' IN A LINKAGE IS NOT A CAUSE, AND FOUR OF FIVE WILL BE LOCOMOTION "
     "DRESSED UP (travel vlog, filed 2026-08-07 from THIS PLAN's round-1 J2 fail: 0->1 "
     "was an editorial rewind, 4->5 asserted a parking that appeared in no shot, 14->15 "
     "and 15->16 were 'he finished, so he left' - and shots 11-16 held one unchanged "
     "state for 7.2s)",
     "the four surviving consequences are each grounded in something ON SCREEN: 4 (the "
     "sealed road ENDS in D's first frames, so the car is left), 9 (the pool is waist "
     "deep, so he gets in), 11 (he is standing under the falls, so the phone comes up) "
     "and 14 (23C water has beaten him - G now shows shoulders drawn up and jaw set - so "
     "the phone goes down). The two that were locomotion are relabelled subject carries. "
     "TEST TO APPLY NEXT TIME: if the cause is not visible in the WRITING of the shot "
     "before the boundary, it is not a consequence, whatever the prose says."),

    ("THE PLAN'S TEXT BANS LIVE ON THE CLIPS AND NOT ON THE PLATE THAT EVERY CLIP CITES "
     "(general craft, filed 2026-08-07 from THIS PLAN's round-2 J4 fail: _LOOK is "
     "appended to all nine SOURCES and to NO PLATE prompt. The glc300 plate was framed "
     "three-quarter FRONT - the one angle that puts a number plate dead centre - and "
     "ASKED for 'real tyre sidewall lettering'. An invented Malaysian plate string would "
     "have been baked into the 4cr reference image and carried as image_reference into "
     "six shots. planqc's plate check tests resolution and existence, nothing else, so "
     "no mechanical gate could ever have caught it - the lesson-35 badge mechanism one "
     "level upstream of where lesson 35 put the guard)",
     "the glc300 plate now states an EMPTY plate recess in the positive prompt and bans "
     "registration plates, plate lettering, dealer stickers, model badge text and tyre "
     "brand lettering in its own negative block; 'real tyre sidewall lettering' is "
     "deleted. The mahua and crocker plates already banned 'any signage or text'. "
     "STANDING RULE FROM THIS: a plate prompt is a GENERATION prompt and gets the same "
     "negative discipline as a shot - LOOK at every rendered plate for lettering before "
     "it is passed as a reference to anything."),

    ("A DECISION BEAT IS SPENT ON THE MOST INERT IMAGE IN THE FILM (general craft, filed "
     "2026-08-07 from THIS PLAN's round-2 J0 fail: the hook resolved at ~0.4s and then "
     "shot 1 handed 1.21-2.41s - the rest of the window that decides the scroll - to a "
     "long-lens valley establisher with the car receding from the lens)",
     "shots 1 and 2 are swapped: the cabin (a face, near-field mist, window down) now "
     "holds the second half of the 2s window and the valley long-lens moves to shot 2, "
     "where it is a breath and not a decision. The 0->1 'cold' linkage token survived "
     "the swap unchanged. TEST TO APPLY NEXT TIME: judge the SECOND second, not just "
     "frame zero - a hook that resolves at 0.4s still has 1.6s of window to lose."),

    ("A SOURCE IS DEFINED AS A PLACE INSTEAD OF AS A CHANGE, SO EVERY EXTRA WINDOW OF IT "
     "IS THE SAME PICTURE AGAIN (general craft, from THIS PLAN's round-3 J2 fail: shots "
     "16-19 held 7.2s - a QUARTER of the film - as one state, cut four times out of two "
     "clips, with no causal boundary anywhere in the tail. The named fix was a tenth "
     "source, which board.py cannot render)",
     "NO SOURCE WAS ADDED. Source H was REDEFINED: it was a golden portrait that stood "
     "still, and it now performs a monotonic arc - arms crossed and shivering at frame "
     "one, arms down and shaking the water out by the last frame - so shots 16 and 18 "
     "sit at OPPOSITE ENDS of a change instead of being two windows of a constant. "
     "Boundary 15 became a consequence on the same body state that drove him out of the "
     "water, so the tail has a cause in it for the first time. Cost: 0cr, 0 new sources, "
     "board.py untouched. THE GENERAL RULE, and it is the most useful thing this plan "
     "learned: WHEN A SPAN READS FLAT, ASK WHAT THE CLIP DOES, NOT HOW MANY CLIPS THERE "
     "ARE. A plan-level fix beats a pipeline-level fix even when the pipeline fix is "
     "cleaner - his standing rule, and here it also beat the more expensive fix."),

    # ---- added 2026-08-11 at the L96-L115 / tv-L6 re-ack ----
    ("THE DECLARED WHIP SHORTENS THE TIMELINE INSTEAD OF OVERLAPPING IT AND EVERY "
     "LATER CUT SITS EARLY AGAINST THE BED (travel vlog L5, measured on desafarm "
     "v2: 240ms declared, 197ms stolen from the shot, 60% of the film ~170ms off a "
     "bed that kept its own tempo - and every per-shot check passed). This plan "
     "declares the same 240ms whip, after shot 4, on a 48-beat grid that TARGET_S "
     "was computed from",
     "The engine reserves and renders the blend-in shot one blend-width longer - "
     "the blend eats the OVERLAP, never the timeline - and since 2026-08-11 planqc "
     "34 reads engine.BLEND_RESERVES_OVERLAP itself (one mechanism, PENDING 2.3 "
     "closed). verify's beat-grid check runs on post-blend boundaries, so if the "
     "reservation ever regresses the delivered cut fails the grid, not just the "
     "plan gate."),

    ("A SOURCE WITH AN INTERNAL ARC IS DELIVERED IN THE WRONG ORDER AND THE FILM "
     "PLAYS ITS REACTION BEFORE ITS CAUSE (craft L101's shape on source H: the "
     "allocator guarantees non-overlap but never guaranteed ORDER, so the grin "
     "could arrive before the shiver - this plan's own declared open risk 1)",
     "SHOT_WINDOW = {16: 0.20, 18: 3.70} - the additive per-shot pin the risk "
     "asked for, built 2026-08-11 on his go-ahead. Pinned windows allocate first, "
     "a pin that does not fit FAILS the allocation loudly, and syncqc check 5 "
     "(arc order) plus the eye on the delivered strip stay as the second and "
     "third belts."),
]

# ---------------------------------------------------------------- PLATES
PLATES = {
    "nev": {"job": "4c542b39-a06e-42c6-affd-2d6d3c93a392", "res": "4k", "ar": "4:5",
            "cr": 0, "status": "3-angle face set, EXISTS (reused from KK/kundasang)",
            "identity_refs": ["assets/nev/face/front_neutral.jpeg",
                              "assets/nev/face/profile_right.jpeg",
                              "assets/nev/face/front_calm.jpeg"],
            "wardrobe_refs": ["assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg",
                              "assets/nev/wardrobe/10_shirt_white_print/79_front.jpeg"],
            "must_show": "actually him - face, hair, EARRING. This film gets him WET: "
                         "the white print shirt is worn over dark shorts, and from the "
                         "pool onward the shirt and hair are SOAKED and stay soaked for "
                         "the rest of the day. That continuity is declared here, not "
                         "improvised per shot - a dry shirt after the plunge is the "
                         "same class of error as a light state running backwards.",
            "prompt": "(identity from photo references, not regenerated)"},

    "glc300": {"job": "9eb26ccb-11a3-4878-9565-7285dcfc5741", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-07, 5504x3072. OCR CLEAN: RapidOCR at 2048px "
                      "detected ZERO text - no registration plate, no badge lettering, "
                      "no tyre lettering. That is the J4 round-2 risk, MEASURED clear "
                      "rather than eyeballed. Was: 4cr at 4k. Shared with plans/kundasang.py, which "
                      "planned the same plate and never built it. A named product is "
                      "NEVER generated from text alone - a text-only '2026 Toyota Crown' "
                      "returned a generic crossover and shipped an 87cr wrong-car build. "
                      "LOOK at this plate before any clip.",
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
            "generation, parked three-quarter front on a narrow sealed mountain road "
            "with dense Borneo rainforest behind it. Upright SUV proportions, long "
            "bonnet, short front overhang, AMG Line diamond-pin grille with one "
            "horizontal bar and a large centred star, slim two-piece headlamps each "
            "with one sweeping daytime-running bar, a shoulder crease from the front "
            "wing into the tail lamp, flush door handles, 19-inch five-twin-spoke AMG "
            "wheels. THE NUMBER-PLATE RECESS IS EMPTY - no plate is fitted, front or "
            "rear, and no lettering of any kind appears on the body. Full-frame DSLR, "
            "50mm, f/5.6, ISO 200. REAL PHOTOGRAPH ARTEFACTS, "
            "not a render: true paint reflections with visible sky gradient, accurate "
            "panel gaps, correct tyre sidewall relief, no HDR halos. Negative: CGI, "
            "videogame look, any visible registration or number plate, plate lettering, "
            "dealer sticker, model badge text, invented badges, tyre brand lettering, "
            "wrong grille pattern, coupe roofline, oversaturated postcard grade."},
            # J4 ROUND 2, 2026-08-07 — the catch that saved a 4cr plate from poisoning
            # six shots: _LOOK is appended to every SOURCE prompt and to NO PLATE prompt,
            # so the plan's text bans lived only on the clips and not on the reference
            # image they all cite. This plate was framed three-quarter FRONT (the one
            # angle that puts a plate dead centre) and ASKED for "real tyre sidewall
            # lettering". That is the lesson-35 'SR' badge mechanism exactly, and
            # planqc's plate check only tests resolution and existence, so no mechanical
            # gate could ever have caught it. LOOK at the rendered plate for ANY
            # lettering before it is passed as image_reference to B, C or I.

    "mahua": {"job": "4b981c95-7bc1-43c9-8dbb-ede76cb4939a", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-07, 5504x3072. OCR CLEAN (zero text detected). Was: The PLACE anchor for five of nine sources. "
                      "A named PLACE is a named subject: a text-only 'Mahua Waterfall' "
                      "will return a generic tropical cascade and every shot after it "
                      "will be somewhere else.",
            "must_show": "Mahua Waterfall, Crocker Range Park, Tambunan: a SINGLE "
                         "17-metre drop coming off a dark rock lip in one unbroken "
                         "column - not a tiered or fanned cascade - landing in a small "
                         "plunge pool about 1.3 metres deep, chest deep on a standing "
                         "adult, boulders around the "
                         "rim, mossy wet rock walls close on both sides, dense "
                         "highland rainforest canopy overhead with light coming through "
                         "in shafts. NO SIGNAGE, no railings, no buildings anywhere = "
                         "zero invented-text risk.",
            "prompt":
            "Photograph of a single seventeen-metre waterfall in a narrow Borneo "
            "rainforest gorge, Crocker Range, Sabah. One unbroken column of white water "
            "falling from a dark rock lip into a small shallow plunge pool ringed with "
            "grey boulders, mossy wet rock walls close on both sides, dense highland "
            "canopy overhead with shafts of daylight coming through the leaves and "
            "spray hanging in them. Full-frame DSLR, 35mm, f/5.6, ISO 400, 1/500s. "
            "REAL PHOTOGRAPH ARTEFACTS, not a render: frozen droplet detail at the lip, "
            "true wet-rock specularity, accurate deep-shade colour, no HDR halos. "
            "Negative: CGI, videogame look, oversaturated postcard grade, tiered or "
            "fanned cascade, wide open sky, any signage or text, railings, crowds."},

    "crocker": {"job": "014b8022-5d1b-4b5b-8c46-6ac8bdd3166f", "res": "4k", "ar": "16:9", "cr": 4,
            "status": "BUILT 2026-08-07, 5504x3072. OCR CLEAN (zero text detected). Was: The ROAD anchor - the 1.5 hours that the "
                      "first card is about. Separate from the mahua plate on purpose: "
                      "the road and the gorge are two different places, and citing the "
                      "gorge plate for a driving shot is how a plate anchors the wrong "
                      "composition.",
            "must_show": "the Tambunan side of the Crocker Range: a narrow sealed "
                         "two-lane road switchbacking along a forested mountain "
                         "shoulder, layered blue ridges receding behind, low cloud "
                         "sitting in the valleys below the road, no buildings and no "
                         "signage in frame.",
            "prompt":
            "Photograph of a narrow sealed two-lane mountain road switchbacking along a "
            "forested ridge in the Crocker Range, Sabah, Borneo, early morning. Layered "
            "blue ridges receding into distance, low cloud lying in the valleys below "
            "the road, dense green forest crowding both verges, wet tarmac catching the "
            "first light. Full-frame DSLR, 35mm, f/8, ISO 200. REAL PHOTOGRAPH "
            "ARTEFACTS, not a render: true atmospheric haze with distance, accurate "
            "cool shadow and warm sunlit split, real asphalt texture, no HDR halos. "
            "Negative: CGI, videogame look, oversaturated postcard grade, any signage "
            "or text, buildings, power lines, crowds."},
}

# _LOOK is appended to every source prompt, so every word in it is BOILERPLATE and is
# subtracted by planqc 29 before a linkage token is checked. Deliberately written to
# contain NONE of the carry tokens used below (cold, mist, road, river, spray, pool,
# falls, phone, walkway, suv, trailhead).
_LOOK = (
    "Humid highland Borneo air at a thousand metres; true texture on skin, soaked "
    "fabric and leaf. REAL FOOTAGE, NOT A RENDER: handheld micro-shake, natural depth "
    "of field, accurate reflections, no HDR halos. Negative: CGI, videogame look, "
    "postcard oversaturation, invented signage text, legible device screens, visible "
    "registration plates, rear model badges or lettering of any kind, any legible "
    "slogan wordmark logo or printed graphic on clothing, any legible "
    "instrument-cluster or infotainment display, extra fingers, "
    "warped faces, drone-stock look."
)

# ---------------------------------------------------------------- SOURCES (9 x 22.5cr)
SOURCES = {
 "A": ("EVENT · THE COLD HIT", "#2E6F8E", "EVENT", ["mahua", "nev"],
       "Vertical 9:16. THE EVENT, and it RESOLVES INSIDE 1.2 SECONDS. Camera low at "
       "water level at the edge of the shallow plunge pool from the first reference "
       "image, MIDDAY light coming down through the canopy. THE DROP IS ALREADY "
       "HAPPENING AT FRAME ZERO - his body is entering the water in the first three "
       "frames, never after a beat of empty pool. The man from the second "
       "reference images - white print shirt, dark shorts - drops into the cold pool "
       "from the boulder rim and the water bursts white around his chest in the first "
       "half second; he comes up gasping, hair flat and soaked, the seventeen-metre "
       "column still falling behind him. A body event, not a camera move. His face, "
       "hair and EARRING match the references exactly. " + _LOOK),

 "B": ("the Crocker road at first light", "#7B3F6B", "EXTERIOR", ["crocker", "glc300"],
       "Vertical 9:16. DAWN, first light. Long lens from across a valley onto the "
       "switchbacking mountain road of the first reference image: the white SUV from "
       "the second reference image climbing away from the lens into layered ridges, "
       "mist lying in the valley under the road and burning off the tarmac as the "
       "sun reaches it. IN THE FINAL FRAMES THE SEALED ROAD RUNS OUT into a gravel "
       "turnout at the forest edge and the vehicle slows toward it - the tarmac "
       "visibly ENDS inside this clip. Continuous vehicle movement first frame to "
       "last. " + _LOOK),

 "C": ("cabin, window down", "#4A6FA5", "HUMAN", ["nev", "glc300"],
       "Vertical 9:16. DAWN turning to full MORNING - one continuous light move, which "
       "is why this single clip serves both of its shots. Interior of the SUV from the "
       "second reference image, over-the-shoulder onto the windscreen: the man from the "
       "first reference images - white print shirt, dry, hair dry - driving with the "
       "window down, cold air moving his hair, the mountain road narrowing into forest "
       "ahead through the glass, mist crossing the windscreen. His face, hair and "
       "EARRING match the references exactly, real skin, no smoothing. " + _LOOK),

 "D": ("the walkway in", "#5B8C5A", "EXTERIOR", ["mahua"],
       "Vertical 9:16. Flat overcast MORNING shade under a closed rainforest canopy - "
       "diffuse light with no direct sun anywhere in frame, which is why this clip "
       "serves shots in two different light states without dating either one. THE CLIP "
       "OPENS WHERE THE SEALED ROAD ENDS - the last two metres of tarmac and a gravel "
       "turnout are in the first frames, and the walkway starts from them. Waist-"
       "height camera moving forward along a narrow flat concrete walkway through dense "
       "highland forest toward the gorge of the reference image, wet leaves crowding "
       "both sides, a bright gap of daylight and hanging spray held at the end of the "
       "walkway so the frame keeps a highlight. Feet on wet concrete. No railings, no "
       "boards, no signage. Continuous forward movement. " + _LOOK),

 "E": ("the falls, whole", "#1F6E63", "EXTERIOR", ["mahua"],
       "Vertical 9:16. MIDDAY. Static long lens from across the gorge of the reference "
       "image, framed so the whole seventeen-metre column reads top to bottom: one "
       "unbroken white fall coming off the dark lip, hammering into the shallow pool at "
       "the base, spray blowing back off the rock and drifting through shafts of "
       "daylight. Wet black rock walls both sides. The water never stops moving. "
       + _LOOK),

 "F": ("the river over boulders", "#3F7BA8", "EXTERIOR", ["mahua"],
       "Vertical 9:16. LATE MORNING into MIDDAY under canopy shade. Ground-level camera "
       "just above the surface where the pool of the reference image drains out: clear "
       "cold river water running fast over grey boulders straight toward the lens, "
       "white where it breaks, the stones visible through it, a bright patch of sky "
       "reflected in the moving surface so the frame keeps a highlight. Nothing but "
       "water and stone in frame. " + _LOOK),

 "G": ("NEV filming the falls", "#93507E", "HUMAN", ["nev", "mahua"],
       "Vertical 9:16. AFTERNOON. Handheld camera close behind and slightly above the "
       "man from the first reference images, standing waist-deep at the edge of the "
       "pool of the second reference image, shirt and hair SOAKED, holding a phone up "
       "at arm's length toward the falling water. THE PHONE IS SEEN FROM BEHIND, its "
       "blank back to the lens, and its screen is never visible or legible. His "
       "shoulders are drawn up and tight against the cold, jaw set, breath short - he "
       "is enjoying it and he is freezing at the same time. He turns "
       "his head back toward the lens with a grin, water running off his hair. Face and "
       "EARRING exact. " + _LOOK),

 "H": ("NEV · THE COLD LETS GO", "#A9553E", "HUMAN", ["nev"],
       "Vertical 9:16. GOLDEN hour, low warm side light. THIS CLIP PERFORMS A CHANGE "
       "OF STATE FROM ITS FIRST FRAME TO ITS LAST AND THAT ARC IS THE POINT OF IT - it "
       "must be monotonic, never a loop. Medium-close on the man from the reference "
       "images, chest up, hair soaked flat, shirt dark with water, forest thrown out of "
       "focus behind him. HE STARTS COLD: arms crossed hard over his chest, shoulders "
       "up around his ears, jaw locked, short shallow breaths, one visible shiver. Then "
       "the low sun reaches him and it LETS GO across the second half of the clip - the "
       "arms come down, the shoulders drop, he shakes the water out of his hair in one "
       "quick movement with droplets flying off into the light, and he grins. Face, "
       "hair, EARRING exact, real skin, no smoothing. " + _LOOK),

 "I": ("PAYOFF · the road out", "#6A4F8C", "PAYOFF", ["glc300", "crocker"],
       "Vertical 9:16. THE PAYOFF. GOLDEN hour. Camera tracking from behind the white "
       "SUV of the first reference image as it pulls away and runs down the "
       "switchbacking mountain road of the second reference image, low sun coming "
       "through the trees across the tarmac in bars, ridges going blue and long behind "
       "it. Continuous forward movement, first frame to last. " + _LOOK),
}

# FRAMING (planqc 28). FIVE of nine sources cite the mahua plate - a heavier single-plate
# load than kundasang's four - so every camera position is stated. A plate anchors PLACE;
# framing must be declared or the model returns the picture it was given.
FRAMING = {
    "A": "low at water level on the pool rim, subject dropping into frame from above",
    "B": "long lens across the valley, vehicle receding up the road into layered ridges",
    "C": "interior over-the-shoulder, windscreen and hands, no exterior camera position",
    "D": "waist height moving forward along the walkway, leaves crowding both sides",
    "E": "static long lens across the gorge, full column top to bottom in frame",
    "F": "ground level just above the surface, water running straight at the lens",
    "G": "handheld close behind and above the subject, over his raised arm",
    "H": "medium-close static, chest up, the subject changing state inside the frame",
    "I": "rear tracking behind the vehicle, road descending away from the lens",
}

# ---------------------------------------------------------------- TIMELINE 20 shots
# 48 beats at 99.4 BPM = 28.9739s. burst = 2 beats = 1.2072s, med = 4 beats = 2.4145s.
# 16 bursts + 4 meds. Median 1.207s against the profile's 1.13s (range 0.6-2.51).
# 20 shots / 28.974s = 41.4 cuts/min against the profile's 40.3 (band 32.2-48.4).
# ONE designed whip at boundary 4; every other boundary is a hard cut.
# The four meds are the breathing beats: the pool, the falls held, his face, the road out.
SHOTS = [
 ("A", 1.00, "burst", "cold water takes him - he drops into the pool and it goes white"),
 # J0 ROUND 2: shot 1 used to be source B - a long-lens valley establisher, the most
 # inert image in the timeline - and it drained the second half of the 2s window. B and
 # C are swapped so 1.21-2.41s holds a face and near-field motion. The 0->1 'cold'
 # token survives the swap unchanged.
 ("C", 1.15, "burst", "in the cabin at first light, window down, cold mist crossing the windscreen"),
 ("B", 1.20, "burst", "outside: the SUV climbing the mountain road, mist lying in the valley under it"),
 ("C", 1.00, "burst", "hands on the wheel, the road narrowing into forest - the river somewhere below"),
 ("B", 1.00, "burst", "the road bending up into the range and running out at a gravel turnout"),
 ("D", 1.20, "burst", "the sealed road ends - he leaves the car and walks in, the flat walkway heading for the sound of the river"),
 ("F", 1.25, "burst", "first sight of it - the river running fast over grey boulders"),
 ("D", 1.00, "burst", "the walkway deeper in beside the river, spray already in the air"),
 ("E", 1.15, "burst", "the falls: seventeen metres in one drop, spray blowing off the rock into a shallow pool"),
 ("F", 1.00, "med",   "the pool draining out - clear cold water over the boulders, chest deep at most"),
 ("A", 1.25, "burst", "so he gets in: the cold takes him, white water, right under the falls"),
 # J2 ROUND 2: this note used to say "he comes up" - source E is a person-free
 # cross-gorge long lens and cannot show him. The note now describes what the clip
 # actually contains, and the consequence that leaned on it moved to boundary 12.
 ("E", 1.00, "burst", "the falls carry on regardless - seventeen metres, unbothered, right where he just was"),
 ("G", 1.15, "burst", "he lifts the phone out of the water and films the falls from inside them"),
 # NOT "the shot he is taking" - source E is a static cross-gorge long lens and a phone
 # held at arm's length in the pool cannot produce that frame. J2 round 4. The note now
 # claims only what the clip is.
 ("E", 1.20, "med",   "the falls whole, held - the thing he drove two hours for, nothing cut away"),
 ("G", 1.00, "burst", "the selfie: phone at arm's length, soaked hair, grin, shoulders drawn up against the cold, the falls behind him"),
 # NOT "the walkway back out" - source D moves FORWARD toward the gorge in every frame it
 # has, so a note claiming the opposite direction describes footage that does not exist.
 # J2 round 4. The leaving is carried by shot 16, where it is actually on screen.
 ("D", 1.35, "burst", "the cold wins - phone down, one last look down the walkway, the gorge all shade now"),
 # THE TAIL NOW CARRIES THE FILM'S LAST STATE CHANGE, and it costs nothing: source H was
 # a golden portrait that only stood there, so shots 16 and 18 were two windows of one
 # unchanging clip - J2's round-3 finding, and it was right. H now PERFORMS an arc
 # (cold -> warm) and the two windows sit at opposite ends of it. A source is a CHANGE,
 # not a place. Same 22.5cr, same nine sources, board still renders.
 ("H", 1.00, "burst", "out of the gorge and into the last sun, arms crossed hard, still cold - the SUV waiting"),
 ("I", 1.00, "burst", "the white SUV pulls away from the trailhead, low sun in bars across the road"),
 ("H", 1.20, "med",   "the cold finally lets go - arms down, he shakes the water out and grins back at the trailhead, the road already going"),
 ("I", 1.15, "med",   "the last of it: the road out of the range, light going long"),
]

CALLBACKS = []          # no repeated (source, crop) pair exists - every repeat is re-framed
# MEASURED 2026-08-07 from the delivered clip, not guessed - which is what this field
# was always for. HIS CATCH, rewatching the preview: "i thought the cold chilling scene
# was supposed to be the starting visual hook?" It was, and the plan demanded it in
# capitals: "THE DROP IS ALREADY HAPPENING AT FRAME ZERO - his body is entering the
# water in the first three frames, never after a beat of empty pool."
# THE GENERATOR IGNORED IT. Frame-by-frame on the delivered clip A:
#     t=0.00  legs only, top of frame, airborne. THE POOL IS EMPTY.
#     t=0.15  airborne     t=0.30  airborne     t=0.45  airborne, feet above water
#     t=0.60  IMPACT - frame delta jumps 27.5 -> 36.5, the largest step in the clip
# So the first HALF of a 1.207s hook was a man falling through air over an empty pool -
# J0's veto class, delivered inside a clip that was prompted against it.
# BANNING the airborne head moves shot 0 to the impact for ZERO extra credits.
# Capacity after the ban: A needs 2.41s, has 5.0 - 0.52 - 0.1 = 4.38s (planqc 21).
# ---------------------------------------------------------------- SCENE REFS
# HIS CORRECTION 2026-08-11 (see desafarm's block for the full statement): refs are
# chosen PER SCENE from assets/nev/ (97 measured images, index.json), never the
# blanket three. Wardrobe here is 10_shirt_white_print - but it is SOAKED DARK from
# shot 8 onward, so wet scenes deliberately carry NO wardrobe ref: a crisp white
# reference would fight the prompt's "shirt dark with water". planqc 27b enforces.
SOURCE_REFS = {
    # A: THE COLD HIT - camera low at water level, his body entering side-on at
    # frame zero: right profile (earring) + front anchor + dry shirt front.
    "A": ["assets/nev/face/profile_right.jpeg",
          "assets/nev/face/front_neutral.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/75_front.jpeg"],
    # C: OVER-THE-SHOULDER onto the windscreen -> back of head + right profile +
    # the shirt's BACK (that is what the lens actually sees).
    "C": ["assets/nev/face/back_head.jpeg",
          "assets/nev/face/profile_right.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/76_back.jpeg"],
    # G: close BEHIND and slightly above, waist-deep, soaked -> back of head + the
    # shirt's back for shoulder geometry; right profile for the sliver of face at
    # the phone. Soaked scene: the wardrobe back is for CUT, not colour.
    "G": ["assets/nev/face/back_head.jpeg",
          "assets/nev/wardrobe/10_shirt_white_print/76_back.jpeg",
          "assets/nev/face/profile_right.jpeg"],
    # H: THE COLD LETS GO - medium-close, chest up, INTO the lens, cold -> grin.
    # Face-only set, all three fronts: the arc's endpoints (neutral -> smile) plus
    # calm for the EARRING. No wardrobe ref: the shirt is soaked dark by design.
    "H": ["assets/nev/face/front_neutral.jpeg",
          "assets/nev/face/front_smile.jpeg",
          "assets/nev/face/front_calm.jpeg"],
}

BAN_SPANS = {"A": [(0.0, 0.52)]}
DELOGO    = {}          # EMPTY ON PURPOSE. The phone-screen risk is handled in the PROMPT
                        # (G shows the phone's blank back; "legible phone screens" is in
                        # every negative block) and READ at clipqc. A DELOGO box before a
                        # clip exists would be an invented number - planqc 25 can only
                        # check that a box is in frame, never that it is on the right
                        # pixels. Populate from the measured clip, then re-run.

# THE ONE DECLARED BACKWARDS BOUNDARY. planqc 30 reads this dict; a jump listed here is a
# CHOICE and anything else is the KK v15 bug. Boundary 0 only.
TIME_JUMPS = {
    0: "COLD OPEN. Shot 0 is midday - the water taking him - and shot 1 rewinds to dawn "
       "on the road. The whole field opens this subject on the trail-reveal and arrives "
       "at the falls at 8-15s; we spend the payoff at frame zero and then tell the day "
       "that earned it. Every boundary from 1 onward is strictly monotonic.",
}

BEATS = {"burst": 2, "med": 4}

# ONE WHIP, and it is a measurement, not a taste. travel_vlog declared 0% blended from a
# frame-difference heuristic whose own analysis file says "a very fast whip can read as a
# hard cut". RE-MEASURED with tools/blendsense.py across the same 6 references: 3 whips +
# 1 dissolve in 42 cuts = 9.5% pooled designed, and 3 of 6 refs use one. 9.5% of 19
# boundaries = 1.8. Taking ONE, not two, because three of the six use none.
# PLACED AT BOUNDARY 4, the first consequence beat: the road runs out, SO he walks in. A
# whip is the physical act of that turn - the only boundary in the film where the mode of
# travel changes. planqc 20 forbids a blend touching an EVENT shot, which rules out
# boundaries 9 and 10 either side of shot 10, and boundary 0.
BLEND_AFTER  = [4]
BLEND_KIND   = "whip"               # the ONLY designed kind blendsense found here
BLEND_WIDTH  = 0.24                 # floor of the 240-560ms band: a whip must be FAST

SFX_LEAD     = 0.22
IMPACT_AT    = []                   # hero_only: no whoosh/impact layer on a vlog's cuts
SUBDROP_AT   = []

# ---------------------------------------------------------------- SOUND (ambience gate)
SOUND = {
    "bed":        "BGM/travel_vlog/Easy-Love-by-Hotham.mp3 - 99.4 BPM NATIVE, zero "
                  "stretch, 199s (6.9x the video: the widest segment choice in the "
                  "measured bank), 15.5dB dynamics, CC BY 3.0. Credit line REQUIRED at "
                  "publish - see BGM/travel_vlog/MEASURED.md. NOT Crystal-Water: that "
                  "is kundasang's bed.",
    "hero":       "the water impact on shot 0 - the body hitting the pool. After that "
                  "the gorge itself carries the film: river, then falls, then the road.",
    # THE KEY THE ENGINE ACTUALLY READS. engine.py:781 reads SOUND["hero_shot"] under
    # edit_sfx=hero_only and silently defaults to 0. crown defined "hero" and not
    # "hero_shot", which would have put the only sound in a 30s film 14.00s early on a
    # 278cr build. travel_vlog runs hero_only, so this key is LIVE on this plan.
    "hero_shot":  0,
    "duck_shots": [0],
    "silence":    "none - water is continuous from shot 5 to shot 16; the two quiet "
                  "shots are the portraits, where the bed is allowed to come forward",
}

FOLEY = {   # ambience gate: every shot lays its own clip audio, mostly UNDER the bed.
     0:  -3.0,   # A  EVENT - the impact and the gasp. Must be HEARD. (planqc 19: >= -6)
     1: -11.0,   # B  distant engine on the switchbacks
     2:  -9.0,   # C  cabin, window down, air rush
     3: -11.0,   # B  the road, mid distance
     4:  -9.0,   # C  wheel, air, tyre hum
     5: -10.0,   # D  feet on wet concrete, forest close
     6:  -6.0,   # F  the river - the reason the walk exists. Forward.
     7:  -8.0,   # D  walkway beside the water, spray coming up
     8:  -5.0,   # E  the falls hitting the pool - the loudest thing in the film
     9:  -7.0,   # F  the pool draining out
    10:  -3.0,   # A  EVENT source again - the water stays forward (planqc 19: >= -6)
    11:  -5.0,   # E  under the column, full weight
    12:  -9.0,   # G  him in the water, phone up
    13:  -6.0,   # E  the falls held
    14: -10.0,   # G  the selfie beat - pulled back so the grin reads
    15: -11.0,   # D  walking out, the noise falling behind
    16: -12.0,   # H  quiet - the face is the shot
    17:  -6.0,   # I  PAYOFF - the car leaving. Must be HEARD. (planqc 19: >= -6)
    18: -12.0,   # H  clean under the card
    19:  -6.0,   # I  PAYOFF source again - the descent stays forward
}

# ---------------------------------------------------------------- THE CLOCK (planqc 30)
# Shot 0 is the COLD OPEN and sits at midday; boundary 0 is declared in TIME_JUMPS.
# From shot 1 the clock is strictly monotonic: dawn -> morning -> midday -> afternoon ->
# golden, no state skipped. THERE IS NO DUSK STATE: the park gate shuts at 5pm
# (sabahparks.org.my, fetched 2026-08-07), so a dusk shot at this waterfall would be a
# lie a local viewer can catch. Each source prompt PINS its own light state.
SHOT_TIME = ["midday",
             "dawn", "dawn", "dawn",
             "morning", "morning", "morning", "morning",
             "midday", "midday", "midday", "midday",
             "afternoon", "afternoon", "afternoon", "afternoon",
             "golden", "golden", "golden", "golden"]

# ---------------------------------------------------------------- LINKAGE (19 boundaries)
# TYPED, never prose: (kind, token, intent). planqc 29 requires the TOKEN to be findable
# in the writing of BOTH shots it joins, with the shared _LOOK boilerplate subtracted
# first - so a connection cannot exist only in my head. Written AFTER the shot order was
# frozen (craft L59), boundary by boundary.
# Kinds: motion · gaze · subject · object · light · sound · consequence.
# planqc 31 floor: 4 consequence boundaries out of 19. This plan declares 5.
LINKAGE = [
    # J2 (2026-08-07) refused this as a consequence: a rewind is an EDITORIAL move, not
    # an effect of shot 0. Downgraded to the carry it actually is - the same cold, at the
    # end of the day and at the start of it.
    ("subject",     "cold",      "the cold water that takes him -> the cold mist he drove through to reach it"),
    ("light",       "mist",      "mist on the windscreen -> the same mist lying in the valley outside"),
    ("motion",      "road",      "the SUV climbing the mountain road -> the same road narrowing through the windscreen"),
    ("motion",      "road",      "the road narrowing ahead of him -> the road bending up and running out"),
    # J2: "neither the road ending nor the parking is in any shot". Source D now OPENS on
    # the last two metres of tarmac and the gravel turnout, so the cause is ON SCREEN.
    ("consequence", "road",      "the sealed road ENDS in frame, SO he leaves the car and goes in on foot"),
    ("subject",     "river",     "the walkway is heading for the river -> the river itself"),
    ("motion",      "river",     "the river running at the lens -> the walkway climbing beside it"),
    ("motion",      "spray",     "spray coming up off the water -> spray blowing off the rock at the lip"),
    ("object",      "pool",      "the column lands in the shallow pool -> the same pool draining out"),
    ("consequence", "cold",      "the pool is waist deep and cold, SO he gets in"),
    ("subject",     "falls",     "he goes under the falls -> he comes up and they are still going"),
    # J2 ROUND 2 killed the version of this that lived here: it claimed "he is standing
    # under the falls" as the cause, but shot 11's source E contains no person at all.
    # The carry is what E and G genuinely share - the falls themselves.
    ("subject",     "falls",     "the falls carrying on -> the falls he raises the phone at"),
    # WAS a consequence claiming shot 13 is the phone's own frame - J2 round 4 killed it:
    # E is a tripod long lens across the gorge and cannot be a phone at arm's length.
    # It is a gaze carry, which is what it always actually was.
    ("gaze",        "falls",     "he is filming the falls -> the falls, whole, the way they actually are"),
    ("subject",     "falls",     "the falls held -> the falls behind him in the selfie"),
    # J2 called the old version ("got the shot SO he leaves") a tautology of locomotion.
    # The real cause is 23C water: G now shows shoulders drawn up and jaw set, and this
    # boundary is the moment the body decides. The one irreversible state change after
    # dry->wet.
    ("consequence", "cold",      "the cold has beaten him, SO the phone goes down and he starts back out"),
    # WAS a subject carry on 'walkway' - J2 round 3 said the whole tail had no causal
    # boundary at all, and it did not. The cause is the same one that drove him out of
    # the water and it is still acting on his body when he reaches the car.
    ("consequence", "cold",      "he is soaked and the gorge is all shade, SO he walks out to the last patch of sun"),
    ("subject",     "suv",       "he walks back to the SUV -> the SUV pulling away"),
    ("gaze",        "trailhead", "the trailhead behind the car -> one look back at it"),
    ("motion",      "road",      "the road already going -> the road out of the range"),
]

CROP_XY = {}            # nothing measured yet; populated only from a probe

# ---------------------------------------------------------------- THE ONE OPEN RISK
# SOURCE H'S ARC CAN BE DELIVERED BACKWARDS, AND NO PLAN FIELD CAN STOP IT.
# MEASURED against engine.py:409-495, not assumed. The window allocator hands out
# NON-OVERLAPPING windows per source (built 2026-08-04 after Gavril caught frame-for-
# frame duplicates by eye), so shots 16 and 18 CANNOT overlap - a judge claimed they
# would and the code says otherwise. But the allocator places the LONGEST shot first
# and picks by action-peak proximity to best_in_s, so nothing guarantees that shot 16
# takes the EARLY window (arms crossed) and shot 18 the LATE one (the grin). The arc
# can arrive in reverse: he warms up, then shivers.
#
# CLOSED 2026-08-11 - option 1 built on his go-ahead ("help me fix it"). The engine
# now reads an additive SHOT_WINDOW = {shot: t_in}: pinned shots allocate FIRST (a
# free-choice shot cannot steal the window) and a pin that does not fit is an
# ALLOCATION FAILURE, never a silent fallback. Shot 16 is pinned to H's head (arms
# crossed hard, still cold) and shot 18 to its tail (the grin), so the arc CANNOT
# arrive in reverse. Values are conservative head/tail picks inside the measured
# 5.0417s clip; refine at ingest from the motion curve if the state change sits
# elsewhere. THE STRIP IS STILL CHECKED BY EYE - the pin fixes the order, only the
# eye confirms the performance.
SHOT_WINDOW = {16: 0.20, 18: 3.70}

CARD_Y       = 0.72
CARD_STYLE   = "fragment"           # pillar style: sentence fragments, <= 6 words
# Two facts and one ask. Both facts are ones BOTH fetched sources agree on. THE ENTRANCE
# FEE IS DELIBERATELY OFF SCREEN: sabahparks.org.my says RM6 for a Malaysian adult and
# mysabah.com says RM3, and a fee goes stale exactly like the crown's price did. The
# disagreement is recorded in CONTENT.verified with its date, which is where a market
# status belongs.
CARDS = [
    # WAS "90 MINUTES FROM KK" at shots 1-4. J4 ABSOLUTE VETO 2026-08-07, and it was
    # right twice over: (a) 90 minutes asserts the LOW END of a range as a fact -
    # clladventureborneo.com (fetched 2026-08-07) states "about 1.5 to 2 hours to reach
    # Mahua Waterfall" from Kota Kinabalu, and mysabah.com's 1.5h is the only source for
    # the short figure; (b) sabahparks.org.my states NO drive time at all, so the old
    # card's claim of two agreeing sources was false. "ABOUT" + the upper bound is the
    # figure no source contradicts. MOVED to shot 0 on J0's fix so the 2s window is
    # never text-empty.
    ("ABOUT 2 HOURS FROM KK",     0, 4, "cap"),
    ("SEVENTEEN METRES, ONE DROP", 8, 4, "cap"),  # verified, both sources
    ("GATE SHUTS AT 5PM",         12, 4, "cap"),  # verified, both sources - and it is why
                                                  # this film has no dusk state
    ("MAHUA NEXT WEEKEND?",       16, 4, "cta"),  # a question, not a beg
]
AI_LABEL_BURNED_IN = False          # HUMAN step at upload. Never burned in (planqc 15).

# ---------------------------------------------------------------- RELATIONSHIPS
# planqc 32, built from the desafarm v2 rejection (craft L101): every defect his eye
# caught was a RELATIONSHIP between two elements that each passed alone. For each
# known pair: how THIS plan holds it. The clips for this film ALREADY EXIST (214.5cr,
# zero failures), so several answers point at the delivered footage, not at prompts.
RELATIONSHIPS = {
    "subject_vs_background":
        "The driving shots (B, I) put the SUV on a mountain road: each prompt states "
        "the camera axis relative to travel, and the contact sheet (tools/contact.py "
        "--raw, his standing order) is read for window-and-road geometry agreement "
        "at ingest, BEFORE assembly - the desafarm sideways-road defect is checked "
        "on real frames here, not asserted.",
    "performance_vs_sound":
        "Nev's three states (cold shock at the plunge, shivering at 16, the grin at "
        "18) each carry their own audio: generate_audio=true kept every clip's OWN "
        "track and the FOLEY design lays it under the bed at foreground level - the "
        "plunge has the gasp and the water, the shiver has breath, the release has "
        "the shake-out. syncqc refuses a foreground-FOLEY clip with an empty lane.",
    "bed_vs_foley":
        "The bed is the 99.4 BPM grid-holder, never the place: clip-own diegetic "
        "audio (water, gorge, road) sits over it and the hero moments duck it. The "
        "desafarm measurement (cuts changed place, sound did not: 0.935 vs 0.947 "
        "control) is re-run on the delivered cut - a waterfall film whose cuts do "
        "not change the sound of water has failed this pair.",
    "card_vs_card":
        "Four cards, spans 0-3, 8-11, 12-15, 16-19: disjoint BY CONSTRUCTION, no "
        "two ever share the y=0.72 zone (craft L107), and planqc 12's clock check "
        "blocks any future edit that makes them overlap.",
    "event_vs_window":
        "The film's events (the plunge, the cascade reveal, the exit) are placed at "
        "action peaks by the allocator, and the engine's mid-action gate (craft "
        "L102, now a HARD refusal) blocks any window that ends above 80% of its own "
        "peak - the cold-water hook cannot be cut off mid-gasp.",
    "arc_vs_shot_order":
        "Source H's arc (arms crossed -> grin) is the film's closing state change. "
        "SHOT_WINDOW = {16: 0.20, 18: 3.70} pins the order mechanically (closed "
        "2026-08-11); syncqc check 5 stays live as the second belt, and the strip "
        "is still checked by eye for the performance itself.",
    "picture_grid_vs_music_grid":
        "The 240ms whip after shot 4 is timing='overlap': the engine RESERVES a "
        "blend-width on the outgoing shot by contract "
        "(engine.BLEND_RESERVES_OVERLAP, read by planqc 34 since 2026-08-11 - one "
        "mechanism, not two agreeing by hand), so the 48-beat grid that TARGET_S "
        "was computed from survives the transition; verify measures post-blend "
        "boundaries against the same grid.",
    "clip_variety_vs_shot_count":
        "Seven of nine sources carry two shots. Every pair was planned as two "
        "DECLARED states (H is the template: cold vs released), the allocator's "
        "look-dupe gate refuses same-look pairs at >=0.80, and because the raws "
        "exist, ingest_gate measures each source's best available window pair "
        "BEFORE assembly - a source that cannot supply two looks loses its second "
        "shot at plan level, the desafarm source-E lesson (L103/L104).",
}

GRADE_SAT    = 1.00                 # daylight vlog: the prompts carry the look
GRADE_BRI    = 0.0
TARGET_BLACK = 10.0                 # profile values
TARGET_SAT   = 74.5

# ---------------------------------------------------------------- CONTENT
CONTENT = {
    "claim":    "Mahua Waterfall is about two hours from Kota Kinabalu, it is a "
                "single seventeen-metre drop into a pool about 1.3 metres deep - chest "
                "deep on a standing adult, which is the whole point: you can walk into "
                "it - and the "
                "park gate shuts at 5pm - which is why this is a day trip and why the "
                "film ends in golden light instead of dusk.",
    "verified": "THREE sources, all fetched 2026-08-07. The two facts on cards 2 and 3 "
                "- the 17m drop and the 8am-5pm gate - are stated by all three. THE "
                "DRIVE TIME IS A RANGE, NOT A NUMBER, and card 1 says so: "
                "clladventureborneo.com states 'From Kota Kinabalu... it takes about "
                "1.5 to 2 hours to reach Mahua Waterfall'; mysabah.com states 1.5 "
                "hours; sabahparks.org.my states NO drive time at all. An earlier "
                "version of this card read '90 MINUTES FROM KK' and claimed two "
                "agreeing sources - J4 vetoed it 2026-08-07 on both counts, and the "
                "card now carries the upper bound with 'ABOUT' in front of it. THE "
                "SOURCES ALSO DISAGREE ON THE TAMBUNAN LEG: sabahparks.org.my puts the "
                "substation 'approximately 14km from Tambunan town', mysabah.com says "
                "26km via Jln Ranau-Tambunan plus a 6km village road. That figure is "
                "not on screen and must not go on screen until one of them is "
                "confirmed. (1) sabahparks.org.my, the official Sabah Parks "
                "page for Crocker Range Park: park area 139,919ha, elevation 100-2050m, "
                "Mahua substation at 1,000m with 'the 17 m tall Mahua waterfall which "
                "fall into a 1.3m deep pool', operating hours 8.00am-5.00pm daily. "
                "(2) mysabah.com's Mahua Waterfall page: height 'nearly 17 meters', "
                "water around 23 degrees Celsius, 1.5 hours' drive from Kota Kinabalu, "
                "26km from Tambunan town via Jln Ranau-Tambunan then a 6km paved "
                "village road, a 500m flat concrete trail from the substation to the "
                "falls, swimming permitted, about 1,600 visitors a month. "
                "DELIBERATELY OFF SCREEN, recorded here with its date because the two "
                "sources DISAGREE and a fee is a market status: sabahparks.org.my "
                "states RM6 per Malaysian adult per day (RM20 international) while "
                "mysabah.com states RM3 (RM10 non-Malaysian). No card asserts a price. "
                "Also off screen: the GLC 300 4Matic AMG Line is not in Mercedes-Benz "
                "Malaysia's current X254 lineup, which is what makes it a recond "
                "audience's car - the same market-status reasoning that kept the "
                "crown's price off its cards after J4's veto.",
    "twist":    "the payoff is spent at frame zero. The field's Mahua reels walk you in "
                "and hand you the waterfall at 8-15 seconds; this one gives you the "
                "cold water in the first 1.2 and then makes you watch the day that "
                "earned it - a drive, a walk, and a man who gets in. The water is the "
                "clock: dry shirt, wet shirt, still wet at golden hour.",
    "why_stop": "frame zero is a BODY EVENT, not a landscape - someone hits cold water "
                "and reacts, which reads at phone size and resolves inside 1.2s; card 1 "
                "is a drive time, the single thing anyone planning this trip actually "
                "searches for; card 3 is a closing time, which converts a nice video "
                "into a plan; and the CTA is a question with a date implied in it "
                "rather than a request for a follow.",
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

PROBE_FIRST  = "A"     # the cold hit. It is the hook, it is the only shot with a body
                       # event in water, and it is the one clip whose failure means the
                       # film does not exist. Probe alone, LOOK, then batch the other 8.

# GENERATED 2026-08-07. seedance_2_0, 720p, mode std, 5s, 9:16, generate_audio=true.
# All nine returned 720x1280 @ 24fps, 5.041667s, with an AAC track. Zero failures.
# MEASURED SPEND: balance 4927.82 -> 4713.32 = 214.50cr, exactly the planned figure.
CLIPS = {"A": "mahua_A.mp4", "B": "mahua_B.mp4", "C": "mahua_C.mp4",
         "D": "mahua_D.mp4", "E": "mahua_E.mp4", "F": "mahua_F.mp4",
         "G": "mahua_G.mp4", "H": "mahua_H.mp4", "I": "mahua_I.mp4"}

# THE RAWS. Run tools/pull_mahua.py to fetch all nine into projects/mahua/clips/.
# KEEP THEM: travel_vlog's motion_floor 0.6 and brightness_band [35,200] are still
# PROVISIONAL, and every kk_*.mp4 was deleted before they could be re-derived.
CLIP_JOBS = {
 "A": "hf_20260807_050205_f106c547-5c1e-4622-b363-d7b7f84851ae.mp4",
 "B": "hf_20260807_050205_37d646ef-8988-4c7f-8bcf-c90cba89afa8.mp4",
 "C": "hf_20260807_050128_84d6779e-0f05-4a81-8851-c4b83efe7221.mp4",
 "D": "hf_20260807_050205_53ff5dcd-0a94-42c1-bd22-d1d5ff8d1e0b.mp4",
 "E": "hf_20260807_050204_59387b45-fe98-4c29-8512-9e75e9d817f5.mp4",
 "F": "hf_20260807_050205_f5055250-a87b-4c79-87cf-595ce9d68e03.mp4",
 "G": "hf_20260807_050128_c4f6c15e-81e0-4fc7-b6c2-48ad4238e58e.mp4",
 "H": "hf_20260807_050128_d6b35dd1-1e26-47c8-beff-96bc3df525b8.mp4",
 "I": "hf_20260807_050128_919f3c83-24ad-4209-a95b-cc878b22f08c.mp4",
}
PLATE_JOBS = {
 "glc300":  "hf_20260807_044021_9eb26ccb-11a3-4878-9565-7285dcfc5741.png",
 "mahua":   "hf_20260807_044021_4b981c95-7bc1-43c9-8dbb-ede76cb4939a.png",
 "crocker": "hf_20260807_044021_014b8022-5d1b-4b5b-8c46-6ac8bdd3166f.png",
}
CLIP_BASE = ("https://d8j0ntlcm91z4.cloudfront.net/"
             "user_3AmHAoGOCTD0Ph5D4HI7jSA04wi/")         # INERT BY DESIGN (bugsense class 2, MED): no pipeline file reads
                       # this. It is the download provenance of the paid artefacts, kept
                       # so a later session can re-fetch a clip it no longer has on disk.
                       # Every kk_*.mp4 is already gone; that is why this field exists.


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
