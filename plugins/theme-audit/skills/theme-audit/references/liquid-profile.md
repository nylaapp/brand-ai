# Server speed lane: the Theme Inspector

Shopify's **Theme Inspector** shows where the server spends time running the theme's own code
(its "Liquid" templates) before any page is sent to the visitor. Lighthouse can't see this: it
only sees the result in the browser. A slow theme shows up in Lighthouse as a long wait for the
first byte (the `server-response-time` audit and the first row of the main-image breakdown), and
the Theme Inspector says which files caused it.

The Chrome extension and the command line do the same job. This skill uses the command line,
`shopify theme profile`, so it can run without a person clicking through a browser.

## 1. What it needs

- The Shopify CLI signed in to the store with theme access (setup check rows E and F). Check with
  `shopify theme list --store <store>.myshopify.com --no-input --json`. If it asks for a sign-in,
  stop: this lane is "not run: the Shopify CLI isn't signed in to this store", and the person
  signs in themselves (setup check section F). Never sign in for them.
- A theme id. **Always pass `--theme <id>` and name the role in the report.** Profiling only reads,
  so the live theme is allowed in audit-only mode. In fix mode, profile the draft.
- Nothing else. It doesn't change the theme, the store or the page.

## 2. Run it: three times, same page

The first profile after a long gap is often slower (cold caches), so run it three times in a row
and use the **median** run.

```bash
for i in 1 2 3; do
  shopify theme profile --store <store>.myshopify.com --theme <theme id> --url <path, e.g. / or /products/handle> \
    --json --no-input > <scratch>/liquid-<handle>-$i.json 2> <scratch>/liquid-<handle>-$i.err
done
for i in 1 2 3; do node <skill>/scripts/liquid_profile_summary.mjs <scratch>/liquid-<handle>-$i.json > <scratch>/liquid-<handle>-$i.summary.json; done
```

- `--url` is the path on the store, not the full address. A password-protected store also needs
  `--store-password`; ask the person to type it in the terminal themselves, never in the chat.
- Without `--json` the command opens a Speedscope page in the browser. That flame chart is the
  visual version: offer to open it ("here is the same data as a chart") but the readout comes from the
  summary.
- Each profile file is large (often 2 MB). Keep them in the scratch folder, not the project.
- Report the median of `total_liquid_ms` and use the median run's tables.

## 3. Reading the summary

`liquid_profile_summary.mjs` gives, in milliseconds:

| Field | What it says |
|---|---|
| `total_liquid_ms` | all the time the server spent running theme code for this page |
| `slowest_files_own_time` | files ranked by time in their own lines (not counting what they render) |
| `slowest_files_with_children` | sections, blocks and snippets ranked by their whole time, including what they render. A file rendered inside itself is counted once. |
| `repeated_pieces` | files rendered five or more times: how many, total, average, slowest |
| `costliest_lines` | single lines (`file:line`) with the most own time and how often they ran |
| `costliest_filters` | the Liquid filters (`image_tag`, `image_url`, `strip_html`...) that took the most time |

**These times include the profiler's own overhead.** They show which files are heavy compared with
each other, and whether a change helped, not the real server time. For the real time, read the
"waiting for the server" figure from Lighthouse: the `server-response-time` audit, or the "Time to
first byte" row in `lcp_breakdown`. Report both and say which is which.

Rule of thumb used by this skill (an estimate, not a Shopify standard): Liquid under about 200 ms
in the profile is not worth chasing. Above about 500 ms, or a single file above about a fifth of the
total, is worth a developer's look. Judge by the share first.

## 4. Who owns each finding, and what to do

| Finding | Owner | What to do |
|---|---|---|
| A theme file is a large share of the total (a header menu, a product card, a slideshow) | This theme | Report the file, its time and its share. Fixes are Liquid code changes and are **not** in the safe list: offer them as a developer task, one at a time, each verified by profiling again |
| One block or snippet rendered dozens of times (`repeated_pieces`) | This theme, usually by design | Normal for page builders (a group block rendered 30 times). Only report it if the total is a large share |
| A loop over products, collections or articles with no `limit`, or `paginate` set high | This theme (the setting) or store content (how many items exist) | Report the file and line. A smaller limit changes what shows, so ask |
| The same expensive work done again inside a loop (a repeated `image_url`, `strip_html`, or a lookup like `all_products[...]` per row) | This theme | Report the file and line as a developer task |
| `inline_asset_content` or `render` of large SVG or script files on every card | This theme | Report with the count; a developer can move it out of the loop |
| Time in app blocks, or in a snippet the app injected (the file names the app) | An app | Report the cost and the owner. Never remove or turn off the app |
| Time that sits in `(page structure)` or layout with no file line | Shopify | Skip, with the numbers |

No Liquid edit in this lane is applied without the person's yes, and each one is re-profiled three
times afterwards. A change inside the spread of the three runs is "no measurable change".

## 5. In the report

- A one-line scorecard row: "Server time (theme code): about 510 ms in the profile (heavy / OK / light), real wait for the server about N ms".
- The top three files by share, in plain words: "The header menu takes about a tenth of it".
- Anything an app owns, with its cost.
- Not run: say why in the "what I couldn't check" line.
