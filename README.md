# TALYX — AI VIDEO AUTOMATION

Fully-AI short-form video for a Malaysian recond-car audience, fronted by a consistent
AI KOL persona (Nev). Facebook · TikTok · Instagram.

## READ THESE FOUR, IN THIS ORDER. NOTHING ELSE.

| | file | what it is |
|---|---|---|
| 1 | **`CLAUDE.md`** | the rules and the contract |
| 2 | **`SYSTEM-MAP.md`** | the whole pipeline: every file, every gate, every threshold, the plan→engine contract, the bug classes that have cost money, the seats, the cost model |
| 3 | **the newest `RESUME-*.md`** | where we actually are right now |
| 4 | **`LESSONS.md`** | every lesson this system has learned, in one generated file. Start with THE TEN THAT COST US MOST |

`START-NEW-CHAT.txt` is the paste-into-a-new-chat version of the above.

**Do not re-derive the architecture by reading `planqc.py` / `engine.py` / `verify.py`.**
It is already written down. If the map disagrees with the code, the CODE is right — fix
the map and say so in the RESUME.

## THE SHAPE OF IT

```
plans/<name>.py     THE PLAN, as DATA. One file per video.
talyx.py            the front door:  plan · board · cost · ingest · build · verify · ls
planqc.py           the plan gate. 39 checks. Free, and it BLOCKS.
clipqc.py           the paid-artefact gate. 13 checks per generated clip.
engine.py           the builder. Plan + clips -> one encode.
verify.py           the cut gate. 15 checks, freshness FIRST.
tools/              ~55 measurers. contact.py · lessonize.py · judge.py · bugsense.py …
ledgers/            the memory. knowledge.json is the source of truth for lessons.
00-28-*.md          the DOCTRINE — the seats the gates exist to enforce.
archive/            superseded entry files and old RESUMEs. Nothing deleted, ever.
```

## THE ONE ARCHITECTURAL RULE

**The plan is DATA, the pipeline is CODE, and they never multiply.** A new video is one
new file in `plans/`.

## THE STANDING GAP

**Zero posts, ever.** One posted video with a real 24-hour retention curve outranks
everything in this repository.
