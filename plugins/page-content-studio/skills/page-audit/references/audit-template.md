# PAGE-AUDIT.md template and readout format

Copy the skeleton below when creating the file (rules in `audit-file.md`). Keep placeholders
only where a fact is genuinely unknown, and delete sections that don't apply yet.

## File skeleton

````markdown
---
page_audit_schema: 1.0
site: <domain>
brand: <name>
brand_md_revision: <rev | none>
last_audit: <YYYY-MM-DD>
playbook: <date or plugin version>
theme_tested: <id, name, role>
pages: [homepage]
audited_by: page-audit <version>
---

# <Brand>: page audit

> What this file is: the evidence and ranked recommendations for the pages listed above.
> It reports what was observed on <date>; it does not prove what will improve results.
> Changes are made by page-create, page-edit-content and page-edit-design (each verifies and
> pushes to a draft theme itself), never by this audit.

## 1. Brief
**Homepage**
- Goal: <book / sell / promote / trust / inform / fix>. Audience: <...>. Open to: <small tweak / refresh / rebuild>.
- Must not change: <hard limits>. Business type: <catalog / service / both>.
- Assumptions made (no answer given): <...>

## 2. Observation log
| Date | Page | Viewport | Theme id confirmed | Overlays seen (1 s / 15 s) | Could not observe, and why |
|---|---|---|---|---|---|

## 3. Gap report
**Homepage** (Pass n, Partial n, Missing n, Can't tell n)
| Check | Status | What was observed | Viewport | Grade |
|---|---|---|---|---|

## 4. Recommendations
| ID | Page | Part | Playbook check | What could improve | Numbers (source) | Why | Impact | Effort | Owner | Goal fit | Type | Status | Baseline to re-check |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 5. Out of scope and handed off
| ID | Owner | What was observed | What to ask them |
|---|---|---|---|

## 6. Questions
- <question>

## 7. Changelog
- <YYYY-MM-DD>: page-audit <version>. <homepage audited; n rows opened>.
````

## Readout to the person (chat)

Short, plain words, in this order:

1. **Assumptions and scope:** the goal, audience, change appetite and limits used, and the
   theme and viewports observed. Say which answers were assumed.
2. **Result:** the page's counts (Pass, Partial, Missing, Can't tell).
3. **The top rows** (about five) as a table: part, playbook check with grade, what was
   observed, owner, effort, finding or suggestion. Then "also noticed" in one line each.
4. **Not observed and why:** blocked access, quotas, missing analytics. Say which checks stay
   "Can't tell".
5. **Recommendation:** which rows to take first and why, which need a decision or another
   owner, and what can't be fixed in the theme.
6. **Where the file is** and the next skill to run for rows they pick.

Never present a suggestion as a finding, and quote research with its source and date.
