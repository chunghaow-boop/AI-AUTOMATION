#!/usr/bin/env bash
# TALYX — local setup. Run on YOUR machine, where the network is unrestricted.
# Unlocks Whisper: the one component the Cowork sandbox cannot have.
set +e
echo "=================================================="
echo " TALYX AI VIDEO AUTOMATION — local setup"
echo "=================================================="
OS="$(uname -s)"

echo "[1/5] ffmpeg"
if command -v ffmpeg >/dev/null; then echo "  ok  ffmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3)"
else
  echo "  !! MISSING."
  [ "$OS" = "Darwin" ] && echo "     brew install ffmpeg"
  [ "$OS" = "Linux" ]  && echo "     sudo apt install -y ffmpeg"
  echo "     Windows: winget install Gyan.FFmpeg"
fi

echo "[2/5] python packages"
PIPFLAGS=""; python3 -c "import sys;sys.exit(0)" 2>/dev/null && PIPFLAGS="--break-system-packages"
pip install $PIPFLAGS -q faster-whisper opencv-python-headless numpy \
    librosa soundfile pyloudnorm playwright 2>&1 | tail -2
echo "      installing chromium for card rendering (~150MB, one time)"
python3 -m playwright install chromium 2>&1 | tail -2

echo "[3/5] Node + Claude Code (for the local agent)"
if command -v node >/dev/null; then echo "  ok  node $(node -v)"
else echo "  !! install Node 18+ from https://nodejs.org then: npm i -g @anthropic-ai/claude-code"; fi
command -v claude >/dev/null && echo "  ok  claude code installed" \
  || echo "  -> npm install -g @anthropic-ai/claude-code   (then run: claude)"

echo "[4/5] whisper model warm-up (downloads weights ~74MB for 'base')"
python3 - <<'PY'
try:
    from faster_whisper import WhisperModel
    WhisperModel("base", device="cpu", compute_type="int8")
    print("  ok  faster-whisper 'base' ready")
    print("      -> UNLOCKED: filler-word cuts, sentence jump cuts, retake detection,")
    print("                   hook selection from text, word-exact captions")
except Exception as e:
    print("  !!  faster-whisper failed:", str(e)[:110])
PY

echo "[5/5] verify the toolchain"
python3 - <<'PY2'
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b=p.chromium.launch(); b.close()
    print("  ok  playwright + chromium -> designed HTML/CSS cards UNLOCKED")
except Exception as e:
    print("  !!  playwright:", str(e)[:100])
PY2
python3 - <<'PY'
for m in ["cv2","numpy","librosa","soundfile"]:
    try: __import__(m); print(f"  ok  {m}")
    except Exception: print(f"  !!  {m} MISSING")
PY
for b in ffmpeg ffprobe; do command -v $b >/dev/null && echo "  ok  $b" || echo "  !!  $b MISSING"; done

echo
echo "=================================================="
echo " NEXT:"
echo "   1. claude                      # start the local agent here"
echo "   2. /talyx-shotlist <title>     # Phase 1, gated, costed"
echo "   3. python3 tools/transcribe.py IN.mp4 -o t.json"
echo "   4. python3 tools/autocut.py IN.mp4 t.json --captions -o OUT.mp4"
echo "   5. python3 tools/cards.py checklist --title \"Before you pay deposit\" --items items.txt -o card.png"
echo "   6. python3 tools/mastermind.py OUT.mp4    # the gate"
echo "=================================================="
