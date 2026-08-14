# JUDGE PACKET — desafarm · stage plan
_generated 2026-08-07 06:42 by tools/judge.py_

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
PROJECT: NEV AT DESA DAIRY FARM · travel vlog · BRZ day trip · Kundasang
PILLAR:  travel_vlog   97.5 BPM   20 shots   28.31s pre-blend

CONTENT BLOCK
  claim     Desa Dairy Farm sits at about two thousand metres in Kundasang, costs RM10 for a Malaysian adult with MyKad, opens 8am to 5pm - and you cannot just turn up, tickets have to be booked in advance.
  verified  explorekundasang.com, 'Desa Dairy Farm Kundasang Guide', FETCHED 2026-08-07, states each figure outright: 'Malaysian adults with MyKad: RM10', non-Malaysians RM20, Malaysian children 7+ RM7, under 7 free; 'No walk-ins; tickets must be booked in advance'; '8:00 AM - 5:00 PM daily'; Mesilau village, Kundasang, Ranau at approximately 2,000 metres elevation; 'roughly a two-hour drive from Kota Kinabalu'; the cattle are Holstein Friesians, brought in for milk yield and highland tolerance; soft-serve ice cream is made from the farm's own milk. A PRICE IS A MARKET STATUS AND MARKET STATUSES GO STALE - that is what J4 vetoed on crown - so the card says RM10 WITH MYKAD, which names the exact qualifier the source names and is checkable at the gate. DELIBERATELY OFF SCREEN: the 'Little New Zealand' epithet, which J4 vetoed on kundasang when it was asserted in our own voice. ALSO OFF SCREEN: the BRZ's market position. Subaru Malaysia lists the current ZD8 and paultan.org lists the previous ZC6 from RM232,869; a BRZ at this price point is a recond or used buy, which is the audience exactly - and it is a status, so it stays in this block with its date and never on a card.
  twist     the animals act on HIM. The whole field posts this farm as a photo-stop - green hills, a cone of ice cream, a drone over the pasture, the New Zealand line - and in almost none of it does an animal do anything. Here a goat takes the bottle out of his hand in the first second and he is still laughing about it four shots later. A sports car parked on a cow pasture at 2,000m is the second joke, and neither is explained.
  why_stop  frame zero is an ANIMAL DOING SOMETHING TO A PERSON - it reads at phone size, it resolves inside a second, and it is funny before it is pretty; card 2 is the single most useful fact about this place (you cannot walk in) and it is the one every other post leaves out; the BRZ gives the recond audience a reason to watch a farm video at all; and the CTA is a question with a date implied rather than a request for a follow.

SHOT LIST  (index · source · act · beats · delivered t · note)
   0  A       EVENT    burst   0.00s  the goat takes it - lunges and yanks the bottle clean out of his hand on the open green slope
   1  B       EXTERIOR burst   1.23s  rewind to first light: the blue BRZ climbing the road toward that same green slope
   2  C       HUMAN    burst   2.46s  low in the seat, one hand on the wheel, the road unrolling ahead
   3  B       EXTERIOR burst   3.69s  the road opening out, pasture on both sides, the ridge ahead
   4  C       HUMAN    burst   4.92s  hands on the wheel, the road now running straight through open pasture - he is here
   5  D       EXTERIOR burst   6.15s  the BRZ stopped on the grass at the edge of the pasture
   6  F       EXTERIOR burst   7.38s  the herd on the slope, one lifting its head at him
   7  K       EXTERIOR burst   8.62s  the hills wide - the whole green slope and the granite ridge
   8  L       HUMAN    burst   9.85s  he walks out across the grass with the bottle, cattle turning
   9  E       HUMAN    med    10.84s  the calf takes the bottle and shoves it upward, froth, his arm absorbing it
  10  G       EXTERIOR burst  13.30s  the goats crowd the rail, climbing over each other, mouths working
  11  A       EVENT    burst  14.53s  one goat gets the bottle - yanks it sideways and takes it
  12  H       HUMAN    burst  15.76s  the laugh: startled first, hands still up where the bottle was, the goats still going behind him
  13  G       EXTERIOR burst  16.99s  the goats still pushing, unbothered, while the calf feeds on behind them
  14  E       HUMAN    burst  18.22s  back to the calf, calmer now, draining the last of the milk out of the bottle
  15  J       EXTERIOR burst  19.45s  the milk itself - a plain cold glass of it, condensation running, the animals behind
  16  H       HUMAN    med    20.68s  the laugh lands - shoulders down, still looking at the animals, the road down waiting
  17  I       PAYOFF   burst  23.14s  the BRZ pulls away down the road, low sun in bars across its flank
  18  M       EXTERIOR burst  24.38s  last look at the car - the flank, the ducktail, the ridge behind, the road below
  19  I       PAYOFF   med    25.61s  the last of it: the road down, ridges going blue and long

CARDS
  shot 4-7  [cap]  "RM10 WITH MYKAD"
  shot 9-12  [cap]  "BOOK AHEAD, NO WALK-INS"
  shot 14-17  [cap]  "TWO THOUSAND METRES UP"
  shot 16-19  [cta]  "KUNDASANG NEXT WEEKEND?"

LINKAGE (boundary · kind · token · why)
   0-> 1  place       slope              the green slope where the goat took it -> the road climbing toward that same slope, hours earlier
   1-> 2  place       road               the highland road from across the valley -> the same road through the windscreen
   2-> 3  motion      road               the road climbing away -> the road opening out ahead
   3-> 4  activity    road               the drive continues - the same road outside the car, then through the windscreen
   4-> 5  consequence pasture            the pasture fills the windscreen, SO he stops the car on the grass
   5-> 6  place       slope              the car at the edge of the slope -> the herd standing on the same slope
   6-> 7  subject     ridge              the granite ridge behind the herd -> the same ridge above the wide hills
   7-> 8  action      grass              he starts walking out across the grass -> he is out on the grass with the bottle
   8-> 9  consequence bottle             he carries the bottle out to them, SO the calf takes it
   9->10  audio       animal             the feeding noise carries straight into the goats' jostling
  10->11  consequence goat               the goats are crowding and shoving, SO one of them gets the bottle
  11->12  event       bottle             the bottle is yanked out of his hand -> his hands are still up where it was
  12->13  activity    goats              the goats carry on regardless - going behind him as he reacts, still going after
  13->14  audio       calf               the animals keep going - goats at the rail, then the calf still feeding
  14->15  consequence milk               the calf drains the bottle, SO the milk is what he goes and drinks
  15->16  gaze        animals            he looks off at the animals -> the laugh lands on the same look
  16->17  consequence road               the day is done, SO he takes the road down
  17->18  object      flank              the car pulling away -> the same flank, close, in the last light
  18->19  motion      road               the car leaving the frame -> the road running down and away

SOUND hero: the goat's grunt and the bottle scraping out of his hand on shot 0. After that the farm carries it - hooves, bleating, distant lowing, then the boxer engine on the road down.
SOUND silence: none - animals are continuous from shot 6 to shot 15; the two quiet shots are the wide and the milk, where the bed comes forward
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
