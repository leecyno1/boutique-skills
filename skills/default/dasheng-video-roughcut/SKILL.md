---
name: dasheng-video-roughcut
description: Use when rough-cutting Chinese talking-head video with local FunASR transcription, silence trimming, repetition/filler detection, subtitles, and an audit page.
---

# Dasheng Video Roughcut｜口播视频粗剪

## 定位

这是 Transwrite 的口播视频辅助环节，处理“用户已经有真人口播素材”的场景。

目标是先给出可审核的粗剪版本，不直接替代人工精剪。

它不是独立主阶段，而是 `transwrite -> talking_head_video` 的“初检/粗剪”子环节。后续视频视觉层、HTML 动画、字幕烧录和平台导出继续留在 video lane 内组合。

## 输入

- 真人口播视频：`.mp4` / `.mov`
- 可选热词：股票、平台名、英文公司名、专有名词

## 技术栈

- ASR：FunASR `paraformer-zh + fsmn-vad + ct-punc`
- 渲染：FFmpeg
- 音频增强：FFmpeg 开源滤镜 `afftdn`、`dynaudnorm`、`acompressor`、`loudnorm`、`alimiter`
- 审核：本地 HTML 审核页

## 双路径实验

当前口播粗剪保留两条并行路径：

- 路径 A：`FunASR -> Agent 字幕/语义整理 -> FFmpeg 精剪 -> HTML 审核页`，作为可复现主链路。
- 路径 B：`剪映专业版 -> 时间线片段右键 -> 智能剪口播`，作为实验通路，用于测试剪映内置去水词、去重复和停顿识别能力。

剪映路径只测试剪映自己的智能剪口播结果，不再叠加 Agent 根据原提纲做二次语义检查。

## 标准命令

### 初检审核包

```bash
.venv_media/bin/python scripts/video_roughcut_funasr.py \
  --input-video "/path/to/source.mp4" \
  --output-dir "产物/06_转写生产/<run_id>/talking_head_video/roughcut" \
  --mode balanced
```

### Agent 整理稿对齐剪辑

先生成 Agent 整理输入：

```bash
python3 scripts/video_roughcut_agent_align.py \
  --source-video "/path/to/source.mp4" \
  --segments-json "roughcut/work/segments.json" \
  --output-dir "roughcut_agent_refine"
```

Agent 输出 `agent_plan.json` 后渲染：

```bash
python3 scripts/video_roughcut_agent_align.py \
  --source-video "/path/to/source.mp4" \
  --segments-json "roughcut/work/segments.json" \
  --agent-plan "roughcut_agent_refine/agent_plan.json" \
  --output-dir "roughcut_agent_refine"
```

首次使用媒体环境：

```bash
.venv_media/bin/python -m pip install -r requirements-media.txt
```

## 输出

- `roughcut_manifest.json`
- `work/funasr_raw.json`
- `work/segments.json`
- `work/delete_segments.json`
- `work/keep_segments.json`
- `final/*_roughcut_funasr.mp4`
- `final/*_roughcut_funasr.srt`
- `final/*_roughcut_funasr_softsub.mp4`
- `review/3_review_live.html`
- `review/review_server.js`
- `review/start_review.command`
- `review/2_candidates.json`
- `review/3_delete_segments.json`
- `review/3_delete_segments.reviewed.json`（人工保存后生成）
- `review/reviewed_output_loud.mp4`（保存并重剪后生成）
- `review/reviewed_output_loud.srt`（保存并重剪后生成）
- `review/reviewed_output_loud_softsub.mp4`（保存并重剪后生成）
- `review/proofread_agent_input.md`（保存并重剪后生成）

## 审核方式

```bash
cd "<output-dir>/review"
PORT=8899 node review_server.js
```

浏览器打开 `http://localhost:8899/`。

- 勾选候选片段只影响实时预览，不会自动保存。
- 点击“保存审核”写入 `3_delete_segments.reviewed.json`。
- 点击“保存并重剪”生成审核后视频、SRT、软字幕视频和 Agent 字幕校对输入包。
- 字幕显示默认小字号，可关闭或调整。

## 剪映智能剪口播实验通路

适用条件：

- 用户本机已安装剪映专业版。
- 用户允许用剪映草稿作为交付物或由助理继续云端接力。
- 当前目标是验证剪映自身的去水词能力，而不是追求完全可复现的开源流水线。

操作顺序：

1. 新建干净剪映草稿。
2. 导入口播原片。
3. 对素材执行“根据选中素材新建时间线”，确保原片先入时间线。
4. 在时间线片段上右键选择“智能剪口播”。
5. 保持剪映默认识别结果和类别勾选，点击剪映的应用/删除按钮。
6. 记录草稿路径、原始时长、剪后时长、识别无效词数量和剪映时间线名称。

注意：

- 不要从素材库直接右键触发“智能剪口播”；那会进入“选择文本插入时间线”模式，不是自动去水词路径。
- 剪映草稿主时间线文件在新版剪映中可能被封装或加密，不能假设可用普通 JSON 解析。
- 当前剪映路径的交付重点是草稿和 UI 结果，不强制自动导出视频。

## 剪辑策略

- 默认只做句段级删除，避免字词级硬切导致口播断裂。
- 删除长静音时保留少量呼吸间隔。
- 删除纯口水句，如单独的“嗯、呃、这个、那个”。
- 删除相邻重复句，保留更完整的一句；高风险语义候选必须让用户审核确认。
- 语义删改必须进入 `delete_segments.json`，供审核页追溯。
- 更精细的口水词、口吃、重复表达，优先走 Agent 整理稿对齐剪辑：Agent 按原口播顺序整理文字，脚本用差异对齐反推删除区间。
- Agent 整理稿不得重构文章，只能在原始口播顺序上做轻量删改、断句和专名修正；否则无法稳定映射回视频时间轴。

## 音频策略

- 默认对输出视频应用降噪、动态音量平衡、压缩、响度提升和限幅。
- 当前内置滤镜：`highpass -> lowpass -> afftdn -> dynaudnorm -> acompressor -> loudnorm(I=-14) -> alimiter`。
- 如果录音底噪很重，可后续升级接入 RNNoise / DeepFilterNet，但默认先用 FFmpeg 内置开源滤镜，减少部署复杂度。

## 视觉滤镜后处理

- 粗剪后如需暖光电影风格、轻磨皮增白、低风险轻拉瘦，调用 `dasheng-video-open-filter`。
- 原视频已经烧录大字幕时，滤镜环节默认不再封装 softsub，避免出现两套字幕。
- 远景侧脸素材不默认做局部 FaceMesh 拉瘦，优先用轻微整体横向瘦身，避免人物和字幕漂移。

## 字幕时间轴

- SRT 输出必须强制单调递增，避免字幕重叠。
- 删除区间映射后，字幕 cue 默认只做时间重映射，不整体平移。
- Agent 校对默认只改文字，不重算时间轴；拆分/合并 cue 必须显式记录。

## 字幕校对

- Agent 字幕校对发生在人工审核和重剪之后。
- 校对输入是 `review/proofread_agent_input.md` / `review/proofread_agent_input.json`。
- 默认只改字幕文字，不整体平移时间轴，避免“字幕滞后”。
- 不再用 Python 写死专名替换词表；专名、同音词、断句和口水词由主 Agent 根据上下文校正。

## 约束

1. 不在这里改正文事实。
2. 不把粗剪当终剪；必须让用户审核。
3. 专名修正交给 Agent 校对字幕，不用硬编码词表替换。
4. 如果 FunASR 缺失，先安装 `requirements-media.txt`，不要静默退回低质量转写。
