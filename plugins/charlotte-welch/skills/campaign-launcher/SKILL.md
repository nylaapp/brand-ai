---
name: campaign-launcher
description: Charlotte Welch (Hautebox) store. Plans and runs a time-boxed campaign (seasonal, product launch, discount or promotion, or a mix) from one sentence, uploaded materials or links. It shows a one-line plan (name, type, exact dates, channels) and a calendar file, then readies the website on an unpublished preview copy (announcement bar, homepage hero, optional countdown) in the brand's voice, drafts email, SMS and ads as stubs, and schedules Launch and Stop. Works through the Shopify connector in a normal Claude chat (no terminal) or the Shopify CLI. Reads BRAND.md and BRAND-VOICE.md. Use whenever someone says "new campaign", "plan a campaign", "put the sale on the homepage", "we're launching a new product", "launch the promo", "BFCM or holiday sale prep", "add a countdown", "launch or stop the campaign", "take the sale down", "the sale's over", or sends a campaign brief, graphic or video, even without saying "theme" or "Shopify".
---

# Campaign launcher

Turn a campaign idea, or a folder of campaign materials, into a plan the owner can check in one line. Then get every
channel as ready as it can be on its own, and launch and stop the campaign on time. The person using this is usually
a solo founder with ten minutes: ask one question, show one plan, come back with something ready to approve, and
keep them out of the JSON.

## Words

- **Campaign:** one named push with an exact start and end, on one or more channels.
- **Launch / Stop:** make it visible to shoppers / take it down and put everything back (`references/launch-stop.md`).
- **Preview copy:** an unpublished copy of the live theme. All website work happens there; the live theme is never
  edited.
- **Ready / Draft route:** materials final, so prepare everything for a one-step launch approval / materials still
  in progress, so stage and draft only, and launch nothing.

## Effort

| | One change on a ready preview (quick path) | Plan step only | Full campaign (plan, website, stub drafts, schedule) |
|---|---|---|---|
| Time | target 1 to 2 minutes (not yet measured) | about 3 minutes, measured 2026-11-13 (one fresh offline run, 17 tool calls) | website part 4 to 6 minutes, measured 2026-11-12 (offline dry runs); stubs and schedule not yet measured |
| Tokens | not yet measured | about 130,000, mostly reading the project the first time | about 125,000 to 135,000 for the website part |

Use Opus 5.5 at high effort or above: dates, claims and "everything vs sitewide" are what weaker settings get wrong
(inferred from the AYA brand runs, not measured for this skill). If the run passes 15 minutes, something is looping:
stop and say what's blocking.

## What good looks like

- **One question, one plan, one yes** before any work starts. The plan line is right: name, type or types, an exact
  start and end with time and time zone, and channels.
- **Every surface and draft tells the same story** with the same facts: offer, dates, link. A shopper never sees
  "35% off" in the hero and "Free shipping" alone in the bar.
- The copy sounds like the brand (BRAND-VOICE.md) and never over-claims (BRAND.md → Claim limits).
- **Only what was planned.** Extras (countdown, badges, sale colours) are offered as a short list, never added
  unasked.
- **Nothing goes live without the owner.** The live theme is untouched until they publish.
- **Launch and Stop each have a time and a way of happening**, and Stop puts the site back exactly as it was.

## Step 0: Read the project

1. **Files.** Look for these:
   - `AGENTS.md` / `CLAUDE.md`: the store, the live theme id and the house rules;
   - `BRAND.md` and `BRAND-VOICE.md`;
   - `THEME-SPECIFICS.md`.

   Look in the project folder, in the chat project's files, or in what's attached to the message. If BRAND.md is
   missing, say so and offer the brand-capture skill. You can continue with the site's own copy as the voice
   reference, but say the copy hasn't been checked against a brand file.
2. **Store access:** read `references/store-access.md` and pick connector, CLI or offline. Say which in one line.
3. **Theme:** read `theme_info` in `config/settings_schema.json`. Read `THEME-SPECIFICS.md` if the project has one: it
   records this store's quirks and every code change already made, so don't undo them. Then read the theme
   reference: **Honey** (Archer Commerce) → `references/honey.md`; anything else → `references/other-themes.md`.
