# Starter setup: what a theme needs before pages get built on it

The essential settings to get a new store's theme ready to build on. The starting theme decides the
list, so walk its own settings instead of working from memory.

## 1. Inventory the theme

1. Read `config/settings_schema.json` and list its setting groups with their ids and types. Note the
   theme and its version (the schema's theme info, `AGENTS.md`, or the repo's notes).
2. **Ids differ between versions.** In Horizon v3.5.1 the input and variant settings are
   `inputs_border_radius`, `variant_background_color` and `pills_border_radius`, and colour uses a
   `color_scheme_group`. Current upstream Horizon uses `palette_input_*`, `variant_button_radius` and a
   single `color_palette`. Never hardcode an id from this file: find the theme's own.
3. Build one table: group, setting ids, what the brand says (with its source), and a status.

| Status | Meaning |
|---|---|
| set | A brand value from a source was applied |
| default, confirmed | The theme's default fits and the brand evidence agrees (for example "no shadows") |
| default, no evidence | Left at the theme default because no source covers it; say so in the summary |
| not applicable | The brand has nothing of that kind (for example no badges) |

## 2. Horizon's groups and where the brand evidence comes from

| Group | Typical settings | Brand evidence |
|---|---|---|
| Logo and favicon | logo, inverse logo, heights, favicon | `logo-favicon.md` |
| Colors | schemes or palette | brand book, measured computed colours |
| Typography | font pickers, sizes, line heights, case | brand book, measured; the font sourcing ladder |
| Page layout | page width, margins | measured container widths |
| Animations | page transition, add-to-cart, card hover | `motion.md` |
| Badges | position, radius, sale and sold-out colours | measured on a product card, or "none" |
| Buttons | colours, hover, border, radius, case | measured states |
| Cart, drawers, popovers and modals | cart style, drawer and popover radius | measured, else default |
| Icons | style | measured |
| Input fields | colours, border, radius | measured on a real form |
| Prices | regular, sale and unit price styles | measured on a product card |
| Product cards | corner radius, hover effect | measured |
| Search | style | measured, else default |
| Swatches and variant pickers | pills, buttons, swatches, states | measured on a product page with variants |

Another starting theme (Dawn and others) has different groups: use its own, same method.

## 3. Apply, then report

- Reuse first: use the theme's existing settings. Where you must add one, bound its `min` and `max` to
  the brand's scale, and grep section CSS for hardcoded values the setting should feed.
- "Ready to build on" means every group in the table has a status. List the groups still at default with
  no evidence in the summary, so a later page build doesn't discover the gap halfway.
