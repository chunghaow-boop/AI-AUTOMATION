@echo off
REM ===================================================================
REM  REORG.bat - the doc reorganisation, 2026-08-07.
REM  Measured in DOC-AUDIT.md: 71 markdown files, 46 at the root, 595KB,
REM  and NINE of them all trying to be the entry point.
REM
REM  NOTHING IS DELETED. Every file is git mv'd into archive/ and every
REM  line stays in git history. Run it from C:\Users\User\Desktop\AI
REM  Undo: git reset --hard HEAD   (before you commit)
REM ===================================================================
cd /d "%~dp0"
echo.
echo   Moving 8 old RESUMEs, 5 superseded entry files and 10 superseded docs...
echo.
if not exist archive\resumes         mkdir archive\resumes
if not exist archive\entry-superseded mkdir archive\entry-superseded
if not exist archive\docs-superseded  mkdir archive\docs-superseded

for %%F in (RESUME-2026-08-04.md RESUME-2026-08-05.md RESUME-2026-08-05b.md RESUME-2026-08-05c.md RESUME-2026-08-05d.md RESUME-2026-08-06.md RESUME-2026-08-06b.md RESUME-2026-08-06c.md) do if exist %%F git mv %%F archive\resumes\

for %%F in (RUNNER.md SYNC.md FOLDER-MAP.md RECONCILE.md) do if exist %%F git mv %%F archive\entry-superseded\
if exist README.md if exist README-NEW.md git mv README.md archive\entry-superseded\README-old.md

for %%F in (START-HERE-2026-07-31.md HANDOVER-2026-07-31.md START-HERE-RESTORE.md HANDOVER-RESTORE-superseded.md README-RESTORE.md RUN.md RUNNER.md PIPELINE.md PIPELINE-V2.md V2-REBUILD.md) do if exist docs\%%F git mv docs\%%F archive\docs-superseded\

if exist README-NEW.md git mv -f README-NEW.md README.md

echo.
echo   DONE. Root .md should now be: the 29 numbered doctrine docs +
echo   CLAUDE.md SYSTEM-MAP.md RESUME-2026-08-07.md LESSONS.md DOC-AUDIT.md README.md
echo.
echo   Check it, then:  git add -A ^&^& git commit -m "doc reorg: four files own the entry"
echo   Undo instead:    git reset --hard HEAD
echo.
pause
