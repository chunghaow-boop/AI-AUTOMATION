#!/usr/bin/env python3
# panborneo v2 rebuilt IN THE CONTAINER from the staged Downloads clips.
# Same spec as the sandbox v2: 13 whole scenes, 97.5 grid, xfade slideleft
# with 7-frame reserved overlap after shot 4 (A->D), crops 1.00, one encode.
import subprocess, sys

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
S=[('G',0.30,74,-3),('B',0.20,55,-7),('C',0.60,56,-9),('A',0.00,73,-3),
   ('D',0.60,74,-8),('F',0.60,56,-7),('E',2.30,74,-5),('I',0.30,73,-9),
   ('H',1.20,74,-6),('J',2.50,74,-9),('K',3.00,55,-6),('L',2.20,74,-9),('M',1.50,56,-6)]
XF=7; FPS=30
FONT="/usr/share/fonts/opentype/montserrat/Montserrat-ExtraBold.otf"
CARDS=[("SABAH ENDS HERE",0.15,2.4615,54),("REWIND TO DAWN",2.4615,6.1538,54),
       ("KLIAS\\: PROBOSCIS COUNTRY",8.6154,12.9231,38),
       ("SARAWAK. STILL TOLL-FREE.",15.3846,20.3077,38),
       ("KUCHING BY DUSK?",22.7692,24.6154,54)]

inputs=[]; f=[]
for i,(k,tin,fr,db) in enumerate(S):
    inputs += ["-i", D+CLIP[k]]
    vfr = fr + (XF if i==3 else 0)          # A carries the 7-frame reserve
    f.append(f"[{i}:v]fps={FPS},scale=720:1280,trim=start={tin}:end_frame={int(tin*FPS)+vfr},"
             f"setpts=PTS-STARTPTS[v{i}]")
    f.append(f"[{i}:a]atrim=start={tin}:duration={fr/FPS:.6f},asetpts=PTS-STARTPTS,"
             f"volume={db}dB,aresample=44100,aformat=channel_layouts=stereo[a{i}]")
f.append("[v0][v1][v2][v3]concat=n=4:v=1[p1]")
f.append("[v4][v5][v6][v7][v8][v9][v10][v11][v12]concat=n=9:v=1[p2]")
f.append(f"[p1][p2]xfade=transition=slideleft:duration={XF/FPS:.6f}:offset={258/FPS:.6f}[vx]")
dt="[vx]"
for j,(txt,st,en,fs) in enumerate(CARDS):
    out=f"[vc{j}]" if j<len(CARDS)-1 else "[vtxt]"
    f.append(f"{dt}drawtext=fontfile={FONT}:text='{txt}':fontsize={fs}:fontcolor=white:"
             f"borderw=3:bordercolor=black@0.6:x=(w-text_w)/2:y=908:"
             f"enable='between(t,{st},{en})'{out}")
    dt=out
f.append(f"[vtxt]trim=end_frame=868,setpts=PTS-STARTPTS[vout]")
f.append("".join(f"[a{i}]" for i in range(13))+"concat=n=13:v=0:a=1[acat]")
f.append("[acat]alimiter=limit=0.891:level=disabled[aout]")
graph=";".join(f)
cmd=(["ffmpeg","-y","-nostdin"]+inputs+["-filter_complex",graph,
     "-map","[vout]","-map","[aout]","-c:v","libx264","-crf","16","-preset","medium",
     "-profile:v","high","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k",
     "/home/claude/panborneo_V2_local.mp4"])
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
print("BUILT")
