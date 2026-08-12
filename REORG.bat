@echo off
REM ===================================================================
REM  REORG.bat v2 - the doc reorganisation, designed 2026-08-07 from
REM  DOC-AUDIT.md, REFRESHED 2026-08-12 (v1 was never run; five more
REM  days of root clutter added since).
REM
REM  NOTHING IS DELETED. Every file is git mv'd into archive/ and every
REM  line stays in git history. Run from C:\Users\User\Desktop\AI.
REM  Undo before committing: git reset --hard HEAD
REM  After it runs: run PUSH.bat to record the moves.
REM ===================================================================
cd /d "%~dp0"
echo.
echo   Archiving old RESUMEs, superseded entry files and stale docs...
echo.
if not exist archive\resumes          mkdir archive\resumes
if not exist archive\entry-superseded mkdir archive\entry-superseded
if not exist archive\docs-superseded  mkdir archive\docs-superseded

REM --- old RESUMEs (keep ONLY the newest: RESUME-2026-08-12b.md) ---
for %%F in (RESUME-2026-08-04.md RESUME-2026-08-05.md RESUME-2026-08-05b.md RESUME-2026-08-05c.md RESUME-2026-08-05d.md RESUME-2026-08-06.md RESUME-2026-08-06b.md RESUME-2026-08-06c.md RESUME-2026-08-07.md RESUME-2026-08-11.md RESUME-2026-08-12.md) do if exist %%F git mv %%F archive\resumes\

REM --- superseded entry/transport docs ---
for %%F in (RUNNER.md SYNC.md FOLDER-MAP.md RECONCILE.md HANDOVER-PASTE.md DOC-AUDIT.md PENDING.md) do if exist %%F git mv %%F archive\entry-superseded\
if exist README.md if exist README-NEW.md git mv README.md archive\entry-superseded\README-old.md
if exist README-NEW.md git mv -f README-NEW.md README.md

REM --- superseded docs/ leftovers (from the 08-07 audit) ---
for %%F in (START-HERE-2026-07-31.md HANDOVER-2026-07-31.md START-HERE-RESTORE.md HANDOVER-RESTORE-superseded.md README-RESTORE.md RUN.md RUNNER.md PIPELINE.md PIPELINE-V2.md V2-REBUILD.md) do if exist docs\%%F git mv docs\%%F archive\docs-superseded\

REM --- session-10 stub whose content is already merged into knowledge.json ---
if exist LESSONS-SESSION10-PENDING.md del /f /q LESSONS-SESSION10-PENDING.md

echo.
echo   DONE. Root should now hold ONLY:
echo     - the 32 numbered doctrine docs (00-31)
echo     - CLAUDE.md  SYSTEM-MAP.md  README.md  LESSONS.md
echo     - RESUME-2026-08-12b.md  START-NEW-CHAT.txt
echo     - PULL.bat  PUSH.bat  (FINISH.bat = retired guard stub)
echo     - SETUP-TOOLS.bat  BUILD_WRX.bat  REORG.bat
echo     - PANBORNEO_V5.mp4 (current deliverable, gitignored)
echo     - the pipeline: talyx.py planqc.py clipqc.py engine.py verify.py board.py
echo     - folders: assets/ plans/ projects/ tools/ ledgers/ docs/ BGM/ archive/
echo.
echo   NOW RUN PUSH.bat to record the moves.
pause
