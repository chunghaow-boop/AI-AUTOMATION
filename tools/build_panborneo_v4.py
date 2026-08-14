#!/usr/bin/env python3
# panborneo v3 — the fix build. Native 24fps (no dupe-frame judder), per-shot
# audio leveling to -18 RMS (keeps half the plan's intent deltas), 80ms audio
# crossfades at every boundary, ONE card size, KLIAS card after the whip.
import subprocess, sys, json
import numpy as np

D="/mnt/user-data/uploads/Downloads/"
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
# v4: WHOLE CLIPS (his rule 2026-08-12). t_in=0, 8 beats each, order unchanged.
S=[('G',0.0,8,-3),('B',0.0,8,-7),('C',0.0,8,-9),('A',0.0,8,-3),
   ('D',0.0,8,-8),('F',0.0,8,-7),('E',0.0,8,-5),('I',0.0,8,-9),
   ('H',0.0,8,-6),('J',0.0,8,-9),('K',0.0,8,-6),('L',0.0,8,-9),('M',0.0,8,-6)]
FPS=24; BEAT=60/97.5; XFV=6           # 6-frame (0.25s) whip reserve
ACF=0.08                              # 80ms audio crossfade
TGT=-18.0                             # per-shot RMS target
FONT="/usr/share/fonts/opentype/montserrat/Montserrat-ExtraBold.otf"
FS=44                                 # ONE card size
CARDS=[("SABAH ENDS HERE",0.15,3.0),("REWIND TO DAWN",4.92,8.5),
       ("KLIAS\\: PROBOSCIS COUNTRY",20.0,23.6),
       ("SARAWAK. STILL TOLL-FREE.",34.6,38.2),
       ("KUCHING BY DUSK?",54.3,57.9)]

# frame-exact 24fps grid from cumulative beats
cum=[0];
for _,_,b,_ in S: cum.append(cum[-1]+b)
bound=[round(c*BEAT*FPS) for c in cum]          # frame boundaries
frames=[bound[i+1]-bound[i] for i in range(13)] # per-shot frames
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
    tgt=TGT+(db-mean_plan)*0.5           # keep half the plan's relative intent
    gains.append(round(float(tgt-r),2))
print("per-shot gains:",gains)

inputs=[]; f=[]
for i,(k,tin,b,db) in enumerate(S):
    inputs+=["-i",D+CLIP[k]]
    if i==3:   # A: use its 2 real spare frames + clone-pad to fill the 6f whip reserve
        f.append(f"[{i}:v]fps={FPS},scale=720:1280,trim=start=0:end_frame={frames[i]+2},"
                 f"setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop={XFV-2}[v{i}]")
    else:
        f.append(f"[{i}:v]fps={FPS},scale=720:1280,trim=start={tin}:end_frame={int(round(tin*FPS))+frames[i]},"
                 f"setpts=PTS-STARTPTS[v{i}]")
    ad=sec[i]+(ACF if i<12 else 0)       # each shot carries the crossfade tail
    f.append(f"[{i}:a]atrim=start={tin}:duration={ad:.6f},asetpts=PTS-STARTPTS,"
             f"volume={gains[i]}dB,aresample=44100,aformat=channel_layouts=stereo[a{i}]")
f.append("[v0][v1][v2][v3]concat=n=4:v=1[p1]")
f.append("[v4][v5][v6][v7][v8][v9][v10][v11][v12]concat=n=9:v=1[p2]")
f.append(f"[p1][p2]xfade=transition=slideleft:duration={XFV/FPS:.6f}:offset={bound[4]/FPS:.6f}[vx]")
dt="[vx]"
for j,(txt,st,en) in enumerate(CARDS):
    out=f"[vc{j}]" if j<len(CARDS)-1 else "[vtxt]"
    f.append(f"{dt}drawtext=fontfile={FONT}:text='{txt}':fontsize={FS}:fontcolor=white:"
             f"borderw=3:bordercolor=black@0.6:x=(w-text_w)/2:y=908:"
             f"enable='between(t,{st},{en})'{out}")
    dt=out
f.append(f"[vtxt]trim=end_frame={TOTAL},setpts=PTS-STARTPTS[vout]")
ac="[a0]"
for i in range(1,13):
    o=f"[ax{i}]" if i<12 else "[acat]"
    f.append(f"{ac}[a{i}]acrossfade=d={ACF}:c1=tri:c2=tri{o}")
    ac=o
f.append(f"[acat]atrim=0:{DUR:.6f},alimiter=limit=0.891:level=disabled[aout]")
cmd=(["ffmpeg","-y","-nostdin"]+inputs+["-filter_complex",";".join(f),
     "-map","[vout]","-map","[aout]","-c:v","libx264","-crf","16","-preset","medium",
     "-profile:v","high","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k",
     "/home/claude/panborneo_V4.mp4"])
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
print(json.dumps({"frames":frames,"total":TOTAL,"dur":round(DUR,4),
                  "whip_at":round(bound[4]/FPS,4)}))
