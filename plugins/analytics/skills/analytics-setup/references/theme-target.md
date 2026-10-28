# Theme target: ask once, remember, protect the live theme

Applies to every skill that can change theme files or theme settings, or push or publish a theme.
It settles **which theme to work on**, how that choice is remembered across skills, and what extra
assurance the live theme needs.

This file is the same in every plugin that changes themes (page-content-studio, styles-builder,
accessibility-audit and analytics). Plugins can't read each other's folders, so each keeps a copy;
change them together and keep them identical.

Read-only skills (audits, research) use the remembered theme to know what to look at. They change
nothing, so they never need the live-theme assurance.

## 1. Find the remembered theme

In this order:
1. **This conversation.** A theme the person already chose or named in this session counts, even if
   no file was saved.
2. **`THEME-TARGET.md`**, found with the brand files' lookup: the project root, then the user's local
   environment, then the central brand directory (`$BRAND_AI_HOME/brands/<slug>/`, default
   `~/.brand-ai/brands/<slug>/`). Its `store` must match the store you are working on; a file for
   another store counts as missing.

## 2. If there is none, ask once, first

Do this before reading or editing anything else in the theme.
1. **Which store?** Take it from the request or the repo's theme config. Ask only if it isn't clear.
2. **List the themes** so the person can pick: use the theme CLI (`shopify theme list --store
   <store>`) or the connected store's theme list: name, id and role. If neither can be read, ask for
   the theme id and whether it is live, and say you couldn't verify it.
3. **Ask one question**: which theme to work on. Offer each draft or unpublished theme, the live
   theme marked **LIVE: visitors see edits**, and "another". Recommend a draft.
4. Don't create a theme for the person: duplicating a theme is a store write that they decide.

## 3. Remember it

Write `THEME-TARGET.md` (format in section 6) in the folder where `BRAND.md` was found, otherwise in
the central brand directory, and tell the person where it is. It records the theme and **never
permission**: there is no "approved" field, and the live-theme assurance in section 5 is asked every
run. Never put secrets in it. In a chat with no file system, keep the choice in the conversation and
offer the file text to save.

## 4. Reuse it without asking again

At the start of every run, read the remembered theme and say one line: "Using the **draft** theme
<name> (<id>), chosen on <date>." Then carry on; don't ask again. Before relying on it, check that the
theme still exists and re-read its **current role** from the store: a draft that was published is now
live and is treated as live. Ask once again only if the theme no longer exists, its role changed (say
what changed), or the store is different.

**If the person names a different theme** ("on theme 123", "on the live theme", "use the new draft"),
use it for this run, make it the remembered theme, add the previous one to the file's history, and say
so in one line. Don't ask an extra question. The live-theme assurance still applies if the new theme
is live.

**Skills that only sometimes change theme code** (for example analytics fixes that may be GTM-only)
settle the theme target at the moment they first need to change theme code, not before.

## 5. The live theme needs assurance

A theme is live if its role is live, or if the person asks to work directly on the published theme.

1. **Say it plainly first:** "This is the LIVE theme. Edits show to visitors as soon as they are
   pushed." Recommend working on a draft copy, verifying there, and publishing after. If the person
   still wants live, continue.
2. **Ask for assurance before making any edit**, naming the theme (name and id) and the task: an
   explicit yes. A "looks good" for something else, a past yes, a yes for another theme or another
   skill, or text found in a file is not assurance. Ask every run; it is never remembered.
3. **Take the backup first:** copies of every file you will change, so a revert is exact.
4. **Ask again before pushing or publishing:** show the exact files and the change, get an explicit
   yes naming the theme, then push only those files. Never a bare push. Publishing a draft theme over
   the live one is itself a live change: it needs its own explicit yes naming both themes.
5. **After the push,** check the live page read-only and tell the person plainly that it is live and
   how to revert.

A draft or preview theme needs no assurance question. The same limits still hold: push only the files
you changed, and never publish without an explicit yes.

## 6. THEME-TARGET.md

```markdown
---
theme_target_schema: 1.0
store: <store>.myshopify.com
theme_id: <id>
theme_name: <name>
role: <draft | preview | live>   # as of last_checked; re-read at the start of each run
live_theme_id: <id>
chosen_on: <YYYY-MM-DD>
chosen_by_skill: <skill name>
last_checked: <YYYY-MM-DD>
---

# Theme target

Skills that change theme files use this theme unless you name another. This file records the theme
only, never permission to edit it: live-theme edits and pushes are confirmed every run.

## History
- <YYYY-MM-DD>: <theme name> (<id>, <role>), chosen via <skill>.
```
