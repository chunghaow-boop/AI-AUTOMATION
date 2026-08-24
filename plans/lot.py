"""LOT — TALYX BMW recond lot: X1 · X5 · X4. HIS OWN FOOTAGE.
Shot 2026-08-04, 60 clips / 12.7 min, DJI vertical 1728x3072 @59.94.

THIS IS THE FIRST PLAN WRITTEN FOR REAL FOOTAGE (file 32, REAL_FOOTAGE below).
V1-V5 were cut with NO PLAN FILE AT ALL, which meant every story gate was never
invoked - not failed, INVOKED (L176). Five versions reached him with no hook, no
turn and no CTA while an explicit CTA sat unused in the footage.

THE READ CAME FIRST THIS TIME: projects/lot/READ.md (60 clips, 4-frame strips,
text verified at full res) and projects/lot/TRANSCRIPT.json (sherpa-onnx whisper
-small, in-sandbox). Everything below is derived from those two files, not from
motion scores.
"""

REAL_FOOTAGE = True                  # file 32 seat. The camera recorded whatever
                                     # happened; nobody declared it. Read, then cut.
PROJECT   = "TALYX LOT — X1, X5 and the red X4 · dealership promo"
PILLAR    = "car_advice"
PILLAR_FIT = ("car_advice, not car_review: car_review is a SINGLE-subject deep dive and "
              "this is a three-car inventory pitch. Diffed key by key against car_review: "
              "cuts/min 14.3 kept (speech-led) · median shot kept · edit_sfx OVERRIDDEN to "
              "'none' because the only sound that matters is his voice and a bed - there is "
              "no mechanical hero sound in a walkaround · CARD_REGISTER kept as 'card' "
              "(white pill, dark text) because that is this pillar's measured grammar.")

GEN_MODE  = "real"                   # nothing is generated. Zero credits.
BPM       = 98.0                     # measured off the bed itself, not assumed
BEAT      = 60.0 / BPM               # 0.6122s
MODE      = "n/a"
RES       = "1080x1920"              # downscaled from 1728x3072, his 720p cost rule is
                                     # about GENERATION credits and does not apply here
CLIP_S    = 5                        # nominal; real sources run 1-40s (see SOURCES)
MAX_CROP  = 1.00                     # no punch-ins: the sources are already tight
TARGET_S  = 25.93   # 26.53 minus 5 x 0.12s grid dissolves
W, H      = 1080, 1920
FPS       = 30
PROBE_FIRST = None                   # nothing is generated - there is nothing to probe.
                                     # The equivalent safety step for real footage is the
                                     # READ PASS, which ran first (projects/lot/READ.md).

LESSONS_ACK = {
    "bmw i8 car cinematic": 16,       # nearest prior art by SUBJECT (a BMW, his lot)
    "car cinematic": 15,              # the beat-cut grammar the 4 hook shots borrow
    "travel vlog": 9,                 # the speech-led/presenter lessons live here
    "general craft": 183,   # + L182 a builder ships with manifest-writing or it is not
                                     # a builder · L183 a negative control must be synthetic ·
                                     # L184 a gate not wired into the line does not exist · L181: frame geometry is PASSED, never defaulted -
                                     # capcards.overlay_filters defaults frame_h=1280 and put
                                     # this film's captions at 921px (48%, dead centre) the
                                     # moment CARD_Y moved to 0.72. Now passed W,H explicitly.   # + L180: a MINIMUM-DURATION FILTER ON SPEECH AMPUTATES
                                     # THE ASK - his CTA ended in 0.56s and 0.28s runs, both
                                     # under my 0.8s floor, so the take was cut at 17.12 and
                                     # "you PM me for a moment" was deleted. An out-point comes
                                     # from the last speech run of ANY length.            # incl. L174 ASR is the only speech detector (this
                                     # film proved it: 6 of 8 "speech" clips were count-ins,
                                     # a blooper, MUSIC and a bell) · L175 motion metrics
                                     # cannot find a hook/turn/CTA · L176 no plan = no gates
                                     # · L177 when a gate fires, LOOK before arguing ·
                                     # L178 one frame per clip is a thumbnail · L179 a
                                     # mirror call from a thumbnail is a coin flip (clip 41
                                     # is ROTATED 180, the other five were never mirrored)
}

