"""flinch.py — you point at a second, I measure everything in it.

    python3 tools/flinch.py desafarm 9.2
    python3 tools/flinch.py desafarm 9.2 --video path/to/any.mp4
    python3 tools/flinch.py desafarm 15.8 --window 2.0

WHY THIS EXISTS (2026-08-08, out of a conversation rather than a bug).

Gavril, asked how he finds things: "usually i know the moment it happens, and then
i have a feeling even if there is nothing wrong with the video, but i have the
feeling or the urge when i see this video is not right or it's a little bit weird,
then i will directly tell you. i would not go and find it somewhere else."

That is the most valuable instrument in this whole system and it was going to waste.
He had been sitting on reactions until he could justify them in words — the car at
90 degrees to its road took him half a second to feel and a sentence to explain, and
the sentence is the part I could have worked out myself. The flinch is the part I
cannot produce at all.

Retention is private, and it is also just this: thousands of people having that same
half-second reaction and leaving. He is one of them, reporting the decision directly
instead of as a statistic a week later — and with a CAUSE attached, which analytics
never give you. A retention curve says where they left. It never says why.

So the division of labour is: HE SUPPLIES THE FLINCH AND THE TIMESTAMP.
THIS SUPPLIES THE MICROSCOPE.

"Second nine feels off, I don't know why" is a complete and excellent bug report.
Run this at 9.0 and it prints every number in the neighbourhood: which shot, which
source, where it sits against its own action, what the light is doing, what the
sound is doing, whether it repeats another shot, whether it is on the beat, whether
a card is up. Something in that list is usually the reason.

If nothing in the list explains it, THAT IS THE FINDING — it means the reaction
came from something nothing here measures yet, which is exactly how the eight
element-pairs in 29-relationship-master.md were discovered. File it and build the
instrument.
"""
import argparse
import glob
import json
import math
import os
import subprocess
import sys
import tempfile
import wave

import cv2
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def _plan(name):
    try:
        import importlib.util
        p = os.path.join(HERE, "plans", f"{name}.py")
        if not os.path.exists(p):
            return None
        s = importlib.util.spec_from_file_location(name, p)
        m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m)
        return m
    except Exception:
        return None


