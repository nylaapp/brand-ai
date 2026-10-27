# QA log entry format

Use the store repo's own QA log and format if its engineering rules (`AGENTS.md` or
equivalent) name one -- open the log and copy its most complete entry. If none exists,
use this. One entry per page touched (bundle only truly related small fixes to the same
page in one entry).

```
## <Page name> -- <what changed/was built, short> -- <YYYY-MM-DD>

- kind: <new page | update: content | update: settings | update: section code | update: structure>
- requested: <what the Site Editor asked for, in their words>
- goal (Step 1a): <primary action, audience, change appetite, must-not-change limits>
- baseline (if Step 1b ran): <metric = value (source, date, device)>; target to re-check: <metric, when>
- target: <page handle/URL> -> <template file> -> <section(s)/setting(s)>
- source: <reference URL, or "new design (no reference)", or "n/a (update only)">
- implementation: <file(s) touched>; sections used/added: <list>; new settings added:
  <none | list>; base-theme files edited: <none | list>
- theme validation: <theme check result, before -> after>
- render check: <templates/widths/color-schemes checked, what was confirmed, how>
- gates run: <list>
- gates not run: <which, and why>

### Before / after (or reference / build, for a new page)
| What | Before (or reference) | After (or build) | Within tolerance? |
|---|---|---|---|

### Out of scope / flagged, not done
- <thing noticed but not changed/added>: <why -- out of scope | needs a decision | needs an asset>

### Deviations (new page with a reference only)
- <property>: <difference>. Reason: <base-theme breakpoint | accessibility minimum | merchant content>

final result: <pushed to draft | pushed live (approved by: <who, when>) | blocked (name
the tool and why)>
```

Rules:

- `pushed to draft` / `pushed live` need the before/after (or reference/build) table
  filled with *measured* values -- actual text read from the rendered DOM, actual computed
  style, actual setting value -- not "looks right" or "matches."
- `pushed live` requires naming who approved it and when, in chat, not inferred from
  silence.
- A visible difference noticed but not addressed counts as a defect unless it's listed
  under "out of scope / flagged."
- `blocked` only when no browser/render path is truly available. Say which tool failed.
