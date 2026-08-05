"""
silent_vlog_maker.pipeline — R16 verify grid + voice profile loader + R9 filter_complex orchestrator.

The big one — combines all rules into the master ffmpeg filter_complex string.
"""
import json
import subprocess
from pathlib import Path
from typing import Optional

from .constants import TONEMAP_FILTER, FONT_NOTO_BOLD
from .text_overlay import Overlay


# ─────────────────────────────────────────────────────────────────────
# R16 Verify: Single keyframe grid (saves 75% Read tokens)
# ─────────────────────────────────────────────────────────────────────

def make_keyframe_grid(
    video_path: Path,
    timestamps: list[float],
    output_path: Path,
    cols: int = 2,
    label: bool = True,
) -> Path:
    """
    Extract N keyframes and tile into single grid image.

    Before optimization: 4-6 Read calls = ~20-30k tokens
    After: 1 Read of grid image = ~5-8k tokens (-75%)

    Args:
        timestamps: list of seconds to extract frames at
        cols: grid columns (rows derived)
        label: overlay timestamp label on each frame
    """
    temp_dir = output_path.parent / "_temp_frames"
    temp_dir.mkdir(exist_ok=True)

    # Extract each frame (use -i then -ss for accurate seek; format=yuvj420p
    # because cinematic curves can produce full-range YUV that MJPEG rejects)
    frame_paths = []
    for i, ts in enumerate(timestamps):
        frame = temp_dir / f"_f{i:02d}.jpg"
        vf = "scale=540:960,format=yuvj420p"
        if label:
            vf += (
                f",drawtext=fontfile='{FONT_NOTO_BOLD}':"
                f"text='{ts:.1f}s':fontsize=36:fontcolor=yellow:"
                f"borderw=3:bordercolor=black:x=20:y=20"
            )
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-i", str(video_path), "-ss", str(ts),
             "-vf", vf, "-frames:v", "1", "-q:v", "3", str(frame)],
            check=True
        )
        frame_paths.append(frame)

    rows = (len(frame_paths) + cols - 1) // cols
    grid_w = 540 * cols
    grid_h = 960 * rows

    # Use ffmpeg tile filter to combine
    inputs = []
    for p in frame_paths:
        inputs.extend(["-i", str(p)])

    filter_inputs = "".join(f"[{i}:v]" for i in range(len(frame_paths)))
    filter_complex = f"{filter_inputs}xstack=inputs={len(frame_paths)}:layout="
    # Build xstack layout: e.g. "0_0|w0_0|0_h0|w0_h0" for 2x2
    layout_parts = []
    for i in range(len(frame_paths)):
        col = i % cols
        row = i // cols
        x_expr = f"{col * 540}" if col > 0 else "0"
        y_expr = f"{row * 960}" if row > 0 else "0"
        layout_parts.append(f"{x_expr}_{y_expr}")
    filter_complex += "|".join(layout_parts)

    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         *inputs, "-filter_complex", filter_complex, str(output_path)],
        check=True
    )

    # Cleanup temp frames
    for p in frame_paths:
        p.unlink(missing_ok=True)
    temp_dir.rmdir() if not list(temp_dir.iterdir()) else None

    return output_path


# ─────────────────────────────────────────────────────────────────────
# R15 Voice profile loader
# ─────────────────────────────────────────────────────────────────────

VOICE_PROFILES_PATH = Path(__file__).parent / "voice_profiles.json"


def load_voice_profile(mode: str) -> dict:
    """Load cached voice profile (saves Explore agent ~30s + 3-5k tokens per video).

    Modes: vlog / high-demo / high-reflective / low-diy

    Returns dict matching voice_profiles.json schema, e.g. for vlog:
    - tone_persona (str)
    - opening_pattern (dict: template / example_from_sample / structure)
    - punctuation (dict: soft_tail / exclaim_intensity / particles / ...)
    - pronouns (list)
    - wandering_verbs (list)
    - hedged_evaluations (list)
    - evaluation_template (str)
    - evaluation_examples (list)
    - sign_off (dict: uses_boilerplate / reason / alternatives)
    - avoid_strict (list)
    - on_screen_text_rules (dict)
    - example_overlays_template (list)
    """
    if not VOICE_PROFILES_PATH.exists():
        raise FileNotFoundError(
            f"voice_profiles.json not found at {VOICE_PROFILES_PATH}. "
            f"Run Explore agent to generate it first."
        )
    profiles = json.loads(VOICE_PROFILES_PATH.read_text(encoding="utf-8"))
    if mode not in profiles:
        raise KeyError(f"Voice mode '{mode}' not in cache. Available: {list(profiles.keys())}")
    return profiles[mode]


# ─────────────────────────────────────────────────────────────────────
# R9 Pipeline orchestrator (combines all rules)
# ─────────────────────────────────────────────────────────────────────

def build_filter_complex(
    clips_spec: list[tuple[str, float, float, list[Overlay]]],
    raw_dir: Path,
    temp_dir: Path,
    apply_tonemap: bool = True,
    bgm_input_idx: Optional[int] = None,
    total_duration: float = 0.0,
) -> str:
    """
    Build complete ffmpeg filter_complex string.

    Args:
        clips_spec: [(filename, start_offset, duration, [Overlay, ...]), ...]
        apply_tonemap: True if any clip is HDR (auto-detect upstream)
        bgm_input_idx: input index of BGM audio (after all video inputs)
        total_duration: required for BGM atrim
    """
    temp_dir.mkdir(exist_ok=True)
    chains = []
    text_idx = 0

    for i, (clip, start, dur, overlays) in enumerate(clips_spec):
        chain = f"[{i}:v]trim={start}:{start + dur},setpts=PTS-STARTPTS"
        if apply_tonemap:
            chain += f",{TONEMAP_FILTER}"

        for ov in overlays:
            tf = temp_dir / f"text_{text_idx:02d}.txt"
            tf.write_text(ov.text, encoding="utf-8")
            text_idx += 1
            tf_path = str(tf).replace("\\", "/").replace(":", "\\:")
            chain += "," + ov.to_drawtext(tf_path)

        chain += f"[v{i}]"
        chains.append(chain)

    concat_in = "".join(f"[v{i}]" for i in range(len(clips_spec)))
    concat_chain = f"{concat_in}concat=n={len(clips_spec)}:v=1:a=0[outv]"

    parts = [";".join(chains), concat_chain]
    if bgm_input_idx is not None and total_duration > 0:
        audio_chain = (
            f"[{bgm_input_idx}:a]"
            f"atrim=0:{total_duration},"
            f"afade=t=in:st=0:d=0.5,"
            f"afade=t=out:st={total_duration - 3}:d=3,"
            f"volume=0.3"
            f"[bgma]"
        )
        parts.append(audio_chain)

    return ";".join(parts)
