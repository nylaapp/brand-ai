# design.md template

design.md holds the brand's visual system as **actual values**: palette, type, spacing, corners, components, imagery,
the deep set below, and a value for every setting a Shopify theme needs (§12). It is always **complete**: however
little the site or brand book covers, a designer or the styles-builder skill can set up a whole theme from it.
It sits next to BRAND.md; BRAND.md's `design_doc: design.md` key and its Visual identity section point to it. It is
written so it still works from a blank theme or a design tool with none of the brand's CSS present. Where design.md
and BRAND.md disagree on a visual value, design.md wins; on names, voice and claims, BRAND.md wins.

**What goes here, and what doesn't.** Visual brand facts only. Naming, voice and claim rules stay in BRAND.md and
BRAND-VOICE.md. Build procedures, section-by-section theme instructions and QA logs are the project's own docs
(AGENTS.md, a QA log), not this file. Link them under Companions if they exist; never copy them in.

**Where values come from (best first).**
1. **Measured on the live site** with a browser tool, at 1440 and 390 wide: computed `font-size`, `line-height`,
   `letter-spacing`, `border-radius`, padding, colours and hover states read from real elements (a text fetch is
   not a measurement). Record the date and the viewport.
2. **The scan's `visual` block** (`colors_ranked`, `fonts_ranked`, `font_face_families`, `google_fonts`,
   `font_variables`) and `repo.shopify` theme settings (colour schemes, font settings). Theme settings are
   authoritative for colour roles when present.
3. **The site's CSS and screenshots**, read by eye for rules the numbers can't show (square vs rounded images, no
   shadows, band layout).
4. **A brand book's stated values** (hex, type, spacing, logo rules), labelled `(from brand book)`. These are stated,
   not measured. Where the live site measures differently, record both and ask which is current; with no site yet,
   they are the only source.
5. **Proposed**, only where none of the above covers a value: derived from the brand's own stated or measured values
   by the rules in §12, labelled `(proposed)`, with the reason in the same row ("H4: 24px, continues the 1.25 scale
   from the 16px body"). This is how gaps are filled; a table is never left with a blank.

**Complete, never invented.** Every value has an origin label, and a gap is filled with a `(proposed)` value, not left
out. A proposal is a design decision made for the brand, not a fact about it: it is never written as `(from brand
book)` or `(from site)`, never adds a colour outside the brand's palette, and never adds a font family the brand
didn't name or name as a fallback. What needs a file or a licence (logo, favicon, font files) can't be proposed: it
stays open, says what the theme uses meanwhile, and goes in BRAND-QUESTIONS.md (font licences especially: a font
named TRIAL or DEMO is a licence question, shown under Assets). All `(proposed)` values are listed once under Held
for later in BRAND-QUESTIONS.md as "Proposed design values", for the designer or approver to confirm.

**The deep set (always covered).** Every design.md brand-capture writes covers these, so a later skill never has to
go back and measure them. Each item is measured, `(from brand book)`, `(inferred)`, `(proposed)`, or said plainly to be
absent (for example "No animation", "no swatches"); an item is never silently skipped:
1. **Product, collection and cart pages:** layout measurements for each (section 7).
2. **Hover and focus states** for buttons, links, cards and inputs (sections 6 and 7).
3. **Input fields:** every property and state (section 6).
4. **Logo and favicon:** files, rendered heights, favicon links (section 9).
5. **Motion:** each effect, or an explicit "No animation" (section 6).
6. **Theme settings map:** a value for every Shopify theme settings group, including the full H1 to H6 scale (§12).
Palette, type, spacing, corners, components and imagery stay as before.

**Sizing.** Aim for 200 to 400 lines. Skip a section whose subject the brand doesn't have (a store with no
accordions has no Accordion entry). Keep every rule that a designer would otherwise get wrong: the counterintuitive
ones (what is rounded and what is square, what hover does, which family does which job) earn the most space.

**Origin labels** are the same as in BRAND.md. Use `(from site)` for measured values, `(from brand book)` for values a brand book states, `(inferred)` for what you conclude from them, and `(proposed)` for a gap filled by §12's rules (always with its reason);
`(client)` lines are never overwritten by a re-scan, and a confirmed proposal becomes `(client)`.

The front matter is flat `key: value` lines (no nesting, no quotes). Dates are `YYYY-MM-DD`.

---

