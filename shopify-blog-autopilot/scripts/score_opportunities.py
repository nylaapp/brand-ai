#!/usr/bin/env python3
"""Score blog opportunities and apply autopilot guardrails deterministically.

Usage:
  python score_opportunities.py --candidates C.json --profile brand-profile.yaml \
      --ledger ledger.json --existing existing-articles.json --today YYYY-MM-DD \
      --out decisions.json [--write-ledger]

Inputs
  candidates.json : list of candidate records (see references/scoring-rubric.md)
  brand-profile   : YAML (or JSON) profile from assets/brand-profile.template.yaml
  ledger.json     : autopilot ledger (created if missing)
  existing.json   : list of store articles INCLUDING hidden drafts:
                    [{title, handle, tags:[], created_at:"YYYY-MM-DD", published:bool}]

Output: decisions.json with every candidate labeled write / backlog / skip and the reasons.
--write-ledger merges backlog, skips and the run entry into the ledger, and adds each
'write' decision as a topic with status "pending" (set it to "drafted" after the writer
creates the article). Don't pass it on dry runs.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

WEIGHTS = {"demand": 0.25, "business_value": 0.25, "winnability": 0.20,
           "uniqueness": 0.15, "urgency": 0.15}
FAMILY = {  # trigger -> source family, for the multi-signal bonus
    "store_new_product": "store", "store_new_collection": "store", "store_restock": "store",
    "store_rising_product": "store", "store_conversion_gap": "store",
    "gsc_striking": "search", "gsc_decay": "search", "gsc_gap": "search",
    "voc": "voc", "competitor": "competitor", "trend": "trend",
    "occasion": "occasion", "periodic": "periodic", "manual": "manual", "ai_citation_gap": "search",
}
STOP = set("a an the and or for of to in on with your my our how what which why best vs is are do does can at by from guide".split())
INTENT_BUCKET = {"informational": "informational", "commercial": "commercial",
                 "transactional": "transactional", "post_purchase": "post_purchase_brand",
                 "brand": "post_purchase_brand"}


def load_any(path, default=None):
    if not path or not os.path.exists(path):
        return default
    with open(path) as f:
        text = f.read()
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError:
            sys.exit("PyYAML missing: pip install pyyaml --break-system-packages")
        return yaml.safe_load(text)
    return json.loads(text) if text.strip() else default


def d(s):
    if not s:
        return None
    return dt.date.fromisoformat(str(s)[:10])


def tokens(s):
    words = re.findall(r"[a-z0-9]+", (s or "").lower().replace("-", " "))
    out = set()
    for w in words:
        if w in STOP:
            continue
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.add(w)
    return out


def matches(keyword, title, handle=""):
    kw = tokens(keyword)
    if not kw:
        return False
    # Handles are concise, so containment there is a strong signal; titles are long,
    # so they need real overlap (Jaccard) to avoid one keyword matching every post that shares a single word.
    ht = tokens(handle)
    if ht and kw <= ht:
        return True
    tt = tokens(title)
    jac = len(kw & tt) / len(kw | tt) if (kw | tt) else 0
    return jac >= 0.67


def get(dct, path, default):
    cur = dct
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return default if cur is None else cur


def base_score(f):
    total = 0.0
    for k, w in WEIGHTS.items():
        v = f.get(k, 3)
        v = max(1, min(5, int(v)))
        total += w * v
    return round((total - 1) / 4 * 100, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--existing", default=None)
    ap.add_argument("--today", default=dt.date.today().isoformat())
    ap.add_argument("--out", required=True)
    ap.add_argument("--write-ledger", action="store_true")
    a = ap.parse_args()

    today = d(a.today)
    prof = load_any(a.profile, {}) or {}
    ledger = load_any(a.ledger, None) or {"runs": [], "topics": [], "backlog": [], "skips": [], "snapshots": {}}
    for k in ("runs", "topics", "backlog", "skips"):
        ledger.setdefault(k, [])
    ledger.setdefault("snapshots", {})
    existing = load_any(a.existing, []) or []
    cands = load_any(a.candidates, []) or []

    th_write = get(prof, "thresholds.write", 65)
    th_backlog = get(prof, "thresholds.backlog", 45)
    th_periodic = get(prof, "thresholds.periodic_min", 55)
    cap = get(prof, "limits.max_posts_per_week", 2)
    per_run = get(prof, "limits.max_posts_per_run", 1)
    cooldown = get(prof, "limits.cluster_cooldown_days", 21)
    expiry = get(prof, "limits.backlog_expiry_days", 60)
    max_gap = get(prof, "periodic.max_gap_days", 14)
    excluded = [x.lower() for x in get(prof, "brand.excluded_topics", [])]
    mix = get(prof, "content_mix", {}) or {}

    # ---- merge backlog from ledger (new candidates with the same id win) ----
    ids = {c.get("id") for c in cands}
    kept_backlog, expired = [], []
    for b in ledger["backlog"]:
        added = d(b.get("added_on")) or today
        if (today - added).days > expiry:
            expired.append(b)
            continue
        if b.get("id") in ids:
            continue
        c = dict(b)
        c["_from_backlog"] = True
        kept_backlog.append(c)
    cands = cands + kept_backlog

    # ---- weekly cap: ledger topics + autopilot-tagged articles in last 7 days ----
    week_start = today - dt.timedelta(days=6)
    used_handles = set()
    for t in ledger["topics"]:
        td = d(t.get("date"))
        if td and td >= week_start and t.get("status") in ("drafted", "pending", "html"):
            used_handles.add(t.get("handle") or t.get("id"))
    for art in existing:
        tags = [x.lower() for x in (art.get("tags") or [])]
        ad = d(art.get("created_at"))
        if "autopilot" in tags and ad and ad >= week_start:
            used_handles.add(art.get("handle"))
    used = len(used_handles)
    remaining = max(0, cap - used)
    slots = min(per_run, remaining)

    # ---- content mix over last 90 days ----
    recent = [t for t in ledger["topics"] if d(t.get("date")) and (today - d(t["date"])).days <= 90]
    mix_count = {}
    for t in recent:
        b = INTENT_BUCKET.get(t.get("intent", ""), None)
        if b:
            mix_count[b] = mix_count.get(b, 0) + 1
    n_recent = len(recent)

    post_dates = [d(t.get("date")) for t in ledger["topics"] if d(t.get("date"))]
    post_dates += [d(x.get("created_at")) for x in existing
                   if "autopilot" in [y.lower() for y in (x.get("tags") or [])] and d(x.get("created_at"))]
    last_post = max(post_dates) if post_dates else None
    gap_days = (today - last_post).days if last_post else None

    results = []
    for c in cands:
        reasons, decision = [], None
        f = c.get("factors", {}) or {}
        score = base_score(f)
        trig = c.get("triggers") or [c.get("trigger")]
        fams = {FAMILY.get(t, t) for t in trig if t}
        if len(fams) > 1:
            bonus = min(10, 5 * (len(fams) - 1))
            score += bonus
            reasons.append(f"+{bonus} multi-signal ({', '.join(sorted(fams))})")
        bucket = INTENT_BUCKET.get(c.get("intent", ""))
        if bucket and n_recent >= 3 and bucket in mix:
            share = mix_count.get(bucket, 0) / n_recent
            if share + 0.10 < float(mix[bucket]):
                score += 5
                reasons.append(f"+5 content-mix ({bucket} at {share:.0%} vs target {float(mix[bucket]):.0%})")
        score = round(min(100, score), 1)

        kw = c.get("primary_keyword", "")
        text = " ".join([kw, c.get("title_idea", ""), c.get("cluster", "")]).lower()
        deadline = d(c.get("deadline"))

        # hard gates
        hit = next((x for x in excluded if x and x in text), None)
        if hit:
            decision = "skip"; reasons.append(f"excluded topic '{hit}'")
        elif int(f.get("business_value", 3)) <= 1:
            decision = "skip"; reasons.append("no brand fit (business_value=1)")
        elif deadline and deadline <= today:
            decision = "skip"; reasons.append(f"deadline {deadline} already passed")

        if decision is None:
            for t in ledger["topics"]:
                td = d(t.get("date"))
                if td and (today - td).days <= 180 and matches(kw, t.get("primary_keyword", ""), t.get("handle", "")) \
                        and c.get("action", "new") == "new":
                    decision = "skip"; reasons.append(f"autopilot already covered '{t.get('primary_keyword')}' on {td}")
                    break

        if decision is None and c.get("action", "new") == "new":
            for art in existing:
                if not matches(kw, art.get("title", ""), art.get("handle", "")):
                    continue
                age = (today - d(art.get("created_at"))).days if d(art.get("created_at")) else 999
                if not art.get("published", True):
                    decision = "skip"; reasons.append(f"hidden draft already exists: /{art.get('handle')}")
                elif age < 90:
                    decision = "skip"; reasons.append(f"covered recently by /{art.get('handle')} ({age}d old) — cannibalization risk")
                else:
                    c["action"] = "refresh"; c["refresh_target"] = art.get("handle")
                    reasons.append(f"converted to REFRESH of /{art.get('handle')} ({age}d old) to avoid cannibalization")
                break

        if decision is None:
            for t in ledger["topics"]:
                td = d(t.get("date"))
                if td and t.get("cluster") and t.get("cluster") == c.get("cluster") and (today - td).days < cooldown:
                    until = td + dt.timedelta(days=cooldown)
                    if deadline and deadline < until + dt.timedelta(days=7):
                        reasons.append(f"cluster cooldown until {until} overridden: deadline {deadline}")
                    else:
                        decision = "backlog"; reasons.append(f"cluster '{c.get('cluster')}' cooling down until {until}")
                    break

        if decision is None:
            if score >= th_write:
                decision = "write"; reasons.append(f"score {score} ≥ write threshold {th_write}")
            elif score >= th_backlog:
                decision = "backlog"; reasons.append(f"score {score} between {th_backlog} and {th_write}")
            else:
                decision = "skip"; reasons.append(f"score {score} < backlog threshold {th_backlog}")

        results.append({"id": c.get("id"), "decision": decision, "score": score,
                        "reasons": reasons, "candidate": c})

    # ---- rank writes; apply per-run and weekly limits ----
    def prio(r):
        dl = d(r["candidate"].get("deadline"))
        urgent = 1 if dl and (dl - today).days <= 45 else 0
        return (-urgent, (dl - today).days if dl else 9999, -r["score"])

    writes = sorted([r for r in results if r["decision"] == "write"], key=prio)
    for i, r in enumerate(writes):
        if i >= slots:
            r["decision"] = "backlog"
            r["reasons"].append("weekly cap reached" if remaining == 0 or i >= remaining else
                                f"per-run limit ({per_run}) reached")

    # ---- periodic rule ----
    if slots > 0 and not any(r["decision"] == "write" for r in results) and \
            (gap_days is None or gap_days >= max_gap):
        pool = sorted([r for r in results if r["decision"] == "backlog" and r["score"] >= th_periodic
                       and not any("cooling down" in x for x in r["reasons"])], key=prio)
        if pool:
            pool[0]["decision"] = "write"
            pool[0]["reasons"].append(f"promoted by periodic rule (gap {gap_days if gap_days is not None else 'n/a'}d ≥ {max_gap}d)")

    final_writes = [r for r in results if r["decision"] == "write"]
    out = {
        "today": today.isoformat(),
        "cap": {"max_per_week": cap, "used_last_7_days": used, "remaining": max(0, remaining - len(final_writes)),
                "max_per_run": per_run, "window_start": week_start.isoformat()},
        "days_since_last_autopilot_post": gap_days,
        "expired_backlog": [b.get("id") for b in expired],
        "summary": {k: sum(1 for r in results if r["decision"] == k) for k in ("write", "backlog", "skip")},
        "decisions": sorted(results, key=lambda r: ({"write": 0, "backlog": 1, "skip": 2}[r["decision"]], -r["score"])),
    }
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=2, default=str)

    if a.write_ledger:
        new_backlog = []
        for r in results:
            if r["decision"] == "backlog":
                c = {k: v for k, v in r["candidate"].items() if not k.startswith("_")}
                c.setdefault("added_on", today.isoformat())
                c["last_score"] = r["score"]
                new_backlog.append(c)
        ledger["backlog"] = new_backlog
        for r in results:
            if r["decision"] == "skip" and not r["candidate"].get("_from_backlog"):
                ledger["skips"].append({"id": r["id"], "date": today.isoformat(), "reasons": r["reasons"],
                                        "primary_keyword": r["candidate"].get("primary_keyword")})
        ledger["skips"] = ledger["skips"][-200:]
        for r in final_writes:
            c = r["candidate"]
            ledger["topics"].append({"id": c.get("id"), "date": today.isoformat(), "status": "pending",
                                     "primary_keyword": c.get("primary_keyword"), "cluster": c.get("cluster"),
                                     "intent": c.get("intent"), "trigger": c.get("trigger"),
                                     "action": c.get("action", "new"), "refresh_target": c.get("refresh_target"),
                                     "handle": None, "article_id": None, "score": r["score"]})
        ledger["runs"].append({"date": today.isoformat(), "summary": out["summary"],
                               "written": [r["id"] for r in final_writes]})
        with open(a.ledger, "w") as fh:
            json.dump(ledger, fh, indent=2, default=str)

    print(json.dumps({"summary": out["summary"], "cap": out["cap"],
                      "write": [(r["id"], r["score"]) for r in final_writes]}, indent=2))


if __name__ == "__main__":
    main()
