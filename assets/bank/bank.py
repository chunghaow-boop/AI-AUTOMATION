"""Query the Talyx asset bank by measurement, not by filename.

v3. Replaces the bank.py inside talyx-bank-v3.zip - that copy still filtered on
`transient`, a field v2 removed, and treated a null loudness as -99 dB, which
would have silently hidden every sound shorter than 400 ms.
"""
import json, os

# A file's loudness is null when it is under 400ms - integrated LUFS is undefined
# there. That is NOT quiet. Never coerce it to a number for ranking or filtering.
SHORT = object()


class Bank:
    def __init__(self, root):
        self.root = root
        d = json.load(open(os.path.join(root, "bank_index.json")))
        self.items = d["items"]
        self.meta = {k: v for k, v in d.items() if k != "items"}

    def pick(self, bucket=None, contains=None, band=None, role=None,
             cut_safe=None, max_tail_ms=None, max_attack_ms=None,
             min_lufs=None, max_lufs=None, min_dur=None, max_dur=None,
             clean_only=False, limit=10):
        """Filter by measurement. Returns loudest-first, clean files before limited ones.

        role       'hit'     - safe to drop on a cut frame
                   'gesture' - align its attack to the cut
                   'bed'     - ambience, never hang it on a cut
        cut_safe   True      - attack <=25ms, no offset needed
        clean_only True      - only files that hit their loudness target exactly
                               (gain_limited_db == 0), i.e. the foley clamp will
                               never bind on them
        min_lufs   filters ONLY files that have a loudness. Short files (null)
                   are kept, because -3 dBFS peak-normalised is not quiet.
        """
        r = self.items
        if bucket:        r = [x for x in r if x["bucket"].startswith(bucket)]
        if contains:
            q = contains.lower()
            r = [x for x in r if q in (x["title"] + " " + x["category"]).lower()]
        if band:          r = [x for x in r if x.get("band") == band]
        if role:          r = [x for x in r if x.get("role") == role]
        if cut_safe is not None:
            r = [x for x in r if bool(x.get("cut_safe")) is cut_safe]
        if max_tail_ms is not None:
            r = [x for x in r if x.get("tail_ms", 9e9) <= max_tail_ms]
        if max_attack_ms is not None:
            r = [x for x in r if x.get("attack_ms", 9e9) <= max_attack_ms]
        if min_dur is not None:
            r = [x for x in r if x.get("duration_s", 0) >= min_dur]
        if max_dur is not None:
            r = [x for x in r if x.get("duration_s", 9e9) <= max_dur]
        # loudness filters skip files whose loudness is undefined rather than
        # pretending they are silent
        if min_lufs is not None:
            r = [x for x in r if x.get("lufs_i") is None or x["lufs_i"] >= min_lufs]
        if max_lufs is not None:
            r = [x for x in r if x.get("lufs_i") is None or x["lufs_i"] <= max_lufs]
        if clean_only:
            r = [x for x in r if x.get("gain_limited_db", 0) == 0]

        def rank(x):
            # clean first, then smallest shortfall, then loudest. Short files sort
            # with the clean group - they were normalised by peak on purpose.
            short = x.get("gain_limited_db", 0)
            loud = x["lufs_i"] if x.get("lufs_i") is not None else -3.0
            return (short, -loud)

        return sorted(r, key=rank)[:limit]

    def path(self, item):
        return os.path.join(self.root, item["file"])

    def why(self, item):
        """One line explaining what this file is and how to place it."""
        lu = ("%.1f LUFS" % item["lufs_i"]) if item.get("lufs_i") is not None \
             else "peak -3 dBFS (under 400ms, LUFS undefined)"
        place = ("place ON the cut frame" if item.get("cut_safe")
                 else "align its attack at %d ms" % item.get("attack_ms", 0))
        short = item.get("gain_limited_db", 0)
        warn = ("  !! %.1f dB under target - the foley clamp may bind" % short) if short > 1 else ""
        return "%s [%s, %s, %s] %s%s" % (
            item["title"], item.get("role"), item.get("band"), lu, place, warn)
