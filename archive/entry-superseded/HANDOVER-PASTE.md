# TALYX HANDOVER — PASTE THIS WHOLE FILE INTO THE NEW CHAT (2026-08-12, session 9 → 10)

**READ THIS FIRST, NEW SESSION.** This document is SELF-CONTAINED on purpose:
GitHub is 6 days STALE (still at commit `e2b4485`, Aug 6) because the push has
not completed yet. Do NOT trust a fresh clone. The truth lives in TWO places:
this document, and the files already updated in `Desktop\AI` (bridge-mounted).
When the push lands, repo == this document.

## WHAT THIS PROJECT IS (one paragraph)

Talyx = fully-AI short-form video for a Malaysian recond-car audience, fronted
by AI persona **Nev**. Pipeline: plans as data (`plans/*.py`) → planqc (39
checks) → judge panels → ONE approval gate with full storyboard + exact cost →
generate on Higgsfield → QC → build → verify → mastermind QC → deliver WITH
measurements. Gavril is the operator: identity and "is it good" are HIS call.
Chat is disposable; the repo is the memory. Claude PULLS, Gavril PUSHES.

## HARD RULES (unchanged, the digest)

1 Evidence before claims — every audio/pacing claim cites a measurement.
2 MEASURE the credit balance, never estimate. 3 Mechanical beats judgement.
4 After any fix, re-run the check. 5 Five failures on one problem → stop, ask.
6 Rank options, name the pick. 7 No push credentials — he pushes.
8 Frames and spectrograms ARE the work — look at them, always.

## GAVRIL'S BINDING EDIT RULES (both from tonight — these override defaults)

- **L120 (superseded by L125 but still true in spirit):** never split one
  generated clip into two windows placed at different points — reads as a
  duplicate.
- **L125 THE RULE THAT GOVERNS ALL FUTURE CUTS: "Let the whole clip play.
  Do not cut and paste. No cutting. Just move the scene, the order of the
  scene, unless if needed. Analyze carefully before doing cutting work."**
  Whole clips, reorder only. The one sanctioned cut: tiny tail trims so cut
  points land on the music beat.
- Any cut that reaches his eye is a DELIVERY — run every gate first (L119:
  "preview-grade" was a gate bypass and he caught it).

## WHERE WE ARE (the one-line answer he expects)

panborneo (Nev drives a Land Rover Defender 110 SE, KK→Kuching) is GENERATED
(13/13 clips, 308.5cr exact to the gate) and CUT: **PAN BORNEO v4, 64.0s,
whole-clip build, delivered to him** — balance **3,977.57cr measured**, 26
commits waiting on FINISH.bat, next input is HIS VERDICT on v4.

## THE FILM AS DELIVERED (v4 spec — everything needed to rebuild)

- 13 whole clips, order `G B C A D F E I H J K L M`, native **24fps** (source
  fps — a 30fps conform duplicated every 5th frame = judder; L124 check now).
- Each clip 8 beats @ 97.5 BPM (0.14s tail trim only), 104 beats = 64.0s,
  frame boundaries `round(i*118.154)`, total 1536 frames.
- Whip: xfade slideleft 6f at A→D (19.708s), A's 2 spare frames + 4
  clone-padded feed the overlap so the timeline never shortens.
