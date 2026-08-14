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


def load_style(pillar):
    """STYLE, DECLARED (2026-08-05). The brightness band used to be the constant
    (18, 90) — a NIGHT band measured off WRX/LC300 car clips. Measured that day:
    daylight footage reads 142-165 mean luma, so every vlog clip would have been
    REJECTED with 'regenerate this clip (22.5cr)'. The car look was the silent
    default for every pillar that came after it. Now each pillar declares its own."""
    for c in (os.path.join(HERE, "assets", "pillars", "PILLAR-PROFILES.json"),
              os.path.join(HERE, "pillars", "PILLAR-PROFILES.json")):
        if os.path.exists(c):
            pf = json.load(open(c, encoding="utf-8")).get(pillar) or {}
            return pf.get("style") or {}
    return {}


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
    # this pillar's DECLARED style — every genre-taste threshold below reads from it
    _sty = load_style(getattr(P, "PILLAR", ""))
    _prov_motion = not str(_sty.get("motion_source", "")).startswith("MEASURED")

    # role, needed early: EVENT clips are consumed via action-peak centering,
    # so their head checks are warnings, not blocks (see EVENT section).
    act = P.SOURCES[key][2].upper() if key and key in P.SOURCES else None

    # ---- 2 OPENING SETTLE (warn) + 2b DELIVERED WINDOW (blocking) ----
    # AMENDED AGAIN 2026-08-04, WRX batch: clip C (scoop macro) repeated probe A's
    # false-reject - static raw head, live delivered window (3.53 at 2.25s). The
    # engine centers EVERY shot on its action peak, so the clip head is the wrong
    # measurement for ALL roles, not just EVENT. The honest gate: no-settle drops to
    # warn, and the BEST shot-length window becomes the blocking check - a clip that
    # is dead everywhere still fails, on the measurement the edit actually consumes.
    head = mot[:max(2, int(0.4 * fps))]
    hm = float(np.mean(head))
    add("no-settle open", hm >= 1.5, f"first 0.4s motion {hm:.2f} "
        f"(raw head only - engine centers on action peak)", False)
    try:
        _shot_ds = sorted({P.BEATS[k2] * P.BEAT for _s, _c, k2, _n in P.SHOTS
                           if _s == key} | {1.35})
        _d2 = _shot_ds[-1]                       # longest use of this source
    except Exception:
        _d2 = 1.35
    _w2 = max(2, int(_d2 * fps))
    _bw, _bi = -1.0, 0
    for _i in range(0, max(1, len(mot) - _w2 + 1)):
        _m = float(np.mean(mot[_i:_i + _w2]))
        if _m > _bw:
            _bw, _bi = _m, _i
    # PER-PILLAR MOTION FLOOR (2026-08-05). 1.5 was measured on car footage — launches,
    # spray, tracking moves. MEASURED the same day: a slow landscape drift reads 1.18
    # and a locked-off shot 0.00, so a legitimate SERENE travel shot would have been
    # rejected as dead at 22.5cr a time. In a travel vlog a calm hold is content; in a
    # car edit it is a failure. The floor is genre taste, so it lives in the style block.
    _mf = _sty.get("motion_floor", 1.5)
    add("delivered window", _bw >= _mf,
        f"best {_d2:.2f}s window mean {_bw:.2f} at {_bi / fps:.2f}s (floor {_mf} for "
        f"'{getattr(P,'PILLAR','?')}': the edit consumes this window, not the head)"
        + ("  [PROVISIONAL floor]" if _prov_motion else ""))

    # ---- 3 DEAD TAIL ----
    # The failed probe spent 3.4s motionless after its event. A clip that dies early
    # wastes the seconds the edit will actually use. WARN, not block — holds only use 3.2s.
    tail = mot[int(2.0 * fps):]
    tm = float(np.mean(tail)) if tail else 0.0
    add("alive after 2s", tm >= 0.8, f"mean motion after 2.0s = {tm:.2f} "
        f"(<0.8 = dead air; fine ONLY if the plan never uses past 2s)", False)

    # ---- 4 BRIGHTNESS vs THIS PILLAR's declared palette ----
    bri = float(np.mean([g.mean() for g in c["gray"]]))
    lo, hi = _sty.get("brightness_band", (18, 90))
    _src = _sty.get("brightness_source", "UNDECLARED — falling back to the CAR night band")
    _prov = not _src.startswith("MEASURED")
    add("brightness", lo <= bri <= hi,
        f"mean {bri:.1f} in [{lo},{hi}] for pillar '{getattr(P,'PILLAR','?')}'"
        + ("  [PROVISIONAL band — re-derive from real clips at ingest]" if _prov else ""))

    # ---- 5 SHARPNESS FLOOR ----
    sharp = float(np.mean([cv2.Laplacian(g, cv2.CV_32F).var()
                           for g in c["gray"][:: max(1, c["n"] // 12)]]))
    add("sharpness", sharp >= 25, f"laplacian var {sharp:.0f} (floor 25; LC300 sources ~56)")

    # ---- role-specific checks, driven by the PLAN ----
    if act == "EVENT":
        # AMENDED 2026-08-04 after WRX probe A: measure what the EDIT CONSUMES, not
        # the clip head. The engine centers every shot on its action peak, so the
        # event may sit anywhere in the raw clip — probe A carried a perfect
        # swerve-pass at 2.1-3.7s behind a 2s wind-up, and the old head-based check
        # rejected a clip whose delivered window measured ~16. Gate the BEST
        # shot-length window instead. Floor 4.0 came from a Supra probe measuring 4.11. PROVENANCE UNVERIFIED
        # (ledgers/approvals.json UNV-1): no quote exists showing he approved that
        # probe at any scope. This gate REJECTS clips at 22.5cr a time on a warrant
        # I cannot produce. Do not tighten it; re-derive or ask.
        try:
            d = P.BEATS[P.SHOTS[0][2]] * P.BEAT          # the hook shot's real length
        except Exception:
            d = 1.6
        wlen = max(2, int(d * fps))
        best_m, best_i = -1.0, 0
        for i in range(0, max(1, len(mot) - wlen + 1)):
            m = float(np.mean(mot[i:i + wlen]))
            if m > best_m:
                best_m, best_i = m, i
        rest = mot[:best_i] + mot[best_i + wlen:]
        ratio = (best_m + 1e-6) / ((float(np.mean(rest)) if rest else 0.0) + 1e-6)
        # DOWNGRADED TO NON-BLOCKING 2026-08-05 (session 3), by Gavril's decision when
        # asked to settle UNV-1: "Mark PROVISIONAL, non-blocking". The floor 4.0 has no
        # producible approval quote behind it, and as a BLOCKING gate it rejected clips
        # at 22.5cr each on a warrant I cannot show. It now reports and does not reject;
        # his eye calls the first probe of a new pillar. Re-promote to blocking ONLY
        # after an approvals.json entry exists with a verbatim quote at clip scope.
        _ef = _sty.get("event_motion_floor", 4.0)
        add("EVENT window (delivered)", best_m >= _ef,
            f"best {d:.2f}s window mean {best_m:.2f} at {best_i / fps:.2f}s "
            f"(floor {_ef} for '{getattr(P,'PILLAR','?')}' - PROVISIONAL, NON-BLOCKING: "
            f"the 4.0 origin 'Supra probe 4.11' has no approval quote, approvals.json "
            f"UNV-1. Reported for your eye, not enforced)", False)
        add("EVENT is the loudest thing", ratio >= 2.0,
            f"delivered-window/rest ratio {ratio:.1f}x (>=2x)", False)

    # ---- foley-audibility (2026-08-05, red-team wave 3) ----
    # A spec-correct but SILENT clip on a FOREGROUND foley shot passed every check;
    # the engine prints "NO clip carried audio" and builds anyway - the genre's
    # sound design thins silently. If the plan mixes this source foreground
    # (>= -6dB), the clip's own audio must exist and carry signal.
    fg = [i for i, (s2, _c2, _k2, _t2) in enumerate(getattr(P, "SHOTS", []))
          if s2 == key and (getattr(P, "FOLEY", {}) or {}).get(i, -99) >= -6]
    if fg:
        import subprocess as _sp
        r = _sp.run(["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
                    capture_output=True, text=True)
        mv = None
        for ln in r.stderr.splitlines():
            if "mean_volume" in ln:
                try:
                    mv = float(ln.split("mean_volume:")[1].split("dB")[0])
                except Exception:
                    pass
        if mv is None:
            add("foley source audible", False,
                f"shots {fg} mix this clip FOREGROUND but the clip has NO audio "
                f"stream - the paid diegetic layer would ship silent")
        else:
            add("foley source audible", mv > -45.0,
                f"clip audio mean {mv:.1f}dB (foreground shots {fg}; "
                f"<= -45dB = effectively silent)")

    if act in ("EXTERIOR", "PAYOFF", "EVENT"):
        # LESSON 35 (2026-08-04): an invented red 'SR' badge in a plate recess shipped
        # through 8 builds - every gate measured geometry/motion, none READ text on the
        # subject, and the eye at strip scale cannot. Mechanize the ZOOM, not the
        # reading: write 2x crops of the delivered window's frame; the EYE must read
        # every legible string. Invented text = REJECT (22.5cr) or plan a DELOGO patch
        # (free at rebuild). OCR deliberately not attempted - stylised fonts defeat it.
        try:
            cap = cv2.VideoCapture(path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, _bi + _w2 // 2)
            okf, frf = cap.read()
            cap.release()
            if okf:
                Hh, Ww = frf.shape[:2]
                tiles = []
                for cyy in (0.30, 0.52, 0.74):      # upper / centre / lower bands
                    y0 = max(0, min(Hh - Hh // 4, int(Hh * cyy) - Hh // 8))
                    t_ = frf[y0:y0 + Hh // 4, Ww // 4: Ww // 4 + Ww // 2]
                    tiles.append(cv2.resize(t_, (Ww, Hh // 2)))
                adir = os.path.join(os.path.dirname(os.path.abspath(path)), "..", "analysis")
                os.makedirs(adir, exist_ok=True)
                zp = os.path.abspath(os.path.join(adir, f"textzoom_{key or 'x'}.png"))
                cv2.imwrite(zp, cv2.vconcat(tiles))
                add("on-subject text -> EYE", True,
                    f"2x text-zoom written ({os.path.basename(zp)}) - READ every legible "
                    f"string; invented badge/text = reject or DELOGO", False)
        except Exception as e:
            add("on-subject text -> EYE", False, f"zoom failed: {e}", False)

    stages_persona = bool(key) and key in P.SOURCES and "man from the" in P.SOURCES[key][4].lower()
    # FACE_OPTOUT (2026-08-05, his call on KK shot F). Some human shots are PRESENCE,
    # not face beats - the back/profile "looking out at the view" shot is real vlog
    # language, and KK's F prompt deliberately turns him toward the view. Opting out
    # must be DECLARED in the plan with a reason, never fudged by mislabelling the act
    # as EXTERIOR (which would lie about the shot containing a person). planqc 27
    # enforces that enough human sources still carry a readable face, so identity can
    # never be opted out of ENTIRELY.
    _optout = (getattr(P, "FACE_OPTOUT", {}) or {}).get(key)
    if _optout and (act == "HUMAN" or stages_persona):
        add("face READS (delivered window)", True,
            f"DECLARED PRESENCE SHOT, face-read waived — {_optout}", False)
    elif act == "HUMAN" or (act == "EVENT" and stages_persona):
        # The probe's killer defect: the face never read. Haar on the first 1.5s,
        # full resolution. A HUMAN/EVENT clip where no face is ever detected fails.
        # DELIVERED WINDOW, not the head (2026-08-05). This was the LAST head-based
        # measurement left in clipqc — the same trap that produced two false rejects
        # on 2026-08-04 (probe A, clip C) and was fixed everywhere EXCEPT here.
        # MEASURED on the KK batch: clip H ("watches the horizon, THEN turns to the
        # lens") read 1.3% in the first 1.5s and 19.4% at 4.88s. The head-based check
        # called it a REJECT and would have burned 22.5cr regenerating a clip whose
        # face beat was simply late — exactly where the prompt put it. The engine
        # centres every shot on its action peak, so scan the WHOLE clip and score the
        # best shot-length window, which is what the edit actually consumes.
        fc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        pc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
        cap = cv2.VideoCapture(path)
        hits = []          # (t_seconds, area_px)
        i = 0
        while True:
            ok, f = cap.read()
            if not ok:
                break
            if i % 3 == 0:
                g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
                r = list(fc.detectMultiScale(g, 1.1, 4, minSize=(36, 36))) or \
                    list(pc.detectMultiScale(g, 1.1, 4, minSize=(36, 36)))
                if len(r):
                    hits.append((i / fps, max(w * h for (_x, _y, w, h) in r)))
            i += 1
        cap.release()
        # best window of this source's longest planned use
        _win = _d2
        found, best, best_t = 0, 0, 0.0
        for t0 in [h[0] for h in hits] or [0.0]:
            inw = [h for h in hits if t0 <= h[0] < t0 + _win]
            if len(inw) > 0:
                a = max(h[1] for h in inw)
                if a > best:
                    best, found, best_t = a, len(inw), t0
        # PRESENCE IS NOT THE STANDARD - LEGIBILITY IS. The failed probe had a face in
        # 7 sampled frames at 18,496px^2 = 2.0% of frame, and by eye it never read.
        # Require >=3.5% of frame area: a face beat, not a face pixel.
        frac = best / float(c["W"] * c["H"])
        add("face READS (delivered window)", found >= 2 and frac >= 0.035,
            f"best {_win:.2f}s window at {best_t:.2f}s: {found} detections, largest "
            f"{frac*100:.1f}% of frame (>=3.5%: the failed Supra probe measured 2.0% "
            f"and never read by eye). Whole clip scanned — the edit centres on the "
            f"action peak, not the head.")

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
