#!/usr/bin/env python3
"""Parse every skill script before the weekly publish.

Upstream sync writes third-party files straight into skills/default. A syntax
error there would be committed and shipped silently because the catalog audit
and the tier tests only look at structure. This gate compiles Python sources in
memory (no bytecode artifacts) and runs `node --check` on JavaScript when node
is available, failing the cycle on the first broken file.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

MIN_PARSER = (3, 12)  # upstream code uses PEP 701 f-strings; older parsers false-positive


def reexec_with_newer_python() -> None:
    """Re-run under a >= 3.12 interpreter when the current one is older."""
    if sys.version_info >= MIN_PARSER or os.environ.get("SKILL_SYNTAX_NO_REEXEC"):
        return
    candidates = ["python3.14", "python3.13", "python3.12", "/opt/homebrew/bin/python3"]
    for name in candidates:
        exe = shutil.which(name) if not name.startswith("/") else (name if Path(name).exists() else None)
        if not exe:
            continue
        probe = subprocess.run([exe, "-c", "import sys; print(sys.version_info >= (3, 12))"], capture_output=True, text=True)
        if probe.stdout.strip() == "True":
            os.environ["SKILL_SYNTAX_NO_REEXEC"] = "1"
            os.execv(exe, [exe, *sys.argv])
    print(f"[WARN] python {sys.version.split()[0]} < 3.12 and no newer interpreter found; PEP 701 f-strings may be reported as errors", file=sys.stderr)

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills" / "default"
NODE_SUFFIXES = {".js", ".mjs", ".cjs"}


def check_python(files):
    errors = []
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"{path}: not valid UTF-8 ({error})")
            continue
        try:
            compile(source, str(path), "exec")
        except SyntaxError as error:
            errors.append(f"{path}:{error.lineno}: {error.msg}")
    return errors


def check_javascript(files, node):
    errors = []
    for path in files:
        try:
            result = subprocess.run(
                [node, "--check", str(path)],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except subprocess.TimeoutExpired:
            errors.append(f"{path}: node --check timed out")
            continue
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip().splitlines()
            errors.append(f"{path}: {detail[0] if detail else 'node --check failed'}")
    return errors


def main() -> int:
    py_files = sorted(SKILLS_DIR.rglob("*.py"))
    js_files = sorted(p for p in SKILLS_DIR.rglob("*") if p.suffix in NODE_SUFFIXES)
    node = shutil.which("node")

    errors = check_python(py_files)
    if js_files and node:
        errors += check_javascript(js_files, node)
    elif js_files and not node:
        print(f"[WARN] node not found; skipped {len(js_files)} JavaScript files")

    print(
        json.dumps(
            {
                "python_files": len(py_files),
                "javascript_files": len(js_files),
                "node": node or None,
                "errors": len(errors),
            },
            ensure_ascii=False,
        )
    )
    for error in errors[:40]:
        print(f"[FAIL] {error}")
    if len(errors) > 40:
        print(f"[FAIL] ... {len(errors) - 40} more")
    return 1 if errors else 0


if __name__ == "__main__":
    reexec_with_newer_python()
    raise SystemExit(main())
