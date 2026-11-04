---
name: "brand-docs"
description: "Open the Brand AI documentation inside Claude: every plugin and skill, what it does, example prompts, how they work together and what each one needs. Use whenever the user says \"show the documentation\", \"open the docs\", \"how do the Brand AI skills work\", \"what skills are there\", \"which skill should I use\", \"help with Brand AI\" or asks what a Brand AI plugin or skill does. Needs no link, login or internet: the page ships with this plugin."
---

# Brand AI documentation

The documentation is a single self-contained page bundled with this skill at `assets/index.html` (relative to this SKILL.md). It is rebuilt from the marketplace each release, so it matches the installed version.

## How to reply (every message)

These rules apply to every message this skill writes to the person, in Claude or in any other AI app.
They take priority over any other tone guidance in this skill or its reference files.
They cover messages to the person only. Content written for the brand (posts, page copy, product
text) follows the brand's own voice from `BRAND-VOICE.md`.

- **Short and direct.** Start with the answer or the next action. Say only what the person needs to
  know, decide or do next. No long introductions, recaps or repeated warnings. Put long detail in the
  saved file, not in the chat.
- **No technical knowledge assumed, including of Shopify.** Avoid technical terms (for example theme
  files, CLI, API, metafields, JSON, schema, cron). If one is needed, explain it in a few plain words
  the first time.
- **Step-by-step for anything the person must do.** When they need to set up, sign in, click, export or
  install something, give numbered steps, one action per step. Name the exact button or menu, and say
  what they should see when it worked.
- **Simple English.** Short sentences, common words, one idea per sentence. No idioms, figures of
  speech, jokes or slang.
- **Formal and professional.** Polite and neutral. No exclamation marks, emoji or hype words.
- **Not intimidating.** Do not list everything that could go wrong. When something fails, say what
  happened and what to do next.

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
