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

## On the connector route

When `setup-check.md` chose the connector route (`connector-route.md`: no Shopify CLI, no local
copy of the theme), the rules above still hold, and three things differ.

**1. The rendered checks run after the write, on the draft.** There is nothing to render on this
computer first. The order is: pre-write checks (below), write to the draft (`ship-to-draft.md`),
then every check in section 3 on the draft's preview address. A draft is private, so visitors never
see the change while it is checked. "Verified before the push" cannot hold for the rendered checks
on this route, so don't say it: say "checked on the draft after it was written."

**2. Pre-write checks are source checks, and they are not verification.** Run them on the files in
`work/` before anything is written, and record them as one line ("Pre-write checks: ...") in the
change pack's section 3, never as passes in section 5:

- the files in `work/` differ from `baseline/` only as sections 3 and 4 of the change pack say;
- every JSON file parses, and every setting value is inside its schema's min, max or options;
- the approved copy appears exactly as approved, and no placeholder text is left unless meant;
- every colour, font and size traces to `design.md` or the theme settings;
- new copy that makes a claim has been through `fact-check`;
- the guards in `ship-to-draft.md` sections 2 and 3 passed.

Any failure goes back to the editing step before the write.

**3. Check 8 (`theme check`) is "Can't tell".** The code checker is part of the Shopify CLI. Record
"Can't tell: the code checker needs the Shopify CLI", in the baseline too. The plan step tells the
person once, and their agreement is the "reason the person accepted" that lets the change go on.
Shopify's own refusal of a bad file (the `userErrors` of the write) and the pre-write JSON and range
checks cover part of what it would have caught; say that it is only part. A baseline captured
without the checker can't prove the count didn't grow, so never write "theme check unchanged".

A failed rendered check means the draft is **not ready**: fix it with the same guards or revert
(`revert-mode.md`). The live theme was never touched.

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
| 8 | `theme check` | Run it on the working copy (connector route: it can't run; see above) | The offense count is not higher than the baseline's (connector route: "Can't tell") | all |
| 9 | Accessibility basics | One h1, no skipped heading levels, icon-only controls have names, images have alt text, tap targets meet the threshold the playbook states, contrast per colour scheme | No new problem versus the baseline; list any that were already there | all |
| 10 | New page or section: editor behaviour | Add, remove, reorder and duplicate the new sections in the theme editor; empty fields; a very long heading | Controls work and layout holds. "Can't tell" if there is no editor access | create |
| 11 | No new overlay or console error from the change | Overlays at 1 s and about 15 s; browser console | Nothing new that the change caused | all |
| 12 | Values come from the spec | Compare changed colours, fonts and sizes with `design.md` or the theme settings | Every value traces to the spec; none invented | design, create |

A baseline captured at different widths than you can observe makes a check "Can't tell"; say which.

## 4. Record and report

Write section 5 of the change pack: each check, its result, number and viewport. Then report in
plain words:

- **Verdict:** safe to put on the target theme, or not, and why. (Connector route: it is already
  on the draft; "safe" means ready to leave there and offer for publishing, "not safe" means fix
  or revert.)
- **The numbers:** before and after for the changed thing, the section inventory result, the
  `theme check` count, and anything "Can't tell" with its reason.
- **What it does not prove:** that the change will improve results, and anything not observable
  (analytics, other devices).

Any failed check makes the verdict **not safe**. List exactly what failed and return to the editing
step. Never ship a change whose verdict is not safe.

## 5. Move on

| Verdict | Next |
|---|---|
| Every check passed, or "Can't tell" with a reason the person accepted | Ship to the target theme (`ship-to-draft.md`). Connector route: the files are already on the draft, so go on to the log (`ship-to-draft.md` section 7) |
| A check failed | Back to the editing step with the failing check and numbers |
| The baseline is stale, or the theme was edited in the admin | Re-capture the baseline, then verify again |
