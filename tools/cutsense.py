#!/usr/bin/env python3
"""
CUTSENSE — the three things nothing in this repo currently measures on a FINISHED cut.

ADDITIVE BY DESIGN, 2026-08-05. This file touches nothing. It does not import, patch or
modify verify.py, planqc.py, engine.py, clipqc.py or qc.py, and nothing depends on it.
Run it or don't. It exists because three complaints have been made repeatedly by eye and
ear and none of them has a number behind it yet:

  1 "it doesn't hit"          -> DYNAMICS. Measured on WRX_CINEMATIC_v9: LRA 1.0 LU. The
                                 whole 20.8s sits at one loudness. A music-led edit lives on
                                 contrast and there was none. Integrated LUFS and true peak
                                 were both in band, so every existing gate passed it.
  2 "alot of reused scenes"   -> REPETITION, far apart. Adjacent-shot checks exist. Shot-to-
                                 shot across the WHOLE timeline does not. v9 measured SEVEN
                                 pairs over 0.90 histogram correlation in 15 shots, worst
                                 0.984. All of them non-adjacent, so nothing saw them.
  3 "nothing happens"         -> EVENT CURVE. Every check measures conformance to a profile;
                                 none asks whether anything OCCURS, or whether the loudest
                                 visual moment is anywhere near the hook.

None of it blocks. It prints numbers and leaves the verdict to the eye that owns it.

USAGE
  python3 tools/cutsense.py path/to/cut.mp4
  python3 tools/cutsense.py path/to/cut.mp4 --json out.json

WHY THE THRESHOLDS ARE SOFT
  LRA >= 4.0 LU and hist-corr <= 0.90 are STRUCTURAL CHOICES, not measurements. They are
  declared here as choices so nobody later cites them as findings. Re-derive both from
  references, or from the first posted video's real numbers, whichever comes first.
"""
import os, sys, json, math, subprocess, argparse

try:
    import cv2, numpy as np
except ImportError:
    sys.exit("cutsense needs opencv-python and numpy (both already used by clipqc.py)")

LRA_FLOOR      = 4.0     # CHOICE. v9 measured 1.0.
REPEAT_CORR    = 0.90    # CHOICE. v9 had 7 pairs above it.
CUT_CORR       = 0.55    # CHOICE. below this, two sampled frames are different shots.
HOOK_S         = 3.0     # TikTok Q2 2026 ranks 3s retention above watch time.


