---
name: page-update
description: >-
  Change something that already exists on a Shopify page, the narrowest safe way: copy, an image,
  a link, a button label, a section's settings or layout, or which sections appear and in what
  order. Finds what actually controls the thing (a section setting, the template, a locale file,
  or content that lives in admin and not the theme), captures a baseline first, shows the exact
  change, and edits a local working copy of the theme. Also acts on audit rows a person picked in
  PAGE-AUDIT.md. Brand-agnostic, written for the Site Editor, not a developer. Use for "swap the
  hero image", "change this headline", "fix the typo on", "move the pricing above the FAQ", "make
  this button go to X", "do row HOME-02". Edits the working copy only; it never pushes. Not for
  open-ended "improve this page" (use page-audit), a brand-new page (page-build), checking a change
  (page-verify), pushing or going live (page-ship), blog posts (shopify-blog-writer) or accessibility
  audits (accessibility-audit).
---

# Page update

Change what already exists on a page without changing anything else. This skill finds what
controls the thing, captures a baseline, shows the exact edit, and makes it in a **local working
copy** of the theme. It never pushes: `page-verify` checks the result and `page-ship` pushes it.

```
1. Context -> 2. Understand the request -> 3. Resolve the target ->
4. Find what controls it -> 5. Capture the baseline -> 6. Show the exact change ->
7. Edit the working copy -> 8. Hand to page-verify, then page-ship
```

## Rules

- **Working copy only.** Never push, publish or edit the live theme. Pushing belongs to
  `page-ship`.
- **Narrowest change that works.** A setting beats code; a new setting beats new markup. Never
  widen a content or settings fix into a code change when an existing setting would do.
- **Capture the baseline before the first edit**, or the change can't be proven safe or reverted.
- **Stay in scope.** Everything else on the page stays visually identical. If the request would
  touch something the person didn't mention, stop and ask in plain terms.
- **Don't invent brand facts or claims.** New or rewritten copy comes from the brand files or from
  the person; with neither, wait for brand-capture. Never copy a claim, number or proper noun from
  memory.
- **Never touch a shared base-theme file or token** without checking every usage it affects, and
  never delete or rename a section or block file another page still references.
- **Never type a password or credential** for the person.
- **Hard limits win.** What the person said must not change (tracked booking links, regulated
  wording, brand look) overrides the request.

## Who this is for

A Site Editor on the marketing, content or operations side: they describe what a visitor sees
("the homepage photo is outdated", "move the pricing above the FAQ"), not where it lives in the
theme. Plain language, explain a term once ("the hero, the big banner at the top"), narrate before
acting ("I'll swap the homepage hero image and leave everything else as it is"), flag trade-offs
in plain terms, and explain draft versus live the first time it comes up: nothing visitors see
changes until they say go.

## 1. Context

Follow section 1 of `../page-audit/references/intake.md`: resolve the brand files and `design.md`,
handle a partial set, and read the store repo's own engineering rules (`AGENTS.md` or
`CLAUDE.md`). Brand files missing: a pure structural change (reordering sections, a toggle) can go
ahead; anything with new copy waits for brand-capture. Say which gates you can't confirm if the
repo rules are missing.

## 2. Understand the request

Short, plain, multiple-choice questions until these are answered. If the goal isn't obvious, ask
the one-line goal check in `../page-audit/references/intake.md` section 3.

- **Which page, in their words, and what type is it?** Resolve it to an actual template; don't
  assume `index` means the homepage, check.
- **What should stay exactly the same?** Default: everything else.
- **Is there a reference** to match, or is the wording given?
- **How urgent is it?** Even a live typo goes through verification and a draft; say so and explain
  the risk of skipping rather than just refusing.

**From an audit.** If the request is a row ID or points at a `PAGE-AUDIT.md` (rules in
`../page-audit/references/audit-file.md`), read the rows marked `picked` whose owner is this
theme. Work only on those, carry each row's baseline number forward, and ignore rows nobody
picked. If a row is owned by store settings, an app or an off-site page, say so and don't edit it.

## 3. Resolve the target

1. Confirm the page exists: check the page in admin or the `templates/` folder rather than
   trusting the name used in chat. If it doesn't exist, this is a new page: use `page-build`.
2. Confirm which theme to work on, and that it is a draft or preview. Record its id and role.
3. Get a working copy: follow the store repo's workflow if it names one (usually pull the draft
   theme first so admin-side edits aren't lost); otherwise pull the draft theme's files into a
   scratch working folder. Never work from the live theme's files without saying so.
4. Resolve a real local URL to test against (`shopify theme dev` or the draft preview).

## 4. Find what controls it

A request like "update the headline on the homepage" could live in a section's schema default, a
section's setting (set per page), a locale file, or, for merchant-authored content like a product
description, nowhere in the theme at all.

1. Find which section renders that part of the page: walk the template's section list and match
   it visually against the render; don't guess from the name.
2. Check whether a setting already exists. Reusing one beats adding one.
3. If the content is rendered from outside the theme (product description, metafield,
   admin-authored data), say so plainly -- "that text comes from the product page in admin, not
   this page's design; here's where to edit it" -- rather than editing Liquid that won't change what
   they see.
4. Check whether the same visual change is needed elsewhere (a section reused across pages) and
   flag it before changing it, not after.
5. Classify the change and pick the narrowest safe technique:

   | Kind of change | Safe technique | Avoid |
   |---|---|---|
   | Content (text, image, link, price) | Edit the value in the page's setting, or point to the theme editor or admin if the person can self-serve it | Hardcoding the value into markup where a setting should hold it |
   | Settings (existing toggle or variant) | Change the setting value | Editing the section file to "handle it in code" when a setting exists |
   | Section code (no setting covers it) | Add the new setting plus minimal markup; match a sibling section's pattern | Inventing a new pattern when the theme already has one |
   | Structure (add, remove, reorder) | Edit the page's section list only | Deleting a section or block file another page still references |
   | Visible beyond what was asked | Stop, name the trade-off in plain terms, ask | Silently "improving" something nearby |

## 5. Capture the baseline

Before the first edit, capture the baseline and start the change pack exactly as set out in
`../page-verify/references/baseline-and-change-pack.md`: theme id and role, section inventory,
total height, `theme check` count, heading outline, the link map for links in scope, overlays,
and a copy of each file you will edit. Desktop and mobile. This is what makes "nothing else moved"
provable and a revert exact.

## 6. Show the exact change

Say in plain words what will change and show it: the file or setting, the before and the after.
For anything beyond a single setting value, or anything that could affect another page, get a yes
before editing. Write it into section 3 of the change pack.

## 7. Edit the working copy

Make exactly that change. Keep it as small as the plan; no drive-by clean-ups. Follow the store
repo's rules for scoping, naming and where changes go. Run `theme check` and make sure the count is
not higher than the baseline's. Record the files touched, with lines added and removed, in section 4
of the change pack.

## 8. Hand on

Tell the person what changed in the working copy, that nothing is pushed or live, and what comes
next: `page-verify` checks it on the rendered page, then `page-ship` pushes the touched files to
the draft theme. Offer to run `page-verify` now. Never push from here, and never say a change "works"
before it has been verified.

## Checklist before finishing

- [ ] Brand files handled; no new copy invented
- [ ] Target theme is a draft or preview, id and role recorded
- [ ] Controlling setting or section found; admin-owned content pointed to admin
- [ ] Baseline captured before the first edit; change pack started
- [ ] Exact change shown and agreed where it wasn't a single setting
- [ ] Only the planned files changed; `theme check` count not higher
- [ ] Nothing pushed; live theme untouched; no credential typed
- [ ] The person knows verify and ship come next
