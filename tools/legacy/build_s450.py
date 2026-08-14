#!/usr/bin/env python3
"""
BUILD_S450 — 15s Mercedes S450 car cinematic, built to the MEASURED reference profile.

TARGETS (assets/pillars/PILLAR-PROFILES.json, from 5 references he selected)
    median shot   0.77s     Crown scored 2.00s  (2.6x too slow)
    cuts/min      44.7      Crown scored 28.4
    blended       20%       Crown scored 0%
    BPM           140-165   Crown used 90
    sub-bass      60-92%    Crown 48%

CUT GRAMMAR, from the frame-level study of his references:
    most cuts are HARD (33-67ms). Blends are RARE and WIDE (240-560ms), used as section
    punctuation. Cuts arrive in BURSTS one beat apart, then hold.
    Measured: 8.27 / 8.63 / 9.03s = exactly one beat at 145.8 BPM.

18 shots from 4 generations. 150 BPM, beat = 0.400s.
"""
import os, subprocess, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W   = os.path.join(ROOT, "work")
A   = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "output")
TMP = os.path.join(W, "_s450_tmp")
sys.path.insert(0, os.path.join(ROOT, "tools"))

BPM  = 150.0
BEAT = 60.0/BPM        # 0.400s

def sh(c, cwd=None):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr

def dur(p):
    _, o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"')
    try: return float(o.strip().splitlines()[0])
    except Exception: return 0.0

FRONT="S450_A_front.mp4"; WIDE="S450_B_wide.mp4"
WHEEL="S450_C_wheel.mp4"; INT="S450_D_interior.mp4"

# tag, source, in-point, beats, crop(scale,cx,cy), transition-out
TL = [
 # BURST A - the ignition, six one-beat cuts
 ("a1", FRONT, 0.20, 1, (1.9,0.50,0.45), None),
 ("a2", FRONT, 1.10, 1, (1.0,0.50,0.50), None),
 ("a3", FRONT, 1.90, 1, (2.4,0.50,0.40), None),
 ("a4", FRONT, 2.60, 1, (1.4,0.50,0.55), None),
 ("a5", FRONT, 3.30, 1, (2.8,0.50,0.42), None),
 ("a6", FRONT, 4.00, 1, (1.2,0.50,0.50), "mask_slice"),   # BLEND 1
 # HOLD - the reveal
 ("h1", WIDE,  0.30, 4, (1.0,0.50,0.50), None),
 # BURST B - the details
 ("b1", WHEEL, 0.20, 1, (1.0,0.50,0.50), None),
 ("b2", WHEEL, 1.00, 1, (2.0,0.50,0.55), None),
 ("b3", WHEEL, 1.80, 1, (1.3,0.50,0.45), None),
 ("b4", WHEEL, 2.60, 1, (2.6,0.50,0.50), None),
 ("b5", WHEEL, 3.40, 1, (1.6,0.50,0.60), "whip"),         # BLEND 2
 # HOLD - inside
 ("h2", INT,   0.40, 5, (1.0,0.50,0.50), None),
 # BURST C - the cabin
 ("c1", INT,   1.60, 1, (2.0,0.45,0.45), None),
 ("c2", INT,   2.30, 1, (1.3,0.55,0.55), None),
 ("c3", INT,   3.00, 1, (2.6,0.50,0.40), None),
 ("c4", INT,   3.70, 1, (1.5,0.50,0.60), "speedramp"),    # BLEND 3
 # LOOP - back to the grille
 ("z1", FRONT, 0.20, 4, (1.9,0.50,0.45), None),
]

def slots():
    t, out = 0.0, []
    for r in TL:
        L = round(r[3]*BEAT, 4)
        out.append((r[0], round(t,4), L)); t += L
    return out, round(t,4)

def need(f): return os.path.join(W, f)

def check():
    srcs = sorted({r[1] for r in TL})
    miss = [s for s in srcs if not os.path.exists(need(s))]
    if miss:
        print("!! MISSING:"); [print("   -",m) for m in miss]; return False
    _, total = slots()
    print(f"OK  {len(srcs)} sources -> {len(TL)} shots, {total:.2f}s at {BPM:.0f} BPM")
    return True