# ---------------------------------------------------------------- 0 FRESHNESS
def freshness(path):
    """CHECK 0 EVERYWHERE ELSE IN THIS REPO, AND FOR THE SAME REASON: a build that timed
    out before its atomic write leaves the PREVIOUS render on disk, and then every number
    below is fiction."""
    import time
    st = os.stat(path)
    age_min = (time.time() - st.st_mtime) / 60.0
    return {"path": path, "bytes": st.st_size, "age_min": round(age_min, 1),
            "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))}


# ---------------------------------------------------------------- 1 DYNAMICS
def dynamics(path):
    """Integrated loudness, LOUDNESS RANGE and true peak, straight from ffmpeg's ebur128.

    LRA is the one this repo has never printed. Integrated LUFS says how loud the file is;
    LRA says whether it goes anywhere. A brick-walled edit passes every loudness gate ever
    written and still feels like nothing happens."""
    # NO '-v error' HERE. ebur128 prints its summary block at INFO level, so quieting
    # ffmpeg silently returns None for every number and the check reports 'ok' on a file
    # it never measured. Caught on the first run against WRX v9 - a check that cannot fail
    # loudly enough to notice it measured nothing is worse than no check.
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
                        "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    out = {}
    lines = r.stderr.splitlines()
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("I:") and "LUFS" in s:
            out["integrated_lufs"] = float(s.split()[1])
        elif s.startswith("LRA:"):
            out["lra_lu"] = float(s.split()[1])
        elif s.startswith("Peak:") and "dBFS" in s:
            out["true_peak_dbfs"] = float(s.split()[1])
    out["lra_floor_choice"] = LRA_FLOOR
    if "lra_lu" not in out:
        out["measured"] = False          # say so LOUDLY rather than pass by default
        out["flat"] = None
    else:
        out["measured"] = True
        out["flat"] = out["lra_lu"] < LRA_FLOOR
    return out


# ---------------------------------------------------------------- shot detection
def _hist(f):
    h = cv2.calcHist([cv2.cvtColor(f, cv2.COLOR_BGR2HSV)], [0, 1], None,
                     [32, 32], [0, 180, 0, 256])
    return cv2.normalize(h, h).flatten()


def sample(path, stride=3, w=120, h=213):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    small, n = [], 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if n % stride == 0:
            small.append(cv2.resize(f, (w, h)))
        n += 1
    cap.release()
    return small, fps, n, stride


def shots(frames, fps, stride):
    """Boundaries by HISTOGRAM CORRELATION, not pixel difference. A punch-in moves every
    pixel while showing nothing new; mean|diff| flags it as a cut and hist-corr does not.
    Same trap, documented in this repo more than once."""
    H = [_hist(f) for f in frames]
    cor = [cv2.compareHist(H[i], H[i + 1], cv2.HISTCMP_CORREL) for i in range(len(H) - 1)]
    cuts = [i for i, c in enumerate(cor) if c < CUT_CORR]
    bounds, prev = [], 0
    for c in cuts + [len(H) - 1]:
        bounds.append((prev, c))
        prev = c
    segs = [{"i": k, "start_s": round(a * stride / fps, 2),
             "end_s": round(b * stride / fps, 2),
             "dur_s": round((b - a) * stride / fps, 2),
             "mid": (a + b) // 2}
            for k, (a, b) in enumerate(bounds) if b > a]
    return H, segs


# ---------------------------------------------------------------- 2 REPETITION
def repetition(H, segs):
    """Every shot against every OTHER shot, not just its neighbour.

    The failure this exists for: WRX v9 shot 0 and shot 8 measured 0.984 correlation, five
    shots apart. Nothing in the pipeline compares shots that far apart, so the repetition
    the eye complains about most is exactly the repetition nothing looks for."""
    pairs = []
    for a in range(len(segs)):
        for b in range(a + 2, len(segs)):
            c = float(cv2.compareHist(H[segs[a]["mid"]], H[segs[b]["mid"]],
                                      cv2.HISTCMP_CORREL))
            if c > REPEAT_CORR:
                pairs.append({"a": a, "b": b, "corr": round(c, 3),
                              "a_at_s": segs[a]["start_s"], "b_at_s": segs[b]["start_s"]})
    pairs.sort(key=lambda p: -p["corr"])
    # how much of the RUNTIME is spent on a picture already shown
    dup_shots = sorted({p["b"] for p in pairs})
    dup_s = sum(segs[i]["dur_s"] for i in dup_shots)
    total = sum(s["dur_s"] for s in segs)
    return {"threshold_choice": REPEAT_CORR, "n_shots": len(segs),
            "n_pairs": len(pairs), "worst": pairs[:8],
            "repeat_runtime_s": round(dup_s, 2),
            "repeat_runtime_pct": round(100.0 * dup_s / max(total, 1e-6), 1)}


# ---------------------------------------------------------------- 3 EVENT CURVE
def events(frames, fps, stride, segs):
    """Does anything HAPPEN, and does it happen where the hook is?

    Per-shot mean frame-to-frame motion, then two questions no existing check asks:
      - is the biggest visual event inside the first 3 seconds?
      - how many shots are effectively static?
    A tour scores flat. An edit that opens on an EVENT spikes early."""
    g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in frames]
    mot = [float(np.mean(np.abs(g[i] - g[i - 1]))) for i in range(1, len(g))]
    per = []
    for s in segs:
        a = max(0, int(s["start_s"] * fps / stride))
        b = min(len(mot), max(a + 1, int(s["end_s"] * fps / stride)))
        seg = mot[a:b] or [0.0]
        per.append({"i": s["i"], "start_s": s["start_s"],
                    "motion": round(float(np.mean(seg)), 2),
                    "peak": round(float(np.max(seg)), 2)})
    if not per:
        return {}
    peak_shot = max(per, key=lambda p: p["peak"])
    static = [p["i"] for p in per if p["motion"] < 0.6]
    early = [p for p in per if p["start_s"] < HOOK_S]
    early_peak = max((p["peak"] for p in early), default=0.0)
    allpeak = max(p["peak"] for p in per)
    return {"per_shot": per,
            "biggest_event_at_s": peak_shot["start_s"],
            "biggest_event_in_hook": peak_shot["start_s"] < HOOK_S,
            "hook_peak_vs_max_pct": round(100.0 * early_peak / max(allpeak, 1e-6), 1),
            "static_shots": static,
            "static_pct": round(100.0 * len(static) / len(per), 1)}


# ---------------------------------------------------------------- report
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--json", default=None)
    ap.add_argument("--stride", type=int, default=3)
    a = ap.parse_args()

    if not os.path.exists(a.video):
        sys.exit(f"no such file: {a.video}")

    fr = freshness(a.video)
    frames, fps, nframes, stride = sample(a.video, a.stride)
    dur = nframes / fps if fps else 0
    H, segs = shots(frames, fps, stride)
    dyn = dynamics(a.video)
    rep = repetition(H, segs)
    ev = events(frames, fps, stride, segs)

    durs = sorted(s["dur_s"] for s in segs) or [0]
    med = durs[len(durs) // 2]
    cpm = (len(segs) - 1) / dur * 60.0 if dur else 0

    W = 74
    print("=" * W)
    print(f"CUTSENSE  {os.path.basename(a.video)}")
    print("=" * W)
    print(f"  0 freshness      {fr['mtime']}  ({fr['age_min']} min old, "
          f"{fr['bytes']/1e6:.1f} MB)  <- verify this is the render you think it is")
    print(f"    shape          {dur:.2f}s @ {fps:.0f}fps · {len(segs)} shots · "
          f"median {med:.2f}s · {cpm:.1f} cuts/min")
    print()
    lra = dyn.get("lra_lu")
    flag = ("NOT MEASURED - ebur128 returned nothing" if not dyn.get("measured")
            else "FLAT" if dyn.get("flat") else "ok")
    print(f"  1 DYNAMICS       integrated {dyn.get('integrated_lufs')} LUFS · "
          f"true peak {dyn.get('true_peak_dbfs')} dBFS")
    print(f"                   LOUDNESS RANGE {lra} LU  [{flag}, floor {LRA_FLOOR} is a "
          f"CHOICE not a measurement]")
    if dyn.get("flat"):
        print("                   -> the file never goes anywhere. Integrated loudness and")
        print("                      true peak can both be perfect while this is 1.0.")
    print()
    print(f"  2 REPETITION     {rep['n_pairs']} non-adjacent shot pairs over "
          f"{REPEAT_CORR} histogram correlation")
    print(f"                   {rep['repeat_runtime_pct']}% of runtime "
          f"({rep['repeat_runtime_s']}s) is a picture already shown")
    for p in rep["worst"][:5]:
        print(f"                   shot {p['a']:>2} @{p['a_at_s']:>5.2f}s  ==  "
              f"shot {p['b']:>2} @{p['b_at_s']:>5.2f}s   corr {p['corr']}")
    print()
    if ev:
        print(f"  3 EVENT CURVE    biggest visual event at {ev['biggest_event_at_s']}s "
              f"({'IN' if ev['biggest_event_in_hook'] else 'OUTSIDE'} the first "
              f"{HOOK_S:.0f}s)")
        print(f"                   hook peak is {ev['hook_peak_vs_max_pct']}% of the "
              f"video's biggest moment")
        print(f"                   {ev['static_pct']}% of shots are effectively static "
              f"{ev['static_shots'][:10] if ev['static_shots'] else ''}")
    print()
    print("  none of the above blocks anything. it is three numbers the eye has been")
    print("  carrying alone. the verdict stays with the eye.")
    print("=" * W)

    if a.json:
        json.dump({"freshness": fr, "duration_s": round(dur, 2), "fps": fps,
                   "shots": segs, "median_shot_s": med, "cuts_per_min": round(cpm, 2),
                   "dynamics": dyn, "repetition": rep, "events": ev},
                  open(a.json, "w", encoding="utf-8"), indent=2)
        print(f"  json -> {a.json}")


if __name__ == "__main__":
    main()
