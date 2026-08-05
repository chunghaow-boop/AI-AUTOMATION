# VOICE — the speech layer's identity decisions
### Created 2026-08-05. Speech-led content (pillar `industry`, `car_review`) reads this
### BEFORE any generate_audio call. Chat is disposable; this file is the memory.

## CURRENT DEFAULT (his pick, 2026-08-05)
```
name        Arthur
voice_id    30fc8796-ceb6-4a66-b3a7-4a145ef7f346
voice_type  preset
gender      male (as reported by list_voices)
model       seed_audio (Higgsfield default) unless a variant is named
preview     https://d1xarpci4ikg0w.cloudfront.net/audio_voice_preset/preview/080fcbab-8be3-4d60-8156-3c3040421e0f.mp3
```
**VERIFIED 2026-08-05** against the full `list_voices` catalog (60 presets, has_more
false). The id he supplied matches the catalog exactly — not an invented id.
Hard rule 2 applies to identifiers as much as to credits.

## WHAT IS **NOT** VERIFIED — read this before trusting the pick
**Claude cannot hear audio** (file 06, the Revision Delta Test). The API returns a
NAME and a GENDER — nothing about accent, age, warmth or pace. Any statement about
how Arthur *sounds* would be an invention. The preview URL above is for GAVRIL'S
EARS. Until he has listened and confirmed, the register below is an INFERENCE FROM
THE NAME ONLY, and inference is not measurement.

## THE REGISTER CONFLICT — named once, his call per video
File 14 defines four language modes. A Western-preset voice is right for ONE:

| mode | avatar | Arthur fits? |
|---|---|---|
| **Clean English** — Mode A hero films, brand work | 5 Silent Businessman | **YES** — quiet-luxury narration is exactly this register |
| **Manglish** (default, most content) | 1-4 | **NO** — J4 Local holds an ABSOLUTE veto; a Western voice over Sabah car content is the "copying a Western ad" failure he roasts |
| **BM lead** | 2, 3 heartland | NO |
| **CN/EN mix** | Chinese-market units | NO |

So: Arthur = the brand/hero lane. He is NOT the voice for "car hacks / tips /
life + struggles" content aimed at Avatars 1-4 — that lane needs Nev.

## THE NEV CLONE (the real answer for value content, not yet built)
Drop ONE clean recording of Nev talking (~60s, quiet room, his natural Manglish,
no music) in this folder as `nev_voice_source.wav`. Then:
`create_voice` / `create_voice_from_confirmed_audio` -> a custom voice
(`voice_type: "element"`) that IS him. Recorded once, used forever, and it is the
single strongest trust signal available to J4 and J5 — a real local voice cannot
be faked by any preset.
STATUS: waiting on the recording. Nothing generated yet.

## STANDING RULES FOR THIS LAYER
1. Every speech-led plan DECLARES its voice (`VOICE = {name, voice_id, voice_type}`)
   and its language mode. No orphan narration.
2. `get_cost: true` preflights every generate_audio call. MEASURE before spending.
3. Gavril's ear is the gate on every voice take. No mix/voice claim ships from
   Claude without either a measurement or his confirmation.
