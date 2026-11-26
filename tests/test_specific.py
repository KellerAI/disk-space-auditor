import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class DiskAuditorSpecific(unittest.TestCase):
    def test_guard_is_roadmap_not_shipped(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Planned for v0.2, not built", readme)
        self.assertIn("not part of this release", readme)
        self.assertFalse((ROOT / "hooks").exists())

    def test_run_audit_protects_paths_and_requires_exact_approval(self):
        text = (ROOT / "skills" / "run-audit" / "SKILL.md").read_text(encoding="utf-8").lower()
        for needle in ("protected, never touch", "no wildcards", "unpushed commits", "approval on that exact item"):
            self.assertIn(needle, text)

    def test_get_started_defaults_to_always_ask(self):
        text = (ROOT / "skills" / "get-started" / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("default: always ask", text)


if __name__ == "__main__":
    unittest.main()
