---
name: page-content-studio
description: >-
  Make a change to a Shopify page, or build a new one: copy, an image, a link, a section's
  settings, a section's layout, which sections appear and in what order, or a whole new page
  (homepage section, landing page, campaign, service or region page). Also acts on the
  recommendations a page-audit picked, reading them from PAGE-AUDIT.md. Brand-agnostic, built for
  the Site Editor: the marketing, content or ops person who asks for page changes but isn't
  necessarily a developer. Use when the user names a change or a page to build -- "swap the image
  on", "change this section", "fix the copy on", "move this section up/down", "make a landing page
  for X", "build a page for X", "recreate this page from the live site", or points at a live or
  preview URL and describes something to change. When the ask is open-ended -- "improve the
  homepage", "what's wrong with this page", "what should we fix" -- it hands off to page-audit
  first. Not for blog posts (use shopify-blog-writer or shopify-blog-rewrite) and not for
  accessibility audits (use accessibility-audit).
---

# Page content studio

The front door for changing or building a Shopify page. It decides which job a request is,
hands open-ended "improve this page" requests to `page-audit`, and carries out named changes
and new builds on a draft theme without handing off partway through. Brand-agnostic; brand
facts come from `BRAND.md` and `BRAND-VOICE.md`, never invented and never hardcoded here.

## Which job is this?

| The person says... | Do this |
|---|---|
| "Improve the homepage", "what's wrong with this page", "what should we fix", "is this page any good", or any ask with no change named | **Hand off to `page-audit`** (invoke it with the Skill tool, passing the page and anything already known). Come back here only for the rows they pick. |
| Names a change: "swap the hero image", "move pricing above the FAQ", "fix the typo on" | Continue here: Steps 1 to 5. |
| "Build a page for X", "recreate this page from the live site" | Continue here: Steps 1, 2, 3b, 4, 5. |
| "Do row HOME-02", or points at a `PAGE-AUDIT.md` | Read the picked rows from the file (see below), then Steps 2 to 5. |
| Only wants to check a change that was already made | Step 4 (verify) on its own; no edits. |
| Unclear | Ask one short question: "Do you already know what you want changed, or should I review the page first?" |

**Acting on an audit.** If `PAGE-AUDIT.md` exists for this site (rules in
`../page-audit/references/audit-file.md`), read its recommendation rows. Work only on rows
marked `picked` that this theme owns. Carry each row's baseline number forward, and when the
change is verified set that row to `done` and add a changelog line. Never change anything
else in the file, and never act on a row nobody picked.

## References

- `../page-audit/references/intake.md`: brand and theme context, page and type, the goal check.
- `../page-audit/references/page-type-playbook.md`: what each page type is for and the
  checks a good one passes. Use its must-haves to plan a new page (Step 3b).
- `../page-audit/references/observation-recipes.md`: how to observe a rendered page. Use it
  in Step 4.
- `references/qa-entry-format.md`: the log entry format (Step 5).

## Who this is for: the Site Editor

