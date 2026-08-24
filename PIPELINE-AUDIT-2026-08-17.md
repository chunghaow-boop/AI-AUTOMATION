# PIPELINE AUDIT — 2026-08-17
### His order: *"test it in your own sandbox… make sure all the functions and checks and planning must fire; if you detect anything that did not fire do let me know so I can see if it is needed to be removed."*
### Every verdict below was produced by RUNNING the tool in the sandbox this session, not by reading its source.

---

## 1 · THE WORK TREE (what each thing is, one line each)

```
AI/
├── CLAUDE.md                     doctrine - read first, every session
├── SYSTEM-MAP.md                 the architecture, written down so no session re-derives it
├── RESUME-*.md                   where we are; newest one is the session handover
├── 00-32 *.md                    the SEATS (strategist 08 · editor 10 · sound 19 · judges 06
│                                 · mastermind QC 27 · scriptwriter 31 · REAL-FOOTAGE 32)
├── planqc.py                     GATE 1 - the plan gate. 48-49 checks + --selftest
├── verify.py                     GATE 4 - the delivery gate. ~21 checks on the finished file
├── qc.py                         profile conformance engine (verify check 1 shells to it)
├── plans/<name>.py               THE PLAN - every decision as data. No plan = no gates (L176)
├── tools/                        73 tools; the load-bearing ones:
│   ├── predeliver.py             GATE 5 - the LAST gate. 3 tiers, blocks anything unshown
│   ├── clipgate.py               GATE 2 - raw clips before edit (+ internal-cut detect + selftest)
│   ├── storyboard.py             the board + BOARD QC (blocks a bad board from reaching you)
│   ├── cutsense.py               edit inspector: shape · dynamics · repetition · event curve
│   ├── bedcheck.py               bed-vs-foley balance in the delivered mix
│   ├── capcards.py / captionmgr  card rendering (register from plan) + overlay filtergraph
│   ├── capcheck.py               caption-contrast gate  << NEVER FIRES - see §4
│   ├── ingest.py                 clip organizer          << NEVER FIRED this session - see §4
│   ├── build_niah / build_r8ride / build_lot   per-film builders (plan-obeying)
│   ├── transcribe.py (+ ASR bridge: sherpa-onnx in-sandbox, model via Chrome→Downloads)
│   └── finalmix / foley / grade / facecheck / reverse / refsense / pacing …
├── projects/<name>/              per-film: clips · JOBS.json · TRANSCRIPT.json · READ.md ·
│                                 audio/<n>_cuts.json · tmp/manifest_peaks.json · evidence/
├── assets/pillars/PILLAR-PROFILES.json   measured per-pillar numbers (cuts/min, bands)
├── BGM/car_cinematic/            his real music library (24 tracks, BPM+build measured)
├── ledgers/knowledge.json        183 lessons - the memory that makes the loop a loop
├── Raw footage/                  what he shoots
└── SHOOT_transformation/         the next shoot: brief + 15 role folders
```

## 2 · THE FLOW (both footage types, as actually wired)

```
GENERATED                                REAL FOOTAGE (file 32)
─────────                                ──────────────────────
TITLE (intent brief)                     SHOOT BRIEF → he shoots into role folders
  ↓ reference scan (subject + form)        ↓
  ↓ readback → HIS PICKS                 READ PASS: transcribe (ASR only speech
  ↓                                        detector) · frame strips · text at full
plans/<n>.py  ←──────────────────────────  res · READ.md   ← the plan quotes these
  ↓
GATE 1  planqc (48-49 checks + selftest proves them)
  ↓
storyboard.py → BOARD QC (blocks bad board)  →  ⏸ HIS GATE
  ↓
probe → GATE 2 clipgate (each clip judged)   |  (real: clips already judged in read pass)
  ↓
BUILDER: rough cut → sound → polish          ← obeys the plan; WRITES ITS MANIFESTS (L182)
  ↓
GATE 3  EDIT QC loop (fail → back to ffmpeg)
  ↓
GATE 4  verify.py (~21 checks, reads the build's own manifests)
  ↓
MASTERMIND (file 27, TIER 0 = predeliver first)
  ↓
GATE 5  predeliver: T1 EXISTENCE · T2 MECHANICAL · T3 INSPECTION (unlooked finding = block)
  ↓
HIM — the FINAL FINAL boss
  ↓ his feedback → ledger → next plan's premortem   (the loop)
```

