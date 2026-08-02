---
name: dasheng-html-video-bridge
description: Use when Dasheng transwrite needs no-human or human-material talking-head videos rendered through the local html-video project.
---

# Dasheng HTML Video Bridge

正式 1:1 无真人口播交付必须遵循 `docs/technical/no-human-square-video-production-standard.md`。

## Role

Use the external `html-video` repository as the default renderer for Dasheng video transwrite. This skill turns a confirmed Draft into an executable html-video project package; it does not research facts or rewrite the article thesis.

`html-video` is an external dependency, not vendored into this repo and not version-locked. Default path: `/Volumes/PSSD/html-video`; override with `HTML_VIDEO_ROOT`.

Check or install before first use:

```bash
python3 scripts/ensure_video_external_deps.py --dep html-video --mode check
python3 scripts/ensure_video_external_deps.py --dep html-video --mode install --install-node-deps
```

For Dasheng no-human explainer scenes, external `html-video` must also provide `gsap` and `lottie-web`; `ensure_video_external_deps.py --install-node-deps` checks and installs them in the external repo.

## Inputs

- `talking_head_video_manifest.json`
- `video_storyboard.json`
- `talking_head_script.md`
- Optional human media: real video, real audio, or subtitle/SRT files

## Default Renderer

Resolve the root from `HTML_VIDEO_ROOT` or `/Volumes/PSSD/html-video`, then run:

```bash
HTML_VIDEO_ROOT="${HTML_VIDEO_ROOT:-/Volumes/PSSD/html-video}"
node "$HTML_VIDEO_ROOT/packages/cli/dist/bin.js" doctor --cwd "$HTML_VIDEO_ROOT"
node "$HTML_VIDEO_ROOT/packages/cli/dist/bin.js" search-templates --intent "<intent>" --aspect 9:16 --top 5 --cwd "$HTML_VIDEO_ROOT"
```

Prefer these templates for market commentary:

- `frame-liquid-bg-hero`: hook/title/opening atmosphere
- `frame-data-chart-nyt`: one clear data comparison
- `frame-electric-studio`: quote or conflict frame
- `frame-light-leak-cinema`: cinematic transition
- `frame-logo-outro`: ending card

## Bridge Command

Generate a project plan without mutating html-video:

```bash
python3 scripts/transwrite_html_video_bridge.py \
  --video-manifest <talking_head_video_manifest.json>
```

Create and preview a real html-video project only when the user asks to render:

```bash
python3 scripts/transwrite_html_video_bridge.py \
  --video-manifest <talking_head_video_manifest.json> \
  --execute create
```

Render MP4:

```bash
python3 scripts/transwrite_html_video_bridge.py \
  --video-manifest <talking_head_video_manifest.json> \
  --execute render
```

## Two Production Modes

### No Human Material

Flow:

`draft -> short script -> storyboard beats -> TTS audio -> html-video template vars -> preview -> MP4`

Rules:

- Do not use macOS `say` for production voice unless explicitly accepted as a rough preview.
- Use MiniMax CLI (`mmx`) as the default production provider for final narration, generated口播音频, background music, and AI image/video assets.
- Coze or direct MiniMax API calls are fallback paths only when the CLI cannot express the required operation.
- Visuals must contain market/data metaphors, charts, and scene motion; do not render only enlarged outline bullets.
- Motion stack: HyperFrames scene composition + GSAP timing + optional Lottie accents. Lottie cannot replace real data charts or evidence.

Default voice render entry:

```bash
python3 scripts/render_html_anything_scene_pack_video.py \
  --manifest <scene_pack_manifest.json> \
  --output-dir <render_dir> \
  --with-voice \
  --voice-provider mmx \
  --voice "Chinese (Mandarin)_Radio_Host" \
  --mmx-model speech-2.8-hd \
  --mmx-speed 1.08
```

### Human Material Present

Flow:

`human audio/video -> Whisper/SRT -> beat alignment -> transparent/non-transparent HTML visual layer -> FFmpeg/html-video compose`

Rules:

- Existing human audio is the master timeline.
- Visual frames follow the audio; do not force the speaker to follow animation timing.
- If only real video exists, extract audio first, then transcribe.

## Output Contract

The bridge writes:

- `html_video_project_vars.json`
- `html_video_project_plan.json`
- `html_video_commands.sh`
- Optional `html_video_execution.json` when executed

`talking_head_video_manifest.json` must point to `html_video_project_plan.json`.

## Hard Rules

1. Draft owns facts, charts, and source claims.
2. This skill owns video structure, visual metaphor, timing, and renderer handoff.
3. Plans are not final videos; only mark `rendered` after an MP4 exists.
4. Keep output folders shallow: manifest, storyboard, script, vars, plan, renders.
5. Never hardcode API keys or write credentials into manifests.
6. Do not vendor or pin `html-video`; install or update the external repo when the skill needs it.
