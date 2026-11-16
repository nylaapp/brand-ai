# Other themes: where colours and fonts live

- **Dawn family and most Online Store 2.0 themes:** `config/settings_data.json` → `current.color_schemes.<id>.settings`
  with `background`, `background_gradient` (a CSS gradient string, native gradient support), `text`, `button`,
  `button_label`, `secondary_button_label`, `shadow`. Sections pick one with `color_scheme`. Badge schemes:
  `sale_badge_color_scheme`, `sold_out_badge_color_scheme`. Fonts: `type_header_font`, `type_body_font`.
- **Older Dawn (v2 to v5) and Shopify's "Generated Data Theme":** no colour schemes; global `colors_accent_1`
  (solid button background), `colors_accent_2`, `colors_text`, `colors_background_1/2`, `colors_solid_button_labels`,
  `colors_outline_button_labels`. If `settings_data.json` has `"current": "Default"` (a preset name, not an object),
  the active values live in `presets.Default`: copy that preset into `current` as an object, then change values there
  (tested 2026-11-13 on the dev store; the editor does the same on first save).
- **Older or vendor themes:** read `config/settings_schema.json`; list every `type: color`, `color_background` and
  `font_picker` setting with its label, then map roles as in SKILL.md Step 2.
- Section-level colours: search `templates/*.json` and `sections/*.json` for `#` hex values (find_colors.py does
  this) and for settings named like `*color*`, `*background*`.
- Section-level custom CSS (`"custom_css": [...]` on a section in a JSON template) works on every OS 2.0 theme for
  effects the settings don't offer, such as a gradient on a theme without `background_gradient`.
