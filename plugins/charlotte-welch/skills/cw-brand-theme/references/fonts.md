# Brand fonts that aren't in Shopify's font library

Shopify's font library is system fonts plus a selection of Google Fonts. Commercial fonts (Adobe, Monotype,
foundry fonts) aren't in it. Handles are `<family>_<style><weight>`: `n` normal, `i` italic, `4` = 400 regular
(`lora_n4`, `crimson_pro_i4`). Exceptions exist (`ebgaramond_n4`, `source_serif_4_n4`), so confirm against
https://shopify.dev/docs/storefronts/themes/architecture/settings/fonts before using a handle. Checked 2026-11-12.

| Brand font | Closest library font (handle) | Also close | Notes |
|---|---|---|---|
| Minion Pro | Crimson Pro (`crimson_pro_n4`, weights 2 to 9, italics) | Crimson Text (`crimson_text_n4`), EB Garamond (`ebgaramond_n4`), Cardo (`cardo_n4`) | Crimson was drawn in the Minion tradition; closest x-height and rhythm |
| Garamond (Adobe, Monotype) | EB Garamond (`ebgaramond_n4`) | Cormorant (`cormorant_n4`) | Cormorant Garamond itself isn't in the library |
| Caslon | Libre Caslon Text, if listed | Libre Baskerville (`libre_baskerville_n4`) | check the library list |
| Baskerville | Libre Baskerville (`libre_baskerville_n4`) | | |
| Source Serif Pro | Source Serif 4 (`source_serif_4_n4`) | | renamed family |
| Helvetica / Neue Haas | Inter (`inter_n4`) | system sans | |
| Futura | Jost, if listed | Montserrat | check the library list |
| Gotham | Montserrat | | |

When you substitute, say so in the hand-over, and include the route to the real font:
- **Adobe Fonts (Typekit):** the owner creates a web project for the font in their Adobe account, which gives a
  `<link>` tag; add it to `layout/theme.liquid` and override `--font-heading-family` / `--font-body-family` in CSS.
  Needs an active Creative Cloud licence that covers web use.
- **Self-hosted:** upload licensed web font files (`.woff2`) to the theme's `assets/` and add `@font-face` with
  `asset_url`. Only with a web licence.
