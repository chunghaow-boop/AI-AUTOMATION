#!/usr/bin/env python3
"""
QC — one blocking checkpoint per phase. Nothing advances until its phase passes.

HIS REQUIREMENT, VERBATIM
  "every single phase must be QCed so that these things doesnt happen"
  "maybe everytime i give you an exam... go and search the web for related contents similar
   to the topic... analyze 5 to 10 of the contents then learn from it remember it save the
   skills then only start the generation"

WHY EVERY PHASE, NOT JUST THE END
  Cost of catching the same defect at each stage:
      research   free           the wrong idea never gets planned
      plan       free           the missing transitions column is visible on paper
      preflight  free           the 22.5-vs-17.5 cost error caught before the gate
      clip       17.5 cr        regenerate one clip
      delivery   the whole build, re-run, plus his review time
  Everything in this session that hurt was caught at the last possible stage.

PHASES
  0 research    >=5 references studied and SAVED before planning may start
  1 plan        the plan contains the fields whose absence caused past failures
  2 preflight   cost measured with the LITERAL params, never assumed
  3 clip        clipgate.py on every raw generation          (Layer 1)
  4 assemble    duration matches EDL; transitions actually rendered
  5 sound       peak, loudness band, silence gap present
  6 text        text present when the plan called for it
  7 deliver     verdict.py — blocking                        (Layer 2)

Every phase returns PASS or BLOCK. BLOCK stops the pipeline.

Usage
  python3 qc.py phase0 --topic "toyota crown cinematic"
  python3 qc.py phase1 --plan work/CROWN-PHASE1.md
  python3 qc.py phase4 --video work/_crown_tmp/cut.mp4 --expect 15.0 --tmp work/_crown_tmp
  python3 qc.py all --build crown
"""
import argparse, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
def _ledger_path(name):
    """work/ledgers/ is canonical (organizer.py moves them there); work/ is the legacy
    location. Look in both so a reorganise can never orphan a ledger again."""
    import os as _o
    _r = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__)))
    for c in (_o.path.join(_r, "work", "ledgers", name), _o.path.join(_r, "work", name)):
        if _o.path.exists(c): return c
    return _o.path.join(_r, "work", "ledgers", name)

KNOW = _ledger_path("knowledge.json")

def _k():
    if os.path.exists(KNOW):
        try: return json.load(open(KNOW, encoding="utf-8"))
        except Exception: pass
    return {"topics": {}}

