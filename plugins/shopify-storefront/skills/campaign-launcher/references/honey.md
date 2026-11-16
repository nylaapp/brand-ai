# Honey theme (Archer Commerce, v11): campaign surfaces

Checked against Honey 11.0.2. Honey is not a Dawn fork for colours: it has five fixed colour groups, not
`color_schemes`. Sections pick a group with a `background` select.

## Colour groups (config/settings_data.json → current)

| Group (editor label) | Section `background` value | Settings |
|---|---|---|
| 1 | `main-background` | color_primary_background, color_primary_text_1, color_primary_text_2, color_primary_button, color_primary_button_text, color_errors_1 |
| 2 | `alt-background` | color_alt_background_1, color_accent_1_text_1, color_accent_1_text_2, color_alt_button_1, color_alt_button_text_1, color_errors_2 |
| 3 | `alt-background-2` | color_alt_background_2, color_accent_2_text_1, color_accent_2_text_2, color_alt_button_2, color_alt_button_text_2, color_errors_3 |
| 4 | `alt-background-3` | color_alt_background_3, color_accent_3_text_1, color_accent_3_text_2, color_alt_button_3, color_alt_button_text_3, color_errors_4 |
| 5 | `background-modal` | color_background_modal, color_modal_text_1, color_modal_text_2, color_modal_button, color_modal_button_text, color_errors_5 |
| Sale | `alt-sale` | sale_color (sale price text), promo_tag_background, promo_tag_text |

Other badge colours: color_notification / color_text_notification (in-stock badge).

## Announcement bar (sections/header-group.json → sections.announcement-bar.settings)

`text` (richtext, `<p>...</p>`), `link` (url), `background_color`, `text_color` (hex, not a colour group),
`font_size` (range), `font_type` (heading-font | body-font | button-font | accent-font), `font_style`
(none | all_caps), `dismiss_button`. Only one bar; no rotating messages. Its colours are hard-coded hex, so check
they come from the brand palette.

## Hero

- `hero-video` section: settings `video` (`shopify://files/videos/...`), `fallback_image`, `image_height`,
  `show_scrim`, `scrim_lightness`, `content_aligment` (sic), `vertical_position`, `horizontal_position`,
  `transparent_header`. Blocks: `heading` (heading, subheading, font_size, font_color) and `buttons`
  (button_label_1, button_link_1, button_label_2, button_link_2, font_size, button_color, font_button_color).
- `hero-image` section: same idea with `custom_background_image`. A disabled hero (`"disabled": true`) is the
  owner's previous campaign: leave it disabled, don't delete it.
- Heading and button colours are hex per block. Keep them readable over the media (scrim on, or brand light colour).
- **Vertical (phone) videos break the desktop hero.** `hero-video` sets its height from the video's own aspect ratio
  (`padding-bottom: 100% / ratio`); `image_height` is only a mobile min-height (under 768px). A 9:16 video makes the
  hero about 1.8x the screen width tall on desktop (2,500px+ at 1440px). Stock Honey has no setting for it. First check
  whether the project's `sections/hero-video.liquid` has the Nyla settings `desktop_height_mode` / `desktop_height` /
  `desktop_video_focus` (see the project's `THEME-SPECIFICS.md`); if so, set `desktop_height_mode: "fixed"`,
  `desktop_height: 75`, `desktop_video_focus` 50 to 65. Otherwise check the video's `aspect_ratio`; if it's below 1, add
  section Custom CSS (`"custom_css"` on the section in `templates/index.json`):
  `@media screen and (min-width: 769px) { .hero-video:before { padding-bottom: 0; } .hero-video { height: 75vh; min-height: 520px; max-height: 820px; } .hero__media-custom-video { object-position: 50% 60%; } }`
  and tune `object-position` so the product stays in frame. Mobile keeps the full vertical video. Tell the owner a
  landscape cut would look sharper on desktop (a 606px-wide video is upscaled about 2.4x at 1440px).

## Countdown section (sections/countdown.liquid)

```json
"countdown_<id>": {
  "type": "countdown",
  "blocks": {
    "content_<id>": {"type": "content", "settings": {"title": "...", "text": "<p>...</p>", "button_label": "...", "button_link": "shopify://collections/<handle>", "content_align": "center"}},
    "timer_<id>": {"type": "timer", "settings": {"end_date": "2026-11-17", "end_time": "23:59"}},
    "done_<id>": {"type": "content_on_complete", "settings": {"title": "...", "text": "<p>...</p>"}}
  },
  "block_order": ["content_<id>", "timer_<id>", "done_<id>"],
  "settings": {"background": "alt-sale", "hide_timer": false, "padding_top": 44, "padding_bottom": 44}
}
```

`end_date` format yyyy-mm-dd, `end_time` hh:mm 24-hour, store time zone. `background` options: main-background,
alt-background, alt-background-2, alt-background-3, background-modal, alt-sale. Add the id to `templates/index.json`
→ `order`, after the hero.

## Product countdown and badges (store data)

- Product page countdown: block `countdown` inside `templates/product.json` → `product-information` (settings
  `countdown_title`, `background`). It shows only for products whose metafield `theme.countdown_date` is set
  (date-time). Enabling the block is a theme change; setting the metafield is a product change (ask first).
- Product cards: theme setting `show_countdown` (Products → Product card), same metafield.
- Promo badges: theme setting `product_tags` (comma list, e.g. "On sale, Selling fast") with matching
  `product_tags_icons`; a product shows the badge when it carries a tag of the same name. Tags are product data.
