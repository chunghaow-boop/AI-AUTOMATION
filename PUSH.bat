@echo off
REM ============================================================
REM  PUSH.bat v2 (2026-08-12) - one click: commit + sync + push,
REM  with L129 self-verification. Repo: github.com/chunghaow-boop/AI-AUTOMATION
REM
REM  v2 fixes (his catch: "multiple ways of pushing is causing bugs"):
REM  - v1 hid pull errors with 2>nul, then ran `git add -A` anyway:
REM    a conflicted pull would have COMMITTED CONFLICT MARKERS silently.
REM    Now: commit FIRST, then pull --rebase with errors VISIBLE, and the
REM    script STOPS on conflict instead of pushing broken files.
REM  - DONE is printed only after ls-remote proves GitHub == local HEAD.
REM  - FINISH*/PUSH-NOW retired; PULL.bat to sit down, this to stand up.
REM ============================================================
setlocal
cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
    echo [ERROR] git is not installed. https://git-scm.com/download/win
    pause & exit /b 1
)

REM --- janitor: bridge sessions cannot delete; clear their leftovers ---
del /f /q ".git\*.lock" 2>nul
del /f /q ".git\refs\heads\*.lock" 2>nul
del /f /q ".git\objects\*.lock" 2>nul
del /f /q ".git\objects\*\tmp_obj_*" 2>nul
if exist "_to_delete" rmdir /s /q "_to_delete" 2>nul

git remote add origin https://github.com/chunghaow-boop/AI-AUTOMATION.git 2>nul

echo === 1. committing local changes (errors visible) ===
git add -A
git commit -m "session %date% %time%"
if errorlevel 1 echo    (nothing new to commit)

echo.
echo === 2. syncing with GitHub (rebase, errors visible) ===
git pull --rebase origin main
if errorlevel 1 (
    echo.
    echo   STOPPED: the pull failed. Nothing is lost. READ THE LINE ABOVE:
    echo   - "Failed to connect" / "Could not resolve host" = NETWORK, not a
    echo     conflict. Your commit is safe locally - just RE-RUN this file
    echo     when the internet is back.
    echo   - "CONFLICT" / "could not apply" = real conflict. Do NOT re-run;
    echo     copy the message into the chat. ledgers/ conflicts must be
    echo     MERGED - both machines' entries are real.
    pause & exit /b 1
)

echo.
echo === 3. pushing ===
git push -u origin main
if errorlevel 1 (
    echo.
    echo   STOPPED: push failed (sign-in cancelled?). Run this file again.
    pause & exit /b 1
)

echo.
echo === 4. SELF-VERIFY (DONE is a measurement, not a feeling - L129) ===
for /f %%h in ('git rev-parse HEAD') do set LOCALHEAD=%%h
git ls-remote origin main | findstr /b "%LOCALHEAD%" >nul
if errorlevel 1 (
    echo   FAILED: GitHub main does not match local HEAD %LOCALHEAD%.
    echo   Copy this message to the chat.
    pause & exit /b 1
)
echo   VERIFIED: GitHub main == local HEAD %LOCALHEAD:~0,7%
echo.
echo [OK] Pushed and verified. https://github.com/chunghaow-boop/AI-AUTOMATION
pause
exit /b 0
