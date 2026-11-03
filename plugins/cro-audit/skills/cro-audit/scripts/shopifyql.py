#!/usr/bin/env python3
"""Read Shopify Analytics with ShopifyQL through the Shopify CLI. READ-ONLY. Stdlib only.

  shopifyql.py --store <shop>.myshopify.com --check
  shopifyql.py --store <shop>.myshopify.com --preset device-funnel --since 2026-10-20 --until 2026-11-01
  shopifyql.py --store <shop>.myshopify.com --preset all --since -28d --until -1d

Dates: YYYY-MM-DD, -Nd (days before today), today or yesterday, read in the store's time zone. Relative
dates are turned into absolute ones before querying, because a relative UNTIL can drop the last day.
  shopifyql.py --store <shop>.myshopify.com --query "FROM sessions SHOW sessions GROUP BY referrer_source SINCE -28d UNTIL -1d"

Runs `shopify store execute` with a GraphQL *query* only. It never passes --allow-mutations, and it
refuses anything that looks like a write (the words mutation, Create, Update, Delete, Set, Remove,
Publish). It can't change the store.

Needs the CLI to be authorised for the store with `read_reports` (analytics) and, for sales by
channel, `read_orders`. If access is denied it says so and stops. Granting access is the person's step,
never this script's: they run `shopify store auth -s <store> --scopes <existing scopes>,read_reports,read_orders`
themselves and approve it in the browser.

--preset choices:
  check-data      sessions per day, to find step changes (a storefront switch, a tracking break)
  device-funnel   sessions -> cart -> checkout -> completed, by device
  landing         top entry pages with bounce and time
  sources         sessions and bounce by traffic source and device
  social          social sessions by network and by entry page
  orders-channel  orders and net sales by sales channel (subscriptions, other storefronts, POS)
  homepage        homepage entries by device and by source
  all             all of the above
--csv prints the device funnel as Name=count steps ready for funnel.py.
"""
import argparse, datetime, json, re, subprocess, sys

WRITE_WORDS = re.compile(r"\b(mutation|create|update|delete|set|remove|publish|upsert|append)\b", re.I)

def run_graphql(store, gql):
    if WRITE_WORDS.search(gql.split("shopifyqlQuery", 1)[0]) or gql.lstrip().lower().startswith("mutation"):
        sys.exit("refused: this script only reads. It will not send a mutation.")
    cmd = ["shopify", "store", "execute", "-s", store, "--no-input", "-j", "-q", gql]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except FileNotFoundError:
        sys.exit("The Shopify CLI isn't installed. Ask the person for an analytics export instead.")
    # with -j the result is JSON on stdout (possibly after a hint); progress events go to stderr,
    # one JSON object per line, and an error may arrive on either stream
    data = None
    so = out.stdout
    if "{" in so:
        try:
            data = json.loads(so[so.find("{"):])
        except ValueError:
            data = None
    if data is None:
        for line in reversed((out.stderr or "").splitlines()):
            line = line[line.find("{"):] if "{" in line else ""
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            if "error" in obj:
                data = obj
                break
    if data is None:
        sys.exit("Unexpected CLI output:\n" + (out.stdout + out.stderr)[-1500:])
    if "error" in data:
        msg = json.dumps(data["error"])
        if "ACCESS_DENIED" in msg or "Access denied" in msg:
            need = re.findall(r"`(read_[a-z_]+)`", msg)
            sys.exit("ACCESS DENIED: the CLI connection lacks " + (", ".join(sorted(set(need))) or "a required scope") +
                     ". Granting it is the person's decision: they run `shopify store auth` themselves. Nothing was changed.")
        if "auth" in msg.lower() or "login" in msg.lower():
            sys.exit("The CLI isn't authorised for this store. The person runs `shopify store auth` themselves. Nothing was changed.")
        sys.exit("CLI error: " + msg[:1200])
    return data

def shopifyql(store, q):
    data = run_graphql(store, "{ shopifyqlQuery(query: %s) { tableData { columns { name } rows } parseErrors } }" % json.dumps(q))
    r = data.get("shopifyqlQuery") or {}
    if r.get("parseErrors"):
        sys.exit(f"ShopifyQL parse error in: {q}\n{r['parseErrors']}")
    td = r.get("tableData") or {"columns": [], "rows": []}
    return [c["name"] for c in td["columns"]], td["rows"]

def fmt(v):
    if v is None:
        return "(none)"
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if f.is_integer():
        return f"{int(f):,}"
    return f"{f:.3f}" if abs(f) < 1 else f"{f:,.2f}"

def table(title, cols, rows, limit=25):
    print(f"\n### {title}\n")
    if not rows:
        print("(no rows)")
        return
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for row in rows[:limit]:
        print("| " + " | ".join(fmt(row.get(c)) for c in cols) + " |")

REL = re.compile(r"^-(\d+)d$")

def join_dash_values(argv):
    """Let `--since -28d` work: argparse would read -28d as a new option."""
    out, i = [], 0
    while i < len(argv):
        if argv[i] in ("--since", "--until") and i + 1 < len(argv) and REL.match(argv[i + 1]):
            out.append(f"{argv[i]}={argv[i + 1]}")
            i += 2
        else:
            out.append(argv[i])
            i += 1
    return out

