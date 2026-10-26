---
name: page-verify
description: >-
  Check a Shopify page change on the rendered page, not the code: that the thing asked for really
  changed or exists, that nothing else moved, and that nothing broke. Loads the page on the target
  theme at desktop and mobile, compares it with the baseline captured before the edit (section
  positions and heights, total height, heading outline, tracked links, theme check count),
  re-runs the accessibility basics, and writes the results into the change pack. Also works on a
  change someone else made, by capturing the current state as a new baseline. Use for "verify
  the change", "did anything else move", "check the draft before we push", "is this safe to ship",
  or after page-update or page-build. Read-only: never edits a theme or store. Not for deciding what
  to change (page-audit), making the change (page-update, page-build), pushing it (page-ship), or a
  full accessibility audit (accessibility-audit).
---

# Page verify

Prove a change did what it should and nothing else, by loading the rendered page. Reading the
source you just wrote is not verification. Read-only: it never writes to a theme or a store; its
only output is the verification section of the change pack and a short report.

```
1. Load the change pack -> 2. Observe the page, same way as the baseline ->
3. Run the checks -> 4. Record the result -> 5. Hand on or hand back
```

## Rules

- **Read-only.** Never edit a theme file or push. If something is wrong, report it and hand it
  back; don't fix it here.
- **Rendered, not source.** A check passes only from what loaded on the target theme. If the page
  can't be loaded, the check is "Can't tell", never a pass.
- **Same method as the baseline.** Same viewports, same recipes, same theme id, so numbers are
  comparable (`../page-audit/references/observation-recipes.md`).
- **Never type a password or credential** for the person. Follow the blocked-access table in the
  recipes; if the storefront is locked, ask the person or use a local preview.
- **A failure is a result, not an obstacle.** Report it with the numbers; don't soften it or
  re-run until it passes.
- **Don't invent a baseline.** If there isn't one, say so (see step 1).

## Who this is for

Usually a Site Editor, not a developer. Report in plain words ("the booking button now sits in the
first screen; every other section is exactly where it was"), show the numbers, and say clearly
whether it is safe to move on.

## 1. Load the change pack

Find the change pack for this change (format and rules in
`references/baseline-and-change-pack.md`). Read the request, the target theme, the baseline and
the files touched. Confirm the pack is current: its theme id matches, and the working copy
matches sections 3 and 4.

No change pack (a change made by someone else, or by hand)? Say so, capture the **current state**
as a baseline now using the same table, and tell the person what that means: you can prove the
change works and that nothing is broken now, but you can't prove nothing moved earlier. Ask what
the change was meant to be.

## 2. Observe the page

Load the target theme's page at desktop (1440x900) and mobile (375x812) following the recipes: a
real viewport, the theme id confirmed, a slow scroll for lazy content, overlays noted. Confirm you
are on the target theme, not the live one.

## 3. Run the checks

For each, record the result, the number or evidence, and the viewport.

| # | Check | How | Pass when |
|---|---|---|---|
| 1 | The change exists on the render | Find the exact thing the pack says changed (text, link, section, position) | It is there, as intended, at both widths |
| 2 | Nothing else moved | Compare the section inventory and total height with the baseline | Every other section's top and height match; the total changed only by what the change should cause |
| 3 | Tracked links unchanged | Compare the link map for the links in scope | Same destinations and labels as the baseline, unless the change was meant to alter one |
| 4 | Other breakpoints and colour schemes | Check at the widths and schemes the change can reach (for example tablet, and any scheme the section offers) | No overflow, overlap or clipped text |
| 5 | `theme check` | Run it on the working copy | The offense count is not higher than the baseline's |
| 6 | Accessibility basics | One h1, no skipped heading levels, icon-only controls have names, images have alt text, tap targets meet the threshold the playbook states, contrast per colour scheme | No new problem versus the baseline; list any that were already there |
| 7 | New page only: editor behaviour | Add, remove, reorder and duplicate the new sections in the theme editor; empty fields; a very long heading | Controls work and layout holds. Mark "Can't tell" if there is no editor access |
| 8 | No new overlay or console error from the change | Overlays at 1 s and about 15 s; browser console | Nothing new that the change caused |

A baseline that was captured at different widths than you can observe makes a check "Can't tell";
say which.

## 4. Record the result

Write section 5 of the change pack: each check with its result, number and viewport. Then report
in plain words:

- **Verdict:** safe to ship, or not, and why.
- **The numbers:** before and after for the changed thing, the section inventory result, the
  `theme check` count, and anything marked "Can't tell" with its reason.
- **What it does not prove:** that the change will improve results, and anything not observable
  (analytics, other devices).

If any check failed, set the verdict to **not safe to ship** and list exactly what failed.

## 5. Hand on or hand back

| Verdict | Next |
|---|---|
| Every check passed or "Can't tell" with an accepted reason | `page-ship` pushes the touched files to the draft theme |
| A check failed | Back to `page-update` or `page-build` with the failing check and numbers; nothing ships |
| The baseline is stale or the theme changed in the admin | Re-capture the baseline, then re-verify |

## Checklist before finishing

- [ ] Change pack found and current, or a new baseline captured and its limits explained
- [ ] Target theme id confirmed; live theme not used
- [ ] Desktop and mobile both observed with the same method as the baseline
- [ ] Every check has a result, a number or evidence, and a viewport
- [ ] No check passed without a rendered load; "Can't tell" used where it couldn't be observed
- [ ] Section 5 of the change pack written; nothing else edited
- [ ] Verdict given plainly, with what it does and doesn't prove