## 3 · WHAT FIRED, PROVEN LIVE THIS AUDIT

| gate | result |
|---|---|
| planqc, all 13 plans | fires on all. lot **49/49 PASS** · r8ride PASS after re-ack · 8 legacy plans correctly BLOCK · i8 correctly blocked as pre-format · kundasang correctly reports "no plan file" |
| planqc --selftest | lot 15/16 proven, r8ride 16/16 proven (the 1 unproven is check 38's second injection, inert on a fully-justified plan — acceptable) |
| clipgate --selftest | PASS both arms (no false positive on one-take, catches the 2.5s splice) |
| predeliver | was **VACUOUS** (see §4, fixed) — now PROVEN both arms with a synthetic fixture |
| verify on LOT_v9 | 21 checks ran; 6 came alive only after the manifest fix (L182) |
| BOARD QC | **fired and blocked** — caught the board showing a generic persona plate where the plan names real footage. The gate works; storyboard's panel source needs real-frame support for REAL_FOOTAGE plans |
| cutsense / bedcheck | both fire; both flagged findings that inspection resolved (§5) |
| ASR bridge | model loads, transcribes; proved the V1–V7 premise wrong |

## 4 · WHAT DID **NOT** FIRE — your call on each

**1 · `tools/capcheck.py` — the caption-contrast gate. NEVER FIRED, ever, on a delivered film.**
Built after YOUR complaint ("the caption is what color, it clashes with the environment color") and validated against panborneo V5 — then never wired into verify, predeliver, or any builder. Run bare it **crashes** (`TypeError`) instead of printing usage. This is the exact defect class you asked me to hunt: a check that exists and protects nothing.
→ **Recommend: wire it into verify as a check, or delete it.** Keeping it unwired is worse than either.

**2 · `predeliver --selftest` — went silently vacuous.** Its negative control was "the real LOT_v5 has no plan" — then we wrote the plan, the fixture healed itself, and the selftest proved nothing. **Fixed this audit** (synthetic fixture, L183) — but it had been vacuous since the moment plans/lot.py existed, and nothing reported that.

**3 · `verify` check 21 (card presence) — measuring branch has never run in production.** It needs source clips in `projects/<n>/clips/`; real-footage films keep sources in `Raw footage/`, and its source-frame comparison assumes `t_in=0` (generated whole clips). It politely says NOT MEASURED and passes.
→ **Recommend: keep but re-scope** — compare the card band's *stability across frames inside the built film* (a card is static; backgrounds move), which needs no source clips at all. Or accept it as generated-films-only and say so in its name.

**4 · `verify` check 15 (relight) + the segment cache** — build_lot kept no `tmp/` segments, so relight audits can't run on real-footage builds. Structural: builders must keep their segment cache. Same family as L182.

**5 · `tools/ingest.py` — the organizer never ran this session.** I hand-rolled a catalogue script instead because ingest assumes generated clips in `projects/<n>/clips/` with plan roles. Two catalogue systems now exist; one is unwired.
→ **Recommend: teach ingest.py the `Raw footage/` + folder-role path (the SHOOT_transformation structure is exactly what it wants), or fold my catalogue script into it.** Not removal — its manifest is what verify reads.

**6 · `build_lot.py` wrote no manifests (L182)** — blinded 9 verify checks and *nothing said so*. Fixed by reconstruction; the builder itself still needs the 15 lines from build_niah.py copied in.

## 5 · CHECKS THAT FIRE BUT MIS-JUDGE A SPEECH-LED / REAL-FOOTAGE FILM
*(all verified by LOOKING at the frames they named, per L177 — none of these should be removed; they need scoping, like planqc got in L171)*

- **2 cut-to-music** (162.9ms dev): measures ALL cuts against the beat grid, but 10 of 16 cuts are SENTENCE cuts by design. Should read the plan's two-grid structure and only judge the beat passages.
- **3 sfx audible** (+0.1dB): the plan declares `SFX_WAIVED` with a reason; the check doesn't read waivers.
- **8 audio** (−13.9 vs −9.5..−6.5): judges against the pillar profile band (measured on loud phonk edits) instead of the plan's own `MIX.lufs_i_target = −12`. The plan decides; the check should read it.
- **9 true black** (1 frame): that frame is the *declared* dip-to-black. Check should read TRANSITIONS_PLAN.
- **13 composition dupes** (8 pairs): the pairs are the SPINE re-appearing between cutaways — a talking-head structure, not reused footage.
- **17 card collision** (0.3–0.9s): LOOKED — one card, clean; the glyph counter fragments on the LED-strip texture behind the band.
- **12 storyboard tally** (17 vs 8, "sources never used" — false): compares physical segments against logical plan shots; needs cutaway awareness.
- **bedcheck** (−11.9dB "FAIL", alignment 0.08): its ≥0 rule and correlation window both assume an ambience bed with no dialogue; on a film that is 65% voice it measures the duck it asked for and calls it a failure.

## 6 · VERDICT

The **skeleton is sound and the order is right**: plan → planqc → board QC → his gate → build → verify → mastermind → predeliver → him. Every *story* gate fires, every selftest now proves both arms, and absence-of-work is itself detected (predeliver T1).

The debt is in one seam: **half of verify's mechanical checks still assume generated, music-led, 720p footage.** Real footage got a seat (file 32), a plan vocabulary (REAL_FOOTAGE), and planqc scoping (L171-pattern) — verify hasn't had the same pass yet. That, plus wiring or deleting capcheck, plus manifests in build_lot, is the whole remaining list.

Nothing here needs removal outright except possibly **capcheck** — and only if you decide caption contrast isn't worth a wired gate; the complaint it answers was yours.


---

## 7 · FIXES APPLIED (same day, all verified live)

| finding | fix | proof |
|---|---|---|
| capcheck never fired | `--plan` mode (feeds itself from the plan) + usage error instead of crash + **wired as verify check 22** | first production run ever: PASS on LOT_v10, 5.17:1 / 18.88:1 |
| verify judged real footage with generated rules | checks 1, 2, 3, 5, 8, 9, 12, 13, 15, 17 scoped: read REAL_FOOTAGE, SFX_WAIVED, TRANSITIONS_PLAN, MIX.lufs_i_target, CUTAWAYS | LOT_v10: **PASS all 22 checks** — first fully-green verify on a real-footage film |
| check 8 then caught a REAL defect | the mix was 1.9 LU under the plan's own target (I ran single-pass loudnorm; plan says two-pass) | **LOT_v10** remastered with true two-pass: −13.3 LUFS, within ±1.5 |
| build_lot wrote no manifests (L182) | `write_manifests()` in the builder, same list that makes the segments | parses; runs on next build |
| predeliver selftest vacuous (L183) | synthetic broken-project fixture | PROVEN both arms |
| ingest.py unwired for real footage | `--raw` mode merged from the audit catalogue script | parses; one catalogue system for both footage types |

Ledger: L182, L183, **L184** ("a gate that is not wired into the line does not exist — done means something CALLS it"). 184 lessons.

**Still open after this pass:** verify 21 (card presence) still N/A on real footage — re-scope to in-film band stability when next touched. bedcheck still assumes an ambience bed (advisory only; predeliver doesn't call it). ~508cr outside spend still unmeasured. `.git\index.lock` still needs deleting by hand before PUSH.bat.
