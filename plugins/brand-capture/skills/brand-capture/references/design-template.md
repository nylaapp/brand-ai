# design.md template

design.md holds the brand's visual system as **actual values**: palette, type, spacing, corners, components, imagery.
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

A value you could not measure is labelled `(inferred)` or left out. **Never invent** a hex, size, radius, font or
hover behaviour to fill a table. Put anything that cannot be settled in BRAND-QUESTIONS.md like any other open item
(font licences especially: a font named TRIAL or DEMO is a licence question, shown under Assets).

**Sizing.** Aim for 150 to 330 lines. Skip a section whose subject the brand doesn't have (a store with no
accordions has no Accordion entry). Keep every rule that a designer would otherwise get wrong: the counterintuitive
ones (what is rounded and what is square, what hover does, which family does which job) earn the most space.

**Origin labels** are the same as in BRAND.md. Use `(from site)` for measured values and `(inferred)` for the rest;
`(client)` lines are never overwritten by a re-scan.

The front matter is flat `key: value` lines (no nesting, no quotes). Dates are `YYYY-MM-DD`.

---

```markdown
---
design_md_schema: 1.0
brand: <same as BRAND.md `brand`>
parent_doc: BRAND.md
brand_md_revision: <the BRAND.md `revision` this file was last checked against>
status: <draft | approved, same as BRAND.md>
revision: <1, 2, 3 ... +1 on every write>
captured: <YYYY-MM-DD of the first capture>
last_updated: <YYYY-MM-DD of the latest write>
measured: <YYYY-MM-DD and viewports, e.g. "2026-10-09 at 1440 and 390", or "not measured: scan CSS only">
source: <e.g. "brand-capture scan of https://example.com plus browser measurement">
captured_by: brand-capture 1.2.0
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
*H1, H2, H3, body, small body, nav link, button label, eyebrow, caption: only the roles the site has, desktop first
with the mobile step noted where it differs.*

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

### Inputs · Links · Navigation · Accordion · Product card
*Only those the brand uses. One short paragraph or table each, with real values. Third-party widgets that render
their own unbranded styles (a pop-up app, a reviews widget) are named as "not the brand's reference".*

## 7. Imagery
*Corner treatment; `object-fit`; filters, overlays or colour treatment (usually none); aspect ratios by context
(people, product, hero); subject matter and setting; alt text, width and height, eager vs lazy loading.*

## 8. Assets
- **Typefaces:** <families, where they come from (Google, Adobe, self-hosted), and a ⚠️ licence flag for any TRIAL or DEMO file>
- **Logo:** <description, rendered size in the header, URL or path, clear-space or colour variants if the site shows them>
- **Icons:** <size range, fill or stroke, colour, style>
- **Custom-code prefix:** <only when a connected repo uses one (e.g. `aya-`), otherwise delete this line>

## 9. Visual parity
*Only when the work will rebuild existing pages: the live page is the specification, measured at 1440 and 390.
Tolerances table (container, padding and gaps ± 2px; font size, line height, letter spacing, weight, radius, border
width exact; image ratio and crop exact; section order and count exact; copy verbatim), and the rule that every
deviation is logged with its reason. Delete this section otherwise.*

## 10. Implementing this in <platform>
*Only when a repo or theme is connected (scan `repo.shopify`): map the values above onto that platform's own
settings and tokens, in the order a developer should try them (theme setting, then token override, then scoped
rule, then inline style). Never hardcode a value the platform already exposes as a setting. Record any known gap
between the saved settings and this file, dated. With no repo connected, delete this section: everything above is
platform-neutral.*

## Change log
| Rev | Date | Requested by | Summary |
|---|---|---|---|
| 1 | <YYYY-MM-DD> | <client name or "agency for client", with reference> | <first capture> |
```
