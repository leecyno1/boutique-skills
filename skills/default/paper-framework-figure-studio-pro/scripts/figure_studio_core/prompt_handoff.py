"""Generic file-reference prompt handoff helpers for v3.2.15b.

Full image prompts are persisted as files. User-visible next prompts should
reference prompt indexes rather than inline long multi-candidate prompts. The
candidate id written into the prompt-index is the source of truth for prompt,
image, registry, artifact, and checkpoint paths.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .identity import (
    assert_path_candidate_id,
    default_candidate_paths,
    normalize_candidate_id,
    normalize_prompt_index,
)


def _as_path(path: str | Path) -> Path:
    return path if isinstance(path, Path) else Path(path)


def save_candidate_prompt(candidate_id: str, prompt_text: str, stage_root: str | Path, *, filename: str = "prompt-v01.md") -> str:
    cid = normalize_candidate_id(candidate_id)
    candidate_dir = _as_path(stage_root) / "candidates" / cid
    candidate_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = candidate_dir / filename
    assert_path_candidate_id(prompt_path.as_posix(), cid, label="candidate prompt path")
    prompt_path.write_text(prompt_text.rstrip() + "\n", encoding="utf-8")
    return prompt_path.as_posix()


def create_prompt_index(
    stage_root: str | Path,
    candidate_ids: Iterable[str],
    *,
    stage: str | None = None,
    substage: str = "IMAGE_GENERATE",
    prompt_filename: str = "prompt-v01.md",
    target_filename: str = "image-v01.png",
    extra_candidate_metadata: Mapping[str, Mapping[str, Any]] | None = None,
) -> str:
    stage_root_path = _as_path(stage_root)
    stage_root_path.mkdir(parents=True, exist_ok=True)
    ids = [normalize_candidate_id(cid) for cid in candidate_ids]
    rows: list[dict[str, Any]] = []
    for cid in ids:
        prompt_path = stage_root_path / "candidates" / cid / prompt_filename
        target_image_path = stage_root_path / "candidates" / cid / target_filename
        row: dict[str, Any] = {
            "candidate_id": cid,
            "prompt_path": assert_path_candidate_id(prompt_path.as_posix(), cid, label=f"{cid}.prompt_path"),
            "target_image_path": assert_path_candidate_id(target_image_path.as_posix(), cid, label=f"{cid}.target_image_path"),
        }
        if extra_candidate_metadata and cid in extra_candidate_metadata:
            row.update(dict(extra_candidate_metadata[cid]))
        rows.append(row)
    index: dict[str, Any] = normalize_prompt_index(
        {
            "schema_version": 2,
            "stage": stage,
            "substage": substage,
            "prompt_mode": "file_reference_handoff",
            "candidate_ids": ids,
            "candidates": rows,
            "image_route_policy": "Codex must use image_gen; ChatGPT web must use Create Image / ChatGPT Images 2.0; other runtimes require a named approved image-generation API. Do not use SVG, Python/PIL, Matplotlib, Graphviz, TikZ, Mermaid, canvas, PPT/PDF rendering, screenshots, or any local raster substitute.",
            "user_visible_policy": "Visible handoff prompts should reference this index and should not inline full prompt bodies.",
            "candidate_id_source_of_truth": "candidate_id in this prompt-index; do not renumber or reinterpret IDs during image generation or registration.",
        },
        stage=stage,
    )
    index_path = stage_root_path / "prompt-index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index_path.as_posix()


def user_visible_handoff(index_path: str | Path, *, mode: str = "IMAGE_GENERATE") -> str:
    index = _as_path(index_path).as_posix()
    return (
        f"进入相应的 {mode} 子阶段。请读取并使用已保存的 prompt-index：\n\n"
        f"{index}\n\n"
        "逐一读取 prompt-index 中每个 candidate 的 prompt_path，并按同一行 candidate_id 生成对应 target_image_path。"
        "不得改写、重排、重命名或猜测 candidate_id；图像、状态、artifact、checkpoint 中的 ID 必须与 prompt-index 完全一致。"
        "必须使用当前 runtime 锁定的图像生成路线：Codex=image_gen；ChatGPT web=Create Image / ChatGPT Images 2.0；其他 runtime=已登记的 approved image-generation API。"
        "禁止用 SVG、Python/PIL、Matplotlib、Graphviz、TikZ、Mermaid、canvas、PPT/PDF 渲染、截图或本地程序化 PNG/WebP 代替生图。"
        "本轮为 image-only：只生成/附加图像；不要写解释、审核、排序、修改建议或下一步提示词。"
    )