def _ksave(d):
    os.makedirs(os.path.dirname(KNOW), exist_ok=True)
    json.dump(d, open(KNOW, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def ok(msg):    print(f"  PASS   {msg}"); return True
def bad(msg):   print(f"  BLOCK  {msg}"); return False

# ---------------------------------------------------------------- phase 0
def phase0(topic, minimum=5):
    """Research gate. A topic cannot be planned until >=`minimum` references have been
    studied AND what was learned is written down. Learning that is not saved is not learning -
    this session repeatedly re-derived things it had already worked out."""
    d = _k(); t = d["topics"].get(topic.lower())
    print(f"[phase 0] research — topic '{topic}'")
    if not t:
        return bad(f"no research on file. Study >={minimum} references, then:\n"
                   f"         python3 qc.py learn --topic \"{topic}\" --url U --lesson \"...\"")
    n = len(t.get("references", []))
    lastr = t.get("last_researched", "unknown")
    print(f"         {n} reference(s) studied, {len(t.get('lessons',[]))} lesson(s) saved")
    print(f"         last researched: {lastr}")
    try:
        from datetime import datetime
        age = (datetime.now() - datetime.strptime(lastr, "%Y-%m-%d")).days
        if age > 45:
            return bad(f"research is {age} days old. The meta moves - re-search before "
                       f"planning. Stale research that looks confident is the failure mode.")
    except Exception:
        pass
    for l in t.get("lessons", [])[:6]: print(f"           - {l}")
    if n < minimum:
        return bad(f"only {n}/{minimum} references studied")
    if not t.get("lessons"):
        return bad("references logged but nothing was learned from them")
    return ok(f"{n} references, {len(t['lessons'])} lessons")

def learn(topic, url=None, lesson=None):
    """Lessons are dated. What is true about a platform's meta this quarter may not be true
    next quarter - his point about references going out of date applies to research too."""
    from datetime import datetime
    d = _k(); t = d["topics"].setdefault(topic.lower(), {"references": [], "lessons": []})
    t["last_researched"] = datetime.now().strftime("%Y-%m-%d")
    if url and url not in t["references"]: t["references"].append(url)
    if lesson and lesson not in t["lessons"]: t["lessons"].append(lesson)
    _ksave(d)
    print(f"  saved: {len(t['references'])} refs, {len(t['lessons'])} lessons for '{topic}'")

# ---------------------------------------------------------------- phase 1
# Each required field exists because its ABSENCE caused a specific failure.
PLAN_FIELDS = {
    "transition": "the Crown timeline had NO transition column - 8 hard cuts shipped",
    "location":   "prompting the car but not the place gave a studio void",
    "reference":  "no locked plate -> a text-only prompt returned a crossover, and it shipped. "
                  "A 2cr nano_banana_pro plate prevents an 87cr build being wrong.",
    "foley":      "v2 shipped with no diegetic sound at all",
    "caption":    "v1 shipped with no captions",
    "cost":       "cost must be preflighted, not assumed (17.5 vs 22.5)",
}
def phase1(plan_path):
    print(f"[phase 1] plan — {os.path.basename(plan_path)}")
    if not os.path.exists(plan_path): return bad("plan file not found")
    txt = open(plan_path, encoding="utf-8", errors="ignore").read().lower()
    missing = [f"{k}  ({why})" for k, why in PLAN_FIELDS.items() if k not in txt]
    for k in PLAN_FIELDS:
        if k in txt: print(f"         has '{k}'")
    if missing:
        print()
        for m in missing: print(f"         MISSING {m}")
        return bad(f"{len(missing)} required plan element(s) absent")
    return ok("all required plan elements present")

# ---------------------------------------------------------------- phase 2
def phase2(quoted, measured):
    print(f"[phase 2] preflight — quoted {quoted} cr/clip, measured {measured} cr/clip")
    if abs(quoted-measured) > 0.01:
        return bad(f"quote is wrong by {abs(quoted-measured):.1f} cr/clip. "
                   f"Re-gate before spending. (This exact error was live at 17.5 vs 22.5.)")
    return ok("quote matches the measured cost")

# ---------------------------------------------------------------- phase 3
def phase3(folder, match, expect_dur=None, reference=None):
    print(f"[phase 3] clips — {match} in {folder}")
    import clipgate
    paths = sorted(glob.glob(os.path.join(folder, match)))
    if not paths: return bad("no clips found")
    rows = [clipgate.check(p, expect_dur, reference) for p in paths]
    good = clipgate.report(rows)
    if reference is None:
        return bad("NO REFERENCE PLATE — subject drift cannot be detected. "
                   "This is exactly how a crossover passed as a Crown.")
    return ok("all clips cleared") if good else bad("one or more clips must be regenerated")

# ---------------------------------------------------------------- phase 4
def phase4(video, expect, tmp):
    print(f"[phase 4] assemble — {os.path.basename(video)}")
    import build_kk as K
    d = K.dur(video); print(f"         duration {d:.2f}s (EDL {expect:.2f}s)")
    fails = []
    if abs(d-expect) > 0.35: fails.append(f"duration adrift {abs(d-expect):.2f}s")
    tx = glob.glob(os.path.join(tmp, "tx*.mp4"))
    print(f"         transitions rendered: {len(tx)}")
    if not tx:
        fails.append("ZERO transitions rendered — every cut is hard. "
                     "This shipped on the Crown build.")
    for f in fails: print(f"         x {f}")
    return ok("assembly sound") if not fails else bad(f"{len(fails)} failure(s)")

# ---------------------------------------------------------------- phase 5/6/7
def phase5(video, band=(-9.5,-6.5)):
    print(f"[phase 5] sound — {os.path.basename(video)}")
    import mastermind
    a = mastermind.audio_metrics(video)
    pk, lu = a.get("peak"), a.get("lufs")
    print(f"         peak {pk} dBTP   loudness {lu} LUFS")
    f=[]
    if pk is None or pk > -1.0: f.append(f"peak {pk} > -1.0")
    if lu is None or not (band[0] <= lu <= band[1]): f.append(f"loudness {lu} outside {band}")
    for x in f: print(f"         x {x}")
    return ok("sound within spec") if not f else bad(f"{len(f)} failure(s)")

def phase6(video):
    print(f"[phase 6] text — {os.path.basename(video)}")
    import verdict as V
    has = V._has_text(video)
    print(f"         text on screen: {'yes' if has else 'NO'}")
    return ok("text present") if has else bad("no text — the plan called for captions")

def phase7(video, expect=None, reference=None, ident=None):
    print(f"[phase 7] deliver")
    import verdict as V
    return ok("verdict PASS") if V.run(video, expect, True, reference, ident,
                                       quarantine=False) else bad("verdict BLOCKED")

def phase_profile(video, pillar):
    """Gate a finished build against the MEASURED profile for its pillar, not my assumptions.
    Source: 23 reference videos he selected. See assets/pillars/PILLAR-PROFILES.md"""
    import json as _j
    pf = os.path.join(ROOT, "assets", "pillars", "PILLAR-PROFILES.json")
    if not os.path.exists(pf): return bad("no pillar profile on file - run refstudy first")
    P = _j.load(open(pf)).get(pillar)
    if not P: return bad(f"no profile for pillar '{pillar}'")
    print(f"[profile] {pillar} — measured from his references")
    import pacing, refstudy
    r = refstudy._cuts_and_grade(video)
    fails = []
    tgt = P.get("shot_median_s")
    if tgt:
        got = r.get("shot_median", 0)
        print(f"         median shot   {got:.2f}s   target {tgt}s")
        if got > tgt * 1.6:
            fails.append(f"shots {got/tgt:.1f}x longer than his references ({got:.2f}s vs {tgt}s)")
    tb = P.get("blended_pct")
    if tb is not None:
        gb = r.get("blended_pct", 0)
        print(f"         blended cuts  {gb}%      target {tb}%")
        if tb >= 15 and gb < tb * 0.5:
            fails.append(f"only {gb}% blended transitions vs {tb}% in his references")
        if tb == 0 and gb > 15:
            fails.append(f"{gb}% blended, but this pillar uses hard cuts only")
    # ---------------------------------------------------------------- GRADE
    # THIS WAS THE HOLE. PILLAR-PROFILES.json stores 16 measured fields; this gate read
    # TWO of them (shot_median_s, blended_pct) and reported PASS. black_point and
    # saturation were measured from his 23 references and then never checked against
    # anything, by any gate, ever. A build shipped with 40% of every frame crushed to
    # pure black and qc.py said "matches the reference profile".
    #
    # refstudy._cuts_and_grade ALREADY returns black_point / white_point / saturation in
    # the same dict this function reads. The data was sitting there unused.
    tbp = P.get("black_point")
    if tbp is not None and r.get("black_point") is not None:
        gbp = r["black_point"]
        print(f"         black point   {gbp:.1f}      target {tbp}")
        if gbp > tbp + 12:
            fails.append(f"black point {gbp:.1f} vs {tbp} - lifted, washed out")
        if gbp < max(0.0, tbp - 2.0):
            fails.append(f"black point {gbp:.1f} vs {tbp} - crushed below the reference")
    tsat = P.get("saturation")
    if tsat is not None and r.get("saturation") is not None:
        gs = r["saturation"]
        print(f"         saturation    {gs:.1f}      target {tsat}")
        if abs(gs - tsat) > tsat * 0.30:
            fails.append(f"saturation {gs:.1f} vs {tsat} ({100*(gs-tsat)/tsat:+.0f}%)")

    # CLIPPING - a median black point cannot see this. 40% of the frame at value <4 is
    # destroyed detail, not a look, and it bands hard after platform compression.
    clip = _clip_pct(video)
    if clip is not None:
        print(f"         clipped <4    {clip:.1f}%     limit 12%")
        if clip > 12.0:
            fails.append(f"{clip:.0f}% of pixels crushed to pure black (limit 12%) - "
                         f"detail destroyed, likely a DOUBLE grade")

    # EXPOSURE CONTINUITY across cuts. clipsense.py measures brightness[] with the
    # docstring "for matching exposure across a cut" - nothing ever used it. Alternating
    # bright/dark shots at 0.8s reads as a strobe, not as energy.
    fl = _flicker(video, r.get("cut_times") or [])
    if fl is not None:
        n, tot, worst = fl
        print(f"         exposure jump {n}/{tot} cuts >18  (worst {worst:.0f})")
        if tot and n / tot > 0.33:
            fails.append(f"{n} of {tot} cuts swing brightness >18 - exposure flicker")

    for x in fails: print(f"         x {x}")
    return ok("matches the reference profile") if not fails else bad(f"{len(fails)} deviation(s)")


def _clip_pct(video, sample=6):
    """% of sampled pixels at value < 4 (pure black)."""
    try:
        import cv2, numpy as np
    except Exception:
        return None
    cap = cv2.VideoCapture(video); vals = []; i = 0
    while True:
        okf, fr = cap.read()
        if not okf: break
        if i % sample == 0:
            vals.append(cv2.cvtColor(cv2.resize(fr, (160, 284)), cv2.COLOR_BGR2GRAY))
        i += 1
    cap.release()
    if not vals: return None
    import numpy as np
    return float((np.stack(vals) < 4).mean() * 100)


def _flicker(video, cut_times, thresh=18.0):
    """Brightness delta across each cut. Returns (n_over, total, worst)."""
    try:
        import cv2, numpy as np
    except Exception:
        return None
    if not cut_times: return None
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frames = []
    while True:
        okf, fr = cap.read()
        if not okf: break
        frames.append(cv2.cvtColor(cv2.resize(fr, (96, 171)), cv2.COLOR_BGR2GRAY).mean())
    cap.release()
    if len(frames) < 4: return None
    n, worst = 0, 0.0
    for c in cut_times:
        a, b = int((c - 0.15) * fps), int((c + 0.15) * fps)
        if a < 0 or b >= len(frames): continue
        d = abs(frames[b] - frames[a])
        worst = max(worst, d)
        if d > thresh: n += 1
    return n, len(cut_times), worst

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd")
    p0=sub.add_parser("phase0"); p0.add_argument("--topic",required=True); p0.add_argument("--min",type=int,default=5)
    lr=sub.add_parser("learn"); lr.add_argument("--topic",required=True)
    lr.add_argument("--url"); lr.add_argument("--lesson")
    p1=sub.add_parser("phase1"); p1.add_argument("--plan",required=True)
    p2=sub.add_parser("phase2"); p2.add_argument("--quoted",type=float,required=True); p2.add_argument("--measured",type=float,required=True)
    p3=sub.add_parser("phase3"); p3.add_argument("--folder",default="work"); p3.add_argument("--match",required=True)
    p3.add_argument("--expect-duration",type=float); p3.add_argument("--reference")
    p4=sub.add_parser("phase4"); p4.add_argument("--video",required=True); p4.add_argument("--expect",type=float,required=True); p4.add_argument("--tmp",required=True)
    p5=sub.add_parser("phase5"); p5.add_argument("--video",required=True)
    p6=sub.add_parser("phase6"); p6.add_argument("--video",required=True)
    pp=sub.add_parser("profile"); pp.add_argument("--video",required=True); pp.add_argument("--pillar",required=True)
    p7=sub.add_parser("phase7"); p7.add_argument("--video",required=True); p7.add_argument("--expect",type=float); p7.add_argument("--reference"); p7.add_argument("--id")
    a=ap.parse_args()
    r=True
    if   a.cmd=="phase0": r=phase0(a.topic,a.min)
    elif a.cmd=="learn":  learn(a.topic,a.url,a.lesson)
    elif a.cmd=="phase1": r=phase1(a.plan)
    elif a.cmd=="phase2": r=phase2(a.quoted,a.measured)
    elif a.cmd=="phase3": r=phase3(a.folder,a.match,a.expect_duration,a.reference)
    elif a.cmd=="phase4": r=phase4(a.video,a.expect,a.tmp)
    elif a.cmd=="phase5": r=phase5(a.video)
    elif a.cmd=="phase6": r=phase6(a.video)
    elif a.cmd=="profile": r=phase_profile(a.video,a.pillar)
    elif a.cmd=="phase7": r=phase7(a.video,a.expect,a.reference,a.id)
    else: ap.print_help()
    return 0 if r else 1

if __name__=="__main__":
    sys.exit(main())
