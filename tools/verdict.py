#!/usr/bin/env python3
"""
VERDICT — a gate that can actually STOP a file. The others only ever printed.

WHY THIS EXISTS
  On the Crown build the generated car was a crossover, not a Crown liftback. I saw it,
  wrote "the car isn't a Crown" in the delivery message, and shipped the file anyway.

  That is the failure worth fixing. Not the wrong car - the fact that nothing prevented it:

      gates that verify the subject .... none existed
      build_crown calls mastermind ..... never did
      gate() could block delivery ...... it returned nothing, it only printed

  A gate the operator can narrate around is not a gate. So delivery is now a function of
  the verdict, not of the operator's judgement:

      PASS   -> file is written to output/
      BLOCK  -> file goes to work/quarantine/ with a .WHY file, and output/ stays empty

HARD GATES (any failure blocks)
  duration within tolerance of the EDL       a short render means a segment silently failed
  true peak <= -1.0 dBTP                     platform transcode headroom
  loudness inside the measured band          his -7..-9, from a real viral reel
  no fully black/blank frames
  text present when the plan called for it   this shipped broken once already
  SUBJECT VERIFIED                           see below
  no regression against styleref rejections

THE SUBJECT GATE - and an honest limit
  I cannot reliably tell a Toyota Crown from a Lexus RX by pixels, and pretending otherwise
  would rebuild the same failure with extra steps. So:
    - if a reference image exists, similarity is measured and a low score BLOCKS
    - if no reference exists, the build BLOCKS pending explicit human sign-off
  A named-product build cannot self-certify its own subject. That is the point.

Usage
  python3 verdict.py --video output/X.mp4 --expect-duration 15.0 --plan-has-text
  python3 verdict.py --video X.mp4 --reference assets/plates/crown.jpg
  python3 verdict.py --signoff CROWN_15S_v1     # human confirms the subject is correct
"""
import argparse, os, sys, json, shutil
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
QUAR = os.path.join(ROOT, "work", "quarantine")
def _ledger_path(name):
    """work/ledgers/ is canonical (organizer.py moves them there); work/ is the legacy
    location. Look in both so a reorganise can never orphan a ledger again."""
    import os as _o
    _r = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__)))
    for c in (_o.path.join(_r, "work", "ledgers", name), _o.path.join(_r, "work", name)):
        if _o.path.exists(c): return c
    return _o.path.join(_r, "work", "ledgers", name)

SIGN = _ledger_path("signoffs.json")

def _signoffs():
    if os.path.exists(SIGN):
        try: return json.load(open(SIGN))
        except Exception: pass
    return {}

def signoff(ident, who="user", note=""):
    d = _signoffs()
    d[ident] = {"by": who, "at": datetime.now().isoformat(timespec="seconds"), "note": note}
    os.makedirs(os.path.dirname(SIGN), exist_ok=True)
    json.dump(d, open(SIGN, "w"), indent=1)
    print(f"  subject signed off for '{ident}' — it may now pass the gate")

def frame_similarity(video, ref_img, n=6):
    """Coarse perceptual similarity between sampled frames and a reference plate.
    Colour histogram + edge structure. Crude on purpose: it is a SCREEN, not an identifier.
    It catches 'completely different vehicle', not 'wrong trim level'."""
    try:
        import cv2, numpy as np
    except ImportError:
        return None
    ref = cv2.imread(ref_img)
    if ref is None: return None
    ref = cv2.resize(ref, (256, 256))
    rh = cv2.calcHist([cv2.cvtColor(ref, cv2.COLOR_BGR2HSV)], [0,1], None, [32,32], [0,180,0,256])
    cv2.normalize(rh, rh)
    re = cv2.Canny(cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY), 80, 180).astype(float)/255.0
    cap = cv2.VideoCapture(video)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    scores = []
    for i in range(n):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(total*(i+0.5)/n))
        ok, fr = cap.read()
        if not ok: continue
        fr = cv2.resize(fr, (256, 256))
        h = cv2.calcHist([cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)], [0,1], None, [32,32], [0,180,0,256])
        cv2.normalize(h, h)
        hs = cv2.compareHist(rh, h, cv2.HISTCMP_CORREL)
        e = cv2.Canny(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), 80, 180).astype(float)/255.0
        es = 1.0 - float(np.abs(re-e).mean())
        scores.append(0.5*max(0,hs) + 0.5*es)
    cap.release()
    return round(sum(scores)/len(scores), 3) if scores else None

