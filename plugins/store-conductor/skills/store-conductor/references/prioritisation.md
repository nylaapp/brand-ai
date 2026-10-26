# Prioritisation: what is best for this store, and in what order

A ranking aid built from the client's goals and the audits' evidence. It is a house rule of thumb
(grade H): it orders the work, it doesn't predict results. Say so when you present it, and show
the scores so the client can disagree with them.

## Score

For each open row:

```
score = goal fit x evidence strength x impact / effort
```

| Factor | Scale |
|---|---|
| **Goal fit** | 3 serves the top-ranked client goal directly, 2 serves another stated goal, 1 is useful but off the stated goals, 0 serves nothing the client asked for |
| **Evidence strength** | 3 observed and tied to an A-grade check or a measured number, 2 grade B practitioner guidance, 1 grade H or unmeasured |
| **Impact** | 3 high, 2 medium, 1 low (from the source; "unknown" counts as 1 and is shown as unknown) |
| **Effort** | 1 is S (a setting, a link, a reorder), 2 is M (a new setting, a small section change, new content), 3 is L (a new section type or page structure) |

Show the four numbers beside each row. A row scoring 0 on goal fit is listed under "worth
knowing" and never scheduled unless it unblocks something that serves a goal.

## Vetoes (a row is not scheduled)

- It would break a **hard limit** the client set. Name the limit in the row.
- It needs a **brand fact or claim** that isn't in the brand files, until `brand-capture` or
  `content-fact-check` has settled it.
- Its **owner is outside the theme**: it is `handoff`, reported, not scheduled.
- Its **evidence is stale** (see `sources.md`): schedule the audit that refreshes it, not the fix.

## Promotions (these go first regardless of score)

- **Foundation:** missing brand files block all copy work.
- **Trustworthy measurement:** if tracking is unknown or broken, tracking audit and fix come before
  work whose success will be judged by conversion numbers.
- **Blocking dependencies:** a section that other rows need, an audit a build row is waiting on.
- **A near client date:** work that serves a launch or season within the next batch window; and
  defer risky structural work close to a date.

## Sequence

1. Foundation (brand files, then competitors if the goal needs them).
2. Evidence that gates decisions (page audit of key pages, tracking audit, claim checks).
3. Builders in dependency order: section, then page, then content.
4. Verify each change on the rendered page.
5. Ship to the draft theme; the client reviews.
6. Only then, ask for an explicit approval to go live.

Within a step, order by score. Read-only audits may run in parallel; anything that writes to a
theme runs alone.

## Batches

- At most five rows per batch, one page or one theme area per batch, so a regression is traceable
  to a small set of changes.
- Match batch size and cadence to the client's effort budget and approver turnaround. A "careful"
  client gets smaller batches and fact-checks before every publish; a "fast" client gets larger
  batches with the same verification.
- Roadmap columns: **Now** (the approved batch), **Next** (the following one or two batches,
  scored but not approved), **Later** (everything else open, plus "worth knowing").
- Every batch lists what it needs from the client (an image, a decision, an approval, an export)
  so nothing starts blocked.

## Presenting the plan

A plain-language table per batch: row, what changes, owner skill, goal fit and score, why it is in
this order, what it needs from the client. Then one sentence on what is deliberately not scheduled
and why (vetoed, handed off, off-goal, waiting on evidence). Ask for approval of the first batch.

## Re-ranking

Re-score on every re-plan. Keep IDs and statuses; only order and batch membership change. A row
that was verified stays `done` unless new evidence shows it regressed, in which case add a new row
that references the old one.
