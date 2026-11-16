#!/usr/bin/env python3
"""Campaign calendar: print the one-line plan summary and write an .ics file.

The .ics holds three events: the campaign itself (start to end), "Launch: <name>" at the start and
"Stop: <name>" at the stop time (the end, unless --stop says otherwise). Launch and Stop carry a
reminder and the exact sentence to say to Claude, so the owner can act on time even where Claude
can't run scheduled tasks.

Usage:
  python campaign_calendar.py --name "Autumn Stroll Sale" --types "Seasonal,Discount" \
      --start "2026-11-10 00:00" --end "2026-11-17 23:59" --tz America/New_York \
      --channels "Website,Email,SMS,Ads" --offer "35% off sitewide" \
      --preview "https://example.com/?preview_theme_id=123" --out campaigns/autumn-stroll/autumn-stroll.ics

  --tz needs Python's time zone data (built in on macOS and Linux; on Windows, `pip install tzdata`).
  Without it, pass --utc-offset=-05:00 instead (the offset in force on the start date; keep the "=").
  Leave out --out to only print the summary line (for the plan step).

Standard library only. Exit code 2 on bad input, with the reason on stderr.
"""
import argparse
import datetime as dt
import re
import sys

TYPES = {
    "seasonal": "Seasonal",
    "season": "Seasonal",
    "product launch": "Product launch",
    "product": "Product launch",
    "launch": "Product launch",
    "new product": "Product launch",
    "discount": "Discount",
    "promotion": "Discount",
    "promo": "Discount",
    "promotional": "Discount",
    "sale": "Discount",
}
TYPE_ORDER = ["Seasonal", "Product launch", "Discount"]
CHANNELS = {"website": "Website", "web": "Website", "email": "Email", "sms": "SMS", "text": "SMS",
            "ads": "Ads", "ad": "Ads", "paid ads": "Ads", "digital ads": "Ads"}
CHANNEL_ORDER = ["Website", "Email", "SMS", "Ads"]


def fail(msg):
    print("campaign_calendar.py: " + msg, file=sys.stderr)
    sys.exit(2)


def parse_local(value, label):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", value or ""):
        fail(f"{label} must be a specific date and time, YYYY-MM-DD HH:MM (got {value!r}). "
             "Relative dates like 'next week' or 'for three days' must be turned into real dates first.")
    try:
        return dt.datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError as e:
        fail(f"{label}: {e}")


def parse_offset(value):
    value = re.sub(r"^(UTC|GMT)", "", (value or "").strip(), flags=re.I)
    m = re.fullmatch(r"([+-])(\d{2}):?(\d{2})", value)
    if not m:
        fail(f"--utc-offset must look like --utc-offset=-05:00 or --utc-offset=+01:00 (got {value!r})")
    sign = 1 if m.group(1) == "+" else -1
    return dt.timezone(sign * dt.timedelta(hours=int(m.group(2)), minutes=int(m.group(3))))


def to_utc(local, tz_name, offset):
    if offset is not None:
        return local.replace(tzinfo=offset).astimezone(dt.timezone.utc)
    try:
        from zoneinfo import ZoneInfo
        zone = ZoneInfo(tz_name)
    except Exception:
        fail(f"no time zone data for {tz_name!r} on this computer. Run `pip install tzdata`, "
             "or pass the store's offset on that date instead, for example --utc-offset=-05:00.")
    return local.replace(tzinfo=zone).astimezone(dt.timezone.utc)


def normalise(raw, table, order, label):
    out = []
    for part in [p.strip() for p in (raw or "").split(",") if p.strip()]:
        key = part.lower()
        if key not in table:
            fail(f"unknown {label} {part!r}; use one or more of: {', '.join(order)}")
        if table[key] not in out:
            out.append(table[key])
    if not out:
        fail(f"give at least one {label}")
    return sorted(out, key=order.index)


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:40] or "campaign"


def human(local):
    return f"{local:%b} {local.day} {local.year}, {local:%H:%M}"


def esc(text):
    return (text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
            .replace("\r\n", "\\n").replace("\n", "\\n"))


def fold(line):
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts, chunk = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        limit = 75 if not parts else 74
        if len(chunk) + len(b) > limit:
            parts.append(chunk.decode("utf-8"))
            chunk = b""
        chunk += b
    parts.append(chunk.decode("utf-8"))
    return "\r\n ".join(parts)


def stamp(t):
    return t.strftime("%Y%m%dT%H%M%SZ")


