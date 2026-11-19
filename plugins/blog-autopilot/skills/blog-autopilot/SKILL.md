---
name: "blog-autopilot"
description: "Brand-agnostic autopilot that decides WHEN a Shopify store should get a new or refreshed blog post and what it should cover. It scans store events (new products, restocks, rising sellers), Search Console exports, review and helpdesk exports, competitor blog feeds, trends and a lead-time occasion calendar, scores opportunities with a rubric, applies guardrails (dedupe, cannibalization, cooldowns, weekly cap), then by default checks in with the user (weekly) and drafts only after they say yes, handing the brief to blog-generator as a hidden draft; optional auto-draft. Each brand keeps its own profile. Use whenever the user wants blog posts created on a schedule or when something happens, e.g. \"run my blog autopilot\", \"weekly blog check-in\", \"should we post this week?\", \"set up automatic blog posts\", \"what should we blog about next\", a scheduled blog-scan firing, or any request to trigger or prioritize Shopify blog content from store, SEO, competitor or seasonal signals."
---

# Shopify Blog Autopilot

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

## Ground rules (every run)

These come before every step below. The full text is `references/ground-rules.md`; where it and a step below disagree, the
stricter rule wins.

- **Brand files first (required: BRAND.md and BRAND-VOICE.md).** Read them before any work and follow them: words follow
  BRAND-VOICE.md and stay inside BRAND.md's claim limits; visuals use design.md's values. If one is missing or
  belongs to another store, stop and ask once: create it now (brand-capture, voice-builder or styles-builder,
  `references/ground-rules.md` section 1) or tell me where it is. Never work from memory or the live site instead, and
  never carry on without it. With no person present, stop and report what is missing. The brief it hands to blog-generator names
  the files it found.
- **Hidden first.** Everything this skill creates in the store is saved hidden (`isPublished: false`), so the
  person can preview it before customers see it. Any theme change goes to the staging theme, never the live one.
- **Visible only when the person asks.** Never suggest, offer or schedule making a post visible, and never do it
  in an automated run. Only when the person asks in their own words in this chat, run the go-live gate
  (`references/ground-rules.md` section 3): checks (fact-check and review checklist done, preview seen), then two
  confirmations, the second typed.

## Effort (read before starting)

Weekly check-in: about 5 to 10 minutes and $1 to $2 with the deep web sources, under $0.50 without them (store events, ledger and occasions only). Drafting a post adds the blog writer's own effort. Estimate, not yet measured. Stop and report if a scan passes 20 minutes or $4.

Decide **whether, what and when** a Shopify store should publish, then hand off to `blog-generator` to do the writing. This skill never writes the post itself: it's the editor-in-chief, and the writer skill is the staff writer. Keeping them apart means the rubric can change without breaking the writing workflow, and the writer still works on its own when the user asks for a post directly.

```
Setup check → Load brand profile → Gather signals → Build candidates → Score → Guardrails → Decide → Check in → Hand off → Log
        (setup if missing)                                                      (ask first)  (hidden draft)
```

The default operating model is **polling with a weekly check-in**: a scheduled task (weekly by default) runs this skill, which looks at everything that changed since the last run, then asks the user whether to write the best idea. Nothing is drafted until they say yes, unless the brand's profile sets `approval: auto_draft`. There's no external automation to set up. Because detection uses "since last successful run" rather than "last 24 hours", a missed day is caught up on the next run.

## Reference files

Read each one when you reach the step that needs it.

| File | Read at |
|---|---|
| `references/setup-check.md` | Before Step 1: what must be set up first and how to guide the person through it |
| `references/setup.md` | First run for a brand (no profile yet), or when the user asks to change settings or the schedule |
| `assets/brand-profile.template.yaml` | Setup: the file you copy and fill in for each brand |
| `references/triggers.md` | Step 2: how to detect each trigger type, with queries and file formats |
| `references/scoring-rubric.md` | Steps 4–5: factors, weights, thresholds, guardrails, worked examples |
| `references/occasions.md` | Step 2: the default occasion calendar and how lead times work |
| `references/checkin.md` | Step 5b: the ask-first check-in message, replies, pending check-ins |
| `references/handoff.md` | Step 6: the brief contract with `blog-generator`, tagging and ledger format |
| `references/automation-options.md` | Only if the user wants faster-than-daily events (free, optional upgrades) |
| `scripts/occasions.py` | Step 2: computes upcoming occasions and whether their lead-time window is open |
| `scripts/gsc_signals.py` | Step 2: turns Search Console CSV exports into striking-distance, decay and gap candidates |
| `scripts/score_opportunities.py` | Steps 4–5: scores candidates and applies every guardrail deterministically |

