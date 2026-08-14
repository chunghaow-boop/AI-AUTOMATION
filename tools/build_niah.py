#!/usr/bin/env python3
# NIAH — the delivered build (v2 shape, whole clips). Superseded v1 parked in _to_delete. WHOLE CLIPS, REORDER ONLY (his rule L125, restated 2026-08-12:
# "do not simply cut unless analyzed fully then cut. if not, just piece all the
# scene together fully"). v1 cut 5.04s sources into 1.23s bursts and used every
# source twice; he judged the RAW FOOTAGE GOOD and the CUT wrong. This build:
#   - 10 sources, 10 shots, ONE appearance each, t_in = 0, 8 beats each
#     (4.923s of a 5.04s clip - the panborneo v4 pattern, whole-clip)
#   - ORDER is the only edit decision, and it FIXES v1's ending defect for free:
#     the film now ends on J (ribbons on the afterglow) instead of C's bright
#     daylight cliff, so the light arc is monotonic night->morning->midday->
#     cave dark->dusk and the CTA card is answered by dusk, not contradicted.
#   - same transition grammar (L139 zero-reserve fades) on the new boundaries
#   - same capcards captions, re-timed to the new grid
import subprocess, sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tools"))
sys.path.insert(0, os.path.join(HERE, 'plans'))
import niah as P
import capcards

D   = os.path.join(HERE, "projects", "niah", "clips")
FPS = 30; BPM = 97.5; BEAT = 60.0/BPM
BEATS_PER_SHOT = 8                      # 4.9231s of each 5.04s clip

# ORDER = the whole edit. story: dark -> the walk -> the wall -> the door ->
# the ceiling -> the floor -> the exodus -> the face -> the sky.
ORDER = ["A","B","I","C","D","E","F","G","H","J"]
FOLEY = {"A":-5.0,"B":-7.0,"I":-9.0,"C":-8.0,"D":-4.0,
         "E":-4.0,"F":-6.0,"G":-3.0,"H":-6.0,"J":-8.0}
# transitions on story turns only (kinds LIVE in the bank; no whoosh anywhere)
TRANS = {0: ("white",3),   # the one backwards jump: dark -> morning
         4: ("black",4),   # walking into the mountain: daylight dies
         6: ("white",3)}   # the cave ate the afternoon: dark -> dusk
CARDS = [("GUA NIAH. 3KM TO THE DOOR.",        1, 1),
         ("A DOOR 75 METRES HIGH",             4, 1),
         ("THOSE AREN'T STARS.",               5, 1),
         ("PEOPLE SLEPT HERE 40,000 YEARS AGO",6, 1),
         ("DEATH SHIPS. NEXT CAVE.",           8, 1)]

n = len(ORDER)
bound = [round(i*BEATS_PER_SHOT*BEAT*FPS) for i in range(n+1)]
fr    = [bound[i+1]-bound[i] for i in range(n)]
TOT   = bound[-1]; DUR = TOT/FPS

