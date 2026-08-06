#!/usr/bin/env python3
"""
SMOKETEST — run every route on synthetic stand-ins and ASSERT on measurable properties.

WHY THIS EXISTS
  16 tools were written and syntax-checked. Syntax-checking proves a file parses; it proves
  nothing about behaviour. One afternoon of actually executing them found NINE real defects,
  every one invisible to inspection:

    1. whip crashed at 720x1280 (SAR 6615:6616 from scale=W*1.15:-1; concat refuses)
    2. zoomblur +1.0s / punch +1.0s (zoompan d=N emits N frames PER INPUT FRAME)
    3. -shortest silently deleted 8s of video (mix ended at VO length)
    4. the last 7s were dead air at -33 dB (flat bed, no ducking)
    5. single-pass loudnorm pumped for ~3s after the deliberate silence gap
    6. alimiter did not limit at all - its auto-level defaults ON and renormalises to
       full scale, so limit=0.85 still measured -0.0 dBFS
    7. a slow push on a VIDEO hung ffmpeg (~16k frames, same zoompan bug)
    8. no text at all in the final 7s, and no AI disclosure
    9. a 6.0s slot is impossible - every generated clip is 5s

  ffmpeg is the reason. It rarely errors; it produces SOMETHING wrong and exits 0. So the
  only defence is to assert on measured numbers, at the real output resolution.

WHAT IT CHECKS (all mechanical - no judgement anywhere)
  route 1  transitions   all 9, at 720x1280, exact duration, non-zero output
  route 2  stills        zoompan gives exact duration and real motion
  route 3  push          held-shot push is exact duration and does not hang
  route 4  concat        SAR/fps consistency; total = sum of parts
  route 5  audio mix     no truncation, silence gap present and deep, tail not dead
  route 6  loudness      converges into the target band, true peak <= -1.0 dBTP
  route 7  captions      whisper resolves, cards render, text fits inside the frame
  route 8  guards        source files are never overwritten
  route 9  gate          mastermind + pacing run and return numbers

Usage
  python3 tools/smoketest.py            # everything
  python3 tools/smoketest.py -k audio   # only routes whose name matches
  python3 tools/smoketest.py --keep     # keep the scratch dir for inspection
"""
import os, sys, subprocess, tempfile, shutil, argparse, time, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
W, H, FPS = 720, 1280, 30

RESULTS = []

def sh(c, timeout=120):
    try:
        r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return -9, f"TIMEOUT after {timeout}s"

def dur(p):
    _, o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"')
    try: return float(o.strip().splitlines()[0])
    except Exception: return 0.0

def probe(p, stream="v:0", fields="width,height,sample_aspect_ratio,r_frame_rate"):
    _, o = sh(f'ffprobe -v error -select_streams {stream} -show_entries stream={fields} '
              f'-of default=nw=1 "{p}"')
    return dict(l.split("=", 1) for l in o.strip().splitlines() if "=" in l)

def lufs(p):
    _, o = sh(f'ffmpeg -nostats -i "{p}" -af ebur128=peak=true -f null /dev/null')
    I = pk = None
    for ln in o.splitlines():
        if "I:" in ln and "LUFS" in ln:
            try: I = float(ln.split("I:")[1].split("LUFS")[0].strip())
            except Exception: pass
        if "Peak:" in ln and "dBFS" in ln:
            try: pk = float(ln.split("Peak:")[1].split("dBFS")[0].strip())
            except Exception: pass
    return I, pk

def envelope(p, sr=8000, win_ms=100):
    import numpy as np
    raw = subprocess.run(f'ffmpeg -v error -i "{p}" -ac 1 -ar {sr} -f s16le -',
                         shell=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
    if len(x) < sr // 4: return None, None
    w = max(1, int(sr * win_ms / 1000))
    r = np.sqrt(np.convolve(x**2, np.ones(w)/w, "same"))
    return 20*np.log10(r + 1e-9), sr

def motion(p, max_frames=90):
    try:
        import cv2, numpy as np
    except Exception:
        return None
    cap = cv2.VideoCapture(p); prev = None; vals = []
    while len(vals) < max_frames:
        ok, fr = cap.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), (160, 284))
        if prev is not None:
            f = cv2.calcOpticalFlowFarneback(prev, g, None, .5,3,15,3,5,1.2,0)
            vals.append(float(np.linalg.norm(f, axis=2).mean()))
        prev = g
    cap.release()
    return float(np.mean(vals)) if vals else 0.0

