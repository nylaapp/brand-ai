# Accessibility lane

Target: **1.00 on every page, mobile and desktop, on the local dev server.** Don't stop at
"improved". Fixes are additive only (`SKILL.md` section 0).

Measure on the local dev server (`SKILL.md` step 3a). The preview domain injects Shopify's
preview-bar iframe, which always fails `frame-title` and can't be fixed in the theme.

From `lh_summary.mjs`, take `failing.accessibility`: every audit with a score below 1 and a
weight above 0, with its elements (selector, snippet, explanation, label). The score alone isn't
actionable.

## 1. Classify every finding into exactly one bucket

### Skip (report with evidence, don't fix)

- `frame-title` on the preview-bar iframe: Shopify's own bar, only on the preview domain.
- Elements that come from outside the theme: third-party popups, marketing or chat widgets, or
  markup from another site. Before calling something third-party, confirm all three: (1) searching
  the theme's files for the element's class or attribute finds nothing; (2) the element is absent
  from a normal authenticated page load (it only appears in Lighthouse's fresh crawl); (3) the
  page's script list (`Array.from(document.scripts).map(s=>s.src)`) includes a known third-party
  tool. Owner: the app, through its settings or its support.
- Merchant content the theme only renders (for example a `heading-order` failure from an `<h4>`
  inside a product description). If the flagged text isn't in the repo it's live store data: flag
  it for the owner. Don't reformat it or globally renormalise rich-text headings.

### Fix, choosing the technique deliberately

| Finding | Safe fix | Do not |
|---|---|---|
| `aria-prohibited-attr` (an `aria-label` on a bare `<div>`) | add the correct `role` (often `role="status"` for a loading placeholder) | remove the label |
| `aria-required-children` (a `role="tablist"` whose children lack `role="tab"`) | add `role="tab"` and `aria-selected` where the buttons are created; first check sibling components (near-identical dot or pagination components often exist) and match whichever already does it right | change the container role |
| `link-name` or `button-name` (icon or image only) | a visually-hidden text span (copy the pattern the theme already uses, for example in its product card) or an `aria-label` mirroring the text a hidden or responsive state would show | add visible text, change the icon |
| `link-name` from a blank dynamic setting (`<a href="tel:">`) | guard the block: `{% if block.settings.number != blank %}` | fill in placeholder text, delete the merchant's empty block |
| `image-alt` on a theme-coded image | `alt="{{ image.alt | escape }}"`, or `alt=""` when the image is decorative | invent alt text for a merchant image (that's content: flag it) |
| `color-contrast` | measure first (`contrast.md`), then nudge by the minimum; reuse a "muted but legible" opacity the theme already uses before computing a new value | guess, round up "to be safe" (that's a style change), or edit a shared colour-scheme token globally |

If a fix touches a shared token, don't edit the token unless every usage is checked. Scope an
override to the flagged selector instead.

## 2. Contrast

Muted text is usually alpha-blended (`opacity`, `rgb(var(--color-foreground-rgb) / X%)`,
`color-mix(...)`) over a scheme-dependent background. The number in the CSS says nothing about
rendered contrast. Use `contrast.md`: sanity-check against the report's own numbers, find the
smallest opacity that clears the threshold with headroom (4.5:1 for normal text, 3:1 for large
text), check every colour scheme the component can render in, and verify on the live page.

## 3. Prove nothing visibly moved

After the re-run (`SKILL.md` step 7):

- Blank-value guard: every real (non-empty) instance keeps the same `innerText` and the same count
  as before.
- Label or role: image source, position and size unchanged; only accessibility-tree attributes
  changed.
- Contrast: visible text and position unchanged; only the colour moved, by the computed minimum.

If any page or form factor isn't 1.00, return to section 1 for what remains.
