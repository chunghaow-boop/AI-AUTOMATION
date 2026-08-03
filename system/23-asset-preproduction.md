# ASSET PRE-PRODUCTION — build the assets BEFORE the video
### File 23 · Learned from a Chinese AI-drama tutorial (log #35). **This is the biggest structural
### upgrade since the multi-shot template.** It solves identity/scene drift at the root.

---

## THE CORE IDEA WE WERE MISSING

Our system prompts every shot **fresh** and hopes identity holds. Theirs builds a **reusable asset
library first**, then generates video *from* those assets. Consistency stops being luck.

```
OUR OLD WAY   title → prompt → generate → hope the face/car/room matches → reroll
THE NEW WAY   title → BUILD ASSETS (character · expression · action · scene)
                    → generate video FROM the assets → consistency is structural
```

## THE FIVE ASSET CLASSES (their taxonomy, translated)

| # | Asset | 中文 | What it is |
|---|---|---|---|
| 1 | **Character asset** | 角色资产 | the person, locked |
| 2 | **Four-view asset** | 四视图资产 | that person from front / side / back / 3-4 — one image |
| 3 | **Expression asset** | 表情资产 | a sheet of emotions so *"the character's mood changes without the face changing"* |
| 4 | **Action asset** | 动作资产 | poses/movements as reference |
| 5 | **Scene asset** | 场景资产 | *"don't just give AI one pretty spatial image"* — a full spatial system |

## ⚡ THE NINE-GRID TECHNIQUE (九宫格) — the single most useful trick

Generate **ONE image containing a 3×3 grid = nine angles of the same space (or character)**.
That one image then becomes the reference for every subsequent video shot.

Their actual scene-asset prompt, translated from the video:
> *"Generate a set of cinematic empty-office scene reference images for a workplace power-reversal
> short drama, in a **3×3 nine-grid layout. No people in frame.** The space is a modern corporate
> office — not a lobby, not a luxury executive suite — a complete space **suitable for long-take
> staging.** Cold, transparent, with a sense of pressure; the meeting room formal, quiet, strong
> sense of power. The space must **support a camera move that starts at the printer's paper output
> and follows the document through…** Nine cells with clear boundaries, each showing a different
> angle. There is a walkable passage beside the table, **suitable for a semi-circular camera move
> around the meeting table.** The projection screen may show abstract diagrams but **no readable text.**"*

**Four rules hiding in that prompt:**
1. **Empty the scene of people** — the space is generated separately from the characters
2. **Design the space to SUPPORT the intended camera move** — name the move inside the scene prompt
3. **Nine angles in one image** = one generation, nine consistent references
4. **No readable text** — matches our Bank 9 never-render-text law ✓ (independent confirmation)

## ⚡ THE TIMESTAMPED BLOCKING DIAGRAM

They storyboard action as a **top-down map with numbered positions mapped to video seconds**:
```
glass meeting-room outer wall · trajectory: centre gets surrounded
6-8s   pull back / encirclement      9-11s  right-side pincer
12-15s table-edge suppression, wind down
"black dots = attacker key positions; numbers = seconds in the video"
```
**This is a floor plan with a clock on it.** Our Director works in shot lists; this adds *spatial
staging over time* — which is exactly what multi-character scenes need and what we've never had.

---

## HOW THIS PLUGS INTO OUR SYSTEM

**New Phase 1.5 — ASSET BUILD (between DECIDE and BUILD):**
```
1. CHARACTER  → four-view sheet of the KOL (front/side/back/3-4) in ONE image
                → replaces re-uploading 3 loose photos and hoping
2. EXPRESSION → 3×3 grid of the KOL's emotions from the Emotion bank
3. SCENE      → 3×3 nine-grid of the location, EMPTY, designed around the planned camera move
4. BLOCKING   → top-down diagram, numbered positions ↔ timestamps (multi-character only)
5. Feed the asset images as references into the multi-shot generation (file 17)
```

**What it fixes, specifically:**
| Our known problem | Fixed by |
|---|---|
| Identity drift across 9 shots | four-view + expression assets |
| Scene/lighting drift between shots | nine-grid scene asset |
| The phrasing trap (empty frame 1) | an asset image IS the `start_image` |
| Vague blocking in multi-person shots | timestamped blocking diagram |
| Re-uploading KOL photos every session | one four-view sheet, stored |

**Cost:** image generations are cheap (~0.12–low credits) versus 45–135 per video generation.
**Building assets first is the cheapest insurance in the whole system.**

## THE ORDER (do not reorder)
```
1. Strategist decides the concept        (free)
2. ASSET BUILD — images only             (cheap)
3. Multi-shot video generation FROM assets (the expensive step, now de-risked)
4. Edit
```

> **The Line:** stop prompting for consistency. Build it, then reference it.
