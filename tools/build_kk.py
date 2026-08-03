#!/usr/bin/env python3
"""
BUILD_KK — full auto-assembly for "3 best spots in Kota Kinabalu Sabah".
Every creative decision was locked at the Phase 1 gate. This executes it deterministically.

PIPELINE
  1. verify all assets present
  2. trim each shot to its slot (hook trimmed so Nev is already mid-stride at 0:00)
  3. stills -> zoompan motion
  4. transitions per seam, motivated (max one flashy per 15s)
  5. VO normalised to -8 LUFS (your MEASURED target from file 19)
  6. SFX: whoosh on location jumps, impact on food reveal,
     SILENCE 0.4s before the sunset reveal then sub_drop  <- Arena Zero technique
  7. ambience bed under everything at -32dB
  8. word-exact captions via Whisper
  9. mastermind + pacing + rhythm gate, numbers printed
Usage:  python3 tools/build_kk.py
"""
import os, subprocess, sys, json, glob, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W    = os.path.join(ROOT, "work")
A    = os.path.join(ROOT, "assets")
OUT  = os.path.join(ROOT, "output")
TMP  = os.path.join(W, "_kk_tmp")
sys.path.insert(0, os.path.join(ROOT, "tools"))

def sh(c, cwd=None):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr

def dur(p):
    _, o = sh(f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{p}"')
    try: return float(o.strip().splitlines()[0])
    except Exception: return 0.0

# ---------------------------------------------------------------- the timeline
# Rebuilt after his review. Three complaints drove every change:
#   "no BGM"                   -> bgmgen.py synthesises a bed arranged to this cut
#   "stagnant image of fish"   -> stills go through animate.py (parallax + caustics + drift)
#   "just a sunset... stale"   -> MEASURED: KK_08_sunset_hero is 0.149 mean optical flow, i.e.
#                                 the generated sunset is itself nearly frozen. So the sunset
#                                 material is re-cut as COVERAGE - wide then tight from the same
#                                 clip - which reads as two shots and costs zero credits.
# 14 shots in 30s instead of 10. Cut rate is deliberately above the vlog band: this is a
# montage, and the old 10-shot version spent 46% of its runtime on one visual idea.
#
# fields: tag, source, in-point, slot, transition-out, treatment, crop(scale,cx,cy)
TL = [
 ("01",  "KK_01_hook_sunset.mp4",    1.2, 2.6, "whip",     "enliven:generic",  None),
 ("02",  "KK_02_market_wide.mp4",    0.3, 2.0, None,       "enliven:generic",  None),
 ("03",  "KK_03_grill.mp4",          0.4, 1.6, None,       "enliven:generic",  None),
 ("03b", "KK_03_grill.mp4",          2.2, 1.2, None,       "enliven:generic",  (2.0, 0.50, 0.55)),
 ("04",  "KK_04_nev_eating.mp4",     0.4, 2.2, "zoomblur", "enliven:generic",  None),
 ("05",  "KK_05_boat.mp4",           0.3, 1.8, None,       "enliven:generic",  None),
 ("06",  "KK_S6_coral.png",          0.0, 2.6, None,       "animate:underwater", None),
 ("07",  "KK_07_beach_nev.mp4",      0.4, 2.8, None,       "enliven:generic",  None),
 ("07b", "KK_07_beach_nev.mp4",      2.0, 1.4, None,       "enliven:generic",  (1.9, 0.50, 0.45)),
 ("08",  "KK_08_sunset_hero.mp4",    0.2, 2.4, None,       "enliven:sunset",   None),   # reveal
 ("08b", "KK_08_sunset_hero.mp4",    1.6, 1.8, None,       "enliven:sunset",   (2.1, 0.50, 0.40)),
 ("09",  "KK_S9_silhouettes.png",    0.0, 3.0, None,       "animate:sunset",   None),
 ("10",  "KK_10_cta_silhouette.mp4", 0.3, 3.2, None,       "enliven:sunset",   None),
 ("10b", "KK_10_cta_silhouette.mp4", 1.5, 1.4, None,       "enliven:sunset",   (1.8, 0.50, 0.45)),
]                                                                    # slots total 30.0s
REVEAL_TAG = "08"       # the sunset reveal - the silence gap lands just before this

def need(f): return os.path.join(W, f)

def check():
    srcs = {t[1] for t in TL}
    missing = [x for x in sorted(srcs) if not os.path.exists(need(x))]
    if not os.path.exists(need("KK_VO.wav")): missing.append("KK_VO.wav")
    if missing:
        print("!! MISSING from work/ :"); [print("   -", m) for m in missing]
        return False
    print(f"OK  {len(srcs)} sources -> {len(TL)} shots")
    return True

def build_segments(force=False):
    """Resumable: a segment already rendered at the right duration is kept. animate/enliven
    are per-frame numpy, so a full pass is minutes - resuming makes iteration practical."""
    os.makedirs(TMP, exist_ok=True)
    try:
        import animate as AN
    except Exception as e:
        print("  !! animate.py unavailable:", str(e)[:60]); AN = None
    segs = []
    for tag, src, tin, slot, _tr, treat, crop in TL:
        p = need(src); o = os.path.join(TMP, f"s{tag}.mp4")
        # cache key must include the TREATMENT, not just duration: segments rendered before
        # motion treatment existed have the right length and were silently reused untreated.
        spec = f"{src}|{tin}|{slot}|{treat}|{crop}"
        sf = o + ".spec"
        cached = (not force and os.path.exists(o) and abs(dur(o) - slot) < 0.12
                  and os.path.exists(sf) and open(sf).read() == spec)
        if cached:
            segs.append(o); print(f"  seg {tag:4s} {dur(o):.2f}s  (cached)"); continue
        kind, _, preset = (treat or "").partition(":")
        preset = preset or "generic"
        done = False
        if AN and kind == "animate":
            try:
                AN.animate(p, o, dur=slot, preset=preset, zoom=0.22, quiet=True); done = True
            except Exception as e: print(f"  !! animate {tag}: {str(e)[:70]}")
        elif AN and kind == "enliven":
            avail = dur(p)
            if avail < slot + tin - 0.05:
                tin = max(0.0, avail - slot - 0.05)
            try:
                trimmed = os.path.join(TMP, f"t{tag}.mp4")
                sh(f'ffmpeg -y -v error -ss {tin} -t {slot} -i "{p}" '
                   f'-vf "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,'
                   f'fps=30,setsar=1" -an -c:v libx264 -crf 18 -preset veryfast '
                   f'-pix_fmt yuv420p "{trimmed}"')
                AN.enliven(trimmed, o, dur=slot, preset=preset,
                           zoom=(0.14 if crop else 0.09), crop=crop, quiet=True)
                done = True
            except Exception as e: print(f"  !! enliven {tag}: {str(e)[:70]}")
        if not done:                                  # plain trim fallback
            vf = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1"
            if src.lower().endswith(".png"):
                sh(f'ffmpeg -y -v error -loop 1 -i "{p}" -t {slot} -vf "scale=1400:-1,'
                   f'zoompan=z=\'min(zoom+0.0030,1.28)\':d={int(slot*30)}:s=720x1280:fps=30,'
                   f'setsar=1" -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{o}"')
            else:
                sh(f'ffmpeg -y -v error -ss {tin} -t {slot} -i "{p}" -vf "{vf}" -an '
                   f'-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p "{o}"')
        if os.path.exists(o):
            open(sf, "w").write(spec)
            segs.append(o); print(f"  seg {tag:4s} {dur(o):.2f}s  {treat or 'trim'}"
                                  + (f"  crop x{crop[0]}" if crop else ""))
    return segs

def apply_transitions(segs):
    """Only 2 flashy transitions in 30s = one per 15s. Everything else is a hard cut.
    Returns (segments, {shot_tag: absolute_start}, total). Times are MEASURED from the
    rendered files, so every SFX cue lands on the real timeline, not the planned one."""
    base = {TL[i][0]: dur(segs[i]) for i in range(len(segs))}   # pre-merge lengths
    try:
        import transitions as TX
    except Exception as e:
        print("  !! transitions.py unavailable:", str(e)[:60]); TX = None

    out = list(segs); merged = {}          # seg index -> [tags it contains]
    for i in range(len(out)): merged[i] = [TL[i][0]]
    if TX:
        for i, (tag, _, _, _, tr, _t, _c) in enumerate(TL):
            if not tr or i+1 >= len(out) or out[i] is None or out[i+1] is None: continue
            o = os.path.join(TMP, f"tx{tag}.mp4")
            want = base[tag] + base[TL[i+1][0]]
            spec = f"{tr}|{out[i]}|{out[i+1]}|{want:.3f}"
            sf = o + ".spec"
            if (os.path.exists(o) and os.path.exists(sf) and open(sf).read() == spec
                    and dur(o) > 1.0):
                print(f"  transition {tr:8s} seam {tag} -> {dur(o):.2f}s  (cached)")
                merged[i] = merged[i] + merged[i+1]
                out[i] = o; out[i+1] = None; merged[i+1] = []
                continue
            kw = dict(d=0.20, W=720, H=1280, fps=30)
            if tr in ("whip", "push"): kw["direction"] = "left"
            ok = False
            for attempt in (1, 2):                 # one retry: whip failed flaky once
                try: TX.TRANSITIONS[tr](out[i], out[i+1], o, **kw)
                except Exception as e: print(f"  !! {tr}@{tag}: {str(e)[:60]}")
                if os.path.exists(o) and dur(o) > 1.0: ok = True; break
                print(f"  .. {tr}@{tag} produced nothing (attempt {attempt})")
            if ok:
                open(sf, "w").write(spec)
                print(f"  transition {tr:8s} seam {tag} -> {dur(o):.2f}s "
                      f"(was {want:.2f}s)")
                merged[i] = merged[i] + merged[i+1]
                out[i] = o; out[i+1] = None; merged[i+1] = []
            else:
                print(f"  -- {tr}@{tag} FAILED twice -> hard cut (safe fallback)")

    segs2 = [x for x in out if x]
    tags2 = [merged[i] for i in range(len(out)) if out[i]]
    t, starts = 0.0, {}
    for seg, tags in zip(segs2, tags2):
        inner = t
        for tg in tags:
            starts[tg] = round(inner, 3); inner += base[tg]
        t += dur(seg)
    return segs2, starts, round(t, 3)

def concat(segs, o):
    l = os.path.join(TMP,"list.txt")
    open(l,"w").write("".join(f"file '{s}'\n" for s in segs))
    # every segment is already libx264 720x1280 30fps yuv420p, so stream-copy the concat.
    # Re-encoding here cost ~25s per run and gained nothing.
    rc, _ = sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{l}" -c copy -an "{o}"')
    if rc != 0 or dur(o) < 1.0:
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{l}" -c:v libx264 -crf 20 '
           f'-preset veryfast -pix_fmt yuv420p -an "{o}"')
    return o

