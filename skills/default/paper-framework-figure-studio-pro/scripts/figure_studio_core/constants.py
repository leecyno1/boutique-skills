"""Stable public constants and schema values for paper-framework-figure-studio-pro v3.2.15b."""

from __future__ import annotations

from pathlib import Path
import re

SKILL_NAME = "paper-framework-figure-studio-pro"
SKILL_VERSION = "3.2.15b"
SCHEMA_VERSION = 1
DEFAULT_ROOT = "figure-studio-runs"
STATE_RELATIVE_PATH = Path("state") / "project-state.json"

PREFERENCE_REFERENCE_ROOT = "inputs/preference-reference-images"
PREFERENCE_ANALYSIS_PATH = "outputs/S0-paper-foundation/preference-reference-analysis.md"

SAFE_PROJECT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
SECRET_KEY_RE = re.compile(r"(api[_-]?key|token|secret|password|credential)", re.I)

REFERENCE_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TARGET_RASTER_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TARGET_RASTER_IMAGE_STEPS = {
    "S2-SKETCH-EXPLORE",
    "S5-CANDIDATE-IMAGE",
}
TARGET_RASTER_REFERENCE_ROLES = {
    "s2.primary_sketch",
    "s5.primary_candidate",
}
FORBIDDEN_TARGET_IMAGE_KINDS = {"svg", "html", "mermaid", "canvas", "pptx", "pdf"}
FORBIDDEN_TARGET_IMAGE_EXTS = {".svg", ".html", ".htm", ".mmd", ".pptx", ".pdf"}
RUNTIME_ENVIRONMENTS = {"unknown", "chatgpt_web", "codex", "claude_code", "other"}
IMAGE_GENERATION_ROUTES = {
    "unknown",
    "chatgpt_create_image",
    "codex_image_gen",
    "codex_imagegen",  # alias accepted only for migration; new state writes codex_image_gen.
    "approved_image_api",
    "user_supplied_api_required",
}
IMAGE_GENERATION_EVENT_GENERATORS = {"image_gen", "imagegen", "create-image", "approved-image-api"}

CANDIDATE_STATUS_VALUES = {
    "PASS",
    "FLAG_MINOR",
    "FLAG_MAJOR",
    "BLOCKED",
    "PENDING",
    "MISSING",
    "NEEDS_REVIEW",
    "ISSUE_LEDGER_READY",
    "HAS_ISSUES",
    "HAS_BLOCKER_ISSUE",
    "NEEDS_HUMAN_SELECTION",
}
SUBSTAGE_STATUS_VALUES = {"pending", "in_progress", "complete", "blocked", "stale"}
SUBSTAGE_MODES = {"IMAGE_GENERATE"}
SUBSTAGE_STEPS = {"S2-SKETCH-EXPLORE", "S5-CANDIDATE-IMAGE"}
GUIDANCE_STEPS = {"S2-SKETCH-EXPLORE", "S5-CANDIDATE-IMAGE"}

DEFAULT_CANDIDATE_COUNT_BY_STEP = {"S2-SKETCH-EXPLORE": 8, "S5-CANDIDATE-IMAGE": 6}
# Absolute public second-round/formal-candidate cap. S4 may expand beyond the
# default six only up to this value; if preference/style coverage cannot fit,
# S4 must repair/replan or redo before S5 handoff rather than creating more rows.
MAX_SECOND_ROUND_CANDIDATES = 8
MAX_CANDIDATE_COUNT_BY_STEP = {"S2-SKETCH-EXPLORE": 12, "S5-CANDIDATE-IMAGE": MAX_SECOND_ROUND_CANDIDATES}
CHATGPT_WEB_IMAGE_CHUNK_LIMIT = 8
CHATGPT_WEB_RECOMMENDED_IMAGE_CHUNK_SIZE = 8
CODEX_IMAGE_CHUNK_LIMIT = 8

