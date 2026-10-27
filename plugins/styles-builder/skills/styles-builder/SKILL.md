---
name: "styles-builder"
description: Guide for creating design.md (the brand visual guide) in a Shopify theme repo from a brand book or a reference store, and applying its tokens into the theme's settings_schema.json and settings_data.json. Brand agnostic. Covers the full token set a theme needs before pages get built on it: typography, color schemes, spacing, corner radius, shadows, buttons and component states. Use whenever the user says "generate design tokens", "create design.md", "set up the brand's colors and fonts in the theme", "match the reference store's look", "build a style guide from this brand book", "what do we need before building pages", or whenever page-content-studio reports design.md is missing.
---

# Styles Builder (brand agnostic)

This skill fills the gap `page-content-studio` point at and neither
fills: **`design.md`, the brand's visual guide, has no generator.** Those skills stop and ask the user
for it, or refuse to invent brand values. This skill is how `design.md` gets made in the first place —
by extracting real design tokens from a source, then applying them into the theme so every later page
build starts from the same values instead of guessing them section by section.

It holds no brand facts of its own and is reusable across any Shopify theme repo and any client.

## What this skill is NOT

- **Not `brand-capture`.** Brand identity — voice, story, claims, competitors, proper names — lives in
  `brand.md`/`BRAND-VOICE.md` and is that skill's job. `brand-capture` deliberately keeps its own "Visual
  identity" section shallow — a palette/typography/imagery/logo summary, with "Full specification:
  design.md (it wins on any visual value)" once this skill has run — because going deeper there would
  duplicate what this skill owns. If `brand.md` doesn't exist yet, run brand-capture first (or alongside
  this one) and don't duplicate its content here. This skill only owns **visual** tokens: color,
  type, spacing, radius, shadow, buttons, components.
- **Not a ClickUp workflow.** This is theme-repo and live-store work only.
- **Not ongoing page editing.** Once `design.md` exists, `page-content-studio`
  read it for every subsequent build — this skill is run once per client (or once per rebrand), and again
  only when the source material changes.

## Why this runs before any page gets built

A theme has no visual identity of its own until something sets one. Build a page before that happens and
every section invents its own padding, its own button radius, its own shade of the brand color — small
differences that don't show up section by section but add up to a site that looks hand-assembled rather
than designed. This skill is the step that gives every later build the same values to pull from, so
`page-content-studio` and `page-content-studio` are filling in content and layout, never guessing brand values.

## Inputs (ask which the user has, in this order of preference)

1. **A brand book / style guide file** (PDF, Figma export, brand guidelines doc) — most reliable, use
   this first if available. Read it directly (pdf/figma/image tools as appropriate).
2. **A reference live store URL** — an existing site (the client's current site, or a competitor/inspiration
   named in `brand.md` if that file already exists) to extract computed values from.
3. **Direct answers in chat** — only for values not covered by 1 or 2, e.g. the user states a specific hex
   code or confirms a font license.

Multiple inputs can combine: e.g. a brand book for colors/fonts plus a reference store to confirm computed
spacing/button states in practice. When sources conflict, ask the user which wins rather than guessing.

## Step 0: Before starting

1. Check whether `design.md` already exists in the repo. If it does, this is an update, not a fresh capture
   — read it first, show the user what would change, and only touch the sections the new source affects.
2. Check whether `brand.md`/`BRAND.md` exists. If not, mention that brand-capture can produce it, but don't
   block on it — visual tokens can be captured independently.
3. Confirm which theme repo / branch this is for, and whether the user also wants tokens applied live into
   `config/settings_schema.json` and `config/settings_data.json`, or only written to `design.md` as reference.
   Default to **both** unless the user says otherwise, since a `design.md` with no theme applied just
   recreates the gap this skill exists to close.

## Step 0.5: The initial token set — what "ready to build on" means

Before a theme is ready for `page-content-studio` to build or edit pages against, these are the
things that need a settled, sourced value. Treat this as the checklist for Step 1's extraction and Step 3's
`design.md`: a design.md missing one of these isn't wrong, but say plainly in the summary which are still
`unconfirmed` rather than letting a later skill discover the gap mid-build.

- **Color schemes** — not just "the brand colors," but how they group into the named sets a Shopify
  theme actually uses (a scheme defines roles: text, background, button, border — see Step 4). At minimum:
  a primary/light scheme, and a dark or inverse scheme if the brand's site or book uses one anywhere
  (a footer, a promo band, a dark hero). Each scheme needs its role colors identified, not just a swatch list.
