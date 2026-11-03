# CRO-AUDIT.md template and update rules

Write in the project root (or where the person names). If the file exists, update it: keep
resolved rows marked `Done` with the date, mark rows that no longer apply `Gone`, add new
rows with the next number, and bump `runs_completed`.

```
---
cro_audit_schema: 1.0
brand: <name from BRAND.md or "not provided">
scope: <page URL or "store main path">
conversion: <what counts>
last_run: <YYYY-MM-DD>
runs_completed: <n>
evidence_used: [heuristic, speed, mobile, funnel, customer-voice]   # only those actually run
next_review: <last_run + about 3 months>
analyzed_by: cro-audit 0.1.0
---

# <Brand>: CRO audit (<date>)

> What this is: an expert and measurement review with no analytics tool connected. It shows
> likely friction and measured problems. It does not show what visitors did.

## Top five
1. **CRO-01** <one line> `[Heuristic]` impact High, effort Low
...

## Findings
| ID | Evidence | Where | What we saw | Principle or number | Why it likely matters | Fix | Owner | Impact | Effort | Status |
|---|---|---|---|---|---|---|---|---|---|---|

Evidence is one of Heuristic, Measured, Reported, Customer voice. Owner is one of: this theme,
store admin, store settings, an installed app, images and media, a third-party embed, content
(copy), the person. Impact and effort are High, Medium or Low, with the reason in the
"Why" or "Fix" cell. Rank by impact first, then effort.

## Speed
Mobile and desktop: LCP, INP or TBT, CLS, with lab vs. field labelled, and the top
opportunities with owners.

## Mobile pass
Rows from the mobile checklist that failed, with measured sizes.

## Funnel (if numbers were given)
The table from funnel.py, the source and date range given, the small-sample flag, and the
two leaks. Marked Reported.

## Customer voice (if REVIEW-MINING.md exists)
Top themes tied to page elements, with the mention counts that file reports.

## Passed checks
One line.

## Test ideas (hypotheses, not findings)
| Idea | Why we think so | What would confirm it | Metric |

## Open questions for behavioural data
What session recordings, scroll maps or a funnel report would answer that this audit cannot.

## What this audit did not do
List the streams skipped and why (no numbers given, no browser, no review file, network
blocked).
```
