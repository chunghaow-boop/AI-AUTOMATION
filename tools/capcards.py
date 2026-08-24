#!/usr/bin/env python3
"""
CAPCARDS — PIL renderer for the Caption Manager seat.

WHY (2026-08-12, session 11)
  captionmgr.py plans captions well but renders through ffmpeg drawtext, which
  cannot do per-word colour (its own comment admits it: the WHOLE card flips to
  accent). The 2026 field standard — measured by web scan, sources in RESUME —
  is: phrase captions, ONE accent-colour keyword per line (#FFD54A class),
  scrim/pill behind text, 100–150ms pop-in. drawtext can do none of the first
  three properly. PIL + the repo's own CapCutSansText-Bold does all of it, with
  real font metrics, and runs in the sandbox AND on his box (no Playwright
  needed — Playwright remains the premium path for complex cards.py templates).

DIVISION OF LABOUR
  captionmgr.plan()/keyword()  → grouping, emphasis, overflow  (unchanged, imported)
  capcards.render()            → RGBA PNG with pill + keyword highlight
  capcards.overlay_filters()   → the ffmpeg overlay+fade chain for a build script

STYLE (locked with Gavril 2026-08-12: V6 full)
  White CapCutSansText-Bold, one #FFD54A keyword, rounded pill black@0.45,
  120ms fade/pop-in, y=0.70 (inside captionmgr.SAFE, above the bottom UI band).
  Pill opacity 0.45 at worst-case V5 band luma 122 → effective contrast 9.8:1,
  double the capcheck floor. The pill is WHY capcheck can never fail again on
  bright footage — legibility no longer depends on the frame behind it.
"""
import os, sys, argparse, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from captionmgr import plan, keyword          # the seat still makes the decisions
from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "assets", "fonts", "loose", "CapCutSansText-Bold.otf")
ACCENT = (255, 213, 74, 255)      # #FFD54A
WHITE  = (255, 255, 255, 255)
PILL   = (0, 0, 0, 115)           # black @ 0.45
PAD_X, PAD_Y, RADIUS = 26, 14, 18
POP = 0.12                        # fade/pop-in seconds

# ---------------------------------------------------------------- REGISTERS
# FINDING 3 (file 31 PART H, 2026-08-12): text register is PER PILLAR, measured
# from the reference library. One caption style for every pillar was our own
# invention, not the field's. Each preset below is what that pillar's references
# actually do. 'punch' reproduces the pre-2026-08-12 behaviour byte-for-byte, so
# existing builds are unaffected — it is the default and the industry register.
REGISTERS = {
    # industry / general: white + ONE yellow keyword on a dark scrim.
    # Independently confirmed by the industry refs (yellow keyword karaoke).
    "punch":   dict(size=44, fill=WHITE, accent=ACCENT, pill=PILL, radius=18,
                    pad=(26, 14), upper=False, y=0.70,
                    why="industry/default: white + one #FFD54A keyword on a scrim"),
    # travel_vlog: the refs WHISPER — tiny, lowercase, delicate, low-opacity.
    "quiet":   dict(size=30, fill=(255, 255, 255, 232), accent=(255, 255, 255, 232),
                    pill=(0, 0, 0, 70), radius=14, pad=(18, 9), upper=False, y=0.74,
                    why="travel_vlog: tiny lowercase, lower-mid, barely-there scrim"),
    # travel_vlog journey spine: the TIME chip (finding 4). Small, monospaced feel,
    # high contrast, sits high-left out of the caption lane.
    "time":    dict(size=26, fill=(255, 255, 255, 245), accent=(255, 255, 255, 245),
                    pill=(0, 0, 0, 110), radius=10, pad=(14, 7), upper=False, y=0.09,
                    why="travel_vlog: the clock advancing IS the process (7:00 -> 8:00)"),
    # car_cinematic: huge display type as a design element, no scrim at all.
    "display": dict(size=96, fill=WHITE, accent=ACCENT, pill=(0, 0, 0, 0), radius=0,
                    pad=(0, 0), upper=True, y=0.62,
                    why="car_cinematic: huge display type, no box, letters may crop"),
    # car_review: white rounded CARD, dark text, top-left, frame 1 = subject+price.
    "card":    dict(size=34, fill=(17, 17, 17, 255), accent=(17, 17, 17, 255),
                    pill=(255, 255, 255, 240), radius=12, pad=(20, 12), upper=False,
                    y=0.13, why="car_review: white card, dark text, subject + price"),
}
# which register a pillar defaults to, from its own references
PILLAR_REGISTER = {"travel_vlog": "quiet", "car_cinematic": "display",
                   "car_cinematic_chill": "display", "car_review": "card",
                   "industry": "punch"}

