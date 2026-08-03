@echo off
cd /d "%~dp0"
title TALYX - Build "3 Best Spots in Kota Kinabalu"
if not exist "work\" mkdir "work"
echo Starting. All output is also saved to  work\last-run.txt
echo (the ffmpeg search can take a minute - let it run)
echo.
python "tools\run_kk.py" %*
echo.
pause
