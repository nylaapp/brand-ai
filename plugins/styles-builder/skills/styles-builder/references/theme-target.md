# Theme target: a draft theme, never the live theme

Applies to every skill that can change theme files or theme settings, or push a theme. It settles
**which theme to work on**, how that choice is remembered across skills, and the one rule that never
bends: **these skills never edit, push to or publish over the live theme.** Work always happens on a
draft (unpublished) theme.

This file is the same in every plugin that changes themes (page-studio, styles-builder,
accessibility-audit and analytics). Plugins can't read each other's folders, so each keeps a copy;
change them together and keep them identical.

Read-only skills (audits, research) may look at any theme, the live one included, because they
change nothing. Observing the live theme is fine; editing it is not.

## 1. The rule

- **Never edit the live theme.** Not for a typo, not in an emergency, not if the person says "just do
  it on live", not with a yes. No yes unlocks it, and none is asked for.
- **Always a draft.** Edits go to an unpublished draft theme: an existing one the person names, or a
  new copy of the live theme made for the job.
- **Never publish.** Publishing a draft over the live theme is a live change. The person does it
  themselves in the store admin (section 5). These skills never run a publish command and never use a
  flag that allows a live push (`--allow-live`).
- **Re-check the role before every write.** Right before pulling for edit, editing, or pushing, read the
  theme's current role from the store. A draft that was published since is now live and is no longer a
  target.

## 2. Find the remembered theme

In this order:
1. **This conversation.** A theme the person already chose or named in this session counts, even if
   no file was saved.
2. **`THEME-TARGET.md`**, found with the brand files' lookup: the project root, then the user's local
   environment, then the central brand directory (`$BRAND_AI_HOME/brands/<slug>/`, default
   `~/.brand-ai/brands/<slug>/`). Its `store` must match the store you are working on; a file for
   another store counts as missing.

A remembered theme only counts if its role, read now, is still a draft or unpublished (section 4).

## 3. If there is none, settle a draft first

Do this before reading or editing anything else in the theme.
1. **Which store?** Take it from the request or the repo's theme config. Ask only if it isn't clear.
   A repo's theme config may default to the live theme (for example a `shopify.theme.toml` with the
   live theme id). Never use that default as the target; always pass an explicit draft theme id.
2. **List the themes** (`shopify theme list --store <store>`, or the connected store's theme list):
   name, id and role. If neither can be read, ask for the id of a draft theme and its role, and say
   you couldn't verify it. Mark the live theme **LIVE: never edited here**.
3. **If there are draft or unpublished themes, ask once:** "Is there already a draft you want me to
   use?" Offer each one (name and id), plus "none of these: make a new copy of the live theme".
   Recommend the one that looks like the person's current working draft, if it is obvious.
4. **If there are none, create one** without asking again, and say so in one line: a private copy of
   the live theme that visitors can't see. Use the theme CLI (`shopify theme duplicate --store <store>
   --theme <live theme id> --name "<live theme name> draft <YYYY-MM-DD>"`), or the connected store if it
   can duplicate a theme. If neither can, ask the person to duplicate the live theme in the store admin
   (Online Store > Themes > the live theme's menu > Duplicate) and give you the new theme's id; wait for
   it. Never fall back to editing the live theme.
5. **If the person names the live theme anyway,** say in one line that these skills never edit it, and
   carry on with step 3 or 4.
6. Name the chosen draft by id and confirm its role is not live before any edit.

## 4. Remember it, and reuse it

Write `THEME-TARGET.md` (format in section 6) in the folder where `BRAND.md` was found, otherwise in
the central brand directory, and tell the person where it is. It records the theme only; there is no
"approved" field. Never put secrets in it. In a chat with no file system, keep the choice in the
conversation and offer the file text to save.

At the start of every run, read the remembered theme and say one line: "Using the **draft** theme
<name> (<id>), chosen on <date>." Then carry on; don't ask again. Before relying on it, check that
the theme still exists and re-read its **current role**: if it was published and is now live, it is no
longer a target. Say what changed and go back to section 3 for a new draft. Ask again only if the
theme no longer exists, its role changed, or the store is different.

**If the person names a different draft** ("on theme 123", "use the new draft"), use it for this run,
make it the remembered theme, add the previous one to the file's history, and say so in one line.

**Skills that only sometimes change theme code** (for example analytics fixes that may be GTM-only)
settle the theme at the moment they first need to change theme code, not before.

## 5. Going live is the person's step

When the work on the draft is verified and the person wants it live, tell them plainly that these
skills don't publish and how to do it: in the store admin, Online Store > Themes, open the draft's
menu and choose **Publish**, or ask whoever manages the store. Suggest checking the draft's preview
first, and offer the QA entry and change pack as the checklist. After they publish, that theme is live
and is no longer a target: the next job starts from a fresh draft (section 3).

If the person asks you to edit the live theme because something is urgent (a typo, a broken link),
the answer is still no: make the fix on a draft, verify it, and give them the publish steps. Say that
this is quick and keeps the live site from breaking.

## 6. THEME-TARGET.md

```markdown
---
theme_target_schema: 2.0
store: <store>.myshopify.com
theme_id: <id of the draft>
theme_name: <name>
role: <draft | preview>          # as of last_checked; re-read before every write. Never "live".
live_theme_id: <id>              # for reference only: never a target
chosen_on: <YYYY-MM-DD>
chosen_by_skill: <skill name>
last_checked: <YYYY-MM-DD>
---

# Theme target

Skills that change theme files use this draft theme unless you name another draft. They never edit the
live theme. This file records which draft, never permission to edit anything live.

## History
- <YYYY-MM-DD>: <theme name> (<id>, <role>), chosen via <skill>.
```
