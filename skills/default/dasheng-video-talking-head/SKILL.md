---
name: dasheng-video-talking-head
description: Use when producing or improving Dasheng真人出镜口播视频 from raw speaker footage, subtitles, rough cuts, B-roll, data charts, or HTML sticker overlays.
---

# Dasheng Video Talking Head

## Role

Build the真人出镜口播 production line. The speaker is the trust anchor; evidence screens, charts, documents, B-roll, subtitles, camera motion, and music carry the pace.

## Required First Artifact

Create a director timeline before rendering:

```bash
python3 scripts/video_director_timeline.py \
  --srt <agent_proofread.srt> \
  --source-video <speaker.mp4> \
  --title "<title>" \
  --output <talking_head_timeline.json>
```

Use `--captions-json` instead of `--srt` when the rough-cut review page produced captions JSON.

## Director Mechanism

Read `docs/technical/video-editing-driving-mechanism.md` and `configs/video/video_editing_driver_rules.json` before planning final shots.

Do not map every sentence to a sticker. Drive editing with:

`evidence_need -> attention_debt -> trust_debt -> cognitive_load -> shot -> template/material -> transition -> audio`

Default state machine:

`speaker_anchor -> claim_closeup -> evidence_fullscreen -> broll_with_pip -> document_zoom/chart_card -> speaker_return`

## Production Rules

- Human audio/video is the master timeline.
- Subtitles must be Agent-proofread and semantically punctuated before final render.
- Use external `html-video` through `dasheng-html-video-bridge` only for evidence overlays, chart cards, title cards, or non-transparent visual layers; install on demand with `scripts/ensure_video_external_deps.py`.
- Every chart/table must come from article data or verified data collection. Fake placeholders are forbidden.
- Keep developer labels out of final video.
- Target vertical mobile output: `9:16`, speaker crop safe, subtitle near the source-video bottom edge.
- If `trust_debt` exceeds 16 seconds, return to the speaker unless the current sequence is a dense evidence run.
- If a beat contains numbers, source documents, policies, companies, or market data, force an evidence shot before another decorative overlay.

## Quality Targets

- Median visual segment: 2.5-4s.
- Evidence/B-roll ratio: 45%-65%.
- Speaker returns at least every 8-20s.
- Human voice target: about -16 LUFS, no mid-video silent gaps.
- Subtitle: 1-2 lines, about 24 Chinese chars per line, no overlap.

## Output Contract

- `talking_head_timeline.json`
- `agent_proofread.srt`
- `final_talking_head.mp4`
- `video_qc_report.json`
- `qa_contact_sheet.jpg`
