# VLOG — analysis of your 6 references
### Measured from the files. Snapshot 2026-07-30, expires 2026-09-28.

---

## PROFILE (n=6)

| metric | median | range |
|---|---|---|
| cuts/min | **40.3** | 18.5 – 63.9 |
| median shot | **1.13s** | 0.60 – 2.51 |
| longest shot | 3.31s | 2.42 – 7.37 |
| **blended transitions** | **0%** | 0 – 28 |
| BPM | 104.6 | 83 – 176 |
| LUFS | −21.4 | −37.0 – −9.0 |
| true peak | −4.4 | |
| black point | **10.0** | |
| saturation | **74.5** | |

Shot-length distribution:

```
                          <=1s   1-2.5s   >2.5s   fastest
7577468220488060174        26       3       2      0.17s
7622675185858055431        16       0       3      0.03s
7608221210291342614         9       5       2      0.40s
7631383112307461396         6      10       0      0.46s
7632719636974341390         1       7       1      0.30s
7178823736408280325         0       3       3      2.00s   <- the outlier
OUR KK v3                   0       ~9      ~4     1.20s
```

Five of six lean on sub-second shots. **Ours has none.**

---

## THE FINDING THAT MATTERS MOST: the two pillars are different grammars

I had been treating "vlog" and "car cinematic" as the same craft with different footage.
The measurements say otherwise.

| | car cinematic (n=5) | vlog (n=6) | what it means |
|---|---|---|---|
| median shot | **0.77s** | **1.13s** | car cuts ~45% faster |
| **blended transitions** | **27%** | **0%** | **car edits are designed; vlogs are cut** |
| black point | **2.0** | **10.0** | car crushes blacks; vlog keeps them open |
| saturation | **91.5** | **74.5** | car is punchier; vlog is flatter and more natural |
| sub-bass share | 60–92% | see below | car is bass-dominated |

**The single biggest divergence: blended transitions.** 27% in car edits, **0% in five of six
vlogs.** Vlogs are almost entirely hard cuts — no wipes, no masks, no ramps. The energy comes
from *cut rate* and *content*, not from designed transitions.

That is the opposite of what I assumed. I built one transition philosophy and would have
applied whips and masks to a travel vlog, where the references say plainly: don't.

**Second divergence: the grade.** Car edits crush to black point 2 and push saturation to 91.
Vlogs sit at black point 10 and saturation 74 — lifted, flatter, more natural. Applying a
car-edit grade to a vlog would look wrong, and vice versa.

---

## vs OUR KK VLOG

| | references | our KK v3 |
|---|---|---|
| median shot | **1.13s** | ~2.0s |
| cuts/min | 40.3 | 25.8 |
| shots ≤1s | 6–26 per video | **0** |
| blended | 0% | 0% ✓ |

**We're about 2× too slow.** The one thing we got right by accident: zero blended transitions
is *correct* for this pillar. Our failure there was the Crown, not the KK video.

---

## CAVEATS — stated so the numbers aren't over-trusted

1. **n=6.** Medians are indicative, not statistical. The range column matters more than the
   median on several rows.
2. **All re-downloaded** through snaptik/ssstik, which re-encode. **LUFS is unreliable**
   (range −37 to −9 is implausibly wide for published content) and high-frequency content may
   be rolled off. Cut timing, shot length and grade survive re-encoding; loudness does not.
3. `7178823736408280325` is an outlier on every axis (18.5 cuts/min, 2.51s median, −37 LUFS).
   It pulls medians down. Worth you telling me whether it's a different sub-format.
4. Blended-transition detection is a frame-difference heuristic — it catches wipes and fades
   reliably, but a very fast whip can read as a hard cut.

---

## WHAT TO CHANGE FOR THE VLOG PILLAR

| # | change | evidence |
|---|---|---|
| 1 | **median shot 2.0s → 1.1s** | their median; ours is ~2× slower |
| 2 | **include sub-second shots** | 5 of 6 references have 6–26 of them; we have 0 |
| 3 | **keep hard cuts — do NOT add masks/wipes here** | 0% blended in 5 of 6 |
| 4 | **lift the grade**: black point ~10, saturation ~75 | ours is car-graded |
| 5 | bed around 100 BPM | median 104.6 |

---

### Both profiles written. `qc.py` can now gate a build against its own pillar's numbers
### instead of against my assumptions.
