# Drift watch: noticing changes nobody announced

Tags change outside the site's code: someone publishes a new GTM version, installs an app with a pixel, switches the theme, or an agency adds a tool. The register is only true until then. A weekly snapshot catches these within days, without logins.

## 1. The snapshot

`python scripts/drift_snapshot.py <urls> --dir <snapshots folder>` records, from public pages only:

- the live version of every GTM container found (from the public `gtm.js`) and the tag IDs inside it,
- script hosts and tag IDs in the page source,
- on Shopify: the live theme and the pixel list (type, app, consent purposes, destination IDs).

Each run saves a dated JSON next to the previous ones and prints what changed. Pick 2 to 4 URLs: home, a product or service page, and any page with special tags (thank-you or booking hand-off pages that load without a login). Add `--gtm GTM-XXXX` for a container that a front end injects at runtime and so is not in the static source.

**One named folder.** The client file's front matter `snapshots` names it (default `analytics-snapshots/` next to ANALYTICS.md, or in the central brand directory), never the theme's deploy path. Always pass that folder, so each run compares with the last one; a baseline nobody can find is no baseline. If the file mentions an earlier baseline without a folder, add the field and start a new baseline.

**Reading the output.** Script hosts are counted from the static source only: a headless front end or a loader that injects every tag at runtime shows "0 script hosts (static source only)", which does not mean "no tags" (the browser inventory sees them). A `?preview_theme_id=` URL is served by the published theme without a browser session; the script warns, and a preview is checked with the browser inventory instead.

## 2. What a change means

| Drift | Means | Do |
|---|---|---|
| GTM version changed | The container was republished | Ask the owner for the new export; `../analytics-audit/scripts/gtm_export_summary.py --diff old new`; update the register for any changed trigger or tag. Until the export arrives, `../analytics-audit/scripts/gtm_public_rules.py GTM-XXXX` shows the live conditions by tag number |
| GTM container added or gone | A new install point, or one removed | Find where it loads; check for duplicates (one path per destination) |
| Pixel added, removed or changed purposes | An app installed or removed, or consent settings changed | Identify the app; check for a second path to a destination; check the consent purposes |
| New script host | A new tool or app embed | Identify it; does it have an owner and a load-policy row? |
| Tag ID changed or added | A destination re-pointed or a second property | Confirm with the owner; check reports for a split |
| Live theme changed | A theme was published | Run the change check for theme switches |

Report drift to the person in plain words with the "Do" column. Nothing is changed automatically.

## 3. Optional data checks

With GA4 access (Google's Analytics MCP server), add a small weekly data check to the watch:

- core events per day for the last 14 days vs the previous 28-day daily average (a drop or a doubling of more than about 30 percent is worth a look),
- page views per session by day (step changes),
- duplicate transaction ids in the last 7 days,
- new hostnames.

Native GA4 custom insights (anomaly or threshold alerts on key events) are a free complement; they only see data after it arrives, so they catch breakages a day or more later than the snapshot catches the change that caused them.

## 4. Scheduling

Weekly is enough for most clients; daily during a launch or migration. Use the environment's scheduler (a scheduled task or routine in Claude, or cron on the person's machine) to run the snapshot and, when there is drift, notify the person. A scheduled run never changes anything and never signs in; if a check needs access it does not have, it reports that and stops.