PREMORTEM = [
    ("L174 I will trust an energy detector again and cut a chime or a count-in as speech. "
     "MITIGATION: every speech source below is quoted verbatim from TRANSCRIPT.json in "
     "SOURCES; a clip with no quote may not carry audio."),
    ("L179 I will 'fix' a clip that was never broken. MITIGATION: ROTATE_180 lists exactly "
     "one clip (41) verified at full resolution; NO hflip is applied anywhere in this film, "
     "because at full res 33/34/38/39/42/49 all read forward."),
    ("L177 a gate will fire and I will explain it away. MITIGATION: predeliver TIER 3 "
     "refuses to pass an uninspected finding, and the waiver must name the frames looked at."),
    ("L178 I will pick an in-point I have never seen. MITIGATION: READ.md carries a written "
     "line for all 60 clips; no source appears below that is not described there."),
    ("The b-roll will drift off the sentence again. MITIGATION: SHOTS is built as a SYNC "
     "MAP against clip 48's word timings - when he says X1 the X1 is on screen, and planqc "
     "40's LINKS carry the sentence that each boundary is serving."),
]

# ------------------------------------------------------------------ SOURCES (0 credits)
# duration/motion/luma from raw_catalogue.json; description from READ.md.
# SCHEMA (matches every other plan): (title, palette, ACT, tags, description).
# For real footage the "description" is WHAT THE CAMERA RECORDED, read from READ.md -
# it is not a prompt, because nobody wrote one. That inversion is the whole of file 32.
SOURCES = {
 "X4_FRONT":  ("the red one, front 3/4", "#7A1F24", "EXTERIOR", ["x4","red","lot"],
               "clip 6 - red X4 front three-quarter, its headlight lit, badge and plate SWH "
               "3190 legible, slow drift. 18.3s."),
 "X5_LIGHT":  ("the flare", "#C8CCD0", "EVENT", ["x5","white","lot"],
               "clip 43 - white X5 headlight with a rainbow lens flare across it. The most "
               "arresting single frame in all 60 clips. 19.5s, motion 73.0."),
 "X1_BADGE":  ("X1, named", "#C8CCD0", "EXTERIOR", ["x1","badge","lot"],
               "clip 52 - the X1 badge on the tailgate, drifting, the rear wheel below it. "
               "Identifies the car he names first. 4.7s."),
 "X4_WHEEL":  ("blue calipers", "#7A1F24", "EXTERIOR", ["x4","red","wheel","lot"],
               "clip 9 - red X4 wheel orbiting, BLUE M-Sport calipers visible. 18.4s."),
 "SPINE":     ("THE TAKE", "#8B2E34", "HUMAN", ["nev","x5","speech","lot"],
               "clip 48 - HIM, on the lot, gesturing at the cars. THE COMPLETE TAKE. "
               "VERBATIM (TRANSCRIPT.json): 'So guys, we are Talyx, we promote car dealers "
               "like X1 earlier. With X5 this is also available. Or you are interested in "
               "X4, this red one. So if you want to be interested, YOU PM ME FOR A MOMENT.' "
               "Word windows: "
               "brand 1.96-2.92 | X1 3.20-5.72 | X5 7.80-9.68 | X4 11.44-13.68 | "
               "CTA 16.16-18.80. 20.2s source, 16.89s used."),
 "BOTH":      ("both cars, one frame", "#A8A29B", "EXTERIOR", ["x5","x4","white","red","lot"],
               "clip 45 - white X5 front with the red X4 parked behind it. 37.1s."),
 "X4_REAR":   ("the red one, last", "#7A1F24", "EXTERIOR", ["x4","red","lot"],
               "clip 11 - red X4 rear, taillight and the X4 badge. The last look from "
               "outside is the RED car, because that is the one he asked about - then the "
               "film goes inside and presses start. 23.1s."),
 "X1_START":  ("START", "#2B2B2E", "PAYOFF", ["x1","interior","lot"],
               "clip 59 - a finger presses the red START button, cluster lit behind. The "
               "closing action: the car is waiting to be started. 3.8s. AUDIO IS A CHIME, "
               "not speech (ASR-verified) - it carries no voice and is used muted."),
}
# b-roll used INSIDE the take as cutaways (see CUTAWAYS); same schema, same read.
CUTAWAY_SOURCES = {
 "X1_WHEEL":  ("clip 51 - X1 wheel, orbit. 3.7s."),
 "X5_BADGE":  ("clip 34 - the X5 badge, red X4 visible behind it. 5.4s."),
 "X5_FRONT":  ("clip 42 - white X5 front 3/4, plate SJQ 2315 reads FORWARD. 12.6s."),
 "X4_BADGE":  ("clip 10 - the X4 badge. 6.0s."),
 "X4_ROUNDEL":("clip 5 - red bonnet roundel, camera arcs around it. 10.1s."),
 "HIM_WIDE":  ("clip 47 - him again, wider, gesturing along the white X5. An earlier, less "
               "complete take of the same pitch (ASR-verified) - PICTURE ONLY, never its audio."),
}
SRC_CLIP = {"X5_LIGHT":43,"X4_FRONT":6,"X1_BADGE":52,"X4_WHEEL":9,"SPINE":48,
            "BOTH":45,"X4_REAR":11,"X1_START":59,
            "X1_FRONT":50,"X1_WHEEL":51,"X5_BADGE":34,"X5_FRONT":42,
            "X4_BADGE":10,"X4_ROUNDEL":5,"HIM_WIDE":47}
