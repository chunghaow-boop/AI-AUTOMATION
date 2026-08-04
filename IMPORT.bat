@echo off
cd /d "%~dp0"
title TALYX - Import downloads into assets
if not exist "work\" mkdir "work"
echo Searching your drives for recent downloads and sorting them into assets\
echo Nothing is ever overwritten. Output is saved to work\last-import.txt
echo.
python "tools\import_bank.py" %* > "work\last-import.txt" 2>&1
type "work\last-import.txt"
echo.
pause
