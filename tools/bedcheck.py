#!/usr/bin/env python3
"""
BEDCHECK v2 — is the MUSIC on top of the foley? (L128's gate, L136's lesson)

v1 measured a 300–2kHz "melody band" gap and FAILED any mix using a bass-led
bed: liqwyd-to-the-moon measures a 28dB gap SOLO, so 100% pure music would have
failed the 12dB threshold. A gate must be calibrated against its reference
signal before its threshold means anything (L136 — the file-27 VACUOUS PASS
trap, built into a brand-new gate).

v2 measures the thing itself: with the bed file + window known, project the bed
signal onto the mix per 0.5s frame (auto lag-corrected — mp3 decoder offset of
5ms faked a buried bed once). bed level vs residual (foley+sfx) level, direct.

Usage:
  python3 tools/bedcheck.py FINAL.mp4 --bed bed.mp3 --bed-ss 9.57 [--margin 0]
  python3 tools/bedcheck.py FINAL.mp4              # legacy spectral report only, never a verdict

PASS: median(bed − foley) >= --margin dB (default 0: music at least level with foley).
Exit 0 PASS / 1 FAIL / 2 no-verdict (no bed given).
"""
import argparse, subprocess, sys
import numpy as np

SR = 22050

def pcm(path, ss=None, t=None):
    cmd = ["ffmpeg","-v","quiet"]
    if ss: cmd += ["-ss",str(ss)]
    cmd += ["-i",path]
    if t: cmd += ["-t",str(t)]
    cmd += ["-ac","1","-ar",str(SR),"-f","f32le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout, dtype=np.float32)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--bed", help="the bed audio file used in the mix")
    ap.add_argument("--bed-ss", type=float, default=0.0, help="bed window start used in the mix")
    ap.add_argument("--margin", type=float, default=0.0,
                    help="required median dB of bed OVER foley (default 0)")
    a = ap.parse_args()

    m = pcm(a.video)
    if len(m) < SR: sys.exit("FAIL: no audio decoded")

    if not a.bed:
        print("NO --bed GIVEN: spectral report only, NO VERDICT (v1's threshold was miscalibrated, L136)")
        sys.exit(2)

    dur = len(m)/SR
    b = pcm(a.bed, ss=a.bed_ss, t=dur)

    # lag correction: mp3/aac decoder delays differ (5ms measured once)
    s = int(min(20, dur/3)*SR); w = int(min(10, dur/4)*SR); pad = int(0.2*SR)
    ms = m[s:s+w]-m[s:s+w].mean(); bs = b[s:s+w]-b[s:s+w].mean()
    c = np.correlate(ms, bs[pad:w-pad], mode="valid")
    lag = int(np.argmax(np.abs(c))) - pad
    q = float(np.abs(c).max()/(np.linalg.norm(ms)*np.linalg.norm(bs[pad:w-pad])+1e-12))
    if lag >= 0: m2, b2 = m[lag:], b
    else:        m2, b2 = m, b[-lag:]

    hop = SR//2
    n = min(len(m2), len(b2))//hop*hop
    M, B = m2[:n].reshape(-1,hop), b2[:n].reshape(-1,hop)
    g = (M*B).sum(1)/((B*B).sum(1)+1e-12)
    bed = g[:,None]*B; res = M-bed
    bl = 10*np.log10((bed**2).mean(1)+1e-12)
    fl = 10*np.log10((res**2).mean(1)+1e-12)
    val = (10*np.log10((B*B).mean(1)+1e-12)) > -45   # skip bed-silent frames
    d = (bl-fl)[val]
    med = float(np.median(d)); worst = float(np.percentile(d,10))

    print(f"alignment: lag {lag/SR*1000:+.1f} ms, corr quality {q:.2f}"
          + ("  (WEAK <0.30 — wrong bed or window?)" if q < 0.30 else ""))
    print(f"bed   level in mix : median {float(np.median(bl[val])):6.1f} dB")
    print(f"foley level in mix : median {float(np.median(fl[val])):6.1f} dB")
    ok = med >= a.margin and q >= 0.30
    print(f"BED minus FOLEY    : median {med:+6.1f} dB (need >= {a.margin:+.1f})   "
          f"{'PASS' if ok else 'FAIL - foley covers the BGM (L128)'}")
    print(f"deepest duck (p10) : {worst:+6.1f} dB")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
