---
name: page-edit-design
description: >-
  Edit the design of an existing Shopify page without changing what it says: layout, section order
  and structure (reordering, hiding, showing or removing existing sections), spacing and padding,
  colour scheme, typography, button and card styles, and how the page behaves on phones and tablets.
  Uses the narrowest technique that works (a theme setting, then a token override, then scoped CSS,
  and section code only last), takes every visual value from the design spec, checks every other
  page that shares the section or style, captures a baseline, edits a local working copy, verifies
  on the rendered page across breakpoints and colour schemes, and pushes only the touched files to
  the theme the person chose (a draft unless they say live). Also acts on audit rows a person picked
  in PAGE-AUDIT.md. Brand-agnostic, written for the Site Editor. Use for "move the booking section
  up", "make the hero shorter on mobile", "change this section's colour scheme", "increase the
  spacing", "restyle this button", "fix the second h1", "do row HOME-01" when the row is about
  layout, order or style. Not for the words, images or links (use page-edit-content), a new page or
  section (page-create), open-ended "improve this page" (page-audit), or accessibility audits
  (accessibility-audit).
---

# Page edit: design

Change how an existing page **looks and is arranged** (layout, order, spacing, colour, type,
component styles, responsive behaviour) and nothing about what it says. The skill picks the
narrowest technique, captures a baseline, edits a local working copy, proves nothing else moved
across breakpoints and colour schemes, and puts only the touched files on the theme the person chose
(a draft unless they say live). The live theme needs their explicit yes before any edit and again
before the push.

```
1. Context -> 2. Understand the request -> 3. Resolve the target and working copy ->
4. Pick the narrowest technique -> 5. Capture the baseline -> 6. Show the exact change ->
7. Edit the working copy -> 8. Verify -> 9. Ship to the theme -> 10. Hand back
```

## Rules

- **Working copy first, on the theme the person chose.** Never push from the working copy except
  through the ship step. The theme is asked once and remembered (`theme-target.md`); a draft is
  recommended. The live theme needs an explicit yes before the first edit and again before the push,
  every run (`theme-target.md`, `ship-to-draft.md`).
- **Design only.** If the request also changes words, images or links, do that in
  `page-edit-content` as its own change.
- **Narrowest technique that works:** a theme setting, then a token override, then scoped CSS,
  and section code only when nothing else can do it. Follow the store repo's cascade and scoping
  rules; never edit shared base files or vendor code, and don't add selectors tied to one section's
  id when the repo says to avoid them.