## Operating rules

- **Ask first by default.** Unless the profile says `approval: auto_draft`, never start writing from a scheduled run. Send the check-in and wait for a yes. A quiet week is a good outcome, and unnecessary runs cost the user credits.
- **Hidden drafts only.** Every post is created unpublished (`isPublished: false`). This skill never publishes or makes a post visible, even if QA passes, and never schedules it. If the person asks how a post goes live, explain both ways in one line each: they set it to Visible themselves in Shopify admin, or they ask Claude to do it outside the autopilot run, which runs the go-live gate (`references/ground-rules.md` section 3).
- **Every draft ships with a human review checklist.** The writer saves `<handle>-review-checklist.md` and tags the draft `needs-review`. A draft that passed QA has not been reviewed: surface the checklist in every report and summary, and never describe a draft as ready to publish.
- **Never modify a live article.** A "refresh" becomes a new hidden draft titled `[REFRESH] <original title>` with a note pointing to the original, so the user can compare and swap.
- **Brand-agnostic skill, brand-specific profile.** Everything about a particular store (competitors, occasions, markets, excluded topics, thresholds) lives in that brand's `brand-profile.yaml`, never in this skill. When you learn something durable about the brand, write it to the profile, not to memory.
- **Assume nothing about the brand.** No country, language, currency, industry, competitors or voice is built into this skill. All of it comes from the profile or from the store during setup. If a value is missing, derive it from the store or skip the feature that needs it. Never fall back to a default market.
- **Don't invent data.** If a source isn't configured or its file is missing, skip that trigger and say so in the run report. Don't guess search volumes, rankings or review counts. The rubric works with the evidence you have.
- **Quiet by default.** A scheduled run with nothing worth writing is a successful run. Log it and stop. Don't write a weak post just to fill the week.

## Setup check (before Step 1)

Run `references/setup-check.md` for the `blog-autopilot` column: a folder on this computer, web search, brand files, blog-generator installed, Shopify connected, Python 3 and, for the weekly check-in, the computer awake with Claude open, are required; competitor research, Search Console exports and review or helpdesk exports are recommended, because they are where the best post ideas come from. Assume the person isn't technical: check silently yourself, then walk them through anything missing one step at a time, in plain words, and check again after each step. Required items block the run; recommended ones are offered once, with what they add, and can be skipped. Skip the check if it already passed in this conversation. With nobody there (a scheduled or fully automated run), never ask: use the fallback for recommended items and list what's missing under "Needs your attention". A missing BRAND.md or BRAND-VOICE.md has no fallback: write the run report with `stopped: missing <file>` and stop. When handing off to `blog-generator`, say in the brief that the check passed.

## Step 1 — Load the brand profile

Look for the brand's workspace folder, `blog-autopilot/<brand-slug>/`, in the connected folder. It holds:

```
blog-autopilot/<brand-slug>/
├── brand-profile.yaml   # settings (from the template)
├── ledger.json          # run history, topics covered, backlog, snapshots
├── inputs/              # optional exports the user drops in
│   ├── gsc/             #   Search Console CSVs
│   ├── reviews/         #   review app exports
│   └── helpdesk/        #   ticket exports
└── runs/                # one report per run: YYYY-MM-DD.md
```