FIRST_ROUND_DEFAULT_STYLE_ID = "formal_publication_schematic"
FIRST_ROUND_STYLE_OPTIONS = [
    {
        "id": "formal_publication_schematic",
        "label_zh": "正式出版风格",
        "meaning": "Default polished academic framework schematic suitable for publication-style first-round comparison, while remaining a candidate direction rather than the final chosen figure.",
    },
    {
        "id": "low_fidelity_sketch",
        "label_zh": "低保真草图",
        "meaning": "Rough exploratory framework sketch with whiteboard/wireframe feel and sparse labels.",
    },
    {"id": "whiteboard_wireframe", "label_zh": "白板线框", "meaning": "Very rough boxes, arrows, grouping, and layout structure."},
    {"id": "clean_flat_minimal_line", "label_zh": "干净扁平极简线稿", "meaning": "Cleaner line-art while still exploratory, not final-polished."},
    {"id": "formal_schematic_layout_study", "label_zh": "正式 schematic 布局草案", "meaning": "Ordered schematic grammar for layout testing, still not final."},
    {"id": "precision_blueprint_light", "label_zh": "轻量蓝图精密稿", "meaning": "Grid/port/routing emphasis for high arrow-risk papers."},
    {"id": "scientific_editorial_light", "label_zh": "轻量科学插画", "meaning": "Light scientific editorial treatment with restrained texture."},
    {"id": "interface_metaphor_light", "label_zh": "轻量界面隐喻", "meaning": "UI/control-board metaphor only when it clarifies paper mechanisms."},
    {"id": "isometric_structure_light", "label_zh": "轻量等距结构", "meaning": "Mild dimensional structure only when connectors and labels stay clear."},
    {"id": "infographic_board_light", "label_zh": "轻量信息图板", "meaning": "Compact explanation board with explicit density/caption budget."},
    {"id": "hand_drawn_storyboard", "label_zh": "手绘故事板", "meaning": "Narrative storyboard only with a close story-to-paper bridge."},
    {
        "id": "acm_ieee_aaai_line_art_schematic",
        "label_zh": "ACM/IEEE/AAAI 双栏论文 line-art schematic",
        "meaning": "Optional first-round publication-line-art surface. Use only when explicitly requested in the S1 user request before S1 finalizes S2 prompt packages.",
    },
]
FIRST_ROUND_STYLE_USER_REMINDER = (
    "非复制表面风格提示：第一轮 S2 默认表面风格为正式出版风格；这只约束渲染表面，不等同于候选图的叙事、布局或处理方案。"
    "若要修改，请在下一轮 S1 请求中另行明确写入表面风格选择或取消默认表面风格；请不要把本说明复制进默认提示词块。"
    "可写例如“第一轮采用 ACM/IEEE/AAAI 双栏论文 line-art schematic 表面风格”，也可以写“取消默认表面风格，请 S1 根据论文实际需要自行设置表面风格”。"
    "可选表面风格包括：正式出版风格、低保真草图、白板线框、"
    "干净扁平极简线稿、正式 schematic 布局草案、轻量蓝图精密稿、轻量科学插画、轻量界面隐喻、"
    "轻量等距结构、轻量信息图板、手绘故事板、ACM/IEEE/AAAI 双栏论文 line-art schematic。"
)
S1_TO_S2_STYLE_OPTIONS_REMINDER = (
    "非复制表面风格提示：第一轮 S2 默认表面风格为正式出版风格，除非 S1 已在 prompt-index 中记录了显式覆盖或取消默认表面风格；"
    "S2 只会按该记录生成图片。若想在运行 S2 前修改第一轮表面风格，需要回到 S1 重做 prompt packages，而不是改 S2 生图提示词。"
    "可选表面风格包括：正式出版风格、低保真草图、白板线框、干净扁平极简线稿、正式 schematic 布局草案、"
    "轻量蓝图精密稿、轻量科学插画、轻量界面隐喻、轻量等距结构、轻量信息图板、手绘故事板、"
    "ACM/IEEE/AAAI 双栏论文 line-art schematic。可在重新执行 S1 时另行写入例如“第一轮采用 轻量蓝图精密稿 表面风格”"
    "或“取消默认表面风格，请 S1 根据论文实际需要自行设置表面风格”。"
)

