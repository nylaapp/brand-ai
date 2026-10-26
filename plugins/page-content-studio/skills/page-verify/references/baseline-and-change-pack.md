# Baseline and change pack

The hand-off between `page-update` or `page-build` (which edit), `page-verify` (which checks)
and `page-ship` (which pushes). `page-verify` owns this format; the others follow it.

The **baseline** is what the page looked like before any edit, so "nothing else moved" can be
proven. The **change pack** is one small file that carries the request, the baseline, the
intended change, the files touched and the results from one skill to the next.

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
| Files that will be edited, with a copy of each | Copy to the scratch folder as `baseline/` | Lets `page-ship` revert exactly |
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
live_theme: <id, name>   # never touched without an explicit yes
created: <YYYY-MM-DD>
skill: page-update | page-build
---

## 1. Request
<what was asked, in the person's words; hard limits that must not change>

## 2. Baseline (desktop and mobile)
<the table above, filled in; section inventory as a table>
Baseline copies: <path to baseline/ folder>

## 3. Intended change
<exact edits: file, setting or lines, before and after>

## 4. Files touched
| File | Change | Lines +/- |
|---|---|---|

## 5. Verification (written by page-verify)
| Check | Result | Number or evidence | Viewport |
|---|---|---|---|

## 6. Ship record (written by page-ship)
- Pushed: <date, files, theme id>. Pulled back and diffed: <identical | differences>.
- Go-live: <not requested | approved by <who> on <date>, where given>.
- QA log entry: <path or "in chat">.
```

## 3. Who writes what

- `page-update` and `page-build` write sections 1 to 4 and nothing else.
- `page-verify` writes section 5 and nothing else. It never edits a theme file.
- `page-ship` reads sections 1 to 5, writes section 6, and updates audit row status.
- If sections 3 and 4 disagree with the files in the working copy, stop: the pack is stale.
  Re-capture or ask the person.
- A pack is valid only for the theme and working copy named in its front matter. If the theme was
  edited in the admin after the baseline, the baseline no longer describes it; say so and
  re-capture before verifying.

## 4. What "verified" means

A change is verified only when `page-verify` loaded the rendered page on the target theme at
desktop and mobile and every check in its section 5 table passed or is marked "Can't tell" with
a reason that the person accepted. A source diff is never verification.
