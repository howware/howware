"""Install the howware skills into an agent host.

    python tools/install_skills.py                              # ~/.claude/skills
    python tools/install_skills.py --target-dir ~/.codex/skills  # Codex

Installs howware-builder (with the template bundled, so it works outside this repository) and howware-review.
Reinstalling replaces them.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the howware skills")
    parser.add_argument("--target-dir", default=str(Path.home() / ".claude" / "skills"))
    target_dir = Path(parser.parse_args().target_dir).expanduser()
    for name in ("howware-builder", "howware-review"):
        target = target_dir / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(ROOT / "skills" / name, target, ignore=IGNORE)
        if name == "howware-builder":
            shutil.copytree(ROOT / "template", target / "template", ignore=IGNORE)
        print(f"Installed {name} in {target}")
    print("The template's tools need the project-memory skill: https://github.com/howware/long-term-memory-for-AI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
