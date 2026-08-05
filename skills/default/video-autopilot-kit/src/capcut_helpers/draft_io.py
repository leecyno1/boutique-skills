"""
capcut_helpers.draft_io — Load / save / sync CapCut draft JSON (M18 7-file sync).

關鍵：CapCut Desktop 寫 draft_info.json，讀 draft_content.json，散落 backup 在
.bak / .tmp + Timelines/<UUID>/。任一不同步 → CapCut「載入」時用舊版覆蓋新版改動。
"""
import json
import shutil
from pathlib import Path
from typing import Optional, Union

try:
    from .paths import draft_path, discover_all_draft_jsons
except ImportError:  # 直接 python src/capcut_helpers/draft_io.py 跑 self-test 時
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from capcut_helpers.paths import draft_path, discover_all_draft_jsons

# BOM + whitespace we strip before sniffing the first structural byte
_JSON_HEAD_STRIP = b"\xef\xbb\xbf \t\r\n"

_ENCRYPTED_DRAFT_MSG = """\
Draft file is NOT plaintext JSON (binary header) — this draft is most likely ENCRYPTED: {path}

Known version boundary (community-documented, verify on your install):
  - Jianying Pro (CN, JianyingPro) 6.0+ stores draft_content.json as AES-encrypted binary.
    5.9.x is the last plaintext line. There is NO official decryption/bypass.
  - CapCut international builds (6.x-9.x, incl. 8.9 verified locally) remain plaintext JSON.

Two ways forward:
  1) Switch to a compatible version: use CapCut international, or pin JianyingPro
     to 5.9.x and block auto-update. (Exporting a project from Jianying 6.0+ can
     also yield a plaintext variant.)
  2) Skip draft editing entirely and use the programmatic path (ffmpeg pipeline,
     e.g. Path E in knowledge/capcut-automation-sop.md) — it never touches drafts.

Run capcut_helpers.detect_draft_format(r'{path}') for a machine-readable report.
See TROUBLESHOOTING.md > 'CapCut version compatibility & Mac' for the full matrix."""


def detect_draft_format(path: Union[str, Path]) -> dict:
    """Detect whether a CapCut / Jianying draft is plaintext JSON (editable) or encrypted.

    Args:
        path: any of
            - a draft **folder** (containing draft_content.json / draft_info.json —
              the second name is the macOS-primary variant, community reported)
            - a direct path to a draft JSON file
            - a bare **project name** (resolved under DRAFTS_ROOT)

    Returns:
        {
            'encrypted':    bool,        # True = binary header (Jianying CN 6.0+ AES style)
            'version_hint': str | None,  # e.g. 'version=360000, new_version=169.x' when parseable
            'editable':     bool,        # True = plaintext JSON, safe for direct edit
            'file':         str,         # the file actually inspected
        }
    """
    p = Path(path)
    if not p.exists():
        # Maybe caller passed a project name — resolve under DRAFTS_ROOT
        candidate = draft_path(str(path))
        if candidate.exists():
            p = candidate
        else:
            raise FileNotFoundError(f"No draft file/folder/project found for: {path}")
    if p.is_dir():
        for fname in ("draft_content.json", "draft_info.json"):
            f = p / fname
            if f.exists():
                p = f
                break
        else:
            raise FileNotFoundError(
                f"Neither draft_content.json nor draft_info.json found under: {p}"
            )

    raw = p.read_bytes()
    head = raw.lstrip(_JSON_HEAD_STRIP)
    if not head.startswith(b"{"):
        return {
            "encrypted": True,
            "version_hint": ("binary header, not JSON — matches Jianying CN 6.0+ "
                             "AES-encrypted drafts (5.9.x was the last plaintext line)"),
            "editable": False,
            "file": str(p),
        }
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {
            "encrypted": False,
            "version_hint": "starts with '{' but is not valid JSON (corrupt / truncated)",
            "editable": False,
            "file": str(p),
        }

    hints = []
    if isinstance(data, dict):
        if "version" in data:
            hints.append(f"version={data['version']}")
        if "new_version" in data:
            hints.append(f"new_version={data['new_version']}")
    return {
        "encrypted": False,
        "version_hint": ", ".join(hints) if hints else None,
        "editable": True,
        "file": str(p),
    }


