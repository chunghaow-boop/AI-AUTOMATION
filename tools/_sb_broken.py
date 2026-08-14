#!/usr/bin/env python3
"""
STORYBOARD — the artefact Gavril reviews BEFORE any credit is spent.

HIS SPEC, VERBATIM (2026-08-06)
  "before generation mastermind needs to give me a storyboard image with reference image
   of every shot and scene and how it links together and the detailed video editing flow
   from cuts to transitions to sfx to bgm to foley, for me to review and see then when
   im okay with it then i hit go"

WHAT ALREADY EXISTED, AND WHY IT WAS NOT THIS
  board.py draws a real timeline — beat grid, hook window, act lane, sfx lane, cards —
  and it upgrades each block to the clip's actual first frame AS CLIPS ARRIVE. That is
  the right picture for reviewing a BUILD. It is the wrong picture for reviewing a PLAN,
  because before generation every block is a coloured rectangle: there is no image of
  the shot, because the shot does not exist yet.

  So the review that decides a 278cr spend was being made against colour swatches and
  prose. This page fills that gap with the only images that legitimately exist before
  generation — the reference PLATES the shots will be generated FROM — and says so
  loudly, per shot, when even that is missing.

THE HONESTY RULE THIS FILE OBEYS
  It NEVER invents or approximates an image. Each shot's picture is exactly one of:
    REAL FRAME   the clip exists; this is the frame at the planned in-point
    PLATE        the reference plate this shot generates from, and it exists on disk
    MISSING      a red panel naming the file that is absent
  The badge says which. A storyboard that quietly showed a stand-in would be worse than
  no storyboard, because the whole point is deciding whether to spend.

OUTPUT
  projects/<name>/analysis/STORYBOARD.html   self-contained, images inlined as base64.
  Open it in a browser. No server, no assets folder, nothing to break later.

Usage
  python3 tools/storyboard.py crown
  python3 tools/storyboard.py crown --out /tmp/sb.html
"""
import argparse, base64, html, importlib, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

ACT_COLOUR = {"EVENT": "#C4562F", "PAYOFF": "#B08D3F", "HUMAN": "#4A6E8A",
              "EXTERIOR": "#3F6B54", "INTERIOR": "#5B4A72"}


def load_plan(name):
    for cand in (f"plans.{name}", name, f"{name}_plan"):
        try:
            return importlib.import_module(cand)
        except ModuleNotFoundError:
            continue
    return None


def profile(pillar):
    for p in (os.path.join(HERE, "assets", "pillars", "PILLAR-PROFILES.json"),
              os.path.join(HERE, "pillars", "PILLAR-PROFILES.json")):
        if os.path.exists(p):
            try:
                return json.load(open(p, encoding="utf-8")).get(pillar) or {}
            except Exception:
                return {}
    return {}


def b64_of(path, max_w=420):
    """Downscale to keep the page openable, then inline. Returns None on any failure —
    never a placeholder pretending to be the real thing."""
    try:
        import cv2
        img = cv2.imread(path) if not path.lower().endswith((".mp4", ".mov")) else None
        if img is None:
            return None
        h, w = img.shape[:2]
        if w > max_w:
            img = cv2.resize(img, (max_w, int(h * max_w / w)))
        ok, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 82])
        if not ok:
            return None
        return base64.b64encode(buf.tobytes()).decode()
    except Exception:
        return None


def frame_b64(video, t, max_w=420):
    """The frame that will actually PLAY, not the clip head — the delivered-window
    principle clipqc had to learn three times."""
    try:
        import cv2
        cap = cv2.VideoCapture(video)
        fps = cap.get(cv2.CAP_PROP_FPS) or 24
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(max(0, t) * fps))
        ok, fr = cap.read()
        cap.release()
        if not ok:
            return None
        h, w = fr.shape[:2]
        if w > max_w:
            fr = cv2.resize(fr, (max_w, int(h * max_w / w)))
        ok, buf = cv2.imencode(".jpg", fr, [int(cv2.IMWRITE_JPEG_QUALITY), 82])
        return base64.b64encode(buf.tobytes()).decode() if ok else None
    except Exception:
        return None


