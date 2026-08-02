# Publish 技能矩阵

更新时间：`2026-06-14`

## 当前原则

Publish 不生产正文、图表、封面、视频或播客。它只读取 `transwrite_manifest.json` 中已完成或可打包的 lane，生成平台发布包、执行器请求、人工包和发后验真记录。

## 平台矩阵

| 平台 | 主执行器 | 备选/辅助 | 自动化等级 | 当前决策 |
| --- | --- | --- | --- | --- |
| 微信公众号 | `baoyu-post-to-wechat` | `wechat-multi-publisher`、`wechat-public-cli`、`md2wechat` | 半自动/草稿优先 | 直接集成 |
| 小红书 | `dasheng-xhs-publish-bridge` | `all-in-one`、`xhs-skills`、`spider-xhs`、`xiaohongshu-mcp`、`rednote-mcp`、`xiaohongshu-auto` | API-first + browser fallback | 直接集成 |
| 抖音 | `douyin-upload-skill` | `social-auto-upload` | 官方 API + fallback | 直接集成 |
| B站 | `bilibili-upload-bridge` | `biliup-rs`、`bilibiliupload`、`social-auto-upload` | 手动/半自动 | 已新增包装 skill |
| 微博 | `weibo-manager` | `baoyu-post-to-weibo` | 强审批/半自动 | 短帖强审批，长文半自动 |
| X | `baoyu-post-to-x` | `xurl`、`x-cli`、`Postiz` | 半自动/API fallback | 直接集成 |
| 知乎 | `zhihu-post` | 浏览器自动化 | 半自动 | 按需启用 |
| 视频号/快手/百家号/TikTok | 暂无 Dasheng 主执行器 | `social-auto-upload` | 待验证 | 后续统一视频桥 |

## 本地已具备 Skills

| Skill | 来源 | 角色 |
| --- | --- | --- |
| `baoyu-post-to-wechat` | `boutique-openclaw-skills` / 本机已安装 | 公众号单篇文章、图文、HTML/Markdown 发布 |
| `wechat-multi-publisher` | `boutique-openclaw-skills` | 多篇文章推草稿箱 |
| `wechat-public-cli` | `boutique-openclaw-skills` / 本机已安装 | 公众号 CLI fallback |
| `baoyu-post-to-weibo` | `boutique-openclaw-skills` | 微博长文/图文半自动 |
| `weibo-manager` | `boutique-openclaw-skills` | 微博短帖强审批流 |
| `baoyu-post-to-x` | `boutique-openclaw-skills` | X 文本、图片、视频、X Article |
| `dasheng-xhs-publish-bridge` | 本仓库 | 小红书 API-first / browser fallback 发布桥 |
| `xiaohongshu-auto` | `boutique-openclaw-skills` | 小红书发布执行器 |
| `xiaohongshu-ops` | `boutique-openclaw-skills` | 小红书发布前演练、发布后运营维护 |
| `all-in-one` | `cv-cat/All-IN-ONE` | 小红书/微博/抖音统一 CLI + skill 参考 |
| `xhs-skills` | `cv-cat/XhsSkills` | Spider_XHS 的薄 skill 包装 |
| `spider-xhs` | `cv-cat/Spider_XHS` | 小红书 API/source-of-truth |
| `xiaohongshu-mcp` | `xpzouying/xiaohongshu-mcp` | MCP publish/search/access 参考 |
| `rednote-mcp` | `TimeCyber/mcp-xiaohongshu` | 浏览器/MCP 参考 |
| `xhs-downloader` | `JoeanAmier/XHS-Downloader` | 素材与竞品采集，不作发布主链 |
| `douyin-upload-skill` | `boutique-openclaw-skills` | 抖音官方上传与 fallback outbox |
| `zhihu-post` | `boutique-openclaw-skills` | 知乎专栏/想法发布 |
| `publish-guard` | `boutique-openclaw-skills` | 发后验真、凭据和审计参考 |
| `social-auto-upload-bridge` | 本仓库 | 外部 `social-auto-upload` 多视频平台桥 |
| `bilibili-upload-bridge` | 本仓库 | B站投稿桥，优先 `biliup-rs`，fallback `social-auto-upload` |

