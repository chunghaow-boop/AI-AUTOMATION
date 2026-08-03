#!/usr/bin/env python3
"""
REFSTUDY — turn his reference videos into a measurable TARGET PROFILE per pillar.

WHY THIS IS THE MISSING PIECE
  19 of his critiques are recorded; only 8 are machine-checkable. The unmeasurable ones -
  "stale and boring", "doesn't match the feeling", "the captions need design" - stayed
  unmeasurable because I had nothing to compare against. I was building toward my idea of
  good and checking it against my own gate.

  A reference FILE changes that. Run the same measurement stack over videos he has already
  judged good, and his taste stops being prose I might misread and becomes numbers a build
  can be gated against.

  This is also the honest fix for the phonk failure: I would not have had to guess the genre
  if I had measured the tempo of three car edits he likes.

WHAT IT EXTRACTS
  pacing      cuts/min, shot-length distribution, longest shot, cut-rate variation
  rhythm      detected BPM, and what FRACTION of cuts land on that grid
  transitions how many cuts are hard vs blended (frame-difference signature at each cut)
  audio       LUFS, true peak, spectral balance, loudness range
  hook        motion + cut count in the first 3s
  text        how much of the runtime carries on-screen text
  grade       black point, white point, saturation, contrast

OUTPUT
  assets/pillars/<pillar>/refs/target_profile.json
  A build for that pillar can then be gated against the MEDIAN of the references, with the
  spread reported - so "your references cut every 0.8s and ours cuts every 2.4s" is a
  measurement, not an argument.

Usage
  python3 refstudy.py --pillar car_cinematic --scan assets/pillars/car_cinematic/refs
  python3 refstudy.py --pillar car_cinematic --report
"""
import argparse, glob, json, os, statistics as st, subprocess, sys
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
A = os.path.join(ROOT, "assets")
STALE_DAYS = 60   # a viral profile does not survive a quarter

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def _audio(path):
    _, o = sh(f'ffmpeg -nostats -i "{path}" -af ebur128=peak=true -f null /dev/null')
    I = LRA = pk = None
    for ln in o.splitlines():
        if "I:" in ln and "LUFS" in ln:
            try: I = float(ln.split("I:")[1].split("LUFS")[0]); 
            except Exception: pass
        if "LRA:" in ln and "LU" in ln:
            try: LRA = float(ln.split("LRA:")[1].split("LU")[0])
            except Exception: pass
        if "Peak:" in ln and "dBFS" in ln:
            try: pk = float(ln.split("Peak:")[1].split("dBFS")[0])
            except Exception: pass
    return I, LRA, pk

