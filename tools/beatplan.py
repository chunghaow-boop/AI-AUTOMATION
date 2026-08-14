#!/usr/bin/env python3
"""
BEATPLAN — turn a BPM into a shot plan that BURSTS and RESTS, on the grid.

WHY THIS EXISTS
  Every hand-typed timeline in this repo picked durations that summed to the target length.
  Measured consequence, car cinematic:

      shot_median   2.00-2.50s   vs   0.77s in his references     (2.6-3.2x too slow)
      cuts_per_min       6-28    vs   44.7                        (up to -80%)
      cuts_on_beat            0%                                  (never once)
      rate_variation        1.0  vs   1.5                         (a metronome)

  Uniform shot lengths are the single clearest amateur tell in this system. The references
  do not cut at a constant rate - they cut in CLUSTERS one beat apart, then hold:

      8.27 / 8.63 / 9.03s      = 0.40s apart at 145.8 BPM = exactly one beat
      14.80 / 15.20 / 15.60s   = the same pattern again

  So the plan is: BURST (n cuts at 1 beat) -> HOLD (m beats) -> BURST -> HOLD.
  Everything lands on the grid by construction, so editsense.snap has nothing to fix.

THIS FILE DECIDES LENGTHS AND BOUNDARIES ONLY.
  It does not choose WHICH clip goes where - that is clipsense (perception) + editsense
  (decision). Feed beatplan's boundaries into editsense.snap/score alongside real cuts.

Usage
  python3 beatplan.py --bpm 150 --dur 20
  python3 beatplan.py --bpm 150 --dur 20 --pillar car_cinematic --json plan.json
  python3 beatplan.py --bpm 150 --dur 20 --pattern 6,4,5,5,4,4
"""
import argparse, json, os, sys
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# measured from his references - the fallbacks only apply if the profile is missing
FALLBACK = {
    "car_cinematic": {"shot_median_s": 0.77, "cuts_per_min": 44.7, "blended_pct": 20},
    "travel_vlog":   {"shot_median_s": 1.13, "cuts_per_min": 40.3, "blended_pct": 0},
}


def load_profile(pillar):
    p = os.path.join(ROOT, "assets", "pillars", "PILLAR-PROFILES.json")
    if not os.path.exists(p):
        p = os.path.join(ROOT, "pillars", "PILLAR-PROFILES.json")
    if os.path.exists(p):
        try:
            d = json.load(open(p)).get(pillar)
            if d:
                return d
        except Exception:
            pass
    print(f"  !! no PILLAR-PROFILES.json found - using FALLBACK numbers for {pillar}.")
    print(f"  !! these are a snapshot and expire. Measure, do not trust this path.")
    return FALLBACK.get(pillar, FALLBACK["car_cinematic"])


