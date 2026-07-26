---
name: dasheng-stage-publish
description: Use when entering the slim Dasheng publish execution stage to validate transwrite outputs, create publish packs, push drafts/manual packages, and recover published links.
---

# Dasheng Stage: Publish｜发布执行

## 定位

这是 `transwrite` 之后的轻量执行层。

正式阶段顺序：

`intake -> brief -> draft -> transwrite -> publish -> postmortem`

Publish 不再生成正文、封面、视频、播客或图表。上述生产动作全部归入 Draft / Transwrite。

## 正式输入

- `transwrite_manifest.json`
- `publish_decision.json`

缺少 `transwrite_manifest.json` 或 `publish_decision.json` 时禁止执行。

## 职责

1. 验收转写包是否具备对应渠道所需材料。
2. 生成公众号、微博、X、小红书、抖音、B站、播客等发布包。
3. 对可自动/半自动发布的平台生成执行器调用计划。
4. 对缺少执行器的平台导出人工发布包。
5. 发布后回收草稿 ID、正式链接、发布时间、截图或错误状态。

## 验收规则

Publish 不只看 lane `status`，还必须检查关键最终产物是否存在。

- 文字渠道：需要 `wechat_article.final.html` 或 `wechat_article.final.md`。
- 视频渠道：需要最终 MP4。
- 播客渠道：需要最终音频文件。
- 缺少关键产物时，即使 lane 标记为 `completed`，也必须写成 `blocked_or_waiting`。

## 标准命令

```bash
python3 scripts/build_stage5_publish.py \
  --transwrite-manifest 产物/06_转写生产/<run_id>/transwrite_manifest.json \
  --publish-decision 产物/07_发布执行/<run_id>/publish_decision.json
```

统一入口：

```bash
python3 scripts/run_mainline_stage.py publish --run-id <run_id>
```

安全预演：

```bash
python3 scripts/run_mainline_stage.py publish \
  --transwrite-manifest 产物/06_转写生产/<run_id>/transwrite_manifest.json \
  --publish-decision 产物/07_发布执行/<run_id>/publish_decision.json \
  --dry-run
```

`--dry-run` 只会生成 `publish_dry_run_report.json` 和各渠道执行计划，不会触发真实发布。

发布通路体检：

```bash
python3 scripts/run_mainline_stage.py doctor --publish
python3 scripts/run_mainline_stage.py doctor --publish --channel wechat_article --channel xiaohongshu_video
```

`doctor --publish` 不需要 `transwrite_manifest.json`，只检查本地 skill、外部依赖根目录、CLI 二进制和持久化浏览器 Profile 配置，不会打开浏览器、读取 cookies 或发布内容。

发布批次验收：

```bash
python3 scripts/publish_guard.py \
  --publish-manifest 产物/07_发布执行/<run_id>/publish_manifest.json

python3 scripts/run_mainline_stage.py doctor \
  --publish-manifest 产物/07_发布执行/<run_id>/publish_manifest.json
```

`publish_guard.py` 只检查某个发布批次的回填结果是否自洽，不检查依赖安装，也不会打开浏览器、读取 cookies 或发布内容。它必须同时读取 `publish_manifest.json` 与 `publish_verification_report.json`；缺少验真报告时不得通过。每条回填结果都必须能追到磁盘上的 `publish_result.json`，且文件中的核心发布字段必须与 manifest/verification 记录一致。它会重算 `publish_summary`，校验两份文件中的 `records` / `publish_summary` 是否一致，并校验 `published_links`、`draft_records`、待执行渠道、未验真链接和草稿/正式 URL 隔离。

默认模式会写出报告并回填 `publish_manifest.publish_guard`，即使未通过也返回 0，方便人工查看报告。CI 或正式门禁必须追加 `--fail-on-error`，未通过时返回非 0：

```bash
python3 scripts/publish_guard.py \
  --publish-manifest 产物/07_发布执行/<run_id>/publish_manifest.json \
  --fail-on-error
```

发布结果回填：

```bash
python3 scripts/record_publish_result.py \
  --channel-pack 产物/07_发布执行/<run_id>/channel_packs/<topic_id>/<channel>/channel_pack.json \
  --success true \
  --status draft \
  --draft-id <draft_id> \
  --verification-status verified \
  --account <account_name>
```

执行器或人工发布完成后必须用该入口回填平台 URL、草稿 ID、截图或错误状态。它只写回结果文件和验真报告，不会触发发布。

回填后 `publish_manifest.json` 与 `publish_verification_report.json` 会生成统一的 `publish_summary`：

- `pending_execution`：尚无渠道回填。
- `partially_recorded`：部分渠道已回填，仍有渠道待执行。
- `failed`：任一渠道回填失败。
- `all_drafted`：全部渠道只推送到草稿或定时草稿。
- `all_published`：全部渠道均回收正式发布状态。
- `completed_with_mixed_status`：全部渠道已回填，但草稿、正式发布、人工上传等状态混合。

