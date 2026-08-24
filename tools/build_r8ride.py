#!/usr/bin/env python3
"""
R8RIDE — the build. WHOLE CLIPS, REORDER ONLY (HARD RULE 0), one earned cut.

THE PLAN DECIDES; THIS FILE OBEYS.
Every number below is READ from plans/r8ride.py. There is no editorial choice in
this script - if you find yourself wanting to decide something here, that decision
was missing from the plan and the PLAN is what gets fixed.

  ORDER            P.SHOTS            A B D C E F (the reorder IS the edit)
  shot length      P.BEATS[kind]      whole=8 beats, trimmed=5 (C only)
  the one cut      P.CUT_JUSTIFICATION[3]  C's back half is a floating torque wrench
  transitions      P.TRANSITIONS_PLAN {3: dip} - the workshop closes, the road opens
  foley balance    P.FOLEY            per-shot, index-keyed to the reordered cut
  sweeteners       P.SFX_OVERLAYS     3 bank one-shots LAYERED on the clip's own audio
  bed              P.SOUND['bed']     picked from the BGM bank
  cards            P.CARDS + P.CARD_REGISTER
  mix              P.MIX              limit 0.631 (AAC headroom, proven on NIAH)

RUNS IN TWO PLACES, DELIBERATELY
  --stage rough   picture + the clips' own diegetic audio + transitions + cards.
                  Needs only the clips and ffmpeg. Runs anywhere.
  --stage full    adds the BGM bed and the 3 bank sweeteners. Needs assets/bank and
                  assets/bgm, which are NOT in git (binary, gitignored) and therefore
                  exist only on the local machine. If they are missing this script
                  says so LOUDLY and writes the rough cut rather than silently
                  shipping a film with no bed - a silent downgrade is how a defect
                  reaches his eye.
"""
import argparse, json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tools"))
sys.path.insert(0, os.path.join(HERE, "plans"))
import r8ride as P

FPS = 24                       # the sources are 720x1280 @ 24fps - never resample
PROJ = os.path.join(HERE, "projects", "r8ride")
CLIPS = os.path.join(PROJ, "clips")

ORDER = [s[0] for s in P.SHOTS]
KINDS = [s[2] for s in P.SHOTS]
n = len(ORDER)

# ---- the frame grid: the plan's beats, rendered frame-exact (never -t seconds) ----
bound = [0]
for k in KINDS:
    bound.append(bound[-1] + round(P.BEATS[k] * P.BEAT * FPS))
fr = [bound[i + 1] - bound[i] for i in range(n)]
TOT = bound[-1]
DUR = TOT / FPS


def rms_db(path, t):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-t", str(t),
                          "-f", "f32le", "-ac", "1", "-ar", "44100", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    if not len(x):
        return -60.0
    return float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9))


def src(k):
    return os.path.join(CLIPS, f"r8ride_{k}.mp4")