```markdown
---
brand: <same as BRAND.md `brand`>
parent_doc: BRAND.md
status: <draft | approved, same as BRAND.md>
revision: <1, 2, 3 ... +1 on every write>
last_updated: <YYYY-MM-DD of the latest write>
measured: <YYYY-MM-DD and viewports, e.g. "2026-10-09 at 1440 and 390", or "not measured: scan CSS only", or "not measured: stated by the brand book (no live site)">
source: <e.g. "brand-capture scan of https://example.com plus browser measurement">
---

# <Brand> — Visual design guide

> **Brand facts live in `BRAND.md`** ... *(the standard pointer block, so an agent that opens only this file still
> finds BRAND.md. `scripts/link_brand.py` adds the same block to agent files.)*

<One paragraph: what this file is, that it works without the brand's own CSS, where the values were measured and when.>

**Companions:** <the project's own build or QA docs, if any, or delete this line>

---

## 1. The look
*Three to five lines: how the brand looks and feels in plain words (editorial, clinical, playful, quiet), the single
most recognisable visual signature, and what the brand never does visually (gradients, shadows, stock imagery).
Voice and positioning stay in BRAND.md; one line here is enough.*

## 2. Colour
| Name | Hex | RGB | Role / used for |
|---|---|---|---|
*Six to ten rows. Name each colour the way the brand would; give the role, not just the value. Add the theme's
scheme or token name in an extra column only when a theme is connected.*

**Rules** *(text colours per surface; whether colour arrives as whole bands or tinted cards; gradients, shadows and
overlays yes or no; the contrast target: 4.5:1 body, 3:1 large text and UI, in every background a section supports)*

## 3. Typography
| Family | Job |
|---|---|
*One row per family. If two families split content from interface, say so plainly: getting that backwards is the
commonest way to look off-brand while using the right fonts.*

| Role | Size / weight / line-height | Family | Notes |
|---|---|---|---|
*Always every level: H1, H2, H3, H4, H5, H6, body, small body, nav link, button label, eyebrow or label, caption, price.
Give size, weight, line height, letter spacing and case, at desktop and at mobile. A level the sources don't show
gets a `(proposed)` value from §12's type rules; never stop at the levels the brand book happens to show.*

**Rules** *(one H1 per page, never skip levels; heading and eyebrow casing; italics; a third typeface yes or no)*

## 4. Spacing and layout
*Container max width and side padding (desktop, mobile gutter); section rhythm (block padding desktop and mobile,
how adjacent bands meet); grid gaps; the breakpoints the site uses; minimum touch target 48×48px.*

## 5. Corners and borders
*State the rounding rule in one line, especially if it is specific (for example "interactive things are pills,
everything else is square"), then a table:*
| Element | Radius |
|---|---|
*Border width and colour, and whether shadows exist at all.*

## 6. Components
### Buttons
*State the governing hover rule first (for example "hover inverts, it never tints"). Then default and hover tables,
one row per variant that exists: fill, text, border, radius, padding, height; hover fill, text, border. Include
padding and font size, and say whether they change on hover. Add disabled, focus (ring, offset, `:focus-visible`
only) and motion (which properties animate, how long). If a measured hover state fails contrast on some surface,
say so and give the accessible variant.*

### Inputs
*Always. Background, text, border colour and width, radius, height and padding, placeholder colour, hover and
focus ring (`:focus-visible`), error state and label style, plus checkboxes, radios and selects if the brand styles
them. Measure on a real form (newsletter, search, cart note, account) at 1440 and 390.*

### Links, cards and focus
*Link default, hover and focus; product card hover (image, title, price, button); keyboard focus ring colour,
width and offset, and any surface where it fails contrast.*

### Motion
*Always. Each effect that exists (page transitions, card and image hover, button transitions, add-to-cart feedback,
scroll reveals, drawers) with where, the properties animated, duration and easing, and whether
`prefers-reduced-motion` is honoured. If the site has none, write "No animation" rather than leaving it out.*

### Navigation · Accordion · Badges
*Only those the brand uses. One short paragraph or table each, with real values. Third-party widgets that render
their own unbranded styles (a pop-up app, a reviews widget) are named as "not the brand's reference".*

## 7. Product, collection and cart pages
*Always, measured at 1440 and 390 on a real product, a real collection and the cart (a drawer, a page, or both).
Where a template doesn't exist, say so.*
- **Product:** gallery layout and image ratio, thumbnails, column split and gap, title, price and compare-at price
  styles, variant picker and swatch states (default, hover, selected, selected-hover, unavailable), quantity
  selector, add-to-cart button size and states, accordions or tabs, and the mobile order.
- **Collection:** grid columns at 1440 and 390 and the gap, card image ratio, card text rows, badges, filters and
  sort, pagination or load more.
- **Cart:** drawer or page, line-item layout, image size, quantity control, remove, subtotal and checkout button
  styles, empty state, notes and the free-shipping or upsell bar if any.

## 8. Imagery
*Corner treatment; `object-fit`; filters, overlays or colour treatment (usually none); aspect ratios by context
(people, product, hero); subject matter and setting; alt text, width and height, eager vs lazy loading.*

## 9. Assets
- **Typefaces:** <families, where they come from (Google, Adobe, self-hosted), and a ⚠️ licence flag for any TRIAL or DEMO file>
- **Logo:** <description, file and URL or path, rendered height in the header at 1440 and 390, inverse version if the site uses a light logo on dark, clear space and minimum size if stated>
- **Favicon:** <the favicon and touch-icon links in the page head, sizes, format, or "not set">
- **Icons:** <size range, fill or stroke, colour, style>
- **Custom-code prefix:** <only when a connected repo uses one (e.g. `aya-`), otherwise delete this line>

## 10. Visual parity
*Only when the work will rebuild existing pages: the live page is the specification, measured at 1440 and 390.
Tolerances table (container, padding and gaps ± 2px; font size, line height, letter spacing, weight, radius, border
width exact; image ratio and crop exact; section order and count exact; copy verbatim), and the rule that every
deviation is logged with its reason. Delete this section otherwise.*

## 11. Implementing this in <platform>
*Only when a repo or theme is connected (scan `repo.shopify`): map the values above onto that platform's own
settings and tokens, in the order a developer should try them (theme setting, then token override, then scoped
rule, then inline style). Never hardcode a value the platform already exposes as a setting. Record any known gap
between the saved settings and this file, dated. With no repo connected, delete this section: everything above is
platform-neutral.*

## 12. Shopify theme settings
*Always, even with no theme connected: the complete set of values a Shopify theme is set from, one table per
settings group. With a theme connected, use its own groups and setting ids (read `config/settings_schema.json`);
without one, use these groups. Every row has a value and an origin label; no row says "not stated". A row that needs
a file or licence says "needs file" and the value the theme uses until then.*

| Group | What to give |
|---|---|
| Logo and favicon | logo and inverse logo files (or "needs file"), logo height desktop and mobile, favicon file |
| Colours | the brand palette with a role for each colour; the theme's colour schemes or palette slots (background, text, primary and secondary button fill, text and border, input, border/divider, accent), each mapped to a palette colour, with its contrast ratio |
| Typography | heading, body, subheading and accent fonts (the brand's, or its stated fallback from Shopify's font library); the full scale from the Typography table: H1 to H6 and body, each with size, line height, letter spacing, case and font role |
| Page layout | page width, side margins, section padding desktop and mobile, gaps |
| Buttons | per variant: fill, text, border, border width, radius, font, case, hover, focus, disabled |
| Inputs | background, text, border, border width, radius, height, focus ring, error, label |
| Variant pickers and swatches | button style, radius, border, default, hover, selected, unavailable; swatch shape and size |
| Badges | position, radius, font, case, sale and sold-out colours |
| Product cards | image ratio, corner radius, hover effect, title case, price style |
| Cart, drawers, popovers | cart type, drawer and popover colours, radius, border, shadow |
| Animations | page transition, add-to-cart feedback, card hover, reduced motion |
| Icons | stroke or style |

**Rules for `(proposed)` values** (use the first that applies, and write which one in the row):
1. **Follow the brand's own pattern.** Continue a rule the sources show: if buttons are pills, inputs and variant
   buttons are pills; if images are square, cards and media are square; if the book shows no shadows, there are none.
2. **Type scale.** Take the stated or measured body size (16px if none) and the largest heading size the sources show
   or imply; fill the missing levels on a single ratio between them (1.2 to 1.333; 1.25 when nothing suggests
   otherwise), snapped to the theme's allowed sizes. Mobile steps H1 to H3 down by about 20%, H4 to H6 by about 10%.
   Line height: about 1.1 for display, 1.2 for H3 to H6, 1.5 for body. Letter spacing 0 unless the sources show
   tracking. Headings use the brand's heading weight; H5 and H6 may use the subheading role.
3. **Spacing.** Use one base unit (4px or 8px) and the proportions the sources show; when they show none, section
   padding 64px desktop and 40px mobile, 24px gaps, 16px mobile side gutter.
4. **States.** Hover and focus follow the brand's palette: hover darkens or inverts within the palette, focus is a 2px
   ring in the text colour with a 2px offset (`:focus-visible`), disabled uses 50% opacity; every state checked for
   contrast (4.5:1 text, 3:1 UI).
5. **Theme default.** Where nothing above decides it, keep the theme's own default and say so ("theme default,
   proposed"), so the choice is visible rather than silent.

## Change log
| Rev | Date | Requested by | Summary |
|---|---|---|---|
| 1 | <YYYY-MM-DD> | <client name or "agency for client", with reference> | <first capture> |
```
