---
name: dasheng-video-explainer-html
description: Use when turning a Dasheng HTML article into a no-human vertical explainer video with voiceover, storyboard scenes, HTML animation, real charts, music, and final MP4.
---

# Dasheng Video Explainer HTML

## Role

Build the无真人出镜科普 production line. The article is the fact source; the storyboard is the first-class artifact; html-video renders the animated scenes.

## Required First Artifact

Build the template router, extract the article into a storyboard, then expand it into an HTML Anything video timeline:

```bash
python3 scripts/build_html_anything_template_router.py \
  --output configs/video/html_anything_template_router.json

python3 scripts/video_explainer_storyboard.py \
  --html <article.html> \
  --template-router configs/video/html_anything_template_router.json \
  --output <explainer_storyboard.json> \
  --preview-html <storyboard_preview.html>

python3 scripts/build_html_anything_video_timeline.py \
  --storyboard <explainer_storyboard.json> \
  --article-html <article.html> \
  --template-router configs/video/html_anything_template_router.json \
  --output <html_anything_video_timeline.json>
```

## Director Mechanism

Read `docs/technical/video-editing-driving-mechanism.md`, `docs/technical/video-script-template-routing-guide.md`, and `configs/video/video_editing_driver_rules.json` before rendering.

No-human explainer is not PPT pagination. Drive scene choice with:

`voiceover beat -> evidence_need -> cognitive_load -> template -> intra-scene motion -> transition -> music/SFX`

Default state machine:

`hook_card -> question_setup -> chapter_card -> evidence_scene -> logic_animation -> cinematic_bridge -> evidence_scene -> recap_card -> outro`

## Production Rules

- Do not create a second fact chain. Reuse the article's real tables, charts, images, and sourced claims.
- Generate one continuous voiceover with MiniMax CLI (`mmx`) by default, then align scene durations to that audio. Use per-scene TTS only as a fallback or debugging mode.
- Use MiniMax CLI for production narration, background music, AI image assets, and generated口播音频. Do not call MiniMax APIs directly from ad-hoc scripts unless the CLI cannot express the operation.
- Use external `html-video` as the default renderer via `dasheng-html-video-bridge`; install on demand with `scripts/ensure_video_external_deps.py`.
- Use external `html-anything` only as visual/template reference via `dasheng-html-anything-bridge`; install on demand with `scripts/ensure_video_external_deps.py`.
- No generic framework diagrams when article data can support a concrete chart/table.
- No CDN-dependent final assets; preview HTML may be simple, final MP4 must be rendered locally.
- Prefer HyperFrames as the scene composition model.
- Use GSAP-style timelines for entrance, exit, chart reveal, path draw, table scan, and title kinetics.
- Lottie is allowed only as decorative/auxiliary motion. It must never replace real article charts, tables, screenshots, or evidence.
- Do not render from raw storyboard directly unless debugging. Final video planning must route content parts to HTML Anything templates first.
- macOS `say` is only a smoke-test fallback; it is not acceptable for final voiceover unless explicitly requested.
- Evidence scenes must appear every 20-35 seconds. Chapter or structure reset must appear every 45-90 seconds.
- A scene longer than 8 seconds needs explicit intra-scene motion: data reveal, document zoom, path highlight, focus shift, or exit motion.

## MiniMax CLI Defaults

Check authentication and quota before production rendering:

```bash
mmx auth status --no-color
mmx quota --no-color
```

Default render command shape:

```bash
python3 scripts/render_html_anything_scene_pack_video.py \
  --manifest <scene_pack_manifest.json> \
  --output-dir <render_output_dir> \
  --with-voice \
  --voice-mode single \
  --voice-provider mmx \
  --voice "Chinese (Mandarin)_Radio_Host" \
  --mmx-model speech-2.8-hd \
  --mmx-speed 1.32
```

Default narration command shape used by the renderer:

```bash
mmx speech synthesize \
  --text-file <full_voiceover_script.txt> \
  --out <voiceover_single.wav> \
  --model speech-2.8-hd \
  --voice "Chinese (Mandarin)_Radio_Host" \
  --speed 1.32 \
  --format wav \
  --sample-rate 44100 \
  --channels 1 \
  --language Chinese
```

Default background music command shape:

```bash
mmx music generate \
  --prompt "cinematic financial documentary, restrained tension, no vocals" \
  --instrumental \
  --out <bgm.mp3>
```

Default AI image command shape:

```bash
mmx image generate \
  --prompt "<article-specific visual prompt>" \
  --aspect-ratio 9:16 \
  --out <image.jpg>
```

## Style Targets

- Vertical finance/documentary style.
- Average scene: 5-7s; median: 4-5s.
- Evidence screen every 20-35s.
- Chapter card every 45-90s.
- Prefer document zoom, data reveal, chart animation, terminal/Bloomberg-like information rhythm.
- Add Lottie-style accent motion for warning, market ticker, data flow, document scan, and outro only when it supports the spoken beat.

## Output Contract

- `explainer_storyboard.json`
- `html_anything_video_timeline.json`
- `storyboard_preview.html`
- `voiceover.wav` or provider-specific audio file
- `final_explainer_vertical.mp4`
- `video_qc_report.json`
- `qa_contact_sheet.jpg`
