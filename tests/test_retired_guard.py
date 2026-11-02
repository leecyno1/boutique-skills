import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    name = "weekly_curation_under_test"
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "weekly_curation.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class RetiredGuardTests(unittest.TestCase):
    """Retired skills must never be auto re-imported by the weekly discover step."""

    def setUp(self):
        self.module = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.module.SKILLS_DIR = root / "skills"
        self.module.SKILLS_DIR.mkdir()
        self.module.RETIRED_SKILLS = root / "retired.json"
        self.module.RETIRED_SKILLS.write_text(json.dumps({
            "skills": {"brainstorming": {"reason": "harness-native"}},
            "blocked_repos": ["Obra/Superpowers"],
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_load_retired_normalises_repo_case(self):
        ids, repos = self.module.load_retired()
        self.assertEqual(ids, {"brainstorming"})
        self.assertEqual(repos, {"obra/superpowers"})

    def test_register_candidate_skips_retired_id(self):
        m = self.module
        m.collect_skill_files = lambda candidate, remote_path, token: [("skills/x/SKILL.md", 10)]
        candidate = m.Candidate(
            owner="someone", repo="skills", url="https://github.com/someone/skills",
            stars=100, forks=1, pushed_at="2026-10-01T00:00:00Z", description="", topics=[],
            license="MIT", default_branch="main",
        )
        candidate.has_root_skill = False
        candidate.skill_subdirs = ["skills/brainstorming", "skills/fresh-skill"]
        installed = m.register_candidate(candidate, token=None, apply=False)
        self.assertEqual(installed, ["fresh-skill"])

    def test_real_registry_is_consistent(self):
        data = json.loads((ROOT / "catalog" / "retired-skills.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "catalog" / "default-skills.json").read_text(encoding="utf-8"))
        live = {s["id"] for tier in catalog["tiers"].values() for s in tier["skills"]}
        leaked = sorted(set(data["skills"]) & live)
        self.assertEqual(leaked, [], "retired skills must not remain in default-skills.json")
        for skill_id in data["skills"]:
            self.assertFalse((ROOT / "skills" / "default" / skill_id).exists(), skill_id)


if __name__ == "__main__":
    unittest.main()
