# Stores whose live theme is connected to GitHub

Read this before any theme work when the live theme is connected to a GitHub repository. On these stores it replaces
"make a copy, then publish it": publishing a copy would replace the connected theme and cut the site off from the repo.

## How to tell

- The live theme's name looks like `<repo>/<branch>` (for example `brandname-theme/main`). Shopify's GitHub
  integration names connected themes that way.
- Or `THEME-SPECIFICS.md` / `AGENTS.md` says the store is connected to GitHub.

## The staging gate

Every connected store has a **`staging` branch** in the same repository, connected to its own unpublished theme
(named `<repo>/staging`). That theme is where all work happens and where every preview link points.

| Step | What happens |
|---|---|
| Work | Write changes to the **staging theme** only (connector writes or `shopify theme push --theme <staging-id>`). Never make a separate copy, never touch the live theme |
| Record | Shopify commits each change made on the staging theme back to the `staging` branch, so the branch history is the change log |
| Preview | `https://<store-domain>/?preview_theme_id=<staging-id>` |
| Go live | Merge `staging` into `main` with a pull request. Shopify then updates the live theme from `main`, usually within a minute or two. The owner or the agency approves the merge; Claude never merges without that OK in the chat |
| Undo | Put the "before" values back on the staging theme and merge again, or revert the merge on `main` |

## Before every piece of work: staging must match live

The owner can still edit the live theme in the theme editor, and Shopify commits those edits to `main`. So staging
can fall behind:
1. Compare the staging theme with the live theme for the files you'll touch (read both, as in the drift check).
2. If live has changes staging doesn't, `staging` needs `main` merged into it first. With access to the repository,
   do that merge (it touches only the `staging` branch). Without access, stop and ask whoever owns the repository.
3. Never start new work on a staging branch that still holds someone else's unmerged changes without saying so: a
   merge to `main` ships everything on `staging`, not just your part.

## When there's no staging theme yet

Say so, and ask the owner or agency to connect one, once: in Shopify, **Online Store → Themes → Add theme → Connect
from GitHub**, choose the repository and the `staging` branch. If the `staging` branch doesn't exist yet, it's made
from `main` first. Until it's connected, you may build a preview on an unpublished copy to show the idea, but never
publish that copy.

## Notes

- One piece of work at a time on `staging`. Parallel work needs its own branch (`staging-<slug>`) and its own
  connected theme: ask first.
- Files outside the theme folders (AGENTS.md, BRAND.md, THEME-SPECIFICS.md) can live at the repository root.
- The connector can't merge on GitHub. The person with repository access does the merge, or Claude does it where it
  has GitHub access and the OK.
