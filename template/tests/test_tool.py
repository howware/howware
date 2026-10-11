"""Tests of the tool against a real, temporary memory. Synthetic data only.

The memory helper is found in HOWWARE_MEMORY_HELPER or in the installed project-memory skill.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = next((ROOT / "skill").glob("*/scripts/*.py"))
BY = "person:test"


def find_helper() -> Path | None:
    for c in (os.environ.get("HOWWARE_MEMORY_HELPER"), Path.home() / ".claude/skills/project-memory/scripts/memory.py"):
        if c and Path(c).is_file():
            return Path(c)
    return None


HELPER = find_helper()


@unittest.skipUnless(HELPER, "project-memory is not installed")
class ToolTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name) / "memory.sqlite")
        subprocess.run([sys.executable, str(HELPER), "--db", self.db, "init", "--owner-name", "Test",
                        "--owner-key", BY], check=True, capture_output=True)
        self.assertTrue(self.tool("setup", "--by", BY)["ok"])

    def tearDown(self):
        self.tmp.cleanup()

    def tool(self, *args: str, code: int = 0) -> dict:
        proc = subprocess.run([sys.executable, str(TOOL), "--mem", str(HELPER), "--db", self.db, "--tz=-06:00", *args],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, code, proc.stdout + proc.stderr)
        return json.loads(proc.stdout)

    def test_record_is_idempotent_and_exact(self):
        first = self.tool("record", "--amount", "0.10", "--description", "a", "--date", "2026-01-05", "--by", BY)
        again = self.tool("record", "--amount", "0.10", "--description", "a", "--date", "2026-01-05", "--by", BY)
        self.assertTrue(first["created"])
        self.assertFalse(again["created"])
        self.tool("record", "--amount", "0.20", "--description", "b", "--date", "2026-01-06", "--by", BY)
        report = self.tool("report", "--since", "2026-01-01", "--until", "2026-02-01")
        self.assertEqual(report["months"], [{"month": "2026-01", "total": "$0.30", "items": 2}])

    def test_refuses_invalid_input(self):
        result = self.tool("record", "--amount", "ten", "--description", "x", "--by", BY, code=2)
        self.assertFalse(result["ok"])


class ContractTest(unittest.TestCase):
    def test_version(self):
        out = subprocess.run([sys.executable, str(TOOL), "--version"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0)
        self.assertIn(".py ", out.stdout)


if __name__ == "__main__":
    unittest.main()
