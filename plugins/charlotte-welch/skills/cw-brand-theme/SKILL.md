---
name: cw-brand-theme
description: Charlotte Welch (Hautebox) store. Make a Shopify store's theme match its brand guide. Maps the palette, gradients and (when asked) typography in BRAND.md or a brand book onto the theme's colour settings, fonts and the colours set on individual sections, checks every text/background pair for readable contrast, and delivers it on an unpublished preview copy with a before/after table. Works through the Shopify connector in a normal Claude chat (no terminal), or the Shopify CLI. Use whenever someone says "change the brand colors on the website", "make the site match our brand guide / style guide", "update the fonts", "apply the new branding", "our site doesn't look on brand", "rebrand the store", or sends hex codes, a palette or a brand book and wants the website updated, even if they don't say "theme".
---

# Shopify brand theme

Bring a live store in line with its brand guide without breaking readability or the owner's layout. The owner is
usually a busy founder who customised a paid theme by hand: they want the site to look like the brand book, and they
need a preview and a short before → after list, not settings.

## Effort

| | Colours | Fonts only |
|---|---|---|
| Time | about 4.5 minutes, measured 2026-11-12 (offline dry run) | about 3 minutes, measured 2026-11-12 |
| Tokens | about 125,000 | about 110,000 |

Use Opus 5.5 at high effort or above (contrast pairings and role decisions are where weaker settings slip; inferred,
not measured). Past 15 minutes, stop and say what's blocking.

## What good looks like

- **Only what was asked.** "Change the brand colors" means colours; fonts, letter-spacing or logo changes are offered
  as extras with a one-line why, and done only on a yes. Sitewide changes (page background, fonts) are named as such:
  the owner should know a change reaches every page.
- Every colour on the site traces to the brand palette (or a neutral the owner approved), including hex values set on
  individual sections, not just the global colour settings.
- **The owner's signature stays.** A surface already in a brand colour (an orange header when orange is in the
  guide) is kept; only its text and buttons are fixed. Read the guide's own labels: a colour it lists as *primary* may
  be the brand's main surface colour, not just an accent. Repaint a surface only when its colour is off-palette.
  (Learned on Charlotte Welch: the skill moved her orange header to the dark gradient; her team said orange is the
  site's main colour.)
- Every text-on-background pair passes WCAG AA (4.5:1 body text, 3:1 large text and UI). Fix failures by changing
  the pairing, not the brand colour.
- One approval before writing; delivered on an unpublished copy with a preview link; the live theme is untouched.

## Step 0: Read the brand and the theme

1. **Files:** `AGENTS.md` / `CLAUDE.md`, `BRAND.md` (Visual identity: palette and roles, gradients, typography,
   logo), `THEME-SPECIFICS.md` and `BRAND-REQUESTS.md` (open visual requests, such as "orange is the main colour"),
   in the project folder, the chat project's files, or attached. No BRAND.md: use the brand book the user gave you
   and offer the brand-capture skill.
2. Note values the brand file marks unconfirmed ("possible colors", `[[CLIENT TO CONFIRM]]`): build the preview
   anyway, but tell the owner which values are unconfirmed.
3. **Store access:** `references/store-access.md` (connector, CLI or offline). Say which in one line.
4. **Theme:** `theme_info` in `config/settings_schema.json`. Honey → `references/honey.md`; others →
   `references/other-themes.md`. THEME-SPECIFICS.md wins where it's more specific (it reflects this store today).

## Step 1: Inventory what's in use

```bash
python scripts/find_colors.py <theme-folder> --palette "#152E38,#111B18,#104F4C,#c93d0d,#000000,#ffffff"
```

It lists every hex colour in `config/settings_data.json`, `templates/*.json` and `sections/*.json` with its JSON path
and marks the off-palette ones. Working through the connector? If you can run Python, save the files you read into a
scratch folder with the same paths and run the script there; otherwise read the JSON and list the colours by hand.
Also note the fonts (`type_*_font`) and **which sections use each colour group**, because changing a group repaints
every section on it (on Honey the header and footer share one group).

## Step 2: Plan the mapping

A table: setting or section · current · new · role · why. Roles from the guide:

- **Signature surfaces** (header, footer, announcement bar) already on-palette: keep.
- **Light surface** (page background): the guide's light colour. If the guide only gives pure white and the site uses
  an off-white, propose white but flag it: it's a visible sitewide change.
- **Dark surfaces:** the guide's darks; where a dark gradient lives.
- **Accent:** buttons, sale price, badges, links.
- **Text:** the guide's dark on light, white on dark and on saturated colours.
- **Off-palette leftovers:** nearest role, or list for the owner if it might carry meaning (a seasonal section).

Gradients: the theme's native gradient setting if it has one; otherwise section-level Custom CSS on chosen sections
(see the theme reference). The guide gives the stops; where to use it is your proposal, so say so. A design-tool
angle of -90° (top-to-bottom stops) is `linear-gradient(180deg, ...)`.

Fonts (only if asked, or as an offered extra): a Shopify-library handle; if the brand font isn't in the library,
the closest from `references/fonts.md` plus how to load the real one (Adobe Fonts or self-hosted, both need the
owner's web licence). Never upload font files the owner hasn't licensed.

**Freshness (up to 3, never applied without a yes):** while reading the theme, note what makes it look dated or
off-brand beyond colour (a disabled old campaign hero worth deleting, mismatched button styles) and offer it.

## Step 3: Contrast, then one yes

```bash
python scripts/contrast.py "#ffffff:#c93d0d" "#c93d0d:#111B18" --label "button text,accent on dark"
```

Check text on every surface, button text on buttons, badge text on badges, links on surfaces, and text against both
ends of a gradient. Fix failures by changing the pairing; if a brand colour can't pass anywhere it's needed, propose a
nearest shade for the owner. (No Python? The WCAG formula is in the script; compute it, or say it wasn't checked.)

Show the owner the plan: the before → after table grouped as page colours · buttons and badges · individual
sections · fonts (if any), which changes are sitewide, contrast results, extras offered, unconfirmed values. Write
nothing until they say yes.

## Step 4: Write, read back, look

1. Edit `config/settings_data.json` → `current` and the section JSON values from the plan. Keep `/* ... */` headers
   and ids; change only planned values. Validate: JSON parses, setting ids exist in the schema, colours are `#rrggbb`,
   font handles are real library handles.
2. Write to the unpublished copy (`references/store-access.md`; section code before templates). Read back and confirm
   only the planned values changed.
3. **Look at it on desktop and mobile:** with a browser tool, open the preview home page, a product page, a collection
   and the cart drawer at about 390 and 1440 pixels wide (and 1920 for the home page). Check the header, buttons,
   badges and text are readable. Without a browser, say the visual check wasn't run.
4. Theme code changed (rare)? Mark it `Nyla:`, save the file in `theme-mods/`, add a row to `THEME-SPECIFICS.md`.

## Step 5: Hand over

Tell the owner briefly: the before → after table, what's sitewide, contrast (all pass, or which pairing changed),
what's unconfirmed and what needs their licence, the preview link, and the next step (approve, then publish
themselves or tell you to; if they edited live since the duplicate, re-duplicate and re-apply instead). Save the
table as `brand-theme-<YYYY-MM-DD>.md` in the project root (or give it in chat), and add to `THEME-SPECIFICS.md` any
colour-group facts you learned.

## Quick path (demo mode)

BRAND.md exists and a fresh preview copy exists: for a single request ("make the buttons our orange", "use our dark
green on the newsletter band"), read only the files involved, show before → after with the contrast result, get the
yes, write, read back, give the preview link. About a minute of work.
