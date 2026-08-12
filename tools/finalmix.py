#!/usr/bin/env python3
"""
FINALMIX — bed + duck + whoosh + foley-forward master onto a finished cut.
Born 2026-08-12 from panborneo v1's three audio defects (L119/L121): foley
attenuated for an absent bed, no BGM, no transition sfx. This script is the
fix as a REUSABLE, MEASURED step: it never touches the video stream (-c:v copy)
and every level decision is derived from measurement of THIS file, not taste.

Usage:
  python3 tools/finalmix.py --video V2.mp4 --bed bed.mp3 --bed-ss 36.64 \
      --whoosh assets/bank/sfx/whoosh_whip.wav --whoosh-at 8.18 \
      --shots 74,55,56,73,74,56,74,73,74,74,55,74,56 --out FINAL.mp4

Level policy (travel_vlog, MIX file 19: I=-8, TP=-1):
  foley makeup -> median shot RMS hits --foley-target (default -18 dB), cap +12
  bed gain     -> bed RMS = foley target - --bed-under (default 3 dB below foley;
                  NEGATIVE puts the bed ABOVE foley — the L128 direction)
  duck         -> sidechaincompress --duck-ratio/--duck-release (default 4, 250ms)
  master       -> 2-pass loudnorm to I/TP, then alimiter safety

L128 (2026-08-12, his ear, measured): v4 shipped bed 3dB UNDER foley + 4:1 duck ->
melody band flat at -40dB for 64s. travel_vlog is BGM-LED: bed is the anchor.
The constants became flags so the policy is a CHOICE, never a silent default:
  --foley-target -22 --bed-under -4 --duck-ratio 2 --duck-release 300
"""
import argparse, json, subprocess, sys, tempfile, os
import numpy as np

FOLEY_TARGET = -18.0   # dB RMS, median shot, pre-master
BED_UNDER    = 3.0     # bed RMS sits this far under foley target
LOUD_I, LOUD_TP = -8.0, -1.0
FPS = 30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"FAIL: {' '.join(cmd)}\n{r.stderr[-800:]}")
    return r

def pcm(path, ss=None, t=None, sr=44100):
    cmd = ["ffmpeg","-v","quiet"]
    if ss: cmd += ["-ss",str(ss)]
    cmd += ["-i",path]
    if t: cmd += ["-t",str(t)]
    cmd += ["-f","f32le","-ac","1","-ar",str(sr),"-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32), sr

def rms_db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--bed", required=True)
    ap.add_argument("--bed-ss", type=float, default=0.0)
    ap.add_argument("--whoosh")
    ap.add_argument("--whoosh-at", type=float)
    ap.add_argument("--whoosh-gain", type=float, default=4.0)
    ap.add_argument("--shots", help="comma frame counts per shot @30fps (for per-shot RMS)")
    ap.add_argument("--out", default="FINAL.mp4")
    ap.add_argument("--foley-target", type=float, default=FOLEY_TARGET,
                    help="dB RMS the median shot is pushed to (default -18)")
    ap.add_argument("--bed-under", type=float, default=BED_UNDER,
                    help="bed sits this many dB under foley target; NEGATIVE = bed above (L128)")
    ap.add_argument("--duck-ratio", type=float, default=4.0,
                    help="sidechain ratio (L128 travel_vlog: 2)")
    ap.add_argument("--duck-release", type=int, default=250,
                    help="sidechain release ms (L128 travel_vlog: 300)")
    a = ap.parse_args()

    dur = float(json.loads(run(["ffprobe","-v","quiet","-print_format","json",
        "-show_format",a.video]).stdout)["format"]["duration"])

    # 1 MEASURE the cut's own audio, per shot if boundaries given
    x,_ = pcm(a.video)
    shot_rms = []
    if a.shots:
        b = 0.0
        for f in a.shots.split(","):
            s,e = int(b*44100), int((b+int(f)/FPS)*44100)
            shot_rms.append(rms_db(x[s:e])); b += int(f)/FPS
        med = float(np.median(shot_rms))
    else:
        med = rms_db(x)
    makeup = min(a.foley_target - med, 12.0)

    # 2 MEASURE the bed window, derive bed gain
    bx,_ = pcm(a.bed, ss=a.bed_ss, t=dur)
    bed_gain = (a.foley_target - a.bed_under) - rms_db(bx)

    # 3 build mix (pass 1: loudnorm measure)
    inputs = ["-i",a.video,"-ss",str(a.bed_ss),"-i",a.bed]
    wl = ""
    if a.whoosh and a.whoosh_at is not None:
        inputs += ["-i",a.whoosh]
        wl = (f";[2:a]adelay={int(a.whoosh_at*1000)}|{int(a.whoosh_at*1000)},"
              f"volume={a.whoosh_gain:.1f}dB,aresample=44100,aformat=channel_layouts=stereo[wh];"
              f"[duckmix][wh]amix=inputs=2:normalize=0[premix]")
    # aformat pins: strict ffmpeg builds refuse sidechaincompress without
    # explicit channel layouts (found in the cloud container 2026-08-12; no-op elsewhere)
    graph = (
        f"[0:a]volume={makeup:.2f}dB,aresample=44100,aformat=channel_layouts=stereo[fol];"
        f"[1:a]atrim=0:{dur:.3f},volume={bed_gain:.2f}dB,"
        f"afade=t=out:st={dur-0.8:.3f}:d=0.8,aresample=44100,aformat=channel_layouts=stereo[bed];"
        f"[fol]asplit[folA][folB];"
        f"[bed][folB]sidechaincompress=threshold=0.05:ratio={a.duck_ratio:g}:attack=50:release={a.duck_release}[bedduck];"
        f"[folA][bedduck]amix=inputs=2:normalize=0[duckmix]"
        + (wl if wl else ";[duckmix]anull[premix]")
    )
    with tempfile.TemporaryDirectory() as td:
        p1 = subprocess.run(["ffmpeg","-v","info","-nostdin"]+inputs+
            ["-filter_complex",graph+f";[premix]loudnorm=I={LOUD_I}:TP={LOUD_TP}:print_format=json[out]",
             "-map","[out]","-f","null","-"], capture_output=True, text=True)
        j = json.loads(p1.stderr[p1.stderr.rindex("{"):p1.stderr.rindex("}")+1])
        ln = (f";[premix]loudnorm=I={LOUD_I}:TP={LOUD_TP}:"
              f"measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
              f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:"
              f"offset={j['target_offset']}:linear=true,"
              f"alimiter=limit=0.891:level=disabled,aresample=44100[out]")
        run(["ffmpeg","-y","-nostdin"]+inputs+
            ["-filter_complex",graph+ln,"-map","0:v","-map","[out]",
             "-c:v","copy","-c:a","aac","-b:a","256k",a.out])

    # 4 EVIDENCE
    fx,_ = pcm(a.out)
    ev = {"policy":{"foley_target":a.foley_target,"bed_under":a.bed_under,
          "duck_ratio":a.duck_ratio,"duck_release_ms":a.duck_release},
          "makeup_db":round(float(makeup),2),"bed_gain_db":round(float(bed_gain),2),
          "shot_rms_before":[round(float(v),1) for v in shot_rms],
          "median_shot_rms_before":round(float(med),1),
          "final_rms_db":round(float(rms_db(fx)),1),
          "loudnorm_measured_input_I":j["input_i"]}
    print(json.dumps(ev,indent=1))

if __name__ == "__main__":
    main()
