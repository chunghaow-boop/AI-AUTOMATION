@echo off
REM ===================================================================
REM  FINISH.bat  -  apply this session's commits and push to GitHub
REM
REM  FIXED 2026-08-11 (lesson craft L118): the previous version ran
REM  `git stash push -u` with no excludes, so the stash swallowed the
REM  UNTRACKED FINISH.bat ITSELF mid-run - Windows reads .bat files
REM  line by line from disk, so the script died the moment the stash
REM  took it, before a single commit applied. Gavril ran it at 20:17
REM  and it silently self-destructed. The stash now excludes this file
REM  and the bundle, and this file is TRACKED in the repo from now on.
REM
REM  Your loose changes still go into a stash named pre-finish-backup.
REM  Recover with:  git stash list   /   git stash pop
REM ===================================================================
setlocal
cd /d "%~dp0"

echo.
echo === 0. clearing any stale lock ===
if exist ".git\index.lock" (
  del /f /q ".git\index.lock"
  echo    removed .git\index.lock
) else (
  echo    no lock present
)

echo.
echo === 1. where are we ===
git rev-parse --abbrev-ref HEAD
git log --oneline -1
echo.

echo === 2. backing up loose files (NOT this script, NOT the bundle) ===
git stash push -u -m "pre-finish-backup" -- . ":(exclude)FINISH.bat" ":(exclude)talyx-FINISH.bundle" 2>nul
if errorlevel 1 (
  echo    nothing to stash, working tree already clean
) else (
  echo    stashed. recover any time with:  git stash pop
)

echo.
echo === 3. applying this session's commits ===
if not exist "talyx-FINISH.bundle" (
  echo    ERROR: talyx-FINISH.bundle is not in this folder.
  echo    Put it beside this .bat file and run again.
  pause
  exit /b 1
)
git bundle verify talyx-FINISH.bundle
if errorlevel 1 (
  echo    ERROR: the bundle does not apply to this repo.
  echo    Send me the output of:  git log --oneline -1
  pause
  exit /b 1
)
git fetch talyx-FINISH.bundle main:finish-tmp
if errorlevel 1 goto :failed

git merge --ff-only finish-tmp
if errorlevel 1 (
  echo.
  echo    ff-only merge refused - your main has diverged.
  echo    Nothing was changed. Send me the output of:  git log --oneline -5
  pause
  exit /b 1
)
git branch -d finish-tmp >nul 2>&1

echo.
echo === 4. what landed ===
git log --oneline -16
echo.

echo === 5. pushing to GitHub ===
echo    (Windows may ask you to sign in - that is your credential manager,
echo     not this script. Nothing here stores or reads your password.)
git push origin main
if errorlevel 1 goto :failed

echo.
echo ===================================================================
echo   DONE. github.com/chunghaow-boop/AI-AUTOMATION is up to date.
echo.
echo   Your previous loose files are in the stash:
echo       git stash list
echo       git stash show -p "stash@{0}"
echo   Most are older copies of what just landed - review before popping.
echo ===================================================================
pause
exit /b 0

:failed
echo.
echo   STOPPED. Nothing was pushed. Send me the error above.
pause
exit /b 1
