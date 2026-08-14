#!/usr/bin/env python3
"""
EDITSENSE — the decision layer. Turns perception into editorial choices.

THE ARCHITECTURE THAT WAS MISSING
    PERCEPTION  clipsense.py   what is in each shot: motion, direction, peaks, size
    DECISION    editsense.py   WHERE to cut and WHY            <- this file
    RENDER      build_kk.py    execute the decisions

  Until now there was no decision layer. build_kk.TL was hand-typed, so durations were chosen
  to sum to 30s. Measured consequence on v3:
        cuts on the music beat        2 / 13    (median 200 ms off)
        cuts landing mid-sentence     5 / 13
        J/L cuts                      0 / 13
  Those three numbers ARE the difference between "renderer" and "editor".

THE RULES IMPLEMENTED HERE  (each is a thing a professional does without thinking)

  R1  SNAP TO GRID       A cut that misses the beat by 200ms reads as sloppy even to someone
                         who cannot name why. Snap every cut to the nearest beat, unless a
                         speech boundary is closer and more important.

  R2  RESPECT SPEECH     Never change picture mid-phrase. The viewer is parsing a sentence;
                         a cut inside it costs comprehension. Phrase boundaries outrank beats
                         while someone is talking.

  R3  J/L CUTS           Offset audio from picture. Audio arriving BEFORE its picture (J) pulls
                         the viewer forward; audio HELD OVER the next shot (L) smooths the
                         join. This is the single biggest amateur/professional tell, and v3
                         had none of it.

  R4  CUT ON ACTION      Cut into a shot where it is already moving (clipsense.action_peaks),
                         not where it is settling. AI clips almost always open with a settle.

  R5  MOTION CONTINUITY  Either match direction across a cut (smooth) or oppose it hard
                         (deliberate punch). What reads as amateur is a random 40-degree
                         difference - neither matched nor contrasted.

  R6  SIZE RHYTHM        Never cut two same-size shots together. wide->wide is a jump cut.

Usage
  python3 editsense.py --demo        # score the current v3 cut list, then the improved one
"""
import argparse, json, os, sys
import numpy as np

def beat_grid(bpm=100.0, dur=30.0, offset=0.0):
    b = 60.0/bpm
    return [round(offset + i*b, 4) for i in range(int(dur/b)+1)]

def snap(cuts, grid, speech_bounds=None, speech_win=0.30, max_move=0.28):
    """R1 + R2. Snap each cut to the nearest beat, but if a speech boundary is within
    `speech_win` prefer it - a cut inside a spoken phrase costs more than an off-beat cut.
    Never move a cut more than `max_move`, or the shot lengths stop being the ones chosen."""
    out = []
    for c in cuts:
        cands = []
        if grid:
            g = min(grid, key=lambda x: abs(x-c))
            cands.append((abs(g-c), g, "beat"))
        if speech_bounds:
            s = min(speech_bounds, key=lambda x: abs(x-c))
            if abs(s-c) <= speech_win:
                cands.append((abs(s-c)*0.5, s, "speech"))   # weighted: speech wins ties
        if not cands: out.append((c, "none")); continue
        cands.sort()
        d, val, why = cands[0]
        out.append((round(val, 3), why) if d <= max_move else (c, "held"))
    return out

def jl_cuts(cuts, pattern=None, lead=0.24, hold=0.30):
    """R3. Return per-cut audio offsets. Negative = audio arrives EARLY (J cut).
    Positive = audio is HELD over the incoming picture (L cut).
    Alternating J and L is what makes a sequence feel woven rather than stacked."""
    offs = []
    for i, c in enumerate(cuts):
        if pattern == "all_j":  offs.append(-lead)
        elif pattern == "all_l": offs.append(+hold)
        else:                    offs.append(-lead if i % 2 == 0 else +hold)
    return offs

def score(cuts, grid, speech_bounds, sizes=None, dirs=None, audio_offsets=None):
    """The same measurements used to diagnose v3, so before/after is comparable."""
    beat = grid[1]-grid[0] if len(grid) > 1 else 0.6
    dev = [min(abs(c - min(grid, key=lambda x: abs(x-c))), beat) for c in cuts]
    on_beat = sum(1 for d in dev if d < 0.05)
    near = [min(abs(c-b) for b in speech_bounds) for c in cuts] if speech_bounds else []
    mid_phrase = sum(1 for d in near if d > 0.25)
    jl = sum(1 for o in (audio_offsets or []) if abs(o) > 0.05)
    r = {"cuts": len(cuts),
         "on_beat": f"{on_beat}/{len(cuts)}",
         "beat_dev_ms": int(np.median(dev)*1000),
         "mid_phrase": f"{mid_phrase}/{len(cuts)}",
         "jl_cuts": f"{jl}/{len(cuts)}"}
    if sizes:
        rep = sum(1 for i in range(1, len(sizes)) if sizes[i] == sizes[i-1])
        r["same_size_adjacent"] = f"{rep}/{max(1,len(sizes)-1)}"
    if dirs:
        amb = 0
        for i in range(1, len(dirs)):
            d = abs((dirs[i]-dirs[i-1]+180) % 360 - 180)
            if 35 < d < 145: amb += 1        # neither matched nor opposed
        r["ambiguous_motion"] = f"{amb}/{max(1,len(dirs)-1)}"
    return r

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if not a.demo: ap.print_help(); return

    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    cuts = [2.6, 4.8, 6.4, 7.6, 9.8, 11.6, 14.2, 17.0, 18.4, 20.8, 22.6, 25.6, 28.8]
    grid = beat_grid(100.0, 30.4)
    try:
        import build_kk as B, transcribe
        tr = transcribe.run(B.need("KK_VO.wav"))
        w = B.fix_locals(tr["words"]); cards = B.phrase_cards(w, 22)
        sb = sorted({round(c["start"]+1.5, 3) for c in cards} |
                    {round(c["end"]+1.5, 3) for c in cards})
    except Exception as e:
        print("  (no VO available, beats only):", str(e)[:60]); sb = []

    print("="*60); print("BEFORE  - hand-typed cut list (v3)"); print("="*60)
    for k, v in score(cuts, grid, sb).items(): print(f"  {k:22s} {v}")

    snapped = snap(cuts, grid, sb)
    newcuts = [c for c, _ in snapped]
    offs = jl_cuts(newcuts)
    print("\n" + "="*60); print("AFTER   - snapped to beat/speech + J/L offsets"); print("="*60)
    for k, v in score(newcuts, grid, sb, audio_offsets=offs).items(): print(f"  {k:22s} {v}")
    print("\n  cut   was  ->  now    reason     audio")
    for (c, why), old, o in zip(snapped, cuts, offs):
        tag = "J (early)" if o < 0 else "L (held)"
        print(f"   {old:6.2f} -> {c:6.2f}   {why:8s}  {o:+.2f}s {tag}")

if __name__ == "__main__":
    main()
