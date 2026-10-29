# Brand home: the draft theme's folder

Where brand-capture and competitor-research keep the files they write: in the folder of a **draft theme** the
person chooses, so the brand files travel with the theme and every later skill that customizes it finds them in
the working folder. Both skills ask for the draft theme (this file says how) and save there. Choosing and
remembering the theme follows `theme-target.md` (sections 1 to 4 and 6); its live-theme assurance (section 5)
doesn't apply here, because these skills write local files only and change nothing on the store. The one thing
written elsewhere is the optional shared copy for the rest of the team (section 8), made only on the person's yes:
it is only a copy, and this folder stays the source of truth.

The files: `BRAND.md`, `BRAND-VOICE.md`, `design.md`, `BRAND-QUESTIONS.md`, `BRAND-REQUESTS.md`, `BRAND.html`,
`COMPETITORS.md`, and `THEME-TARGET.md` (which records the theme).

## 1. Ask which draft theme

Ask in brand-capture's Step 1 (question C), in the same message as the sources question. Skills that run later
(competitor-research, and any skill that has to save a brand file) ask only when no draft theme is remembered.
If no local folder exists for the project yet, section 2's first check comes before this question.

1. **Is one remembered?** Look as `theme-target.md` section 1 says, through
   `BRAND-HOME.md` too (section 5).
   - **A new capture always asks**, even when a theme is remembered, with the remembered one first: "Same draft
     as before: <name>?" A capture is the run that sets where the brand lives.
   - **Every other run** says one line ("Saving to the **draft** theme <name>, folder <path>.") and goes on. The
     person can name another draft at any time; then switch, as `theme-target.md` section 4 says.
2. **If none, ask once.** Settle the store, list its themes and ask which draft to use, as `theme-target.md`
   section 2 says, with these differences:
   - **Offer draft and unpublished themes only.** The live theme is not offered: the brand files belong with the
     working copy. A person who names the live theme anyway is told once that a draft is better (a published draft
     counts as live, and later skills ask for extra assurance before touching it); if they still want it, use it.
     The files are written locally and nothing is pushed.
   - **Offer "another" and "none yet".**
3. **No draft theme yet.** Don't create one (`theme-target.md` section 2, step 4). Say how: Online Store, Themes,
   the live theme's menu, Duplicate. Then either wait, or carry on with section 6 ("no draft yet") and let the
   next skill that works on a theme ask again.
4. **Not a Shopify store.** Skip the question and use section 6.

## 2. Find the theme's folder

The folder on this computer that holds the draft theme's files: it has `layout/theme.liquid`, `templates/`,
`sections/` and `config/settings_schema.json`.

**First, is there a local folder at all?** Check before asking which draft theme (section 1), and ask only when
there is none. A folder counts if it is remembered (`BRAND-HOME.md`'s `path`, or the folder holding
`THEME-TARGET.md`) or if the current folder looks like a theme (step 1 below). If none counts, ask once, in one
short message:

> I don't see a folder on this computer for **<store or brand>** yet. Please create one named **<slug>**, where
> you keep your project files (for example `~/Documents/<slug>/`), and tell me its path.

- **Name it, and say where.** The name is the project's slug, the one used for the central brand directory
  (`brands/<slug>/`): usually the store's .myshopify.com name, or the theme's name. Always give a suggested
  location with it.
- **Create nothing without saying where.** The person creates the folder. If they ask you to, say the exact path
  first, including any parent folders that don't exist yet, and wait for a yes.
- **Use it in the steps below.** The folder they name is the folder for step 3 (the pull goes into it).
- **Skip it** when there is no file system, when it isn't a Shopify store, or when the person has said there is
  no draft theme yet (section 6); in that case don't ask question C again either.
- **Once only.** When the folder is remembered (section 4: `BRAND-HOME.md`, `THEME-TARGET.md`), never ask again
  for that project.

1. **The current folder**, if it looks like that. Say so and ask the person to confirm it is the chosen draft.
   `shopify.theme.toml`, when it exists, can name the theme (a hint, not proof).
2. **Another folder**, if the person names one. Check it looks like a theme.
3. **Not on this computer yet.** Offer to pull the draft into a new or empty folder the person names (the one
   asked for above, if there was one), and do it only on a yes:
   `shopify theme pull --store <store> --theme <id> --path <folder>` (it reads the draft and writes only into that
   folder). Never sign in for the person.
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
- **Committing:** never unless asked. When asked, say first that `BRAND-QUESTIONS.md` and `COMPETITORS.md` are
  internal, and check the repo isn't public or shared with the client.
