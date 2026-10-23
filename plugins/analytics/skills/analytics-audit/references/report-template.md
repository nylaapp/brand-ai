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
<stack inventory table: destination, IDs, installed via, host or pages, consent gate, evidence>

Destinations reached by more than one path: <destination: path A, path B; ...> (or "none found").
Install points checked: <theme code, app embeds, ScriptTags, pixels, tag manager, server-side, checkout, third-party domains; each "yes", "no" or "not checked">

## Consent and privacy
<regions, banner, what fires in each state; regions not tested>

## Core events (full audit only)
| Event | State | GA4 | Ads | Meta | Other | Result |

## Findings

### Broken (an event that should fire does not, or fires wrong)
| ID | Severity | Finding (catalog code) | Evidence | Impact | Suggested fix | Owner |

### Risky (works today but breaks on a likely change, or a legal or data-quality exposure)
| ID | Severity | Finding (catalog code) | Evidence | Impact | Suggested fix | Owner |

### Hygiene (clutter, unowned tools, cost)
| ID | Severity | Finding (catalog code) | Evidence | Impact | Suggested fix | Owner |

## Questions for you
<numbered, each with what it blocks>

## Method and limits
Tools and versions, dates, hosts and pages tested, states and regions. Browser state: fresh profile or not, stored consent, and on Shopify the theme role seen on each host (a preview is not the published theme). Container source: export version, or the public gtm.js of the live version when the export was stale or missing. What was inferred rather than observed.
```

Rules:
- Every finding has evidence the reader could check (a request, a line in an export, a tag number in the public build, a screenshot the person shared).
- A table with no rows says "none found"; do not drop it.
- Say "not checked" or "not tested" plainly; never fill a gap with an assumption.
- Keep IDs and labels as they appear in the tools, in code font.
- Numbers from GA4 or ad platforms are quoted with their date range and source; never estimate them.