4. **Existing campaigns.** Check what already exists, so you never ask what you can look up:
   - `campaigns/*/campaign.md`;
   - unpublished themes named for a campaign;
   - discounts, if the connector can read them;
   - what the live site's announcement bar and hero say right now (offline: use the latest pulled theme and say how
     old it is).

   This answers the first two questions: does this campaign already exist, and is it live?
5. **Store time zone.** Every date in the plan is in it.
   - Connector: `query { shop { ianaTimezone } }`.
   - CLI or offline: AGENTS.md or BRAND.md, if they say.
   - Otherwise it's one of the plan's open questions, with the likeliest zone first. Never copy the zone from an
     example in this skill.

## Step 1: One open question

If the message already describes the campaign or includes materials or links, skip straight to Step 2. Otherwise ask
exactly one question, in plain chat text (it's open-ended, so no option window):

> What's the campaign? Describe it in a sentence, and drop in anything you already have: a brief, copy, images, a
> video, or links.

Any mix of a description, uploads and links is enough. Read all of it:
- video frames and any text burned into them;
- text in images;
- copy documents;
- linked pages (a landing page, a social post).

**To read a video:** take about one frame per second with `ffmpeg`. If it isn't installed, Python's
`imageio_ffmpeg.get_ffmpeg_exe()` often provides it. Tile the frames into one image and look at it. Write the
frames to a scratch or temporary folder, never into the project or theme folder. If nothing can read the video, use
what the project files say about it, or ask what it says.

Ask nothing else yet. A sentence plus one graphic usually answers everything Step 2 needs.

## Step 2: The plan (one screen, one yes)

Work out each fact from what they gave, the project and the store. Ask only for what's still missing or ambiguous.

| Fact | Values | Rule |
|---|---|---|
| Name | e.g. "Cousin Walk Sale" | From the materials; otherwise suggest one |
| Status | New · Exists, not live (where) · Live now (since when, which channels) | From Step 0.4. Never ask what you can see |
| Type | **One or more** of: Seasonal · Product launch (a new or changed product or line) · Discount or promotion | Multi-select. A Thanksgiving 35% off sale is Seasonal + Discount |
| Dates | Start date and time, end date and time, store time zone (Step 0.5) | **Exact calendar dates only.** Turn "a week from now, for three days" into real dates and show them. A date or time that reads two ways ("Dec 1 at midnight") becomes a question with two options: the countdown, the copy and the discount must end at the same moment |
| Stop time | When the website goes back | The end, by default. If the end is after 9 pm, offer the next morning at 9:00 as an option; the discount and the countdown still end on time |
| Offer | What, how it applies (automatic or code), exclusions | Discount type only. Shopify discounts never apply to gift cards, so on any store that sells them say "sitewide", never "everything". A code must appear in the copy, so if neither the materials nor the store show whether there's a code, ask it as an open question (options: "Automatic at checkout" and "A code"). Check the discount exists if the connector can read discounts; otherwise it goes in the owner's to-do. A sale banner over a checkout that charges full price is the worst outcome of this skill |
| Channels | Website · Email · SMS · Ads | All four by default. Only the website is connected; the rest are stubs (`references/channels.md`) |
| Materials | Final · In progress · None | Decides the route |
| Link | Where the buttons go | An existing collection or product: check it exists |
| Media | What the hero will show | Look at what the live hero already plays first: owners often uploaded a clean cut of the same footage, which works better behind theme text than a video with words burned in. A new file has to be uploaded by the owner to Content → Files (neither the connector nor the CLI uploads local files) |

**When the request and the materials disagree** (for example "Thanksgiving week" in the request, but "Nov 10 to
17" in the video), never pick one silently. Ask, with one option from each source. If the answer is a new campaign,
re-plan it: its materials may need a new version.

**Route.**
- **Ready:** the materials are final and the facts are known. Prepare everything, then come back with one approval
  to launch. This is the critical path.
- **Draft:** the materials are still in progress or missing. Stage and draft everything you can, list what's missing,
  and schedule nothing to launch until the owner says the materials are final.

**Show the plan** in this shape. Make the first line, the calendar line, with
`python scripts/campaign_calendar.py --name ... --types ... --start ... --end ... --tz ...` (no `--out`), so its
format never varies. Where Python can't run, write it by hand in the same format.

```
Campaign: Cousin Walk Sale · Seasonal + Discount · Nov 10 2026, 00:00 to Nov 17 2026, 23:59 (America/New_York) · Website, Email, SMS, Ads
Status: new · Route: ready (materials final)
Website: homepage hero and announcement bar (countdown offered as an extra)
Email, SMS, Ads: not connected yet, so I'll draft them for you to send
Launch: Nov 10, 00:00 (the discount starts itself; you publish the preview) · Stop: Nov 18, 09:00
Assumed: <anything not confirmed yet, e.g. the end time>
```

Keep the same lines when the campaign already exists or is live, but say what's already done and what's left. For
example, "Website: already on preview #188494086362; only a drift check is left" or "Launch: already live since
Nov 10".

Then ask once, in the option window (`AskUserQuestion` in Claude Code and the desktop app; load it with ToolSearch if
it's only listed by name; in a plain chat, one short numbered message):
- "Does this plan look right?" Options: "Yes, go (Recommended)" and "Change something".
- Each fact that's still open as its own question in the same call, with options (up to 4 questions per call).

The yes approves the plan and the work on the preview copy and the drafts. It doesn't approve publishing, or changes
to store data (discounts, product tags or metafields). Each connector write still shows its own confirmation.

**After the yes**, write `campaigns/<slug>/campaign.md` with the plan, if you can write files. Use a short slug
(`cousin-walk`): Windows refuses paths over 260 characters. Then make the calendar file with
`scripts/campaign_calendar.py ... --slug <slug> --out campaigns/<slug>/<slug>.ics` and give it to the owner ("open
it to add the campaign, Launch and Stop to your calendar"). If the plan changes later, make the file again.

## Step 3: Get every channel as ready as it can be

Work through the channels in order without stopping to check in: website first, then email, SMS and ads. If
something blocks a channel, note it, do what you can, and move on. Collect every question for the end.

### 3a. Website

**Safe copy and "before" values.** Never edit the live theme. The owner edits it in the editor, so local files go
stale fast. Make or reuse an unpublished copy and read the files you'll touch (`references/store-access.md`). Keep
the original text of every file before changing it:
- **Project folder available:** `python scripts/snapshot.py save <theme-folder> campaigns/<slug> <files...>` writes
  `campaigns/<slug>/before/` and a `manifest.json` (`restore` puts them back). Keep `campaigns/` outside the theme
  folder, so it's never pushed.
- **No folder (connector in a chat):** the before → after table in the hand-over must hold every old value.

**Surfaces.** Pick them from the campaign type (`references/channels.md`); the homepage always changes. For each
surface, decide: change, add or leave. Reuse what the owner built: an existing sale hero is a head start.
1. **Announcement bar:** offer, end date, link. It's on every page, so it does the most work. One line, under about
   60 characters on mobile. Make sure it stands apart from the header colour.
2. **Homepage hero:** a headline (the campaign name), one supporting line (offer and dates) and one button. The text
   needs a scrim or enough contrast against the media. If the hero video is vertical, check its desktop height (theme
   reference).
3. **Product page** (product launch): the launched product's page and the collection it sits in.
4. **Countdown** (an extra unless asked for): only for a real deadline. It hides when it completes, with an "on
   complete" message as a fallback.
5. **Sale colours** (an extra unless asked for): sale price and promo badge from the brand palette, badge text at
   least 4.5:1.
6. **Product badges and per-product timers** (an extra): product tags or metafields are store data. List exactly which
   products would change, and record them so Stop can remove them.

**Copy rules, in order:**
- the facts are identical everywhere;
- the brand's names are exact (BRAND.md → Terminology);
- Claim limits are respected (no "everything" with exclusions, no fake scarcity);
- the copy follows BRAND-VOICE.md's length, humour and turns of phrase, echoing the campaign materials' own words
  (the owner already approved them);
- dates read the way shoppers read them ("Nov 10 to 17", never "11/17");
- no em dashes in customer copy.

**Freshness (up to 3 suggestions, never applied without a yes):** while reading the page, note anything that makes
the store look out of date and offer it. Examples: a past season's hero left enabled, an old offer in the bar, a
stale headline.

**Write, read back, look.**
1. **Edit the files.** Keep the `/* ... */` header comments and existing ids. New sections get a unique id and go in
   `order`. Then validate:
   - the JSON parses;
   - the section types exist;
   - every setting id exists in that section's schema;
   - dates match the theme's format.
2. **Write to the preview copy only** (`references/store-access.md`: section code before templates). Read the files
   back and confirm only the planned values changed. Stop on any error and quote it.
3. **Look at it on desktop and mobile**, for every visual change, every time. With a browser tool, open the preview
   at about 390, 768, 1440 and 1920 pixels wide and check:
   - no text is cut off;
   - the bar fits on one line on mobile;
   - the hero isn't several screens tall;
   - the button is visible.

   Without a browser, say the visual check wasn't run.
4. **Theme code changed?** This is rare: only when no setting can do it. Prefer settings and section Custom CSS over
   code. If you do change code:
   - mark it with a `Nyla:` comment;
   - save the file in `theme-mods/`;
   - add a row to `THEME-SPECIFICS.md` (create it if missing), so a theme update or another agent never loses it.

### 3b. Email, SMS and ads (stubs)

Follow `references/channels.md`: a short draft for each channel in the plan, the same facts and voice as the
website, marked "not sent". Nothing is sent or scheduled on these channels in this version.

## Step 4: Come back with it ready

Send one message:
- the plan line again, with any changes;
- **Website:** the before → after table (surface · before · after) and the preview link, plus the editor link;
- **Stubs:** one line per drafted channel (what it is, where it is);
- extras you're offering, freshness suggestions, and anything you couldn't confirm (the discount, media);
- the question, which depends on the route:
  - **Ready:** "Launch it?" in the option window. Offer "Launch at <start> (Recommended)" when the start is still
    ahead, or "Launch now" when it has passed, plus "Not yet".
  - **Draft:** no launch question. Say everything is staged, list what's missing, and add: "When the materials are
    final, say 'launch <name>'."

## Step 5: Launch and Stop

Read `references/launch-stop.md`.
- **"Launch at <start>":** set up every scheduling layer available (store timers, one-time scheduled tasks, the
  calendar file) and record each one in campaign.md.
- **"Launch now":** run the drift check, then the owner publishes. With the CLI, Claude publishes only when the owner
  says so in the chat. Confirm the discount is active, then schedule Stop.
- **Stop:** at its scheduled time or whenever the owner asks. Mark campaign.md `Stopped <date>`.

Publishing replaces the live theme with the copy, so edits made to live after the copy was made are lost. If the
owner edited live since, or more than a day has passed, make a fresh copy and re-apply instead of publishing an old
one.

## Hand-over: campaigns/<slug>/campaign.md

Write it, or give the same content in the chat if there's no folder. It holds:
- the plan line;
- the facts;
- the before → after table;
- the preview theme id and links;
- each channel's state;
- Launch and Stop: the time and how each happens;
- the Stop steps.

Then tell the owner briefly:
- what changed (the table, not a diff) and the preview link;
- their to-do: approve and publish, or tell you to; confirm the discount; upload media if needed; send the stub
  drafts;
- what happens at the end: a countdown hides itself, and everything else stays until Stop.

## Quick path (one change, demo mode)

When the request is a single change to one surface ("change the announcement bar to say free shipping on all
orders") rather than a new or changed campaign, skip Steps 1 and 2:
1. Read only the files for that surface.
2. Show the before → after for it and get the yes.
3. Write it, read it back, and give the preview link.

That's about a minute of work. Everything else is an offer for later. If BRAND.md is missing, still say the copy
hasn't been checked against a brand file.

## Dry runs

"Dry run", "test" or offline: run every step, but write only local files (a theme copy and `campaigns/`). Never touch
the store and never create scheduled tasks.

The plan still comes first, and you still wait for the yes. There's one exception: when the request itself already
says to go ahead ("can you do it?", "go ahead", "just do it"), count that as the yes. Show the plan with your
assumptions marked and carry on to Step 4. Either way, stop at the launch question.

## Report format

```
Campaign: <name> · <type(s)> · <start> to <end> (<tz>) · <channels>
Status: <new | exists | live> · Route: <ready | draft>
Preview: <link>   Editor: <link>
Changed: <surface: before → after, one line each>
Drafted, not sent: <email / SMS / ads: file>
Offered, not done: <extras>
Owner to do: <approve / publish / confirm discount / upload media / send drafts>
Launch: <date time> · <how>   Stop: <date time> · <how>
Calendar: campaigns/<slug>/<slug>.ics · Hand-over: campaigns/<slug>/campaign.md
```
