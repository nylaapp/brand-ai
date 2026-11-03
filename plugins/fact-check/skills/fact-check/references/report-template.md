# Report layout

Save as `<content-name>-fact-check.md`. Show the user a short version (the summary and the items needing action); keep the full detail in the file. Use plain language and explain regulatory terms in a few words.

```markdown
# Fact-check: <content title>
**Checked:** <YYYY-MM-DD> · **Market(s):** <countries> · **Brand context:** <brand file used | none>
**Scope:** <n> claims found, <n> checked in depth

> This is a fact-check, not legal or medical advice. "Verified" means a primary source supported the wording on the date above. Regulated claims should still be reviewed by a qualified person before publishing.

## Summary
| Verified | Needs rewording | Incorrect | Unsupported | Cannot verify | Needs expert sign-off |
|---|---|---|---|---|---|
| n | n | n | n | n | n |

**Most important:** <the 1–3 claims that matter most, in one line each>

## Claim-by-claim
| # | Claim (as written) | Category / risk | Verdict | What the source says | Source (date checked) |
|---|---|---|---|---|---|
| 1 | "…" | Regulatory / High | Needs rewording | <exact finding> | <title, URL (YYYY-MM-DD)> |

## Suggested rewrites
| # | Original | Suggested | Why |
|---|---|---|---|

## Needs a person
<Claims marked "Needs expert sign-off" or "Cannot verify", and who should look: legal/regulatory, clinician, product team (e.g., to confirm the product's cleared indication).>

## Disclaimers to consider
<Only those the brand file or the claim type calls for.>

## Checks not done
<Anything you couldn't verify and why (source unavailable, not public, outside the market).>
```

## Result for another skill

When another skill calls this one, return: counts by verdict, the claims changed or removed (number and one-line reason each), and the list needing expert sign-off.
