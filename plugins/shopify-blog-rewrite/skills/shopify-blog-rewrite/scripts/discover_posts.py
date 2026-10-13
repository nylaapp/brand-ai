#!/usr/bin/env python3
"""List the blog articles on a site, newest first, so a series transfer can start from a tracker.

    python3 discover_posts.py <site-or-blog-url> --out articles.json [--max 500]

Looks, in order, at: the WordPress REST API, RSS/Atom feeds (including Shopify's /blogs/<handle>.atom), then
sitemaps (robots.txt, /sitemap.xml and the usual post sitemaps). Keeps only URLs that look like articles.
Reads public pages only, honours robots.txt, one request at a time with a short pause. Python 3 standard library.
Exit codes: 0 found articles, 2 bad input, 3 nothing found (use a browser tool to read the blog index instead).
Output: a JSON list of {url, title, date, category, found_by}. Titles and dates may be blank; the rewrite fills them in.
Dates from a sitemap are "last modified", not published: many sites regenerate them all at once, so do not trust
them for ordering. Read the real publish date from each article when it is fetched.
"""
import argparse, json, re, shutil, ssl, subprocess, sys, time, urllib.error, urllib.parse, urllib.request, urllib.robotparser
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (compatible; brand-ai-blog-transfer/1.0)"
SKIP_PATH = re.compile(r"/(tag|tags|category|categories|author|authors|page|search|cart|account|products?|collections?|"
                       r"pages?|locations?|wp-content|wp-json|feed|amp|cdn-cgi|wp-admin)(/|$)|\.(jpg|jpeg|png|gif|webp|svg|pdf|xml|css|js)$", re.I)
