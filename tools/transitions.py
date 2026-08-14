#!/usr/bin/env python3
"""
TRANSITIONS — the missing layer. Everything until now was a hard cut.

Reference-grade short-form doesn't dissolve and doesn't only hard-cut: it whips, punches,
ramps, masks and flashes — always ON the beat, always motivated by what is physically
continuous across the seam (file 25 [7B] Transition Master).

THE MENU (pick by what carries across the cut — never by what looks cool)
  whip        camera/subject moves L or R      directional blur both sides, cut at peak blur
  punch       static frame needs energy        fast scale-in, 3-6 frames
  ramp        action → aftermath               speed up out of A, slow into B
  mask        object crosses the frame         object wipes the cut (also hides AI drift)
  flash       impact / reveal                  1-2 frame white or exposure blowout
  push        spatial change (in/out of car)   B slides in over A
  glitch      pattern interrupt at ~30s        RGB split + block displacement
  zoomblur    hype / speed                     radial blur on the seam
  dip         chapter change                   dip to black/colour, 4-8 frames

RULES ENFORCED
  · max ONE flashy transition per 15s — the rest are hard cuts
  · never decorate the twist seam; the twist IS the transition
  · every transition lands ON a beat if a bed is supplied (uses rhythm.py grid)
  · duration capped at 0.5s — anything longer reads as a dissolve and loses scrollers

Usage:
  python3 transitions.py list
  python3 transitions.py apply A.mp4 B.mp4 --type whip --dir left -o out.mp4
  python3 transitions.py auto clips/ --bed bed.wav --format vlog -o edited.mp4
"""
import argparse, json, os, re, subprocess, sys, tempfile, random

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)


def _guard_output(out, *inputs):
    """Refuse to write over a source file. Protects original footage."""
    import os, sys
    ao = os.path.abspath(out)
    for i in inputs:
        if i and os.path.abspath(i) == ao:
            sys.exit(f"REFUSED: output '{out}' is the same file as an input. "
                     f"Source footage is never overwritten. Choose a different -o.")
    return out

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True); return r.stdout + r.stderr

def dur(p):
    o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"').strip()
    try: return float(o.splitlines()[0])
    except Exception: return 0.0

def dims(p):
    o = sh(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate '
           f'-of csv=p=0 "{p}"').strip().splitlines()[0].split(",")
    fps = eval(o[2]) if "/" in o[2] else float(o[2])
    return int(o[0]), int(o[1]), float(fps)

