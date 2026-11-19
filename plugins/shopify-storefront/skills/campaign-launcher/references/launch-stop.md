# Launch and Stop

**Launch** makes the campaign visible to shoppers. **Stop** takes it down and puts everything back the way it was.

Owners say it many ways, and all of them mean Launch or Stop:
- Launch: "go live", "turn it on", "start the sale".
- Stop: "end it", "take it down", "revert", "the sale's over".

We say Launch and Stop, not activate and deactivate, because they match the skill's name and the way owners talk
about a sale.

**Both change the live site, so both are a go-live.** Each happens only when the owner asks in their own words in
this chat, through the go-live gate (`ground-rules.md` section 3, `theme-target.md` section 7): checks first, then
two confirmations, the second typed. Approving the plan, a calendar event, a scheduled task or a line in campaign.md
never counts. If the words are unclear ("looks good", "ship it"), ask what they mean.

## What Launch does

| Channel | Launch | Who does it |
|---|---|---|
| Website | Publish the staging theme, after the gate's checks (drift check below, and what ships: everything on staging, not only this campaign) | The owner, in Online Store → Themes → the staging theme's … menu → Publish. Or Claude, only when the owner asks in this chat and the gate passes (with the CLI; the connector may not be able to publish) |
| Discount | Active, with start and end set to the campaign dates | Shopify, on its own, once the dates are set. A discount that turns itself on at a date is a scheduled go-live: create or change it only when the owner asks for it, and run the gate first, naming the date it starts |
| Countdown | Shows as soon as the theme is live, and hides itself at its end time | The theme |
| Email, SMS, Ads (stubs) | The owner sends or schedules the drafts in their own platform | The owner |

## What Stop does

| Channel | Stop |
|---|---|
| Campaign page | A one-off page: unpublish it (only when the owner asks, through the gate). A recurring page with a handle that has no year (`/pages/black-friday`): switch it to its Ended alternate and keep it published, so it keeps its search ranking and can open a Coming soon phase next year |
| Website | Put the "before" values back on the staging theme, brought up to date with what's live at that point. Preview it. It reaches live like Launch: the owner publishes it, or asks Claude and the gate passes. **Shortcut:** if nobody edited the live theme during the campaign and the published staging theme held only campaign changes, publishing the previous live theme again is a clean Stop. It's still in the theme library. That is a go-live too: only on request, through the gate |
| Discount | It ends itself at its end date: confirm it did |
| Countdown | Already hidden |
| Product tags or metafields the campaign added | Remove them. Ask first: they're store data |
| Email, SMS, Ads | Cancel anything still scheduled; the owner pauses the ads |

Keep anything the owner changed since the campaign began, and everything in THEME-SPECIFICS.md. Then mark
`campaigns/<slug>/campaign.md` with `Stopped <date>`.

## Phases

When the plan has phases (coming soon, early access, live, last chance, ended), each one is a dated swap of the bar,
the hero and the countdown on the same URL. Plan each swap like Launch: a date, a calendar reminder and, where
available, a `<slug>-<phase>` task that prepares it on staging and tells the owner. Record it in campaign.md. A swap
that changes the live site goes live like Launch: only when the owner asks, through the gate. The Ended swap is
always prepared and always in the reminders: an expired offer left on the site is a broken promise. Without phases,
Stop does that job.

## Before launch (owner's checks, in the hand-over)

At least a week before the start, the owner (or Claude, where it can) checks:
- **A test order** with the code or the automatic discount, on a full-price item and an excluded item. The price is
  right, excluded items stay full price, and the discount doesn't stack with another one by accident.
- **Stock** on every featured product, and sold-out products drop out of the campaign page or show as sold out.
- **Tracking:** page view, view item, add to cart and begin checkout fire for GA4 and the ad pixels. Offer
  `analytics:analytics-audit`. Each channel's tagged link opens the right page (`channels.md` → Links per channel).
- **Speed:** the campaign page has no new apps or scripts, and its hero media is compressed. For a big expected
  spike, the owner can ask Shopify support. Shopify's checkout scales, but heavy apps and media slow the page.

