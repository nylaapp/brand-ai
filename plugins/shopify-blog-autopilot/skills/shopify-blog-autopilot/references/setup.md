# Setup: a new brand, settings changes, schedule

Setup should take the user about two minutes. Discover everything you can from the store, ask only what you can't find, and show them the finished profile.

## 1. Workspace folder

The profile and ledger must live somewhere that persists between runs.

1. **A connected folder (preferred).** If none is connected, ask the user to pick one (e.g. `Documents/`). Create `blog-autopilot/<brand-slug>/` with `inputs/gsc`, `inputs/reviews`, `inputs/helpdesk` and `runs/`.
2. **Fallback, when the user can't connect a folder:** store the profile and ledger in the Shopify store itself, as shop metafields `blog_autopilot.profile` and `blog_autopilot.ledger` (type `json`), via the connector. Explain that input exports (GSC, reviews) then can't be dropped in, so those triggers stay off. This is a write to store settings, so confirm with the user first.

## 2. Discover the profile

First look for the brand's central brand file (`brand.md` or similar). If it exists, take identity, voice, competitors, inspiration brands and claim limits from it and set `brand.knowledge_file`; don't scan or ask again. Then copy `assets/brand-profile.template.yaml` to `brand-profile.yaml` and fill in what you can find:

| Field | How to find it |
|---|---|
| brand.name, store_url | `get-shop-info` or `shop { name primaryDomain { url } }` |
| one_liner, voice | Homepage and about page (web fetch). Write the one-liner as a plain fact |
| categories | Top collections by product count, merged into 3–8 topic clusters |
| shopify.blog_handle | `blogs(first:20)`. With several blogs, pick the one with the most articles and note that |
| default_collection_handle | The main or all-products collection |
| markets.primary, language, currency | Shop country and currency (`shop { currencyCode billingAddress { countryCodeV2 } }`) and the storefront language; others come from Markets if available. Never assume US or English: if it can't be found, ask |
| author | The most common author on existing articles; else "The <Brand> Team" |
| competitors, inspiration brands | From the brand file if present. Otherwise **ask once**; don't invent them. If the user is unsure, offer 3–5 *suggestions* from a web search of the brand's categories, labeled as suggestions, and let them confirm. Offer to save the answers to the brand file so no skill asks again. Refresh only when the user asks |

## 3. Ask only the gaps (one AskUserQuestion call, at most 4 questions)

1. **Competitors:** confirm the suggestions, or name your own (free text).
2. **Data exports:** which the user can provide: Search Console, a reviews app, a helpdesk (multi-select). Enable those sources and tell them where to drop files.
3. **Off-limits topics and claims** (free text, optional), plus any local dates or festivals in the brand's markets worth a post (suggest a few from a web search if the default calendar has few for the market).
4. **Check-in and cap:** by default I check in once a week (Monday 9:00) with a top idea and you choose to write it, do it together, pick another, or skip; max 2 posts a week. Offer: a different day, or `auto_draft` (drafts hidden posts without asking).

In a scheduled or no-user run, don't set up. Write a "setup needed" run report and stop.

## 4. Show, then save

Show the filled profile summary (brand, categories, blog, markets, sources on/off, competitors, occasions active in the next 90 days via `occasions.py`, thresholds and limits). Save it. Create `ledger.json` as `{"brand": "<slug>", "runs": [], "topics": [], "backlog": [], "skips": [], "snapshots": {}, "checkin": null}`.

## 5. Create the schedule

Use `create_scheduled_task` (list existing tasks first, to avoid duplicates):
- name: `blog-autopilot-<brand-slug>`
- cron: the profile's `schedule.cron` (default `0 9 * * 1`, weekly)
- prompt: `Run the shopify-blog-autopilot skill for brand "<Brand>" using the profile at <folder>/blog-autopilot/<brand-slug>/brand-profile.yaml. Scheduled run: scan, then follow the profile's `approval` setting. With `ask_first`, send the check-in message and wait for the reply; don't write anything until the user says yes. With `auto_draft`, create at most the allowed hidden drafts. Always write the run report.`

Offer a test check-in right away ("Want me to send a test check-in now so you can see how it works?") and note how the reply is captured (`references/checkin.md` §6).

Tell the user plainly: the scan runs on their computer, so it needs to be awake with Claude open at that time. A missed day is caught up on the next run.

**First run.** Offer to run a **dry run** now, so they can see what it would do before anything is created.

## 6. Monthly nudges (in the run report's "Needs your attention")

- The Search Console export is older than `max_age_days`: re-export it (Compare: last 28 days vs. previous).
- The reviews or helpdesk export is older than 35 days.
- A competitor feed has failed three runs in a row: check the URL.
- Drafts are piling up unreviewed (three or more autopilot hidden drafts older than 14 days): suggest lowering the cap.

## Changing settings

For "change the cap", "add a competitor", "skip Valentine's" and similar requests, edit `brand-profile.yaml`, show the diff, and if the cron changed, update the scheduled task.
