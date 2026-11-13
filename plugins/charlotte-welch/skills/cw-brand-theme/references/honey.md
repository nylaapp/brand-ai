# Honey theme (Archer Commerce, v11): colours, fonts, gradients

Checked against Honey 11.0.2.

## Colour groups (config/settings_data.json → current)

Five fixed groups; sections choose one with their `background` select. Each group has background, two text
colours, button, button text and error text.

| Group | Section `background` value | Background | Text 1 / Text 2 | Button / Button text | Error |
|---|---|---|---|---|---|
| 1 | `main-background` | color_primary_background | color_primary_text_1 / color_primary_text_2 | color_primary_button / color_primary_button_text | color_errors_1 |
| 2 | `alt-background` | color_alt_background_1 | color_accent_1_text_1 / color_accent_1_text_2 | color_alt_button_1 / color_alt_button_text_1 | color_errors_2 |
| 3 | `alt-background-2` | color_alt_background_2 | color_accent_2_text_1 / color_accent_2_text_2 | color_alt_button_2 / color_alt_button_text_2 | color_errors_3 |
| 4 | `alt-background-3` | color_alt_background_3 | color_accent_3_text_1 / color_accent_3_text_2 | color_alt_button_3 / color_alt_button_text_3 | color_errors_4 |
| 5 | `background-modal` | color_background_modal | color_modal_text_1 / color_modal_text_2 | color_modal_button / color_modal_button_text | color_errors_5 |

Badges and sale: `sale_color` (sale price text, on group 1 background), `promo_tag_background` / `promo_tag_text`,
`color_notification` / `color_text_notification` (in-stock badge). The `alt-sale` section background uses the promo
tag colours.

Group 1 is the page itself (product pages, cart, collection grid), so its contrast matters most. Before changing a
group, check which sections use it (`grep '"background": "alt-background-2"' templates/*.json sections/*.json`):
the header and footer often use an alternate group, so changing it repaints them too.

## Hard-coded colours in sections

These are hex values per section, not groups, so global changes miss them:
- `sections/header-group.json` → announcement-bar: `background_color`, `text_color`; header: `active_color`,
  `highlight_color`.
- Hero sections (`hero-video`, `hero-image`): heading block `font_color`; buttons block `button_color`,
  `font_button_color`.
- `multicolumn`: `gradient_background` (a CSS gradient string) and `gradient_text_color`.
- Product gallery border: `product_gallery_border_color`.

## Gradients

Honey's colour groups are solid colours. Options, best first:
1. `multicolumn` has a native `gradient_background` setting: `"linear-gradient(180deg, #152E38 11%, #111B18 50%, #104F4C 100%)"`.
2. Any other section: section-level custom CSS (theme editor → section → Custom CSS), stored in the template JSON as
   `"custom_css": ["<rule>", ...]` on that section. Rules are scoped to the section automatically, e.g.
   `".hero-video-section, .countdown-section { background: linear-gradient(180deg, #152E38 11%, #111B18 50%, #104F4C 100%); }"`.
   Check the section's outer class in its `.liquid` file. Pick the section's colour group so the text is light.
3. The header's `custom_background: "gradient"` option is NOT a brand gradient: it only fades the submenu into the
   group background. Don't use it for brand gradients.

A design-tool angle of -90° (top-to-bottom stops in a brand book) is `linear-gradient(180deg, ...)` in CSS. Keep
the stop percentages from the guide.

## Fonts (Typography)

`type_header_font`, `type_body_font`, `type_button_font`, `type_accent_font` (font_picker handles such as
`lora_n4`), scales `heading_scale`, `body_scale`, `button_scale`, `accent_scale`, `header_line_height`,
`uppercase_headings` (none | all_caps), `uppercase_product_title`, `font_subheading_style` (heading | body),
`font_price_style` (heading | body). The layout loads all four with `font_face`, so only library handles work in
settings; a non-library font needs a `<link>` or `@font-face` plus CSS overriding `--font-heading-family` /
`--font-body-family` (owner's licence required).
