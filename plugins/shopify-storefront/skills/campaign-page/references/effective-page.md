# What makes a campaign page sell

A campaign page has one job. It takes a visitor who already wants to buy to the right product fast, with no doubt
about the offer. Every rule below serves that job. Use it to plan the regions (SKILL.md → The template), to
write the copy brief for `voice-builder`, and to check the page before the hand-over.

Each rule says who owns it:
- **Page:** this skill sets it in the template.
- **Store data:** discounts, compare-at prices, collections, product tags. Ask before every write.
- **Owner:** something only the owner can do or confirm.

Never fake anything to meet a rule. Leave the region out, and say what would unlock it.

## 1. The offer, above the fold (page)

At 375 px wide, the first screen shows all three of these, with nothing to scroll for:
- **Headline with the offer in concrete terms.** "25% off sitewide" or "A free OG Hautebox with every order". Never
  a vague line such as "Our biggest sale". A campaign name that doesn't say the offer goes in the supporting line.
- **When it ends and how it applies.** The end date ("Ends Dec 1"). The code, if there is one, in plain text the
  shopper can copy.
- **One primary button.** "Shop the sale" or the brand's version of it. It links to the products region on the page
  (`#products`, where the theme supports anchors) or to the campaign collection. One button only. A second link,
  if any, is plain text.

**No code to copy, where possible.** Prefer an automatic discount (store data). For a code campaign, every
channel's link uses Shopify's shareable discount link, which applies the code in the cart:
`https://<store-domain>/discount/<CODE>?redirect=/pages/<handle>`. Check the code exists before the link goes
anywhere.

**Match the ad.** The first screen repeats the offer and wording of the ad, email or post that sent the visitor.
If `ads.md` or `email.md` exists, the hero headline and the ad headline state the same offer. If they differ,
change one of them; never ship both.

## 2. Urgency only when it's true (page)

