# Ship to the chosen theme

The shared delivery step. `page-create`, `page-edit-content` and `page-edit-design` run it
themselves after a change is verified, and the front door runs it when someone only wants an
already-made change pushed. It puts exactly the verified files on the theme the person chose (a draft
or preview, never the live theme), proves they landed, logs it, and holds the gates that
protect the live site. These rules are the same whichever skill runs them; this file is their single
source. The file keeps its original name so existing links keep working.

Which theme to use, and how the live theme is protected, are set in `theme-target.md`. Read it first.

## Rules

- **The target is the theme the person chose**: named earlier in the conversation or remembered in
  `THEME-TARGET.md` (`theme-target.md`). Never switch themes silently.
- **Never the live theme.** Re-read the target's role from the store right before every pull, edit and
  push. If it is live, stop: do not edit, push or publish it, whatever the person says. Use or create a
  draft (`theme-target.md`). Never use a flag that allows a live push (`--allow-live`).
- **Push only what the change pack lists.** Name each file with `--only`; never a bare push that
  could carry unrelated work; keep other remote files (`--nodelete`) unless the change itself
  deletes a file.
- **Verified first.** Push only a change `verify.md` passed. If the person insists on pushing an
  unverified change to a **draft**, explain the risk once; then it is their call. Record "pushed
  unverified at <name>'s request".
- **A success message is not proof.** The proof is the pulled-back files matching the working copy.
- **Never overwrite someone else's edits.** If the touched files changed on the theme since the
  baseline, stop.
- **These skills never publish a theme.** Publishing a draft over the live theme is a live change the
  person makes themselves in the store admin (section 8).
- **Don't touch git remotes.** Don't commit or push a repository for the person unless they ask.
- **Never type a password or credential** for the person.

## 1. Read the change pack

Confirm sections 1 to 4 are filled in, section 5 (verification) exists with the verdict "safe", and
the files in the working copy match section 4. If verification is missing or failed, go back to it;
don't push.

## 2. Confirm the target

Name the target theme by id and role, and the live theme by id. Re-read the target's role from the
store now: a draft that has been published since is live.

- **Draft or preview:** continue.
- **Live:** stop. Say "This is the LIVE theme, so I won't edit it." Go to `theme-target.md` to use or
  create a draft; the change pack carries over to it.

## 3. Check nobody edited since the baseline

Pull the touched files from the target theme into a scratch folder and compare each with the
baseline copy in the change pack. Identical: continue. Different: stop. Someone edited the theme
(often in the admin) after the baseline, and pushing would overwrite it. Tell the person which
files differ and re-capture the baseline or reconcile the edits first. On the live theme, keep the
baseline copies: they are the backup that makes a revert exact.

## 4. Push only the touched files

Use the theme CLI with an explicit file list and the target theme id: one `--only` per file in
section 4 of the change pack, and `--nodelete` unless the change deletes a file. Never a bare push.
Never use the live-theme flag (`--allow-live`). If
the store repo's workflow names a different command, follow it. Record the exact command (without
any credentials) and the result.

## 5. Pull back and diff

Pull the same files back from the target theme to a fresh scratch folder and diff them against the
working copy. They must be identical. That diff is the proof the push landed. Any difference is a
failed ship: say what differs and don't continue.

## 6. Re-check the page

Load the page on the target theme (the draft's preview) and confirm the changed thing and the key baseline numbers hold (section inventory, total
height, tracked links). Expect small differences from local (the preview bar, third-party scripts);
confirm rather than assume. If something is off, treat it as a failed ship and offer revert mode
(`revert-mode.md`).

## 7. Log it

Write the QA entry in `qa-entry-format.md` (or the store repo's own format if it names one): what
was asked, what controlled it, what changed, what was verified with the numbers, what the person
still has to do, and the goal and baseline if the change came from an audit. Fill section 6 of the
change pack. If the change came from `PAGE-AUDIT.md` rows, set each of those rows to `done` and add
a changelog line; change nothing else in that file.

## 8. Going live is the person's step

These skills never publish a theme. If the person asks to publish the draft, or to go live with the
work, say in one line that they do it themselves, and give the steps: in the store admin, Online Store
> Themes, open the draft's menu and choose **Publish** (or ask whoever manages the store). Suggest
checking the draft's preview first and offer the QA entry and change pack as the checklist. Do not run
a publish command. Once they publish, that theme is live and is no longer a target: the next job
starts from a fresh draft (`theme-target.md` section 3).

## 9. Summary

Short and plain: what was pushed and where, how it was proved (pulled back and identical), what the
page shows, what was logged, anything flagged but not done, that it is on a draft only (publishing is theirs to do), and
what to re-check and when.
