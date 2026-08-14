#!/usr/bin/env python3
# panborneo v6 — session 11 (2026-08-12). His two catches on V5, fixed at the build:
#   1. "captions way too basic / white clashes with environment"
#      → drawtext REPLACED by capcards.py PNG overlays (pill scrim + #FFD54A keyword
#        + 120ms fade-in). capcheck.py gates contrast ≥4.5:1 (V5 failed at 4.29).
#   2. "transition between scene to scene is still not there yet"
#      → 4 MOTIVATED transitions at the story turns, all ZERO-DRIFT (fades spend a
#        shot's own frames; only the whip keeps its pre-reserved 6-frame xfade):
#        b1  G→B   flash-white 3f out/3f in   "REWIND TO DAWN" — a rewind reads as a flash
#        b4  A→D   slideleft whip (unchanged from v4, whoosh at 19.37 via finalmix)
#        b7  E→I   dip-to-black 4f/4f         Sabah→Sarawak state line — hard geography turn
#        b11 K→L   dip-to-black 4f/4f         arrival leg, "KUCHING BY DUSK?"
#      TRANSITIONS.json doctrine: hard cuts remain the default; each of these earns
#      its place on a story beat. No timeline drift possible — grid is v4's, frame-exact.
# Grid, gains, audio chain: byte-identical to build_panborneo_v4.py.
# After this: finalmix.py with the L128 flags → bedcheck → capcheck → verify.
import subprocess, sys, json, os, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--clips", default="/mnt/user-data/uploads/Downloads/")
ap.add_argument("--out",   default="panborneo_v6_diegetic.mp4")
ap.add_argument("--carddir", default="/tmp/capcards_v6")
A = ap.parse_args()
D = A.clips if A.clips.endswith(("/","\\")) else A.clips + os.sep

CLIP={ 'G':"hf_20260812_013352_6ea04155-c2eb-4bd0-a5fd-be012eefeab6.mp4",
 'B':"hf_20260812_013945_a0ea9c0e-03c5-4ba2-9c22-07431803ac88.mp4",
 'C':"hf_20260812_013944_2ff0e9b5-29cc-4966-90e5-e26610710094.mp4",
 'A':"hf_20260812_013944_bae2cbc1-8efb-4c36-9d52-86f842c6a8a6.mp4",
 'D':"hf_20260812_013944_fc725a80-05cb-447c-b3c4-81235209be76.mp4",
 'F':"hf_20260812_013945_565611be-cec7-4968-8c69-9c8c33a6db47.mp4",
 'E':"hf_20260812_013944_52cf20ff-d1c5-4242-8adf-a02e41cdc00a.mp4",
 'I':"hf_20260812_014031_b0463077-a1b0-4f0b-9275-d42de489fa4c.mp4",
 'H':"hf_20260812_014031_bc8b6f76-a54e-4a17-8d4e-6d12a725bb8c.mp4",
 'J':"hf_20260812_014031_a0a80cfc-0870-44d2-87dd-83884d2a5e6c.mp4",
 'K':"hf_20260812_014031_3427b1bb-c182-4362-a988-38e9e38c41b4.mp4",
 'L':"hf_20260812_014031_39f52888-1814-4784-9fe5-6f5f2bb66b0c.mp4",
 'M':"hf_20260812_014031_6008c272-94b4-46af-97f1-e1c6befa2587.mp4"}
S=[('G',0.0,8,-3),('B',0.0,8,-7),('C',0.0,8,-9),('A',0.0,8,-3),
   ('D',0.0,8,-8),('F',0.0,8,-7),('E',0.0,8,-5),('I',0.0,8,-9),
   ('H',0.0,8,-6),('J',0.0,8,-9),('K',0.0,8,-6),('L',0.0,8,-9),('M',0.0,8,-6)]
FPS=24; BEAT=60/97.5; XFV=6; ACF=0.08; TGT=-18.0

CARDS=[dict(text="SABAH ENDS HERE",           start=0.15, end=3.0),
       dict(text="REWIND TO DAWN",            start=4.92, end=8.5),
       dict(text="KLIAS: PROBOSCIS COUNTRY",  start=20.0, end=23.6),
       dict(text="SARAWAK. STILL TOLL-FREE.", start=34.6, end=38.2),
       dict(text="KUCHING BY DUSK?",          start=54.3, end=57.9)]

# TRANSITIONS: shot_index -> (kind, frames_per_side). Applied INSIDE the shot's own
# frames — timing='consume-internal', zero reserve, zero drift (TRANSITIONS.json lesson).
TRANS = {0:("flash",3), 6:("dip",4), 10:("dip",4)}   # fade OUT of these shots, IN to next

