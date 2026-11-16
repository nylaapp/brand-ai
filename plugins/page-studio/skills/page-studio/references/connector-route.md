# Connector route: change a draft theme through the Shopify connection, with no Shopify CLI

The second way to do the shared steps in this folder. `page-create`, `page-edit-content` and
`page-edit-design` use it only when `setup-check.md` chose it: the Shopify CLI is not installed and
signed in, and the Shopify connector can read **and** change themes on the right store. If the CLI
is ready, the CLI route in `ship-to-draft.md`, `verify.md` and `revert-mode.md` runs exactly as
written and nothing here applies.

The connector is any connected Shopify tool that runs Admin GraphQL (`graphql_query`,
`graphql_mutation`, `graphql_schema`). If a call is rejected for an unknown field, check the field
with `graphql_schema` before retrying; never guess.

Every promise in `ship-to-draft.md` holds on this route: never the live theme, never publish, only
the files the change pack lists, proof that the write landed, nobody's edits overwritten, no
credential typed. Only the means differ.

| Step | CLI route | Connector route |
|---|---|---|
| List themes, make a draft | `shopify theme list`, `shopify theme duplicate` | `themes` query, `themeDuplicate` (section 2) |
| Working copy | The whole theme, pulled to a scratch folder | **No local copy of the theme.** Only the files the change touches: read, saved as `baseline/`, edited in `work/` |
| `theme check` | Runs on the working copy | **Cannot run** (it is part of the CLI): check 8 is "Can't tell" (section 6) |
| First rendered check | Local preview, before anything is sent | **On the draft, after the write** (safe: visitors never see a draft) (section 5) |
| Send the files | `shopify theme push --only ... --nodelete` | `themeFilesUpsert` with an explicit file list |
| Proof it landed | Pull back and diff | Read back and compare checksums (section 4) |
| Revert | Push the baseline copies | Write the baseline copies back; delete the files the change added |

## 1. Detect, read-only

Run these silently. They read; they change nothing. All must pass for the route to be chosen.

```graphql
query { currentAppInstallation { accessScopes { handle } } }
query { shop { myshopifyDomain } }
query { themes(first: 50) { nodes { id name role processing } } }
```

- **Access:** the scope handles include `read_themes` **and** `write_themes`.
- **Right store:** `myshopifyDomain` is the store the page belongs to. A connector that points at
  another store is not ready, however well it answers. Never switch the connector's store silently.
- **Reads work:** the themes query returns the themes with their roles.

Scopes alone do not prove the connector may change themes. Shopify's docs say changing theme files
needs `write_themes` **and** an exemption from Shopify, and the exemption cannot be read. Do not
test it with a trial write. The first real write (the duplicate in section 2, or the first upsert to
the chosen draft) is the test: if Shopify refuses it with an access or exemption error, nothing was
changed (read the draft again to confirm), and `setup-check.md` falls back to the CLI guidance.

## 2. The calls

Theme ids look like `gid://shopify/OnlineStoreTheme/<number>`; the number is the id the CLI and the
admin address show. Pass values as variables, never by editing the query text.

**List themes and roles** (`theme-target.md` section 3, step 2): the themes query above. The role
`MAIN` is the live theme: mark it **LIVE: never edited here**.

**Read one theme's role** (before every read-for-edit, write and delete):

```graphql
query ($id: ID!) { theme(id: $id) { id name role processing processingFailed } }
```

**Make a draft** (`theme-target.md` section 3, step 4). This is the only call that takes the live
theme's id, as the thing to copy; it reads the live theme and changes nothing on it.

```graphql
mutation ($id: ID!, $name: String) {
  themeDuplicate(id: $id, name: $name) {
    newTheme { id name role processing }
    userErrors { field message }
  }
}
```

Name it `<live theme name> draft <YYYY-MM-DD>`. Read the new theme back: its role must be
`UNPUBLISHED` (or `DEVELOPMENT`), never `MAIN`, and `processing` must be false before any write.
Wait and read again until it is; if `processingFailed` is true, say so and stop.

**Read files** (up to 50 names per call; `*` matches part of a name; leave out `body` for a cheap
list). Check `userErrors` and that every requested name came back; the store may return fewer
files than asked to stay within its size limit, so ask again for the missing names.

```graphql
query ($id: ID!, $names: [String!], $after: String) {
  theme(id: $id) {
    id role
    files(filenames: $names, first: 50, after: $after) {
      edges { node { filename checksumMd5 size
        body { ... on OnlineStoreThemeFileBodyText { content } } } }
      pageInfo { hasNextPage endCursor }
      userErrors { code filename }
    }
  }
}
```

