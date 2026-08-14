#!/usr/bin/env python3
"""
CAPTIONMGR — the Caption Manager seat. Owns nothing but captions, and owns them completely.

WHY A SEPARATE SEAT (his request)
  "the captions really need some design, maybe you can create another role caption manager,
   that focuses only on the captions in the editing automation part"

  Right call. Until now captions were a side-effect of the render step: one font, one size,
  one grey box, dropped at a fixed y. That is subtitling, not design. On short-form the
  caption IS a graphic element - it carries the hook, the emphasis and half the retention.

WHAT THIS SEAT DECIDES
  1. GROUPING     break on phrasing, not character count
  2. EMPHASIS     the ONE word per card that carries the meaning, highlighted
  3. TYPE         size scales with importance; numbers in a list get their own treatment
  4. POSITION     TikTok-safe: above the UI, clear of the right-hand action rail
  5. MOTION       pop-in scale so a card ARRIVES instead of blinking on
  6. LEGIBILITY   measured contrast + width, never trusted by eye

STYLES
  punch    big, tight, keyword-highlighted     - hooks and payoffs
  clean    medium, plain box                   - body narration
  list     numbered rows, left-aligned         - the CTA / artefact drop

NO AI-GENERATED WATERMARK
  Removed at his request. Disclosure still matters - use the PLATFORM toggle instead
  (TikTok "AI-generated content" switch, Meta "AI info" tag). Same compliance, no burn-in.

Usage
  python3 captionmgr.py --preview out.png        # audition the styles on one frame
"""
import os, subprocess, argparse

# TikTok/Reels safe area. The right rail (like/comment/share) eats ~14% of width; the bottom
# caption+handle block eats ~18% of height. Anything inside those is thumbed over.
SAFE = {"top": 0.06, "bottom": 0.80, "right": 0.86}

# stroke = outline width in px. Legibility over unknown footage comes from the stroke, not
# from a box - a box that is opaque enough to guarantee contrast covers the picture.
STYLES = {
    "punch": dict(size=54, y=0.70, box=0.0,  border=6,  stroke=6,
                  colour="white", hi_colour="#FFD54A", shadow=True,  pop=0.16),
    "clean": dict(size=40, y=0.755, box=0.42, border=14, stroke=3,
                  colour="white", hi_colour="#FFE083", shadow=False, pop=0.10),
    "list":  dict(size=34, y=0.62, box=0.48, border=12, stroke=3,
                  colour="white", hi_colour="#FFD54A", shadow=False, pop=0.12),
}

# Words that never carry the emphasis - articles, fillers, connectives.
STOP = {"a","an","the","in","on","at","to","of","and","or","but","is","are","was","were",
        "you","your","i","it","its","this","that","for","with","so","if","by","as","be",
        "can","will","just","really","very","one","two","three","few","only","first",
        "should","hit","go","going","see","and","that","which"}

