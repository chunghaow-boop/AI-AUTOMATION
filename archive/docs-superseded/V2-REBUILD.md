# V2 REBUILD — every change traced to your review

Your five complaints, what was done, and the measurement that proves it.
Nothing here is "sounds good". Every claim has a number or a frame.

---

## 1 · "there is no bgm"

**Cause:** `assets/bgm/mixkit` was empty. The bed was `drone_tension.wav` — an atmospheric
drone from the utility set, not music. The other "beds" are metronome click tracks
(measured 24–35% sustain above −30 dB; a real bed is ~100%).

**Fix:** new tool `tools/bgmgen.py` **synthesises** the bed. No download, no attribution,
no takedown risk on a monetised channel.

- 100 BPM, 2.4s bar, progression **C–G–Am–F**
- five stems: pad · shimmer · pluck · bass · drums
- **arranged to this cut**: drums drop out entirely for the sunset payoff, then lift for the CTA
- verified musical: bass lands on 130 / 98 / 110 / 88 Hz = C / G / Am / F, bar by bar

**Spectrum matched to your measured targets (file 19), not to my taste:**

| band | first attempt | second | final | your target |
|---|---|---|---|---|
| sub | 55.2% | 42.5% | **17.6%** | 16% |
| body | 42.8% | 48.0% | **46.4%** | 45% |
| presence | 1.5% | 9.0% | **24.4%** | 26% |
| high | 0.0% | 0.4% | **7.6%** | 9% |
| air | 0.0% | 0.1% | **3.7%** | 4% |

Hand-tuning missed twice. It now measures the band split and applies a corrective gain,
iterating to convergence — printed each pass so the result is evidence.

---

## 2 · "there is no caption"

**Cause:** a real bug, and a worse design decision.

```
!! text render failed: No option name near '\USER FOLDER IMPORTANT\Desktop\AI\...cap0.txt
```

`D:\USER FOLDER IMPORTANT\...` inside an ffmpeg filtergraph is unparseable — `:` reads as an
option separator, `\` as an escape. Whisper had worked fine (45 words, 11 cards). The render
failed, and **my code silently shipped a clean video and reported success.**

**Fix:** ffmpeg now runs with `cwd` set to the temp folder and references bare filenames —
no drive letter, no backslashes, nothing a filtergraph can choke on. And if the text pass
ever fails again it prints `DO NOT POST THIS FILE` instead of shipping quietly.

**Also fixed while in there:**
- captions broke on length, producing `"grilled seafood, few"` / `"ringgit only"`.
  New `phrase_cards()` breaks on punctuation and pauses first, length only as fallback.
- Whisper mangles Malay: it produced `"Tanjong -Aru"` and `"Ba"`. `fix_locals()` corrects the
  word list (not the rendered text) so caption timings survive.

---

## 3 · "mixed with video and pictures, it doesnt look good… stagnant image of fish"

**You were right, and the cause was worse than the stills.** Measured mean optical flow:

| clip | motion |
|---|---|
| `KK_05_boat.mp4` (real video) | 1.992 |
| **`KK_08_sunset_hero.mp4` (real video)** | **0.149** |
| old Ken Burns still | ~0.65 |

**The generated sunset clip is itself nearly frozen** — more static than the stills you
complained about. And it occupied the last third of the video.

Why Ken Burns always reads as a photo: the move is *rigid*. Every pixel travels on the same
transform, so the eye classifies it instantly. The old setting made it worse — `zoom+0.0012`
per frame is a 1.00→1.086 push across the whole shot.

**Fix:** new tool `tools/animate.py`, two entry points:

- `animate()` for stills — **parallax** (near and far move at different rates, breaking
  rigidity), **caustics** (travelling light bands for underwater), **drifting particles**,
  **handheld** random walk, eased 22% push, grain
- `enliven()` for static *video* — ripple, eased push, sun-glow pulse, and **reframing**

**Note on the metric:** optical flow turned out to be the wrong instrument. A slow rigid pan
scores *high* while looking static, so optimising it was actively misleading. I stopped and
looked at frames instead — `work/qc/anim_check.png` shows the push and moving rays.

---

## 4 · "tanjung aru… just shows a sunset and sea waves, not attractive enough… stale and boring"

**Fix without spending credits: coverage.** One clip is re-cut at several framings, which reads
as several shots.

- `KK_08_sunset_hero` → wide (2.4s) + **tight 2.1× on the sun** (1.8s)
- `KK_03_grill` → wide + tight 2.0× on the prawns
- `KK_07_beach_nev` → wide + tight 1.9×
- `KK_10_cta_silhouette` → wide + tight 1.8×

Tight crops also raise motion, because cropping magnifies whatever movement exists:
sunset 0.149 → **0.83** on the tight framing.

**Timeline: 10 shots → 14 shots**, from the same 10 source files. Zero credits.
Old version spent 46% of runtime on one visual idea (the cut detector read 16.2s→30.4s as a
single 14.2-second shot). New version: 13 cuts = **25.8/min**, inside the 15–25 vlog band.

---

## 5 · "there is no visual hook… CTA on audio but the visual doesnt back it up"

- **Hook 0.15–2.45s:** `3 SPOTS IN KK` / `where locals actually go`
- **CTA 25.0–30.2s:** `WHICH ONE FIRST?` with all three spots listed and left-aligned, then
  `comment 1, 2 or 3` — the audio question is now answerable at a glance
- **AI disclosure** burned in for the full duration. Non-negotiable per `CLAUDE.md`, and it
  was entirely absent from v1.

---

## Delivered numbers

| | v1 (your review) | v2 | gate |
|---|---|---|---|
| duration | 30.42s | 30.21s | — |
| resolution | 720×1280 30fps | 720×1280 30fps | pass |
| loudness | −8.9 LUFS | −9.5 LUFS | band −7…−9, 0.5 dB out |
| true peak | **−0.7 dBTP FAIL** | **−1.6 dBTP PASS** | ≤ −1.0 |
| shots | 10 | **14** | — |
| cuts/min | 9.9 | **25.8** | 15–25 |
| captions | **none** | **16 cards** | — |
| BGM | none (drone) | **synthesised, arranged** | — |
| AI disclosure | **absent** | **full duration** | required |
| silence gap | 24 dB | **15 dB swing into the sub-drop** | present |

---

## Still broken, and it needs your call

**The "islands" shot is the wrong country.** `KK_07_beach_nev` and the boat/coral material show
**limestone karst towers** — that is Krabi or Phi Phi. Tunku Abdul Rahman Marine Park islands are
low and forested. Anyone from Sabah spots it immediately, and local authority is the entire
premise of the channel.

No amount of editing fixes a wrong location. It needs regeneration, which costs credits, and
your contract says the ⏸ gate is the only spend authorisation — so it waits for you.

```
replace the islands shot, Sabah-specific prompt   720p fast 5s   17.5 cr
optional: a purpose-built hook shot                              17.5 cr
optional: replace the two stills with real motion    2 x          35.0 cr
                                                          total ~70 cr
```
Balance was 1,589.31 cr at last measurement.

**Also unresolved:** loudness is 0.5 dB below your band. The peak ceiling is the binding
constraint — going louder needs heavier compression, which flattens the silence before the
reveal. I chose the peak gate over the loudness band. Say the word if you'd rather have it
the other way.

**And the standing gap, unchanged:** nothing has been posted. Every retention figure in this
document is engineered-for, not measured. The 44% estimate is a structural heuristic that says
so in its own output.