SECOND_ROUND_STYLE_OPTIONS = [
    {
        "id": "formal_publication_schematic",
        "label_zh": "正式出版风格",
        "meaning": "Default formal publication schematic surface for S5 candidates.",
        "style_family": "publication_schematic",
    },
    {
        "id": "clean_flat_minimal_line",
        "label_zh": "干净扁平极简线稿",
        "meaning": "Clean flat line-art surface for formal candidates with minimal ornament.",
        "style_family": "minimal_line_art",
    },
    {
        "id": "precision_blueprint_light",
        "label_zh": "轻量蓝图精密稿",
        "meaning": "Light blueprint/grid/port/routing treatment for arrow-risk formal candidates.",
        "style_family": "precision_blueprint",
    },
    {
        "id": "scientific_editorial_light",
        "label_zh": "轻量科学插画",
        "meaning": "Restrained scientific editorial treatment while preserving modular semantics.",
        "style_family": "scientific_editorial",
    },
    {
        "id": "interface_metaphor_light",
        "label_zh": "轻量界面隐喻",
        "meaning": "Light UI/control-board metaphor only when it clarifies the paper mechanism.",
        "style_family": "interface_metaphor",
    },
    {
        "id": "isometric_structure_light",
        "label_zh": "轻量等距结构",
        "meaning": "Mild dimensional structure only when connectors and labels remain clear.",
        "style_family": "isometric_structure",
    },
    {
        "id": "infographic_board_light",
        "label_zh": "轻量信息图板",
        "meaning": "Compact explanatory board with explicit density and caption-burden control.",
        "style_family": "infographic_board",
    },
    {
        "id": "acm_ieee_aaai_line_art_schematic",
        "label_zh": "ACM/IEEE/AAAI 双栏论文 line-art schematic",
        "meaning": "Optional publication-line-art surface; inject the dedicated ACM/IEEE/AAAI style block when active.",
        "style_family": "publication_line_art",
        "reference": "references/acm-ieee-aaai-line-art-schematic-style-policy-v3215c.md",
        "prompt_injection_required": True,
    },
]
SECOND_ROUND_STYLE_USER_REMINDER = (
    "可选第二轮表面风格：S5 正式候选默认由 S4 根据论文需要设置表面风格；表面风格只约束渲染层，"
    "不改变候选图的论文语义、布局骨架、连线证据和密度预算。若希望指定第二轮表面风格，请在下一轮 S4 请求中另行写入"
    "“第二轮采用 <表面风格名> 表面风格”。可选项包括：正式出版风格、干净扁平极简线稿、轻量蓝图精密稿、"
    "轻量科学插画、轻量界面隐喻、轻量等距结构、轻量信息图板、ACM/IEEE/AAAI 双栏论文 line-art schematic。"
    "也可以写“取消默认表面风格，请 S4 根据论文实际需要自行设置 S5 表面风格”。"
    "低保真草图、白板线框、手绘故事板默认只适合第一轮探索；若要用于第二轮，必须在 S4 请求中明确说明它仍需保持 formal candidate 可读性。"
)

WORKFLOW_STEPS = [
    (
        "S0-PAPER-FOUNDATION",
        "TEXT_ONLY",
        "Build the paper/source foundation, runtime state, canvas defaults, framework-figure readiness state, optional author-supplement request, and risk register.",
        "outputs/S0-paper-foundation",
    ),
    (
        "S1-FIGURE-STRATEGY",
        "TEXT_ONLY_WITH_EMBEDDED_S2_PREPARE",
        "Prepare reader question, figure role, narrative structure, visual directions, sketch candidate cards, and all S2 prompt packages/prompt-index before S2 image generation, with strict source-grounded modular prompt audits and up to three repair cycles.",
        "outputs/S1-figure-strategy",
    ),
    (
        "S2-SKETCH-EXPLORE",
        "IMAGE_GENERATE_ONLY",
        "Generate first-round publication-style framework candidates from S1-prepared prompt packages unless an explicit compatible style override is recorded. Do not write text review, aggregate, or next-step prose.",
        "outputs/S2-sketch-explore",
    ),
    (
        "S3-DIRECTION-SELECT",
        "TEXT_ONLY_WITH_EMBEDDED_S2_REVIEW_AGGREGATE",
        "Review S2 sketches with issue-ledger and exploration aggregate duties, accept optional user-preferred S2 candidate IDs as preference signals, then select the paper-grounded refinement direction.",
        "outputs/S3-direction-select",
    ),
    (
        "S4-CANDIDATE-BRIEF",
        "TEXT_ONLY_WITH_EMBEDDED_S5_PREPARE",
        "Prepare the formal candidate matrix and all S5 prompt packages/prompt-index before formal candidate image generation, with strict source-grounded modular prompt audits and up to three repair cycles.",
        "outputs/S4-candidate-brief",
    ),
    (
        "S5-CANDIDATE-IMAGE",
        "IMAGE_GENERATE_ONLY_TERMINAL",
        "Generate formal paper-framework raster candidates from S4-prepared prompt packages. This is the terminal assistant workflow stage; remaining decisions are human decisions.",
        "outputs/S5-candidate-image",
    ),
]

STEP_OUTPUT_DIRS = {step: output_dir for step, _, _, output_dir in WORKFLOW_STEPS}
STEP_SEQUENCE = tuple(step for step, _, _, _ in WORKFLOW_STEPS)
DEFAULT_NEXT_STEP_BY_STEP = {
    step: STEP_SEQUENCE[index + 1] if index + 1 < len(STEP_SEQUENCE) else None
    for index, step in enumerate(STEP_SEQUENCE)
}
TEXT_REPLY_STEP_BANNER_TEMPLATE = (
    "当前流程位置\n"
    "全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> "
    "S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> END\n"
    "当前 step：{current_step}\n"
    "默认下一步：{default_next_step}"
)
STEP_CLEANUP_EXTRA_DIRS = {}
STEP_CLEANUP_EXTRA_FILES = {}