ROTATE_180 = [41]        # verified at full res: camera held upside down. NOT used in the
                         # cut, listed so no future session re-derives it wrong.
NO_FLIP    = "NO hflip anywhere. 33/34/38/39/42/49 all read forward at native resolution."
DEAD       = [20, 60]    # unusable: blown highlight / near-black (luma 3.8)

FRAMING = {"X5_LIGHT":"macro slow drift","X4_FRONT":"wide drift","X1_BADGE":"macro drift",
           "X4_WHEEL":"medium orbit","SPINE":"medium handheld, him three-quarter to lens",
           "BOTH":"wide static","X4_REAR":"low wide","X1_START":"macro static, locked on the button"}
# Identity on REAL footage is not a reference plate - it is the actual person, filmed.
SOURCE_REFS = {"SPINE": ["he is himself, on camera, clip 48 - no plate can be more "
                         "authoritative than the man"],
               "X1_START": ["his own hand, clip 59"]}
FACE_OPTOUT = {"X1_START": "a hand only, no face in frame"}
# SPINE is deliberately NOT opted out: his face IS the credibility of a dealership promo.

# ------------------------------------------------------------------ THE CUT
# 23.27s = 4-beat hook + the take played WHOLE + a 4-beat close.
# During the take the AUDIO IS CONTINUOUS and only the PICTURE cuts - that is the
# whole point. B-ROLL FOLLOWS THE SENTENCE.
SHOTS = [
 ("X5_LIGHT", 1.00, "beat", "HOOK - an EVENT, not a tour: the flare rakes across the "
                            "headlight. Measured the most arresting frame of all 60."),
 ("X4_FRONT", 1.00, "beat", "the red one, because it is the one he ends up asking about"),
 ("X1_BADGE", 1.00, "beat", "X1 - naming the stock before he does"),
 ("X4_WHEEL", 1.00, "beat", "blue calipers, into his first word"),
 ("SPINE",    1.00, "take", "THE TAKE, WHOLE - 15.16s, audio unbroken. He names the X1, "
                            "the X5 and the red X4 and the picture follows each in turn."),
 ("BOTH",     1.00, "beat", "CLOSE 1 - the white X5 with the red X4 behind it, both in "
                            "one frame: the lot as a whole, after he has asked."),
 ("X4_REAR",  1.00, "beat", "CLOSE 2 - THE RED ONE. He ends on 'this red one', so the "
                            "picture must end on it too. V6 played four WHITE shots after "
                            "that line and the payoff contradicted his last sentence."),
 ("X1_START", 1.00, "hold", "CLOSE 3 - THE PRESS ITSELF: finger in, START, cluster lights. "
                            "V6 started this at 1.3s and caught only the aftermath - 2.4s "
                            "of a static dashboard. The action is at 0.6-1.4s (L178)."),
]
BEATS = {"beat": 2, "take": 16.89, "hold": 2.30}   # 2 beats = 1.224s: V5 measured
                                     # 0.61s as DOUBLE the pillar's 1.34s median - too fast to read   # take = 17.12 - 1.96, his first word to his last
