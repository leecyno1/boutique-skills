import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    name = "upstream_relocation_under_test"
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "check_upstream_updates.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


TREE = {
    "main": [
        "skills/category/new-name/SKILL.md",
        "skills/category/other/SKILL.md",
        "skills/unrelated/SKILL.md",
    ],
    "stable-v1": [
        "skills/legacy-name/SKILL.md",
    ],
}


class RelocationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.skills_dir = Path(cls.tmp.name)
        cls.module.SKILLS_DIR = cls.skills_dir

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self._orig_repo_tree = self.module.repo_tree
        self._orig_candidate_refs = self.module.candidate_refs
        self._orig_list_branches = self.module.list_branches

    def tearDown(self):
        self.module.repo_tree = self._orig_repo_tree
        self.module.candidate_refs = self._orig_candidate_refs
        self.module.list_branches = self._orig_list_branches

    def make_skill(self, skill_id, content=b"same content"):
        path = self.skills_dir / skill_id / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def source(self, skill_id, path):
        return self.module.GitHubSource(
            skill_id, f"https://github.com/o/r/tree/main/{path}", "o", "r", "main", path, False
        )

    def patch_tree(self, refs, shas):
        def fake_repo_tree(source, token, ref):
            return [
                {"path": path, "sha": shas.get(path, "0" * 40)}
                for path in TREE.get(ref, [])
            ]

        def fake_candidate_refs(source, current_ref, token):
            return refs

        self.module.repo_tree = fake_repo_tree
        self.module.candidate_refs = fake_candidate_refs

    def test_version_key_orders_branches(self):
        self.assertEqual(self.module.version_key("taste-skill-v1.9"), (1, 9))
        self.assertEqual(self.module.version_key("v2.5"), (2, 5))
        self.assertEqual(self.module.version_key("main"), (0,))

    def test_candidate_refs_only_stable_or_versioned(self):
        self.module.list_branches = lambda source, token: [
            "main",
            "taste-skill-v1.9",
            "taste-skill-v2",
            "feature/v9",
            "scene-media",
            "stable-2024",
        ]
        refs = self.module.candidate_refs(self.source("x", "skills/x"), "main", None)
        self.assertEqual(refs[0], "main")
        self.assertIn("taste-skill-v2", refs)
        self.assertIn("taste-skill-v1.9", refs)
        self.assertIn("stable-2024", refs)
        self.assertNotIn("feature/v9", refs)
        self.assertNotIn("scene-media", refs)

    def test_content_match_beats_name_match(self):
        local = self.make_skill("demo", b"exact")
        sha = self.module.git_blob_sha_bytes(local.read_bytes())
        self.patch_tree(["main"], {"skills/category/new-name/SKILL.md": sha})
        hit = self.module.find_relocation(self.source("demo", "skills/demo"), None, "main")
        self.assertEqual(hit, ("main", "skills/category/new-name", "content"))

    def test_unique_dir_name_is_used(self):
        self.make_skill("demo")
        self.patch_tree(["main"], {})
        hit = self.module.find_relocation(self.source("demo", "skills/new-name"), None, "main")
        self.assertEqual(hit, ("main", "skills/category/new-name", "name"))

    def test_ambiguous_dir_name_is_not_guessed(self):
        self.make_skill("demo")
        self.patch_tree(["main"], {})
        TREE["main"].append("skills/other-category/new-name/SKILL.md")
        try:
            hit = self.module.find_relocation(self.source("demo", "skills/new-name"), None, "main")
            self.assertIsNone(hit)
        finally:
            TREE["main"].pop()

    def test_same_path_on_version_branch(self):
        self.make_skill("legacy")
        self.patch_tree(["main", "stable-v1"], {})
        hit = self.module.find_relocation(self.source("legacy", "skills/legacy-name"), None, "main")
        self.assertEqual(hit, ("stable-v1", "skills/legacy-name", "path"))


if __name__ == "__main__":
    unittest.main()