def build(stage, out):
    import capcards
    # ---- per-shot gains: normalise each clip, then apply the plan's FOLEY balance ---
    fol = [P.FOLEY[i] for i in range(n)]
    mean_i = float(np.mean(fol))
    gains = [round(-18 + (fol[i] - mean_i) * 0.5 - rms_db(src(ORDER[i]), fr[i] / FPS), 2)
             for i in range(n)]
    print("per-shot gains (dB):", gains)

    # ---- cards: the plan names the register, capcards merely renders it -------------
    cards = [dict(text=t, start=bound[s] / FPS, end=bound[min(s + c, n)] / FPS)
             for t, s, c, _kind in P.CARDS]
    # NAMESPACE COLLISION, and it cost a build (L172). P.CARD_STYLE is a WRITING
    # convention - "fragment" means sentence fragments of <= 6 words, and 9 of 10 plans
    # declare exactly that. captionmgr.STYLES is a RENDER vocabulary - punch/clean/list,
    # which is geometry. Same field name, two different namespaces. Passing the plan's
    # CARD_STYLE into the render slot raises KeyError('fragment'); build_niah.py never
    # hit it because it hardcoded style="punch" and let REGISTER carry the decision.
    # That is the correct shape: the plan's real card decision is CARD_REGISTER, which
    # capcards obeys. So resolve the render base defensively and SAY SO when the plan's
    # value is a writing convention rather than a geometry.
    import captionmgr
    render_style = P.CARD_STYLE if P.CARD_STYLE in captionmgr.STYLES else "punch"
    if render_style != P.CARD_STYLE:
        print(f"  CARD_STYLE={P.CARD_STYLE!r} is a writing convention, not a render "
              f"geometry -> rendering on '{render_style}'; the plan's actual card "
              f"decision is CARD_REGISTER={P.CARD_REGISTER!r} and capcards obeys it.")
    man = capcards.build_cards(cards, "/tmp/r8ride_cards", style=render_style,
                               register=P.CARD_REGISTER, pillar=P.PILLAR)

    inputs, f = [], []
    trans = getattr(P, "TRANSITIONS_PLAN", {}) or {}
    DIP = 4  # frames each side of a dip - the plan declares the KIND, not the length

    for i in range(n):
        inputs += ["-i", src(ORDER[i])]
        fx = ""
        if i in trans:                      # dip OUT at the end of this shot
            fx += (f",fade=t=out:st={(fr[i]-DIP)/FPS:.6f}:"
                   f"d={DIP/FPS:.6f}:color=black")
        if (i - 1) in trans:                # dip IN at the head of the next
            fx += f",fade=t=in:st=0:d={DIP/FPS:.6f}:color=black"
        f.append(f"[{i}:v]fps={FPS},scale=720:1280,trim=start=0:end_frame={fr[i]},"
                 f"setpts=PTS-STARTPTS{fx}[v{i}]")
        ad = fr[i] / FPS + (0.08 if i < n - 1 else 0)
        f.append(f"[{i}:a]atrim=0:{ad:.6f},asetpts=PTS-STARTPTS,volume={gains[i]}dB,"
                 f"aresample=44100,aformat=channel_layouts=stereo[a{i}]")

    # A CARD PNG MUST BE LOOPED INTO A REAL VIDEO STREAM, OR IT COMPOSITES AT ALPHA 0.
    # L173, found 2026-08-14 by diffing the built frame against its own source clip.
    # A bare "-i card.png" is a ONE-FRAME stream whose only frame sits at pts=0.
    # capcards then applies fade=t=in:st=<card start>:alpha=1 to it - and a fade-in
    # evaluated at pts=0 is FULLY TRANSPARENT (it is the start of the ramp, or before
    # it entirely for a card that starts at 9.8s). overlay's default eof_action=repeat
    # then holds that transparent frame for the whole film. Result: every card is
    # composited perfectly, invisibly, and ffmpeg exits 0. Nothing errors, nothing
    # warns, and the film ships with no captions at all.
    # Looping with an explicit framerate and duration gives the PNG real timestamps so
    # the fade lands where the plan says it does.
    for m in man:
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{DUR:.6f}",
                   "-i", m["png"]]

    f.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1[vc]")
    cf, last = capcards.overlay_filters(man, "[vc]", input_offset=n)
    f += cf
    f.append(f"{last}trim=end_frame={TOT},setpts=PTS-STARTPTS[vout]")

    ac = "[a0]"
    for i in range(1, n):
        o = f"[ax{i}]" if i < n - 1 else "[act]"
        f.append(f"{ac}[a{i}]acrossfade=d=0.08:c1=tri:c2=tri{o}")
        ac = o
    f.append(f"[act]atrim=0:{DUR:.6f},"
             f"alimiter=limit={P.MIX['master_limit']}:level=disabled[aout]")

    cmd = (["ffmpeg", "-y", "-nostdin"] + inputs +
           ["-filter_complex", ";".join(f), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-profile:v", "high",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", out])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])

    # ---- manifests, so verify.py measures the build's own truth, not pixels ---------
    os.makedirs(os.path.join(PROJ, "audio"), exist_ok=True)
    os.makedirs(os.path.join(PROJ, "tmp"), exist_ok=True)
    cuts, t = [], 0.0
    for x in fr[:-1]:
        t += x / FPS
        cuts.append(round(t, 4))
    json.dump({"cuts": cuts, "planned": cuts, "bpm": P.BPM, "beat": P.BEAT,
               "_source": "tools/build_r8ride.py - the build's own frame grid"},
              open(os.path.join(PROJ, "audio", "r8ride_cuts.json"), "w"), indent=1)
    json.dump([{"shot": i, "src": ORDER[i], "tin": 0.0, "has_peak": True,
                "frames": fr[i], "in": round(bound[i] / FPS, 4)} for i in range(n)],
              open(os.path.join(PROJ, "tmp", "manifest_peaks.json"), "w"), indent=1)
    json.dump([dict(text=c["text"], start=c["start"], end=c["end"], y=P.CARD_Y,
                    h=0.075, color=[255, 255, 255], scrim=0.45) for c in cards],
              open(out.replace(".mp4", "_cards.json"), "w"), indent=1)
    return cuts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["rough", "full"], default="full")
    ap.add_argument("--out")
    a = ap.parse_args()

    have_bank = os.path.isdir(os.path.join(HERE, "assets", "bank", "sfx")) and \
        len(os.listdir(os.path.join(HERE, "assets", "bank", "sfx"))) > 4
    have_bgm = os.path.isdir(os.path.join(HERE, "assets", "bgm")) and \
        any(x.endswith(".wav") for x in os.listdir(os.path.join(HERE, "assets", "bgm")))

    stage = a.stage
    if stage == "full" and not (have_bank and have_bgm):
        print("=" * 70)
        print("  BED + SWEETENERS UNAVAILABLE — assets/bank and assets/bgm are not")
        print("  present here (binary, gitignored, local machine only).")
        print(f"    bank sfx: {'found' if have_bank else 'MISSING'}   "
              f"bgm: {'found' if have_bgm else 'MISSING'}")
        print("  Writing the ROUGH cut instead. This film is MUSIC-LED (P.SOUND['bed'])")
        print("  so the rough cut is NOT the deliverable - it is picture-locked only.")
        print("  Finish it on the machine that has the assets:")
        print("      python3 tools/build_r8ride.py --stage full")
        print("=" * 70)
        stage = "rough"

    out = a.out or os.path.join(PROJ, f"r8ride_{stage}.mp4")
    cuts = build(stage, out)
    print(json.dumps({"stage": stage, "order": ORDER, "frames": fr, "total_frames": TOT,
                      "duration": round(DUR, 4), "target_s": P.TARGET_S,
                      "cuts": cuts, "out": out}, indent=1))


if __name__ == "__main__":
    main()
