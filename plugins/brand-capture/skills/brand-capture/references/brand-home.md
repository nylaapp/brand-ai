# Brand home: the draft theme's folder

Where brand-capture and competitor-research keep the files they write: in the folder of a **draft theme** the
person chooses, so the brand files travel with the theme and every later skill that customizes it finds them in
the working folder. Both skills ask for the draft theme (this file says how) and save there. Choosing and
remembering the theme follows `theme-target.md` (sections 1 to 4 and 6); its live-theme assurance (section 5)
doesn't apply here, because these skills write local files only and change nothing on the store.

The files: `BRAND.md`, `BRAND-VOICE.md`, `design.md`, `BRAND-QUESTIONS.md`, `BRAND-REQUESTS.md`, `BRAND.html`,
`COMPETITORS.md`, and `THEME-TARGET.md` (which records the theme).

## 1. Ask which draft theme

Ask in brand-capture's Step 1 (question C), in the same message as the sources question. Skills that run later
(competitor-research, and any skill that has to save a brand file) ask only when no draft theme is remembered.

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

1. **The current folder**, if it looks like that. Say so and ask the person to confirm it is the chosen draft.
   `shopify.theme.toml`, when it exists, can name the theme (a hint, not proof).
2. **Another folder**, if the person names one. Check it looks like a theme.
3. **Not on this computer yet.** Offer to pull the draft into a new or empty folder the person names, and do it
   only on a yes: `shopify theme pull --store <store> --theme <id> --path <folder>` (it reads the draft and writes
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
