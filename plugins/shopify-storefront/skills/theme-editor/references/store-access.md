# Reaching the store: connector first, CLI second, offline last

Every theme change in this skill is the same four moves: **find the live theme and the staging theme, read the
files, write the changed files back to the staging theme, read them back**. Only the delivery differs. The staging
theme is the store's one unpublished theme whose name contains "staging" (`theme-target.md`). Pick the first that
works:

| Situation | Use |
|---|---|
| A Shopify connector is connected in this chat (tools such as `get-shop-info`, `graphql_query`, `graphql_mutation`) | **Connector.** No terminal, works in a regular Claude chat, Cowork or Claude Code. Preferred for owners |
| No connector, but the Shopify CLI is signed in on this machine (`shopify theme list --store <store>` answers) | **CLI** |
| Neither, or the user asked for a dry run | **Offline:** edit a copy of the local theme folder, say clearly that nothing reached the store |

Never ask for, type or store passwords, tokens or API keys. If the connector says the store isn't connected, tell the
user: the **store owner** (or a staff account with every permission the app asks for) connects it once in Claude's
connector settings; staff accounts often see "You need permission to update Shopify Claude Connector App".

**Live theme connected to GitHub?** (its name looks like `<repo>/<branch>`, or THEME-SPECIFICS.md says so.) Then
read `github-stores.md` first: the staging theme is the one connected to the `staging` branch, and going live is a
merge of `staging` into the live branch, through the gate. Never publish a theme on such a store.

## Connector

First call `get-shop-info` and check the domain is the store in BRAND.md / AGENTS.md. If it isn't, stop and say so;
never switch stores without the user asking (switching revokes the current store's access).

1. **Themes:**
   ```graphql
   query { themes(first: 20) { nodes { id name role updatedAt } } }
   ```
   `role: MAIN` is live. Never write to it: the connector blocks it anyway ("Theme file writes against the live
   storefront are blocked").
2. **Staging theme:** use the remembered one (`theme-target.md` sections 2 and 5). It must still exist, and its
   `role`, read right before every write, must not be `MAIN`. If none is remembered, settle it (`theme-target.md`
   section 3). Duplicating live is only for creating the staging theme, named "<live theme name> staging", never a
   copy per job:
   ```graphql
   mutation($id: ID!, $name: String) {
     themeDuplicate(id: $id, name: $name) { newTheme { id name role } userErrors { field message } }
   }
   ```
   If `themeDuplicate` is refused or errors, ask the owner to click **Online Store → Themes → (live theme) … →
   Duplicate**, then rename that copy to "<live theme name> staging" and use it. (Verified on 2026-11-09: reads, file writes to an unpublished theme, live writes
   refused. Not yet verified through the connector: `themeDuplicate`.)
3. **Read files** (up to 50 names per call; theme JSON can be large, so ask only for what you need):
   ```graphql
   query($id: ID!) {
     theme(id: $id) {
       files(filenames: ["config/settings_data.json", "sections/header-group.json", "templates/index.json"], first: 3) {
         nodes { filename updatedAt body { ... on OnlineStoreThemeFileBodyText { content } } }
       }
     }
   }
   ```
   For a section's settings list, read `sections/<type>.liquid` and use its `{% schema %}`.
4. **Keep the "before" text.** Before writing, keep each file's original content: in the project folder as
   `campaigns/<slug>/before/<path>` when you have a folder, otherwise inside the hand-over (the before → after
   table must hold every old value, so a revert never depends on memory).
5. **Write** (the app asks the user to confirm each write; up to 50 files per call):
   ```graphql
   mutation($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
     themeFilesUpsert(themeId: $themeId, files: $files) {
       upsertedThemeFiles { filename }
       userErrors { field code message }
     }
   }
   ```
   with `files: [{"filename": "templates/index.json", "body": {"type": "TEXT", "value": "<whole file text>"}}]`.
   Send the whole file, keep its `/* ... */` header comment, and make sure it parses as JSON first.
   **Section code before templates:** if you changed a section's schema, write the section in one call and the
   template in a second call. Shopify silently drops template settings the schema doesn't know yet.
6. **Read back** the files you wrote and confirm only the planned values changed. Stop on any `userErrors` and quote
   them; don't retry blindly or work around a block.
7. **Preview:** `https://<store-domain>/?preview_theme_id=<numeric id>` (the number at the end of the theme gid).
   Editor: `https://admin.shopify.com/store/<handle>/themes/<numeric id>/editor`. Password-protected stores need the
   storefront password to view the preview. Nothing here publishes: going live happens only when the owner asks,
   through the gate (`theme-target.md` section 7).

## CLI

```bash
shopify theme list --store <store>
shopify theme duplicate --store <store> --theme <live-id> --name "<live theme name> staging" --force --json   # only to create the staging theme
shopify theme pull --store <store> --theme <staging-id> --path <work-folder> --no-color   # check it says "has been pulled"
shopify theme push --store <store> --theme <staging-id> --path <work-folder> --only <file> [--only <file>]
```

Never `--live`, `--allow-live` or `--publish`; never a bare `shopify theme push` without `--theme`. `theme pull`
doesn't accept `--json`. Same rule as above: push changed section files first, templates in a second push, then pull
the template back to check.

## Offline

Copy the local theme folder, edit the copy, validate it, and report the result as a dry run with the exact files and
values that would be written.
