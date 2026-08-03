#!/usr/bin/env python3
"""
CLIPQC — per-clip quality gate, BETWEEN generation and the edit.

WHY THIS EXISTS
  The pipeline had a hole exactly where the credits are: planqc gates the plan (free),
  verify gates the finished cut (free) — but the clips themselves, the only paid artefacts,
  entered the edit unexamined. Only shot 0 (the probe) ever got looked at.

  Video quality is ~90% decided at generation; the edit can only preserve it. So this is
  the video-quality gate. It answers, per clip, the questions that were answered by eye on
  the Supra probe — and it must catch what the eye caught there, or it is decoration:

    the probe's face never read      -> face-present check on HUMAN/EVENT clips
    the event never resolved         -> event-resolution check on the hook clip
    (and the ones that DID pass)     -> no-settle open, brightness, sharpness, specs

  One clip failing = one 22.5cr regeneration. The same defect discovered at final review
  = a rebuilt edit and a burned evening.

USAGE
  python3 talyx.py ingest supra              gate everything in projects/supra/clips/
  python3 clipqc.py supra [--clip FILE]      single file: gate it before accepting it
"""
import os, sys, json, glob, argparse, importlib
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "tools"))


def load_plan(name):
    for cand in (f"plans.{name}", name, f"{name}_plan"):
        try:
            return importlib.import_module(cand)
        except ModuleNotFoundError:
            pass
    return None


def read_clip(path, w=120, h=213):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    small, full_first = [], None
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if full_first is None:
            full_first = f
        small.append(cv2.cvtColor(cv2.resize(f, (w, h)), cv2.COLOR_BGR2GRAY).astype(np.float32))
    cap.release()
    return dict(fps=fps, W=W, H=H, n=len(small), gray=small, first=full_first,
                dur=len(small) / fps if fps else 0)


def motion_profile(gray):
    return [float(np.mean(np.abs(gray[i] - gray[i - 1]))) for i in range(1, len(gray))]


