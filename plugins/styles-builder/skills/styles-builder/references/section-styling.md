# Optional: brand styling on existing section templates

One optional step for a new theme whose pre-built section templates still carry the theme's demo look. It is
off unless the person said yes in the opening questions (Step 0 in `SKILL.md`) or asked for it in the
request, and it is offered once, at the start, never later in the run. It works on the theme settled in
Step 0 (`theme-target.md`): a draft is recommended, and the live theme needs the assurance described there.

It changes how the sections look, never what they say or show: no copy, no images, no section order or
count. Those are other jobs (`page-edit-content` for words, images and links, `page-edit-design` for order
and layout, `page-create` for new sections).

## Before it
The opening questions in Step 0 ask, in the same message as the theme: do you want brand styling on the
existing section templates, and which templates (for example home, product, collection, page, blog,
article, cart, search). Anything not named is left alone, and nothing is asked again here. When the run
reaches this step, pull the latest theme and baseline each template you will touch (section order, section
heights, total height, the `theme check` count, and copies of the files) so the change can be proved and
reverted.

## Brand styling on existing section templates

Apply the brand's spacing, colour schemes, corner radius, padding and widths to the sections already in the
named templates.

1. **Inventory.** For each section, list the styling settings it exposes (colour scheme, top and bottom
   padding, gap, width, height, corner radius where offered) and their current values.
2. **Map from `design.md` only.** Use its section padding (desktop and mobile), container widths, scheme
   roles and radius scale. Where `design.md` has no value, leave the section alone and say so. Never invent one.
3. **Existing settings only.** No new settings, no markup or CSS changes, no change to the order or count of
   sections, and no copy or image changes: those are other jobs.
4. **Show first.** A before and after table for every section changed. Get a yes per template, then apply.
5. **Verify per template** at desktop and mobile: no overflow or clipped text, contrast per scheme (text on
   background and on buttons), every section's height compared with the baseline and each difference
   explained, and the `theme check` count unchanged.
6. **Revert** is always available: restore the baseline copies for the template and push only those files.

## Never
Do not touch templates the user didn't name. Do not change copy, images, section order or section count.
Do not edit or push to the live theme without the yes before the edit and again before the push
(`theme-target.md`).
