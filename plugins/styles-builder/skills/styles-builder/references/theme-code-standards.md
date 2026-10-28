# Theme code standards: safe, reviewable, easy to update

For anyone changing a theme's code, settings or styles from `design.md`. The aim is a small, labelled
set of changes that a developer can review and that survives the next update of the starting theme.

## What is and isn't documented
- Documented by Shopify: modular templates, sections and blocks; simple merchant settings;
  performance; accessibility; version control.
- Not spelled out in Shopify's docs: CSS rules, how to avoid upgrade conflicts, whether to hand-edit
  `settings_data.json`. The rules below for those are this skill's recommendations, not requirements.
- Facts to design around: template and settings JSON files carry a header saying they are
  auto-generated and may be overwritten; and Horizon is updated by merging its upstream repository, so
  an edit to a file Horizon owns can conflict at the next update.

## Layers, in the order to try
1. A theme setting, changed in the theme editor or set in the settings data.
2. A design token (CSS custom property) overridden in the brand stylesheet.
3. A scoped component rule in the same stylesheet.
4. A new snippet, block or section with the brand prefix.
5. An edit to a file the starting theme owns, only when nothing above can do it.

## Rules
- **Additive first.** New files and new rules, prefixed (for example `brand-`), never reusing the
  starting theme's file names. One brand stylesheet and one `:root` block of tokens, each commented with
  the `design.md` section it came from.
- **Don't edit the starting theme's own files** (base CSS, JS, sections, snippets) to change a styling
  value. Override it from the brand stylesheet with a scoped rule.
- **If a base-file edit is unavoidable:** make the smallest change, fence it with a comment saying what
  and why and "remove if the theme provides this" (`BRAND:` ... `/BRAND`), and add it to the repo's
  register of base-file changes (create `CUSTOMIZATIONS.md` if there is none).
- **The settings schema is append-only.** New setting ids carry the brand prefix. Never rename, reorder
  or delete an existing id: saved merchant values are keyed by id. Add labels the way the repo does
  (locale keys or plain text) and keep `theme check` clean; a missing translation key is a common offence.
- **Settings and template JSON are written by the theme editor too.** Pull first, change only the keys
  needed, push only those files, and don't write them while someone is in the editor. For colour schemes
  prefer the editor route and pull the result. Follow the repo's rule on committing `settings_data.json`;
  if it is kept out of git, record the final values in `design.md` instead.
- **CSS conventions:** custom properties for tokens, namespaced BEM-style classes, selectors by class
  (never by a section's generated id), mobile-first with the theme's own breakpoints, no inline styles for
  tokens, and no `!important` unless documented with the reason.
- **Fonts and motion:** custom fonts as assets with `@font-face` and a documented licence; honour reduced
  motion.
- **One concern per commit,** on a branch named by the repo's pattern, with the files touched listed in
  the message. Don't commit anything the repo says to keep out of git.

## Leave a map for the next developer
Write an "Implementing this in the theme" section in `design.md`: for each token, the setting id or custom
property that carries it, where it is set, and which files were touched. Add the register entries and the
commit list. After the starting theme is updated, a developer can re-run the verify list and see exactly
what to re-check.

## Check before pushing
`theme check` count not higher than before; the diff touches no starting-theme file except the registered
ones; every new id and class is prefixed; no `!important` without a note; the rendered page matches the
baseline apart from the intended change.
