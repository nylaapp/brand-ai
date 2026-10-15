# Audit report layout

Two readers: the client (what is wrong, what it costs them, what we propose) and the team doing the work (evidence and detail). Write the client part in plain language, explain any technical word in a few words, and keep it to one screen. No em dashes.

```markdown
# <Site>: analytics audit (<tagging | full>), <YYYY-MM-DD>

## In short
- What we checked, at which access level (public site / code / tag manager / GA4 / ad platforms), and what we could not check.
- The 3 to 5 things that matter most, each in one line with its business effect
  ("Purchases are counted twice in GA4, so reported revenue is about double").
- Overall: <working | working with gaps | not reliable for decisions>.

## What we propose
| # | Change | Why (effect on the business) | Who does it | Effort | Risk |
|---|---|---|---|---|---|
The full list with evidence is below. Nothing has been changed yet.

## What is installed
<stack inventory table: destination, IDs, installed via, consent gate, evidence>

## Consent and privacy
<regions, banner, what fires in each state; regions not tested>

## Core events (full audit only)
| Event | State | GA4 | Ads | Meta | Other | Result |

## Findings
| ID | Severity | Finding (catalog code) | Evidence | Impact | Suggested fix | Owner |

## Questions for you
<numbered, each with what it blocks>

## Method and limits
Tools and versions, dates, pages tested, states and regions, what was inferred rather than observed.
```

Rules:
- Every finding has evidence the reader could check (a request, a line in an export, a screenshot the person shared).
- Say "not checked" or "not tested" plainly; never fill a gap with an assumption.
- Keep IDs and labels as they appear in the tools, in code font.
- Numbers from GA4 or ad platforms are quoted with their date range and source; never estimate them.
