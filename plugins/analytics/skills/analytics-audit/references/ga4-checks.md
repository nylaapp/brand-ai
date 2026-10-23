# GA4 property and data-quality checks

Two halves: settings (how the property is configured) and data (what the numbers say about the implementation). Settings need GA4 access, either the person sharing screenshots or exports, or Google's Analytics MCP server. Data checks run through that server's `run_report` and `run_realtime_report` tools, or the person exports the same reports.

**Access.** Google's official server is `analytics-mcp` (experimental, read-only scope `analytics.readonly`, tools: `get_account_summaries`, `get_property_details`, `list_google_ads_links`, `run_report`, `run_funnel_report`, `get_custom_dimensions_and_metrics`, `run_realtime_report`). Setup: Google Cloud project with the Analytics Admin and Data APIs enabled, then `gcloud auth application-default login` with that scope, then `claude mcp add analytics-mcp --scope user -e GOOGLE_APPLICATION_CREDENTIALS=... -e GOOGLE_PROJECT_ID=... -- pipx run analytics-mcp`. The person signs in; never handle their credentials. Without it, ask for screenshots or CSV exports and say which checks could not run.

## 1. Settings checklist

| Check | Where in GA4 Admin | Good | Why it matters |
|---|---|---|---|
| Data retention | Data collection and modification > Data retention | 14 months | Default 2 months truncates Explorations |
| Time zone, currency | Property details | Match the business and the store | Day boundaries and revenue |
| Streams | Data streams | One web stream per site; the measurement ID matches every install point | A second stream or property splits data |
| Enhanced measurement | Stream > Enhanced measurement | Each toggle intentional; form interactions and page changes reviewed | Auto events can duplicate custom ones |
| Domains | Stream > Configure tag settings > Configure your domains | Every domain in the journey (store, booking, checkout) | Cross-domain sessions |
| Unwanted referrals | Configure tag settings > List unwanted referrals | Payment gateways, booking engine hosts, Shop Pay if relevant | Gateways steal the session source |
| Session timeout | Configure tag settings > Adjust session timeout | Fits the buying cycle | Long decisions show as new sessions |
| Internal traffic | Define internal traffic + Data filters | Filter Active, not Testing | Staff and agency visits inflate data |
| Consent | Stream > Consent settings (where shown) | Consent signals present for EEA traffic | Modelling and Ads eligibility |
| Key events | Admin > Events / Key events | Only business outcomes; counting method set (purchase per event, leads once per session) | Engagement events as key events distort reports and bidding |
| Custom definitions | Custom definitions | Every parameter used in reports registered with the right scope (limits: 50 event, 25 user, 10 item dimensions; 50 metrics) | Unregistered parameters are invisible in reports |
| Google signals, reporting identity, attribution | Data collection; Reporting identity; Attribution settings | Documented choice | Thresholding and credit rules |
| Links | Product links | Google Ads (auto-tagging on), Search Console, Merchant Center; BigQuery if used | Conversions and raw data |

## 2. Data checks (Data API reports)

Use a date range that covers at least 28 days, and the last 7 days for anything recent. Record the query and the result in the audit report.

| # | Check | Dimensions | Metrics / filter | Red flag |
|---|---|---|---|---|
| 1 | Duplicate transactions | `transactionId` | `transactions`, `ecommercePurchases`; keep rows where transactions > 1 | Any transaction ID counted more than once |
| 2 | Purchases vs the platform | `date` | `ecommercePurchases`, `purchaseRevenue` | Compare with the platform's order count per day; record the gap as the client's baseline. A sudden change in the gap matters more than its size |
| 3 | Hostnames | `hostName` | `sessions`, `screenPageViews` | Staging, preview, `myshopify.com`, translation proxies or unknown hosts |
| 4 | Self-referrals and gateways | `sessionSource`, `sessionMedium` | `sessions`, `keyEvents`; filter source contains the client's domains or payment and booking hosts | Own domain or gateway as a converting source |
| 5 | Channel health | `sessionDefaultChannelGroup` | `sessions` share | High Unassigned (UTM or click-id problems); Direct share jumping after a change |
| 6 | Landing pages | `landingPagePlusQueryString` | `sessions`; look for `(not set)` | `(not set)` share above a few percent: sessions starting without a page_view |
| 7 | Event hygiene | `eventName` | `eventCount` | Case or spelling variants (`Purchase` and `purchase`), legacy names, PII in names |
| 8 | Page views per session | `date` | `screenPageViews` / `sessions` | A step change: a second page_view source arrived or one left |
| 9 | PII in URLs | `pagePath` or `pageLocation` | filter contains `@`, `email=`, `phone=`, `name=` | Personal data in collected URLs |
| 10 | Realtime during tests | `eventName`, `minutesAgo` (realtime) | `eventCount` | Test events arriving once, with the right names |

## 3. Reading the gap with the platform

GA4 revenue is normally lower than the store's: consent rejection, blockers, closed tabs before the thank-you page, cross-device purchases. Vendor estimates range from 5 to 40 percent and none is authoritative, so do not judge against a fixed number. Record the client's own gap once the setup is verified, then watch it: a change of more than a few points week over week, or GA4 above the platform, points at a tracking change.
