# Handoff to shopify-blog-writer, and the ledger

## 1. The autopilot brief

This is the contract between the two skills. It pre-answers every setup question the writer would otherwise ask, so the writer runs end to end without stopping. Save it as `runs/<date>-<handle>-autopilot-brief.md`, then pass it to the writer.

```markdown
# Autopilot brief: <working title>

**Run:** <YYYY-MM-DD> · **Candidate:** <id> · **Score:** <n>/100 · **Trigger(s):** <list>
**Delivery:** Shopify draft, HIDDEN (isPublished: false). Never publish.
**Mode:** fully automated | guided. (Fully automated: don't ask questions; use this brief and the defaults, and list assumptions. Guided: the user is present; ask only what this brief doesn't answer.)
**Intent:** education | brand | search | promotion (from the user's reply, else the trigger default)
**Media:** stock | own uploads | both (profile default: stock)
**Format:** match | match-layout | best-practice (profile default: match-layout)
**Action:** new post | REFRESH of /blogs/<blog>/<handle> (create a NEW hidden draft titled "[REFRESH] <original title>"; don't edit the live article)

## Brand (from the central brand file; profile as fallback)
- Brand file: <path>. The writer reads it for voice, competitors, inspiration brands, claim limits and blog house style; don't paste them here.
- Brand: <name> — <store_url>
- One-liner: <brand.one_liner>
- Voice: <voice>; avoid: <words_to_avoid>
- Author: <name> — <bio>
- Market: <primary market>, <language>, <currency>
- Blog handle: <shopify.blog_handle>
- Claims restrictions: <list or "none">

## Target
- Primary keyword: <kw> — intent: <intent> — post type: <post_type>
- Secondary keywords: <list>
- Deadline (publish-by): <date or "none">

## Why now (evidence — cite in the post where useful)
- <source>: <detail> (<url>)

## Must include
- Products to feature and link: <handles, verified>
- CTA: <cta_default + target>
- Customer questions to answer (from VOC, paraphrased): <list>
- For refreshes: what's decaying or out of date, and what to keep (URL handle stays the same)

## Tags to add
autopilot, autopilot-<trigger>, <cluster slug>
```

Default intent when the user hasn't chosen: store events and occasions → `promotion`; Search Console, competitor and AI-citation triggers → `search`; customer-question triggers → `education`; periodic → `search`.

## 2. Invoking the writer

Invoke the `shopify-blog-writer` skill with a message like:

> Write a Shopify blog post from this autopilot brief: `<path>`. Run in the mode the brief states (fully automated or guided) with **Shopify draft** delivery (hidden). The brief answers the setup questions. Add the tags listed in the brief. When done, report the article ID, handle, admin location, QA result and placeholders.

The writer does the keyword, SERP and voice-of-customer research, writing, images, schema, QA and the hidden draft itself. Don't duplicate its research here. The autopilot's evidence is a starting point, not a substitute.

**Refresh specifics.** The writer creates a new hidden article titled `[REFRESH] <original title>`, with the handle `<original-handle>-refresh-<yyyymmdd>` (Shopify handles must be unique) and a first-line note in the body: `<!-- Refresh of /blogs/<blog>/<handle>: copy this content into the original article to keep its URL, then delete this draft. -->`. Keeping the original URL preserves its links and rankings, which is the whole point of refreshing.

## 3. After the writer returns

Update the matching ledger topic (added with status `pending` by `--write-ledger`):

```json
{"id": "gsc-<keyword>", "date": "2026-09-29", "status": "drafted",
 "primary_keyword": "<keyword>", "cluster": "<cluster>", "intent": "commercial",
 "trigger": "gsc_striking", "action": "new", "refresh_target": null,
 "handle": "how-to-choose-<keyword>", "article_id": "gid://shopify/Article/123",
 "score": 78.8, "placeholders": 3}
```

- `status` is one of `pending` (decided, not yet written), `drafted` (hidden draft created), `html` (the writer fell back to HTML files) or `failed` (the writer errored; retry next run, and it still counts toward the cap only if a draft exists).
- If the writer failed completely, set `failed` and put the candidate back in the backlog, so the next run can retry it.

## 4. Ledger format (`ledger.json`)

```json
{
  "brand": "<slug>",
  "runs":    [{"date": "2026-09-29", "summary": {"write": 1, "backlog": 4, "skip": 6}, "written": ["gsc-<keyword>"], "status": "ok"}],
  "topics":  [ /* one per write decision, as above */ ],
  "backlog": [ /* candidate records + added_on + last_score */ ],
  "skips":   [{"id": "...", "date": "...", "primary_keyword": "...", "reasons": ["..."]}],
  "snapshots": {"out_of_stock": ["gid://shopify/Product/1"], "competitor_seen": {"competitor.example": "2026-09-28"}, "ai_check_date": "2026-09-01"}
}
```

A run counts as *successful* (for the lookback window) when it finished Step 7. Add `"status": "ok"` to the run entry after writing the report; use `"error"` with a note otherwise.

Keep the ledger small: the last 200 skips, and topics indefinitely (they're the dedupe memory and cheap).
