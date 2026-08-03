#!/usr/bin/env python3
"""
SFXGEN — synthesise the short-form SFX pack procedurally. No downloads, no licence risk.

WHY: the sandbox cannot reach pixabay / mixkit / freesound / archive.org (all 403 at the proxy,
verified 2026-07-27). But the SFX that actually carry short-form video — whooshes, impacts,
risers, clicks, sub-drops, swells — are *synthesis*, not recordings. These are generated from
noise + filters + envelopes, which is how they're made commercially anyway.

100% original output → no attribution, no licence, no takedown risk. Safe for monetised content.

WHAT IT CANNOT DO: real music (BGM). Melody/harmony/performance don't synthesise convincingly
here. It does produce BPM-LOCKED UTILITY BEDS so `rhythm.py` has a known grid to cut against —
useful for building and testing, not a substitute for a real track.

Usage:
  python3 sfxgen.py --out ../assets            # generate the full pack
  python3 sfxgen.py --list
"""
import argparse, os, math, wave, struct
import numpy as np

SR = 48000

# ---------- helpers ----------
def _w(path, x, sr=SR):
    x = np.clip(x, -1, 1)
    # short fades to kill clicks
    n = min(len(x), int(sr*0.004))
    if n > 0:
        x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    # normalise to -1.5 dBFS peak
    pk = np.max(np.abs(x)) or 1.0
    x = x / pk * 0.84
    with wave.open(path, "w") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((x*32767).astype(np.int16).tobytes())

def noise(n): return np.random.uniform(-1, 1, int(n))
def t(dur): return np.linspace(0, dur, int(SR*dur), endpoint=False)
def env_exp(n, k=6.0): return np.exp(-np.linspace(0, k, int(n)))
def env_ar(n, a=0.02, r=0.9):
    n = int(n); na = max(1, int(n*a))
    return np.concatenate([np.linspace(0,1,na), np.exp(-np.linspace(0,5,n-na))])

def lp(x, cut, sr=SR):
    """one-pole lowpass, cut in Hz (accepts array for a sweep)"""
    cut = np.asarray(cut, dtype=float)
    if cut.ndim == 0: cut = np.full(len(x), float(cut))
    y = np.zeros_like(x); prev = 0.0
    a = 1.0 - np.exp(-2*np.pi*np.clip(cut,20,sr/2-100)/sr)
    for i in range(len(x)):
        prev += a[i]*(x[i]-prev); y[i] = prev
    return y

def hp(x, cut, sr=SR): return x - lp(x, cut, sr)

# ---------- the pack ----------
def whoosh(dur=0.55, up=True):
    n = int(SR*dur); sweep = np.linspace(300, 6000, n) if up else np.linspace(6000, 300, n)
    x = lp(noise(n), sweep) * env_ar(n, 0.25)
    return x * 1.4

def whoosh_long(dur=1.1): return whoosh(dur, up=True)

def impact(dur=0.7):
    n = int(SR*dur); tt = t(dur)
    body = np.sin(2*np.pi*np.linspace(120, 45, n)*tt) * env_exp(n, 5)
    crack = hp(noise(n), 2000) * env_exp(n, 40) * 0.5
    return body*0.9 + crack

def thud(dur=0.45):
    n = int(SR*dur); tt = t(dur)
    return np.sin(2*np.pi*np.linspace(90, 38, n)*tt) * env_exp(n, 7)

def sub_drop(dur=1.4):
    n = int(SR*dur); tt = t(dur)
    return np.sin(2*np.pi*np.linspace(70, 22, n)*tt) * env_exp(n, 2.4)

def riser(dur=2.0):
    n = int(SR*dur); tt = t(dur)
    nz = lp(noise(n), np.linspace(400, 9000, n)) * np.linspace(0.05, 1.0, n)**2
    tone = np.sin(2*np.pi*np.cumsum(np.linspace(200, 1400, n))/SR) * np.linspace(0,0.5,n)**2
    return nz*0.8 + tone*0.5

def downlifter(dur=1.6):
    n = int(SR*dur); nz = lp(noise(n), np.linspace(8000, 300, n)) * np.linspace(1.0,0.02,n)**1.5
    return nz

def click(dur=0.06):
    n = int(SR*dur); return hp(noise(n), 3000) * env_exp(n, 55)

def tick(dur=0.04):
    n = int(SR*dur); tt = t(dur)
    return (np.sin(2*np.pi*2400*tt) + hp(noise(n),4000)*0.4) * env_exp(n, 70)

def pop(dur=0.12):
    n = int(SR*dur); tt = t(dur)
    return np.sin(2*np.pi*np.linspace(900, 220, n)*tt) * env_exp(n, 25)

def swell(dur=1.8):
    n = int(SR*dur); tt = t(dur)
    base = sum(np.sin(2*np.pi*f*tt) for f in (110, 165, 220, 330))/4
    return base * (np.linspace(0,1,n)**2) * 0.8

def stinger(dur=0.9):
    n = int(SR*dur); tt = t(dur)
    ch = sum(np.sin(2*np.pi*f*tt) for f in (196, 294, 392))/3
    return ch * env_exp(n, 4) + hp(noise(n),3000)*env_exp(n,30)*0.25

def camera_shutter(dur=0.18):
    n = int(SR*dur); a = hp(noise(n), 2500)*env_exp(n, 60)
    b = np.zeros(n); off = int(SR*0.055)
    b[off:] = (hp(noise(n-off), 2000)*env_exp(n-off, 45))*0.8
    return a + b