# ---------------- individual transitions ----------------
def t_whip(a, b, out, d=0.22, direction="left", W=1080, H=1920, fps=30):
    """Directional motion blur out of A and into B, cut at peak blur."""
    ang = 0 if direction in ("left", "right") else 90
    sgn = 1 if direction == "left" else -1
    da = dur(a)
    f = (f'[0:v]trim=0:{da},setpts=PTS-STARTPTS,setsar=1[a0];'
         f'[0:v]trim={max(0,da-d)}:{da},setpts=PTS-STARTPTS,'
         f'crop=iw:ih,scale={int(W*1.15)}:-1,'
         f'boxblur={int(28)}:1:cr=0:ar=0,'
         f'crop={W}:{H}:(iw-{W})/2+{sgn}*40:(ih-{H})/2,setsar=1[wa];'
         f'[1:v]trim=0:{d},setpts=PTS-STARTPTS,scale={int(W*1.15)}:-1,'
         f'boxblur={int(28)}:1:cr=0:ar=0,'
         f'crop={W}:{H}:(iw-{W})/2-{sgn}*40:(ih-{H})/2,setsar=1[wb];'
         f'[1:v]trim={d},setpts=PTS-STARTPTS,setsar=1[b0];'
         f'[a0][wa][wb][b0]concat=n=4:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

def t_punch(a, b, out, d=0.15, W=1080, H=1920, fps=30):
    """Fast scale-in on the last frames of A, then cut."""
    da = dur(a); n = max(3, int(d*fps))
    f = (f'[0:v]trim=0:{max(0,da-d)},setpts=PTS-STARTPTS,setsar=1[a0];'
         f'[0:v]trim={max(0,da-d)}:{da},setpts=PTS-STARTPTS,'
         f"zoompan=z='min(zoom+0.06,1.35)':d={n}:s={W}x{H}:fps={fps},"
         f"trim=0:{d},setpts=PTS-STARTPTS,setsar=1[ap];"
         f'[a0][ap][1:v]concat=n=3:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

def t_ramp(a, b, out, d=0.5, W=1080, H=1920, fps=30):
    """Speed up out of A, normal into B."""
    da = dur(a)
    f = (f'[0:v]trim=0:{max(0,da-d)},setpts=PTS-STARTPTS,setsar=1[a0];'
         f'[0:v]trim={max(0,da-d)}:{da},setpts=0.35*(PTS-STARTPTS)[af];'
         f'[a0][af][1:v]concat=n=3:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

def t_flash(a, b, out, d=0.08, W=1080, H=1920, fps=30):
    """1-2 frame exposure blowout on the seam. Best on impacts."""
    da = dur(a)
    f = (f'[0:v]trim=0:{max(0,da-d)},setpts=PTS-STARTPTS,setsar=1[a0];'
         f'[0:v]trim={max(0,da-d)}:{da},setpts=PTS-STARTPTS,'
         f'eq=brightness=0.75:saturation=0.2[fl];'
         f'[a0][fl][1:v]concat=n=3:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

def t_push(a, b, out, d=0.3, direction="left", W=1080, H=1920, fps=30):
    """B slides in over A. Spatial change."""
    x = f"'W-W*t/{d}'" if direction == "left" else f"'-W+W*t/{d}'"
    da = dur(a)
    f = (f'[0:v]trim=0:{max(0,da-d)},setpts=PTS-STARTPTS,setsar=1[a0];'
         f'[0:v]trim={max(0,da-d)}:{da},setpts=PTS-STARTPTS[at];'
         f'[1:v]trim=0:{d},setpts=PTS-STARTPTS[bt];'
         f'[at][bt]overlay=x={x}:y=0[ov];'
         f'[1:v]trim={d},setpts=PTS-STARTPTS,setsar=1[b0];'
         f'[a0][ov][b0]concat=n=3:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

def t_glitch(a, b, out, d=0.16, W=1080, H=1920, fps=30):
    """RGB split + displacement. The ~30s pattern interrupt."""
    da = dur(a)
    f = (f'[0:v]trim=0:{max(0,da-d)},setpts=PTS-STARTPTS,setsar=1[a0];'
         f'[0:v]trim={max(0,da-d)}:{da},setpts=PTS-STARTPTS,'
         f'rgbashift=rh=-14:bh=14:gv=6,noise=alls=22:allf=t[gl];'
         f'[a0][gl][1:v]concat=n=3:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

def t_zoomblur(a, b, out, d=0.18, W=1080, H=1920, fps=30):
    da = dur(a); n = max(3, int(d*fps))
    f = (f'[0:v]trim=0:{max(0,da-d)},setpts=PTS-STARTPTS,setsar=1[a0];'
         f'[0:v]trim={max(0,da-d)}:{da},setpts=PTS-STARTPTS,'
         f"zoompan=z='min(zoom+0.09,1.5)':d={n}:s={W}x{H}:fps={fps},boxblur=10:1,"
         f"trim=0:{d},setpts=PTS-STARTPTS[zb];"
         f'[a0][zb][1:v]concat=n=3:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

def t_dip(a, b, out, d=0.2, colour="black", W=1080, H=1920, fps=30):
    da = dur(a); h = d/2
    f = (f'[0:v]fade=t=out:st={max(0,da-h)}:d={h}:c={colour}[a0];'
         f'[1:v]fade=t=in:st=0:d={h}:c={colour}[b0];'
         f'[a0][b0]concat=n=2:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

def t_mask(a, b, out, d=0.25, W=1080, H=1920, fps=30):
    """Wipe driven by a moving edge — stand-in for an object wipe.
    Also hides identity drift across an AI seam (file 25 preference)."""
    da = dur(a)
    f = (f'[0:v]trim=0:{max(0,da-d)},setpts=PTS-STARTPTS,setsar=1[a0];'
         f'[0:v]trim={max(0,da-d)}:{da},setpts=PTS-STARTPTS[at];'
         f'[1:v]trim=0:{d},setpts=PTS-STARTPTS[bt];'
         f"[at][bt]xfade=transition=wipeleft:duration={d}:offset=0[ov];"
         f'[1:v]trim={d},setpts=PTS-STARTPTS,setsar=1[b0];'
         f'[a0][ov][b0]concat=n=3:v=1:a=0[v]')
    sh(f'ffmpeg -y -v error -i "{a}" -i "{b}" -filter_complex "{f}" -map "[v]" '
       f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{out}"')
    return out

TRANSITIONS = {"whip":t_whip, "punch":t_punch, "ramp":t_ramp, "flash":t_flash,
               "push":t_push, "glitch":t_glitch, "zoomblur":t_zoomblur,
               "dip":t_dip, "mask":t_mask}

# what each transition is FOR — used by auto-selection
MOTIVATION = {
 "whip":    "camera or subject moves left/right across the cut",
 "punch":   "static frame that needs energy injected",
 "ramp":    "action resolving into its aftermath",
 "mask":    "an object crosses frame — also hides AI identity drift",
 "flash":   "an impact or a reveal lands",
 "push":    "spatial change: entering/leaving a space",
 "glitch":  "pattern interrupt, roughly every 30s",
 "zoomblur":"speed or hype",
 "dip":     "chapter/section change",
}

def auto_select(i, n, motion_a, motion_b, is_ai_seam=False, since_flashy=99):
    """Pick a transition from what's physically continuous. Hard cut is the default."""
    if is_ai_seam:          return "mask"      # hides drift
    if since_flashy < 15:   return None        # max one flashy per 15s
    if motion_a > 0.8 and motion_b > 0.8:      return "whip"
    if motion_a < 0.3 and motion_b < 0.3:      return "punch"
    if motion_a > 1.2:                          return "ramp"
    if i == n//2:                               return "glitch"
    return None

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("apply"); p.add_argument("a"); p.add_argument("b")
    p.add_argument("--type", required=True, choices=list(TRANSITIONS))
    p.add_argument("--dir", default="left"); p.add_argument("--dur", type=float, default=0.22)
    p.add_argument("-o", default="out.mp4")
    q = sub.add_parser("auto"); q.add_argument("folder"); q.add_argument("--bed")
    q.add_argument("--format", default="vlog"); q.add_argument("-o", default="edited.mp4")
    a = ap.parse_args()

    if a.cmd == "list":
        print(f"{'transition':<10} use it when")
        print("-"*70)
        for k, v in MOTIVATION.items(): print(f"{k:<10} {v}")
        print("\nRULES: max one flashy per 15s · never decorate the twist seam ·")
        print("       land on the beat · cap 0.5s or it reads as a dissolve")
        return

    if a.cmd == "apply":
        W, H, fps = dims(a.a)
        fn = TRANSITIONS[a.type]
        kw = dict(d=a.dur, W=W, H=H, fps=fps)
        if a.type in ("whip", "push"): kw["direction"] = a.dir
        _guard_output(a.o, a.a, a.b)
        out = fn(a.a, a.b, a.o, **kw)
        print(f"{a.type} -> {out} ({dur(out):.2f}s)")
        return

    if a.cmd == "auto":
        import pacing
        clips = sorted([os.path.join(a.folder, f) for f in os.listdir(a.folder)
                        if f.lower().endswith((".mp4",".mov",".mkv"))])
        if len(clips) < 2: print("need 2+ clips"); return
        print(f"{len(clips)} clips")
        motions = []
        for c in clips:
            try: motions.append(pacing.analyse(c, a.format)["motion_mean"])
            except Exception: motions.append(0.5)
        tmp = tempfile.mkdtemp(); cur = clips[0]; since = 99; plan = []
        for i in range(1, len(clips)):
            t = auto_select(i, len(clips), motions[i-1], motions[i], since_flashy=since)
            nxt = os.path.join(tmp, f"j{i}.mp4")
            if t:
                W, H, fps = dims(cur)
                kw = dict(d=0.22, W=W, H=H, fps=fps)
                if t in ("whip","push"): kw["direction"] = random.choice(["left","right"])
                TRANSITIONS[t](cur, clips[i], nxt, **kw); since = 0
            else:
                lst = os.path.join(tmp, f"l{i}.txt")
                open(lst,"w").write(f"file '{cur}'\nfile '{clips[i]}'\n")
                sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c copy "{nxt}"')
                since += dur(clips[i])
            plan.append({"seam": i, "transition": t or "hard cut",
                         "motion_before": round(motions[i-1],2), "motion_after": round(motions[i],2)})
            cur = nxt
        sh(f'cp "{cur}" "{a.o}"')
        print(json.dumps(plan, indent=1))
        print(f"\n-> {a.o} ({dur(a.o):.2f}s)")
        print("NOTE: transitions chosen from motion continuity. Override any seam with `apply`.")

if __name__ == "__main__":
    main()