cum=[0]
for _,_,b,_ in S: cum.append(cum[-1]+b)
bound=[round(c*BEAT*FPS) for c in cum]
frames=[bound[i+1]-bound[i] for i in range(13)]
TOTAL=bound[-1]; DUR=TOTAL/FPS
sec=[f/FPS for f in frames]

def rms_db(path, ss, t):
    raw=subprocess.run(["ffmpeg","-v","quiet","-ss",str(ss),"-i",path,"-t",str(t),
        "-f","f32le","-ac","1","-ar","44100","-"],capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32)
    return 20*np.log10(np.sqrt((x**2).mean())+1e-9)

mean_plan=np.mean([d for _,_,_,d in S])
gains=[]
for i,(k,tin,b,db) in enumerate(S):
    r=rms_db(D+CLIP[k],tin,sec[i])
    tgt=TGT+(db-mean_plan)*0.5
    gains.append(round(float(tgt-r),2))
print("per-shot gains:",gains)

# render caption cards (real-metric fit, pill, keyword highlight)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capcards
man = capcards.build_cards(CARDS, A.carddir, style="punch")

def shot_fades(i):
    """fade filters this shot needs, spending its own frames. Colour from TRANS."""
    fx=[]
    if i in TRANS:                                   # fade OUT at tail
        kind,n = TRANS[i]; col = "white" if kind=="flash" else "black"
        st = sec[i] - n/FPS
        fx.append(f"fade=t=out:st={st:.6f}:d={n/FPS:.6f}:color={col}")
    if (i-1) in TRANS:                               # fade IN at head
        kind,n = TRANS[i-1]; col = "white" if kind=="flash" else "black"
        fx.append(f"fade=t=in:st=0:d={n/FPS:.6f}:color={col}")
    return ("," + ",".join(fx)) if fx else ""

inputs=[]; f=[]
for i,(k,tin,b,db) in enumerate(S):
    inputs+=["-i",D+CLIP[k]]
    if i==3:
        f.append(f"[{i}:v]fps={FPS},scale=720:1280,trim=start=0:end_frame={frames[i]+2},"
                 f"setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop={XFV-2}{shot_fades(i)}[v{i}]")
    else:
        f.append(f"[{i}:v]fps={FPS},scale=720:1280,trim=start={tin}:end_frame={int(round(tin*FPS))+frames[i]},"
                 f"setpts=PTS-STARTPTS{shot_fades(i)}[v{i}]")
    ad=sec[i]+(ACF if i<12 else 0)
    f.append(f"[{i}:a]atrim=start={tin}:duration={ad:.6f},asetpts=PTS-STARTPTS,"
             f"volume={gains[i]}dB,aresample=44100,aformat=channel_layouts=stereo[a{i}]")
for j,m in enumerate(man):
    inputs+=["-i",m["png"]]
f.append("[v0][v1][v2][v3]concat=n=4:v=1[p1]")
f.append("[v4][v5][v6][v7][v8][v9][v10][v11][v12]concat=n=9:v=1[p2]")
f.append(f"[p1][p2]xfade=transition=slideleft:duration={XFV/FPS:.6f}:offset={bound[4]/FPS:.6f}[vx]")
cf, last = capcards.overlay_filters(man, "[vx]", input_offset=13)
f += cf
f.append(f"{last}trim=end_frame={TOTAL},setpts=PTS-STARTPTS[vout]")
ac="[a0]"
for i in range(1,13):
    o=f"[ax{i}]" if i<12 else "[acat]"
    f.append(f"{ac}[a{i}]acrossfade=d={ACF}:c1=tri:c2=tri{o}")
    ac=o
f.append(f"[acat]atrim=0:{DUR:.6f},alimiter=limit=0.891:level=disabled[aout]")
cmd=(["ffmpeg","-y","-nostdin"]+inputs+["-filter_complex",";".join(f),
     "-map","[vout]","-map","[aout]","-c:v","libx264","-crf","16","-preset","medium",
     "-profile:v","high","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k",A.out])
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
caps=[dict(text=c["text"],start=c["start"],end=c["end"],y=0.70,h=0.075,
           color=[255,255,255],scrim=0.45) for c in CARDS]
json.dump(caps, open(os.path.splitext(A.out)[0]+"_cards.json","w"), indent=1)
print(json.dumps({"frames":frames,"total":TOTAL,"dur":round(DUR,4),
                  "whip_at":round(bound[4]/FPS,4),
                  "transitions":{str(k):v for k,v in TRANS.items()},
                  "cards":len(man),"out":A.out}))
