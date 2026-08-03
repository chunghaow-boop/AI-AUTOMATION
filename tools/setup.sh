#!/usr/bin/env bash
# ONE-COMMAND SESSION SETUP — the sandbox wipes every session, this restores everything.
# Run:  bash tools/setup.sh
set +e
echo "=== Talyx/Nev video system — session setup ==="

echo "[1/4] python packages (pypi is allowlisted)"
pip install --quiet --break-system-packages \
  librosa soundfile pyloudnorm pytesseract pocketsphinx numpy pillow 2>&1 | tail -1

echo "[2/4] OCR languages (reads burned-in captions when images won't render)"
apt-get install -y -qq tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra \
  tesseract-ocr-msa espeak-ng 2>&1 | tail -1

echo "[3/4] verify"
python3 - <<'PY'
mods=["librosa","soundfile","pyloudnorm","pytesseract","pocketsphinx","numpy","PIL","playwright"]
for m in mods:
    try: __import__(m); print(f"  ok  {m}")
    except Exception: print(f"  !!  {m} MISSING")
PY
for b in ffmpeg ffprobe tesseract espeak-ng node; do
  command -v $b >/dev/null && echo "  ok  $b" || echo "  !!  $b MISSING"
done
tesseract --list-langs 2>/dev/null | tail -n +2 | tr '\n' ' ' | sed 's/^/  langs: /'; echo

echo "[4/4] ASR check (needs huggingface.co in the network allowlist)"
python3 - <<'PY'
import urllib.request, socket
socket.setdefaulttimeout(8)
try:
    urllib.request.urlopen("https://huggingface.co/api/models/Systran/faster-whisper-tiny")
    print("  ok  huggingface reachable -> run: pip install --break-system-packages faster-whisper")
    print("      then Whisper gives multilingual subtitle-grade transcription")
except Exception:
    print("  !!  huggingface BLOCKED -> add huggingface.co + cdn-lfs.huggingface.co to the")
    print("      network egress allowlist. Fallback is pocketsphinx (~30% accuracy, English only)")
PY
echo
echo "=== done. Read 22-HANDOVER.md, then RUNNER.md ==="
