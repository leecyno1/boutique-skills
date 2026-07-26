---
name: dasheng-stage-transwrite
description: Use when converting confirmed Dasheng drafts into channel-ready WeChat article, talking-head video, and podcast production packages.
---

# Dasheng Stage: Transwrite｜转写生产

## 定位

这是 Draft 之后、Publish 之前的正式主链阶段。

正式阶段顺序：

`intake -> brief -> draft -> transwrite -> publish -> postmortem`

Draft 负责事实、数据、图表、配图和自包含 HTML。Transwrite 只负责把已确认稿转成不同渠道的表达形态，不重新发明事实链。

本阶段采用轻内核：Python 只生成任务包、提示词、请求体、最终产物槽位、QC 契约和 manifest；真正生产由 Agent 调用对应技能完成，并回写 lane manifest。

## 正式输入

- `draft_manifest.json`
- `final_structure_snapshot.json`
- `transwrite_decision.json`

缺少 `final_structure_snapshot.json` 或 `transwrite_decision.json` 时禁止执行。

## 三条通路

### 1. wechat_article｜公众号文章

目标：

- 调用 Style DNA / humanize 规则做文字调教
- 内容扩展、节奏重排、微信格式转写
- 可选调用 `baoyu-cover-image` / `baoyu-imagine` 生成封面
- 最终输出 `wechat_article.final.md` 与 `wechat_article.final.html`
- 最终必须有 `wechat_article_qc_report.json`，确认图表、表格、图片、事实锚点没有丢失
- 公众号排版必须遵守 `configs/publish/wechat_layout_rules.json`：H2 使用阿拉伯数字大标题并左对齐，不用居中块状标题；表格内文字约 12px，单元格紧凑，避免手机端换行挤压；正文不得全篇蓝色或全篇加粗。

继承技能：

- `dasheng-style-profiler`
- `wechat-style-profiler`
- `baoyu-markdown-to-html`
- `baoyu-cover-image`
- `scripts/wechat_layout_variants.py`（生成候选排版预览，并可做最终 HTML 版式后处理）

文字洁癖：

- 少用“不是...而是...”
- 少用“一方面...另一方面...”
- 避免把事实稿洗成模板腔

### 2. talking_head_video｜口播视频

目标：

- 支持真人口播素材可选
- 支持透明 / 非透明 HTML 视觉层
- 支持真人音频 / 合成音频
- 支持主动对齐（跟随已有音频）/ 被动对齐（跟随动画配音）

默认渲染器：

- `dasheng-html-video-bridge`
- `/Volumes/PSSD/html-video`
- 默认模板：`frame-liquid-bg-hero`，可按题材切换 `frame-data-chart-nyt`、`frame-electric-studio`、`frame-light-leak-cinema`

典型模式：

- 用户有真人口播素材：`human video/audio -> transcription -> timeline -> HTML visual layer -> html-video/FFmpeg compose`
- 用户没有真人口播素材：`draft script -> MiniMax CLI TTS -> animation timeline -> html-video render`

推荐模块：

- `dasheng-html-video-bridge`
- `dasheng-html-anything-bridge`
- `dasheng-video-talking-head`
- `dasheng-video-explainer-html`
- `motion-frames`
- `remotion-best-practices`（复杂透明合成兜底）
- `WhisperX` / `stable-ts`
- MiniMax CLI `mmx`（生产配音、配乐、图片生成、口播音频）
- `FFmpeg`

### 3. podcast｜播客

目标：

- 生成播客脚本和 API 请求体
- 优先通过 MiniMax CLI 或 Coze 既有工作流生成音频，不重复造轮子
- 最终必须有音频文件和 `podcast_qc_report.json`

默认 MiniMax CLI：

```bash
mmx auth status --no-color
mmx speech synthesize --text-file <podcast_script.txt> --out <podcast.wav> --model speech-2.8-hd --voice "Chinese (Mandarin)_Radio_Host"
```

未配置 CLI/auth/API key 时，manifest 必须标记 `blocked_missing_audio_provider`，不得误报“已生成音频”。

