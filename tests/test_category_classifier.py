import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    name = "generate_enriched_catalog_under_test"
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "generate_enriched_catalog.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class CategoryClassifierTests(unittest.TestCase):
    """The keyword classifier is a heuristic; it must not silently misfile skills.

    Two failure modes are guarded here:
      * a keyword matching inside an unrelated word ("ui" in "quick", "ios" in
        "ratios", "media" in "medians", "vision" in "revision");
      * no keyword matching at all, which used to dump the skill into the
        commerce-ops fallback bucket without anyone noticing.
    """

    def setUp(self):
        self.module = load_module()
        self.enriched = json.loads((ROOT / "catalog" / "skills.enriched.json").read_text(encoding="utf-8"))

    def test_no_silent_commerce_ops_fallback(self):
        """commerce-ops is only reachable through an explicit, reviewed override."""
        m = self.module
        unreviewed = []
        for skill in self.enriched["skills"]:
            if skill["primary_category"] != "commerce-ops":
                continue
            if m.CATEGORY_OVERRIDES.get(skill["id"]) != "commerce-ops":
                unreviewed.append(skill["id"])
        self.assertEqual(unreviewed, [], "commerce-ops must be an explicit override, not a fallback")

    def test_catalog_matches_classifier(self):
        """A stale catalog is a bug: regenerate instead of hand-editing categories."""
        m = self.module
        stale = []
        for skill in self.enriched["skills"]:
            recomputed = m.classify_category(skill["id"], skill.get("description") or "")
            if recomputed != skill["primary_category"]:
                stale.append(f"{skill['id']}: catalog={skill['primary_category']} classifier={recomputed}")
        self.assertEqual(stale, [], "run scripts/generate_enriched_catalog.py")

    def test_overrides_use_known_categories(self):
        m = self.module
        known = {category for category, _ in m.CATEGORY_KEYWORDS}
        known |= {skill["primary_category"] for skill in self.enriched["skills"]}
        known.add("commerce-ops")
        bad = {k: v for k, v in m.CATEGORY_OVERRIDES.items() if v not in known}
        self.assertEqual(bad, {}, "override points at an unknown category")

    def test_boundary_keywords_reject_cross_word_hits(self):
        m = self.module
        cases = [
            ("demo-translate", "translate articles in quick mode", "design-ui"),
            ("demo-ratios", "image generation with aspect ratios", "coding-devtools"),
            ("demo-medians", "benchmark medians and immediate feedback", "media-generation"),
            ("demo-revision", "self-critique, fewer revision rounds", "media-generation"),
            ("demo-scenarios", "usage scenarios for the suite", "coding-devtools"),
            # 逐个核对时实测到的跨词误命中
            ("demo-hunting", "developer psychology and anomaly detection", "coding-devtools"),
            ("demo-redteam", "pull the app from the store developer page", "coding-devtools"),
            ("demo-growth", "marketing copy and content strategy", "finance-trading"),
            ("demo-prompt", "prompt compression for long threads", "media-generation"),
            ("demo-strategy", "strategy designer for swing setups", "design-ui"),
            ("demo-scorecard", "campaign evaluation and reporting", "finance-trading"),
        ]
        for skill_id, description, wrong in cases:
            with self.subTest(skill=skill_id):
                self.assertNotEqual(m.classify_category(skill_id, description), wrong)

    def test_boundary_keywords_still_match_real_terms(self):
        m = self.module
        cases = [
            ("demo-ui", "UI design system for dashboards", "design-ui"),
            ("demo-ios", "iOS app development", "coding-devtools"),
            ("demo-media", "social media image pipeline", "media-generation"),
            ("demo-vision", "computer vision analysis", "media-generation"),
            # 屈折变化必须保留：复数、过去式、-ous 形容词
            ("demo-stocks", "screen stocks for a pullback", "finance-trading"),
            ("demo-images", "generate images for the article", "media-generation"),
            ("demo-tasks", "track tasks and reminders", "productivity-pkm"),
            ("demo-danger", "dangerous permission requests", "security-audit"),
            ("demo-markets", "compare markets across sectors", "finance-trading"),
            ("demo-compressed", "compressed archive of the bundle", "media-generation"),
            ("demo-designed", "designed for reading comfort", "design-ui"),
        ]
        for skill_id, description, expected in cases:
            with self.subTest(skill=skill_id):
                self.assertEqual(m.classify_category(skill_id, description), expected)

    def test_reviewed_families_stay_in_one_category(self):
        """同库同岗：这三个家族整库一个岗位，逐个核对后定死，防止关键词再把它们拆散。"""
        expected = {
            "tradermonty/claude-trading-skills": "finance-trading",
            "elementalsouls/Claude-BugHunter": "security-audit",
            "affaan-m/ECC": "agent-orchestration",
        }
        strays = []
        seen = {repo: 0 for repo in expected}
        for skill in self.enriched["skills"]:
            origin = skill.get("origin") or {}
            url = origin.get("origin_url") or origin.get("mirror_source_url") or ""
            for repo, category in expected.items():
                if f"github.com/{repo}" not in url:
                    continue
                seen[repo] += 1
                if skill["primary_category"] != category:
                    strays.append(f"{skill['id']}: {skill['primary_category']} != {category}")
        self.assertEqual(strays, [], "family member filed under the wrong category")
        self.assertTrue(all(count > 0 for count in seen.values()), f"family vanished from catalog: {seen}")

    def test_block_scalar_frontmatter_headers(self):
        """`>-` / `|-` used to leave the literal header as the description."""
        m = load_module()
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        m.ROOT = Path(tmp.name)
        body = "line one of the description\n  line two of the description\n"
        for header in (">-", ">", "|", "|-", ">+", "|2"):
            skill_dir = m.ROOT / "skills" / "default" / "demo-skill"
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: demo-skill\ndescription: {header}\n  {body}---\n\n# Demo\n",
                encoding="utf-8",
            )
            with self.subTest(header=header):
                parsed = m.parse_frontmatter("demo-skill")
                description = parsed.get("description", "")
                self.assertNotIn(description, {">-", ">", "|", "|-", ">+", "|2"})
                self.assertIn("line one of the description", description)
                self.assertIn("line two of the description", description)


if __name__ == "__main__":
    unittest.main()