ARTIFACT_ROLES = {
    "s0.paper_foundation_report": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/paper-foundation-report.md",
    },
    "s0.framework_figure_risk_register": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/framework-figure-risk-register.md",
    },
    "s0.author_supplement_request": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/author-supplement-request.md",
    },
    "s0.supplement_integration_log": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/supplement-integration-log.md",
    },
    "s1.figure_strategy": {
        "step": "S1-FIGURE-STRATEGY",
        "kind": "markdown",
        "relative_path": "outputs/S1-figure-strategy/figure-strategy-brief.md",
    },
    "s1.s2_prompt_index": {
        "step": "S1-FIGURE-STRATEGY",
        "kind": "json",
        "relative_path": "outputs/S2-sketch-explore/prompt-index.json",
    },
    "s2.primary_sketch": {
        "step": "S2-SKETCH-EXPLORE",
        "kind": "image",
        "relative_path": "outputs/S2-sketch-explore/candidates/C01/image-v01.png",
    },
    "s3.direction_selection": {
        "step": "S3-DIRECTION-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S3-direction-select/s3-direction-decision.md",
    },
    "s3.s2_exploration_aggregate": {
        "step": "S3-DIRECTION-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S3-direction-select/s2-exploration-aggregate.md",
    },
    "s4.candidate_brief": {
        "step": "S4-CANDIDATE-BRIEF",
        "kind": "markdown",
        "relative_path": "outputs/S4-candidate-brief/formal-candidate-brief.md",
    },
    "s4.s5_prompt_index": {
        "step": "S4-CANDIDATE-BRIEF",
        "kind": "json",
        "relative_path": "outputs/S5-candidate-image/prompt-index.json",
    },
    "s5.primary_candidate": {
        "step": "S5-CANDIDATE-IMAGE",
        "kind": "image",
        "relative_path": "outputs/S5-candidate-image/candidates/F01/image-v01.png",
    },
}

PRIMARY_ARTIFACT_ROLE_BY_STEP = {
    "S0-PAPER-FOUNDATION": "s0.paper_foundation_report",
    "S1-FIGURE-STRATEGY": "s1.figure_strategy",
    "S2-SKETCH-EXPLORE": "s2.primary_sketch",
    "S3-DIRECTION-SELECT": "s3.direction_selection",
    "S4-CANDIDATE-BRIEF": "s4.candidate_brief",
    "S5-CANDIDATE-IMAGE": "s5.primary_candidate",
}

CANONICAL_OUTPUTS = {step: ARTIFACT_ROLES[role]["relative_path"] for step, role in PRIMARY_ARTIFACT_ROLE_BY_STEP.items()}


def _pending_row(role_id: str) -> dict[str, str]:
    role = ARTIFACT_ROLES[role_id]
    return {"step": role["step"], "relative_path": role["relative_path"], "artifact_role": role_id}


PENDING_CANONICAL_OUTPUTS = []
for _step, _, _, _ in WORKFLOW_STEPS:
    _role_id = PRIMARY_ARTIFACT_ROLE_BY_STEP[_step]
    PENDING_CANONICAL_OUTPUTS.append(_pending_row(_role_id))
for _role_id in (
    "s1.s2_prompt_index",
    "s3.s2_exploration_aggregate",
    "s4.s5_prompt_index",
):
    PENDING_CANONICAL_OUTPUTS.append(_pending_row(_role_id))

TEXT_ONLY_STEPS = {step for step, mode, _, _ in WORKFLOW_STEPS if mode.startswith("TEXT_ONLY")}
IMAGE_ONLY_STEPS = {step for step, mode, _, _ in WORKFLOW_STEPS if mode.startswith("IMAGE")}

ATLAS_BOARD_ROOT = "assets/subtype-atlas/boards"
ATLAS_THUMBNAIL_ROOT = "assets/subtype-atlas/thumbnails"
ATLAS_MANIFEST_PATH = "assets/subtype-atlas/manifest.json"
ATLAS_BOARD_IDS = (
    "subtype-overview",
    "visual-grammar-layout",
    "reader-role-detail",
    "visual-communication-styles",
)
ATLAS_DISPLAY_POLICY = (
    "Whenever a reply mentions subtype/category atlas boards, layout grammar, visual communication styles, "
    "reader-role detail, or subtype overview, embed the corresponding saved PNG board with Markdown. "
    "Do not build generated web pages in any environment, including Codex."
)
