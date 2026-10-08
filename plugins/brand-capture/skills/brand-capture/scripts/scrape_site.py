#!/usr/bin/env python3
"""Scrape a brand's public website into one JSON file that brand-capture turns into BRAND.md.

Standard library only, so it runs the same in Claude (desktop, Code, claude.ai) and Codex.

    python scrape_site.py https://example.com --out brand-scrape.json [--evidence <dir>] [--repo .]

What it collects (each part is best effort; failures are recorded under "errors", never fatal):
  site      platform (Shopify online store, headless Shopify, other), language, currency, country
  home      title, meta description, social preview, logo (and how it was found), navigation
  pages     story pages (About, Our story, Mission, Values, Founder), context pages (careers, press,
            why-us, consultations), one FAQ, the best locations page, the contact page and up to two
            company-news posts (expansions, partnerships), as clean text with headings. Each page
            carries its kind and whether it renders on the server or only in a browser
  products  full catalog from /products.json on Shopify online stores; otherwise a spread sample
            of product pages read through their structured data. Types, prices, colors, options, tags
  visual    colors and fonts from the site's CSS (custom properties, frequency, @font-face,
            Google Fonts), theme-color, fonts under a TRIAL or DEMO licence
  blog      every blog and article found, plus a measured sample of recent posts (body length from
            the byline to the disclaimer, disclaimer length, headings, images, byline, date, links)
  social    social profile links; Organization / LocalBusiness data and locations
  signals   regulated-category signals and disclaimer sentences found on the site
  evidence  (with --evidence, default: next to --out) every fetched page's full text with URL, date
            and sha256, plus manifest.json, so quotes can be checked and drift detected later
  repo      (with --repo) brand or design docs already in the repo, Shopify theme settings, the state
            of an existing BRAND.md, open requests and questions, and files that mention the brand
  warnings  things the reader must act on first (pages that only render in a browser)

It reads public pages only, honours robots.txt, waits between requests and stops at fixed caps.
"""
import argparse
import datetime as dt
import email.utils
import gzip
import hashlib
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCHEMA_VERSION = "1.1"
TOOL = "brand-capture/scrape_site.py 1.2.0"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 brand-capture/1.2.0"
MAX_REQUESTS = 160
TEXT_CAP = 5000

STORY_WORDS = ["about", "our-story", "story", "mission", "values", "who-we-are", "founder", "founders",
               "philosophy", "ethos", "manifesto", "purpose", "our-promise", "why-us", "sustainability",
               "impact", "heritage", "team", "people", "commitment"]
STORY_TEXT = re.compile(r"\b(about|our story|story|mission|values|who we are|founders?|philosophy|ethos|"
                        r"manifesto|purpose|our promise|why us|sustainability|heritage|our team)\b", re.I)
FAQ_WORDS = ["faq", "faqs", "frequently-asked-questions", "help"]
CONTEXT_WORDS = ["careers", "jobs", "join-us", "join-our-team", "work-with-us", "press", "newsroom",
                 "in-the-news", "why-us", "why-choose-us", "difference", "our-approach", "consultation",
                 "consultations"]
CONTEXT_TEXT = re.compile(r"\b(careers?|jobs|join (?:us|our team)|press|newsroom|in the news|why (?:us|choose)|"
                          r"the [\w-]+ difference|our approach|consultations?)\b", re.I)
PLACE_RANK = [("locations", 0), ("location", 0), ("store-locator", 0), ("find-a-store", 0), ("our-clinics", 0),
              ("stores", 1), ("visit-us", 1), ("contact", 2)]
# Company-news slugs, by how much they tend to say about the business. Plain "open" is left out on purpose:
# on real sites it mostly means events ("open house") or unrelated copy ("open your skincare packages").
NEWS_HINTS = [(3, re.compile(r"expand|acquir|merg|unites?\b|now-part-of", re.I)),
              (2, re.compile(r"partner(?!s?-card)|welcome|announc|joins\b|joining|mission|new-ceo|leadership", re.I)),
              (1, re.compile(r"anniversary|milestone|grand-opening|now-open|opens-|new-location", re.I))]


def news_score(slug):
    return max((score for score, rx in NEWS_HINTS if rx.search(slug)), default=0)
ARTICLE = re.compile(r"/(blogs/[^/]+|blog|journal|news|press|articles|stories)/[^/]+$")
# Pages that hold service terms, offers and the legal name. The reading checklist needs them, and on real sites
# they hold the facts that disagree (stores that moved, financing partners, the legal entity).
SERVICE_WORDS = ["custom", "bespoke", "made-to-order", "appointment", "appointments", "book-an-appointment",
                 "services", "repairs", "engraving", "personalization", "personalisation"]
OFFER_WORDS = ["financing", "finance", "payments", "payment-options", "klarna", "affirm", "afterpay", "bread",
               "loyalty", "rewards", "membership", "memberships", "vip", "referral", "refer-a-friend"]
POLICY_WORDS = ["returns", "shipping", "exchanges", "warranty", "guarantee"]
LEGAL_WORDS = ["terms", "terms-of-service", "terms-and-conditions", "terms-of-use", "legal", "imprint", "impressum"]
SERVICE_TEXT = re.compile(r"\b(custom|bespoke|made to order|book an appointment|appointments?|services|repairs|"
                          r"engraving)\b", re.I)
OFFER_TEXT = re.compile(r"\b(financing|payment options|pay over time|klarna|affirm|afterpay|loyalty|rewards|"
                        r"membership|vip|refer a friend)\b", re.I)
POLICY_TEXT = re.compile(r"\b(shipping|returns|exchanges|warranty|guarantee)\b", re.I)
LEGAL_TEXT = re.compile(r"\b(terms(?: of (?:service|use))?|terms (?:and|&) conditions|legal|imprint)\b", re.I)
STORE_SLUG = re.compile(r"(^|[-/])(stores?|showrooms?|boutiques?|flagship)(-|/|$)")
STOCKIST_SLUG = re.compile(r"(^|[-/])(stockists?|retailers|where-to-buy)(-|/|$)")  # other shops: after own stores
STORE_TEXT = re.compile(r"\b(stores?|showrooms?|stockists?|boutiques?)\b", re.I)
# Bot checks and challenge pages: an HTTP 200 that holds no content. Titles are a strong signal on their own;
# challenge markup only counts when the page has almost no text (Cloudflare injects scripts into normal pages too).
BOT_TITLE = re.compile(r"^(client challenge|just a moment|attention required|security checkpoint|"
                       r"vercel security checkpoint|access denied|pardon our interruption|are you a robot|"
                       r"please verify you are a human|one more step|request rejected)\b", re.I)
BOT_TEXT = re.compile(r"verif(?:y|ying) (?:that )?you are (?:a )?human|checking (?:your browser|if the site connection)|"
                      r"verifying your browser|enable javascript and cookies to continue|cf-chl-|px-captcha|"
                      r"captcha-delivery\.com|vercel-challenge", re.I)
# Product wording that makes a claim someone must be able to back up (materials, origin, sourcing, safety).
CLAIM_TERMS = re.compile(r"\b(recycled|reclaimed|conflict[- ]free|ethical(?:ly)?|responsibl[ey]|sustainab\w*|"
                         r"made in|hand[- ]?made|hand[- ]?crafted|hypoallergenic|nickel[- ]free|lifetime|"
                         r"warrant(?:y|ied)|guarantee[ds]?|certified|certification|organic|vegan|cruelty[- ]free|"
                         r"clinically|dermatologist|non[- ]toxic|lab[- ](?:grown|created)|solid (?:gold|silver)|"
                         r"vermeil|gold[- ](?:plated|filled)|fair[- ]?trade|b corp|fda)\b", re.I)
JUNK = re.compile(r"(^|[-_/])(void|test|copy|old|draft|backup|temp|tmp|zz)([-_]|$)", re.I)  # e.g. careers-v2-void
SOCIAL_HOSTS = {"instagram.com": "instagram", "facebook.com": "facebook", "tiktok.com": "tiktok",
                "youtube.com": "youtube", "pinterest.com": "pinterest", "linkedin.com": "linkedin",
                "twitter.com": "x", "x.com": "x", "threads.net": "threads", "snapchat.com": "snapchat"}
REGULATED = {
    "medical / medical aesthetics": ["fda", "physician*", "medical", "clinical", "clinic*", "dermatolog*", "injectable*",
                                     "botox", "filler*", "laser*", "prescription*", "patient*", "surgeon*",
                                     "nurse practitioner*", "board-certified", "medspa", "med spa"],
    "dietary supplements": ["supplement*", "vitamin*", "dietary", "capsule*", "gummies", "probiotic*"],
    "cosmetics / skincare claims": ["anti-aging", "anti-ageing", "acne", "spf", "sunscreen*", "retinol", "wrinkle*",
                                    "hyperpigmentation", "eczema", "rosacea", "clinically proven"],
    "cannabis / CBD": ["cbd", "thc", "cannabis", "cannabinoid*"],
    "alcohol / tobacco / vape": ["wine*", "spirits", "whiskey", "vape*", "nicotine", "tobacco"],
    "financial services": ["financing", "apr", "credit check*", "loan*", "interest rate*"],
}
DISCLAIMER = re.compile(r"[^.!?\n]{0,200}\b(disclaimer|not intended to (?:diagnose|treat|cure|prevent)|"
                        r"consult (?:your|a|with your|with a) (?:doctor|physician|healthcare|medical|provider)|"
                        r"results (?:may )?vary|individual results|not (?:medical|financial) advice|"
                        r"has not been evaluated by the food and drug administration|fda[- ](?:approved|cleared))"
                        r"[^.!?\n]{0,240}[.!?]?", re.I)
COLOR_WORDS = re.compile(r"colou?r|shade|tone|finish|tint|hue", re.I)
VISIBLE_DATE = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December|"
                          r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.? \d{1,2},? \d{4}\b")
BYLINE = re.compile(r"\b[Bb]y\s+([A-Z][\w.&'’-]*(?:\s+[A-Z][\w.&'’-]*){0,4})")


