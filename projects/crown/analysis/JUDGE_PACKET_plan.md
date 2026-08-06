# JUDGE PACKET — crown · stage plan
_generated 2026-08-06 06:08 by tools/judge.py_

You are running the reception judges from file `06-content-judges.md`.
This is the gate that kills BORING, which no mechanical check can measure.

## RULES

- Judge what is HERE, not what could be added. Be specific: name a shot index or a timestamp in every finding.
- J0 and J4 hold SOLO VETOES. If either fails, `overall.ship` is false regardless of the other scores.
- Do NOT judge identity (is it really Nev). That verdict is Gavril's, always — it flipped between crop scales on KK, same frames, same session.
- If the evidence does not let you judge a seat, say so in `finding` and set `pass` to false. Never score a seat you could not see.

## SEATS

### J0 — HOOK TYRANT — SOLO VETO
Judge ONLY the first 2 seconds. Is an EVENT already resolving on screen, or is this a tour? A tour is an automatic veto. State the exact moment a thumb would stop, or say there isn't one.

### J2 — STORY — does anything HAPPEN
Is there a state change with a cause, or a sequence of pretty pictures? Name the consequence chain if there is one. Resemblance is not story.

### J4 — TEXT + CLAIM — absolute veto on invented facts
Any on-screen text, badge, spec or claim that is wrong or unverifiable. An invented 'SR' badge shipped through 8 builds. You have an ABSOLUTE veto.

## EVIDENCE

