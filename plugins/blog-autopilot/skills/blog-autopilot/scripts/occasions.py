#!/usr/bin/env python3
"""List upcoming occasions for a brand's markets and say whether each lead-time window is open.

Usage:
  python occasions.py --profile brand-profile.yaml [--today YYYY-MM-DD] [--horizon 120] [--json]

Each occasion has a date rule and a lead time (days before the occasion when drafting should start).
The window is:
  upcoming : before the window opens (listed only if it opens within 30 days)
  open     : today is between (date - lead_days) and the publish-by date   -> suggest urgency 5
  late     : past publish-by but before the occasion (SEO benefit is small) -> suggest urgency 2-3,
             still fine for transactional/gift posts or a refresh of last year's post
publish_by = date - publish_by_days (default 14: time for indexing; gift guides use more, since shoppers start at BFCM). It becomes the candidate's deadline.

Rule formats (defaults below; profiles add their own under occasions.custom):
  fixed:MM-DD | nth:N:DOW:MONTH (N=-1 for last; DOW mon..sun) | thanksgiving_us+K | easter+K
  dates:[YYYY-MM-DD, ...] for lunar/variable holidays | a plain "date: YYYY-MM-DD" in custom entries
"""
import argparse
import datetime as dt
import json
import os
import sys

DOW = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
NORTH = ["US", "CA", "GB", "IE", "DE", "FR", "NL", "ES", "IT", "SE", "NO", "DK", "FI", "JP", "KR", "CN", "IN"]
SOUTH = ["AU", "NZ", "ZA", "AR", "CL", "BR"]
WEST = ["US", "CA", "GB", "IE", "AU", "NZ", "DE", "FR", "NL", "ES", "IT", "SE", "NO", "DK", "FI"]
ALL = "*"

