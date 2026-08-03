#!/usr/bin/env python3
"""
RHYTHM — the missing timing engine for the Sound Engineer seat.
Answers the question the spectral check CANNOT: *did the hit land on the beat?*

Measures, in milliseconds:
  - onset times of every transient (SFX hits, impacts, stingers)
  - the tempo + beat grid of the bed
  - each onset's deviation from the nearest beat
  - each VIDEO CUT's deviation from the nearest beat
  - each SFX's deviation from its intended cut (SFX should hit the cut, not float)

Pure numpy STFT — no librosa needed. Deps: ffmpeg + numpy (+cv2 only for cut detection).

Usage:
  python3 rhythm.py MIX.wav                       # onsets + tempo + grid tightness
  python3 rhythm.py VIDEO.mp4 --cuts              # also check cuts land on beats
  python3 rhythm.py MIX.wav --bed bed.wav         # grid from the bed, hits from the mix
"""
import subprocess, sys, os, json, argparse
import numpy as np

SR = 22050
TIGHT_MS = 50      # pro tolerance: a hit >50ms off reads as "off"
LOOSE_MS = 90      # >90ms is audibly late/early to a casual listener

def pcm(path, sr=SR):
    """Decode any media to mono float32 via ffmpeg."""
    cmd = ["ffmpeg","-v","quiet","-i",path,"-f","f32le","-ac","1","-ar",str(sr),"-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

def stft_flux(x, n_fft=1024, hop=256):
    """Spectral flux onset envelope (half-wave rectified spectral difference)."""
    if len(x) < n_fft: return np.array([]), hop
    w = np.hanning(n_fft)
    n = 1 + (len(x)-n_fft)//hop
    S = np.empty((n, n_fft//2+1), dtype=np.float32)
    for i in range(n):
        seg = x[i*hop:i*hop+n_fft] * w
        S[i] = np.abs(np.fft.rfft(seg))
    S = np.log1p(S)
    d = np.diff(S, axis=0)
    flux = np.maximum(d, 0).sum(axis=1)
    if flux.max() > 0: flux = flux/flux.max()
    return flux, hop

def pick_onsets(flux, hop, sr=SR, delta=0.12, min_gap_ms=70):
    """Adaptive-threshold peak picking."""
    if flux.size == 0: return np.array([])
    w = 12
    pad = np.pad(flux, (w,w), mode="edge")
    local = np.array([pad[i:i+2*w+1].mean() for i in range(len(flux))])
    thr = local + delta
    peaks = []
    min_gap = int((min_gap_ms/1000)*sr/hop)
    last = -10**9
    for i in range(1, len(flux)-1):
        if flux[i] > thr[i] and flux[i] >= flux[i-1] and flux[i] > flux[i+1]:
            if i - last >= min_gap:
                peaks.append(i); last = i
    return np.array(peaks) * hop / sr

def _fit_grid(period, onsets, dur, tol=0.050):
    """Brute-force phase; score = fraction of onsets within tol of a grid point."""
    best = (-1.0, 0.0)
    for off in np.arange(0, period, period/64):
        grid = np.arange(off, dur + 1e-9, period)
        if len(grid) == 0: continue
        dev = np.abs(onsets[:, None] - grid[None, :]).min(axis=1)
        hit = float((dev <= tol).mean()) - 0.001*float(dev.mean())
        if hit > best[0]: best = (hit, off)
    return best  # (score, offset)

def estimate_tempo(flux, hop, sr=SR, bpm_range=(60,200), onsets=None):
    """Autocorrelation + OCTAVE CORRECTION + onset-fitted phase.
    Half/double-time errors were producing garbage grids; candidates are now
    scored by how well they actually explain the detected onsets."""
    if flux.size < 16: return None, None
    dur = len(flux)*hop/sr
    if onsets is None or len(onsets) == 0:
        onsets = pick_onsets(flux, hop, sr)
    if len(onsets) < 2: return None, None

    f = flux - flux.mean()
    ac = np.correlate(f, f, mode="full")[len(f)-1:]
    lo = max(1, int((60.0/bpm_range[1])*sr/hop))
    hi = min(int((60.0/bpm_range[0])*sr/hop), len(ac)-1)
    if hi <= lo: return None, None

    # take several autocorrelation peaks, not just the max
    seg = ac[lo:hi]
    order = np.argsort(seg)[::-1]
    cands, seen = [], set()
    for k in order[:40]:
        lag = int(k+lo)
        if any(abs(lag-s) < 3 for s in seen): continue
        seen.add(lag); cands.append(lag*hop/sr)
        if len(cands) >= 6: break

    # expand each candidate by its octaves — this is the half/double-time fix
    periods = []
    for p in cands:
        for mult in (0.25, 0.5, 1.0, 2.0, 4.0):
            q = p*mult
            bpm = 60.0/q
            if bpm_range[0] <= bpm <= bpm_range[1] and not any(abs(q-r) < 1e-3 for r in periods):
                periods.append(q)
    if not periods: return None, None

    best = (-1.0, None, None)
    for q in periods:
        score, off = _fit_grid(q, onsets, dur)
        # prefer denser grids only when they genuinely explain more onsets
        if score > best[0] + 1e-6:
            best = (score, q, off)
    _, period, off = best
    if period is None: return None, None
    return round(60.0/period,1), np.arange(off, dur + 1e-9, period)

def deviations(events, grid):
    """ms deviation of each event from nearest grid point (signed: + = late)."""
    if grid is None or len(grid)==0 or len(events)==0: return []
    out = []
    for t in events:
        nearest = grid[np.argmin(np.abs(grid - t))]
        out.append({"t": round(float(t),3), "beat": round(float(nearest),3),
                    "dev_ms": round(float((t-nearest)*1000),1)})
    return out

def video_cuts(path, thresh=0.45):
    import cv2
    cap = cv2.VideoCapture(path); fps = cap.get(cv2.CAP_PROP_FPS) or 24
    prev, cuts, i = None, [], 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        if i % max(1,int(fps//8)) == 0:
            g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
            h = cv2.calcHist([g],[0],None,[64],[0,256]); h = cv2.normalize(h,h).flatten()
            if prev is not None and cv2.compareHist(prev,h,cv2.HISTCMP_BHATTACHARYYA) > thresh:
                cuts.append(round(i/fps,3))
            prev = h
        i += 1
    cap.release()
    return cuts

def grade(devs, label):
    if not devs:
        return {"label":label,"n":0,"verdict":"NO EVENTS","score":0}
    a = np.abs([d["dev_ms"] for d in devs])
    tight = float((a<=TIGHT_MS).mean()*100)
    loose = float((a<=LOOSE_MS).mean()*100)
    med = float(np.median(a))
    if tight >= 80: v, s = "TIGHT", 10
    elif loose >= 80: v, s = "ACCEPTABLE", 6
    else: v, s = "OFF-BEAT", 2
    return {"label":label,"n":len(devs),"median_abs_ms":round(med,1),
            "pct_within_50ms":round(tight,1),"pct_within_90ms":round(loose,1),
            "verdict":v,"score":s,
            "worst":sorted(devs,key=lambda d:-abs(d["dev_ms"]))[:5]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media"); ap.add_argument("--bed"); ap.add_argument("--cuts",action="store_true")
    ap.add_argument("--out")
    A = ap.parse_args()

    x = pcm(A.media)
    if x.size == 0:
        print(json.dumps({"error":"no audio decoded"})); return
    flux, hop = stft_flux(x)
    onsets = pick_onsets(flux, hop)

    # grid source: the bed if given (music defines the grid), else the mix itself
    if A.bed:
        bflux, bhop = stft_flux(pcm(A.bed))
        bpm, grid = estimate_tempo(bflux, bhop)
    else:
        bpm, grid = estimate_tempo(flux, hop)

    rep = {"file":A.media,"bpm":bpm,"beats":0 if grid is None else len(grid),
           "onsets_detected":len(onsets)}
    od = deviations(onsets, grid)
    rep["sfx_vs_beat"] = grade(od, "SFX/transients vs beat grid")

    if A.cuts:
        cuts = video_cuts(A.media)
        rep["cuts_detected"] = len(cuts)
        rep["cuts_vs_beat"] = grade(deviations(np.array(cuts), grid), "video cuts vs beat grid")
        # SFX should also coincide with cuts
        if len(cuts) and len(onsets):
            cd = deviations(onsets, np.array(cuts))
            rep["sfx_vs_cuts"] = grade(cd, "SFX vs video cuts")

    fails = [k for k in ("sfx_vs_beat","cuts_vs_beat","sfx_vs_cuts")
             if k in rep and rep[k].get("verdict")=="OFF-BEAT"]
    rep["verdict"] = "SEND BACK -> Sound Engineer / Editor" if fails else "TIMING OK"
    rep["failing"] = fails
    print(json.dumps(rep, indent=2))
    if A.out: json.dump(rep, open(A.out,"w"), indent=2)

if __name__ == "__main__":
    main()
