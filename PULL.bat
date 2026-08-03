@echo off
REM ============================================================
REM  PULL.bat - one click: fetch the latest work from GitHub
REM  Run this FIRST when you sit down at a machine.
REM  (PUSH.bat when you stand up; PULL.bat when you sit down.)
REM ============================================================
cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
    echo [ERROR] git is not installed.
    echo Install it from https://git-scm.com/download/win then run this again.
    pause
    exit /b 1
)

git remote add origin https://github.com/chunghaow-boop/AI-AUTOMATION.git 2>nul

echo === pulling latest from GitHub ===
git pull origin main --no-edit
if errorlevel 1 (
    echo.
    echo [PULL FAILED] If it mentions ledgers/ conflicts: those files must be
    echo MERGED - both machines' entries are real history. Ask Claude to merge them.
) else (
    echo.
    echo [OK] Up to date.
)
echo.
pause
