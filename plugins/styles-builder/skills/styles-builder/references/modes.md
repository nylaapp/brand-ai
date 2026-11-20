# Modes: fresh, established, completed

This skill never overwrites a brand look that already exists, and it runs only when the style is not built yet or is inconsistent. Before any change, settle
which of three modes the theme is in. The mode is found by measuring the staging theme, not asked, and it
decides everything after.

## Settle the mode (Step 0g)

Run `python scripts/theme_state.py detect <staging theme folder> --design <design.md>`. Where Python can't
run, read the same evidence by hand: compare `config/settings_data.json` with the defaults in
`config/settings_schema.json`, look for brand files (`assets/brand*`, `snippets/brand*`), filled custom CSS
settings, and the run marker below.

| Verdict | What it means | What the run does |
|---|---|---|
| **completed** | A run marker exists: the look was built before | Count the gaps: none means stop, change nothing; some means established mode on them. See "When it runs, and when it stops". |
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

## When it runs, and when it stops

It runs in exactly two situations, and otherwise leaves the theme alone:

1. **Not built yet:** the theme has no brand look. Fresh mode builds it.
2. **Built, but inconsistent:** a brand look exists and a measurement finds a gap (contrast, colours off the palette
   or near-duplicates, an extra font family, line height outside a readable range, a missing state). Established
   mode refines only those.

When it is built **and** consistent, it does nothing: it says so in one line and changes nothing. That is the
usual end state, so the skill is not something to run again and again.

**The marker.** When a run finishes (Step 6), write it: `styles_built: <date> (theme <id>, mode <mode>)` in
`design.md`'s front matter and `/* styles-builder: completed <date>, mode <mode> */` at the top of the brand
stylesheet. Either one means the look is **built**. It does not mean "never run again": `theme_state.py detect`
still counts the measured gaps. `next: nothing to refine` means stop; a gap count above 0 means show the gap
table and let the person pick rows.

**What starts it.**
- The person asks, in their own words ("run the styles builder", "fix the inconsistent styling", "refine the
  theme styles"). A rebrand or a new brand book is also a request.
- Another skill that has measured an inconsistency (page-audit, theme-audit, an editor skill) may hand it over
  with the gap named. The gap table is still shown and every row still needs the person's yes.
- It is not started by a passing mention, by `design.md` looking thin (that is brand-capture's add-design mode),
  or by a built and consistent theme.

**Full rebuild** (fresh mode on a theme that already has a look) only on a clear "start over" or "reset the
styling" in the person's words, confirmed once, naming what will be replaced. It never touches the live theme.

Update the marker's date and mode each time it makes changes. When there was nothing to refine, change nothing,
the marker included.