def render(item, out_png, scale=2, max_w=None, register="punch"):
    """One caption card → transparent PNG (rendered at 2x, downscaled = clean edges).
    REAL-METRIC FIT (caught 2026-08-12): captionmgr.plan() estimates width at
    0.52 em/glyph but CapCutSansText-Bold runs wider — cards 3+4 of the panborneo
    set rendered 784/730px on a 720 frame. The estimate stays for planning; the
    renderer re-fits with true getbbox() widths and shrinks until it fits."""
    R = REGISTERS.get(register, REGISTERS["punch"])
    pad_x, pad_y = R["pad"]
    txt = item["text"].upper() if R["upper"] else item["text"]
    words = txt.split()
    key = (item.get("key") or "").lower().strip(".,!?;:")
    # the register sets the base size; the plan's per-card size still shrinks it
    size_1x = R["size"] if R["size"] != REGISTERS["punch"]["size"] else item["size"]
    min_size = max(16, int(R["size"] * 0.55))
    while True:
        size = size_1x * scale
        font = ImageFont.truetype(FONT, size)
        space = font.getbbox(" ")[2]
        widths = [font.getbbox(w)[2] for w in words]
        text_w = sum(widths) + space*(len(words)-1)
        total_w = (text_w + 2*pad_x*scale) // scale
        if max_w is None or total_w <= max_w or size_1x <= min_size:
            break
        size_1x -= 2
    asc, desc = font.getmetrics()
    text_h = asc + desc
    W, H = text_w + 2*pad_x*scale, text_h + 2*pad_y*scale
    im = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(im)
    if R["pill"][3] > 0:
        d.rounded_rectangle([0,0,W-1,H-1], radius=R["radius"]*scale, fill=R["pill"])
    x = pad_x*scale
    for w, wd in zip(words, widths):
        col = R["accent"] if w.lower().strip(".,!?;:") == key else R["fill"]
        d.text((x, pad_y*scale), w, font=font, fill=col)
        x += wd + space
    im = im.resize((max(1, W//scale), max(1, H//scale)), Image.LANCZOS)
    im.save(out_png)
    return im.size

def build_cards(cards, outdir, style="punch", register=None, pillar=None):
    """Plan + render every card. Returns overlay manifest for the build script.

    register: one of REGISTERS (finding 3 - text register is per pillar). If not
    given it is looked up from `pillar`, and falls back to 'punch' (the original
    behaviour, byte-identical). A card may override with its own 'register' key -
    that is how TIMESTAMP chips ride along with normal captions (finding 4)."""
    os.makedirs(outdir, exist_ok=True)
    base = register or PILLAR_REGISTER.get(pillar or "", "punch")
    items = plan(cards, style)
    man = []
    for j, it in enumerate(items):
        png = os.path.join(outdir, f"card{j}.png")
        reg = (cards[j].get("register") if j < len(cards) and isinstance(cards[j], dict)
               else None) or base
        w, h = render(it, png, max_w=int(720*0.88), register=reg)
        man.append(dict(png=png, w=w, h=h, start=round(it["start"],3),
                        end=round(it["end"],3), key=it["key"], text=it["text"],
                        register=reg, y=REGISTERS.get(reg, REGISTERS["punch"])["y"]))
    with open(os.path.join(outdir, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1)
    return man

def overlay_filters(man, chain_in, frame_w=720, frame_h=1280, y=0.70, input_offset=0):
    """ffmpeg filtergraph: overlay each card centred at y with a 120ms alpha fade-in.
    Card PNGs are inputs input_offset..input_offset+n-1. Returns (filters, last_label).

    frame_h MUST be the real frame height. L181, found 2026-08-17: the 1280 default is a
    720p-vertical assumption, and every 1080x1920 film silently placed its cards against
    1280 instead of 1920. At y=0.13 that shifted a card from 250px to 166px and looked
    merely "a bit high"; at y=0.72 it put the caption at 921px - 48% of frame, DEAD
    CENTRE, which CLAUDE.md forbids outright ("never centre - the subject lives there").
    A default that is right for one format is a silent defect in every other."""
    f, cur = [], chain_in
    for j, m in enumerate(man):
        idx = input_offset + j
        f.append(f"[{idx}:v]format=rgba,fade=t=in:st={m['start']:.3f}:d={POP}:alpha=1[cd{j}]")
        out = f"[co{j}]"
        yy = m.get("y", y)
        f.append(f"{cur}[cd{j}]overlay=(W-w)/2:{int(frame_h*yy)}:"
                 f"enable='between(t,{m['start']:.3f},{m['end']:.3f})'{out}")
        cur = out
    return f, cur

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards", help="json [{text,start,end},...]")
    ap.add_argument("--out", default="/tmp/capcards")
    ap.add_argument("--style", default="punch")
    a = ap.parse_args()
    demo = [dict(text="SABAH ENDS HERE", start=0.15, end=3.0)]
    cards = json.load(open(a.cards)) if a.cards else demo
    man = build_cards(cards, a.out, a.style)
    for m in man:
        print(f"  {m['w']}x{m['h']}  key={m['key']!r:20}  {m['text']}")
    print(f"wrote {len(man)} cards + manifest.json → {a.out}")