CUT_JUSTIFICATION = {
 0: ("1.22s of clip 43 (19.5s). DISCARDED: the rest is the same headlight orbit before and "
     "after the flare crosses it - READ.md line 43. The flare is the only event in the clip "
     "and 1.22s is the whole of it. 2 beats, matching the pillar's measured 1.34s median."),
 1: ("1.22s of clip 6 (18.3s). DISCARDED: a slow continuous drift across the same front "
     "three-quarter - no second subject, no second event (READ.md 6)."),
 2: ("1.22s of clip 52 (4.7s). DISCARDED: the badge drifts in and out of the same framing; "
     "1.22s holds it legible, which is the shot's only job (READ.md 52)."),
 3: ("1.22s of clip 9 (18.4s). DISCARDED: a continuous wheel orbit; the blue caliper is "
     "visible throughout, so any 1.22s window is equivalent (READ.md 9)."),
 5: ("1.22s of clip 45 (37.1s). DISCARDED: a long static two-car frame - nothing changes "
     "across it (READ.md 45)."),
 6: ("1.22s of clip 11 (23.1s). DISCARDED: a continuous drift along the red rear; the "
     "taillight and X4 badge are legible throughout (READ.md 11)."),
 7: ("2.30s of clip 59 (3.8s), window 0.30-2.60. CORRECTED 2026-08-17: V6 used 1.30-3.75 "
     "and caught only the AFTERMATH - the finger already leaving, then 2.4s of a static "
     "dashboard. Frame-by-frame read of clip 59: finger enters ~0.5s, PRESSES 0.6-1.4s, "
     "cluster needles light from 1.8s. DISCARDED: 0.00-0.30 (settle) and 2.60-3.75 (the "
     "lit cluster sitting still). The window now contains the whole event."),
 4: ("The take plays from his first word (1.96) to his TRUE last word (18.85) with NOTHING "
     "removed "
     "from the middle - the internal pauses at 5.72-7.80 and 13.68-16.16 are KEPT, "
     "because they are where he gestures at the cars and they are the only room the "
     "cutaways have. CORRECTED 2026-08-17: the out-point was 17.12 and cut the CTA in "
     "half. Discarded: 0.00-1.96 (settle) and 18.85-20.18 "
     "(silence after the CTA, he walks out of frame). Neither contains a word. Verified "
     "against TRANSCRIPT.json phrase boundaries, not guessed."),
}
SHOT_TIME = ["afternoon"] * 8   # one covered lot, one continuous take, no light jump
TIME_JUMPS = {}

# ------------------------------------------------------------------ THE SYNC MAP
# The reason this plan exists. Film-time windows inside the take where the PICTURE
# leaves his face and shows the car he is naming at that instant.
SPINE_IN, SPINE_OUT = 1.96, 18.85
CUTAWAYS = [   # NON-OVERLAPPING by construction, each a DISTINCT source. An earlier
               # version nested these and the collapse silently reused the hook's X1
               # badge - the duplicate-shot failure he caught twice, reappearing in the
               # data rather than the edit. (window in CLIP time, source, why)
 ((3.20, 4.50),  "X1_FRONT",  "he says 'X1' - the X1's face"),
 ((4.50, 5.72),  "X1_WHEEL",  "still on the X1, its wheel, while he finishes the clause"),
 ((7.80, 8.80),  "X5_BADGE",  "he says 'X5' - the badge that proves it"),
 ((8.80, 9.68),  "X5_FRONT",  "the X5 itself, plate SJQ 2315"),
 ((11.44, 12.60),"X4_BADGE",  "THE TURN - 'or you are interested in X4, THIS RED ONE'"),
 ((12.60, 13.68),"X4_ROUNDEL","stays on the red car through the turn"),
]
# he stays ON SCREEN for: the brand line (1.96-3.20) and the CTA (16.16-17.12).
# Those are the two moments the viewer must see a person, not a car.

