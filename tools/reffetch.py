#!/usr/bin/env python3
"""
REFFETCH — pull the reference videos you picked, straight into the pillar's folder.

WHAT THIS REPLACES
  Until now the reference workflow was: find a video, open snaptik.io or ssstik.io in a
  browser, download, find the file, move it into assets/refs/<pillar>/, remember to run
  refstudy. Twenty-three files arrived that way. It works and it is slow, and the last
  two steps get skipped, which is why the strips and the teardowns never existed.

WHAT THIS IS NOT
  Not a crawler. It does not search, discover, follow, or harvest anything. You give it
  URLs of videos YOU chose; it fetches those and stops. intel.py records the reason the
  repo has no scraper — "any scraper here would break on first run" — and that judgement
  still stands for DISCOVERY. Fetching a list you already decided on is a different act,
  and it is the one that was costing you time.

  A folder of references you CHOSE is worth more than any feed. That was true before
  this file and it is still true; this only removes the browser round-trip.

REALITY
  Platforms rate-limit, geo-block, and change their players. yt-dlp is the most
  maintained tool for this and it still fails sometimes. When a URL fails this says so,
  per URL, and keeps going — it never reports a partial fetch as complete. If a
  platform blocks you, the snaptik route still works; drop the file in the folder by
  hand and run --scan. Nothing downstream cares how a file arrived.

Usage
  python3 tools/reffetch.py --pillar car_cinematic --url https://... [--url ...]
  python3 tools/reffetch.py --pillar car_cinematic --file urls.txt
  python3 tools/reffetch.py --pillar car_cinematic --file urls.txt --study
  python3 tools/reffetch.py --list

--study runs refsense --scan and --strip afterwards, so a fetched reference is measured
and has a hook strip to look at without a second command.

Exit codes
  0  every URL fetched
  1  at least one URL failed (named individually)
  2  yt-dlp missing, or nothing to do
"""
import argparse, glob, json, os, subprocess, sys
from datetime import datetime

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(HERE, "assets")
LOG = os.path.join(A, "refs", "_fetch_log.json")


def refdir(pillar):
    d = os.path.join(A, "refs", pillar)
    os.makedirs(d, exist_ok=True)
    return d


def have_ytdlp():
    try:
        import yt_dlp  # noqa: F401  (import IS the check)
        return True
    except Exception:
        return False


def log_append(rows):
    d = {"_what": "Every reference fetch, so a corpus can always say where a file came "
                  "from. A reference with no recorded source cannot be re-fetched or "
                  "re-checked when it goes stale.", "fetches": []}
    if os.path.exists(LOG):
        try:
            d = json.load(open(LOG, encoding="utf-8"))
        except Exception:
            pass
    d.setdefault("fetches", []).extend(rows)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    json.dump(d, open(LOG, "w", encoding="utf-8"), indent=1)


def fetch_one(url, outdir):
    """One URL. Returns (ok, path_or_reason)."""
    before = set(glob.glob(os.path.join(outdir, "*")))
    # %(id)s keeps names stable and collision-free; the platform id is also the only
    # durable handle back to the original post.
    tmpl = os.path.join(outdir, "%(extractor_key)s_%(id)s.%(ext)s")
    cmd = [sys.executable, "-m", "yt_dlp",
           "-f", "mp4/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
           "--no-playlist", "--no-warnings", "--retries", "3",
           "--socket-timeout", "20", "-o", tmpl, url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return False, "timed out after 300s"
    after = set(glob.glob(os.path.join(outdir, "*")))
    new = [p for p in (after - before)
           if p.lower().endswith((".mp4", ".mov", ".webm", ".mkv"))]
    if new:
        return True, new[0]
    if r.returncode == 0:
        return False, "yt-dlp exited 0 but produced no video file"
    tail = [l for l in (r.stderr or "").splitlines() if l.strip()][-1:] or ["no output"]
    return False, tail[0][:200]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pillar")
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--file")
    ap.add_argument("--study", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        base = os.path.join(A, "refs")
        print(f"\n  REFERENCE CORPUS — {os.path.relpath(base, HERE)}\n")
        if not os.path.isdir(base):
            print("    nothing yet.\n"); return 2
        for p in sorted(os.listdir(base)):
            d = os.path.join(base, p)
            if not os.path.isdir(d) or p.startswith("_"):
                continue
            vids = [f for f in os.listdir(d)
                    if f.lower().endswith((".mp4", ".mov", ".webm", ".mkv"))]
            rs = os.path.join(d, "refsense.json")
            read = 0
            if os.path.exists(rs):
                try:
                    j = json.load(open(rs, encoding="utf-8"))
                    read = sum(1 for r in j.get("refs", {}).values()
                               if all((r.get("read") or {}).values()))
                except Exception:
                    pass
            print(f"    {p:24s} {len(vids):>3} video(s) · {read} fully READ")
        print()
        return 0

    if not a.pillar:
        ap.print_help(); return 2

    urls = list(a.url)
    if a.file:
        if not os.path.exists(a.file):
            print(f"  no such file: {a.file}"); return 2
        for ln in open(a.file, encoding="utf-8"):
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                urls.append(ln)
    if not urls:
        print("\n  no URLs. Pass --url, or --file with one URL per line.\n")
        return 2

    if not have_ytdlp():
        print("\n  yt-dlp is not installed — NOT FETCHED, nothing was downloaded.")
        print("  Run SETUP-TOOLS.bat, or:  python -m pip install -U yt-dlp")
        print("\n  The manual route still works: download by hand into")
        print(f"  {os.path.relpath(refdir(a.pillar), HERE)} and run")
        print(f"  python3 tools/refsense.py --pillar {a.pillar} --scan\n")
        return 2

    out = refdir(a.pillar)
    print(f"\n  fetching {len(urls)} reference(s) into "
          f"{os.path.relpath(out, HERE)}\n")
    rows, ok_n = [], 0
    for u in urls:
        print(f"    {u[:78]}")
        ok, res = fetch_one(u, out)
        if ok:
            ok_n += 1
            print(f"      -> {os.path.basename(res)}")
        else:
            print(f"      FAILED: {res}")
        rows.append({"url": u, "ok": ok, "result": os.path.basename(res) if ok else res,
                     "pillar": a.pillar,
                     "at": datetime.now().strftime("%Y-%m-%d %H:%M")})
    log_append(rows)

    failed = len(urls) - ok_n
    print(f"\n  {ok_n}/{len(urls)} fetched" + (f", {failed} FAILED" if failed else ""))
    if failed:
        print("  Failed URLs are named above and logged. A partial fetch is never")
        print("  reported as complete — re-run with just the failures, or fall back")
        print("  to snaptik for those and drop the files in the same folder.")

    if a.study and ok_n:
        print("\n  --study: measuring and building hook strips ...\n")
        for args in (["--scan"], ["--strip"]):
            subprocess.run([sys.executable, os.path.join(HERE, "tools", "refsense.py"),
                            "--pillar", a.pillar] + args, cwd=HERE)
        print(f"  Now LOOK at the strips, then fill each reference:")
        print(f"    python3 tools/refsense.py --pillar {a.pillar} --gaps\n")
    elif ok_n:
        print(f"\n  next: python3 tools/refsense.py --pillar {a.pillar} --scan --strip\n")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
