# START HERE — restoring the TALYX session
### Drop this folder into a new chat. Read this file first, then HANDOVER.md.

---

## WHAT THIS IS

The **knowledge** half of a video-automation system. 2.8 MB out of a 7.7 GB project — the
other 7.7 GB is media (b-roll, Whisper weights, render intermediates) which lives on the
machine and is not needed to restore context.

**The full folder is `D:\USER FOLDER IMPORTANT\Desktop\AI` on Gavril's desktop**, also
mirrored to GitHub (`chunghaow-boop/AI-AUTOMATION`). Claude PULLS from GitHub; the USER
PUSHES — no credentials, ever.

---

## READ IN THIS ORDER

```
1  HANDOVER.md                    state, open items, what went wrong and why
2  pillars/PILLAR-PROFILES.md     the measured targets. THE most important file.
3  ledgers/style_ledger.json      19 critiques he has already given. Never repeat one.
4  docs/PIPELINE-V2.md            the pipeline and every gate, traced to a real failure
```

## WHAT'S IN HERE

```
HANDOVER.md CLAUDE.md README.md
docs/                  PIPELINE-V2, V2-REBUILD, WHAT-WE-ARE-BUILDING, GATE, RUNNER, PROMPTS...
pillars/               PILLAR-PROFILES (.md/.json) + per-pillar ANALYSIS + target profiles
                       + music_profile.json (real phonk spectrum, measured)
ledgers/               style_ledger (his critiques) · knowledge (researched lessons, dated)
                       retention_ledger (EMPTY - no posts yet)
tools/                 all 40 tools. This IS the system - 948 KB of Python.
skills/                talyx-shotlist
plates/                s450.png - the verified W223 reference plate
plans/                 the two gated Phase-1 plans
```

## WHAT IS **NOT** IN HERE (and doesn't need to be)

```
work/      4.5 GB  render intermediates, source clips
assets/    3.0 GB  700 SFX, 149 BGM, 41 b-roll, 50 Nev photos, 23 reference videos
models/    280 MB  Whisper weights
output/     60 MB  the finished videos
```

All of it is on the desktop and in the repo. **The 23 reference videos matter** — they are
what the pillar profiles were measured from. If profiles need re-deriving, they are in
`assets/pillars/<pillar>/refs/`.

---

## FIRST FIVE COMMANDS ON A NEW MACHINE

```
python tools/smoketest.py                     verify env - 9 routes at real resolution
python tools/qc.py phase0 --topic "<topic>"   research gate. DO NOT SKIP THIS.
python tools/styleref.py report               what he has already rejected
python tools/retention.py report              still empty. This is the real gap.
python tools/pillar.py                        confirm assets resolve per pillar
```

Needs: Python 3, ffmpeg + ffprobe on PATH, `pip install opencv-python-headless numpy
faster-whisper`.

---

## THE THREE THINGS THAT MATTER MOST

1. **Build against `pillars/PILLAR-PROFILES.json`, not instinct.** It was measured from 23
   videos he chose. Every expensive mistake came from reasoning instead of measuring.
2. **`verdict.py` decides delivery, not the operator.** A video was once shipped with
   "the car isn't a Crown" written in the same message. That is why the gate blocks.
3. **Zero posts exist.** Every retention figure in this repo is a hypothesis.
