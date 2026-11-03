---
name: "brand-docs"
description: "Open the Brand AI documentation inside Claude: every plugin and skill, what it does, example prompts, how they work together and what each one needs. Use whenever the user says \"show the documentation\", \"open the docs\", \"how do the Brand AI skills work\", \"what skills are there\", \"which skill should I use\", \"help with Brand AI\" or asks what a Brand AI plugin or skill does. Needs no link, login or internet: the page ships with this plugin."
---

# Brand AI documentation

The documentation is a single self-contained page bundled with this skill at `assets/index.html` (relative to this SKILL.md). It is rebuilt from the marketplace each release, so it matches the installed version.

## Open it

1. Find `assets/index.html` next to this SKILL.md.
2. Open it for the user, using the first route that works:
   - **Artifact tool available:** publish that file as a private Artifact (`Artifact` with `file_path` set to the page, title "Brand AI Docs", icon "book") and give the user the link. Do not edit the page.
   - **Otherwise, on a computer with a browser:** open the file locally (`open` on macOS, `xdg-open` on Linux, `start` on Windows) and say where it is.
   - **Neither:** give the file's full path and say it opens in any browser.
3. Say in one line what is in it: the plugins grouped by job, each with example prompts, steps, what it produces and what it needs.

## Answer from it, not from memory

When the user asks about one plugin or skill instead of the whole thing ("what does fact-check do?"), read `assets/index.html`, answer from the entry for that plugin, then offer to open the full page.

## Rules

- Read-only. Never change the page, the marketplace or any plugin.
- Do not send the page or its contents anywhere other than the user's own Artifact or browser.
- If `assets/index.html` is missing, say the plugin install looks incomplete and suggest reinstalling `brand-docs@brand-ai`.
