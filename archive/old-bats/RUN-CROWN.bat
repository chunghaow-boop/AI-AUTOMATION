@echo off
cd /d "%~dp0"
title TALYX - Toyota Crown 2026 - 15s cinematic
if not exist "work\" mkdir "work"
echo Step 1 of 2  importing the 4 Crown renders from your Downloads
echo             (they arrive named hf_*.mp4 and get renamed automatically)
echo.
python "tools\import_bank.py" --days 2
echo.
echo Step 2 of 2  building
echo.
python "tools\build_crown.py"
echo.
if exist "output\CROWN_15S_v1.mp4" (
  echo   FINAL: %~dp0output\CROWN_15S_v1.mp4
  start "" "%~dp0output"
)
pause
