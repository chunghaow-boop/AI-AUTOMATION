# The SFX / Foley Bank — Sound Library for Auto-Assembly
### Companion to `19-sound-engineer.md` (the mix) and `11-editing-bank.md` (the recipes).
### Supersedes the old `04-foley-master.md`.
### Talyx / Nev — every beat type maps to a sound. The Editor drops them by rule, not by taste.

---

## How This Bank Works

The Foley Master designs the sound *concept* (file 04). This bank is the **execution library** — for every beat type the pipeline can produce, the exact sounds to drop, with **search terms that work in CapCut/free SFX libraries** (Pixabay, Mixkit, CapCut Sounds). The Editor's auto-edit spec references these entries by ID.

```
beat type in the script → look up its SFX entry → drop at the timestamp → done
```

**The mixing law (applies to every entry):**
- Music bed: sits UNDER the master; master target **-7 to -9 LUFS** (file 19, measured)
- Foley sits **above** the music (music ducks, foley never fights it)
- Hero sound peaks **-6dB** — the loudest thing in the video except the drop
- **One hero sound per video.** Everything else supports.

---

## SECTION A — AUTOMOTIVE (the core bank)

| ID | Beat | The sound | Search terms | Notes |
|---|---|---|---|---|
| A1 | **Door close (premium)** | deep damped *thunk*, no rattle | "car door close solid", "luxury car door" | THE money sound. Cheap = clang, premium = thunk |
| A2 | **Door open** | latch click + seal release | "car door open" | pair with A9 cabin ambience shift |
| A3 | **Engine start (petrol)** | starter whir → catch → settle to idle | "engine start V6", "car ignition" | let the idle breathe 1s before music returns |
| A4 | **Engine start (big/turbo)** | deeper catch + turbo whistle hint | "turbo car start", "engine start deep" | for LC300/performance content |
| A5 | **Key fob** | electronic *chirp* + door locks thunk | "car unlock beep", "central locking" | the fob = the prop-motion trick's sound |
| A6 | **Key slide/drop on desk** | metallic scrape → tap | "keys on table", "metal slide" | the lowball beat. Land it in a music duck |
| A7 | **Keys jingle/handover** | bright jingle into a palm | "keys jingle" | the CTA/handover beat |
| A8 | **Drive-off** | tyres roll on tarmac + engine fades | "car drive away", "car pass by" | fade under the CTA card |
| A9 | **Cabin drop-out** | exterior noise CUTS to near-silence + faint AC hum | "room tone quiet", "car interior ambience" | ⭐ the luxury cue — the SILENCE is the sound |
| A10 | **Wipe/polish** | soft cloth drag + faint squeak on paint | "cloth wipe", "squeak clean glass" | ASMR-tactile, close-miked feel |
| A11 | **Seatbelt** | smooth reel + firm metallic click | "seatbelt click" | the ritual beat |
| A12 | **Indicator** | soft precise tick-tock | "turn signal", "car indicator" | intimacy/familiarity cue |
| A13 | **Showroom ambience** | large clean room tone, faint AC | "showroom ambience", "large room tone" | the floor of every showroom scene |
| A14 | **Rev/exhaust note** | throttle blip, exhaust crackle | "engine rev", "exhaust sound" | J4 warning: wrong engine note = roasted. Match cylinder count |

---

## SECTION B — TRANSITIONS & EDIT PUNCTUATION (pairs with the Transition Library, file 10)

| ID | Edit move | The sound | Search terms | Timing |
|---|---|---|---|---|
| B1 | Whip-pan | short air whoosh | "whoosh transition" | starts 0.1s BEFORE the cut |
| B2 | Flash/light leak | bright airy swish | "swish", "light whoosh" | on the flash frame |
| B3 | Speed ramp (slow→real) | riser into a *snap* | "riser", "time warp" | riser through the slow-mo, snap at real-time |
| B4 | Climax burst cuts | rapid tick/impact per cut | "impact hit", "boom hit" | one hit PER cut in the burst |
| B5 | The payoff/hero reveal | deep cinematic impact + sub drop | "cinematic hit", "braam", "sub drop" | THE loudest moment. Music drops out under it |
| B6 | Double-cut (pod change) | whoosh + soft hit | "whoosh hit" | on the second cut of the pair |
| B7 | Text card ON | subtle pop/tick | "pop click UI" | tiny — felt, not heard |
| B8 | The pre-twist silence | NOTHING — music ducks to 10% | (automation: volume keyframe) | 1.0s of near-silence, then the twist sound lands |

