# Chat readout

`CRO-AUDIT.md` is the full record. The chat message is what the person actually reads, so it gets its
own layout: short, in plain words, in the order a store owner thinks (what's wrong, what to do, how
sure we are), not in the order the audit ran. The same text goes at the top of `CRO-AUDIT.md` as
**Read this first**, so a client opening the file sees it too. The "How to reply" rules at the top of
`SKILL.md` still apply to every word here (short, plain, simple English, formal, not intimidating); this
file adds the layout.

## Layout, in this order

Use these labels as short bold lines or small headings. Skip a part that has nothing in it.

1. **Headline.** Two sentences at most: the single thing that matters most, and the overall state.
   Lead with the person's goal (bookings, sales, leads), not the method.
2. **What I looked at.** One line: the page and theme, the devices, the data used, and what wasn't
   available. Example shape: "Live homepage on desktop and phone · speed test · Shopify Analytics,
   14 days · 25 reviews. Not available: booking data, recordings."
3. **What changed since last time** (re-audits only). Up to four bullets: what is fixed, what is new,
   and any correction to an earlier run, stated plainly ("Last time I said X; that was wrong because Y").
4. **Where visitors stop.** The stage table from the funnel report, one row per stage, top to bottom:

   | Step | What happens now | Compared with | Verdict |
   |---|---|---|---|

   - **Step**: in visitor words ("Land → open a treatment page", "Click Book → finish booking").
   - **What happens now**: the rate and the count ("about 2 in 100 visits (106 of 5,800)"), or "Not
     measured yet".
   - **Compared with**: the target and its source, or "the store's own average".
   - **Verdict**: "Biggest leak", "Below target", "Fine", "Too few to judge" or "Not measured: <what to
     add>". Say "Fine" plainly when it is.

   Then one line naming the stage to work on first, and why.
5. **Fix these first.** A table of at most five rows, most important first:

   | # | The problem | Why it matters | What to do | How we know | Effort |
   |---|---|---|---|---|---|

   - **#**: the rank, then the finding ID in brackets so the person can refer to it later: "1 (CRO-02)".
   - **The problem**: what a visitor experiences, in one sentence, with one concrete number if there
     is one ("A sign-up pop-up covers the page about 6 seconds in").
   - **Why it matters**: one sentence about the visitor or the goal, not a principle name.
   - **What to do**: one action, and who does it ("Delay it until visitors scroll, in Klaviyo").
   - **How we know**: a plain phrase from the glossary below ("Measured", "Your analytics",
     "Customers said", "Expert review"), plus "likely" wording for expert-review-only rows.
   - **Effort**: Quick, Medium or Bigger.
   - Where the file has a picture for a row, end "The problem" with "(picture N in the file)". If the
     chat can show images, show the one or two strongest pictures under the table.
6. **Quick wins.** Up to six one-line bullets of small, safe fixes not already in the table, each with
   who does it.
7. **Worth testing, not just changing.** Up to three bullets. For each: what to compare, and whether it
   can finish at their traffic ("about 4 to 18 weeks at your traffic; count bookings first").
8. **What the numbers say** (only if analytics ran). Three or four bullets of plain facts, then one
   line on how far to trust them.
9. **What I couldn't check.** One or two lines.
10. **Close.** The link to `CRO-AUDIT.md` (it has the stage-by-stage report with pictures, every
   finding, the scores and the plans), then one
   question offering the next step, such as applying the quick wins on a draft theme.

## Writing rules

