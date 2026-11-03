# Clustering and reasoning guide

The script (`scripts/parse_reviews.py`) handles the deterministic part: finding
columns, cleaning text, deduping, redacting names. Everything from here is reading
and judgment, done by you, in batches.

## 1. Why clustering, not keyword counting

The same complaint shows up in a dozen different wordings: "too small," "wish it
was bigger," "not enough room for a change of clothes" are all one pain point, not
three. Counting exact phrases undercounts badly and keyword search over-counts
(matching "space" in "parking space" or "storage space" as unrelated hits). So the
method is: extract the *claim* a review is making, then group claims by what they
actually mean, not by shared words.

## 2. Batch size

Context is finite and clustering needs to compare each new claim against
everything found so far, so work in batches rather than one giant pass:

- Under ~150 usable reviews: one batch is usually fine.
- 150 to ~600: 3 to 5 batches of roughly 100-150 reviews each.
- 600+: stratify instead of reading everything. Take all 1 and 2-star reviews (the
  richest pain-point source), a recent slice (last 90 days, to catch anything new),
  and a random sample of the rest. Say in the report that this run sampled rather
  than read every review, and how.

Within each batch:

1. **Extract atomic claims.** For each review, pull out 1 to 3 short claims it
   makes (a review can both praise the design and complain about the price). Each
   claim gets: the type (pain or praise), a short label in your own words, the
   exact quote it came from, the review's rating, and its date.
2. **Match against the running taxonomy.** Before naming a new category, check
   whether this claim is really the same thing as a category already on the list
   (either from an earlier batch in this run, or from the taxonomy already saved
   in `REVIEW-MINING.md` from a previous run — see §4). Match on meaning: "the
   shoe compartment eats all my packing space" and "not enough room for clothes
   when shoes are in" are the same category even though no words overlap.
3. **Only create a new category when it's genuinely distinct**, and when it has
   enough independent mentions to be a real pattern rather than noise — a single
   odd complaint doesn't need its own row. If something shows up only once or
   twice, hold it in a short "one-off mentions" note rather than giving it a
   category; it can graduate to a category once (or if) more reviews confirm it.

## 3. Root cause, impact, and metrics

For each pain point that makes the top of the list, go one level deeper than
restating the complaint — a store owner already knows customers are complaining;
what they need is why it's happening and how they'd know it's fixed.

- **Root cause**: the structural reason, not the symptom. "Customers say it's too
  small" is the symptom; "the shoe compartment's depth was designed for shoe
  height, not shoe + clothing volume together" is closer to a cause. Infer this
  from the pattern of complaints (what specifically do multiple reviews point at?)
  rather than guessing — if the reviews don't give enough to infer a cause
  confidently, say that plainly instead of inventing one.
- **User impact**: tie it to a real business consequence — a lost sale before
  purchase, a return after, a support ticket, a negative public review, lost
  repeat-purchase likelihood. "Customers are unhappy" isn't an impact; "customers
  choose a competitor's larger bag instead" is.
- **Success metric**: something a store could actually track going forward —
  a percentage of reviews mentioning the issue (with the current rate as the
  baseline, computed from this data), a return-reason code rate, a survey
  question's target score. If you can compute today's baseline from the data in
  front of you, include it; don't invent a number you can't support.

## 4. Matching against a prior run (trend tracking)

If `REVIEW-MINING.md` already exists for this store, its **Pain-point taxonomy**
table is the starting point, not a blank slate. Read it first, before extracting
anything new:

- A claim that matches an existing category adds to that category's count; don't
  rename or split an established category just because this run's wording differs
  slightly — stability is what makes the trend column meaningful.
- A genuinely new, repeated pattern gets a new row, with "first seen" set to this
  run's date.
- A category with zero mentions this run isn't deleted — mark it stable/resolved
  and keep it, so a future spike is visible as a change, not a mystery new entry.
- Mention counts in the taxonomy table should reflect the review set the category
  was found in — if this run analyzed a different number of reviews than the last
  one (more data, or a sampled subset), say so next to the trend, since raw counts
  alone can mislead when the denominator changed.

## 5. The "what customers love" side

Run the same extraction and clustering process on 4 and 5-star reviews to find
the top reasons people buy and stay happy — this is the mirror image of pain-point
mining, not an afterthought. It's often the more useful output for the client: a
pain point says what to fix, but a praise category says what to put on the
homepage, in ads, or in a blog post. Keep it to the same rigor — real quotes,
real mention counts, no invented enthusiasm.

## 6. A/B test ideas

For the top 3 to 5 pain points, propose one concrete test idea each:

- **Test idea**: a specific, buildable change to the site or flow — not "improve
  trust," but "add a 60-second unedited packing video to the PDP, A/B'd against
  the current polished video."
- **Hypothesis**: the specific belief being tested, stated so it could be proven
  wrong — "customers who see a realistic packing demo will have fewer size-related
  returns" rather than "customers will like this more."
- **Psychological lever**: name the actual mechanism — trust/honesty, control and
  self-selection, social proof, loss aversion, anchoring, reduced friction. This
  is what makes the test idea more than a guess; it says *why* it should work.
- **Metrics to watch**: the specific numbers that would show the test worked
  (click-through, add-to-cart lift, return-rate change) — things that could
  realistically be instrumented, not vague sentiment.

## 7. Quotes: pick well, never fabricate

A quote earns its place in the report when it's specific and representative, not
just the most dramatic one found. Use the `reviewer` field the parser already
redacted (first name + last initial, or "a customer") — never pull a full name,
email, or other identifying detail back in from the raw file. Every quote must be
copied verbatim from a review in the normalized data; never smooth out the
wording or combine two reviews into one invented quote.

## 8. Regulated or risky claims found inside reviews

Sometimes a customer's own words make a claim the brand shouldn't repeat verbatim
— a medical benefit, a safety claim, an unverifiable statistic. If a review you'd
otherwise want to quote makes one of these claims, don't use it as supporting
"evidence" for the brand's own marketing; flag it in the report as something for
a human (or the fact-check skill, if the output is headed into copy) to
look at before it's reused anywhere customer-facing.
