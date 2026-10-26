# STORE-PLAN.md: the shared plan file

One living file per store, written by the conductor. It records the client's needs, the evidence
inventory, the unified backlog, the roadmap in batches, every dispatch, and every approval. A
re-plan updates it; it never starts over.

## 1. Find or create it

Check in order, first confirmed match wins:

1. The project root or working folder, then subfolders up to three levels.
2. The folder where `BRAND.md` or `PAGE-AUDIT.md` was found.
3. The central brand directory: `$BRAND_AI_HOME/brands/<slug>/`, or `~/.brand-ai/brands/<slug>/`
   when the variable is unset.

The front matter `site` must match the store being planned; a file for another store counts as
missing. More than one match at the same level: stop and list the paths. If none exists, create it
from `plan-template.md` next to `PAGE-AUDIT.md` (or `BRAND.md`), else in the central directory,
and tell the person the path. Never overwrite an existing file without reading it.

## 2. Front matter

```yaml
---
store_plan_schema: 1.0
site: <domain>
brand: <name>
brand_md_revision: <rev | none>
last_plan: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
draft_theme: <id, name, role>
live_theme: <id, name>
sources_read: [<file: date>, ...]
approvers: [<names or roles>]
planned_by: store-conductor <plugin version>
---
```

## 3. Sections

| # | Section | Contents |
|---|---|---|
| 1 | Client need | Ranked goals with numbers, hard limits, approvers and turnaround, effort budget, dates, risk tolerance, cadence; assumptions marked "assumed" |
| 2 | Evidence inventory | Each source: found or missing, path, date, theme observed, stale or fresh |
| 3 | Backlog | Unified rows (below) |
| 4 | Roadmap | Now, Next, Later, each batch with the rows, what it needs from the client, and entry and exit conditions |
| 5 | Dispatch log | One line per handoff: date, specialist, row IDs, brief sent, result, verification, resulting status |
| 6 | Decisions and approvals | Who approved what and when, with a pointer to where it was given in chat. Every go-live approval is recorded here |
| 7 | Handed off | Rows owned by store settings, apps or off-site pages: observation, owner, what to ask |
| 8 | Open questions | For the client |
| 9 | Changelog | Newest first; one line per plan, dispatch result or status change |

## 4. Backlog rows

Columns: `ID`, source reference, lane, what, owner skill, goal fit, evidence grade and
finding or suggestion, impact, effort, score, depends on, `status`, baseline to re-check.

- **IDs are stable:** `SP-001`, `SP-002`, in order of first appearance. Never renumber or reuse,
  even when a row is closed or merged. A merged duplicate keeps its ID and points to the survivor.
- **Source reference** cites the specialist's own ID (`PAGE-AUDIT HOME-01`, `ANALYTICS F-014`) so
  the two files can be compared.
- **Status values:** `proposed`, `approved`, `in-progress`, `verifying`, `done`, `parked`,
  `handed-off`, `blocked` (with the reason in the row).

## 5. Who writes what

- The conductor writes every section. It changes a row to `in-progress` when it dispatches,
  `verifying` when the specialist reports, and `done` only after verification (see
  `dispatch-briefs.md`, acceptance).
- Specialists never edit this file. They report back; their own files (`PAGE-AUDIT.md`,
  `ANALYTICS.md`, the QA log) remain the source of truth for their rows.
- On disagreement, the specialist's file wins. Add a line to the changelog noting the drift and
  correct the plan.

## 6. Update rules

- **Re-plan:** re-read every source, update section 2, add rows for new findings with new IDs,
  mark rows `done` only from verification, re-score the open rows, re-cut the batches, and add a
  changelog line. Do not edit the history of a row.
- **Older or foreign files:** if a plan exists in another shape, keep its content, append these
  sections below it, and never renumber its IDs.
- **Never write** passwords, tokens, customer personal data or analytics identifiers beyond what a
  public page already shows. Screenshots and exports stay in the scratch folder.
- If the person declines to save the file, give the same content in chat and say it was not saved.
