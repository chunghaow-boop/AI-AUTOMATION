# DOC AUDIT — measured 2026-08-07

### His observation: *"there is alot of duplicated lessons, skills, knowledge, etc all in different different files but they share the same purpose, so maybe we can organize it?"*
### He is right. Here is the measurement, and a proposal. **NOTHING HAS BEEN DELETED — every option below is his call.**

---

## WHAT IS ACTUALLY THERE

**71 markdown files** across root, `docs/` and `skills/`. **46 at the root alone,
595 KB.** Overlap measured as the share of the smaller file's distinctive vocabulary
that also appears in the larger one.

### PROBLEM 1 — NINE FILES ALL TRY TO BE THE ENTRY POINT (58 KB)

| file | size | what it claims to be |
|---|---|---|
| `START-NEW-CHAT.txt` | 4K | **the actual entry point.** Paste-into-new-chat |
| `CLAUDE.md` | 14K | the rules and the contract |
| `00-START-HERE.md` | 4K | entry orientation |
| `22-HANDOVER.md` | 12K | session state — **superseded by RESUME-\*** |
| `README.md` | 8K | repo readme |
| `RUNNER.md` | 13K | how to run it |
| `SYNC.md` | 2K | push/pull |
| `RECONCILE.md` | 4K | the desktop/repo merge, 2026-08-03 |
| `FOLDER-MAP.md` | 1K | where things live |

Measured overlaps among these and their descendants:

```
0.64  README.md            <-> docs/HANDOVER-2026-07-31.md
0.62  CLAUDE.md            <-> docs/README-RESTORE.md
0.61  docs/RUNNER.md       <-> docs/README-RESTORE.md
0.59  README.md            <-> docs/START-HERE-2026-07-31.md
0.58  CLAUDE.md            <-> docs/RUN.md
0.57  RUNNER.md            <-> 16-master-skeleton.md
0.72  docs/START-HERE-2026-07-31.md <-> docs/HANDOVER-2026-07-31.md
0.55  docs/START-HERE-RESTORE.md    <-> docs/HANDOVER-RESTORE-superseded.md
```

**A new session reads whichever one it happens to open.** That is the same failure mode
as the dead `GATE.md` pointer that made every session start cold — corrected in
CLAUDE.md on 2026-08-06.

### PROBLEM 2 — NINE RESUME FILES, 106 KB, AND ONLY THE NEWEST IS EVER READ

`RESUME-2026-08-04` → `-05` → `-05b` → `-05c` → `-05d` → `-06` → `-06b` → `-06c` →
`-07`. The 08-07 file alone is 18K. `0.56` overlap between 08-04 and 08-05;
`0.55` between 08-06c and `SYSTEM-MAP.md` — **state has been leaking into the
architecture doc**, which SYSTEM-MAP's own header forbids.

### PROBLEM 3 — THE SKILLS PREDATE THE GATES (known since 2026-08-06, still open)

`skills/talyx-shotlist/SKILL.md` overlaps `docs/RUNNER.md` at **0.68** and `CLAUDE.md`
at **0.57** — three files describing the same Phase 1. And that skill mentions
`planqc` **0 times**, `clipqc` 0, `judge` 0, `lessonize` 0, while CLAUDE.md still says
*"Use the `/talyx-shotlist` skill for Phase 1"*. **Obeying CLAUDE.md gets you guidance
written before the 68-check architecture existed.**

### PROBLEM 4 — DOCTRINE OVERLAP

```
0.65  17-car-cinematic-master-prompt.md <-> 05-cinematic-ai-video-spec.md  (42K)
0.64  25-qc-debate-protocol.md          <-> 09-learning-log.md
0.63  00-START-HERE.md                  <-> 02-ai-video-crew-roles.md
```

`09-learning-log.md` is **4 lines** and predates `ledgers/knowledge.json`, which now
holds **148 lessons**. It is a pointer to a system that replaced it.

---

## WHAT IS ALREADY FIXED

**`LESSONS.md` — 148 lessons, one file, GENERATED.** `tools/lessons_book.py` compiles
`ledgers/knowledge.json` into a single readable book: the ten that cost us most at the
top, then every lesson grouped by theme within its topic. It carries the ledger's own
counts and a `--check` mode that fails if it is stale.

**The ledger stays the source of truth.** `planqc` 23 blocks on its counts and
`lessonize.py` is the only writer. `LESSONS.md` is a READ surface — a hand-maintained
copy of a ledger goes stale, and a stale ledger is the most expensive bug class in
SYSTEM-MAP section 6.

---

## THE PROPOSAL — RANKED, HIS CALL, NOTHING DONE YET

### OPTION 1 — FOUR FILES OWN THE ENTRY. EVERYTHING ELSE IS ARCHIVED. *(my pick)*

```
START-NEW-CHAT.txt   the paste. Points at exactly three files and says nothing else.
CLAUDE.md            the rules and the contract. Nothing about state, nothing about how-to-run.
SYSTEM-MAP.md        the architecture. Changes only when the architecture changes.
RESUME-<newest>.md   where we are. One file. The previous eight move to archive/resumes/.
LESSONS.md           generated, read-only, the whole memory.
```

Everything else moves to `archive/` **unchanged** — `22-HANDOVER`, `README`, `RUNNER`,
`SYNC`, `RECONCILE`, `FOLDER-MAP`, `00-START-HERE`, `09-learning-log`, the eight old
RESUMEs, and the superseded `docs/*RESTORE*` and `docs/*2026-07-31*` files.
**Nothing is deleted. `git mv` keeps every line recoverable.**

Cost: one commit. Risk: a path in a script points at a moved file → grep first.

### OPTION 2 — LEAVE THE FILES, ADD ONE INDEX

A generated `INDEX.md` marks each file **CURRENT / SUPERSEDED-BY-X / ARCHIVE**, and
every superseded file gets a one-line banner at the top pointing at its replacement.
Zero moves, zero risk, and the sprawl stays — but a new session can no longer read the
wrong file by accident.

### OPTION 3 — REWRITE THE TWO SKILLS AGAINST THE CURRENT GATES

Independent of 1 and 2, and it is the oldest open item here. Either rewrite
`talyx-shotlist` and `talyx-cinematic` so Phase 1 names `planqc`, `clipqc`, `judge`,
`lessonize` and `contact` — or **delete the pointer from CLAUDE.md.** *Do not leave
both*, which is what the 2026-08-06 audit already said.

---

## THE ONE RULE THIS AUDIT MUST NOT BREAK

> *"we must respect each other work, those stuff are my days and night effort
> adjustments"*

Every option above is **additive or a move**. No file is rewritten, no content is
deleted, and the `git` history holds all of it. **His call, all three.**
