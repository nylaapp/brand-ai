#!/usr/bin/env python3
"""Send one local image to a Shopify staged-upload target, and print the resourceUrl to use in fileCreate.

    python3 upload_staged.py --target target.json --file image.jpg [--dry-run]

`target.json` is one object from the `stagedTargets` list that the Admin API's stagedUploadsCreate mutation returns:
{"url": "...", "resourceUrl": "...", "parameters": [{"name": "...", "value": "..."}]}. The script posts the file to `url`
with every parameter as a form field (the file field comes last, as Shopify requires), checks for HTTP 200/201/204, and
prints the resourceUrl. It never prints or stores credentials: the target's signed parameters are single-use.
Python 3 standard library plus the system `curl`. Exit codes: 0 uploaded, 2 bad input, 3 upload refused.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--target", required=True); ap.add_argument("--file", required=True); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        t = json.loads(Path(a.target).read_text(encoding="utf-8"))
        url, res, params = t["url"], t["resourceUrl"], t["parameters"]
    except Exception as e:
        print(f"bad target file: {e}", file=sys.stderr); return 2
    f = Path(a.file)
    if not f.is_file():
        print(f"no such file: {f}", file=sys.stderr); return 2
    cmd = ["curl", "-sS", "-m", "120", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST"]
    for p in params:
        cmd += ["-F", f"{p['name']}={p['value']}"]
    cmd += ["-F", f"file=@{f}", url]
    if a.dry_run:
        shown = [c if not c.startswith(("x-goog-signature", "Signature", "policy")) else c.split("=")[0] + "=<hidden>" for c in cmd]
        print("would run:", " ".join(shown)); print(res); return 0
    if not shutil.which("curl"):
        print("curl is required for the multipart upload", file=sys.stderr); return 2
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=150)
    code = r.stdout.strip()
    if r.returncode != 0 or code not in ("200", "201", "204"):
        print(f"upload refused: HTTP {code or '?'} {r.stderr.strip()[:200]}", file=sys.stderr); return 3
    print(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
