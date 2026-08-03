#!/usr/bin/env python3
"""
CARDS — HTML/CSS → PNG graphics via Playwright. Replaces ffmpeg drawtext.

WHY THIS MATTERS: drawtext is the weakest visual element in the current output — one font,
no kerning control, no gradients, no layout. Reference-grade channels use designed cards.
HTML/CSS gives real typography, and Playwright screenshots it at 1080×1920.

Unlocks the ARTEFACT DROP format (the Douyin top-post mechanic): a genuinely
screenshot-able checklist / price ladder that people SAVE. Save-bait beats watch-bait.

TEMPLATES
  punch      big centre text, the beat card ("you don't")
  title      pillar + episode number — the fixed series asset (file 14)
  checklist  the 9-point inspection card  ← the Artefact Drop
  ladder     RM30k / RM50k / RM80k price ladder
  cta        end card
  lower      lower-third name/role strip

LOCAL ONLY for full quality: Playwright browser binaries are blocked by the Cowork proxy
(cdn.playwright.dev 403), same as the Whisper weights. Falls back to an ffmpeg renderer that
works anywhere but looks plainer. `bash setup-local.sh` installs the good path.

Usage:
  python3 cards.py punch     --text "you don't"                        -o card.png
  python3 cards.py checklist --title "Before you pay deposit" --items items.txt -o card.png
  python3 cards.py ladder    --rows "RM30k|Myvi 2019|~85k km" ...      -o card.png
  python3 cards.py title     --pillar "Recond Truth" --ep 12           -o card.png
  python3 cards.py --list
"""
import argparse, json, os, subprocess, sys, tempfile, html

W, H = 1080, 1920
BRAND = {
    "bg":      "#0d0f12",
    "fg":      "#ffffff",
    "accent":  "#ffd400",     # high-contrast highlight — reads at 30% zoom
    "muted":   "#9aa4b2",
    "panel":   "rgba(0,0,0,0.55)",
    "font":    "'Inter','Helvetica Neue',Arial,'Noto Sans',sans-serif",
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(W)spx;height:%(H)spx;background:transparent;font-family:%(font)s;
 -webkit-font-smoothing:antialiased}
.wrap{width:100%%;height:100%%;display:flex;flex-direction:column;justify-content:center;
 align-items:center;padding:90px 70px}
.panel{background:%(panel)s;border-radius:28px;padding:48px 56px;backdrop-filter:blur(6px)}
.punch{font-size:118px;font-weight:800;color:%(fg)s;text-align:center;line-height:1.05;
 letter-spacing:-2px;text-shadow:0 6px 40px rgba(0,0,0,.65)}
.punch .hl{color:%(accent)s}
.kicker{font-size:34px;font-weight:700;color:%(accent)s;letter-spacing:6px;text-transform:uppercase;
 margin-bottom:26px;text-align:center}
