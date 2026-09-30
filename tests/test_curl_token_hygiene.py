import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Both scripts carry their own copy of the curl transport fallback.
TRANSPORT_SCRIPTS = ("weekly_curation.py", "check_upstream_updates.py")


def load_module(filename):
    name = f"transport_under_test_{Path(filename).stem}"
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class CurlTokenHygieneTests(unittest.TestCase):
    """The curl transport fallback must never put the token in argv."""

    @classmethod
    def setUpClass(cls):
        cls.modules = {name: load_module(name) for name in TRANSPORT_SCRIPTS}

    def fetch_with_captured_argv(self, module, token):
        captured = {}

        class Result:
            stdout = b"{}\n200"
            stderr = b""
            returncode = 0

        def fake_run(command, **kwargs):
            captured["argv"] = command
            captured["input"] = kwargs.get("input")
            return Result()

        original = module.subprocess.run
        module.subprocess.run = fake_run
        try:
            status, _ = module._curl_fetch(
                "https://api.github.com/repos/a/b",
                token,
                accept="application/vnd.github+json",
            )
        finally:
            module.subprocess.run = original
        return status, captured

    def test_token_is_passed_over_stdin_not_argv(self):
        token = "SECRET_TOKEN_DO_NOT_LEAK"
        for name, module in self.modules.items():
            with self.subTest(script=name):
                status, captured = self.fetch_with_captured_argv(module, token)
                self.assertEqual(status, 200)
                self.assertNotIn(token, " ".join(captured["argv"]))
                self.assertIn("--config", captured["argv"])
                self.assertIn(token, (captured["input"] or b"").decode("utf-8"))

    def test_header_values_are_escaped_for_curl_config(self):
        for name, module in self.modules.items():
            with self.subTest(script=name):
                self.assertEqual(module._curl_config_escape('a"b\\c'), 'a\\"b\\\\c')

    def test_fetch_without_headers_skips_stdin_config(self):
        module = self.modules[TRANSPORT_SCRIPTS[0]]
        captured = {}

        class Result:
            stdout = b"{}\n200"
            stderr = b""
            returncode = 0

        def fake_run(command, **kwargs):
            captured["argv"] = command
            captured["input"] = kwargs.get("input")
            return Result()

        original = module.subprocess.run
        module.subprocess.run = fake_run
        try:
            module._curl_fetch("https://example.com/SKILL.md", None)
        finally:
            module.subprocess.run = original
        self.assertNotIn("--config", captured["argv"])
        self.assertEqual(captured["input"], b"")


if __name__ == "__main__":
    unittest.main()