草稿 ID 只能说明“已推草稿”，不得对外汇报为“已发布”。

`publish_verification_report.json` 中：

- `published_links` 只允许记录 `status=published`、`verification_status=verified` 且有正式平台 URL 的结果。
- `draft_records` 专门记录 `status=draft|scheduled`、`verification_status=verified` 且有草稿 ID 的结果。
- `verification_status=verified` 是进入 `published_links` 或 `draft_records` 的必要条件。
- `record_publish_result.py` 不会因为存在正式 URL 或草稿 ID 自动推断 `verified`；执行器或人工回填必须显式传入 `--verification-status verified`。
- 不得把草稿 ID 塞进 `published_links`。
- `status=published` 但没有正式 URL、或 `status=draft` 但没有草稿 ID 时，整体状态必须是 `needs_manual_verification`。

执行器标准 payload：

```bash
python3 scripts/build_publish_payload.py \
  --channel-pack 产物/07_发布执行/<run_id>/channel_packs/<topic_id>/<channel>/channel_pack.json
```

`publish_payload.json` 是平台执行器的统一输入，执行器完成后必须再调用 `record_publish_result.py` 回填结果。

安全执行入口：

```bash
python3 scripts/execute_publish_request.py \
  --execution-request 产物/07_发布执行/<run_id>/channel_packs/<topic_id>/<channel>/execution_request.json
```

默认只做 dry-run。只有当前会话明确确认后，才允许追加 `--confirm-execute` 调用受支持的本地 skill 路线；浏览器、人工包、外部 CLI 路线仍只输出下一步命令，不自动执行。

`--confirm-execute` 目前只允许 `skill_draft_push` 类型的本地草稿推送路线，例如公众号草稿推送。`api_first_cli`、`external_cli`、`mcp_fallback`、`browser_confirm_fallback`、`manual_package` 即便依赖可用，也只能生成执行计划和命令，不得由该入口自动调用。

## 标准输出

- `07_发布计划.md`
- `07_发布包.md`
- `publish_preflight_report.md`
- `channel_packs/<topic_id>/<channel>/channel_pack.json`
- `channel_packs/<topic_id>/<channel>/README.md`
- `channel_packs/<topic_id>/<channel>/publish_payload.json`
- `channel_packs/<topic_id>/<channel>/publish_result.json`
- `channel_execution_manifest.json`
- `publish_verification_report.json`
- `publish_manifest.json`
- `publish_guard_report.json`（可选，批次验收输出）

## 平台执行器矩阵

- 公众号：`baoyu-post-to-wechat` / `wechat-multi-publisher` / `md2wechat`
- 微博：`baoyu-post-to-weibo`
- X：`baoyu-post-to-x`
- 小红书：`dasheng-xhs-publish-bridge` → `all-in-one` / `xhs-skills` / `spider-xhs` / `xiaohongshu-mcp` / `rednote-mcp`
- 抖音：`douyin-upload-skill`
- B站：`bilibili-upload-bridge`
- 播客：人工上传或音频平台 API
- 验真：`publish-guard`

## 浏览器登录态

浏览器型发布必须使用持久化发布 Profile，不得使用 Chrome DevTools MCP 临时 profile、一次性自动化 profile 或项目目录保存 cookies。

统一配置：

```bash
configs/publish/browser_profiles.json
```

统一打开命令：

```bash
python3 scripts/open_publish_browser.py xiaohongshu_video
python3 scripts/open_publish_browser.py douyin_video
python3 scripts/open_publish_browser.py wechat_article
```

每个 `channel_pack.json` 必须写入 `browser_profile`，包括 `profile_dir`、`entry_url` 和 `open_command`。Agent 只允许复用该 profile 目录，不允许读取、导出、复制或提交 cookies。

## 强约束

1. 只允许 `completed` / `packageable` 的 transwrite lane 进入发布执行包；兼容旧文字包时 `ready_base_package` 可视为可打包。
2. 不允许把 `planned_for_render`、`ready_for_agent_execution`、`ready_for_skill_execution`、`blocked_missing_api_key` 等状态误报为可发布。
3. 没有正式执行器的平台，只能导出人工发布包。
4. 任何浏览器/平台发布动作都必须经过人工确认。
5. 未经过链接回收和 `Publish Guard` 验真，不得回报“已发布”。
6. 旧 `scripts/publish_video_supplement.py` 仅作为兼容工具或视频补充参考，不再是正式 publish 主入口。
7. 发布包、截图、平台回执、临时 HTML、上传素材副本不得写入 `skills/` 目录；默认写入 `产物/07_发布执行/<run_id>/...`。
8. 小红书、抖音、公众号等需要登录的平台必须通过 `scripts/open_publish_browser.py` 打开持久化 Profile 完成登录和上传准备。
9. 小红书主路径优先 API-first Skill/CLI/MCP，浏览器自动化只做 fallback；不要把它降级成纯手动搬运。
