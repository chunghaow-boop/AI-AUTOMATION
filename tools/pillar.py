#!/usr/bin/env python3
"""
PILLAR — scoped asset lookup. A build can only see its own pillar's material.

WHY
  His diagnosis, and it was right: "all of the assets are in the same folder, maybe you got
  confused". assets/bgm/generated/ held the travel bed, the auto-hero bed and the phonk bed
  together. I picked by FILENAME and put a 90 BPM marimba bed on a car edit, when the genre
  is 140-170 BPM drift phonk.

  Filename matching is not scoping. This is: ask for a bed and you get YOUR pillar's bed, or
  nothing. Reaching into another pillar is not possible, so it cannot happen by accident.

Usage
  import pillar
  bed = pillar.bed("car_cinematic")            # -> the phonk bed, never a travel bed
  sfx = pillar.sfx("car_cinematic", "engine_rev_v1.wav")
"""
import glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A    = os.path.join(ROOT, "assets")

# Where the pillar's material may live. Both the new scoped path and the legacy flat path
# are searched, so this works before AND after organizer.py --apply.
LEGACY = {
    "car_cinematic": {"bgm": ["BGM_phonk_*.wav", "BGM_auto_hero.wav"], "sfx": ["car"]},
    "travel_vlog":   {"bgm": ["BGM_sunset_warm.wav", "BGM_travel_bright.wav",
                              "BGM_lofi_chill.wav", "BGM_travel_arrangement.wav"], "sfx": []},
    "car_review":    {"bgm": [], "sfx": ["car", "ui"]},
    "industry":      {"bgm": [], "sfx": ["ui"]},
}
SHARED_SFX = ["transition", "impact", "ui"]

def _first(paths):
    for p in paths:
        g = sorted(glob.glob(p))
        if g: return g[0]
    return None

def bed(pillar, prefer=None):
    """The music bed for this pillar. Returns None rather than another pillar's bed -
    silence is a correct failure; the wrong genre is not."""
    scoped = os.path.join(A, "pillars", pillar, "bgm")
    cands = []
    if prefer: cands.append(os.path.join(scoped, prefer))
    cands.append(os.path.join(scoped, "*.wav"))
    for pat in LEGACY.get(pillar, {}).get("bgm", []):
        if prefer and prefer != pat: continue
        cands.append(os.path.join(A, "bgm", "generated", pat))
    for pat in LEGACY.get(pillar, {}).get("bgm", []):
        cands.append(os.path.join(A, "bgm", "generated", pat))
    found = _first(cands)
    if not found:
        print(f"  !! no bed for pillar '{pillar}'. NOT falling back to another pillar - "
              f"that is exactly how a marimba bed landed on a car edit.")
    return found

def sfx(pillar, name):
    """Pillar sfx first, then genuinely shared categories (transition/impact/ui)."""
    cands = [os.path.join(A, "pillars", pillar, "sfx", name)]
    for sub in LEGACY.get(pillar, {}).get("sfx", []):
        cands.append(os.path.join(A, "sfx", sub, name))
    for sub in SHARED_SFX:
        cands += [os.path.join(A, "shared", "sfx", sub, name),
                  os.path.join(A, "sfx", sub, name)]
    return _first(cands)

def plate(pillar, subject):
    """Locked reference plate for a named subject. Absence is why a crossover passed as
    a Crown - clipgate cannot verify a subject it has no reference for."""
    for d in (os.path.join(A, "pillars", pillar, "plates"), os.path.join(A, "plates")):
        p = _first([os.path.join(d, f"{subject}.*")])
        if p: return p
    return None

def describe(pillar):
    mp = os.path.join(A, "pillar_map.json")
    if os.path.exists(mp):
        try: return json.load(open(mp)).get(pillar, {}).get("note", "")
        except Exception: pass
    return ""

if __name__ == "__main__":
    for p in LEGACY:
        b = bed(p)
        print(f"  {p:16s} bed={os.path.basename(b) if b else 'NONE':28s} {describe(p)}")
