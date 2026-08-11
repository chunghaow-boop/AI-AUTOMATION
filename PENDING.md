# PENDING — updated 2026-08-11

What changed this session is at the bottom. This is what is still open.

---

## 1 · ONE ACTION FROM YOU

| # | task |
|---|---|
| 1.1 | **Double-click `FINISH.bat`** in `C:\Users\User\Desktop\AI`. It clears the stale `.git\index.lock`, backs up your loose files into a stash, applies ALL the session commits in `talyx-FINISH.bundle` (08-07 + 08-08 + the 08-11 fixes), and pushes to GitHub. It is the only step I cannot do — the push needs your credentials and the lock cannot be removed through the file bridge. |
| 1.2 | Download the bank: `talyx-bank-v3.zip` → unzip into `assets\bank\`. **Do not let it overwrite `assets\bank\bank.py`** — the copy inside the zip is the broken one. |

---

## 2 · STILL OPEN — REAL WORK

| # | task | note |
|---|---|---|
| 2.1 | **Reference-video bank** | You hand me winning video files. I measure cut times, shot lengths, motion curve, luma arc, hook timing, caption timing. This is the only path left to §4 — and the only one that survives without API keys. **This is now the biggest single item.** |
| 2.4 | Two stale skills | rewrite or delete |

**CLOSED 2026-08-11** (was 2.2 / 2.3): `desafarm` AND `mahua` now pass planqc **38/38** — cards de-collided, acks re-read against craft 115 / travel vlog 6 + the three neighbouring pillars, `RELATIONSHIPS` blocks written for both, thresholds derived. And `BLEND_RESERVES_OVERLAP` is ONE mechanism: `engine.py` exports the contract constant, planqc 34 reads it from the engine — a plan flag is now only an explicit opt-out. Also closed: `SHOT_WINDOW` per-shot pins (mahua's arc-order risk, both plans pinned) and verify check 5 is REPORT-ONLY for travel_vlog (`style.exposure_gate`), still blocking for car_cinematic. |

---

## 3 · NUMBERS NOBODY CAN SOURCE

Seven guesses now declare themselves in `ledgers/thresholds.json`. They still run as if they were facts.

| number | value | status |
|---|---|---|
| `travel_vlog.median_shot` | 1.13 s | guess — published guidance says 1.5–2.0 s |
| `travel_vlog.target_length` | 28.31 s | guess — 20–25 s cited as the sweet spot |
| `mix.foley_trim_clamp` | 8.0 dB | guess — 0 samples |
| `verify5.exposure_max_swing` | 18.0 | guess — and since 08-11 travel_vlog is REPORT-ONLY on it (`style.exposure_gate`), so the guess can no longer block a legitimate multi-light-state arc. car_cinematic still blocks on it. |
| `bank.target_lufs_sfx` | −16 LUFS | **guess — new** |
| `bank.target_lufs_ambience` | −20 LUFS | **guess — new** |
| `bank.cut_safe_attack_ms` | 25 ms | **guess — new** |

Plus four provisional thresholds fitted on 1–6 samples.

**Every one of these is replaced by §2.1.** That is why §2.1 is the biggest item.

---

## 4 · BANK REMAINDERS

- 59 files still short of loudness target after limiting — each carries its shortfall in `gain_limited_db`
- Ambience capped at 10 s, head and tail not loop-matched
- 11 transition files still have attack >150 ms — correctly marked `gesture`, worth an ear
- Mixkit only. Freesound needs per-file licence checks; Pixabay blocked the host.

---

## 5 · CLOSED BY YOUR DECISION

- **Meta Graph token — declined.** No retention data from Urban Auto Hub. This was the only legitimate retention source in the system.
- **YouTube Data API key — declined.** The scanning agent as originally described is not buildable. Replaced by §2.1.

---

## DONE THIS SESSION

| what | evidence |
|---|---|
| Asset bank v1 → v3 | 445 measured files. Ambience usable without the clamp: **68 → 129**. Loudness spread **−70…−1 → −26…−16**. |
| Bank defects found by measuring my own output | 7 of them, including v2 storing ebur128's **−70 floor as if it were a measurement** — the same shape as the ±8 dB clamp printing its clamped value as success |
| **Transition bank** | `assets/transitions/TRANSITIONS.json`, 5 kinds, definitions not clips. planqc **34** blocks desafarm. |
| `verify.py` pillar bug | `PILLAR = "car_cinematic"` hard-coded — **every travel vlog was verified against the car profile.** Now read from the plan; new check **5b** blocks when absent. |
| `verify.py` check 5 | `if d > 18` moved into each pillar's style block, unchanged, now traceable |
| `board.py` | crashed with IndexError on the 10th source. desafarm has 14 — **the contact sheet could never draw it.** Fixed. |
| `.gitignore` | did not cover `.flac`; the bank would have committed 353 MB to a repo that caps at 100 MB/file |

---

## THE RULE THIS LIST KEEPS PROVING

Four times now, the same shape: **a tool returned a sentinel and the pipeline stored it
as data.** The whip that reported 240 ms and delivered −197. The clamp that reported
+8 dB and needed +16.3. The meter that returned −70 and meant *ask me later*. And a
gate that reported "car_cinematic" because nobody ever asked the plan.

> If a measurement has a floor, a ceiling, a clamp, or a default,
> the code must know that limit and refuse to record it as a value.

Section 3 exists because the same thing happens with numbers nobody fitted.
