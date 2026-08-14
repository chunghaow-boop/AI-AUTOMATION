#!/usr/bin/env python3
"""
BGMGEN — synthesise a musical bed as STEMS, arranged to the cut. No downloads, no licence.

WHY STEMS AND NOT A TRACK
  A stock loop has to be fought: it peaks where your cut doesn't, and it cannot get out of
  the way of a deliberate silence before a reveal. Stems can be arranged per section, so the
  music does what the edit needs - drop the drums for the payoff, lift for the CTA.
  And synthesised output is 100% original: no attribution, no takedown risk on a monetised
  channel. sfxgen.py's docstring says music "doesn't synthesise convincingly" - that is true
  of a vocal pop track, not of a warm instrumental bed, which is pads + plucks + bass + kit.

WHAT IT MAKES  (48kHz mono wav, per stem)
  pad     detuned saw stack through a lowpass, slow attack   - the harmonic floor
  pluck   Karplus-Strong string, pentatonic 8ths             - the movement
  bass    triangle+sine root, envelope per chord             - the weight
  drums   kick + hat + shaker on a real grid                 - the pulse
  Plus MIX previews so you can hear each arrangement without running the video build.

MUSIC
  100 BPM, 2.4s per bar. Progression I-V-vi-IV (C-G-Am-F): the warmest, most "travel" of the
  common loops. Pentatonic melody so nothing can clash.

Usage
  python3 bgmgen.py --out ../assets/bgm/generated --dur 32
  python3 bgmgen.py --preview            # also render 3 arrangement previews
"""
import argparse, os, wave
import numpy as np

SR = 48000
BPM = float(os.environ.get("TALYX_BPM", 100.0))
BEAT = 60.0 / BPM          # 0.6s
BAR  = BEAT * 4            # 2.4s

# C major: I  V  vi  IV
PROG = [("C", [261.63, 329.63, 392.00]),
        ("G", [246.94, 293.66, 392.00]),
        ("Am", [220.00, 261.63, 329.63]),
        ("F", [174.61, 261.63, 349.23])]
ROOTS = {"C": 130.81, "G": 98.00, "Am": 110.00, "F": 87.31}
PENTA = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25]

def wr(path, x, sr=SR):
    x = np.nan_to_num(x)
    n = min(len(x), int(sr * 0.008))
    if n > 0:
        x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    pk = float(np.max(np.abs(x))) or 1.0
    x = x / pk * 0.82
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "w") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((x * 32767).astype(np.int16).tobytes())
    return path

def lp(x, cut, sr=SR):
    """One-pole lowpass, applied twice for a steeper slope."""
    a = np.exp(-2 * np.pi * cut / sr)
    y = np.empty_like(x); acc = 0.0
    for _ in range(2):
        for i, v in enumerate(x):
            acc = a * acc + (1 - a) * v; y[i] = acc
        x = y.copy(); acc = 0.0
    return y