def _spectrum(path):
    import numpy as np
    raw = subprocess.run(f'ffmpeg -v error -i "{path}" -ac 1 -ar 32000 -f s16le -',
                         shell=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(float)/32768
    if len(x) < 32000: return {}
    X = np.abs(np.fft.rfft(x*np.hanning(len(x)))); f = np.fft.rfftfreq(len(x), 1/32000)
    P = X**2; tot = P.sum() or 1
    return {lab: round(100*P[(f>=lo)&(f<hi)].sum()/tot, 1) for lo, hi, lab in
            [(20,150,"sub"),(150,1500,"body"),(1500,6000,"presence"),(6000,16000,"air")]}

def _tempo(path):
    import numpy as np
    raw = subprocess.run(f'ffmpeg -v error -i "{path}" -ac 1 -ar 12000 -f s16le -',
                         shell=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(float)/32768
    if len(x) < 24000: return None
    sr = 12000; w = int(0.02*sr)
    env = np.sqrt(np.convolve(x**2, np.ones(w)/w, "same"))
    d = np.diff(env); d[d < 0] = 0; d -= d.mean()
    ac = np.correlate(d, d, "full")[len(d)-1:]
    lo, hi = int(sr*60/200), int(sr*60/70)
    if hi >= len(ac): return None
    return round(60*sr/(lo+int(np.argmax(ac[lo:hi]))), 1)

STRIDE_AFTER_S = 25      # reviews run 60-110s; full-rate scanning does not fit a call

def _cuts_and_grade(path):
    """Cut list plus, at each cut, whether the change was INSTANT (hard cut) or spread over
    several frames (a blended transition). That ratio is the transition signature."""
    import numpy as np, cv2
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_s = (cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)/max(fps,1)
    stride = 1
    if total_s > STRIDE_AFTER_S:  stride = 3
    if total_s > 60:             stride = 5   # 60-110s reviews: 5x decimation still
    if total_s > 100:            stride = 7   # resolves cuts to ~0.2s, which is enough
    prev = None; diffs = []; frames = 0; lows = []; highs = []; sats = []
    _i = -1
    while True:
        ok, fr = cap.read()
        if not ok: break
        _i += 1
        if stride > 1 and _i % stride: continue
        s = cv2.resize(fr, (96, 170))
        g = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
        if frames % 6 == 0:
            lows.append(float(np.percentile(g, 2))); highs.append(float(np.percentile(g, 98)))
            sats.append(float(cv2.cvtColor(s, cv2.COLOR_BGR2HSV)[:, :, 1].mean()))
        if prev is not None:
            diffs.append(float(np.abs(g.astype(float)-prev).mean()))
        prev = g.astype(float); frames += 1
    cap.release()
    if not diffs: return {}
    d = np.array(diffs)
    thr = max(12.0, d.mean() + 2.2*d.std())
    idx = [i for i in range(1, len(d)-1) if d[i] > thr and d[i] >= d[i-1] and d[i] >= d[i+1]]
    merged = []
    for i in idx:
        if not merged or i - merged[-1] > int(max(2, fps/stride*0.20)): merged.append(i)
    hard = sum(1 for i in merged
               if d[i] > 2.2*max(d[max(0,i-2)], d[min(len(d)-1,i+2)]))
    eff = fps/stride
    dur = (cap_frames/fps) if False else (frames*stride/fps if fps else 0)
    shots = []
    b = [0]+merged+[len(d)]
    for k in range(len(b)-1): shots.append(round((b[k+1]-b[k])*stride/fps, 2))
    return {"duration": round(dur,2), "fps": round(fps,1), "cuts": len(merged),
            "cuts_per_min": round(len(merged)/(dur/60), 1) if dur else 0,
            "cut_times": [round(i*stride/fps,2) for i in merged],
            "shot_lengths": shots,
            "shot_median": round(st.median(shots),2) if shots else 0,
            "shot_max": round(max(shots),2) if shots else 0,
            "hard_cut_pct": round(100*hard/max(1,len(merged))),
            "blended_pct": round(100*(len(merged)-hard)/max(1,len(merged))),
            "black_point": round(st.median(lows),1) if lows else None,
            "white_point": round(st.median(highs),1) if highs else None,
            "saturation": round(st.median(sats),1) if sats else None}

def _on_grid(cut_times, bpm):
    if not bpm or not cut_times: return None
    beat = 60.0/bpm
    hits = sum(1 for c in cut_times if min(abs(c - round(c/beat)*beat), beat) < 0.06)
    return round(100*hits/len(cut_times))

def study(path):
    r = {"file": os.path.basename(path)}
    r.update(_cuts_and_grade(path))
    I, LRA, pk = _audio(path)
    r.update({"lufs": I, "lra": LRA, "true_peak": pk})
    r["bpm"] = _tempo(path)
    r["cuts_on_grid_pct"] = _on_grid(r.get("cut_times", []), r.get("bpm"))
    r["spectrum"] = _spectrum(path)
    return r

def profile(rows):
    def med(k):
        v = [x[k] for x in rows if isinstance(x.get(k), (int, float))]
        return round(st.median(v), 2) if v else None
    def rng(k):
        v = [x[k] for x in rows if isinstance(x.get(k), (int, float))]
        return [min(v), max(v)] if v else None
    return {"n": len(rows),
            "cuts_per_min": {"median": med("cuts_per_min"), "range": rng("cuts_per_min")},
            "shot_median":  {"median": med("shot_median"),  "range": rng("shot_median")},
            "shot_max":     {"median": med("shot_max"),     "range": rng("shot_max")},
            "blended_pct":  {"median": med("blended_pct"),  "range": rng("blended_pct")},
            "bpm":          {"median": med("bpm"),          "range": rng("bpm")},
            "cuts_on_grid_pct": {"median": med("cuts_on_grid_pct")},
            "lufs":         {"median": med("lufs"),         "range": rng("lufs")},
            "lra":          {"median": med("lra")},
            "true_peak":    {"median": med("true_peak")},
            "black_point":  {"median": med("black_point")},
            "saturation":   {"median": med("saturation")}}

def freshness(d):
    """Say out loud how old the calibration is. A stale profile that looks authoritative is
    worse than no profile."""
    try:
        age = (datetime.now() - datetime.strptime(d["studied_at"], "%Y-%m-%d")).days
    except Exception:
        return "  age unknown"
    limit = d.get("stale_after_days", STALE_DAYS)
    if age > limit:
        return (f"\n  STALE: studied {age} days ago (limit {limit}). "
                f"Re-study with fresh references AND re-run web research before trusting it.")
    return f"\n  fresh: studied {age} day(s) ago, valid for {limit-age} more"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pillar", required=True)
    ap.add_argument("--scan"); ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    refdir = a.scan or os.path.join(A, "pillars", a.pillar, "refs")
    out = os.path.join(A, "pillars", a.pillar, "refs", "target_profile.json")
    if a.report and os.path.exists(out):
        d = json.load(open(out))
        print(json.dumps(d["profile"], indent=2))
        print(freshness(d))
        return 0
    vids = sorted([p for p in glob.glob(os.path.join(refdir, "*"))
                   if p.lower().endswith((".mp4", ".mov", ".webm", ".mkv"))])
    if not vids:
        print(f"  no reference videos in {refdir}")
        print(f"  put 3-5 videos you consider GOOD for this pillar there, then re-run")
        return 2
    rows = []
    for v in vids:
        print(f"  studying {os.path.basename(v)} ...", flush=True)
        rows.append(study(v))
    prof = profile(rows)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # A reference profile is a SNAPSHOT of his taste on a date, not a permanent standard.
    # His words: "the ones im giving are just references... they eventually will get
    # outdated". So it expires, and the gate says so rather than quietly aiming at 2026.
    json.dump({"pillar": a.pillar,
               "studied_at": datetime.now().strftime("%Y-%m-%d"),
               "stale_after_days": STALE_DAYS,
               "expires": (datetime.now()+timedelta(days=STALE_DAYS)).strftime("%Y-%m-%d"),
               "note": "calibration snapshot. Re-study with fresh references, and re-run "
                       "web research on what is currently performing, before trusting this.",
               "references": rows, "profile": prof}, open(out, "w"), indent=2)
    print(f"\n  TARGET PROFILE — {a.pillar}  (n={prof['n']})")
    for k in ("cuts_per_min","shot_median","shot_max","blended_pct","bpm",
              "cuts_on_grid_pct","lufs","lra","true_peak","black_point","saturation"):
        v = prof[k]
        print(f"    {k:18s} median {str(v.get('median')):>8s}"
              + (f"   range {v['range']}" if v.get("range") else ""))
    print(f"\n  wrote {os.path.relpath(out, ROOT)}")
    print("  builds for this pillar can now be gated against these numbers.")
    print(f"  snapshot dated {datetime.now():%Y-%m-%d}, expires in {STALE_DAYS} days —"
          f" references date, so this is calibration, not a standard.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
