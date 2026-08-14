#!/usr/bin/env python3
"""
REVERSE — extract the editing DNA of reference videos (Douyin / TikTok / anyone).

Why this instead of scraping: view counts tell you a video worked. They do NOT tell you HOW it
was cut, how fast, where the interrupts land, whether the cuts hit the beat, or how loud the mix
sits. That grammar is recoverable from the file itself — and it's the part you can actually copy.

Drop reference videos in a folder, run this, get a comparison table + the deltas vs your own cut.

Deps: ffmpeg + opencv-python-headless + numpy  (+ pacing.py / rhythm.py alongside)
Usage:
  python3 reverse.py refs/ --format vlog --mine INFLUENCER_v1.mp4 --out dna
"""
import os, sys, json, argparse, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pacing
try:
    import rhythm
    HAVE_RHYTHM = True
except Exception:
    HAVE_RHYTHM = False

VID = (".mp4",".mov",".mkv",".webm",".m4v")

def audio_profile(path):
    """Loudness + whether cuts land on a musical grid."""
    out = {}
    if not HAVE_RHYTHM: return out
    try:
        x = rhythm.pcm(path)
        if x.size == 0: return out
        flux, hop = rhythm.stft_flux(x)
        onsets = rhythm.pick_onsets(flux, hop)
        bpm, grid = rhythm.estimate_tempo(flux, hop, onsets=onsets)
        out["bpm"] = bpm
        out["onsets"] = len(onsets)
        cuts = rhythm.video_cuts(path)
        if cuts and grid is not None and len(grid):
            g = rhythm.grade(rhythm.deviations(__import__("numpy").array(cuts), grid), "cuts vs beat")
            out["cuts_on_beat_pct"] = g.get("pct_within_50ms")
            out["cuts_beat_verdict"] = g.get("verdict")
    except Exception as e:
        out["error"] = str(e)[:80]
    return out

