"""
capcut_helpers.mute — 4-level mute (M29 lesson — `volume=0` alone leaks audio).

M29: CapCut Export 有時即使 segment volume=0 仍把 B-roll 原音混進去。必須 4 處同步：
  1. material.has_audio = false
  2. material.has_sound_separated = true
  3. segment.volume = 0
  4. segment.last_nonzero_volume = 0

Fallback: 若 4-level mute 仍漏 → 走 ffmpeg force-mix BGM 完全 replace audio track。
"""


def mute_all_video_segments(draft: dict) -> tuple[int, int]:
    """Apply 4-level mute to every video segment + its material.

    Returns:
        (n_segments_muted, n_materials_muted)
    """
    materials_video = draft.get("materials", {}).get("videos", [])
    material_by_id = {m["id"]: m for m in materials_video}

    n_segs = 0
    muted_material_ids = set()

    for tr in draft.get("tracks", []):
        if tr.get("type") != "video":
            continue
        for seg in tr.get("segments", []):
            # Segment-level mute
            seg["volume"] = 0.0
            seg["last_nonzero_volume"] = 0.0
            n_segs += 1

            # Material-level mute (one material can back many segments, dedupe)
            mid = seg.get("material_id")
            if mid and mid not in muted_material_ids:
                if mid in material_by_id:
                    mat = material_by_id[mid]
                    mat["has_audio"] = False
                    mat["has_sound_separated"] = True
                    muted_material_ids.add(mid)

    return n_segs, len(muted_material_ids)


def mute_specific_segments(draft: dict, segment_indices: list[int]) -> int:
    """Mute only specific video segments by index (within video track)."""
    materials_video = draft.get("materials", {}).get("videos", [])
    material_by_id = {m["id"]: m for m in materials_video}

    n = 0
    for tr in draft.get("tracks", []):
        if tr.get("type") != "video":
            continue
        for idx, seg in enumerate(tr.get("segments", [])):
            if idx not in segment_indices:
                continue
            seg["volume"] = 0.0
            seg["last_nonzero_volume"] = 0.0
            mid = seg.get("material_id")
            if mid and mid in material_by_id:
                mat = material_by_id[mid]
                mat["has_audio"] = False
                mat["has_sound_separated"] = True
            n += 1
    return n


def audit_mute_state(draft: dict) -> dict:
    """Verify all video segments are properly 4-level muted.

    Returns:
        {
            'total_segments': int,
            'fully_muted': int,
            'partial_muted': list of (seg_idx, missing_level),
            'success_rate': float (0.0-1.0)
        }
    """
    materials_video = draft.get("materials", {}).get("videos", [])
    material_by_id = {m["id"]: m for m in materials_video}

    total = 0
    fully_muted = 0
    partial = []

    for tr in draft.get("tracks", []):
        if tr.get("type") != "video":
            continue
        for idx, seg in enumerate(tr.get("segments", [])):
            total += 1
            issues = []
            if seg.get("volume", 1.0) != 0.0:
                issues.append("seg.volume")
            if seg.get("last_nonzero_volume", 1.0) != 0.0:
                issues.append("seg.last_nonzero_volume")
            mid = seg.get("material_id")
            if mid in material_by_id:
                mat = material_by_id[mid]
                if mat.get("has_audio", True):
                    issues.append("material.has_audio")
                if not mat.get("has_sound_separated", False):
                    issues.append("material.has_sound_separated")
            if not issues:
                fully_muted += 1
            else:
                partial.append((idx, issues))

    return {
        "total_segments": total,
        "fully_muted": fully_muted,
        "partial_muted": partial,
        "success_rate": fully_muted / max(total, 1),
    }
