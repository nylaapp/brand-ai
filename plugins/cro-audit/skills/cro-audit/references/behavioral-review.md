# Behavioural review (stream 5): heatmaps, scroll maps and session recordings

The skill doesn't record visitors. The person supplies what a tool they already use (or a free one
such as Microsoft Clarity or Hotjar) has captured: exported heatmaps or scroll maps as images, a set of
recordings they watch, or their written notes. Tag findings `[Behavioural]` and say how many
recordings or what date range they rest on. If the person has no tool yet, say what to install and
what to watch for, then mark the stream "prepared, awaiting data".

## Collecting a fair sample

- Cover **at least two full weeks** of traffic and **both devices**; mobile and desktop behave differently.
- Watch **converters and non-converters** of the page being audited. Compare them.
- Aim for **20 to 30 recordings per key segment and page** as a minimum. Stop adding when new ones
  stop showing new problems. Skip sessions under a few seconds and obvious bots.
- Note the segment for each (device, source, new or returning).

## What to look for

| Signal | What it usually means |
|---|---|
| Scroll map: most visitors never reach the main action | The action is too low, or the content above it doesn't earn the scroll |
| Scroll map: a sharp drop at one point | A false bottom (a full-width band that looks like the end) |
| Click map: many clicks on something not clickable | A "dead click": it looks like a link or button |
| Repeated fast clicks in one spot | "Rage clicks": something is broken or slow |
| Clicks on the logo, back, or the menu right after landing | The visitor is lost or the page doesn't match what brought them |
| A form field where people stop, retype or leave | Friction in that field (format, wording, a required item) |
| Visitors open and close the same popup or banner, or scroll never moves while one is open | An overlay is blocking the page |
| Switching back and forth between two pages or tabs | The visitor is comparing and can't find the answer on one page |
| Pages that take long to show anything (blank screens) | A speed problem: connect to the technical stream |

## Logging

For each recording or map, write one line: page, device, segment, what happened, the moment (or
scroll depth), and which issue category it supports. Count each issue across the sample ("seen in 9
of 24 mobile recordings"). Report counts, not impressions.

## Limits

Recordings explain; they don't measure. Never turn "9 of 24" into a population rate. Use them to
confirm or contradict the analytics and the heuristic findings, and to write better hypotheses.
Don't watch recordings that capture typed personal data; ask the person to confirm masking is on.