def lp_fast(x, cut, sr=SR):
    """FFT brickwall-ish lowpass with a soft knee - much faster than the sample loop."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/sr)
    X *= 1.0 / (1.0 + (f / max(cut, 1.0))**4)
    return np.fft.irfft(X, len(x))

def hp_fast(x, cut, sr=SR):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/sr)
    with np.errstate(divide="ignore", invalid="ignore"):
        g = 1.0 / (1.0 + (max(cut, 1.0) / np.maximum(f, 1e-9))**4)
    return np.fft.irfft(X * np.nan_to_num(g), len(x))

def saw(freq, n, sr=SR, harm=14):
    """Additive saw - band-limited, so no aliasing buzz."""
    t = np.arange(n) / sr; out = np.zeros(n)
    for h in range(1, harm + 1):
        if freq * h > sr / 2.2: break
        out += np.sin(2*np.pi*freq*h*t) / h
    return out * (2/np.pi)

def adsr(n, a=0.01, d=0.1, s=0.7, r=0.3, sr=SR):
    a_n, d_n, r_n = int(a*sr), int(d*sr), int(r*sr)
    s_n = max(0, n - a_n - d_n - r_n)
    return np.concatenate([np.linspace(0, 1, a_n),
                           np.linspace(1, s, d_n),
                           np.full(s_n, s),
                           np.linspace(s, 0, r_n)])[:n]

# ---------------------------------------------------------------- stems
def stem_pad(dur):
    """Detuned saw stack per chord, lowpassed. The harmonic floor.
    Only 4 unique bars exist, so each is rendered once and tiled - 14x faster."""
    n = int(dur*SR); out = np.zeros(n); bar_n = int(BAR*SR)
    cache = {}
    for name, notes in PROG:
        seg = np.zeros(bar_n)
        for f0 in notes:
            for det in (-6.0, 0.0, +6.0):        # cents-ish detune = width
                seg += saw(f0*(1+det/1200.0), bar_n, harm=5) * 0.33
        cache[name] = seg * adsr(bar_n, a=0.35, d=0.4, s=0.85, r=0.5)
    for b in range(int(np.ceil(dur/BAR))):
        name, _ = PROG[b % len(PROG)]
        s0 = b*bar_n; e = min(n, s0+bar_n)
        if s0 >= n: break
        out[s0:e] += cache[name][:e-s0]
    out = lp_fast(out, 2200)
    # gentle chorus for width
    d = int(0.018*SR)
    out[d:] += out[:-d] * 0.35
    return out / (np.max(np.abs(out)) or 1)

def stem_pluck(dur, seed=7):
    """Plucked-string tone on 8ths, pentatonic so it cannot clash.

    NOT Karplus-Strong: that needs a per-sample Python loop (~2.1M iterations for this
    arrangement) and made synthesis miss the sandbox time budget every run. A harmonic stack
    with per-partial decay is vectorised, ~50x faster, and indistinguishable in a bed.
    The 8-step pattern repeats every bar, so one bar is rendered and tiled.
    """
    rng = np.random.default_rng(seed)
    bar_n = int(BAR*SR); n = int(dur*SR)
    bar = np.zeros(bar_n + int(1.2*SR))
    step = BEAT/2
    pattern = [0, 2, 4, 2, 5, 4, 2, 0]
    for i in range(8):
        if i % 8 in (3, 6):          # gaps: a busy arp reads as a ringtone
            continue
        f0 = PENTA[pattern[i] % len(PENTA)]
        s0 = int(i*step*SR); ln = int(1.0*SR)
        t = np.arange(ln)/SR
        seg = np.zeros(ln)
        for h, amp in ((1, 1.0), (2, 0.45), (3, 0.22), (4, 0.12), (5, 0.07)):
            if f0*h > SR/2.2: break
            seg += amp*np.sin(2*np.pi*f0*h*t)*np.exp(-t*(3.0 + 1.1*h))
        seg += rng.normal(0, 0.05, ln)*np.exp(-t*90)      # pick transient
        bar[s0:s0+ln] += seg*0.5
    out = np.zeros(n)
    for b in range(int(np.ceil(dur/BAR))):
        s0 = b*bar_n
        if s0 >= n: break
        e = min(n, s0+len(bar))
        out[s0:e] += bar[:e-s0]
    out = lp_fast(out, 9000)
    return out / (np.max(np.abs(out)) or 1)

def stem_marimba(dur, seed=23):
    """Wooden mallet tone. THIS is what makes a bed read as tropical/organic rather than
    electronic - his note was "the bgm doesnt really match with the video feeling", and the
    cause was timbre: a detuned-saw pad sounds like a synth, not like somewhere warm.

    A marimba is a struck bar: near-sinusoidal partials at INHARMONIC ratios (1, 3.9, 9.2)
    with a fast attack and a short woody decay. Not a sawtooth.
    """
    rng = np.random.default_rng(seed)
    bar_n = int(BAR*SR); n = int(dur*SR)
    bar = np.zeros(bar_n + int(1.4*SR))
    step = BEAT/2
    pattern = [0, 4, 2, 5, 7, 4, 2, 5]
    for i in range(8):
        if i % 8 == 5: continue
        f0 = PENTA[pattern[i] % len(PENTA)] * (2 if i % 4 == 0 else 1)
        s0 = int(i*step*SR); ln = int(0.9*SR)
        t = np.arange(ln)/SR
        seg = np.zeros(ln)
        for ratio, amp, dec in ((1.0, 1.0, 6.0), (3.9, 0.30, 11.0), (9.2, 0.10, 18.0)):
            f = f0*ratio
            if f > SR/2.2: break
            seg += amp*np.sin(2*np.pi*f*t)*np.exp(-t*dec)
        seg += rng.normal(0, 0.04, ln)*np.exp(-t*160)      # mallet strike
        bar[s0:s0+ln] += seg*0.55
    out = np.zeros(n)
    for b in range(int(np.ceil(dur/BAR))):
        s0 = b*bar_n
        if s0 >= n: break
        e = min(n, s0+len(bar)); out[s0:e] += bar[:e-s0]
    return lp_fast(out, 7000) / (np.max(np.abs(out)) or 1)

def stem_hand(dur, seed=29):
    """Hand percussion - conga, shaker, rim. Replaces the kick/hat pattern, which reads as
    house music and fought the footage."""
    rng = np.random.default_rng(seed)
    n = int(dur*SR); out = np.zeros(n)
    def place(x, at):
        s0 = int(at*SR); e = min(n, s0+len(x))
        if s0 < n: out[s0:e] += x[:e-s0]
    def conga(hi=True):
        L = int(0.20*SR); t = np.arange(L)/SR
        f = (285 if hi else 165)*np.exp(-t*7) + (150 if hi else 92)
        return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*13)*0.75
                + hp_fast(rng.uniform(-1,1,L), 2600)*np.exp(-t*60)*0.16)
    def shaker():
        L = int(0.075*SR)
        return hp_fast(rng.uniform(-1,1,L), 4800)*np.exp(-np.linspace(0,8,L))*0.20
    def rim():
        L = int(0.05*SR); t = np.arange(L)/SR
        return np.sin(2*np.pi*1750*t)*np.exp(-t*70)*0.16
    for i in range(int(dur/BEAT)):
        tb = i*BEAT
        if i % 4 == 0: place(conga(False), tb)
        if i % 4 == 2: place(conga(True), tb)
        place(shaker(), tb + BEAT/2)
        place(shaker(), tb + BEAT*0.75)
        if i % 8 == 6: place(rim(), tb + BEAT/2)
    return out / (np.max(np.abs(out)) or 1)

def stem_bass(dur):
    n = int(dur*SR); out = np.zeros(n); bar_n = int(BAR*SR)
    for b in range(int(np.ceil(dur/BAR))):
        name, _ = PROG[b % len(PROG)]
        f = ROOTS[name]
        for beat in (0, 2):                     # root on 1 and 3
            s = int(b*bar_n + beat*BEAT*SR)
            ln = min(int(BEAT*1.6*SR), n-s)
            if s >= n or ln <= 0: continue
            t = np.arange(ln)/SR
            seg = (np.sin(2*np.pi*f*t)*0.75 +
                   0.25*np.sign(np.sin(2*np.pi*f*t)))
            seg *= adsr(ln, a=0.006, d=0.15, s=0.55, r=0.35)
            out[s:s+ln] += seg
    out = hp_fast(lp_fast(out, 300), 38)      # tame the sub: 55% was far too much
    return out / (np.max(np.abs(out)) or 1)

def stem_drums(dur, seed=3):
    rng = np.random.default_rng(seed)
    n = int(dur*SR); out = np.zeros(n)
    def place(x, at):
        s = int(at*SR); e = min(n, s+len(x))
        if s < n: out[s:e] += x[:e-s]
    def kick():
        L = int(0.30*SR); t = np.arange(L)/SR
        f = 115*np.exp(-t*22) + 46
        return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9) * 0.95
    def hat(open_=False):
        L = int((0.14 if open_ else 0.045)*SR)
        return hp_fast(rng.uniform(-1,1,L), 7500) * np.exp(-np.linspace(0,(5 if open_ else 14),L)) * 0.24
    def shaker():
        L = int(0.07*SR)
        return hp_fast(rng.uniform(-1,1,L), 5200) * np.exp(-np.linspace(0,9,L)) * 0.13
    beats = int(dur/BEAT)
    for i in range(beats):
        tb = i*BEAT
        if i % 4 in (0, 2): place(kick(), tb)
        place(hat(open_=(i % 4 == 3)), tb)
        place(shaker(), tb + BEAT/2)
        if i % 8 == 7: place(shaker(), tb + BEAT*0.75)
    return out / (np.max(np.abs(out)) or 1)

def stem_shimmer(dur, seed=11):
    """High bell/air layer. The mix measured 0.0% above 6kHz without this - which reads as
    dull under bright footage. His target from file 19 is ~4% air."""
    rng = np.random.default_rng(seed)
    n = int(dur*SR); out = np.zeros(n); step = BEAT
    for i in range(int(dur/step)):
        if i % 4 != 0: continue
        f = PENTA[(i//4) % len(PENTA)] * 8          # three octaves = true bell/air register
        s0 = int(i*step*SR); ln = min(int(1.8*SR), n-s0)
        if s0 >= n or ln <= 0: continue
        t = np.arange(ln)/SR
        seg = (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*2.01*t)
               + 0.25*np.sin(2*np.pi*f*3.02*t))
        out[s0:s0+ln] += seg * np.exp(-np.linspace(0, 4.5, ln)) * 0.4
    out += hp_fast(rng.uniform(-1,1,n), 10500) * 0.10      # this IS the "air" band
    return out / (np.max(np.abs(out)) or 1)

STEMS = {"pad": stem_pad, "shimmer": stem_shimmer, "marimba": stem_marimba,
         "hand": stem_hand, "pluck": stem_pluck, "bass": stem_bass, "drums": stem_drums}

# ---------------------------------------------------------------- arrangement
BANDS = [(20,150,"sub"), (150,1500,"body"), (1500,6000,"presence"),
         (6000,10000,"high"), (10000,20000,"air")]
# Targets from file 19 - MEASURED off a real viral reel, not generic guidance.
TARGET = {"sub": 16.0, "body": 45.0, "presence": 26.0, "high": 9.0, "air": 4.0}

def band_split(x, sr=SR):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1/sr); P = X**2; tot = P.sum() or 1.0
    return {lab: 100.0*P[(f>=lo)&(f<hi)].sum()/tot for lo, hi, lab in BANDS}

def match_spectrum(x, sr=SR, iters=4, verbose=False):
    """Iteratively apply per-band gain until the split matches TARGET. Reports each pass so
    the result is evidence, not an assertion."""
    for k in range(iters):
        cur = band_split(x, sr)
        err = max(abs(cur[b] - TARGET[b]) for b in TARGET)
        if verbose:
            print("   pass %d  " % k + " ".join(f"{b} {cur[b]:.1f}%" for b in TARGET))
        if err < 2.5:
            break
        X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/sr); g = np.ones(len(f))
        for lo, hi, lab in BANDS:
            want, got = TARGET[lab], max(cur[lab], 1e-3)
            # amplitude gain = sqrt(power ratio), damped so it converges instead of ringing
            gain = (want/got) ** 0.25
            g[(f >= lo) & (f < hi)] *= np.clip(gain, 0.25, 6.0)
        # smooth the gain curve so band edges do not become audible steps
        # smooth on a decimated curve then interpolate back: same result, ~200x cheaper
        idx = np.linspace(0, len(g)-1, 2048).astype(int)
        gs = np.convolve(g[idx], np.ones(9)/9, mode="same")
        g = np.interp(np.arange(len(g)), idx, gs)
        x = np.fft.irfft(X * g, len(x))
        pk = float(np.max(np.abs(x))) or 1.0
        x = x / pk * 0.85
    return x

def arrange(stems, dur, sections):
    """sections: list of (t0, t1, {stem: gain}). Ramps 250ms between sections so a stem
    entering or leaving never clicks."""
    n = int(dur*SR); out = np.zeros(n)
    for name, x in stems.items():
        gain = np.zeros(n)
        for t0, t1, mix in sections:
            g = mix.get(name, 0.0)
            s, e = int(t0*SR), min(n, int(t1*SR))
            if s >= n: continue
            gain[s:e] = g
        # smooth the gain curve
        k = int(0.25*SR)
        gain = np.convolve(gain, np.ones(k)/k, mode="same")
        L = min(len(x), n)
        out[:L] += x[:L] * gain[:L]
    out = hp_fast(out, 32)                 # nothing useful below 32Hz on a phone
    pk = float(np.max(np.abs(out))) or 1.0
    return out / pk * 0.85

def sunset_warm(dur, reveal=16.2, cta=25.8):
    """Warm and organic. Marimba carries the movement, hand percussion instead of a kit,
    pad soft underneath. Drums-equivalent drops out entirely for the payoff."""
    return [
        (0.0,    2.6,    {"pad":0.50,"marimba":0.40,"bass":0.24,"hand":0.16,"shimmer":0.22}),
        (2.6,    reveal, {"pad":0.38,"marimba":0.62,"bass":0.44,"hand":0.50,"shimmer":0.26}),
        (reveal, cta,    {"pad":0.78,"marimba":0.30,"bass":0.30,"hand":0.00,"shimmer":0.48}),
        (cta,    dur,    {"pad":0.60,"marimba":0.52,"bass":0.40,"hand":0.34,"shimmer":0.38}),
    ]

def travel_bright(dur, reveal=16.2, cta=25.8):
    """More energy end to end - marimba plus pluck, percussion never fully out."""
    return [
        (0.0,    2.6,    {"pad":0.44,"marimba":0.46,"pluck":0.22,"bass":0.28,"hand":0.26,"shimmer":0.28}),
        (2.6,    reveal, {"pad":0.32,"marimba":0.58,"pluck":0.42,"bass":0.48,"hand":0.60,"shimmer":0.32}),
        (reveal, cta,    {"pad":0.70,"marimba":0.40,"pluck":0.18,"bass":0.34,"hand":0.20,"shimmer":0.52}),
        (cta,    dur,    {"pad":0.52,"marimba":0.56,"pluck":0.40,"bass":0.44,"hand":0.46,"shimmer":0.40}),
    ]

def auto_hero(dur, reveal=6.67, cta=12.67):
    """15s automotive cinematic. Pad-led, marimba almost absent (too warm/tropical for a car
    film), hand percussion sparse. Everything except the pad drops out at the reveal so the
    lightbar ignition lands in space."""
    return [
        (0.0,    2.0,    {"pad":0.62,"bass":0.30,"shimmer":0.34,"hand":0.10}),
        (2.0,    reveal, {"pad":0.55,"bass":0.58,"shimmer":0.30,"hand":0.42,"marimba":0.14}),
        (reveal, reveal+1.4, {"pad":0.30,"bass":0.10,"shimmer":0.20}),   # the gap
        (reveal+1.4, cta, {"pad":0.72,"bass":0.62,"shimmer":0.46,"hand":0.30}),
        (cta,    dur,    {"pad":0.66,"bass":0.48,"shimmer":0.52,"hand":0.18}),
    ]

def lofi_chill(dur, reveal=16.2, cta=25.8):
    """Mellow. Pad-led, sparse marimba, almost no percussion - for a slower travel edit."""
    return [
        (0.0,    reveal, {"pad":0.70,"marimba":0.30,"bass":0.34,"hand":0.12,"shimmer":0.24}),
        (reveal, cta,    {"pad":0.85,"marimba":0.20,"bass":0.26,"hand":0.00,"shimmer":0.44}),
        (cta,    dur,    {"pad":0.72,"marimba":0.38,"bass":0.34,"hand":0.22,"shimmer":0.34}),
    ]

def travel_arrangement(dur, reveal=16.2, cta=25.8):
    """Written for THIS video: energy through the three spots, drums OUT for the sunset
    payoff so the reveal lands in space, then a lift into the CTA."""
    return [
        (0.0,     2.6,    {"pad": 0.55, "pluck": 0.20, "bass": 0.26, "drums": 0.10, "shimmer": 0.30}),
        (2.6,     reveal, {"pad": 0.45, "pluck": 0.55, "bass": 0.48, "drums": 0.62, "shimmer": 0.34}),
        (reveal,  cta,    {"pad": 0.80, "pluck": 0.22, "bass": 0.32, "drums": 0.00, "shimmer": 0.55}),
        (cta,     dur,    {"pad": 0.65, "pluck": 0.45, "bass": 0.42, "drums": 0.48, "shimmer": 0.42}),
    ]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "..", "assets", "bgm", "generated"))
    ap.add_argument("--dur", type=float, default=34.0)
    ap.add_argument("--reveal", type=float, default=16.2)
    ap.add_argument("--cta", type=float, default=25.8)
    ap.add_argument("--force", action="store_true", help="re-synthesise stems")
    ap.add_argument("--all-mixes", action="store_true", help="also render alt mixes")
    a = ap.parse_args()
    out = os.path.abspath(a.out); os.makedirs(out, exist_ok=True)

    print(f"BGMGEN  {BPM:.0f} BPM · bar {BAR:.1f}s · C-G-Am-F · {a.dur:.0f}s")
    def rd(path):
        with wave.open(path) as f:
            if abs(f.getnframes()/f.getframerate() - a.dur) > 0.2: return None
            return np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(float)/32768

    stems = {}
    for name, fn in STEMS.items():
        cache = os.path.join(out, f"STEM_{name}.wav")
        got = None
        if os.path.exists(cache) and not a.force:
            try: got = rd(cache)
            except Exception: got = None
        if got is not None:
            print(f"  cached {name}", flush=True); stems[name] = got
        else:
            print(f"  synth {name} ...", flush=True)
            stems[name] = fn(a.dur)
            wr(cache, stems[name].copy())

    mixes = {
        "sunset_warm":  sunset_warm(a.dur, a.reveal, a.cta),
        "travel_bright": travel_bright(a.dur, a.reveal, a.cta),
        "lofi_chill":   lofi_chill(a.dur, a.reveal, a.cta),
        "auto_hero":    auto_hero(a.dur, a.reveal, a.cta),
    }
    if a.all_mixes:
        mixes["full_loop"] = [(0.0, a.dur, {"pad":0.5,"pluck":0.5,"bass":0.45,"drums":0.58,"shimmer":0.35})]
        mixes["no_drums"]  = [(0.0, a.dur, {"pad":0.7,"pluck":0.45,"bass":0.5,"shimmer":0.4})]
    for name, sec in mixes.items():
        mix = arrange(stems, a.dur, sec)
        print(f"  matching spectrum: {name}")
        mix = match_spectrum(mix)
        fin = band_split(mix)
        p = wr(os.path.join(out, f"BGM_{name}.wav"), mix)
        print(f"  wrote {os.path.basename(p)}  " +
              " ".join(f"{b} {fin[b]:.1f}%" for b in TARGET))
    print(f"\nOK -> {out}")

if __name__ == "__main__":
    main()
