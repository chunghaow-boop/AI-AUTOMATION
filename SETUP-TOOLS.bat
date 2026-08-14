@echo off
REM ============================================================
REM  SETUP-TOOLS.bat - one click: install everything the NEW
REM  tools need, then self-test each one.
REM
REM  Written 2026-08-06. Installs:
REM    pyflakes  - bugsense class 3 (undefined names). Without it
REM                that class prints NOT MEASURED instead of a
REM                clean nothing, which is correct but useless.
REM    yt-dlp    - reffetch.py, reference downloads
REM
REM  Does NOT touch opencv or numpy. BUILD_WRX.bat pins opencv to
REM  4.x on purpose (5.x removed CascadeClassifier, which clipqc's
REM  face gate needs). Nothing here may change that pin.
REM
REM  Safe to re-run. Everything is idempotent.
REM ============================================================
cd /d "%~dp0"
echo.
echo ============================================================
echo   TALYX TOOL SETUP
echo ============================================================
echo.

REM ---------------------------------------------------------- python
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] python is not on PATH.
    echo Install Python 3 from https://www.python.org/downloads/windows/
    echo and tick "Add python.exe to PATH" during install.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python -V 2^>^&1') do echo [ok]   %%v

REM ---------------------------------------------------------- ffmpeg
where ffmpeg >nul 2>nul
if errorlevel 1 (
    if exist "ffmpeg-extracted\bin\ffmpeg.exe" (
        echo [ok]   ffmpeg - local copy in ffmpeg-extracted\bin
    ) else (
        echo [WARN] ffmpeg not on PATH and no local copy found.
        echo        refsense/refstudy/storyboard need it. BUILD_WRX.bat
        echo        downloads it - run that once, then re-run this.
    )
) else (
    echo [ok]   ffmpeg on PATH
)

REM ---------------------------------------------------------- pyflakes
echo.
echo [1/3] pyflakes ...
python -c "import pyflakes" 2>nul || python -m pip install --quiet pyflakes
python -c "import pyflakes" 2>nul || ( echo [ERROR] pyflakes install failed - tell Claude & pause & exit /b 1 )
for /f "tokens=*" %%v in ('python -c "import pyflakes;print(pyflakes.__version__)" 2^>^&1') do echo       pyflakes %%v

REM ---------------------------------------------------------- yt-dlp
echo.
echo [2/3] yt-dlp ...
python -c "import yt_dlp" 2>nul || python -m pip install --quiet -U yt-dlp
python -c "import yt_dlp" 2>nul || ( echo [WARN] yt-dlp install failed - reffetch.py will not work, everything else will )

REM ---------------------------------------------------------- cv2 CHECK ONLY
echo.
echo [3/3] opencv check (NOT installed here - BUILD_WRX.bat owns the pin) ...
python -c "import cv2, numpy; cv2.CascadeClassifier; print('       opencv', cv2.__version__)" 2>nul || (
  echo [WARN] opencv missing or 5.x. Run BUILD_WRX.bat once - it pins 4.x.
)

REM ---------------------------------------------------------- SELF TEST
echo.
echo ============================================================
echo   SELF TEST - every new tool, on this repo
echo ============================================================
echo.

echo -- routing audit (must say CLEAN) --------------------------
python tools\mastermind_loop.py --audit
echo.

echo -- bugsense (structural defects) ---------------------------
python tools\bugsense.py > "%TEMP%\bugsense.txt" 2>&1
for /f "tokens=*" %%l in ('findstr /C:"finding(s)" "%TEMP%\bugsense.txt"') do echo    %%l
echo    full report: python tools\bugsense.py
echo.

echo -- storyboard (crown) --------------------------------------
python tools\storyboard.py crown
echo.

echo -- refsense (car_cinematic) --------------------------------
python tools\refsense.py --pillar car_cinematic --scan
echo.

echo ============================================================
echo   DONE
echo ============================================================
echo.
echo   NEXT, in order:
echo     python tools\refsense.py --pillar car_cinematic --strip
echo         then LOOK at assets\refs\car_cinematic\_strips\*.png
echo         and fill each one with --fill. That is the highest
echo         value zero-credit work available.
echo.
echo     python tools\mastermind_loop.py crown --stage plan
echo     start projects\crown\analysis\STORYBOARD.html
echo.
echo   OPTIONAL - the LLM judge calls the Anthropic API. Without a
echo   key it writes a packet you paste into Claude instead, which
echo   works fine. To enable direct calls, set the key ONCE:
echo       setx ANTHROPIC_API_KEY "sk-ant-..."
echo   then open a NEW terminal (setx does not affect this one).
echo.
pause
