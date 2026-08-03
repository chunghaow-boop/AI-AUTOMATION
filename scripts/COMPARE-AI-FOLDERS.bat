@echo off
setlocal EnableDelayedExpansion
title TALYX - Compare AI folders (READ ONLY)
cd /d "%~dp0"

echo ======================================================
echo   COMPARE AI FOLDERS   -   READ ONLY
echo   Moves nothing. Deletes nothing. Just reports.
echo ======================================================
echo.

set "LIVE=%~dp0"
if "%LIVE:~-1%"=="\" set "LIVE=%LIVE:~0,-1%"
echo   LIVE  (the one Claude can see) : %LIVE%

REM ---- find the other AI folder ----
set "OTHER="
if not "%~1"=="" set "OTHER=%~1"
if not defined OTHER (
  for %%C in ("D:\AI" "D:\USER FOLDER IMPORTANT\AI" "C:\AI" "%USERPROFILE%\AI" ^
              "D:\UserFolders\AI" "D:\USER FOLDER IMPORTANT\Documents\AI") do (
    if not defined OTHER if exist "%%~C\" (
      if /i not "%%~C"=="%LIVE%" set "OTHER=%%~C"
    )
  )
)
if not defined OTHER (
  echo.
  echo   Could not auto-find a second AI folder.
  echo   Drag the other AI folder onto this .bat file, or run:
  echo       COMPARE-AI-FOLDERS.bat "D:\path\to\other\AI"
  echo.
  pause
  exit /b 1
)
echo   OTHER (the duplicate)          : %OTHER%
echo.

set "REP=%LIVE%\work\folder-compare.txt"
if not exist "%LIVE%\work\" mkdir "%LIVE%\work"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$live='%LIVE%'; $other='%OTHER%'; $rep='%REP%';" ^
  "function Inv($root){ Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue |" ^
  "  ForEach-Object { [pscustomobject]@{ rel=$_.FullName.Substring($root.Length).TrimStart('\'); size=$_.Length; mt=$_.LastWriteTime } } }" ^
  "$L=@{}; Inv $live  | ForEach-Object { $L[$_.rel]=$_ };" ^
  "$O=@{}; Inv $other | ForEach-Object { $O[$_.rel]=$_ };" ^
  "$onlyO = $O.Keys | Where-Object { -not $L.ContainsKey($_) } | Sort-Object;" ^
  "$onlyL = $L.Keys | Where-Object { -not $O.ContainsKey($_) } | Sort-Object;" ^
  "$diff  = $O.Keys | Where-Object { $L.ContainsKey($_) -and $L[$_].size -ne $O[$_].size } | Sort-Object;" ^
  "$out = New-Object System.Collections.Generic.List[string];" ^
  "$out.Add('AI FOLDER COMPARISON  ' + (Get-Date));" ^
  "$out.Add('LIVE  : ' + $live + '   (' + $L.Count + ' files)');" ^
  "$out.Add('OTHER : ' + $other + '   (' + $O.Count + ' files)');" ^
  "$out.Add('');" ^
  "$out.Add('=== ONLY IN THE OTHER FOLDER  (' + @($onlyO).Count + ')  <-- these would be LOST if you delete it ===');" ^
  "foreach($k in $onlyO){ $out.Add(('  {0,12:N0}  {1}' -f $O[$k].size, $k)) }" ^
  "$out.Add('');" ^
  "$out.Add('=== ONLY IN THE LIVE FOLDER  (' + @($onlyL).Count + ') ===');" ^
  "foreach($k in $onlyL){ $out.Add(('  {0,12:N0}  {1}' -f $L[$k].size, $k)) }" ^
  "$out.Add('');" ^
  "$out.Add('=== SAME NAME, DIFFERENT SIZE  (' + @($diff).Count + ')  <-- check which is newer ===');" ^
  "foreach($k in $diff){ $out.Add(('  live {0,12:N0} {1}   other {2,12:N0} {3}   {4}' -f $L[$k].size,$L[$k].mt.ToString('yyyy-MM-dd HH:mm'),$O[$k].size,$O[$k].mt.ToString('yyyy-MM-dd HH:mm'),$k)) }" ^
  "$bigO = $O.Keys | Where-Object { -not $L.ContainsKey($_) } | Sort-Object { -$O[$_].size } | Select-Object -First 15;" ^
  "$out.Add('');" ^
  "$out.Add('=== BIGGEST FILES THAT EXIST ONLY IN THE OTHER FOLDER ===');" ^
  "foreach($k in $bigO){ $out.Add(('  {0,12:N0}  {1}' -f $O[$k].size, $k)) }" ^
  "$out | Set-Content -LiteralPath $rep -Encoding UTF8;" ^
  "Write-Host ('  LIVE  files : ' + $L.Count);" ^
  "Write-Host ('  OTHER files : ' + $O.Count);" ^
  "Write-Host ('');" ^
  "Write-Host ('  only in OTHER : ' + @($onlyO).Count + '   <-- lost if you delete it');" ^
  "Write-Host ('  only in LIVE  : ' + @($onlyL).Count);" ^
  "Write-Host ('  size mismatch : ' + @($diff).Count);" ^
  "if(@($onlyO).Count -gt 0){ Write-Host ''; Write-Host '  Top unique files in the OTHER folder:'; foreach($k in ($bigO | Select-Object -First 8)){ Write-Host ('    ' + $k) } }"

echo.
echo ------------------------------------------------------
echo   Full report written to:
echo     %REP%
echo.
echo   NOTHING WAS MOVED OR DELETED.
echo   Read the report. If "only in OTHER" is 0, the duplicate
echo   is redundant and safe to archive. If it is not 0, copy
echo   those files across FIRST.
echo ------------------------------------------------------
echo.
pause
