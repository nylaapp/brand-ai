---
doc_type: analytics
doc_schema: 1.0
site: https://www.example.com
brand: Example Co
platform: shopify            # shopify | woocommerce | wordpress | custom | headless | other
last_audit: YYYY-MM-DD       # tagging or full, see section 8
last_verified: YYYY-MM-DD    # last privacy-matrix run
owner_analytics: name, company, how to reach, turnaround
owner_site: name, company
sources:
  - GTM-XXXXXXX export vN (YYYY-MM-DD)
  - page source and HAR captures (YYYY-MM-DD)
snapshots: analytics-snapshots/   # drift_snapshot.py --dir; next to this file, outside any deploy path
---

# Example Co: analytics

> Shared file for the analytics skills (audit, setup, cleanup, guardrails). Rules: `references/analytics-file.md` in the analytics-audit skill. IDs are permanent; retire rows instead of deleting them.

## 1. Measurement goals and core events

What the business counts, most important first. Tier 1 breaking is stop-ship.

| Tier | Meaning |
|---|---|
| T1 | Money or the main conversion (purchase, booked appointment, qualified lead) |
| T2 | Strong intent or secondary leads (begin checkout, booking click-out, call, form) |
| T3 | Engagement used for audiences or optimisation (view item, add to cart, search) |
| T4 | Base measurement (page views, sessions, click-id capture) |

| ID | Tier | Business event | Fires where | GA4 | Google Ads | Meta | Other | Key params |
|---|---|---|---|---|---|---|---|---|
| E-1 | T1 | | | | | | | transaction_id, value, currency |

## 2. Stack inventory

| ID | Destination or tool | IDs | Installed via | Loads on | Consent gate | Evidence | Status |
|---|---|---|---|---|---|---|---|
| S-1 | GA4 | G-XXXXXXX | e.g. Google & YouTube app pixel | all pages + checkout | consent mode | page source YYYY-MM-DD | live |

Destinations reached by more than one path: (each destination with its paths, or "none found")

Install points checked: theme code [ ] · app embeds [ ] · web pixels (app and custom) [ ] · tag manager [ ] · server-side [ ] · checkout / thank-you [ ] · third-party domains (booking, payments) [ ]

## 3. Consent and privacy

- Regions served and their rule (consent required / opt-out / none):
- Banner and CMP:
- How choices reach Shopify (Customer Privacy API) and each vendor:
- Google consent mode: defaults per region, update path, `url_passthrough`, `ads_data_redaction`:
- GPC: honoured where:
- Last privacy-matrix result (date, states, regions tested, regions not tested):

## 4. Site dependency register

| ID | Tag needs (exact) | Site must provide | Reality | Status |
|---|---|---|---|---|
| D-1 | | | | ok |

## 5. Findings

| ID | Severity | Finding | Evidence | Impact | Owner | Status |
|---|---|---|---|---|---|---|
| F-1 | S1 | | | | | open |

Severity: S1 a T1 event wrong or missing, or a legal exposure · S2 a T2 event or attribution wrong · S3 data quality or hygiene · S4 cosmetic or cost only.

## 6. Rules

- **G-1** One path per destination: each destination receives each event from exactly one install point.
- **G-2** ...

## 7. Load policy

| ID | Tag | Owner | Question it answers | Loads when | Cost (TBT ms / KB, lab) | Decision | Review by |
|---|---|---|---|---|---|---|---|
| L-1 | | | | | | keep / defer / on demand / move / remove | YYYY-MM-DD |

## 8. Verification baseline

Static checks (expected results):

```
# command                                   # expected
```

Live test matrix: last run YYYY-MM-DD, states: fresh, accept, reject, gpc, blocked; regions: ...; regions not tested: ...

| Event | State | GA4 | Ads | Meta | Other | Result |
|---|---|---|---|---|---|---|

## 9. Open questions

| ID | Question | For | Blocks |
|---|---|---|---|
| Q-1 | | | |

## 10. Changelog

| Date | Change | By |
|---|---|---|
