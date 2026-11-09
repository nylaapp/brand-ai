# Revert mode

Restore a theme to its baseline and prove it. Use when the person asks to undo changes, a ship
failed, or verification of a pushed change found a regression that can't be fixed quickly.

A revert is a push, so everything in `ship-to-draft.md` applies: scoped files only, no bare push, no live flag, and never the live theme: a revert happens on the draft the change was made on.

On the **connector route** (`connector-route.md`; no CLI, no local copy of the theme) a revert is a
write too: the same guards apply (role read right before, explicit theme id, only the listed files),
and the paragraphs marked **Connector route** below say what changes.

## 1. Find the baseline

In order of preference:

1. The change pack's `baseline/` folder (copies of each file from before the first edit).
2. The store repo's git history at the commit before the change, if the store uses one (read the
   files from that commit; don't commit or push the repository for the person).
3. A saved pull of the theme taken before the work began.

If none exists, say so: you can describe what changed but can't restore it exactly. Don't guess
a "clean" version from memory.

## 2. Check nobody edited since the change

Pull the files you would restore from the target theme and compare them with the change pack's
"after" state (the working copy that was shipped). Identical: continue. Different: someone edited
the theme after the ship (often in the admin). Stop, show which files differ, and ask whether those
edits should be kept, because restoring the baseline would erase them.

**Connector route:** read those files from the draft and compare each one's `checksumMd5` (or body)
with the md5 of the matching file in `work/`, which is what was written. Same rule if they differ.

## 3. Work out exactly what to restore

From section 4 of the change pack:

| What the change did | The revert |
|---|---|
| Modified an existing file | Put the baseline copy back |
| Added a new file | Remove it from the theme, after confirming no template still references it |
| Added an entry to a template (for example a new section in a page template) | Restore the template first, then remove the file it referenced, in that order |
| Deleted a file | Restore it from the baseline |

Never remove a section or block file that another template still references; check first.

## 4. Push the revert, scoped

Restore the files in the working copy, then push only those files to the target theme with an
explicit `--only` for each. Allow deletion only for the files the revert itself removes, and name
each one. Order matters: push the templates that stop referencing a file before deleting the file.

**Connector route:** write the baseline copies back with `themeFilesUpsert` (whole files, an
explicit list, at most 50 per call), then remove the files the change added with `themeFilesDelete`,
each named, in that order. Role gate first, as for any write. A baseline copy whose md5 did not
match its `checksumMd5` when it was taken is not a backup: don't restore from it.

## 5. Prove it

1. Pull the whole target theme to a fresh scratch folder.
2. Compare it with the baseline, file by file. Ignore files that are not tracked by the store repo
   (for example theme settings the store keeps out of version control), and say that you ignored
   them. Differences: list them; the revert is not complete.
3. Load the page on the theme and confirm the baseline numbers return: section inventory, total
   height, heading outline, tracked links, and the `theme check` count.

**Connector route:** instead of pulling the whole theme, read the restored files back (retrying for
up to about 30 seconds, because writes are asynchronous) and compare them with `baseline/`, then
read the whole-theme manifest and compare it with `baseline/manifest.json`: it should match, apart
from files someone else edited, which you name. The `theme check` count is "Can't tell" on this
route, as it was at the baseline.

## 6. Log it

Write a QA entry marked as a revert: what was undone, why, the baseline used, how it was proved,
and what was not restored and why. Set any `PAGE-AUDIT.md` rows that had been marked `done` for the
reverted change back to `picked` with a changelog line, so the audit doesn't claim a change that is
no longer there.

## What a revert does not do

It does not undo edits made outside this change, it never touches the live theme, and it does not restore content that lives in the admin (pages, products, menus,
metafields), only theme files.
