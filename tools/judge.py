#!/usr/bin/env python3
"""
JUDGE — the LLM loop. The half of QC no threshold can do, wired into the same routing
and the same attempt ledger as the mechanical gates.

THE GAP
  Thirteen mechanical gates measure CONFORMANCE: is this shot bright enough, does that
  cut land on the beat, is the loudness in band. Every one can pass while the video is
  boring, and the repo says so in four separate places. file 06 defines the judges —
  J0 the Hook Tyrant with a solo veto, J1-J6 the reception panel — and file 27 defines
  the final-boss pass. Both are PROSE. Running them meant a person pasting context into
  a chat, reading a verdict, and remembering what it said. The verdict died with the
  chat; only the measurements survived.

  This runs them as a defined step with a defined output, and files the result next to
  the mechanical failures so one work order covers both.

TWO MODES, AND IT IS HONEST ABOUT WHICH
  API   ANTHROPIC_API_KEY is set -> calls the model directly, with the frames attached,
        and parses a structured verdict.
  PACKET  no key -> writes a self-contained packet to
        projects/<name>/analysis/JUDGE_PACKET_<stage>.md
        You paste it into Claude, paste the JSON verdict back with --ingest.

  Both produce the SAME verdict format and both file into the SAME ledger. The packet
  mode is not a degraded fallback — it is how this actually gets used most of the time,
  and it costs nothing.

  What it will NOT do is emit a verdict it did not receive. No key and no ingest means
  it says NOT JUDGED, loudly. A judge that invents a verdict is worse than no judge,
  and this repo has already paid for that lesson twice.

WHAT IT MAY NEVER DECIDE
  ledgers/routing.json _not_routed names it: IDENTITY is Gavril's, always. On KK the
  identity verdict FLIPPED between crop scales — "not him" at thumbnail, "plausibly
  him" at matched size, same frames, same session. This tool presents evidence at
  matched scale and records that the call is not its own.

Usage
  python3 tools/judge.py crown --stage plan                 build packet / call API
  python3 tools/judge.py crown --stage cut --video out.mp4
  python3 tools/judge.py crown --ingest verdict.json
  python3 tools/judge.py crown --status
"""
import argparse, base64, json, os, sys
from datetime import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
LEDGER = os.path.join(HERE, "ledgers", "attempts.json")
VERDICTS = os.path.join(HERE, "ledgers", "verdicts.json")
MODEL = os.environ.get("TALYX_JUDGE_MODEL", "claude-sonnet-4-20250514")

SEATS = {
    "J0": ("HOOK TYRANT — SOLO VETO",
           "Judge ONLY the first 2 seconds. Is an EVENT already resolving on screen, or "
           "is this a tour? A tour is an automatic veto. State the exact moment a thumb "
           "would stop, or say there isn't one."),
    "J1": ("RECEPTION — would a stranger watch to the end",
           "You are a Malaysian recond-car buyer scrolling at 11pm. Be honest and "
           "specific about where you would leave, and why."),
    "J2": ("STORY — does anything HAPPEN",
           "Is there a state change with a cause, or a sequence of pretty pictures? "
           "Name the consequence chain if there is one. Resemblance is not story."),
    "J3": ("CRAFT — does it read as real footage",
           "Anything that reads as AI, a render, a repeat, or a stock move. Be specific "
           "about timestamps or shot numbers."),
    "J4": ("TEXT + CLAIM — absolute veto on invented facts",
           "Any on-screen text, badge, spec or claim that is wrong or unverifiable. An "
           "invented 'SR' badge shipped through 8 builds. You have an ABSOLUTE veto."),
    "J6": ("ALGORITHM — is there a share trigger",
           "What would make someone send this to one specific friend? If nothing, say "
           "nothing.")
}

SCHEMA = {
    "verdicts": [{"seat": "J0", "pass": True, "score": 0,
                  "finding": "one sentence", "fix": "one concrete action",
                  "where": "shot index / timestamp / 'whole cut'"}],
    "overall": {"ship": False, "one_line": "the single most important thing to fix"}
}


