# REMOTION MOGRAPH — proof-of-concept spec (2026-08-12)
### ADDITIVE. Zero edits to engine.py / planqc / verify / the flow.
### Pattern: same as finalmix.py — finished cut in → layer on → out → RE-GATE.
### License: free tier covers individuals & companies ≤3 people, commercial use OK
### (remotion.dev/docs/license/faq, checked 2026-08-12). Renders need headless
### Chrome → HIS BOX ONLY (cloud container 403s browser binaries, same as Playwright).

## PIPELINE ORDER (his design 2026-08-12 session 11, REVISED same day:
## sound BEFORE polish — "after ffmpeg we do the sound first, then polish at Remotion")
```
1 ROUGH CUT      ffmpeg from the plan: frame-exact grid, cuts, xfade/whip.
                 Diegetic clip audio captured here (cut with the picture).
2 SOUND          finalmix, the sound-engineer seat: bed, duck, whoosh, foley
                 balance, loudness (-c:v copy, video untouched — proven V5
                 path). SFX placed by the PLAN's declared timestamps, which
                 is why sound does not need to see the polish layer.
3 PICTURE POLISH Remotion overlay LAST: cards, captions, dip/wipe/flash.
                 WHY LAST: the layer his eye re-iterates most — a rejected
                 card re-renders one overlay, never the mix.
                 HARD RULE A: frame count in == frame count out.
                 HARD RULE B: -c:a copy — the approved mix passes through
                 BYTE-IDENTICAL (hash-comparable), never re-encoded.
4 EDIT QC GATE   on the final file: capcheck, bedcheck re-run, verify (reference-
                 baselined picture). FAIL -> the gate's ADJUSTMENTS go BACK to
                 step 1 and the whole 1-2-3 runs again. Loop until PASS.
                 (his adjustment 2026-08-12; the loop re-EDITS and never
                 regenerates - a defect that editing cannot fix stops the loop.)
5 MASTERMIND     FINAL BOSS QC, file 27, on the passing file. FAIL -> back to
                 step 1. PASS -> hand to HIM.
6 HIM            THE FINAL FINAL BOSS QC, his eye. Then wait for his feedback.
_ old note       on the FINAL file only: capcheck (final visuals), bedcheck
                 re-run (PROVES the gated mix survived the composite — measure,
                 never trust), verify CHECK 0 freshness first.
```

## DIVISION OF LABOR (the contract — HIS RULING 2026-08-12 session 11:
## "ffmpeg is for the rough cut and the basic cutting. Remotion is to polish,
## to add transition into the video.")
| job | owner | why |
|---|---|---|
| decode, frame-exact cuts, audio, encode/mux | ffmpeg (engine/finalmix) | untouched, proven |
| xfade dissolves + reserved whips | ffmpeg | a dissolve needs BOTH source clips; the overlay layer only sees the finished cut. Moving the timeline into Remotion = re-proving frame-exactness from zero. The ONE carve-out from his ruling, flagged to him same day. |
| overlay-class transitions: dip, flash, wipes, mask swipes, light leaks | **Remotion** | alpha .mov overlaid at declared boundary timestamps, finalmix-pattern, zero engine edits. Upgrades v6's plain fades to designed moves. |
| animated cards, kinetic captions, lower thirds, checklist Artefact Drops, progress bars | **Remotion** | typography + easing ffmpeg drawtext can never do; upgrades capcards.py static PNGs to motion |

## POC — SMALLEST THING THAT PROVES IT (his box, ~30 min)
```
npm create video@latest talyx-mograph   # template: "Blank"
```
One composition: `Card.tsx` — 720x1280, transparent background, props
`{text, inMs, outMs}`, THE LOCKED CAPTION STYLE (2026-08-12, capcards.py):
CapCutSansText-Bold, white + ONE #FFD54A keyword, rounded pill black@0.45,
y=0.70 — animated: 6-frame slide-up+fade in, 4-frame fade out. Must pass
capcheck.py on the composited output (the new gate, floor 4.5:1).
SECOND composition (his transition ruling): `Dip.tsx` — full-frame black (or
white for flash) alpha ramp, props `{atMs, widthMs, colour}` — replaces v6's
plain ffmpeg fades with eased, designed versions. Same overlay pattern.
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
