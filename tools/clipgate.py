#!/usr/bin/env python3
"""
CLIPGATE — Layer 1 of the double crosscheck. Gates every RAW generation before it is edited.

THE GAP THIS FILLS
  There were two places a bad clip could be caught and only one existed:

      LAYER 1  each raw generation, at ingest      <- did not exist
      LAYER 2  the finished film, at delivery      <- verdict.py

  On the Crown build I generated 4 clips and put all 4 straight into the edit without ever
  inspecting one of them. The crossover-instead-of-Crown was visible in the very first frame
  of two clips. It surfaced only after editing, foley, captions and a full render.

  Catching it here is strictly cheaper:
      caught at Layer 1   17.5 cr to regenerate one clip
      caught at Layer 2   the whole build is wasted and re-run

  His note: "I thought the AI VIDEO GENERATION part is already settled". Fidelity IS settled -
  the frames are beautiful. ADHERENCE is not: the model drifts off-subject and nothing was
  checking. Those are different problems and I treated them as one.

CHECKS PER CLIP
  format      resolution, aspect, fps, duration vs what was ordered
  black       fully black / blown frames anywhere
  static      mean optical flow - a frozen "video" is a still that cost 17.5 cr
  exposure    clipped blacks or whites across the whole clip
  subject     similarity to a locked reference plate, when one exists
  usable_in   where the real motion starts (AI clips open with a settle)

VERDICT PER CLIP:  ACCEPT · WARN · REGENERATE

Usage
  python3 clipgate.py --scan work/ --match "CROWN_*.mp4" --expect-duration 5
  python3 clipgate.py --clip work/CROWN_A_macro.mp4 --reference assets/plates/crown.jpg
"""
import argparse, glob, os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

