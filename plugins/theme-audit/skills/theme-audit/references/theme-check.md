# Theme Check lane

Theme Check is Shopify's own checker for theme code. It reads every file in the theme copy, so it
runs **once per audit for the whole theme**, not once per page. It does two jobs here:

1. **An audit lane**: what in the theme's code is broken, slow or out of date.
2. **A safety net**: after every fix, no new problem may appear (`SKILL.md` section 0).

## 1. Run it

In the theme copy's folder, with the theme's own `.theme-check.yml` if it has one (don't create or
edit that file):

```bash
shopify theme check --path <theme folder> -o json > <scratch>/theme-check-baseline.json
node <skill>/scripts/theme_check_summary.mjs <scratch>/theme-check-baseline.json > <scratch>/theme-check-baseline.summary.json
```

Never use `--auto-correct`: it rewrites files across the whole theme without a plan.

The summary groups offenses by check and marks two kinds:

- `broken: true`: something doesn't work (a Liquid syntax error, a missing file or snippet, an
  invalid section schema, an unknown filter). These come first in the report.
- `speed: true`: something slows pages or makes them jump (images without width and height,
  scripts that block the page, files hosted outside Shopify, oversized theme assets, deprecated
  lazy-loading libraries, preload and preconnect problems, heavy Liquid loops).

## 2. Decide what to fix

Theme Check findings are about code, so there's no score to chase. Choose:

| Kind | Fix in this pass? |
|---|---|
| `broken`, in a file used by a page in scope | yes, when the fix is local and obvious (a missing `endif`, a renamed snippet, a missing translation key in the default locale) and changes nothing a visitor sees on a page that works today |
| `broken`, elsewhere in the theme | report; offer it as a follow-up |
| `speed`, in a file used by a page in scope | yes, using the fix table in `performance.md` section 3; it must pass the same visual proof |
| `speed`, elsewhere | report |
| Deprecated tags, filters or fonts (`DeprecatedTag`, `DeprecatedFilter`, `DeprecatedFonts*`) | report as a planned upgrade; the replacement can render differently |
| Style and housekeeping (`UnusedAssign`, `OrphanedSnippet`, `VariableName`, `LiquidFreeSettings` and similar) | report as a count only; never fix in this pass |
| Anything in files the theme vendor ships and updates (core scripts, base styles) | report; edit only on the person's yes, with a comment saying what and why |

Find which files a page uses by following its template's sections, their snippets and the layout,
rather than guessing from names.

## 3. After every fix

Run the check again and compare with the baseline:

```bash
shopify theme check --path <theme folder> -o json > <scratch>/theme-check-now.json
node <skill>/scripts/theme_check_summary.mjs <scratch>/theme-check-now.json <scratch>/theme-check-baseline.json
```

- `new_offenses` must be **empty**. Anything there was caused by the edit: fix or undo it.
- `fixed_offenses` should list exactly the offenses the plan said it would fix. Anything else
  disappearing is a surprise worth a look (a file may have been deleted or emptied by mistake).

## 4. In the report

One short table: total offenses before and after, broken and speed counts, then the broken and
speed checks one per row (check, plain-language meaning, count, files, fixed or not and why).
Housekeeping goes in one line ("42 style findings, left as they are").
