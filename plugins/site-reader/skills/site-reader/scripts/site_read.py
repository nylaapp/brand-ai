#!/usr/bin/env python3
r"""Read a web page cheaply and reliably, without the browser pane or any browser extension.

Standard library only. One command, one compact JSON result (plus files you can open if you want to look).

  python site_read.py https://example.com/ --out site-read/home
  python site_read.py https://example.com/ --layers fetch              # text and structure only, no Chrome
  python site_read.py https://example.com/ --devices mobile --shots     # also save a small screenshot per device
  python site_read.py https://example.com/ --full --out site-read/home  # also a shrunk full-page picture

Layers (each is best effort; a failure is recorded under "errors" and never stops the others):
  fetch   plain HTTP: status, redirects, title, meta, headings, readable text, links, images, structured data,
          platform and Shopify theme id, and a flag when the page only renders in a browser.
          Costs a few hundred tokens. The default first read.
  layout  headless Chrome driven over its debugging port (the Chrome or Chromium already on the machine; no
          pane, no extension, a fresh private profile). Per device (desktop 1440x900, mobile 375x812):
          sections top to bottom with position and height, the first screen, calls to action, overlays,
          fonts and colours as computed, tap targets, images (broken, missing alt), horizontal overflow,
          and a plain-text wireframe of the page. About 1,000 to 3,000 tokens per device.
  visual  only on request (--shots, --full): small JPEG pictures and an SVG wireframe saved to --out.
          Look at them only when the text answer isn't enough.

Read-only: it loads and scrolls the page and never clicks, types or submits anything. It never types a
password: a password-protected store is reported as blocked.
"""
import argparse, base64, json, os, re, shutil, socket, ssl, struct, subprocess, sys, tempfile, time
import urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from xml.sax.saxutils import escape

DEVICES = {
    "desktop": {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False, "ua": None},
    "mobile": {"width": 375, "height": 812, "deviceScaleFactor": 2, "mobile": True,
               "ua": ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
                      "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")},
}
UA = "Mozilla/5.0 (compatible; brand-ai-site-reader/0.1; read-only)"


# ----------------------------------------------------------------------------------------- fetch layer
def _ctx():
    ctx = ssl.create_default_context()
    return ctx