def pick(*cands):
    for c in cands:
        g = glob.glob(os.path.join(A,"sfx",c))
        if g: return g[0]
    return None

def build_audio(video, o, reveal_t, starts, durations=None):
    """VO -8 LUFS + a bed that DUCKS under speech and RISES when speech stops,
    + SFX, + 0.4s of near-silence before the sunset reveal.

    The bed is not decoration. The VO ends at ~23s but the video runs to 30s; without a
    bed that comes up, the sunset payoff and the CTA play over dead air. Measured: a flat
    0.10 bed left the tail at -33 dB, which is silence on a phone. Sidechain ducking fixes
    both ends - it also fills the 1.5s before the VO starts, where the hook lives.
    """
    vo  = need("KK_VO.wav")
    # MEASURED: the raw VO is -22.8 LUFS and single-pass loudnorm could only lift it to
    # -11.6, not the -5 requested - it is a dynamic normaliser with a limited gain range.
    # That was the root cause of every loudness miss this session. Use a measured STATIC
    # gain instead: deterministic, reaches any target, and no pumping around the silence gap.
    vo_lufs = _lufs(vo) or -20.0
    vo_gain = max(-24.0, min(24.0, -6.0 - vo_lufs))
    print(f"  VO {vo_lufs:.1f} LUFS -> static {vo_gain:+.1f} dB (target -6)")
    bed = choose_bed()
    wh  = pick("transition/whoosh_up_v1.wav")
    wh2 = pick("transition/whoosh_down_v1.wav") or wh
    imp = pick("impact/impact_hit_v1.wav")
    sub = pick("impact/sub_drop_v1.wav")
    swl = pick("transition/swell_v1.wav")
    vd  = dur(video)

    # DIEGETIC FOLEY - his note: "there are no sound effects, for example the fishes in the
    # sea... bubbles... the walking at the night market... crowded night market sfx... when
    # the boat splashes the water... a splash water sfx".
    # v2 only had transition SFX, which decorate the CUT. This is ambience + spot effects that
    # say the PLACE is real, and the beds cross-fade across cuts so the edit stops being
    # audible ("the linkage are so seamless").
    foley_path = None
    if durations:
        try:
            import foley
            foley_path = os.path.join(TMP, "foley.wav")
            foley.render_track(starts, durations, vd, foley_path)
        except Exception as e:
            print(f"  !! foley unavailable: {str(e)[:70]}"); foley_path = None

    foley_ok = bool(foley_path) and os.path.exists(foley_path)
    ins = ["-i", f'"{video}"', "-i", f'"{vo}"']
    fl, mix, idx = [], [], 2
    has_bed = bool(bed) and os.path.exists(bed)
    fmt_s = "aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo"

    if has_bed:
        fl.append(f"[1:a]volume={vo_gain:.2f}dB,adelay=1500|1500,apad,"
                  "aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,"
                  + ("asplit=3[vo][vokey][vokey2]" if foley_ok else "asplit=2[vo][vokey]"))
        bed_lufs = _lufs(bed) or -18.0
        bed_gain = max(-24.0, min(24.0, -19.0 - bed_lufs))
        print(f"  bed {bed_lufs:.1f} LUFS -> static {bed_gain:+.1f} dB (target -19)")
        ins += ["-stream_loop", "-1", "-i", f'"{bed}"']
        fl.append(f"[{idx}:a]atrim=0:{vd:.2f},asetpts=N/SR/TB,volume={bed_gain:.2f}dB,"
                  f"afade=t=in:st=0:d=0.10,afade=t=out:st={vd-1.8:.2f}:d=1.8,"
                  f"aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[bedraw]")
        # duck the bed hard under speech; it recovers in ~400ms when Nev stops talking
        fl.append("[bedraw][vokey]sidechaincompress=threshold=0.03:ratio=12:"
                  "attack=15:release=400:makeup=1[bed]")
        mix += ["[vo]", "[bed]"]; idx += 1
    else:
        fl.append(f"[1:a]volume={vo_gain:.2f}dB,adelay=1500|1500,apad[vo]")
        mix.append("[vo]")

    if foley_ok:
        fl_lufs = _lufs(foley_path) or -20.0
        fl_gain = max(-24.0, min(24.0, -21.0 - fl_lufs))
        print(f"  foley {fl_lufs:.1f} LUFS -> static {fl_gain:+.1f} dB (target -21, under the VO)")
        ins += ["-i", f'"{foley_path}"']
        fl.append(f"[{idx}:a]volume={fl_gain:.2f}dB,{fmt_s}[foleyraw]")
        if has_bed:
            fl.append("[foleyraw][vokey2]sidechaincompress=threshold=0.05:ratio=7:"
                      "attack=15:release=350:makeup=1[foley]")
        else:
            fl.append("[foleyraw]anull[foley]")
        mix.append("[foley]"); idx += 1

    S = lambda tag, d=0.0: max(0.0, starts.get(tag, 0.0) + d)
    cues = [("wh",  wh,  S("02") - 0.10, 0.55),   # whip: sunset -> market
            ("imp", imp, S("03") + 0.10, 0.45),   # grilled seafood reveal
            ("wh2", wh2, S("05") - 0.10, 0.55),   # zoomblur: night market -> island
            ("sub", sub, reveal_t + 0.05, 0.80),  # lands INTO the 0.4s silence
            ("swl", swl, S("10") - 0.20, 0.40)]   # lift into the CTA
    placed = []
    for lab, f, t, g in cues:
        if not f or not os.path.exists(f): continue
        ins += ["-i", f'"{f}"']
        fl.append(f"[{idx}:a]adelay={int(t*1000)}|{int(t*1000)},volume={g}[{lab}]")
        mix.append(f"[{lab}]"); placed.append(f"{lab}@{t:.2f}s"); idx += 1

    g0, g1 = reveal_t - 0.45, reveal_t - 0.05
    fl.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=longest:"
              f"dropout_transition=0:normalize=0,"
              f"volume=enable='between(t,{g0:.2f},{g1:.2f})':volume=0.08,"
              f"alimiter=limit=0.79:level=disabled[aout]")

    cmd = (f'ffmpeg -y -v error {" ".join(ins)} -filter_complex "{";".join(fl)}" '
           f'-map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -t {vd:.2f} "{o}"')
    rc, err = sh(cmd)
    if rc != 0 or not os.path.exists(o):
        print("  !! full mix failed:", err.strip()[:150])
        print("  -> VO-only fallback")
        sh(f'ffmpeg -y -v error -i "{video}" -i "{vo}" -filter_complex '
           f'"[1:a]volume={vo_gain:.2f}dB,adelay=1500|1500,apad[a]" '
           f'-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t {vd:.2f} "{o}"')
    else:
        print(f"  VO + {'ducked bed + ' if has_bed else ''}{len(placed)} SFX: {', '.join(placed)}")
        print(f"  silence gap {g0:.2f}-{g1:.2f}s before the reveal")
    return o

