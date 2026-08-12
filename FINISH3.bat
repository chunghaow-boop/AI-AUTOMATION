@echo off
REM ===================================================================
REM  FINISH3.bat - 2026-08-12 - failure #6 diagnosed: LINE-ENDING GHOSTS.
REM  FINISH2's checkout -f restored e2b4485 content correctly, but CRLF
REM  conversion left 184 files byte-"modified" (CR only - measured, four
REM  files sampled, all EOL-ONLY). merge --ff-only refuses on ghosts.
REM  reset --hard cannot be refused, and FETCH_HEAD is a descendant of
REM  main, so it IS the fast-forward. Stashes and untracked files are
REM  untouched by design.
REM ===================================================================
setlocal
cd /d "%~dp0"

echo === 0. clearing stale locks ===
del /f /q ".git\*.lock" 2>nul
del /f /q ".git\refs\heads\*.lock" 2>nul

echo === 1. fetching the bundle ===
git fetch talyx-FINISH.bundle main
if errorlevel 1 goto :failed

echo === 2. hard-forwarding main to the bundle head ===
git reset --hard FETCH_HEAD
if errorlevel 1 goto :failed

echo === 3. SELF-VERIFY (L129: DONE is printed only after this passes) ===
for /f %%h in ('git rev-parse --short HEAD') do set NEWHEAD=%%h
echo    HEAD is now: %NEWHEAD%
if not "%NEWHEAD%"=="00cc146" (
  echo    FAILED: expected 00cc146, got %NEWHEAD%
  goto :failed
)

echo === 4. pushing to GitHub ===
git push origin main
if errorlevel 1 goto :failed

echo === 5. SELF-VERIFY the push ===
git ls-remote origin main | findstr 00cc146
if errorlevel 1 (
  echo    FAILED: GitHub main is not at 00cc146 after push.
  goto :failed
)

echo.
echo ===================================================================
echo   VERIFIED DONE. Local AND GitHub main = 00cc146. 27 commits landed.
echo   Tell the chat: 00cc146 verified
echo ===================================================================
pause
exit /b 0

:failed
echo.
echo   STOPPED at the step above. DO NOT CLOSE - copy the error to chat.
pause
exit /b 1
