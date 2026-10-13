#!/usr/bin/env python3
"""Progress tracker for a series (batch) transfer of blog articles, kept in a CSV so a run can stop and resume.

A transfer folder holds two files:
  transfer-tracker.csv   one row per source article, with its status and results
  transfer-config.json   the rewrite settings chosen once for the whole series

Commands (Python 3 standard library only; `python` on Windows):
  init     --dir D --site URL --urls-json FILE [--tier T --seo none|light --review MODE --batch-size N --target-blog H ...]
  queue    --dir D (--all | --newest N | --ids T001 T002 ...)     discovered -> queued
  next     --dir D [--n N]                                         take the next batch: queued -> in_progress
  set      --dir D ID [ID ...] --status S [--skip-reason R] [--field key=value ...]
  resume   --dir D                                                 in_progress -> queued (after an interrupted run)
  summary  --dir D [--json]
  validate --dir D
Exit codes: 0 ok, 1 problem found by validate, 2 bad input.
"""
import argparse, csv, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

FIELDS = ["id", "source_url", "source_title", "source_date", "category", "status", "skip_reason", "batch",
          "tier", "seo_tune_up", "target_blog", "handle", "new_title", "run_folder", "shopify_article_id",
          "preview_url", "overlap_pct", "claims_removed", "images_used", "images_flagged", "notes", "updated_at"]
STATUSES = ["discovered", "queued", "in_progress", "ready_for_review", "drafted", "needs_attention", "skipped"]
OPEN = {"discovered", "queued", "in_progress"}
CONFIG_KEYS = ["site", "ownership_confirmed", "tier", "seo_tune_up", "review_mode", "batch_size", "target_blog",
               "blog_map", "image_policy", "store", "created"]
REVIEW_MODES = ["review_each_batch", "draft_straight", "local_files_only"]
TIERS = ["match", "reword", "restructure", "reimagine"]


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm_url(u):
    p = urlsplit(u.strip())
    path = re.sub(r"/+$", "", p.path) or "/"
    return urlunsplit((p.scheme.lower() or "https", p.netloc.lower().removeprefix("www."), path, "", ""))


def paths(d):
    d = Path(d)
    return d / "transfer-tracker.csv", d / "transfer-config.json"


def read_rows(d):
    csv_path, _ = paths(d)
    if not csv_path.exists():
        sys.exit(f"no tracker in {d}: run init first")
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(d, rows):
    csv_path, _ = paths(d)
    tmp = csv_path.with_suffix(".csv.tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    os.replace(tmp, csv_path)  # atomic: a crash never leaves half a file


def read_config(d):
    _, cfg = paths(d)
    return json.loads(cfg.read_text(encoding="utf-8")) if cfg.exists() else {}


def counts(rows):
    c = {s: 0 for s in STATUSES}
    for r in rows:
        c[r["status"]] = c.get(r["status"], 0) + 1
    return c


def cmd_init(a):
    d = Path(a.dir); d.mkdir(parents=True, exist_ok=True)
    csv_path, cfg_path = paths(d)
    items = json.loads(Path(a.urls_json).read_text(encoding="utf-8"))
    rows = read_rows(d) if csv_path.exists() else []
    seen = {norm_url(r["source_url"]) for r in rows}
    n = len(rows)
    added = 0
    for it in items:
        url = it["url"] if isinstance(it, dict) else it
        key = norm_url(url)
        if key in seen:
            continue
        seen.add(key); n += 1; added += 1
        rows.append({"id": f"T{n:03d}", "source_url": url, "source_title": (it.get("title", "") if isinstance(it, dict) else ""),
                     "source_date": (it.get("date", "") if isinstance(it, dict) else ""),
                     "category": (it.get("category", "") if isinstance(it, dict) else ""),
                     "status": "discovered", "updated_at": now()})
    write_rows(d, rows)
    cfg = read_config(d)
    given = {"site": a.site, "ownership_confirmed": a.ownership, "tier": a.tier, "seo_tune_up": a.seo,
             "review_mode": a.review, "batch_size": a.batch_size, "target_blog": a.target_blog,
             "blog_map": a.blog_map, "image_policy": a.image_policy, "store": a.store}
    for k, v in given.items():
        if v not in (None, ""):
            cfg[k] = v
    cfg.setdefault("created", now())
    if cfg.get("tier") and cfg["tier"] not in TIERS:
        sys.exit(f"tier must be one of {TIERS}")
    if cfg.get("review_mode") and cfg["review_mode"] not in REVIEW_MODES:
        sys.exit(f"review must be one of {REVIEW_MODES}")
    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"tracker: {csv_path} ({added} new rows, {len(rows)} total); config: {cfg_path}")


def cmd_queue(a):
    rows = read_rows(a.dir)
    disc = [r for r in rows if r["status"] == "discovered"]
    if a.all:
        pick = disc
    elif a.newest:
        pick = sorted(disc, key=lambda r: r["source_date"] or "", reverse=True)[:a.newest]
    else:
        ids = set(a.ids or [])
        pick = [r for r in rows if r["id"] in ids and r["status"] in ("discovered", "skipped")]
    for r in pick:
        r.update(status="queued", skip_reason="", updated_at=now())
    write_rows(a.dir, rows)
    print(f"queued {len(pick)} article(s)")


