---
name: content-fact-check
description: Independent fact-checker for blog posts, product copy and marketing content, with guardrails for regulated claims. Pulls out each factual claim, flags the risky ones (FDA and other regulatory status such as "approved" or "cleared", medical and treatment claims, ingredient facts, pregnancy and safety statements, "clinically proven", statistics), verifies them against authoritative primary sources, and returns a claim-by-claim report with verdicts, citations and safer rewrites. Works for any brand and any market. Can run on its own on pasted text, a file, a URL or a Shopify article, or after shopify-blog-writer. Use whenever the user asks to fact-check, verify claims, check FDA or medical wording, review a post for compliance or accuracy, or says "is this accurate", "can we say this", or "check this before we publish", especially for health, beauty, wellness, treatment, supplement, skincare or food content.
---

# Content Fact-Check

## Effort (read before starting)

About 3 to 8 minutes and under $1 for a 1,000-word post with 10 to 20 claims; up to 15 minutes for a heavily regulated post. Estimate, not yet measured. Stop and tell the person if a run passes 20 minutes or $3.

Check what a piece of content claims, against sources that can actually settle the question, and say plainly what is solid, what needs different wording, and what to remove. This skill **flags and verifies; it never approves.** A claim marked "verified" means a primary source supported it on the date checked, not that the brand is legally cleared to say it. Regulated claims still need a qualified human or legal review.

It stands alone: it doesn't depend on any writing skill, and any writing skill can hand content to it.

## Reference files

| File | Read at |
|---|---|
| `references/claim-types.md` | Step 2: claim categories, risk tiers, and the precise wording rules for regulatory status |
| `references/sources.md` | Step 3: which sources settle which kind of claim, by market |
| `references/report-template.md` | Step 5: the report layout |
| `scripts/flag_claims.py` | Step 1: cheap pre-screen that finds candidate claims, so research is spent only where it matters |

## Operating rules

- **Primary sources only for risky claims.** Regulator databases, official labels, peer-reviewed studies, clinical registries and professional bodies. Another brand's blog, a forum or an AI summary can point you to a source but can't be the source.
- **Date-stamp everything.** Regulatory status, labels and guidance change. Record the URL and the date you checked.
- **No source, no claim.** If a claim can't be verified, the verdict is "cannot verify" and the fix is to remove or soften it, not to assume it's fine.
- **Don't add claims.** Rewrites may only make a claim narrower, more precise or better qualified, never stronger.
- **Not legal or medical advice.** Say so once in the report. Flag claims needing expert or legal sign-off instead of ruling on them.
- **Spend research where the risk is.** Check every high-risk claim; sample the medium-risk ones; leave plain common knowledge alone.
- **Read-only by default.** Don't edit a live article or any store content unless the user asks you to apply fixes, and even then produce the revised text for them to publish.

## Step 0: Get the content and the context

1. **Content:** pasted text, a file, a URL (fetch it), or a Shopify article (via the connector or browser, read-only). If the user says "the post we just wrote", use the writer's HTML.
2. **Brand context (optional but useful):** find the right store's `BRAND.md` using the lookup order in brand-capture `references/brand-context.md` if that plugin is installed (project root, user local environment, central brand directory `$BRAND_AI_HOME/brands/<slug>/` or `~/.brand-ai/brands/<slug>/`, then memory and connected knowledge); otherwise the project root. The file whose `site`, `store` or `brand` matches the content wins; if unclear, ask which store. Read only: front matter `markets` (which regulator applies), `regulated` and `brand_approver`; Terminology; and Claim limits (Approved claims, Never say (client), Not allowed, Required disclaimers). Only Approved claims may be treated as brand-confirmed; flag anything under Never say or Not allowed. Never edit BRAND.md: when you find something that should change, append a line to `BRAND-REQUESTS.md` next to it. If there's no file, ask one short question only if it matters: which country or countries is this for, and what do the products or treatments do? Otherwise infer from the content and state your assumption.
3. **Mode:** *report only* (default) or *report and apply fixes* (also returns revised text). If unclear, do the report and offer the revision.

## Step 1: Pre-screen

Save the content to a file and run the screener. It splits the text into sentences and flags those containing regulatory, medical, safety, ingredient, statistical, performance or sustainability language, with a risk tier:

```bash
python scripts/flag_claims.py <content.html|.txt|.md> --json
```

Use its output as the candidate list, then add anything it missed (it uses patterns, not understanding) and drop false alarms. For short content you can skip the script and read it yourself.

## Step 2: Extract and classify claims

Read `references/claim-types.md`. Turn flagged sentences into **atomic claims** (one checkable statement each, so "FDA-approved and safe for all skin types" becomes two). For each, note the category and risk tier, and whether the post already cites a source for it.

## Step 3: Verify

Read `references/sources.md`. Work high-risk claims first:

1. Identify exactly what is being claimed (which product, device, drug or ingredient, which indication, which population, which country).
2. Look it up in the source that settles it (for example the regulator's database for status, the official label for indications and warnings, the study or registry for efficacy numbers).
3. Compare **precisely**: the exact term (approved vs cleared), the exact indication, the exact figure, the exact population, the date.
4. Record the finding, the URL and the date accessed.

If a search tool or page is unavailable, say which check couldn't be done; don't fill the gap from memory. For each claim, assign one verdict:

| Verdict | Meaning |
|---|---|
| **Verified** | A primary source supports the claim as worded, as of the date checked |
| **Needs rewording** | True in part, but the wording is wrong, too broad or misleading (the usual fix is a more precise phrase) |
| **Incorrect** | A primary source contradicts it |
| **Unsupported** | No adequate evidence found, or only weak or promotional sources |
| **Cannot verify** | Couldn't be checked (source unavailable, not publicly documented); treat as unsupported until a human confirms |
| **Needs expert sign-off** | Verifiable in principle but too sensitive to rule on: individual medical advice, pregnancy and breastfeeding safety, treatment outcomes, legal compliance |

## Step 4: Fix

For every claim that isn't Verified, write the smallest safe fix: a precise rewording, a qualifier, a citation to add, or removal. Keep the brand's voice. Where a standard disclaimer is needed (for example the brand file requires one, or supplement structure/function wording needs its notice), suggest it. In *apply fixes* mode, produce the revised text with each change listed, preserving the HTML.

## Step 5: Report

Use `references/report-template.md`. Lead with the verdict summary (counts by verdict, and the one or two claims that matter most), then the claim table, then the rewrites, then what needs a human. Plain language; explain regulatory terms in a few words. Save the report next to the content (`<name>-fact-check.md`) and show a short version.

When invoked by another skill (for example from the blog writer), also return a compact result: counts by verdict, the list of claims changed or removed, and the list needing expert sign-off.

## Credit efficiency

Run the screener first, check high-risk claims before anything else, batch several claims about the same product into one lookup, reuse one source for every claim it covers, and stop researching a claim once a primary source settles it.
