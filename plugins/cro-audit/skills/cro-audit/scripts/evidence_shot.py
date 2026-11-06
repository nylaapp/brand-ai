#!/usr/bin/env python3
r"""Evidence pictures for the audit: take a clean screenshot of a page section on a phone or desktop, or use
one you already have, then crop it, draw numbered boxes and dots, and add a caption. Writes a
self-contained SVG (the image is embedded) and, with --capture, the PNG beside it. Stdlib only.

  # capture: drives the local Chrome or Chromium headless, as a phone (390x844) or desktop (1440x900),
  # scrolls to the section with wheel events like a visitor, and boxes elements by CSS selector
  evidence_shot.py --capture https://example.com/ --device phone --wait 3 \
      --selector "#shopify-section-header" --mark-el "1=.header__icons" --mark-el "2=a[href*=book]" \
      --title "CRO-03 · phone · header" --out cro-evidence/cro-03-phone.svg

  # from the Lighthouse report the speed check already made (it holds a full-page screenshot)
  evidence_shot.py --lighthouse lh-mobile.json --list
  evidence_shot.py --lighthouse lh-mobile.json --section image_banner --mark "1:200,3010" \
      --box "2:16,3200,380,60" --title "CRO-01 · phone · second band" --out cro-evidence/cro-01-phone.svg

  # from any screenshot file (PNG, JPEG or WebP) taken at a known page width in CSS pixels
  evidence_shot.py --image shot.png --css-width 375 --crop 0:812 --mark "1:180,700" --out cro-evidence/cro-02-phone.svg

Coordinates are CSS pixels from the top-left of the whole page (what getBoundingClientRect() plus the
scroll offset gives at the same page width). --crop TOP:BOTTOM picks the band to show; --section picks a
Lighthouse node's band by its id (for example a Shopify section id). With --capture, boxes come from
selectors, so no coordinates are needed.

Read-only: it loads and scrolls the page in a fresh, private browser profile (so no cookie choice, popup
or draft-theme preview carries over) and never clicks, types or submits anything.
"""
import argparse, base64, json, os, shutil, socket, struct, subprocess, sys, tempfile, time, urllib.request
from xml.sax.saxutils import escape

COLOR = "#E5484D"

def image_size(raw):
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", raw[16:24])
    if raw[:2] == b"\xff\xd8":
        i = 2
        while i < len(raw) - 9:
            if raw[i] != 0xFF:
                i += 1
                continue
            m = raw[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", raw[i + 5:i + 9])
                return w, h
            i += 2 + struct.unpack(">H", raw[i + 2:i + 4])[0]
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        kind = raw[12:16]
        if kind == b"VP8X":
            return 1 + int.from_bytes(raw[24:27], "little"), 1 + int.from_bytes(raw[27:30], "little")
        if kind == b"VP8L":
            b = int.from_bytes(raw[21:25], "little")
            return 1 + (b & 0x3FFF), 1 + ((b >> 14) & 0x3FFF)
        if kind == b"VP8 ":
            w, h = struct.unpack("<HH", raw[26:30])
            return w & 0x3FFF, h & 0x3FFF
    sys.exit("unknown image type: use PNG, JPEG or WebP")

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}

def from_lighthouse(path):
    d = json.load(open(path))
    fp = d.get("fullPageScreenshot") or (d.get("audits", {}).get("full-page-screenshot") or {}).get("details")
    if not fp or "screenshot" not in fp:
        sys.exit("this Lighthouse report has no full-page screenshot (run Lighthouse without --skip-audits full-page-screenshot)")
    s = fp["screenshot"]
    return s["data"], float(s["width"]), float(s["height"]), fp.get("nodes", {})

def from_image(path, css_width):
    raw = open(path, "rb").read()
    w, h = image_size(raw)
    mime = MIME.get(os.path.splitext(path)[1].lower())
    if not mime:
        sys.exit("unknown image extension: use .png, .jpg or .webp")
    cw = float(css_width or w)
    return f"data:{mime};base64," + base64.b64encode(raw).decode(), cw, h * cw / w, {}

# ---------- capture through the Chrome DevTools protocol (stdlib websocket) ----------

DEVICES = {
    "phone": dict(width=390, height=844, deviceScaleFactor=2, mobile=True,
                  ua="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"),
    "desktop": dict(width=1440, height=900, deviceScaleFactor=1, mobile=False, ua=None),
}

