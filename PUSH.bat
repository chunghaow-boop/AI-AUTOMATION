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
