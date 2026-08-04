@echo off
REM ============================================================
REM  BUILD_WRX — one click on the laptop/desktop: clips -> cut
REM  Written 2026-08-04 after the sandbox-build lesson: the
REM  remote sandbox gates CLIPS; only THIS machine builds VIDEO
REM  (full toolchain, Playwright cards, CDN access, no vanishing
REM  filesystem). Safe to re-run: downloads and bed are cached.
REM ============================================================
cd /d "%~dp0"

echo [1/5] downloading the 9 gated clips (skips ones already here)...
if not exist projects\wrx\clips mkdir projects\wrx\clips
cd projects\wrx\clips
set B=https://d8j0ntlcm91z4.cloudfront.net/user_3AmHAoGOCTD0Ph5D4HI7jSA04wi
for %%J in (
  hf_20260804_090255_25e603b7-bd83-446a-b48a-56a8b8e7faa5.mp4
  hf_20260804_092131_fba6d6df-a444-4e66-82ca-0ea3f6d064fd.mp4
  hf_20260804_092131_e93e708b-ace7-4085-ba6f-6935bd187fe9.mp4
  hf_20260804_092131_0baee410-124b-4186-9874-5ad1ca96db5b.mp4
  hf_20260804_092131_97f49b91-20f5-4c31-aae2-9e44d5a17b65.mp4
  hf_20260804_092131_f0773cd0-4ddf-4d31-9f45-c03e78df9b8b.mp4
  hf_20260804_092131_0d24d3a0-d84a-4611-8ff8-f448b88ab9fc.mp4
  hf_20260804_092131_dd1a60de-9b55-46ff-9c3b-9e41c68bfae7.mp4
  hf_20260804_092131_b12932b6-d078-4246-8ce1-5569470b02f6.mp4
) do (
  if not exist %%J curl -sf -O "%B%/%%J"
)
cd ..\..\..

echo [2/5] music bed (phonk 150) if missing...
if not exist projects\wrx\audio mkdir projects\wrx\audio
if not exist projects\wrx\audio\BGM_phonk_150.wav (
  if exist assets\bgm\BGM_phonk_150.wav (
    copy /y assets\bgm\BGM_phonk_150.wav projects\wrx\audio\ >nul
  ) else (
    python tools\phonk.py --out projects\wrx\audio --bpm 150 --dur 24
  )
)

echo [3/5] per-clip gate (clipqc)...
python clipqc.py wrx
if errorlevel 1 (
  echo.
  echo  !! clipqc BLOCKED a clip - do not build around it. Tell Claude.
  pause
  exit /b 1
)

echo [4/5] build...
python talyx.py build wrx
if errorlevel 1 ( echo build failed & pause & exit /b 1 )

echo [5/5] verify...
set TALYX_PROJECT=wrx
python verify.py

echo.
echo Output: projects\wrx\output\WRX_CINEMATIC_v1.mp4
start "" "projects\wrx\output\WRX_CINEMATIC_v1.mp4"
pause