def ui_confirm(dur=0.35):
    n = int(SR*dur); tt = t(dur)
    return (np.sin(2*np.pi*880*tt)*env_exp(n,12) +
            np.sin(2*np.pi*1320*tt)*np.concatenate([np.zeros(int(n*0.35)), env_exp(n-int(n*0.35),12)]))*0.6

def ui_error(dur=0.4):
    n = int(SR*dur); tt = t(dur)
    return (np.sin(2*np.pi*220*tt) + np.sin(2*np.pi*233*tt))*env_exp(n,8)*0.6

def page_turn(dur=0.4):
    n = int(SR*dur); return lp(noise(n), np.linspace(2000, 700, n))*env_ar(n, 0.15)*0.9

def cash(dur=0.6):
    n = int(SR*dur); tt = t(dur)
    bells = sum(np.sin(2*np.pi*f*tt)*env_exp(n, 6+i*2) for i,f in enumerate((1200,1800,2400)))
    return bells/3

def engine_rev(dur=1.8):
    n = int(SR*dur); tt = t(dur)
    f = np.concatenate([np.linspace(60,180,int(n*0.55)), np.linspace(180,90,n-int(n*0.55))])
    saw = 2*(tt*f - np.floor(0.5 + tt*f))
    return lp(saw, 2200)*0.55 + lp(noise(n), 900)*0.25

def door_close(dur=0.5):
    n = int(SR*dur); tt = t(dur)
    return np.sin(2*np.pi*np.linspace(150,60,n)*tt)*env_exp(n,9) + hp(noise(n),1500)*env_exp(n,35)*0.4

def tyre_screech(dur=1.0):
    n = int(SR*dur); tt = t(dur)
    base = np.sin(2*np.pi*np.linspace(1400, 900, n)*tt)
    return (base*0.5 + hp(noise(n), 1800)*0.5) * env_ar(n, 0.1)

def glitch(dur=0.3):
    n = int(SR*dur); x = noise(n)
    step = int(SR*0.012)
    for i in range(0, n-step, step*2): x[i:i+step] = 0
    return hp(x, 800)*0.8

def reverse_cymbal(dur=1.5):
    n = int(SR*dur); return hp(noise(n), 3000) * (np.linspace(0,1,n)**2.2)

# BPM-locked utility beds (NOT music — a grid for rhythm.py)
def bed_pulse(bpm=120, bars=8, dur=None):
    per = 60.0/bpm; dur = dur or per*4*bars
    n = int(SR*dur); x = np.zeros(n)
    for b in np.arange(0, dur, per):
        i = int(b*SR); k = thud(0.22)*0.55
        x[i:i+len(k)] += k[:max(0, min(len(k), n-i))]
    for b in np.arange(per/2, dur, per):
        i = int(b*SR); h = hp(noise(int(SR*0.05)),6000)*env_exp(int(SR*0.05),30)*0.18
        x[i:i+len(h)] += h[:max(0, min(len(h), n-i))]
    return x

def bed_drone(dur=30.0):
    tt = t(dur); n = len(tt)
    d = sum(np.sin(2*np.pi*f*tt + np.sin(2*np.pi*0.07*tt)*0.6) for f in (55, 82.5, 110, 164))/4
    return lp(d, 1200) * (0.55 + 0.12*np.sin(2*np.pi*0.05*tt))

PACK = {
 "transition": {"whoosh_up":whoosh, "whoosh_long":whoosh_long,
                "whoosh_down":lambda: whoosh(0.55, up=False),
                "riser":riser, "downlifter":downlifter,
                "reverse_cymbal":reverse_cymbal, "glitch":glitch, "swell":swell},
 "impact":     {"impact_hit":impact, "thud":thud, "sub_drop":sub_drop, "stinger":stinger},
 "ui":         {"click":click, "tick":tick, "pop":pop, "ui_confirm":ui_confirm,
                "ui_error":ui_error, "page_turn":page_turn, "cash_register":cash,
                "camera_shutter":camera_shutter},
 "car":        {"engine_rev":engine_rev, "door_close":door_close, "tyre_screech":tyre_screech},
 "bed":        {"pulse_90bpm":lambda: bed_pulse(90), "pulse_100bpm":lambda: bed_pulse(100),
                "pulse_120bpm":lambda: bed_pulse(120), "pulse_128bpm":lambda: bed_pulse(128),
                "drone_tension":bed_drone},
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="assets"); ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for cat, d in PACK.items(): print(f"{cat:12} {', '.join(d)}")
        return
    np.random.seed(7)   # reproducible pack
    total = 0
    for cat, items in PACK.items():
        sub = "bgm" if cat == "bed" else "sfx"
        d = os.path.join(a.out, sub, cat if cat != "bed" else "utility-beds")
        os.makedirs(d, exist_ok=True)
        for name, fn in items.items():
            # 3 variations of each short SFX; beds get one
            reps = 1 if cat == "bed" else 3
            for v in range(reps):
                x = fn()
                suffix = "" if reps == 1 else f"_v{v+1}"
                p = os.path.join(d, f"{name}{suffix}.wav")
                _w(p, x); total += 1
    print(f"generated {total} files -> {a.out}/")
    print("100% synthesised — no licence, no attribution, safe for monetised content.")
    print("NOTE: 'utility-beds' are BPM grids for cut-to-beat testing, NOT hero music.")

if __name__ == "__main__":
    main()
