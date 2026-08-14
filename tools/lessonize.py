#!/usr/bin/env python3
"""
LESSONIZE — the loop that was doctrine and is now mechanism.

HIS ASK, 2026-08-06: "every time each QC found a bug or an error it automatically fix
and passed it to mastermind so next time on new generation the mastermind wont make
this mistake again and essentially learn from it and improvise and improve."

WHAT THIS DOES, AND THE ONE HALF IT REFUSES TO DO
-------------------------------------------------
CAPTURE      automatic. Every FAILING gate check and every FAILING judge seat becomes
             a dated, structured lesson in ledgers/knowledge.json. No human retyping,
             so no finding is lost when a chat is cleared.
BLOCK        automatic, and this is the part that makes it stick. Filing a lesson
             raises that topic's COUNT. planqc check 23 BLOCKS any plan whose
             LESSONS_ACK is lower than the current count. So the next plan literally
             CANNOT PASS until someone has read the new lessons and re-acked them.
             The loop is closed by a gate, not by anyone's memory.
FIX          REFUSED, on purpose, and this is not a limitation to be removed later.
             tools/mastermind_loop.py already states it: "It does not fix anything by
             itself and never will. Fixing is judgement. A loop that edited plans on
             its own would be a claimed capability - the one thing this repo forbids."
             A tool that auto-edited a plan to clear its own gate would be optimising
             the CHECK instead of the FILM. That is the SMOOTH NUMBER trap from file
             27 PART C, automated and running unattended.

So: it learns automatically, it blocks automatically, and it hands the fix to a human
with the evidence attached. That is the strongest honest version of what he asked for.

USAGE
  python3 tools/lessonize.py <project> --from-judge   file every FAILED seat in the
                                                      latest verdict for that project
  python3 tools/lessonize.py <project> --from-gate    run planqc, file every FAIL
  python3 tools/lessonize.py --add "<topic>" "<CLASS: finding>" "<mitigation>"
  python3 tools/lessonize.py --status                 counts + which plans are now STALE
  python3 tools/lessonize.py ... --dry                show what WOULD be filed, write nothing

Every write backs up ledgers/knowledge.json to _backup_lessonize/ first.
Re-running is safe: lessons are deduped on a normalised signature, so the same finding
filed twice does not inflate a count and does not falsely block every plan in the repo.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOW = os.path.join(HERE, "ledgers", "knowledge.json")
VERD = os.path.join(HERE, "ledgers", "verdicts.json")
BACKUP = os.path.join(HERE, "_backup_lessonize")
CRAFT = "general craft"

# Which topic a finding belongs to. A gate check about MEASUREMENT, TOOLING or PROCESS
# is pillar-independent and goes to craft; anything about how this GENRE should look
# goes to the pillar's own topic, because planqc 23 acks the two separately.
CRAFT_MARKERS = (
    "import", "glob", "traceback", "nameerror", "indexerror", "encode", "ffmpeg",
    "freshness", "manifest", "measure", "measured", "tool", "script", "backup",
    "delete", "path", "lock", "commit", "peak", "lufs", "true-peak", "cost",
    "balance", "credit", "plate", "claim", "source", "verified", "stale",
)

# INVERTED 2026-08-08, and this is the fix for the thing that has cost him most.
# His words: "it keeps on happening, especially when i switch frm vlog content to
# car review then switch to car cinematic there turns out to be more and more
# problem". The cause was in this file. _route DEFAULTED to the pillar's own topic
# and only sent a lesson to craft if it happened to contain one of the markers
# above - so most lessons got filed under a genre, and planqc 23 only blocks on the
# topics a plan DECLARES. A lesson filed under "travel vlog" was not deprioritised
# for a car review plan, it was INVISIBLE to it. Every format switch started over.
# Ledger at the time of the fix: general craft 112, car cinematic 15, car review 8,
# travel vlog 6 - and almost nothing in those genre buckets was truly genre-only.
# NOW: craft is the default. A lesson goes to a genre ONLY if it is about that
# genre's own conventions - how this KIND of video should look, move or sound - or
# if it is filed with --genre explicitly. Anything about the pipeline, the gates,
# the measurement or the craft travels with you to every format.
GENRE_MARKERS = (
    "this pillar", "this genre", "this format", "audience of this",
    "car cinematic looks", "vlog looks", "review looks",
    "genre convention", "for this kind of video", "viewers of this genre",
)


def _today():
    return datetime.date.today().isoformat()


def _load():
    with open(KNOW, encoding="utf-8") as f:
        return json.load(f)


def _topics(k):
    return k.setdefault("topics", {})


def _lessons(k, topic):
    t = _topics(k).setdefault(topic, {"references": [], "lessons": [],
                                      "last_researched": _today()})
    if isinstance(t, list):                       # tolerate an older shape
        t = {"references": [], "lessons": t, "last_researched": _today()}
        _topics(k)[topic] = t
    return t.setdefault("lessons", [])


def _sig(text):
    """Normalised signature for dedupe: drop the date, punctuation and case, keep the
    first 12 content words. Two phrasings of the same finding collapse to one lesson.
    Without this, --from-gate on a repeatedly-failing check would inflate the count
    every run and block every plan in the repo for no new knowledge."""
    t = re.sub(r"^\d{4}-\d{2}-\d{2}\s*", "", text.lower())
    words = re.findall(r"[a-z0-9]+", t)
    return " ".join(words[:12])


def _route(text, pillar_topic, force_genre=False):
    """Craft by default. A lesson only belongs to a genre if it is ABOUT that genre.

    See the note on GENRE_MARKERS: this used to be the other way round and it is
    why every format switch felt like starting over."""
    low = text.lower()
    if force_genre and pillar_topic:
        return pillar_topic
    if pillar_topic and any(m in low for m in GENRE_MARKERS):
        return pillar_topic
    return CRAFT


def _plan_pillar(project):
    p = os.path.join(HERE, "plans", f"{project}.py")
    if not os.path.exists(p):
        return None, None
    src = open(p, encoding="utf-8").read()
    m = re.search(r'^PILLAR\s*=\s*["\']([^"\']+)', src, re.M)
    pillar = m.group(1) if m else None
    topic = pillar.replace("_", " ") if pillar else None
    if topic and topic not in _topics(_load()):
        topic = topic if topic in _topics(_load()) else topic
    return pillar, topic


def _compose(cls, finding, mitigation):
    cls = cls.strip().upper().rstrip(":")
    out = f"{_today()} {cls}: {finding.strip()}"
    if mitigation and mitigation.strip():
        out += f" MITIGATION: {mitigation.strip()}"
    return out


def file_lessons(items, dry=False):
    """items = [(topic, text)]. Returns (filed, skipped_duplicates)."""
    k = _load()
    filed, dup = [], []
    for topic, text in items:
        lst = _lessons(k, topic)
        sigs = {_sig(x if isinstance(x, str) else json.dumps(x)) for x in lst}
        if _sig(text) in sigs:
            dup.append((topic, text))
            continue
        lst.append(text)
        filed.append((topic, text))
    if filed and not dry:
        os.makedirs(BACKUP, exist_ok=True)
        shutil.copy2(KNOW, os.path.join(
            BACKUP, f"knowledge_{datetime.datetime.now():%Y%m%d_%H%M%S}.json"))
        with open(KNOW, "w", encoding="utf-8") as f:
            json.dump(k, f, indent=1, ensure_ascii=False)
    return filed, dup


# ---------------------------------------------------------------- sources of findings
def from_judge(project):
    """Every FAILED seat in EVERY recorded verdict for this project becomes a lesson.

    CAUGHT ON THE FIRST RUN, 2026-08-06: the first version of this read only the LATEST
    verdict. kundasang's J4 veto was in run 1 and run 2 passed clean, so the tool filed
    NOTHING and the one finding of the day would have been lost - the exact failure this
    tool exists to prevent, in the tool itself. A fixed defect is still knowledge: the
    lesson is not "the plan was wrong", it is "this class of mistake reached a gate".
    Dedupe on the signature means re-reading old runs costs nothing."""
    if not os.path.exists(VERD):
        return []
    runs = json.load(open(VERD, encoding="utf-8")).get("runs", [])
    mine = [r for r in runs if r.get("project") == project]
    if not mine:
        return []
    _p, topic = _plan_pillar(project)
    out = []
    for r in mine:
        for s in r.get("verdict", {}).get("verdicts", []):
            if s.get("pass"):
                continue
            text = _compose(
                f"JUDGE {s.get('seat','?')} FAIL on {project}",
                f"{s.get('finding','').strip()} (scored {s.get('score','?')}/10 at "
                f"{s.get('where','?')})",
                s.get("fix", ""))
            out.append((_route(text, topic), text))
    return out


def from_gate(project):
    """Run planqc and file every FAIL line. The gate output IS the finding - nobody
    has to remember to write it down, which is the step that has always been skipped."""
    _p, topic = _plan_pillar(project)
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, "talyx.py"),
                            "plan", project],
                           capture_output=True, text=True, timeout=300)
    except Exception as e:                                    # noqa: BLE001
        return [(CRAFT, _compose("GATE UNRUNNABLE",
                                 f"planqc could not run on {project}: {e}", ""))]
    out = []
    for line in (r.stdout + r.stderr).splitlines():
        if not line.strip().startswith("FAIL"):
            continue
        body = line.strip()[4:].strip()
        text = _compose(f"PLANQC FAIL on {project}",
                        body, "fix at PLAN level first - a plan fix beats a pipeline "
                              "fix even when the pipeline fix is cleaner")
        out.append((_route(text, topic), text))
    return out


# ---------------------------------------------------------------- status
def status():
    k = _load()
    counts = {t: len(v.get("lessons", []) if isinstance(v, dict) else v)
              for t, v in _topics(k).items()}
    print("=" * 78)
    print("LEDGER — every plan must ack these EXACT counts (planqc 23)")
    print("=" * 78)
    for t, n in sorted(counts.items()):
        print(f"  {t:<45} {n}")
    print()
    stale = []
    pdir = os.path.join(HERE, "plans")
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith(".py") or fn.startswith("_"):
            continue
        src = open(os.path.join(pdir, fn), encoding="utf-8").read()
        m = re.search(r"LESSONS_ACK\s*=\s*\{(.*?)\}", src, re.S)
        pm = re.search(r'^PILLAR\s*=\s*["\']([^"\']+)', src, re.M)
        topic = pm.group(1).replace("_", " ") if pm else None
        if not m:
            stale.append((fn, "NO LESSONS_ACK"))
            continue
        acked = dict(re.findall(r'["\']([^"\']+)["\']\s*:\s*(\d+)', m.group(1)))
        for t in {CRAFT, topic} - {None}:
            have = counts.get(t)
            if have is None:
                continue
            got = int(acked.get(t, -1))
            if got != have:
                stale.append((fn, f"'{t}' acked {got if got >= 0 else 'MISSING'}, "
                                  f"ledger holds {have}"))
    print("PLANS THAT PLANQC 23 WILL NOW BLOCK")
    if not stale:
        print("  none - every plan is current")
    for fn, why in stale:
        print(f"  BLOCKED  plans/{fn:<18} {why}")
    print()
    print("  This is the mechanism working, not a bug. A lesson that does not change")
    print("  the next build is not learned. Re-ack only AFTER reading the new lessons")
    print("  and updating that plan's PREMORTEM - the ack is a claim that you did.")
    return 0


def brief(project=None):
    """PRINT the lessons a plan has not yet acknowledged.

    THE GAP THIS CLOSES (his question, 2026-08-06: "does mastermind have all these
    skills and info?"). planqc 23 enforces that LESSONS_ACK equals the ledger COUNT.
    A count is not comprehension - a session can ack 76 without reading one line, and
    the gate cannot tell the difference. THE MASTERMIND IS NOT A PROGRAM: it is a seat
    (27-mastermind-qc.md) executed by a human plus an LLM, so its entire memory is
    these files. If the lessons are never read, the loop is a counter, not learning.
    This prints exactly the unread ones, so the ack can be EARNED."""
    k = _load()
    counts = {t: len(v.get("lessons", []) if isinstance(v, dict) else v)
              for t, v in _topics(k).items()}
    acked = {}
    if project:
        p = os.path.join(HERE, "plans", f"{project}.py")
        if os.path.exists(p):
            src = open(p, encoding="utf-8").read()
            m = re.search(r"LESSONS_ACK\s*=\s*\{(.*?)\}", src, re.S)
            if m:
                acked = {t: int(n) for t, n in
                         re.findall(r'["\']([^"\']+)["\']\s*:\s*(\d+)', m.group(1))}
            pm = re.search(r'^PILLAR\s*=\s*["\']([^"\']+)', src, re.M)
            topics = [CRAFT] + ([pm.group(1).replace("_", " ")] if pm else [])
        else:
            print(f"  no plan '{project}'"); return 2
    else:
        topics = list(counts)
    for t in topics:
        if t not in counts:
            continue
        lst = _lessons(k, t)
        frm = acked.get(t, 0) if project else 0
        new_ = lst[frm:]
        if not new_:
            continue
        print("=" * 78)
        print(f"{t.upper()} — {len(new_)} lesson(s) not yet acknowledged "
              f"({frm} -> {len(lst)})")
        print("=" * 78)
        for i, x in enumerate(new_, start=frm):
            print(f"\n[{i}] {x if isinstance(x, str) else json.dumps(x)}")
    print("\n  Read these, put the ones that apply into the plan's PREMORTEM, THEN")
    print("  raise LESSONS_ACK. The ack is a claim that you did - planqc 23 only")
    print("  checks the number, so the honesty of it is on the reader.")
    return 0


def main():
    a = argparse.ArgumentParser()
    a.add_argument("project", nargs="?")
    a.add_argument("--from-judge", action="store_true")
    a.add_argument("--from-gate", action="store_true")
    a.add_argument("--add", nargs=3, metavar=("TOPIC", "FINDING", "MITIGATION"))
    a.add_argument("--status", action="store_true")
    a.add_argument("--brief", action="store_true",
                   help="PRINT the lessons this plan has not acked yet")
    a.add_argument("--dry", action="store_true")
    args = a.parse_args()

    if args.status:
        return status()
    if args.brief:
        return brief(args.project)

    items = []
    if args.add:
        topic, finding, mit = args.add
        cls, _, rest = finding.partition(":")
        items.append((topic, _compose(cls, rest or finding, mit)))
    if args.project and args.from_judge:
        items += from_judge(args.project)
    if args.project and args.from_gate:
        items += from_gate(args.project)

    if not items:
        print("nothing to file - pass --from-judge / --from-gate / --add, or --status")
        return 1

    filed, dup = file_lessons(items, dry=args.dry)
    print("=" * 78)
    print(f"LESSONIZE{'  (DRY RUN - nothing written)' if args.dry else ''}")
    print("=" * 78)
    for t, txt in filed:
        print(f"  FILED    [{t}] {txt[:150]}")
    for t, _txt in dup:
        print(f"  already known  [{t}] - deduped, count unchanged")
    if not filed:
        print("  no NEW lessons - every finding was already in the ledger")
    print()
    print("  NOT FIXED, and never will be by this tool. Fixing is judgement.")
    print("  Run  python3 tools/lessonize.py --status  to see which plans are now")
    print("  BLOCKED until they read these and re-ack.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