def find_disclaimers(texts):
    """Disclaimer-like sentences; a bare "Disclaimer:" label is joined to the sentence that follows it."""
    out, keys = [], set()
    for t in texts:
        flat = re.sub(r"\s+", " ", t or "")
        for m in DISCLAIMER.finditer(flat):
            kw = m.start(1)
            if m.group(1).lower() == "disclaimer":  # start at the label, and keep the sentence after a bare "Disclaimer:"
                parts = re.split(r"(?<=[.!?])\s", flat[kw:kw + 500].strip(), maxsplit=2)
                s = " ".join(parts[:2]) if len(parts[0]) < 40 else parts[0]
            else:
                s = m.group(0).strip()
            key = re.sub(r"\W+", "", flat[kw:kw + 160].lower())  # same wording from the keyword on = same disclaimer
            if key not in keys:
                keys.add(key)
                out.append(s[:400])
    return out[:12]


# ---------------------------------------------------------------- fetching

def retry_after_seconds(value, cap=30, default=5):
    """Seconds to wait from a Retry-After header (seconds or an HTTP date), capped."""
    if not value:
        return default
    value = value.strip()
    if value.isdigit():
        return min(int(value), cap)
    try:
        when = email.utils.parsedate_to_datetime(value)
        return max(0, min((when - dt.datetime.now(when.tzinfo)).total_seconds(), cap))
    except (TypeError, ValueError):
        return default


class Fetcher:
    def __init__(self, base, delay, max_requests=MAX_REQUESTS):
        self.base = base
        self.delay = delay
        self.max_requests = max_requests
        self.count = 0
        self.errors = []
        self.robots = urllib.robotparser.RobotFileParser()
        try:
            status, _, _, text = self._get(urllib.parse.urljoin(base, "/robots.txt"), check_robots=False)
            self.robots.parse(text.splitlines() if status == 200 else [])
            self.robots_text = text if status == 200 else ""
        except Exception:
            self.robots.parse([])
            self.robots_text = ""

    def _get(self, url, check_robots=True, binary=False, retried=False):
        if self.count >= self.max_requests:
            raise RuntimeError("request cap reached")
        if check_robots and not self.robots.can_fetch("*", url):
            raise PermissionError("disallowed by robots.txt")
        self.count += 1
        if self.count > 1:
            time.sleep(self.delay)
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip",
                                                   "Accept": "text/html,application/xhtml+xml,application/json,*/*"})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                raw = r.read(4_000_000)
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                ctype = r.headers.get("Content-Type", "")
                status, final = r.status, r.geturl()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and not retried:  # rate-limited or busy: wait as asked (max 30 s), retry once
                time.sleep(retry_after_seconds(e.headers.get("Retry-After") if e.headers else None))
                return self._get(url, check_robots=False, binary=binary, retried=True)
            return e.code, url, e.headers.get("Content-Type", "") if e.headers else "", ""
        if binary:
            return status, final, ctype, raw
        charset = "utf-8"
        m = re.search(r"charset=([\w-]+)", ctype)
        if m:
            charset = m.group(1)
        return status, final, ctype, raw.decode(charset, errors="replace")

    def get(self, url, what=""):
        """Return text or None, recording failures."""
        try:
            status, final, ctype, text = self._get(url)
            if status != 200:
                self.errors.append({"url": url, "what": what, "error": f"HTTP {status}"})
                return None
            return text
        except Exception as e:  # network, robots, cap
            self.errors.append({"url": url, "what": what, "error": str(e)[:160]})
            return None

    def get_json(self, url, what=""):
        text = self.get(url, what)
        if not text:
            return None
        try:
            return json.loads(text)
        except ValueError:
            self.errors.append({"url": url, "what": what, "error": "not JSON"})
            return None


# ---------------------------------------------------------------- HTML parsing

class Page(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "template", "iframe"}
    REGION = {"header": "header", "nav": "nav", "footer": "footer"}
    ROLE = {"navigation": "nav", "banner": "header", "contentinfo": "footer"}
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "td", "th", "figcaption", "dd", "dt", "summary"}
    VOID = {"img", "br", "meta", "link", "input", "hr", "source", "wbr", "area", "base", "col", "embed", "param", "track"}
    CONTAINER = {"div", "section", "main", "article", "aside", "header", "footer", "nav", "ul", "ol", "table", "form", "figure"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.lang = ""
        self.metas = {}
        self.links = []
        self.anchors = []
        self.ld = []
        self.json_blobs = []
        self.styles = []
        self.imgs = []
        self.chunks = []           # (tag, text, region, in_article)
        self.order = []            # ("img"|"text", in_article) in document order
        self._stack = []           # (tag, region_pushed, article_pushed)
        self._skip = 0
        self._regions = []
        self._article = 0
        self._buf = []
        self._intitle = False
        self._ld_on = False
        self._json_on = False
        self._style_on = False
        self._a = None

    def region(self):
        return self._regions[-1] if self._regions else "main"

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]
        if tag == "meta":
            k = a.get("property") or a.get("name") or a.get("itemprop")
            if k and a.get("content") is not None:
                self.metas.setdefault(k.lower(), a["content"])
            return
        if tag == "link":
            self.links.append(a)
            return
        if tag == "img":
            if not self._skip:
                self.imgs.append({"src": a.get("src") or a.get("data-src") or "", "alt": a.get("alt"),
                                  "cls": a.get("class") or "", "region": self.region(), "article": self._article > 0,
                                  "link": self._a["href"] if self._a else None,
                                  "link_label": self._a["label"] if self._a else ""})
                self.order.append(("img", self._article > 0))
            return
        if tag in self.VOID:
            return
        region_pushed = False
        article_pushed = False
        if tag == "script":
            stype = (a.get("type") or "").lower()
            self._ld_on = stype == "application/ld+json"
            # framework data blobs (Next.js, Hydrogen, others) often carry the full product objects
            self._json_on = not self._ld_on and (stype == "application/json" or a.get("id") == "__NEXT_DATA__")
        if tag == "style":
            self._style_on = True
        if tag in self.SKIP:
            self._skip += 1
        if tag in self.CONTAINER:
            self._flush("div")  # text belongs to the region it was read in, not where the next block starts
        reg = self.REGION.get(tag) or self.ROLE.get((a.get("role") or "").lower())
        if reg:
            self._regions.append(reg)
            region_pushed = True
        if tag == "article" or (tag in ("div", "section", "main") and re.search(r"\b(rte|article__content|article-content|post-content|entry-content|blog-post)\b", a.get("class") or "")):
            self._article += 1
            article_pushed = True
        if tag in self.BLOCK:
            self._flush("div")
        if tag == "title":
            self._intitle = True
        if tag == "a":
            self._a = {"href": a.get("href") or "", "text": "", "region": self.region(),
                       "label": a.get("aria-label") or ""}
        self._stack.append((tag, region_pushed, article_pushed))

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        # pop to the matching tag (tolerates sloppy HTML)
        idx = None
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                idx = i
                break
        if idx is None:
            return
        while len(self._stack) > idx:
            t, reg, art = self._stack.pop()
            if t in self.BLOCK:
                self._flush(t)
            elif t in self.CONTAINER or reg or art:
                self._flush("div")
            if t in self.SKIP:
                self._skip = max(0, self._skip - 1)
            if t == "script":
                self._ld_on = False
                self._json_on = False
            if t == "style":
                self._style_on = False
            if reg and self._regions:
                self._regions.pop()
            if art:
                self._article = max(0, self._article - 1)
            if t == "title":
                self._intitle = False
            if t == "a" and self._a is not None:
                self._a["text"] = re.sub(r"\s+", " ", self._a["text"]).strip()
                self.anchors.append(self._a)
                self._a = None

    def handle_data(self, data):
        if self._ld_on:
            self.ld.append(data)
            return
        if self._json_on:
            self.json_blobs.append(data)
            return
        if self._style_on:
            self.styles.append(data)
            return
        if self._skip:
            return
        if self._intitle:
            self.title += data
            return
        if self._a is not None:
            self._a["text"] += data
        self._buf.append(data)

    def _flush(self, tag):
        text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        self._buf = []
        if text:
            self.chunks.append((tag, text, self.region(), self._article > 0))
            if len(text) > 40:
                self.order.append(("text", self._article > 0))

    def close(self):
        super().close()
        self._flush("div")


def parse(html):
    p = Page()
    try:
        p.feed(html)
        p.close()
    except Exception:
        pass
    return p


def ld_nodes(page):
    out = []

    def walk(x):
        if isinstance(x, list):
            for i in x:
                walk(i)
        elif isinstance(x, dict):
            if "@graph" in x:
                walk(x["@graph"])
            if "@type" in x:
                out.append(x)
    for raw in page.ld:
        try:
            walk(json.loads(raw.strip()))
        except ValueError:
            continue
    return out


def types_of(node):
    t = node.get("@type")
    return [t] if isinstance(t, str) else (t or [])


def main_text(page, article_only=False):
    chunks = [c for c in page.chunks if c[2] == "main"]
    if article_only:
        art = [c for c in chunks if c[3]]
        chunks = art or chunks
    lines = []
    for tag, text, _, _ in chunks:
        if tag in ("h1", "h2", "h3", "h4"):
            lines.append(f"{'#' * int(tag[1])} {text}")
        elif tag == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)
    out, seen = [], set()
    for ln in lines:  # drop repeated boilerplate lines
        if ln in seen:
            continue
        seen.add(ln)
        out.append(ln)
    return "\n".join(out)


# ---------------------------------------------------------------- URL helpers

def norm(url):
    u = urllib.parse.urlsplit(url)
    path = re.sub(r"/+$", "", u.path) or "/"
    return urllib.parse.urlunsplit((u.scheme, u.netloc.lower(), path, "", ""))


def same_site(url, base):
    h1 = urllib.parse.urlsplit(url).netloc.lower().removeprefix("www.")
    h2 = urllib.parse.urlsplit(base).netloc.lower().removeprefix("www.")
    return h1 == h2


