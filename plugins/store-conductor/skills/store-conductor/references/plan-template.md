# STORE-PLAN.md template and readout format

Copy the skeleton when creating the file (rules in `plan-file.md`). Delete sections that don't
apply yet; keep placeholders only where a fact is genuinely unknown.

## File skeleton

````markdown
---
store_plan_schema: 1.0
site: <domain>
brand: <name>
brand_md_revision: <rev | none>
last_plan: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
draft_theme: <id, name, role>
live_theme: <id, name>
sources_read: []
approvers: []
planned_by: store-conductor <version>
---

# <Brand>: store plan

> What this file is: the ranked plan for the store, built from the client's goals and the audits.
> It orders work and records what was done. Changes are made by the specialist skills, on a draft
> theme, and nothing goes live without a recorded approval.

## 1. Client need
- Goals (ranked): 1) <goal> (<number>) 2) ... 3) ...
- Must not change: <hard limits>
- Approvers: <who>, turnaround <days>. Effort budget: <batches per month>. Dates: <...>.
- Risk tolerance: <standard | careful | fast>. Refresh cadence: <...>.
- Assumed (no answer given): <...>

## 2. Evidence inventory
| Source | Status | Path | Date | Theme observed | Stale? |
|---|---|---|---|---|---|

## 3. Backlog
| ID | Source ref | Lane | What | Owner skill | Goal fit | Grade, type | Impact | Effort | Score | Depends on | Status | Baseline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 4. Roadmap
**Now: <batch name>** (needs from the client: <...>)
| ID | Change | Owner skill | Why this order |
|---|---|---|---|

**Next:** <rows, scored, not approved>
**Later:** <rows, plus worth knowing>

## 5. Dispatch log
| Date | Specialist | Rows | Brief | Result | Verified how | Status set |
|---|---|---|---|---|---|---|

## 6. Decisions and approvals
| Date | Decision | Approved by | Where given |
|---|---|---|---|

## 7. Handed off
| ID | Owner | Observed | What to ask |
|---|---|---|---|

## 8. Open questions
- <question>

## 9. Changelog
- <YYYY-MM-DD>: store-conductor <version>. <plan created; n rows; batch 1 proposed>.
````

## Readout to the person (chat)

Plain words, in this order:

1. **What I used:** the goals and limits, which evidence exists and how old it is, and which
   specialist skills were available (and which weren't).
2. **The plan:** the first batch as a table (change, owner skill, goal fit and score, why it is
   first, what it needs from you), then the next one or two batches in a line each.
3. **What is deliberately not scheduled and why:** vetoed by a limit, handed to someone else,
   off your goals, or waiting for evidence.
4. **What needs someone else:** store settings, apps, off-site pages, with who and what to ask.
5. **What I need from you now:** the approval for batch one, plus any missing input.
6. **Where the plan is saved,** and when I would re-plan.

After a batch: what changed, how it was verified at desktop and mobile, what was flagged and not
done, the baseline number to re-check and when, and a clear statement that nothing is live yet
unless an approval is recorded.

Say that the ranking is a judgement about order, not a forecast of results.