```
PROJECT: Toyota Crown Crossover 2.4 RS Advance · chill coastal cinematic · Nev
PILLAR:  car_cinematic_chill   100.0 BPM   21 shots   31.20s pre-blend

CONTENT BLOCK
  claim     The Crown Crossover has never been sold new in Malaysia by UMW Toyota - every unit here is a Japan-market import through the recond channel.
  verified  paultan.org 2024-03-04 covers a Crown Hybrid SPOTTED in Malaysia and asks whether it is coming at all; Malaysian availability is recond/used listings only (motortrader recond index, carlist). Card 4 says NEVER SOLD NEW IN MALAYSIA, exactly this claim - not the wider 'Toyota never sold it here', which is false and which J4 would roast. POWER FIGURE RETRACTED 2026-08-05: v1 shipped 350PS on a derivation (272+83+81) that sums to 436. Hybrid output is not additive and Toyota's own release states no figure. NO NUMBER SHIPS until a JDM spec sheet confirms one.
  twist     the product feature is the story device AND the man operates it. Combustion is withheld for 14 seconds so one engine start is the loudest thing in the film - he causes that start, and later causes the darkness. A non-hybrid car has no silence to spend. Cards read as a sentence: CROWN, hybrid, no engine yet -> Sabah coast, still nothing running -> he asks, it wakes -> you cannot buy it new here -> DM me.
  why_stop  shot 0 is a light EVENT, not a tour - the car crosses from black shade into blazing backlight inside 1.8s - and card 1 names the car AND the mechanism, so a MUTED viewer is told what to notice. v2's fatal weakness was that its differentiator was inaudible and unstated; sound-off, it was a car at sunset. Payoff at 14.00s delivered, inside the 15s line.

SHOT LIST  (index · source · act · beats · delivered t · note)
   0  A       EVENT    med     0.00s  shadow into gold - already moving, and silent
   1  B       PAYOFF   burst   1.80s  gold on the coast road, still silent
   2  C       EXTERIOR burst   3.00s  the alloy turns, tarmac streaming, silent
   3  D       HUMAN    burst   4.20s  his hands settle on the rim, silent, the road runs ahead
   4  B       PAYOFF   med     5.40s  the coast road opens out, gold everywhere, nothing driving it
   5  K       EXTERIOR burst   7.20s  the Sabah shoreline past the barrier, gold flat on the water
   6  C       EXTERIOR burst   8.40s  kerb line under the alloy at road level, the last of the gold
   7  E       EXTERIOR burst   9.20s  the light bar comes on as the gold dies
   8  G       EXTERIOR burst  10.40s  wide bay, the coast road bends away, the last gold flat on it
   9  F_load  EVENT    burst  11.60s  the road tilts up into the ramp - still electric, nothing running
  10  J       HUMAN    burst  12.80s  HIS DECISION - the silhouette commits, foot down on the ramp
  11  F_wake  EVENT    hold   14.00s  IT WAKES on the ramp because he asked for it
  12  E       EXTERIOR burst  17.00s  the light bar pulls away from the ramp, climbing now
  13  G       EXTERIOR burst  18.20s  wide - the car small, climbing toward the crest
  14  F_wake  EVENT    burst  19.40s  at the crest it hardens and holds, steady under load
  15  G       EXTERIOR burst  20.60s  the load falls away past the crest, it goes quiet again
  16  I       EXTERIOR burst  21.40s  quiet at the barrier, blue hour, nothing running
  17  H       HUMAN    burst  22.60s  he sits, hand still on the rim at the barrier
  18  I       EXTERIOR med    23.80s  the bay from outside the barrier, the cabin still lit
  19  H       HUMAN    hold   25.20s  HIS HAND KILLS IT - key off, the cabin goes dark
  20  I       EXTERIOR med    28.20s  dark bay, the car parked in it, nothing running

CARDS
  shot 0-3  [cap]  "CROWN. HYBRID. NO ENGINE YET"
  shot 5-8  [cap]  "SABAH COAST. STILL NOTHING RUNNING"
  shot 11-13  [cap]  "HE ASKS. IT WAKES."
  shot 15-17  [cap]  "NEVER SOLD NEW IN MALAYSIA"
  shot 18-20  [cta]  "RECOND. DM FOR THE PRICE"

LINKAGE (boundary · kind · token · why)
   0-> 1  light       gold               the car breaks into the gold -> the gold is the whole road
   1-> 2  sound       silent             silent at speed -> still silent, the absence is established
   2-> 3  sound       silent             the alloy turns in silence -> his hands rest in the same silence
   3-> 4  consequence road               his hands settle -> the road opens out in front of that decision
   4-> 5  light       gold               the gold on the road -> the same gold laid flat on the water
   5-> 6  light       gold               gold on the water -> the last of the gold down at ground level
   6-> 7  consequence gold               the gold is dying -> so the light bar comes on
   7-> 8  light       gold               the light bar against the dying gold -> the bay holding the last of it
   8-> 9  motion      road               the road bending away -> the road tilting up into the ramp
   9->10  consequence ramp               the ramp arrives -> HE COMMITS to it, foot down
  10->11  consequence ramp               he asked for it on the ramp -> THE ENGINE ANSWERS. the hero
  11->12  consequence ramp               it woke on the ramp -> the car pulls away from it
  12->13  motion      climb              climbing away -> still climbing, seen small across the bay
  13->14  motion      crest              climbing toward the crest -> arriving at the crest
  14->15  consequence crest              the crest is reached -> so the load falls away past it
  15->16  consequence quiet              it goes quiet -> arrival, quiet at the barrier
  16->17  subject     barrier            the car at the barrier -> him inside it at the same barrier
  17->18  object      barrier            him at the barrier -> the same barrier seen from outside
  18->19  consequence cabin              the cabin is still lit -> HIS HAND KILLS IT
  19->20  consequence dark               he switched it off -> the whole frame dark, nothing left running

SOUND hero: THE PETROL ENGINE CATCHING (shot 11, 14.00s delivered), CAUSED by his commit in shot 10. ONE hero sound per video (file 04, law 4).
SOUND silence: shots 0-10 (0.00-14.40s pre-blend) carry NO COMBUSTION - written into eleven prompts, not just into the gain map. Shot 20 returns to it.
```

## RETURN EXACTLY THIS JSON, nothing else

```json
{
  "verdicts": [
    {
      "seat": "J0",
      "pass": true,
      "score": 0,
      "finding": "one sentence",
      "fix": "one concrete action",
      "where": "shot index / timestamp / 'whole cut'"
    }
  ],
  "overall": {
    "ship": false,
    "one_line": "the single most important thing to fix"
  }
}
```

`score` is 0-10. `pass` is your verdict for that seat alone.
