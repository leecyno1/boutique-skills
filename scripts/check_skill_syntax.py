#!/usr/bin/env python3
"""Parse every skill script before the weekly publish.

Upstream sync writes third-party files straight into skills/default. A syntax
error there would be committed and shipped silently because the catalog audit
and the tier tests only look at structure. This gate compiles Python sources in
memory (no bytecode artifacts) and runs `node --check` on JavaScript when node
is available, failing the cycle on the first broken file.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

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
    raise SystemExit(main())