- **Every visual value traces to the spec** (`design.md`, else the store repo's visual spec or the
  theme's settings). Never invent a hex, font, size or radius to fill a gap, and never swap a font
  without a licence check with the person.
- **Shared code is shared.** A change to a section type, snippet, token or stylesheet affects every
  page that uses it. Find every usage and flag them before editing, not after.
- **Capture the baseline before the first edit**, including the other pages that share the code,
  so "nothing else moved" can be proved and the edit reverted exactly.
- **Don't change tracked links, labels or the words** while restyling.
- **Never delete or rename** a section or block file another page references.
- **Never type a password or credential** for the person.
- **Hard limits win.** What the person said must not change (brand look, tracked links) overrides
  the request.

## Who this is for

A Site Editor on the marketing, content or operations side: they describe what a visitor sees ("the
booking section is too far down", "the hero is too tall on my phone"), not where it lives in the
theme. Plain language, explain a term once, narrate before acting ("I'll move that section up and
leave every other section where it is"), flag trade-offs in plain terms ("this style is also used on
your contact page"), and explain draft versus live the first time it comes up: on a draft, nothing
visitors see changes until they say go; on the live theme, edits show to visitors as soon as they
are pushed.

## 1. Context

**Theme first.** Before anything else, settle which theme this runs on, with
`../page-content-studio/references/theme-target.md`: use the theme already chosen in this
conversation or remembered in `THEME-TARGET.md` and say so in one line, or ask once which draft or
the live theme to work on and remember the answer for every other skill. Don't ask again unless the
person names a different theme. If it is the live theme, section 5 of that file applies: an explicit
yes before the first edit and again before the push.

Follow section 1 of `../page-audit/references/intake.md`: resolve the brand files and `design.md`,
handle a partial set, and read the store repo's own engineering rules (`AGENTS.md` or `CLAUDE.md`),
especially its cascade order, scoping rules and any register of base-file changes. Visual values come
from `design.md`; values marked inferred are unconfirmed and are flagged, not built on silently.

## 2. Understand the request

Short, plain, multiple-choice questions until these are answered. If the goal isn't obvious, ask the
one-line goal check in `../page-audit/references/intake.md` section 3.

- **Which page, in their words, and what type is it?** Resolve it to an actual template.
- **What exactly looks wrong or should be different, and on which device?** Reproduce it on the
  render at desktop and mobile before touching anything.
- **Is there a reference** of what right looks like?
- **What should stay exactly the same?** Default: everything else.
- **How urgent is it?** Even a quick fix goes through verification and a draft.

**From an audit.** If the request is a row ID or points at a `PAGE-AUDIT.md` (rules in
`../page-audit/references/audit-file.md`), read the rows marked `picked` that are about layout,
order or style and owned by this theme. Work only on those and carry each row's baseline number.
Content rows go to `page-edit-content`; rows owned by store settings, an app or an off-site page are
reported, not edited here.

## 3. Resolve the target and the working copy

1. Confirm the page exists in admin or `templates/`; if it doesn't, this is `page-create`.
2. Confirm the theme settled in step 1, with its id and role recorded.
3. Get a working copy: follow the store repo's workflow if it names one (usually pull the theme
   first so admin-side edits aren't lost); otherwise pull the theme's files into a scratch folder.
4. List every other page and template that uses the section, snippet, token or style you expect to
   touch.

## 4. Pick the narrowest technique

| Kind of change | Safe technique | Avoid |
|---|---|---|
| Section order, hide or show, remove from the page | Edit the page template's section list only | Deleting a section or block file another page references |
| A look the section already offers (colour scheme, alignment, width, height, spacing) | Change the section's existing setting value | Writing CSS for what a setting already does |
| A global look (type scale, colour roles, radius) | Override the design token or edit the theme setting | Hardcoding a value in one place |
| Restyle one component on this page | A scoped rule in the store's custom stylesheet, in the repo's preferred scoping style | Editing base or vendor files; selectors tied to one section's id when the repo says to avoid them |
| Responsive behaviour | A breakpoint rule in the same scoped block, matching the repo's breakpoints | A one-off fix at one width that breaks another |
| A design option no setting offers | A new setting plus minimal markup that matches a sibling section's pattern | Inventing a new pattern when the theme already has one |
| Larger than asked | Stop, name the trade-off in plain terms, ask | Silently "improving" something nearby |

Enlarging a small tap target, for example, can usually be done by adding padding with a matching
negative margin so layout doesn't shift. Verify that it didn't.

## 5. Capture the baseline

Before the first edit, start the change pack as set out in
`../page-content-studio/references/baseline-and-change-pack.md`: theme id and role, section
inventory, total height, `theme check` count, heading outline, the link map, overlays, and a copy of
each file to edit. Desktop and mobile, plus tablet for responsive work, **and the same inventory for
each other page that uses the shared code**, so nothing else can move unnoticed.

## 6. Show the exact change

Say in plain words what will change and show it: the setting or file, the before and the after, and
the expected effect on position and size. Name every other page that shares the code and what you
expect to happen there (usually nothing). Get a yes before editing anything beyond a single setting
value or anything that touches shared code. If the theme is live, a yes is always needed, even for a
single value; it names the theme (name and id) and is the live-theme assurance (`theme-target.md`
section 5). Record it in section 3 of the change pack.

## 7. Edit the working copy

Make exactly that change; no drive-by clean-ups. Follow the repo's rules for scoping, naming and where
changes go. Run `theme check`; the count must not be higher than the baseline's. Record the files
touched, with lines added and removed, in section 4 of the change pack.

## 8. Verify

Run `../page-content-studio/references/verify.md` on the rendered page. For a design change the checks
that matter most are: nothing else moved on this page (check 2) **and on every page that shares the
code** (check 7), other breakpoints and colour schemes hold (check 6), values come from the spec
(check 12), tracked links unchanged (check 3), and accessibility basics including contrast and tap
targets (check 9). Any failure goes back to step 7; nothing ships on a failed check.

## 9. Ship to the chosen theme

Run `../page-content-studio/references/ship-to-draft.md`: check nobody edited the files since the
baseline, push only the touched files to the chosen theme, pull them back as proof, re-check the
preview, write the QA entry (`../page-content-studio/references/qa-entry-format.md`), and set any
audit rows to `done`. On the live theme, the second yes (the exact files and change) comes before
the push. Publishing a draft over the live theme happens only if the person asks, with an explicit,
recorded yes. To undo, use `../page-content-studio/references/revert-mode.md`.

## 10. Hand back

Give a short, plain summary: what changed and where it can be seen, what was verified with the
numbers (including the other pages checked), what was flagged and not done, and whether it is on the
draft only or live.

## Checklist before finishing

- [ ] Visual values traced to the spec; none invented; no font swapped without a licence check
- [ ] Every other page using the shared code identified, baselined and verified
- [ ] Narrowest technique used; repo scoping rules followed; no base or vendor file edited
- [ ] Baseline captured before the first edit; change pack started
- [ ] Exact change shown and agreed where it wasn't a single setting
- [ ] Only design changed; any wording request handed to `page-edit-content`
- [ ] Verified at desktop, mobile and tablet where relevant, across colour schemes; tracked links unchanged
- [ ] Theme settled once (remembered or asked); pushed only to it, only the touched files, pulled back identical;
      if live, a yes before the edit and again before the push
- [ ] No credential typed; QA entry written; audit rows updated only when verified