def check(path, expect_duration=None, reference=None, min_motion=0.25,
          want_w=720, want_h=1280):
    import numpy as np, cv2
    r = {"file": os.path.basename(path), "fails": [], "warns": []}
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    n   = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    dur = n/fps if fps else 0
    r.update({"w": w, "h": h, "fps": round(fps,2), "duration": round(dur,2)})
    if (w, h) != (want_w, want_h):
        r["fails"].append(f"resolution {w}x{h}, expected {want_w}x{want_h}")
    if expect_duration and abs(dur-expect_duration) > 0.4:
        r["fails"].append(f"duration {dur:.2f}s, ordered {expect_duration}s")

    prev=None; mot=[]; blacks=0; blown=0; means=[]; dif=[]; dift=[]; prev_all=None
    step=max(1,int(fps//8) if fps else 3); i=0
    while True:
        ok, fr = cap.read()
        if not ok: break
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        small_all = cv2.resize(g,(160,284)).astype(np.float32)
        # frame differencing runs at FULL rate, deliberately. Measured on the r8ride
        # batch: at the step=3 subsample a real cut in a high-motion clip fell to
        # 3.0x peak/mean and slipped under the threshold, because 0.125s-apart frames
        # make ordinary motion look like a cut and inflate the mean. Full rate put the
        # same cut at 6.1x. Subsampling here made the check VACUOUS for exactly the
        # clips most likely to contain one.
        if prev_all is not None:
            dif.append(float(np.abs(small_all-prev_all).mean())); dift.append(i/max(fps,1))
        prev_all = small_all
        if i % step == 0:
            m = float(g.mean()); means.append(m)
            if m < 6: blacks += 1
            if m > 248: blown += 1
            small = small_all.astype(np.uint8)
            if prev is not None:
                f2 = cv2.calcOpticalFlowFarneback(prev, small, None,.5,3,15,3,5,1.2,0)
                mot.append(float(np.linalg.norm(f2,axis=2).mean()))
            prev = small
        i += 1
    cap.release()
    if not means:
        r["fails"].append("unreadable"); r["verdict"]="REGENERATE"; return r

    mm = float(np.mean(mot)) if mot else 0.0
    r["motion_mean"] = round(mm,3)
    r["brightness"] = round(float(np.mean(means))/255,3)
    r["black_frames"] = blacks; r["blown_frames"] = blown
    if blacks: r["fails"].append(f"{blacks} black frame(s)")
    if blown:  r["warns"].append(f"{blown} blown frame(s)")
    if mm < min_motion:
        r["fails"].append(f"static: mean flow {mm:.3f} < {min_motion} "
                          f"(this is a still that cost a video generation)")
    elif mm < min_motion*2:
        r["warns"].append(f"low motion {mm:.3f} - will need animate.enliven()")

    # ---- INTERNAL CUT DETECTION -------------------------------------------
    # Added 2026-08-14 (L166). The generator does not always return ONE take.
    # On r8ride, 2 of 6 clips came back as two-shot clips with a hard cut inside
    # them, and NOTHING in this gate looked for it: shot C cut at 3.26s and on
    # the far side a torque wrench turned with no hand on it (a floating tool,
    # explicitly banned in its own prompt). It was found by eye on a contact
    # sheet - which is exactly the failure this repo is trying to stop.
    #
    # An internal cut is NOT automatically a defect: on the same batch shot D
    # cut at 2.72s into a matched second angle of the same dust-sheet pull and
    # was stronger for it. So this does not REGENERATE. It forces the thing that
    # was missing: EACH SIDE OF THE CUT IS A SEPARATE CLIP AND IS JUDGED ON ITS
    # OWN MERITS (his adjustment 2, 2026-08-12).
    r["internal_cuts"] = []
    if len(dif) >= 8:
        dm = float(np.mean(dif)); ds = float(np.std(dif))
        thr = max(dm*3.5, dm + 4*ds)
        r["cut_ratio"] = round(float(np.max(dif))/dm, 1) if dm else 0.0
        r["internal_cuts"] = [round(dift[k],2) for k,v in enumerate(dif) if v > thr]
        if r["internal_cuts"]:
            r["warns"].append(
                f"INTERNAL CUT at {r['internal_cuts']}s (peak/mean {r['cut_ratio']}x) - "
                f"this is a {len(r['internal_cuts'])+1}-shot clip, not one take. "
                f"JUDGE EACH SIDE SEPARATELY before it enters the edit.")

    # where does it actually start moving?
    if mot:
        med = float(np.median(mot)) or 1e-6
        head = next((k for k,v in enumerate(mot) if v >= med*0.6), 0)
        r["usable_in_s"] = round(head*step/max(fps,1), 2)
        if r["usable_in_s"] > 1.0:
            r["warns"].append(f"first {r['usable_in_s']}s is a settle - trim it")

    if reference and os.path.exists(reference):
        try:
            import verdict as V
            s = V.frame_similarity(path, reference)
            r["subject_similarity"] = s
            if s is not None and s < 0.45:
                r["fails"].append(f"SUBJECT similarity {s} < 0.45 vs the reference plate")
        except Exception as e:
            r["warns"].append(f"subject check unavailable: {str(e)[:40]}")
    else:
        r["warns"].append("no reference plate - subject cannot be verified automatically")

    r["verdict"] = "REGENERATE" if r["fails"] else ("WARN" if r["warns"] else "ACCEPT")
    return r

def report(rows, cost_per_clip=17.5):
    print("="*66); print("CLIPGATE — Layer 1: raw generations, before any editing"); print("="*66)
    bad=[]
    for r in rows:
        v=r["verdict"]
        print(f"\n  [{v}] {r['file']}")
        print(f"     {r.get('w')}x{r.get('h')} @{r.get('fps')}fps  {r.get('duration')}s  "
              f"motion {r.get('motion_mean')}  bright {r.get('brightness')}"
              + (f"  subj {r['subject_similarity']}" if r.get("subject_similarity") is not None else ""))
        for f in r["fails"]: print(f"     x {f}")
        for w in r["warns"]: print(f"     ~ {w}")
        if r.get("internal_cuts"):
            print(f"     ! NOT ONE TAKE — sides to judge: "
                  + " | ".join(f"{s:.2f}-{e:.2f}s" for s,e in
                    zip([0.0]+r["internal_cuts"], r["internal_cuts"]+[r.get('duration',0)])))
        if v=="REGENERATE": bad.append(r["file"])
    print("\n" + "="*66)
    acc=sum(1 for r in rows if r["verdict"]=="ACCEPT")
    wrn=sum(1 for r in rows if r["verdict"]=="WARN")
    print(f"  ACCEPT {acc}   WARN {wrn}   REGENERATE {len(bad)}")
    if bad:
        print(f"\n  DO NOT EDIT THESE — regenerate first: {', '.join(bad)}")
        print(f"  cost to fix now: {len(bad)*cost_per_clip:.1f} cr")
        print(f"  cost if it reaches delivery instead: the whole build, re-run")
    else:
        print("  all clips cleared to enter the edit")
    return not bad

def selftest():
    """NEGATIVE CONTROL for the internal-cut check (L169: a gate ships PROVEN or not at all).

    Synthesises two clips with ffmpeg and asserts the check gets both right:
      one-take   a continuous pan          -> MUST report no internal cut
      two-shot   two sources spliced hard  -> MUST report the cut, near 2.5s
    A check that fires on everything is as useless as one that fires on nothing,
    so the one-take case is the half that actually proves it.
    """
    import subprocess, tempfile
    d = tempfile.mkdtemp(); ok = True
    one = os.path.join(d, "onetake.mp4"); two = os.path.join(d, "twoshot.mp4")
    common = ["-c:v","libx264","-pix_fmt","yuv420p","-r","24","-y"]
    # one take: a single source with continuous motion (a slow zoom on noise)
    subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i",
                    "testsrc2=size=720x1280:rate=24:duration=5",
                    "-vf","zoompan=z='min(zoom+0.0006,1.3)':d=1:s=720x1280"]+common+[one],check=True)
    # two shot: 2.5s of one pattern hard-spliced to 2.5s of a very different one
    a1=os.path.join(d,"a1.mp4"); a2=os.path.join(d,"a2.mp4")
    subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i",
                    "testsrc2=size=720x1280:rate=24:duration=2.5"]+common+[a1],check=True)
    subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i",
                    "smptebars=size=720x1280:rate=24:duration=2.5"]+common+[a2],check=True)
    lst=os.path.join(d,"l.txt"); open(lst,"w").write(f"file '{a1}'\nfile '{a2}'\n")
    subprocess.run(["ffmpeg","-v","error","-f","concat","-safe","0","-i",lst,"-c","copy","-y",two],check=True)

    print("="*66); print("CLIPGATE SELFTEST — internal cut detection"); print("="*66)
    r1 = check(one, min_motion=0.0); r2 = check(two, min_motion=0.0)

    if r1.get("internal_cuts"):
        print(f"  UNPROVEN  false positive: one-take clip reported cuts at {r1['internal_cuts']}"); ok=False
    else:
        print("  PROVEN    one-take clip -> no internal cut reported")

    cuts = r2.get("internal_cuts") or []
    if not cuts:
        print(f"  UNPROVEN  MISSED the splice (peak/mean {r2.get('cut_ratio')}x) - check is VACUOUS"); ok=False
    elif not any(abs(c-2.5) <= 0.4 for c in cuts):
        print(f"  UNPROVEN  fired at {cuts}s but the real splice is at 2.50s"); ok=False
    else:
        print(f"  PROVEN    two-shot clip -> cut found at {cuts}s (splice is 2.50s), "
              f"peak/mean {r2.get('cut_ratio')}x")

    print("="*66); print("  SELFTEST PASS" if ok else "  SELFTEST FAIL — do not trust this check")
    return ok

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--clip"); ap.add_argument("--scan"); ap.add_argument("--match", default="*.mp4")
    ap.add_argument("--expect-duration", type=float); ap.add_argument("--reference")
    ap.add_argument("--json"); ap.add_argument("--selftest", action="store_true")
    a=ap.parse_args()
    if a.selftest: return 0 if selftest() else 1
    paths=[a.clip] if a.clip else sorted(glob.glob(os.path.join(a.scan or ".", a.match)))
    if not paths: print("no clips found"); return 2
    rows=[check(p, a.expect_duration, a.reference) for p in paths]
    ok=report(rows)
    if a.json: json.dump(rows, open(a.json,"w"), indent=2)
    return 0 if ok else 1

if __name__=="__main__":
    sys.exit(main())
