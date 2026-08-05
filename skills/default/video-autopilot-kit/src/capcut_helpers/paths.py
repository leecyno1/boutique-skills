"""
capcut_helpers.paths — Standard CapCut Desktop paths.

⚙️ Auto-detects for the CURRENT user (no hardcoded username). Override any path
   via environment variables (see config.example.py):
       CAPCUT_USER_DATA   CAPCUT_CLI   VIDEO_KIT_PROJECT_ROOT
"""
import os
from pathlib import Path


def _env_path(var: str, default: Path) -> Path:
    """Env override -> else auto-detected default."""
    v = os.environ.get(var)
    return Path(v) if v else default


# ─────────────────────────────────────────────────────────────────────
# CapCut Desktop User Data root (Windows default; override via env)
# ─────────────────────────────────────────────────────────────────────
def _default_capcut_user_data() -> Path:
    """Windows 現值不變；非 Windows 走 platform_compat 偵測
    （Mac = ~/Movies/CapCut/User Data，CapCut/JianyingPro 都試）。
    偵測不到 → 回 Windows 預設值（錯誤留到實際存取時報，跟舊行為一致）。"""
    win_default = Path.home() / "AppData" / "Local" / "CapCut" / "User Data"
    if os.name == "nt":
        return win_default
    try:
        from platform_compat import capcut_drafts_dir
        d = capcut_drafts_dir()  # .../User Data/Projects/com.lveditor.draft
        if d is not None:
            return d.parents[1]  # 上兩層 = User Data
    except ImportError:
        pass
    return win_default


CAPCUT_USER_DATA = _env_path("CAPCUT_USER_DATA", _default_capcut_user_data())
DRAFTS_ROOT = CAPCUT_USER_DATA / "Projects" / "com.lveditor.draft"
EFFECT_CACHE = CAPCUT_USER_DATA / "Cache" / "effect"

# capcut-cli npm shim (Windows .cmd shim); override via env
CAPCUT_CLI = _env_path(
    "CAPCUT_CLI",
    Path.home() / "AppData" / "Roaming" / "npm" / "capcut.cmd",
)

# Your project workspace — defaults to current dir; set VIDEO_KIT_PROJECT_ROOT or config.py
PROJECT_ROOT = _env_path("VIDEO_KIT_PROJECT_ROOT", Path.cwd())
VIDEOS_DIR = PROJECT_ROOT / "videos" / "current"
ASSETS_DIR = PROJECT_ROOT / "assets"
BGM_DIR = ASSETS_DIR / "bgm"
FONTS_DIR = ASSETS_DIR / "fonts"


def draft_path(project_name: str) -> Path:
    """Resolve full path to a CapCut project draft folder."""
    return DRAFTS_ROOT / project_name


def draft_files(project_name: str) -> dict[str, Path]:
    """Resolve the **7 JSON files** that need to stay in sync (M18 lesson).

    CapCut Desktop reads draft_content.json but writes draft_info.json + scatters
    backups in bak/tmp + Timelines/<UUID>/ subfolder. All 7 must match or CapCut
    silently rolls back to oldest version on next open.

    Returns dict { logical_name: Path } — note Timelines/<UUID>/ paths are
    glob-discovered (UUID is per-project so caller iterates).
    """
    d = draft_path(project_name)
    return {
        "root_content": d / "draft_content.json",
        "root_info": d / "draft_info.json",
        "root_content_bak": d / "draft_content.json.bak",
        "root_info_bak": d / "draft_info.json.bak",
        "root_tmp": d / "template-2.tmp",
        "timelines_dir": d / "Timelines",  # iterate subdirs for <UUID>/draft_content.json + bak + tmp
    }


def discover_all_draft_jsons(project_name: str) -> list[Path]:
    """Return all JSON-like files that must stay synced (handles Timelines/<UUID>/ subdirs).

    M18: 7+ files actually:
      - root: draft_content.json + draft_info.json + 2 bak + 1 tmp
      - Timelines/<UUID>/: draft_content.json + draft_content.json.bak + template-2.tmp
    """
    d = draft_path(project_name)
    files = []
    for fname in ("draft_content.json", "draft_info.json",
                  "draft_content.json.bak", "draft_info.json.bak", "template-2.tmp"):
        p = d / fname
        if p.exists():
            files.append(p)
    timelines = d / "Timelines"
    if timelines.exists():
        for sub in timelines.iterdir():
            if sub.is_dir():
                for fname in ("draft_content.json", "draft_content.json.bak", "template-2.tmp"):
                    p = sub / fname
                    if p.exists():
                        files.append(p)
    return files
