#!/usr/bin/env python3
"""
PHONK — drift phonk bed for car edits. Built from researched specs, not from my priors.

WHY THIS FILE EXISTS
  For the Crown build I invented a 90 BPM marimba-and-warm-pad bed by REASONING that
  "automotive hero is weighty". I never checked. The actual genre for car edits is
  drift phonk, and my bed was wrong on every axis that matters:

      axis          drift phonk            what I made
      BPM           140-170                90
      signature     TR-808 cowbell         marimba
      bass          distorted, sliding     clean sine sub
      aesthetic     saturation/bitcrush    clean and warm

  Researched specs (saved in work/knowledge.json under 'car cinematic'):
    - drift phonk 140-170 BPM, most sit 140-160; Memphis phonk 130-150
    - the TR-808 COWBELL is the single most recognisable signature, not optional
    - 808 bass is distorted and PITCH-SLIDING - mid-range growl, not clean sub
    - saturation, bitcrush and tape distortion ARE the aesthetic, not defects

SYNTHESIS NOTES
  808 cowbell is famously two square waves at ~540Hz and ~800Hz through a band-pass with a
  fast decay. That interval is what makes it read as "cowbell" rather than "beep".
  808 bass is a sine with a fast downward pitch envelope, then driven into saturation so the
  harmonics land in the mids where a phone speaker can actually reproduce them.

Usage
  python3 phonk.py --out ../assets/bgm/generated --bpm 145 --dur 16
"""
import argparse, os, wave
import numpy as np

SR = 48000

def wr(path, x, sr=SR, peak=0.89):
    x = np.nan_to_num(x)
    n = min(len(x), int(sr*0.005))
    if n > 0: x[:n] *= np.linspace(0,1,n); x[-n:] *= np.linspace(1,0,n)
    pk = float(np.max(np.abs(x))) or 1.0
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with wave.open(path,"w") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((x/pk*peak*32767).astype(np.int16).tobytes())
    return path

def bp(x, lo, hi, sr=SR):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/sr)
    g=1.0/(1.0+(f/max(hi,1))**4)
    with np.errstate(divide="ignore",invalid="ignore"):
        g*=1.0/(1.0+(max(lo,1)/np.maximum(f,1e-9))**4)
    return np.fft.irfft(X*np.nan_to_num(g), len(x))

def sat(x, drive=3.5):
    """Saturation IS the genre. tanh drive pushes harmonics into the mids where a phone
    speaker can reproduce them - a clean sub is inaudible on the device this plays on."""
    return np.tanh(x*drive)/np.tanh(drive)

def bitcrush(x, bits=7):
    q = 2**bits
    return np.round(x*q)/q

# ---------------------------------------------------------------- voices
def cowbell(dur=0.16, f1=540.0, f2=800.0):
    """TR-808 cowbell: two squares a specific interval apart, band-passed, fast decay.
    The 540/800 Hz pair is what makes it read as 'cowbell' and not 'beep'."""
    n=int(dur*SR); t=np.arange(n)/SR
    sq=lambda f: np.sign(np.sin(2*np.pi*f*t))
    x=bp(sq(f1)*0.5+sq(f2)*0.5, 420, 5200)
    return x*np.exp(-t*22)*1.0

def bass808(dur, f_start=95.0, f_end=36.0, drive=2.4):
    """Pitch-sliding, distorted. The slide is the attitude; the distortion is the audibility."""
    n=int(dur*SR); t=np.arange(n)/SR
    f=f_end+(f_start-f_end)*np.exp(-t*13)
    x=np.sin(2*np.pi*np.cumsum(f)/SR)
    env=np.exp(-t*2.6)
    return sat(x*env, drive)*0.95

def kick808(dur=0.42):
    n=int(dur*SR); t=np.arange(n)/SR
    f=118*np.exp(-t*30)+36
    return sat(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7.5), 2.6)

def hat(open_=False, rng=None):
    rng = rng or np.random.default_rng(0)
    d=0.10 if open_ else 0.032; n=int(d*SR); t=np.arange(n)/SR
    return bp(rng.uniform(-1,1,n), 6500, 15000)*np.exp(-t*(11 if open_ else 42))*0.75

def snare(rng):
    d=0.20; n=int(d*SR); t=np.arange(n)/SR
    return (bp(rng.uniform(-1,1,n), 900, 7000)*np.exp(-t*17)*0.6
            + np.sin(2*np.pi*190*t)*np.exp(-t*24)*0.35)

# ---------------------------------------------------------------- arrangement
# minor pentatonic in F# - the dark register phonk lives in
COW_NOTES = [739.99, 830.61, 987.77, 1108.73, 830.61, 739.99, 622.25, 739.99]
BASS_ROOT = [92.50, 92.50, 77.78, 82.41]          # F#  F#  D#  E