def gate_clip(path, P, key=None):
    """Returns (checks, blocking_fails). Each check: (name, ok, detail, blocking)."""
    C = []

    def add(name, ok, detail, blocking=True):
        C.append((name, bool(ok), detail, blocking))

    c = read_clip(path)
    if c["n"] < 10:
        add("readable", False, "fewer than 10 frames — file corrupt or truncated")
        return C, 1

    # ---- 1 SPECS ----
    ok_spec = (c["W"], c["H"]) == (P.W, P.H) and abs(c["dur"] - P.CLIP_S) < 1.2
    add("specs", ok_spec, f"{c['W']}x{c['H']} @ {c['fps']:.0f}fps, {c['dur']:.2f}s "
                          f"(want {P.W}x{P.H}, ~{P.CLIP_S}s)")

    mot = motion_profile(c["gray"])
    fps = c["fps"]

    # ---- 2 OPENING SETTLE ----
    # AI clips open with a settle. Measured: a settle/static open reads < ~1.5 mean
    # |diff|; the approved Supra probe opened at 6.35. First 0.4s must move.
    head = mot[:max(2, int(0.4 * fps))]
    hm = float(np.mean(head))
    add("no-settle open", hm >= 1.5, f"first 0.4s motion {hm:.2f} (>=1.5; a settle reads <1.5)")

    # ---- 3 DEAD TAIL ----
    # The failed probe spent 3.4s motionless after its event. A clip that dies early
    # wastes the seconds the edit will actually use. WARN, not block — holds only use 3.2s.
    tail = mot[int(2.0 * fps):]
    tm = float(np.mean(tail)) if tail else 0.0
    add("alive after 2s", tm >= 0.8, f"mean motion after 2.0s = {tm:.2f} "
        f"(<0.8 = dead air; fine ONLY if the plan never uses past 2s)", False)

    # ---- 4 BRIGHTNESS vs the plan's palette ----
    bri = float(np.mean([g.mean() for g in c["gray"]]))
    lo, hi = (18, 90)   # night palette band; source clips measured 46.8-81.2
    add("brightness", lo <= bri <= hi, f"mean {bri:.1f} (band {lo}-{hi} for night look)")

    # ---- 5 SHARPNESS FLOOR ----
    sharp = float(np.mean([cv2.Laplacian(g, cv2.CV_32F).var()
                           for g in c["gray"][:: max(1, c["n"] // 12)]]))
    add("sharpness", sharp >= 25, f"laplacian var {sharp:.0f} (floor 25; LC300 sources ~56)")

    # ---- role-specific checks, driven by the PLAN ----
    act = P.SOURCES[key][2].upper() if key and key in P.SOURCES else None

    if act == "EVENT":
        # The whole thesis of the hook: the event must be OVER inside 2.00s and the
        # first 2s must carry far more motion than the rest (approved-probe signature:
        # 4.11 vs 0.41 — a 10x ratio; require >=2x and a real peak inside the window).
        first2 = [m for i, m in enumerate(mot) if (i + 1) / fps <= 2.0]
        rest = [m for i, m in enumerate(mot) if (i + 1) / fps > 2.0] or [0.0]
        ratio = (np.mean(first2) + 1e-6) / (np.mean(rest) + 1e-6)
        pk_t = (int(np.argmax(mot)) + 1) / fps
        add("EVENT in window", np.mean(first2) >= 2.0 and pk_t <= 2.0,
            f"first-2s motion {np.mean(first2):.2f} (>=2.0), peak at {pk_t:.2f}s (<=2.0)")
        add("EVENT resolves", ratio >= 2.0,
            f"first-2s/after ratio {ratio:.1f}x (>=2x: the event must be the loudest thing)", False)

    if act in ("EVENT", "HUMAN"):
        # The probe's killer defect: the face never read. Haar on the first 1.5s,
        # full resolution. A HUMAN/EVENT clip where no face is ever detected fails.
        fc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        pc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
        cap = cv2.VideoCapture(path)
        found, best = 0, 0
        for i in range(int(1.5 * fps)):
            ok, f = cap.read()
            if not ok:
                break
            if i % 3:
                continue
            g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            r = list(fc.detectMultiScale(g, 1.1, 4, minSize=(36, 36))) or \
                list(pc.detectMultiScale(g, 1.1, 4, minSize=(36, 36)))
            if len(r):
                found += 1
                best = max(best, max(w * h for (_x, _y, w, h) in r))
        cap.release()
        # PRESENCE IS NOT THE STANDARD - LEGIBILITY IS. The failed probe had a face in
        # 7 sampled frames at 18,496px^2 = 2.0% of frame, and by eye it never read.
        # Require >=3.5% of frame area: a face beat, not a face pixel.
        frac = best / float(c["W"] * c["H"])
        add("face READS (first 1.5s)", found >= 2 and frac >= 0.035,
            f"found in {found} frames, largest {frac*100:.1f}% of frame "
            f"(>=3.5%: the probe measured 2.0% and did not read by eye)")

    fails = sum(1 for _n, ok, _d, b in C if not ok and b)
    return C, fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--clip", help="single file instead of the whole clips/ folder")
    ap.add_argument("--key", help="source key in the plan (A..K) for role checks")
    a = ap.parse_args()

    P = load_plan(a.name)
    if not P:
        print(f"no plan: plans/{a.name}.py"); return 2

    if a.clip:
        targets = [(a.key, a.clip)]
    else:
        cdir = os.path.join(HERE, "projects", a.name, "clips")
        named = {v: k for k, v in getattr(P, "CLIPS", {}).items()}
        targets = []
        for f in sorted(glob.glob(os.path.join(cdir, "*.mp4"))):
            base = os.path.basename(f)
            key = named.get(base)
            if key is None:                      # SUPRA_A_event.mp4 style
                for k in P.SOURCES:
                    if f"_{k}_" in base or base.startswith(f"{k}_"):
                        key = k; break
            targets.append((key, f))

    if not targets:
        print("no clips to gate"); return 1

    print("=" * 70)
    print(f"CLIPQC  {P.PROJECT}")
    print("=" * 70)
    total_block = 0
    for key, path in targets:
        checks, fails = gate_clip(path, P, key)
        total_block += fails
        role = P.SOURCES[key][2] if key in getattr(P, "SOURCES", {}) else "?"
        print(f"\n  {os.path.basename(path)}   source={key or '?'} act={role}")
        for n, ok, d, b in checks:
            tag = "OK  " if ok else ("FAIL" if b else "warn")
            print(f"    {tag}  {n:24s} {d}")
        print(f"    -> {'ACCEPT' if fails == 0 else 'REJECT — regenerate this clip (22.5cr), do NOT edit around it'}")

    print()
    print("=" * 70)
    print(f"  {'PASS — clips may enter the edit' if total_block == 0 else f'BLOCK  {total_block} failing check(s)'}")
    print("=" * 70)
    return 1 if total_block else 0


if __name__ == "__main__":
    sys.exit(main())