def resolve_date(value, today):
    """Turn -Nd, today or yesterday into an absolute YYYY-MM-DD in the store's time zone.

    ShopifyQL's relative UNTIL (for example UNTIL -1d) was seen returning 0 for the last day while the
    same day queried by date had data, so the window is always sent as absolute dates."""
    v = value.strip().lower()
    m = REL.match(v)
    if m:
        return (today - datetime.timedelta(days=int(m.group(1)))).isoformat()
    if v == "today":
        return today.isoformat()
    if v == "yesterday":
        return (today - datetime.timedelta(days=1)).isoformat()
    try:
        datetime.date.fromisoformat(v)
    except ValueError:
        sys.exit(f"bad date '{value}': use YYYY-MM-DD, -Nd (for example -28d), today or yesterday")
    return v

def store_today(store):
    d = run_graphql(store, "{ shop { ianaTimezone } }")
    tz = d["shop"]["ianaTimezone"]
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo(tz)).date(), tz
    except Exception:
        return datetime.date.today(), "local time (store time zone unavailable)"

FUNNEL = "sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout"

def presets(win):
    return {
        "check-data": ("Sessions per day", f"FROM sessions SHOW sessions TIMESERIES day {win}"),
        "device-funnel": ("Shop funnel by device", f"FROM sessions SHOW {FUNNEL} GROUP BY session_device_type {win}"),
        "landing": ("Top entry pages", f"FROM sessions SHOW sessions, bounce_rate, average_session_duration GROUP BY landing_page_path {win} ORDER BY sessions DESC LIMIT 15"),
        "sources": ("Traffic by source and device", f"FROM sessions SHOW sessions, bounce_rate GROUP BY referrer_source, session_device_type {win} ORDER BY sessions DESC LIMIT 15"),
        "social": ("Social by network", f"FROM sessions SHOW sessions GROUP BY referrer_name WHERE referrer_source = 'social' {win} ORDER BY sessions DESC LIMIT 10"),
        "social-landing": ("Social by entry page", f"FROM sessions SHOW sessions, bounce_rate GROUP BY landing_page_path WHERE referrer_source = 'social' {win} ORDER BY sessions DESC LIMIT 10"),
        "orders-channel": ("Orders by sales channel", f"FROM sales SHOW orders, net_sales GROUP BY sales_channel {win}"),
        "homepage": ("Homepage entries by device", f"FROM sessions SHOW sessions, bounce_rate, average_session_duration, pageviews_per_session GROUP BY session_device_type WHERE landing_page_path = '/' {win}"),
        "homepage-source": ("Homepage entries by source", f"FROM sessions SHOW sessions, bounce_rate GROUP BY referrer_source WHERE landing_page_path = '/' {win}"),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True, help="<shop>.myshopify.com")
    ap.add_argument("--check", action="store_true", help="show the shop and the CLI connection's scopes, then stop")
    ap.add_argument("--preset", choices=["check-data", "device-funnel", "landing", "sources", "social", "orders-channel", "homepage", "all"])
    ap.add_argument("--query", help="a ShopifyQL query (read-only)")
    ap.add_argument("--since", default="-28d")
    ap.add_argument("--until", default="-1d")
    ap.add_argument("--csv", action="store_true", help="print the device funnel as funnel.py --steps strings")
    a = ap.parse_args(join_dash_values(sys.argv[1:]))

    if a.check:
        d = run_graphql(a.store, "{ shop { name myshopifyDomain ianaTimezone currencyCode } currentAppInstallation { accessScopes { handle } } }")
        scopes = sorted(s["handle"] for s in d["currentAppInstallation"]["accessScopes"])
        print(f"Shop: {d['shop']['name']} ({d['shop']['myshopifyDomain']}), {d['shop']['ianaTimezone']}, {d['shop']['currencyCode']}")
        print("Scopes: " + ", ".join(scopes))
        missing = [s for s in ("read_reports", "read_orders") if s not in scopes]
        print("Analytics: " + ("ready" if not missing else "missing " + ", ".join(missing) + " (the person grants it, not this script)"))
        writes = [s for s in scopes if s.startswith("write_")]
        if writes:
            print("Note: the connection also has " + ", ".join(writes) + ". This audit never uses them.")
        return

    today, tz = store_today(a.store)
    since, until = resolve_date(a.since, today), resolve_date(a.until, today)
    if since > until:
        sys.exit(f"the window starts after it ends: {since} to {until}")
    win = f"SINCE {since} UNTIL {until}"
    if a.query:
        if re.search(r"UNTIL\s+-\d+d", a.query, re.I):
            print("Warning: a relative UNTIL (for example UNTIL -1d) can drop the last day. Prefer an absolute date.")
        cols, rows = shopifyql(a.store, a.query)
        table("Query", cols, rows, 100)
        return
    if not a.preset:
        sys.exit("give --check, --preset or --query")
    p = presets(win)
    names = list(p) if a.preset == "all" else ([a.preset] + (["social-landing"] if a.preset == "social" else []) + (["homepage-source"] if a.preset == "homepage" else []))
    print(f"Window: {since} to {until} (both days included, {tz}; asked for {a.since} to {a.until}). "
          "Source: Shopify Analytics via ShopifyQL, read-only.")
    for n in names:
        title, q = p[n]
        cols, rows = shopifyql(a.store, q)
        table(title, cols, rows, 40 if n == "check-data" else 25)
        if n == "device-funnel" and a.csv:
            print("\nfunnel.py steps by device (unknown-device rows are usually bots; leave them out):")
            for r in rows:
                if r.get("session_device_type") in (None, "other"):
                    continue
                print(f"  {r['session_device_type']}: \"Sessions={r['sessions']},Added to cart={r['sessions_with_cart_additions']},"
                      f"Reached checkout={r['sessions_that_reached_checkout']},Completed checkout={r['sessions_that_completed_checkout']}\"")

if __name__ == "__main__":
    main()