def http_get(url, timeout=25, max_bytes=3_000_000):
    """GET with redirects. Returns (status, final_url, headers, body_text, redirect_chain)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8",
                                               "Accept-Language": "en-US,en;q=0.9"})
    chain = []

    class Track(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, r, fp, code, msg, headers, newurl):
            chain.append((code, newurl))
            return super().redirect_request(r, fp, code, msg, headers, newurl)

    def go(ctx):
        opener = urllib.request.build_opener(Track, urllib.request.HTTPSHandler(context=ctx))
        try:
            r = opener.open(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            r = e
        raw = r.read(max_bytes)
        enc = "utf-8"
        m = re.search(r"charset=([\w-]+)", r.headers.get("Content-Type", ""))
        if m:
            enc = m.group(1)
        return r.status if hasattr(r, "status") else r.code, r.geturl(), dict(r.headers), raw.decode(enc, "replace"), chain

    try:
        return go(_ctx())
    except (ssl.SSLError, urllib.error.URLError) as e:
        if "CERTIFICATE" in str(e).upper() and os.path.exists("/etc/ssl/cert.pem"):
            ctx = ssl.create_default_context(cafile="/etc/ssl/cert.pem")
            return go(ctx)
        raise


class Page(HTMLParser):
    SKIP = {"script", "style", "noscript", "template", "svg", "head"}
    BLOCK = {"p", "div", "section", "article", "li", "h1", "h2", "h3", "h4", "h5", "h6", "br", "tr", "header",
             "footer", "main", "nav", "ul", "ol", "blockquote", "figcaption", "summary", "details", "form"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self.meta = {}; self.canonical = None; self.lang = None
        self.headings = []; self.links = []; self.images = []; self.ld = []; self.text = []
        self.scripts = 0; self.inline_scripts = []; self.stylesheets = []
        self._skip = 0; self._in_title = False; self._h = None; self._a = None; self._ld = False
        self._script = False; self._buf = []; self.buttons = []; self._btn = None; self.has_main = False
        self.forms = 0; self.iframes = 0; self.videos = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if tag == "title": self._in_title = True
        if tag == "meta":
            k = (a.get("name") or a.get("property") or "").lower()
            if k and a.get("content") is not None: self.meta.setdefault(k, a["content"])
        if tag == "link":
            rel = (a.get("rel") or "").lower()
            if "canonical" in rel: self.canonical = a.get("href")
            if "stylesheet" in rel and a.get("href"): self.stylesheets.append(a["href"])
        if tag == "script":
            self.scripts += 1; self._script = True; self._buf = []
            self._ld = (a.get("type") or "").lower() == "application/ld+json"
        if tag == "main": self.has_main = True
        if tag == "form": self.forms += 1
        if tag == "iframe": self.iframes += 1
        if tag == "video": self.videos += 1
        if tag in self.SKIP and tag != "script": self._skip += 1
        if self._skip: return
        if tag in self.BLOCK: self.text.append("\n")
        if re.fullmatch(r"h[1-6]", tag): self._h = [int(tag[1]), []]
        if tag == "a" and a.get("href"): self._a = [a["href"], []]
        if tag == "button" or (tag == "a" and re.search(r"\b(btn|button)\b", (a.get("class") or "").lower())):
            self._btn = []
        if tag == "img":
            self.images.append({"src": (a.get("src") or a.get("data-src") or "")[:140], "alt": a.get("alt"),
                                "lazy": a.get("loading") == "lazy", "w": a.get("width"), "h": a.get("height")})

    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False
        if tag == "script":
            body = "".join(self._buf)
            if self._ld:
                try:
                    j = json.loads(body)
                    self.ld += j if isinstance(j, list) else (j.get("@graph") or [j])
                except Exception:
                    self.ld.append({"@type": "PARSE_ERROR"})
            elif body.strip():
                self.inline_scripts.append(body[:6000])
            self._script = False; self._ld = False
        if tag in self.SKIP and tag != "script":
            self._skip = max(0, self._skip - 1)
        if self._skip: return
        if re.fullmatch(r"h[1-6]", tag) and self._h:
            t = re.sub(r"\s+", " ", "".join(self._h[1])).strip()
            if t: self.headings.append((self._h[0], t[:120]))
            self._h = None
        if tag == "a" and self._a:
            t = re.sub(r"\s+", " ", "".join(self._a[1])).strip()
            self.links.append((self._a[0], t[:80])); self._a = None
        if tag in ("button", "a") and self._btn is not None:
            t = re.sub(r"\s+", " ", "".join(self._btn)).strip()
            if t: self.buttons.append(t[:60])
            self._btn = None
        if tag in self.BLOCK: self.text.append("\n")

    def handle_data(self, d):
        if self._script: self._buf.append(d); return
        if self._in_title: self.title += d
        if self._skip: return
        self.text.append(d)
        if self._h: self._h[1].append(d)
        if self._a: self._a[1].append(d)
        if self._btn is not None: self._btn.append(d)


def clean_text(chunks):
    t = "".join(chunks)
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return "\n".join(l.strip() for l in t.split("\n") if l.strip())


def fetch_layer(url, max_text):
    out = {}
    status, final, headers, body, chain = http_get(url)
    p = Page(); p.feed(body)
    text = clean_text(p.text)
    words = len(text.split())
    host = urllib.parse.urlparse(final).netloc
    internal, external = [], []
    for href, label in p.links:
        h = urllib.parse.urljoin(final, href)
        if h.startswith(("mailto:", "tel:", "javascript:", "#")): continue
        (internal if urllib.parse.urlparse(h).netloc == host else external).append({"href": h[:160], "text": label})
    ltypes = []
    for o in p.ld:
        t = o.get("@type") if isinstance(o, dict) else None
        ltypes += t if isinstance(t, list) else [t or "unknown"]
    theme = None
    for s in p.inline_scripts:
        m = re.search(r"Shopify\.theme\s*=\s*(\{[^}]*\})", s)
        if m:
            try: theme = json.loads(m.group(1))
            except Exception:
                n = re.search(r'"id"\s*:\s*(\d+)', m.group(1)); nm = re.search(r'"name"\s*:\s*"([^"]*)"', m.group(1))
                theme = {"id": int(n.group(1)) if n else None, "name": nm.group(1) if nm else None}
            break
    is_shopify = bool(theme) or "cdn.shopify.com" in body or "Shopify.shop" in body
    blocked = None
    if "/password" in urllib.parse.urlparse(final).path or re.search(r"<form[^>]+/password", body):
        blocked = "password page (storefront is locked); not typing a password"
    elif status in (401, 403, 429) or status >= 500:
        blocked = f"HTTP {status}"
    needs_browser = None
    if not blocked and words < 120 and (p.scripts >= 8 or re.search(r'id="(root|app|__next|__nuxt)"', body)):
        needs_browser = "very little text in the HTML but many scripts: probably rendered in the browser; use the layout layer"
    out.update({
        "status": status, "final_url": final, "redirects": [{"code": c, "to": u[:160]} for c, u in chain],
        "blocked": blocked, "needs_browser": needs_browser,
        "platform": "shopify" if is_shopify else None, "shopify_theme": theme,
        "lang": p.lang, "title": p.title.strip(), "title_len": len(p.title.strip()),
        "meta_description": p.meta.get("description"), "canonical": p.canonical,
        "robots": p.meta.get("robots"), "theme_color": p.meta.get("theme-color"),
        "og": {k[3:]: v[:140] for k, v in p.meta.items() if k.startswith("og:")},
        "headings": [f"h{l}: {t}" for l, t in p.headings[:60]],
        "h1_count": sum(1 for l, _ in p.headings if l == 1),
        "words": words, "text": text[:max_text] + (" …[cut]" if len(text) > max_text else ""),
        "buttons": list(dict.fromkeys(p.buttons))[:20],
        "links": {"internal": len(internal), "external": len(external), "sample_internal": internal[:15],
                  "sample_external": external[:8]},
        "images": {"count": len(p.images), "missing_alt": sum(1 for i in p.images if i["alt"] is None),
                   "empty_alt": sum(1 for i in p.images if i["alt"] == ""),
                   "lazy": sum(1 for i in p.images if i["lazy"])},
        "structured_data": sorted(set(ltypes)),
        "counts": {"scripts": p.scripts, "stylesheets": len(p.stylesheets), "forms": p.forms,
                   "iframes": p.iframes, "videos": p.videos, "has_main": p.has_main},
    })
    return out


# ----------------------------------------------------------------------------------------- layout layer
def find_chrome():
    env = os.environ.get("CHROME_PATH")
    cands = [env] if env else []
    cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    for c in cands:
        if c and os.path.exists(c): return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        w = shutil.which(name)
        if w: return w
    return None


class WS:
    """Minimal WebSocket client for Chrome's debugging port (same approach as cro-audit's evidence_shot.py)."""
    def __init__(self, url):
        rest = url.split("://", 1)[1]
        hostport, path = rest.split("/", 1)
        host, port = hostport.split(":")
        self.s = socket.create_connection((host, int(port)), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.extra = buf.split(b"\r\n\r\n", 1)[1]
        self.n = 0; self.events = []

    def _recv(self, k):
        while len(self.extra) < k:
            chunk = self.s.recv(1 << 20)
            if not chunk: raise ConnectionError("browser closed the connection")
            self.extra += chunk
        out, self.extra = self.extra[:k], self.extra[k:]
        return out

    def _frame(self):
        msg = b""
        while True:
            b1, b2 = self._recv(2)
            ln = b2 & 0x7F
            if ln == 126: ln = struct.unpack(">H", self._recv(2))[0]
            elif ln == 127: ln = struct.unpack(">Q", self._recv(8))[0]
            msg += self._recv(ln)
            if b1 & 0x80: return msg

    def send(self, method, params=None):
        self.n += 1
        data = json.dumps({"id": self.n, "method": method, "params": params or {}}).encode()
        mask = os.urandom(4)
        ln = len(data)
        head = bytes([0x81]) + (bytes([0x80 | ln]) if ln < 126 else
                                (bytes([0x80 | 126]) + struct.pack(">H", ln) if ln < 65536 else
                                 bytes([0x80 | 127]) + struct.pack(">Q", ln)))
        self.s.sendall(head + mask + bytes(c ^ mask[i % 4] for i, c in enumerate(data)))
        want = self.n
        while True:
            m = json.loads(self._frame())
            if m.get("id") == want:
                if "error" in m: raise RuntimeError(f"{method}: {m['error']}")
                return m.get("result", {})
            self.events.append(m)

    def wait_event(self, name, timeout):
        end = time.time() + timeout
        while time.time() < end:
            if any(e.get("method") == name for e in self.events): return True
            self.s.settimeout(max(0.1, end - time.time()))
            try:
                self.events.append(json.loads(self._frame()))
            except socket.timeout:
                break
            finally:
                self.s.settimeout(60)
        return False

    def drain(self, secs):
        end = time.time() + secs
        while time.time() < end:
            self.s.settimeout(max(0.05, end - time.time()))
            try:
                self.events.append(json.loads(self._frame()))
            except (socket.timeout, TimeoutError):
                break
            finally:
                self.s.settimeout(60)


def js(ws, expr):
    r = ws.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    if r.get("exceptionDetails"):
        raise RuntimeError("page script failed: " + json.dumps(r["exceptionDetails"])[:200])
    return (r.get("result") or {}).get("value")


# One script, run in the page. Returns everything the layout layer reports for one viewport.
MEASURE = r"""
(() => {
  const vw = innerWidth, vh = innerHeight, docH = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
  const px = n => Math.round(n);
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    return r.width > 1 && r.height > 1 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const abs = e => { const r = e.getBoundingClientRect(); return {top: px(r.top + scrollY), h: px(r.height), left: px(r.left + scrollX), w: px(r.width)}; };
  const words = (e, n) => (e.innerText || '').replace(/\s+/g, ' ').trim().split(' ').slice(0, n).join(' ');
  const label = e => (e.id || '').replace(/^shopify-section-(template--\d+__)?/, '') || (e.className && typeof e.className === 'string' ? e.className.split(' ')[0] : '') || e.tagName.toLowerCase();
  const main = document.querySelector('#MainContent, main, [role=main]') || document.body;
  let secs = [...main.querySelectorAll(':scope > .shopify-section, :scope > section, :scope > div > .shopify-section')];
  if (secs.length < 2) secs = [...main.children];
  secs = secs.filter(e => vis(e) && e.getBoundingClientRect().height > 30);
  const header = document.querySelector('header, .shopify-section-group-header-group, #shopify-section-header');
  const footer = document.querySelector('footer, .shopify-section-group-footer-group, #shopify-section-footer');
  const ctaSel = 'a.button, a.btn, button, [class*=button], [class*=btn], a[href*="cart"], a[href*="book"], a[href*="shop"], input[type=submit]';
  const sections = [];
  const add = (kind, e) => {
    const a = abs(e), cs = getComputedStyle(e);
    const h = e.querySelector('h1,h2,h3');
    const ctas = [...e.querySelectorAll(ctaSel)].filter(vis).map(c => (c.innerText || c.value || c.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim()).filter(Boolean);
    sections.push({kind, id: label(e), top: a.top, h: a.h,
      heading: h ? words(h, 12) : null, text: words(e, 14),
      ctas: [...new Set(ctas)].slice(0, 4),
      media: {img: e.querySelectorAll('img, picture').length, video: e.querySelectorAll('video, iframe[src*=youtube], iframe[src*=vimeo]').length},
      bg: cs.backgroundColor, bgImage: cs.backgroundImage !== 'none' ? 'yes' : undefined});
  };
  if (header) add('header', header);
  secs.forEach(e => { if (e !== header && e !== footer) add('section', e); });
  if (footer) add('footer', footer);
  sections.sort((x, y) => x.top - y.top);
  const firstScreen = {
    headings: [...document.querySelectorAll('h1,h2')].filter(e => vis(e) && e.getBoundingClientRect().top < vh && e.getBoundingClientRect().bottom > 0).map(e => e.tagName + ': ' + words(e, 14)).slice(0, 4),
    ctas: [...document.querySelectorAll(ctaSel)].filter(e => vis(e) && e.getBoundingClientRect().top < vh && e.getBoundingClientRect().bottom > 0).map(e => (e.innerText || e.value || e.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim()).filter(Boolean).filter((v, i, a) => a.indexOf(v) === i).slice(0, 6),
    hasMedia: !![...document.querySelectorAll('img, video')].find(e => vis(e) && e.getBoundingClientRect().top < vh && e.getBoundingClientRect().width > vw * 0.4)
  };
  const overlays = [...document.querySelectorAll('body *')].filter(e => { const s = getComputedStyle(e);
      if (!['fixed', 'sticky'].includes(s.position) || !vis(e) || e.closest('[aria-hidden=true], [inert]') || s.pointerEvents === 'none') return false;
      const r = e.getBoundingClientRect();
      const iw = Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0)), ih = Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0));
      return iw * ih > vw * vh * 0.04 && (s.position === 'fixed' || r.top <= 2 && e !== header && !header?.contains(e)); })
    .map(e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
      return {el: label(e) + (e.getAttribute('role') ? '[' + e.getAttribute('role') + ']' : ''), position: s.position,
              x: px(r.left), y: px(r.top), w: px(r.width), h: px(r.height), coversPct: Math.round(100 * (Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0)) * Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0))) / (vw * vh)), text: words(e, 10)}; })
    .filter(o => o.coversPct >= 4).slice(0, 6);
  const cs = (sel, props) => { const e = document.querySelector(sel); if (!e) return null; const s = getComputedStyle(e);
    return Object.fromEntries(props.map(p => [p, s[p]])); };
  const type = {
    body: cs('body', ['fontFamily', 'fontSize', 'color', 'backgroundColor', 'lineHeight']),
    h1: cs('h1', ['fontFamily', 'fontSize', 'fontWeight', 'color', 'lineHeight', 'textTransform']),
    h2: cs('main h2, h2', ['fontFamily', 'fontSize', 'fontWeight', 'color']),
    p: cs('main p, p', ['fontFamily', 'fontSize', 'color', 'lineHeight']),
    link: cs('main a, a', ['color', 'textDecorationLine']),
    button: cs('a.button, .button, button:not([aria-label]), .btn', ['backgroundColor', 'color', 'borderRadius', 'fontSize', 'fontFamily', 'borderTopWidth'])
  };
  const small = [...document.querySelectorAll('a[href], button, input, select, textarea, [role=button]')].filter(vis)
    .filter(e => { const r = e.getBoundingClientRect(); return r.width < 44 || r.height < 44; }).length;
  const imgs = [...document.images];
  const broken = imgs.filter(i => i.complete && i.naturalWidth === 0 && (i.currentSrc || i.src)).map(i => (i.currentSrc || i.src).slice(0, 100));
  const heads = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis).map(h => +h.tagName[1]);
  let skipped = 0; for (let i = 1; i < heads.length; i++) if (heads[i] - heads[i - 1] > 1) skipped++;
  const t = (window.Shopify || {}).theme;
  return {
    viewport: {w: vw, h: vh}, docHeight: docH, themeId: t ? t.id : null, themeName: t ? t.name : null,
    overflowX: document.documentElement.scrollWidth > vw + 1 ? document.documentElement.scrollWidth - vw : 0,
    sections, firstScreen, overlays, type,
    images: {count: imgs.length, broken: broken.slice(0, 5), brokenCount: broken.length,
             missingAlt: imgs.filter(i => i.getAttribute('alt') === null).length},
    headings: {h1: heads.filter(x => x === 1).length, skippedLevels: skipped},
    tapTargetsUnder44: small,
    title: document.title
  };
})()
"""

def scroll_through(ws, dev, settle):
    """Wheel-scroll to the bottom and back like a visitor so lazy content loads."""
    h = js(ws, "Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)") or 0
    y, steps = 0, 0
    while y < h and steps < 80:
        ws.send("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": dev["width"] / 2, "y": dev["height"] / 2,
                                             "deltaX": 0, "deltaY": 700})
        time.sleep(0.12)
        y = js(ws, "scrollY + innerHeight") or y + 700
        h = js(ws, "Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)") or h
        steps += 1
    time.sleep(settle)
    js(ws, "scrollTo(0,0)")
    time.sleep(0.6)


def wireframe_text(m):
    vh = m["viewport"]["h"]; lines = []
    marked = False
    for s in m["sections"]:
        if not marked and s["top"] >= vh:
            lines.append(f"{'-' * 8} first screen ends at {vh}px {'-' * 8}"); marked = True
        bits = [f"{s['top']}-{s['top'] + s['h']}", f"{s['kind']}:{s['id']}"]
        if s["heading"]: bits.append(f"“{s['heading']}”")
        elif s["text"]: bits.append(f"“{s['text'][:60]}”")
        md = []
        if s["media"]["img"]: md.append(f"{s['media']['img']} img")
        if s["media"]["video"]: md.append("video")
        if s.get("bgImage"): md.append("bg-img")
        if md: bits.append("[" + ", ".join(md) + "]")
        if s["ctas"]: bits.append("CTA: " + " | ".join(c[:24] for c in s["ctas"][:3]))
        lines.append("  ".join(bits))
    if not marked:
        lines.append(f"{'-' * 8} first screen ({vh}px) covers the whole page {'-' * 8}")
    return lines


def wireframe_svg(m, path):
    W = 360; sc = W / m["viewport"]["w"]
    H = max(120, int(min(m["docHeight"], 12000) * sc)) + 20
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 20}" height="{H}" font-family="sans-serif" font-size="9">',
             f'<rect width="100%" height="100%" fill="#fff"/>']
    for s in m["sections"]:
        y, h = 10 + s["top"] * sc, max(3, s["h"] * sc)
        parts.append(f'<rect x="10" y="{y:.1f}" width="{W}" height="{h:.1f}" fill="#f1f5f9" stroke="#94a3b8"/>')
        t = escape(f"{s['id']}  {s['top']}-{s['top'] + s['h']}  {s['heading'] or s['text'][:30]}")[:70]
        parts.append(f'<text x="14" y="{y + 10:.1f}" fill="#0f172a">{t}</text>')
    fy = 10 + m["viewport"]["h"] * sc
    parts.append(f'<line x1="0" x2="{W + 20}" y1="{fy:.1f}" y2="{fy:.1f}" stroke="#e5484d" stroke-dasharray="4"/>'
                 f'<text x="14" y="{fy - 3:.1f}" fill="#e5484d">first screen ends</text>')
    for o in m["overlays"]:
        parts.append(f'<rect x="{10 + o["x"] * sc:.1f}" y="{10 + o["y"] * sc:.1f}" width="{o["w"] * sc:.1f}" height="{max(3, o["h"] * sc):.1f}" fill="none" stroke="#e5484d" stroke-width="2"/>')
    parts.append("</svg>")
    open(path, "w").write("\n".join(parts))


def layout_layer(url, devices, wait, shots, full, out_dir, late):
    chrome = find_chrome()
    if not chrome:
        raise RuntimeError("No Chrome or Chromium found (set CHROME_PATH). Layout and visuals can't be read; the fetch layer still works.")
    res = {}
    for name in devices:
        dev = DEVICES[name]
        prof = tempfile.mkdtemp(prefix="site-read-")
        proc = subprocess.Popen([chrome, "--headless=new", "--remote-debugging-port=0", f"--user-data-dir={prof}",
                                 "--hide-scrollbars", "--no-first-run", "--no-default-browser-check",
                                 "--disable-extensions", "about:blank"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            pf = os.path.join(prof, "DevToolsActivePort")
            for _ in range(150):
                if os.path.exists(pf) and open(pf).read().strip(): break
                time.sleep(0.1)
            else:
                raise RuntimeError("Chrome did not start")
            port = open(pf).read().split()[0]
            rq = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")
            target = json.load(urllib.request.urlopen(rq, timeout=10))
            ws = WS(target["webSocketDebuggerUrl"])
            for dom in ("Page.enable", "Runtime.enable", "Network.enable"):
                ws.send(dom)
            ws.send("Emulation.setDeviceMetricsOverride", {k: dev[k] for k in ("width", "height", "deviceScaleFactor", "mobile")})
            if dev["ua"]: ws.send("Emulation.setUserAgentOverride", {"userAgent": dev["ua"]})
            ws.send("Emulation.setTouchEmulationEnabled", {"enabled": dev["mobile"]})
            t0 = time.time()
            ws.send("Page.navigate", {"url": url})
            loaded = ws.wait_event("Page.loadEventFired", 45)
            load_s = round(time.time() - t0, 1)
            time.sleep(wait)
            if str(js(ws, "location.href")).startswith("chrome-error:"):
                raise RuntimeError("Chrome could not load the page (address not found, refused or timed out)")
            if not js(ws, "innerWidth > 0 && innerHeight > 0"):
                raise RuntimeError("viewport reports 0x0; measurements would be wrong")
            early = js(ws, "(()=>{const o=[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);const r=e.getBoundingClientRect();return s.position==='fixed'&&r.width*r.height>innerWidth*innerHeight*0.12&&s.visibility!=='hidden'&&s.display!=='none'}).length;return o})()")
            scroll_through(ws, dev, 1.2)
            if late:
                time.sleep(late)
            m = js(ws, MEASURE)
            m["device"] = name
            m["loadEventSeen"] = loaded; m["loadSeconds"] = load_s
            m["largeFixedAt1s"] = early
            fails = [e for e in ws.events if e.get("method") == "Network.loadingFailed"
                     and not e.get("params", {}).get("canceled")]
            exc = [e for e in ws.events if e.get("method") == "Runtime.exceptionThrown"]
            m["failedRequests"] = len(fails); m["pageErrors"] = len(exc)
            m["wireframe"] = wireframe_text(m)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
                wireframe_svg(m, os.path.join(out_dir, f"wireframe-{name}.svg"))
                files = []
                if shots:
                    p = os.path.join(out_dir, f"first-screen-{name}.jpg")
                    r = ws.send("Page.captureScreenshot", {"format": "jpeg", "quality": 55})
                    open(p, "wb").write(base64.b64decode(r["data"])); files.append(p)
                if full:
                    h = min(int(m["docHeight"]), 9000)
                    sc = round(min(0.6, 1400 / max(h, 1)), 2) if name == "mobile" else round(min(0.5, 2200 / max(h, 1)), 2)
                    clip = {"x": 0, "y": 0, "width": dev["width"], "height": h, "scale": max(0.15, sc)}
                    r = ws.send("Page.captureScreenshot", {"format": "jpeg", "quality": 50, "clip": clip, "captureBeyondViewport": True})
                    p = os.path.join(out_dir, f"full-page-{name}.jpg")
                    open(p, "wb").write(base64.b64decode(r["data"])); files.append(p)
                files.append(os.path.join(out_dir, f"wireframe-{name}.svg"))
                m["files"] = files
            res[name] = m
        finally:
            proc.terminate()
            try: proc.wait(timeout=5)
            except Exception: proc.kill()
            shutil.rmtree(prof, ignore_errors=True)
    return res


def brief(r):
    L = []
    f = r.get("fetch")
    L.append(f"READ {r['url']}  ({r['read_at']})  layers: {', '.join(r['layers_run']) or 'none'}")
    if f:
        th = f.get("shopify_theme") or {}
        L.append(f"status {f['status']}" + (f" -> {f['final_url']}" if f["final_url"].rstrip('/') != r['url'].rstrip('/') else "")
                 + (f" | Shopify theme {th.get('id')} “{th.get('name')}”" if th else "")
                 + f" | lang {f['lang']} | {f['words']} words | h1 x{f['h1_count']}")
        L.append(f"title ({f['title_len']}): {f['title']}")
        L.append(f"meta description: {(f['meta_description'] or 'MISSING')[:160]}")
        if f["structured_data"]: L.append("structured data: " + ", ".join(f["structured_data"]))
        if f["headings"]: L.append("headings: " + " | ".join(f["headings"][:12]))
        im = f["images"]; L.append(f"images {im['count']} (no alt attr: {im['missing_alt']}) | links in {f['links']['internal']} out {f['links']['external']}")
        if f["blocked"]: L.append("BLOCKED: " + f["blocked"])
        if f["needs_browser"]: L.append("NOTE: " + f["needs_browser"])
    for name, m in (r.get("layout") or {}).items():
        t = m["type"]; fs = m["firstScreen"]
        L.append("")
        L.append(f"== {name.upper()} {m['viewport']['w']}x{m['viewport']['h']} | page {m['docHeight']}px | load {m['loadSeconds']}s | "
                 f"sideways overflow {m['overflowX']}px | tap targets under 44px: {m['tapTargetsUnder44']} | "
                 f"broken images {m['images']['brokenCount']} | skipped heading levels {m['headings']['skippedLevels']} | "
                 f"page errors {m['pageErrors']}, failed requests {m['failedRequests']}")
        L += m["wireframe"]
        L.append("first screen: " + "; ".join(fs["headings"]) + " | actions: " + ", ".join(fs["ctas"][:5]) + (" | big picture" if fs["hasMedia"] else " | no big picture"))
        if m["overlays"]:
            L.append("in the way: " + "; ".join(f"{o['el']} covers {o['coversPct']}% “{o['text'][:40]}”" for o in m["overlays"]))
        def tp(x, keys):
            return ", ".join(f"{k} {x[k]}" for k in keys if x and x.get(k)) if x else "n/a"
        L.append("type: h1 " + tp(t.get("h1"), ["fontFamily", "fontSize", "fontWeight"]) + " | body " + tp(t.get("body"), ["fontFamily", "fontSize", "color"]))
        if t.get("button"): L.append("button: " + tp(t["button"], ["backgroundColor", "color", "borderRadius", "fontSize"]))
        if m.get("files"): L.append("files: " + ", ".join(m["files"]))
    for n in r["notes"]: L.append("NOTE: " + n)
    for k, v in r["errors"].items(): L.append(f"COULD NOT READ {k}: {v}")
    if r.get("saved"): L.append("full detail: " + r["saved"])
    return "\n".join(L)


# ----------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--layers", default="fetch,layout", help="comma list of fetch,layout (default both)")
    ap.add_argument("--devices", default="desktop,mobile", help="desktop,mobile (default both; visual checks need both)")
    ap.add_argument("--out", help="folder for report.json, wireframes and pictures (created)")
    ap.add_argument("--shots", action="store_true", help="save a small first-screen JPEG per device")
    ap.add_argument("--full", action="store_true", help="save a shrunk full-page JPEG per device")
    ap.add_argument("--max-text", type=int, default=3000, help="characters of page text to keep (default 3000)")
    ap.add_argument("--wait", type=float, default=2.0, help="seconds to settle after load (default 2)")
    ap.add_argument("--late", type=float, default=0, help="extra seconds before measuring, to catch late popups (try 15)")
    ap.add_argument("--expect-theme-id", help="Shopify theme id the page should report; mismatch is flagged")
    ap.add_argument("--json", action="store_true", help="print the full JSON instead of the short text summary")
    ap.add_argument("--compact", action="store_true", help="with --json, print on one line")
    a = ap.parse_args()
    if not re.match(r"https?://", a.url): a.url = "https://" + a.url
    layers = {x.strip() for x in a.layers.split(",")}
    devices = [d.strip() for d in a.devices.split(",") if d.strip() in DEVICES]
    result = {"url": a.url, "read_at": time.strftime("%Y-%m-%d %H:%M:%S %z"), "layers_run": [], "errors": {}, "notes": []}
    if len(devices) < 2 and "layout" in layers:
        result["notes"].append("Only one device was read. Anything about how the page looks needs both desktop and mobile.")
    if "fetch" in layers:
        try:
            result["fetch"] = fetch_layer(a.url, a.max_text); result["layers_run"].append("fetch")
        except Exception as e:
            result["errors"]["fetch"] = f"{type(e).__name__}: {e}"
    blocked = (result.get("fetch") or {}).get("blocked")
    if "layout" in layers and not blocked:
        try:
            result["layout"] = layout_layer(a.url, devices, a.wait, a.shots, a.full, a.out, a.late)
            result["layers_run"].append("layout")
        except Exception as e:
            result["errors"]["layout"] = f"{type(e).__name__}: {e}"
    elif blocked:
        result["notes"].append(f"Not rendered: {blocked}. Ask the person to lift it or use a theme preview; read the theme files instead.")
    if a.expect_theme_id:
        seen = {str((v.get('themeId'))) for v in (result.get("layout") or {}).values() if v.get("themeId")}
        ft = (result.get("fetch") or {}).get("shopify_theme") or {}
        if ft.get("id"): seen.add(str(ft["id"]))
        if not seen:
            result["notes"].append("Theme id: can't tell (the page didn't report one).")
        elif seen != {str(a.expect_theme_id)}:
            result["notes"].append(f"THEME MISMATCH: expected {a.expect_theme_id}, the page reports {sorted(seen)}. Don't trust results for the expected theme.")
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        with open(os.path.join(a.out, "report.json"), "w") as f:
            json.dump(result, f, indent=1, ensure_ascii=False)
        result["saved"] = os.path.join(a.out, "report.json")
    if a.json:
        print(json.dumps(result, ensure_ascii=False, **({} if a.compact else {"indent": 1})))
    else:
        print(brief(result))
    if not result["layers_run"]:
        sys.exit(2)

if __name__ == "__main__":
    main()
