# REMOTION MOGRAPH — proof-of-concept spec (2026-08-12)
### ADDITIVE. Zero edits to engine.py / planqc / verify / the flow.
### Pattern: same as finalmix.py — finished cut in → layer on → out → RE-GATE.
### License: free tier covers individuals & companies ≤3 people, commercial use OK
### (remotion.dev/docs/license/faq, checked 2026-08-12). Renders need headless
### Chrome → HIS BOX ONLY (cloud container 403s browser binaries, same as Playwright).

## DIVISION OF LABOR (the contract)
| job | owner | why |
|---|---|---|
| decode, frame-exact cuts, xfade/whips | ffmpeg (engine.py) | untouched, proven |
| audio: bed, duck, whoosh, loudnorm | ffmpeg (finalmix.py) | untouched, proven |
| final encode / mux | ffmpeg | untouched |
| animated cards, kinetic captions, lower thirds, checklist Artefact Drops, progress bars | **Remotion** | typography + easing ffmpeg drawtext can never do; upgrades cards.py from static PNG to motion |

## POC — SMALLEST THING THAT PROVES IT (his box, ~30 min)
```
npm create video@latest talyx-mograph   # template: "Blank"
```
One composition: `Card.tsx` — 720x1280, transparent background, props
`{text, inMs, outMs}`, Montserrat-ExtraBold 44px white border-black (the v4 card
spec exactly), animated: 6-frame slide-up+fade in, 4-frame fade out.
Render WITH ALPHA:
```
npx remotion render Card out/card.mov --codec=prores --prores-profile=4444
```
Composite onto a finished cut (post-step, like finalmix):
```
ffmpeg -i PANBORNEO.mp4 -i out/card.mov -filter_complex \
  "[0:v][1:v]overlay=0:0:enable='between(t,0.15,3.0)'" -c:a copy OUT.mp4
```

## ACCEPTANCE (before it touches any delivery)
1. Frame-step the seam: card in/out lands on the planned frames, no judder (L124 class).
2. OCR the card region: text renders (the engine font bug class — never trust, read pixels).
3. verify.py still passes on the composited file (CHECK 0 freshness first).
4. A/B against the static-PNG card: HIS EYE decides if motion earns its render time.

## IF THE POC EARNS IT (later, HIS CALL)
- `tools/mograph/` into the repo; a `cards2.py` wrapper so plans declare animated
  cards the same way they declare static ones.
- Karaoke word-timed captions from transcribe.py word timestamps (speech pillars, when the sentence editor exists).
- The Artefact Drop checklist as an animated save-bait card — the Douyin mechanic, upgraded.
