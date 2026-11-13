---
name: cw-sale-campaign
description: Charlotte Welch (Hautebox) store. Put a time-boxed sale or campaign on a Shopify store's theme (homepage hero, announcement bar, optional countdown, sale colours) in the brand's own voice, on an unpublished preview copy, with a revert plan for when it ends. Works through the Shopify connector in a normal Claude chat (no terminal), or the Shopify CLI. Reads BRAND.md and BRAND-VOICE.md for names, tone and claim limits. Use whenever someone says "put the sale on the homepage", "update the site for our campaign", "the homepage should reflect the X% off sale", "add a countdown", "BFCM / Black Friday / holiday sale prep", "launch the promo", "take the sale down", "revert the campaign", or sends a campaign video, graphic or brief and wants the website to match, even if they don't say "theme" or "Shopify".
---

# Shopify sale campaign

Turn a campaign brief (an offer, its dates, maybe a video or graphic) into on-brand theme changes that a busy
owner can preview, approve and later undo. The person using this is usually a solo founder with ten minutes: do the
thinking, show a before → after list and a preview link, and keep them out of the JSON.

## Effort

| | Quick change on a ready preview (one surface, facts known) | Full campaign (bar, hero, colours, hand-over) |
|---|---|---|
| Time | target 1 to 2 minutes (not yet measured) | 4 to 6 minutes, measured 2026-11-12 (offline dry runs) |
| Tokens | not yet measured | about 125,000 to 135,000 |

Use Opus 5.5 at high effort or above: dates, claims and "everything vs sitewide" are what weaker settings get wrong
(inferred from the AYA brand runs, not measured for this skill). If the run passes 15 minutes, something is looping:
stop and say what's blocking.

## What good looks like

- Every surface tells the same story with the same facts: offer, dates, link. A shopper never sees "35% off" in the
  hero and "Free shipping" alone in the bar.
- The copy sounds like the brand (BRAND-VOICE.md) and never over-claims (BRAND.md → Claim limits).
- **Only what was asked.** If they asked for the homepage, change the homepage surfaces; offer anything else
  (countdown, badges, sale colours) as a short list of extras they can say yes to.
- One approval before anything is written, nothing goes live without the owner, and the live theme is untouched.
- When the sale ends, the site can go back to exactly how it was, and the owner was told how and when.

## Step 0: Read the project

1. **Files.** Look for `AGENTS.md` / `CLAUDE.md` (store, live theme id, house rules), `BRAND.md`, `BRAND-VOICE.md`
   and `THEME-SPECIFICS.md`: in the project folder, in the chat project's files, or attached to the message. If
   BRAND.md is missing, say so and offer the brand-capture skill; you can continue with the site's own copy as the
   voice reference, but say the copy is unchecked against a brand file.
2. **Store access:** read `references/store-access.md` and pick connector, CLI or offline. Say which in one line.
3. **Theme:** read `theme_info` in `config/settings_schema.json`. Read `THEME-SPECIFICS.md` if the project has one
   (it records this store's quirks and every code change already made: don't undo them). Then the theme reference:
   **Honey** (Archer Commerce) → `references/honey.md`; anything else → `references/other-themes.md`.

## Step 1: Get the campaign facts (ask once, offer choices)

Pull the facts from the brief, the campaign asset (read video frames or image text) and the live site first. Then ask
for what is still missing in **one message**, with choices wherever you can (A / B / other), never open questions
when the options are knowable.

| Fact | Why it matters |
|---|---|
| Campaign name and offer ("Cousin Walk Sale, 35% off sitewide") | headline and bar copy |
| Start and end date **and time**, store time zone | countdown and revert date; "ends Sunday" is not enough |
| What the discount covers and how it applies (automatic or code; exclusions) | Shopify discounts never apply to gift cards, so "everything" is false on any store that sells them: say "sitewide". A code must appear in the copy |
| Where the button goes | an existing collection (check it exists) |
| Media | look at what the live hero already plays first: owners often uploaded a clean cut of the same footage, which works better behind theme text than a video with words burned in. A new file must be uploaded by the owner to Content → Files (neither the connector nor the CLI uploads local files) |

- A date or time that reads two ways ("Dec 1 at midnight" = start or end of Dec 1) is a question with two options,
  never a guess: the countdown, the copy and the discount must end at the same moment.
- Check the discount exists if the connector can read discounts; otherwise put "discount set up in Shopify admin?"
  in the owner's to-do. A sale banner over a checkout that charges full price is the worst outcome of this skill.

## Step 2: Safe copy and "before" values

Never edit the live theme; the owner edits it in the editor, so local files go stale fast. Make or reuse an
unpublished copy and read the files you'll touch (`references/store-access.md`). Keep the original text of every
file before changing it:

