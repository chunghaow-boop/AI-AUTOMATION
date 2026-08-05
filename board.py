#!/usr/bin/env python3
"""
Render the Supra board FROM supra_plan.py. Never beside it.

The previous board (make_storyboard_i8.py) was typed alongside the plan and drifted; it
also died on a typo'd colour string. This one has no content of its own — every label,
colour, length and note is read out of the plan module, so the picture cannot disagree
with the code.

Looking at the board is the point: the LC300 version caught one clip carrying 4 of 14
shots, and a lighting arc that contradicted the comment above it.
"""
import os, sys, importlib
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

BG, INK, DIM, LINE = "#12141A", "#F2F4F8", "#8B93A3", "#252A35"
W = 2300
PX_S = 86.0          # pixels per second


def _pillar_style(pillar):
    """The board is a picture of the PLAN, so it must read the plan's declared style.
    Added 2026-08-05 after the sound panel found this board and PRODUCTION.md both
    printing car_cinematic's whoosh-on-every-cut under a hero_only dialect."""
    import json
    for c in (os.path.join(HERE, "assets", "pillars", "PILLAR-PROFILES.json"),
              os.path.join(HERE, "pillars", "PILLAR-PROFILES.json")):
        if os.path.exists(c):
            return (json.load(open(c, encoding="utf-8")).get(pillar) or {}).get("style") or {}
    return {}


