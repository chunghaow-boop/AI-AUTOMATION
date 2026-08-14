# FOLDER MAP — what everything is, one line each (2026-08-04)

## YOU CLICK THESE
BUILD_WRX.bat        build the current WRX video on this machine
PUSH.bat / PULL.bat  sync with GitHub (push after sessions, pull on the other PC)
START-NEW-CHAT.txt   the 3-step ritual for ending/starting a chat

## CLAUDE READS THESE FIRST
CLAUDE.md            the contract + hard rules (auto-loaded)
RESUME-2026-08-04.md newest session handover — where everything stands
README.md            project entry point

## DOCTRINE (00–26, root, DO NOT MOVE — RUNNER references these names)
00–26-*.md           the crew: beats, roles, judges, banks, scorecard, handover(22)
RUNNER.md            how the numbered docs chain together
RECONCILE.md         how desktop docs + laptop engine became one system
SYNC.md              the two-machine git workflow

## THE PIPELINE (code, root, DO NOT MOVE — paths are relative)
talyx.py             the CLI: plan/board/cost/ingest/build/verify
engine.py            the generic builder (plan in, video out)
planqc.py            19-check plan gate (free, pre-spend)
clipqc.py            per-clip gate (the paid artefacts)
verify.py            10-check cut gate
board.py             storyboard renderer
i8_plan.py           plan-as-data reference

## FOLDERS
plans/               one .py per video — the plan IS the data
projects/            per-video work: clips, audio, output, analysis
assets/              fonts, pillars (measured profiles), nev identity, bgm
tools/               fx, cards, phonk, sfxgen, rhythm + helpers
ledgers/             rejects + lessons (merge, never overwrite)
docs/                superseded/long-form docs (safe to ignore day-to-day)
scripts/, skills/    helpers + the talyx-cinematic skill
archive/             old handovers + retired one-off bats
reference/, system/  desktop-era leftovers, kept for history

## IGNORE
ffmpeg.zip           mid-download artifact — BUILD_WRX.bat manages it
ffmpeg-extracted/    local ffmpeg install (gitignored)
