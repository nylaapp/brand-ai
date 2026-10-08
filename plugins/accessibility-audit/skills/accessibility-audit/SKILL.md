---
name: accessibility-audit
description: "Score a Shopify theme's pages with the Lighthouse CLI (accessibility), classify every failing audit, propose minimal fixes, and after approval apply them and re-score until the page hits 1.00. Use whenever the user says \"score this page\", \"run Lighthouse\", \"accessibility audit\", \"check accessibility on the product page / about page / collection page\", \"get this to 100%\", \"fix the a11y score\", or asks to improve Lighthouse accessibility on any page template, even if they don't say Lighthouse. Fixes are additive only (aria attributes, roles, hidden labels, blank-value guards, a minimum contrast nudge) and never change layout, styling or copy. Never pushes to the live theme."
---

# Accessibility audit (Lighthouse CLI, classify, fix, re-score)

## Effort (read before starting)

About 15 to 40 minutes per page template with a handful of findings, mostly waiting on Lighthouse runs. Estimate, not yet measured. Stop and tell the person if a pass passes 90 minutes.

Use this whenever someone asks for a Lighthouse accessibility pass on a Shopify theme ("score the product page", "run accessibility on these templates", "get this to 100%").

**Goal: a higher score without moving anything a visitor or the store owner can see.** The owner judges "did anything change" by eye, so this is a trust contract: why each rule below exists is to keep that trust.

If the project has its own instructions file (for example `AGENTS.md` or `CLAUDE.md`) with safety rules or invariants, read it first and follow it; it outranks this skill.

## 0. Non-negotiables

- **No layout, styling or content changes.** A fix may add an `aria-*` attribute, a `role`, a visually-hidden label, a guard around a blank or broken dynamic value, or nudge a colour's contrast by the minimum needed. Never move, resize, reword or restyle. If a real fix needs a visible change, stop and ask; don't reinterpret "no changes" to permit it.
- **Never push to the live theme** (`shopify theme push --allow-live` or `--publish`). Pushing means the unpublished draft theme named in the project's theme config, unless the owner explicitly asks for live and confirms in chat.
- **Don't edit shared, vendor or base theme files** (global stylesheets, the theme's core scripts, shared colour-scheme tokens). If it's unavoidable, keep the edit minimal, mark it with a comment saying what and why, and log it.
- **`shopify theme check` must equal baseline** before and after every edit. Take a clean baseline run first; don't trust a remembered number. A changed count means something broke.
- **Verify every fix on the rendered page**, never from the code alone. Reading `document.querySelector(...).getAttribute('role')` on the running page is verification; "I added the role" is not.
- **Verify no regression on the live render**, not by reading the diff.
- Never enter credentials or 2FA codes in a browser. The person signs in themselves.

## 1. Resolve a real 200 URL per template

Lighthouse won't audit non-200 responses. For each page template:

1. Look for a Shopify Page that uses the template (read-only GraphQL): `query { pages(first: 50) { nodes { handle title templateSuffix } } }`, and paginate past 50 so no page is missed.
2. Confirm it is published: `query { page(id: "gid://shopify/Page/...") { handle templateSuffix isPublished } }`. `isPublished: false` is why it returns 404.
3. If it is unpublished, publish it only if every other requested page already follows that pattern. Publishing is a real store write: state it plainly in the summary and get the person's OK first.
4. If no Page exists at all, stop and tell the person (it's a content decision).
5. Confirm the status: `curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:9292/pages/<handle>"`. Product, collection and home templates use their normal routes.

## 2. Baseline (mobile and desktop, accessibility only)

Run against the local dev server (`shopify theme dev`, usually `http://127.0.0.1:9292`), not the password-protected preview domain: that injects Shopify's preview-bar iframe (it always fails `frame-title` and can't be fixed in the theme) and adds noise. Save reports to the session's scratch folder. `npx lighthouse` installs itself on first use.

```bash
npx lighthouse "<url>" --output=json --output-path=<scratch>/baseline-<handle>-mobile.json \
  --only-categories=accessibility --chrome-flags="--headless=new" --quiet
npx lighthouse "<url>" --output=json --output-path=<scratch>/baseline-<handle>-desktop.json \
  --only-categories=accessibility --preset=desktop --chrome-flags="--headless=new" --quiet
```

Extract every audit with a score below 1 and a weight above 0 from `categories.accessibility.auditRefs`, keeping the full `details.items[].node` (selector, snippet, explanation, node label). The score alone isn't actionable.

## 3. Classify every finding into exactly one bucket

### 3a. Skip (report with evidence, don't fix)