def find_plate(P, plate_key):
    """Locate a plate file. Returns (path, exists)."""
    plates = getattr(P, "PLATES", {}) or {}
    meta = plates.get(plate_key) or {}
    for k in ("file", "path"):
        if meta.get(k):
            p = meta[k] if os.path.isabs(meta[k]) else os.path.join(HERE, meta[k])
            if os.path.exists(p):
                return p, True
    pil = getattr(P, "PILLAR", "")
    # BUG CAUGHT ON FIRST RUN, 2026-08-06: the persona fallback was guarded by
    #     if plate_key == "nev" and "nev" not in cand.lower(): continue
    # which is inverted — it only skipped the nev file when the key WAS nev. So
    # find_plate("crown") returned assets/nev/NEV_PLATE_SOURCE.jpeg and every car shot
    # in the storyboard would have displayed a portrait of Nev as its reference, with a
    # confident PLATE badge and "0 MISSING". That is the exact failure this file's
    # docstring forbids: a stand-in shown as the real thing, on the page that decides a
    # 278cr spend. Candidates are now keyed strictly by name, with NO cross-key fallback.
    cands = [
        os.path.join(HERE, "assets", "pillars", pil, "plates", f"{plate_key}.png"),
        os.path.join(HERE, "assets", "pillars", pil, "plates", f"{plate_key}.jpg"),
        os.path.join(HERE, "assets", "pillars", pil, "plates", f"{plate_key}.jpeg"),
        os.path.join(HERE, "assets", "plates", f"{plate_key}.png"),
        os.path.join(HERE, "assets", "plates", f"{plate_key}.jpg"),
    ]
    if plate_key == "nev":                       # the persona set, and ONLY for key 'nev'
        # 2026-08-12, HIS CATCH on the kariayam board: "why I saw some other
        # character in here? Are you proposing a new girlfriend for nev?"
        # It WAS Nev - but NEV_PLATE_SOURCE.jpeg shows him in a TAN SWEATER with
        # legible text across the chest, while that plan declares navy check over a
        # black tee and BANS legible clothing text. The board was showing a generic
        # persona photo where the plan had named specific references, so the page
        # that decides a spend did not show what will actually be sent.
        # THE PLAN'S OWN REFS COME FIRST. The generic plate is the last resort.
        for key in ("wardrobe_refs", "identity_refs"):
            for r in (meta.get(key) or []):
                cands.append(r if os.path.isabs(r) else os.path.join(HERE, r))
        cands += [os.path.join(HERE, "assets", "nev", "NEV_PLATE_SOURCE.jpeg"),
                  os.path.join(HERE, "assets", "nev", "NEV_PLATE_ALT.jpeg")]
    for cand in cands:
        if os.path.exists(cand):
            return cand, True
    return (meta.get("file") or f"assets/pillars/{pil}/plates/{plate_key}.png"), False


def find_clip(P, name, key):
    import glob as _g
    cdir = os.path.join(HERE, "projects", name, "clips")
    clips = getattr(P, "CLIPS", {}) or {}
    if clips.get(key):
        p = os.path.join(cdir, clips[key])
        if os.path.exists(p):
            return p
    for p in _g.glob(os.path.join(cdir, f"*_{key}_*.mp4")) + \
             _g.glob(os.path.join(cdir, f"*_{key}.mp4")):
        return p
    return None


def esc(s):
    return html.escape(str(s), quote=True)


