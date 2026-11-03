# Prioritisation (stream 8)

Every issue ends up in one **bucket** (what to do) and gets a **score** (what first).

## 1. Buckets

| Bucket | Use when | Next step |
|---|---|---|
| **Just do it** | Clearly broken or clearly better, low risk, low effort (a broken link, an unreadable label, an oversized video, a missing alt, a duplicate script) | Fix directly; no test needed |
| **Instrument** | The question can't be answered because it isn't measured (no event on the booking button, a step with no data) | Add tracking first (`analytics-setup`) |
| **Investigate** | A leak is seen but the cause isn't known | More research: recordings, a survey, a test round |
| **Test** | There is a clear hypothesis backed by evidence, and the page has enough traffic (`scripts/sample_size.py`) | Design an experiment (`experiment-design.md`) |
| **Hypothesize** | An idea with only weak support so far | Keep on the list; gather evidence before building anything |

If traffic is too low to test, say so, move the idea to **Just do it** (if safe) or **Investigate**,
and prefer bigger changes and qualitative checks over a test that can never finish.

## 2. Score

Use `scripts/prioritize.py` on a JSON list of issues, ICE by default (impact, confidence, ease, each
1 to 10, averaged) or PIE (potential, importance, ease).

- **Impact or potential**: how many visitors it touches and how close to the conversion; the
  analytics leak sizes help.
- **Confidence**: how sure we are. Use `--evidence-confidence` so confidence follows the number of
  **different kinds** of evidence (one kind is low; three or more is high). Don't raise it on enthusiasm.
- **Ease**: effort and who can do it (this theme, an app, content, a developer).

State the scoring method and the inputs in the report so the ranking can be questioned. A score is a
way to order a list, not a measurement of value.

## 3. Rating each finding

Rate each finding's overall confidence:

- **High**: two or more different kinds of evidence agree, including at least one measured or
  behavioural source.
- **Medium**: one strong source (a measured problem, or a clear heuristic failure).
- **Low**: a single opinion or a small-sample observation with no second source.

Put High-confidence, high-impact, low-effort items at the top. Don't let a Low-confidence idea
outrank a High one because it sounds exciting.