DEFAULTS = [
    {"id": "new_year", "name": "New Year (resolutions, fresh starts)", "rule": "fixed:01-01", "lead_days": 42, "markets": ALL, "post_types": ["informational", "commercial"]},
    {"id": "lunar_new_year", "name": "Lunar New Year", "rule": "dates:2026-02-17,2027-02-06,2028-01-26", "lead_days": 42, "markets": ["CN", "HK", "TW", "SG", "MY", "VN", "KR"], "post_types": ["commercial", "transactional"]},
    {"id": "valentines_day", "name": "Valentine's Day", "rule": "fixed:02-14", "lead_days": 49, "markets": ALL, "post_types": ["commercial", "transactional"]},
    {"id": "womens_day", "name": "International Women's Day", "rule": "fixed:03-08", "lead_days": 35, "markets": ALL, "post_types": ["brand"]},
    {"id": "mothering_sunday_uk", "name": "Mother's Day (UK/IE)", "rule": "easter-21", "lead_days": 49, "markets": ["GB", "IE"], "post_types": ["commercial", "transactional"]},
    {"id": "easter", "name": "Easter", "rule": "easter+0", "lead_days": 42, "markets": WEST, "post_types": ["commercial", "informational"]},
    {"id": "earth_day", "name": "Earth Day", "rule": "fixed:04-22", "lead_days": 35, "markets": ALL, "post_types": ["brand", "informational"]},
    {"id": "mothers_day", "name": "Mother's Day", "rule": "nth:2:sun:5", "lead_days": 56, "markets": ["US", "CA", "AU", "NZ", "JP", "IN", "DE", "IT"], "post_types": ["commercial", "transactional"]},
    {"id": "memorial_day_us", "name": "Memorial Day (US sales, summer kickoff)", "rule": "nth:-1:mon:5", "lead_days": 35, "markets": ["US"], "post_types": ["transactional"]},
    {"id": "fathers_day", "name": "Father's Day", "rule": "nth:3:sun:6", "lead_days": 56, "markets": ["US", "CA", "GB", "IE", "IN", "JP"], "post_types": ["commercial", "transactional"]},
    {"id": "fathers_day_au", "name": "Father's Day (AU/NZ)", "rule": "nth:1:sun:9", "lead_days": 56, "markets": ["AU", "NZ"], "post_types": ["commercial", "transactional"]},
    {"id": "independence_day_us", "name": "Fourth of July", "rule": "fixed:07-04", "lead_days": 35, "markets": ["US"], "post_types": ["informational", "transactional"]},
    {"id": "back_to_school", "name": "Back to school", "rule": "fixed:08-10", "lead_days": 56, "markets": ["US", "CA"], "post_types": ["commercial"]},
    {"id": "back_to_school_uk", "name": "Back to school (UK/IE)", "rule": "fixed:09-01", "lead_days": 49, "markets": ["GB", "IE"], "post_types": ["commercial"]},
    {"id": "labor_day_us", "name": "Labor Day", "rule": "nth:1:mon:9", "lead_days": 35, "markets": ["US"], "post_types": ["transactional"]},
    {"id": "thanksgiving_ca", "name": "Thanksgiving (Canada)", "rule": "nth:2:mon:10", "lead_days": 42, "markets": ["CA"], "post_types": ["informational", "commercial"]},
    {"id": "halloween", "name": "Halloween", "rule": "fixed:10-31", "lead_days": 49, "markets": ["US", "CA", "GB", "IE"], "post_types": ["informational", "commercial"]},
    {"id": "diwali", "name": "Diwali", "rule": "dates:2026-11-08,2027-10-29,2028-10-17", "lead_days": 49, "markets": ["IN"], "post_types": ["commercial", "transactional"]},
    {"id": "singles_day", "name": "Singles' Day (11.11)", "rule": "fixed:11-11", "lead_days": 42, "markets": ["CN", "SG", "MY", "KR"], "post_types": ["transactional"]},
    {"id": "thanksgiving_us", "name": "Thanksgiving (US: hosting, recipes, gratitude)", "rule": "thanksgiving_us+0", "lead_days": 49, "markets": ["US"], "post_types": ["informational", "commercial"]},
    {"id": "bfcm", "name": "Black Friday / Cyber Monday", "rule": "thanksgiving_us+1", "lead_days": 63, "markets": ALL, "post_types": ["commercial", "transactional"]},
    {"id": "holiday_gifting", "name": "Holiday gifting (Christmas gift guides)", "rule": "fixed:12-25", "lead_days": 77, "publish_by_days": 35, "markets": WEST + ["SG", "PH", "ZA", "BR", "MX"], "post_types": ["commercial", "transactional"]},
    {"id": "boxing_day", "name": "Boxing Day sales", "rule": "fixed:12-26", "lead_days": 35, "markets": ["GB", "IE", "CA", "AU", "NZ"], "post_types": ["transactional"]},
    {"id": "spring", "name": "Spring (seasonal routines, refresh)", "rule": "fixed:03-20", "lead_days": 42, "markets": NORTH, "post_types": ["informational"]},
    {"id": "summer", "name": "Summer (seasonal routines, travel)", "rule": "fixed:06-21", "lead_days": 42, "markets": NORTH, "post_types": ["informational"]},
    {"id": "fall", "name": "Fall/autumn (seasonal routines)", "rule": "fixed:09-22", "lead_days": 42, "markets": NORTH, "post_types": ["informational"]},
    {"id": "winter", "name": "Winter (seasonal routines, care)", "rule": "fixed:12-21", "lead_days": 42, "markets": NORTH, "post_types": ["informational"]},
    {"id": "spring_south", "name": "Spring (southern hemisphere)", "rule": "fixed:09-22", "lead_days": 42, "markets": SOUTH, "post_types": ["informational"]},
    {"id": "summer_south", "name": "Summer (southern hemisphere)", "rule": "fixed:12-21", "lead_days": 42, "markets": SOUTH, "post_types": ["informational"]},
    {"id": "fall_south", "name": "Autumn (southern hemisphere)", "rule": "fixed:03-20", "lead_days": 42, "markets": SOUTH, "post_types": ["informational"]},
    {"id": "winter_south", "name": "Winter (southern hemisphere)", "rule": "fixed:06-21", "lead_days": 42, "markets": SOUTH, "post_types": ["informational"]},
]


def easter(y):
    a = y % 19; b = y // 100; c = y % 100; d_ = b // 4; e = b % 4
    f = (b + 8) // 25; g = (b - f + 1) // 3; h = (19 * a + b - d_ - g + 15) % 30
    i = c // 4; k = c % 4; l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31; day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(y, month, day)