- **Profile found:** load it and `ledger.json` (create an empty ledger if it's missing).
- **Brand files (required):** also find the brand's `BRAND.md` and `BRAND-VOICE.md`: `brand.knowledge_file` in the profile if set, else the lookup in brand-capture `references/brand-context.md` (project root, user local environment, central brand directory `$BRAND_AI_HOME/brands/<slug>/` or `~/.brand-ai/brands/<slug>/`, then connected knowledge sources), before asking the user anything. They are the source of truth for identity, voice, competitors, inspiration brands and claim limits. The profile's copies, memory and `CLAUDE.md` never stand in for a missing file. If either file is missing or is for another store: with a person present, stop and ask once, "Create it now (Recommended)" (brand-capture; voice-builder for BRAND-VOICE.md) or "I will tell you where it is"; on a scheduled run, write the run report with `stopped: missing <file>` and the places checked, and stop. Don't re-research the brand; read the file. Competitors and inspiration brands are asked or scanned once, saved there, and refreshed only when the user asks.
- **Several brands found and the request doesn't say which:** a scheduled task always names its brand. Interactively, ask once.
- **No profile, or no folder connected:** run setup (`references/setup.md`). Setup discovers most of the profile from the store itself and asks only for what it can't find. If there's no user present (a scheduled run), don't guess a setup. Write a run report saying setup is needed and stop.

**Dry run:** if the request says "dry run" (or "test", "preview", "what would you do"), run every step but don't create drafts, don't call the writer, and don't create or change scheduled tasks. Write the decisions and briefs to `runs/`, and leave `ledger.json` untouched: put the changes a live run would make in `runs/<date>-ledger-proposed.json` instead, so dry runs never affect caps, cooldowns or the lookback window. If a `store-snapshot.json` file is provided, use it instead of querying the live store.

## Step 2 — Gather signals

Read `references/triggers.md`. Work through the trigger families below, **only for sources the profile enables and that actually have data**. Each family produces zero or more *candidates*.

| Family | Source | Typical candidate |
|---|---|---|
| Store events | Shopify connector (products, collections, inventory, analytics, existing articles) | New product → launch or deep-dive post; restock → "it's back" or usage guide; rising product → buying guide |
| Search data | `inputs/gsc/*.csv` via `scripts/gsc_signals.py` | Striking-distance query → new post; decaying post → refresh; query with no matching page → new post |
| Voice of customer | `inputs/reviews/`, `inputs/helpdesk/` exports | Recurring question or complaint theme → FAQ, fit or care guide |
| Competitors | Competitor blog feeds and sitemaps listed in the profile | Competitor covers a topic in your core categories that you don't → new post |
| Market trends | Web search: category news, forums, trend coverage | A rising query or breakout topic in the category → timely post |
| Occasions | `scripts/occasions.py` using the profile's markets and custom dates | Occasion whose lead-time window is open → seasonal post, or a refresh of last year's |
| Periodic | Ledger and backlog | No post in `periodic.max_gap_days` → top backlog item |

**Keep the scan cheap.** Free and local sources run every time: store events, existing articles, Search Console, review and helpdesk exports, the occasions script, the ledger. The credit-heavy web sources (market trends, competitor feeds, the AI citation check) run at most once per `scan.deep_every_days` (default 7), and only for the brand's saved competitors and categories. If an earlier scan this week already found a strong candidate, don't deepen the scan.

Update the ledger's `snapshots` (for example the out-of-stock product IDs) as you go, so the next run can diff against them.

## Step 3 — Build candidates

Normalize every signal into one candidate record. The schema is in `references/scoring-rubric.md`. At minimum it needs: `id`, `trigger`, `title_idea`, `primary_keyword`, `cluster`, `intent`, `post_type`, `action` (`new` or `refresh`), `evidence` (with URLs, numbers or quotes), `products` (handles to link), `deadline` (or null), and the five factor scores.

Merge candidates that describe the same topic. For example, a new "<product name>" product plus a GSC query "best <product type>" become one candidate with both pieces of evidence. More independent evidence is a real signal, and the rubric rewards it.

Score each factor 1–5 from the evidence, following the anchors in `scoring-rubric.md`. Be conservative: when you can't see evidence for a high score, give 2–3, not 5.

## Step 4 — Score and apply guardrails

Save the candidates to `runs/<date>-candidates.json`, then run:

```bash
python scripts/score_opportunities.py \
  --candidates runs/<date>-candidates.json \
  --profile brand-profile.yaml \
  --ledger ledger.json \
  --existing runs/<date>-existing-articles.json \
  --today <YYYY-MM-DD> \
  --out runs/<date>-decisions.json
```

`--existing` is the list of the store's existing articles, **including hidden drafts**, from Step 2. It's how the script catches duplicates and cannibalization. The script is deterministic so decisions are consistent across runs. It:

1. Computes a 0–100 score from the weighted factors, plus bonuses for multi-signal evidence and under-represented intents in the content mix.
2. Applies hard gates: excluded topics, a cluster cooldown, an existing article targeting the same keyword (turned into a refresh where appropriate), and missing brand fit.
3. Applies the weekly cap (counted from the ledger *and* from `autopilot`-tagged articles created in the last 7 days) and the per-run limit.
4. Labels each candidate `write`, `backlog` or `skip`, with reasons.

Read the output. If a decision looks wrong because a factor score was wrong, fix the candidate and rerun. Don't override the script's gates by hand. If a gate itself seems wrong for this brand, that's a profile setting: tell the user and suggest the change.

## Step 5 — Decide

- **`write`:** at most `limits.max_posts_per_run` (default 1), never beyond the weekly cap. Deadline-driven items go first.
- **`backlog`:** stored in the ledger with score and expiry, and re-scored on later runs. Evidence goes stale, so items expire after `limits.backlog_expiry_days`.
- **`skip`:** logged with the reason, so the same signal isn't re-evaluated from scratch every day.
- **Nothing to write:** check the periodic rule. If the gap since the last autopilot post is at least `periodic.max_gap_days` and the top backlog item scores at least `thresholds.periodic_min`, promote it. Otherwise log a quiet run and stop.

## Step 5b — Check in (ask-first mode)

If `approval` is `ask_first` (the default), don't hand off yet. Read `references/checkin.md`, send the check-in message with the top idea (and up to two alternates), and wait for the user's reply: write it for me, do it together, pick another, or skip. If there is an unanswered check-in from an earlier run, don't send a second one; add a reminder to the report. Only after a "write" choice, continue to Step 6 with the right mode. Until then, don't write topics to the ledger (run the scorer without `--write-ledger`); record only the `checkin` entry. If `approval` is `auto_draft`, skip this step.

## Step 6 — Hand off to the writer

Read `references/handoff.md`. For each `write` decision:

1. Build the **autopilot brief**: target keyword and intent, post type, action, the evidence, products to feature, deadline, and the brand's voice, author and constraints from the profile. The format is in `handoff.md`.
2. Invoke the `blog-generator` skill with the brief. In `auto_draft` mode, or when the user chose "write it for me", the brief says **fully automated** with **Shopify draft delivery** (hidden), and the writer asks nothing. If the user chose "do it together", the brief says **guided**, and the writer asks only what the brief doesn't answer. Pass the tags `autopilot` and `autopilot-<trigger>` so later runs can count and trace autopilot posts.
3. If `blog-generator` isn't available, save the brief to `runs/<date>-<handle>-brief.md`, flag it in the report, and stop.
4. If the writer falls back to HTML delivery (for example because the connector is missing), record that in the ledger and report. The post still counts against the weekly cap, since review effort is the real limit.
5. **Collect the review checklist.** The writer adds the tag `needs-review` to the draft and returns the path to `<handle>-review-checklist.md` (placeholders to fill, claims to verify, links to click, images to check). Record the path in the ledger topic (`review_checklist`) and carry it into the report. If the writer didn't return one, say so in the report under "Needs your attention" instead of skipping silently.

## Step 7 — Log and report

Update `ledger.json`: the run entry, topics written (keyword, cluster, handle, article ID, trigger, date, review checklist path), backlog changes, skips and snapshots. Then write `runs/<date>.md` using this template:

```markdown
# Blog autopilot — <Brand> — <YYYY-MM-DD>

**Result:** <n> draft(s) created | check-in sent (awaiting reply) | check-in answered: skipped | quiet run | setup needed | blocked
**Weekly cap:** <used>/<cap> (resets <date>)

## Drafts created — NOT ready to publish until reviewed
| Title | Keyword | Trigger | Score | Admin location | Review checklist |
|---|---|---|---|---|---|

## Backlog (top 5)
| Idea | Score | Why not now | Expires |
|---|---|---|---|

## Skipped
| Idea | Reason |
|---|---|

## Sources checked
<each trigger family: ok / no data / not configured / error, with a one-line note>

## Needs your attention
1. Review each draft with its checklist (accuracy, placeholders and links, voice and first-hand detail, images, SEO fields, compliance). Remove the `needs-review` tag when done. The drafts stay hidden; your live store has not changed.
2. <placeholders to fill in drafts, missing exports, stale GSC data, profile suggestions>
```

When a user is present, finish with a short summary: what was drafted and where it is in Shopify admin, the cap status, that the draft still needs the human review checklist (with the file path), and anything else that needs their attention. On a scheduled run, the report file is the output.

## Scheduling

Setup creates the recurring task. By default it runs **weekly** (Monday 9:00 local time), checks in with the user and waits for a yes; its prompt names the brand and profile path (see `references/setup.md`). Brands that want more frequent scans can set a different cron, and brands that want hands-off drafting can set `approval: auto_draft`. Weekly scans use fewer credits than daily ones. Scheduled tasks run on the user's computer, so it needs to be awake with Claude running at that time. A missed run is caught up next time, because every trigger looks back to the last successful run.