**Theme manifest** (every file's name, checksum and size, no bodies, so it is small): the same
query with `names` left out, `first: 250`, and only `filename checksumMd5 size` selected; follow
`pageInfo` until `hasNextPage` is false. Used in sections 3 and 4.

**Write files.** Variables: `themeId`, and `files` as a list of `{ filename, body: { type: TEXT,
value: "<the whole file>" } }`, at most 50 per call, each file whole (the call replaces the file).

```graphql
mutation ($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    job { id }
    upsertedThemeFiles { filename }
    userErrors { code field filename message }
  }
}
```

**Delete files** (only files the change itself removes, each named, never a wildcard):

```graphql
mutation ($themeId: ID!, $files: [String!]!) {
  themeFilesDelete(themeId: $themeId, files: $files) {
    deletedThemeFiles { filename }
    userErrors { code field filename message }
  }
}
```

Any `userErrors` entry is a failed write for that call: show it plainly and stop. A rate-limit
reply is not a failure: wait a few seconds and send the same call again.

## 3. The guards

These are the connector route's version of the CLI route's flags. They are not optional.

1. **One pinned target.** The change pack names one theme id. Every call takes its `themeId` from
   the pack. Never use "the main theme", a role filter, or a theme config default as the target. The
   only call that may take another id is the duplicate's source (section 2).
2. **Role gate, every time.** Right before every read-for-edit, write and delete, read the target's
   role from the store (section 2). Continue only when it is `UNPUBLISHED` or `DEVELOPMENT`. `MAIN`
   is live: stop and say "This is the LIVE theme, so I won't edit it." Also stop for `DEMO`,
   `LOCKED`, `ARCHIVED` or anything else unexpected. A draft published since you chose it is live.
3. **Right store, every time.** `myshopifyDomain` still matches the page's store.
4. **Only these mutations:** `themeDuplicate`, `themeFilesUpsert` and `themeFilesDelete`. Never
   `themePublish`, `themeCreate`, `themeUpdate`, `themeDelete` or `themeFilesCopy`, and no mutation on
   products, pages, menus, metafields or anything outside theme files. Publishing is the person's step.
5. **Only the files the change pack lists.** An explicit filename list in every write, equal to the
   change pack's section 4: this is the connector route's `--only`. An upsert never deletes anything,
   which is the equivalent of `--nodelete`; a delete names each file and happens only when the change
   deletes it.
6. **Nobody edited since the baseline.** Right before the write, read the touched files again.
   Their checksum (and, if the store gives none, their body) must equal the baseline's. Any
   difference: stop, name the files, and re-capture or reconcile; never overwrite. A file the pack
   says is new must still not exist.
7. **No credential typed or passed.** The connection signs in through the Claude app, by the
   person. Never ask for, paste or store a token or password. If the connection drops or is refused,
   stop and ask the person to reconnect it themselves (`setup-check.md`, row K).

## 4. Reading, writing and proving

**Baseline copies.** Read each file the change will touch and save it **exactly as received** in
`baseline/`. Compute its md5 on the computer and compare it with `checksumMd5`: a copy that does not
match is not a backup, so read it again. Also save the whole-theme manifest as
`baseline/manifest.json`. A file you cannot read exactly (an image, a font) is not changed on this
route: use the CLI route, or ask the person to change it in the store admin.

**Editing.** Put the file in `work/`, make the change there, and note lines added and removed
against `baseline/`. Check each edited JSON file parses before it is written, and each setting value
sits inside its schema's range. A very large file must be sent whole: if that is too much for the
connection, say so and offer the CLI route; never send a shortened file.

**Writing.** Only after the guards in section 3 pass, in the order the change needs: a template
only after the files it refers to exist. Send at most 50 files per call.

**Proof.** The write is asynchronous: a reply with no `userErrors` means Shopify accepted the job,
not that the files changed. So:

1. Read the written files back (section 2), waiting a few seconds between tries, for up to about 30
   seconds.
2. Compare each file's `checksumMd5` with the md5 of the file you sent. If the store gives no
   checksum, or the two differ, compare the bodies. Any difference other than line endings or a
   final newline is a **failed ship**: name the files, do not continue, offer revert. If only line
   endings or a final newline differ, say so and record it.
3. Read the whole-theme manifest again. Every file that is not listed in the change pack's
   section 4 must have the same checksum as in the baseline manifest. A difference is either
   someone else's edit (say so) or an unplanned change (a failed ship).

A success message is still not proof; the read-back is.

## 5. Preview and the first rendered check

There is no local preview. The first time the change is rendered is on the draft, which visitors
never see:

`https://<store>.myshopify.com/<path>?preview_theme_id=<draft id>`

Open it in the browser Claude uses (a real browser session: the same address fetched without one
returns the live theme), read the id the page reports (`Shopify.theme.id`) and confirm it is the
draft's, then run `verify.md`. A bar at the top of the page says it is a preview; expect that.
Before the write, only source checks are possible; they are not verification (`verify.md`, "On the
connector route").

Say this once in the plan, in plain words: the change is checked on the private draft after it is
written, not on this computer first. If the draft is one other people work in, offer a fresh copy
instead (section 2), because a failed check is visible there until it is fixed or reverted.

## 6. What cannot run

- **`theme check`** is part of the CLI. On this route `verify.md` check 8 is "Can't tell: the code
  checker needs the Shopify CLI", and the baseline records the same. Say so in the plan and get the
  person's agreement once. Shopify's own file checks still run when the files are written (their
  `userErrors` are read); the source checks in `verify.md` and the rendered checks make up for the rest.
- **A usage search over the whole theme** (the files that use a shared section, snippet or style)
  is possible but heavy: read the template, section-group and layout files by name pattern and
  search them; for a snippet, a stylesheet or a token, most of the theme's files are needed. If that
  is too much for the connection, say so and offer the CLI route.
- **Images and fonts** (binary files) are not read or written on this route.

## 7. If the connection stops

Stop. Read the draft's touched files to see exactly what was written, and tell the person which
files changed, in plain words. Ask them to reconnect the Shopify connection themselves, then start
again from the guards. Never retry a write blind, and never move to a different theme to get past it.