- **Project folder available:** `python scripts/snapshot.py save <theme-folder> campaigns/<slug> <files...>` writes
  `campaigns/<slug>/before/` and a `manifest.json` (`restore` puts them back). Keep the slug short (`cousin-walk`):
  Windows refuses paths over 260 characters. Keep `campaigns/` outside the theme folder so it's never pushed.
- **No folder (connector in a chat):** the before → after table in the hand-over must hold every old value.

## Step 3: Plan, write the copy, get one yes

Decide each surface: change, add, or leave. Reuse what the owner built (an existing sale hero is a head start).

1. **Announcement bar:** offer, end date, link. On every page, so it does the most work. One line, under about 60
   characters on mobile. Make sure it stands apart from the header colour.
2. **Homepage hero:** headline (campaign name), one supporting line (offer and dates), one button. Text needs a scrim
   or contrast against the media. If the hero video is vertical, check its desktop height (theme reference).
3. **Countdown** (an extra unless asked): only for a real deadline; hidden when it completes, with an "on complete"
   message as a fallback.
4. **Sale colours** (an extra unless asked): sale price and promo badge from the brand palette, badge text ≥ 4.5:1.
5. **Product badges and per-product timers** (an extra): product tags or metafields are store data; list exactly
   which products would change, and record them so the revert can remove them.

Copy rules, in order: facts identical everywhere; the brand's names exactly (BRAND.md → Terminology); Claim limits
respected (no "everything" with exclusions, no fake scarcity); BRAND-VOICE.md's length, humour and turns of phrase,
echoing the campaign asset's own words (the owner already approved them); shopper dates ("Nov 10 to 17", never
"11/17"); no em dashes in customer copy.

**Freshness (up to 3, never applied without a yes):** while reading the page, note anything that makes the store
look out of date (a past season's hero left enabled, an old offer in the bar, a stale headline) and offer it.

**Approval:** show one compact table, surface · before · after, plus the extras you're offering and anything you
couldn't confirm (discount, media). Write nothing until the user says yes to that table.

## Step 4: Write, read back, look

1. Edit the files: keep `/* ... */` header comments and existing ids; new sections get a unique id and go in
   `order`. Validate: JSON parses, section types exist, every setting id exists in that section's schema, dates match
   the theme's format.
2. Write to the preview copy only (`references/store-access.md`: section code before templates). Read back and
   confirm only the planned values changed.
3. **Look at it on desktop and mobile** (every visual change, every time): with a browser tool, open the
   preview at about 390, 768, 1440 and 1920 pixels wide; check text isn't cut off, the bar fits one line on mobile,
   the hero isn't several screens tall, the button is visible. Without a browser, say the visual check wasn't run.
4. **Theme code changed?** (rare: only when no setting can do it.) Mark the code with a `Nyla:` comment, save the
   file in `theme-mods/`, and add a row to `THEME-SPECIFICS.md` (create it if missing) so a theme update or another
   agent never loses it. Prefer settings and section Custom CSS over code.

## Step 5: Hand over, including the end

Write `campaigns/<slug>/campaign.md` (or give the same content in chat): facts, the before → after table, preview
theme id, end date and time, revert steps. Then tell the owner briefly:

- what changed (the table, not a diff) and the preview link;
- their to-do: approve, then publish it themselves (Online Store → Themes → Publish) or tell you to; confirm the
  discount; upload media if needed;
- what happens at the end: a countdown hides itself; everything else stays until reverted. Offer to schedule the
  revert if scheduling is available.

Publishing replaces the live theme with the copy, so edits made to live after the duplicate are lost. If the owner
edited live since, or more than a day has passed, re-duplicate and re-apply instead of publishing an old copy.

## Quick path (demo mode)

When BRAND.md exists, the facts are known and a fresh preview copy exists: skip the intake, read only the files for
the surface asked about, show the before → after for that surface, get the yes, write, read back, give the preview
link. One surface, one approval, about a minute of work. Everything else is an offer for later.

## Reverting a campaign

"The sale's over" / "revert the campaign": read `campaigns/<slug>/campaign.md`. On a fresh copy of the current live
theme, put back the "before" values for each surface (or `snapshot.py restore` if nothing was edited since; check with
`snapshot.py diff`). Keep anything the owner changed since and anything listed in THEME-SPECIFICS.md. Remove product
tags or metafields the campaign added. Preview, get the OK, mark the campaign file `Reverted <date>`.

## Report format

```
Campaign: <name> · <offer> · <start> to <end> (<tz>)
Preview: <link>   Editor: <link>
Changed: <surface: before → after, one line each>
Offered, not done: <extras>
Owner to do: <approve / publish / confirm discount / upload media>
Revert: <date> · campaigns/<slug>/campaign.md
```
