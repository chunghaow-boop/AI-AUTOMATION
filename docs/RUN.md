# RUN — the commands, in order

## ONE-TIME
```bash
bash setup-local.sh                  # ffmpeg, whisper, deps
claude                               # start local agent in this folder
```

## MAKE A VIDEO
```bash
# 1 · Phase 1 (free) — inside claude:
/talyx-shotlist "RM50k gets you THIS"
#    → target, beats, shot list, cost preflight → ⏸ approve

# 2 · probe the hook before the real spend (~52cr)
#    3 hooks × 5s × 720p fast → pick blind in qc-console.html

# 3 · generate the winner (Higgsfield MCP, inside claude)

# 4 · edit
python3 tools/transcribe.py raw.mp4 -o t.json
python3 tools/autocut.py  raw.mp4 t.json --captions -o cut.mp4
#    or fully automatic:
python3 tools/edl.py auto raw.mp4 --format review --bed bed.wav -o final.mp4

# 4b · designed cards (Playwright — local only, replaces ffmpeg drawtext)
python3 tools/cards.py punch     --text "you don't" --highlight "don't" -o cards/punch.png
python3 tools/cards.py checklist --title "Before you pay deposit" --items items.txt -o cards/check.png
python3 tools/cards.py ladder    --title "RM50k gets you THIS" --rows "RM30k|Myvi 2019|~85k km" "RM50k|Vios 2020|~60k km" -o cards/ladder.png
python3 tools/cards.py title     --pillar "Recond Truth" --ep 12 -o cards/title.png

# 5 · gate — nothing ships until these pass
python3 tools/mastermind.py final.mp4 --cards cards.json --bed bed.wav --out qc
python3 tools/pacing.py     final.mp4 --format review
python3 tools/facecheck.py  final.mp4 --seam 15.0
python3 tools/rhythm.py     final.mp4 --bed bed.wav --cuts

# 6 · post, then at +24h log predicted vs actual
```

## LEARN FROM REFERENCES
```bash
python3 tools/reverse.py refs/ --format review --mine final.mp4    # their editing DNA vs yours
python3 tools/intel.py add "<url>" --note "why it stopped me"
python3 tools/intel.py brief
```

## CALIBRATE THE GATES (free, uses already-spent credits)
```bash
open qc-console.html                 # rate 30 clips + blind A/B
python3 tools/calibrate.py reference/generation_history.json ratings.csv
```