## 标准命令

```bash
python3 scripts/build_stage4_transwrite.py \
  --draft-manifest 产物/05_初稿生成/<run_id>/draft_manifest.json \
  --transwrite-decision 产物/06_转写生产/<run_id>/transwrite_decision.json
```

统一入口：

```bash
python3 scripts/run_mainline_stage.py transwrite --run-id <run_id>
```

## transwrite_decision.json 示例

```json
{
  "run_id": "<run_id>",
  "gate": "Transwrite Gate",
  "status": "approved",
  "topics": [
    {
      "topic_id": "topic-demo",
      "lanes": ["wechat_article", "talking_head_video", "podcast"],
      "wechat_article": {
        "dna_profile": "project_or_user_default",
        "humanize": true,
        "cover_generation": {"enabled": true}
      },
      "talking_head_video": {
        "base_video": "/path/to/user-talking-head.mp4",
        "visual_layer": {
          "mode": "html_overlay",
          "background": "transparent"
        },
        "audio": {"mode": "human_audio"},
        "alignment": {
          "mode": "active_to_existing_audio",
          "engine": "whisperx"
        },
        "render": {
          "engine": "html-video",
          "template_id": "frame-liquid-bg-hero",
          "aspect_ratios": ["9:16", "16:9"]
        }
      },
      "podcast": {
        "provider": "minimax",
        "mode": "solo"
      }
    }
  ]
}
```

如果没有真人口播素材，把 `base_video` 移除，并把 `audio.mode` 改为 `synthetic_audio`；系统会走被动对齐路径。

## 标准输出

- `04_转写计划.md`
- `transwrite_manifest.json`
- 每题独立目录：
  - `wechat_article/wechat_article_manifest.json`
  - `wechat_article/agent_rewrite_prompt.md`
  - `wechat_article/cover_prompt.md`
  - `talking_head_video/talking_head_video_manifest.json`
  - `talking_head_video/video_storyboard.json`
  - `talking_head_video/talking_head_script.md`
  - `talking_head_video/html_overlay.html`
  - `talking_head_video/render_plan.json`
  - `talking_head_video/html_video_project_vars.json`
  - `talking_head_video/html_video_project_plan.json`
  - `talking_head_video/html_video_commands.sh`
  - `podcast/podcast_manifest.json`
  - `podcast/podcast_script.md`
  - `podcast/provider_request.json`

## 状态语义

脚本初次生成的 lane 通常只到：

- `ready_for_agent_execution`：等待 Agent 做文字转写、DNA、人味化、封面、QC。
- `ready_for_skill_execution`：等待具体技能/API/渲染器执行，例如视频、播客。
- `blocked_missing_human_media` / `blocked_missing_audio_provider`：缺少输入素材或外部服务。

只有以下状态可进入 Publish 执行包：

- `packageable`
- `completed`

兼容旧产物时，`ready_base_package` 可被 publish 当作文字包可用；新产物不要再主动使用这个状态。

## 强约束

1. 不在本阶段补事实、补数据或重做图表；这些都必须回到 Draft。
2. Python 脚本只生成包、提示词、请求体和 manifest；真正的 DNA/humanize、生图、渲染、播客 API 调用由 Agent/技能执行。
3. 有真人素材与无真人素材走同一个 video lane，只通过配置切换。
4. 外部 API 或素材缺失时必须显式写入状态，不得把计划当成完成品。
5. `transwrite_manifest.json` 是进入 Publish 的唯一正式输入。
6. Agent/技能完成生产后，必须更新对应 lane manifest 的 `final_artifacts`、`qc.status` 和 lane `status`，否则 Publish 只能等待。
7. 文章、HTML、封面、图片、音频、视频、字幕、审核页等运行产物不得写入任何 `skills/` 目录；默认写入 `产物/06_转写生产/<run_id>/...`，实验缓存写入 `tmp/`。

## 外部项目桥接

- 视频渲染见 `references/html-video-workflow.md`。
- HTML 模板与视觉语言见 `references/html-anything-workflow.md`。
