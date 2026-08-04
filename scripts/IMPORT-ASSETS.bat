@echo off
REM Double-click this. Sorts SFX/BGM/B-roll/Nev from Downloads into assets/
cd /d "%~dp0"
echo ==================================================
echo  TALYX ASSET IMPORT
echo ==================================================
echo.
echo [STEP 1 of 2] DRY RUN - shows what WOULD move. Nothing is touched.
echo.
python tools\import_assets.py --dry-run
if errorlevel 1 python3 tools\import_assets.py --dry-run
echo.
echo ==================================================
echo  Review the list above.
echo  Only SFX_* BGM_* BROLL_* and the Nev zip are touched.
echo  Your own footage is NOT matched and will NOT move.
echo ==================================================
echo.
set /p GO="Type Y then Enter to import for real (anything else cancels): "
if /i not "%GO%"=="Y" goto :cancel
echo.
echo [STEP 2 of 2] Importing and measuring...
python tools\import_assets.py
if errorlevel 1 python3 tools\import_assets.py
echo.
echo ==================================================
python tools\preflight.py
if errorlevel 1 python3 tools\preflight.py
goto :end
:cancel
echo Cancelled. Nothing was moved.
:end
echo.
pause
