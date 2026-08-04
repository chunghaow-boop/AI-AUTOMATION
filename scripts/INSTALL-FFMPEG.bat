@echo off
cd /d "%~dp0"
title TALYX - Install ffmpeg
echo ======================================================
echo   INSTALL FFMPEG
echo ======================================================
echo.
echo   This will DOWNLOAD AND INSTALL software on your PC.
echo.
echo   What it does, in order:
echo     1. winget install Gyan.FFmpeg      (official Windows package manager)
echo     2. if winget is unavailable: tells you the manual download link
echo     3. verifies that BOTH ffmpeg.exe and ffprobe.exe now exist
echo.
echo   Why: the ffmpeg inside D:\capcut is a partial bundle - it has
echo   ffmpeg.exe but no ffprobe.exe, so it cannot measure durations.
echo   Every tool in this repo needs both.
echo.
echo   Press Ctrl+C to cancel, or
pause
echo.

where winget >nul 2>&1
if errorlevel 1 goto :nowinget

echo   Running: winget install Gyan.FFmpeg
echo.
winget install Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
echo.
echo ------------------------------------------------------
echo   Install finished. Verifying...
echo ------------------------------------------------------
python "tools\run_kk.py" --dry-run
echo.
echo   If it still says ffmpeg not found, CLOSE this window and
echo   open a NEW one - PATH changes only apply to new processes.
echo   Then double-click RUN-KK.bat
echo.
pause
exit /b 0

:nowinget
echo   ^^! winget is not available on this machine.
echo.
echo     Manual route (5 minutes):
echo       1. Go to  https://www.gyan.dev/ffmpeg/builds/
echo       2. Download  ffmpeg-release-full.7z   (or the .zip)
echo       3. Extract it
echo       4. Open the extracted folder, then  bin\
echo       5. Copy BOTH  ffmpeg.exe  and  ffprobe.exe  into:
echo            %~dp0
echo       6. Double-click RUN-KK.bat - it checks this folder first
echo.
pause
exit /b 1
