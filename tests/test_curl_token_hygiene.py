import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_weekly_curation():
    spec = importlib.util.spec_from_file_location(
        "weekly_curation_under_test", ROOT / "scripts" / "weekly_curation.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CurlTokenHygieneTests(unittest.TestCase):
    """The curl transport fallback must never put the token in argv."""

    @classmethod
    def setUpClass(cls):
        cls.module = load_weekly_curation()

    def fetch_with_captured_argv(self, token):
        captured = {}

        class Result:
            stdout = b"{}\n200"
            stderr = b""
            returncode = 0

        def fake_run(command, **kwargs):
            captured["argv"] = command
            captured["input"] = kwargs.get("input")
            return Result()

        original = self.module.subprocess.run
        self.module.subprocess.run = fake_run
        try:
            status, _ = self.module._curl_fetch(
                "https://api.github.com/repos/a/b",
                token,
                accept="application/vnd.github+json",
            )
        finally:
            self.module.subprocess.run = original
        return status, captured

    def test_token_is_passed_over_stdin_not_argv(self):
        token = "SECRET_TOKEN_DO_NOT_LEAK"
        status, captured = self.fetch_with_captured_argv(token)
        self.assertEqual(status, 200)
        self.assertNotIn(token, " ".join(captured["argv"]))
        self.assertIn("--config", captured["argv"])
        self.assertIn(token, (captured["input"] or b"").decode("utf-8"))

    def test_header_values_are_escaped_for_curl_config(self):
        escaped = self.module._curl_config_escape('a"b\\c')
        self.assertEqual(escaped, 'a\\"b\\\\c')

    def test_fetch_without_headers_skips_stdin_config(self):
        captured = {}

        class Result:
            stdout = b"{}\n200"
            stderr = b""
            returncode = 0

        def fake_run(command, **kwargs):
            captured["argv"] = command
            captured["input"] = kwargs.get("input")
            return Result()

        original = self.module.subprocess.run
        self.module.subprocess.run = fake_run
        try:
            self.module._curl_fetch("https://example.com/SKILL.md", None)
        finally:
            self.module.subprocess.run = original
        self.assertNotIn("--config", captured["argv"])
        self.assertEqual(captured["input"], b"")


if __name__ == "__main__":
    unittest.main()