- **Typography** — font family per role (heading, body, and accent/display if the brand uses one),
  weights actually used (don't carry over every weight a font file ships with — list only the ones that
  appear), a type scale (H1 through H4 or H5, plus body and small/caption sizes), line height per role,
  letter-spacing where the brand uses it (often headings only), and casing convention (sentence case,
  title case, or uppercase for eyebrows/labels).
- **Spacing and layout rhythm** — section vertical padding (desktop and mobile — these are almost always
  different), the gap between stacked elements within a section, the max container width(s) the brand's
  layout uses, and the grid/column gap for multi-column layouts (card grids, feature grids).
- **Corner radius** — a single brand radius is common, but check for more than one scale (e.g. a tight
  radius on buttons and inputs, a larger one on cards or image containers) rather than assuming one value
  covers every component.
- **Shadows** — many brands use none at all; confirm this rather than skipping it silently. If the brand
  does use elevation (cards, dropdowns, hover states), capture the actual shadow values (offset, blur,
  spread, color and opacity), not just "subtle shadow."
- **Buttons** — every variant the brand uses (primary, secondary, tertiary/text-link-style), and for each:
  default, hover, focus, and disabled states. A brand book often only shows the default state — note which
  states are inferred vs. shown.
- **Other components** — anything the brand treats consistently enough to be a token rather than a
  one-off: form inputs (border, focus ring, radius — often shares the button radius), badges/tags, dividers,
  the announcement bar if one exists. Don't invent a component the brand doesn't visibly have a convention
  for; a reference store with one styled form field is evidence, one styled anything-else is not.
- **Imagery** — aspect ratios by use (hero, card, product gallery), crop behaviour, and whether images
  get a consistent treatment (corner radius, border, duotone, grayscale on hover).

This list is what makes Step 1's extraction systematic instead of "grab whatever's easy to see." Work
through it in order; it's also the order `design.md`'s sections should follow (Step 3).

## Step 1: Extract tokens from the source