- `frame-title` on the preview-bar iframe: Shopify's own bar, only on the preview domain.
- Elements that come from outside the theme: third-party popups, marketing or chat widgets, or markup from another site. Before calling something third-party, confirm all three: (1) searching the theme's files for the element's class or attribute finds nothing; (2) the element is absent from a normal authenticated page load (it only appears in Lighthouse's fresh crawl); (3) the page's script list (`Array.from(document.scripts).map(s=>s.src)`) includes a known third-party tool.
- Merchant content the theme only renders (for example a `heading-order` failure from an `<h4>` inside a product description). If the flagged text isn't in the repo it's live store data: flag it for the owner. Don't reformat it or globally renormalise rich-text headings.

### 3b. Fix, choosing the technique deliberately

| Finding | Safe fix | Do not |
|---|---|---|
| `aria-prohibited-attr` (an `aria-label` on a bare `<div>`) | add the correct `role` (often `role="status"` for a loading placeholder) | remove the label |
| `aria-required-children` (a `role="tablist"` whose children lack `role="tab"`) | add `role="tab"` and `aria-selected` where the buttons are created; first check sibling components (near-identical dot or pagination components often exist) and match whichever already does it right | change the container role |
| `link-name` or `button-name` (icon or image only) | a visually-hidden text span (copy the pattern the theme already uses, for example in its product card) or an `aria-label` mirroring the text a hidden or responsive state would show | add visible text, change the icon |
| `link-name` from a blank dynamic setting (`<a href="tel:">`) | guard the block: `{% if block.settings.number != blank %}` | fill in placeholder text, delete the merchant's empty block |
| `color-contrast` | measure first (section 4), then nudge by the minimum; reuse a "muted but legible" opacity the theme already uses before computing a new value | guess, round up "to be safe" (that's a style change), or edit a shared colour-scheme token globally |

If a fix touches a shared token, don't edit the token unless every usage is checked. Scope an override to the flagged selector instead.

## 4. Measuring contrast

Muted text is usually alpha-blended (`opacity`, `rgb(var(--color-foreground-rgb) / X%)`, `color-mix(...)`) over a scheme-dependent background. The number in the CSS says nothing about rendered contrast. Use `references/contrast.md` for the method and the helper functions. In short: sanity-check against the report's own numbers, find the smallest opacity that clears the threshold with headroom (4.5:1 for normal text, 3:1 for large text), check every colour scheme the component can render in, and verify on the live page.

## 5. Present the plan and WAIT for approval

Show a table: page, audit, element or selector, bucket (skip or fix), exact edit (file, before to after), and reason. List skipped items with their evidence. Make no edits until the person says go; these files render on live pages.

## 6. Apply fixes, verify each on the page

Apply each approved edit and read back the running page (attribute values, computed colours). Run `shopify theme check` and compare it to the baseline.

## 7. Re-run and confirm 100%

Repeat step 2 for every page and both form factors against the dev server. Every one must score `1.0`; if not, return to step 3 for what remains. Don't stop at "improved". Then prove nothing visibly moved:

- Blank-value guard: every real (non-empty) instance keeps the same `innerText` and the same count as before.
- Label or role: image source, position and size unchanged; only accessibility-tree attributes changed.
- Contrast: visible text and position unchanged; only the colour moved, by the computed minimum.

## 8. Push, verify, re-check deployed (only after the person approves pushing)

1. `shopify theme check` must match the pre-pass baseline exactly.
2. `shopify theme push --theme <draft theme id> --only <exact touched files>`. Never a bare push: the branch may carry unrelated work in progress.
3. `shopify theme pull` the same files to a scratch folder and `diff` them: they must be byte-identical to local. That is the proof, not the CLI's "success" message.
4. Re-run Lighthouse on the deployed preview domain for every page and both form factors. Say plainly that this is the Lighthouse CLI engine, not the Chrome extension UI.
5. Expect lower scores than local (the preview bar, third-party scripts). Don't reopen step 3 to chase the gap, but confirm every new finding lands in bucket 3a with evidence rather than assuming it's third-party noise.

## 9. Log

Append an entry to the project's QA log (for example `design-qa.md`, or create one): baseline scores, every fix (file, before and after, why), the not-fixed list with reasons, re-run scores, push and pull verification, and deployed-domain numbers with an explanation. Write "not run" for anything not run.

## Final report

Per page, a before and after row (mobile and desktop), then: fixes applied, items skipped and why, `theme check` before and after, and anything needing the store owner (merchant content, unpublished pages, store writes made).

## Checklist

- [ ] Real, published, 200 URL for every page
- [ ] Baseline: mobile and desktop, accessibility only, on the dev server
- [ ] Every failing audit classified skip or fix, with a reason
- [ ] Plan approved before any edit
- [ ] Fixes additive, or a measured-minimum colour nudge only
- [ ] Contrast verified on the live composited page
- [ ] `theme check` unchanged
- [ ] 1.0 on every page, both form factors, locally
- [ ] Live regression check passed
- [ ] Pushed to the draft theme only, with `--only` touched files; pulled and diffed identical
- [ ] Deployed-domain gaps traced to confirmed non-theme causes
- [ ] QA log entry written
