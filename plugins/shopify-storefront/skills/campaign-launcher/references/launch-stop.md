# Launch and Stop

**Launch** makes the campaign visible to shoppers. **Stop** takes it down and puts everything back the way it was.

Owners say it many ways, and all of them mean Launch or Stop:
- Launch: "go live", "turn it on", "start the sale".
- Stop: "end it", "take it down", "revert", "the sale's over".

We say Launch and Stop, not activate and deactivate, because they match the skill's name and the way owners talk
about a sale.

## What Launch does

| Channel | Launch | Who does it |
|---|---|---|
| Website | Publish the campaign's preview theme, after the drift check below | The owner, in Online Store → Themes → Publish. The connector can't publish. With the CLI, Claude publishes only when the owner says so in the chat, or when they pre-approved an automatic launch (below) |
| Discount | Active, with start and end set to the campaign dates | Shopify, on its own, once the dates are set. Creating or changing a discount is a store write: ask first |
| Countdown | Shows as soon as the theme is live, and hides itself at its end time | The theme |
| Email, SMS, Ads (stubs) | The owner sends or schedules the drafts in their own platform | The owner |

## What Stop does

| Channel | Stop |
|---|---|
| Campaign page | A one-off page: unpublish it (the owner's call, ask first). A recurring page with a handle that has no year (`/pages/black-friday`): switch it to its Ended alternate and keep it published, so it keeps its search ranking and can open a Coming soon phase next year |
| Website | Put the "before" values back on a fresh copy of the theme that's live at that point. Preview it, then the owner publishes. **Shortcut:** if nobody edited the live theme during the campaign and the campaign copy held only campaign changes, publishing the previous theme again is a clean Stop. It's still in the theme library |
| Discount | It ends itself at its end date: confirm it did |
| Countdown | Already hidden |
| Product tags or metafields the campaign added | Remove them. Ask first: they're store data |
| Email, SMS, Ads | Cancel anything still scheduled; the owner pauses the ads |

Keep anything the owner changed since the campaign began, and everything in THEME-SPECIFICS.md. Then mark
`campaigns/<slug>/campaign.md` with `Stopped <date>`.

## Phases

When the plan has phases (coming soon, early access, live, last chance, ended), each one is a dated swap of the bar,
the hero and the countdown on the same URL. Schedule each swap like Launch, with a `<slug>-<phase>` task and a
calendar event, and record it in campaign.md. The Ended swap always happens: an expired offer left on the site is a
broken promise. Without phases, Stop does that job.

## Before launch (owner's checks, in the hand-over)

At least a week before the start, the owner (or Claude, where it can) checks:
- **A test order** with the code or the automatic discount, on a full-price item and an excluded item. The price is
  right, excluded items stay full price, and the discount doesn't stack with another one by accident.
- **Stock** on every featured product, and sold-out products drop out of the campaign page or show as sold out.
- **Tracking:** page view, view item, add to cart and begin checkout fire for GA4 and the ad pixels. Offer
  `analytics:analytics-audit`. Each channel's tagged link opens the right page (`channels.md` → Links per channel).
- **Speed:** the campaign page has no new apps or scripts, and its hero media is compressed. For a big expected
  spike, the owner can ask Shopify support. Shopify's checkout scales, but heavy apps and media slow the page.

## Drift check (before every publish)

Publishing replaces the live theme with the copy, so edits made to live after the copy was made are lost.
1. Compare the live theme's `updatedAt` with the time the copy was made.
2. If live changed since then (the owner edited it in Customize), don't publish the old copy.
3. Instead, duplicate live again and re-apply the campaign changes from the before → after table.
4. Read the files back and preview them, then publish.

The same check applies at Stop.

## Scheduling Launch and Stop

Use every one of these that's available; they stack.

1. **The store's own timers (always).** The Shopify discount's start and end dates, and the countdown's end time.
   They run without Claude or the owner.
2. **One-time scheduled tasks (only where this Claude has them).** In the Claude desktop app (Cowork or Claude
   Code), use `create_scheduled_task`. Load it with ToolSearch if it's only listed by name.
   - **First:** list the existing tasks, to avoid duplicates.
   - **Two tasks:** `<slug>-launch` and `<slug>-stop`. Each has `fireAt` set to the Launch or Stop time, as ISO 8601
     with the store's UTC offset.
   - **Prompt:** each run starts with no memory, so the prompt names the store, the project folder and
     `campaigns/<slug>/campaign.md`, then says: "Use the campaign-launcher skill to <Launch | Stop> the <name>
     campaign. Do the drift check and prepare the website on an unpublished copy. Read it back, then send the owner
     the preview link and the one step left (publish). Publish only if campaign.md records that the owner
     pre-approved an automatic <launch | stop> with the CLI."
   - **Tell the owner:** the task runs on their computer, so Claude has to be open at that time. If it's closed,
     the task runs the next time Claude opens.
   - **A plain claude.ai chat has no scheduled tasks.** Say so, and rely on 1 and 3.
3. **Calendar reminders (always).** Run
   `python scripts/campaign_calendar.py ... --out campaigns/<slug>/<slug>.ics`. It writes three events with
   reminders:
   - the campaign itself;
   - Launch, with reminders a day and 30 minutes before;
   - Stop, with a reminder 30 minutes before.

   Each event holds the preview link and the sentence to say to Claude. Give the owner the file to open: it adds
   to Google, Apple and Outlook calendars. Where Python can't run, write the same three events as text in the
   hand-over.

**Stop time.** By default Stop runs at the campaign's end. If the end is late at night (after 9 pm), offer the next
morning at 9:00 for the steps a person has to do. The discount and the countdown still end on time. Offer this as
an option, never silently.

**Automatic publish (CLI only, opt-in).** Only when the owner explicitly asks for it ("publish it automatically at
launch"):
- Record it in campaign.md: `Auto-publish: <launch | stop>, approved by <name> on <date>`.
- The scheduled run still does the drift check. If live changed, it doesn't publish: it sends the owner a message
  instead.
- Never automatically through the connector (it can't publish), and never without that line in campaign.md.
