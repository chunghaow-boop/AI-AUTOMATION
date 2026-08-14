#!/usr/bin/env python3
"""
FOLEY — diegetic sound effects tied to what is ON SCREEN, synthesised from scratch.

WHY THIS EXISTS (his review, verbatim)
  "there are no sound effects, for example the fishes in the sea, you can add on bubbles
   sound effects, and the walking at the night market, can add on crowded night market sfx,
   and when the boat splashes the water, can add a splash water sfx"

  He is right and the distinction matters. v2 had only TRANSITION sfx - whooshes on cuts, a
  sub-drop on the reveal. Those decorate the EDIT. They say nothing about the WORLD. A reef
  with no bubbles and a night market with no crowd read as stock footage with music over it,
  which is exactly the "not seamless" feeling he described.

  Transition SFX  = punctuation for the cut      (sfxgen.py already covers this)
  Diegetic SFX    = evidence the place is real   (this file)

EVERYTHING IS SYNTHESISED
  Same reasoning as sfxgen.py and bgmgen.py: the sandbox cannot reach freesound/pixabay, and
  synthesised output carries no attribution or takedown risk on a monetised channel. Ambience
  and foley are noise + filters + envelopes, which is how they are built commercially anyway.

BEDS (continuous, per shot)     HITS (one-shots, on an action)
  reef      bubbles + water     splash      boat hitting water
  market    crowd murmur        bubble_pop  a single close bubble
  grill     sizzle + crackle    footstep    on wet sand
  waves     surf swells         sizzle_hit  meat hitting the grill
  wind      open beach air      gull        a distant bird
  boat      engine + wake

Usage
  python3 foley.py --demo out/          # render one of everything to audition
  python3 foley.py --list
"""
import argparse, os, wave
import numpy as np

SR = 48000

# ---------------------------------------------------------------- helpers
def wr(path, x, sr=SR, peak=0.8):
    x = np.nan_to_num(x)
    n = min(len(x), int(sr*0.006))
    if n > 0:
        x[:n] *= np.linspace(0,1,n); x[-n:] *= np.linspace(1,0,n)
    pk = float(np.max(np.abs(x))) or 1.0
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with wave.open(path,"w") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((x/pk*peak*32767).astype(np.int16).tobytes())
    return path

def _n(dur, rng): return rng.uniform(-1, 1, int(dur*SR))
def _ns(n, rng):  return rng.uniform(-1, 1, int(n))     # exact sample count

