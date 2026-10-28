# Baseline and change pack

The record carried through one change. The editing skill (`page-create`, `page-edit-content` or
`page-edit-design`) captures the baseline and starts it, the shared verify step (`verify.md`) adds
the results, and the shared ship step (`ship-to-draft.md`) adds the ship record. This file owns
the format.

The **baseline** is what the page looked like before any edit, so "nothing else moved" can be
proven. The **change pack** is one small file that carries the request, the baseline, the
intended change, the files touched and the results from one step to the next.

## Where it lives

In the scratch folder next to the working copy, named `change-pack-<page>-<YYYY-MM-DD>.md`
(for example `change-pack-homepage-2026-10-27.md`). It is a working file, not a client file:
don't commit it, and never put passwords, tokens, customer data or analytics identifiers in it.
Tell the person its path. If there is a `PAGE-AUDIT.md`, rows are referenced by ID only.

## 1. Capture the baseline (before the first edit)

Follow `../../page-audit/references/observation-recipes.md` (real viewport, theme id confirmed,
slow scroll, overlays noted). Capture at desktop (1440x900) and mobile (375x812):

| Item | How | Why it is needed later |
|---|---|---|
| Theme id, name and role (draft, preview or live) | The theme list and the id the page reports | Proves the right theme was changed |
| Section inventory: id, top, height, first words | Section snippet in the recipes | Proves nothing else moved |
| Total page height | `document.body.scrollHeight` | A quick whole-page check |
| `theme check` offense count for the working copy | `theme check` | The count must not grow |
| Heading outline and h1 count | Headings snippet | Catches a second h1 or a skipped level |
| Link map for the links in scope (label, destination, position) | Link map snippet | Proves tracked links did not change |
| Overlays seen at 1 s and about 15 s | Overlay snippet | Separates the change from consent or pop-up noise |
| Files that will be edited, with a copy of each | Copy to the scratch folder as `baseline/` | Lets the ship step revert exactly (`revert-mode.md`) |
| For an update: the exact thing that will change | A screenshot or the text before | Proves the change happened |

For a **new page**, the baseline is the list of existing templates and the same site-wide
numbers, because the new page has no "before". For **verifying someone else's change**, capture
the current state now and say that anything wrong before this point can't be detected.

## 2. Change pack format

```markdown
---
change_pack_schema: 1.0
page: <homepage | about | ...>
rows: [<PAGE-AUDIT row IDs, or "none (named change)">]
target_theme: <id, name, role>
live_theme: <id, name>   # needs an explicit yes before any edit and again before any push
created: <YYYY-MM-DD>
skill: page-create | page-edit-content | page-edit-design
---

## 1. Request
<what was asked, in the person's words; hard limits that must not change>

## 2. Baseline (desktop and mobile)
<the table above, filled in; section inventory as a table>
Baseline copies: <path to baseline/ folder>

## 3. Intended change
<exact edits: file, setting or lines, before and after>
Approval: <who agreed to this exact change, when, where given; on the live theme this is the yes before the edit>

## 4. Files touched
| File | Change | Lines +/- |
|---|---|---|

## 5. Verification (written in the verify step)
| Check | Result | Number or evidence | Viewport |
|---|---|---|---|

## 6. Ship record (written in the ship step)
- Pushed: <date, files, theme id>. Pulled back and diffed: <identical | differences>.
- Live-theme assurance: <not needed (draft or preview) | before the edit: <who, when, where given>; before the push: <who, when, where given>>.
- Publishing a draft over the live theme: <not requested | approved by <who> on <date>, where given>.
- QA log entry: <path or "in chat">.
```

## 3. Who writes what

- The editing skill writes sections 1 to 4 before and during the edit.
- The verify step writes section 5 and never edits a theme file.
- The ship step reads sections 1 to 5, writes section 6, and updates audit row status.
- If sections 3 and 4 disagree with the files in the working copy, stop: the pack is stale.
  Re-capture or ask the person.
- A pack is valid only for the theme and working copy named in its front matter. If the theme was
  edited in the admin after the baseline, the baseline no longer describes it; say so and
  re-capture before verifying.

## 4. What "verified" means

A change is verified only when the verify step loaded the rendered page on the target theme at
desktop and mobile and every check in its section 5 table passed or is marked "Can't tell" with
a reason that the person accepted. A source diff is never verification.
