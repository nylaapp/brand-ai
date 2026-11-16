# Channels: website now, email, SMS and ads as stubs

Every campaign is planned for four channels: **Website, Email, SMS and Ads**. Assume all four unless the owner
takes one out in the plan ("website only" is a fine answer). Work them in this order, each as far as it can go
before the next: website, email, SMS, ads. In this version only the website is connected. The other three are
**stubs**: they get a short draft and a to-do for the owner, never a send.

## Website (connected)

SKILL.md Step 3a does the work. Which surfaces change depends on the campaign type; the homepage always changes.
For a campaign with several types, combine the rows.

| Type | Always | Usually | Extras to offer (never added without a yes) |
|---|---|---|---|
| Seasonal | homepage hero, announcement bar | | countdown to a real date, seasonal collection order |
| Product launch | homepage hero, the product's page | announcement bar, the collection it sits in | "New" badge (a product tag), launch countdown |
| Discount or promotion | homepage hero, announcement bar | | countdown (real deadline only), sale colours, sale badges |

## Stub: Email

- **Status:** not connected. When it is (Shopify Email, Klaviyo or the store's own platform), this step will build
  the emails, schedule them for Launch and cancel what's left at Stop.
- **Now:** write `campaigns/<slug>/email.md` (or put it in the chat). One block per send: the launch email, plus a
  last-chance email on the final day for a discount longer than two days. Each block: subject (under 50
  characters), preview text (under 90), three short lines of body, button text and link, send date and time.
- **First line of the file:** `Draft: not sent. Email isn't connected yet.`
- **Owner to do:** build and schedule it in their email platform, or wait for the connection.

## Stub: SMS

- **Status:** not connected. Later it will connect to Shopify Messaging, Postscript, Attentive or Klaviyo SMS.
- **Now:** write `campaigns/<slug>/sms.md`. One message per send, under 160 characters including the link and
  "Reply STOP to opt out". Send times between 9 am and 8 pm in the shopper's time zone. That's inside the 8 am to
  9 pm window US rules allow for marketing texts.
- **Rules:** texts go only to people who opted in, and that's the platform's job: never collect or import numbers.
- **First line of the file:** `Draft: not sent. SMS isn't connected yet.`

## Stub: Ads

- **Status:** not connected. Later it will connect to Meta, Google Ads or TikTok.
- **Now:** write `campaigns/<slug>/ads.md`:
  - three headlines under 30 characters (Google's limit; they fit Meta too);
  - two primary texts under 125 characters;
  - which piece of the owner's creative fits which shape: square 1:1, vertical 9:16, landscape 1.91:1;
  - the landing page, the same link as the website button;
  - start and end, the same as the campaign.
- **Rules:**
  - Claim limits matter even more in ads, because platforms reject over-claims.
  - For a discount, the landing page must show the offer.
- **First line of the file:** `Draft: not sent. Ads aren't connected yet.`

## Every stub, every time

- Same facts as the website: offer, dates, link, exclusions. Same brand voice and claim limits.
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