# MEASURED from the audio of his 5 car-cinematic references - not from prose.
# Two corrections this forced on me:
#   sub 20-80Hz   real 65.7%  mine 30.3%  -> I was far too light on the low end
#   cowbell       real  5.9%  mine 15.8%  -> I had OVER-corrected from "cowbell is THE
#                                            signature". It is characteristic, not dominant.
# The genre is a SUB-BASS record with a cowbell on top, not a cowbell record.
REF = {"sub": 65.7, "bass": 21.1, "cow": 5.9, "pres": 1.5}
BANDS = [(20,80,"sub"), (80,250,"bass"), (500,900,"cow"), (2000,6000,"pres")]

def band_split(x, sr=SR):
    X = np.abs(np.fft.rfft(x)); f = np.fft.rfftfreq(len(x), 1/sr)
    P = X**2; tot = P.sum() or 1.0
    return {lab: 100*P[(f>=lo)&(f<hi)].sum()/tot for lo, hi, lab in BANDS}

def match_reference(x, sr=SR, iters=12, verbose=True):
    """Iteratively shape toward the MEASURED reference balance. Same discipline as bgmgen:
    stop guessing at the mix, measure it and correct."""
    for k in range(iters):
        cur = band_split(x, sr)
        err = max(abs(cur[b]-REF[b]) for b in REF)
        if verbose:
            print("   pass %d  " % k + "  ".join(f"{b} {cur[b]:.1f}" for b in REF))
        if err < 4.0: break
        X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/sr); g = np.ones(len(f))
        for lo, hi, lab in BANDS:
            gain = (REF[lab]/max(cur[lab], 1e-3))**0.5
            g[(f>=lo)&(f<hi)] *= np.clip(gain, 0.2, 6.0)
        idx = np.linspace(0, len(g)-1, 2048).astype(int)
        gs = np.convolve(g[idx], np.ones(9)/9, mode="same")
        x = np.fft.irfft(X*np.interp(np.arange(len(g)), idx, gs), len(x))
        pk = float(np.max(np.abs(x))) or 1.0
        x = x/pk*0.9
    return x

def build(dur=16.0, bpm=150.0, seed=5, reveal=None):
    beat=60.0/bpm; n=int(dur*SR); out=np.zeros(n)
    rng=np.random.default_rng(seed)
    def place(x, at, g=1.0):
        s=int(at*SR); e=min(n, s+len(x))
        if s<n: out[s:e]+=x[:e-s]*g
    steps=int(dur/(beat/2))                      # 8ths
    for i in range(steps):
        t=i*(beat/2)
        bar=int(t/(beat*4))
        # drums
        if i%8 in (0,6):      place(kick808(), t, 1.0)
        if i%8 == 4:          place(snare(rng), t, 0.8)
        place(hat(i%4==3, rng), t, 1.0)
        if i%16==15:          place(hat(True,rng), t+beat/4, 0.5)
        # cowbell melody - the signature
        if True:
            place(cowbell(f1=COW_NOTES[(i//2)%len(COW_NOTES)]*0.72,
                          f2=COW_NOTES[(i//2)%len(COW_NOTES)]*1.06), t, 1.35)
        # sliding 808
        if i%8 in (0,6):
            place(bass808(beat*1.35, f_start=BASS_ROOT[bar%4]*1.9,
                          f_end=BASS_ROOT[bar%4]), t, 0.95)
    out = sat(out, 1.15)          # crest was 3.9 dB - too crushed even for phonk
    out = bitcrush(out, 10)
    out = match_reference(out)    # shape to the MEASURED reference balance
    if reveal is not None:                        # drop everything for a beat at the reveal
        s=int(max(0,reveal-0.45)*SR); e=int(min(dur,reveal-0.05)*SR)
        out[s:e]*=0.08
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "..","assets","bgm","generated"))
    ap.add_argument("--bpm", type=float, default=150.0)
    ap.add_argument("--dur", type=float, default=16.0)
    ap.add_argument("--reveal", type=float)
    a=ap.parse_args()
    x=build(a.dur, a.bpm, reveal=a.reveal)
    p=wr(os.path.join(os.path.abspath(a.out), f"BGM_phonk_{int(a.bpm)}.wav"), x)
    print(f"  wrote {os.path.basename(p)}  {a.bpm:.0f} BPM  {a.dur:.0f}s")
    print(f"  beat {60/a.bpm:.3f}s -> a 2-beat shot is {2*60/a.bpm:.2f}s "
          f"({60/(2*60/a.bpm):.0f} cuts/min)")

if __name__=="__main__":
    main()
