# CRO-AUDIT.md template and update rules

Write in the project root (or where the person names). If the file exists, update it: keep resolved
rows marked `Done` with the date, mark rows that no longer apply `Gone`, add new rows with the next
number, and bump `runs_completed`. Quick audits fill sections 1 to 8; full audits fill all of them.
Skipped sections stay in the file with "Not run: <reason>".

```
---
cro_audit_schema: 2.0
brand: <name from BRAND.md or "not provided">
scope: <page URL, or "store main path">
mode: <quick | full>
conversion: <what counts>
segments_considered: [<device, source, new/returning ... or "none given">]
last_run: <YYYY-MM-DD>
runs_completed: <n>
streams: {technical: done|partial|not run, heuristic: ..., competitive: ..., analytics: ..., behavioural: ..., voice-of-customer: ..., user-testing: ...}
next_review: <last_run + about 3 months>
analyzed_by: cro-audit 0.2.0
---

# <Brand>: CRO audit (<date>)

> What this is: <one line saying which streams ran and which kinds of evidence back it. State plainly
> that heuristic and measured findings show likely friction, and only analytics, behavioural and test
> evidence show what visitors did.>

## 1. Summary
- The goal and the one primary action assumed or confirmed.
- The three to five things that matter most, one line each, with evidence tags and confidence.
- What was not done.

## 2. Data validity (full audits)
The checks from `analytics-analysis.md` section 1 and their results, so readers know how far to trust
section 6.

## 3. Findings (ranked)
| ID | Bucket | Evidence | Confidence | Where | What we saw | Principle or number | Why it likely matters | Fix or next step | Owner | Impact | Effort | Score | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Bucket: Just do it, Instrument, Investigate, Test or Hypothesize. Evidence is one or more of Heuristic,
Measured, Reported, Behavioural, Customer voice, Survey, Test. Confidence is High, Medium or Low
(`prioritization.md` section 3). Score is from `scripts/prioritize.py` and the method is named in
section 8. Owner is one of: this theme, store admin, store settings, an installed app, images and
media, a third-party embed, content (copy), the person.

## 4. Technical and speed
Mobile and desktop: LCP, INP or TBT, CLS, lab vs. field labelled, the top opportunities with owners,
browser and device issues found.

## 5. Heuristic and mobile review
Failed checks (from `heuristics-checklist.md` and `mobile-checklist.md`) and a one-line list of passed
checks. Competitive comparison (`competitor-benchmark.md`) if run.

## 6. Analytics (full audits)
Funnel tables by segment from `scripts/funnel.py`, the source and date range, the largest leak by
segment, small-sample flags. Marked Reported.

## 7. Behavioural, customer voice, surveys and user testing
What each stream found, with the sample size ("seen in 9 of 24 recordings", "5 participants"), the
themes with counts and quotes, and the stream's limits. For a stream prepared but awaiting data, attach
the instrument (survey questions, test script, recording plan) and say what to send back.

## 8. Prioritisation
The method (ICE or PIE) and the inputs; the ranked list from `scripts/prioritize.py`; the bucket for
each item.

## 9. Experiment roadmap
For each Test item: the hypothesis (`experiment-design.md`), primary and guardrail metrics, the
sample size and duration from `scripts/sample_size.py`, feasibility, and the order to run in. For items
that can't be tested at the available traffic, the alternative.

## 10. Quick wins (Just do it)
The short list that can be fixed now with the owner of each. Offer to hand rows to `page-edit-content`,
`page-edit-design`, `page-create` or `fact-check`.

## 11. Open questions
What still needs data or research, phrased as questions, and which stream would answer each.

## 12. What this audit did not do
Every skipped stream or check and why (no data supplied, no browser, quota, not run).
