# PROMPTS — build these assets ONCE, reuse forever
### For an AI persona, consistency IS the product. Build in this order.

## ⭐ STEP 1 — THE CHARACTER SHEET (do this before anything else)
Source: Tao Prompts, *How to Create LONG AI Films in Minutes* — his exact structure, adapted.
Run with your KOL reference images as inputs. Output = permanent `start_image` for every build.

```
Create a professional character reference sheet of a young Malaysian man in his early twenties,
short black hair with a side-swept fringe, wearing an oversized plain tan mock-neck sweatshirt,
light blue straight-leg jeans and black-and-grey sneakers. Plain empty neutral grey background.

Arrange into four vertical columns, each representing one viewing angle. Each column contains a
full-body view on top and a matching close-up portrait directly beneath it.
Column 1: front view (full body above, front portrait below)
Column 2: left profile (full body facing left) with portrait facing left below
Column 3: right profile (full body facing right) with portrait facing right below
Column 4: back view, with matching portrait below

Maintain even spacing and framing around the character portraits. Clean silhouette, consistent
alignment, clean panel separation. Photorealistic, DSLR, muted colors. Shot on 35mm film.
No Text. Thin borders. Flat lighting.
```

## STEP 2 — THE LOCKED ASSET SET (images only, cheap, permanent)
```
□ 3 wardrobe states     episodes feel distinct without identity drift
□ 3 locations           garage / open lot / desk-office — one per pillar
□ 1 title card / pillar  fixed font+position = recognition in frame 1 (file 14 rule)
```

## STEP 3 — SHOT CHAINING (how to exceed 15s without drift)
Seedance caps at 15s. To go longer:
> extract the **last frame** of shot N → use it as the **`start_image`** of shot N+1.
Your own doctrine already says *"only a start_image fixes frame 1."* This is that, recursively.

## STEP 4 — THE FORMAT TEMPLATES

### CAR REVIEW (route: Marketing Studio "Product Review" preset, or Seedance + refs)
```
avatar_ids: [<Nev>]   hook_id: <from show_marketing_studio>   setting_id: <lot/garage>
generate_audio: TRUE           ← the old "silent always" rule is OBSOLETE for talking formats
9:16 · 720p · 12-15s per clip
PERFORM: weight in the body · hands have a JOB · head-first-eyes-follow · reset to neutral
EMOTION: name the CONFLICT, not the expression (suppress → leak → reset)
CAMERA:  body + lens + T-stop written literally into the prompt
```

### VLOG  — 15-25 cuts/min, max 3s per shot, hard cuts not dissolves
### INDUSTRY VALUE — 6-12 cuts/min, proof-driven hook, on-screen data

## ⚠️ THE COST ARCHITECTURE — read before generating anything
720p std = 4.5cr/s. Naive 60s = 270cr. Three pillars weekly = 3,240cr/month. You have 1,850.
**Do not generate 60 seconds of video. Generate the moments that must move.**
```
0-15s   TALKING clip (Seedance, audio ON, KOL ref)     67.5cr
15-35s  STILLS + ffmpeg zoompan + VO + captions          ~8cr
35-50s  TALKING clip #2 (the payoff/verdict)           67.5cr
50-60s  STILL CTA card (the Artefact Drop)               ~2cr
        ≈145cr vs 270cr naive — same runtime, ~46% saved
```
Further levers: `seedance_2_0_mini` for B-roll · `fast` mode for all probes · 720p not 1080p ·
reuse one asset set forever.

## MODEL ROUTING (verified via models_explore)
| need | model |
|---|---|
| car review / UGC / tutorial | **Marketing Studio** (Product Review preset, avatar_ids) |
| talking head, identity-locked | **Seedance 2.0** + refs, generate_audio:true |
| lip-sync to your own VO | **Wan 2.7** (accepts audio_references) |
| multi-shot single gen | **Kling v3.0** |
| cheap B-roll | **Seedance 2.0 Mini** |
