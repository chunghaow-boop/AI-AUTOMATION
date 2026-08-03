# QUICK REFERENCE — the commands that do the work
Run `bash tools/setup.sh` first, every session.

## SEE SOUND (Claude cannot hear — this is the workaround)
```bash
ffmpeg -v error -y -i in.mp4 -lavfi "showspectrumpic=s=1000x420:mode=separate:legend=1:scale=log" spec.png
ffmpeg -hide_banner -nostats -i in.mp4 -af ebur128=framelog=quiet -f null - 2>&1 | grep -A4 Integrated
```
**Targets (measured from a real viral reel, not theory):**
`-7 to -9 LUFS · body 150-1500Hz ~45% · sub+low <150Hz ~8% · air >10k ~4% · centroid ~2400Hz · STEREO`

## READ TEXT OFF FRAMES (when images render blank)
```bash
# band-scan 10 horizontal strips to LOCATE the text, then threshold+invert+3x upscale
# langs available: eng chi_sim chi_tra msa
```
Reliable on solid-band text. Fails on white outlined captions over moving video.

## AUTO JUMP-CUT (the Recipe 7 primitive — removes every pause)
```bash
python3 tools/autojumpcut.py raw.mp4 tight.mp4 --db -35 --min 0.25 --pad 0.05
```

## STYLED CAPTIONS (Playwright -> transparent PNG -> overlay)
Beats FFmpeg drawtext by a mile. See tools/playwright-SKILL.md.

## CHECK BEFORE CLAIMING
```bash
# cuts
ffmpeg -hide_banner -i in.mp4 -vf "select='gt(scene,0.25)',metadata=print" -an -f null - 2>&1 | grep -oE "pts_time:[0-9.]+"
# brightness/colour per frame — diagnoses grade breaks and bad seams
```
**Never claim a mix "sounds good" or a balance figure without measuring it. Run Higgsfield:balance.**

## KNOWN BLOCKED
`huggingface.co` (Whisper) · `cloudfront.net` (Higgsfield outputs — user must download/upload) ·
`youtube/tiktok/facebook` · `api.github.com`. **Reachable:** github.com, raw.githubusercontent, pypi, npm.
