#!/usr/bin/env python3
"""Save or restore the theme files a campaign changes, so it can be reverted exactly.

  python snapshot.py save    <theme-folder> <campaign-folder> <relative-file> [...]
  python snapshot.py restore <theme-folder> <campaign-folder>
  python snapshot.py diff    <theme-folder> <campaign-folder>

save copies each file to <campaign-folder>/before/<relative-file> and writes manifest.json (paths, sha256, date).
restore copies them back over the theme folder (only the files in the manifest).
diff lists which saved files differ from the theme folder now (to spot edits made after the campaign started).
Standard library only.
"""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(theme: Path, camp: Path, files):
    before = camp / "before"
    entries = []
    for rel in files:
        src = theme / rel
        if not src.is_file():
            sys.exit(f"not found: {src}")
        dst = before / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        entries.append({"path": rel.replace("\\", "/"), "sha256": sha(src)})
    manifest = {"saved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "theme_folder": str(theme), "files": entries}
    (camp / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"saved {len(entries)} file(s) to {before}")


def load(camp: Path):
    m = camp / "manifest.json"
    if not m.is_file():
        sys.exit(f"no manifest at {m}")
    return json.loads(m.read_text(encoding="utf-8"))


def restore(theme: Path, camp: Path):
    for e in load(camp)["files"]:
        src = camp / "before" / e["path"]
        dst = theme / e["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"restored {e['path']}")


def diff(theme: Path, camp: Path):
    for e in load(camp)["files"]:
        cur = theme / e["path"]
        state = "missing" if not cur.is_file() else ("unchanged" if sha(cur) == e["sha256"] else "changed since snapshot")
        print(f"{e['path']}: {state}")


def main():
    cmd, theme, camp = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    if cmd == "save":
        if len(sys.argv) < 5:
            sys.exit("save needs at least one file")
        camp.mkdir(parents=True, exist_ok=True)
        save(theme, camp, sys.argv[4:])
    elif cmd == "restore":
        restore(theme, camp)
    elif cmd == "diff":
        diff(theme, camp)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main()
