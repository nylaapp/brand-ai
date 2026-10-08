# Occasion calendar

Seasonal posts need time to be crawled, indexed and to earn some ranking before the peak. So the calendar isn't about the occasion date; it's about the **window** that opens `lead_days` before it.

```
window_opens = date − lead_days      (start drafting)
publish_by   = date − publish_by_days  (default 14, for indexing; holiday gifting uses 35 so guides are live before Black Friday shoppers start)
status: upcoming → open → late → (past)
```

`scripts/occasions.py` computes this from the profile's markets. It includes rule-based dates (nth weekday, Easter-relative, US Thanksgiving-relative), so nothing needs updating each year, and explicit date lists for lunar holidays (Lunar New Year and Diwali through 2028; extend these lists as the years roll on).

## Defaults (filtered by the brand's markets)

| Group | Occasions (lead days) |
|---|---|
| Q4 retail peak | Halloween (49), US Thanksgiving (49), **Black Friday/Cyber Monday (63)**, **holiday gifting (77)**, Boxing Day (35), Diwali (49), Singles' Day (42), Canadian Thanksgiving (42) |
| Gifting | Valentine's (49), Mother's Day (56; UK uses Mothering Sunday), Father's Day (56; AU/NZ in September) |
| Retail sales | Memorial Day, Fourth of July, Labor Day (US, 35) |
| Resolutions and seasons | New Year (42), spring/summer/fall/winter by hemisphere (42), back to school (56 US/CA, 49 UK/IE) |
| Values | International Women's Day (35), Earth Day (35) |
| Regional | Lunar New Year (42), Easter (42) |

The script has the full list with market filters. Disable any default with `occasions.exclude` in the profile.

## Markets the defaults don't cover

The default calendar is broad but not complete. It has no entry for many regional occasions (for example Ramadan and Eid, Golden Week, Chuseok, Songkran, Carnival, local harvest or school-term dates). Never assume the defaults are right for a market. During setup, once the markets are known, check which defaults apply. If the market has few, offer 3–5 *suggested* local occasions from a web search, labeled as suggestions, for the user to confirm into `occasions.custom`. Don't add them silently.

## Brand-specific additions (profile `occasions.custom`)

Good candidates: the brand's anniversary or annual sale, niche awareness days in its category (for example an awareness day or month that matches what the brand sells), a regional festival for its market, trade-show dates, and marketplace sale events such as Prime Day once the dates are announced, since those change every year.

```yaml
custom:
  - id: "<occasion_id>"
    name: "<Occasion name>"
    date: "rule: 10-01"
    lead_days: 42
    post_types: ["informational", "brand"]
```

## Fit and refresh rules

- **Fit first.** An open window is permission, not an order. Occasion candidates still go through the rubric; a weak brand fit gets a low business value and is skipped.
- **Refresh beats new.** If last year's post for the occasion exists, refresh it at the same URL. The scorer enforces this when the keyword matches an older article, but check yourself too, since occasion titles vary ("gift guide 2025" vs. "gifts for hikers").
- **Late windows.** Past `publish_by`, organic search benefit is small, but a transactional post (sale announcement, last-minute gifts) can still help email and social. It gets urgency 3 by default.