The person asking is usually a **Site Editor**: someone on the client's marketing, content or
operations side, responsible for how the live site looks and reads, but not necessarily a
developer. They describe what a *visitor* sees ("the homepage photo is outdated", "we need a
landing page for the new treatment", "move the pricing above the FAQ"), not where it lives in
the theme.

- **Plain language by default.** Say "section" or "template" and explain it in one short
  clause the first time ("the hero -- the big banner at the top"). Don't drop into file paths
  or schema terms unless they're clearly comfortable with them.
- **You translate the request into the technical target** (Steps 1 to 3); they describe what
  they see, you find or plan what controls it.
- **Narrate before acting**, in a sentence they'd understand ("I'll swap the homepage hero
  image and leave everything else as-is").
- **Flag trade-offs in plain terms.** "This section is also used on your contact page --
  changing it there too, or just here?"
- **Explain draft vs. live the first time it comes up**: "this updates the draft/preview
  first; nothing visitors see changes until you say go."

## Why update and build are one skill

Creating a new page and updating an existing one share almost everything that matters:
the same brand and theme facts, reusing sections before building new ones, verifying against
the live render instead of the source, never pushing live without sign-off. Step 2 is the fork
in the road partway through a single pass, not a hand-off.

## Step 0: Brand and theme context

Follow section 1 of `../page-audit/references/intake.md`: resolve `BRAND.md`,
`BRAND-VOICE.md` and `design.md`, handle a partial set, and read the store repo's own
engineering rules (`AGENTS.md` or `CLAUDE.md`). In short:

- **Brand files missing:** stop and offer brand-capture before writing any brand-facing copy.
  A pure structural change with no new copy (reordering sections, a settings toggle) can
  proceed if the Site Editor would rather not wait; say so and flag that copy should wait.
- **Visual values** come from `design.md` when it exists, else the store repo's visual spec or
  the theme's settings. Never invent a hex, font, size or radius.
- **Theme rules** (where changes go, naming, file ownership, verification gates) live in the
  store's repo. Read them fully; if they're missing, say which gates you can't confirm.

## Step 1: Understand the request

Ask short, plain, multiple-choice questions until these are answered. If the goal isn't
obvious, ask the one-line goal check from `../page-audit/references/intake.md` section 3 and
note any limits that must not change.

- **Which page, in their words, and what type is it?** Resolve it to an actual template;
  don't assume `index` means the homepage, check.
- **New or existing?** If they're not sure, Step 2 settles it.
- **What should stay exactly the same?** Default: everything else stays visually identical.
  If the request would touch something they didn't mention, stop and ask in plain terms
  rather than quietly widening it.
- **Is there a reference** (a live URL to match, inspiration, brand pages to stay consistent
  with), or is this from scratch?
- **How urgent is this?** Even a live typo goes through draft staging and verification; say
  so and explain the risk of skipping rather than just refusing.

## Step 2: Resolve the real target -- this decides the path

1. Confirm whether the page already exists: check the Page in Admin (or the `templates/`
   folder for a template-level question) rather than trusting the name used in chat.
2. **Exists -> this is an update.** Go to Step 3a.
3. **Doesn't exist -> this is a new build.** Go to Step 3b.
4. If "update the live page" is the ask, confirm it's actually published; an unpublished page
   can look fine locally and still 404 for a visitor.
5. Resolve a real local URL to test against (`shopify theme dev`, not the password-protected
   preview domain, which injects its own preview-bar UI and is noisier signal).
6. If nothing matches what the Site Editor described, say so and ask for the actual URL or
   name rather than guessing the closest match.

## Step 3a: Updating an existing page -- find what controls it

A request like "update the headline on the homepage" could live in a section's schema
default, a section's setting (set per page), a locale file, or, if it's merchant-authored
content like a product description, nowhere in the theme at all.

1. Find which section renders that part of the page (walk the template's section list,
   matching visually against the live or dev render; don't guess from the name).
2. Check whether a setting already exists for what's being asked. Reusing an existing setting
   beats adding a new one; adding a new setting beats touching markup or logic.
3. If the content is rendered from outside the theme (product description, metafield,
   Admin-authored data), say so plainly -- "that text comes from the product page in Admin,
   not this page's design; here's where to edit it" -- rather than editing Liquid that won't
   change what they see.
4. Check whether the same visual change is needed elsewhere (a section reused across several
   pages); flag this before changing it, not after.
5. Classify the change and pick the narrowest safe technique:

   | Kind of change | Safe technique | Avoid |
   |---|---|---|
   | Content (text, image, link, price) | Edit the value in the page's setting, or point to the theme editor or Admin if the Site Editor can self-serve it | Hardcoding the new value into markup where a setting should hold it |
   | Settings (existing toggle or variant) | Change the setting value | Editing the section file to "handle it in code" when a setting already exists |
   | Section code (no setting covers it) | Add the new setting plus minimal markup; match the pattern a sibling section already uses | Inventing a new pattern when the theme already has one |
   | Structure (add, remove, reorder) | Edit the page's section list only | Deleting a section or block file another page still references |
   | Visible beyond what was asked | Stop, name the trade-off in plain terms, ask | Silently "improving" something nearby |

Then go to Step 4.

## Step 3b: Building a new page -- plan it from sections, reuse first

1. Confirm the page name and URL handle; check it doesn't clash with an existing template.
2. If there's a reference (a live URL): capture desktop and mobile widths, scroll slowly so
   lazy content loads, list every section top to bottom including ones with no text, read
   computed values (container, padding, gaps, font, size, weight, colours, radius) rather than
   eyeballing them, and capture hover, focus and disabled states. If no rendered view is
   possible, say plainly it's blocked and name what failed; don't guess.
3. No reference: start from the playbook section for this page type
   (`../page-audit/references/page-type-playbook.md`): its must-have checks decide which
   regions the page needs and in what order, with the primary action in the first screen.
   Take copy facts from the brand files and visual values from `design.md` (Step 0).
4. For each region, choose in this order: (1) an existing section that already fits, (2) the
   same section with one small new setting, (3) a native base-theme section or block, (4) a
   new section, only when the layout is genuinely different. One section per visual region;
   blocks are for repeated items inside one region.
5. Show the Site Editor a plain-language table: region, what it'll use, why. Get a yes before
   building.
6. Build the template: add every section, list all ids in the right order. No hardcoded
   colours, fonts or text a setting could hold. Check every number against the schema's
   min and max, since a bad value can reject the whole push. Leave image pickers blank if
   rights aren't confirmed; never link to a reference site's own CDN.
7. CSS only if the existing sections truly can't do it, following the store repo's cascade,
   scoping and breakpoint rules. A new font needs a licence check with the Site Editor first;
   never swap in a lookalike silently.

Then go to Step 4.

## Step 4: Verify -- live, not from the diff

Reading the source you just wrote is not verification; loading the rendered page is. Follow
`../page-audit/references/observation-recipes.md` (real viewport, theme id confirmed, slow
scroll, overlays noted).

1. Load the page in `shopify theme dev` or the draft preview. For an update, compare against
   what it looked like before (a screenshot, saved HTML or the section inventory from before
   you started). For a new page, check the fresh build and, if there's a reference,
   side-by-side against it.
2. Confirm the thing asked for actually changed or exists on the rendered page, not just that
   the source now says so.
3. Confirm nothing *else* visibly moved. For an update, every other section keeps its
   position and size. For a new page, the theme editor's add, remove, reorder and duplicate
   controls work, each setting changes something visible, and empty fields and very long
   headings don't break layout.
4. Check every breakpoint and colour scheme the change could plausibly reach.
5. Run `theme check`: no new offenses; an update's count from before must be unchanged. A
   changed count means something broke; find it before continuing.
6. Accessibility baseline: one h1, no skipped heading levels, icon-only buttons have names,
   images have alt text, keyboard-only pass, contrast per colour scheme. This is a baseline,
   not the dedicated audit; for a full pass use `accessibility-audit`.

## Step 5: Push, verify, log

1. Push only to the unpublished draft or preview theme, scoped to the exact touched files;
   never a bare push that could carry unrelated work. Never push to the live theme without the
   Site Editor's explicit go-ahead, confirmed in chat.
2. Pull the same files back to a scratch path and diff; that is the proof the push landed, not
   the CLI's success message.
3. Re-check on the deployed preview domain. Small differences from local (the preview bar,
   third-party scripts) are expected noise; confirm rather than assume.
4. Log an entry (`references/qa-entry-format.md`, or the store repo's own QA log format if it
   names one): what was asked, what controlled it, what changed, what was verified, measured
   parity if there was a reference, and what the Site Editor still has to do. If the work came
   from `PAGE-AUDIT.md`, set the row to `done` and add a changelog line.
5. Give the Site Editor a short, plain summary: what changed or was built and where it's
   visible, what was checked, anything flagged but not done and why, and whether it's only on
   draft or preview or already live.

## Never

Do not invent a brand fact that isn't in `BRAND.md` or `BRAND-VOICE.md`. Do not widen a
content or settings fix into a code change when an existing setting would do. Do not touch a
shared base-theme file or token without checking every usage it affects. Do not delete or
rename a section or block file another page still references. Do not claim a visual check
passed without having loaded the rendered page. Do not push to the live theme without the
Site Editor's explicit, chat-confirmed go-ahead. Do not type a password or credential for the
person. Do not act on an audit row nobody picked. Do not recreate a reference page from a
text-only fetch -- a capture missing computed values and images isn't a capture. Do not call
something "matches the reference" without a measured parity table.
