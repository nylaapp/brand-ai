---
name: page-edit-content
description: >-
  Edit the content of an existing Shopify page without changing how it looks: words, headlines,
  subheads, button labels, link targets, images and their alt text, FAQ entries, testimonial quotes,
  announcement text, and SEO fields set in the theme. Finds where the text actually lives (a section
  setting, the page template, a locale file shared by many pages, or content that belongs in the
  store admin and not the theme), keeps new copy within the brand files and flags claims for a
  fact-check, captures a baseline, edits a local working copy, verifies on the rendered page, and
  pushes only the touched files to the theme the person chose (a draft unless they say live). Also
  acts on audit rows a person picked in PAGE-AUDIT.md. Brand-agnostic, written for the Site Editor.
  Use for "change the headline to", "fix the typo on", "swap this image", "update the button label",
  "make this link go to", "do row HOME-02" when the row is about words, images or links. Not for
  layout, spacing, colour, type or section order (use page-edit-design), a new page or section
  (page-create), open-ended "improve this page" (page-audit), blog posts (blog-generator) or
  accessibility audits (accessibility-audit).
---

# Page edit: content

Change what an existing page **says and shows** (words, images, links) and nothing about how it
looks or is laid out. The skill finds where the content lives, captures a baseline, makes the edit
in a local working copy, proves it on the rendered page, and puts only the touched files on the
theme the person chose (a draft unless they say live). The live theme needs their explicit yes
before any edit and again before the push.

```
1. Context -> 2. Understand the request -> 3. Resolve the target and working copy ->
4. Find where the content lives -> 5. Capture the baseline -> 6. Show the exact change ->
7. Edit the working copy -> 8. Verify -> 9. Ship to the theme -> 10. Hand back
```

## Rules

- **Working copy first, on the theme the person chose.** Never push from the working copy except
  through the ship step. The theme is asked once and remembered (`theme-target.md`); a draft is
  recommended. The live theme needs an explicit yes before the first edit and again before the push,
  every run (`theme-target.md`, `ship-to-draft.md`).
- **Content only.** If the request also changes layout, spacing, colour, type or section order,
  split it: do the content here and hand the design part to `page-edit-design` as its own change.
- **Narrowest change.** Edit the value in the setting that holds it. Never hardcode text into
  markup where a setting should hold it, and never widen a content fix into a code change.
- **Capture the baseline before the first edit**, so "nothing else changed" can be proved and the
  edit reverted exactly.
- **New copy comes from the brand files or from the person.** Never invent a claim, number,
  credential, price or proper noun, and never copy one from memory. Health, result and "best"
  wording, and any figure, goes through `content-fact-check` before it ships.
- **Don't change tracked links** (booking, checkout) unless that is the request, and say so when it
  is; the verify step compares the link map.
- **Images:** use files already in the store or theme. Don't upload to the store's media library
  for the person, and leave an image picker blank if rights aren't confirmed. Always set alt text
  that describes the image.
- **Never delete or rename** a section or block file another page references, and never touch a
  shared base-theme file without checking every usage.
- **Never type a password or credential** for the person.
- **Hard limits win.** What the person said must not change overrides the request.

## Who this is for

