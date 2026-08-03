# BMW i8 · CAR CINEMATIC · 30s · 720p 9:16
### Phase 1 — planned before generating. Gate below.

---

## PHASE 0 — RESEARCH GATE: **PASS** (5 refs, 9 lessons)

The plate has to prove these or the build is a wrong-car build:

- **BUTTERFLY / SCISSOR DOORS**, hinged at the A-pillar, rising theatrically. The single
  most recognisable i8 move, and the only shot in this list nothing else can fake.
- **LASER HEADLAMPS with a passively lit BMW i BLUE BAND inside the housing.** World's first
  production laser lights. That blue band is the night signature — and it matches the pillar's
  *"night, hard artificial, the car emits its own light"* finding exactly.
- **Black "stream flow" floating rear buttress** with an open air channel through the C-pillar,
  separated from the roof. Nothing else on the road has this silhouette.
- Narrow closed kidney grilles with **BMW i blue surround**, exposed carbon sill, blue skirt.
- 20-inch turbine alloys with aero covers. Adaptive rear spoiler, diffuser.

**Grade note: the i8 palette is blue / black / white. Do NOT reuse the LC300 warm grade.**

---

## THE GRID — `beatplan --bpm 150 --dur 30 --hold 8`

```
26 shots · 30.40s · 150 BPM · beat 400ms
median shot 0.80s (target 0.77) · 49.3 cuts/min (target 44.7) · rate_variation 1.08
```

---

## COVERAGE — THE NUMBER THAT DECIDES THE COST

```
distinct sources >= shots / 2.5      26 / 2.5 = 10.4  ->  11 SOURCES MINIMUM
```

This is the rule that cost us the whole afternoon on the LC300. Four clips carrying 14 shots
gave 7 of 13 cuts with histogram correlation > 0.95 — the timing was perfect and the video
still read as a stutter, because **cut rate has to be earned by coverage.**

A 30s cinematic is roughly **double** the 16s LC300, so it needs roughly double the footage.
There is no way around this that does not reintroduce the stutter.

| # | slot | what it must show | fills |
|---|---|---|---|
| A | front 3/4, night | laser lamps + blue band igniting | hook, loop |
| B | **butterfly doors opening** | the signature move | HOLD 1 |
| C | wheel / turbine alloy | + carbon sill, blue skirt | burst |
| D | rear 3/4 | floating buttresses, spoiler up | burst |
| E | **rolling, night, wet road** | the payoff | HOLD 2 |
| F | interior cockpit | driver-angled, blue ambient | burst |
| G | laser lamp macro | the blue band, tight | burst |
| H | side profile | stream-flow C-pillar air channel | burst |
| I | rear lights + diffuser macro | night | burst |
| **J** | **Nev + car, exterior** | persona, night forecourt | HOLD 3 |
| **K** | **Nev, driving / doorway** | persona, second angle | burst |

---

## COST — preflighted, `mode: fast` explicit

| item | qty | cr |
|---|---|---|
| i8 plate `nano_banana_pro` | 1 | **2.00** ✅ *spent* |
| Nev plate `nano_banana_pro` | 1 | 2.00 |
| car clips `seedance_2_0 fast 720p 5s` | 9 | 157.50 |
| Nev clips (`image_references` = [nev_plate, i8_plate]) | 2 | 35.00 |
| | **total** | **196.50** |

Balance ~1,338 → **~1,141** after.

> `std` is the model default at 4.5 cr/s. Every clip must pass `mode: fast` explicitly or
> this quote is wrong by 45%.

---

## TWO BLOCKERS

**1 · The i8 plate is generated and I cannot look at it.** The sandbox has no outbound
network — Higgsfield's CDN returns `000`. Check it for: blue band inside the lamp, floating
rear buttress with an air channel, low wedge stance. If it rendered an i4 or an 8-Series,
that is 2 cr to fix and 157 cr to not fix.

**2 · Nev still has no plate.** The Higgsfield upload widget is open from earlier — pick
`NEV_PLATE_SOURCE.jpeg` from this folder, one click. Without it, slots J and K cannot be
generated, and "with Nev inside" is the brief.

`seedance_2_0` takes `image_references` **plural**, so one generation carries Nev *and* the
i8 — that is how J and K stay on-model for both subjects at once.

---

## WHAT RUNS AFTER APPROVAL

Everything is already built and proven on the LC300:

```
phonk.py --bpm 150 --dur 30        bed FIRST, phase-trimmed so hit 1 lands on t=0
beatplan --hold 8                  26 shots, burst/rest, frame-exact
clipsense action_peaks_s           every shot centred on a real action peak
shot_match                         exposure matched on RENDERED segments
fx.mask_slice                      blends at section boundaries only, never dip
grade                              saturation only - NO double grade
sfxgen                             whoosh/impact, bed sidechain-ducks under it
captions                           lower third y=0.72, never centre
verify.py                          10 checks, one verdict
```

No burned-in AI label — set the platform AI toggle at upload.