def path_of(url):
    return urllib.parse.urlsplit(url).path.lower()


def slug_hit(url, words):
    segs = [s for s in path_of(url).split("/") if s]
    if not segs:
        return False
    last = segs[-1]
    return any(last == w or last.startswith(w + "-") or last.endswith("-" + w) for w in words)


def slug_has(url, words):
    """Like slug_hit, but a word may also sit in the middle of the last segment (a-list-loyalty-program)."""
    segs = [s for s in path_of(url).split("/") if s]
    return bool(segs) and any(re.search(r"(^|-)" + re.escape(w) + r"(-|$)", segs[-1]) for w in words)


def claim_sentences(text, limit=4):
    """Sentences that make a checkable claim (materials, origin, sourcing, safety), verbatim."""
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text or "").strip()):
        sent = sent.strip()
        if 15 <= len(sent) <= 300 and CLAIM_TERMS.search(sent) and sent not in out:
            out.append(sent)
            if len(out) >= limit:
                break
    return out


def bot_check(html, page):
    """The reason when a fetched page is a bot check or challenge instead of the real page, else None."""
    title = re.sub(r"\s+", " ", page.title or "").strip()
    if BOT_TITLE.match(title):
        return f'bot check page: "{title[:60]}"'
    words = sum(len(c[1].split()) for c in page.chunks)
    if words < 150 and BOT_TEXT.search(html or ""):
        return "bot check page (challenge markup, almost no text)"
    return None


def spread(items, n):
    if len(items) <= n:
        return list(items)
    step = len(items) / n
    return [items[int(i * step)] for i in range(n)]


# ---------------------------------------------------------------- sitemap and feeds

def strip_ns(tag):
    return tag.split("}", 1)[-1]


def read_sitemaps(f, base):
    urls, seen_maps = [], set()
    queue = []
    for line in (f.robots_text or "").splitlines():
        if line.lower().startswith("sitemap:"):
            queue.append(line.split(":", 1)[1].strip())
    queue.append(urllib.parse.urljoin(base, "/sitemap.xml"))
    while queue and len(seen_maps) < 30:
        sm = queue.pop(0)
        if sm in seen_maps or sm.endswith(".gz"):
            continue
        seen_maps.add(sm)
        text = f.get(sm, "sitemap")
        if not text:
            continue
        try:
            root = ET.fromstring(text.encode("utf-8"))
        except ET.ParseError:
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text)
            urls.extend(locs)
            continue
        kind = strip_ns(root.tag)
        for child in root:
            loc = next((c.text.strip() for c in child if strip_ns(c.tag) == "loc" and c.text), None)
            lastmod = next((c.text.strip() for c in child if strip_ns(c.tag) == "lastmod" and c.text), None)
            if not loc:
                continue
            if kind == "sitemapindex":
                queue.append(loc)
            else:
                urls.append((loc, lastmod))
    out, seen = [], set()
    for u in urls:
        loc, lastmod = u if isinstance(u, tuple) else (u, None)
        n = norm(loc)
        if n not in seen and same_site(n, base):
            seen.add(n)
            out.append((n, lastmod))
    return out[:6000], len(seen_maps)


def read_feed(text):
    """Parse an Atom or RSS feed into [{title, url, date, author, tags}]."""
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except ET.ParseError:
        return []
    items = []
    for el in root.iter():
        name = strip_ns(el.tag)
        if name not in ("entry", "item"):
            continue
        it = {"title": "", "url": "", "date": "", "author": "", "tags": []}
        for c in el:
            cn = strip_ns(c.tag)
            if cn == "title":
                it["title"] = (c.text or "").strip()
            elif cn == "link":
                it["url"] = c.get("href") or (c.text or "").strip() or it["url"]
            elif cn in ("published", "pubDate") or (cn == "updated" and not it["date"]):
                it["date"] = (c.text or "").strip()
            elif cn == "author":
                nm = next((g.text for g in c if strip_ns(g.tag) == "name"), None)
                it["author"] = (nm or c.text or "").strip()
            elif cn == "creator":
                it["author"] = (c.text or "").strip()
            elif cn == "category":
                term = c.get("term") or (c.text or "").strip()
                if term:
                    it["tags"].append(term)
        items.append(it)
    return items


# ---------------------------------------------------------------- CSS: colors and fonts

HEX = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b")
RGB = re.compile(r"rgba?\(\s*(\d{1,3})[\s,]+(\d{1,3})[\s,]+(\d{1,3})(?:\s*[,/]\s*([\d.]+%?))?\s*\)")
TRIPLET = re.compile(r"^\s*(\d{1,3})\s*,?\s+(\d{1,3})\s*,?\s+(\d{1,3})\s*$|^\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\s*$")
VAR = re.compile(r"(--[\w-]+)\s*:\s*([^;{}]+)")
FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;{}]+)", re.I)
FONT_FACE = re.compile(r"@font-face\s*{[^}]*?font-family\s*:\s*([^;}]+)", re.I | re.S)
GENERIC_FONTS = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif", "ui-serif",
                 "ui-monospace", "-apple-system", "blinkmacsystemfont", "inherit", "initial", "unset", "emoji",
                 "apple color emoji", "segoe ui emoji", "segoe ui symbol", "noto color emoji", "helvetica",
                 "arial", "segoe ui", "roboto", "helvetica neue", "times new roman", "courier new"}


def hex6(h):
    h = h.lower()
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    return "#" + h[:6]


def to_hex(r, g, b):
    r, g, b = (max(0, min(255, int(x))) for x in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def colors_in(value):
    out = []
    for m in HEX.finditer(value):
        if len(m.group(1)) == 8 and m.group(1)[6:].lower() == "00":
            continue
        out.append(hex6(m.group(1)))
    for m in RGB.finditer(value):
        alpha = m.group(4)
        if alpha and alpha.rstrip("%") in ("0", "0.0"):
            continue
        out.append(to_hex(m.group(1), m.group(2), m.group(3)))
    m = TRIPLET.match(value)
    if m:
        g = [x for x in m.groups() if x is not None]
        if all(0 <= int(x) <= 255 for x in g):
            out.append(to_hex(*g))
    return out


def first_family(value, var_map):
    v = value.strip()
    m = re.match(r"var\((--[\w-]+)", v)
    if m and m.group(1) in var_map:
        v = var_map[m.group(1)]
    for part in v.split(","):
        name = part.strip().strip("'\"").strip()
        if not name or name.startswith("var(") or name.lower() in GENERIC_FONTS:
            continue
        return name
    return None


def analyse_css(css_texts, google_links):
    color_count = Counter()
    var_colors = {}
    var_map = {}
    for css in css_texts:
        for name, value in VAR.findall(css):
            var_map.setdefault(name, value.strip())
            cs = colors_in(value)
            if cs:
                var_colors.setdefault(name, cs[0])
        for c in colors_in(css):
            color_count[c] += 1
    named_bonus = re.compile(r"primary|secondary|accent|brand|background|foreground|text|button|heading|link|surface", re.I)
    by_var = {}
    for name, c in var_colors.items():
        by_var.setdefault(c, []).append(name)
        if named_bonus.search(name):
            color_count[c] += 5
    fonts = Counter()
    for css in css_texts:
        for value in FONT_FAMILY.findall(css):
            f = first_family(value, var_map)
            if f:
                fonts[f] += 1
        for name, value in VAR.findall(css):
            if re.search(r"font", name, re.I) and not re.search(r"size|weight|style|scale|height|spacing|case", name, re.I):
                f = first_family(value, var_map)
                if f:
                    fonts[f] += 3
    faces = sorted({f.strip().strip("'\"") for css in css_texts for f in FONT_FACE.findall(css)})
    google = []
    for href in google_links:
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(href).query)
        for fam in q.get("family", []):
            google.append(fam.split(":")[0].replace("+", " "))
    font_vars = {k: v for k, v in var_map.items()
                 if re.search(r"font", k, re.I) and re.search(r"family", k, re.I)}
    return {
        "colors_ranked": [{"hex": c, "weight": n, "css_variables": by_var.get(c, [])[:6]}
                          for c, n in color_count.most_common(16)],
        "fonts_ranked": [{"family": f, "weight": n} for f, n in fonts.most_common(8)],
        "font_face_families": faces[:12],
        "google_fonts": sorted(set(google)),
        "font_variables": dict(list(font_vars.items())[:12]),
    }


# ---------------------------------------------------------------- sections

def scrape_home(f, base):
    html = f.get(base, "home")
    if not html:
        return None, None
    page = parse(html)
    return page, html


def detect_platform(f, base, html):
    shopify = bool(re.search(r"cdn\.shopify\.com|Shopify\.theme|shopify-section|myshopify\.com", html or "", re.I))
    meta = f.get_json(urllib.parse.urljoin(base, "/meta.json"), "shopify meta") if shopify else None
    products_ok = None
    if shopify:
        probe = f.get_json(urllib.parse.urljoin(base, "/products.json?limit=1"), "products.json probe")
        products_ok = bool(probe and "products" in probe)
    if shopify and products_ok:
        kind = "shopify (online store)"
    elif shopify:
        kind = "shopify (headless or restricted storefront)"
    elif re.search(r"__NEXT_DATA__|/_next/static", html or ""):
        kind = "next.js"
    elif re.search(r"wp-content|wordpress", html or "", re.I):
        kind = "wordpress"
    elif re.search(r"squarespace", html or "", re.I):
        kind = "squarespace"
    elif re.search(r"wix\.com|wixstatic", html or "", re.I):
        kind = "wix"
    elif re.search(r"webflow", html or "", re.I):
        kind = "webflow"
    else:
        kind = "unknown"
    return kind, meta, bool(products_ok)


def navigation(page, base):
    nav = {"header": [], "footer": []}
    for a in page.anchors:
        href = a["href"]
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        url = norm(urllib.parse.urljoin(base, href))
        text = a["text"] or a["label"]
        if not text or not same_site(url, base):
            continue
        bucket = "footer" if a["region"] == "footer" else ("header" if a["region"] in ("header", "nav") else None)
        if bucket and len(nav[bucket]) < 80 and (text, url) not in [(x["text"], x["url"]) for x in nav[bucket]]:
            nav[bucket].append({"text": text[:80], "url": url})
    return nav


