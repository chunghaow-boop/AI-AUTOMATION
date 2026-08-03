# SAFETY — your original footage is never touched
### You asked whether downloads or transitions could overwrite your source. Answer: no.
### But there WAS a real risk path, and it's now closed with hard guards. Both are tested.

## 1 · DOWNLOADS CANNOT COLLIDE WITH YOUR FOOTAGE
Everything I fetched is written with a forced prefix:
```
SFX_<category>_<id>.mp3     BGM_<genre>_<id>.mp3     BROLL_<category>_<id>.mp4
```
`import_assets.py` only ever touches files matching **those exact patterns** (regex-matched).
Your own footage sitting in Downloads is *invisible* to the script — it will not be seen,
moved, renamed or read, unless you happened to name it `SFX_...` yourself.

## 2 · NOTHING IS EVER OVERWRITTEN ON IMPORT
`safe_move()` replaced `shutil.move()`. If a destination filename already exists it writes
`name_1.ext`, `name_2.ext`, and so on. The zip extractor does the same, per file.
**There is no code path in the importer that can clobber an existing file.**

## 3 · SOURCE FILES ARE PROTECTED AT THE TOOL LEVEL  ⚠️ this was the real risk
Every video tool runs `ffmpeg -y` (auto-overwrite). If you'd ever typed an output path equal
to an input path, ffmpeg would have silently destroyed the source. That was a genuine hazard.

`_guard_output()` now sits in `transitions.py`, `grade.py`, `autocut.py` and `edl.py`.
It compares absolute paths and **exits before ffmpeg runs**.

**Tested, both directions:**
```
$ grade.py match part1.mp4 --ref part2.mp4 -o part1.mp4
REFUSED: output 'part1.mp4' is the same file as an input.
         Source footage is never overwritten. Choose a different -o.

$ transitions.py apply part1.mp4 part2.mp4 --type whip -o part2.mp4
REFUSED: output 'part2.mp4' is the same file as an input.
```
Normal outputs still work — verified on the same clips immediately after.

## 4 · DIRECTORY CONTRACT — who writes where
| Folder | Written by | Contains |
|---|---|---|
| `assets/` | `import_assets.py`, `sfxgen.py` | library only — SFX, BGM, B-roll, Nev refs |
| `work/` | **you** | your source footage. **No tool writes here unless you name it as `-o`** |
| `output/` | you, via `-o` | finished videos |
| `tools/` `system/` `reference/` | code and docs | never media |

**Rule of thumb:** every tool writes exactly where your `-o` says and nowhere else. There are no
hidden in-place edits anywhere in the toolchain.

## 5 · RECOMMENDED HABIT
```bash
python3 tools/import_assets.py --dry-run     # prints what WOULD move, touches nothing
```
Run that first, always. And keep your master footage outside `Downloads` — not because the tools
would touch it, but because Downloads is the one folder you might clear out by hand one day.