def font_path():
    """Filtergraph-safe: forward slashes, escaped drive colon. A raw Windows path breaks the
    filter parser - that bug shipped a video with no captions at all."""
    for f in ("C:/Windows/Fonts/seguibl.ttf",     # Segoe UI Black - best weight for captions
              "C:/Windows/Fonts/arialbd.ttf",
              "C:/Windows/Fonts/segoeuib.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            return f.replace("\\", "/").replace(":", "\\:")
    return None

def keyword(text):
    """Pick the ONE word worth highlighting. Longest non-stopword wins, with a bonus for
    proper nouns and digits - those are the things a viewer is scanning for."""
    best, score = None, -1
    for raw in text.split():
        w = raw.strip(".,!?;:").lower()
        if not w or w in STOP or len(w) < 3: continue
        sc = len(w) + (4 if raw[:1].isupper() else 0) + (6 if any(c.isdigit() for c in raw) else 0)
        if sc > score: best, score = raw.strip(".,!?;:"), sc
    return best

def measure_width(text, size, font_px_ratio=0.52):
    """Rough advance-width estimate. Bold sans averages ~0.52 em per glyph; used to catch
    overflow BEFORE rendering rather than discovering it in a frame."""
    return int(len(text) * size * font_px_ratio)

def plan(cards, style="clean", frame_w=720, frame_h=1280, max_w_frac=0.88):
    """Turn timed text into a render plan. Splits any card that would overflow, picks the
    emphasis word, and reports every decision so it can be checked."""
    st = STYLES[style]; out = []
    limit = int(frame_w * max_w_frac)
    for c in cards:
        text = c["text"].strip()
        size = st["size"]
        # shrink, then split, rather than let it run off frame
        while measure_width(text, size) > limit and size > 26:
            size -= 2
        if measure_width(text, size) > limit:
            words = text.split(); mid = len(words)//2
            halves = [" ".join(words[:mid]), " ".join(words[mid:])]
            span = c["end"] - c["start"]
            for k, h in enumerate(halves):
                out.append(dict(text=h, start=c["start"] + k*span/2,
                                end=c["start"] + (k+1)*span/2,
                                size=size, key=keyword(h), style=style, split=True))
            continue
        out.append(dict(text=text, start=c["start"], end=c["end"], size=size,
                        key=keyword(text), style=style, split=False))
    return out

def drawtext(item, font, tmpdir, idx, frame_h=1280):
    """One drawtext chain per card.

    Two bugs the first preview exposed:
      1. the shadow used a FIXED size while the main text used the animated pop-in expression,
         so during the pop the shadow was visibly larger than the text it was shadowing.
         Both now share one expression.
      2. the emphasis word was computed and then never drawn. ffmpeg has no rich text and
         per-word colour needs real font metrics, which are not available here - so instead
         the WHOLE card takes the accent colour when its keyword is a scannable token
         (a number or a proper noun). Robust, and it still creates the visual rhythm.
    """
    st = STYLES[item["style"]]
    y = f"h*{st['y']}"
    tf = os.path.join(tmpdir, f"cm{idx}.txt")
    with open(tf, "w", encoding="utf-8") as fh: fh.write(item["text"])
    base = os.path.basename(tf)
    t0, t1 = item["start"], item["end"]
    pop = st["pop"]
    small = int(item["size"]*0.82)
    size_expr = (f"if(lt(t-{t0:.2f},{pop:.2f}),"
                 f"{small}+({item['size']}-{small})*(t-{t0:.2f})/{pop:.2f},{item['size']})")
    key = item.get("key") or ""
    scannable = bool(key) and (any(c.isdigit() for c in key) or key[:1].isupper())
    colour = st["hi_colour"] if scannable else st["colour"]
    parts = []
    if st["shadow"]:
        parts.append(f"drawtext=fontfile='{font}':textfile='{base}':"
                     f"enable='between(t,{t0:.2f},{t1:.2f})':fontsize='{size_expr}':"
                     f"fontcolor=black@0.7:x=(w-tw)/2+3:y={y}+3")
    box = (f":box=1:boxcolor=black@{st['box']}:boxborderw={st['border']}"
           if st["box"] > 0 else "")
    stroke = (f":borderw={st['stroke']}:bordercolor=black@0.9"
              if st.get("stroke") else "")
    parts.append(f"drawtext=fontfile='{font}':textfile='{base}':"
                 f"enable='between(t,{t0:.2f},{t1:.2f})':fontsize='{size_expr}':"
                 f"fontcolor={colour}{stroke}{box}:x=(w-tw)/2:y={y}")
    item["accent"] = scannable
    return parts

def contrast_ok(fg=(255,255,255), bg=(0,0,0), alpha=0.45):
    """WCAG-style relative luminance ratio against the boxed background. Captions are read at
    arm's length on a bright phone; 4.5:1 is the floor."""
    def lum(c):
        s = [v/255 for v in c]
        s = [(v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4) for v in s]
        return 0.2126*s[0] + 0.7152*s[1] + 0.0722*s[2]
    eff = tuple(int(b*alpha + 128*(1-alpha)) for b in bg)   # box over mid-grey footage
    l1, l2 = sorted([lum(fg), lum(eff)], reverse=True)
    return round((l1+0.05)/(l2+0.05), 2)

def report(items, frame_w=720):
    print(f"  Caption Manager: {len(items)} cards")
    over = [i for i in items if measure_width(i["text"], i["size"]) > frame_w*0.88]
    split = sum(1 for i in items if i["split"])
    keys = sum(1 for i in items if i["key"])
    acc = sum(1 for i in items if i.get("accent"))
    print(f"    emphasis word found on {keys}/{len(items)} cards; "
          f"{acc} rendered in the accent colour")
    if split: print(f"    {split} card(s) split to stay inside the frame")
    print(f"    overflow after fitting: {len(over)}  (must be 0)")
    print(f"    contrast on boxed style: {contrast_ok()}:1  (floor 4.5:1)")
    print(f"    baseline y {STYLES[items[0]['style']]['y'] if items else '-'} "
          f"- above the {SAFE['bottom']} bottom UI band")
    return not over

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="render the three styles onto one frame")
    a = ap.parse_args()
    font = font_path()
    if not font: print("no bold font found"); return
    demo = [{"text": "Grilled seafood, few ringgit only", "start": 0, "end": 3}]
    for s in STYLES:
        items = plan(demo, s)
        print(f"\n[{s}]"); report(items)
    if a.preview:
        os.makedirs(os.path.dirname(a.preview) or ".", exist_ok=True)
        tmp = "/tmp/cmprev"; os.makedirs(tmp, exist_ok=True)
        vf = []
        for j, s in enumerate(STYLES):
            it = plan([{"text": f"{s}: grilled seafood", "start": 0, "end": 3}], s)[0]
            it["style"] = s
            STYLES[s]["y"] = 0.30 + 0.18*j
            vf += drawtext(it, font, tmp, j)
        subprocess.run(f'ffmpeg -y -v error -f lavfi -i "color=c=0x2a3540:s=720x1280:d=1" '
                       f'-vf "{",".join(vf)}" -frames:v 1 "{a.preview}"',
                       shell=True, cwd=tmp)
        print(f"\nwrote {a.preview}")

if __name__ == "__main__":
    main()
