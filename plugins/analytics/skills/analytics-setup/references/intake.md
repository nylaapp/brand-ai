# Intake: collecting the client's issue list

The client knows where the numbers feel wrong; we know where to look. Intake turns their symptoms into a short list of things to prove. Ask in one message, plain words, at most eight questions in the first round; follow up only on what the answers leave open.

## First-round questions

1. **What looks wrong?** Numbers that do not match (which two sources, by how much, since when), something counted twice, a sudden drop or spike (dates), conversions missing in Google Ads, Meta or another platform, too much "Direct" or "Unassigned" traffic, anything else that feels off.
2. **Which numbers do you make decisions with?** The reports or dashboards people actually use, and who reads them. These decide what is Tier 1.
3. **What changed recently?** New theme or site, new or removed apps, domain or subdomain changes, checkout or thank-you page upgrade, a new consent banner, a new agency, a booking or payment provider change. Rough dates are enough.
4. **Which tools are connected?** GA4, Google Ads, Meta, TikTok, Pinterest, email or SMS, heatmaps, call tracking, A/B testing, affiliate, anything else you pay for.
5. **Who owns each account and the tag manager?** Names, company, how to reach them, and how fast they can change things.
6. **Where are your customers?** Countries and US states that matter. Any legal or privacy guidance you already follow, and who your counsel is if consent questions come up.
7. **What can we access?** Site code or theme, a tag manager export, GA4 (read access or exports), screenshots from ad platforms, the store admin.
8. **Any deadline?** A campaign launch, a site relaunch, a budget review.

For a regulated category (health, finance, children), also ask whether any pages or flows must not carry advertising pixels. Ask this only when BRAND.md or the site shows that category.

## Triage: symptom to first checks

| Symptom | Likely causes (catalog) | Check first |
|---|---|---|
| GA4 purchases or revenue above the store's | FC-01, FC-02 | Same ID twice; duplicate transaction ids; thank-you reload |
| GA4 far below the store's | FC-06, FC-09, FC-10, consent rejection, blockers | Purchase reaches GA4 in a test order; consent sync; privacy matrix |
| Page views jumped (double) | FC-01, FC-20 | Two `page_view` hits per page |
| Ads conversions "inactive" or dropping | FC-06, FC-07, FC-10 | Conversion tag fires in a test; site dependency changed; consent defaults |
| Meta reports more purchases than orders | FC-03, FC-04, FC-01 | Shared `event_id`; pixel in two places |
| Lots of Direct or Unassigned | FC-13, FC-14, UTM hygiene, consent | Cross-domain; gateways as referrals; tagging of campaigns |
| Own domain or payment provider as a source | FC-13, FC-14 | Linker domains; unwanted referrals |
| Leads in the CRM but not in analytics | FC-19, FC-08 | What the lead trigger listens to; whether that signal exists |
| Numbers changed right after a site or theme change | FC-07, FC-18, FC-17 | Diff of tracking before and after the change |
| "Is our banner working?" | FC-09 to FC-12 | Privacy matrix |
| Site feels slow | FC-24, FC-25, FC-26 | `tag_cost.py`, third-party table (cleanup skill) |

## Writing it down

Record each reported issue in ANALYTICS.md section 9 as a question or section 5 as a suspected finding (`status: open`, evidence "client report YYYY-MM-DD"), with the client's own words in quotes. After the audit, every client-reported issue gets an answer: proved, disproved (with evidence), or not testable (and why).
