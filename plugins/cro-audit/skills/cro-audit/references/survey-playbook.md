# Voice of customer and surveys (stream 6)

Customers' own words are the best source for **why**. The skill can't send surveys, but it can write
them, and it can analyse the answers, reviews, support tickets, chat logs and emails the person brings.
Tag findings `[Customer voice]` (from existing text such as `REVIEW-MINING.md`) or `[Survey]` (answers
to questions asked for this audit).

## Existing text first (no new collection needed)

1. `REVIEW-MINING.md`, if it exists (from the `review-miner` skill): top pain points and praise, with
   counts and quotes.
2. Support tickets, live chat and email, and the questions asked before booking or buying. A sample
   of 50 to 100 recent threads is plenty to find the repeat themes.
3. Reviews on other platforms (Google, Yelp, Trustpilot) and the brand's social comments.

Code each into the same themes: **objections** (what nearly stopped them), **motivations** (why they
came), **language** (the exact words they use), **confusions** (what they didn't understand),
**delighters**. Count mentions per theme and keep short quotes with the source and date.

## Surveys to write (and the person to send)

Keep each to **one to three questions**; short surveys get answered. Use open text first, because
closed options only echo what you already assumed.

**On-site (a small prompt, shown after engagement, not on landing)**
- What brought you to the site today?
- Is there anything you were hoping to find that you haven't?
- What is stopping you from [booking / buying] right now? (offer "nothing, just browsing")

**Exit or abandonment (cart, booking form, pricing page)**
- What stopped you from finishing today?
- What would have made this easier?

**Post-purchase or post-booking (best for learning what convinced people)**
- What nearly stopped you from [buying / booking]?
- What was the main reason you chose us over other options?
- How did you first hear about us?

**Existing customers (email, a few weeks later)**
- What problem were you trying to solve when you found us?
- What would you tell a friend about us in one sentence?

## Sending it

State who sees it, when, and how many answers to wait for. Below about 30 open answers per question,
treat the themes as leads. Don't offer a discount to answer, because it changes who answers. Check
privacy and consent rules for the region before collecting.

## Analysing the answers

Read all of them. Group into themes, count, pick representative quotes, and note the exact
wording for use in copy (as a lead for `page-edit-content`, to be checked by `fact-check` where it
makes a claim). A theme that appears in surveys **and** in reviews **and** in the analytics leak is a
high-confidence finding.
