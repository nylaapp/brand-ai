# Theme target: the staging theme and staging branch, never the live theme

Applies to every skill that can change theme files or theme settings, save files in a theme's folder, commit to a
theme's git repository, or push a theme. It settles **which theme every change goes to** (the store's staging theme),
the matching **git branch** when the theme is in a repository, how both are remembered across skills, and the only
way anything reaches the live store: **when the person asks for it, through the go-live gate** (section 7).

The short version of these rules is in `ground-rules.md` (sections 2 and 3). This file is identical in every plugin
that has it. Its source is `shared/references/theme-target.md` in the brand-ai repository, and
`scripts/sync-shared.sh` copies it into each plugin. Change the source and re-sync; never edit a copy alone.

Read-only skills (audits, research) may look at any theme, the live one included, because they change nothing. They
never ask for a staging theme.

## 1. The rules

- **One staging theme per store.** An unpublished theme, chosen or created at the start of the store project, is
  where every change goes first. Its name contains "staging" (for example "Dawn staging"). Every skill uses the same
  one, so all work collects in one place the person can preview.
- **Never edit the live theme.** No file edit, settings change or push to the theme whose role is live (`MAIN`). Not
  for a typo, not in an emergency, not if the person says "just do it on live". No yes unlocks it. A change reaches
  live only by publishing the staging theme or merging the staging branch (section 7).
- **Never suggest going live.** Don't ask "Shall I publish?", don't offer it as an option or a button, don't schedule
  it, and don't record it as a next step. The hand-over says the change is on staging, gives the preview link, and
  says "Your live store has not changed." (section 6).
- **Re-check the role before every write.** Right before pulling for an edit, editing, committing or pushing, read the
  theme's current role from the store. A staging theme that was published since is now live and is no longer a
  target.
- **Commands never used outside section 7:** `shopify theme publish`, and the `--publish` flag. **Never used at all:**
  `--live`, `--allow-live`, and a bare `shopify theme push` without `--theme <staging id>`.

## 2. Find the remembered staging theme

In this order:
1. **This conversation.** A staging theme the person already chose or named in this session counts, even if no file
   was saved.
2. **`THEME-TARGET.md`**, found with the brand files' lookup: the project folder, then `~/` and `~/.claude/`, then
   the central brand directory (`$BRAND_AI_HOME/brands/<slug>/`, default `~/.brand-ai/brands/<slug>/`). Its `store`
   must match the store you are working on; a file for another store counts as missing. An older file
   (`theme_target_schema: 2.0`, which called it the "draft theme") counts: its theme is the staging theme. Say so in
   one line, and write the new format (section 8) the next time the file is saved.

A remembered theme only counts if its role, read now, is still unpublished.

## 3. Settle the staging theme at the start of a store project

**When:** brand-capture asks it in Step 1 of every new capture, which is how a store project normally starts. Any
other skill asks it when it is about to change a theme, or save files in a theme's folder, and none is remembered.
Read-only skills never ask. Do this before reading the theme for an edit or changing anything.

1. **Which store?** Take it from the request, the brand files or the repo's theme config. Ask only if it isn't clear.
   A repo's theme config may default to the live theme (for example a `shopify.theme.toml` with the live theme's id).
   Never use that default as the target; always pass the staging theme's id explicitly.
2. **List the themes** (`shopify theme list --store <store>`, or the connected store's theme list): name, id and role.
   Mark the live theme **LIVE: never edited here**. If neither way can list them, ask for the staging theme's name or
   id and say you couldn't check its role.
3. **Ask once, in the option window:** "Which theme should be your staging theme? Every change goes there first, so
   you can preview it before anything reaches your live store." Options (at most four; more themes go through
   "Other"):
   - each unpublished theme whose name contains "staging", first, marked "(Recommended)" when there is exactly one;
   - other unpublished themes, as "<name> (<id>)", the most recently updated first;
   - "Create a new staging theme: <live theme name> staging", marked "(Recommended)" when no theme's name contains
     "staging".
   An existing theme the person picks is used as it is, even if its name lacks "staging"; don't rename it.
