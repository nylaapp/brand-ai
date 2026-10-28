# Logo and favicon

## What to collect
- **Logo files:** the primary logo and, if the brand uses a light version on dark backgrounds (a
  transparent header over a dark hero, a dark footer), an inverse logo. Best source first: files from the
  client or the brand book package; then the brand's own live site, with the user's permission to download
  it (the client's own logo, named by file, source and size).
- **Display size:** measure the logo's rendered height on the live site at desktop and mobile, and set the
  theme's logo height settings from those numbers.
- **Brand rules:** minimum size and clear space, if the brand book states them. Record them in `design.md`.
- **Favicon:** a square mark. Sources agree on a square PNG at least 32 by 32 pixels, but Shopify's own help
  centre is the authority: check its current requirement, and say so if you couldn't. Use the logo mark,
  not the full wordmark, unless the wordmark is already square.

## Format
- Use the logo as supplied. A vector is crisp at any size if the theme editor accepts it; if you can't
  confirm that, use a PNG at twice the display height. Never redraw, recolour or "tidy up" a logo.
- If only a low-resolution copy exists, say so and ask for a better file. Never rebuild a logo from a
  screenshot.

## Getting it into the theme
Logo and favicon settings are image pickers, and an image picker can only point at a file in the store's
**Files** area. So:
1. Check Files for an existing upload (read-only).
2. If there is none, there are two routes: the user uploads it in the theme editor, or, with their explicit
   yes naming the file, source, size and rights, you upload it to Files. Uploading is a store-level change.
3. Set the picker settings on the theme settled in Step 0 (`theme-target.md`), and set the logo heights from the measured numbers.
4. If the theme falls back to a file in its own assets when no logo is set, that is a repo choice: follow
   the repo's rules and note it in `design.md`. Don't add a fallback of your own.

## Verify
On the chosen theme's preview, fresh load, desktop and mobile: the logo renders at the measured height with no
layout shift, the inverse logo shows where it should, and the favicon appears in the browser tab. Browsers
cache favicons, so check in a fresh private window. Record file names, dimensions, source and rights in
`design.md`.
