#!/usr/bin/env python3
"""
PACING — retention-curve analyser. The piece that targets 50%+ directly.

Top creators design around a TARGET RETENTION CURVE, not a target length. This measures the
structural properties that produce that curve, per format, and names the exact timestamps
where a viewer is most likely to drop.

Measured (all from evidence, see 30-creator-mechanisms.md):
  - cuts per minute vs the format target   (vlog 15-25 · review 8-15 · industry 6-12)
  - shot-length distribution + DEAD ZONES  (>3s static stretch = drop risk)
  - cut-rate VARIATION                     (constant rhythm = monotony; top creators vary)
  - pattern-interrupt gaps                 (needs one every 30-60s)
  - the 4-part structure                   (hook 0-3s · value 4-15s · payoff 16-45s · CTA last 5s)
  - hook motion in 0-3s                    (if 30s retention <70%, fix the intro FIRST)

Deps: ffmpeg + opencv-python-headless + numpy
Usage: python3 pacing.py CUT.mp4 --format vlog|review|industry [--json out.json]
"""
import subprocess, json, argparse, sys
import numpy as np
import cv2

# evidence-based per-format targets
FORMATS = {
    "vlog":     {"cpm": (15, 25), "max_shot": 3.0, "shot_note": "jump-cut dead air out"},
    "review":   {"cpm": (8, 15),  "max_shot": 6.0, "shot_note": "education tolerates +5-10s"},
    "industry": {"cpm": (6, 12),  "max_shot": 8.0, "shot_note": "B2B: proof + on-screen data"},
    "hero":     {"cpm": (10, 30), "max_shot": 4.0, "shot_note": "cinematic, motion-led"},
    "car_edit": {"cpm": (40, 90), "max_shot": 1.6,
                 "shot_note": "phonk car edit: fast cut on the beat, 1-2 beats per shot"},
}
INTERRUPT_MAX_GAP = 60.0   # a pattern interrupt at least every 30-60s
HOOK_WINDOW       = 3.0