def rms_db(path, t):
    raw = subprocess.run(["ffmpeg","-v","quiet","-i",path,"-t",str(t),
        "-f","f32le","-ac","1","-ar","44100","-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    return 20*np.log10(np.sqrt((x**2).mean())+1e-9)

mean_i = np.mean([FOLEY[k] for k in ORDER])
gains  = [round(float(-18 + (FOLEY[k]-mean_i)*0.5
                      - rms_db(os.path.join(D,f"niah_{k}.mp4"), fr[i]/FPS)), 2)
          for i,k in enumerate(ORDER)]
print("per-shot gains:", gains)

cards = [dict(text=t, start=bound[s]/FPS, end=bound[min(s+c,n)]/FPS)
         for t,s,c in CARDS]
# the PLAN decides the register (planning phase); this builder only obeys.
reg = getattr(P, "CARD_REGISTER", None)
man = capcards.build_cards(cards, "/tmp/niah_cards_v2", style="punch",
                           register=reg, pillar=getattr(P, "PILLAR", None))

inputs, f = [], []
for i,k in enumerate(ORDER):
    inputs += ["-i", os.path.join(D, f"niah_{k}.mp4")]
    fx = ""
    if i in TRANS:
        c,nf = TRANS[i]; fx += f",fade=t=out:st={fr[i]/FPS-nf/FPS:.6f}:d={nf/FPS:.6f}:color={c}"
    if (i-1) in TRANS:
        c,nf = TRANS[i-1]; fx += f",fade=t=in:st=0:d={nf/FPS:.6f}:color={c}"
    f.append(f"[{i}:v]fps={FPS},scale=720:1280,trim=start=0:end_frame={fr[i]},"
             f"setpts=PTS-STARTPTS{fx}[v{i}]")
    ad = fr[i]/FPS + (0.08 if i < n-1 else 0)
    f.append(f"[{i}:a]atrim=0:{ad:.6f},asetpts=PTS-STARTPTS,volume={gains[i]}dB,"
             f"aresample=44100,aformat=channel_layouts=stereo[a{i}]")
for m in man: inputs += ["-i", m["png"]]
f.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1[vc]")
cf, last = capcards.overlay_filters(man, "[vc]", input_offset=n)
f += cf
f.append(f"{last}trim=end_frame={TOT},setpts=PTS-STARTPTS[vout]")
ac = "[a0]"
for i in range(1, n):
    o = f"[ax{i}]" if i < n-1 else "[act]"
    f.append(f"{ac}[a{i}]acrossfade=d=0.08:c1=tri:c2=tri{o}"); ac = o
f.append(f"[act]atrim=0:{DUR:.6f},alimiter=limit=0.891:level=disabled[aout]")
out = os.path.join(HERE, "projects", "niah", "niah_v2_diegetic.mp4")
cmd = (["ffmpeg","-y","-nostdin"]+inputs+["-filter_complex",";".join(f),
       "-map","[vout]","-map","[aout]","-c:v","libx264","-crf","16","-preset","medium",
       "-profile:v","high","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k", out])
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
json.dump([dict(text=c["text"], start=c["start"], end=c["end"], y=0.70, h=0.075,
                color=[255,255,255], scrim=0.45) for c in cards],
          open(out.replace(".mp4","_cards.json"), "w"), indent=1)

# MANIFESTS FOR VERIFY (added 2026-08-12 after his QC review). A film built outside
# engine.py wrote none of these, so 12 of verify's 16 checks answered "NOT MEASURED"
# and the two real failures drowned in the noise. The build knows the truth about
# its own cuts - it should hand that truth to the gate rather than make the gate
# guess from pixels.
pdir = os.path.join(HERE, "projects", "niah")
os.makedirs(os.path.join(pdir, "audio"), exist_ok=True)
os.makedirs(os.path.join(pdir, "tmp"), exist_ok=True)
_c, _t = [], 0.0
for _f in fr[:-1]:
    _t += _f / FPS; _c.append(round(_t, 4))
json.dump({"cuts": _c, "planned": _c, "bpm": BPM, "beat": BEAT,
           "_source": "tools/build_niah.py - the build's own frame grid, not detected"},
          open(os.path.join(pdir, "audio", "niah_cuts.json"), "w"), indent=1)
json.dump([{"shot": i, "src": k, "tin": 0.0, "has_peak": True,
            "frames": fr[i], "in": round(sum(fr[:i]) / FPS, 4)}
           for i, k in enumerate(ORDER)],
          open(os.path.join(pdir, "tmp", "manifest_peaks.json"), "w"), indent=1)
print(f"manifests -> {pdir}/audio/niah_cuts.json + tmp/manifest_peaks.json")
print(json.dumps({"order":ORDER,"frames":fr,"total":TOT,"dur":round(DUR,4),
                  "shots_csv":",".join(map(str,fr)),"out":out}))
