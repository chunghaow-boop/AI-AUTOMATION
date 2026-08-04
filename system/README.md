# Talyx / Nev — AI Video Production System

24 markdown files that turn **one video title** into a finished, postable 9:16 video.

## ⚡ STANDING ORDER (from the user, applies every session)
**Claude pulls this repo automatically at session start — no need to be asked.**
**Claude rebuilds the zip and says "commit these" at session end — no need to be asked.**
Claude CANNOT push (tokens are off-limits). The user commits.

## For Claude — boot sequence
```
1. git clone --depth 1 https://github.com/<user>/<repo>.git /home/claude/sys
2. Read 22-HANDOVER.md   ← state: open threads, credit balance, what's proven
3. Read RUNNER.md        ← process: the 12 steps
4. Everything else is reference — read only when a task needs it.
```
**Do not read every file on boot.** Context is the bill.

## The contract (file 18)
User gives a TITLE. Agent derives everything else.
Phase 1 free + autonomous → **⏸ one gate: full prompt + scores + exact cost** → Phase 2 paid + autonomous → finished mp4.

## Map
| | |
|---|---|
| `22-HANDOVER.md` | **read first** — current state |
| `RUNNER.md` | the 12-step process |
| `16-master-skeleton.md` | architecture: all seats, banks, models |
| `17-car-cinematic-master-prompt.md` | ⭐ proven multi-shot template |
| `18-agent-contract.md` | the spec / checklist / inspector / budget |
| `09-learning-log.md` | 30 entries — what was learned, and from what |
| `13-role-asset-banks.md` | ~320 assets across 11 banks |
| `/archive/` | rolled-off handover history, append-only |

## Verified environment facts
- `git clone` and `raw.githubusercontent.com` reachable from the sandbox ✅
- `api.github.com` returns 403 ❌
- Claude **cannot push** — it prepares files, the user commits
- Sandbox resets each session: `pip install --break-system-packages librosa soundfile` for audio work