.title{font-size:92px;font-weight:800;color:%(fg)s;text-align:center;line-height:1.08}
.ep{font-size:40px;font-weight:700;color:%(muted)s;margin-top:22px;letter-spacing:3px}
.card{background:#14171c;border:2px solid #262b33;border-radius:34px;padding:60px 56px;width:100%%}
.card h1{font-size:62px;font-weight:800;color:%(fg)s;line-height:1.12;margin-bottom:14px}
.card .sub{font-size:32px;color:%(muted)s;margin-bottom:40px}
.item{display:flex;gap:26px;align-items:flex-start;padding:24px 0;border-bottom:1px solid #222831}
.item:last-child{border-bottom:none}
.num{min-width:64px;height:64px;border-radius:16px;background:%(accent)s;color:#111;
 font-weight:800;font-size:32px;display:flex;align-items:center;justify-content:center}
.txt{font-size:40px;color:#e8ecf1;font-weight:600;line-height:1.28;padding-top:6px}
.row{display:flex;align-items:center;gap:28px;padding:30px 0;border-bottom:1px solid #222831}
.price{font-size:58px;font-weight:800;color:%(accent)s;min-width:250px}
.what{font-size:38px;color:#e8ecf1;font-weight:600}
.meta{font-size:28px;color:%(muted)s;margin-top:6px}
.foot{margin-top:44px;font-size:30px;color:%(muted)s;text-align:center;letter-spacing:1px}
.cta{font-size:76px;font-weight:800;color:%(fg)s;text-align:center;line-height:1.15}
.cta .hl{color:%(accent)s}
.lower{position:absolute;left:70px;bottom:230px;background:%(panel)s;border-left:10px solid %(accent)s;
 padding:26px 38px;border-radius:0 16px 16px 0}
.lower .n{font-size:52px;font-weight:800;color:%(fg)s}
.lower .r{font-size:30px;color:%(muted)s;margin-top:6px;letter-spacing:2px;text-transform:uppercase}
""" % {**BRAND, "W": W, "H": H}

def esc(s): return html.escape(str(s))

def tpl_punch(a):
    t = esc(a.text)
    if a.highlight:
        t = t.replace(esc(a.highlight), f'<span class="hl">{esc(a.highlight)}</span>')
    return f'<div class="wrap"><div class="panel"><div class="punch">{t}</div></div></div>'

def tpl_title(a):
    return (f'<div class="wrap"><div class="kicker">{esc(a.pillar)}</div>'
            f'<div class="title">{esc(a.text or a.pillar)}</div>'
            f'<div class="ep">EPISODE #{esc(a.ep)}</div></div>')

def tpl_checklist(a):
    items = [l.strip() for l in open(a.items, encoding="utf-8") if l.strip()] if a.items else \
            (a.rows or [])
    li = "".join(f'<div class="item"><div class="num">{i+1}</div>'
                 f'<div class="txt">{esc(x)}</div></div>' for i, x in enumerate(items[:9]))
    sub = f'<div class="sub">{esc(a.sub)}</div>' if a.sub else ""
    foot = f'<div class="foot">{esc(a.foot)}</div>' if a.foot else \
           '<div class="foot">screenshot this · no link, no DM</div>'
    return (f'<div class="wrap"><div class="card"><h1>{esc(a.title)}</h1>{sub}{li}</div>{foot}</div>')

def tpl_ladder(a):
    rows = ""
    for r in (a.rows or []):
        parts = [p.strip() for p in r.split("|")]
        price = parts[0] if parts else ""
        what  = parts[1] if len(parts) > 1 else ""
        meta  = parts[2] if len(parts) > 2 else ""
        rows += (f'<div class="row"><div class="price">{esc(price)}</div>'
                 f'<div><div class="what">{esc(what)}</div>'
                 f'{f"<div class=meta>{esc(meta)}</div>" if meta else ""}</div></div>')
    return (f'<div class="wrap"><div class="card"><h1>{esc(a.title or "RM___ gets you THIS")}</h1>'
            f'{rows}</div><div class="foot">save this before you go showroom</div></div>')

def tpl_cta(a):
    t = esc(a.text)
    if a.highlight: t = t.replace(esc(a.highlight), f'<span class="hl">{esc(a.highlight)}</span>')
    return f'<div class="wrap"><div class="cta">{t}</div></div>'

def tpl_lower(a):
    return (f'<div class="wrap"></div><div class="lower"><div class="n">{esc(a.text)}</div>'
            f'<div class="r">{esc(a.sub or "")}</div></div>')

TEMPLATES = {"punch":tpl_punch, "title":tpl_title, "checklist":tpl_checklist,
             "ladder":tpl_ladder, "cta":tpl_cta, "lower":tpl_lower}

def render_playwright(body, out, transparent=True):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False, ("playwright not installed — run: bash setup-local.sh\n"
                       "  (browser binaries are blocked in the Cowork sandbox; this is local-only)")
    doc = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    f = os.path.join(tempfile.gettempdir(), "card.html")
    open(f, "w", encoding="utf-8").write(doc)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width":W,"height":H}, device_scale_factor=1)
            pg.goto("file://" + f)
            pg.wait_for_timeout(220)
            pg.screenshot(path=out, omit_background=transparent)
            b.close()
        return True, out
    except Exception as e:
        return False, f"playwright render failed: {str(e)[:160]}"

def render_ffmpeg_fallback(a, out):
    """Plain but works anywhere. Quality is visibly lower — this is the degraded path."""
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font):
        for c in ["/System/Library/Fonts/Helvetica.ttc","C:/Windows/Fonts/arialbd.ttf"]:
            if os.path.exists(c): font = c; break
    text = a.text or a.title or ""
    tf = os.path.join(tempfile.gettempdir(), "c.txt")
    open(tf,"w",encoding="utf-8").write(text)
    cmd = (f'ffmpeg -y -v error -f lavfi -i color=c=black@0.0:s={W}x{H}:d=1,format=rgba '
           f'-vf "drawtext=fontfile={font}:textfile={tf}:fontsize=96:fontcolor=white:'
           f'box=1:boxcolor=black@0.55:boxborderw=40:x=(w-tw)/2:y=(h-th)/2" -frames:v 1 "{out}"')
    subprocess.run(cmd, shell=True, capture_output=True)
    return os.path.exists(out)

def composite(video, card, out, at=0.0, dur=3.0, y="H*0.62", fade=0.25):
    """Overlay a transparent card PNG onto video with an alpha fade.
    Pattern taken from the repo's own playwright-SKILL.md."""
    vf = (f"[1:v]format=rgba,fade=t=in:st=0:d={fade}:alpha=1,"
          f"fade=t=out:st={max(0,dur-fade)}:d={fade}:alpha=1[c];"
          f"[0:v][c]overlay=0:{y}:enable='between(t,{at},{at+dur})'")
    cmd = f'ffmpeg -y -v error -i "{video}" -i "{card}" -filter_complex "{vf}" -c:a copy "{out}"'
    subprocess.run(cmd, shell=True, capture_output=True)
    return os.path.exists(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template", nargs="?", choices=list(TEMPLATES))
    ap.add_argument("--text"); ap.add_argument("--title"); ap.add_argument("--sub")
    ap.add_argument("--foot"); ap.add_argument("--highlight"); ap.add_argument("--pillar")
    ap.add_argument("--ep", default="1"); ap.add_argument("--items")
    ap.add_argument("--rows", nargs="*"); ap.add_argument("-o", default="card.png")
    ap.add_argument("--opaque", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--onto", help="composite the rendered card onto this video")
    ap.add_argument("--at", type=float, default=0.0); ap.add_argument("--dur", type=float, default=3.0)
    ap.add_argument("--y", default="H*0.62")
    a = ap.parse_args()

    if a.list or not a.template:
        print("templates:", ", ".join(TEMPLATES)); print(__doc__.split("Usage:")[1]); return

    body = TEMPLATES[a.template](a)
    ok, msg = render_playwright(body, a.o, transparent=not a.opaque)
    if ok:
        print(f"rendered {a.template} -> {a.o}  ({W}x{H}, "
              f"{'transparent' if not a.opaque else 'opaque'})")
        if a.onto:
            o2 = a.o.replace(".png","_composited.mp4")
            print("composited ->", o2 if composite(a.onto, a.o, o2, a.at, a.dur, a.y) else "FAILED")
        return
    print("!!", msg)
    print("-> falling back to ffmpeg (plainer output)")
    if render_ffmpeg_fallback(a, a.o):
        print(f"fallback rendered -> {a.o}")
    else:
        print("fallback failed too"); sys.exit(1)

if __name__ == "__main__":
    main()
