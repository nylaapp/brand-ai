# Stores whose live theme is connected to GitHub

Read this before any theme work when the live theme is connected to a GitHub repository. It is the short version of
`theme-target.md` sections 4 (the staging branch) and 7 (going live) for these stores; where they differ,
`theme-target.md` wins. On these stores, publishing a theme would replace the connected theme and cut the live site
off from the repository, so a theme is never published here: going live is a merge.

## How to tell

- The live theme's name looks like `<repo>/<branch>` (for example `brandname-theme/main`). Shopify's GitHub
  integration names connected themes that way.
- Or `THEME-SPECIFICS.md` / `AGENTS.md` says the store is connected to GitHub.

The branch in the live theme's name is the **live branch** (usually `main`). Skills never commit to it, push to it or
merge into it outside the go-live gate.

## The staging theme and branch

The staging theme is the theme connected to the **`staging` branch** of the same repository (named
`<repo>/staging`). All work happens there, and every preview link points to it.

| Step | What happens |
|---|---|
| Work | Write changes to the staging theme only (connector writes, `shopify theme push --theme <staging-id>`, or commits on `staging`). Never make a separate copy per job, never touch the live theme or the live branch |
| Record | Shopify commits each change made on the staging theme back to the `staging` branch, so the branch history is the change log |
| Push | Push the `staging` branch only (`git push origin staging`). Ask before the first push in a project, then record it in `THEME-TARGET.md` (`theme-target.md` section 4) |
| Preview | `https://<store-domain>/?preview_theme_id=<staging-id>` |
| Go live | Only when the person asks in their own words in this chat, through the go-live gate (`theme-target.md` section 7). Open a pull request from `staging` into the live branch and merge it, never with an admin override. If the repository requires reviews or checks, stop at the open pull request and give its link; the reviewers merge it. Shopify then updates the live theme from the live branch, usually within a minute or two |
| Undo | Revert the merge commit on the live branch, which is also a go-live (on request, through the gate) |

## Before every piece of work: bring staging up to date with live

The owner can still edit the live theme in the theme editor, and Shopify commits those edits to the live branch. So
`staging` can fall behind:
1. Check whether the live branch has commits that `staging` lacks. Without the repository, compare the staging theme
   with the live theme for the files you'll touch.
2. If it does, merge the live branch into `staging` first (`git merge origin/<live branch>` with `staging` checked
   out). This changes only `staging`. On a conflict, stop and ask. Without access to the repository, stop and ask
   whoever owns it.
3. Never start new work on a staging branch that still holds someone else's unmerged changes without saying so: a
   merge into the live branch ships everything on `staging`, not just your part.

## When there's no staging theme yet

Say so, and give the person numbered steps to connect one, once: in Shopify, **Online Store → Themes → Add theme →
Connect from GitHub**, choose the repository and the `staging` branch. If the `staging` branch doesn't exist yet,
offer to create it from the live branch first (`theme-target.md` section 4; pushing it is a separate yes). Until it's
connected, an unpublished copy may hold a preview to show the idea, but on these stores a copy is never published.

## Notes

- One piece of work at a time on `staging`. Parallel or larger work gets its own branch (`staging-<slug>`), merged
  into `staging` with a pull request, and may get its own connected theme whose name still contains "staging": ask
  first.
- Files outside the theme folders (AGENTS.md, BRAND.md, THEME-SPECIFICS.md) can live at the repository root. Commit
  brand files only if the person wants them in the repository.
- Never force-push, rebase or reset a shared branch, delete a branch, or change branch protection.
- The connector can't merge on GitHub. The person with repository access merges, or Claude does it where it has
  GitHub access, only through the gate.
