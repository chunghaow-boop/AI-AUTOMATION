# CREATOR MECHANISMS — what the top performers actually do
### Candidate file 30. Feeds Phase 1 (banks) and the pacing gate. Platforms: FB · TikTok · IG.
### Formats: VLOG · CAR REVIEW · INDUSTRY VALUE. Target: 50%+ retention, 30s–2min.

---

## ⚠️ HONESTY FIRST — what this is and isn't

You asked me to study the **top 100 creators**. I did not, and cannot, do that empirically:
their retention curves are private analytics, and the platforms cannot be scraped. A ranked
"top 100" table with invented numbers would be worthless and would poison every downstream
decision.

**What this is instead:** documented, sourced mechanisms from published 2026 platform research
and creator analysis — converted into **measurable rules** the automation can enforce. Every
number below traces to a source. Where something is my inference, it says so.

**To make it empirical:** drop creator video URLs into `intel.py`. `video_analysis_create`
breaks each one down scene-by-scene, and the mechanisms bank fills with *observed* patterns
instead of reported ones. That is the honest path to "study the top 100" — one at a time,
starting with the 10 that matter most to you.

---

## ⚠️ YOUR TARGET, CALIBRATED

"50% retention, 30s–2min" is two different problems:

| Length | 2026 benchmark | Your 50% target is… |
|---|---|---|
| 30s | 50–60% (TikTok) | **at par** — achievable |
| 60s | 40–50% | **above par** — strong |
| 2 min | 30–40% | **top-tier** — exceptional |

**A 90s Reel with high completion outperforms a 3-min Reel every time.** The rule from the
research: *design around a target retention curve, not a target length.* If your 30-second
retention is below 70%, fix the intro before touching anything else.

**Implication for your formats:** vlog and industry-value should target **60–90s**, not 2 min,
until the curve proves it can hold. Length is earned by retention, not chosen up front.

---

## PLATFORM MECHANICS (they are NOT the same)

| | Facebook Reels | Instagram Reels | TikTok |
|---|---|---|---|
| Reach model | pushes **beyond followers** — best cold reach | relevance + cultural fit; small accounts can pop | interest graph, fastest cold start |
| Top signal | comments-between-people (friend-to-friend) | **DM sends per reach** ⭐ + watch time + likes | completion rate + rewatch |
| Your avatars | 2 & 3 (Family Upgrader, Resale Uncle) | 1 & 4 | 1 & 4 |
| Best window (MY) | 6–9pm weekdays, 9pm peak | 6–9pm | 6–11pm; **Sat is TikTok's best, FB's worst** |

**The biggest CTA change:** on Reels, **DM sends are the most heavily weighted distribution
signal.** Your CTAs currently optimise for comments. At least one CTA per video should be
engineered for a *send* — "send this to the friend who's about to overpay for a recond."

**Originality penalty:** original content gets 40–60% more distribution than reposts, and
accounts posting 10+ reposts in 30 days are excluded from recommendations entirely.

---

## THE STRUCTURE ALL THREE FORMATS SHARE

```
HOOK       0–3s    open loop: promise, curiosity, or a surprising visual. MOTION in frame 1.
VALUE DROP 4–15s   pay something immediately — don't make them wait for the whole payoff
PAYOFF     16–45s  deliver the hook's specific promise. Vague payoff = wasted-time feeling
CTA        last 5s one ask, engineered for a SEND on Reels / a comment war on FB
```
Pattern interrupt every **30–60s**: B-roll cutaway, zoom punch-in, text pop, angle switch,
music shift. Resets attention before the drop happens.

## PACING TARGETS BY FORMAT (now enforced by `tools/pacing.py`)

| Format | cuts/min | max shot | why |
|---|---|---|---|
| **Vlog** | **15–25** | 3.0s | highest cut rate of any format; jump-cuts kill dead air |
| **Car review** | 8–15 | 6.0s | education tolerates +5–10s shots; needs proof time |
| **Industry value** | 6–12 | 8.0s | B2B: proof-driven hook, on-screen data, slower is fine |
| Hero cinematic | 10–30 | 4.0s | motion-led |

**Vary the rate — don't hold it constant.** Fast during energy, slow on the important beat.
A flat rhythm reads as monotony; `pacing.py` flags cut-rate standard deviation <0.6.

## WHY THE TOP CREATORS HOLD ATTENTION (mechanisms, not vibes)
- **Authenticity beats polish.** Phone-shot, native-feeling content outperforms studio work —
  which is exactly why your "phone + second-hand Myvi" concept is on-strategy.
- **Information density**, not length. Douyin's shift: audiences will watch longer *if* density
  is high. Dead air is the enemy, not duration.
- **Save-worthy content** triggers the collection/save signal: checklists, inspection points,
  price ladders. Your pillars #5 (Check Before You Buy) and #2 (RM___ Gets You) are built for it.
- **Open loops.** The brain seeks closure — a promise made in the hook and paid specifically.
- **Face = trust.** You cannot AI-generate trust. In vlog and review, Nev on camera IS the
  product; AI serves as B-roll only. (Already your Mode B/C doctrine — the research agrees.)

---

## FIRST REAL MEASUREMENT — `INFLUENCER_v1.mp4`
```
format hero · 30.1s · cuts/min 6.0 (target 10-30) · variation 0.82 (ok) · hook motion 2.20 (ok)
longest shot 15.1s · estimated retention 44%  ->  SEND BACK: "CUTS TOO SLOW"
```
**The finding that matters:** the Seedance multi-shot prompt explicitly asked for *"smooth
seamless transitions between every shot — no hard cuts."* That is cinematic grammar, and it is
**working against short-form retention.** Dissolves are gentle; hard cuts are what create the
pattern interrupt that resets attention. For FB/TikTok/IG, cut hard.

**Detector limitation (stated, not hidden):** the cut detector is histogram-based, so it sees
hard cuts and misses slow dissolves. On dissolve-heavy footage the true visual-change rate is
higher than the 6.0/min reported. The *conclusion* still holds — dissolves don't interrupt a
scroller the way a cut does — but the number understates the edit. A gradual-transition
detector is the next upgrade.

**Action:** stop asking Seedance for seamless dissolves on short-form. Ask for distinct shots
and cut them hard in the edit, on the beat.

---

## WHAT THIS CHANGES IN THE AUTOMATION
1. `pacing.py` enforces per-format cuts/min, dead zones, interrupt gaps, structure — before you see it.
2. Prompt template (file 17) drops "no hard cuts" for short-form; hard cuts become the default.
3. CTA bank gains a **DM-send** variant per video, not just comment-bait.
4. Length is a *result*: start 60–90s, extend only when the curve earns it.
5. `intel.py` watchlist = the real "study the top creators" engine. Feed it URLs.

## THE HONEST BOTTOM LINE
Every retention number in this system is still **engineered-for, not measured.** Nothing has
been posted. The estimate in `pacing.py` is a structural heuristic and says so in its own
output. One posted video with a real 24-hour curve is worth more than every prediction here.
