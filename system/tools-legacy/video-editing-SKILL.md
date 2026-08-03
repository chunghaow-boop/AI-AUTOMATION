---
name: video-editing
description: Automated video editing primitives — auto jump-cut (silence removal) for talking-head content, frame-burst montage cutting, batch processing, and the honest map of which editing capabilities work in this sandbox versus which need external tools. Use whenever assembling or tightening any video.
---

# Video editing automation

## 1. AUTO JUMP-CUT — the highest-value tool (WORKING)
Removes every pause automatically. **This is the Recipe 7 primitive** — the Chinese talking-head
reference cut every breath and "um", which is what created its 3.1s-average cut density.
Doing that by hand is hours; this is one command.

```bash
python3 /mnt/skills/user/video-editing/autojumpcut.py in.mp4 out.mp4 [--db -32] [--min 0.30] [--pad 0.05]
```
| Flag | Meaning | Tune when |
|---|---|---|
| `--db` | silence threshold | quiet room → `-40`, noisy → `-25` |
| `--min` | min pause length to cut | `0.20` = aggressive, `0.50` = gentle |
| `--pad` | breath left at each edge | raise to `0.08` if words clip |

**Verified:** 9.0s test → 5.5s out, 5 silences removed, 39% tightened.
**Workflow:** shoot talking head → autojumpcut → captions → done. Zero credits, zero AI.

## 2. THE FRAME-BURST (learned from a viral reference)
A 123s reference contained a burst where cuts were **0.03–0.1s apart — 1 to 3 FRAMES each.**
Far more aggressive than a normal 0.5s burst.
```bash
# 1-3 frame cuts, stacked on a music hit
ffmpeg -ss <t> -i in.mp4 -frames:v 2 -c:v libx264 -crf 18 shard.mp4   # 2 frames @30fps = 0.066s
```
Use for: the drop, a decision moment, a "brain overload" beat. **Max ~1.5s total** or it reads
as noise. Always land the FIRST frame of the burst on the beat.

## 3. BATCH PROCESSING
```bash
for f in *.mp4; do ffmpeg -v error -y -i "$f" -vf "eq=contrast=1.05:saturation=1.05,fps=30" \
  -c:v libx264 -crf 19 "out_${f}"; done
```

## 4. WHAT WORKS HERE vs WHAT DOESN'T
| Capability | Status |
|---|---|
| FFmpeg cut/merge/transcode/mix/batch | ✅ full |
| ffprobe duration/dimensions/streams | ✅ full |
| Silence detect → auto jump-cut | ✅ **working, script above** |
| Scene-change detection | ✅ `select='gt(scene,0.25)'` |
| Styled captions | ✅ Playwright → transparent PNG → overlay |
| Spectrogram / LUFS / librosa | ✅ see `audio-analysis` skill |
| **ASR / auto-subtitles** | ⚠️ `faster-whisper` **installs but model download is BLOCKED** — huggingface.co not in egress allowlist. **User can fix by adding `huggingface.co` to network settings.** Until then: no auto-transcription |
| Remotion (React motion graphics) | ⚠️ npm reachable, but heavy install + needs a render pipeline. Playwright covers 80% at 1% of the cost |
| YouTube / Bilibili download | ❌ domains blocked. User downloads and uploads |
| videodb / cloud video AI | ❌ external API, not in allowlist |

## 5. THE RULE
Do the boring 80% here (cut, tighten, grade, caption, mix). Leave taste — the one drop-out
before the twist, the perfect caption timing — to the human. Automating taste produces generic.

---

## 6. OCR — reading text off frames without seeing them
`tesseract` + `chi_sim` + `eng` are installed (chi_sim via `apt-get install -y tesseract-ocr-chi-sim`).
**This is how to read burned-in captions, UI, documents, and on-screen text when images won't render.**

```python
from PIL import Image; import pytesseract, numpy as np
a = np.array(crop.convert('L')).astype(float)
mask = (a > 195).astype(np.uint8)*255          # isolate white text
img  = Image.fromarray(255-mask).resize((w*3,h*3), Image.LANCZOS)   # invert + upscale
txt  = pytesseract.image_to_string(img, lang='chi_sim', config='--psm 7')
```
**Band-scan first** — split the frame into 10 horizontal strips and OCR each to FIND the text
region before trying to read it. Don't guess the crop.

**Verified reliability:**
| Target | Works? |
|---|---|
| Text on a solid/flat band (disclaimers, title cards, UI) | ✅ reliable |
| Dark text on light background (documents, screenshots) | ✅ reliable |
| White outlined captions over moving video | ❌ **usually garbage** — too low contrast, motion blur |

**When OCR fails on captions, the fallback ladder is:**
1. `Higgsfield:video_analysis_create` — scene-by-scene + spoken content (costs credits, works)
2. ASR — blocked until `huggingface.co` is added to the network allowlist
3. Ask the user
