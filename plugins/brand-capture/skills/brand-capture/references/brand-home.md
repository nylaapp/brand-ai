# Brand home: the staging theme's folder

Where brand-capture, voice-builder and competitor-research keep the files they write: in the folder of the store's
**staging theme**, the unpublished theme every change goes to first, so the brand files travel with it and every
later skill that customizes it finds them in the working folder. brand-capture settles the staging theme at the
start of the store project (this file says how); the others use the remembered one and ask only when there is none.
Choosing, creating and remembering the theme, and the staging branch, follow `theme-target.md` (sections 2 to 5 and
8); its never-edit-the-live-theme rule (section 1) is met here because these skills write local files only and
change nothing customers see. The one thing
written elsewhere is the optional shared copy for the rest of the team (section 8), made only on the person's yes:
it is only a copy, and this folder stays the source of truth.

The files: `BRAND.md`, `BRAND-VOICE.md`, `design.md`, `BRAND-QUESTIONS.md`, `BRAND-REQUESTS.md`, `BRAND.html`,
`COMPETITORS.md`, and `THEME-TARGET.md` (which records the theme).

## 1. Ask which theme is the staging theme

Ask in brand-capture's Step 1 (question C), in the same message as the sources question. Skills that run later
(competitor-research, and any skill that has to save a brand file in a theme's folder) ask only when no staging
theme is remembered. voice-builder writes BRAND-VOICE.md next to BRAND.md, wherever that is.
If no local folder exists for the project yet, section 2's first check comes before this question.

1. **Is one remembered?** Look as `theme-target.md` section 2 says, through
   `BRAND-HOME.md` too (section 5). A remembered theme counts only if its role, read now, is still unpublished.
   - **A new capture always asks**, even when a theme is remembered, with the remembered one first: "Same staging
     theme as before: <name>?" A capture is the run that starts the store project and sets where the brand lives.
   - **Every other run** says one line ("Saving to the **staging** theme <name>, folder <path>.") and goes on. The
     person can name another unpublished theme at any time; then switch, as `theme-target.md` section 5 says.
2. **If none, ask once.** Settle the store, list its themes and ask which theme is the staging theme, as
   `theme-target.md` section 3 says: "Which theme should be your staging theme? Every change goes there first, so
   you can preview it before anything reaches your live store. The brand files are saved in its folder; nothing is
   sent to your store."
   - **Offer unpublished themes only**, those whose name contains "staging" first. The live theme is never offered.
     A person who names the live theme is told in one line that the live theme can't be the staging theme, and is
     asked again (`theme-target.md` section 3, step 6).
   - **Offer "Create a new staging theme: <live theme name> staging"**, marked "(Recommended)" when no theme's name
     contains "staging", and "Not now".
   - **When the theme's folder is a git repository**, settle the staging branch in the same step, as a separate
     question in the same call (`theme-target.md` section 4).
3. **Create it on a yes.** Duplicate the live theme and name the copy "<live theme name> staging"
   (`theme-target.md` section 3, step 4). Say in one line that it is a private copy customers can't see: creating it
   changes nothing on the live store. If neither the CLI nor the connector can duplicate it, give the numbered
   store-admin steps from that section and wait for its id. Then find or pull its folder (section 2).
4. **"Not now", or not a Shopify store.** Don't ask again in this run, and use section 6. The next skill that changes
   a theme asks again.

## 2. Find the theme's folder

The folder on this computer that holds the staging theme's files: it has `layout/theme.liquid`, `templates/`,
`sections/` and `config/settings_schema.json`.

**First, is there a local folder at all?** Check before asking which theme is the staging theme (section 1), and ask only when
there is none. A folder counts if it is remembered (`BRAND-HOME.md`'s `path`, or the folder holding
`THEME-TARGET.md`) or if the current folder looks like a theme (step 1 below). If none counts, ask once, in the
option window (options: "I created it, I will give the path", "Create it for me (I will confirm the path)", "Not
a Shopify store, or no staging theme for now"), with this text as the question:

> I don't see a folder on this computer for **<store or brand>** yet. Please create one named **<slug>**, where
> you keep your project files (for example `~/Documents/<slug>/`), and tell me its path.

- **Name it, and say where.** The name is the project's slug, the one used for the central brand directory
  (`brands/<slug>/`): usually the store's .myshopify.com name, or the theme's name. Always give a suggested
  location with it.
- **Create nothing without saying where.** The person creates the folder. If they ask you to, say the exact path
  first, including any parent folders that don't exist yet, and wait for a yes.
- **Use it in the steps below.** The folder they name is the folder for step 3 (the pull goes into it).
- **Skip it** when there is no file system, when it isn't a Shopify store, or when the person has said "Not now"
  to a staging theme (section 6); in that case don't ask question C again either.
- **Once only.** When the folder is remembered (section 4: `BRAND-HOME.md`, `THEME-TARGET.md`), never ask again
  for that project.

1. **The current folder**, if it looks like that. Say so and ask the person to confirm it is the staging theme's.
   `shopify.theme.toml`, when it exists, can name the theme (a hint, not proof).
2. **Another folder**, if the person names one. Check it looks like a theme.
3. **Not on this computer yet** (always so for a staging theme just created). Offer to pull the staging theme into
   a new or empty folder the person names (the one asked for above, if there was one), and do it only on a yes:
   `shopify theme pull --store <store> --theme <staging id> --path <folder>` (it reads the staging theme and writes
   only into that folder). Never sign in for the person.
4. **No file system (a chat).** Section 6.

## 3. Write the files

- **At the folder's root**, beside `assets/`, `config/`, `sections/` and the rest, never inside them. Only the
  theme's own folders are part of the theme, and `shopify theme push` sends only those, so the store never
  receives these files.
- **Never in `assets/`.** Every file there is served from the store's public CDN, and these files hold internal
  notes: the client questions, competitor research, the never-say list and who approves.
- **Don't touch `.shopifyignore`** or any theme file. Don't push, and don't ask to.
- **An existing `design.md`** in the folder (any case, for example `DESIGN.md`) is the client's visual source:
  adopt it, never write a second one.
- **Committing:** never unless asked (`theme-target.md` section 4: brand files at the folder's root are not theme
  files; ask once and remember the answer in `brand_files_in_git`). When asked, commit on the staging branch only,
  say first that `BRAND-QUESTIONS.md` and `COMPETITORS.md` are internal, and check the repo isn't public or shared
  with the client.
- Scratch (the scan JSON, the evidence folder) stays out of this folder.

## 4. Remember it

1. `THEME-TARGET.md` next to `BRAND.md` (`theme-target.md` sections 5 and 8, `chosen_by_skill: brand-capture`),
   with the staging theme and, when there is a repository, the live and staging branches. Later theme skills read it
   and don't ask again.
2. `BRAND-HOME.md` in the central brand directory (`$BRAND_AI_HOME/brands/<slug>/`, default
   `~/.brand-ai/brands/<slug>/`; create the folder), so a skill run from any folder finds the files:

```markdown
---
brand_home_schema: 1.0
brand: <brand>
store: <store>.myshopify.com
path: <absolute path to the staging theme's folder>
updated: <YYYY-MM-DD>
---

# Brand home

The brand files for <brand> are kept in the folder named by `path`: the staging theme's folder. Skills that
look here follow it. `THEME-TARGET.md` in that folder says which staging theme it is.
```

Tell the person both paths. If the central directory can't be written, skip `BRAND-HOME.md`, say so, and say the
files are found from the theme's folder.

## 5. Find them later (every skill)

`brand-context.md` section 2 gives the order. The theme's folder is the project root whenever a skill runs
there. From anywhere else, the central brand directory's `BRAND-HOME.md` names it:
- Follow `path` only if the folder exists and holds the file you want. Confirm the front matter `brand`, `site`
  or `store` as for any other match.
- If the folder is gone or has no brand files, say so in one line and ask for the new folder. Don't guess, and
  don't fall back to a stale copy.

## 6. When there is no staging theme to save in

Use these only after asking, and say so in the report so the person can fix it later.
- **"Not now", or not a Shopify store:** save in the central brand directory, as before (`$BRAND_AI_HOME/brands/<slug>/`,
  default `~/.brand-ai/brands/<slug>/`). Write no `THEME-TARGET.md`. The next skill that works on a theme asks.
- **No file system (a chat or a project):** hand the files over for download. Say to save them in the root of the
  staging theme's folder, and offer the `THEME-TARGET.md` text (`theme-target.md` section 8) to save beside them.

## 7. Moving existing files into the staging theme's folder

When the brand files are found in the central directory or another folder and a staging theme is now chosen, offer
once to copy them in: `BRAND.md`, `BRAND-VOICE.md`, `design.md`, `BRAND-QUESTIONS.md`, `BRAND-REQUESTS.md`,
`BRAND.html` and `COMPETITORS.md`, whichever exist. Copy byte for byte (never edit them in the move), then point
`BRAND-HOME.md` at the new folder. Leave the old copies where they are and say they can be removed; delete
nothing. The same steps move the files to another staging theme later (a new staging theme after the old one went
live, a new checkout). If the
person says no, leave everything where it is and save new files next to `BRAND.md`.

## 8. Optional shared copy

An optional second copy of the non-confidential files, for the rest of the team. It runs after section 4, once the
staging theme's folder is settled and the files are written there (brand-capture Step 6b; competitor-research Step 4).
It adds a copy and changes nothing in that folder.

- **A copy, never a move, never the source.** The staging theme's folder stays the source of truth. Section 5 stays
  as it is: skills read the local folder first, then `BRAND-HOME.md`, and never read from a shared copy or fall
  back to one.
- **If a shared copy and the local file disagree, the local file wins.** Say this plainly when you ask. Edits made
  in a shared copy are not read back: the next update replaces them, so a change goes to whoever works in the local
  folder.
- **Only these files:** `BRAND.md`, `BRAND-VOICE.md`, `design.md`, `BRAND.html` and `COMPETITORS.md`, whichever
  exist, copied byte for byte. **Never `BRAND-QUESTIONS.md` or `BRAND-REQUESTS.md`**: they hold internal and
  client-facing questions and stay local only. `THEME-TARGET.md`, `BRAND-HOME.md` and scratch aren't copied either.
- **Not offered when section 6 applies** (no staging theme yet, not a Shopify store, no file system): there is no
  staging theme's folder to copy from. It is offered once the files are in one (section 7).

### Ask once

After the local files are written, ask once in the option window (`AskUserQuestion`, multi-select on; plain
numbered message only if there is no question tool):

> Do you also want a shared copy of the brand files for the rest of the team? Your local folder stays the master:
> the copy is only a copy, and if the two ever differ, the local file wins.
> Options: **A shared Google Drive folder**, **A `brand/` folder in the theme repo**, **No, local only** (this one
> cannot be combined with the others).

### Option 1: a shared Google Drive folder

1. **The folder:** a top-level `Shopify Brand & Competitor Research/` with one subfolder per store, named after the
   store: its .myshopify.com name, or the project slug. Look for the top-level folder before creating anything,
   so a second store or run adds to it and never makes a duplicate.
2. **A Google Drive connector or tool is available in this session:** use it to create or update the files in the
   store's subfolder. Upload them as they are (don't convert them to Google Docs), after saying the folder path.
   Don't change sharing settings: if you had to create the top-level folder, tell the person to share it with the
   team, not the client, since `COMPETITORS.md` is internal (section 3).
3. **None is available:** tell the person the folder to create, `Shopify Brand & Competitor Research/<store>/`,
   and the files (with their local paths) to put in it. They can sync the files themselves, or re-run this step
   once Drive is connected. Record the choice all the same.

### Option 2: a `brand/` folder in the theme repo

1. Add `brand/` at the root of the theme repo, beside `assets/`, `sections/` and `config/`, never inside any of
   them. The theme repo is the staging theme's folder; if it isn't a git checkout, say that `brand/` is then only a
   second local copy.
2. Copy the same files into it.
3. **`brand/` is not part of the theme and is never pushed to the store**, the same rule as the root-level files
   in section 3 (`THEME-TARGET.md` and the rest): `shopify theme push` sends only the theme's own folders. Don't
   touch `.shopifyignore`, don't push, and don't ask to.
4. **Committing** follows section 3: never unless asked. If the person wants `brand/` under version control,
   suggest committing it, ask first, say that `COMPETITORS.md` is internal, and check the repo isn't public or
   shared with the client.

### Record the choice, and later runs

- **Record it** in `BRAND-HOME.md`'s front matter as an optional key under `path`, and update `updated`:
  `shared_copy: drive`, `shared_copy: repo` or `shared_copy: both`. Leave the key out when the person chose local
  only. `brand_home_schema` stays 1.0. If `BRAND-HOME.md` couldn't be written (section 4), say the choice is
  remembered only in this conversation.
- **Asked once**, in the run that writes the brand files. Later runs (apply-answers, add-design, split-voice, a
  competitor-research refresh) don't ask again: when `shared_copy` is set they update the copies it names after the
  local files change, saying in one line what was updated; when it is absent they offer nothing, and the report says
  none was chosen. A person who asks for a shared copy later runs this section from "Ask once".
- **Updating a copy** replaces each shared file with the local one. When a shared file differed, say which.
  Moving the files to another staging theme (section 7) keeps `shared_copy`; update the copies from the new folder.
- **Report it** next to the staging theme line (`report-template.md`): where the shared copy is, or that none was
  chosen.
