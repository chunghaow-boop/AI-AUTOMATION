@echo off
REM ===================================================================
REM  RETIRED 2026-08-12. The bundle transport is DEAD (L132/L135).
REM  This script applied talyx-FINISH.bundle - that bundle landed at
REM  00cc146 and the repo has moved past it. Running any bundle-apply
REM  now would ROLL THE REPO BACK.
REM
REM  The only two sync scripts:
REM      PULL.bat  - when you sit down
REM      PUSH.bat  - when you stand up
REM  History of the 6 silent failures: knowledge.json L127, L129-L134.
REM ===================================================================
echo.
echo   RETIRED. Use PUSH.bat to push, PULL.bat to pull.
echo   (This file is kept only so old instructions fail loudly, not silently.)
echo.
pause
exit /b 1