def build_segments(force=False):
    os.makedirs(TMP, exist_ok=True)
    try: import animate as AN
    except Exception: AN=None
    sl,_ = slots(); segs=[]
    for (tag, src, tin, _b, crop, _tr), (_, t0, L) in zip(TL, sl):
        p=need(src); o=os.path.join(TMP, f"s{tag}.mp4")
        spec=f"{src}|{tin}|{L}|{crop}"
        sf=o+".spec"
        if (not force and os.path.exists(o) and abs(dur(o)-L)<0.08
                and os.path.exists(sf) and open(sf).read()==spec):
            segs.append(o); continue
        avail=dur(p)
        if avail < tin+L-0.05: tin=max(0.0, avail-L-0.05)
        done=False
        if AN and crop and crop[0] > 1.05:
            try:
                trimmed=os.path.join(TMP,f"t{tag}.mp4")
                sh(f'ffmpeg -y -v error -ss {tin} -t {L} -i "{p}" -vf '
                   f'"scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,'
                   f'fps=30,setsar=1" -an -c:v libx264 -crf 18 -preset veryfast "{trimmed}"')
                AN.enliven(trimmed, o, dur=L, preset="generic", zoom=0.06, crop=crop, quiet=True)
                done=True
            except Exception as e: print(f"  !! {tag}: {str(e)[:50]}")
        if not done:
            vf="scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1"
            if crop and crop[0] > 1.05:
                cs,cx,cy=crop
                vf=(f"crop=iw/{cs}:ih/{cs}:(iw-iw/{cs})*{cx}:(ih-ih/{cs})*{cy},"
                    f"scale=720:1280,fps=30,setsar=1")
            sh(f'ffmpeg -y -v error -ss {tin} -t {L} -i "{p}" -vf "{vf}" -an '
               f'-c:v libx264 -crf 19 -preset veryfast -pix_fmt yuv420p "{o}"')
        if os.path.exists(o):
            open(sf,"w").write(spec); segs.append(o)
    print(f"  {len(segs)}/{len(TL)} segments")
    return segs

def apply_blends(segs):
    """Only 3 blends in 15s = 18%, matching the measured 20%. Everything else hard."""
    try: import fx
    except Exception as e:
        print("  !! fx:", str(e)[:50]); return segs, 0
    out=list(segs); n=0
    for i,(tag,_,_,_,_,tr) in enumerate(TL):
        if not tr or i+1>=len(out) or out[i] is None or out[i+1] is None: continue
        o=os.path.join(TMP, f"bx{tag}.mp4")
        try:
            fx.FX[tr](out[i], out[i+1], o, d=0.40, W=720, H=1280, fps=30)
            if os.path.exists(o) and dur(o)>0.5:
                print(f"  blend {tr:11s} at seam {tag} -> {dur(o):.2f}s")
                out[i]=o; out[i+1]=None; n+=1
        except Exception as e: print(f"  !! {tr}@{tag}: {str(e)[:60]}")
    return [x for x in out if x], n

def concat(segs, o):
    l=os.path.join(TMP,"list.txt")
    open(l,"w").write("".join(f"file '{s}'\n" for s in segs))
    rc,_=sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{l}" -c copy -an "{o}"')
    if rc!=0 or dur(o)<1:
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{l}" -c:v libx264 -crf 19 '
           f'-preset veryfast -pix_fmt yuv420p -an "{o}"')
    return o

if __name__ == "__main__":
    print("="*58); print("BUILD: Mercedes S450 - 15s car cinematic"); print("="*58)
    if not check(): sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    sl,total = slots()
    print(f"\n  shot lengths: {sorted(set(round(L,2) for _,_,L in sl))}")
    print(f"  median shot : {sorted(L for _,_,L in sl)[len(sl)//2]:.2f}s   target 0.77s")
    print(f"  cuts/min    : {(len(TL)-1)/(total/60):.1f}   target 44.7")
    print("\n[1/3] segments"); segs=build_segments()
    if len(segs)!=len(TL): sys.exit(1)
    print("\n[2/3] blends"); segs,nb=apply_blends(segs)
    print(f"  {nb} blend(s) = {100*nb//(len(TL)-1)}%   target 20%")
    print("\n[3/3] concat")
    v=concat(segs, os.path.join(TMP,"cut.mp4")); print(f"  {dur(v):.2f}s")
    json.dump({"starts":{t:s for t,s,_ in sl},"durs":{t:L for t,_,L in sl},"total":total},
              open(os.path.join(TMP,"edl.json"),"w"), indent=1)