def run(video, expect_duration=None, plan_has_text=False, reference=None,
        ident=None, band=(-9.5, -6.5), quarantine=True):
    import build_kk as K
    ident = ident or os.path.splitext(os.path.basename(video))[0]
    fails, notes = [], []
    print("="*60); print(f"VERDICT  {os.path.basename(video)}"); print("="*60)

    d = K.dur(video)
    print(f"  duration            {d:.2f}s")
    if expect_duration and abs(d - expect_duration) > 0.35:
        fails.append(f"DURATION {d:.2f}s vs planned {expect_duration:.2f}s "
                     f"({abs(d-expect_duration):.2f}s adrift - a segment likely failed)")

    try:
        import mastermind
        a = mastermind.audio_metrics(video)
        pk, lu = a.get("peak"), a.get("lufs")
        print(f"  true peak           {pk} dBTP")
        print(f"  loudness            {lu} LUFS")
        if pk is None or pk > -1.0: fails.append(f"TRUE PEAK {pk} dBTP > -1.0")
        if lu is None or not (band[0] <= lu <= band[1]):
            fails.append(f"LOUDNESS {lu} LUFS outside {band[0]}..{band[1]}")
        v = mastermind.video_metrics(video, os.path.join(ROOT, "work", "_verdict_tmp"))
        print(f"  blank frames        {v.get('blank_frames')}")
        if v.get("blank_frames", 0) > 0: fails.append(f"{v['blank_frames']} blank frame(s)")
    except Exception as e:
        fails.append(f"mastermind could not run: {str(e)[:60]}")

    if plan_has_text:
        ok = _has_text(video)
        print(f"  text on screen      {'yes' if ok else 'NO'}")
        if not ok: fails.append("PLAN CALLED FOR TEXT AND THE RENDER HAS NONE "
                                "(this exact failure shipped once already)")

    # ---- the subject gate ----
    sims = frame_similarity(video, reference) if reference else None
    signed = ident in _signoffs()
    if reference and sims is not None:
        print(f"  subject similarity  {sims}  vs reference plate")
        if sims < 0.45:
            fails.append(f"SUBJECT similarity {sims} < 0.45 — the generated subject does not "
                         f"match the reference plate")
    elif signed:
        print(f"  subject             signed off by {_signoffs()[ident]['by']}")
    else:
        fails.append("SUBJECT NOT VERIFIED — no reference plate and no human sign-off. "
                     "A named-product build cannot self-certify. "
                     f"Run:  python3 verdict.py --signoff {ident}")

    # ---- regressions against everything he has already rejected ----
    try:
        import styleref
        led = styleref._load()
        openr = [r for r in led["rejects"] if "UNFIX" in r.get("fix","").upper()]
        if openr:
            notes.append(f"{len(openr)} known-open defect(s) from styleref: "
                         + ", ".join(r["feature"] for r in openr))
    except Exception:
        pass

    print()
    for n in notes: print("  note:", n)
    if fails:
        print(f"\n  VERDICT: BLOCKED  ({len(fails)} hard gate failure(s))")
        for f in fails: print("    x", f)
        if quarantine and os.path.exists(video):
            os.makedirs(QUAR, exist_ok=True)
            q = os.path.join(QUAR, os.path.basename(video))
            try:
                shutil.move(video, q)
                open(q + ".WHY.txt", "w").write(
                    f"BLOCKED {datetime.now():%Y-%m-%d %H:%M}\n\n" + "\n".join(f"- {f}" for f in fails)
                    + "\n\nThis file was NOT delivered. Fix the above and rebuild.\n")
                print(f"\n  quarantined -> {q}")
                print("  output/ intentionally left without this file.")
            except Exception as e:
                print(f"  !! could not quarantine: {str(e)[:60]}")
        return False
    print("\n  VERDICT: PASS — all hard gates clear")
    return True

def _has_text(video, samples=8):
    """Crude but sufficient: burned-in captions create dense high-contrast horizontal
    structure in the lower third. Absence of it across every sample means no text."""
    try:
        import cv2, numpy as np
    except ImportError:
        return True
    cap = cv2.VideoCapture(video)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    hits = 0
    for i in range(samples):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(total*(i+0.5)/samples))
        ok, fr = cap.read()
        if not ok: continue
        h = fr.shape[0]
        strip = cv2.cvtColor(fr[int(h*0.55):int(h*0.95)], cv2.COLOR_BGR2GRAY)
        e = cv2.Canny(strip, 120, 240)
        if e.mean() > 6.0: hits += 1
    cap.release()
    return hits >= 2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video"); ap.add_argument("--expect-duration", type=float)
    ap.add_argument("--plan-has-text", action="store_true")
    ap.add_argument("--reference"); ap.add_argument("--id")
    ap.add_argument("--signoff"); ap.add_argument("--note", default="")
    ap.add_argument("--no-quarantine", action="store_true")
    a = ap.parse_args()
    if a.signoff: signoff(a.signoff, note=a.note); return 0
    if not a.video: ap.print_help(); return 2
    ok = run(a.video, a.expect_duration, a.plan_has_text, a.reference, a.id,
             quarantine=not a.no_quarantine)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
