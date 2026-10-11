"""The template scaffolds a working howware, the skills install, and the repository holds no private data."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = ROOT / "skills" / "howware-builder" / "scripts" / "new_howware.py"
sys.path.insert(0, str(ROOT / "tools"))
import check_private_data as guard  # noqa: E402


def run(*args: str, cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8")


class TemplateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def scaffold(self, name: str = "car-maintenance") -> Path:
        proc = run(str(NEW), "--name", name, "--description", "Car maintenance without an app.", "--out", str(self.out))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return Path(json.loads(proc.stdout)["path"])

    def test_scaffold_replaces_every_placeholder(self):
        project = self.scaffold()
        leftovers = [p for p in project.rglob("*") if "__NAME__" in str(p)
                     or (p.is_file() and ("__NAME__" in p.read_text(encoding="utf-8")
                                          or "__DESCRIPTION__" in p.read_text(encoding="utf-8")))]
        self.assertEqual(leftovers, [])
        manifest = json.loads((project / "howware.json").read_text(encoding="utf-8"))
        for field in ("howware", "name", "version", "description", "license", "hosts", "skill", "tools", "memory",
                      "privacy"):
            self.assertIn(field, manifest)
        self.assertTrue((project / manifest["skill"] / "SKILL.md").is_file())

    def test_scaffold_refuses_bad_names_and_overwrites(self):
        self.assertNotEqual(run(str(NEW), "--name", "Bad Name", "--description", "x", "--out", str(self.out)).returncode, 0)
        self.scaffold()
        self.assertNotEqual(run(str(NEW), "--name", "car-maintenance", "--description", "x",
                                "--out", str(self.out)).returncode, 0)

    def test_scaffolded_howware_passes_its_own_tests(self):
        helper = os.environ.get("HOWWARE_MEMORY_HELPER") or str(ROOT.parent / "long-term-memory-for-AI" / "db" / "memory.py")
        if not Path(helper).is_file():
            self.skipTest("project-memory helper not found")
        project = self.scaffold()
        proc = run("-m", "unittest", "discover", "-s", "tests", cwd=project,
                   env={**os.environ, "HOWWARE_MEMORY_HELPER": helper})
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("OK", proc.stderr)

    def test_skills_install_with_bundled_template(self):
        proc = run(str(ROOT / "tools" / "install_skills.py"), "--target-dir", str(self.out / "skills"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        installed = self.out / "skills" / "howware-builder"
        self.assertTrue((installed / "template" / "howware.json").is_file())
        proc = run(str(installed / "scripts" / "new_howware.py"), "--name", "from-installed",
                   "--description", "x", "--out", str(self.out))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


class RepositoryTest(unittest.TestCase):
    def test_no_private_data(self):
        files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts]
        self.assertEqual([f for p in files for f in guard.findings(p.relative_to(ROOT))], [])


if __name__ == "__main__":
    unittest.main()
