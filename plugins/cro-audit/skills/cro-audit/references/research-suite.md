# The research suite

A full CRO audit combines several kinds of evidence, because each one alone misleads: analytics
shows **where** people drop off but not **why**; recordings and tests show **why** but are small;
heuristics are fast but are opinions. The suite below mirrors how CRO agencies structure a research
phase (the "ResearchXL" style: technical, heuristic, analytics, behavioural, qualitative and testing
streams), without depending on any particular tool. Where a stream needs data the skill can't
collect itself, the person supplies it (an export, a screenshot set, notes), and the skill tells
them exactly what to bring.

| # | Stream | What it answers | Collected by | Evidence tag | Playbook |
|---|---|---|---|---|---|
| 1 | Technical | Is anything broken, slow or inconsistent across browsers and devices? | The skill (browser, Lighthouse) | Measured | `mobile-checklist.md`, `scripts/pagespeed.py` |
| 2 | Heuristic | Where does the page break known usability and persuasion principles? | The skill (rendered page) | Heuristic | `heuristics-checklist.md` |
| 3 | Competitive | How do others solve the same journey, and what do shoppers compare us with? | The skill (public pages; `COMPETITORS.md` if present) | Heuristic | `competitor-benchmark.md` |
| 4 | Web analytics | Where are visitors lost, for which segments? | The skill, read-only, through the Shopify CLI if authorised; otherwise the person (exports, numbers) | Reported | `analytics-analysis.md`, `scripts/shopifyql.py`, `scripts/funnel.py` |
| 5 | Behavioural | What do visitors actually do on the page? | The person (heatmaps, scroll maps, recordings, as exports or notes) | Behavioural | `behavioral-review.md` |
| 6 | Voice of customer | What do customers say, in their own words? | The person (reviews, support tickets, chats, surveys); `REVIEW-MINING.md` | Customer voice, Survey | `survey-playbook.md` |
| 7 | User testing | Can a real person complete the key task, and where do they stumble? | The person (sessions run from the script) | Test | `user-testing-playbook.md` |
| 8 | Synthesis | What matters most, and what do we do about each issue? | The skill | all | `prioritization.md`, `experiment-design.md` |

## Rules for combining streams

- **Triangulate.** A finding backed by two or more different kinds of evidence is stronger than one
  backed by a single kind. Say how many, and which.
- **Analytics find the where, qualitative finds the why.** Never explain a leak from analytics alone.
- **Check the data before trusting it** (`analytics-analysis.md` section 1). Bad tracking turns every
  later number into noise.
- **Segment before averaging.** An overall rate hides the segment that is failing (device, source,
  new vs returning, location).
- **Small samples are leads.** Recordings, surveys and tests are small by nature. Use them to explain
  and to form hypotheses, not to measure rates.
- **No invented numbers.** No benchmarks, uplifts or "industry averages" without a named source and
  date. When a figure is missing, say what to measure to get it.
- **Be honest about what the skill didn't do.** List every stream skipped and why in the report.

## What stays human

The skill can plan, analyse and write up, and read the store's analytics when read-only access already
exists. It can't recruit test participants, run interviews, send surveys, or run and read a live
experiment on its own, and it never changes anything on the store. It prepares the instruments (scripts,
questions, a test plan), analyses what comes back, and checks the maths (`scripts/`). Say so plainly
when a stream is "prepared, awaiting data".
