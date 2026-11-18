# Channels: website now, email, SMS and ads as stubs

The channels come from the brand file (BRAND.md → Channels): **only what the brand actually uses**. A brand that
doesn't text its customers gets no SMS draft; a brand that runs ads on Instagram and TikTok gets one ad set per
platform. If the brand file is silent, ask once, with Website, Email, SMS and Ads as options ("website only" is a
fine answer). Work them in this order, each as far as it can go
before the next: website, email, SMS, ads. In this version only the website is connected. The other three are
**stubs**: they get a short draft and a to-do for the owner, never a send.

## Website (connected)

SKILL.md Step 3a does the work. Which surfaces change depends on the campaign type; the homepage always changes.
For a campaign with several types, combine the rows.

| Type | Always | Usually | Extras to offer (never added without a yes) |
|---|---|---|---|
| Seasonal | homepage hero, announcement bar | | countdown to a real date, seasonal collection order |
| Product launch | homepage hero, the product's page | announcement bar, the collection it sits in | "New" badge (a product tag), launch countdown |
| Discount or promotion | homepage hero, announcement bar | campaign page when ads or email run | countdown (real deadline only), sale colours, sale badges, compare-at prices on featured products, tiered offer (spend more, save more) |

When ads or email will send traffic, the buttons land on a campaign page built by the `campaign-page` skill, not on
a plain collection. That page repeats the ad's offer in its first screen (`../campaign-page/references/effective-page.md`).

## Stub: Email

- **Status:** not connected. When it is (Shopify Email, Klaviyo or the store's own platform), this step will build
  the emails, schedule them for Launch and cancel what's left at Stop.
- **Now:** the Email section of the plan artifact (or `campaigns/<slug>/email.md` if the owner wants files). One block per send: the launch email, plus a
  last-chance email on the final day for a discount longer than two days, and an early-access email to subscribers
  when the plan has that phase (with the gated code). Each block: subject (under 50
  characters), preview text (under 90), three short lines of body, button text and link, send date and time.
- **First line of the file:** `Draft: not sent. Email isn't connected yet.`
- **Owner to do:** build and schedule it in their email platform, or wait for the connection.

## Stub: SMS

- **Status:** not connected. Later it will connect to Shopify Messaging, Postscript, Attentive or Klaviyo SMS.
- **Now:** only when the brand uses SMS: the SMS section of the plan artifact (or `campaigns/<slug>/sms.md`). One message per send, under 160 characters including the link and
  "Reply STOP to opt out". Send times between 9 am and 8 pm in the shopper's time zone. That's inside the 8 am to
  9 pm window US rules allow for marketing texts.
- **Rules:** texts go only to people who opted in, and that's the platform's job: never collect or import numbers.
- **First line of the file:** `Draft: not sent. SMS isn't connected yet.`

## Stub: Ads

- **Status:** not connected. Later it will connect to Meta, Google Ads or TikTok.
- **Now:** the Ads section of the plan artifact (or `campaigns/<slug>/ads.md`), **one set per platform the brand
  runs**, each with:
  - three headlines under 30 characters (Google's limit; they fit Meta too);
  - two primary texts under 125 characters;
  - which piece of the owner's creative fits which shape: square 1:1, vertical 9:16, landscape 1.91:1;
  - the landing page, the same link as the website button, tagged for the platform (Links per channel below);
  - **message match:** each headline states the same offer, in the same words, as the landing page's hero. If the
    hero changes, the ads change with it;
  - start and end, the same as the campaign.
- **Rules:**
  - Claim limits matter even more in ads, because platforms reject over-claims.
  - Platforms differ. TikTok is stricter than Meta for regulated products (cannabis accessories, alcohol,
    supplements and the like): write a TikTok set that avoids anything its policy is likely to reject, keep it
    separate from the Instagram or Meta set, and say in the Brief that the two sets differ and why.
  - For a discount, the landing page must show the offer.
- **First line of the file:** `Draft: not sent. Ads aren't connected yet.`

## Links per channel

Every channel gets its own tagged link to the same landing page, so the owner can see in Shopify's or GA4's reports
what sold. List them in campaign.md and put each one in its stub.

| Channel | utm_source | utm_medium |
|---|---|---|
| Email | the platform (`klaviyo`, `shopify_email`) | `email` |
| SMS | the platform (`postscript`, `attentive`) | `sms` |
| Meta ads | `meta` | `paid_social` |
| Google ads | `google` | `cpc` |
| Instagram or TikTok post | `instagram` / `tiktok` | `social` |

Format: `https://<domain>/pages/<handle>?utm_source=<source>&utm_medium=<medium>&utm_campaign=<slug>`. Keep tags
lower case and the slug the same as the campaign folder. For a code campaign, use the shareable discount link
(`/discount/<CODE>?redirect=/pages/<handle>`) and check once on the preview that the tags survive the redirect. If
they don't, use the tagged page link and show the code in the hero. This skill doesn't check that pixels fire;
offer `analytics:analytics-audit` or list it in the owner's before-launch checks.

## Every stub, every time

- Same facts as the website: offer, dates, link, exclusions. Same brand voice and claim limits.
- Written with `copywriting.md`: the brand's own words first, no generic sale-speak, every line through its checks.
- Short. The owner should be able to read every draft in under a minute.
- Use only the owner's own materials for creative; never invent images, testimonials or numbers.
- In the hand-over, each stub is one line: what was drafted, where it is, and the owner's to-do.

## Connecting a channel later

Every stub has the same shape: status, what it will do when connected, what to do now, and the owner's to-do. To
connect a channel:
1. Replace "Now" with the steps through that platform's connector: draft, read back, schedule for Launch, cancel at
   Stop.
2. Keep the order: website, email, SMS, ads.
3. Add the channel's lines to the Launch and Stop tables in `launch-stop.md`.