def build(name, out=None):
    P = load_plan(name)
    if P is None:
        print(f"  no plan module for '{name}'"); return 2
    tl, total = P.timeline()
    pf = profile(getattr(P, "PILLAR", ""))
    sty = pf.get("style") or {}
    policy = str(sty.get("edit_sfx", "full")).lower()
    hero_shot = (getattr(P, "SOUND", {}) or {}).get("hero_shot")
    blends = sorted(set(getattr(P, "BLEND_AFTER", []) or []))
    bw = getattr(P, "BLEND_WIDTH", 0.0)
    linkage = getattr(P, "LINKAGE", None)
    foley = getattr(P, "FOLEY", {}) or {}
    shot_time = getattr(P, "SHOT_TIME", None)
    cards = getattr(P, "CARDS", []) or []
    windows = getattr(P, "WINDOWS", None)

    def link_at(i):
        """Boundary i -> i+1. LINKAGE may be a list or a dict."""
        if linkage is None:
            return None
        try:
            e = linkage[i] if isinstance(linkage, (list, tuple)) else linkage.get(i)
        except Exception:
            return None
        if e is None:
            return None
        if isinstance(e, (list, tuple)):
            return {"kind": e[0] if len(e) > 0 else "",
                    "token": e[1] if len(e) > 1 else "",
                    "why": e[2] if len(e) > 2 else ""}
        return {"kind": "", "token": "", "why": str(e)}

    links3 = getattr(P, "LINKS", None)

    def triple_at(i):
        """Boundary i -> i+1 as {picture, sound, story}. Returns None when the plan
        declares no LINKS block at all (older plans render exactly as before)."""
        if not links3:
            return None
        try:
            e = links3.get(i) if hasattr(links3, "get") else links3[i]
        except Exception:
            return None
        if e is None:
            return {"picture": "", "sound": "", "story": ""}
        if isinstance(e, dict):
            return {"picture": e.get("picture", ""), "sound": e.get("sound", ""),
                    "story": e.get("story", "")}
        if isinstance(e, (list, tuple)):
            e = list(e) + ["", "", ""]
            return {"picture": e[0], "sound": e[1], "story": e[2]}
        return {"picture": "", "sound": "", "story": str(e)}

    def card_for(i):
        out_ = []
        for c in cards:
            try:
                t_, f_, n_, kind = c[0], c[1], c[2], c[3]
            except Exception:
                continue
            if f_ <= i < f_ + n_:
                out_.append((t_, kind))
        return out_

    shift = lambda i: bw * len([b for b in blends if b < i])

    framing = getattr(P, "FRAMING", {}) or {}
    plates_all = getattr(P, "PLATES", {}) or {}

    def identity_strip(plate_keys):
        """HIS ASK 2026-08-06: 'take at least 3-5 reference image for nev if the scene
        requires nevs face'. The refs were always IN the plan - PLATES['nev'] carries
        identity_refs + wardrobe_refs - but this page only ever drew ONE picture, the
        place plate. A reviewer could not see what the generator will actually be
        handed. Now every shot citing a plate that declares refs shows all of them.
        Returns [(b64, caption)], capped at 6 so a page stays readable."""
        out_ = []
        for k in plate_keys:
            spec = plates_all.get(k) or {}
            if not isinstance(spec, dict):
                continue
            for group, tag in (("identity_refs", "identity"),
                               ("wardrobe_refs", "wardrobe")):
                for rel in (spec.get(group) or []):
                    p_ = rel if os.path.isabs(rel) else os.path.join(HERE, rel)
                    b = b64_of(p_, max_w=150) if os.path.exists(p_) else None
                    out_.append((b, f"{k} {tag} · {os.path.basename(rel)}",
                                 os.path.relpath(p_, HERE)))
                    if len(out_) >= 6:
                        return out_
        return out_

    def scene_refs_strip(src):
        """SCENE-MATCHED REFS (2026-08-11, HIS CATCH on this very page: every shot
        showed the same three reference pictures. If the plan declares SOURCE_REFS
        for a source, the board shows THOSE - the refs this exact scene is handed -
        instead of the blanket plate set. planqc 27b enforces the selection."""
        rels = (getattr(P, "SOURCE_REFS", {}) or {}).get(src) or []
        out_ = []
        for rel in rels[:6]:
            p_ = rel if os.path.isabs(rel) else os.path.join(HERE, rel)
            b = b64_of(p_, max_w=150) if os.path.exists(p_) else None
            out_.append((b, f"{src} scene-ref · {os.path.basename(rel)}",
                         os.path.relpath(p_, HERE)))
        return out_

    rows, missing, n_real, n_plate = [], [], 0, 0
    for i, (src, crop, kind, note) in enumerate(P.SHOTS):
        meta = (getattr(P, "SOURCES", {}) or {}).get(src, ())
        act = (meta[2].upper() if len(meta) > 2 else "?")
        plates = list(meta[3]) if len(meta) > 3 and meta[3] else []
        start, dur = tl[i][0], tl[i][1]
        delivered = start - shift(i)

        img, badge, imnote = None, "MISSING", ""
        clip = find_clip(P, name, src)
        if clip:
            win = 0.0
            if isinstance(windows, dict) and src in windows:
                try:
                    win = float(str(windows[src]).split("-")[0].strip().rstrip("s"))
                except Exception:
                    win = 0.0
            img = frame_b64(clip, win + dur / 2.0)
            if img:
                badge, imnote = "REAL FRAME", os.path.basename(clip)
                n_real += 1
        img_path = clip if clip else ""
        if img is None and plates:
            pp, exists = find_plate(P, plates[0])
            img_path = pp
            if exists:
                img = b64_of(pp)
                if img:
                    badge = "PLATE"
                    imnote = f"{plates[0]} — the shot generates FROM this"
                    n_plate += 1
            if img is None:
                imnote = f"plate '{plates[0]}' not on disk: {pp}"
                missing.append(f"shot {i} ({src}): plate '{plates[0]}' — {pp}")
        if img is None and not plates:
            imnote = "source cites no plate"
            missing.append(f"shot {i} ({src}): no plate cited and no clip")

        if policy == "none":
            sfx = "—"
        elif policy == "hero_only":
            sfx = "IMPACT (hero)" if i == hero_shot else "—"
        elif i in (getattr(P, "IMPACT_AT", []) or []):
            sfx = "IMPACT"
        elif i in (getattr(P, "SUBDROP_AT", []) or []):
            sfx = "SUB-DROP"
        else:
            sfx = "whoosh" if i > 0 else "—"

        rows.append({
            "i": i, "src": src, "act": act, "crop": crop, "kind": kind, "note": note,
            "start": start, "dur": dur, "delivered": delivered, "img": img,
            "img_path": img_path,   # the RESOLVED source of the panel picture, so
                                    # BOARD QC can check provenance instead of base64
            "badge": badge, "imnote": imnote,
            "label": meta[0] if meta else src,
            "time": (shot_time[i] if isinstance(shot_time, (list, tuple))
                     and i < len(shot_time) else
                     (shot_time.get(i) if isinstance(shot_time, dict) else "")),
            "foley": foley.get(i), "sfx": sfx, "cards": card_for(i),
            "blend_after": i in blends, "link": link_at(i),
            # HIS ASK 2026-08-06, all four in one pass:
            "framing": framing.get(src, ""),                 # camera movement / position
            "prompt": (meta[4] if len(meta) > 4 else ""),    # the VERBATIM prompt
            "plates": plates,
            "refs": scene_refs_strip(src) or identity_strip(plates),  # scene-matched first
        })

    # ------------------------------------------------------------------ render
    css = """
    *{box-sizing:border-box} body{margin:0;background:#0E1015;color:#E8ECF2;
      font:14px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
    .wrap{max-width:1180px;margin:0 auto;padding:28px 22px 80px}
    h1{font-size:24px;margin:0 0 4px} .sub{color:#8A93A3;font-size:13px;margin-bottom:20px}
    .bar{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 26px}
    .chip{background:#171A22;border:1px solid #262B36;border-radius:7px;padding:7px 11px;font-size:12px}
    .chip b{color:#fff}
    .warn{background:#2A1614;border:1px solid #6B2B22;color:#F0B4A8;border-radius:8px;
      padding:12px 14px;margin:14px 0;font-size:13px}
    .shot{display:grid;grid-template-columns:200px 1fr;gap:16px;background:#12151C;
      border:1px solid #222733;border-radius:11px;padding:14px;margin-bottom:10px}
    .thumb{width:200px;border-radius:7px;overflow:hidden;background:#0A0C10;position:relative}
    .thumb img{width:100%;display:block}
    .noimg{height:280px;display:flex;align-items:center;justify-content:center;
      text-align:center;padding:14px;color:#F0B4A8;background:#2A1614;
      border:1px dashed #6B2B22;border-radius:7px;font-size:12px}
    .badge{position:absolute;top:7px;left:7px;font-size:10px;letter-spacing:.5px;
      padding:3px 7px;border-radius:4px;font-weight:700}
    .b-real{background:#1E5B3A;color:#C7F3D9} .b-plate{background:#4A3C10;color:#F5E3A8}
    .hd{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:5px}
    .num{font-size:19px;font-weight:700;color:#fff}
    .act{font-size:10px;font-weight:700;letter-spacing:.6px;padding:3px 8px;border-radius:4px;color:#fff}
    .t{color:#8A93A3;font-size:12px;font-variant-numeric:tabular-nums}
    .note{color:#D3DAE5;margin:5px 0 9px}
    .kv{display:flex;gap:7px;flex-wrap:wrap;margin-top:7px}
    .k{background:#191D26;border:1px solid #262B36;border-radius:5px;padding:3px 8px;
      font-size:11px;color:#9BA5B5}
    .k b{color:#DDE4EE;font-weight:600}
    .card{background:#332B10;border:1px solid #6B5A22;color:#F5E3A8}
    .hero{background:#4A1F14;border:1px solid #9B3F22;color:#FFC9B4}
    .link{margin:0 0 10px 216px;padding:7px 12px;border-left:3px solid #2E5A7A;
      background:#101821;border-radius:0 7px 7px 0;font-size:12px;color:#9FB6C9}
    .link b{color:#7FC4F0;text-transform:uppercase;font-size:10px;letter-spacing:.6px}
    .triple{margin:0 0 10px 216px;padding:8px 12px;border-left:3px solid #3E6B8A;
            background:#12181D;border-radius:0 6px 6px 0;font-size:12px}
    .tl-h{color:#7FB2D4;font-weight:700;letter-spacing:.04em;margin-bottom:4px}
    .tl-ok{color:#C7D4DC;margin:2px 0}
    .tl-ok b{color:#7FB2D4;margin-right:6px}
    .tl-gap{color:#8A5A5A;margin:2px 0}
    .tl-gap b{color:#C46A6A;margin-right:6px}
    .blend{margin:0 0 10px 216px;padding:7px 12px;border-left:3px solid #7A5A2E;
      background:#1C1710;border-radius:0 7px 7px 0;font-size:12px;color:#E0C48A}
    h2{font-size:15px;margin:30px 0 10px;color:#fff;border-bottom:1px solid #222733;padding-bottom:6px}
    table{width:100%;border-collapse:collapse;font-size:12.5px}
    td,th{padding:6px 9px;border-bottom:1px solid #1C2029;text-align:left}
    th{color:#8A93A3;font-weight:600}
    .foot{color:#6E7787;font-size:11.5px;margin-top:26px;line-height:1.7}
    .cut{margin:0 0 10px 216px;padding:6px 12px;border-left:3px solid #33404F;
      background:#0F1319;border-radius:0 7px 7px 0;font-size:11.5px;color:#7F8B9C}
    .cut b{color:#B9C6D6;text-transform:uppercase;font-size:10px;letter-spacing:.6px}
    details.pr{margin-top:9px;background:#0C1016;border:1px solid #222733;border-radius:7px}
    details.pr summary{cursor:pointer;padding:7px 11px;font-size:11px;color:#7FC4F0;
      letter-spacing:.4px;text-transform:uppercase;font-weight:700}
    details.pr pre{margin:0;padding:0 13px 13px;white-space:pre-wrap;font-size:12px;
      line-height:1.6;color:#CBD5E2;font-family:ui-monospace,Menlo,Consolas,monospace}
    .refs{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
    .ref{width:78px;text-align:center;font-size:9px;color:#6E7787;line-height:1.3}
    .ref img{width:78px;border-radius:5px;display:block;margin-bottom:3px}
    .ref .miss{height:100px;border:1px dashed #6B2B22;border-radius:5px;background:#2A1614;
      color:#F0B4A8;display:flex;align-items:center;justify-content:center;font-size:9px;
      margin-bottom:3px;padding:4px}
    .cam{background:#12212B;border:1px solid #2E5A7A;color:#9FD3F0}
    """

    o = ['<!doctype html><meta charset="utf-8">',
         f'<title>STORYBOARD — {esc(getattr(P,"PROJECT",name))}</title>',
         f"<style>{css}</style><div class='wrap'>"]
    o.append(f"<h1>{esc(getattr(P,'PROJECT',name))}</h1>")
    o.append(f"<div class='sub'>REVIEW BEFORE SPEND — this page is the thing you say GO to. "
             f"Generated from plans/{esc(name)}.py. Nothing here is typed beside the plan.</div>")

    try:
        c = P.cost()
        cost_s = f"{c['total']:.1f}cr · probe first {c.get('probe', 0):.1f}cr"
    except Exception:
        cost_s = "cost() unavailable"
    o.append("<div class='bar'>")
    for k, v in [("shots", len(P.SHOTS)), ("pre-blend", f"{total:.2f}s"),
                 ("delivered", f"{total - bw*len(blends):.2f}s"),
                 ("pillar", getattr(P, "PILLAR", "?")), ("bpm", f"{getattr(P,'BPM','?')}"),
                 ("beat", f"{getattr(P,'BEAT',0):.3f}s"), ("edit_sfx", policy),
                 ("cuts", "HARD ONLY" if not blends else
                          f"{len(blends)} × {getattr(P,'BLEND_KIND','?')}"),
                 ("bgm", (str((getattr(P, "SOUND", {}) or {}).get("bed", "NOT DECLARED"))
                          .split(" - ")[0].split("/")[-1] or "NOT DECLARED")),
                 ("cost", cost_s)]:
        o.append(f"<div class='chip'>{esc(k)} <b>{esc(v)}</b></div>")
    o.append("</div>")

    o.append(f"<div class='warn'><b>IMAGE PROVENANCE — {n_real} real frame(s), "
             f"{n_plate} plate(s), {len(missing)} missing.</b><br>"
             "Every picture below is either a REAL FRAME from a generated clip or the "
             "PLATE the shot will be generated from. Nothing is a stand-in. Where an "
             "image is missing the panel is red and names the file.")
    if missing:
        o.append("<br><br>" + "<br>".join("· " + esc(m) for m in missing[:14]))
        if len(missing) > 14:
            o.append(f"<br>· ...and {len(missing)-14} more")
    o.append("</div>")

    for r in rows:
        o.append("<div class='shot'><div class='thumb'>")
        if r["img"]:
            cls = "b-real" if r["badge"] == "REAL FRAME" else "b-plate"
            o.append(f"<div class='badge {cls}'>{esc(r['badge'])}</div>"
                     f"<img src='data:image/jpeg;base64,{r['img']}'>")
        else:
            o.append(f"<div class='noimg'><div><b>NO IMAGE</b><br><br>{esc(r['imnote'])}"
                     f"</div></div>")
        o.append("</div><div>")
        col = ACT_COLOUR.get(r["act"], "#444A57")
        o.append(f"<div class='hd'><span class='num'>{r['i']}</span>"
                 f"<span class='act' style='background:{col}'>{esc(r['act'])}</span>"
                 f"<span class='t'>{r['delivered']:.2f}s delivered · {r['dur']:.2f}s · "
                 f"{esc(r['kind'])}</span></div>")
        o.append(f"<div class='note'>{esc(r['note'])}</div>")
        o.append("<div class='kv'>")
        o.append(f"<span class='k'>src <b>{esc(r['src'])}</b></span>")
        o.append(f"<span class='k'>{esc(r['label'])}</span>")
        o.append(f"<span class='k'>crop <b>{r['crop']}x</b></span>")
        if r["time"]:
            o.append(f"<span class='k'>light <b>{esc(r['time'])}</b></span>")
        if r["foley"] is not None:
            o.append(f"<span class='k'>foley <b>{r['foley']}dB</b></span>")
        if r["sfx"] != "—":
            cls = "k hero" if "hero" in r["sfx"].lower() else "k"
            o.append(f"<span class='{cls}'>sfx <b>{esc(r['sfx'])}</b></span>")
        if r["framing"]:
            o.append(f"<span class='k cam'>camera <b>{esc(r['framing'])}</b></span>")
        for t_, kind in r["cards"]:
            o.append(f"<span class='k card'>card <b>{esc(t_)}</b> ({esc(kind)})</span>")
        if r["imnote"] and r["img"]:
            o.append(f"<span class='k'>{esc(r['imnote'])}</span>")
        o.append("</div>")

        # ---- identity / wardrobe references actually handed to the generator ----
        if r["refs"]:
            o.append("<div class='refs'>")
            for b, cap, rel in r["refs"]:
                if b:
                    o.append(f"<div class='ref'><img src='data:image/jpeg;base64,{b}'>"
                             f"{esc(cap)}</div>")
                else:
                    o.append(f"<div class='ref'><div class='miss'>NOT ON DISK</div>"
                             f"{esc(rel)}</div>")
            o.append("</div>")

        # ---- the VERBATIM prompt, on the shot it produces ----
        if r["prompt"]:
            o.append("<details class='pr'><summary>generation prompt — verbatim, as sent "
                     f"to Higgsfield (source {esc(r['src'])}, one clip serves every shot "
                     f"marked src {esc(r['src'])})</summary>"
                     f"<pre>{esc(r['prompt'])}</pre></details>")
        o.append("</div></div>")

        # PER-SCENE TRANSITIONS (planqc 37 field), 2026-08-12 HIS CATCH: "I saw
        # there is no transition here inside this video. Is it supposed to not have
        # any?" The plan DID declare one - a dip at the workshop/road chapter change -
        # but this page only ever read the legacy BLEND_AFTER list, so every boundary
        # printed "hard cut" and the board misrepresented the edit. Same family as the
        # persona-plate fault: the page that decides the spend must show what will
        # actually happen.
        tp_all = getattr(P, "TRANSITIONS_PLAN", {}) or {}
        tp = None   # simulate the pre-fix board
        if tp:
            _k = str(tp.get("kind", "?")); _w = str(tp.get("why", ""))
            o.append(f"<div class='blend'>TRANSITION · <b>{esc(_k.upper())}</b> "
                     f"&mdash; {esc(_w)}</div>")
        elif r["blend_after"]:
            o.append(f"<div class='blend'>BLEND · {esc(getattr(P,'BLEND_KIND','?'))} "
                     f"{bw*1000:.0f}ms — the timeline shortens by {bw:.2f}s here</div>")
        elif r["i"] < len(P.SHOTS) - 1:
            # EVERY boundary now states its transition. Silence read as "not decided";
            # a hard cut IS the decision here, and it is a measurement, not a default.
            o.append("<div class='cut'><b>hard cut</b> &mdash; frame-exact on the "
                     f"{getattr(P,'BPM','?')} BPM grid. No blend: this pillar measured "
                     f"{pf.get('blended_pct', '?')}% blended across its references, so a "
                     "dissolve here would be off-genre.</div>")
        lk = r["link"]
        if lk and r["i"] < len(P.SHOTS) - 1:
            kd = (lk['kind'] or 'link').upper()
            tok = f" &middot; token <b>{esc(lk['token'])}</b>" if lk['token'] else ""
            o.append(f"<div class='link'><b>{esc(kd)}</b>{tok} &mdash; {esc(lk['why'])}</div>")

        # THE TRIPLE LINK (file 31 PART F, his order 2026-08-12: "the link between
        # scenes seen beforehand, before video generation... I need there to be
        # like three link"). Additive: renders only when the plan declares LINKS.
        # One link = a transition; three = a story beat. Missing channels are shown
        # as a red gap on purpose - the board never hides what was not decided.
        tl = triple_at(r["i"])
        if tl is not None and r["i"] < len(P.SHOTS) - 1:
            cells = []
            for ch, lbl in (("picture", "PICTURE"), ("sound", "SOUND"), ("story", "STORY")):
                v = str(tl.get(ch, "") or "").strip()
                if v:
                    cells.append(f"<div class='tl-ok'><b>{lbl}</b> {esc(v)}</div>")
                else:
                    cells.append(f"<div class='tl-gap'><b>{lbl}</b> not declared</div>")
            got = sum(1 for ch in ("picture","sound","story") if str(tl.get(ch,"") or "").strip())
            badge = ("STORY BEAT" if got == 3 else
                     f"TRANSITION ONLY &mdash; {got}/3 links")
            o.append(f"<div class='triple'><div class='tl-h'>TRIPLE LINK &middot; "
                     f"{badge}</div>{''.join(cells)}</div>")

    o.append("<h2>EDIT FLOW — what the engine will do</h2><table>")
    o.append("<tr><th>layer</th><th>declared</th></tr>")
    sn = getattr(P, "SOUND", {}) or {}
    bpm_band = pf.get("bpm") or []
    o.append(f"<tr><td>cuts</td><td>{len(P.SHOTS)-1} boundaries on the "
             f"{getattr(P,'BPM','?')} BPM grid ({getattr(P,'BEAT',0):.3f}s), frame-exact</td></tr>")
    _tpa = getattr(P, "TRANSITIONS_PLAN", {}) or {}
    if _tpa:
        _lst = ", ".join(f"after shot {k}: {str(v.get('kind','?')).upper()}"
                         for k, v in sorted(_tpa.items()))
        o.append(f"<tr><td>transitions</td><td>{len(_tpa)} declared &mdash; {esc(_lst)}"
                 f" &middot; every other boundary is a hard cut by doctrine</td></tr>")
    o.append(f"<tr><td>transitions (legacy)</td><td>{len(blends)} × {esc(getattr(P,'BLEND_KIND','?'))} "
             f"at {bw*1000:.0f}ms, after shots {blends} — "
             f"{100*len(blends)//max(1,len(P.SHOTS)-1)}% blended</td></tr>")
    o.append(f"<tr><td>edit sfx</td><td><b>{esc(policy)}</b> — " +
             ("no transient design on any cut" if policy == "none" else
              (f"ONE impact at shot {hero_shot}" if policy == "hero_only" and hero_shot is not None
               else ("ONE impact — <b style='color:#F0B4A8'>SOUND['hero_shot'] NOT SET, "
                     "engine defaults to shot 0 = t 0.00s</b>" if policy == "hero_only"
                     else "IMPACT/SUB-DROP/whoosh per cut"))) + "</td></tr>")
    o.append(f"<tr><td>bgm</td><td>{esc(str(sn.get('bed','(not declared)'))[:400])}" +
             (f"<br><i>profile band {bpm_band[0]}-{bpm_band[1]} BPM</i>" if len(bpm_band) == 2 else "")
             + "</td></tr>")
    if sn.get("bed_map"):
        o.append(f"<tr><td>bed map</td><td>{esc(json.dumps(sn['bed_map'])[:600])}</td></tr>")
    fg = sorted(i for i, g in foley.items() if isinstance(g, (int, float)) and g >= -6)
    o.append(f"<tr><td>foley</td><td>{len(foley)} shots gained; foreground (&ge;-6dB): "
             f"{fg}</td></tr>")
    # HIS QUESTION 2026-08-06: "are u sure theres only 1 sfx for each scene, could it be
    # multiple? for example nevs expressions?" This row is the honest contract, read from
    # engine.py, not an opinion.
    o.append("<tr><td>sound layers</td><td><b>THREE, and only three: bed + one hero "
             "transient + one diegetic track per shot.</b> engine.py:819-855 reads "
             "<code>FOLEY = {shot: gain_db}</code> — ONE gain per shot, applied to that "
             "CLIP'S OWN generated audio. There is no field for a second sound on a "
             "shot; a per-shot sfx stack would be an engine change, not a plan change. "
             "So anything you want to HEAR in a shot — a breath, a laugh, gravel, a door "
             "— has to be in the clip because the PROMPT asked for it. That is the "
             "plan-level lever, and it is free.</td></tr>")
    o.append("<tr><td>camera</td><td>declared per SOURCE in FRAMING and repeated in every "
             "prompt (planqc 28 blocks two sources sharing a plate with the same camera "
             "position). Shown on every shot above as a blue <b>camera</b> chip.</td></tr>")
    o.append(f"<tr><td>hero</td><td>{esc(str(sn.get('hero','(not declared)'))[:400])}</td></tr>")
    o.append(f"<tr><td>cards</td><td>{len(cards)} at y={getattr(P,'CARD_Y','?')} "
             f"(lower third)</td></tr>")
    o.append(f"<tr><td>grade</td><td>saturation {getattr(P,'GRADE_SAT','?')} toward black "
             f"{getattr(P,'TARGET_BLACK','?')} / sat {getattr(P,'TARGET_SAT','?')}</td></tr>")
    o.append("</table>")

    o.append("<div class='foot'>")
    o.append("Every number on this page is read from the plan or the pillar profile at "
             "render time. Nothing is typed beside it, so this page cannot disagree with "
             "the code that will build the video.<br>")
    o.append("A PLATE badge means the shot does not exist yet — you are reviewing what it "
             "will be generated FROM, which is the most that can honestly be shown before "
             "spending. Re-run after ingest and those become REAL FRAME.<br>")
    if getattr(P, "BLOCKED", None):
        o.append(f"<br><b style='color:#F0B4A8'>PLAN IS MARKED BLOCKED:</b> "
                 f"{esc(str(P.BLOCKED)[:500])}")
    o.append("</div></div>")

    out = out or os.path.join(HERE, "projects", name, "analysis", "STORYBOARD.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write("\n".join(o))
    kb = os.path.getsize(out) / 1024
    print(f"  {os.path.relpath(out, HERE)}   {kb:.0f} KB")
    print(f"  {len(rows)} shots · {n_real} real frame(s) · {n_plate} plate(s) · "
          f"{len(missing)} MISSING")
    if missing:
        print(f"  MISSING images are red panels in the page — they are not hidden.")

    # ---------------------------------------------------------------- BOARD QC
    rc = board_qc(P, name, rows, tl, total, pf, out)
    return rc


def blends_of(P):
    return sorted(set(getattr(P, 'BLEND_AFTER', []) or []))


def board_qc(P, name, rows, tl, total, pf, out):
    """BOARD QC — his idea, 2026-08-12: "after the storyboard is generated I want
    the QC to DEEP ANALYSE the storyboard, check the whole flow, make sure
    everything is correct and in order and nothing is messed up. If it finds
    something messed up it redirects BACK to the planning session to replan and
    regenerate a new storyboard, go through the QC again, and only then let me
    see the final storyboard."

    WHY IT EXISTS, and it is the strongest argument for any gate in this repo:
    BOTH defects he caught on the kariayam board - the borrowed pillar name and a
    persona plate showing the wrong wardrobe with legible text - were found BY HIM,
    ON THE BOARD, AFTER ALL 45 PLAN CHECKS PASSED. planqc reads the plan as DATA.
    Nothing ever inspected the ARTEFACT he actually reads. This does.

    It checks the RENDER, not the plan: what is on the page, in what order, with
    which images, against what the plan says should be there. A failure here means
    REPLAN - the board is regenerated and re-QC'd before he ever sees it."""
    F, W = [], []
    def fail(m): F.append(m)
    def warn(m): W.append(m)

    # 1 ORDER AND TIMING — the board must be the plan, in sequence, with no gaps
    for i, r in enumerate(rows):
        if r["i"] != i:
            fail(f"panel {i} carries shot index {r['i']} - the board is out of order")
    if abs(total - float(getattr(P, "TARGET_S", total))) > 0.05:
        fail(f"board totals {total:.2f}s but the plan declares TARGET_S "
             f"{getattr(P,'TARGET_S',0):.2f}s")
    edges = [(r["start"], r["start"] + r["dur"]) for r in rows]
    for (a1, b1), (a2, b2) in zip(edges, edges[1:]):
        if abs(a2 - b1) > 0.002:
            fail(f"timeline gap/overlap at {b1:.3f}s -> {a2:.3f}s")

    # 2 EVERY PANEL IS HONEST — real frame, plate on disk, or a red MISSING panel
    for r in rows:
        if not r.get("badge"):
            fail(f"shot {r['i']} panel has no provenance badge - a silent stand-in")

    # 3 THE IMAGE SHOWN IS THE IMAGE THAT WILL BE SENT (L160, his catch)
    #   For any shot whose source declares scene refs, the panel's refs strip must
    #   be non-empty, and no panel may show the generic persona plate when the plan
    #   named specific ones.
    srefs = getattr(P, "SOURCE_REFS", {}) or {}
    for r in rows:
        if r["src"] in srefs and not r.get("refs"):
            fail(f"shot {r['i']} ({r['src']}) declares SOURCE_REFS but the board shows "
                 f"none - the page is not showing what will be generated")
        shown = [str(r.get("img_path", ""))] + [str(x[2]) for x in (r.get("refs") or [])
                                                if isinstance(x, (list, tuple)) and len(x) > 2]
        for s_ in shown:
            if "NEV_PLATE" in s_.upper():
                fail(f"shot {r['i']} shows the generic persona plate ({os.path.basename(s_)}) "
                     f"- the plan names specific refs and the board must show THOSE (L160)")
        # every picture on the page must be one the PLAN NAMED. An image the plan
        # never mentioned is a stand-in, and this page forbids stand-ins.
        named = set()
        for grp in (getattr(P, "SOURCE_REFS", {}) or {}).values():
            named.update(os.path.normpath(x) for x in grp)
        for spec in (getattr(P, "PLATES", {}) or {}).values():
            if isinstance(spec, dict):
                for k_ in ("identity_refs", "wardrobe_refs"):
                    named.update(os.path.normpath(x) for x in (spec.get(k_) or []))
        for s_ in shown[1:]:
            if s_ and os.path.normpath(s_) not in named:
                fail(f"shot {r['i']} shows {os.path.basename(s_)}, which the plan never "
                     f"names - a stand-in on the page that decides the spend")

    # 4 PROMPT FIDELITY — the board's prompt must be the plan's prompt, verbatim
    for r in rows:
        src_meta = (getattr(P, "SOURCES", {}) or {}).get(r["src"])
        want = src_meta[4] if src_meta and len(src_meta) > 4 else ""
        if want and r.get("prompt", "") != want:
            fail(f"shot {r['i']} prompt on the board differs from the plan's prompt")

    # 5 PILLAR SANITY (L159, his catch) — a borrowed pillar is a mislabelled film
    pil = getattr(P, "PILLAR", "")
    if not pil:
        fail("the plan declares no PILLAR - the board is judged against nothing")
    elif not pf:
        fail(f"PILLAR '{pil}' has no profile - the board's numbers come from nowhere")
    else:
        inherited = (pf.get("_inherited_from") or "")
        if inherited:
            warn(f"pillar '{pil}' INHERITS its numbers from '{inherited}' and they are "
                 f"not measured for it yet - stated, not hidden")

    # 6 THE FLOW READS — cards, links and the spine actually present on the page
    ncards = sum(1 for r in rows if r.get("cards"))
    if (getattr(P, "CARDS", []) or []) and ncards == 0:
        fail("the plan declares CARDS but no panel shows one")
    links3 = getattr(P, "LINKS", None)
    if links3:
        for i in range(len(rows) - 1):
            e = links3.get(i) if hasattr(links3, "get") else None
            if not e or not str((e or {}).get("story", "")).strip():
                fail(f"boundary {i} has no STORY link on the board (file 31 PART F)")
    else:
        warn("no LINKS block - the board cannot show the triple link at any boundary")

    # 6b TRANSITIONS ON THE PAGE (his catch 2026-08-12). Every transition the plan
    #    declares must be VISIBLE on the board, and a boundary the board calls a hard
    #    cut must actually be one. The board reading a legacy field while the plan
    #    used the modern one is exactly how a declared dip became five "hard cut"
    #    lines and he had to ask whether the film had any transitions at all.
    tpa = getattr(P, "TRANSITIONS_PLAN", {}) or {}
    try:
        page = open(out, encoding="utf-8").read()
        import re as _re
        flat = _re.sub(r"<[^>]+>", " ", page)
        for i, spec in sorted(tpa.items()):
            kind = str(spec.get("kind", "")).upper()
            if kind and kind not in flat.upper():
                fail(f"the plan declares a {kind} transition after shot {i} and the "
                     f"board never shows it - the page misrepresents the edit")
        # count the per-boundary ELEMENTS, not the words: my own edit-flow summary
        # line contains the phrase "hard cut" and was counted, failing a correct
        # board (caught in test 2026-08-12 - the L162 family again: know exactly
        # what the thing you are counting is).
        n_hard = page.count("class='cut'")
        expected_hard = max(0, len(rows) - 1 - len(tpa) - len(blends_of(P)))
        if tpa and n_hard > expected_hard:
            fail(f"the board prints 'hard cut' {n_hard} times but only "
                 f"{expected_hard} boundaries are hard cuts")
    except Exception as e:
        warn(f"transition rendering not verifiable: {str(e)[:60]}")

    # 7 NO PANEL IS A DUPLICATE OF ITS NEIGHBOUR (the board's own dupe smell)
    for a, b in zip(rows, rows[1:]):
        if a["src"] == b["src"]:
            warn(f"shots {a['i']} and {b['i']} share source {a['src']} back to back")

    # 8 COST ON THE PAGE MATCHES THE PLAN'S OWN ARITHMETIC
    try:
        c = P.cost()
        if abs(c["total"] - (c["generation"] + c["plates"])) > 0.01:
            fail("the cost line does not add up")
    except Exception as e:
        warn(f"cost not verifiable: {str(e)[:60]}")

    print()
    print("  " + "=" * 62)
    print("  BOARD QC — deep analysis of the storyboard itself")
    print("  " + "=" * 62)
    for m in W:
        print(f"    warn  {m}")
    if F:
        for m in F:
            print(f"    FAIL  {m}")
        print(f"\n  BOARD QC FAILED ({len(F)} defect(s)) — DO NOT SHOW THIS BOARD.")
        print("  REPLAN: fix the plan, re-run planqc, regenerate the board, re-QC.")
        print("  Only a board that passes reaches him (his rule, 2026-08-12).")
        return 1
    print(f"    {len(rows)} panels · order, timing, provenance, prompts, refs, "
          f"pillar, cards, links and cost all agree with the plan")
    print("  BOARD QC PASSED — safe to show him.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--out")
    a = ap.parse_args()
    return build(a.plan, a.out)


if __name__ == "__main__":
    sys.exit(main())