---

## SECTION C — HUMAN / POV FOLEY

| ID | Beat | The sound | Search terms |
|---|---|---|---|
| C1 | Footsteps (showroom) | hard-sole on polished floor | "footsteps marble", "footsteps hard floor" |
| C2 | Footsteps (outdoor) | asphalt/gravel scuff | "footsteps gravel" |
| C3 | Fabric/movement | soft cloth rustle | "clothes rustle" |
| C4 | Breath | one soft exhale | "breath exhale" — use ONCE, at the emotional beat |
| C5 | Phone | notification ding + soft tap | "notification ding", "phone tap" |
| C6 | Glass door | handle clack + whoosh + seal | "glass door open", "door whoosh" |
| C7 | Sit/settle | leather creak + suspension settle | "leather creak", "car seat" |
| C8 | Writing/paper | pen scratch, paper slide | "paper slide", "pen writing" |

---

## SECTION D — AMBIENCE FLOORS (one per scene, always)

| ID | Scene | The floor | Search terms |
|---|---|---|---|
| D1 | Showroom | clean large-room tone + faint AC | "showroom ambience" |
| D2 | Malaysian street (day) | traffic hum, distant horn, tropical birds | "city traffic ambience asia" |
| D3 | Malaysian evening | crickets + distant traffic + warm air feel | "evening crickets ambience" |
| D4 | Car interior (moving) | road hum + faint wind | "car interior driving" |
| D5 | Car interior (parked) | near-silence + AC | "car interior idle" |
| D6 | Office/desk | quiet room + AC + distant phones | "office room tone" |
| D7 | Rain (bonus, cheap drama) | rain on roof/glass | "rain on car roof" |

**Rule: every scene has exactly ONE ambience floor, at low volume, for its full duration. No floor = the "AI silence" that feels dead. Two floors = mud.**

---

## SECTION E — MUSIC BED RULES (the one track)

| Video type (recipe) | Bed style | Search terms | Behavior |
|---|---|---|---|
| Hero single-take (R1) | cinematic minimal, building | "cinematic ambient build" | rise into the reveal |
| 4-beat spine (R2) | mid-energy beat, clear BPM | "upbeat lofi hip hop" | duck at the twist (B8) |
| Chaptered long-form (R3) | steady groove, unobtrusive | "chill beat background" | tiny lift at each pod |
| Velocity montage (R4) | high-energy with a DROP | "phonk", "trap beat drop" | burst lands ON the drop |
| POV/relatable (R5) | lofi at 30% volume | "lofi chill" | foley sits ON TOP of music |

**Copyright law (hard rule):** use CapCut's licensed library or royalty-free (Pixabay/Mixkit) only. A copyrighted track = muted audio or killed reach. Never rip a trending song from another video.

---

## THE ASSEMBLY CHEAT — beat type → sound IDs

The auto-edit spec references this directly:

```
door-open beat      → C6 + D-floor shift + A9 if entering car
wipe/detail beat    → A10 + D1
phone/auction beat  → C5
lowball/twist beat  → B8 (duck) → A6 (slide lands in silence)
handover beat       → A7 → A1 → A3 → A8 (the full exit chain)
reveal/hero beat    → B3 riser → B5 impact
pod transition      → B6
montage burst       → B4 per cut → B5 on payoff
any scene start     → its D-floor, always
```

---

## The Line

> **Silence is the AI tell you can hear.**
> A generated clip with no ambience floor feels dead before the eye knows why.
> One floor + one hero sound + foley on the contacts = a world.
> This bank makes that automatic.
