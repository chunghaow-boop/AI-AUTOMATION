# START HERE — 2026-07-31 session
### Drop this folder onto the desktop, into the `AI` project. Read this, then HANDOVER-2026-07-31.md.

---

## WHAT THIS FOLDER IS

One session's work on the Talyx video engine, run from a laptop with the RESTORE package.
Roughly 114 credits spent by me (the rest of the day's drop was your own app usage),
one finished video, four tools patched, one new tool, one new
skill, and a fairly long list of things I got wrong and fixed.

**Balance at close: 823.99 cr — measured, not estimated. Posts: still 0.**

---

## READ IN THIS ORDER

```
1  HANDOVER-2026-07-31.md    state, what broke, what changed, what is open
2  §5 of that handover       "conformance is not interest" - the real gap
3  i8_plan.py                the next build, as data. Verbatim prompts inside.
4  CINEMATIC-STORYBOARDS-10.md   the 10 car boards
```

---

## THE ONE-LINE VERSION

The engine now cuts properly — beat-locked to 3ms, exposure-matched, action-peak placed,
no repeated frames, audible SFX, captions out of the subject. It passes ten mechanical
checks.

**It still does not stop a scroll**, because every check measures *conformance to a
profile* and none measures *whether anything happens*. That is the next problem, and it is
a creative one, not a tooling one.

---

## MERGE NOTES — where things go in the `AI` folder

```
verify.py                    -> project root (next to the tools/ folder)
i8_plan.py                   -> project root
build_lc300_cinematic.py     -> project root  (reference implementation, read the comments)
make_storyboard*.py          -> project root  (i8 one is BROKEN, see handover §6)
tools/beatplan.py            -> tools/        NEW
tools/qc.py                  -> tools/        PATCHED - overwrite
tools/reverse.py             -> tools/        PATCHED - overwrite
tools/fx.py                  -> tools/        PATCHED - overwrite
LC300_*.mp4                  -> work/         6 source clips
LC300ZX_CINEMATIC_v1.mp4     -> output/
NEV_PLATE_SOURCE.jpeg        -> assets/nev/   best frame, measured
*.md                         -> docs/
```

`ledgers/style_ledger.json` and `ledgers/knowledge.json` inside `work/RESTORE/` have new
entries — 22 rejects (3 added today) and 16 lessons on the i8 including the hook research.
Merge those, don't overwrite.

---

## THE SKILL

`talyx-cinematic` is saved to the Claude account, not to this folder. It loads automatically
in any future session and carries every rule learned today — Rule Zero, the quality
defaults, the gate blind spots, the measured failure numbers. Nothing to copy.

---

## FIRST THING TOMORROW

Not another build.

```
python3 verify.py        confirm the LC300 still passes
```

then post it, and get one real 24-hour retention curve. Every target in this repo is
still engineered-for rather than measured, and one real number would tell you more than
another 250 credits of generation.
