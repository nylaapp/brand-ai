# PAGE-AUDIT.md: the shared client file

One living file per site, written by `page-audit` and read by the skills that act on its
recommendations: `page-update`, `page-build`, `page-verify` and `page-ship`, reached through
`page-content-studio` when a request spans jobs. It holds the brief, what was observed, the gap report and the
recommendation rows with their status, so the next skill starts from evidence instead of
asking again. A re-audit updates it; it never starts over.

## 1. Find or create it

Check, in order, and stop at the first confirmed match:

1. The project root or working folder, then subfolders up to three levels.
2. The folder where `BRAND.md` was found (see `intake.md`).
3. The central brand directory: `$BRAND_AI_HOME/brands/<slug>/`, or
   `~/.brand-ai/brands/<slug>/` when the variable is unset.

**Confirm the match.** The front matter `site` must match the store being audited. A file
for another store counts as missing. More than one match at the same level: stop and list
the paths.

**If none exists**, create it from `audit-template.md` at the end of the audit and save it in
the first location that has `BRAND.md`; otherwise in the central brand directory (create the
folder if needed). Tell the person the path. Never overwrite an existing file without reading
it first.

## 2. Front matter

```yaml
---
page_audit_schema: 1.0
site: <domain>
brand: <name>
brand_md_revision: <rev | none>
last_audit: <YYYY-MM-DD>
playbook: <date of references/page-type-playbook.md, or plugin version>
theme_tested: <theme id and name, role: draft | preview | live>
pages: [<page keys audited>]
audited_by: page-audit <plugin version>
---
```

## 3. Sections

| # | Section | Owner |
|---|---|---|
| 1 | Brief: goal, audience, change appetite, hard limits, business type, assumptions made (one block per page) | `page-audit` |
| 2 | Observation log: viewports, dates, theme id confirmed, overlays seen and when, what could not be observed and why | `page-audit` |
| 3 | Gap report: one table per page with every check's ID, status, evidence and grade | `page-audit` |
| 4 | Recommendations: the ranked rows with IDs and statuses | `page-audit` writes; acting skills change only status |
| 5 | Out of scope and handed off: rows owned by someone else, with what to ask them | `page-audit` |
| 6 | Questions open for the person | `page-audit` |
| 7 | Changelog: one line per audit or status change, newest first | any skill that edits the file |

## 4. Recommendation rows

Columns: `ID`, page, part of the page, playbook check (ID and grade), what could improve,
numbers and source, why, impact, effort, owner of the fix, on-goal or off-goal, finding or
suggestion, `status`, baseline number to re-check.

- **IDs are stable.** Format `<PAGE>-<NN>` with `HOME`, `LAND`, `COLL`, `PROD`, `ABOUT`,
  `CONTACT`, `FAQ`, `POLICY`, `LOC`, `SVC`, `CART`, for example `HOME-03`. Number in order of
  first appearance. Never renumber or reuse an ID, even when a row is closed.
- **Status values:** `open`, `picked` (the person chose it), `done` (acted on and verified),
  `parked` (chosen to leave for later), `handed-off` (someone else owns the fix).
- **Effort:** S is a setting value, a link change or reordering sections. M is a new setting,
  a small section change or a section with new content. L is a new section type or a new
  page structure.
- **Impact:** high, medium or low from how close the part is to the page's primary action and
  how many visitors reach it; say "unknown" when there is no traffic data.

## 5. Update rules

- **Re-audit:** re-observe the page, update section 2 and the gap report, keep every ID and
  its status, mark a row `done` only when the check now passes on the render, add new rows
  with new IDs, and add a changelog line. Do not edit a row's history; if a check changed
  grade or wording in the playbook, note it in the changelog.
- **Acting skills** (`page-update`, `page-build`, `page-verify`, `page-ship`) change a row's `status` to
  `picked` or `done`, add the verification result to the changelog, and touch nothing else.
- **Older or foreign files:** if a file exists without these sections, keep its content,
  append the sections below it, and never renumber its existing IDs.
- **Never write** passwords, tokens, customer personal data or analytics identifiers beyond
  what a public page already shows. Screenshots and HAR files stay in the scratch folder.
- If the person declines to save a file, give the same content in chat and say it was not
  saved.