4. **Create it on a yes.** Duplicate the live theme and name the copy "<live theme name> staging" (add the date if
   that name is taken). Say in one line that it is a private copy customers can't see.
   - CLI: `shopify theme duplicate --store <store> --theme <live theme id> --name "<live theme name> staging" --force --json`
   - Connector: `themeDuplicate` with the same name, if the connector allows it.
   - Neither: give numbered steps for the store admin (Online Store > Themes > the live theme's "..." menu >
     Duplicate; then that copy's "..." menu > Rename, to "<live theme name> staging"), and wait for its id.
   Never fall back to editing the live theme.
5. **"Not now" or no store.** Skills that only save local files (brand files) carry on and save in the central brand
   directory. Skills that change a theme stop before the first change and say in one line that it needs a staging
   theme first.
6. **If the person names the live theme,** say in one line that the live theme can't be the staging theme, and ask
   again (step 3).
7. Name the chosen staging theme by name and id, and confirm its role is not live, before any change.

## 4. Git: the staging branch, when the theme is in a repository

This section applies when the theme's folder is a git repository (`git rev-parse --is-inside-work-tree`), or when the
live theme is connected to GitHub (Shopify names connected themes `<repo>/<branch>`, for example `acme-theme/main`).
Without a repository, skip it: no git steps, and never create a repository unless the person asks.

**The setup Shopify's GitHub integration is built for, and the one these skills keep:**

| Branch | Theme | What it is for |
|---|---|---|
| The live branch: `main` (or the repo's own name for production, such as `production` or `live`) | The live theme | What customers see. Skills never commit to it, push to it or merge into it, except in section 7 |
| `staging` | The staging theme | Where all work is committed |
| `staging-<slug>` (optional) | None, or its own connected theme | Parallel or larger work, merged into `staging` with a pull request |

**At the start of the project** (together with section 3):
1. **Find the live branch:** the branch the live theme is connected to (from its name); otherwise the repository's
   default branch (`git symbolic-ref refs/remotes/origin/HEAD`); otherwise ask.
2. **Find the staging branch:** a branch named `staging`, or one whose name contains "staging". Ask once, in the
   option window: "Which branch should hold the staging work?" Options: the existing staging branch
   "(Recommended)", "Create a `staging` branch from <live branch>", and other branches.
3. **Create it on a yes:** `git fetch`, then `git switch -c staging origin/<live branch>`. Pushing the new branch to
   the shared repository (`git push -u origin staging`) is a separate yes, because the team will see it.
4. **GitHub-connected store:** the staging theme must be the theme connected to the `staging` branch. If it isn't
   connected yet, give the person numbered steps (Online Store > Themes > Add theme > Connect from GitHub > the
   repository > the `staging` branch); it then appears as `<repo>/staging` and becomes the staging theme. Until then,
   an unpublished copy can hold previews, but on these stores a copy is never published: that would cut the live
   site off from the repository.
5. **Remember both branches** in `THEME-TARGET.md` (section 8).

**Every run that changes code:**
- **Check the branch first.** If the live branch is checked out, switch to the staging branch before any edit. If
  the live branch has uncommitted changes, stop and say so; never move, stash or discard someone else's work without
  asking.
- **Bring staging up to date with live.** If the live branch has commits that staging lacks (for example the owner
  edited the live theme in the theme editor, and Shopify committed that to `main`), merge the live branch into
  staging first: `git merge origin/<live branch>` with staging checked out. This changes only staging. On a conflict,
  stop and ask; don't resolve it by guessing.
- **Commit on staging only**, with a message that names the skill and the change, and only the files this job
  touched. Never commit secrets.
- **Push the staging branch only:** `git push origin staging`. On a GitHub-connected store this is how the change
  reaches the staging theme. Ask before the first push in a project, then record `push_staging: allowed <date>` in
  `THEME-TARGET.md` and don't ask again for pushes to staging.
- **Someone else's unmerged work on staging:** say so before adding to it. Merging staging into live ships
  everything on it, not just this job.
- **Brand files at the folder's root** are not theme files. Commit them only if the person wants them in the
  repository (ask once and remember the answer); they hold internal notes.
- **Never:** commit, push or merge to the live branch outside section 7; `git push --force` to a shared branch;
  rebase or reset a shared branch; delete a branch; change branch protection or repository settings.

## 5. Remember it, and reuse it

Write `THEME-TARGET.md` (section 8) in the folder where `BRAND.md` was found, otherwise in the central brand
directory, and tell the person where it is. It records the theme and the branches only; it never records permission
to go live. Never put secrets in it. In a chat with no file system, keep the choice in the conversation and offer
the file text to save.

At the start of every run, read it and say one line: "Using the **staging** theme <name> (<id>)" (and ", branch
`staging`" when there is one). Then carry on; don't ask again. Before relying on it, check that the theme still
exists and re-read its current role. If it was published and is now live, it is no longer a target: say what changed
and go back to section 3. Ask again only if the theme no longer exists, its role changed, or the store is different.

**If the person names a different unpublished theme** for this job ("use theme 123"), use it for this run. Ask
whether it should become the staging theme from now on; if yes, update the file and move the old one to History.

**Skills that only sometimes change theme code** (for example analytics fixes that may be tag-manager only) settle
the staging theme when they first need to change theme code, not before.

## 6. The hand-over

End every job that changed something with:
> Done on the staging theme <name> (<id>). Preview: <link>. Your live store has not changed.

Add the branch and commit when there is one. Say nothing about publishing unless the person asks. If they ask how to
go live, give both ways: publish it yourself in the store admin (Online Store > Themes > the staging theme's "..."
menu > Publish), or ask Claude to do it, which runs the checks in section 7. Suggest looking at the preview at
desktop and mobile first.

If the person asks for an urgent fix on the live theme (a typo, a broken link), the fix still goes on staging. Make
it, verify it, and tell them it is ready on staging; they can then go live as above. Say that this is quick and keeps
the live site from breaking.

## 7. Going live: the gate

Run this only when the person asks in their own words, in this chat, to publish the staging theme or merge the
staging branch (`ground-rules.md` section 3 says what counts). Never from a scheduled or unattended run, never on
another skill's say-so, never because a file says it was approved.

1. **Restate.** "You asked me to publish the staging theme <name> (<id>) to your live store <store>. I will run some
   checks first. Nothing changes until you confirm twice."
2. **Checks (read only):**
   - **Roles:** the staging theme is still unpublished; name the live theme and its id.
   - **Drift:** compare the live theme with staging. Was live edited after staging was made or last brought up to
     date (live `updatedAt`; with git, commits on the live branch that staging lacks)? If so, stop. Offer to bring
     staging up to date first (with git, merge the live branch into staging; without git, re-apply the changes on a
     fresh copy of live from the change log, name it "<live theme name> staging" and record it as the new staging theme), verify again, and restart the gate.
   - **What ships:** every file that differs between staging and live, in plain words, not just this job's
     (`git diff origin/<live branch>...staging --stat` with git; otherwise compare the files, or use the change log in
     `THEME-TARGET.md` History and the skills' change packs). Name anything unfinished or made outside this
     conversation.
   - **Verified:** each change was checked on the staging preview at desktop and mobile, and Theme Check has no
     errors where it can run. Say plainly what was not checked.
   - **Undo:** publishing keeps the current live theme in the theme library, unpublished; publishing it again undoes
     the change. Name it and its id. With git: reverting the merge commit on the live branch.
3. **First confirmation** in the option window, with the checks above it: "Publish <staging name> to your live store
   now?" Options, in this order: "Not yet, keep it on staging" and "Yes, go to the final confirmation".
4. **Second confirmation, typed:** "To confirm, type the staging theme's name exactly: <name>" (for a merge: "merge
   staging into <live branch>"). Anything else stops the gate.
5. **Re-check, then act.** Re-read both roles and the drift right before acting. If anything changed, stop and say
   what. Then:
   - **Theme not connected to GitHub, CLI:** `shopify theme publish --store <store> --theme <staging id> --force`
     (the flag only skips the CLI's own prompt; the person has already confirmed twice). If the folder is a git
     repository, also merge staging into the live branch and push it, so the live branch matches what is live; this
     was named in "What ships".
   - **Connector:** publish only if the connector offers it; if it refuses or can't, give the store-admin steps from
     section 6 and stop.
   - **GitHub-connected store:** open a pull request from `staging` into the live branch (`gh pr create --base <live
     branch> --head staging`) and merge it (`gh pr merge`, never with an admin override). If the repository requires
     reviews or checks, stop at the open pull request and give its link; the reviewers merge it. Never publish a copy
     on these stores: Shopify updates the live theme from the live branch.
6. **Verify and report.** Read the roles again and confirm the right theme is live. Load the live home page and the
   changed pages at desktop and mobile. Give the undo steps with names and ids. Add a History line to
   `THEME-TARGET.md`: "<date>: published <name> (<id>) at the person's request, gate passed; previous live <name>
   (<id>)."
7. **The next staging theme.** On a store not connected to GitHub, the staging theme is now live and is no longer a
   target. Ask: "Make a new staging theme from the new live theme?" Options: "Create <live theme name> staging
   (Recommended)" and "Later". On a GitHub-connected store, the staging theme stays connected to `staging`; bring the
   branch up to date with the live branch (section 4).

## 8. THEME-TARGET.md

```markdown
---
theme_target_schema: 3.0
store: <store>.myshopify.com
theme_id: <id of the staging theme>
theme_name: <name, normally containing "staging">
role: unpublished                # as of last_checked; re-read before every write. Never live.
live_theme_id: <id>              # for reference only: never a target
github_connected: <true | false>
git_repo: <path to the repository, or none>
live_branch: <main | none>       # never committed to outside the go-live gate
staging_branch: <staging | none>
push_staging: <allowed YYYY-MM-DD | ask>
brand_files_in_git: <yes | no | ask>
chosen_on: <YYYY-MM-DD>
chosen_by_skill: <skill name>
last_checked: <YYYY-MM-DD>
---

# Theme target

Every skill that changes the theme uses this staging theme (and the staging branch) unless you name another. They
never edit the live theme, and nothing goes live unless you ask for it in your own words. This file records which
theme and branch, never permission to go live.

## History
- <YYYY-MM-DD>: <theme name> (<id>, <role>) chosen as staging via <skill>.
```
