@echo off
REM ============================================================
REM  PUSH.bat - one click: commit everything + push to GitHub
REM  Repo: https://github.com/chunghaow-boop/AI-AUTOMATION
REM  First run: a browser window opens for GitHub sign-in.
REM ============================================================
cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
    echo [ERROR] git is not installed.
    echo Install it from https://git-scm.com/download/win then run this again.
    pause
    exit /b 1
)

REM --- SELF-HEAL (2026-08-05): remote Claude sessions run git through the
REM --- desktop bridge, which cannot delete git's own lock files - they pile
REM --- up and block the next git command. Local git CAN delete them, so this
REM --- clears any stale locks + bridge leftovers before every push. Safe:
REM --- if a real git process were running, you would not be double-clicking this.
del /f /q ".git\index.lock" ".git\HEAD.lock" ".git\objects\maintenance.lock" 2>nul
del /f /q ".git\objects\*\tmp_obj_*" 2>nul
if exist "_to_delete" rmdir /s /q "_to_delete" 2>nul

REM point at the repo (ignored if already set)
git remote add origin https://github.com/chunghaow-boop/AI-AUTOMATION.git 2>nul

echo.
echo === pulling latest from GitHub first (other machine's work) ===
git pull origin main --allow-unrelated-histories --no-edit 2>nul

echo.
echo === committing local changes ===
git add -A
git commit -m "session %date% %time%" 2>nul
if errorlevel 1 echo (nothing new to commit - pushing anyway)

echo.
echo === pushing to GitHub ===
git push -u origin main
if errorlevel 1 (
    echo.
    echo [PUSH FAILED] Most likely the browser sign-in was cancelled,
    echo or there is a conflict in ledgers/ - those must be MERGED, not overwritten.
    echo Run this file again after signing in.
) else (
    echo.
    echo [OK] Pushed. Check: https://github.com/chunghaow-boop/AI-AUTOMATION
)
echo.
pause