def nth_weekday(y, month, n, dow):
    if n > 0:
        first = dt.date(y, month, 1)
        off = (dow - first.weekday()) % 7
        return first + dt.timedelta(days=off + 7 * (n - 1))
    nxt = dt.date(y + (month == 12), month % 12 + 1, 1)
    last = nxt - dt.timedelta(days=1)
    return last - dt.timedelta(days=(last.weekday() - dow) % 7)


def dates_for(rule, year):
    rule = str(rule).strip()
    if rule.startswith("fixed:"):
        mm, dd = rule[6:].split("-")
        return [dt.date(year, int(mm), int(dd))]
    if rule.startswith("nth:"):
        _, n, dow, month = rule.split(":")
        return [nth_weekday(year, int(month), int(n), DOW[dow[:3].lower()])]
    if rule.startswith("thanksgiving_us"):
        k = int(rule[len("thanksgiving_us"):] or 0)
        return [nth_weekday(year, 11, 4, 3) + dt.timedelta(days=k)]
    if rule.startswith("easter"):
        k = int(rule[len("easter"):] or 0)
        return [easter(year) + dt.timedelta(days=k)]
    if rule.startswith("dates:"):
        out = []
        for s in rule[6:].split(","):
            s = s.strip()
            if s and int(s[:4]) == year:
                out.append(dt.date.fromisoformat(s))
        return out
    if rule.startswith("rule:"):
        return dates_for("fixed:" + rule[5:].strip(), year)
    try:
        dd = dt.date.fromisoformat(rule)
        return [dd] if dd.year == year else []
    except ValueError:
        return []


def load_profile(path):
    if not path or not os.path.exists(path):
        return {}
    with open(path) as f:
        t = f.read()
    if path.endswith((".yaml", ".yml")):
        import yaml
        return yaml.safe_load(t) or {}
    return json.loads(t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=None)
    ap.add_argument("--today", default=dt.date.today().isoformat())
    ap.add_argument("--horizon", type=int, default=120, help="days ahead to list")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today)
    prof = load_profile(a.profile)
    markets_cfg = prof.get("markets") or {}
    # No default market: assuming one (e.g. the US) would give other brands the wrong calendar.
    # With no markets set, only the universal (all-market) occasions apply.
    markets = set(m for m in [markets_cfg.get("primary")] + list(markets_cfg.get("others") or []) if m)
    if not markets:
        print("warning: profile has no markets.primary; only universal occasions are listed. "
              "Set markets in the brand profile.", file=sys.stderr)
    occ_cfg = prof.get("occasions") or {}
    items = []
    if occ_cfg.get("use_defaults", True):
        excl = set(occ_cfg.get("exclude") or [])
        for o in DEFAULTS:
            if o["id"] in excl:
                continue
            if o["markets"] != ALL and not (markets & set(o["markets"])):
                continue
            items.append(dict(o, source="default"))
    for o in occ_cfg.get("custom") or []:
        if not o:
            continue
        o = dict(o)
        o.setdefault("rule", o.get("date"))
        o.setdefault("lead_days", 42)
        o["source"] = "custom"
        items.append(o)

    out = []
    for o in items:
        for y in (today.year, today.year + 1):
            for day in dates_for(o["rule"], y):
                if day < today or (day - today).days > a.horizon + int(o["lead_days"]):
                    continue
                opens = day - dt.timedelta(days=int(o["lead_days"]))
                publish_by = day - dt.timedelta(days=int(o.get("publish_by_days", 14)))
                if today < opens:
                    if (opens - today).days > 30:
                        continue
                    status, urg = "upcoming", 2
                elif today <= publish_by:
                    status, urg = "open", 5
                else:
                    status, urg = "late", 3
                out.append({"id": o["id"], "name": o.get("name", o["id"]), "date": day.isoformat(),
                            "window_opens": opens.isoformat(), "publish_by": publish_by.isoformat(),
                            "days_until": (day - today).days, "status": status,
                            "suggested_urgency": urg, "post_types": o.get("post_types", []),
                            "source": o["source"]})
    out.sort(key=lambda x: x["date"])
    if a.json:
        print(json.dumps({"today": today.isoformat(), "markets": sorted(markets), "occasions": out}, indent=2))
    else:
        print(f"Occasions for markets {sorted(markets)} as of {today}:")
        for x in out:
            print(f"  [{x['status']:8}] {x['date']}  {x['name']:<48} window {x['window_opens']} → publish by {x['publish_by']}")


if __name__ == "__main__":
    main()