- **Plain words.** No CRO shorthand in the chat: no ICE, buckets, evidence tags, "LCP", "heuristic",
  "E6". If a technical term is unavoidable, explain it once in passing ("how long until the main
  image shows").
- **Round numbers** and say "about": "about 6 seconds", "10 MB", "63% of visitors are on phones". Use
  counts, not percentages, for small groups ("4 orders", not "0.06%").
- **One idea per line.** Table cells are one sentence; bullets are one line. No nested bullets beyond
  one level, and no paragraphs longer than three lines.
- **Five rows, not fifteen.** The full ranked list stays in the file. If more than five matter, say
  "N more in the file".
- **Keep the honesty, compress the caveats.** Every limit from the file still appears, in "What I
  couldn't check" or a one-line trust note, not spread through every sentence. Expert-review findings
  say "likely"; measured ones don't.
- **Say "phone" and "desktop"**, and name the device when a problem is device-specific.
- **Out-of-scope findings** that matter (another page losing most visitors) go in the table if they
  outrank homepage items, marked "(other page)".
- **Length:** about 250 to 400 words plus the two tables. Never paste the file.

## Glossary: file terms to chat words

| In the file | In the chat |
|---|---|
| `[Measured]` | Measured |
| `[Reported]` | Your analytics (or "the numbers you sent") |
| `[Heuristic]` | Expert review (likely) |
| `[Behavioural]` | Visitor recordings |
| `[Customer voice]` | Customers said (reviews, support) |
| `[Survey]` | Survey answers |
| `[Test]` | User tests |
| Two or more of the above | Name both: "Measured + your analytics" |
| Just do it | Fix now |
| Instrument | Measure it first |
| Investigate | Find out why first |
| Test | Test it |
| Hypothesize | Idea, needs evidence |
| High / Medium / Low confidence | Sure / Fairly sure / Not sure yet |
| LCP, FCP, TBT | time until the main image shows, until anything shows, how long the page is frozen |
| Bounce rate | left without clicking anything else |
| Stage, funnel stage | step |
| 95% range | not shown; say "about", or "too few to judge" when the script says so |
| Not measured | Not measured yet, plus what would measure it |

## Example (fictional store, invented numbers)

> **Headline.** Your homepage holds phone visitors fairly well, but a sign-up pop-up and the cookie
> banner cover it within seconds, and bookings can't be counted yet, so we can't tell what's working.
>
> **What I looked at.** Live homepage on desktop and phone · speed test · Shopify Analytics, 14 days ·
> 40 reviews. Not available: booking data, visitor recordings.
>
> **Where visitors stop**
>
> | Step | What happens now | Compared with | Verdict |
> |---|---|---|---|
> | Land → open a treatment page | About 9 in 100 visits (540 of 6,000) | The store's own average | Biggest leak: phones 6 in 100, desktops 14 |
> | Treatment page → click Book | About 22 in 100 (120 of 540) | The store's own average | Fine |
> | Click Book → finish booking | Not measured yet | | Not measured: count bookings on the booking site |
>
> Work on the first step first: phone visitors open a treatment page less than half as often as desktop
> visitors.
>
> **Fix these first**
>
> | # | The problem | Why it matters | What to do | How we know | Effort |
> |---|---|---|---|---|---|
> | 1 (CRO-02) | A pop-up covers the page about 6 seconds in, and its close button is tiny on phones (picture 1 in the file) | New visitors can't see what you offer | Show it after a scroll, and make the close button bigger, in your pop-up app | Measured | Quick |
> | 2 (CRO-04) | Bookings happen on another site that nothing counts | You can't tell if the homepage brings bookings | Track clicks to the booking site and completed bookings | Measured | Medium |
> | 3 (CRO-01) | The page is slow on phones because of one 10 MB video | Most of your visitors are on phones | Show a still image on phones; shrink the video | Measured + your analytics | Quick |
>
> **Quick wins**
> - Fix the "Book" link that points back to its own page (your developer).
> - Update the Google title and description to name all four cities (store settings).
>
> **Worth testing, not just changing**
> - Booking-first hero against membership-first: about 4 to 18 weeks at your traffic. Count bookings first.
>
> **What the numbers say**
> - About 6 in 10 visitors are on phones.
> - The homepage is the most common first page.
> - Trust note: only 14 days of clean data.
>
> **What I couldn't check.** Booking numbers, visitor recordings, survey answers.
>
> Everything, including 9 more findings, is in [CRO-AUDIT.md](CRO-AUDIT.md). Want me to apply the quick
> wins on a draft theme?