- A countdown only for a real end time. It ends at the plan's end, in the store time zone, and never resets. A
  timer that restarts for each visitor is fake urgency, and some regions treat it as a deceptive practice (the EU's
  consumer law and the UK's CMA guidance among them).
- Stock notes ("Only 40 left") only from real inventory the owner confirms. Otherwise leave them out.
- **Phases on one URL.** A campaign can run in phases, all on the same page:

  | Phase | When | First screen says | Countdown to |
  |---|---|---|---|
  | Coming soon | Before the start | "Opens Nov 27", plus email signup | The start |
  | Early access | Subscribers only, if the plan has it | The offer, "for subscribers" | The public start |
  | Live | Start to the last day | The offer and the end date | The end |
  | Last chance | The final 24 to 48 hours | "Last day" or "Ends tonight" plus the offer | The end |
  | Ended | After the end | That it ended, and where to shop now | none |

  Each phase is a swap of the hero and countdown (hidden alternates, SKILL.md → Making each part swappable). Phase
  changes are scheduled like Launch and Stop (campaign-launcher → `references/launch-stop.md`). An early-access
  phase needs a gated discount (a code sent only to subscribers, or a customer segment). That's store data, so say
  what it needs.

## 3. Curated products, not the whole catalog (page and store data)

- **Lead with what sells.** First come the best sellers, then the deepest discounts, then gifting groups
  ("Under $50", "Gift sets", "For travel"). Use collections that already exist. If a group the page needs doesn't
  exist, offer to create it (store data). Never point the products region at "all products" when a curated
  collection exists.
- **Show the saving on the card.** A sale card shows the compare-at price crossed out beside the sale price. That
  needs compare-at prices on the products (store data) and the theme's sale badge or price setting switched on.
  Check both. An automatic discount alone doesn't change card prices: the saving shows only in the cart. If so, say
  it on the card's region heading ("25% off at checkout").
- **Add to cart without leaving the page.** Turn on the section's quick add or quick view setting when the theme
  has one (read the schema). Never add an app for it.

## 4. Order value (store data, offer only)

Order value matters more than extra traffic in peak season. Offer these as extras, and never add one without a yes:
- **Tiered offers.** "Spend $100, get 15% off" or "Buy 2, save more" are automatic discounts with minimums. A cart
  progress bar needs a theme setting or an app; check which the theme already has.
- **Gift with purchase or a best-value bundle.** Place it near the top of the products region, with its own card or
  a one-line callout.

## 5. Trust and no doubt left (page)

- **Near the button:** the shipping cutoff ("Order by Dec 15 for delivery by Christmas"), the returns line and the
  delivery estimate. Use a slim row of three facts (multicolumn or an icon row), only with dates the owner
  confirmed. Never guess a cutoff.
- **Proof:** the theme's or reviews app's existing ratings or a few real reviews, with names as published. Never
  write a review, never round a rating up, never invent a count. Payment badges come from the store's own payment
  icons setting.
- **FAQ** (collapsible content) answers, in this order:
  1. Does it stack with other discounts?
  2. Which items are excluded or final sale? Gift cards are never discounted by Shopify, so say "sitewide", never
     "everything".
  3. When does it end, and in which time zone?
  4. The shipping cutoff, and the returns rule for sale items.
  5. How the code or gift applies.

  Any answer the owner hasn't confirmed stays `[confirm: …]` on the unpublished page. It goes in the owner to-do,
  never into a guessed answer.

## 6. Capture people not ready to buy (page)

One low-pressure email signup near the end, using the theme's newsletter or email-signup section. For example:
"Get first access to the next sale". It's in the brand's voice and promises only what the owner will send. The
platform handles consent. Never add a pop-up unless the owner asks for one.

## 7. Mobile first, and fast (page)

Most peak-season traffic is on phones. Check at 375 px:
- **Tap targets.** Buttons and FAQ rows are at least 44 px tall.
- **Sticky button.** Turn on the theme's sticky add to cart or sticky header setting if it has one. Never add code
  or an app for it during a campaign.
- **Light hero media.** An image is at least 1,600 px wide but under about 500 KB; Shopify serves smaller sizes on
  its own. A video is short, silent and compressed, with a fallback image. A vertical video breaks the desktop
  hero on some themes (campaign-launcher → `references/honey.md`).
- **Lean page.** Use six to nine visible sections. Add no new apps and no third-party scripts for the campaign: heavy
  scripts slow the page at the worst moment.

## 8. Tracking (owner, with a check)

- **One URL per channel**, so the owner can see what works. Use the same page with UTM tags, listed in
  `campaign.md`:
  `/pages/<handle>?utm_source=<email|instagram|meta|google|sms>&utm_medium=<email|social|paid|sms>&utm_campaign=<slug>`.
  For a code campaign, open one tagged discount link on the preview. Check that the tags survive the redirect. If
  they don't, use tagged page links, and the hero shows the code.
- **Events.** Page view, view item, add to cart and begin checkout should fire from this page. This skill doesn't
  check pixels. Offer `analytics:analytics-audit` (read-only) on the preview, or put "confirm GA4 and Meta events
  fire" in the owner to-do.

## 9. Before launch (owner, listed in the hand-over)

- Place a test order with the code or automatic discount on a product and a sale item. Check the price, that the
  discount doesn't stack with another one by accident, and that excluded items stay full price.
- Check that stock is right on every featured product, and that sold-out products drop out of the products region
  or are marked sold out.
- Load test: for a store expecting a big spike, ask Shopify support or the owner's developer. Shopify's own checkout
  scales; a slow page usually means apps and media, so see 7.
- Build and check the page at least a week before the start. Swaps are scheduled: phases, then Ended. An expired
  offer left on the page is a broken promise, so the Ended swap is never optional.

## Recurring campaigns: same URL every year

For a yearly event (Black Friday, a holiday gift guide), use a page handle with no year (`/pages/black-friday`).
Before you create the page, look for last year's page:
- **It exists:** point it at this year's template (`page.campaign-<slug>`). Keep last year's template for reference.
- **It doesn't exist:** create the page now, with the evergreen handle.

Between campaigns the page stays published in its Ended or Coming soon state. It's never deleted, so it keeps
its search ranking. Publishing or unpublishing the page is still the owner's call.

## Region order this produces

| # | Region | Rule |
|---|---|---|
| 1 | Hero: offer, end date, code or "applied at checkout", one button | 1, 2 |
| 2 | Trust row: shipping cutoff, returns, delivery | 5 |
| 3 | Countdown (real deadline only) | 2 |
| 4 | Products: best sellers and deepest discounts, saving on the card, quick add | 3 |
| 5 | Gifting groups, bundle or gift with purchase (if any) | 3, 4 |
| 6 | Reviews (real ones only, if the store has them) | 5 |
| 7 | FAQ: stacking, exclusions, end time, shipping, how it applies | 5 |
| 8 | Email signup | 6 |
| 9 | Closing call to action: the offer and the end date again, same link | 1 |

Drop what the campaign doesn't need: no deadline means no countdown, and no reviews in the store means no reviews
region. Never pad the page.