def plan(bpm, total, pattern=None, min_beats=2, hold_beats=5):
    """Return [(start, dur, kind)] snapped to the beat grid.

    pattern: list of ints. Odd positions are BURST sizes (number of 1-beat cuts),
             even positions are HOLD lengths in beats. Default alternates.
    """
    beat = 60.0 / bpm
    n_beats_total = int(round(total / beat))
    if pattern is None:
        # burst, hold, burst, hold ... sized so the whole thing fills `total`
        pattern, used, flip = [], 0, True
        while used < n_beats_total:
            if flip:
                n = min(5, max(3, n_beats_total // 6))
                pattern.append(n)
                used += n * min_beats
            else:
                pattern.append(hold_beats)
                used += hold_beats
            flip = not flip

    shots, t, beats_used, kind_flip = [], 0.0, 0, True
    for p in pattern:
        if beats_used >= n_beats_total:
            break
        if kind_flip:                       # BURST: p cuts of min_beats each
            for _ in range(p):
                if beats_used >= n_beats_total:
                    break
                d = min_beats * beat
                shots.append((round(t, 4), round(d, 4), "burst"))
                t += d
                beats_used += min_beats
        else:                               # HOLD: one shot of p beats
            d = p * beat
            shots.append((round(t, 4), round(d, 4), "hold"))
            t += d
            beats_used += p
        kind_flip = not kind_flip
    return shots, beat


def report(shots, beat, bpm, prof, total):
    durs = [d for _s, d, _k in shots]
    if not durs:
        print("  !! empty plan")
        return False
    med = st.median(durs)
    cpm = (len(shots) - 1) / (sum(durs) / 60.0)
    var = st.pstdev(durs) / med if med else 0.0
    tgt_med = prof.get("shot_median_s", 0.77)
    tgt_cpm = prof.get("cuts_per_min", 44.7)

    print(f"\n  {len(shots)} shots over {sum(durs):.2f}s at {bpm:.1f} BPM "
          f"(beat {beat*1000:.0f}ms)")
    print(f"  {'metric':18s} {'plan':>8s} {'target':>8s}")
    print(f"  {'median shot':18s} {med:8.2f} {tgt_med:8.2f}")
    print(f"  {'cuts/min':18s} {cpm:8.1f} {tgt_cpm:8.1f}")
    print(f"  {'rate_variation':18s} {var:8.2f} {1.5:8.2f}   (0 = metronome)")

    ok = True
    if med > tgt_med * 1.6:
        print(f"  x median {med:.2f}s is {med/tgt_med:.1f}x the target - shots too long")
        ok = False
    # A gate that only catches "too slow" let a 102 cuts/min plan pass against a 44.7
    # target on the first run. Overcutting is just as wrong as undercutting and reads
    # as a strobe, not an edit.
    if med < tgt_med * 0.55:
        print(f"  x median {med:.2f}s is {tgt_med/med:.1f}x FASTER than target - strobing")
        ok = False
    if cpm > tgt_cpm * 1.5:
        print(f"  x {cpm:.1f} cuts/min vs {tgt_cpm:.1f} target - overcut")
        ok = False
    if cpm < tgt_cpm * 0.55:
        print(f"  x {cpm:.1f} cuts/min vs {tgt_cpm:.1f} target - undercut")
        ok = False
    if var < 0.35:
        print(f"  x rate_variation {var:.2f} is flat. Bursts and holds are not "
              f"differentiated enough.")
        ok = False
    if abs(sum(durs) - total) > beat:
        print(f"  ! plan is {sum(durs):.2f}s against a {total:.2f}s request "
              f"(grid-quantised, expected)")
    print("  " + ("OK  plan matches the profile" if ok else "BLOCK  fix before cutting"))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bpm", type=float, required=True)
    ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--pillar", default="car_cinematic")
    ap.add_argument("--pattern", help="comma ints: burst,hold,burst,hold...")
    ap.add_argument("--hold", type=int, default=5, help="default hold length in beats")
    ap.add_argument("--minbeats", type=int, default=2, help="beats per burst shot")
    ap.add_argument("--json")
    a = ap.parse_args()

    prof = load_profile(a.pillar)
    pat = [int(x) for x in a.pattern.split(",")] if a.pattern else None
    shots, beat = plan(a.bpm, a.dur, pat, min_beats=a.minbeats, hold_beats=a.hold)

    print(f"[beatplan] {a.pillar} @ {a.bpm:.1f} BPM")
    print(f"  {'#':>3s} {'start':>7s} {'dur':>6s}  kind")
    for i, (s, d, k) in enumerate(shots):
        print(f"  {i:3d} {s:7.3f} {d:6.3f}  {k}")

    ok = report(shots, beat, a.bpm, prof, a.dur)

    if a.json:
        json.dump({"bpm": a.bpm, "beat": beat, "pillar": a.pillar,
                   "cuts": [s for s, _d, _k in shots][1:],
                   "shots": [{"start": s, "dur": d, "kind": k} for s, d, k in shots]},
                  open(a.json, "w"), indent=1)
        print(f"  written: {a.json}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
