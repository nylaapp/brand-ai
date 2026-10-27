---
name: "styles-builder"
description: Guide for creating or deepening design.md (the brand visual guide) in a Shopify theme repo from a brand book or a reference store, and applying its tokens into the theme's settings_schema.json and settings_data.json. Brand agnostic. Covers the full token set a theme needs before pages get built on it: typography, color schemes, spacing, corner radius, shadows, buttons and component states. Use whenever the user says "generate design tokens", "create design.md", "set up the brand's colors and fonts in the theme", "match the reference store's look", "build a style guide from this brand book", "what do we need before building pages", or when page-content-studio or page-audit had to fall back to theme settings because design.md is missing or too thin.
---

# Styles Builder (brand agnostic)

`page-content-studio` and `page-audit` take visual values from `design.md`, the brand's visual guide.
When it is missing they fall back to the store repo's own visual spec or the theme's settings, and they
never invent a value. This skill is for when that fallback isn't enough: on top of brand-capture's
first pass, it builds `design.md` out from a brand book or a reference store by extracting real design
tokens from a source. Then it **applies the tokens into the theme's settings**, so every later page build
starts from the same values instead of re-deriving them section by section. Applying them to the theme
is the part no other skill in this marketplace does.

It holds no brand facts of its own and is reusable across any Shopify theme repo and any client.

## What this skill is NOT

- **Not `brand-capture`.** Brand identity — voice, story, claims, competitors, proper names — lives in
  `BRAND.md` and `BRAND-VOICE.md` and is that skill's job, and this skill needs its files: if `BRAND.md`
  doesn't exist yet, brand-capture runs first (Step 0), never alongside or after, and its content isn't
  duplicated here. This skill only owns **visual** tokens: color, type, spacing, radius, shadow, buttons,
  components.
- **Not a ClickUp workflow.** This is theme-repo and live-store work only.
- **Not ongoing page editing.** Once `design.md` exists, `page-content-studio` and `page-audit`
  read it for every subsequent build — this skill is run once per client (or once per rebrand), and again
  only when the source material changes.

## How this fits with brand-capture

brand-capture always runs first (Step 0): this skill doesn't start without `BRAND.md` and a first-pass
`design.md`. Both skills write to `design.md`, so know which one does what:

- **`brand-capture`** writes a first-pass `design.md` as part of brand setup: values measured on the live
  site (at 1440 and 390 wide), from the scan and from the theme's settings, labelled `(from site)` or
  `(inferred)`. It never overwrites a `design.md` that already exists; it adopts it and points
  `BRAND.md`'s `design_doc` key at it.
- **This skill** goes further where that first pass can't: a brand book or style guide as the source, a
  reference store, a rebrand, the full token set in Step 0.5 (named
  color schemes, every button state, parity tolerances), and, only here, applying the tokens into the
  theme's `settings_schema.json` and `settings_data.json`.
- **If a `design.md` already exists** (brand-capture's, the client's, or an earlier run of this skill), it
  is the starting point, not something to replace. Read it, show the user what would change, wait for a
  yes, and edit only the sections the new source affects (Step 0).
- **Same file either way.** Use the same flat front matter and origin labels brand-capture uses (Step 3)
  so the file reads the same whichever skill wrote it. Leave `BRAND.md` to brand-capture: if its
  `design_doc` key doesn't point at the file yet, say so in the summary and have brand-capture adopt the
  file instead of editing `BRAND.md` here.

## Why this runs before any page gets built

A theme has no visual identity of its own until something sets one. Build a page before that happens and
every section invents its own padding, its own button radius, its own shade of the brand color — small
differences that don't show up section by section but add up to a site that looks hand-assembled rather
than designed. This skill is the step that gives every later build the same values to pull from, so
`page-content-studio` is filling in content and layout, never guessing brand values.

## Inputs (ask which the user has, in this order of preference)

1. **A brand book / style guide file** (PDF, Figma export, brand guidelines doc) — most reliable, use
   this first if available. Read it directly (pdf/figma/image tools as appropriate).
2. **A reference live store URL** — an existing site (the client's current site, or a competitor/inspiration
   named in `BRAND.md`) to extract computed values from.
3. **Direct answers in chat** — only for values not covered by 1 or 2, e.g. the user states a specific hex
   code or confirms a font license.

Multiple inputs can combine: e.g. a brand book for colors/fonts plus a reference store to confirm computed
spacing/button states in practice. When sources conflict, ask the user which wins rather than guessing.

## Step 0: Before starting

1. **brand-capture's files are required. Never skip this.** Check that `BRAND.md` and `design.md` both
   exist, in the theme repo or in the brand's own folder where brand-capture keeps them
   (`$BRAND_AI_HOME/brands/<slug>/`, default `~/.brand-ai/brands/<slug>/`). If either is missing, do not
   start extracting and do not write a `design.md` of your own in its place: tell the user brand-capture
   has to run first, run it (a full run writes both files; if `BRAND.md` exists and only `design.md` is
   missing, it adds that one), and carry on only once both exist. If brand-capture isn't available in this
   session, stop and say so.
2. A `design.md` now exists, so this is an update, not a fresh capture — read it first, show the user what
   would change, wait for a yes, and only touch the sections the new source affects. Update it where it
   lives.
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
- Capture desktop and mobile widths (brand-capture measures at 1440 and 390); scroll slowly so lazy
  content loads (same capture discipline as the reference capture in `page-content-studio` Step 3b).
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
  filling in a plausible guess — `page-content-studio` checks a new font's licence with the Site Editor
  before using it, and that check is only as honest as this file; a theme applying an `unconfirmed` value
  silently is how a guess becomes load-bearing.
- Flag anything inferred (a proposed scheme mapping, a measured-not-stated type scale) clearly as
  `(inferred)`, and anything measured on a live store as `(from site)`, matching brand-capture's origin
  labels for the same situations.

## Step 3: Write design.md

`page-content-studio` and `page-audit` find this file through `BRAND.md`'s `design_doc` key and treat it
as the source for every visual value, so write it the way brand-capture's `design.md` is written
(lowercase name, same front matter and origin labels, below), covering:

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

Front matter: the same flat `key: value` lines brand-capture's `design.md` uses (no nesting, no quotes):
`brand`, `parent_doc: BRAND.md`, `status` (draft or approved, same as `BRAND.md`), `revision` (+1 on every
write), `last_updated`, `measured` (date and viewports, or "not measured"), and `source` (the brand book
file or reference store URL). Label a value `(from site)` when measured on a live store and `(inferred)`
when proposed; values taken as stated from a brand book are covered by `source`. Leave any `(client)` line
as the user wrote it. Keep brand identity content (voice, claims, competitor names) out entirely — link to
`BRAND.md` instead of repeating it.

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
  same rule `page-content-studio` enforces, and it applies doubly here since this skill is what makes
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
  they were resolved, whether `BRAND.md` points at the file through `design_doc` (if not, have
  brand-capture adopt it), and whether this is on draft/preview or live.

## Never

Do not invent a color, font, spacing, radius, or shadow value with no source — mark it `unconfirmed`
instead. Do not start, or write a `design.md` of your own, when `BRAND.md` or brand-capture's `design.md` is
missing: run brand-capture first. Do not duplicate brand identity content that belongs in `BRAND.md`. Do not create a new theme
setting id where an existing one already covers the token. Do not remap a color scheme without checking
its role combinations for contrast. Do not push to the live theme without explicit, chat-confirmed
approval. Do not claim a visual check passed without having loaded the actual rendered theme.
