# travel_vlog BED BANK — MEASURED 2026-08-05
### 19 tracks from chosic.com. Every number MEASURED here (ffprobe + tools/rhythm.py),
### never read off a website. **14 are usable. 7 need zero stretch.**

## THE USABILITY RULE (this is the important part)
A bed is usable if its native tempo reaches the pillar band **within ±8%** — the stretch
the WRX proved safe (Skrrt Slide, +7.73% via asetrate, on-genre). So for travel_vlog's
95-115 band the real acceptance window is **native 88-124 BPM**, not 95-115.
Reading it as "already inside 95-115" scored this same bank at 3/19; the correct rule
scores it 14/19. The plan's BPM is then set to the CHOSEN bed, never the reverse.

`engine.verify_bed_tempo` enforces this at build: it measures the delivered bed and
REFUSES a mismatch (half/double-time accepted as the same grid).

## USABLE — 14 (sorted by how little we have to touch them)

| track | artist | native | plan BPM | stretch | dyn | dur | licence |
|---|---|---|---|---|---|---|---|
| **liqwyd-to-the-moon** | LiQWYD | 97.5 | 97.5 | **0.0%** | 14.6dB | 154s | CC BY 3.0 |
| **Crystal-Water** | Spiring | 99.4 | 99.4 | **0.0%** | 16.4dB | 157s | CC BY 3.0 |
| **Easy-Love** | Hotham | 99.4 | 99.4 | **0.0%** | 15.5dB | 199s | CC BY 3.0 |
| **LiQWYD-Luke-Bergs-Swing** | Luke Bergs & LiQWYD | 95.7 | 95.7 | **0.0%** | 16.3dB | 150s | CC BY 3.0 |
| Back-To-You | Luke Bergs | 105.5 | 105.5 | 0.0% | 14.6dB | 161s | CC BY-SA 3.0 |
| Sunshine-Vibes | Luke Bergs | 97.5 | 97.5 | 0.0% | 13.3dB | 148s | CC BY-SA 3.0 |
| liqwyd-get-away | LiQWYD | 97.5 | 97.5 | 0.0% | 10.6dB | 130s | CC BY 3.0 |
| Love-Me-Back | Hotham | 94.0 | 95.0 | +1.1% | 15.7dB | 148s | CC BY 3.0 |
| **Olive-Spring** | Imperss | 117.5 | 115.0 | -2.1% | **18.5dB** | 269s | CC BY 3.0 |
| focus | Roa | 120.2 | 115.0 | -4.3% | 13.8dB | 260s | CC BY 3.0 |
| stardust | Roa | 120.2 | 115.0 | -4.3% | 14.7dB | 214s | CC BY 3.0 |
| Summer-Breeze | Luke Bergs & Lichu | 120.2 | 115.0 | -4.3% | 14.2dB | 153s | CC BY-SA 3.0 |
| Letting-Go | LYCKEBORN | 90.7 | 95.0 | +4.8% | 14.5dB | 188s | CC BY-SA 4.0 |
| Need-U | Balynt | 121.6 | 115.0 | -5.4% | 14.9dB | 129s | CC BY 3.0 |

## OUT OF REACH — 5 (kept on disk; they may suit a future pillar)
`puzzle` 86.2 (+10.3%) · `Shine-Like-The-Sun` 129.2 (-11.0%) · `Sol` 83.3 (+14.0%) ·
`Pathway-Home` 139.7 (-17.7%) · `Tropical-Soul` 139.7 (-17.7%)

All 19 are STEREO, 129-269s, dynamics 10.6-18.5dB. Tempo is the only rejecting filter.

## THE GENRE-GAP FINDING
Free vlog music clusters at **90-99** (half-time chill) and **117-140** (house/lofi).
95-115 is the trough between them. Sourcing by MOOD tag ("chill", "lofi") lands in the
first cluster; sourcing by "summer"/tropical lands in the second. Both are reachable
once the ±8% rule is applied, which is why the second batch doubled the yield.

## RECOMMENDED FIRST BED
**`liqwyd-to-the-moon`** — 97.5 native (zero stretch), 154s = 5x the video so the
segment scan has real choice, 14.6dB dynamics, and plain **CC BY 3.0** (no share-alike).
Runner-up on numbers alone: **`Olive-Spring`** — the best master in the bank (18.5dB,
269s) at a -2.1% stretch, also plain CC BY.
Avoid `liqwyd-get-away` (10.6dB is the flattest master here — a squashed bed fights
the sidechain) and `Letting-Go` (CC BY-SA 4.0, share-alike).
**These numbers say which beds are ELIGIBLE. Gavril's ear picks the one.**

## LICENCE DISCIPLINE
Chosic tracks are free commercially **only with attribution** — the pages state
"Use without attribution is NOT allowed."
- **CC BY 3.0** (clean, preferred): to-the-moon, get-away, Swing, Love-Me-Back,
  Olive-Spring, focus, stardust, puzzle, Pathway-Home, Need-U, Crystal-Water, Easy-Love
- **CC BY-SA 3.0/4.0** (share-alike — prefer to avoid): Letting-Go, Shine-Like-The-Sun,
  Tropical-Soul, Sunshine-Vibes, Back-To-You, Sol, Summer-Breeze

Credit line format, paste into the description for whichever track ships:
```
<Title> by <Artist> | https://www.chosic.com/download-audio/<id>/
Music promoted by https://www.chosic.com/free-music/all/
Creative Commons CC BY 3.0 — https://creativecommons.org/licenses/by/3.0/
```
Known ids: Get Away 45429 · Focus 45490 · Letting Go 58112 · Pathway Home 45483 ·
Love Me Back 57858 · Olive Spring 37425 · Puzzle 45484 · Swing 53283 · Stardust 45485 ·
To The Moon 58943 · Shine Like The Sun 60566 · Summer Breeze 42078 · Tropical Soul 31985 ·
Need U 59905 · Sunshine Vibes 59298 · Crystal Water 59607 · Back To You 60525 ·
Sol 59665 · Easy Love 58298

## HOW THESE ARRIVED
Claude cannot download in either environment (both network-blocked). These came via
**Claude in Chrome** on Gavril's machine: fetch the mp3 in-page as a blob, trigger a
save. Chrome blocks multiple automatic downloads until the user clicks "Allow" once.
Files land in Downloads and are COPIED here (the bridge cannot delete, so originals
remain in Downloads for Gavril to clear).
