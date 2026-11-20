# Modes: fresh, established, completed

This skill never overwrites a brand look that already exists, and it runs once. Before any change, settle
which of three modes the theme is in. The mode is found by measuring the staging theme, not asked, and it
decides everything after.

## Settle the mode (Step 0g)

Run `python scripts/theme_state.py detect <staging theme folder> --design <design.md>`. Where Python can't
run, read the same evidence by hand: compare `config/settings_data.json` with the defaults in
`config/settings_schema.json`, look for brand files (`assets/brand*`, `snippets/brand*`), filled custom CSS
settings, and the run marker below.

| Verdict | What it means | What the run does |
|---|---|---|
| **completed** | A run marker exists | Stop. See "Run once". |
| **fresh** | Styling settings are still the theme's own defaults (under 10 percent changed), no brand files, no custom CSS | Build everything: "Fresh mode". |
| **established** | A brand look is already set (25 percent or more of the styling settings changed, or brand files, or custom CSS) | Fill gaps only: "Established mode". |
| **ambiguous** | In between | Ask one question with both modes as options, "Fill gaps only (Recommended)" first. Never guess toward "fresh": a wrong "fresh" overwrites someone's work. |

Say the verdict and the evidence in one line ("Established: 31 of 93 styling settings differ from the theme's
defaults, and brand stylesheets are present.") and carry on.

## Fresh mode: apply everything

The theme has no brand look yet, so this is the full job (Steps 0.5 to 6): every token from `design.md` into
the theme's settings (colour schemes, type scale, spacing, radius, shadows, buttons, inputs, variant pickers,
motion, logo and favicon), the brand stylesheet for what no setting can hold (custom CSS, `@font-face` for
fonts that are not in Shopify's library, with the font-file ask), and, only if opted in, the section styling
(Step 7). Still never the live theme, and still reuse existing setting ids and layers in the order
`theme-code-standards.md` gives.

## Established mode: find holes, change only those

The brand look is the person's work. Do not re-apply `design.md` over it, do not re-map schemes, do not
rename, reorder or delete anything, and do not touch anything that is on-brand and consistent.

1. **Measure the gaps.** Run `python scripts/theme_state.py gaps <staging theme folder> --design <design.md>`
   and look at the rendered staging theme at desktop (1440x900) and mobile (375x812). A gap is something a
   measurement or the rendered page shows, never taste. The usual ones:
   - **Contrast:** any text and background pair below 4.5:1 (body) or 3:1 (large text), in every colour scheme,
     button and state.
   - **Inconsistent colour:** colours used that are not in `design.md`'s palette, and near-duplicates (two
     almost identical shades where one is meant).
   - **Inconsistent fonts:** a family or weight not named in `design.md`, more families than the brand uses,
     fonts written out in section code instead of the type settings.
   - **Line spacing and type:** line height outside a readable range (body about 1.4 to 1.8, headings about
     1.0 to 1.4), a type scale that skips or repeats a step, letter spacing that differs between like elements.
   - **Inconsistent spacing:** section padding and gaps that vary with no reason, the same component spaced
     differently on two templates, desktop and mobile out of step.
   - **Missing pieces:** states with no style (focus, disabled, error, unavailable), a setting still at the
     theme's default where `design.md` states a value and nothing else sets it.
2. **Show the table before writing anything:** gap · where · now · proposed · why. Every row has evidence (a
   ratio, a file, a screenshot). Anything you could not measure is a question, not a row. Wait for a yes; the
   person can strike rows.
3. **Change only the rows approved,** in the lightest layer that works (`theme-code-standards.md`: a setting,
   then a token override in the brand stylesheet, then a scoped rule). Add; do not replace. Where a value
   lives in the person's own custom CSS or settings, adjust that one value in place and note it; never rewrite
   the file or overwrite their other rules. Leave what the table did not name exactly as it was.
4. **Prove nothing else moved.** Compare the rendered theme against the baseline taken before (desktop and
   mobile): only the approved areas differ. Re-run `theme check`: the count is not higher.
5. **Summary.** What was found, what was changed (before and after), what was left alone on purpose, and the
   items needing the person's call. The optional section styling (Step 7) is skipped in this mode unless the
   person asks for it by name.

## Run once

When a run finishes (Step 6), write the marker so the skill does not run again by itself:

- In `design.md`'s front matter: `styles_built: <date> (theme <id>, mode <fresh | established>)`. This is a flat
  line like the others there.
- At the top of the brand stylesheet: `/* styles-builder: completed <date>, mode <mode> */`.

Either marker alone means **completed**. Then:

- **Never run again on its own.** Another skill asking for it (page-studio or page-audit finding design.md thin,
  brand-capture finishing) is not a request. Say in one line that styles-builder already ran on `<date>` and
  that you will run it again only if the person asks for it, then carry on with what was asked without it.
  A "thin design.md" is brand-capture's add-design mode, not this skill.
- **Run again only when the user says so,** in their own words in this chat ("run the styles builder again",
  "rebrand the theme", "redo the styling"). Then use **established mode** (gaps only), because the theme now
  has a brand look. Only a clear "start over" or "reset the styling" in their words (confirm it once, naming
  what will be replaced) uses fresh mode, and it still never touches the live theme.
- A new brand book or a new brand (a rebrand) is a new source the person supplies: it counts as a request to
  run again, with the same rules.
- Update the marker's date and mode when it runs again.