def cmd_next(a):
    rows = read_rows(a.dir)
    cfg = read_config(a.dir)
    n = a.n or int(cfg.get("batch_size") or 10)
    if any(r["status"] == "in_progress" for r in rows):
        sys.exit("a batch is still in progress: finish it, or run `resume` if it was interrupted")
    batch_no = max([int(r["batch"]) for r in rows if r["batch"].isdigit()] or [0]) + 1
    todo = [r for r in rows if r["status"] == "queued"][:n]
    for r in todo:
        r.update(status="in_progress", batch=str(batch_no), tier=cfg.get("tier", ""),
                 seo_tune_up=cfg.get("seo_tune_up", ""), updated_at=now())
    write_rows(a.dir, rows)
    print(json.dumps({"batch": batch_no, "count": len(todo), "config": cfg,
                      "articles": [{"id": r["id"], "url": r["source_url"], "title": r["source_title"]} for r in todo]},
                     indent=2, ensure_ascii=False))


def cmd_set(a):
    if a.status and a.status not in STATUSES:
        sys.exit(f"status must be one of {STATUSES}")
    rows = read_rows(a.dir)
    hit = 0
    for r in rows:
        if r["id"] in a.ids:
            hit += 1
            if a.status:
                r["status"] = a.status
            if a.skip_reason is not None:
                r["skip_reason"] = a.skip_reason
            for kv in a.field or []:
                k, _, v = kv.partition("=")
                if k not in FIELDS or k in ("id", "source_url"):
                    sys.exit(f"cannot set field '{k}'")
                r[k] = v
            if r["status"] == "skipped" and not r["skip_reason"]:
                sys.exit(f"{r['id']}: a skipped row needs --skip-reason")
            r["updated_at"] = now()
    if hit != len(a.ids):
        sys.exit("unknown id in list")
    write_rows(a.dir, rows)
    print(f"updated {hit} row(s)")


def cmd_resume(a):
    rows = read_rows(a.dir)
    n = 0
    for r in rows:
        if r["status"] == "in_progress":
            r.update(status="queued", batch="", updated_at=now()); n += 1
    write_rows(a.dir, rows)
    print(f"{n} interrupted article(s) put back in the queue")
    cmd_summary(argparse.Namespace(dir=a.dir, json=False))


def cmd_summary(a):
    rows = read_rows(a.dir)
    c = counts(rows)
    done = c["drafted"] + c["ready_for_review"]
    batches = sorted({r["batch"] for r in rows if r["batch"].isdigit()}, key=int)
    out = {"total": len(rows), "counts": c, "batches_started": len(batches),
           "remaining_to_do": c["queued"] + c["in_progress"], "not_yet_chosen": c["discovered"],
           "done": done, "needs_attention": [r["id"] for r in rows if r["status"] == "needs_attention"]}
    if a.json:
        print(json.dumps(out, indent=2)); return
    print(f"{out['total']} articles · done {done} · to do {out['remaining_to_do']} · not chosen {c['discovered']} · "
          f"skipped {c['skipped']} · needs attention {c['needs_attention']} · batches started {len(batches)}")
    for s in STATUSES:
        if c[s]:
            print(f"  {s:17} {c[s]}")


def cmd_validate(a):
    rows = read_rows(a.dir); cfg = read_config(a.dir)
    problems = []
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        problems.append("duplicate ids")
    urls = [norm_url(r["source_url"]) for r in rows]
    if len(urls) != len(set(urls)):
        problems.append("duplicate source_url")
    for r in rows:
        if r["status"] not in STATUSES:
            problems.append(f"{r['id']}: unknown status {r['status']}")
        if r["status"] == "skipped" and not r["skip_reason"]:
            problems.append(f"{r['id']}: skipped without a reason")
        if r["status"] in ("ready_for_review", "drafted") and not r["run_folder"]:
            problems.append(f"{r['id']}: {r['status']} but no run_folder")
        if r["status"] == "drafted" and not (r["shopify_article_id"] or cfg.get("review_mode") == "local_files_only"):
            problems.append(f"{r['id']}: drafted but no shopify_article_id")
    for k in ("site", "tier", "review_mode", "batch_size"):
        if not cfg.get(k):
            problems.append(f"config is missing {k}")
    print("OK" if not problems else "\n".join(problems))
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("--dir", required=True); p.add_argument("--site", required=True)
    p.add_argument("--urls-json", required=True); p.add_argument("--tier"); p.add_argument("--seo", choices=["none", "light"])
    p.add_argument("--review"); p.add_argument("--batch-size", type=int); p.add_argument("--target-blog"); p.add_argument("--blog-map")
    p.add_argument("--image-policy"); p.add_argument("--store"); p.add_argument("--ownership")
    p = sub.add_parser("queue"); p.add_argument("--dir", required=True)
    g = p.add_mutually_exclusive_group(required=True); g.add_argument("--all", action="store_true")
    g.add_argument("--newest", type=int); g.add_argument("--ids", nargs="+")
    p = sub.add_parser("next"); p.add_argument("--dir", required=True); p.add_argument("--n", type=int)
    p = sub.add_parser("set"); p.add_argument("--dir", required=True); p.add_argument("ids", nargs="+")
    p.add_argument("--status"); p.add_argument("--skip-reason"); p.add_argument("--field", action="append")
    p = sub.add_parser("resume"); p.add_argument("--dir", required=True)
    p = sub.add_parser("summary"); p.add_argument("--dir", required=True); p.add_argument("--json", action="store_true")
    p = sub.add_parser("validate"); p.add_argument("--dir", required=True)
    a = ap.parse_args()
    fn = {"init": cmd_init, "queue": cmd_queue, "next": cmd_next, "set": cmd_set, "resume": cmd_resume,
          "summary": cmd_summary, "validate": cmd_validate}[a.cmd]
    sys.exit(fn(a) or 0)


if __name__ == "__main__":
    main()
