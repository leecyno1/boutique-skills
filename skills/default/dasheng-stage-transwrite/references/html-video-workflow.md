# HTML Video Workflow

## Default Path

For `talking_head_video`, use `${HTML_VIDEO_ROOT:-vendor/reserved/render/html-video}` as the production renderer.

The stage builder writes:

- `video_storyboard.json`
- `talking_head_script.md`
- `html_overlay.html`
- `render_plan.json`
- `html_video_project_vars.json`
- `html_video_project_plan.json`

Run the bridge:

```bash
python3 scripts/transwrite_html_video_bridge.py \
  --video-manifest <talking_head_video_manifest.json>
```

Only execute rendering when explicitly needed:

```bash
python3 scripts/transwrite_html_video_bridge.py \
  --video-manifest <talking_head_video_manifest.json> \
  --execute render
```

## Mode Selection

- No human media: synthetic voice + html-video visual frames.
- Human audio/video: transcribe first, then align visuals to the human timeline.

## Quality Bar

- One frame, one idea.
- Use charts, contrast, maps, timelines, quotes, and market metaphors.
- Avoid turning the article outline into a generic framework diagram.
- If TTS is not configured, mark audio as blocked or preview-only.
