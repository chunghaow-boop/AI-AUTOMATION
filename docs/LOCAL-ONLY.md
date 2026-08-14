# LOCAL-ONLY — what needs your machine, and why
### This folder is the home for everything the Cowork sandbox cannot run.
### All three blocks below are the SAME cause: the sandbox egress proxy blocks model/binary CDNs.

## THE THREE BLOCKED CAPABILITIES (all verified by test, not assumed)

| Capability | Blocked because | Unlocks |
|---|---|---|
| **Whisper / ASR** | `openaipublic` 403 · `huggingface` 403 · `alphacephei` 403 | word-level transcript → filler cuts, retake detection, sentence jump-cuts, hook selection from text, word-exact captions |
| **Playwright + Chromium** | `cdn.playwright.dev` 403 · `playwright.azureedge.net` 403 | designed HTML/CSS cards instead of ffmpeg drawtext → the Artefact Drop |
| **Higgsfield CDN media** | `d8j0ntlcm91z4.cloudfront.net` 403 | pulling your own renders directly instead of manual download+upload |

> ⚠️ `system/tools-legacy/playwright-SKILL.md` says Playwright is "PRE-INSTALLED" — that was
> true in an earlier sandbox. **Re-verified 2026-07-27: it is not.** Corrected in that file.

## SETUP
```bash
bash setup-local.sh          # ffmpeg · whisper · playwright+chromium · deps · verification
claude                       # CLAUDE.md auto-loads; /talyx-shotlist becomes available
```

## WHICH TOOLS NEED LOCAL
```
LOCAL ONLY   transcribe.py   (Whisper weights)
             autocut.py      (consumes the transcript)
             cards.py        (full quality; falls back to ffmpeg anywhere)
WORKS ANYWHERE  mastermind · pacing · rhythm · facecheck · reverse · calibrate · intel · edl
```

## FOLDER MAP
```
RUNNER.md · SOURCE-ROUTING.md · GATE.md · PROMPTS.md   the system
CLAUDE.md · RUN.md · HANDOVER.md · README.md           operating docs
skills/talyx-shotlist/                                 Phase 1 as one command
tools/                                                 11 tools
system/                                                your original 27-file repo (reference)
system/tools-legacy/                                   autojumpcut, QUICKREF, old skills
reference/                                             session analysis + generation history
work/                                                  scratch space for builds
```

## CORRECTIONS MADE 2026-07-27 (my defaults were wrong; your measurements won)
1. **Audio target** — `mastermind.py` used −9..−14 LUFS (generic platform guidance).
   Your `system/19-sound-engineer.md` has **−7 to −9 LUFS MEASURED from a real viral reel**.
   Tool corrected to your number. *(This means `INFLUENCER_v1.mp4` at −12.3 is ~4dB too quiet.)*
2. **Spectral targets** — aligned to your measured profile: body 150–1500Hz ≈45% (was ">30%"),
   air >10kHz ≈4% (was "2–25%").
3. **Playwright status** — corrected from "pre-installed" to local-only, with evidence.
4. **`cards.py`** gained `composite()` — the transparent-PNG-overlay-with-fade pattern taken
   from your own `playwright-SKILL.md`, so cards land on video the way that skill specified.
