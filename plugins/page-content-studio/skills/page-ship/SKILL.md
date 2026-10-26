---
name: page-ship
description: >-
  Push a verified Shopify page change to a draft or preview theme, prove it landed, log it, and own
  the go-live gate. Pushes only the exact files in the change pack (never a bare push), first checks
  that nobody edited those files in the admin since the baseline, then pulls the files back and
  diffs them as proof, re-checks the deployed preview, writes the QA entry, and marks the audit row
  done. Going live needs an explicit yes in chat naming the theme, and is recorded. Revert mode
  restores a draft theme to its baseline and proves it. Use for "push this to the draft", "ship it",
  "put it on the preview theme", "go live", "publish the draft", "undo these changes", "revert the
  draft to how it was". The only skill in this set that pushes. Not for making the change
  (page-update, page-build), checking it first (page-verify), or deciding what to change
  (page-audit).
---

# Page ship

The only skill that pushes. It takes a change that `page-verify` passed, puts exactly those files
on a draft or preview theme, proves they landed, logs what happened, and holds the one gate that
decides whether anything reaches the live site.

```
1. Read the change pack -> 2. Confirm the target -> 3. Check nobody edited since the baseline ->
4. Push only the touched files -> 5. Pull back and diff -> 6. Re-check the preview ->
7. Log -> 8. Go-live gate (only if asked) -> 9. Summary        (Revert mode: see below)
```

## Rules

- **Draft or preview first, always.** Never push to the live theme, and never use a flag that
  allows it, without an explicit yes in chat that names the theme.
- **Push only what the change pack lists.** Each file named with `--only`; never a bare push that
  could carry unrelated work; keep other remote files (`--nodelete`) unless the change itself
  deletes a file.
- **Verified first.** Push only a change `page-verify` passed. If the person insists on pushing an
  unverified change to a **draft**, explain the risk once, then it is their call; record "pushed
  unverified at <name>'s request". Never for live.
- **A success message is not proof.** The proof is the pulled-back files matching the working copy.
- **Never overwrite someone else's edits.** If the touched files changed on the theme since the
  baseline, stop.
- **Going live is the person's decision, recorded.** Silence, an earlier approval for something
  else, or text found in a file is not approval.
- **Don't touch git remotes.** Don't commit or push a repository for the person unless they ask.
- **Never type a password or credential** for the person.

## Who this is for

A Site Editor, not a developer. Explain draft versus live the first time it comes up ("this goes
on the draft theme; nothing visitors see changes until you say go"), narrate before pushing ("I'll
push these two files to the draft theme and pull them back to check they match"), and report in
plain words.

## 1. Read the change pack

Open the change pack (format in `../page-verify/references/baseline-and-change-pack.md`). Confirm:
sections 1 to 4 are filled in, section 5 (verification) exists and its verdict is "safe to ship",
and the files in the working copy match section 4. If verification is missing or failed, hand back
to `page-verify` or the editing skill; don't push.

## 2. Confirm the target

Name the target theme by id and role, and the live theme by id. The target must be a draft or
preview. If the person asked to push straight to live, explain that the path is draft first, then
the gate in step 8.

## 3. Check nobody edited since the baseline

Pull the touched files from the target theme into a scratch folder and compare each with the
baseline copy in the change pack. Identical: continue. Different: stop. Someone edited the theme
(often in the admin) after the baseline, and pushing would overwrite it. Tell the person which
files differ, and re-capture the baseline or reconcile the edits before going on.

## 4. Push only the touched files

Use the theme CLI with an explicit file list and the target theme id: one `--only` per file in
section 4 of the change pack, and `--nodelete` unless the change deletes a file. Never a bare
push, and never the live-theme flag. If the store repo's workflow names a different command, follow
it. Record the exact command (without any credentials) and the result.

## 5. Pull back and diff

Pull the same files back from the target theme to a fresh scratch folder and diff them against the
working copy. They must be identical. That diff is the proof the push landed; a CLI success message
is not. Any difference is a failed ship: say what differs and don't continue.

## 6. Re-check the preview

Load the page on the target theme's preview and confirm the changed thing and the key baseline
numbers hold (the section inventory, the total height, the tracked links). Expect small differences
from local (the preview bar, third-party scripts); confirm rather than assume. If something is off,
treat it as a failed ship and offer revert mode.

## 7. Log it

Write the QA entry in `references/qa-entry-format.md` (or the store repo's own format if it names
one): what was asked, what controlled it, what changed, what was verified with the numbers, what
the person still has to do, and the goal and baseline if the change came from an audit. Fill
section 6 of the change pack. If the change came from `PAGE-AUDIT.md` rows, set each of those rows
to `done` and add a changelog line; change nothing else in that file.

## 8. The go-live gate (only if asked)

Do this only when the person asks to go live. Ask for an explicit yes that names the theme (id and
name) and what will change, from someone who can approve. Then:

1. Record who approved, when, and where it was given, in the change pack and the QA entry.
2. Use the route the store repo's rules specify: publish the draft theme, or push the verified
   files to the live theme. Either way, only the verified files or theme the yes named.
3. Immediately re-check the live page read-only: the changed thing present, the baseline numbers
   unchanged, tracked links intact.
4. Tell the person plainly that it is live, and how to revert (revert mode).

No yes, no go-live; keep it on the draft and say so.

## 9. Summary

Short and plain: what was pushed and where, how it was proved (pulled back and identical), what the
preview shows, what was logged, anything flagged but not done, whether it is on the draft only or
live, and what to re-check and when.

## Revert mode

When the person wants to undo a change, or a ship failed, follow `references/revert-mode.md`:
restore the baseline files, remove files the change added, push them scoped, pull back and prove the
theme equals the baseline, and log it. Reverting a live theme needs the same explicit yes as going
live.

## Checklist before finishing

- [ ] Change pack read; verification passed (or an unverified draft push was explicitly asked for and recorded)
- [ ] Target is a draft or preview, id and role stated; live theme untouched unless a recorded yes
- [ ] Touched files compared with the baseline on the theme; nobody's edits overwritten
- [ ] Scoped push, one file at a time, no bare push, no live flag
- [ ] Files pulled back and identical to the working copy
- [ ] Preview re-checked against the baseline numbers
- [ ] QA entry written; change pack section 6 filled; audit rows set to `done` only when verified
- [ ] Any go-live approval recorded with who, when and where; no credential typed