def _sustain(f):
    """Fraction of the file above -30 dB. A music bed sustains (~1.0); a metronome
    click track does not (~0.3). Measured, so the choice is not a guess."""
    try:
        import numpy as np
        raw = subprocess.run(f'ffmpeg -v error -i "{f}" -ac 1 -ar 8000 -f s16le -',
                             shell=True, capture_output=True).stdout
        x = np.frombuffer(raw, dtype=np.int16).astype(float)/32768
        if len(x) < 8000: return 0.0
        w = 800; r = np.sqrt(np.convolve(x**2, np.ones(w)/w, "same"))
        return float((20*np.log10(r+1e-9) > -30).mean())
    except Exception:
        return 0.0

def choose_bed():
    """Prefer real music; fall back to whatever actually sustains. Warn if the library
    is empty, because a click track under a sunset is not a score."""
    # His note: "the bgm doesnt really match with the video feeling". The cause was TIMBRE -
    # a detuned-saw pad reads electronic. sunset_warm leads on marimba (inharmonic struck-bar
    # partials) and hand percussion instead of a kit. travel_bright / lofi_chill are the
    # alternates; swap the filename to A/B them.
    for name in ("BGM_sunset_warm.wav", "BGM_travel_bright.wav", "BGM_lofi_chill.wav",
                 "BGM_travel_arrangement.wav"):
        gen = os.path.join(A, "bgm", "generated", name)
        if os.path.exists(gen):
            print(f"  bed: {name}  (marimba + hand percussion, arranged to this cut, "
                  f"percussion out for the payoff)")
            return gen
    real = sorted(glob.glob(os.path.join(A,"bgm","mixkit","**","*.*"), recursive=True))
    real = [f for f in real if f.lower().endswith((".mp3",".wav",".m4a",".ogg"))]
    if real:
        best = max(real, key=_sustain)
        print(f"  bed: {os.path.basename(best)}  (sustain {_sustain(best)*100:.0f}%)")
        return best
    cands = sorted(glob.glob(os.path.join(A,"bgm","utility-beds","*.wav")))
    if not cands:
        print("  !! NO BGM AT ALL - shipping with VO + SFX only"); return None
    scored = [(f, _sustain(f)) for f in cands]
    best, sus = max(scored, key=lambda t: t[1])
    print(f"  !! assets/bgm/mixkit is EMPTY - no real music imported yet.")
    print(f"     falling back to {os.path.basename(best)} (sustain {sus*100:.0f}%). "
          f"Import music and re-run for a proper score.")
    if sus < 0.6:
        print(f"     WARNING: best available only sustains {sus*100:.0f}% - it is a click "
              f"track, not a bed. The tail will feel thin.")
    return best

