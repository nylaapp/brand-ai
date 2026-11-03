#!/usr/bin/env python3
"""Normalize a product-review export (Judge.me, Yotpo, Loox, Stamped, Fera, or any
similar CSV) into one flat JSON shape the rest of the skill can cluster.

This only does the deterministic, repetitive part: finding the right columns under
whatever header names the export app used, cleaning the text, redacting reviewer
names, deduping exact repeats, and filtering out reviews too short to carry any
signal. It does NOT judge what a review means -- that's a reading task for the
model, not a parsing task for a script.

Usage:
    python3 parse_reviews.py <input.csv> --out <normalized.json>

No third-party packages: standard library only, so this runs anywhere Python 3 does.
"""

import argparse
import csv
import html
import json
import re
import sys
from datetime import datetime

# Known header spellings across the common Shopify review apps. Add a row here
# instead of writing per-app branches -- every app's column just needs to resolve
# to one of these canonical fields.
FIELD_ALIASES = {
    "rating": ["rating", "review rating", "score", "stars", "star_rating", "product rating"],
    "title": ["title", "review title", "headline", "summary"],
    "body": [
        "body", "review", "review body", "content", "comment", "review content",
        "review_content", "text", "review text", "description",
    ],
    "date": [
        "date", "created at", "created_at", "review date", "submitted at",
        "submitted_at", "published at", "timestamp",
    ],
    "product": [
        "product", "product title", "product_title", "product name", "item",
        "sku", "product handle",
    ],
    "reviewer": [
        "reviewer", "reviewer name", "author", "name", "customer", "customer name",
        "nickname", "reviewer_name",
    ],
    "verified": ["verified", "verified purchase", "verified_buyer", "verified buyer"],
    "media": ["photo", "photos", "image", "images", "video", "media", "has_photo", "has_media"],
    "id": ["id", "review id", "review_id", "order id"],
}

HTML_TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
STAR_RE = re.compile(r"^[★]+$")

DATE_FORMATS = [
    "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ", "%m/%d/%Y",
    "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y", "%Y-%m-%d %H:%M:%S",
]


def normalize_header(h):
    return re.sub(r"[\s_]+", " ", h.strip().lower())


def build_column_map(fieldnames):
    """Map each canonical field to the actual CSV column name, if present."""
    normalized = {normalize_header(f): f for f in fieldnames}
    column_map = {}
    for canonical, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                column_map[canonical] = normalized[alias]
                break
    return column_map


def clean_text(raw):
    if raw is None:
        return ""
    text = html.unescape(raw)
    text = HTML_TAG_RE.sub(" ", text)
    text = WHITESPACE_RE.sub(" ", text).strip()
    return text


def parse_rating(raw):
    if raw is None or raw == "":
        return None
    raw = raw.strip()
    if STAR_RE.match(raw):
        return len(raw)
    try:
        value = float(raw)
        return round(value)
    except ValueError:
        pass
    match = re.search(r"(\d+(\.\d+)?)", raw)
    if match:
        try:
            return round(float(match.group(1)))
        except ValueError:
            return None
    return None


def parse_date(raw):
    if not raw:
        return None, raw
    raw = raw.strip()
    # Judge.me exports "2025-02-04 18:03:27 UTC"; drop a trailing zone name.
    stripped = re.sub(r"\s+(UTC|GMT|Z)$", "", raw)
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(stripped, fmt).date().isoformat(), raw
        except ValueError:
            continue
    return None, raw


def redact_reviewer(raw):
    """Keep enough to disambiguate speakers in a transcript, not enough to identify
    them. A full name becomes a first name + last-initial; anything that doesn't
    look like a name (an email, a username) becomes 'a customer'."""
    if not raw:
        return "a customer"
    raw = raw.strip()
    if "@" in raw:
        return "a customer"
    parts = raw.split()
    if len(parts) == 0:
        return "a customer"
    if len(parts) == 1:
        return parts[0]
    return f"{parts[0]} {parts[-1][0]}."


def truthy(raw):
    if raw is None:
        return False
    return raw.strip().lower() in ("true", "yes", "1", "y", "verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv")
    parser.add_argument("--out", required=True, help="path to write normalized JSON")
    parser.add_argument(
        "--min-length", type=int, default=8,
        help="reviews with a body shorter than this (after cleaning) are excluded as low-signal",
    )
    args = parser.parse_args()

    with open(args.input_csv, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        if not reader.fieldnames:
            print("error: could not read a header row from this CSV", file=sys.stderr)
            sys.exit(1)
        column_map = build_column_map(reader.fieldnames)

        missing_core = [c for c in ("body",) if c not in column_map]
        if missing_core:
            print(
                f"error: couldn't find a review-text column among: {reader.fieldnames}. "
                "Tell me which column holds the review body and I'll re-run with a mapping.",
                file=sys.stderr,
            )
            sys.exit(2)

        rows = list(reader)

    reviews = []
    excluded_short = 0
    excluded_empty = 0
    seen_bodies = {}
    duplicates_dropped = 0
    unparsed_dates = 0

    for i, row in enumerate(rows):
        get = lambda field: row.get(column_map[field]) if field in column_map else None

        body = clean_text(get("body"))
        if not body:
            excluded_empty += 1
            continue
        if len(body) < args.min_length:
            excluded_short += 1
            continue

        dedupe_key = body.lower()
        if dedupe_key in seen_bodies:
            duplicates_dropped += 1
            continue
        seen_bodies[dedupe_key] = True

        iso_date, raw_date = parse_date(get("date"))
        if get("date") and iso_date is None:
            unparsed_dates += 1

        reviews.append({
            "id": get("id") or str(i),
            "rating": parse_rating(get("rating")),
            "title": clean_text(get("title")),
            "body": body,
            "date": iso_date or raw_date,
            "product": clean_text(get("product")) or None,
            "reviewer": redact_reviewer(get("reviewer")),
            "verified": truthy(get("verified")) if "verified" in column_map else None,
            "has_media": truthy(get("media")) if "media" in column_map else None,
        })

    rating_counts = {}
    for r in reviews:
        if r["rating"] is not None:
            rating_counts[r["rating"]] = rating_counts.get(r["rating"], 0) + 1

    dated = [r["date"] for r in reviews if r["date"]]
    output = {
        "reviews": reviews,
        "summary": {
            "columns_found": column_map,
            "columns_in_file": reader.fieldnames,
            "total_rows_in_file": len(rows),
            "included": len(reviews),
            "excluded_empty": excluded_empty,
            "excluded_too_short": excluded_short,
            "duplicates_dropped": duplicates_dropped,
            "unparsed_dates": unparsed_dates,
            "rating_distribution": rating_counts,
            "date_range": [min(dated), max(dated)] if dated else None,
        },
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    s = output["summary"]
    print(
        f"Parsed {s['total_rows_in_file']} rows -> {s['included']} usable reviews "
        f"({s['excluded_empty']} empty, {s['excluded_too_short']} too short, "
        f"{s['duplicates_dropped']} exact duplicates dropped).",
        file=sys.stderr,
    )
    if "rating" not in column_map:
        print("note: no rating column found -- can't segment by star rating.", file=sys.stderr)
    if "date" not in column_map:
        print("note: no date column found -- can't show trends over time.", file=sys.stderr)


if __name__ == "__main__":
    main()
