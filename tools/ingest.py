#!/usr/bin/env python3
"""
INGEST — the organizer between generation and the edit. His diagnosis, 2026-08-04:

  "after higgsfield generated these files, there is no organizer to organize those
   clips to let the video editing automation know that this clip is visual hook and
   the second clip is content..."

He was pointing at a real gap. The plan knows each source's ROLE (act), but nothing
catalogued what each delivered CLIP actually contains — where its action peaks are,
where it settles, where a softbox leaks into frame, whether it carries audio. The
engine allocated windows against assumptions; the duplicates and the shipped softbox
both walked through that gap.

This writes projects/<name>/clips/manifest.json — one entry per source:

    role            the act from the plan (EVENT / EXTERIOR / HUMAN / PAYOFF ...)
    file, duration, fps
    action_peaks_s  measured (clipsense)
    best_in_s       the strongest moment
    settle_head_s   how long the clip takes to start MOVING
    audio           present? approximate level (a silent clip cannot carry foley)
    ban_spans       plan BAN_SPANS  +  AUTO-DETECTED softbox/light-rig spans
                    (large bright blob in the top corners — the exact defect that
                     shipped at 1.8s in WRX v1)

The ENGINE reads ban_spans at build time (union with the plan's). VERIFY's storyboard
tally reads the same manifest the build wrote. One catalogue, three consumers.

USAGE
  python3 tools/ingest.py wrx          # after clips are downloaded
  python3 tools/ingest.py wrx --json   # print the manifest too
"""
import os, sys, json, argparse, importlib

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "tools"))


def softbox_spans(path, thresh=215, min_blob=0.02):
    """Large bright blob in the top corners = light rig in frame. Returns [(a,b)]
    spans in seconds. A streetlight is a point (<1% blob); a softbox measured
    5-10% and decayed to background by 2.0s on WRX clip B."""
    import cv2
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    spans, cur, i = [], None, 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        h, w = g.shape
        hit = False
        for reg in (g[:int(h*0.55), :int(w*0.45)], g[:int(h*0.55), int(w*0.55):]):
            bw = (reg > thresh).astype("uint8")
            n, _lab, stats, _c = cv2.connectedComponentsWithStats(bw)
            if n > 1 and max(s[4] for s in stats[1:]) / bw.size > min_blob:
                hit = True
                break
        t = i / fps
        if hit and cur is None:
            cur = t
        if not hit and cur is not None:
            spans.append((round(cur, 2), round(t + 0.1, 2))); cur = None
        i += 1
    if cur is not None:
        spans.append((round(cur, 2), round(i / fps, 2)))
    cap.release()
    return [s for s in spans if s[1] - s[0] > 0.3]     # ignore single-frame flashes


def settle_head(c):
    """Seconds before the clip starts MOVING — clipsense already measures this."""
    return c.get("stillness_head_s", 0.0)


def audio_info(path):
    import subprocess, tempfile, wave, numpy as np
    w = os.path.join(tempfile.gettempdir(), "_ingest_a.wav")
    r = subprocess.run(f'ffmpeg -y -v error -i "{path}" -vn -ac 1 -ar 22050 '
                       f'-c:a pcm_s16le "{w}"', shell=True, capture_output=True)
    if r.returncode != 0 or not os.path.exists(w) or os.path.getsize(w) < 1000:
        return {"present": False}
    wv = wave.open(w)
    x = np.frombuffer(wv.readframes(wv.getnframes()), dtype=np.int16).astype(float) / 32768.0
    wv.close()
    if not len(x) or float(np.sqrt(np.mean(x ** 2))) < 1e-4:
        return {"present": False}
    return {"present": True,
            "rms_db": round(20 * float(np.log10(np.sqrt(np.mean(x ** 2)))), 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    P = importlib.import_module(f"plans.{a.plan}")
    import clipsense
    pdir = os.path.join(HERE, "projects", a.plan)
    plan_bans = getattr(P, "BAN_SPANS", {}) or {}

    man = {}
    print("=" * 78)
    print(f"INGEST  {P.PROJECT}")
    print("=" * 78)
    print(f"{'src':>4} {'role':10} {'dur':>5} {'peaks':>5} {'settle':>6} "
          f"{'audio':>8}  ban spans")
    for key, (_lab, _col, act, _pl, _pr) in P.SOURCES.items():
        fn = getattr(P, "CLIPS", {}).get(key)
        path = os.path.join(pdir, "clips", fn) if fn else None
        if not path or not os.path.exists(path):
            print(f"{key:>4} {act:10} MISSING {fn}")
            continue
        c = clipsense.analyse(path)
        # Auto-detected bright blobs are SUSPECTS for the eye, never binding bans:
        # first run flagged C's rain highlights and I's headlight rim as 'softbox'
        # (C 0-5.04s = the whole clip). A detector that cannot tell a rig from a
        # highlight is judgement's assistant, not a gate. Only plan BAN_SPANS bind.
        suspects = softbox_spans(path)
        bans = [list(b) for b in plan_bans.get(key, [])]
        au = audio_info(path)
        man[key] = {"file": fn, "role": act, "duration": c["duration"],
                    "fps": c.get("fps", 24.0),
                    "action_peaks_s": c["action_peaks_s"],
                    "best_in_s": c["best_in_s"],
                    "settle_head_s": settle_head(c),
                    "audio": au, "ban_spans": bans,
                    "suspect_bright_spans": [list(s) for s in suspects]}
        flag = ""
        un = [s for s in suspects
              if not any(abs(s[0]-b[0]) < 0.3 and abs(s[1]-b[1]) < 0.6 for b in bans)]
        if un:
            flag = f"  SUSPECT bright rig? {un} — LOOK, then promote to BAN_SPANS if real"
        print(f"{key:>4} {act:10} {c['duration']:5.1f} {len(c['action_peaks_s']):5d} "
              f"{man[key]['settle_head_s']:6.2f} "
              f"{(str(au.get('rms_db')) + 'dB') if au.get('present') else 'SILENT':>8}  "
              f"{bans if bans else '-'}{flag}")

    out = os.path.join(pdir, "clips", "manifest.json")
    json.dump(man, open(out, "w"), indent=1)
    print(f"\n  manifest -> {out}")
    silent = [k for k, v in man.items() if not v["audio"].get("present")]
    if silent:
        print(f"  !! SILENT clips {silent} — their FOLEY gains have nothing to gain")
    if a.json:
        print(json.dumps(man, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