def analyse(path, fmt="vlog"):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    step = max(1, int(fps // 8))
    prev_h, prev_g = None, None
    cuts, flows, times, i = [], [], [], 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        if i % step == 0:
            t = i / fps
            g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
            small = cv2.resize(g, (160, 284))
            h = cv2.calcHist([g], [0], None, [64], [0, 256])
            h = cv2.normalize(h, h).flatten()
            if prev_h is not None:
                if cv2.compareHist(prev_h, h, cv2.HISTCMP_BHATTACHARYYA) > 0.45:
                    cuts.append(round(t, 2))
            if prev_g is not None:
                f = cv2.calcOpticalFlowFarneback(prev_g, small, None, .5,3,15,3,5,1.2,0)
                flows.append(float(np.linalg.norm(f, axis=2).mean())); times.append(t)
            prev_h, prev_g = h, small
        i += 1
    cap.release()
    dur = i / fps if fps else 0
    T = FORMATS.get(fmt, FORMATS["vlog"])

    # shot lengths
    bounds = [0.0] + cuts + [dur]
    shots = [round(bounds[k+1]-bounds[k], 2) for k in range(len(bounds)-1)]
    cpm = len(cuts) / (dur/60) if dur else 0

    # dead zones: long shots with low motion = the real drop risk
    dead = []
    for k, s in enumerate(shots):
        if s > T["max_shot"]:
            a, b = bounds[k], bounds[k+1]
            seg = [f for f, t in zip(flows, times) if a <= t < b]
            mo = float(np.mean(seg)) if seg else 0.0
            dead.append({"start": round(a,2), "len": s, "motion": round(mo,3),
                         "severity": "HIGH" if mo < 0.35 else "med"})

    # cut-rate variation across 10s windows (monotony detector)
    win, rates = 10.0, []
    if dur > win:
        for w0 in np.arange(0, dur-win/2, win):
            rates.append(sum(1 for c in cuts if w0 <= c < w0+win))
        variation = float(np.std(rates)) if len(rates) > 1 else 0.0
    else:
        variation = 0.0

    # pattern-interrupt gaps
    marks = [0.0] + cuts + [dur]
    gaps = [{"from": round(marks[k],2), "gap": round(marks[k+1]-marks[k],2)}
            for k in range(len(marks)-1) if marks[k+1]-marks[k] > INTERRUPT_MAX_GAP]

    # hook
    hook = [f for f, t in zip(flows, times) if t <= HOOK_WINDOW]
    hook_motion = float(np.mean(hook)) if hook else 0.0
    hook_cuts = sum(1 for c in cuts if c <= HOOK_WINDOW)

    # structure presence
    structure = {
        "hook_0_3s":      {"cuts": hook_cuts, "motion": round(hook_motion,3),
                           "ok": hook_motion >= 0.35},
        "value_4_15s":    {"cuts": sum(1 for c in cuts if 4 <= c <= 15),
                           "ok": dur < 15 or sum(1 for c in cuts if 4 <= c <= 15) >= 1},
        "payoff_16_45s":  {"cuts": sum(1 for c in cuts if 16 <= c <= 45),
                           "ok": dur < 16 or sum(1 for c in cuts if 16 <= c <= 45) >= 1},
        "cta_last_5s":    {"cuts": sum(1 for c in cuts if c >= dur-5), "ok": True},
    }

    lo, hi = T["cpm"]
    findings, seats = [], []
    if cpm < lo:
        findings.append(f"CUTS TOO SLOW: {cpm:.1f}/min vs {lo}-{hi} for {fmt} -> Editor")
        seats.append("Editor")
    elif cpm > hi:
        findings.append(f"CUTS TOO FAST: {cpm:.1f}/min vs {lo}-{hi} for {fmt} -> Editor")
        seats.append("Editor")
    for d in dead:
        if d["severity"] == "HIGH":
            findings.append(f"DEAD ZONE @{d['start']}s ({d['len']}s, motion {d['motion']}) "
                            f"-> Editor/Director: cut it or add a pattern interrupt")
            seats.append("Editor")
    for g in gaps:
        findings.append(f"NO INTERRUPT for {g['gap']}s from {g['from']}s -> Editor")
    if not structure["hook_0_3s"]["ok"]:
        findings.append(f"HOOK STATIC: motion {hook_motion:.2f} <0.35 in first 3s -> J0. "
                        f"If 30s retention <70%, fix the intro before anything else.")
        seats.append("J0")
    if variation < 0.6 and dur > 20:
        findings.append(f"MONOTONOUS RHYTHM: cut-rate sd {variation:.2f}; top creators VARY "
                        f"pace (fast on energy, slow on the important beat) -> Editor")

    # retention estimate — heuristic, NOT a measurement. Labelled as such.
    penalty = 0
    penalty += 12 * sum(1 for d in dead if d["severity"]=="HIGH")
    penalty += 15 if not structure["hook_0_3s"]["ok"] else 0
    penalty += 8 if (cpm < lo or cpm > hi) else 0
    penalty += 6 if variation < 0.6 and dur > 20 else 0
    penalty += 10 * len(gaps)
    base = 62 if dur <= 30 else (52 if dur <= 60 else 42)
    est = max(10, base - penalty)

    return {
        "file": path, "format": fmt, "duration": round(dur,2), "fps": round(fps,2),
        "cuts": len(cuts), "shot_cuts": cuts, "shot_lengths": shots,
        "cuts_per_min": round(cpm,1), "target_cpm": list(T["cpm"]),
        "shot_len_median": round(float(np.median(shots)),2) if shots else 0,
        "shot_len_max": round(max(shots),2) if shots else 0,
        "cut_rate_variation": round(variation,2),
        "dead_zones": dead, "interrupt_gaps": gaps,
        "hook": {"motion": round(hook_motion,3), "cuts": hook_cuts,
                 "ok": structure["hook_0_3s"]["ok"]},
        "structure": structure,
        "findings": findings, "seats_to_fix": sorted(set(seats)),
        "retention_estimate_pct": est,
        "estimate_disclaimer": ("HEURISTIC from structural features only — NOT a measurement "
                                "and NOT a promise. Only the real 24h curve validates this. "
                                "Log predicted vs actual in 09-learning-log.md."),
        "verdict": "PASS" if not findings else "SEND BACK",
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("video"); p.add_argument("--format", default="vlog", choices=list(FORMATS))
    p.add_argument("--json")
    a = p.parse_args()
    r = analyse(a.video, a.format)
    print(json.dumps(r, indent=2))
    if a.json: json.dump(r, open(a.json,"w"), indent=2)

if __name__ == "__main__":
    main()