def _composition(img):
    g = cv2.cvtColor(cv2.resize(img, (64, 112)), cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(gx * gx + gy * gy)
    ang = (np.arctan2(gy, gx) + np.pi) * (8 / (2 * np.pi))
    v = []
    for r in range(4):
        for c in range(4):
            m = mag[r * 28:(r + 1) * 28, c * 16:(c + 1) * 16]
            a = ang[r * 28:(r + 1) * 28, c * 16:(c + 1) * 16]
            h = np.zeros(8)
            for b in range(8):
                h[b] = m[(a.astype(int) % 8) == b].sum()
            v.append(h / (h.sum() + 1e-9))
    v = np.concatenate(v)
    return v / (np.linalg.norm(v) + 1e-9)


def _colour(img):
    h = cv2.calcHist([cv2.resize(img, (64, 112))], [0, 1, 2], None,
                     [8, 8, 8], [0, 256] * 3)
    return cv2.normalize(h, h).flatten()


def detect_cuts(video):
    """Mean absolute frame difference, adaptive threshold. The greyscale-histogram
    detector this replaces found ZERO cuts in a 20-shot film (2026-08-08)."""
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    prev, diffs, ts = None, [], []
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        small = cv2.cvtColor(cv2.resize(fr, (96, 171)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            diffs.append(float(np.abs(small - prev).mean()))
            ts.append(i / fps)
        prev = small
        i += 1
    cap.release()
    if not diffs:
        return [], fps
    mu, sd = float(np.mean(diffs)), float(np.std(diffs))
    thr = max(18.0, mu + 2.2 * sd)
    cuts = []
    for t, d in zip(ts, diffs):
        if d > thr and (not cuts or t - cuts[-1] > 0.25):
            cuts.append(round(t, 3))
    return cuts, fps


def frame_at(video, t):
    o = os.path.join(tempfile.gettempdir(), "flinch_%d.png" % os.getpid())
    sh(f'ffmpeg -y -v error -ss {t:.3f} -i "{video}" -frames:v 1 "{o}"')
    return cv2.imread(o) if os.path.exists(o) else None


def audio_at(video, t, w=0.30):
    wav = os.path.join(tempfile.gettempdir(), "flinch_%d.wav" % os.getpid())
    r = sh(f'ffmpeg -y -v error -i "{video}" -vn -ac 1 -ar 22050 "{wav}"')
    if r.returncode or not os.path.exists(wav):
        return None
    f = wave.open(wav)
    sr = f.getframerate()
    x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(float) / 32768
    f.close()
    return x, sr


def band_ratio(x, sr, a, b):
    if len(x) < 512:
        return None
    S = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1 / sr)
    lo = S[(f >= 20) & (f < 300)].mean() + 1e-9
    voice = S[(f >= 300) & (f < 3400)].mean()
    return float(voice / lo)


def main():
    ap = argparse.ArgumentParser(
        description="You point at a second. This measures everything in it.")
    ap.add_argument("project")
    ap.add_argument("t", type=float, help="the second that felt wrong")
    ap.add_argument("--video", default=None)
    ap.add_argument("--window", type=float, default=1.2,
                    help="how far either side to look (default 1.2s)")
    A = ap.parse_args()

    pdir = os.path.join(HERE, "projects", A.project)
    video = A.video
    if not video:
        outs = sorted(glob.glob(os.path.join(pdir, "output", "*.mp4")),
                      key=os.path.getmtime)
        if not outs:
            print(f"  no cut in projects/{A.project}/output/ — pass --video")
            return 2
        video = outs[-1]
    if not os.path.exists(video):
        print(f"  no such file: {video}")
        return 2

    P = _plan(A.project)
    t = A.t

    print("=" * 70)
    print(f"FLINCH  {os.path.basename(video)}  at {t:.2f}s")
    print("=" * 70)
    print("  You felt something here. Everything this system can measure about")
    print("  that moment is below. If none of it explains the feeling, that IS")
    print("  the finding — say so and we build the instrument that would see it.\n")

    # ---- where are we ---------------------------------------------------
    cuts_json = sorted(glob.glob(os.path.join(pdir, "audio", "*_cuts.json")),
                       key=os.path.getmtime)
    cuts, fps = [], 30.0
    if cuts_json:
        try:
            cuts = json.load(open(cuts_json[-1])).get("cuts", [])
            fps = cv2.VideoCapture(video).get(cv2.CAP_PROP_FPS) or 30.0
            src_note = "engine cut manifest"
        except Exception:
            cuts = []
    if not cuts:
        cuts, fps = detect_cuts(video)
        src_note = "measured here (no manifest)"
    dur = float(sh(f'ffprobe -v error -show_entries format=duration '
                   f'-of default=nw=1:nk=1 "{video}"').stdout.strip() or 0)
    bounds = [0.0] + list(cuts) + [dur]
    idx = max(0, min(len(bounds) - 2, next((i for i in range(len(bounds) - 1)
                                            if bounds[i] <= t < bounds[i + 1]), 0)))
    a, b = bounds[idx], bounds[idx + 1]
    src = "?"
    if P and idx < len(getattr(P, "SHOTS", [])):
        src = P.SHOTS[idx][0]
    print(f"  WHERE   shot {idx} (source {src}), {a:.2f}s -> {b:.2f}s, "
          f"{b - a:.2f}s long   [cuts from {src_note}]")
    print(f"          you are {t - a:.2f}s into it, {b - t:.2f}s from the next cut")
    if t - a < 0.20:
        print(f"          *** within 0.20s of the CUT INTO this shot")
    if b - t < 0.20:
        print(f"          *** within 0.20s of the CUT OUT of this shot")

    # ---- the picture ----------------------------------------------------
    print()
    fr = frame_at(video, t)
    if fr is not None:
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        lap = float(cv2.Laplacian(g, cv2.CV_64F).var())
        luma = float(g.mean())
        black = float((g < 16).mean() * 100)
        print(f"  PICTURE luma {luma:.1f}   sharpness {lap:.0f}   "
              f"crushed black {black:.1f}%")
        mids = []
        for i in range(len(bounds) - 1):
            m = frame_at(video, (bounds[i] + bounds[i + 1]) / 2)
            mids.append(m)
        lumas = [float(cv2.cvtColor(m, cv2.COLOR_BGR2GRAY).mean())
                 for m in mids if m is not None]
        if lumas:
            print(f"          the film runs {min(lumas):.0f}-{max(lumas):.0f} luma; "
                  f"this shot sits at {lumas[idx]:.0f}")
            if abs(lumas[idx] - float(np.median(lumas))) > 25:
                print(f"          *** {abs(lumas[idx]-np.median(lumas)):.0f} luma from "
                      f"the film's middle — it will read as a different world")
        if lap < 25:
            print(f"          *** SOFT. Under 25 is a melted or motion-blurred frame")
        # does this shot repeat another?
        if mids and mids[idx] is not None:
            cd, kd = _composition(mids[idx]), _colour(mids[idx])
            rep = []
            for j, m in enumerate(mids):
                if j == idx or m is None:
                    continue
                c = float(cd @ _composition(m))
                k = float(cv2.compareHist(kd, _colour(m), cv2.HISTCMP_CORREL))
                if c >= 0.80 and k >= 0.80:
                    rep.append((j, round(c, 3), round(k, 3)))
            if rep:
                print(f"          *** READS AS THE SAME SHOT AS: "
                      + ", ".join(f"shot {j} (comp {c}, colour {k})" for j, c, k in rep))

    # ---- movement -------------------------------------------------------
    f1, f2 = frame_at(video, max(0, t - 0.12)), frame_at(video, t + 0.12)
    if f1 is not None and f2 is not None:
        g1 = cv2.cvtColor(cv2.resize(f1, (96, 171)), cv2.COLOR_BGR2GRAY).astype(float)
        g2 = cv2.cvtColor(cv2.resize(f2, (96, 171)), cv2.COLOR_BGR2GRAY).astype(float)
        mv = float(np.abs(g2 - g1).mean())
        print(f"\n  MOVING  {mv:.1f} at this instant "
              + ("(still — nothing is happening)" if mv < 4 else
                 "(gentle)" if mv < 12 else "(active)"))
        if mv < 4:
            print(f"          *** a still second is where people leave")

    # ---- sound ----------------------------------------------------------
    au = audio_at(video, t)
    if au:
        x, sr = au
        def rms(t0, t1):
            s = x[int(max(0, t0) * sr):int(t1 * sr)]
            return 20 * math.log10(float(np.sqrt(np.mean(s ** 2))) + 1e-9) if len(s) else None
        here = rms(t - 0.25, t + 0.25)
        whole = rms(0, dur)
        print(f"\n  SOUND   {here:.1f} dB here against {whole:.1f} dB for the film")
        if here is not None and whole is not None and here < whole - 2.5:
            print(f"          *** {whole - here:.1f} dB QUIETER than the film — a hole")
        seg = x[int(max(0, t - 0.4) * sr):int((t + 0.4) * sr)]
        vr = band_ratio(seg, sr, 300, 3400)
        if vr is not None:
            print(f"          voice-band ratio {vr:.2f}   "
                  + ("(no human sound here)" if vr < 0.30 else "(something human)"))
        # does the sound change across the nearest cut?
        near = min(cuts, key=lambda c: abs(c - t)) if cuts else None
        if near is not None and abs(near - t) < 1.5:
            def prof(t0, t1):
                s = x[int(max(0, t0) * sr):int(t1 * sr)]
                if len(s) < 512:
                    return None
                S = np.abs(np.fft.rfft(s * np.hanning(len(s))))
                return S / (np.linalg.norm(S) + 1e-9)
            p1, p2 = prof(near - 0.30, near - 0.05), prof(near + 0.05, near + 0.30)
            if p1 is not None and p2 is not None:
                n = min(len(p1), len(p2))
                sim = float(p1[:n] @ p2[:n])
                print(f"          across the cut at {near:.2f}s the soundscape is "
                      f"{sim:.3f} similar")
                if sim > 0.90:
                    print(f"          *** the sound does NOT change at that cut — "
                          f"the bed is covering the place")

    # ---- the grid -------------------------------------------------------
    if P:
        beat = float(getattr(P, "BEAT", 0) or 0)
        if beat:
            off = (t % beat)
            off = min(off, beat - off)
            near = min(cuts, key=lambda c: abs(c - t)) if cuts else None
            print(f"\n  GRID    beat {beat*1000:.0f}ms")
            if near is not None:
                co = (near % beat)
                co = min(co, beat - co)
                print(f"          nearest cut {near:.3f}s sits {co*1000:.0f}ms "
                      f"off the beat")
                if co > 0.05:
                    print(f"          *** more than 50ms off — reads as sloppy")

    # ---- cards ----------------------------------------------------------
    if P and getattr(P, "CARDS", None):
        on = []
        for c in P.CARDS:
            s0 = int(c[1]); n0 = max(1, int(c[2]) if len(c) > 2 else 1)
            if s0 <= idx <= s0 + n0 - 1:
                on.append((c[0], s0, s0 + n0 - 1))
        print(f"\n  CARDS   " + ("none on screen" if not on else
              " · ".join(f"{txt!r} (shots {x}-{y})" for txt, x, y in on)))
        if len(on) > 1:
            print(f"          *** TWO CARDS AT ONCE — they will print through "
                  f"each other")
        for txt, x, y in on:
            if y - x >= 3:
                print(f"          *** {txt!r} holds for {y - x + 1} shots — "
                      f"a caption that outlives its shot reads as stuck")

    print("\n" + "=" * 70)
    print("  If something above is starred, that is probably what you felt.")
    print("  If nothing is, tell me anyway — a reaction this system cannot")
    print("  explain is worth more than one it can.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
