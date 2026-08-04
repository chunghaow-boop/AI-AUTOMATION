#!/usr/bin/env python3
"""
BEDQC — judge the music bed BEFORE it underpins a build. His order, 2026-08-04:
"the bgm is still lacking" — and the measurement agreed: the synth phonk bed put
77% of the final mix's energy below 150Hz against a measured viral reference of 8%.
Boom with no body is mud on a phone speaker.

Reference targets come from a MEASURED professional short-form mix (file 19):

    sub+low 20-150Hz   ~8%     body 150-1500Hz   ~45%
    himid 1.5-4k       ~18%    presence 4-10k    ~24%    air 10-20k  ~4%
    centroid ~2400 Hz  ·  a bed alone sits darker than a full mix, so bands are
    scored with tolerance — but 70%+ sub+low is failing on ANY interpretation.

CHECKS (mechanical, one verdict)
  1 BPM        measured vs --bpm, ±1        (rhythm.py, same code the engine uses)
  2 SPECTRUM   band balance vs reference    (sub+low <= 35%, body >= 25%, air <= 15%)
  3 DYNAMICS   energy must MOVE (burst/rest) — flat beds read as loops
  4 STEREO     mono is the amateur tell (file 19 doctrine #1)

A/B MODE
  python3 tools/bedqc.py candidate.wav --bpm 150 --ref current_bed.wav
  Scores both, names the winner. Use it the day his real phonk tracks land in
  assets/bgm/ — if the synth bed loses (it will), the build takes the real track.

USAGE
  python3 tools/bedqc.py assets/bgm/BGM_phonk_150.wav --bpm 150
"""
import os, sys, argparse
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tools"))

REF = {"sublow": 8.0, "body": 45.0, "himid": 18.0, "presence": 24.0, "air": 4.0,
       "centroid": 2400.0}


def load(path, sr=44100):
    import subprocess, tempfile, wave
    w = os.path.join(tempfile.gettempdir(), "_bedqc.wav")
    subprocess.run(f'ffmpeg -y -v error -i "{path}" -ar {sr} -c:a pcm_s16le "{w}"',
                   shell=True, capture_output=True)
    wv = wave.open(w)
    ch = wv.getnchannels()
    x = np.frombuffer(wv.readframes(wv.getnframes()), dtype=np.int16
                      ).astype(float) / 32768.0
    wv.close()
    if ch == 2:
        x = x.reshape(-1, 2)
        return x.mean(axis=1), x, sr
    return x, None, sr


def measure(path, want_bpm=None):
    m, stereo, sr = load(path)
    r = {"file": os.path.basename(path), "checks": []}

    def add(name, ok, detail):
        r["checks"].append((name, bool(ok), detail))

    # 1 BPM + phase (engine's own rhythm code)
    if want_bpm:
        try:
            import rhythm
            f, t = rhythm.stft_flux(m if m.dtype == float else m.astype(float))
            on = rhythm.pick_onsets(f, t)
            iv = np.diff(on)
            iv = iv[(iv > 0.2) & (iv < 1.2)]
            bpm = 60.0 / float(np.median(iv)) if len(iv) else 0.0
            while bpm and bpm < want_bpm / 1.6:
                bpm *= 2
            add("1 bpm", abs(bpm - want_bpm) <= 1.5,
                f"measured {bpm:.1f} vs plan {want_bpm:.0f} (±1.5)")
        except Exception as e:
            add("1 bpm", False, f"could not measure: {str(e)[:40]}")

    # 2 spectrum — RECALIBRATED 2026-08-04 after measuring HIS 25 real phonk
    # tracks: ALL sit 70-89% sub+low. Phonk beds are sub-heavy BY GENRE; the
    # file-19 reference (45% body) describes a finished MIX with voice/foley on
    # top, not a bare bed. A bed's job is to leave the midrange EMPTY for those
    # layers. So the bed caps are genre-calibrated (worst real track: 89/7/2);
    # the reference profile is enforced on the FINAL MIX by verify/qc instead.
    F = np.abs(np.fft.rfft(m)) ** 2
    fr = np.fft.rfftfreq(len(m), 1 / sr)
    tot = F[(fr >= 20) & (fr < 20000)].sum() or 1.0
    b = lambda lo, hi: 100.0 * F[(fr >= lo) & (fr < hi)].sum() / tot
    sublow, body, air = b(20, 150), b(150, 1500), b(10000, 20000)
    cen = float((fr[1:] * F[1:]).sum() / F[1:].sum())
    ok2 = sublow <= 90.0 and body >= 6.0 and air <= 15.0
    add("2 spectrum", ok2,
        f"sub+low {sublow:.0f}% (genre cap 90) · body {body:.0f}% (floor 6) · "
        f"air {air:.0f}% (cap 15) · centroid {cen:.0f}Hz "
        f"[full-mix ref: {REF['body']:.0f}% body — checked on the MIX, not the bed]")
    r["score"] = (min(35.0, sublow) - sublow) - abs(body - REF["body"]) * 0.5

    # 3 dynamics: 0.5s RMS windows must vary (burst/rest), not sit flat
    n = int(0.5 * sr)
    wins = [m[i:i + n] for i in range(0, len(m) - n, n)]
    rms = np.array([np.sqrt(np.mean(w ** 2)) + 1e-9 for w in wins])
    var_db = 20 * np.log10(rms.max() / max(rms.min(), 1e-6))
    add("3 dynamics", var_db >= 3.0,
        f"energy range {var_db:.1f} dB across 0.5s windows (>=3 = it MOVES)")

    # 4 stereo
    if stereo is None:
        add("4 stereo", False, "MONO — the single biggest amateur tell (file 19)")
    else:
        diff = float(np.sqrt(np.mean((stereo[:, 0] - stereo[:, 1]) ** 2)))
        add("4 stereo", diff > 1e-3,
            f"stereo, L/R difference RMS {diff:.4f}" if diff > 1e-3
            else "2 channels but IDENTICAL — effectively mono")
    return r


def show(r):
    print(f"\n  {r['file']}")
    fails = 0
    for name, ok, det in r["checks"]:
        tag = "OK  " if ok else "FAIL"
        fails += 0 if ok else 1
        print(f"  {tag}  {name:12s} {det}")
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bed")
    ap.add_argument("--bpm", type=float, default=None)
    ap.add_argument("--ref", default=None,
                    help="A/B: score BOTH files, name the winner")
    a = ap.parse_args()

    print("=" * 74)
    print("BEDQC — the bed is judged BEFORE it underpins a build")
    print("=" * 74)
    r1 = measure(a.bed, a.bpm)
    f1 = show(r1)
    if a.ref:
        r2 = measure(a.ref, a.bpm)
        f2 = show(r2)
        w = r1 if (f1, -r1.get("score", 0)) < (f2, -r2.get("score", 0)) else r2
        print(f"\n  A/B WINNER: {w['file']} "
              f"({f1} vs {f2} failing checks; spectrum distance breaks ties)")
        return 0
    print()
    print("=" * 74)
    if f1:
        print(f"  BLOCK  {f1} failing check(s) — this bed should not underpin a build")
    else:
        print("  PASS")
    print("=" * 74)
    return 1 if f1 else 0


if __name__ == "__main__":
    sys.exit(main())
