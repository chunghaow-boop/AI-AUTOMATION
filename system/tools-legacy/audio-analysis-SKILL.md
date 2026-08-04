---
name: audio-analysis
description: How to evaluate audio and mixes without hearing them — spectrograms rendered as viewable images, EBU R128 loudness metering, librosa beat/onset/spectral analysis. Use whenever judging, fixing, or comparing the audio of any video. Claude cannot perceive sound, so every audio claim must come from these measurements, never from assertion.
---

# Analysing audio without hearing it

## THE CORE RULE
**Claude cannot hear.** No MCP or plugin changes this — audio bytes are not a perceivable input. Any statement like "this sounds good/punchy/thin" that is NOT backed by a measurement below is a fabrication. Measure, then claim.

## 1. SEE THE SOUND — spectrogram as an image (highest value)
Claude *can* see images. Convert audio to a picture and view it.
```bash
ffmpeg -v error -y -i in.mp4 -lavfi \
  "showspectrumpic=s=1000x420:mode=separate:legend=1:scale=log" spec.png
```
Then `view spec.png`. What to read:
| Look for | Means |
|---|---|
| Two panels near-identical | stereo is NARROW — width failed |
| Bright constant band at bottom | too much sub/DC — boomy bed |
| Flat uniform wash across mids | broadband noise masking the mix — hissy |
| Vertical bright lines | transients/kicks punching through — good |
| Dark column | a duck or silence — verify it's where intended |
| Black above ~18kHz | normal for AAC, not a fault |

## 2. REAL LOUDNESS (not RMS guessing)
```bash
ffmpeg -hide_banner -nostats -i in.mp4 -af ebur128=framelog=quiet -f null - 2>&1 | grep -A6 "Integrated"
```
Targets: **-14 LUFS integrated**, true peak -1dB, LRA 4-8 LU for short-form.

## 3. LIBROSA — beat, onset, spectral truth
```bash
pip install --break-system-packages librosa soundfile pyloudnorm   # pypi is allowlisted
ffmpeg -v error -y -i in.mp4 -ac 1 -ar 48000 tmp.wav               # librosa needs wav
```
```python
import librosa, numpy as np
y,sr=librosa.load('tmp.wav',sr=48000,mono=True)
tempo,beats=librosa.beat.beat_track(y=y,sr=sr); tempo=float(np.atleast_1d(tempo)[0])
bt=librosa.frames_to_time(beats,sr=sr)
err=[min(abs(bt-c)) for c in MY_CUT_TIMES]          # verify cut-to-beat objectively
sc=librosa.feature.spectral_centroid(y=y,sr=sr)[0]  # brightness
S=np.abs(librosa.stft(y)); f=librosa.fft_frequencies(sr=sr)
band=lambda lo,hi: 100*S[(f>=lo)&(f<hi)].sum()/S.sum()
```
| Metric | Healthy target |
|---|---|
| spectral centroid | **1500–2500 Hz**. >3000 = too bright/hissy |
| body 150–1500Hz | **35–45%**. <20% = hollow, the classic amateur hole |
| sub+low 20–150Hz | ~20–25%. >30% = boomy |
| cut-to-beat error | **<30ms**. >100ms reads as sloppy |
| spectral flatness | <0.1 tonal · >0.4 noisy |

## 4. WHAT MEASUREMENT STILL CANNOT TELL YOU
Whether it sounds *emotionally right* — exciting, tense, premium. That needs a human ear.
**Best proxy: reference-matching.** Measure a professional track in the target genre, then match your numbers to it. "Correct vs a reference" beats "correct vs my opinion."

## 5. OPTIONAL, NOT YET INSTALLED
- `openai-whisper` / `faster-whisper` — speech-to-text, for checking VO and dialogue legibility
- Reference tracks — keep 2–3 pro tracks on disk to measure against

## NOTE: the sandbox resets
librosa/soundfile/pyloudnorm must be reinstalled each session (one pip line, ~30s). ffmpeg spectrogram + ebur128 are always available.

---

## 6. SPEECH → TEXT (the closest thing to "hearing")

**The honest ladder, tested in this sandbox:**

| Option | Status | Quality |
|---|---|---|
| **faster-whisper / openai-whisper** | ⚠️ pip installs, **model download BLOCKED** — huggingface.co 403, openaipublic.azureedge.net 403 | would be excellent |
| **pocketsphinx** | ✅ **WORKS OFFLINE — model bundled in the pypi wheel, no download** | ⚠️ **poor** |
| vosk | pip installs; models on alphacephei.com — untested, likely blocked | good if reachable |

**pocketsphinx — verified working, and verified weak:**
```bash
pip install --break-system-packages pocketsphinx
apt-get install -y -qq espeak-ng     # optional, for generating test speech
ffmpeg -i in.mp4 -ar 16000 -ac 1 out.wav      # MUST be 16kHz mono
```
```python
from pocketsphinx import AudioFile; import os, pocketsphinx
m = os.path.join(os.path.dirname(pocketsphinx.__file__),'model','en-us')
for seg in AudioFile(audio_file='out.wav', hmm=os.path.join(m,'en-us'),
                     lm=os.path.join(m,'en-us.lm.bin'),
                     dict=os.path.join(m,'cmudict-en-us.dict')):
    print(seg)
```
**Measured accuracy test** — input *"the fastest car in the world is not the one you think it is"*
→ output *"sorry but what old is all the while you think the"*. **~30% word accuracy.**

**Use pocketsphinx ONLY for:** does speech exist · roughly where · rough topic gist.
**NEVER use it for:** subtitles, quotes, transcripts, or any claim about what was said.
**English only** — the bundled model has no Chinese/Malay.

## ⚡ THE ONE SETTING THAT FIXES THIS
Add **`huggingface.co`** to the network egress allowlist → faster-whisper downloads its model →
proper multilingual transcription (English, Chinese, Malay), accurate enough for subtitles.
**One setting change, and speech-to-text goes from 30% to production quality.**