def find_chrome():
    env = os.environ.get("CHROME_PATH")
    cands = [env] if env else []
    cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"]
    for c in cands:
        if c and os.path.exists(c):
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        w = shutil.which(name)
        if w:
            return w
    sys.exit("No Chrome or Chromium found (set CHROME_PATH). Use --image with a screenshot instead, or --lighthouse.")

class WS:
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
        self.n = 0
        self.events = []

    def _recv(self, k):
        while len(self.extra) < k:
            chunk = self.s.recv(1 << 20)
            if not chunk:
                raise ConnectionError("browser closed the connection")
            self.extra += chunk
        out, self.extra = self.extra[:k], self.extra[k:]
        return out

    def _frame(self):
        msg = b""
        while True:
            b1, b2 = self._recv(2)
            ln = b2 & 0x7F
            if ln == 126:
                ln = struct.unpack(">H", self._recv(2))[0]
            elif ln == 127:
                ln = struct.unpack(">Q", self._recv(8))[0]
            msg += self._recv(ln)
            if b1 & 0x80:
                return msg

    def send(self, method, params=None):
        self.n += 1
        data = json.dumps({"id": self.n, "method": method, "params": params or {}}).encode()
        mask = os.urandom(4)
        head = bytes([0x81])
        ln = len(data)
        head += bytes([0x80 | ln]) if ln < 126 else (bytes([0x80 | 126]) + struct.pack(">H", ln) if ln < 65536 else bytes([0x80 | 127]) + struct.pack(">Q", ln))
        self.s.sendall(head + mask + bytes(c ^ mask[i % 4] for i, c in enumerate(data)))
        want = self.n
        while True:
            m = json.loads(self._frame())
            if m.get("id") == want:
                if "error" in m:
                    raise RuntimeError(f"{method}: {m['error']}")
                return m.get("result", {})
            self.events.append(m)

    def wait_event(self, name, timeout):
        end = time.time() + timeout
        while time.time() < end:
            if any(e.get("method") == name for e in self.events):
                return True
            self.s.settimeout(max(0.1, end - time.time()))
            try:
                self.events.append(json.loads(self._frame()))
            except socket.timeout:
                break
            finally:
                self.s.settimeout(60)
        return False

def js(ws, expr):
    r = ws.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return (r.get("result") or {}).get("value")

RECT = ("(s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect();"
        "return {x:r.left+scrollX, y:r.top+scrollY, w:r.width, h:r.height};})")

