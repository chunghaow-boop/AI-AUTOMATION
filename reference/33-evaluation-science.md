# HOW PROFESSIONALS ACTUALLY SCORE AI SYSTEMS
### File 33. The field is called **LLM-as-a-Judge**. It is well studied, and some of its
### findings contradict what we built in files 25 and 26. Evidence cited throughout.

---

## ⚠️ THE HEADLINE FINDING — IT CHALLENGES OUR DEBATE PROTOCOL

You asked: *"is it through AI debating?"* Professionals tried that. The research says:

> **"Debate frameworks amplify biases sharply after the initial debate, and this increased bias
> is sustained in subsequent rounds, while meta-judge approaches exhibit greater resistance."**
> — *Judging with Many Minds* (arXiv 2505.19477)

**Multi-agent debate — file 25's core mechanism — can make evaluation worse, not better.**
More rounds of argument don't converge on truth; they entrench whichever bias got in first.
A **meta-judge** (one evaluator reviewing independent, non-interacting assessments) resists bias
better than agents arguing with each other.

This does not mean file 25 was wrong to demand specific objections instead of "looks good."
That part is solid. What's unsupported is the belief that **more rounds of debate = better verdict.**

---

## ⚠️ A DESIGN FLAW IN OUR TOURNAMENT (file 25 / log #40)

Our tournament instructs each seat to propose three options:
> *"A the obvious (generated only to be KILLED — it's the benchmark, not a candidate) …
> C wins most often; if A survives, the seat didn't try."*

**That is designed-in bias, and the research has a name for it.** Identity/label bias: when
proposals carry identities, judges score the label, not the content. The mitigation is
**anonymisation** — *Measuring and Mitigating Identity Bias in Multi-Agent Debate via
Anonymization* (arXiv 2510.07517).

We pre-committed the verdict before seeing the content. If the obvious option is genuinely the
best one for a given title, **our protocol structurally cannot select it.** "C wins most often"
isn't a finding — it's an instruction we gave ourselves.

**Fix:** strip the A/B/C identities. Present three unlabelled candidates in randomised order.
Remove "A must lose" entirely. If the obvious option wins on merit, that is a valid result.

---

## THE KNOWN BIASES (all four apply to us)

| Bias | What it does | Our exposure |
|---|---|---|
| **Self-preference** | a model rates its own output higher | **maximum** — every seat, judge and proposal is generated and scored by one model |
| **Position** | favours whichever option appears first/last | tournament + swipe-file comparisons |
| **Verbosity** | longer = better, regardless of quality | our prompts run to 3,500 chars |
| **Bandwagon** | agrees with the apparent consensus | 13 seats "agreeing" in sequence |

> *"Self-assessment can amplify internal biases due to alignment or instruction tuning…
> external LLM-as-a-judge can provide more objective evaluations."*

**The uncomfortable implication:** a system where one model proposes, defends, judges, and scores
is the maximum-self-preference configuration. That is our current architecture.

---

## WHAT THE PROFESSIONALS ACTUALLY DO

### 1. Pairwise where you're choosing; pointwise where you're monitoring
- **Pointwise** (score /10) is *less stable* — it needs a consistent internal scale that models
  don't reliably have. Use it for **regression testing and monitoring** (has quality dropped
  since last version?).
- **Pairwise** ("is A better than B?") is more reliable for **choosing** between candidates —
  which prompt, which hook, which cut.
- Caveat worth knowing: pairwise preferences flip in **35%** of cases when a distractor feature
  is introduced, vs **9%** for absolute scores. Neither is clean; use the right one per job.

**For us:** hook selection, prompt variants and cut choices should be **pairwise**. The /60 and
/100 scorecards should be kept for **tracking quality over time**, not for picking winners.

### 2. Position-consistency checking
Run every pairwise comparison **twice with the order swapped**, then average. If the winner flips
when you swap the order, the comparison carried no signal. Free, and it directly measures noise.

### 3. Anchored few-shot rubrics
Pin scores to concrete examples rather than adjectives. This is the standard fix for scale drift —
and it's what makes a rubric reproducible.

### 4. DAG / binary decomposition
Break a subjective /10 into a tree of **binary** sub-decisions ("does frame 1 contain motion?
yes/no"). Binary questions are far more reliable than a 10-point scale.
**Our hard gates already do this** — that instinct was correct and should be extended, not the
scored seats.

### 5. Chain-of-thought before the verdict
Force explicit reasoning *before* the score. Reasoning-then-score materially outperforms
score-then-justify (arXiv 2509.13332).

### 6. Ground truth beats every judge
All of the above are proxies. The field's ground truth is **human preference and real outcomes**.
For us that is the 24-hour retention curve. Nothing above replaces it.

---

## WHAT THIS CHANGES IN OUR SYSTEM

| Current | Change to | Why |
|---|---|---|
| debate rounds until resolution (25) | **meta-judge**: independent assessments, one reviewer | debate amplifies bias |
| A/B/C labels, "A must lose" | **anonymised, randomised order** | identity bias, pre-committed verdict |
| pointwise /10 to pick winners | **pairwise to pick, pointwise to monitor** | pointwise scales are unstable |
| single-pass comparison | **swap order, run twice** | position bias is measurable and free to remove |
| adjective rubrics ("fresh for 2026") | **anchored to named videos** | stops scale drift |
| more seats = more confidence | **one mind counted 13 times** | self-preference is our largest exposure |

## THE HONEST SUMMARY
- **Debate is not the professional answer.** It was tried; it amplifies bias. Meta-judging,
  anonymisation, pairwise selection, binary decomposition and anchored rubrics are.
- **Our biggest structural exposure is self-preference**, because one model does everything.
  The cheapest real mitigation available to you is *you* — your thumb on a pairwise A/B is an
  genuinely external signal, which is exactly what RUNNER 9b's hook test already asks for.
- **Every method above is a proxy for the real score**, which is what the audience does.

## SOURCES
- *Judging with Many Minds: bias amplification in multi-agent LLM-as-judge* — arXiv 2505.19477
- *Measuring and Mitigating Identity Bias in Multi-Agent Debate via Anonymization* — arXiv 2510.07517
- *Pairwise or Pointwise? Evaluating Feedback Protocols* — arXiv 2504.14716
- *Explicit Reasoning Makes Better Judges* — arXiv 2509.13332
- *Split and Merge: Aligning Position Biases in LLM-based Evaluators* — arXiv 2310.01432
- DeepEval, Confident AI, Cameron R. Wolfe — LLM-as-a-Judge practitioner guides