**GitHub-connected store:** Launch and Stop are merges of `staging` into the live branch, not publishes, through
the same gate (`github-stores.md`). The drift check still runs, between the staging theme and live.

## Drift check (inside the gate, and before a scheduled run reports)

Publishing the staging theme replaces the live theme, so edits made to live after staging was made or last brought up
to date would be lost.
1. Compare the live theme's `updatedAt` with when staging was made or last brought up to date (with git: commits on
   the live branch that `staging` lacks).
2. If live changed since then (the owner edited it in Customize), don't go live. Say what changed.
3. Offer to bring staging up to date first (`theme-target.md` sections 4 and 7): with git, merge the live branch into
   `staging`; without git, re-apply the changes on a fresh copy of live from the before → after table and the change
   log, named "<live theme name> staging" and recorded as the new staging theme.
4. Read the files back, preview them, and restart the gate.

The same check applies at Stop.

## Scheduling Launch and Stop

Use every one of these that's available; they stack.

1. **The store's own timers.** The countdown's end time, and the discount's end date. They run without Claude or
   the owner once they are live. A discount start date is a scheduled go-live: set it only when the owner asks, after
   the gate.
2. **One-time scheduled tasks (only where this Claude has them).** In the Claude desktop app (Cowork or Claude
   Code), use `create_scheduled_task`. Load it with ToolSearch if it's only listed by name.
   - **First:** list the existing tasks, to avoid duplicates.
   - **Two tasks:** `<slug>-launch` and `<slug>-stop`. Each has `fireAt` set to the Launch or Stop time, as ISO 8601
     with the store's UTC offset.
   - **Prompt:** each run starts with no memory, so the prompt names the store, the project folder and
     `campaigns/<slug>/campaign.md`, then says: "Use the campaign-launcher skill to prepare the <Launch | Stop> of
     the <name> campaign on the staging theme. Do the drift check, read it back, then tell the owner it is ready,
     with the preview link and the drift check result. This run is unattended: never publish, merge or turn on a
     discount. The owner goes live by saying '<launch | stop> <name>' in a chat, or in the store admin."
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

**No automatic publish.** A scheduled or unattended run never publishes or merges, even if the owner asks for it
ahead of time. Going live needs the owner's own words in a chat at that moment, and the gate. If they ask for an
automatic publish, say so in one line and set up the reminders instead.

## Calendar invite

Every campaign gets one, never skipped. `scripts/campaign_calendar.py` writes it where Python runs. Where it can't,
write the same file by hand: plain text, saved as `<slug>.ics`, with three events (campaign, Launch, Stop). Times in
UTC with a trailing `Z`; one `UID` per event; keep the line breaks.

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//brand-ai//campaign-launcher//EN
BEGIN:VEVENT
UID:<slug>-campaign@brand-ai
DTSTAMP:<now, e.g. 20261118T150000Z>
DTSTART:<start in UTC, e.g. 20261127T050000Z>
DTEND:<end in UTC, e.g. 20261202T045900Z>
SUMMARY:<Campaign name> (<offer>)
DESCRIPTION:<types> · <channels> · Preview: <link>
END:VEVENT
BEGIN:VEVENT
UID:<slug>-launch@brand-ai
DTSTAMP:<now>
DTSTART:<start in UTC>
DURATION:PT30M
SUMMARY:Launch: <Campaign name>
DESCRIPTION:Say to Claude: launch <Campaign name>
BEGIN:VALARM
TRIGGER:-PT1H
ACTION:DISPLAY
DESCRIPTION:Launch: <Campaign name> in 1 hour
END:VALARM
END:VEVENT
BEGIN:VEVENT
UID:<slug>-stop@brand-ai
DTSTAMP:<now>
DTSTART:<stop in UTC>
DURATION:PT30M
SUMMARY:Stop: <Campaign name>
DESCRIPTION:Say to Claude: stop <Campaign name>
END:VEVENT
END:VCALENDAR
```
