"""Create a new howware from the template.

    python new_howware.py --name mantenimiento-auto --description "Car maintenance without an app." --out ~/dev

Copies the template, replaces __NAME__ and __DESCRIPTION__ in paths and contents, and prints the files created
as JSON. Refuses to overwrite an existing folder. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Installed: <skill>/template · In the repository: <repo>/template
TEMPLATE = next((p for p in (HERE.parent / "template", HERE.parents[2] / "template") if p.is_dir()), None)
NAME = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new howware from the template")
    parser.add_argument("--name", required=True, help="kebab-case, e.g. car-maintenance")
    parser.add_argument("--description", required=True, help="One sentence: what it does, for whom")
    parser.add_argument("--out", default=".", help="Folder where the new howware folder is created")
    args = parser.parse_args()
    if TEMPLATE is None:
        print(json.dumps({"ok": False, "error": "template folder not found"}))
        return 3
    if not NAME.match(args.name):
        print(json.dumps({"ok": False, "error": f"name must be kebab-case: {args.name!r}"}))
        return 2
    target = Path(args.out).expanduser().resolve() / args.name
    if target.exists():
        print(json.dumps({"ok": False, "error": f"{target} already exists; not overwriting"}))
        return 2
    description = args.description.strip().replace('"', "'")
    shutil.copytree(TEMPLATE, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for path in sorted(target.rglob("*"), key=lambda p: -len(p.parts)):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace("__NAME__", args.name).replace("__DESCRIPTION__", description),
                            encoding="utf-8")
        if "__NAME__" in path.name:
            path.rename(path.with_name(path.name.replace("__NAME__", args.name)))
    created = sorted(str(p.relative_to(target)).replace("\\", "/") for p in target.rglob("*") if p.is_file())
    print(json.dumps({"ok": True, "path": str(target), "files": created}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
