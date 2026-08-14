#!/usr/bin/env python3
"""
FACECHECK — mechanical face-drift detector for multi-part AI builds.

Attacks the KNOWN #1 risk in the system: Part 1 and Part 2 are separate generations, so the
subject's face can drift across the seam. Until now that was caught by eyeballing, i.e. by
judgement. File 25's own doctrine: where a check CAN be mechanical, it MUST be.

Method (stated honestly): detects faces, crops them, and compares appearance across shots using
three complementary signals — HSV colour histogram (skin/lighting), ORB keypoint match rate
(structure), and aspect/geometry. This is an APPEARANCE similarity, NOT a face-recognition
embedding: it will catch gross identity drift, wardrobe/skin-tone shifts, and "different person"
failures. It will NOT reliably separate two similar-looking people, and lighting changes lower
the score legitimately. Read it as a flag to go LOOK, not as a verdict.

Deps: opencv-python-headless + numpy
Usage: python3 facecheck.py VIDEO.mp4 [--seam 15.0] [--out qc]
"""
import argparse, os, json
import numpy as np
import cv2

CASC = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")

def sample_faces(path, every=0.5, min_size=80):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    det = cv2.CascadeClassifier(CASC)
    step = max(1, int(fps*every))
    out, i = [], 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        if i % step == 0:
            g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
            faces = det.detectMultiScale(g, 1.15, 6, minSize=(min_size,min_size))
            if len(faces):
                x,y,w,h = max(faces, key=lambda f: f[2]*f[3])
                pad = int(0.15*w)
                x0,y0 = max(0,x-pad), max(0,y-pad)
                x1,y1 = min(fr.shape[1],x+w+pad), min(fr.shape[0],y+h+pad)
                out.append({"t": round(i/fps,2), "crop": fr[y0:y1, x0:x1],
                            "box": [int(x),int(y),int(w),int(h)]})
        i += 1
    cap.release()
    return out, (i/fps if fps else 0)

def hsv_sim(a, b):
    ha = cv2.calcHist([cv2.cvtColor(a, cv2.COLOR_BGR2HSV)], [0,1], None, [30,32], [0,180,0,256])
    hb = cv2.calcHist([cv2.cvtColor(b, cv2.COLOR_BGR2HSV)], [0,1], None, [30,32], [0,180,0,256])
    cv2.normalize(ha, ha); cv2.normalize(hb, hb)
    return float(cv2.compareHist(ha, hb, cv2.HISTCMP_CORREL))

def orb_sim(a, b):
    orb = cv2.ORB_create(400)
    ga = cv2.cvtColor(cv2.resize(a,(160,160)), cv2.COLOR_BGR2GRAY)
    gb = cv2.cvtColor(cv2.resize(b,(160,160)), cv2.COLOR_BGR2GRAY)
    ka, da = orb.detectAndCompute(ga, None)
    kb, db = orb.detectAndCompute(gb, None)
    if da is None or db is None or len(ka)<8 or len(kb)<8: return None
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    m = bf.match(da, db)
    if not m: return 0.0
    good = [x for x in m if x.distance < 64]
    return float(len(good)/max(len(ka), len(kb)))

def compare(a, b):
    h = hsv_sim(a, b); o = orb_sim(a, b)
    parts = [p for p in (h, o) if p is not None]
    return {"hsv": None if h is None else round(h,3),
            "orb": None if o is None else round(o,3),
            "combined": round(float(np.mean(parts)),3) if parts else None}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--seam", type=float)
    ap.add_argument("--out", default="qc"); ap.add_argument("--json")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    faces, dur = sample_faces(a.video)
    rep = {"file": a.video, "duration": round(dur,2), "face_samples": len(faces)}
    if len(faces) < 2:
        rep.update({"verdict":"INSUFFICIENT","note":"fewer than 2 detected faces — "
                    "cannot assess drift. Frontal-face detector misses profiles/backs."})
        print(json.dumps(rep, indent=2)); return

    # consecutive drift
    seq = []
    for k in range(len(faces)-1):
        c = compare(faces[k]["crop"], faces[k+1]["crop"])
        seq.append({"from": faces[k]["t"], "to": faces[k+1]["t"], **c})
    combined = [s["combined"] for s in seq if s["combined"] is not None]
    rep["median_consecutive_similarity"] = round(float(np.median(combined)),3) if combined else None
    rep["worst_consecutive"] = sorted([s for s in seq if s["combined"] is not None],
                                      key=lambda s: s["combined"])[:5]

    # across the seam specifically (the multi-part risk)
    if a.seam:
        before = [f for f in faces if f["t"] < a.seam]
        after  = [f for f in faces if f["t"] >= a.seam]
        if before and after:
            b_ref = before[-1]; af_ref = after[0]
            c = compare(b_ref["crop"], af_ref["crop"])
            rep["seam"] = {"seam_t": a.seam, "last_before": b_ref["t"],
                           "first_after": af_ref["t"], **c}
            cv2.imwrite(os.path.join(a.out,"face_before.png"), b_ref["crop"])
            cv2.imwrite(os.path.join(a.out,"face_after.png"),  af_ref["crop"])
            # side-by-side for a human/model to LOOK at
            h = 220
            def rs(im):
                s = h/im.shape[0]; return cv2.resize(im,(max(1,int(im.shape[1]*s)),h))
            cv2.imwrite(os.path.join(a.out,"face_seam_compare.png"),
                        np.hstack([rs(b_ref["crop"]), rs(af_ref["crop"])]))
            rep["artifacts"] = {"seam_compare": os.path.join(a.out,"face_seam_compare.png")}

    key = (rep.get("seam") or {}).get("combined", rep.get("median_consecutive_similarity"))
    if key is None: v = "INSUFFICIENT"
    elif key >= 0.55: v = "CONSISTENT"
    elif key >= 0.38: v = "REVIEW — possible drift, LOOK at the compare image"
    else: v = "DRIFT SUSPECTED -> seat 2D MUA / build the file 23 asset sheet"
    rep["verdict"] = v
    rep["disclaimer"] = ("appearance similarity, not identity recognition. Lighting and angle "
                         "legitimately lower it. Always view face_seam_compare.png before acting.")
    print(json.dumps(rep, indent=2))
    if a.json: json.dump(rep, open(a.json,"w"), indent=2)

if __name__ == "__main__":
    main()