def capture(url, device, wait, selector, pad, max_h, marks, png_path):
    dev = DEVICES[device]
    chrome = find_chrome()
    prof = tempfile.mkdtemp(prefix="cro-shot-")
    proc = subprocess.Popen([chrome, "--headless=new", "--remote-debugging-port=0", f"--user-data-dir={prof}",
                             "--hide-scrollbars", "--no-first-run", "--no-default-browser-check", "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        port_file = os.path.join(prof, "DevToolsActivePort")
        for _ in range(100):
            if os.path.exists(port_file) and open(port_file).read().strip():
                break
            time.sleep(0.1)
        port = open(port_file).read().split()[0]
        req = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")
        target = json.load(urllib.request.urlopen(req, timeout=10))
        ws = WS(target["webSocketDebuggerUrl"])
        ws.send("Page.enable")
        ws.send("Emulation.setDeviceMetricsOverride", {k: dev[k] for k in ("width", "height", "deviceScaleFactor", "mobile")})
        if dev["ua"]:
            ws.send("Emulation.setUserAgentOverride", {"userAgent": dev["ua"]})
        ws.send("Emulation.setTouchEmulationEnabled", {"enabled": dev["mobile"]})
        ws.send("Page.navigate", {"url": url})
        ws.wait_event("Page.loadEventFired", 45)
        time.sleep(wait)
        theme = js(ws, "JSON.stringify((window.Shopify||{}).theme||null)")
        top = 0.0
        if selector:
            if not js(ws, f"!!document.querySelector({json.dumps(selector)})"):
                sys.exit(f"selector not found on the page: {selector}")
            last, still = -1, 0
            for _ in range(120):  # wheel-scroll like a visitor until the section's top is near the top
                r = js(ws, f"{RECT}({json.dumps(selector)})")
                vy = js(ws, "scrollY")
                if r["y"] - vy <= dev["height"] * 0.25:
                    break
                ws.send("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": dev["width"] / 2, "y": dev["height"] / 2,
                                                     "deltaX": 0, "deltaY": min(500, r["y"] - vy)})
                time.sleep(0.15)
                still = still + 1 if vy == last else 0
                last = vy
                if still >= 4:
                    break
            time.sleep(1.5)  # let lazy images in view load
            r = js(ws, f"{RECT}({json.dumps(selector)})")
            top = max(0.0, r["y"] - pad)
            height = min(r["h"] + 2 * pad, max_h)
            clip = {"x": 0, "y": top, "width": dev["width"], "height": height, "scale": 1}
            shot = ws.send("Page.captureScreenshot", {"format": "png", "clip": clip, "captureBeyondViewport": True})
        else:
            vy = js(ws, "scrollY") or 0
            top = float(vy)
            height = dev["height"]
            shot = ws.send("Page.captureScreenshot", {"format": "png"})
        boxes = []
        for label, sel in marks:
            r = js(ws, f"{RECT}({json.dumps(sel)})")
            if not r:
                print(f"warning: mark {label}: selector not found: {sel}", file=sys.stderr)
                continue
            boxes.append((label, [r["x"], r["y"] - top, r["w"], r["h"]]))
        with open(png_path, "wb") as f:
            f.write(base64.b64decode(shot["data"]))
        return dev["width"], height, boxes, theme
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        shutil.rmtree(prof, ignore_errors=True)

def parse_pairs(items, n):
    out = []
    for it in items or []:
        if ":" not in it:
            sys.exit(f"bad marker '{it}': use LABEL:x,y (or LABEL:x,y,w,h for --box)")
        label, xy = it.split(":", 1)
        try:
            vals = [float(v) for v in xy.split(",")]
        except ValueError:
            sys.exit(f"bad numbers in '{it}'")
        if len(vals) != n:
            sys.exit(f"'{it}' needs {n} numbers")
        out.append((label.strip(), vals))
    return out

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--capture", metavar="URL", help="take the screenshot with headless Chrome (read-only: it only loads and scrolls)")
    src.add_argument("--lighthouse", help="a Lighthouse JSON report (its full-page screenshot is often mid-load: prefer --capture)")
    src.add_argument("--image", help="a PNG, JPEG or WebP screenshot")
    ap.add_argument("--device", choices=["phone", "desktop"], default="phone", help="with --capture")
    ap.add_argument("--wait", type=float, default=3, help="with --capture: seconds after load before the picture (a popup that opens at 6 s needs about 7)")
    ap.add_argument("--selector", help="with --capture: CSS selector of the section to show (default: the first screen)")
    ap.add_argument("--max-height", type=float, default=1400, help="with --capture: tallest band in CSS px")
    ap.add_argument("--mark-el", action="append", help='with --capture: numbered box around an element, "LABEL=css selector"; repeat')
    ap.add_argument("--css-width", type=float, help="with --image: the page width in CSS px when it was taken")
    ap.add_argument("--list", action="store_true", help="list the Lighthouse nodes with their bands, then stop")
    ap.add_argument("--section", help="crop to the Lighthouse node whose id or key contains this text")
    ap.add_argument("--crop", help="TOP:BOTTOM in CSS px")
    ap.add_argument("--pad", type=float, default=0, help="extra CSS px above and below the crop")
    ap.add_argument("--mark", action="append", help='numbered dot, "LABEL:x,y"; repeat')
    ap.add_argument("--box", action="append", help='numbered outline, "LABEL:x,y,w,h"; repeat')
    ap.add_argument("--title", help="caption shown above the picture, e.g. 'CRO-02 · phone · first visit'")
    ap.add_argument("--display-width", type=float, help="width of the SVG on screen (default: the page width, max 720)")
    ap.add_argument("--out", help="the SVG to write")
    a = ap.parse_args()

    extra_boxes = []
    if a.capture:
        if not a.out:
            sys.exit("give --out")
        marks = []
        for m in a.mark_el or []:
            if "=" not in m:
                sys.exit(f"bad --mark-el '{m}': use LABEL=css selector")
            marks.append(tuple(x.strip() for x in m.split("=", 1)))
        png = os.path.splitext(a.out)[0] + ".png"
        os.makedirs(os.path.dirname(os.path.abspath(png)), exist_ok=True)
        cw, ch, extra_boxes, theme = capture(a.capture, a.device, a.wait, a.selector, a.pad, a.max_height, marks, png)
        print(f"Captured: {png} ({a.device}, {cw:g} px wide). Theme on the page: {theme or 'not a Shopify page or not readable'}")
        data, W, H, nodes = from_image(png, cw)
        a.pad = 0
        if not a.crop:
            a.crop = f"0:{H:g}"
    else:
        data, W, H, nodes = from_lighthouse(a.lighthouse) if a.lighthouse else from_image(a.image, a.css_width)

    if a.list:
        print(f"Page: {W:g} x {H:g} CSS px")
        for key, r in sorted(nodes.items(), key=lambda kv: kv[1].get("top", 0)):
            if not r.get("height"):
                continue
            print(f"{r.get('top', 0):>7.0f} to {r.get('bottom', 0):>7.0f}  {key}  id={r.get('id') or '-'}")
        return
    if not a.out:
        sys.exit("give --out (or --list)")

    if a.section:
        hits = [r for k, r in nodes.items() if a.section in k or a.section in (r.get("id") or "")]
        if not hits:
            sys.exit(f"no node matches '{a.section}'; run with --list")
        top, bottom = min(r["top"] for r in hits), max(r["bottom"] for r in hits)
    elif a.crop:
        try:
            top, bottom = (float(v) for v in a.crop.split(":"))
        except ValueError:
            sys.exit("bad --crop: use TOP:BOTTOM")
    else:  # a whole screenshot as given; a Lighthouse full page is cut to its first two screen widths
        top, bottom = 0.0, (min(H, W * 2) if a.lighthouse else H)
    top, bottom = max(0.0, top - a.pad), min(H, bottom + a.pad)
    if bottom <= top:
        sys.exit(f"empty crop {top:g}:{bottom:g} (page is {H:g} tall)")

    r = min(24.0, max(11.0, W / 36))
    cap = r * 2.6 if a.title else 0
    vb_top = top - cap
    vb_h = bottom - top + cap
    dw = a.display_width or min(W, 720)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             f'viewBox="0 {vb_top:g} {W:g} {vb_h:g}" width="{dw:g}" height="{dw * vb_h / W:.0f}" '
             f'font-family="system-ui, -apple-system, Segoe UI, Arial, sans-serif">',
             f'<defs><clipPath id="c"><rect x="0" y="{top:g}" width="{W:g}" height="{bottom - top:g}"/></clipPath></defs>',
             f'<image clip-path="url(#c)" x="0" y="0" width="{W:g}" height="{H:g}" preserveAspectRatio="none" '
             f'href="{data}" xlink:href="{data}"/>',
             f'<rect x="0.5" y="{top:g}" width="{W - 1:g}" height="{bottom - top:g}" fill="none" stroke="#d0d0d0"/>']
    if a.title:
        parts.append(f'<rect x="0" y="{vb_top:g}" width="{W:g}" height="{cap:g}" fill="#111"/>'
                     f'<text x="{r * 0.8:g}" y="{vb_top + cap * 0.64:g}" fill="#fff" font-size="{r * 1.05:g}" '
                     f'font-weight="600">{escape(a.title)}</text>')

    def badge(label, x, y):
        x, y = min(max(x, r), W - r), min(max(y, top + r), bottom - r)
        return (f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{COLOR}" stroke="#fff" stroke-width="{r / 6:g}"/>'
                f'<text x="{x:g}" y="{y + r * 0.36:g}" text-anchor="middle" fill="#fff" font-size="{r * 1.05:g}" '
                f'font-weight="700">{escape(label)}</text>')

    for label, (x, y, w, h) in parse_pairs(a.box, 4) + extra_boxes:
        parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="none" stroke="{COLOR}" '
                     f'stroke-width="{r / 4:g}" rx="{r / 4:g}"/>')
        parts.append(badge(label, x, y))
    for label, (x, y) in parse_pairs(a.mark, 2):
        if not top <= y <= bottom:
            print(f"warning: marker {label} at y={y:g} is outside the crop {top:g}:{bottom:g}", file=sys.stderr)
        parts.append(badge(label, x, y))
    parts.append("</svg>")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as f:
        f.write("\n".join(parts))
    print(f"Written: {a.out} (band {top:.0f} to {bottom:.0f} of {H:.0f} CSS px, {len(a.mark or []) + len(a.box or []) + len(extra_boxes)} markers)")

if __name__ == "__main__":
    main()