def load_plan(name):
    import importlib
    for cand in (f"plans.{name}", name, f"{name}_plan"):
        try:
            return importlib.import_module(cand)
        except ModuleNotFoundError:
            continue
    return None


def _jload(p, default):
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    return default


def frames_of(video, n=9, max_w=420):
    """Evenly spaced frames, base64 jpeg. Evidence, not decoration."""
    try:
        import cv2
    except Exception:
        return []
    cap = cv2.VideoCapture(video)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    out = []
    for k in range(n):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(total * (k + 0.5) / n))
        ok, fr = cap.read()
        if not ok:
            continue
        h, w = fr.shape[:2]
        if w > max_w:
            fr = cv2.resize(fr, (max_w, int(h * max_w / w)))
        ok, buf = cv2.imencode(".jpg", fr, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if ok:
            out.append(base64.b64encode(buf.tobytes()).decode())
    cap.release()
    return out


def plan_evidence(P):
    """Everything a judge needs about a PLAN, and nothing it does not."""
    tl, total = P.timeline()
    L = []
    L.append(f"PROJECT: {getattr(P,'PROJECT','?')}")
    L.append(f"PILLAR:  {getattr(P,'PILLAR','?')}   {getattr(P,'BPM','?')} BPM   "
             f"{len(P.SHOTS)} shots   {total:.2f}s pre-blend")
    c = getattr(P, "CONTENT", {}) or {}
    L.append("\nCONTENT BLOCK")
    # NOT TRUNCATED, deliberately. The first version cut every field at 400 chars and
    # sliced crown's `verified` mid-word at "350PS on a deriva" — hiding the fact that
    # a power figure had been RETRACTED. J4 holds an ABSOLUTE VETO on claims and was
    # being handed a truncated verification source: a seat that cannot see the thing it
    # is vetoing. That is the blind-spot class planqc 21 already demonstrated (the check
    # measured the clip while the prompt split it). The CONTENT block is the smallest
    # and most load-bearing text in the plan — it ships whole.
    for k in ("claim", "verified", "twist", "why_stop"):
        L.append(f"  {k:9s} {str(c.get(k,'(missing)'))}")
    L.append("\nSHOT LIST  (index · source · act · beats · delivered t · note)")
    blends = sorted(set(getattr(P, "BLEND_AFTER", []) or []))
    bw = getattr(P, "BLEND_WIDTH", 0.0)
    for i, (src, crop, kind, note) in enumerate(P.SHOTS):
        act = ((getattr(P, "SOURCES", {}) or {}).get(src) or ("", "", "?"))[2]
        d = tl[i][0] - bw * len([b for b in blends if b < i])
        L.append(f"  {i:2d}  {src:7s} {act:8s} {kind:5s} {d:6.2f}s  {note}")
    L.append("\nCARDS")
    for t_, f_, n_, kind in (getattr(P, "CARDS", []) or []):
        L.append(f"  shot {f_}-{f_+n_-1}  [{kind}]  \"{t_}\"")
    lk = getattr(P, "LINKAGE", None)
    if lk:
        L.append("\nLINKAGE (boundary · kind · token · why)")
        for i, e in enumerate(lk if isinstance(lk, (list, tuple)) else []):
            if isinstance(e, (list, tuple)) and len(e) >= 3:
                L.append(f"  {i:2d}->{i+1:2d}  {str(e[0]):11s} {str(e[1])[:18]:18s} {e[2]}")
    sn = getattr(P, "SOUND", {}) or {}
    L.append(f"\nSOUND hero: {str(sn.get('hero','(none)'))[:300]}")
    L.append(f"SOUND silence: {str(sn.get('silence','(none)'))[:300]}")
    return "\n".join(L)


def build_packet(name, stage, P, video=None):
    ev = plan_evidence(P) if P else "(no plan module)"
    frames = frames_of(video) if (stage == "cut" and video) else []
    seats = ["J0", "J2", "J4"] if stage == "plan" else list(SEATS)
    head = [
        f"# JUDGE PACKET — {name} · stage {stage}",
        f"_generated {datetime.now():%Y-%m-%d %H:%M} by tools/judge.py_", "",
        "You are running the reception judges from file `06-content-judges.md`.",
        "This is the gate that kills BORING, which no mechanical check can measure.",
        "", "## RULES", "",
        "- Judge what is HERE, not what could be added. Be specific: name a shot index "
        "or a timestamp in every finding.",
        "- J0 and J4 hold SOLO VETOES. If either fails, `overall.ship` is false "
        "regardless of the other scores.",
        "- Do NOT judge identity (is it really Nev). That verdict is Gavril's, always — "
        "it flipped between crop scales on KK, same frames, same session.",
        "- If the evidence does not let you judge a seat, say so in `finding` and set "
        "`pass` to false. Never score a seat you could not see.",
        "", "## SEATS", ""]
    for s in seats:
        t, d = SEATS[s]
        head += [f"### {s} — {t}", d, ""]
    head += ["## EVIDENCE", "", "```", ev, "```", ""]
    if frames:
        head += [f"_{len(frames)} frames from the cut are attached (API mode) or must "
                 f"be viewed alongside this packet._", ""]
    head += ["## RETURN EXACTLY THIS JSON, nothing else", "",
             "```json", json.dumps(SCHEMA, indent=2), "```", "",
             "`score` is 0-10. `pass` is your verdict for that seat alone.", ""]
    return "\n".join(head), frames


def call_api(packet, frames):
    """Returns (verdict_dict, error_or_None). Never fabricates."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None, "no ANTHROPIC_API_KEY"
    try:
        import anthropic
    except Exception:
        return None, ("anthropic sdk not installed "
                      "(python -m pip install anthropic)")
    content = [{"type": "text", "text": packet}]
    for f in frames[:9]:
        content.append({"type": "image", "source": {
            "type": "base64", "media_type": "image/jpeg", "data": f}})
    try:
        cl = anthropic.Anthropic(api_key=key)
        r = cl.messages.create(model=MODEL, max_tokens=3000,
                               messages=[{"role": "user", "content": content}])
        txt = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    except Exception as e:
        return None, f"API call failed: {e}"
    s, e = txt.find("{"), txt.rfind("}")
    if s < 0 or e < 0:
        return None, "model returned no JSON object"
    try:
        return json.loads(txt[s:e + 1]), None
    except Exception as ex:
        return None, f"verdict JSON did not parse: {ex}"


def file_verdict(name, stage, v):
    """Record the verdict AND push failures into the shared attempt ledger, so a
    semantic failure and a mechanical one appear in one place."""
    allv = _jload(VERDICTS, {"_what": "Every judge verdict, kept because a verdict that "
                                      "lives only in a chat is not a gate.",
                             "runs": []})
    allv["runs"].append({"project": name, "stage": stage,
                         "at": datetime.now().strftime("%Y-%m-%d %H:%M"), "verdict": v})
    json.dump(allv, open(VERDICTS, "w", encoding="utf-8"), indent=1)

    led = _jload(LEDGER, {"_what": "Attempt counts per project per check.",
                          "projects": {}})
    proj = led["projects"].setdefault(name, {})
    for row in (v.get("verdicts") or []):
        if row.get("pass"):
            continue
        k = f"JUDGE {row.get('seat','?')}"
        rec = proj.setdefault(k, {"attempts": 0, "history": []})
        rec["attempts"] += 1
        rec["history"].append({"at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                               "gate": "judge",
                               "detail": str(row.get("finding", ""))[:200]})
    json.dump(led, open(LEDGER, "w", encoding="utf-8"), indent=1)
    return allv, led


def report(name, v, led):
    rows = v.get("verdicts") or []

    print("=" * 78)
    print(f"JUDGE VERDICT — {name}")
    print("=" * 78)
    for r in rows:
        mark = "PASS" if r.get("pass") else "FAIL"
        seat = r.get("seat", "?")
        veto = "  [SOLO VETO]" if seat in ("J0", "J4") and not r.get("pass") else ""
        print(f"\n  {mark}  {seat}  {SEATS.get(seat,('?',''))[0]}{veto}")
        print(f"        score  {r.get('score','?')}/10")
        print(f"        where  {r.get('where','?')}")
        print(f"        found  {r.get('finding','')}")
        if not r.get("pass"):
            print(f"        FIX    {r.get('fix','(none given)')}")
    o = v.get("overall") or {}
    print("\n" + "=" * 78)
    print(f"  SHIP: {'YES' if o.get('ship') else 'NO'}   {o.get('one_line','')}")
    proj = led["projects"].get(name, {})
    at_limit = [k for k, r in proj.items()
                if k.startswith("JUDGE") and r["attempts"] >= 5]
    if at_limit:
        print(f"\n  STOP — {at_limit} have failed 5 times. His rule: stop and ask.")
    print("=" * 78 + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--stage", choices=["plan", "cut"], default="plan")
    ap.add_argument("--video")
    ap.add_argument("--ingest")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()

    if a.status:
        allv = _jload(VERDICTS, {"runs": []})
        runs = [r for r in allv.get("runs", []) if r["project"] == a.project]
        print(f"\n  JUDGE HISTORY — {a.project}: {len(runs)} run(s)\n")
        for r in runs[-8:]:
            o = r["verdict"].get("overall", {})
            f = sum(1 for x in (r["verdict"].get("verdicts") or []) if not x.get("pass"))
            print(f"    {r['at']}  {r['stage']:5s}  ship={o.get('ship')}  "
                  f"{f} seat(s) failed  {str(o.get('one_line',''))[:60]}")
        print()
        return 0

    if a.ingest:
        if not os.path.exists(a.ingest):
            print(f"  no such file: {a.ingest}"); return 2
        try:
            v = json.load(open(a.ingest, encoding="utf-8"))
        except Exception as e:
            print(f"  verdict JSON did not parse: {e}"); return 2
        if "verdicts" not in v:
            print("  that file has no 'verdicts' key — not a judge verdict."); return 2
        allv, led = file_verdict(a.project, "ingested", v)
        report(a.project, v, led)
        return 0 if (v.get("overall") or {}).get("ship") else 1

    P = load_plan(a.project)
    if P is None and a.stage == "plan":
        print(f"  no plan module for '{a.project}'"); return 2
    video = a.video
    if a.stage == "cut" and not video:
        import glob as _g
        c = sorted(_g.glob(os.path.join(HERE, "projects", a.project, "output",
                                        "*.mp4")), key=os.path.getmtime)
        video = c[-1] if c else None
        if not video:
            print(f"  no video in projects/{a.project}/output — build first."); return 2

    packet, frames = build_packet(a.project, a.stage, P, video)
    v, err = call_api(packet, frames)

    if v is not None:
        allv, led = file_verdict(a.project, a.stage, v)
        report(a.project, v, led)
        return 0 if (v.get("overall") or {}).get("ship") else 1

    # PACKET MODE — the honest path when there is no key. Never invent a verdict.
    odir = os.path.join(HERE, "projects", a.project, "analysis")
    os.makedirs(odir, exist_ok=True)
    p = os.path.join(odir, f"JUDGE_PACKET_{a.stage}.md")
    open(p, "w", encoding="utf-8").write(packet)
    print(f"\n  NOT JUDGED — {err}")
    print(f"\n  packet written: {os.path.relpath(p, HERE)}")
    if frames:
        fdir = os.path.join(odir, f"judge_frames_{a.stage}")
        os.makedirs(fdir, exist_ok=True)
        for i, f in enumerate(frames):
            open(os.path.join(fdir, f"f{i:02d}.jpg"), "wb").write(base64.b64decode(f))
        print(f"  {len(frames)} frame(s):  {os.path.relpath(fdir, HERE)}")
    print(f"""
  PASTE that packet into Claude (attach the frames if there are any), save the
  JSON it returns as verdict.json, then:

      python3 tools/judge.py {a.project} --ingest verdict.json

  This is not a degraded mode — the verdict is identical either way, and it costs
  nothing. To call the API directly instead:  setx ANTHROPIC_API_KEY "sk-ant-..."
""")
    return 2


if __name__ == "__main__":
    sys.exit(main())