## 外部候选

| 项目 | 地址 | 适合用途 | 决策 |
| --- | --- | --- | --- |
| `social-auto-upload` | `https://github.com/dreammis/social-auto-upload` | 抖音、B站、小红书、快手、视频号、百家号、TikTok 等视频上传 | 作为外部依赖桥，不 vendoring |
| `All-IN-ONE` | `https://github.com/cv-cat/All-IN-ONE` | 小红书/微博/抖音统一 CLI & skill 参考 | 作为 API-first 发布参考 |
| `XhsSkills` | `https://github.com/cv-cat/XhsSkills` | 小红书接口 skill 包装 | 作为 API-first 主候选 |
| `Spider_XHS` | `https://github.com/cv-cat/Spider_XHS` | 小红书 API/creator 能力底座 | 作为 API-first 主候选 |
| `xiaohongshu-mcp` | `https://github.com/xpzouying/xiaohongshu-mcp` | 小红书 MCP 发布/访问 | 作为 MCP 候选 |
| `rednote-mcp` | `https://github.com/TimeCyber/mcp-xiaohongshu` | 小红书 MCP 发布/访问 | 作为 MCP 候选 |
| `XHS-Downloader` | `https://github.com/JoeanAmier/XHS-Downloader` | 下载/采集/竞品素材 | 不作为发布主链 |
| `biliup-rs` | `https://github.com/biliup/biliup-rs` | B站命令行投稿、登录、上传、追加稿件 | B站首选包装对象 |
| `bilibiliupload` | GitHub/PyPI 同名项目 | Python B站上传库/CLI | B站 fallback |
| `Postiz` | `https://github.com/gitroomhq/postiz-app` | 海外社媒排程，X/TikTok/YouTube/LinkedIn 等 | 海外平台排程候选 |
| `xurl` | `https://github.com/xdevplatform/xurl` | X 官方 API CLI、媒体上传 | X API fallback |
| `x-cli` | `https://github.com/Infatoshi/x-cli` | X/Twitter API v2 CLI | X API fallback |

## 执行模式

| 模式 | 含义 | 适用平台 |
| --- | --- | --- |
| `api_official` | 官方 API 上传/发布 | 抖音、X、公众号部分路径 |
| `browser_confirm` | 浏览器填充，人工确认发布 | 公众号、X、微博头条、知乎 |
| `approval_required` | Request -> Approve -> Execute | 微博短帖 |
| `manual_package` | 只导出人工发布包 | B站/视频号未配置执行器时 |
| `fallback_export` | 自动失败后导出 outbox | 抖音、B站、小红书 |

## 强约束

1. 所有平台必须先生成 `channel_pack.json`，再调用执行器。
2. 浏览器型、审批型平台不得自动点击最终发布按钮。
3. 微博短帖必须走 `weibo-manager` 审批流。
4. 小红书优先走 API-first / MCP / CLI，只有失败时才切浏览器 fallback。
5. B站在 `bilibili-upload-bridge` 未完成真实提交和验真前不得标记自动发布完成。
6. `social-auto-upload` 作为外部依赖调用，不把运行产物写入 skill 目录。
7. 没有 `Publish Guard` 或平台回执验真，不得回报“已发布”。

## 后续开发

1. `build_stage5_publish.py` 为每个 channel pack 输出 `execution_request.json` 和 `verification_request.json`。
2. `run_mainline_stage.py publish --dry-run` 输出 `publish_preflight_report.md`，汇总每个平台的选中路线、缺失依赖、浏览器 Profile 和人工确认要求。
3. `run_mainline_stage.py doctor --publish` 提供不依赖内容包的发布通路体检，只检查 skill、外部依赖、CLI 和持久化 Profile 配置。
4. 实现 `bilibili-upload-bridge` 的执行脚本。
5. 实现 `social-auto-upload-bridge` 的 channel_pack 转换器。
6. 为每个平台补更细的登录态、API key、权限、每日限额检测；不得读取或导出 cookies。