TURNS = [   # film-time, derived from the 4.896s hook + clip-48 word windows
 (4.90,  "THE REVERSAL: his voice enters and the montage becomes a person addressing you"),
 (14.38, "the list of stock becomes a direct offer - 'or you are interested in X4, THIS "
         "RED ONE'. A catalogue turns into a question aimed at the viewer."),
 (19.10, "the CTA begins - and it now runs to its last word, 20.85s"),
]

TRANSITIONS_PLAN = {
 3: {"kind": "dip", "why": "the one chapter change - the cinematic hook closes and the "
     "person begins. A short dip so his first word lands in clean air."},
}
# GRID BLENDS - his instruction 2026-08-17: "you can still add little bit transition for
# the cut to bit section". Deliberately kept SEPARATE from TRANSITIONS_PLAN, which the
# doctrine reserves for STORY turns (planqc 37 checks that a transition sits on a turn).
# These are not story transitions - they are a texture on the two music-grid passages,
# and marking them as story turns would be a lie to the gate. 0.12s dissolves, only
# where the cut is ON THE BEAT; the take's cuts stay HARD because they cut to his
# sentence and a dissolve there would soften a word.
GRID_BLENDS = {"kind": "dissolve", "d": 0.12,
               "hook": [0, 1, 2],      # between the four hook beats
               "close": [5, 6],        # between the three closing beats
               "why": "a light blend on the beat-cut passages only. The take is untouched."}
ALL_HARD_CUTS = False

LINKS = {
 0: {"picture": "red X4 nose -> the white X5's headlight flare",
     "sound":   "bed alone, no voice yet",
     "story":   "there is more than one car here"},
 1: {"picture": "the flare -> the X1 badge, small and specific",
     "sound":   "bed continues",
     "story":   "and they are named"},
 2: {"picture": "X1 badge -> red wheel and blue calipers",
     "sound":   "bed continues",
     "story":   "the red one is the one with the M kit"},
 3: {"picture": "blue calipers -> HIM, standing at the cars",
     "sound":   "the bed dips and his voice enters on 'So guys'",
     "story":   "someone is here to tell you about them"},
 4: {"picture": "his last word -> both cars in one frame",
     "sound":   "his voice ends, the bed comes back up",
     "story":   "he has asked; now you are looking at what he asked about"},
 5: {"picture": "both cars -> the X5's flank",
     "sound":   "bed",
     "story":   "one last look"},
 6: {"picture": "the flank -> a finger on the START button",
     "sound":   "bed resolving",
     "story":   "the car is waiting to be started - by you. That is the CTA, in picture."},
}
LINKAGE = [
 ("subject",     "headlight","the X5's headlight -> the red X4's lit headlight: same feature, two cars"),
 ("subject",     "badge",  "the red X4's badge -> the X1 badge: the stock, named one at a time"),
 ("subject",     "wheel",  "the wheel under the X1 badge -> the red X4's wheel and blue caliper"),
 ("consequence", "red",    "the red wheel -> HIM saying 'this red one': shown, SO explained"),
 ("consequence", "x5",     "his last word -> both cars in one frame: he asked, now you look"),
 ("subject",     "red",    "both cars -> the RED X4's tail: the film ends on the car he ended on"),
 ("gaze",        "start",  "the red tail -> a finger pressing START: his ask, answered as an action"),
]

BLEND_AFTER  = []
BLEND_KIND   = ""
BLEND_WIDTH  = 0.0
SFX_LEAD     = 0.0
IMPACT_AT    = []
SUBDROP_AT   = []
SFX_OVERLAYS = []
SFX_WAIVED   = ("No SFX layer, deliberately. This is a man talking on a covered lot: the "
                "only sounds that belong are his voice and the bed. car_review's edit_sfx "
                "policy is inherited as 'none' and that inheritance is CORRECT here - "
                "checked, not assumed (L165 was the opposite case, a workshop film that "
                "needed them). A whoosh on a walkaround would announce the edit.")