def font(sz, bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
              "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def _thumb(name, P, key, cache={}):
    """First frame of the real clip for this source, if it exists. The board upgrades
    itself from colour-blocks to actual footage as clips arrive - free previz."""
    if key in cache:
        return cache[key]
    import glob as _g
    HERE_ = os.path.dirname(os.path.abspath(__file__))
    cdir = os.path.join(HERE_, "projects", name, "clips")
    path = None
    named = getattr(P, "CLIPS", {}).get(key)
    if named and os.path.exists(os.path.join(cdir, named)):
        path = os.path.join(cdir, named)
    else:
        c = [f for f in _g.glob(os.path.join(cdir, "*.mp4"))
             if f"_{key}_" in os.path.basename(f) or os.path.basename(f).startswith(f"{key}_")]
        path = c[0] if c else None
    im = None
    if path:
        try:
            import cv2
            cap = cv2.VideoCapture(path); ok, f = cap.read(); cap.release()
            if ok:
                f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(f)
        except Exception:
            im = None
    cache[key] = im
    return im


def main(mod="supra", out=None):
    name = mod
    for cand in (f"plans.{name}", name, f"{name}_plan"):
        try:
            P = importlib.import_module(cand); break
        except ModuleNotFoundError:
            P = None
    if P is None:
        raise SystemExit(f"no plan module for '{name}' (looked for plans/{name}.py)")
    tl, total = P.timeline()
    c = P.cost()
    _edit_sfx = (_pillar_style(getattr(P, "PILLAR", "")) or {}).get("edit_sfx", "full")

    L, T = 70, 40
    tw = int(total * PX_S)
    # 2026-08-05: W was a hardcoded 2300, measured off the 21.6s WRX plan. A 30s plan
    # rendered 280px past the right edge and the last three shots - the whole ending -
    # were simply not in the picture Gavril reviews. The canvas follows the timeline now.
    W = max(2300, L + tw + 120)
    H = 1180
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    f28 = font(28, True); f18 = font(18, True); f15 = font(15); f13 = font(13); f11 = font(11)

    d.text((L, T), P.PROJECT.upper(), font=f28, fill=INK)
    d.text((L, T + 40),
           f"{len(P.SHOTS)} shots · {total:.2f}s · {P.W}x{P.H}@{P.FPS} · {P.PILLAR} · "
           f"{P.BPM:.0f} BPM · mode {P.MODE} {P.RES} · {c['total']}cr",
           font=f15, fill=DIM)

    y = T + 95

    # ---- beat grid ----
    d.text((L - 55, y - 22), "BEAT", font=f11, fill=DIM)
    b = 0.0
    while b <= total + 1e-6:
        x = L + b * PX_S
        bar = abs((b / P.BEAT) % 4) < 1e-6
        d.line([(x, y - 8), (x, y + 470)], fill="#2E3442" if bar else "#1B2028", width=2 if bar else 1)
        b += P.BEAT

    # ---- hook window ----
    hx = L + 2.0 * PX_S
    d.rectangle([L, y - 6, hx, y + 400], outline="#C4562F", width=2)
    d.text((hx + 10, y - 24), "^ 2.00s — the event must be OVER inside this box",
           font=f13, fill="#C4562F")

    # ---- shot lane ----
    lane_y, lane_h = y + 20, 96
    for i, ((s, cr, kind, note), (st, dur, _k)) in enumerate(zip(P.SHOTS, tl)):
        x0 = L + st * PX_S
        x1 = L + (st + dur) * PX_S
        col = P.SOURCES[s][1]
        d.rectangle([x0 + 2, lane_y, x1 - 2, lane_y + lane_h], fill=col)
        th = _thumb(name, P, s)
        if th is not None:
            w_box = max(4, int(x1 - x0 - 4))
            tw_, th_ = th.size
            crop_w = int(th_ * (w_box / lane_h))
            if crop_w <= tw_:
                x_c = (tw_ - crop_w) // 2
                t2 = th.crop((x_c, 0, x_c + crop_w, th_)).resize((w_box, lane_h))
            else:
                t2 = th.resize((w_box, lane_h))
            im.paste(t2, (int(x0 + 2), int(lane_y)))
            d.rectangle([x0 + 2, lane_y, x1 - 2, lane_y + lane_h], outline=col, width=3)
        d.text((x0 + 9, lane_y + 7), f"{i}", font=f13, fill="#0C0E12")
        d.text((x0 + 8, lane_y + 6), f"{i}", font=f13, fill="#FFFFFF")
        d.text((x0 + 9, lane_y + 25), s, font=f18, fill="#0C0E12")
        d.text((x0 + 8, lane_y + 24), s, font=f18, fill="#FFFFFF")
        if dur > 0.7:
            d.text((x0 + 8, lane_y + 48), note[:22], font=f11, fill="#12141A")
        d.text((x0 + 8, lane_y + lane_h - 18),
               f"{cr:.2f}x" + ("" if kind == "burst" else f" {kind}"), font=f11, fill="#12141A")
        if i in P.BLEND_AFTER:
            d.rectangle([x1 - 8, lane_y, x1 + 8, lane_y + lane_h], fill="#F2F4F8")
            d.text((x1 - 6, lane_y + lane_h + 4), "blend", font=f11, fill=INK)

    d.text((L - 55, lane_y + 30), "SHOT", font=f11, fill=DIM)

    # ---- act lane ----
    ay = lane_y + lane_h + 34
    d.text((L - 55, ay + 6), "ACT", font=f11, fill=DIM)
    for (s, _cr, _k, _n), (st, dur, _kk) in zip(P.SHOTS, tl):
        x0, x1 = L + st * PX_S, L + (st + dur) * PX_S
        act = P.SOURCES[s][2]
        shade = {"EVENT": "#C4562F", "EXTERIOR": "#3A4757", "INTERIOR": "#4A3F57",
                 "HUMAN": "#7B3F6B", "PAYOFF": "#8C3B3B"}.get(act.upper(), "#2A303C")
        d.rectangle([x0 + 2, ay, x1 - 2, ay + 26], fill=shade)
        if dur > 1.2:
            d.text((x0 + 8, ay + 6), act, font=f11, fill=INK)

    # ---- sfx lane ----
    sy = ay + 46
    d.text((L - 55, sy + 6), "SFX", font=f11, fill=DIM)
    d.line([(L, sy + 14), (L + tw, sy + 14)], fill=LINE, width=1)
    for i, (st, dur, _k) in enumerate(tl):
        if i == 0:
            continue
        x = L + st * PX_S
        lead = x - P.SFX_LEAD * PX_S
        if i in P.IMPACT_AT:
            tag, col = "IMPACT", "#E0B341"
        elif i in P.SUBDROP_AT:
            tag, col = "sub", "#5B8C5A"
        elif _edit_sfx == "full":
            tag, col = "whoosh", "#4A6FA5"
        else:
            # hero_only / none: NO transient design on ordinary cuts. Drawing a whoosh
            # here was WRX boilerplate - it printed a whoosh on all 19 cuts of a plan
            # whose entire subject is silence. The board must not contradict the style.
            continue
        d.line([(lead, sy + 6), (x, sy + 22)], fill=col, width=3)
        d.text((lead - 2, sy + 26), tag, font=f11, fill=col)
    _sfx_note = (f"whoosh LEADS the cut by {P.SFX_LEAD*1000:.0f}ms — it RESOLVES on the cut, "
                 f"it does not start there. Bed sidechain-ducks under it."
                 if _edit_sfx == "full" else
                 f"edit_sfx = {_edit_sfx.upper()} — NO transient design on ordinary cuts. "
                 f"The marked beat is the only designed sound in the video.")
    d.text((L, sy + 44), _sfx_note, font=f13, fill=DIM)

    # ---- card lane ----
    cy = sy + 80
    d.text((L - 55, cy + 6), "TEXT", font=f11, fill=DIM)
    for t, first, n, kind in P.CARDS:
        st = tl[first][0]
        en = tl[min(first + n - 1, len(tl) - 1)]
        x0, x1 = L + st * PX_S, L + (en[0] + en[1]) * PX_S
        col = "#E0B341" if kind == "cta" else "#F2F4F8"
        d.rectangle([x0 + 2, cy, x1 - 2, cy + 30], outline=col, width=2)
        d.text((x0 + 10, cy + 7), t, font=f15, fill=col)
    d.text((L, cy + 38), f"all cards y={P.CARD_Y} — LOWER THIRD. Never centre: the car lives there.",
           font=f13, fill=DIM)

    # ---- legend ----
    gy = cy + 80
    d.line([(L, gy - 14), (W - L, gy - 14)], fill=LINE, width=1)
    d.text((L, gy), "SOURCES — one generation each, 5s, std 720p", font=f18, fill=INK)
    use = {}
    for s, _c, _k, _t in P.SHOTS:
        use[s] = use.get(s, 0) + 1
    col_x = [L, L + 760, L + 1520]
    for n, (k, (lab, col, act, plates, _p)) in enumerate(P.SOURCES.items()):
        cx = col_x[n // 3]
        ry = gy + 34 + (n % 3) * 46
        d.rectangle([cx, ry, cx + 26, ry + 26], fill=col)
        _t = _thumb(name, P, k)
        if _t is not None:
            im.paste(_t.resize((26, 26)), (int(cx), int(ry)))
            d.rectangle([cx, ry, cx + 26, ry + 26], outline=col, width=2)
        d.text((cx + 36, ry + 1), f"{k}   {lab}", font=f15, fill=INK)
        d.text((cx + 36, ry + 18), f"{act} · plates: {', '.join(plates)} · used {use.get(k,0)}x",
               font=f11, fill=DIM)

    # ---- footer ----
    fy = H - 92
    d.line([(L, fy - 16), (W - L, fy - 16)], fill=LINE, width=1)
    need = -(-len(P.SHOTS) // 2.5)
    d.text((L, fy),
           f"COVERAGE {len(P.SOURCES)} sources / {len(P.SHOTS)} shots (need >= {int(need)}) · "
           f"crop cap {P.MAX_CROP}x · blends {len(P.BLEND_AFTER)}/{len(P.SHOTS)-1} · "
           f"grade sat {P.GRADE_SAT} toward black {P.TARGET_BLACK} / sat {P.TARGET_SAT}",
           font=f13, fill=DIM)
    d.text((L, fy + 22),
           f"PROBE: plates + shot {P.PROBE_FIRST} = {c['probe']}cr, LOOK at it, then commit "
           f"{c['after_probe']}cr for the remaining {c['clips']-1} clips.  TOTAL {c['total']}cr",
           font=f13, fill="#E0B341")
    d.text((L, fy + 44),
           "AI label is NOT burned in — it is a platform toggle at upload, and therefore a HUMAN step.",
           font=f13, fill=DIM)

    out = out or os.path.join(HERE, "projects", name, "analysis", "STORYBOARD.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)
    print(f"{out}  {im.size[0]}x{im.size[1]}")
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "supra")
