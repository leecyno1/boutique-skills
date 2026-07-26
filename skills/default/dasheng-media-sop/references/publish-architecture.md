# Publish 阶段正式架构

更新时间：`2026-06-08`

## 目标

`publish` 是轻量执行层，只做验收、打包、推草稿/人工发布包、链接回收和发后验真。

正式阶段顺序：

`intake -> brief -> draft -> transwrite -> publish -> postmortem`

`transwrite` 已负责公众号转写、口播视频、播客生产包；`publish` 不再生成正文、封面、视频、播客或图表。

## 正式输入

- `transwrite_manifest.json`
- `publish_decision.json`

若缺少任一文件，`publish` 必须拒绝执行。

## 执行闭环

### 1. Publish Gate

校验 `publish_decision.json`：

- 发布平台矩阵
- 每题每平台路由
- 标题、发布时间、可见性
- 是否允许立即发布，还是仅创建草稿 / 打开浏览器待人工确认

### 2. Package

从 `transwrite_manifest.json` 读取各 lane：

- `wechat_article`：公众号、微博、X 等文字渠道
- `talking_head_video`：小红书、抖音、B站等视频渠道
- `podcast`：播客渠道

只有 `completed` / `packageable` 的 lane 可进入发布执行包。兼容旧文字包时，`ready_base_package` 可被视为可打包。

若 lane 状态仍是 `planned`、`planned_for_render`、`ready_for_agent_execution`、`ready_for_skill_execution`、`blocked_missing_*`、`waiting_for_human_media` 或 `failed_qc`，只能标记为等待，不得误报完成。

### 3. Draft Push / Manual Pack

按渠道生成执行器调用计划：

- 公众号：`baoyu-post-to-wechat` / `wechat-multi-publisher` / `md2wechat`
- 微博：`baoyu-post-to-weibo`
- X：`baoyu-post-to-x`
- 小红书：`dasheng-xhs-publish-bridge` → `all-in-one` / `xhs-skills` / `spider-xhs` / MCP / 持久化浏览器 fallback
- 抖音：`douyin-upload-skill` / `social-auto-upload` / 持久化浏览器 fallback
- B站：`bilibili-upload-bridge` / `biliup-rs` / 人工投稿包
- 播客：人工上传或音频平台 API

浏览器型、MCP、API-first CLI、外部 CLI 或人工包路线默认只生成流程计划，不直接点击最终发布按钮。`execute_publish_request.py --confirm-execute` 只允许 `skill_draft_push` 类型的本地草稿推送。

### 4. Link Recovery

发布后必须回填：

- 平台 URL
- 平台 post ID / 草稿 ID
- 发布时间
- 发布账号
- 截图或错误状态

### 5. Publish Guard

所有平台执行后都要通过 `record_publish_result.py` 回填并生成 `publish_verification_report.json`，禁止“只执行命令就宣称已发布”。

- `published_links`：仅允许 `status=published`、`verification_status=verified` 且带正式 `platform_url` 的结果进入。
- `draft_records`：仅允许 `status=draft|scheduled`、`verification_status=verified` 且带 `draft_id` 的结果进入。
- `draft_url` 必须与 `platform_url` 分离，草稿链接不得冒充正式发布链接。
- 同一 `topic_id` 多渠道分发时，公众号草稿 + 小红书/抖音/B站正式发布属于 `completed_with_mixed_status`，Postmortem 仍按一个 topic 聚合。
- Postmortem 只从已验真的 `publish_results` 计算 `published/drafted`，不得读取旧 `channel_pack.wechat_article_url` 作为成功发布证据。

## 标准输出

- `07_发布计划.md`
- `07_发布包.md`
- `channel_execution_manifest.json`
- `publish_verification_report.json`
- `publish_manifest.json`

## 旧能力去向

- `publish_video_supplement.py`：保留为兼容工具或 Transwrite 视频 lane 参考，不再是正式 Publish 主入口。
- `channel_adaptation_manifest.json`：旧适配层产物，不再是当前主链必需文件。