def socials(page, base):
    out = {}
    for a in page.anchors + [{"href": l.get("href", "")} for l in page.links]:
        href = a.get("href") or ""
        host = urllib.parse.urlsplit(href).netloc.lower().removeprefix("www.")
        for h, name in SOCIAL_HOSTS.items():
            if host == h or host.endswith("." + h):
                if name not in out and "share" not in href and "intent" not in href:
                    out[name] = href.split("?")[0]
    return out


def place_rank(url, text=""):
    """0 for a locations index, 1 for stores or visit-us pages, 2 for contact; None otherwise."""
    path = path_of(url)
    if "/products/" in path or "/collections/" in path:
        return None
    hay = (path + " " + text).lower()
    ranks = [rank for word, rank in PLACE_RANK if word in hay]
    if STORE_SLUG.search(path) or STORE_TEXT.search(text):
        ranks.append(1)
    elif STOCKIST_SLUG.search(path):
        ranks.append(1.5)
    return min(ranks, default=None)


def pick_pages(urls, nav, base, max_story=6, max_context=4, max_news=2, max_places=3, max_services=3,
               max_offers=3):
    """Story pages, then context pages (careers, press, why-us, consultations), one FAQ, up to three location or
    store pages AND the contact page, service pages (custom, appointments), offer pages (financing, loyalty,
    returns), the terms page, and up to two company-news posts (expansions, partnerships, mission statements)."""
    story, context, faq, place = [], [], [], {}
    services, offers, policies, legal = [], [], [], []
    for item in nav["header"] + nav["footer"]:
        if STORY_TEXT.search(item["text"]):
            story.append((0, item["url"], item["text"]))
        elif CONTEXT_TEXT.search(item["text"]):
            context.append((0, item["url"], item["text"]))
        if re.search(r"\bfaqs?\b", item["text"], re.I):
            faq.insert(0, item["url"])
        if "/products/" not in path_of(item["url"]) and "/collections/" not in path_of(item["url"]):
            if LEGAL_TEXT.search(item["text"]):
                legal.append((0, item["url"], item["text"]))
            elif OFFER_TEXT.search(item["text"]):
                offers.append((0, item["url"], item["text"]))
            elif POLICY_TEXT.search(item["text"]):
                policies.append((0, item["url"], item["text"]))
            elif SERVICE_TEXT.search(item["text"]):
                services.append((0, item["url"], item["text"]))
        r = place_rank(item["url"], item["text"])
        if r is not None:
            place.setdefault(item["url"], r)
    news = []
    for u, lastmod in urls:
        p = path_of(u)
        if ARTICLE.search(p):
            score = news_score(p.rsplit("/", 1)[-1])
            if score:
                news.append((score, lastmod or "", u))
            continue
        if "/products/" in p or "/collections/" in p or JUNK.search(p.rsplit("/", 1)[-1]):
            continue
        if slug_hit(u, STORY_WORDS):
            story.append((1, u, ""))
        elif slug_hit(u, CONTEXT_WORDS):
            exact = p.rsplit("/", 1)[-1] in CONTEXT_WORDS  # careers before careers-sales-associate-new-york
            context.append((1 if exact else 2, u, ""))
        elif slug_hit(u, FAQ_WORDS):
            faq.append(u)
        elif slug_has(u, LEGAL_WORDS):
            legal.append((1, u, ""))
        elif slug_has(u, OFFER_WORDS):
            offers.append((1, u, ""))
        elif slug_has(u, POLICY_WORDS):
            policies.append((1, u, ""))
        elif slug_has(u, SERVICE_WORDS):
            services.append((1, u, ""))
        else:
            r = place_rank(u)
            if r is not None:
                place.setdefault(u, r)
    seen, picked = set(), []

    def take(kind, items, cap):
        n = 0
        for _, u, label in sorted(items, key=lambda x: x[0]):
            if n >= cap:
                break
            if u not in seen and same_site(u, base) and norm(u) != norm(base):
                seen.add(u)
                picked.append((kind, u, label))
                n += 1

    take("story", story, max_story)
    take("context", context, max_context)
    if faq:
        take("faq", [(0, faq[0], "")], 1)
    ranked = sorted(place.items(), key=lambda kv: kv[1])
    take("locations", [(0, u, "") for u, r in ranked if r < 2], max_places)
    take("contact", [(0, u, "") for u, r in ranked if r == 2][:1], 1)
    take("services", services, max_services)
    take("offers", offers, max_offers)
    take("policies", policies, 1)
    take("legal", legal, 1)
    news.sort(key=lambda x: (x[0], x[1]), reverse=True)  # strongest signal first, then the newest
    take("company_news", [(0, u, "") for _, _, u in news], max_news)
    return picked


SHELL_MARKERS = re.compile(r'id=["\'](__next|root|app|__nuxt|svelte)["\']|data-reactroot|ng-version|<app-root', re.I)


def render_mode(html, page):
    """'client-side' when the HTML is an app shell with almost no readable text anywhere; else 'server'.
    Counts the whole page, not just the main region: a server-rendered page with a short main section
    (a contact form, a store locator) still has its header and footer text, an app shell has nothing."""
    words = sum(len(c[1].split()) for c in page.chunks)
    scripts = len(re.findall(r"<script\b", html or "", re.I))
    if words < 120 and (SHELL_MARKERS.search(html or "") or scripts > 15):
        return "client-side"
    return "server"


def header_has_svg(html):
    m = re.search(r"<header\b.*?</header>", html or "", re.I | re.S)
    return bool(m and re.search(r"<svg\b", m.group(0), re.I))


def home_link_has_svg(html, base):
    """True when a link to the homepage inside the header draws an inline SVG: the usual way to embed a wordmark."""
    m = re.search(r"<header\b.*?</header>", html or "", re.I | re.S)
    if not m:
        return False
    for a in re.finditer(r"<a\b([^>]*)>(.*?)</a>", m.group(0), re.I | re.S):
        href = re.search(r"""href\s*=\s*["']([^"']*)""", a.group(1))
        label = re.search(r"""aria-label\s*=\s*["']([^"']*)""", a.group(1))
        if is_home_link(href.group(1) if href else None, label.group(1) if label else "", base) \
                and re.search(r"<svg\b", a.group(2), re.I):
            return True
    return False


class Evidence:
    """Saves each fetched page's readable text, with URL, date and sha256, for quote checks and verify mode."""

    def __init__(self, folder, today):
        self.dir = Path(folder) if folder else None
        self.today = today
        self.items = []
        self.names = set()
        if self.dir:
            self.dir.mkdir(parents=True, exist_ok=True)

    def add(self, url, kind, page, text=None, name=None):
        """Save the page's main text (or the given text). Returns the first 8 characters of its sha256."""
        if not self.dir:
            return None
        if text is None:
            text = "\n".join(c[1] for c in page.chunks if c[2] == "main")
        flat = re.sub(r"\s+", " ", text).strip()
        sha = hashlib.sha256(flat.encode("utf-8")).hexdigest()
        name = name or re.sub(r"[^a-z0-9]+", "-", path_of(url).lower()).strip("-") or "home"
        name = name[:80]
        stem, n = name, 2
        while name in self.names:  # two URLs with the same path slug must not overwrite each other
            name, n = f"{stem}-{n}", n + 1
        self.names.add(name)
        f = self.dir / f"{name}.txt"
        f.write_text(f"URL: {url}\nFetched: {self.today}\nSHA256: {sha}\n\n{text}\n", encoding="utf-8")
        self.items.append({"url": url, "kind": kind, "file": f.name, "sha256": sha, "words": len(flat.split())})
        return sha[:8]

    def save(self):
        if self.dir:
            (self.dir / "manifest.json").write_text(json.dumps(self.items, indent=1), encoding="utf-8")


def scrape_pages(f, picked, evidence=None):
    out = []
    for kind, url, label in picked:
        html = f.get(url, kind)
        if not html:
            continue
        p = parse(html)
        blocked = bot_check(html, p)
        if blocked:
            f.errors.append({"url": url, "what": kind, "error": blocked})
            continue
        text = main_text(p)
        item = {"kind": kind, "url": url, "nav_label": label, "title": p.title.strip(),
                "meta_description": p.metas.get("description", ""), "text": text[:TEXT_CAP],
                "words": len(text.split()), "render": render_mode(html, p)}
        if evidence:
            item["sha8"] = evidence.add(url, kind, p, text)
        out.append(item)
    return out


def product_from_json(p, base):
    variants = p.get("variants") or []
    prices = [float(v["price"]) for v in variants if v.get("price") not in (None, "")]
    options = {o.get("name"): o.get("values") for o in (p.get("options") or []) if o.get("name")}
    colors = []
    for name, vals in options.items():
        if COLOR_WORDS.search(name or ""):
            colors.extend(vals or [])
    body = re.sub(r"<[^>]+>", " ", p.get("body_html") or "")
    return {"title": p.get("title"), "url": urllib.parse.urljoin(base, "/products/" + (p.get("handle") or "")),
            "type": p.get("product_type") or "", "vendor": p.get("vendor") or "",
            "tags": p.get("tags") if isinstance(p.get("tags"), list) else [t.strip() for t in (p.get("tags") or "").split(",") if t.strip()],
            "price_min": min(prices) if prices else None, "price_max": max(prices) if prices else None,
            "options": options, "colors": colors,
            "description": re.sub(r"\s+", " ", body).strip()[:400], "claims": claim_sentences(body)}