# ---------------------------------------------------------------- assertions
class Route:
    def __init__(self, name):
        self.name = name; self.checks = []
    def ok(self, label, cond, detail=""):
        self.checks.append((bool(cond), label, detail))
        print(f"    {'PASS' if cond else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
        return bool(cond)
    def near(self, label, got, want, tol, unit=""):
        good = got is not None and abs(got - want) <= tol
        return self.ok(label, good, f"got {got}{unit}, want {want}+/-{tol}{unit}")
    def finish(self):
        failed = [c for c in self.checks if not c[0]]
        RESULTS.append((self.name, len(self.checks) - len(failed), len(failed)))
        return not failed

# ---------------------------------------------------------------- fixtures
def make_fixtures(d):
    """Textured stand-ins. Flat colour has ZERO optical flow, which makes every motion
    assertion meaningless - so the fixtures carry real detail and real movement."""
    os.makedirs(d, exist_ok=True)
    a = os.path.join(d, "A.mp4"); b = os.path.join(d, "B.mp4")
    still = os.path.join(d, "still.png"); vo = os.path.join(d, "vo.wav")
    common = (f"-vf \"scale={W}:{H},format=yuv420p\" -c:v libx264 -crf 22 -preset ultrafast")
    sh(f'ffmpeg -y -v error -f lavfi -i "testsrc2=s={W}x{H}:r={FPS}:d=5" {common} "{a}"')
    sh(f'ffmpeg -y -v error -f lavfi -i "smptebars=s={W}x{H}:r={FPS}:d=5" '
       f'-vf "scale={W}:{H},noise=alls=14:allf=t+u,format=yuv420p" '
       f'-c:v libx264 -crf 22 -preset ultrafast "{b}"')
    sh(f'ffmpeg -y -v error -f lavfi -i "testsrc2=s=1400x2400:d=1" -frames:v 1 "{still}"')
    # speech-like: bursts with real gaps, so ducking and gap detection mean something
    sh(f'ffmpeg -y -v error -f lavfi -i "anoisesrc=d=12:c=pink:a=0.5" '
       f'-af "tremolo=f=2.2:d=0.95,highpass=f=180,lowpass=f=3400" "{vo}"')
    return a, b, still, vo

# ---------------------------------------------------------------- routes
def route_transitions(d, A, B):
    r = Route("transitions")
    try:
        import transitions as TX
    except Exception as e:
        r.ok("import transitions.py", False, str(e)[:60]); return r.finish()
    da, db, dd = dur(A), dur(B), 0.20
    for name in TX.TRANSITIONS:
        o = os.path.join(d, f"tx_{name}.mp4")
        if os.path.exists(o): os.remove(o)
        kw = dict(d=dd, W=W, H=H, fps=FPS)
        if name in ("whip", "push"): kw["direction"] = "left"
        t0 = time.time()
        try: TX.TRANSITIONS[name](A, B, o, **kw)
        except Exception as e:
            r.ok(f"{name}: runs", False, str(e)[:60]); continue
        el = time.time() - t0
        if not r.ok(f"{name}: produced a file", os.path.exists(o) and os.path.getsize(o) > 5000,
                    f"{os.path.getsize(o) if os.path.exists(o) else 0} bytes"):
            continue
        # duration must not inflate: that was the zoompan d=N bug (+1.0s)
        got = dur(o)
        r.ok(f"{name}: duration sane", abs(got - (da + db)) <= 0.45,
             f"{got:.2f}s vs sources {da+db:.2f}s")
        st = probe(o)
        r.ok(f"{name}: SAR normalised",
             st.get("sample_aspect_ratio", "1:1") in ("1:1", "0:1", "N/A"),
             f"SAR {st.get('sample_aspect_ratio')}")
        r.ok(f"{name}: {W}x{H}", st.get("width") == str(W) and st.get("height") == str(H),
             f"{st.get('width')}x{st.get('height')}")
        r.ok(f"{name}: not pathologically slow", el < 45, f"{el:.1f}s")
    return r.finish()

def route_stills(d, still):
    r = Route("stills")
    o = os.path.join(d, "still_zp.mp4"); slot = 2.5
    rc, err = sh(f'ffmpeg -y -v error -loop 1 -i "{still}" -t {slot} '
                 f'-vf "scale=1400:-1,zoompan=z=\'min(zoom+0.0012,1.18)\':d={int(slot*FPS)}:'
                 f's={W}x{H}:fps={FPS},setsar=1" -c:v libx264 -crf 20 -preset veryfast '
                 f'-pix_fmt yuv420p "{o}"', timeout=90)
    r.ok("zoompan on a still renders", rc == 0 and os.path.exists(o), err.strip()[:70])
    if os.path.exists(o):
        r.near("still duration exact", round(dur(o), 2), slot, 0.10, "s")
        m = motion(o)
        r.ok("still actually moves", m is None or m > 0.05,
             "opencv absent" if m is None else f"motion {m:.3f}")
    return r.finish()

def route_push(d, A):
    r = Route("push")
    o = os.path.join(d, "push.mp4"); slot = 4.2
    vf = ("crop=w='iw/min(1+0.0007*n,1.09)':h='ih/min(1+0.0007*n,1.09)':"
          f"x='(iw-ow)/2':y='(ih-oh)/2',scale={W}:{H},fps={FPS},setsar=1")
    t0 = time.time()
    rc, err = sh(f'ffmpeg -y -v error -t {slot} -i "{A}" -vf "{vf}" -an '
                 f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{o}"', timeout=60)
    el = time.time() - t0
    r.ok("crop-push renders", rc == 0 and os.path.exists(o), err.strip()[:70])
    r.ok("crop-push does not hang", el < 30, f"{el:.1f}s")
    if os.path.exists(o):
        r.near("push duration exact", round(dur(o), 2), slot, 0.10, "s")
    # the trap: zoompan on a VIDEO input explodes to ~16k frames
    o2 = os.path.join(d, "push_zoompan.mp4")
    rc2, _ = sh(f'ffmpeg -y -v error -t 1.0 -i "{A}" '
                f'-vf "zoompan=z=\'min(zoom+0.001,1.09)\':d=30:s={W}x{H}:fps={FPS}" '
                f'-an -c:v libx264 -preset ultrafast "{o2}"', timeout=25)
    got = dur(o2) if os.path.exists(o2) else 0
    r.ok("zoompan-on-video trap still documented", got > 1.5 or rc2 == -9,
         f"1.0s in -> {got:.2f}s out (this is why push uses crop, not zoompan)")
    return r.finish()

def route_concat(d, A, B):
    r = Route("concat")
    segs = []
    for i, (src, slot) in enumerate([(A, 2.0), (B, 1.5), (A, 3.0)]):
        o = os.path.join(d, f"cseg{i}.mp4")
        sh(f'ffmpeg -y -v error -t {slot} -i "{src}" '
           f'-vf "scale={W}:{H},fps={FPS},setsar=1" -an -c:v libx264 -crf 22 '
           f'-preset ultrafast -pix_fmt yuv420p "{o}"')
        segs.append(o)
    want = sum(dur(s) for s in segs)
    lst = os.path.join(d, "list.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    o = os.path.join(d, "cat.mp4")
    rc, err = sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -c:v libx264 -crf 22 '
                 f'-preset ultrafast -pix_fmt yuv420p -an "{o}"')
    r.ok("concat runs", rc == 0 and os.path.exists(o), err.strip()[:70])
    if os.path.exists(o):
        r.near("total = sum of parts", round(dur(o), 2), round(want, 2), 0.20, "s")
        r.ok("no zero-byte output", os.path.getsize(o) > 10000)
    return r.finish()

def route_audio(d, A, vo):
    r = Route("audio")
    vid = os.path.join(d, "amix_src.mp4")
    sh(f'ffmpeg -y -v error -f lavfi -i "testsrc2=s={W}x{H}:r={FPS}:d=30" '
       f'-c:v libx264 -crf 24 -preset ultrafast -pix_fmt yuv420p "{vid}"')
    vd = dur(vid); reveal = 20.0
    bed = None
    for c in sorted(glob.glob(os.path.join(ROOT, "assets", "bgm", "utility-beds", "*.wav"))):
        e, _ = envelope(c)
        if e is not None and float((e > -30).mean()) > 0.8: bed = c; break
    r.ok("a sustaining bed exists", bed is not None,
         os.path.basename(bed) if bed else "none found - tail will be thin")
    ins = ["-i", f'"{vid}"', "-i", f'"{vo}"']; fl = []; mix = []; idx = 2
    fmt = "aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo"
    if bed:
        fl.append(f"[1:a]adelay=1500|1500,loudnorm=I=-8:TP=-1.5:LRA=11,apad,{fmt},asplit=2[vo][vokey]")
        ins += ["-stream_loop", "-1", "-i", f'"{bed}"']
        fl.append(f"[{idx}:a]atrim=0:{vd:.2f},asetpts=N/SR/TB,volume=0.55,{fmt}[bedraw]")
        fl.append("[bedraw][vokey]sidechaincompress=threshold=0.03:ratio=12:attack=15:"
                  "release=400:makeup=1[bed]")
        mix += ["[vo]", "[bed]"]; idx += 1
    else:
        fl.append(f"[1:a]adelay=1500|1500,loudnorm=I=-8:TP=-1.5:LRA=11,apad[vo]"); mix.append("[vo]")
    g0, g1 = reveal - 0.45, reveal - 0.05
    fl.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=longest:dropout_transition=0:"
              f"normalize=0,volume=enable='between(t,{g0:.2f},{g1:.2f})':volume=0.08,"
              f"alimiter=limit=0.89:level=disabled[aout]")
    o = os.path.join(d, "mixed.mp4")
    rc, err = sh(f'ffmpeg -y -v error {" ".join(ins)} -filter_complex "{";".join(fl)}" '
                 f'-map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -t {vd:.2f} "{o}"',
                 timeout=180)
    if not r.ok("mix renders", rc == 0 and os.path.exists(o), err.strip()[:90]):
        return r.finish()
    # THE -shortest BUG: the mix must never truncate the video
    r.near("mix did not truncate the video", round(dur(o), 2), round(vd, 2), 0.25, "s")
    e, sr = envelope(o)
    if e is None:
        r.ok("audio readable", False, "no samples decoded"); return r.finish()
    import numpy as np
    body = float(np.median(e[int(3*sr):int(18*sr)]))
    gap  = float(e[int((reveal-0.25)*sr)])
    tail = float(np.median(e[int(24*sr):int(29*sr)]))
    r.ok("silence gap is present and deep", body - gap >= 8.0,
         f"body {body:.1f} dB -> gap {gap:.1f} dB = {body-gap:.1f} dB dip")
    r.ok("tail is not dead air", tail > -28.0, f"tail {tail:.1f} dB (dead air was -33)")
    r.ok("hook has audio from the start", float(np.median(e[int(0.2*sr):int(1.2*sr)])) > -35.0,
         f"{float(np.median(e[int(0.2*sr):int(1.2*sr)])):.1f} dB in the first second")
    return r.finish()

def route_loudness(d):
    r = Route("loudness")
    src = os.path.join(d, "mixed.mp4")
    if not os.path.exists(src):
        r.ok("mixed.mp4 from the audio route exists", False); return r.finish()
    # alimiter auto-level defaults ON and defeats `limit` entirely
    bad = os.path.join(d, "lim_default.mp4")
    sh(f'ffmpeg -y -v error -i "{src}" -af "volume=6dB,alimiter=limit=0.85" '
       f'-c:v copy -c:a aac "{bad}"')
    _, pk_bad = lufs(bad)
    good = os.path.join(d, "lim_disabled.mp4")
    sh(f'ffmpeg -y -v error -i "{src}" -af "volume=6dB,alimiter=limit=0.85:level=disabled" '
       f'-c:v copy -c:a aac "{good}"')
    _, pk_good = lufs(good)
    r.ok("alimiter needs level=disabled to actually limit",
         pk_good is not None and pk_bad is not None and pk_good < pk_bad - 0.5,
         f"default {pk_bad} dBFS vs level=disabled {pk_good} dBFS")
    try:
        import build_kk
        o = os.path.join(d, "normed.mp4")
        build_kk.TMP = d
        build_kk.normalise(src, o, target=-8.0)
        I, pk = lufs(o)
        r.ok("converges into your measured band", I is not None and -9.5 <= I <= -6.5,
             f"{I} LUFS (target -7..-9)")
        r.ok("true peak clears the hard gate", pk is not None and pk <= -1.0,
             f"{pk} dBTP (gate <= -1.0)")
    except Exception as e:
        r.ok("build_kk.normalise runs", False, str(e)[:70])
    return r.finish()

def route_captions(d, vo):
    r = Route("captions")
    try:
        import transcribe, autocut
    except Exception as e:
        r.ok("import transcribe + autocut", False, str(e)[:60]); return r.finish()
    tr = transcribe.run(vo)
    r.ok("whisper resolves weights", tr.get("tier") == "faster-whisper",
         f"tier={tr.get('tier')} {str(tr.get('error',''))[:50]}")
    # schema contract: transcribe emits "w", autocut reads "w". A rename breaks captions.
    fake = [{"w": t, "start": 0.3*i, "end": 0.3*i+0.28} for i, t in
            enumerate("Three spots in KK you should hit. One. Filipino Market.".split())]
    try:
        cards = autocut.captions_from_words(fake, max_chars=24)
        r.ok("word schema contract holds ('w')", len(cards) > 0, f"{len(cards)} cards")
    except KeyError as e:
        r.ok("word schema contract holds ('w')", False, f"KeyError {e} - transcribe/autocut disagree")
        return r.finish()
    font = None
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(f): font = f; break
    if not r.ok("a bold font is available", font is not None): return r.finish()
    src = os.path.join(d, "cseg0.mp4")
    if not os.path.exists(src): src = os.path.join(d, "A.mp4")
    o = os.path.join(d, "capped.mp4"); vf = []
    for i, c in enumerate(cards):
        tf = os.path.join(d, f"cap{i}.txt"); open(tf, "w", encoding="utf-8").write(c["text"])
        vf.append(f"drawtext=fontfile='{font}':textfile='{tf}':fontsize=42:fontcolor=white:"
                  f"box=1:boxcolor=black@0.55:boxborderw=14:x=(w-tw)/2:y=h*0.78")
    rc, err = sh(f'ffmpeg -y -v error -i "{src}" -vf "{",".join(vf)}" -t 1 '
                 f'-c:v libx264 -preset ultrafast -pix_fmt yuv420p "{o}"')
    r.ok("caption cards render", rc == 0 and os.path.exists(o), err.strip()[:80])
    # overflow guard: a card must not exceed the frame width
    longest = max((c["text"] for c in cards), key=len)
    r.ok("longest card fits 720px at 42pt", len(longest) * 23 + 28 <= W,
         f"'{longest}' ~{len(longest)*23+28}px of {W}px")
    return r.finish()

def route_guards(d, A):
    r = Route("guards")
    victim = os.path.join(d, "precious.mp4")
    shutil.copy(A, victim); before = os.path.getsize(victim)
    hit = 0
    for mod in ("transitions", "grade", "autocut", "edl"):
        try:
            m = __import__(mod)
        except Exception:
            continue
        g = getattr(m, "_guard_output", None)
        if not g: continue
        hit += 1
        try:
            g(victim, victim); r.ok(f"{mod}._guard_output refuses self-overwrite", False,
                                    "it returned instead of exiting")
        except SystemExit:
            r.ok(f"{mod}._guard_output refuses self-overwrite", True)
        except Exception as e:
            r.ok(f"{mod}._guard_output refuses self-overwrite", False, str(e)[:50])
    r.ok("at least one guard is wired", hit > 0, f"{hit} module(s) expose _guard_output")
    r.ok("source file untouched", os.path.getsize(victim) == before)
    return r.finish()

def route_gate(d):
    r = Route("gate")
    src = os.path.join(d, "mixed.mp4")
    if not os.path.exists(src):
        r.ok("mixed.mp4 exists", False); return r.finish()
    try:
        import mastermind
        a = mastermind.audio_metrics(src)
        r.ok("mastermind.audio_metrics returns LUFS", a.get("lufs") is not None,
             f"{a.get('lufs')} LUFS, peak {a.get('peak')}")
        v = mastermind.video_metrics(src, d)
        r.ok("mastermind.video_metrics returns motion", v.get("motion_mean") is not None,
             f"motion {v.get('motion_mean')}, blanks {v.get('blank_frames')}")
    except Exception as e:
        r.ok("mastermind runs", False, str(e)[:70])
    try:
        import pacing
        p = pacing.analyse(src, "vlog")
        r.ok("pacing.analyse returns numbers", p.get("duration", 0) > 0,
             f"{p['duration']}s, {p['cuts_per_min']} cuts/min")
        r.ok("pacing labels its estimate as a heuristic",
             "HEURISTIC" in p.get("estimate_disclaimer", "").upper())
    except Exception as e:
        r.ok("pacing runs", False, str(e)[:70])
    return r.finish()

ROUTES = [
    ("transitions", lambda d, f: route_transitions(d, f["A"], f["B"])),
    ("stills",      lambda d, f: route_stills(d, f["still"])),
    ("push",        lambda d, f: route_push(d, f["A"])),
    ("concat",      lambda d, f: route_concat(d, f["A"], f["B"])),
    ("audio",       lambda d, f: route_audio(d, f["A"], f["vo"])),
    ("loudness",    lambda d, f: route_loudness(d)),
    ("captions",    lambda d, f: route_captions(d, f["vo"])),
    ("guards",      lambda d, f: route_guards(d, f["A"])),
    ("gate",        lambda d, f: route_gate(d)),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--only", help="run only routes whose name contains this")
    ap.add_argument("--keep", action="store_true", help="keep the scratch dir")
    ap.add_argument("--dir", help="use this scratch dir instead of a temp one")
    args = ap.parse_args()

    rc, _ = sh("ffmpeg -version")
    if rc != 0:
        print("ffmpeg is not on PATH. Nothing can be tested."); return 2

    d = args.dir or tempfile.mkdtemp(prefix="talyx_smoke_")
    os.makedirs(d, exist_ok=True)
    print("=" * 62)
    print("TALYX SMOKETEST   every route, real resolution, measured assertions")
    print(f"scratch: {d}")
    print("=" * 62)
    t0 = time.time()
    A, B, still, vo = make_fixtures(d)
    fix = {"A": A, "B": B, "still": still, "vo": vo}
    for name, fn in ROUTES:
        if args.only and args.only.lower() not in name.lower(): continue
        print(f"\n[{name}]")
        try: fn(d, fix)
        except Exception as e:
            print(f"    FAIL  route crashed: {str(e)[:80]}")
            RESULTS.append((name, 0, 1))

    print("\n" + "=" * 62)
    tot_p = sum(p for _, p, _ in RESULTS); tot_f = sum(f for _, _, f in RESULTS)
    for n, p, f in RESULTS:
        print(f"  {'OK  ' if not f else 'FAIL'} {n:14s} {p} passed" + (f", {f} FAILED" if f else ""))
    print("=" * 62)
    print(f"  {tot_p} passed, {tot_f} failed   in {time.time()-t0:.0f}s")
    if tot_f:
        print("\n  Any FAIL above is a defect that would otherwise reach a real render.")
    if not args.keep and not args.dir:
        shutil.rmtree(d, ignore_errors=True)
    else:
        print(f"\n  scratch kept: {d}")
    return 1 if tot_f else 0

if __name__ == "__main__":
    sys.exit(main())
