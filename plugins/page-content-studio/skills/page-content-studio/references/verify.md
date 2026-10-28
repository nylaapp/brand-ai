# Verify: prove the change on the rendered page

The shared verification step. `page-create`, `page-edit-content` and `page-edit-design` run it
themselves after editing, and the front door runs it when someone only wants an existing change
checked. It writes nothing to a theme; its only output is section 5 of the change pack and a short
report.

Reading the source you just wrote is not verification; loading the rendered page is.

## Rules

- **Rendered, not source.** A check passes only from what loaded on the target theme. If the page
  can't be loaded, the check is "Can't tell", never a pass.
- **Same method as the baseline:** same viewports, same recipes, same theme id, so numbers are
  comparable (`../../page-audit/references/observation-recipes.md`).
- **Never type a password or credential** for the person. Follow the blocked-access table in the
  recipes; if the storefront is locked, ask the person or use a local preview.
- **A failure is a result, not an obstacle.** Report it with the numbers; don't soften it or re-run
  until it passes. Fix it in the editing step, then verify again.
- **Don't invent a baseline.** With no change pack, capture the current state now and say what that
  can't prove (see below).

## 1. Load the change pack

Read the request, target theme, baseline and files touched (format and rules in
`baseline-and-change-pack.md`). Confirm the theme id matches and the working copy matches sections
3 and 4. No change pack (a change made by someone else, or by hand)? Say so, capture the **current
state** as a baseline now, and tell the person that you can prove the change works and nothing is
broken now, but not that nothing moved earlier. Ask what the change was meant to be.

## 2. Observe the page

Load the target theme's page at desktop (1440x900) and mobile (375x812): a real viewport, theme id
confirmed, a slow scroll for lazy content, overlays noted. Confirm the page reports the target
theme's id. If the target is the live theme, say so; observing it is read-only and changes nothing.

## 3. Run the checks

Record each result with the number or evidence and the viewport. "Applies" says which skill must
run it; "all" means every change.

| # | Check | How | Pass when | Applies |
|---|---|---|---|---|
| 1 | The change exists on the render | Find the exact thing the pack says changed (text, link, image, section, position) | It is there as intended at both widths | all |
| 2 | Nothing else moved | Compare the section inventory and total height with the baseline | Every other section's top and height match; the total changed only by what the change should cause | all |
| 3 | Tracked links unchanged | Compare the link map for links in scope | Same destinations and labels, unless the change was meant to alter one | all |
| 4 | Links and images work | Load each link you changed or added; check each image loaded | Links resolve (not a 404); images load with alt text present | content, create |
| 5 | Words as intended | Read the text from the rendered DOM | Matches the approved copy exactly; no placeholder text left unless it was meant to stay | content, create |
| 6 | Other breakpoints and colour schemes | Check tablet and each colour scheme the section offers | No overflow, overlap or clipped text | design, create |
| 7 | Shared code | For a change to a shared section or style, check every other page that uses it | Those pages unchanged, or changed only as agreed | design |
| 8 | `theme check` | Run it on the working copy | The offense count is not higher than the baseline's | all |
| 9 | Accessibility basics | One h1, no skipped heading levels, icon-only controls have names, images have alt text, tap targets meet the threshold the playbook states, contrast per colour scheme | No new problem versus the baseline; list any that were already there | all |
| 10 | New page or section: editor behaviour | Add, remove, reorder and duplicate the new sections in the theme editor; empty fields; a very long heading | Controls work and layout holds. "Can't tell" if there is no editor access | create |
| 11 | No new overlay or console error from the change | Overlays at 1 s and about 15 s; browser console | Nothing new that the change caused | all |
| 12 | Values come from the spec | Compare changed colours, fonts and sizes with `design.md` or the theme settings | Every value traces to the spec; none invented | design, create |

A baseline captured at different widths than you can observe makes a check "Can't tell"; say which.

## 4. Record and report

Write section 5 of the change pack: each check, its result, number and viewport. Then report in
plain words:

- **Verdict:** safe to put on the target theme, or not, and why.
- **The numbers:** before and after for the changed thing, the section inventory result, the
  `theme check` count, and anything "Can't tell" with its reason.
- **What it does not prove:** that the change will improve results, and anything not observable
  (analytics, other devices).

Any failed check makes the verdict **not safe**. List exactly what failed and return to the editing
step. Never ship a change whose verdict is not safe.

## 5. Move on

| Verdict | Next |
|---|---|
| Every check passed, or "Can't tell" with a reason the person accepted | Ship to the target theme (`ship-to-draft.md`) |
| A check failed | Back to the editing step with the failing check and numbers |
| The baseline is stale, or the theme was edited in the admin | Re-capture the baseline, then verify again |