### From a brand book file
Read every page. Pull out, verbatim where stated:
- Primary/secondary/accent colors with hex/RGB values, and which named scheme each belongs to (e.g. "Scheme
  1: Light", "Scheme 2: Dark/Inverse") if the book defines schemes; if it only shows swatches with no scheme
  mapping, propose a mapping and flag it as inferred.
- Font families (headings vs. body vs. accent/display), with weights and license/source named if stated.
- Any defined type scale (e.g. H1 48px/1.1, H2 32px/1.2) — if the book only shows samples without sizes,
  measure proportions and flag as inferred.
- Button styles: primary/secondary/tertiary variants, corner radius, border treatment.
- Spacing/grid guidance if present.
- Imagery treatment: crop ratios, filters, radius, any consistent treatment shown across examples.

### From a reference live store
Do not eyeball rendered colors or guess font names from how text looks — measure them:
- Capture desktop and mobile widths; scroll slowly so lazy content loads (same capture discipline as
  `page-content-studio` Step 2).
- Read **computed values** with `getComputedStyle` (or equivalent) for: background/text/border/link colors
  per distinct visual section (to infer named color schemes), font-family/size/weight/line-height/
  letter-spacing per heading level and body text, container max-width and section padding/gaps, button
  background/text/border color in default, hover, focus and disabled states, image aspect ratios and corner
  radius actually rendered.
- Note which colors repeat together as a set — that's a "scheme" even if the reference site never names it
  as one. Name schemes descriptively (e.g. "Light", "Dark/Inverse", "Accent") unless the user has names
  already in mind.
- If no rendered view is possible, say so plainly and name what failed — do not guess values from a
  text-only fetch, exactly as `page-content-studio` requires for its own captures.

### From direct chat answers
Only to fill specific named gaps (a hex code, a confirmed license) — never as the primary source when a
file or reference store is available.

## Step 2: Resolve conflicts and gaps

- When brand book and reference store disagree (e.g. book says one blue, live site renders a slightly
  different blue), ask the user which is current/authoritative — brand books go stale, live sites
  sometimes drift from guidelines.
- Never invent a value with no source. If something is missing from every source (e.g. no stated font
  license, no documented shadow), leave it explicitly marked `unconfirmed` in `design.md` rather than
  filling in a plausible guess — `page-content-studio`'s font-transfer step depends on this being honest, and a
  theme applying an `unconfirmed` value silently is how a guess becomes load-bearing.
- Flag anything inferred (a proposed scheme mapping, a measured-not-stated type scale) clearly as
  `(inferred)`, matching brand-capture's convention for the same situation.

## Step 3: Write design.md

Follow the shape `page-content-studio` expects for a visual spec it can read (see its
SKILL.md "Visual spec" section, which points `BRAND.md`'s `design_doc` key at this file), covering:

- **Colour palette** — every named scheme, which colours it contains, where each is used (background,
  text, border, accent, link, button).
- **Typography** — families (heading/body/accent), scale per role, weights, casing conventions, font
  licence status per family.
- **Spacing and container widths** — section padding (desktop and mobile), gaps, max container width(s),
  grid/breakpoint values.
- **Corner radius** — per component family (buttons/inputs vs. cards/images) if the brand uses more than
  one scale; otherwise the single brand radius.
- **Shadows** — the actual values if the brand uses elevation, or an explicit "no shadows — flat design"
  line if it confirmed doesn't.
- **Buttons** — every variant (primary/secondary/tertiary/link-style), and default/hover/focus/disabled
  states for each.
- **Components** — form inputs, badges, dividers and any other element the brand treats consistently.
- **Imagery** — aspect ratios by use (hero, card, PDP gallery, etc.), crop behaviour, corner radius,
  consistent treatment (duotone, border, shadow).
- **Shared styling contract** — the rule that sections of the same page family (e.g. all PLP card grids,
  all hero banners) must share these values, so future builds stay consistent without re-deriving them.
- **Parity tolerances** — how close a rebuilt page must measure to a reference (pixel/percent tolerance on
  spacing, color delta tolerance) — propose sensible defaults (e.g. ±4px spacing, ΔE < 2 for color) and
  ask the user to confirm or adjust.

Status/revision header matching the convention other brand docs in this repo use, if one exists (check
`brand.md`'s front matter for the pattern — it has a `design_doc` key for exactly this). Keep brand
identity content (voice, claims, competitor names) out entirely — link to `brand.md` instead of repeating it.

## Step 4: Apply to the theme

Read this whole step before writing anything. Shopify's settings system has specific shapes for each
kind of token, and treating them all the same way is the most common way this step goes wrong.

### What Shopify actually gives you to work with

- **Colors have three different setting types, and they're not interchangeable.** A theme has exactly
  one `color_palette` (lives only in `settings_schema.json`, 2–20 named colors, keyed by *usage* —
  `primary`, `accent` — never by appearance like `blue`). Sections reference a palette color as
  `settings.colors.<key>`, so editing the palette's hex value propagates everywhere that key is used — this
  is the lever to pull for "change the brand's primary color everywhere." Separately, a
  `color_scheme_group` defines named *schemes* (Dawn's convention: something like Background 1, Background
  2, Inverse, Accent 1, Accent 2 — there's no fixed platform limit, but more than 5 or so gets hard for a
  site editor to pick between meaningfully), and each scheme maps **roles** — text, background, buttons,
  borders — to actual colors. Sections and blocks then pick a `color_scheme` by reference. **This is why
  color work is the highest-risk part of this step**: remapping brand colors into existing scheme slots
  changes every section that references that scheme, and Shopify's theme editor does not check contrast
  when you do it. Check every role combination a scheme produces (text-on-background, text-on-button)
  against WCAG AA (4.5:1 for body text) before calling a scheme done — a scheme that looked fine as
  swatches can produce unreadable text once applied.
- **Spacing, corner radius and shadows have no dedicated setting type.** Unlike colors and fonts, Shopify
  doesn't have a `spacing` or `border_radius` or `shadow` input type. These are built with plain `range`
  settings (numeric, in px or rem) that feed CSS custom properties in the theme's stylesheet. This means
  two things: first, the schema enforces nothing about what's a *reasonable* value beyond the `min`/`max`/
  `step` you set — a radius range with no sane max will happily accept a value that breaks the button's
  layout, so set bounds that reflect the brand's actual scale, not arbitrary ones; second, the Liquid
  setting and the CSS variable it feeds can drift out of sync if a section's CSS hardcodes a value instead
  of reading the custom property — when applying tokens to an existing theme, grep for hardcoded px radius/
  shadow/spacing values in section CSS and replace them with the token reference, don't just add the new
  setting alongside the old hardcoded value.
- **Typography is font-picker only.** The `font_picker` setting type draws from Shopify's font library —
  it can't point at an arbitrary custom font file. If the brand's typeface isn't in Shopify's library, it
  has to be uploaded as a custom theme asset and referenced via `@font-face` in the theme's CSS, which
  means it sits outside the normal settings/presets system — note this in `design.md` so `page-content-studio`
  knows the font isn't swappable via the theme editor the way a `font_picker` value is.
- **Buttons and components still have no native type.** They're `range`/`select`/`color` settings read
  into CSS, same as spacing — the guardrails above apply equally.

### Before writing

1. Pull the latest theme (`shopify theme pull`, or the repo's own command from `AGENTS.md`) and check
   `git status` first — Admin edits can be stale otherwise.
2. Create a branch using the repo's naming pattern.
3. **Grep before you add.** Before creating any new setting ID, search the existing
   `settings_schema.json` and the section Liquid/CSS for something that already covers the token (an
   existing radius range, an existing color scheme slot). Reusing an existing ID means every section
   already wired to it picks up the new brand value for free; adding a parallel new ID means you now have
   to go find and update every place that should use it, and anything missed quietly keeps the old look.

### Mapping tokens in

- **Color schemes** → remap into the theme's existing `color_scheme_group` slots first (Dawn-based themes
  already define several; reuse the slots and change their role colors rather than inventing new scheme
  names) unless the user explicitly wants a full reset with new scheme names. After remapping, check every
  scheme's role combinations for contrast (see above) — this is not optional, because a silent contrast
  failure is invisible until a real visitor can't read the button text.
- **Typography** → the theme's existing type settings (`font_picker` values, base size and scale-ratio
  `range` settings) in `settings_schema.json`/`settings_data.json`. Keep the number of distinct weights
  actually enabled small — each additional weight/family Shopify's font library serves is extra page
  weight; a brand book listing six weights of one family doesn't mean the theme should load all six if the
  site only uses two of them in practice.
- **Spacing, radius, shadows, buttons** → same reuse-first rule. Set `range` `min`/`max`/`step` to bound
  values the brand's own scale would plausibly need, not platform maximums — a reviewer two years from now
  should be able to tell from the schema's bounds roughly what this brand's scale looks like.
- Never hardcode a token into Liquid/CSS where a theme setting already exists to hold it — this is the
  same rule page-content-studio enforces, and it applies doubly here since this skill is what makes
  those settings exist in the first place.
- If a brand font isn't already in Shopify's font library, follow the repo's font-transfer steps in
  `AGENTS.md`, including the licence question to the user — do not silently substitute a lookalike font,
  and flag it in `design.md` as an asset-based font, not a `font_picker` value (see above).

## Step 5: Verify

- Load the theme in `shopify theme dev` (or the repo's dev command) and visually confirm colors/fonts/
  buttons/radius/shadows actually render as specified — reading the JSON back is not verification.
- Spot-check at least one page in each defined color scheme and at least one button in each state
  (default/hover/focus/disabled). Check text-on-background and text-on-button contrast visually in each
  scheme, not just the one the homepage happens to use.
- Check at least one narrow mobile width (375px or similar) specifically for spacing and button radius —
  CSS overrides for these tend to break first at narrow widths, not on desktop.
- Re-run `shopify theme check` (or the repo's equivalent) and compare against the baseline from before this
  change — flag anything that changed count.

## Step 6: Push, log, summarize

- Push only to an unpublished/draft/preview theme, scoped to the exact files touched. Never push to the
  live theme without the user's explicit go-ahead, confirmed in chat — same rule as every other theme-repo
  skill in this roster.
- Log an entry in the repo's QA log if one exists, noting the source (brand book file name, or reference
  store URL) and what was applied vs. only documented.
- Final summary, short: what `design.md` now contains, what was and wasn't applied to the live theme
  settings, anything left `unconfirmed` that the user should resolve, any contrast issues found and how
  they were resolved, and whether this is on draft/preview or live.

## Never

Do not invent a color, font, spacing, radius, or shadow value with no source — mark it `unconfirmed`
instead. Do not duplicate brand identity content that belongs in `brand.md`. Do not create a new theme
setting id where an existing one already covers the token. Do not remap a color scheme without checking
its role combinations for contrast. Do not push to the live theme without explicit, chat-confirmed
approval. Do not claim a visual check passed without having loaded the actual rendered theme.