def load_draft(project_name: str) -> dict:
    """Load draft_content.json (the canonical UI-visible state).

    Raises:
        FileNotFoundError: draft_content.json missing.
        ValueError: draft exists but is encrypted (Jianying CN 6.0+) or not valid
            JSON — the message explains the version boundary and the two ways
            forward (compatible version / programmatic path).
    """
    p = draft_path(project_name) / "draft_content.json"
    if not p.exists():
        raise FileNotFoundError(f"draft_content.json not found at {p}")
    raw = p.read_bytes()
    if not raw.lstrip(_JSON_HEAD_STRIP).startswith(b"{"):
        raise ValueError(_ENCRYPTED_DRAFT_MSG.format(path=p))
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ValueError(
            f"draft_content.json at {p} starts with '{{' but failed to parse as JSON "
            f"({e}). File may be corrupt or partially written — restore from .bak or "
            f"the _backup_<project> folder, or run detect_draft_format() for details."
        ) from e


def save_draft_with_sync(project_name: str, draft: dict, backup: bool = True) -> list[Path]:
    """Save draft to root + sync to all 7 locations (M18 fix).

    Args:
        project_name: CapCut project folder name
        draft: dict to save as JSON
        backup: If True, save current root → .bak before overwriting (safety net)

    Returns:
        list of paths written
    """
    d = draft_path(project_name)
    root_content = d / "draft_content.json"
    root_info = d / "draft_info.json"

    # Optional backup before write
    if backup and root_content.exists():
        backup_dir = d.parent / f"_backup_{project_name}"
        backup_dir.mkdir(exist_ok=True)
        import time
        ts = time.strftime("%Y%m%d_%H%M%S")
        shutil.copy(root_content, backup_dir / f"draft_content_{ts}.json")

    # Serialize once (separators=(",",":") matches CapCut's compact format)
    blob = json.dumps(draft, ensure_ascii=False, separators=(",", ":"))

    written = []
    # Write root_content (the file CapCut reads)
    root_content.write_text(blob, encoding="utf-8")
    written.append(root_content)

    # Sync to root_info (the file capcut-cli writes — keep matching)
    root_info.write_text(blob, encoding="utf-8")
    written.append(root_info)

    # Sync to Timelines/<UUID>/draft_content.json (per-timeline subfolder)
    timelines = d / "Timelines"
    if timelines.exists():
        for sub in timelines.iterdir():
            if sub.is_dir():
                tl_dc = sub / "draft_content.json"
                if tl_dc.exists():
                    tl_dc.write_text(blob, encoding="utf-8")
                    written.append(tl_dc)

    return written


def set_canvas_portrait(draft: dict, width: int = 1080, height: int = 1920) -> dict:
    """M46 fix — capcut-cli init 預設 canvas 1920×1080 landscape，
    portrait source (rotation=-90) export 出來會 letterboxed 在 landscape frame。
    必須 explicit 改 canvas_config 為 portrait。

    Args:
        draft: full draft dict
        width / height: 預設 1080×1920 (Shorts portrait)

    Returns: the modified canvas_config dict
    """
    cfg = draft.setdefault("canvas_config", {})
    cfg["width"] = width
    cfg["height"] = height
    cfg["ratio"] = "9:16" if width < height else "16:9"
    return cfg


def set_canvas_landscape(draft: dict, width: int = 1920, height: int = 1080) -> dict:
    """Set canvas to landscape (長片 / YT 長片 / IG square 等)."""
    cfg = draft.setdefault("canvas_config", {})
    cfg["width"] = width
    cfg["height"] = height
    cfg["ratio"] = "16:9" if width > height else "1:1" if width == height else "9:16"
    return cfg


def auto_set_canvas(draft: dict, layout: str) -> dict:
    """One-shot canvas setter based on routing decision.

    Args:
        layout: 'portrait' / 'landscape' / 'mixed' (defaults to portrait for safety)
    """
    if layout == "landscape":
        return set_canvas_landscape(draft)
    # portrait default (also for 'mixed' — safer to render portrait)
    return set_canvas_portrait(draft)