A Site Editor on the marketing, content or operations side: they describe what a visitor reads ("the
homepage headline is out of date"), not where it lives in the theme. Plain language, explain a term
once ("the hero, the big banner at the top"), narrate before acting ("I'll change the headline and
leave everything else as it is"), flag trade-offs in plain terms, and explain draft versus live the
first time it comes up: on a draft, nothing visitors see changes until they say go; on the live
theme, edits show to visitors as soon as they are pushed.

## 1. Context

**Theme first.** Before anything else, settle which theme this runs on, with
`../page-content-studio/references/theme-target.md`: use the theme already chosen in this
conversation or remembered in `THEME-TARGET.md` and say so in one line, or ask once which draft or
the live theme to work on and remember the answer for every other skill. Don't ask again unless the
person names a different theme. If it is the live theme, section 5 of that file applies: an explicit
yes before the first edit and again before the push.

Follow section 1 of `../page-audit/references/intake.md`: resolve `BRAND.md`, `BRAND-VOICE.md` and
`design.md`, handle a partial set, and read the store repo's own engineering rules (`AGENTS.md` or
`CLAUDE.md`). Brand files missing: editing wording the person supplied can go ahead; writing new
copy waits for brand-capture. Voice comes from `BRAND-VOICE.md`; say so if it is missing.

## 2. Understand the request

Short, plain, multiple-choice questions until these are answered. If the goal isn't obvious, ask
the one-line goal check in `../page-audit/references/intake.md` section 3.

- **Which page, in their words, and what type is it?** Resolve it to an actual template; don't
  assume `index` means the homepage, check.
- **Exactly what should the new words, image or link be?** Get the final text or the file, not "make
  it better". If they want help writing it, draft options from the brand voice and let them choose.
- **What should stay exactly the same?** Default: everything else.
- **How urgent is it?** Even a live typo goes through verification and a draft; explain the risk of
  skipping rather than just refusing.

**From an audit.** If the request is a row ID or points at a `PAGE-AUDIT.md` (rules in
`../page-audit/references/audit-file.md`), read the rows marked `picked` that are about content and
owned by this theme. Work only on those and carry each row's baseline number. Rows about layout or
style go to `page-edit-design`; rows owned by store settings, an app or an off-site page are
reported, not edited here.

## 3. Resolve the target and the working copy

1. Confirm the page exists in admin or `templates/` rather than trusting the name used in chat. If
   it doesn't exist, this is `page-create`.
2. Confirm the theme settled in step 1, with its id and role recorded.
3. Get a working copy: follow the store repo's workflow if it names one (usually pull the theme
   first so admin-side edits aren't lost); otherwise pull the theme's files into a scratch folder.

## 4. Find where the content lives

Walk the template's section list and match the text on the render to the setting that holds it;
don't guess from a name.

| Where it lives | How to recognise it | What to do |
|---|---|---|
| A section or block setting in the page template | The text is a value in the template's JSON for that section | Edit that one value |
| The section's schema default | The template has no value, and the default shows | Set the value in the template; don't edit the default |
| A locale file | The same words appear on several pages | Decide: change it everywhere (edit the locale) or only here (set a per-section value). Flag the other pages first |
| Store admin content | A product, collection or page body, a menu, a metafield, policy text | Say so plainly and point to the exact place in admin; don't edit theme code that won't change what they see |
| An app or third-party widget | Reviews, forms, pop-ups, a booking widget | Report it; the app's settings change it, not this theme |

Check whether the same words are used elsewhere (a reused section or locale key) and flag it before
changing it. If the new copy contains a claim, a number or regulated wording, say it will be
fact-checked, and run `content-fact-check` before it ships.

## 5. Capture the baseline

Before the first edit, start the change pack as set out in
`../page-content-studio/references/baseline-and-change-pack.md`: theme id and role, section
inventory, total height, `theme check` count, heading outline, the link map for links in scope,
overlays, a copy of each file to edit, and the current text or image of the thing that will change.
Desktop and mobile.

## 6. Show the exact change

Say in plain words what will change and show it: the setting or file, the before text and the after
text (or the image, link and alt text). Check that longer copy still fits the layout. Get a yes
before editing anything beyond a single value or anything that could affect another page. If the
theme is live, a yes is always needed, even for a single value; it names the theme (name and id) and
is the live-theme assurance (`theme-target.md` section 5). Record it in section 3 of the change
pack.

## 7. Edit the working copy

Make exactly that change and no other. Run `theme check`; the count must not be higher than the
baseline's. Record the files touched, with lines added and removed, in section 4 of the change pack.

## 8. Verify

Run `../page-content-studio/references/verify.md` on the rendered page. For a content change the
checks that matter most are: the new words read exactly as approved (check 5), links and images work
(check 4), tracked links unchanged (check 3), nothing else moved (check 2), and accessibility basics
including alt text (check 9). Any failure goes back to step 7; nothing ships on a failed check.

## 9. Ship to the chosen theme

Run `../page-content-studio/references/ship-to-draft.md`: check nobody edited the files since the
baseline, push only the touched files to the chosen theme, pull them back as proof, re-check the
preview, write the QA entry (`../page-content-studio/references/qa-entry-format.md`), and set any
audit rows to `done`. On the live theme, the second yes (the exact files and change) comes before
the push. Publishing a draft over the live theme happens only if the person asks, with an explicit,
recorded yes. To undo, use `../page-content-studio/references/revert-mode.md`.

## 10. Hand back

Give a short, plain summary: what changed and where it can be seen, what was verified with the
numbers, what was flagged and not done (including any claim awaiting a fact-check), and whether it is
on the draft only or live.

## Checklist before finishing

- [ ] Brand files handled; no claim, number or name invented; claims sent to a fact-check
- [ ] Content found where it lives; admin-owned content pointed to admin; shared locale text flagged
- [ ] Baseline captured before the first edit; change pack started
- [ ] Exact change shown and agreed where it wasn't a single value
- [ ] Only content changed; any design request handed to `page-edit-design`
- [ ] Verified on the rendered page at desktop and mobile; tracked links unchanged
- [ ] Theme settled once (remembered or asked); pushed only to it, only the touched files, pulled back identical;
      if live, a yes before the edit and again before the push
- [ ] No credential typed; QA entry written; audit rows updated only when verified
