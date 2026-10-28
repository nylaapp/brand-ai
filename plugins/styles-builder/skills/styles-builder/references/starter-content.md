# Optional: starter content and section styling

Two optional steps for a new theme whose pre-built section templates still carry the theme's demo look.
Both are off unless the user asked for them in Step 0, and each can run alone. Both work on the theme settled in Step 0 (`theme-target.md`): a draft is recommended, and the live theme
needs the assurance described there.

## Before either one
In Step 0, ask: do you want (a) brand placeholder images, (b) brand styling on the existing section
templates, and which templates (for example home, product, collection, page, blog, article, cart, search).
Anything not named is left alone. Pull the latest theme and baseline each template you will touch (section
order, section heights, total height, the `theme check` count, and copies of the files) so the change can
be proved and reverted.

## 7a. Brand images as placeholders

Replace the starting theme's demo placeholders with the brand's own images, so pages look like the brand
from the first build.

1. **Inventory.** For each named template, list every image setting and whether it is blank (the theme
   shows a built-in placeholder), holds a demo image, or holds a chosen image. Only blank and demo ones are
   candidates. **Never replace an image the client chose.**
2. **Source, in order:** images the client supplied; images already in the store's Files (a read-only
   listing); the brand's own live site, only with the user's permission and only for images the client
   owns. Never stock images, and never images from another brand or site.
3. **Rights and honesty.** These are placeholders, not final art. If rights aren't confirmed, leave the
   picker blank and say so. Never invent product shots or people.
4. **Upload gate.** Image pickers take files from the store's Files area, so placing an image can mean
   uploading it: a store-level change. Do it only with the user's explicit yes naming the files, source,
   sizes and rights, one batch at a time.
5. **Fit.** Pick images that suit the aspect ratio in `design.md` for that use (hero, card, gallery). Add
   alt text that describes the image, and don't crop away the subject.
6. **Show first.** A table: template, section, setting, what is there now, the image proposed, its source
   and rights. Get a yes, then set only those settings.
7. **Record** each placement in `design.md` under "Placeholders": image, where used, source, rights, approver.
8. **Verify** on the rendered theme at desktop and mobile: images load, nothing is badly stretched or
   cropped, and section heights match the baseline unless a new image legitimately changed one (say which).

## 7b. Brand styling on existing section templates

Apply the brand's spacing, colour schemes, corner radius, padding and widths to the sections already in the
named templates.

1. **Inventory.** For each section, list the styling settings it exposes (colour scheme, top and bottom
   padding, gap, width, height, corner radius where offered) and their current values.
2. **Map from `design.md` only.** Use its section padding (desktop and mobile), container widths, scheme
   roles and radius scale. Where `design.md` has no value, leave the section alone and say so. Never invent one.
3. **Existing settings only.** No new settings, no markup or CSS changes, no change to the order or count of
   sections, and no copy changes: those are other jobs.
4. **Show first.** A before and after table for every section changed. Get a yes per template, then apply.
5. **Verify per template** at desktop and mobile: no overflow or clipped text, contrast per scheme (text on
   background and on buttons), every section's height compared with the baseline and each difference
   explained, and the `theme check` count unchanged.
6. **Revert** is always available: restore the baseline copies for the template and push only those files.

## Never
Do not upload to the store's Files without an explicit yes naming file, source, size and rights. Do not
place an image the client didn't supply or approve. Do not replace a chosen image. Do not touch templates
the user didn't name. Do not change copy, section order or section count. Do not edit or push to the live theme without the yes before the edit and again before the push (`theme-target.md`).