NS = {"a": "http://www.w3.org/2005/Atom", "s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
_last = [0.0]
_robots = {}


def _fetch_plain(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read(500_000).decode("utf-8", "replace")
    except urllib.error.URLError as e:
        return _curl(url) if isinstance(getattr(e, "reason", None), ssl.SSLError) else None
    except Exception:
        return None


def allowed(url):
    p = urllib.parse.urlsplit(url)
    base = f"{p.scheme}://{p.netloc}"
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
        txt = _fetch_plain(base + "/robots.txt")
        if txt is None:
            rp = None
        else:
            rp.parse(txt.splitlines())
        _robots[base] = rp
    rp = _robots[base]
    return True if rp is None else rp.can_fetch(UA, url)


def _curl(url):
    """Fallback when Python has no CA certificates (common with python.org builds on macOS): use the system curl,
    which has the system trust store. Certificate checks stay on; nothing is bypassed."""
    if not shutil.which("curl"):
        return None
    r = subprocess.run(["curl", "-sL", "-m", "20", "--max-filesize", "5000000", "-A", UA, url],
                       capture_output=True, timeout=30)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 and r.stdout else None


def get(url):
    if not allowed(url):
        return None
    wait = 0.4 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read(5_000_000).decode("utf-8", "replace")
    except urllib.error.URLError as e:
        if isinstance(getattr(e, "reason", None), ssl.SSLError):
            return _curl(url)
        return None
    except Exception:
        return None
    finally:
        _last[0] = time.time()


def looks_like_article(url, root):
    p = urllib.parse.urlsplit(url)
    if p.netloc.lower().removeprefix("www.") != root:
        return False
    path = p.path.rstrip("/")
    return bool(path) and not SKIP_PATH.search(p.path) and path.count("/") >= 1


def from_wordpress(base, root, cap):
    out = []
    for page in range(1, 11):
        txt = get(f"{base}/wp-json/wp/v2/posts?per_page=100&page={page}&_fields=link,title,date,categories")
        if not txt:
            break
        try:
            items = json.loads(txt)
        except ValueError:
            break
        if not isinstance(items, list) or not items:
            break
        for it in items:
            out.append({"url": it["link"], "title": re.sub(r"<[^>]+>", "", (it.get("title") or {}).get("rendered", "")),
                        "date": (it.get("date") or "")[:10], "category": "", "found_by": "wordpress-api"})
        if len(items) < 100 or len(out) >= cap:
            break
    return out


def from_feed(url, found_by="feed"):
    txt = get(url)
    if not txt or "<" not in txt[:200]:
        return []
    try:
        root = ET.fromstring(txt.encode("utf-8"))
    except ET.ParseError:
        return []
    out = []
    for e in root.findall(".//a:entry", NS):
        link = next((l.get("href") for l in e.findall("a:link", NS) if l.get("rel") in (None, "alternate")), None)
        if link:
            out.append({"url": link, "title": (e.findtext("a:title", "", NS) or "").strip(),
                        "date": (e.findtext("a:published", "", NS) or e.findtext("a:updated", "", NS) or "")[:10],
                        "category": "", "found_by": found_by})
    for it in root.findall(".//item"):
        link = (it.findtext("link") or "").strip()
        if link:
            out.append({"url": link, "title": (it.findtext("title") or "").strip(),
                        "date": _rss_date(it.findtext("pubDate") or ""), "category": (it.findtext("category") or "").strip(),
                        "found_by": found_by})
    return out


def _rss_date(s):
    from email.utils import parsedate_to_datetime
    try:
        return parsedate_to_datetime(s).date().isoformat()
    except Exception:
        return ""


def from_sitemaps(base, root, cap):
    maps = []
    robots = get(base + "/robots.txt") or ""
    maps += re.findall(r"(?im)^sitemap:\s*(\S+)", robots)
    maps += [base + p for p in ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml", "/post-sitemap.xml", "/sitemap_blogs_1.xml")]
    seen, out, queue = set(), [], list(dict.fromkeys(maps))
    while queue and len(seen) < 40 and len(out) < cap:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        txt = get(sm)
        if not txt:
            continue
        try:
            tree = ET.fromstring(txt.encode("utf-8"))
        except ET.ParseError:
            continue
        for s in tree.findall(".//s:sitemap/s:loc", NS):
            loc = (s.text or "").strip()
            if re.search(r"post|blog|article|news|journal|stories|posts", loc, re.I) or "wp-sitemap" in sm:
                queue.append(loc)
        for u in tree.findall(".//s:url", NS):
            loc = (u.findtext("s:loc", "", NS) or "").strip()
            if loc:
                out.append({"url": loc, "title": "", "date": (u.findtext("s:lastmod", "", NS) or "")[:10],
                            "category": "", "found_by": "sitemap"})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url"); ap.add_argument("--out", required=True); ap.add_argument("--max", type=int, default=500)
    a = ap.parse_args()
    p = urllib.parse.urlsplit(a.url if "//" in a.url else "https://" + a.url)
    if not p.netloc:
        print("not a URL", file=sys.stderr); return 2
    base = f"{p.scheme}://{p.netloc}"
    root = p.netloc.lower().removeprefix("www.")
    found = from_wordpress(base, root, a.max)
    if len(found) < 3:
        feeds = []
        html = get(a.url) or ""
        feeds += [urllib.parse.urljoin(a.url, h) for h in re.findall(
            r'<link[^>]+type=["\']application/(?:rss|atom)\+xml["\'][^>]*href=["\']([^"\']+)', html, re.I)]
        feeds += [base + x for x in ("/feed", "/feed/", "/rss", "/blog/feed", "/blog/rss.xml", "/news/feed", "/blogs/news.atom")]
        for f in dict.fromkeys(feeds):
            found += from_feed(f)
            if len(found) >= 3:
                break
    if len(found) < 3:
        found += from_sitemaps(base, root, a.max)
    seen, out = set(), []
    for it in found:
        key = re.sub(r"/+$", "", it["url"].split("#")[0].split("?")[0]).lower().replace("://www.", "://")
        if key in seen or not looks_like_article(it["url"], root):
            continue
        seen.add(key); out.append(it)
    # If most URLs sit under a blog-like folder (/blogs/x/, /blog/, /news/, /articles/ ...), keep only those:
    # that drops treatment, service and landing pages that the sitemap lists next to the posts.
    folder = lambda u: re.match(r"/((?:blogs?|news|articles?|journal|insights|stories|resources|learn)(?:/[^/]+)?)/[^/]+/?$",
                                urllib.parse.urlsplit(u).path, re.I)
    blogish = [i for i in out if folder(i["url"])]
    if len(blogish) >= 5:
        out = blogish
    for i in out:
        m = folder(i["url"])
        if m and not i["category"]:
            parts = m.group(1).split("/")
            i["category"] = parts[1] if len(parts) > 1 else ""
    out.sort(key=lambda i: i["date"] or "", reverse=True)
    out = out[:a.max]
    json.dump(out, open(a.out, "w"), indent=2, ensure_ascii=False)
    if not out:
        print("nothing found: the site may block scripts or render its blog with JavaScript; read the blog index with a browser tool", file=sys.stderr)
    print(f"{len(out)} article URL(s) -> {a.out} (via {', '.join(sorted({i['found_by'] for i in out})) or 'nothing'})")
    return 0 if out else 3


if __name__ == "__main__":
    sys.exit(main())