def event(uid, start, end, summary, description, alarms_min=()):
    lines = ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp(dt.datetime.now(dt.timezone.utc))}",
             f"DTSTART:{stamp(start)}", f"DTEND:{stamp(end)}", f"SUMMARY:{esc(summary)}",
             f"DESCRIPTION:{esc(description)}"]
    for minutes in alarms_min:
        lines += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{esc(summary)}",
                  f"TRIGGER:-PT{minutes}M", "END:VALARM"]
    lines.append("END:VEVENT")
    return lines


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--types", required=True, help="one or more of Seasonal, Product launch, Discount")
    ap.add_argument("--start", required=True, help="YYYY-MM-DD HH:MM, store time")
    ap.add_argument("--end", required=True, help="YYYY-MM-DD HH:MM, store time")
    ap.add_argument("--stop", help="when to run Stop, if not at the end (YYYY-MM-DD HH:MM)")
    ap.add_argument("--tz", help="store time zone, IANA name such as America/New_York")
    ap.add_argument("--utc-offset", help="instead of --tz: offset such as -05:00")
    ap.add_argument("--channels", default="Website,Email,SMS,Ads")
    ap.add_argument("--offer", default="")
    ap.add_argument("--preview", default="", help="preview link for the website")
    ap.add_argument("--slug")
    ap.add_argument("--out", help="where to write the .ics; leave out to only print the summary")
    a = ap.parse_args()

    if not a.tz and not a.utc_offset:
        fail("give the store time zone with --tz (or --utc-offset)")
    offset = parse_offset(a.utc_offset) if a.utc_offset else None
    tz_label = a.tz or ("UTC" + re.sub(r"^(UTC|GMT)", "", a.utc_offset.strip(), flags=re.I))
    start_l, end_l = parse_local(a.start, "--start"), parse_local(a.end, "--end")
    stop_l = parse_local(a.stop, "--stop") if a.stop else end_l
    if end_l <= start_l:
        fail("the end must be after the start")
    if stop_l < end_l:
        fail("Stop can't run before the campaign ends")
    types = normalise(a.types, TYPES, TYPE_ORDER, "type")
    channels = normalise(a.channels, CHANNELS, CHANNEL_ORDER, "channel")
    slug = a.slug or slugify(a.name)

    if a.out:
        start_u, end_u, stop_u = (to_utc(x, a.tz, offset) for x in (start_l, end_l, stop_l))
    summary = (f"Campaign: {a.name} · {' + '.join(types)} · {human(start_l)} to {human(end_l)} "
               f"({tz_label}) · {', '.join(channels)}")
    print(summary)
    if not a.out:
        return

    fifteen = dt.timedelta(minutes=15)
    details = [f"Type: {' + '.join(types)}", f"Channels: {', '.join(channels)}"]
    if a.offer:
        details.insert(0, f"Offer: {a.offer}")
    if a.preview:
        details.append(f"Website preview: {a.preview}")
    details.append(f"Campaign file: campaigns/{slug}/campaign.md")
    launch_desc = ("Time to launch. Say to Claude: \"Launch the " + a.name + " campaign.\"\n"
                   "Claude checks the live site hasn't changed since the preview was made, then you publish "
                   "the preview theme (Online Store > Themes > Publish). The discount should start on its own "
                   "if its start date is set in Shopify.\n\n" + "\n".join(details))
    stop_desc = ("Time to stop. Say to Claude: \"Stop the " + a.name + " campaign.\"\n"
                 "Claude puts the site back the way it was before the campaign, on a copy you approve and "
                 "publish. A countdown hides itself; the bar and hero stay until this is done.\n\n"
                 + "\n".join(details))

    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Nyla//campaign-launcher//EN", "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH"]
    lines += event(f"{slug}-campaign-{stamp(start_u)}@campaign-launcher", start_u, end_u,
                   f"{a.name} ({' + '.join(types)})", "\n".join(details))
    lines += event(f"{slug}-launch-{stamp(start_u)}@campaign-launcher", start_u, start_u + fifteen,
                   f"Launch: {a.name}", launch_desc, alarms_min=(1440, 30))
    lines += event(f"{slug}-stop-{stamp(stop_u)}@campaign-launcher", stop_u, stop_u + fifteen,
                   f"Stop: {a.name}", stop_desc, alarms_min=(30,))
    lines.append("END:VCALENDAR")
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(fold(x) for x in lines) + "\r\n")
    print(f"Calendar file: {a.out} (campaign, Launch at {human(start_l)}, Stop at {human(stop_l)}, {tz_label})")


if __name__ == "__main__":
    main()
