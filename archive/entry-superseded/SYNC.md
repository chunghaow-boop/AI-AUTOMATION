# SYNC — how this project travels between laptop · desktop · GitHub
### Repo: https://github.com/chunghaow-boop/AI-AUTOMATION

## THE SPLIT

| what | travels by | why |
|---|---|---|
| code, plans, docs, ledgers, pillars, boards, Nev face set | **git** | small, diffable, this IS the project |
| clips, cuts, reference videos, music beds | **Google Drive** | 100MB+ media; GitHub blocks it, git bloats on it |

`.gitignore` enforces the split. After cloning on a new machine, drop the media from
Drive into the same paths and `talyx.py ls` will show true state.

## RULES

1. **Claude PULLS, the human PUSHES.** Claude has no credentials — hard rule 7.
2. **`ledgers/` MERGE, never overwrite.** Each machine adds lessons the other has not
   seen. On conflict, union the JSON entries — both sides are real history.
3. One machine at a time per project. Push before you stand up; pull before you sit down.

## FIRST PUSH (laptop, one time)

```
cd Desktop/AI
git remote add origin https://github.com/chunghaow-boop/AI-AUTOMATION.git
git push -u origin main
```

## EVERY SESSION AFTER

```
pull first:   git pull
work
push last:    git add -A && git commit -m "session YYYY-MM-DD" && git push
```

## NEW MACHINE SETUP

```
git clone https://github.com/chunghaow-boop/AI-AUTOMATION.git AI
copy media from Drive into:  projects/<name>/clips/  assets/refs/  assets/bgm/
python3 talyx.py ls          confirms what is present and what is missing
python3 talyx.py verify lc300   the regression test - must say PASS all 10
```

## WHAT IS IN THE REPO (state at 2026-08-03)

```
talyx.py       CLI: plan · board · cost · ingest · build · verify · ls
planqc.py      GATE 1 - 18 checks incl. content block, before any credit
clipqc.py      GATE 1.5 - per-clip, between generation and edit (NEW today)
engine.py      the editor: beat grid, action peaks, shot match, blends, grade,
               cards-or-drawtext captions, sidechained SFX, atomic write
verify.py      GATE 2 - 10 checks on the finished cut, freshness first
board.py       storyboard renderer, draws FROM the plan

plans/         lc300 (historic, honestly failing) · supra (18/18) · i8
projects/      per-video workspaces + PRODUCTION.md + analysis evidence
assets/        pillars (measured targets) · nev/face (identity set) · nev/index.json
ledgers/       style_ledger (22 rejects) · knowledge (5 topics of lessons)
docs/          PIPELINE.md · ROADMAP.md · HANDOVER-2026-07-31.md · archive/
CLAUDE.md      project instructions + TITLE CONTRACT - auto-loads in Claude Code
RESUME-*.md    one-read session restore
```
