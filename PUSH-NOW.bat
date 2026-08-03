@echo off
cd /d "%~dp0"
title TALYX - push once, with full log
echo Working... everything is logged to work\sync-log.txt
echo.
(
  echo ===== PUSH-NOW %DATE% %TIME% =====
  git config --global --add safe.directory "%CD%"
  if exist ".git\index.lock" del /f /q ".git\index.lock"
  if exist ".git\refs\stash.lock" del /f /q ".git\refs\stash.lock"
  echo --- identity ---
  git config user.name
  git config user.email
  echo --- add ---
  git add -A 2>&1
  echo --- commit ---
  git commit -m "S450 build + sync scripts from desktop" 2>&1
  echo --- push ---
  git push origin main 2>&1
  echo --- final state ---
  git log --oneline -3 2>&1
  git status --porcelain 2>&1
  echo ===== END =====
) > "work\sync-log.txt" 2>&1
type "work\sync-log.txt"
echo.
echo Done. Claude can read work\sync-log.txt directly - no screenshot needed.
pause