def verify_sync(project_name: str) -> dict:
    """Verify all draft JSON copies are identical (M18 health check).

    Returns:
        {
            'all_synced': bool,
            'files_checked': int,
            'mismatched': list[Path],
            'reference_size': int,
        }
    """
    files = discover_all_draft_jsons(project_name)
    json_files = [f for f in files if f.suffix == ".json" and not f.suffix.endswith(".bak")]

    if not json_files:
        return {"all_synced": False, "files_checked": 0, "mismatched": [], "reference_size": 0}

    ref = json_files[0].read_bytes()
    ref_size = len(ref)
    mismatched = []
    for f in json_files[1:]:
        if f.read_bytes() != ref:
            mismatched.append(f)

    return {
        "all_synced": len(mismatched) == 0,
        "files_checked": len(json_files),
        "mismatched": mismatched,
        "reference_size": ref_size,
    }


# ─────────────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────────────


def _self_test():
    """Self-test detect_draft_format() + load_draft() error paths (ASCII-only output)."""
    import os
    import tempfile

    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # Case 1: plaintext draft folder -> editable
        d1 = root / "plain-draft"
        d1.mkdir()
        (d1 / "draft_content.json").write_text(
            json.dumps({"id": "x", "version": 360000, "new_version": "169.0.0",
                        "materials": {}, "tracks": []}, separators=(",", ":")),
            encoding="utf-8")
        r = detect_draft_format(d1)
        assert r["editable"] and not r["encrypted"], r
        assert "version=360000" in r["version_hint"], r
        print("[OK] 1 plaintext folder -> editable, hint:", r["version_hint"])
        passed += 1

        # Case 2: encrypted (binary header) -> not editable, clear flag
        d2 = root / "enc-draft"
        d2.mkdir()
        (d2 / "draft_content.json").write_bytes(b"\x8a\x03\xff\x00AESBLOB....")
        r = detect_draft_format(d2)
        assert r["encrypted"] and not r["editable"], r
        print("[OK] 2 binary header -> encrypted=True, editable=False")
        passed += 1

        # Case 3: starts with '{' but corrupt -> not encrypted, not editable
        f3 = root / "corrupt.json"
        f3.write_text('{"id": "x", "tracks": [', encoding="utf-8")
        r = detect_draft_format(f3)
        assert not r["encrypted"] and not r["editable"], r
        print("[OK] 3 corrupt JSON -> encrypted=False, editable=False")
        passed += 1

        # Case 4: macOS-style folder (draft_info.json only) still detected
        d4 = root / "mac-draft"
        d4.mkdir()
        (d4 / "draft_info.json").write_text('{"version": 360000}', encoding="utf-8")
        r = detect_draft_format(d4)
        assert r["editable"] and r["file"].endswith("draft_info.json"), r
        print("[OK] 4 draft_info.json-only folder (mac naming) -> detected")
        passed += 1

        # Case 5: load_draft raises ValueError with guidance on encrypted draft
        os.environ["CAPCUT_USER_DATA"] = str(root / "User Data")
        # paths.py binds DRAFTS_ROOT at import; patch module-level for the test
        import capcut_helpers.paths as _paths
        old_root = _paths.DRAFTS_ROOT
        try:
            _paths.DRAFTS_ROOT = root
            import capcut_helpers.draft_io as _dio
            old_dp = _dio.draft_path
            _dio.draft_path = lambda name: root / name
            try:
                _dio.load_draft("enc-draft")
                raise AssertionError("load_draft should have raised ValueError")
            except ValueError as e:
                msg = str(e)
                assert "ENCRYPTED" in msg and "5.9" in msg and "programmatic" in msg, msg
                print("[OK] 5 load_draft(encrypted) -> ValueError with version guidance")
                passed += 1
            finally:
                _dio.draft_path = old_dp
        finally:
            _paths.DRAFTS_ROOT = old_root
            os.environ.pop("CAPCUT_USER_DATA", None)

    print(f"[OK] draft_io self-test: {passed}/5 green")


if __name__ == "__main__":
    _self_test()