SOUND = {
 "bed":       "BGM/car_cinematic/Neon Ice Show (chill phonk).mp3 - 98.0 BPM measured, the "
              "highest beat confidence (1115) of the 24 tracks in his library. CHILL phonk "
              "specifically: it has to sit under a voice for 15 of 23 seconds.",
 "sfx_policy":"none (see SFX_WAIVED)",
 "hero":      "HIS VOICE. There is no other hero sound and there should not be.",
 "hero_shot": 4,
 "duck_shots":[4],
 "silence":   "none - the bed runs throughout, ducking under the take",
}
FOLEY = {i: -12.0 for i in range(8)}
FOLEY[0] = -4.0                       # EVENT (the flare) - heard, per planqc 19
FOLEY[4] = 4.0                        # the take: his own audio, forward
FOLEY[7] = -5.0                        # the take: his own audio, forward
MIX = {
 "lufs_i_target": -12.0,
 "true_peak_max": -1.0,
 "master_limit":  0.63,
 "stereo":        "bed wide, voice centred",
 "duck_depth_db": -8,
 "duck_shape":    "sidechain, 30ms attack / 380ms release",
 "loudnorm":      "TWO-PASS",
 "bed_under":     6.0,                # POSITIVE: bed sits UNDER the voice. This film is
                                      # speech-led, so L128's negative (bed above foley)
                                      # is correctly INVERTED here - bedcheck's >=0 rule
                                      # assumes an ambience bed with no dialogue.
 "source":        "19-sound-engineer.md; measured on LOT_v3-v5",
}

CROP_XY = {}; BAN_SPANS = {}; DELOGO = {}
CALLBACKS = ["the RED X4 is the film's one object: it opens the hook, it is the car he "
             "singles out at the turn, and it sits behind the X5 in the closing frame."]
SHOT_WINDOW = {}

CARD_Y        = 0.72   # LOWER THIRD. His instruction 2026-08-17: "for a caption, can you
                       # not put it on the top of the video?" - and it restores the repo's
                       # own standing default (CLAUDE.md: "CAPTIONS y=0.72 lower third.
                       # Never centre - the subject lives there"). The 'card' register
                       # carries y=0.13 from the car_review references; his call overrides
                       # the reference, and the override is written here rather than
                       # patched into capcards, because the PLAN decides placement.
CARD_STYLE    = "fragment"
CARD_REGISTER = "card"
CARDS = [
 ("TALYX RECOND",        0, 4, "cap"),
 ("PM US",               7, 1, "cta"),   # lands on the held START button, after his ask
]
AI_LABEL_BURNED_IN = False              # NOT AI. Real footage of real cars. The disclosure
                                        # rule in CLAUDE.md applies to generated content;
                                        # labelling this would be a false statement.

RELATIONSHIPS = {
 "subject_vs_background": "A covered recond lot, rows of stock behind every shot. That "
   "background IS the product - it says 'there is inventory here' - so it is never cropped.",
 "performance_vs_sound": "He is on screen for the brand line and the CTA and nowhere else; "
   "the middle of the take is his voice over the cars he names.",
 "arc_vs_shot_order": "The order is his sentence. X1 then X5 then the red X4, because that "
   "is the order he says them - the arc is not imposed on the footage, it is read from it.",
 "bed_vs_foley": "The bed is the only non-voice layer and it ducks 8dB under him. In the "
   "four b-roll beats it comes up and carries the film alone.",
 "card_vs_card": "Two cards, 15s apart, never on screen together: TALYX RECOND opens, "
   "PM US closes ON the press itself, not after it.",
 "clip_variety_vs_shot_count": "8 shots from 8 distinct sources plus 5 cutaway sources - "
   "13 of the 60 clips used, no source twice.",
 "colour_vs_place": "Red X4 against white X5 and white X1 - the lot's own palette does the "
   "separating, so no grade is needed to tell the cars apart.",
 "event_vs_window": "The one EVENT (the flare, shot 0) sits in the first 1.2s, which is "
   "the only window a scroll gives you. The PAYOFF (START) is held 2.45s, the longest "
   "non-take shot, because a CTA needs time to be read.",
 "picture_grid_vs_music_grid": "The four hook beats and the two close beats sit ON the "
   "98 BPM grid; the 15.16s take does NOT - it runs to his sentence. Two grids, never "
   "mixed inside one block, which is the doctrine's rule stated for a hybrid.",
 "motion_vs_meaning": "The four beat shots are the only fast cutting; the take is one "
   "unbroken 15s. Motion serves the words rather than competing with them (L175).",
}
GRADE_SAT = 1.00; GRADE_BRI = 0.0; TARGET_BLACK = 8.0; TARGET_SAT = 70.0

