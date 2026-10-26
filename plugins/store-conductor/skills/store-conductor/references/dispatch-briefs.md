# Dispatching a specialist

How to hand a row to another skill and check what comes back. The conductor invokes specialists
with the Skill tool; it never does their work, answers their questions for the person, or edits
files itself.

## Rules for every dispatch

- **One writer at a time.** A skill that can write to a theme or store runs alone. Read-only skills
  (audits, research) may run together. Before dispatching a writer, confirm no other write-capable
  skill is mid-run on the same theme.
- **Target a draft or preview theme**, named by ID and role in the brief. Never the live theme.
- **Pass pointers, not secrets.** File paths, IDs, goals and limits only. Never a password, token,
  cookie, API key or customer data.
- **Pass only approved rows.** Say which row IDs are approved and that nothing else may change.
- **Let the specialist run its own steps and gates.** If it asks the person something, relay the
  question; don't answer it.

## Context pack (fill in; send as the specialist's instructions)

```
Store: <site>  Brand: <name>
Brand files: <paths found, with tier>  (BRAND.md rev <n | none>; design.md: <path | none>)
Plan: <path to STORE-PLAN.md>  Batch: <Now batch name>
Goal(s): <ranked goals, with numbers if any>
Audience / change appetite: <...>
Must not change: <hard limits, one per line>
Target theme: <id, name, role: draft | preview>   Live theme (do not touch): <id>
Approved rows: <SP-IDs with source IDs, e.g. SP-004 (PAGE-AUDIT HOME-01)>
Baselines to carry: <metric = value (source, date, device)>
Evidence files to read first: <PAGE-AUDIT.md, ANALYTICS.md, ...> and their dates
Do not: edit anything outside the approved rows; go live; type credentials; skip verification.
Report back: what changed (files, settings), what was verified and how, what was flagged and not
done, anything needing the client or another owner, and the row status you recommend.
```

## Per-specialist brief notes

| Specialist | Add to the pack | Read back |
|---|---|---|
| `brand-capture` | The site URL, who answers the client questions | Paths of the brand files written, open questions, `next_review` |
| `competitor-research` | Competitor names already in `BRAND.md` | `COMPETITORS.md` path and date, openings it found |
| `page-audit` | The page, the goal, the limits; "read-only" | `PAGE-AUDIT.md` path, counts, the ranked rows with owners |
| `page-content-studio` | Row IDs from `PAGE-AUDIT.md` marked `picked`, the target theme, the baseline | Files changed, verification result, `theme check` before and after, QA log entry, row set to `done` |
| `analytics-audit`, `analytics-setup`, `analytics-cleanup`, `analytics-guardrails` | Site URL, access level available, whether a tag manager export exists | `ANALYTICS.md` updates, findings with severity, what the owner must change |
| `accessibility-audit` | The draft theme, the page list | Before and after scores, items skipped and why, what needs the store owner |
| `content-fact-check` | The copy and where it will appear | Claim-by-claim verdicts, safer rewrites, anything unverifiable |
| `shopify-blog-writer`, `shopify-blog-rewrite`, `shopify-blog-autopilot` | Brand files, intent, topic or source, delivery as a hidden draft | The draft's location, SEO fields, claims flagged, the fact-check result |
| `content-seo-audit` | The published URL | Findings and the two-week and four-week tracking dates |

## Acceptance: what to check before updating a row

A row is `done` only when all of these hold for its specialist's result:

1. The specialist says it finished that row, and says what it did and what it did not do.
2. For any change to a page or theme: it was **verified on the rendered page** at desktop and
   mobile, nothing else visibly moved, and the `theme check` count did not grow.
3. Only approved rows were touched; nothing outside the target theme changed; the live theme is
   untouched.
4. Any claims it introduced were checked (`content-fact-check`) or taken from the brand files.
5. Its own file or log (`PAGE-AUDIT.md`, `ANALYTICS.md`, the QA log) shows the same status.
   If they disagree, the specialist's file wins; record the drift in the plan.

If any check fails, set the row `blocked` or back to `approved` with the reason, and tell the
person. Never mark it `done` to keep the plan tidy.

## Failure handling

| What happened | Do |
|---|---|
| The specialist is blocked on access (password, sign-in, quota) | Record `blocked` with the reason and what the person must do; don't work around it and don't pass credentials |
| It reports it cannot fix the row in the theme | Re-route the row to `handoff` with its observation and who acts |
| It changed something outside the approved rows | Stop, tell the person exactly what changed, and recommend restoring the draft to its baseline before continuing |
| Verification shows a regression | Set `blocked`, keep the evidence, and hand the regression back to the same specialist or to a rollback of the draft |
| Two specialists' findings conflict | Present both with their grades and sources and ask the person which to follow |