- Audio: per-shot leveling to −18 dB RMS (keeps half the plan's FOLEY deltas),
  **80ms acrossfade at every boundary** (max seam jump measured 3.8dB),
  alimiter 0.891.
- Bed: **To The Moon (LiQWYD), 97.5 native, zero stretch**, window starts
  **9.57s** (measured scan: opens −15.7dB, +6.4dB lift landing on the whip),
  gain derived to sit 3dB under foley, sidechain duck 4:1 50/250ms.
- Whoosh: `assets/bank/sfx/whoosh_whip.wav` at 19.37s, **+4dB** (−6dB measured
  NO crest lift; +4 gives +3.7dB at the cut).
- Master: 2-pass loudnorm **I=−8, TP=−1**, linear; mux `-c:v copy`.
- Cards, Montserrat-ExtraBold **44px** (one size), y=908, white, border 3
  black@0.6: SABAH ENDS HERE 0.15–3.0 · REWIND TO DAWN 4.92–8.5 · KLIAS:
  PROBOSCIS COUNTRY 20.0–23.6 · SARAWAK. STILL TOLL-FREE. 34.6–38.2 ·
  KUCHING BY DUSK? 54.3–57.9.
- Length is OUTSIDE the 16–29s pillar band — his whole-clip rule overrides;
  deviation is declared, and the 64s becomes the retention experiment.

Rebuild on any machine with the clips + repo:
```
python tools/build_panborneo_v4.py          # → panborneo_V4.mp4 (crf16 master)
python tools/finalmix.py --video panborneo_V4.mp4 ^
  --bed assets/bank/bgm/travel_vlog/liqwyd-to-the-moon.mp3 --bed-ss 9.57 ^
  --whoosh assets/bank/sfx/whoosh_whip.wav --whoosh-at 19.37 --whoosh-gain 4
```
Clips: his `Downloads\hf_20260812_*.mp4` (13 files) or CDN via
`tools/pull_panborneo.py`. Chat delivery cap is 30MB → he received crf22/slow
(28MB); the crf16 master is 56MB and rebuilds from the scripts.

## AT PUBLISH (J4's binding conditions — do not skip)

1. Caption must state the compression: Brunei transit (168km), 1,000+ km,
   multi-day journey compressed.
2. AI-content disclosure label (TikTok/Meta).
3. Music credit line, verbatim:
   `To The Moon by LiQWYD | https://www.chosic.com/download-audio/58943/`
   `Music promoted by https://www.chosic.com/free-music/all/` (CC BY 3.0)

## TONIGHT'S FULL STORY (compressed timeline)

1. Seedance NSFW filter recovered overnight (his 2.5-launch theory) → 13/13
   clips clean, 292.5cr, QC all-pass (720x1280, 5.062s, OCR clean, luma 104).
2. Preview v1 (20 shots, split windows, no bed) → he caught SIX defects in one
   viewing → L119–L123.
3. v2 (13 whole scenes, 28.9s) built in Higgsfield sandbox, uploaded (media
   `304862cf-8d9b-4c0a-94ab-95f1ba37f831`).
4. Discovery: his **Downloads folder is bridge-mounted** — the 13 raw clips
   were staged into the cloud container directly. THE DRAG STEP IS DEAD.
5. Final v(2-based) delivered → he spotted judder + audio pops + card
   inconsistency → measured, confirmed, L124.
6. **His whole-clip rule arrives (L125)** → v4 built and delivered as above.
7. FINISH.bat had failed FOUR TIMES silently: my bundles recorded ref `HEAD`
   not `main` (L127). Fixed: FINISH.bat v3 (clears ALL stale locks, fetches
   HEAD w/ main fallback) + bundle rebuilt as `e2b4485..main`, verified.
8. All 108 changed files written directly to `Desktop\AI` via the bridge +
   whoosh (which `.gitignore *.wav` had silently excluded — force-added).

## ALL NEW LESSONS (L119–L127 + tv L7 — the ledger has full text)

119 any cut reaching his eye runs the gates — no "preview-grade" bypass
120 one scene per source clip (no split windows)
121 mix levels are relative to the FULL stack — absent layer = re-solve, else
    "inaudible" reads as "you cut my audio" (he was right)
122 encode once: single filter_complex, crf16, crops 1.00, master with -c:v copy
123 the asset split (laptop/container/sandbox) is the automation blocker —
    the bank rides the REPO
124 two new machine checks: frame-cadence (0 dupe frames; build at SOURCE fps)
    and seam continuity (RMS jump <6dB across every cut)
125 GAVRIL'S WHOLE-CLIP RULE (above, binding)
126 chat delivery caps at 30MB — ship crf22/slow copy, say so, master rebuilds
127 bundle `base..HEAD` records ref HEAD → FINISH.bat fetched 'main' and died
    silently ×4; always bundle `base..main`. Bridge git = READ-ONLY (cannot
    delete = strands .lock files); git writes happen on Windows only.
tv7 pick the bed WINDOW by per-beat RMS scan (open / lift-at-whip / dropouts),
    never from 0:00

## ENVIRONMENT FACTS (measured, save re-discovery)

- Cloud container: GitHub OK · Higgsfield CDN 403 · upload.higgsfield.ai 403 ·
  chosic 403 · `apt-get install fonts-montserrat` works · ffmpeg/ffprobe yes.
- Higgsfield sandbox (sandbox_exec): CDN OK, S3 presigned PUT OK, GitHub raw
  OK, chosic 403 · ephemeral ~10s between calls · S3 accepts EMPTY PUT with
  200 — verify content-length, never status.
- Bridge (his box): `Desktop\AI` + `Downloads` mounted · stage INTO container
  works (clips came this way) · commit-to-disk ≤20MB/file · CANNOT DELETE
  (parked junk goes to `_to_delete\`) · git write-ops FORBIDDEN (locks).
- Higgsfield: seedance_2_0 720p/5s std = 22.5cr · balance MEASURED 3,977.57 ·
  key media: v2 `304862cf…`, v1 `85c0bbc2…` · 13 clip job IDs in
  `projects/panborneo/JOBS.json`.

## OPEN ITEMS, IN ORDER

1. **FINISH.bat** (v3, on his desktop) — apply 26 commits + push. Until then
   GitHub is stale; his working files are already current.
2. His verdict on v4 → fix list or publish path (see AT PUBLISH above).
3. Copy the other 18 BGM tracks `Desktop\AI\BGM` → `assets\bank\bgm\
   travel_vlog\` and push → full zero-touch automation (edit+mix in cloud).
4. planqc re-run (acks moved to craft 127 / tv 7).
5. STANDING GAP: zero posts ever. One real 24h retention curve beats all.

## HOW TO START

Say where we are in ONE line (use the answer above), then WAIT for his
instruction. Do not re-derive the architecture; do not spend credits;
measure the balance before any spend.