CONTENT = {
 "claim": "TALYX has a BMW X1, an X5 and a red X4 on the lot right now.",
 "verified": ("Verified in the footage itself, not asserted: the X1 badge (clip 52), "
                  "the X5 badge (clip 34) and the X4 badge (clip 10) are all on screen at "
                  "full resolution, plus plates SWH 3190 and SJQ 2315. The claim and the "
                  "evidence are the same frames."),
 "hook": ("Four beat-cut frames of three different BMWs in 2.4s, then his voice: 'So guys, "
          "we are Talyx.' The scroll-stopper is INVENTORY, not motion - a recond buyer "
          "stops for a car they might buy. V1-V5 chose the hook by motion score and it "
          "stopped nobody."),
 "twist": ("THE REVERSAL IS AT 4.90s, when the montage stops and a PERSON is suddenly "
           "talking to you - a scroll expects b-roll and gets addressed directly. The "
           "second, smaller turn is at 14.38s when the list becomes an offer. He has named the X1 and the X5 as stock, "
           "then turns: 'or you are interested in X4, THIS RED ONE'. The viewer stops being "
           "an audience and becomes a customer being asked a question. It lands at 48% of "
           "runtime - late for a story, correct for a pitch, where the ask must follow the "
           "goods."),
 "twist_at": 4.90,
 "cta": ("So if you want to be interested, you PM me for a moment. "
         "Runs 16.16-18.80 in clip 48 - the LAST 1.7s of it sits in two speech runs of "
         "0.56s and 0.28s. V7 filtered phrases at a 0.8s minimum and therefore ENDED THE "
         "TAKE AT 17.12, amputating the ask itself. The end of a sentence is short and "
         "quiet by nature; a duration filter deletes exactly the words that matter (L180)."),
 "why_stop": ("It is 23 seconds and it ends on a finger pressing START on a car that is "
              "for sale, with PM US on screen. Nothing is withheld and nothing is padded."),
 "spine": "promise -> inventory -> the ask (a pitch, not kishotenketsu; declared, not defaulted)",
}
JOURNEY_WAIVED = ("Not a journey format. A journey (planqc 39) is owed by a VLOG, where the "
                  "process is the content. This is a 23-second inventory pitch recorded in "
                  "one place; there is no depart/transit/arrive and inventing one would pad it.")
CLIP_PACKAGE = ["the 4-beat hook stands alone as a 3-second stock teaser",
                "the X1/X5/X4 badge trio is a reusable 'what we have' card"]
PREVIZ = "n/a - real footage, see projects/lot/READ.md"
VOICE = "his own, clip 48"
PLATES = {}
CLIPS = {}

def timeline():
    """(start, DURATION, kind) - the shape planqc reads. 'beat' shots are one beat;
    'take' and 'hold' carry their length in seconds directly, because a 15s take is
    not a multiple of a beat and pretending otherwise would be a lie in the data."""
    out, t = [], 0.0
    gb = globals().get("GRID_BLENDS") or {}
    blends = set(gb.get("hook", []) + gb.get("close", []))
    for i, (_name, _w, kind, _why) in enumerate(SHOTS):
        d = BEATS[kind] * BEAT if kind == "beat" else BEATS[kind]
        # a dissolve OVERLAPS its two shots, so each blended boundary shortens the film
        if i in blends:
            d -= gb.get("d", 0.0)
        out.append((round(t, 4), round(d, 4), kind)); t += d
    return out, round(t, 4)

def cost():
    """ZERO. Nothing is generated - this is his own footage. Same dict shape as every
    other plan so check_cost reads it without a special case."""
    return {"per_clip": 0.0, "clips": 0, "generation": 0.0, "plates": 0.0,
            "total": 0.0, "probe": 0.0, "after_probe": 0.0}
