@echo off
REM ===================================================================
REM  FINISH2.bat - 2026-08-12 - the fix for the FIFTH silent failure.
REM
REM  WHY v3 KEPT DYING (measured, not guessed):
REM    The fetch WORKED (FETCH_HEAD = bundle main, 12:06 today). The
REM    stash step FAILED SILENTLY (its errors go to 2>nul) and printed
REM    "nothing to stash" while 11 modified files stayed on disk. The
REM    ff-only merge then refused to overwrite them and the bat's
REM    failure text reads like a normal finish.
REM
REM  WHY DISCARDING THE LOCAL EDITS IS SAFE:
REM    All 11 dirty files were diffed against the bundle one by one.
REM    Every one is an OLDER mid-session state the bundle supersedes
REM    (planqc.py 1351 lines on disk vs 1711 in bundle, etc). Copies
REM    are in _backup_20260812_prefinish\ anyway.
REM ===================================================================
setlocal
cd /d "%~dp0"

echo === 0. clearing stale locks (a remote session cannot delete these) ===
del /f /q ".git\*.lock" 2>nul
del /f /q ".git\refs\heads\*.lock" 2>nul

echo.
echo === 1. discarding the superseded local edits (backed up already) ===
git checkout -f -- .
if errorlevel 1 goto :failed

echo.
echo === 2. fetching the bundle again (idempotent) ===
git fetch talyx-FINISH.bundle main
if errorlevel 1 goto :failed

echo.
echo === 3. fast-forwarding main e2b4485 -^> 00cc146 (27 commits) ===
git merge --ff-only FETCH_HEAD
if errorlevel 1 goto :failed

echo.
echo === 4. what landed ===
git log --oneline -5

echo.
echo === 5. pushing to GitHub ===
git push origin main
if errorlevel 1 goto :failed

echo.
echo ===================================================================
echo   DONE - and this time verify it yourself, one line:
echo       git log --oneline -1
echo   must start with 00cc146. If it does, tell the chat "00cc146".
echo ===================================================================
pause
exit /b 0

:failed
echo.
echo   STOPPED at the step above. DO NOT CLOSE THIS WINDOW.
echo   Photograph or copy the error text into the chat.
pause
exit /b 1
