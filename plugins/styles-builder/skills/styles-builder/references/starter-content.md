# Optional: starter content and section styling

Two optional steps for a new theme whose pre-built section templates still carry the theme's demo look.
Both are off unless the user asked for them in Step 0, and each can run alone. Both work on the theme settled in Step 0 (`theme-target.md`): a draft is recommended, and the live theme
needs the assurance described there.

## Before either one
In Step 0, ask: do you want (a) brand placeholder images (taken from the images already in the store's
Files, unless you say to use others), (b) brand styling on the existing section templates, and which
templates (for example home, product, collection, page, blog, article, cart, search). Anything not named
is left alone. Pull the latest theme and baseline each template you will touch (section order, section
heights, total height, the `theme check` count, and copies of the files) so the change can be proved and
reverted.

## 7a. Brand images as placeholders

Replace the starting theme's demo placeholders with the images already in the store's Files, so pages look
like the brand from the first build. The store's Files are the default source: use them unless the user
stated other images (step 2).

1. **Inventory.** For each named template, list every image setting and whether it is blank (the theme
   shows a built-in placeholder), holds a demo image, or holds a chosen image. Only blank and demo ones are
   candidates. **Never replace an image the client chose.**
2. **Source: the store's Files first.** Use the images already in the store's Files (a read-only
   listing: the connected store's files query, or Content, Files in the Admin), unless the user stated
   other images. If they did, the images or source they named replace the Files for the settings they
   cover: files they supplied, or the brand's own live site (only for images the client owns). Never
   stock images, never images from another brand or site, and never reach for another source on your
   own: if the Files hold nothing that fits a setting, leave it blank, say so, and offer the options
   (they send images, or allow the live site).
3. **Choose from the Files.** List what is there (file name, dimensions, where it is already used) and
   match each blank or demo setting to the best fit. Skip logos, icons, screenshots, documents, videos
   (unless the setting takes a video), images too small for the setting, and images that clearly belong
   to a different product or brand. Reuse an image across settings only when the Files hold too few, and
   say so in the table. Never rename, move or delete a file in the Files.
4. **Rights and honesty.** These are placeholders, not final art. An image already in the store's Files
   is the client's own (it was uploaded to their store), so its rights are taken as confirmed. For
   anything else, if rights aren't confirmed, leave the picker blank and say so. Never invent product
   shots or people.
5. **Upload gate.** Setting an image that is already in the Files uploads nothing: it changes only the
   theme setting, so no upload yes is needed. Image pickers take files from the Files area, so placing
   an image the user named that isn't there yet means uploading it: a store-level change. Do it only
   with the user's explicit yes naming the files, source, sizes and rights, one batch at a time.
6. **Fit.** Pick images that suit the aspect ratio in `design.md` for that use (hero, card, gallery). Add
   alt text that describes the image, and don't crop away the subject.
7. **Show first.** A table: template, section, setting, what is there now, the image proposed, its source
   ("store Files: <file name>", or what the user named) and rights. Get a yes, then set only those settings,
   using the same reference format the theme already uses for a chosen image.
8. **Record** each placement in `design.md` under "Placeholders": image, where used, source, rights, approver.
9. **Verify** on the rendered theme at desktop and mobile: images load, nothing is badly stretched or
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
place an image from outside the store's Files unless the user named it. Do not rename, move or delete a
file in the Files. Do not replace a chosen image. Do not touch templates the user didn't name. Do not
change copy, section order or section count. Do not edit or push to the live theme without the yes before
the edit and again before the push (`theme-target.md`).