def profile(path, fmt, known_cuts=None):
    """known_cuts: the cut times the BUILD actually made.

    LEDGER E4 - the detector is blind to same-palette cuts. Measured: a file with 8 shots
    in 19.68s (~21 cuts/min) came back as 6.1 cuts/min, and shot_median as 5.0s when the
    real median was 2.33s. The DNA diff then reported a -80% gap that was partly the
    detector's own blindness. A build KNOWS where it cut - so hand the truth over and use
    detection as cross-check only, never as the source.
    """
    p = pacing.analyse(path, fmt)
    a = audio_profile(path)
    if known_cuts:
        import statistics as _st
        det = p["cuts"]
        cuts = sorted(float(c) for c in known_cuts)
        dur = p["duration"] or 0.0
        bounds = [0.0] + cuts + [dur]
        lens = [round(bounds[i+1]-bounds[i], 3) for i in range(len(bounds)-1)
                if bounds[i+1] > bounds[i]]
        p["cuts"] = len(cuts)
        p["cuts_per_min"] = round(len(cuts)/(dur/60.0), 1) if dur else 0.0
        p["shot_len_median"] = round(_st.median(lens), 2) if lens else 0.0
        p["shot_len_max"] = round(max(lens), 2) if lens else 0.0
        p["cut_rate_variation"] = (round(_st.pstdev(lens)/_st.median(lens), 2)
                                   if len(lens) > 1 and _st.median(lens) else 0.0)
        print(f"  [known-cuts] using {len(cuts)} declared cuts; "
              f"the detector found {det} ({det*100//max(1,len(cuts))}% of them)")
        if det < len(cuts) * 0.7:
            print(f"  [known-cuts] detector missed {len(cuts)-det} cut(s) - same-palette "
                  f"blindness (E4). This is why declared cuts win.")
    return {
        "file": os.path.basename(path),
        "duration": p["duration"],
        "cuts": p["cuts"],
        "cuts_per_min": p["cuts_per_min"],
        "shot_median": p["shot_len_median"],
        "shot_max": p["shot_len_max"],
        "rate_variation": p["cut_rate_variation"],
        "hook_motion": p["hook"]["motion"],
        "dead_zones": len(p["dead_zones"]),
        "bpm": a.get("bpm"),
        "cuts_on_beat_pct": a.get("cuts_on_beat_pct"),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder"); ap.add_argument("--format", default="vlog", choices=list(pacing.FORMATS))
    ap.add_argument("--mine"); ap.add_argument("--out", default="dna")
    ap.add_argument("--mine-cuts", dest="mine_cuts",
                    help="JSON with a \"cuts\" list (e.g. beatplan.py --json) - "
                         "the cuts the build ACTUALLY made. Overrides detection.")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    files = [os.path.join(a.folder,f) for f in sorted(os.listdir(a.folder)) if f.lower().endswith(VID)]
    if not files:
        print(f"No videos in {a.folder}"); return
    print(f"Profiling {len(files)} reference videos as format='{a.format}'...\n")

    refs = []
    for f in files:
        try:
            refs.append(profile(f, a.format)); print("  ok", os.path.basename(f))
        except Exception as e:
            print("  FAIL", os.path.basename(f), str(e)[:70])
    if not refs: return

    cols = ["file","duration","cuts_per_min","shot_median","shot_max","rate_variation",
            "hook_motion","dead_zones","bpm","cuts_on_beat_pct"]
    print("\n" + " | ".join(c[:13].ljust(13) for c in cols))
    print("-"*len(cols)*16)
    for r in refs:
        print(" | ".join(str(r.get(c,""))[:13].ljust(13) for c in cols))

    def agg(k):
        v=[r[k] for r in refs if isinstance(r.get(k),(int,float))]
        return (round(st.median(v),2), round(min(v),2), round(max(v),2)) if v else (None,None,None)

    print("\n=== THE REFERENCE DNA (median [min-max]) ===")
    summary={}
    for k in ["duration","cuts_per_min","shot_median","shot_max","rate_variation",
              "hook_motion","bpm","cuts_on_beat_pct"]:
        m,lo,hi = agg(k); summary[k]={"median":m,"min":lo,"max":hi}
        if m is not None: print(f"  {k:<18} {m:>8}   [{lo} – {hi}]")

    result={"format":a.format,"n_refs":len(refs),"refs":refs,"dna":summary}

    if a.mine and os.path.exists(a.mine):
        kc = None
        if a.mine_cuts and os.path.exists(a.mine_cuts):
            _d = json.load(open(a.mine_cuts))
            kc = _d.get("cuts") if isinstance(_d, dict) else _d
        mine = profile(a.mine, a.format, known_cuts=kc)
        result["mine"]=mine
        print(f"\n=== YOURS vs THE REFERENCE ({os.path.basename(a.mine)}) ===")
        gaps=[]
        for k in ["cuts_per_min","shot_median","shot_max","rate_variation","hook_motion","cuts_on_beat_pct"]:
            m=summary.get(k,{}).get("median"); y=mine.get(k)
            if m is None or not isinstance(y,(int,float)): continue
            d = y-m
            pct = (d/m*100) if m else 0
            flag = "  <-- GAP" if abs(pct)>30 else ""
            print(f"  {k:<18} yours {str(y):>8}   ref {str(m):>8}   delta {d:+.2f} ({pct:+.0f}%){flag}")
            if abs(pct)>30: gaps.append((k,y,m,pct))
        result["gaps"]=[{"metric":g[0],"yours":g[1],"reference":g[2],"pct":round(g[3],1)} for g in gaps]
        if gaps:
            print("\n  ACTIONS:")
            for k,y,m,pct in gaps:
                if k=="cuts_per_min":
                    print(f"   - cut rate is {abs(pct):.0f}% {'below' if pct<0 else 'above'} reference "
                          f"({y} vs {m}/min). Re-cut to ~{m}/min.")
                elif k=="shot_max":
                    print(f"   - longest shot {y}s vs {m}s. Break the long shot or add an interrupt.")
                elif k=="hook_motion":
                    print(f"   - hook motion {y} vs {m}. {'Add movement/punch-in to frame 1.' if pct<0 else 'Hook is busier than reference.'}")
                elif k=="cuts_on_beat_pct":
                    print(f"   - only {y}% of cuts on the beat vs {m}%. Quantise cuts to the grid.")
                elif k=="rate_variation":
                    print(f"   - rhythm variation {y} vs {m}. {'Vary pace more.' if pct<0 else 'Steadier pacing may help.'}")

    json.dump(result, open(os.path.join(a.out,"dna.json"),"w"), indent=2)
    print(f"\nwritten: {a.out}/dna.json")
    print("\nNOTE: this measures HOW they cut, not whether the idea was good. Pair it with a "
          "scene-by-scene analysis for the storytelling layer.")

if __name__ == "__main__":
    main()