def _amount(v):
    """Price from the many shapes storefront APIs use: "73.00", 73, {amount}, {value: [{amount}]}."""
    if isinstance(v, (int, float)):
        return float(v), None
    if isinstance(v, str):
        try:
            return float(v.replace(",", "")), None
        except ValueError:
            return None, None
    if isinstance(v, dict):
        if "amount" in v:
            a, _ = _amount(v["amount"])
            return a, v.get("currencyCode")
        for k in ("minVariantPrice", "value", "price"):
            if k in v:
                return _amount(v[k])
    if isinstance(v, list) and v:
        return _amount(v[0])
    return None, None


def raw_blob_products(page, limit=400):
    """Every product-shaped object inside the page's embedded framework JSON (headless Shopify and similar)."""
    found = []

    def walk(x, depth=0):
        if depth > 16 or len(found) >= limit:
            return
        if isinstance(x, dict):
            if (isinstance(x.get("handle"), str) and isinstance(x.get("title"), str)
                    and any(k in x for k in ("priceRange", "price", "minPrice", "variants", "productType"))):
                found.append(x)
            for v in x.values():
                walk(v, depth + 1)
        elif isinstance(x, list):
            for v in x[:400]:
                walk(v, depth + 1)
    for blob in page.json_blobs:
        try:
            walk(json.loads(blob))
        except ValueError:
            continue
    return found


def blob_products(page, base):
    out, seen = [], set()
    for x in raw_blob_products(page):
        if x["handle"] in seen:
            continue
        seen.add(x["handle"])
        out.append(normalise_blob(x, urllib.parse.urljoin(base, "/products/" + x["handle"])))
    return out


def product_from_blobs(page, url):
    handle = path_of(url).rstrip("/").rsplit("/", 1)[-1]
    found = raw_blob_products(page, limit=60)
    if not found:
        return None
    return normalise_blob(next((p for p in found if p.get("handle") == handle), found[0]), url)


def normalise_blob(x, url):
    price, currency = None, None
    for k in ("minPrice", "priceRange", "price"):
        if k in x:
            price, currency = _amount(x[k])
            if price is not None:
                break
    variants = x.get("variants") or []
    if isinstance(variants, dict):
        variants = variants.get("nodes") or [e.get("node", {}) for e in variants.get("edges", [])]
    vprices = [p for p in (_amount(v.get("price"))[0] for v in variants if isinstance(v, dict)) if p is not None]
    prices = vprices or ([price] if price is not None else [])
    options = {}
    for o in x.get("options") or []:
        if isinstance(o, dict) and o.get("name") and o["name"].lower() != "title":
            vals = o.get("values") or [v.get("name") for v in (o.get("optionValues") or []) if isinstance(v, dict)]
            options[o["name"]] = [v for v in vals if isinstance(v, str)]
    colors = [v for name, vals in options.items() if COLOR_WORDS.search(name) for v in vals]
    tags = x.get("tags") if isinstance(x.get("tags"), list) else []
    desc = x.get("description") or re.sub(r"<[^>]+>", " ", x.get("descriptionHtml") or "")
    return {"title": x.get("title"), "url": url, "type": x.get("productType") or "", "vendor": x.get("vendor") or "",
            "tags": [t for t in tags if isinstance(t, str)],
            "price_min": min(prices) if prices else None, "price_max": max(prices) if prices else None,
            "currency": currency, "options": options, "colors": colors,
            "description": re.sub(r"\s+", " ", desc).strip()[:400]}


