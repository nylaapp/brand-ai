# Ship to the chosen theme

The shared delivery step. `page-create`, `page-edit-content` and `page-edit-design` run it
themselves after a change is verified, and the front door runs it when someone only wants an
already-made change pushed. It puts exactly the verified files on the theme the person chose (a draft
or preview, never the live theme), proves they landed, logs it, and holds the gates that
protect the live site. These rules are the same whichever skill runs them; this file is their single
source. The file keeps its original name so existing links keep working.

Which theme to use, and how the live theme is protected, are set in `theme-target.md`. Read it first.

**Two routes.** The **CLI route** (the Shopify CLI, a local working copy) is the default and is
written out below. The **connector route** (no CLI: the Shopify connector changes the draft's files
directly) is chosen by `setup-check.md` only when the CLI isn't ready and the connector can change
themes. Its calls and guards are in `connector-route.md`; the paragraphs marked **Connector route**
below say what changes. Every rule is the same on both routes.

## Rules

- **The target is the theme the person chose**: named earlier in the conversation or remembered in
  `THEME-TARGET.md` (`theme-target.md`). Never switch themes silently.
- **Never the live theme.** Re-read the target's role from the store right before every pull, edit and
  push. If it is live, stop: do not edit, push or publish it, whatever the person says. Use or create a
  draft (`theme-target.md`). Never use a flag that allows a live push (`--allow-live`). On the
  connector route, write only when the role read now is `UNPUBLISHED` or `DEVELOPMENT`, with the
  theme id passed explicitly in every call (`connector-route.md` section 3).
- **Push only what the change pack lists.** Name each file with `--only`; never a bare push that
  could carry unrelated work; keep other remote files (`--nodelete`) unless the change itself
  deletes a file. On the connector route, an explicit file list in every write is the same thing,
  and only `themeFilesUpsert` writes (it never deletes).
- **Verified first.** Push only a change `verify.md` passed. If the person insists on pushing an
  unverified change to a **draft**, explain the risk once; then it is their call. Record "pushed
  unverified at <name>'s request". On the connector route nothing can be rendered before the write,
  so the order is: pre-write checks, write to the draft, then the rendered verification on the draft
  (`verify.md`, "On the connector route"). The person is told the work is ready only after that
  verification passed.
- **A success message is not proof.** The proof is the pulled-back files matching the working copy.
  On the connector route the write is asynchronous, so the proof is the read-back matching what was
  sent.
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

**Connector route:** section 5 does not exist yet; it is written after the write. Confirm sections 1
to 4 are filled in, the files in `work/` match section 4, and the pre-write checks in `verify.md`
("On the connector route") passed. If any failed, go back to the editing step; don't write.

## 2. Confirm the target

Name the target theme by id and role, and the live theme by id. Re-read the target's role from the
store now: a draft that has been published since is live. (Connector route: the `theme` query in
`connector-route.md` section 2; continue only for `UNPUBLISHED` or `DEVELOPMENT`, and the store
domain still matches.)

- **Draft or preview:** continue.
- **Live:** stop. Say "This is the LIVE theme, so I won't edit it." Go to `theme-target.md` to use or
  create a draft; the change pack carries over to it.

## 3. Check nobody edited since the baseline

Pull the touched files from the target theme into a scratch folder and compare each with the
baseline copy in the change pack. Identical: continue. Different: stop. Someone edited the theme
(often in the admin) after the baseline, and pushing would overwrite it. Tell the person which
files differ and re-capture the baseline or reconcile the edits first. On the live theme, keep the
baseline copies: they are the backup that makes a revert exact.

**Connector route:** read the touched files from the target (`connector-route.md` section 2) and
compare each one's `checksumMd5` (or, if there is none, its body) with the baseline copy. A file the
change pack says is new must not exist yet. Identical: continue. Different: stop, as above.

## 4. Push only the touched files

Use the theme CLI with an explicit file list and the target theme id: one `--only` per file in
section 4 of the change pack, and `--nodelete` unless the change deletes a file. Never a bare push.
Never use the live-theme flag (`--allow-live`). If
the store repo's workflow names a different command, follow it. Record the exact command (without
any credentials) and the result.

**Connector route:** send `themeFilesUpsert` with the target theme id and exactly the files in
section 4 of the change pack, whole files, at most 50 per call, files a template refers to before
the template. If the change deletes a file, `themeFilesDelete` with that file named, after the
templates that stop referencing it. No other mutation, never `themePublish`. Record the call
(theme id and file names, never credentials) and any `userErrors`. If Shopify refuses the first
write for access, nothing changed: tell the person plainly and go back to `setup-check.md`
section 2, step 3.

## 5. Pull back and diff

Pull the same files back from the target theme to a fresh scratch folder and diff them against the
working copy. They must be identical. That diff is the proof the push landed. Any difference is a
failed ship: say what differs and don't continue.

**Connector route:** read the written files back, retrying for up to about 30 seconds because the
write is asynchronous, and compare each with what was sent (checksum, then body). Then compare the
whole-theme manifest with the baseline manifest: only the files in section 4 of the change pack may
differ. The exact steps are in `connector-route.md` section 4. Any difference is a failed ship.

## 6. Re-check the page

Load the page on the target theme (the draft's preview) and confirm the changed thing and the key baseline numbers hold (section inventory, total
height, tracked links). Expect small differences from local (the preview bar, third-party scripts);
confirm rather than assume. If something is off, treat it as a failed ship and offer revert mode
(`revert-mode.md`).

**Connector route:** this is the first time the change is rendered, so run the whole of
`verify.md` here, on the draft's preview address (`connector-route.md` section 5), not only a
re-check. The change pack's section 5 is written now. A failed check means the draft is not ready:
fix it with the same guards (steps 2 to 5 again for the files that change) or offer revert mode.
Visitors are never affected; the live theme was not touched.

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

Short and plain: what was pushed and where, how it was proved (pulled back and identical; on the
connector route, read back and identical), what the page shows, what was logged, anything flagged
but not done (on the connector route, always that `theme check` could not run), that it is on a
draft only (publishing is theirs to do), and what to re-check and when.
