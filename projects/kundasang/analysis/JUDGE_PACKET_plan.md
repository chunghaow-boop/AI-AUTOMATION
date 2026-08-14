# JUDGE PACKET — kundasang · stage plan
_generated 2026-08-06 09:06 by tools/judge.py_

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
PROJECT: NEV IN KUNDASANG · travel vlog · one day · GLC 300
PILLAR:  travel_vlog   99.4 BPM   20 shots   28.97s pre-blend

CONTENT BLOCK
  claim     Kundasang is about a two-hour drive from Kota Kinabalu, and Mount Kinabalu shows clearest between 6 and 8am - which is why the whole video opens at dawn and not at lunch.
  verified  explorekundasang.com, 'Mount Kinabalu from Kundasang' (2026 guide) - states a two-hour drive from Kota Kinabalu and names 06:00-08:00 as the clearest window. FETCHED 2026-08-06, same day as this plan. CARD 3, added after J4 vetoed it unsourced: Daily Express Malaysia (Sabah's leading news portal), 'Sabah's own little New Zealand' - the card quotes that published phrasing rather than asserting a nickname in our own voice, and the same epithet is independently attested across Tripadvisor reviews of Desa Dairy Farm and Places Malaysia. The card was ALSO moved from shots 11-14 to shots 8-11 so it sits on the pasture footage it describes - J4's second, independent finding. SEPARATE, and deliberately NOT on screen: carbase.my (fetched 2026-08-06) lists the current Malaysian X254 range as GLC200 CKD RM329,888 and GLC350e 4Matic CKD RM398,888; the GLC300 4Matic AMG Line was the CBU launch variant at RM429,888 and is not in the new lineup. That is a market STATUS and market statuses go stale - it is the reason the car is shown and never captioned.
  twist     the car is the clock. One vehicle, one person, six light states, and every cut is a declared carry - so the day physically moves instead of cutting between postcards. The field posts drone beauty with nobody in it, or itinerary lists with no story; nobody drives you through ONE day.
  why_stop  frame zero is a state change, not a tour - cloud tears off the summit while the car is already moving below it (the refsense finding: an EVENT does not require motion, but here it has both); card 1 is a drive time, which is the single thing anyone planning this trip actually searches for; the CTA is a question with a date attached to it by implication - next weekend - not a request for a follow.

SHOT LIST  (index · source · act · beats · delivered t · note)
   0  A       EVENT    burst   0.00s  cloud tears off the summit at dawn - the GLC small on the ridge road below
   1  B       EXTERIOR burst   1.21s  the GLC climbing the switchback road into the same cloud, summit above
   2  A       EVENT    burst   2.41s  summit clear now - the mountain the whole climb was for
   3  C       HUMAN    burst   3.62s  in the cabin, window down, cold air, the mountain ahead and the valley below
   4  D       EXTERIOR burst   4.83s  vegetable terraces under morning mist, the valley waking
   5  C       HUMAN    burst   6.04s  hands on the wheel, mist crossing the windscreen, the road unrolling
   6  B       EXTERIOR burst   7.24s  the GLC running the valley road down to the farm gate, past the terraces
   7  E       EXTERIOR burst   8.45s  past the gate - cows on the green hills
   8  D       EXTERIOR med     9.66s  the valley wide - the same green hills, terraces stacked, grass moving, cloud rolling back in
   9  E       EXTERIOR burst  12.07s  cows close, grass turning, the cloud shadow crossing them
  10  F       HUMAN    burst  13.28s  the cloud closing in, so Nev pulls over and steps out at the viewpoint, wind pulling his jacket
  11  G       EXTERIOR burst  14.49s  the GLC parked at the viewpoint, summit centred behind it
  12  F       HUMAN    med    15.69s  Nev at the railing, the summit and the mountain straight in front of him
  13  G       EXTERIOR burst  18.11s  the GLC in detail - wheel, flank, mountain held behind, golden starting
  14  H       HUMAN    burst  19.32s  golden hour finds his face
  15  F       HUMAN    burst  20.52s  Nev walking back to the car in the same golden hour
  16  H       HUMAN    med    21.73s  at the car he turns to the lens - the day landed, the road down waiting
  17  I       PAYOFF   burst  24.14s  the GLC pulls away, tail lights lit, road descending
  18  J       EXTERIOR burst  25.35s  tail lights small on the ridge road, valley lamps waking below
  19  I       PAYOFF   med    26.56s  last of it on the descending road home

CARDS
  shot 0-3  [cap]  "2 HOURS FROM KK"
  shot 4-7  [cap]  "CLEAREST 6 TO 8AM"
  shot 8-11  [cap]  "SABAH'S OWN LITTLE NEW ZEALAND"
  shot 16-19  [cta]  "KUNDASANG NEXT WEEKEND?"

LINKAGE (boundary · kind · token · why)
   0-> 1  motion      cloud              the cloud torn off the summit streams down over the climbing car
   1-> 2  object      summit             the summit the car is climbing toward -> the summit uncovered
   2-> 3  consequence mountain           the mountain is clear, SO the day starts: he drives
   3-> 4  gaze        valley             he looks down into the valley -> the valley he is looking at
   4-> 5  light       mist               the same mist, on the terraces then on the windscreen
   5-> 6  motion      road               the road unrolling inside the cabin -> the same road from outside
   6-> 7  consequence gate               the road arrives at the farm gate, SO we are through it
   7-> 8  subject     hills              the hills the cows stand on -> the same hills, wide
   8-> 9  motion      grass              grass moving in the wide valley -> grass turning at the animals' feet
   9->10  consequence cloud              the cloud is closing back over the pasture, SO he pulls over and gets out
  10->11  subject     viewpoint          he arrives at the viewpoint -> the car at the same viewpoint
  11->12  gaze        summit             the summit behind the car -> the summit he is facing
  12->13  subject     mountain           the mountain he faces -> the mountain held behind the car
  13->14  light       golden             golden starts on the paint -> golden lands on his face
  14->15  light       golden             the same golden hour, on his face then on his walk back
  15->16  consequence car                he reaches the car, SO he turns and closes the day
  16->17  consequence road               the day is done, SO he takes the road down
  17->18  motion      tail lights        the tail lights leaving -> the same tail lights small on the ridge
  18->19  motion      road               the ridge road above -> the descending road home

SOUND hero: the dawn reveal (shot 0) - wind and the distant climb, then the highland ambience takes over for the rest of the day
SOUND silence: none - highland ambience carries every gap; the bed breathes with the altitude
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