def product_from_page(html, url):
    p = parse(html)
    prod = next((n for n in ld_nodes(p) if "Product" in types_of(n)), None)
    if not prod:
        blob = product_from_blobs(p, url)
        if blob:
            return blob
    if not prod and "product" not in (p.metas.get("og:type") or "").lower():
        return None
    prod = prod or {}
    offers = prod.get("offers") or {}
    offers = offers if isinstance(offers, list) else [offers]
    prices, currency = [], None
    for o in offers:
        for key in ("price", "lowPrice", "highPrice"):
            try:
                prices.append(float(str(o.get(key)).replace(",", "")))
            except (TypeError, ValueError):
                pass
        currency = currency or o.get("priceCurrency")
    if not prices and p.metas.get("product:price:amount"):
        try:
            prices.append(float(p.metas["product:price:amount"].replace(",", "")))
        except ValueError:
            pass
    currency = currency or p.metas.get("product:price:currency")
    color = prod.get("color")
    brand = prod.get("brand")
    if isinstance(brand, dict):
        brand = brand.get("name")
    desc = prod.get("description") or p.metas.get("og:description") or p.metas.get("description") or ""
    return {"title": prod.get("name") or p.metas.get("og:title") or p.title.strip(), "url": url,
            "type": prod.get("category") or "", "vendor": brand or "", "tags": [],
            "price_min": min(prices) if prices else None, "price_max": max(prices) if prices else None,
            "currency": currency, "options": {}, "colors": [color] if isinstance(color, str) else (color or []),
            "description": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", desc)).strip()[:400]}


def summarise_products(items, total_known, source):
    prices = [x["price_min"] for x in items if x.get("price_min") is not None]
    by_type = {}
    for x in items:
        t = x.get("type") or "(no type)"
        by_type.setdefault(t, []).append(x)
    types = []
    for t, xs in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
        ps = [x["price_min"] for x in xs if x.get("price_min") is not None]
        types.append({"type": t, "count": len(xs), "price_min": min(ps) if ps else None,
                      "price_max": max((x.get("price_max") or x["price_min"]) for x in xs if x.get("price_min") is not None) if ps else None,
                      "examples": [x["title"] for x in xs[:4]]})
    colors = Counter(c.strip() for x in items for c in (x.get("colors") or []) if isinstance(c, str) and c.strip())
    tags = Counter(t for x in items for t in (x.get("tags") or []))
    opts = Counter(o for x in items for o in (x.get("options") or {}).keys() if o and o.lower() != "title")
    vendors = Counter(x.get("vendor") for x in items if x.get("vendor"))
    claims = {}
    for x in items:
        for c in x.get("claims") or claim_sentences(x.get("description") or ""):
            claims.setdefault(c, []).append(x.get("url"))
    return {
        "source": source, "total_products": total_known, "analysed": len(items),
        "price": {"min": min(prices), "max": max(prices), "median": statistics.median(prices)} if prices else None,
        "currency": next((x.get("currency") for x in items if x.get("currency")), None),
        "types": types[:15], "colors": colors.most_common(25), "option_names": opts.most_common(10),
        "top_tags": tags.most_common(25), "vendors": vendors.most_common(8),
        "claims": [{"text": c, "products": len(us), "example": us[0]}
                   for c, us in sorted(claims.items(), key=lambda kv: -len(kv[1]))[:80]],
        "items": items[:60],
    }


def scrape_products(f, base, urls, shopify_json, max_products):
    if shopify_json:
        allp, page = [], 1
        while page <= 6:
            data = f.get_json(urllib.parse.urljoin(base, f"/products.json?limit=250&page={page}"), "products.json")
            batch = (data or {}).get("products") or []
            allp.extend(batch)
            if len(batch) < 250:
                break
            page += 1
        items = [product_from_json(p, base) for p in allp]
        return summarise_products(items, len(items), "/products.json (complete catalog)")
    product_urls = [u for u, _ in urls if re.search(r"/products?/[^/]+$", path_of(u))]
    items, seen = [], set()
    # Headless storefronts embed whole product lists in collection pages: a few pages can cover the catalog.
    col_urls = [u for u, _ in urls if re.search(r"/collections/[^/]+$", path_of(u))]
    # "all" first, then collections spread across the list, so one brand or category doesn't dominate
    first = [u for u in col_urls if u.endswith("/all")]
    col_urls = first + spread([u for u in col_urls if u not in first], 8 - len(first))
    for cu in col_urls:
        html = f.get(cu, "collection page")
        if not html:
            continue
        for item in blob_products(parse(html), base):
            if norm(item["url"]) not in seen:
                seen.add(norm(item["url"]))
                items.append(item)
    if len(items) >= min(40, len(product_urls)):
        src = f"embedded product data on {len(col_urls)} collection pages ({len(items)} products) of {len(product_urls)} in the sitemap"
        return summarise_products(items, len(product_urls), src)
    for u in spread([u for u in product_urls if norm(u) not in seen], max_products):
        html = f.get(u, "product page")
        if html:
            item = product_from_page(html, u)
            if item:
                items.append(item)
    src = f"structured data on {len(items)} of {len(product_urls)} product pages from the sitemap"
    return summarise_products(items, len(product_urls), src) if items else {"source": src, "total_products": len(product_urls), "analysed": 0}


def scrape_collections(f, base, urls, shopify_json):
    if shopify_json:
        data = f.get_json(urllib.parse.urljoin(base, "/collections.json?limit=250"), "collections.json")
        cols = (data or {}).get("collections") or []
        return [{"title": c.get("title"), "url": urllib.parse.urljoin(base, "/collections/" + c.get("handle", "")),
                 "products": c.get("products_count")} for c in cols][:80]
    return [{"title": path_of(u).rsplit("/", 1)[-1].replace("-", " "), "url": u}
            for u, _ in urls if re.search(r"/collections/[^/]+$", path_of(u))][:80]


def article_from_blobs(page):
    """Longest HTML body inside embedded framework JSON, with the object that holds it (headless blogs)."""
    best = (0, None, None)

    def walk(x, depth=0):
        nonlocal best
        if depth > 16:
            return
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(v, str) and len(v) > best[0] and len(v) > 600 and re.search(r"<(p|h2|h3|li)\b", v):
                    best = (len(v), v, x)
                else:
                    walk(v, depth + 1)
        elif isinstance(x, list):
            for v in x[:400]:
                walk(v, depth + 1)
    for blob in page.json_blobs:
        try:
            walk(json.loads(blob))
        except ValueError:
            continue
    return best[1], best[2]


def _name(v):
    if isinstance(v, list):
        v = v[0] if v else None
    if isinstance(v, dict):
        v = v.get("name") or v.get("displayName")
    return v if isinstance(v, str) else ""


STOP_HEADING = re.compile(r"^(related (posts|articles|reads)|you may also like|recent posts|more from|read next|"
                          r"share this|keep reading)", re.I)
DISCLAIMER_START = re.compile(r"^\s*disclaimer\b", re.I)


def split_body(chunks):
    """Body = after the title/byline/date block and before a related-posts block or the disclaimer.
    Returns (body_chunks, disclaimer_words). States: pre -> body -> (skip) -> disclaimer.
    Without an <h1> (an embedded article body, for example) the body starts at the first chunk."""
    out, disclaimer_words = [], 0
    state = "pre" if any(c[0] == "h1" for c in chunks) else "body"
    for c in chunks:
        tag, text = c[0], c[1]
        if state == "pre":
            if tag == "h1":
                state = "body"
            continue
        if DISCLAIMER_START.match(text) and state in ("body", "skip"):
            state = "disclaimer"
            disclaimer_words += len(re.sub(r"^\s*disclaimer:?\s*", "", text, flags=re.I).split())
            continue
        if state == "disclaimer":
            if tag in ("h2", "h3", "h4") or STOP_HEADING.match(text):
                break
            disclaimer_words += len(text.split())
            continue
        if state == "skip":
            continue
        if tag in ("h2", "h3", "h4") and STOP_HEADING.match(text):
            state = "skip"
            continue
        if len(text.split()) <= 12 and (BYLINE.search(text) or VISIBLE_DATE.search(text)) and not out:
            continue  # byline and date lines under the title
        out.append(c)
    return out, disclaimer_words


def body_words(chunks):
    return sum(len(c[1].split()) for c in chunks if c[0] != "h1")


def unique_chunks(chunks):
    """Drop exact repeats. Responsive sites often render the whole article twice (desktop and mobile copies),
    which doubles every count; a real post almost never repeats a block word for word."""
    seen, out = set(), []
    for c in chunks:
        key = (c[0], c[1])
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


def drop_shared(measured_chunks, min_posts=3):
    """Text blocks that repeat across sampled posts (page furniture: CTAs, sign-up bands).
    measured_chunks: one list of text strings per post. Returns the shared set."""
    if len(measured_chunks) < min_posts:
        return set()
    counts = Counter(t for texts in measured_chunks for t in set(texts) if len(t.split()) >= 4)
    return {t for t, n in counts.items() if n >= 2}


def measure_post(html, url, base, evidence=None):
    page = parse(html)
    nodes = ld_nodes(page)
    art = next((n for n in nodes if set(types_of(n)) & {"Article", "BlogPosting", "NewsArticle"}), {})
    p, holder = page, {}
    article_chunks = [c for c in p.chunks if c[2] == "main" and c[3]]
    in_art = article_chunks or [c for c in p.chunks if c[2] == "main"]
    method = "article" if article_chunks else "byline-to-disclaimer"
    if sum(len(c[1].split()) for c in in_art) < 150:
        body, holder = article_from_blobs(page)
        holder = holder or {}
        if body:  # measure the embedded article body instead of the near-empty server HTML
            p = parse("<article>" + body + "</article>")
            in_art = [c for c in p.chunks if c[3]]
            method = "embedded-article"
    text = main_text(p, article_only=True)
    body_chunks, disclaimer_words = split_body(unique_chunks(in_art))
    words = body_words(body_chunks)
    if evidence:
        evidence.add(url, "blog_post", p, text)
    imgs = [i for i in p.imgs if i["region"] == "main" and (i["article"] or not any(c[3] for c in p.chunks))]
    first = next((kind for kind, in_a in p.order if in_a), None) or next((kind for kind, _ in p.order), None)
    author = _name(art.get("author")) or _name(holder.get("author")) or _name(holder.get("authorV2"))
    links = [norm(urllib.parse.urljoin(base, a["href"])) for a in p.anchors if a["region"] == "main" and a["href"]]
    disclaimers = find_disclaimers([text])[:3]
    opening = re.sub(r"\s+", " ", text[:600])
    if not art.get("datePublished") and not page.metas.get("article:published_time") and not holder.get("publishedAt"):
        m = VISIBLE_DATE.search(opening)
        if m:
            art = dict(art, datePublished=m.group(0))
    if not author:
        m = BYLINE.search(opening)
        author = m.group(1).strip() if m else ""
        byline = bool(m)
    else:
        byline = False
    return {"url": url, "title": (art.get("headline") or page.metas.get("og:title") or page.title).strip(),
            "date": art.get("datePublished") or page.metas.get("article:published_time")
                    or holder.get("publishedAt") or holder.get("published_at") or "",
            "author": author or page.metas.get("author") or "", "_byline": byline,
            "words": words, "words_disclaimer": disclaimer_words, "words_method": method,
            "_texts": [c[1] for c in body_chunks],
            "h2": sum(1 for c in body_chunks if c[0] == "h2"), "h3": sum(1 for c in body_chunks if c[0] == "h3"),
            "h1_in_body": sum(1 for c in in_art if c[0] == "h1"),
            "images": len(imgs), "first_element": first,
            "lists": sum(1 for c in body_chunks if c[0] == "li") > 0,
            "tables": sum(1 for c in body_chunks if c[0] in ("td", "th")) > 0,
            "product_links": sum(1 for l in links if "/products/" in l),
            "collection_links": sum(1 for l in links if "/collections/" in l),
            "blog_links": sum(1 for l in links if "/blogs/" in l or "/blog/" in l),
            "external_links": sum(1 for l in links if not same_site(l, base)),
            "disclaimer_like_text": disclaimers,
            "opening": text[:500]}


def iso_date(text):
    """YYYY-MM-DD from an ISO timestamp or a visible date like "October 10, 2019"; None if unreadable."""
    t = (text or "").strip().replace(".", "")
    if re.match(r"\d{4}-\d{2}-\d{2}", t):
        return t[:10]
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%B %d %Y", "%b %d %Y"):
        try:
            return dt.datetime.strptime(t.replace("Sept ", "Sep "), fmt).date().isoformat()
        except ValueError:
            continue
    return None


FEED_PATHS = ["/feed", "/rss.xml", "/feed.xml", "/atom.xml", "/blog/rss.xml", "/blog/feed"]


def scrape_blog(f, base, urls, page, max_posts, evidence=None):
    art_re = re.compile(r"/(blogs/[^/]+|blog|journal|news|articles|stories|magazine)/[^/]+$")
    articles = [(u, lm) for u, lm in urls if art_re.search(path_of(u))]
    blogs = Counter()
    for u, _ in articles:
        parts = [s for s in path_of(u).split("/") if s]
        blogs["/".join(parts[:-1])] += 1
    feed_items = []
    feeds = [l.get("href") for l in page.links if "alternate" in (l.get("rel") or "") and
             re.search(r"rss|atom", l.get("type") or "")] if page else []
    for b in list(blogs)[:8]:
        if b.startswith("blogs/"):
            feeds.append("/" + b + ".atom")
    feeds_found = []
    for feed in dict.fromkeys(feeds):
        text = f.get(urllib.parse.urljoin(base, feed), "blog feed")
        if text:
            items = read_feed(text)
            if items:
                feeds_found.append(urllib.parse.urljoin(base, feed))
            for it in items:
                it["url"] = norm(urllib.parse.urljoin(base, it["url"])) if it["url"] else ""
                feed_items.append(it)
    if not feed_items and (blogs or not urls):
        # Non-Shopify blogs (WordPress, Webflow, others) publish feeds at common paths. The blog's own folder goes
        # first ("/blog/rss.xml" for a blog under /blog/), then the site-wide paths; at most 4 requests in all.
        own = [f"/{b}/{leaf}" for b, _ in blogs.most_common(1) if not b.startswith("blogs/")
               for leaf in ("rss.xml", "feed")]
        for path in list(dict.fromkeys(own + FEED_PATHS))[:4]:
            feed = urllib.parse.urljoin(base, path)
            text = f.get(feed, "blog feed (common path)")
            items = read_feed(text) if text else []
            if items:
                feeds_found.append(feed)
                for it in items:
                    it["url"] = norm(urllib.parse.urljoin(base, it["url"])) if it["url"] else ""
                    feed_items.append(it)
                break

    def sort_key(x):
        return x.get("date") or ""
    recent = sorted([i for i in feed_items if i["url"]], key=sort_key, reverse=True)
    sample_urls = [i["url"] for i in recent]
    if not sample_urls and blogs:
        # No feeds: a blog's index page lists its newest posts first, so take the top links from each blog.
        art_paths = {path_of(u) for u, _ in articles}
        per_blog = []
        for b, _ in blogs.most_common(6):
            html = f.get(urllib.parse.urljoin(base, "/" + b), "blog index")
            if not html:
                continue
            links = []
            for a in parse(html).anchors:
                u = norm(urllib.parse.urljoin(base, a["href"])) if a["href"] else ""
                if u and path_of(u) in art_paths and u not in links:
                    links.append(u)
            per_blog.append(links[:3])
        for rank in range(3):  # newest of each blog first, then second newest...
            sample_urls += [lst[rank] for lst in per_blog if len(lst) > rank and lst[rank] not in sample_urls]
    if len(sample_urls) < max_posts:
        # last resort: newest by sitemap lastmod, taking one post from each blog in turn so every blog is seen
        by_blog = {}
        for u, lm in sorted(articles, key=lambda x: x[1] or "", reverse=True):
            by_blog.setdefault("/".join([s for s in path_of(u).split("/") if s][:-1]), []).append(u)
        queues = sorted(by_blog.values(), key=len, reverse=True)
        while any(queues) and len(sample_urls) < max_posts * 3:
            for q in queues:
                if q:
                    u = q.pop(0)
                    if u not in sample_urls:
                        sample_urls.append(u)
    measured = []
    for u in sample_urls[:max_posts]:
        html = f.get(u, "blog post")
        if html:
            measured.append(measure_post(html, u, base, evidence))
    # text blocks repeated across posts are page furniture (CTAs, sign-up bands): take them out of the word counts
    shared = drop_shared([m["_texts"] for m in measured])
    for m in measured:
        m["words"] -= sum(len(t.split()) for t in set(m.pop("_texts")) if t in shared)
    # visible bylines run into the first word of the post ("by AYA Medical Spa Whether"): keep the shared part
    bylines = [m["author"].split() for m in measured if m.pop("_byline", False)]
    if len(bylines) >= 2:
        common = os.path.commonprefix(bylines)
        for m in measured:
            if common and m["author"].split()[:len(common)] == common:
                m["author"] = " ".join(common)
    words = [m["words"] for m in measured if m["words"]]
    authors = Counter(i["author"] for i in feed_items if i.get("author"))
    authors.update(m["author"] for m in measured if m.get("author"))
    tags = Counter(t for i in feed_items for t in i.get("tags", []))
    dates = sorted(i["date"][:10] for i in feed_items if i.get("date"))
    if not dates:  # no feeds: use the measured posts' own dates
        dates = sorted(d for d in (iso_date(m.get("date")) for m in measured) if d)
    return {
        "blogs": [{"path": "/" + b, "articles_in_sitemap": n} for b, n in blogs.most_common(20)],
        "articles_in_sitemap": len(articles),
        "feeds": feeds_found,
        "feed_articles": len(feed_items),
        "newest": dates[-1] if dates else None, "oldest_in_feeds": dates[0] if dates else None,
        "recent_titles": [{"title": i["title"], "date": i["date"][:10], "url": i["url"]} for i in recent[:15]],
        "authors": authors.most_common(6), "tags": tags.most_common(20),
        "sample": measured,
        "sample_words": {"min": min(words), "max": max(words), "median": statistics.median(words)} if words else None,
    }


def organisation(page, nodes):
    org = next((n for n in nodes if set(types_of(n)) & {"Organization", "Corporation", "Brand", "OnlineStore", "Store"}), None)
    local = [n for n in nodes if any(t.endswith("Business") or t in ("MedicalClinic", "HealthAndBeautyBusiness", "Store", "LocalBusiness", "MedicalBusiness", "DaySpa") for t in types_of(n))]
    def addr(n):
        a = n.get("address") or {}
        if isinstance(a, list):
            a = a[0] if a else {}
        if isinstance(a, str):
            return a
        return ", ".join(x for x in [a.get("streetAddress"), a.get("addressLocality"), a.get("addressRegion"), a.get("addressCountry") if isinstance(a.get("addressCountry"), str) else None] if x)
    out = {}
    if org:
        logo = org.get("logo")
        out["organization"] = {"name": org.get("name"), "description": org.get("description"),
                               "logo": logo.get("url") if isinstance(logo, dict) else logo,
                               "same_as": org.get("sameAs") if isinstance(org.get("sameAs"), list) else []}
    if local:
        out["local_business"] = [{"name": n.get("name"), "type": types_of(n), "address": addr(n)} for n in local[:30]]
    return out


ICON_HINT = re.compile(r"\b(icon|menu|hamburger|search|cart|bag|basket|account|user|profile|close|chevron|arrow|"
                       r"caret|wishlist|heart|globe|flag)\b", re.I)


def is_home_link(href, label, base):
    if re.search(r"\b(home|homepage|logo)\b", label or "", re.I):
        return True
    return bool(href) and norm(urllib.parse.urljoin(base, href)) == norm(base)


def logo_of(page, base, org_logo=None, header_svg=False, home_svg=False):
    """Return (logo, source). Order: Organization JSON-LD, <img> with 'logo' in src/alt/class (header first),
    the image inside the header's link to the homepage, an inline SVG in that link, an inline SVG anywhere in
    the header, and only then the first header image that isn't an icon (a guess: on real sites it is often a
    menu or product photo)."""
    if org_logo:
        return urllib.parse.urljoin(base, org_logo), "organization json-ld"
    imgs = sorted(page.imgs, key=lambda i: 0 if i["region"] in ("header", "nav") else 1)
    header = [i for i in imgs if i["region"] in ("header", "nav") and i["src"]]
    for i in imgs:
        if re.search(r"logo", (i["src"] or "") + " " + (i["alt"] or "") + " " + i["cls"], re.I):
            return urllib.parse.urljoin(base, i["src"]), "img with 'logo'"
    for i in header:
        if is_home_link(i.get("link"), i.get("link_label"), base) and not ICON_HINT.search(i["alt"] or ""):
            return urllib.parse.urljoin(base, i["src"]), "image in the header's home link"
    if home_svg:
        return ("inline SVG in the header's home link (no file URL; ask for the logo file or take it from the repo)",
                "svg in home link")
    if header_svg:
        return "inline SVG in the header (no file URL; ask for the logo file or take it from the repo)", "header svg"
    for i in header:
        if not ICON_HINT.search(" ".join([i["src"], i["alt"] or "", i["cls"]])):
            return urllib.parse.urljoin(base, i["src"]), "first header image (unverified guess)"
    return None, None


def signals(texts):
    blob = " ".join(texts).lower()
    scores = {}
    for cat, words in REGULATED.items():
        # whole words; a trailing * marks a stem ("dermatolog*" matches dermatologist, dermatology)
        hits = {}
        for w in words:
            stem = w.endswith("*")
            n = len(re.findall(r"(?<!\w)" + re.escape(w.rstrip("*")) + (r"\w*" if stem else r"(?!\w)"), blob))
            if n:
                hits[w.rstrip("*")] = n
        if hits:
            scores[cat] = {"total": sum(hits.values()), "terms": dict(sorted(hits.items(), key=lambda kv: -kv[1])[:8])}
    disclaimers = find_disclaimers(texts)
    return {"regulated_categories": dict(sorted(scores.items(), key=lambda kv: -kv[1]["total"])),
            "disclaimer_sentences": disclaimers[:12]}


SKIP_PARTS = {".git", "node_modules", "assets", ".artifact-work", "locales", "dist", "build"}
TEXT_SUFFIX = {".md", ".mjs", ".js", ".json", ".liquid", ".yml", ".yaml", ".txt"}


def brand_mentions(root, brand, limit=20, max_bytes=2_000_000):
    """Files in the repo that mention the brand name 3+ times: places where brand facts live outside BRAND.md.
    Skipped folders are pruned, not walked; dot-files (.env and the like) and large files are never read."""
    root = Path(root)
    if not brand or not root.is_dir():
        return []
    pat = re.compile(re.escape(brand), re.I)
    out = []
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_PARTS]  # .claude/skills stays in: skills hold brand defaults
        for name in files:
            p = Path(folder) / name
            if name.startswith(".") or p.suffix.lower() not in TEXT_SUFFIX or name.lower() in ("brand.md", "brand-voice.md"):
                continue
            try:
                if p.stat().st_size > max_bytes:
                    continue
                n = len(pat.findall(p.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                continue
            if n >= 3:
                out.append({"file": p.relative_to(root).as_posix(), "mentions": n})
    return sorted(out, key=lambda x: -x["mentions"])[:limit]


def brand_md_front(root):
    """Front matter of an existing BRAND.md (schema, revision, status, dates, voice_doc) for Step 0's mode choice."""
    p = Path(root) / "BRAND.md"
    if not p.is_file():   # a lowercase legacy brand.md is still read (new files are always written uppercase)
        p = Path(root) / "brand.md"
    if not p.is_file():
        return None
    text = p.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
    front = {}
    end = text.find("\n---\n", 4) if text.startswith("---\n") else -1
    if end != -1:
        for line in text[4:end].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                front[k.strip()] = v.strip()
    keep = ("brand", "brand_md_schema", "revision", "status", "captured", "last_updated", "captured_by", "voice_doc")
    out = {k: front.get(k, "") for k in keep}
    out["schema"] = front.get("brand_md_schema") or ("1.0" if front else "unknown")
    return out


def open_items(root):
    """Open lines in BRAND-REQUESTS.md and unanswered Q-ids in BRAND-QUESTIONS.md."""
    root = Path(root)
    req, qs = root / "BRAND-REQUESTS.md", root / "BRAND-QUESTIONS.md"
    requests_open = 0
    if req.is_file():
        requests_open = sum(1 for line in req.read_text(encoding="utf-8-sig", errors="replace").splitlines()
                            if line.lstrip().startswith("-") and line.rstrip().endswith("| open"))
    questions_open = []
    if qs.is_file():
        for block in re.split(r"\n(?=\*\*Q-\d{2,3}\b|#)", qs.read_text(encoding="utf-8-sig", errors="replace")):
            m = re.match(r"\*\*(Q-\d{2,3})\b", block.strip())
            if m and not re.search(r"\bAnswered\b", block):
                questions_open.append(m.group(1))
    return requests_open, questions_open


def scan_repo(root, brand=None):
    root = Path(root)
    out = {"path": str(root.resolve()), "docs": [], "shopify": {}}
    out["brand_md"] = brand_md_front(root)
    out["requests_open"], out["questions_open"] = open_items(root)
    out["brand_mentions"] = brand_mentions(root, brand)
    present = {p.name.lower(): p.name for p in root.iterdir() if p.is_file()} if root.is_dir() else {}
    for name in ["brand.md", "brand-voice.md", "design.md", "brand-guidelines.md", "brand-intake.md", "style-guide.md",
                 "readme.md", "agents.md", "claude.md"]:
        if name in present:
            out["docs"].append({"file": present[name], "bytes": (root / present[name]).stat().st_size})
    toml = root / "shopify.theme.toml"
    if toml.exists():
        m = re.search(r'store\s*=\s*"([^"]+)"', toml.read_text(errors="replace"))
        if m:
            out["shopify"]["store"] = m.group(1)
    schema = root / "config" / "settings_schema.json"
    if schema.exists():
        try:
            info = next((x for x in json.loads(schema.read_text(encoding="utf-8")) if x.get("name") == "theme_info"), {})
            out["shopify"]["theme"] = f'{info.get("theme_name", "")} {info.get("theme_version", "")}'.strip()
        except (ValueError, StopIteration, AttributeError):
            pass
    data = root / "config" / "settings_data.json"
    if data.exists():
        try:
            raw = re.sub(r"^\s*/\*.*?\*/", "", data.read_text(encoding="utf-8"), flags=re.S)
            cur = json.loads(raw).get("current", {})
            cur = cur if isinstance(cur, dict) else {}
            out["shopify"]["fonts"] = {k: v for k, v in cur.items() if k.startswith("type_") and isinstance(v, str)}
            schemes = cur.get("color_schemes") or {}
            keep = ("background", "foreground", "foreground_heading", "primary", "border",
                    "primary_button_background", "primary_button_text", "primary_button_hover_background")
            out["shopify"]["color_schemes"] = {k: {s: v.get("settings", {}).get(s) for s in keep}
                                               for k, v in list(schemes.items())[:8]}
            out["shopify"]["colors"] = {k: v for k, v in cur.items() if "color" in k and isinstance(v, str) and v.startswith("#")}
        except ValueError:
            out["shopify"]["settings_data"] = "present but unreadable"
    return out


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("url", help="the brand's public website, e.g. https://example.com")
    ap.add_argument("--out", default="brand-scrape.json")
    ap.add_argument("--repo", help="path to the client's repo, to list existing brand/design docs and theme settings")
    ap.add_argument("--evidence", help="folder for the saved page texts (default: an 'evidence' folder next to --out)")
    ap.add_argument("--max-products", type=int, default=25, help="product pages to sample when there is no products.json")
    ap.add_argument("--max-posts", type=int, default=5, help="recent blog posts to measure")
    ap.add_argument("--max-requests", type=int, default=MAX_REQUESTS, help="stop fetching after this many requests")
    ap.add_argument("--delay", type=float, default=0.3, help="seconds between requests")
    ap.add_argument("--extra-url", action="append", default=[], metavar="URL",
                    help="another page to read and save as evidence (repeatable): pages the scan missed")
    a = ap.parse_args()

    base = a.url if re.match(r"https?://", a.url) else "https://" + a.url
    base = norm(base)
    f = Fetcher(base, a.delay, a.max_requests)
    started = time.time()
    today = dt.date.today().isoformat()
    out = {"schema_version": SCHEMA_VERSION, "tool": TOOL, "site": base, "captured_at": today, "warnings": []}
    evidence_dir = Path(a.evidence) if a.evidence else Path(a.out).resolve().parent / "evidence"
    evidence = Evidence(evidence_dir, today)

    page, html = scrape_home(f, base)
    if not page:
        out["fatal"] = ("home page could not be fetched; check the URL and network access. If the site blocks "
                        "scripts (HTTP 401/403), read it with a browser tool instead")
        out["errors"] = f.errors
        Path(a.out).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"FAILED: could not fetch {base}. Errors: {f.errors[:3]}. If the site blocks scripts, "
              f"read it with a browser tool instead.", file=sys.stderr)
        sys.exit(2)
    blocked = bot_check(html, page)
    if blocked:
        out["fatal"] = f"blocked: the home page is a {blocked}; read the site with a browser tool instead"
        out["errors"] = f.errors
        Path(a.out).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"BLOCKED: {base} returned a {blocked}. Nothing was scanned; read the site with a browser tool "
              f"instead.", file=sys.stderr)
        sys.exit(3)

    platform, meta, shopify_json = detect_platform(f, base, html)
    nodes = ld_nodes(page)
    out["platform"] = platform
    out["shop_meta"] = {k: meta.get(k) for k in ("name", "description", "country", "currency", "city", "province",
                                                 "published_products_count", "myshopify_domain")} if meta else None
    out["language"] = page.lang
    org = organisation(page, nodes)
    logo, logo_source = logo_of(page, base, (org.get("organization") or {}).get("logo"), header_has_svg(html),
                                home_link_has_svg(html, base))
    home_text = main_text(page)
    out["home"] = {"title": page.title.strip(), "meta_description": page.metas.get("description", ""),
                   "og_title": page.metas.get("og:title", ""), "og_description": page.metas.get("og:description", ""),
                   "og_image": page.metas.get("og:image", ""), "theme_color": page.metas.get("theme-color", ""),
                   "logo": logo, "logo_source": logo_source, "render": render_mode(html, page),
                   "sha8": evidence.add(base, "home", page, home_text), "text": home_text[:TEXT_CAP]}
    footer_text = "\n".join(dict.fromkeys(c[1] for c in page.chunks if c[2] == "footer"))
    meta_lines = [f"{k}: {page.metas.get(k)}" for k in ("description", "og:title", "og:description", "og:site_name")
                  if page.metas.get(k)]
    evidence.add(base, "site_meta", page, f"title: {page.title.strip()}\n" + "\n".join(meta_lines)
                 + "\n\n# Footer\n" + footer_text, name="site-meta-and-footer")
    nav = navigation(page, base)
    out["navigation"] = nav
    out["social"] = socials(page, base)
    out.update(org)

    urls, maps_read = read_sitemaps(f, base)
    kinds = Counter()
    for u, _ in urls:
        p = path_of(u)
        k = ("product" if re.search(r"/products?/[^/]+$", p) else "collection" if "/collections/" in p else
             "blog" if re.search(r"/(blogs?|journal|news|articles)/", p) else "page" if "/pages/" in p else "other")
        kinds[k] += 1
    out["sitemap"] = {"sitemaps_read": maps_read, "urls": len(urls), "by_kind": dict(kinds),
                      "pages": [u for u, _ in urls if "/pages/" in path_of(u)][:150]}

    picked = pick_pages(urls, nav, base)
    picked_urls = {norm(u) for _, u, _ in picked}
    for x in a.extra_url:  # pages the person or agent knows the checklist needs
        u = norm(urllib.parse.urljoin(base + "/", x))
        if u not in picked_urls:
            picked.append(("extra", u, ""))
            picked_urls.add(u)
    out["story_pages"] = scrape_pages(f, picked, evidence)
    for p in [{"url": base, "render": out["home"]["render"]}] + out["story_pages"]:
        if p["render"] == "client-side":
            out["warnings"].append(f"client-rendered: {p['url']} needs a browser read")
    out["products"] = scrape_products(f, base, urls, shopify_json, a.max_products)
    if not out["products"].get("currency") and meta and meta.get("currency"):
        out["products"]["currency"] = meta["currency"]
    out["collections"] = scrape_collections(f, base, urls, shopify_json)
    if out["products"].get("claims"):
        evidence.add(base, "product_claims", page, "\n".join(
            f"{c['text']}  [{c['products']} products, e.g. {c['example']}]" for c in out["products"]["claims"]),
            name="product-claims")

    css = list(page.styles)
    google = []
    sheets = []
    for l in page.links:
        rel = (l.get("rel") or "").lower()
        href = l.get("href") or ""
        if "fonts.googleapis.com" in href:
            google.append(href)
        if href and ("stylesheet" in rel or (l.get("as") == "style")):
            sheets.append(urllib.parse.quote(urllib.parse.urljoin(base, href), safe=":/?&=%|,;+@#~"))
    for s in list(dict.fromkeys(sheets))[:8]:
        text = f.get(s, "stylesheet")
        if text:
            css.append(text)
            google += re.findall(r"https://fonts\.googleapis\.com/css2?\?[^'\")\s]+", text)
    out["visual"] = analyse_css(css, google)
    out["visual"]["stylesheets_read"] = len(css)
    families = [x["family"] for x in out["visual"]["fonts_ranked"]] + out["visual"]["font_face_families"]
    out["visual"]["font_license_flags"] = sorted({x for x in families if re.search(r"\b(trial|demo)\b", x, re.I)})

    out["blog"] = scrape_blog(f, base, urls, page, a.max_posts, evidence)

    texts = [out["home"]["text"]] + [p["text"] for p in out["story_pages"]]
    texts += [x.get("description", "") for x in (out["products"].get("items") or [])]
    texts += [m.get("opening", "") for m in out["blog"].get("sample", [])]
    texts += [d for m in out["blog"].get("sample", []) for d in m.get("disclaimer_like_text", [])]
    out["signals"] = signals(texts)

    if a.repo:
        brand = ((out.get("organization") or {}).get("name") or (out["shop_meta"] or {}).get("name")
                 or page.metas.get("og:site_name") or re.split(r"\s[|\u2013\u2014-]\s", page.title.strip())[0])
        out["repo"] = scan_repo(a.repo, brand)

    evidence.save()
    out["evidence_dir"] = str(evidence_dir)
    out["stats"] = {"requests": f.count, "seconds": round(time.time() - started, 1)}
    out["errors"] = f.errors[:60]
    Path(a.out).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    pr = out["products"]
    print(f"Saved {a.out}  ({f.count} requests, {out['stats']['seconds']}s)")
    print(f"  platform: {platform} | language: {page.lang or '?'} | sitemap URLs: {len(urls)}")
    print("  pages: " + (", ".join(f"{p['kind']} {path_of(p['url'])}" for p in out["story_pages"]) or "none found"))
    print(f"  products: {pr.get('total_products')} found, {pr.get('analysed')} analysed ({pr.get('source')})")
    print(f"  colors: {', '.join(c['hex'] for c in out['visual']['colors_ranked'][:6]) or 'none'}")
    print(f"  fonts: {', '.join(x['family'] for x in out['visual']['fonts_ranked'][:4]) or 'none'}"
          + (f" (licence check: {', '.join(out['visual']['font_license_flags'])})" if out["visual"]["font_license_flags"] else ""))
    print(f"  logo: {out['home']['logo_source'] or 'not found'}")
    print(f"  blog: {out['blog']['articles_in_sitemap']} articles in sitemap, {len(out['blog']['sample'])} measured"
          + (f", feed {out['blog']['feeds'][0]}" if out["blog"]["feeds"] else ", no feed"))
    print(f"  regulated signals: {', '.join(out['signals']['regulated_categories']) or 'none'}")
    print(f"  evidence: {len(evidence.items)} pages saved in {evidence_dir}")
    for w in out["warnings"]:
        print(f"  WARNING {w}")
    if f.errors:
        print(f"  {len(f.errors)} fetch issues recorded under 'errors'")


if __name__ == "__main__":
    main()
