#!/usr/bin/env python3
"""
LOT — the build. REAL FOOTAGE. THE PLAN DECIDES; THIS FILE OBEYS.

The structural thing this build does that V1-V5 did not:
  HIS AUDIO IS ONE UNBROKEN 15.16s TAKE. Only the PICTURE cuts.
  When he says X1 the X1 is on screen; when he says X5, the X5; when he says
  "this red one", the red X4. That is P.CUTAWAYS, read from TRANSCRIPT.json word
  windows - not from motion scores (L175).

Everything numeric is read from plans/lot.py. If this file wants to decide
something, the decision was missing from the plan and the PLAN is what gets fixed.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "plans"))
sys.path.insert(0, os.path.join(HERE, "tools"))
import lot as P

RAW  = os.path.join(HERE, "Raw footage")
PROJ = os.path.join(HERE, "projects", "lot")
SEG  = "/tmp/lotseg"
CAT  = {d["idx"]: d for d in json.load(open(os.path.join(PROJ, "raw_catalogue.json")))}
FPS, W, H = P.FPS, P.W, P.H
BEAT = P.BEAT


def src_path(name):
    return os.path.join(RAW, CAT[P.SRC_CLIP[name]]["file"])


def vf(name, dur, fade=""):
    """No hflip anywhere (P.NO_FLIP). Clip 41 would need hflip,vflip - it is not used."""
    rot = ",hflip,vflip" if P.SRC_CLIP.get(name) in getattr(P, "ROTATE_180", []) else ""
    return (f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H}{rot}{fade}")


def build():
    os.makedirs(SEG, exist_ok=True)
    for f in os.listdir(SEG):
        os.remove(os.path.join(SEG, f))

    # ---- the video track, in order ------------------------------------------------
    # (source, t_in, duration)  t_in for beats = a window named in CUT_JUSTIFICATION
    IN = {"X5_LIGHT": 6.0, "X4_FRONT": 8.0, "X1_BADGE": 1.2, "X4_WHEEL": 6.2,
          "BOTH": 14.0, "X5_SIDE": 8.0, "X1_START": 1.3,
          "X1_FRONT": 1.0, "X1_WHEEL": 1.0, "X5_BADGE": 2.0, "X5_FRONT": 2.0,
          "X4_BADGE": 1.8, "X4_ROUNDEL": 3.0}
    beat2 = round(2 * BEAT, 4)                      # 1.2245s - the plan's "beat" kind
    seq = [(n, IN[n], beat2) for n in ("X5_LIGHT", "X4_FRONT", "X1_BADGE", "X4_WHEEL")]
    DIP = len(seq) - 1                              # dip lands on the last hook shot

    # the take: his video, interrupted only where the plan says a car is named
    s_in, s_out = P.SPINE_IN, P.SPINE_OUT
    cuts = sorted([(a, b, n) for (a, b), n, _w in
                   [((a, b), n, w) for (a, b), n, w in P.CUTAWAYS]])
    # collapse the plan's overlapping windows into a non-overlapping strip
    strip, t = [], s_in
    for a, b, n in cuts:
        a = max(a, t)
        if a > t:
            strip.append(("SPINE", t, round(a - t, 4)))
        if b > a:
            strip.append((n, IN[n], round(b - a, 4)))
        t = max(t, b)
    if t < s_out:
        strip.append(("SPINE", t, round(s_out - t, 4)))
    take_start = round(len(seq) * beat2, 4)
    seq += strip
    seq += [("BOTH", IN["BOTH"], beat2), ("X5_SIDE", IN["X5_SIDE"], beat2),
            ("X1_START", IN["X1_START"], round(P.BEATS["hold"], 4))]

    jobs = []
    for i, (name, tin, dur) in enumerate(seq):
        fade = ""
        if i == DIP:
            fade = f",fade=t=out:st={dur-0.16:.3f}:d=0.16:color=black"
        if i == DIP + 1:
            fade = ",fade=t=in:st=0:d=0.16:color=black"
        if i == len(seq) - 1:
            fade = f",fade=t=out:st={dur-0.6:.3f}:d=0.6:color=black"
        jobs.append(f'ffmpeg -y -v error -ss {tin:.3f} -i "{src_path(name)}" -t {dur:.3f} '
                    f'-an -vf "{vf(name, dur, fade)}" -c:v libx264 -crf 18 -preset veryfast '
                    f'-pix_fmt yuv420p {SEG}/v{i:02d}.mp4')
    open(f"{SEG}/jobs.sh", "w").write(
        "#!/bin/bash\n" + "\n".join(j + " &" + ("\nwait" if (k + 1) % 6 == 0 else "")
                                    for k, j in enumerate(jobs)) + "\nwait\n")
    subprocess.run(["bash", f"{SEG}/jobs.sh"], capture_output=True)
    made = sorted(f for f in os.listdir(SEG) if f.startswith("v") and f.endswith(".mp4"))
    total = round(sum(d for _n, _t, d in seq), 4)
    print(f"video: {len(made)}/{len(seq)} segments · take starts {take_start}s · "
          f"total {total}s (plan target {P.TARGET_S})")
    for i, (n, t0, d) in enumerate(seq):
        print(f"   {i:2d} {n:<11} t_in {t0:6.2f}  {d:5.2f}s")
    return seq, take_start, total


def write_manifests(seq, blends=frozenset({0, 1, 2, 14, 15}), xfade=0.12):
    """L182: THE BUILD KNOWS ITS OWN CUTS AND MUST HAND THEM TO THE GATE. This builder
    shipped v6-v9 with no manifests; 9 of verify's checks answered NOT MEASURED on the
    delivered film and nothing flagged the pattern. Never again: manifests are written
    by the same function that makes the segments, from the same list."""
    os.makedirs(os.path.join(PROJ, "audio"), exist_ok=True)
    os.makedirs(os.path.join(PROJ, "tmp"), exist_ok=True)
    cuts, b = [], [0.0]
    for i, (_n, _t, d) in enumerate(seq):
        nd = d - (xfade if i in blends else 0)
        b.append(round(b[-1] + nd, 4))
        if i < len(seq) - 1:
            cuts.append(b[-1])
    json.dump({"cuts": cuts, "planned": cuts, "bpm": P.BPM, "beat": round(P.BEAT, 4),
               "_source": "tools/build_lot.py - the build's own segment grid (L182)"},
              open(os.path.join(PROJ, "audio", "lot_cuts.json"), "w"), indent=1)
    json.dump([{"shot": i, "src": n, "tin": t, "has_peak": True,
                "frames": round(d * FPS), "in": b[i]}
               for i, (n, t, d) in enumerate(seq)],
              open(os.path.join(PROJ, "tmp", "manifest_peaks.json"), "w"), indent=1)
    return cuts


if __name__ == "__main__":
    seq, take_start, total = build()
    json.dump({"seq": seq, "take_start": take_start, "total": total},
              open(f"{SEG}/seq.json", "w"), indent=1)
    cuts = write_manifests(seq)
    print(f"manifests -> projects/lot/audio + tmp ({len(cuts)} cuts)")
