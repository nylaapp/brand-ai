# Funnel by stage: the spine of the report

Agency CRO reports convince because they walk the funnel one stage at a time. Each stage shows where
visitors stop, for whom, what on the page causes it, and what to do. Build the report the same way.
Findings still get IDs, buckets and scores, but each one sits under the stage it affects.

## 1. Pick the stages for the business

Name stages by what the visitor does. Use the first set that fits:

| Business | Stages, top to bottom |
|---|---|
| Shop (sold in the store's checkout) | Visits → Viewed a product → Added to cart → Reached checkout → Purchased |
| Bookings or appointments | Visits → Viewed a service or treatment page → Clicked Book → Started booking → Booked |
| Leads (quote, consultation, demo) | Visits → Viewed the offer page → Started the form → Sent the form |
| Mixed (a clinic that also sells products) | Run the booking funnel as the main one and the shop funnel beside it |

A stage you can't measure stays in the table as **Not measured**, with how to measure it. Never drop it.
A booking business whose bookings happen on another system usually measures only the first stage or
two. Saying so plainly is a finding, and often the most important one.

## 2. Get the counts

- **Shopify, through the CLI (read-only):** `scripts/shopifyql.py --store <shop> --preset stages
  --since <start> --until <end> --stages-out stages.csv`.
  - It counts people only, using Shopify's own bot filter.
  - It splits each stage by device, channel and entry-page type.
  - It covers the shop funnel. For a service sold as a product, "Viewed a product" also counts the
    service pages.
- **Other stages** (Clicked Book, a booking or form step, a booking system's own report) come from GA4,
  the booking system or the person. Add them as columns in the same CSV. Leave a cell blank when a
  segment isn't available.
- **New vs returning visitors:** Shopify's sessions data has no such split. Ask for it from GA4 if the
  person has it. Otherwise say it isn't available. Don't approximate it from customer order counts.
- Use the clean window from the validity checks (`analytics-analysis.md` section 1), at least 14 days.

## 3. Set the reference for each stage

A rate means little alone. Use the first of these that exists, and print its source next to it:

1. **Targets the person or their agency gives**, as ranges (for example "12 to 18%").
2. **A published benchmark you look up now**, with its publisher, date and definition. It must match
   the stage's definition (sessions vs users, add-to-cart per visit vs per product view). Starting
   points:
   - Littledata's Shopify benchmarks (add-to-cart and checkout completion).
   - Dynamic Yield's ecommerce benchmarks (add-to-cart, cart abandonment, by device and industry).
   - Baymard Institute's cart-abandonment average.
   - Vendor blogs that repeat these numbers aren't sources.
   - Benchmarks for bookings and leads are rare and loose. Prefer options 1 and 3 for them.
3. **The store against itself:** each segment compared with the store's own rate for that stage, and,
   when there are two windows, the stage against its earlier self.

Give `stages.py` the targets with `--targets "Stage=low-high,..." --targets-source "<who, date>"`.
Without targets it compares each segment with the store's own rate.

## 4. Read it

`scripts/stages.py --csv stages.csv [--targets ...]` prints:

- a summary row per stage: the rate, its 95% range, the target, the visits lost and the verdict;
- a grid per stage of every segment's rate and base, marked lower, higher or about the same (or
  below, in or above the target);
- which stage loses the most visits and which is furthest below its target.

Rules:

- A segment under 100 visits at the step before is shown but not judged ("too few to judge").
- A segment is called lower or higher only when its 95% range doesn't include the comparison. The
  script does this; don't override it.
- When a count is higher than the step before (for example cart additions from a quick-add button
  without a product view), the stages aren't nested. Say so, and read that rate with care.
- Most visits lost and furthest below target are different questions. Report both. The stage to
  work on is decided with the other evidence, not by one number.

## 5. Write each stage as one block

Use this layout for every stage, in funnel order, in `CRO-AUDIT.md` (and as one slide or panel per
stage if a deck or page is asked for):

1. **Title and verdict.** For example "Landing → Viewed a treatment: the biggest leak" or "Checkout
   → Purchased: not a bottleneck". Say plainly when a stage is fine. That honesty makes the weak
   stages believable.
2. **The grid.** Rate by device, channel and entry page, with the reference. In HTML or a deck, colour
   each cell: red below, green in or above, grey too few or not measured. In Markdown, use the words
   from `stages.py`.
3. **What the numbers say.** Three to five plain bullets, each with a number. For example: "Phones view
   a treatment page half as often as desktops (4% vs 8%)". Include the reason to be careful when
   there is one.
4. **Where it happens on the page.** One or two evidence pictures of the page area this stage depends
   on, with numbered boxes (`visual-evidence.md`). For example, the hero and header for "Visits →
   Viewed", the product page's buy box for "Viewed → Cart", and the cart drawer for "Cart → Checkout".
5. **What to change.** Numbered to match the boxes in the picture. Each item names the finding ID,
   says one specific change (with the exact new wording where copy changes), and gives the reason.
   Where a competitor or inspiration brand already does it, name them (`competitor-benchmark.md`).
6. **Key question to investigate.** What the numbers can't explain yet, and the stream that would
   answer it (recordings, a survey question, a user test).
7. **Next steps.** Fix now, measure first or test, each with an owner.

Stages that aren't measured get the same block. The grid says what is missing, the pictures still show
the page, and the first next step is the tracking that would measure the stage.

## 6. Where it goes

- `CRO-AUDIT.md` section 2, **Funnel by stage**, comes before the findings table. The findings table
  stays as the full ranked list, with a Stage column.
- The chat readout gets a short **Where visitors stop** table: one row per stage with the rate, the
  reference and the verdict (`chat-readout.md`).