- Scratch (the scan JSON, the evidence folder) stays out of this folder.

## 4. Remember it

1. `THEME-TARGET.md` next to `BRAND.md` (`theme-target.md` sections 3 and 6, `chosen_by_skill: brand-capture`).
   Later theme skills read it and don't ask again.
2. `BRAND-HOME.md` in the central brand directory (`$BRAND_AI_HOME/brands/<slug>/`, default
   `~/.brand-ai/brands/<slug>/`; create the folder), so a skill run from any folder finds the files:

```markdown
---
brand_home_schema: 1.0
brand: <brand>
store: <store>.myshopify.com
path: <absolute path to the draft theme's folder>
updated: <YYYY-MM-DD>
---

# Brand home

The brand files for <brand> are kept in the folder named by `path`: the draft theme's folder. Skills that
look here follow it. `THEME-TARGET.md` in that folder says which draft theme it is.
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

## 6. When there is no draft theme to save in

Use these only after asking, and say so in the report so the person can fix it later.
- **No draft yet, or not a Shopify store:** save in the central brand directory, as before (`$BRAND_AI_HOME/brands/<slug>/`,
  default `~/.brand-ai/brands/<slug>/`). Write no `THEME-TARGET.md`. The next skill that works on a theme asks.
- **No file system (a chat or a project):** hand the files over for download. Say to save them in the root of the
  draft theme's folder, and offer the `THEME-TARGET.md` text (`theme-target.md` section 6) to save beside them.

## 7. Moving existing files into a draft theme

When the brand files are found in the central directory or another folder and a draft theme is now chosen, offer
once to copy them in: `BRAND.md`, `BRAND-VOICE.md`, `design.md`, `BRAND-QUESTIONS.md`, `BRAND-REQUESTS.md`,
`BRAND.html` and `COMPETITORS.md`, whichever exist. Copy byte for byte (never edit them in the move), then point
`BRAND-HOME.md` at the new folder. Leave the old copies where they are and say they can be removed; delete
nothing. The same steps move the files to another draft later (a replacement draft, a new checkout). If the
person says no, leave everything where it is and save new files next to `BRAND.md`.

## 8. Optional shared copy

An optional second copy of the non-confidential files, for the rest of the team. It runs after section 4, once the
draft theme's folder is settled and the files are written there (brand-capture Step 6b; competitor-research Step 4).
It adds a copy and changes nothing in that folder.

- **A copy, never a move, never the source.** The draft theme's folder stays the source of truth. Section 5 stays
  as it is: skills read the local folder first, then `BRAND-HOME.md`, and never read from a shared copy or fall
  back to one.
- **If a shared copy and the local file disagree, the local file wins.** Say this plainly when you ask. Edits made
  in a shared copy are not read back: the next update replaces them, so a change goes to whoever works in the local
  folder.
- **Only these files:** `BRAND.md`, `BRAND-VOICE.md`, `design.md`, `BRAND.html` and `COMPETITORS.md`, whichever
  exist, copied byte for byte. **Never `BRAND-QUESTIONS.md` or `BRAND-REQUESTS.md`**: they hold internal and
  client-facing questions and stay local only. `THEME-TARGET.md`, `BRAND-HOME.md` and scratch aren't copied either.
- **Not offered when section 6 applies** (no draft theme yet, not a Shopify store, no file system): there is no
  draft theme's folder to copy from. It is offered once the files are in one (section 7).

### Ask once

After the local files are written, ask once, with your environment's question tool if it has one:

> Do you also want a shared copy of the brand files for the rest of the team? Your local folder stays the master:
> the copy is only a copy, and if the two ever differ, the local file wins. Choose one, both, or neither:
> 1. **A shared Google Drive folder**
> 2. **A `brand/` folder in the theme repo**
> 3. **No, local only**

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
   them. The theme repo is the draft theme's folder; if it isn't a git checkout, say that `brand/` is then only a
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
  Moving the files to another draft (section 7) keeps `shared_copy`; update the copies from the new folder.
- **Report it** next to the draft theme line (`report-template.md`): where the shared copy is, or that none was
  chosen.