def _lufs(f):
    """Integrated loudness. ebur128 emits an 'I:' line per frame plus a final summary,
    so the LAST match is the integrated value - the first is the fade-in."""
    _, out = sh(f'ffmpeg -nostats -i "{f}" -af ebur128 -f null /dev/null')
    v = None
    for ln in out.splitlines():
        if "I:" in ln and "LUFS" in ln:
            try: v = float(ln.split("I:")[1].split("LUFS")[0].strip())
            except Exception: pass
    return v

def normalise(f, o, target=-8.0, tol=0.7, passes=4):
    """Measure, apply a static gain, re-measure, correct. Iterate.

    A single static gain is not enough: the limiter reduces crest factor, which RAISES
    integrated loudness for the same peak. Measured: a +0.8 dB gain landed +1.9 dB.
    Note alimiter needs level=disabled - its auto-level defaults ON and renormalises the
    output back to full scale, which silently defeats `limit` (measured -0.0 dBFS).
    A dynamic normaliser would fix that but pumps for ~3s after the deliberate silence
    gap, flattening the sunset payoff. So: static gain, measured, iterated to convergence.
    """
    cur, gain = f, 0.0
    lufs0 = _lufs(f)
    if lufs0 is None:
        print("  !! could not measure loudness, leaving as-is"); shutil.copy(f, o); return o
    for i in range(1, passes + 1):
        lufs = _lufs(cur)
        if lufs is None: break
        if abs(lufs - target) <= tol:
            if cur != o: shutil.copy(cur, o)
            print(f"  loudness {lufs0:.1f} -> {lufs:.1f} LUFS  "
                  f"(static {gain:+.2f} dB, {i-1} pass{'es' if i-1 != 1 else ''})")
            return o
        step = max(-20.0, min(20.0, target - lufs)); gain += step
        tmp = os.path.join(TMP, f"norm_p{i}.mp4")
        sh(f'ffmpeg -y -v error -i "{f}" -af "volume={gain:.2f}dB,alimiter=limit=0.72:level=disabled" '
           f'-c:v copy -c:a aac -b:a 192k "{tmp}"')
        if not os.path.exists(tmp): break
        cur = tmp
    fin = _lufs(cur)
    if cur != o: shutil.copy(cur, o)
    print(f"  loudness {lufs0:.1f} -> {fin if fin is None else round(fin,1)} LUFS "
          f"(static {gain:+.2f} dB)")
    if fin is not None and abs(fin - target) > 1.0:
        print(f"  note: {fin:.1f} LUFS vs target {target} - the PEAK ceiling is binding here, "
              f"not the gain. Louder needs heavier compression, which flattens the silence "
              f"gap before the reveal. Peak gate matters more, so this is the right trade.")
    return o

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def _font():
    """Return a filtergraph-safe font path: forward slashes, escaped drive colon.
    'C:/Windows/...' must become 'C\\:/Windows/...' or ffmpeg reads C as an option."""
    for f in (FONT,
              "C:/Windows/Fonts/arialbd.ttf",
              "C:/Windows/Fonts/segoeuib.ttf",
              "C:/Windows/Fonts/seguisb.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            return f.replace("\\", "/").replace(":", "\\:")
    return None

def _dt(font, txt_file, t0, t1, size, y, colour="white", box=0.55, x="(w-tw)/2"):
    txt_file = os.path.basename(txt_file)      # bare name; ffmpeg cwd is TMP
    return (f"drawtext=fontfile='{font}':textfile='{txt_file}':"
            f"enable='between(t,{t0:.2f},{t1:.2f})':fontsize={size}:fontcolor={colour}:"
            f"box=1:boxcolor=black@{box}:boxborderw=14:x={x}:y={y}")

def phrase_cards(words, max_chars=20, max_gap=0.34):
    """Group words into caption cards, breaking at PUNCTUATION and PAUSES before length.
    Length-only splitting produced "grilled seafood, few" / "ringgit only" - readable but
    it fights the phrasing, and captions that fight the VO cost comprehension."""
    cards, cur, start = [], [], None
    for i, w in enumerate(words):
        if start is None: start = w["start"]
        cur.append(w["w"])
        txt = " ".join(cur)
        nxt = words[i+1] if i+1 < len(words) else None
        hard = w["w"].rstrip()[-1:] in ".?!"
        soft = w["w"].rstrip()[-1:] in ",;:"
        pause = bool(nxt) and (nxt["start"] - w["end"]) > max_gap
        full = len(txt) >= max_chars
        last = nxt is None
        if hard or last or pause or (soft and len(txt) >= 10) or full:
            cards.append({"text": txt, "start": start, "end": w["end"]})
            cur, start = [], None
    return cards

LOCAL_FIX = {
    "tanjong": "Tanjung", "tanjung": "Tanjung", "-aru": "Aru", "aru": "Aru",
    "ba": "bah", "ba.": "bah.", "kk": "KK", "ringgit": "ringgit",
    "filipino": "Filipino", "sabah": "Sabah", "kinabalu": "Kinabalu",
}

def fix_locals(words):
    """Whisper is trained on English and mangles Malaysian place names - it produced
    'Tanjong -Aru' and 'Ba' for 'bah'. Correct the WORD list, not the rendered text, so
    caption timings are untouched."""
    n = 0
    for w in words:
        raw = w.get("w", "")
        key = raw.lower().strip()
        if key in LOCAL_FIX and LOCAL_FIX[key] != raw:
            tail = "" if raw[-1:].isalnum() else raw[-1:]
            w["w"] = LOCAL_FIX[key] + (tail if not LOCAL_FIX[key].endswith(tail) else "")
            n += 1
        elif raw.startswith("-"):
            w["w"] = raw.lstrip("-"); n += 1
    if n: print(f"  corrected {n} local-vocabulary word(s)")
    return words

def captions(video, o, starts=None):
    """Delegates all caption design to the Caption Manager seat (tools/captionmgr.py).

    NO AI-GENERATED WATERMARK - removed at his request. Disclosure still matters, so use the
    PLATFORM toggle instead: TikTok's "AI-generated content" switch and Meta's "AI info" tag.
    Same compliance, none of the burn-in.
    """
    starts = starts or {}
    vd = dur(video)
    try:
        import captionmgr as CM
    except Exception as e:
        print("  !! captionmgr unavailable:", str(e)[:70]); shutil.copy(video, o); return o
    font = CM.font_path()
    if not font:
        print("  !! no bold font -> shipping clean"); shutil.copy(video, o); return o

    vf, idx = [], 0
    # ---- body narration: word-exact from Whisper, phrase-grouped, 'clean' style
    n_caps = 0
    try:
        import transcribe, autocut
        tr = transcribe.run(need("KK_VO.wav"))
        if tr.get("tier") != "faster-whisper":
            print("  !! whisper unavailable:", str(tr.get("error",""))[:60])
        else:
            words = fix_locals(tr["words"])
            cards = phrase_cards(words, max_chars=22)
            for c in cards: c["start"] += 1.5; c["end"] += 1.5
            items = CM.plan(cards, style="clean")
            CM.report(items)
            for it in items:
                vf += CM.drawtext(it, font, TMP, idx); idx += 1
            n_caps = len(items)
    except Exception as e:
        print("  !! caption stage:", str(e)[:80])

    # ---- HOOK, 'punch' style: big, shadowed, accent-coloured
    hook = [{"text": "3 SPOTS IN KK", "start": 0.15, "end": 2.45},
            {"text": "where locals actually go", "start": 0.55, "end": 2.45}]
    hk = CM.plan(hook[:1], style="punch")
    CM.STYLES["punch"]["y"] = 0.30
    for it in hk:
        vf += CM.drawtext(it, font, TMP, idx); idx += 1
    sub = CM.plan(hook[1:], style="clean")
    for it in sub:
        it["size"] = 34
        CM.STYLES["clean"]["y"] = 0.375
        vf += CM.drawtext(it, font, TMP, idx); idx += 1
    CM.STYLES["clean"]["y"] = 0.755          # restore for the body cards already emitted
    print("  hook 0.15-2.45s  (punch style)")

    # ---- CTA, 'list' style: the three spots, so the audio question is answerable
    cta_in = max(0.0, min(starts.get("10", vd - 5.5) - 0.6, vd - 5.0))
    rows = [("WHICH ONE FIRST?", 0.545, "punch", 46),
            ("1  Filipino Market", 0.630, "list", 34),
            ("2  The Islands",     0.685, "list", 34),
            ("3  Tanjung Aru",     0.740, "list", 34),
            ("comment 1, 2 or 3",  0.815, "clean", 28)]
    for j, (txt, yf, sty, size) in enumerate(rows):
        CM.STYLES[sty]["y"] = yf
        it = CM.plan([{"text": txt, "start": cta_in + (0 if j == 0 else 0.18 + 0.13*j),
                       "end": vd}], style=sty)[0]
        it["size"] = size
        vf += CM.drawtext(it, font, TMP, idx); idx += 1
    print(f"  CTA {cta_in:.1f}-{vd:.1f}s  (list style, three spots)")
    print("  NO AI watermark - use the platform disclosure toggle instead")

    rc, err = sh(f'ffmpeg -y -v error -i "{video}" -vf "{",".join(vf)}" -c:v libx264 -crf 20 '
                 f'-preset veryfast -pix_fmt yuv420p -c:a copy "{o}"', cwd=TMP)
    if rc == 0 and os.path.exists(o) and os.path.getsize(o) > 10000:
        print(f"  OK  burned in {n_caps} captions + hook + CTA")
        return o
    print("  !! " + "="*52)
    print("  !! TEXT RENDER FAILED - this file has NO captions and NO CTA.")
    print("  !! DO NOT POST IT.")
    print("  !! " + err.strip()[:200])
    print("  !! " + "="*52)
    shutil.copy(video, o); return o

def gate(f, starts=None, total=None):
    """Report the numbers. Where the build KNOWS a fact, use it instead of inferring:
    pacing.py detects cuts by colour-histogram distance, which cannot see a cut between two
    framings of the same source (v2 has 14 real cuts and the detector found 3). That gap is
    itself the useful signal - a cut a machine cannot detect is a cut the viewer will not
    feel - so both numbers are reported."""
    print("\n" + "="*58 + "\nGATE\n" + "="*58)
    known = sorted(starts.values())[1:] if starts else []
    try:
        import mastermind, pacing
        a_ = mastermind.audio_metrics(f)
        p = pacing.analyse(f, "vlog")
        pk = a_.get("peak"); lu = a_.get("lufs")
        cpm_known = (len(known)/(p["duration"]/60)) if p["duration"] else 0
        print(f"  duration          {p['duration']}s")
        print(f"  loudness          {lu} LUFS       band -7..-9 (your measured target)")
        print(f"  true peak         {pk} dBTP      gate <=-1.0  "
              f"{'PASS' if (pk is not None and pk <= -1.0) else 'FAIL'}")
        print(f"  cuts (known)      {len(known)}  = {cpm_known:.1f}/min   vlog band {p['target_cpm']}")
        print(f"  cuts (detected)   {p['cuts']}  = {p['cuts_per_min']}/min")
        if known and p["cuts"] < len(known) * 0.6:
            miss = len(known) - p["cuts"]
            print(f"    ^ {miss} cuts are not machine-detectable: adjacent shots share a colour")
            print(f"      histogram. Usually coverage from one source. Reads as smoother than")
            print(f"      the cut list suggests - fine for a montage, weak if you wanted punch.")
        print(f"  hook motion       {p['hook']['motion']}   gate >=0.35  "
              f"{'PASS' if p['hook']['ok'] else 'FAIL'}")
        print(f"  dead zones        {len(p['dead_zones'])}"
              + (f"  (HIGH: {sum(1 for d in p['dead_zones'] if d['severity']=='HIGH')})"
                 if p['dead_zones'] else ""))
        print(f"  est. retention    {p['retention_estimate_pct']}%   HEURISTIC from structure "
              f"only. NOT measured. Only a real 24h curve settles this.")
        for x in p["findings"][:6]: print("   -", x[:96])
    except Exception as e:
        print("  gate error:", str(e)[:100])

def main():
    print("="*54 + "\nBUILD: 3 Best Spots in Kota Kinabalu\n" + "="*54)
    if not check(): return
    os.makedirs(OUT, exist_ok=True)

    print("\n[1/5] segments"); segs = build_segments()
    if len(segs) != len(TL): print(f"!! only {len(segs)}/{len(TL)} segments built"); return

    print("\n[2/5] transitions")
    segs, starts, total = apply_transitions(segs)
    print(f"  timeline {total:.2f}s  ({len(segs)} clips)")

    print("\n[3/5] concat")
    v = concat(segs, os.path.join(TMP, "cut.mp4"))
    vd = dur(v); print(f"  {vd:.2f}s")
    if abs(vd - 30.0) > 1.5:
        print(f"  !! WARNING duration {vd:.2f}s is off the 30s target")

    reveal = starts.get(REVEAL_TAG, 16.0)
    print(f"\n[4/5] audio  (sunset reveal measured at {reveal:.2f}s)")
    durs = {t[0]: t[3] for t in TL}
    av = build_audio(v, os.path.join(TMP, "mixed.mp4"), reveal, starts, durs)
    print(f"  mixed duration {dur(av):.2f}s  (video {vd:.2f}s)")
    if abs(dur(av) - vd) > 0.3:
        print("  !! WARNING mix truncated the video")

    nv = normalise(av, os.path.join(TMP, "norm.mp4"))

    print("\n[5/5] captions")
    final = os.path.join(OUT, "KK_3SPOTS_v1.mp4")
    captions(nv, final, starts)
    gate(final, starts, total)
    print(f"\nFINAL -> {final}   {dur(final):.2f}s")

if __name__ == "__main__":
    main()
