#!/usr/bin/env python3
"""
BEDCHECK — the L128 gate: is the MUSIC actually audible under the foley?
Born 2026-08-12 from panborneo v4: bed mixed 3dB under foley + 4:1 duck left the
melody band (300-2kHz) flat at -40dB for 64 straight seconds — "foley covers the
whole BGM" (operator, correct). Flat RMS proved nothing; the signature is spectral.

CHECK: mean melody-band level (300-2000 Hz) must sit within MAX_GAP dB of mean
broadband level across the cut. Also reports the low-band lift during the loudest
10% of moments (foley-bass dominance tell: v4 measured +10.7dB).

Usage:  python3 tools/bedcheck.py FINAL.mp4 [--max-gap 12]
Exit 0 PASS / 1 FAIL — composes in a shell like planqc/verify.
"""
import argparse, subprocess, sys
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--max-gap", type=float, default=12.0,
                    help="max dB the melody band may sit under broadband (default 12)")
    a = ap.parse_args()

    sr = 22050
    raw = subprocess.run(["ffmpeg","-v","quiet","-i",a.video,"-ac","1","-ar",str(sr),
                          "-f","f32le","-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    if len(x) < sr: sys.exit("FAIL: no audio decoded")
    hop = sr//10                      # 100ms frames
    n = len(x)//hop*hop
    fr = x[:n].reshape(-1,hop)
    bb = 10*np.log10((fr**2).mean(1)+1e-12)
    F = np.fft.rfft(fr,axis=1); f = np.fft.rfftfreq(hop,1/sr)
    def band(lo,hi):
        m=(f>=lo)&(f<=hi)
        return 10*np.log10((np.abs(F[:,m])**2).mean(1)/hop**2*2+1e-15)
    mel, low = band(300,2000), band(40,160)
    loud = bb >= np.percentile(bb,90)
    quiet = bb <= np.percentile(bb,50)
    gap = float(bb.mean()-mel.mean())
    lowlift = float(low[loud].mean()-low[quiet].mean())
    ok = gap <= a.max_gap
    print(f"melody band (300-2k) mean : {mel.mean():7.1f} dB")
    print(f"broadband mean            : {bb.mean():7.1f} dB")
    print(f"gap (must be <= {a.max_gap:.0f})       : {gap:7.1f} dB   {'PASS' if ok else 'FAIL - the bed is buried (L128)'}")
    print(f"low-band lift @ loud 10%  : {lowlift:+7.1f} dB   (v4 measured +10.7 = foley bass dominance)")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
