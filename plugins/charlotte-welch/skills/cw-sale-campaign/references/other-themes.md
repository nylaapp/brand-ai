# Other themes: finding the campaign surfaces

Most current Shopify themes are Online Store 2.0: JSON templates (`templates/*.json`), section groups
(`sections/header-group.json`), and settings in `config/settings_data.json`. Find each surface before writing.

1. **Announcement bar**: in `sections/header-group.json`. Dawn-family themes use an `announcement-bar` section with
   `announcement` blocks (each has `text`, `link`); several blocks rotate. Some themes keep it in the header section.
2. **Hero**: the first section in `templates/index.json` → `order` (types like `image-banner`, `slideshow`,
   `video`, `hero`). Read its schema in `sections/<type>.liquid` (`{% schema %}`) to get setting ids.
3. **Countdown**: search `sections/` for "countdown" or "timer". Dawn has none: then skip it and say so; don't add
   third-party code for a short campaign.
4. **Colours**: Dawn-family themes keep `color_schemes` in `settings_data.json` (`current.color_schemes.<id>.settings`:
   background, background_gradient, text, button, button_label, secondary_button_label). Sections choose one with
   `color_scheme`. Sale badge colours are usually `sale_badge_color_scheme` / `sold_out_badge_color_scheme`.
5. **Badges**: search `snippets/` for "badge"; most themes show "Sale" automatically when a product has a
   compare-at price, which is product data.

Before writing any setting, confirm the id exists in that section's schema; an unknown id is silently dropped by
the editor or fails the push.
