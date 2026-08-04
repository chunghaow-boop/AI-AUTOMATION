@echo off
cd /d "%~dp0"
title TALYX - Auto-file downloads into the AI folder
echo ======================================================
echo   WATCHER
echo   Leave this window open. Anything you download from
echo   Higgsfield, Drive or Google Fonts gets filed into the
echo   AI folder automatically - no manual moving.
echo.
echo   Nothing is ever overwritten.
echo   Close this window (or Ctrl+C) to stop.
echo ======================================================
echo.
python "tools\watcher.py" %*
pause
