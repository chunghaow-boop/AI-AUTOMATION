# generates hostile plan variants from wrx.py by text surgery, saves as plans/rt_*.py
import re, pathlib
base = pathlib.Path("plans/wrx.py").read_text(encoding="utf-8")

def save(name, txt):
    pathlib.Path(f"plans/{name}.py").write_text(txt, encoding="utf-8")

# RT1: single shot plan (structure math, blends past end, cards past end)
t = base.replace('BLEND_AFTER  = [6, 11]', 'BLEND_AFTER  = [0]')
t = re.sub(r"SHOTS = \[.*?\]\n", 'SHOTS = [("A", 1.00, "med", "only shot")]\n', t, flags=re.S)
save("rt_oneshot", t)

# RT2: unicode + apostrophe + emoji card text (drawtext/PIL/doc pipeline)
t = base.replace('("SUBARU WON\'T SELL YOU THIS", 0, 4, "cap")',
                 '("SUBARU WON\'T \\u201cSELL\\u201d \\u4f60 THIS \\U0001F525", 0, 4, "cap")')
save("rt_unicode", t)

# RT3: capacity EXACTLY at the limit (float edge) - B usable 2.9, demand 2.9
t = base.replace('("B", 1.00, "burst", "front 3/4"),', '("B", 1.00, "med", "front 3/4"),')
save("rt_capedge", t)

# RT4: DELOGO out of bounds + negative
t = base.replace('DELOGO = {15: (372, 612, 112, 38)}', 'DELOGO = {15: (700, 1270, 112, 38), 3: (-10, 5, 0, 9999)}')
save("rt_delogo", t)

# RT5: callback self-pair + duplicate pair
t = base.replace('CALLBACKS = [(1, 18), (8, 16)]', 'CALLBACKS = [(5, 5), (8, 16), (8, 16)]')
save("rt_callback", t)

# RT6: odd BPM - grid vs beat rounding
t = base.replace('BPM       = 150.0', 'BPM       = 140.7')
save("rt_bpm", t)

# RT7: SFX_OVERLAYS beyond clip EOF and beyond video end
t = base.replace('("H", 3.90, 0.70, 12.85, -5.0,', '("H", 4.90, 3.00, 20.5, -5.0,')
save("rt_overlay", t)

# RT8: FOLEY missing one shot + duck_shots out of range handled? (19 exists) - negative gain on EVENT
t = base.replace('16:  -2.0,', '16: -20.0,')
save("rt_foleyquiet", t)
print("8 hostile plans written")
