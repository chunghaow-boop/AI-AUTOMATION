# BGM LIBRARY — one folder per PILLAR
### Folder names are the EXACT keys in `assets/pillars/PILLAR-PROFILES.json`.
### That is deliberate: bedqc/planqc can map a plan's PILLAR to its bed folder with
### no lookup table. Do not rename them to friendlier words.

| folder | pillar key | tracks | BPM band (MEASURED profile) | character |
|---|---|---|---|---|
| `car_cinematic/` | car_cinematic | 25 | **140-165** | drift phonk, 60-92% sub-bass, cowbell + distorted 808 |
| `travel_vlog/` | travel_vlog | 0 | **95-115** | see spec below |
| `industry/` | industry | 0 | speech-led, bed is UNDERSCORE only | see spec below |

## THE FINDING THAT MATTERS (2026-08-05)
**Not one of the 25 existing tracks can serve a vlog.** They are 140-165 BPM phonk;
the travel_vlog profile measured 95-115 BPM from 6 reference videos. A phonk bed under
a vlog is the same class of error as the 90-BPM marimba bed under the Crown car edit
(ledger lesson: "wrong on tempo, timbre, distortion and signature instrument").
The vlog library must be sourced fresh, in band. Nothing is reusable.

Also measured: md5 across all 25 files — **zero true duplicates**. The `(1)` / `(2)`
files are different renders, not copies. Nothing to clean.

---

## travel_vlog BED SPEC — what to source (the shopping list)
```
BPM            95-115          (profile, n=6 references)  <- THE hard filter
duration       >= 40s          (video band 16-29s + segment scan needs headroom)
channels       STEREO          (bedqc BLOCKS mono - a synth mono bed failed once)
dynamics       >= 20dB range   (a brick-walled master fights the sidechain)
structure      continuous      (engine scans for the most continuous stretch;
                                a track that is 30% breakdown wastes the scan)
format         mp3/wav, no DRM, no platform rip
```
**Genre words that land in this band:** lo-fi hip hop, chillhop, indie folk-pop,
acoustic travel, "sunny day" indie, bedroom pop, soft house (110-115), tropical
house (100-110), jazzhop. **Avoid:** trap/phonk (too fast + too sub-heavy),
EDM drops (structure fights a 20s cut), anything with a vocal hook (fights the
narration and the captions).

**Count:** 10-15 tracks. bedqc ranks them and picks; a bank of 12 in-band tracks
beats 30 random ones, because the ranking is only as good as the band.

## industry BED SPEC
```
speech-led:    the bed is UNDERSCORE, not the subject. -18 to -24dB under voice.
BPM            not critical (no beat-grid cutting; cuts land on sentence ends)
character      neutral corporate/documentary, NO melody that competes with speech,
               NO drums that imply a cut rhythm the edit does not have
duration       >= 90s (profile duration 35-181s)
```
Source 5-8. This pillar is not next in the queue; fill it when a title needs it.

---

## HOW TRACKS GET IN HERE (measured 2026-08-05 — read before asking Claude to fetch)
Claude **cannot download music**, from either environment. Both are blocked by
mechanism, not by choice:
- **cloud sandbox**: every music host tested (incompetech, pixabay CDN, FMA,
  archive.org, ccmixter, bensound) returns connection-refused — not on the
  container's network allowlist.
- **device_bash** (the bridge to this laptop): has NO network access at all, by design.
- **Higgsfield `generate_audio`**: reads "cannot generate music or sound effects for
  general use ... decline general music requests" — the music model there is walled
  to the game pipeline. It is a TTS tool. Not a bed source.

So beds arrive one of three ways:
1. **Gavril downloads them** (how the 25 phonk tracks arrived) -> drop in the pillar
   folder -> `python3 tools/bedqc.py` ranks and picks.
2. **TikTok Commercial Music Library** — `tiktok_music_trending` lists trending
   COMMERCIALLY LICENSED tracks; the chosen id is passed to `tiktok_publish` as
   `music_sound_id`. Needs the TikTok account connected once (`tiktok_connect`).
   This is the only legitimate route to *famous* music, and it is attached at
   publish, not baked into the mp4.
3. A licensed subscription library (Epidemic/Artlist/Musicbed) — Gavril downloads,
   same as 1.

## WHY NOT JUST BAKE A FAMOUS TRACK INTO THE MP4
Practical, not moral: platform Content ID matches the audio and **mutes or removes
the upload**. A muted car edit is a dead video — the genre is sound-led. The CML
route (2) gets the same recognisable music, legally, and the platform boosts
trending-sound posts. Baking a rip in is the one path that loses both ways.