def bp(x, lo, hi, sr=SR):
    """Band-pass via FFT. Soft knees so it never sounds like a resonant filter sweep."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/sr)
    g = 1.0/(1.0+(f/max(hi,1))**4)
    with np.errstate(divide="ignore", invalid="ignore"):
        g *= 1.0/(1.0+(max(lo,1)/np.maximum(f,1e-9))**4)
    return np.fft.irfft(X*np.nan_to_num(g), len(x))

def lp(x, cut, sr=SR):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/sr)
    return np.fft.irfft(X*(1.0/(1.0+(f/max(cut,1))**4)), len(x))

def env(n, a=0.01, r=0.3):
    a_n = max(1, int(a*SR)); r_n = max(1, int(r*SR)); s = max(0, n-a_n-r_n)
    return np.concatenate([np.linspace(0,1,a_n), np.ones(s), np.linspace(1,0,r_n)])[:n]

# ---------------------------------------------------------------- HITS
def bubble_pop(rng, f0=None):
    """A bubble is a rising sine whose pitch climbs as it detaches. That upward chirp is
    the whole recognisable character - noise alone does not read as 'bubble'."""
    d = rng.uniform(0.05, 0.16); n = int(d*SR); t = np.arange(n)/SR
    f0 = f0 or rng.uniform(420, 1500)
    f = f0*(1 + 2.4*(t/d)**1.6)
    x = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/(d*0.42))
    x += 0.10*bp(_n(d, rng), 900, 5000)*np.exp(-t/(d*0.16))
    return x*0.7

def splash(rng, size=1.0):
    """Impact + spray + droplets. The droplet tail is what makes it read as water rather
    than a generic noise burst."""
    d = 0.55*size; n = int(d*SR); t = np.arange(n)/SR
    core = bp(_n(d, rng), 220, 4200) * np.exp(-t*9/size)
    spray = bp(_n(d, rng), 3500, 12000) * np.exp(-t*15) * 0.5
    low = np.sin(2*np.pi*95*t)*np.exp(-t*17)*0.35
    x = core + spray + low
    for _ in range(int(9*size)):                       # droplets falling back
        at = rng.uniform(0.10, d*0.95); L = int(0.035*SR); s0 = int(at*SR)
        if s0+L < n:
            tt = np.arange(L)/SR
            x[s0:s0+L] += np.sin(2*np.pi*rng.uniform(1400,4200)*tt)*np.exp(-tt*95)*0.22
    return x*0.85

def footstep(rng, wet=True):
    d = 0.16; n = int(d*SR); t = np.arange(n)/SR
    body = lp(_n(d, rng), 700)*np.exp(-t*26)
    grit = bp(_n(d, rng), 2200, 9000)*np.exp(-t*34)*(0.5 if wet else 0.32)
    return (body + grit)*0.55

def sizzle_hit(rng):
    d = 0.5; n = int(d*SR); t = np.arange(n)/SR
    return (bp(_n(d, rng), 2600, 11000)*np.exp(-t*5.5)*0.7
            + bp(_n(d, rng), 500, 1800)*np.exp(-t*13)*0.3)

def gull(rng):
    d = 0.42; n = int(d*SR); t = np.arange(n)/SR
    f = 1250*(1 + 0.55*np.sin(2*np.pi*7*t)) * np.exp(-t*0.7)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n, 0.03, 0.25)*0.30

HITS = {"bubble_pop": bubble_pop, "splash": splash, "footstep": footstep,
        "sizzle_hit": sizzle_hit, "gull": gull}

# ---------------------------------------------------------------- BEDS
def bed_reef(dur, rng):
    """Underwater: a filtered low hiss with slow pressure swells, plus scattered bubbles."""
    n = int(dur*SR); t = np.arange(n)/SR
    base = lp(_n(dur, rng), 900) * (0.32 + 0.13*np.sin(2*np.pi*0.11*t))
    x = base*0.5
    k = 0.0
    while k < dur:                                     # bubbles at irregular intervals
        b = bubble_pop(rng); s0 = int(k*SR)
        e = min(n, s0+len(b))
        if s0 < n: x[s0:e] += b[:e-s0]*rng.uniform(0.22, 0.55)
        k += rng.uniform(0.16, 0.62)
    return x

def bed_market(dur, rng):
    """Crowd murmur: many band-limited noise voices at different rates. Speech-shaped
    (200-2500Hz) with slow amplitude wander, plus occasional nearby chatter peaks."""
    n = int(dur*SR); t = np.arange(n)/SR
    x = np.zeros(n)
    for f_lo, f_hi, g, rate in ((200,900,0.5,0.7),(600,1800,0.38,1.3),(1200,2800,0.22,2.1)):
        v = bp(_n(dur, rng), f_lo, f_hi)
        v *= 0.6 + 0.4*np.sin(2*np.pi*rate*t + rng.uniform(0,6))
        x += v*g
    for _ in range(int(dur*3.5)):                      # a voice passing close
        at = rng.uniform(0, max(0.01, dur-0.5)); L = int(rng.uniform(0.18,0.45)*SR)
        s0 = int(at*SR)
        if s0+L < n:
            tt = np.arange(L)/SR
            x[s0:s0+L] += bp(_ns(L, rng), 350, 2200)*env(L,0.05,0.2)*rng.uniform(0.2,0.45)
    for _ in range(int(dur*1.2)):                      # cutlery / metal clinks
        at = rng.uniform(0, max(0.01, dur-0.2)); L = int(0.09*SR); s0 = int(at*SR)
        if s0+L < n:
            tt = np.arange(L)/SR
            x[s0:s0+L] += np.sin(2*np.pi*rng.uniform(2600,5200)*tt)*np.exp(-tt*30)*0.13
    return x*0.55

def bed_grill(dur, rng):
    n = int(dur*SR); t = np.arange(n)/SR
    hiss = bp(_n(dur, rng), 2400, 12000)*(0.42+0.18*np.sin(2*np.pi*0.7*t))
    x = hiss*0.55
    for _ in range(int(dur*22)):                       # fat spitting
        at = rng.uniform(0, max(0.01,dur-0.05)); L = int(0.03*SR); s0 = int(at*SR)
        if s0+L < n:
            tt = np.arange(L)/SR
            x[s0:s0+L] += bp(_ns(L, rng), 3000, 13000)*np.exp(-tt*140)*rng.uniform(.2,.6)
    return x

def bed_waves(dur, rng):
    """Surf: broadband noise shaped into swells that break. Period ~5s so two 30s shots
    never sound like the same loop."""
    n = int(dur*SR); t = np.arange(n)/SR
    swell = 0.45 + 0.55*(0.5+0.5*np.sin(2*np.pi*0.19*t - 1.1))**2.2
    x = bp(_n(dur, rng), 120, 6500)*swell
    for _ in range(max(1,int(dur/5.0))):               # a wave breaking
        at = rng.uniform(0, max(0.01,dur-1.2)); L = int(1.0*SR); s0 = int(at*SR)
        if s0+L < n:
            tt = np.arange(L)/SR
            x[s0:s0+L] += bp(_ns(L, rng), 500, 9000)*np.exp(-tt*3.2)*0.4
    return x*0.6

def bed_wind(dur, rng):
    n = int(dur*SR); t = np.arange(n)/SR
    return lp(_n(dur, rng), 1100)*(0.35+0.25*np.sin(2*np.pi*0.13*t))*0.5

def bed_boat(dur, rng):
    """Outboard engine: a low fundamental with harmonics, plus hull wake hiss."""
    n = int(dur*SR); t = np.arange(n)/SR
    f0 = 46.0
    eng = sum(np.sin(2*np.pi*f0*h*t)/h for h in (1,2,3,4,5))
    eng *= 0.35 + 0.10*np.sin(2*np.pi*0.6*t)
    wake = bp(_n(dur, rng), 700, 7000)*0.30
    return (lp(eng, 420)*0.55 + wake)*0.7

BEDS = {"reef": bed_reef, "market": bed_market, "grill": bed_grill,
        "waves": bed_waves, "wind": bed_wind, "boat": bed_boat}

# ---------------------------------------------------------------- per-shot mapping
# The point of this table: sound is chosen from WHAT IS ON SCREEN, not from the edit.
# gain is relative; the mix ducks all of it under the VO.
SHOT_FOLEY = {
    "01":  {"bed": ("waves", 0.34), "hits": [("footstep", 0.35, 0.30),
                                             ("footstep", 1.05, 0.30),
                                             ("footstep", 1.80, 0.28)]},
    "02":  {"bed": ("market", 0.52), "hits": [("footstep", 0.40, 0.20)]},
    "03":  {"bed": ("grill", 0.50), "hits": [("sizzle_hit", 0.15, 0.45)]},
    "03b": {"bed": ("grill", 0.58), "hits": [("sizzle_hit", 0.10, 0.55)]},
    "04":  {"bed": ("market", 0.40), "hits": [("sizzle_hit", 0.20, 0.25)]},
    "05":  {"bed": ("boat", 0.46), "hits": [("splash", 0.25, 0.60),
                                            ("splash", 1.10, 0.42)]},
    "06":  {"bed": ("reef", 0.55), "hits": [("bubble_pop", 0.30, 0.55),
                                            ("bubble_pop", 1.15, 0.45),
                                            ("bubble_pop", 2.00, 0.50)]},
    "07":  {"bed": ("waves", 0.44), "hits": [("gull", 0.60, 0.30)]},
    "07b": {"bed": ("waves", 0.44), "hits": []},
    "08":  {"bed": ("waves", 0.40), "hits": []},
    "08b": {"bed": ("waves", 0.36), "hits": [("gull", 0.50, 0.22)]},
    "09":  {"bed": ("waves", 0.34), "hits": []},
    "10":  {"bed": ("waves", 0.34), "hits": [("footstep", 0.50, 0.22)]},
    "10b": {"bed": ("waves", 0.30), "hits": []},
}

def render_track(starts, durations, total, out, seed=17, xfade=0.28, quiet=False):
    """Build ONE continuous foley track for the whole timeline.

    Beds CROSS-FADE across cuts rather than switching hard. That is what he meant by
    "the linkage are so seamless": if ambience cuts dead on every edit, the edit is audible.
    A bed that bleeds across the cut hides it.
    """
    rng = np.random.default_rng(seed)
    n = int(total*SR) + SR
    track = np.zeros(n)
    placed = []
    for tag, t0 in sorted(starts.items(), key=lambda kv: kv[1]):
        spec = SHOT_FOLEY.get(tag)
        if not spec: continue
        d = durations.get(tag, 2.0)
        name, g = spec["bed"]
        # render longer than the shot so it can fade across both cuts
        blen = d + xfade*2
        bedx = BEDS[name](blen, rng)*g
        f = int(xfade*SR)
        if len(bedx) > 2*f:
            bedx[:f] *= np.linspace(0,1,f); bedx[-f:] *= np.linspace(1,0,f)
        s0 = max(0, int((t0-xfade)*SR)); e = min(n, s0+len(bedx))
        track[s0:e] += bedx[:e-s0]
        placed.append(f"{tag}:{name}")
        for hname, rel, hg in spec["hits"]:
            h = HITS[hname](rng)*hg
            hs = int((t0+rel)*SR); he = min(n, hs+len(h))
            if hs < n: track[hs:he] += h[:he-hs]
            placed.append(f"{tag}:{hname}@{t0+rel:.1f}")
    track = track[:int(total*SR)]
    pk = float(np.max(np.abs(track))) or 1.0
    track = track/pk*0.72
    wr(out, track)
    if not quiet:
        print(f"  foley: {len(placed)} elements, beds cross-faded {xfade*1000:.0f}ms across cuts")
        print("   " + "  ".join(placed[:10]) + (" ..." if len(placed) > 10 else ""))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", help="render one of every sound to this folder")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        print("BEDS:", ", ".join(BEDS)); print("HITS:", ", ".join(HITS)); return
    if a.demo:
        rng = np.random.default_rng(3)
        for k, fn in BEDS.items():
            wr(os.path.join(a.demo, f"BED_{k}.wav"), fn(4.0, rng)); print(f"  BED_{k}.wav")
        for k, fn in HITS.items():
            wr(os.path.join(a.demo, f"HIT_{k}.wav"), fn(rng)); print(f"  HIT_{k}.wav")

if __name__ == "__main__":
    main()
