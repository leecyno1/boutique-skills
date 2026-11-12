# Findings

## 2026-11-11（分类器完善：消灭兜底桶与跨词误命中）

已解决：

- **触发**：上一轮把 taste 提为标准默认后，发现分类器还有两类静默错分，用户要求完善。
- **兜底桶清空**：`commerce-ops` 没有任何关键词，是“全不命中”的兜底桶，16 个技能 silently 落在这里（ablation-planner、auto-paper-improvement-loop、blueprint-figure、check-understanding、cli-chat、cli-batches、gstack、gws-chat-send、inference-skills、ponytail-debt/help/review、story-deslop/import/long-analyze、after-hours-editorial-template）。逐个读 SKILL.md 并按同家族惯例归类后，兜底桶为 0。
- **跨词误命中**：`BOUNDARY_KEYWORDS` 从 `{"ui"}` 扩到 `{"ui","ios","media","vision"}`。实证：`ios` 命中 "ratios"（baoyu-image-gen 被判 coding-devtools）、"scenarios"；`media` 命中 "immediate"（analytical-method-validation）、"medians"（ponytail-gain）；`vision` 命中 "revision"（reflection 被判 media-generation）。加边界后 reflection→agent-orchestration、baoyu-image-gen→media-generation 自动归位。
- **另外 11 个核对过的误判**：cli-a2a（"tasks" 判成 productivity-pkm）、cli-backup-sync（判成 data-analysis）、cli-compression / caveman-compress / caveman-commit（压缩的是提示词与提交信息，不是图片，却判成 media-generation）、cavecrew（子代理委派，判成 media-generation）、seo-agentic / seo-cluster（SEO 家族应在 marketing-growth）、agentmail（"drafts" 判成 writing-content，应与 agentmail-cli/toolkit 一致归 communication）、build-project（课程导师，判成 search-research）、analytical-method-validation（ICH/USP/ISO 合规验证，应归 legal-compliance）。
- **结构调整**：`classify_category` 里的局部 `explicit` 字典提升为模块级 `CATEGORY_OVERRIDES`（52 → 80 条，新增条目按家族分组并写明理由），便于测试与维护。
- **新门禁**：`tests/test_category_classifier.py`（6 个用例）断言①兜底桶只能由显式覆盖产生②目录分类与分类器实时计算一致（防手改/忘记重生成）③覆盖表分类名合法④跨词误命中回归⑤真实术语仍命中⑥`>-`/`|-`/`|2` 等块标量头解析出正文。已接入 `weekly_cycle.sh` 第 9 步，周度测试从 5 个变 6 个。
- **影响面**：30 个技能分类变化，coding-devtools 17→27、agent-orchestration 8→12、media-generation 43→38、writing-content 15→17、communication 2→4、marketing-growth 21→23、commerce-ops 16→0；5★ 89→100、4★ 164→152、3★ 58→59；L2 118→128、L3 187→177。**安装档 low/medium/high 未变（53/68/317），标准包仍 21 位且 frontend 仍是 design-taste-frontend，金融组合仍 28 位。**
- **门禁**：audit 317/311、missing_skills 0、duplicate_capabilities 0、standard_bundle_issues 0；syntax 1266 py + 394 js，errors 0；risk 15/15 new 0；6 个测试全 OK。

待观察：

- 分类联动评分与纵向分层，所以归位会改分数：seo-agentic 81→74、baoyu-image-gen 78→71、cli-backup-sync 92→79（都因离开 L2 分类）。这是评分模型既有设计，不是本轮引入；若认为“分类不该影响分数”，要单独改评分器。
- 关键词表还有已知的宽匹配没动：`search` 命中 "research"、`market` 命中 "marketing"、`dev` 命中 "development"、`compress` 命中 "compressed"。这些要么结果尚可接受，要么已有覆盖表兜住；改成词边界会连带产生新兜底，需要逐个核对后再动。

## 2026-11-11（设计去重：taste 设为标准默认，其余按“优于或互补”筛）

已解决：

- **规则**：用户裁定 taste-skill 为标准默认设计库；未定位来源的要重定位；其他设计技能优于 taste 或与 taste 互补则留，否则按重复出库。
- **重定位**：`frontend-design` 定位成功 = `anthropics/skills@00756142`（2025-12-04，上游只有 SKILL.md + LICENSE.txt；SKILL.md 逐字比对 94.67% 相同，本地 4133B / 上游 4440B）。`web-animation-design` 定位失败：无 SOURCE.txt、未注册 origin，GitHub 代码搜索只命中聚合与镜像（LeoYeAI/agent-master-skills、gabrielmoreira/agent-skills-mirror、clonetimer/Clonetimer-Skills、caffeinepub/it-ugi 及若干 vendored 副本），无 license 无署名；内容是 Emil Kowalski animations.dev 课程指南，与在库且来源已核验的 `review-animations`（98，含 STANDARDS.md）同源重复。
- **出库 4 个**：`animation`（bytesagain，677 行 shell 包 CSS keyframes，模型原生已覆盖）、`impeccable`（pbakaus，另一套 24 命令设计流派，taste 96 > 92 且自带 lint.mjs 禁令扫描 + inspect.mjs 真实浏览器验收）、`frontend-design`、`web-animation-design`。前两个走 `remove_skill`（同步清 default-skills.json 与 native-origin-overrides.json），后两个未注册走 `git rm`。仓库 319 → 317。
- **本机归档 4 份**：`frontend-design`、`web-animation-design` 各 Qoder + Codex 一份。dry-run 全部 `refused_active`（近期有调用），按人工裁定用 `--include-active --confirm`，回执 `archived: 4`。`animation`、`impeccable` 本机未安装，只在仓库出库。
- **保留（互补，不重复）**：`review-animations` 98（动画审查，taste 无此岗）、`pick-ui-library` 92（组件库选型）、`scroll-world` 93（滚动叙事视频，seedance/kling 链路，不是前端页面）、`generative-ui` 92（对话内联 widget/图表）、`huashu-design` 81（原型/演示/信息图/视频，SKILL.md 明确排除生产级 Web App 与 SEO 站点）、`gsap` ×8（各 92，GSAP 官方 API 知识，不是设计流派）、taste 家族 13 个。
- **taste 成为默认**：`CAPABILITY_RULES` 的 frontend 候选加 `design-taste-frontend`，标准包 frontend 槽位由 `generative-ui`(92) 换成 `design-taste-frontend`(96，direct，无 key)。`generative-ui` 仍在库，承担内联 widget 岗位。标准包仍 21 位、金融组合仍 28 位。
- **防回流**：`retired-skills.json` 138 个 id（+4）、9 个整库屏蔽（+`bytesagain/ai-skills`、`pbakaus/impeccable`）；`design_school_decision` 补 `standard_default`/`dedupe_rule`/`kept_complementary`/`retired_duplicates`，`pending_user_decision` 清空。
- **顺带修两个目录生成器 bug**（都是把 taste 提上默认后才暴露）：
  1. `parse_frontmatter` 只认 `|`/`>`，不认 `>-`/`|-` 这类带 chomping 的块标量头，4 个技能的 description 变成字面 `">-"`（design-taste-frontend、baoyu-translate、achieving-cmmc-level-2-compliance、westockdata），标准包 note 也显示 `">-"`。改为正则 `[|>][+-]?\d*`。
  2. 分类器 `ui` 用裸子串匹配，`quick`/`build`/`guide` 都命中 design-ui。description 修好后 `baoyu-translate` 因 “quick mode” 被误判成 design-ui 并抬到 92 分。给这类关键词加词边界（`BOUNDARY_KEYWORDS = {"ui"}`），11 个技能回到正确分类：baoyu-article-illustrator→media-generation、baoyu-translate→writing-content、memu→agent-orchestration、ponytail-audit→security-audit、agentmail-toolkit→communication 等。design-ui 45→34，5★ 98→89，L2 129→118 / L3 176→187；安装档 low/medium/high 未变（53/68/317）。
- **impeccable 独有能力备忘**（日后要补 taste 可从这几处取）：`live`/`generate` 浏览器变体循环、PRODUCT.md/DESIGN.md 项目上下文、`reference/ios.md` 与 `android.md` 原生平台参考。
- **门禁**：audit 317/311，missing_skills 0、duplicate_capabilities 0、standard_bundle_issues 0；syntax python 1266 / js 394（-108 全是 impeccable 的 .mjs/.js）errors 0；risk 15/15 new 0；5 个测试全 OK。

待观察：

- `frontend-design` 是高频技能（833 次调用、近 30 天 363 次，最后 2026-11-04），归档会改变日常行为；同岗位由 `design-taste-frontend` 承担。`web-animation-design` 33 次 / 近期 32 次，只在 Codex。要回退：`mv ~/.{qoder,codex}/skills-archive/<name> ~/.{qoder,codex}/skills/`。
- 分类器还有兜底桶问题：`check-understanding`、`gstack`、`ponytail-help` 落到 commerce-ops（无关键词命中），`analytical-method-validation` 落到 media-generation。已不是 design-ui 误判，但分类仍不准，待单独处理。（已于本日第三轮完善，见上一节）
- `web-animation-design` 若日后定位到 canonical 上游且证明优于 taste 体系，删登记表条目即可重新导入。

## 2026-11-11（设计流派收敛：只留 taste 一家）

已解决：

- **触发**：用户给的小红书帖子指向 `elayadesign/ai-design-skills`（15242 星，MIT，2026-11-01 有推送），问是否值得入库。核查结论：不入库。
- **理由一（规则互斥）**：elaya 与已在库的 taste-skill 同属反 AI 味设计流派（都黑名单 Inter/Roboto、推 Geist、禁渐变、同心圆角），但规则冲突且都自称优先——taste 允许 shader/WebGL/表现性瞬间，elaya 锁死封闭 token 集并全面禁渐变。两套同时装载会互相打架。用户裁定：**设计流派只留 taste 一家**。
- **理由二（跑不起来）**：同库 `figma-designer` 依赖 Figma MCP，本机 Figma 工具数为 0，装了也无法执行。
- **理由三（门槛）**：用仓库自己的评分器跑该库得 70 分进 review，且 `skill_subdirs=2 < MONOREPO_MIN_SUBDIRS=3`，自动入库分被抬到 101（不可达），本来就不会自动进库。
- **本机执行**：`landing-page-design` 两份旧副本（Qoder + Codex，18.8KB，落后上游 22.1KB）经 `pending-cleanup.json` → `uninstall_skills.py --include-active --confirm` 归档，回执 `archived: 2`。`redesign-existing-projects` 本机原为 elaya 版（哈希 `6558d92fdeb2`，与上游逐字一致），先备份到 `~/.{qoder,codex}/skills-archive/redesign-existing-projects-elaya-20261111/`，再替换为仓库 taste 版（`0713bbfa0337`）。两个运行时现存 8 个设计技能完全一致。
- **防回流**：`catalog/retired-skills.json` 新增 `design-school` 分组（`landing-page-design`、`figma-designer`）与 2 个整库屏蔽（`elayadesign/ai-design-skills`、`elayadesign/redesign-skill`），并记录 `design_school_decision`。仓库里的 `redesign-existing-projects` origin 指向 `Leonxlnx/taste-skill`，屏蔽 elaya 不影响它。
- **新测试抓到一个旧错**：`tests/test_retired_guard.py` 加了 `test_blocked_repos_do_not_cover_live_origins`（整库屏蔽不得覆盖在库技能的 origin），一跑就报 `frontend-dev -> anthropics/skills/tree/main/skills/canvas-design`。2026-11-02 因为退役 `skill-creator` 把 `anthropics/skills` 整库屏蔽了，但该库还养着在库的 `frontend-dev`（71 分）。按登记表自己的规则（与存活技能共用的仓库只作 id 级跳过），已把它从 `blocked_repos` 移到 `shared_repos_not_blocked`。现状：134 个 id、7 个整库屏蔽、10 个共用不屏蔽。影响面：屏蔽只作用于发现阶段，`frontend-dev` 的上游同步一直正常，属潜在治理漏洞而非线上故障。
- **2026-11-07 那次取消的运行留下了未发布内容**：工作区有 1564 个未跟踪文件（38MB，全是 `design-taste-frontend` 的 taste-skill v2 素材：958 svg / 122 js / 110 html / 66 webp 等，最大单文件 868KB，无 node_modules、无密钥）加 8 个已跟踪文件改动（taste 的 library/references、`memu`、`baoyu-format-markdown`）。ctime 显示素材在 11-07 10:24 落位、memu/baoyu 在 10:28 写入，都晚于 10:00 的发布提交 `9aa8571`，Quest 在 10:29 被取消，所以这批上游同步结果从未入库。本轮先单独提交这批遗留，再提交流派裁定。
- **顺带校正**：`docs/WEEKLY_CURATION.md` 组合表还写着标准包 30 / 金融组合 34，实际已是 21 / 28；金融组合带 key 位 13/34 → 10/28；标准包跳过位去掉已不跳过的 finance-data；补写 `--include-active` 只用于人工裁定。`QODER_HANDOFF.md` 的技能数还停在 11-02 的 304，实际 11-07 重生成后是 319，已按 `catalog/skills.enriched.json` 的 summary 全量刷新。

待用户裁决（已于本日第二轮裁定，见上一节）：

- “只留 taste 一家”是否延伸到其余非 taste 设计流派（分数已核对 `catalog/skills.enriched.json`）：`emilkowalski/skills` 的 review-animations 98 / pick-ui-library 92、`pbakaus/impeccable` 92、`oso95/scroll-world` 93、`bytesagain/ai-skills` 的 animation 92、`himself65/finance-skills` 的 generative-ui 92（占标准包 frontend 槽位）、`alchaincyf/huashu-design` 81，以及 `greensock/gsap-skills` ×8（各 92，属库 API 知识，是否算流派待定）。这些评分高、有脚本或私有知识，不属“被模型覆盖”，等明确指令再处理。
- 另有 `frontend-design`、`web-animation-design` 两份：在 `skills/default/` 磁盘上、两个运行时也装着，但既不在 `default-skills.json` 也没有 SOURCE.txt（未注册、来源不明）。要不要补来源登记或一并归档，同样待裁决。

## 2026-11-07（周度治理：大响应截断导致发现阶段中断）

已解决：

- **症状**：`weekly_cycle.sh` 第 1 步在导入 `openclaw/openclaw` 时崩溃，`api_get` 的 `response.read()` 抛 `http.client.IncompleteRead: IncompleteRead(7838061 bytes read, 9372983 more expected)`。该仓库 recursive tree 响应约 17MB，urllib 读到约 7.8MB 后被截断。
- **根因**：`api_get` 只对 `HTTPError`/`URLError`/`OSError` 做回退，`IncompleteRead` 属于 `http.client.HTTPException`，不在这三类里，因此 curl 回退从未触发，异常直接冒泡终止流水线。`check_upstream_updates.py` 的 `api_get`、以及两个脚本的 `raw_file_bytes` 有同样缺口。
- **修复**：两个脚本均 `import http.client`，`api_get` 与 `raw_file_bytes` 的传输异常捕获扩展为 `(OSError, http.client.HTTPException)`，截断读同样走 curl 回退。实测修复后同一 tree 请求经回退 8.8 秒取回 67401 条、`truncated=false`。
- **重跑**：修复后从头重跑完整 11 步（见本轮后续记录）。

## 2026-11-02（过时退役：新模型 / harness 覆盖的技能）

已解决：

- **判定标准**：只看 skill 里有没有模型不知道、harness 也没提供的东西（私有 CLI、真实端点与限流、凭证约定、用户自有流程、可跑脚本）。没有的归为第一层（流程/元技能 47、人设 4、纯知识 23、薄封装 6、anthropic-fs 纯 prompt 60、llmquant 路由壳 18），同能力多份的归为第二层（PPT/Excel/PDF/网页读取/生图/公众号/视频/个股/财报/alphaear 各留带脚本的一份）。分析全文 `reports/usage/obsolescence-analysis-2026-11-02.md`。
- **本机**：193 个技能、300 份副本归档（`uninstall_skills.py --include-active --confirm`，新增 `--include-active` 以绕过“近期有调用”安全网，因为这是人工决策）。Qoder 292→132，Codex 241→100。回执在 `reports/usage/cleanup-receipts.jsonl`。
- **仓库**：132 个在库技能出库（`remove_skill` 同步清 default-skills.json 与 native-origin-overrides.json），目录 436→304，标准包 30→21，金融组合 34→28，L1 21→12。顺带清掉 wrapper-origins 8 条、risky-baseline 1 条（minimax-xlsx）、standard-bundle-overrides 3 条过时排除、skillopt 候选里的 skill-creator。
- **防回流**：新增 `catalog/retired-skills.json`（132 id、6 个整库屏蔽：obra/superpowers 等；9 个与存活技能共用的仓库不屏蔽，靠 id 级跳过）。`weekly_curation.py` 的 discover 把屏蔽库并入 known、`register_candidate` 跳过退役 id；`tests/test_retired_guard.py` 覆盖并断言退役 id 不在目录与磁盘上。
- **语法门禁环境坑**：本会话 `python3` 解析到 anaconda 3.11，`uzi-skill` 里 PEP 701 f-string 被误报为语法错误（3.12+ 正常）。`check_skill_syntax.py` 现在在 <3.12 时自动 re-exec 到 python3.14/3.13/3.12 或 `/opt/homebrew/bin/python3`，避免周六 Quest 因解释器版本误阻断发布。

待观察：

- codex ecc 一族（tdd-workflow 991 次、e2e-testing 972、security-review 667、frontend-patterns 534、search-first 485）内容通用但被频繁加载，本次按用户决定一并归档。一周内若 Codex 行为明显退化，从 `~/.codex/skills-archive/` 搬回即可。
- 第三层保留的量化脚本（7 个 screener、13 个 market-regime 探测器、11 个 edge-pipeline）几乎零调用，但有脚本和 key 约定，不属于“被模型覆盖”，未动。

## 2026-11-02（本机 skills 清理）

已解决：

- 刷新遥测后全机 576 个已安装技能，推荐引擎给出 29 个零调用/未收录的卸载候选；另补 9 个长期零调用或仓库已出库的旧副本（openclaw-stock 系 3 个、doc、wechat-topic-outline-planner、anthropic-fs-wealth-management 3 个、funda-data），共 38 个执行归档式卸载。
- 归档分布：Qoder 19 个、Codex 19 个；`~/.qoder/skills` 312 → 292，`~/.codex/skills` 263 → 241，`~/.lingma/skills` 3 → 2。归档目录：`~/.qoder/skills-archive/`（2.7MB）、`~/.codex/skills-archive/`（89MB），回执在 `reports/usage/cleanup-receipts.jsonl`。恢复方式：`mv <archive>/<skill> <原路径>`。
- 顺手清掉 3 个断链（`using-coze-cli` ×2、`dasheng-video-omni-browser` ×1）、2 个空目录（`codex-primary-runtime`、`lichengyin-dev-habits`），旧备份 `ima-skill.bak.20260926` 移入 Codex 归档。
- `pending-cleanup.json` 状态已写为 executed；下次周更会重新生成。

待观察：

- 仍有 187 个“零调用 + 仓库内旧版本”安装副本（Qoder 154 / Codex 126，含重叠），以及 74 个“在用但内容旧”的副本。它们不是确定的垃圾，未动；若要瘦身，优先按运行时归档零调用副本；若要保留能力，应从仓库同步更新而不是删除。

## 2026-10-31（周度治理修复：上游同步、发布门禁与目录改名）

已解决：

- **治理停摆一个月**：Quest 自 2026-09-30 起 `enabled=false`，10 月无任何提交。旧任务的执行域是 `chatOnly`，即使启用也拿不到仓库目录。已新建 directory 域任务 `436c5b6e-10c6-487b-b73a-1504e4cc89c0`（cwd 绑定仓库、周六 09:00 Asia/Shanghai、Full Access、独立会话），旧 chatOnly 任务与上一版 workspace 域任务均已删除。
- **周度流程从 10 步扩到 11 步**：新增第 3 步上游同步（`check_upstream_updates.py --apply`，该命令同时产出 `reports/upstream-check-latest.*`，不必再单独跑只读遍），第 9 步扩为审计 + 语法门禁 + 风险门禁 + 单元测试。
- **新增 `scripts/check_skill_syntax.py`**：全量内存编译 `skills/default` 下的 Python（1379 个）与 `node --check` 校验 JS（355 个），不落 `__pycache__`，实测 0 错误。上游自动同步会直接写入第三方代码，没有这道门禁时语法错误会静默入库。
- **新增 `scripts/check_new_risks.py` 与 `catalog/risky-baseline.json`**：把审计的 `(skill, file, pattern)` 风险命中固化为基线，出现基线外的新组合即阻断发布，避免上游更新静默带入 `curl | sh`、`eval(` 之类内容。首跑即生效。
- **首次自动上游同步**：436 个来源 → 118 个技能更新（468 个修改 + 227 个新增文件，全部位于 `skills/default`；无删除、无二进制、无缓存）。`current` 171、`source_path_missing` 52、`metadata_only_root_no_skill_md` 59、`metadata_only_root_too_large` 1、`wrapper_origin` 35。
- **门禁实际拦下一条**：`huashu-design/scripts/verify-video.sh:48` 把 ffprobe 的 `avg_frame_rate`（`num/den`）经字符串插值送进 Python `eval`。取值受限于 ffprobe 的数值比，判为低风险；已连同理由写入基线。不本地改的原因：周度上游同步会把补丁覆盖回去，反而让流水线每周阻断——要改应向上游提。
- 重建结果：458 技能（high 458 / medium 85 / low 67）、标准包 30、金融组合 34、`needs_origin_review=0`；审计 `missing_skills`/`duplicate_capabilities`/`missing_native_origins`/`standard_bundle_issues` 全 0，`missing_env` 149→151，`risky_hits` 15→16（即上述那条）。三个测试文件全通过。
- **本地目录改名**：`/Volumes/PSSD/Projects/boutique-openclaw-skills` → `/Volumes/PSSD/Projects/boutique-skills`，与 GitHub 仓库名一致。原同名陈旧检出（`e16c7a0`，2026-08-16，含 4 个受保护 tushare-eval 文件的未提交改动）已归档为 `boutique-skills.stale-2026-08-16`，未删除。

未决：

- `source_path_missing` 52 个当日已修复（30 迁移 + 22 出库），详见下一节。
- `~/.qoder/skills` 没有 `agent-reach` 副本（`~/.claude/skills`、`~/.agents/skills` 有，CLI 在 `~/.local/bin`）。它已在仓库与标准包 `social-research` 槽位，周更会自动同步其上游。

## 2026-10-31（续：上游路径级治理）

已解决：

- **origin 自动迁移**：`check_upstream_updates.py` 遇到 `source_path_missing` 时按证据强度找新位置——SKILL.md 内容哈希（git blob）最优先，其次唯一同名目录，最后在版本/稳定分支里找原路径；同名目录有歧义、或只存在于未合并功能分支时不猜。命中后写回 `catalog/native-origin-overrides.json` 与 `SOURCE.txt`，并从新路径同步。52 个失效路径中 30 个迁移成功：
  - 15 个 `alphagbm-*` → `skills/{category}/<name>`（main）；
  - 12 个 taste 系技能 → `Leonxlnx/taste-skill` 的 `taste-skill-v1.9` / `taste-skill-v2` 分支（v1.9 与本地 SKILL.md 逐字节一致；v2 的部分子技能内容已改写，故按内容哈希分别选取，避免误升到 v2）；
  - 3 个 `anthropic-fs-wealth-management-*` → `plugins/agent-plugins/meeting-prep-agent/skills/`（main）。
- **路径级出库**：`weekly_curation.py prune --upstream-report reports/upstream-check-latest.json` 把仍是 `source_path_missing` 的行转为 `upstream_path_missing` 出库建议；报告 URL 与当前 override 不一致时跳过，避免旧报告误删刚迁移的技能。周度顺序改为先同步后出库。
- **22 个孤儿确认删除**：AlphaGBM 15（alert、buffett-analysis、company-profile、compare、duan-analysis、fear-score、health-check、investment-thesis、macro-view、marks-cycle、take-profit、tepper-signal、theme-research、vix-status、watchlist），anthropics 3（portfolio-rebalance、financial-plan、tax-loss-harvesting），dasheng 2（stage-brief-ai、stage-draft），`dasheng-video-omni-browser`（仅剩 docs/archive 快照），`funda-data`（上游已移除该插件）。
- **测试**：新增 `tests/test_upstream_relocation.py`，覆盖内容哈希优先、唯一同名才用、歧义不猜、版本分支原路径四种判定，已接入周度第 9 步；四个测试文件全通过。
- **验证与发布**：重建后 436 技能、标准包 30、金融组合 34；审计 `missing_skills`/`duplicate_capabilities`/`missing_native_origins`/`standard_bundle_issues` 全 0，`missing_env` 135，`risky_hits` 16 与基线一致；语法门禁 1384 Python + 354 JS，0 错误。已推送 `462c20e`，GitHub 与 Gitee SHA 一致。

待观察：

- 迁移到版本分支的 12 个 taste 技能不会跟随 main 的 v2 演进；这是有意选择（保持与已审内容一致），后续若要升 v2 需逐个复核并按新内容重新评分。
- `AlphaGBM/skills` 迁移后的 SKILL.md 与本地快照存在差异（上游已更新），本轮按上游覆盖，属正常同步；新增的 scripts/ 一并入库。

同日清理：

- 旧克隆 `~/Desktop/Projects/boutique-skills`（`613ce5d`，2026-08-09）唯一的本地增量是 `wechat-multi-publisher` 的 `package.json` / `package-lock.json`（另有两个 `node_modules/`，共 220MB）。依赖清单对复现有帮助，已并入主仓库；`node_modules/` 加入 `.gitignore`。其余无跟踪改动，克隆整体归档到 `/Volumes/PSSD/Projects/boutique-skills.stale-desktop-2026-10-31`。
- `~/.qoder/skills/agent-reach` 建立指向仓库 `skills/default/agent-reach` 的软链，Qoder 侧可直接发现并随周更更新；CLI 在 `~/.local/bin/agent-reach`。
- 仓库只有 `main` 一个分支（本地、origin、gitee 均无其他分支）。

## 2026-09-30（补漏周度治理 + curl 传输加固：token 泄露与上游检查卡死）

已解决：

- 2026-09-12 记录的残留项：curl 回退把 GitHub token 放在子进程命令行（`ps aux` 可见）。已改为 `curl --config -` 从 stdin 传 header，token 不再进入 argv；`_curl_config_escape` 负责 config 值转义。新增 `tests/test_curl_token_hygiene.py`（token 不入 argv、转义、无 header 时不加 `--config`），已接入 `scripts/weekly_cycle.sh` 第 8 步。验证：authenticated `rate_limit` 返回 limit=5000、raw 文件下载 200、404 仍返回 None、上游改名仓库 301 仍跟随。
- 补漏周度治理（09-19、09-26 因 Quest 暂停未触发）：发现阶段评估 41 个候选，自动入库 5 个仓库 21 个 Skill（claude-seo 5 个 SEO、auto-claude-code-research-in-sleep 6 个科研、oh-story-claudecode 4 个写作、claude-bughunter 5 个漏洞赏金、memu 1 个记忆）；prune 检查 415 个上游，0 项移除。目录 458 个技能（high 458 / medium 85 / low 67），标准包 30，金融组合 34，needs_origin_review = 0。审计 `missing_skills=0`、`duplicate_capabilities=0`、`missing_native_origins=0`、`standard_bundle_issues=0`，`risky_hits=15` 与上轮持平且无一命中新入库技能，`missing_env` 由 116 升至 149（新技能带 env 依赖，预期）。三个测试文件全部通过。
- 入库质检：21 个新目录 SKILL.md 与 SOURCE.txt 齐备，无 `__pycache__`/媒体/大文件（合计 1.6 MB），15 个附带脚本 `py_compile` 与 `node --check` 全通过，注册表分层单调性成立，21 条 origin 已登记。
- `memu` 许可证核验：GitHub licensee 报 NOASSERTION，实际 `LICENSE.txt` 是逐字 Apache-2.0 正文（仅因缩进与附加版权段识别失败），已在 `skills/default/memu/SOURCE.txt` 记录核验结论与日期。
- **月度上游检查卡死并修复**：补跑 `check_upstream_updates.py` 时 2 小时只处理 60/436 个技能，且 GitHub core 配额整点重置后仍为 5000 —— 说明一次成功调用都没发出。根因是 2026-09-12 那类 TLS 指纹切断当晚复发：Python urllib 访问 `api.github.com` 在 0.5–1.7 秒内抛 `SSL: UNEXPECTED_EOF_WHILE_READING`，同一时刻 curl 访问同端点 200/0.5 秒。该脚本当时没有回退，`api_get` 三次重试全部失败后抛错，每个技能被记为 error。已把 `weekly_curation.py` 的加固版回退（`_curl_fetch` / `_api_get_curl` / `_curl_config_escape`，token 走 `curl --config -` stdin）移植进 `check_upstream_updates.py`，并给只在 `--apply` 路径使用的 `raw_file_bytes` 补上同样的回退；`tests/test_curl_token_hygiene.py` 改为对两个脚本同时断言。修复后吞吐从约 30 技能/小时升到约 39 技能/分钟，436 个来源约 11 分钟跑完。实测：repo 元数据 1.2 秒、1122 条 tree 2.1 秒、404 仍返回 None。

- **git 自身的 HTTPS 传输也被切断，publish 步骤当场失败并已加固**：提交 `d5462b8` 后 `git push origin main` 报 `LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to github.com:443`，`git ls-remote` 与 `-c http.version=HTTP/1.1` 同样失败；同一时刻 `curl https://github.com/` 返回 200/1.8 秒、`curl` 访问 `info/refs?service=git-receive-pack` 返回 401/0.64 秒（未带凭证的预期响应），本地代理 127.0.0.1:7890 对 GitHub 仍不通。即被切的是 git 的 TLS 握手，不是主机可达性。`publish_weekly.sh` 因 `set -e` 在 push 处退出，Gitee 已推成功而 GitHub 落后一个提交，两远端一度分叉。已用 SSH 显式 URL 补推（`git push git@github.com:leecyno1/boutique-skills.git main`，不改 remote 配置），并用 `git fetch <ssh-url> main:refs/remotes/origin/main` 修正陈旧的跟踪引用，三方 SHA 重新一致。
- **`publish_weekly.sh` 增加 SSH 回退**：新增 `ssh_url_for`（仅把 `https://github.com/*` 改写为 `git@github.com:*`，Gitee 与已是 SSH 的 URL 返回空）、`push_remote`（HTTPS 失败→SSH 重推→回写跟踪引用）、`resolve_remote_head`（校验改用 `git ls-remote`，HTTPS 取不到再走 SSH，不再依赖 `git fetch` + `git rev-parse origin/main`，避免跟踪引用陈旧误判分叉）。验证：`bash -n` 通过；URL 改写三例正确；两个远端的 `resolve_remote_head` 实测均返回 `d5462b8`。含义：周度 Quest 在同类网络条件下不会再卡在发布步骤。

待观察：

- GitHub 传输层切断的层次在扩大：当晚 20:45 Python urllib 正常，23:30 Python 被切而 curl 与 git 正常，23:55 起 git 的 HTTPS 握手也被切、curl 仍正常，SSH 全程可用。三者是独立通道，判断连通性必须分别测，不能由 curl 通推断 git 通。
- 两份 curl 回退代码目前重复存在于 `weekly_curation.py` 与 `check_upstream_updates.py`。token 处理属安全敏感逻辑，重复副本容易只加固一处（本次正是如此）。后续可抽 `scripts/github_transport.py` 共用，但需同时改测试的按路径加载方式（`sys.path` 不含 `scripts/`），不在本轮动。
- Python OpenSSL 指纹切断是间歇性的：当晚 20:45 与 21:07 两次实测 Python 直连正常（发现/出库阶段全程走 urllib），23:30 后转为全断。因此不能以单次连通性测试判断本轮流水线是否会走回退路径。

未决：

- 周度治理 Quest（id `70f2e60c-b189-445f-ab92-6e4e642f9975`，`0 9 * * 6` Asia/Shanghai）当前 `enabled=false`、`pauseReason=manual`，因此 2026-09-19 与 2026-09-26 两次未触发，本轮为手动补漏。是否重新启用待用户裁决，不代为开启。
- **归档式卸载对 Qoder 客户端重装不具持久性**：`~/.qoder/skills-archive` 已不存在，`~/.qoder/skills` 中 260/311 个目录 mtime 为 2026-09-16，说明当天发生过一次批量恢复/重装，2026-08-22 归档卸载的 31 个 Qoder 技能被还原且归档副本丢失 —— `reports/usage/cleanup-receipts.jsonl` 中对应 `to` 路径已失效，无法 `mv` 回滚，只能重新从上游获取。Codex 侧未受影响（`~/.codex/skills-archive` 22 项完好，2026-09-12 归档的 `grill-with-docs`、`mcp-server-patterns`、`recursive-decision-ledger` 仍未复活）。后果已经显现：本轮 7 项卸载建议里 `doc` 与 `wechat-topic-outline-planner` 是 08-22 已卸载过的技能，属被还原后重新命中。处理原则：卸载建议应当轮确认执行，不跨周悬挂。
- `/Volumes/PSSD/Projects/boutique-skills` 是同一 GitHub 仓库（origin 同为 `leecyno1/boutique-skills`）的陈旧本地检出，停在 `e16c7a0`（2026-08-16），未 fetch 过本轮提交。其工作区含 4 个受保护 tushare-eval 文件的未提交改动，生成时间 `2026-06-18T15:20:38`，比本仓库已提交版本的 `2026-06-14T07:38:30` 新，从未入库。本轮不触碰该目录；保留/同步/归档待用户裁决。
- 月度上游检查已补跑（436 个来源，约 11 分钟），漂移待修复：`current` 187、`would_update` 114（275 改 / 291 新增文件，`tradermonty/claude-trading-skills` 占 50 个技能、`leecyno1/dasheng-media-workflow-skills` 18 个、`himself65/finance-skills` 13 个）、`source_path_missing` 40、`metadata_only_root_no_skill_md` 58、`wrapper_origin` 35、`error` 1。已核实两处不是误报：`AlphaGBM/skills` 把 `skills/<name>` 重组为 `skills/<category>/<name>`（上游现存 27 个 SKILL.md，`alphagbm-alert` 等已删），本仓库 30 个 `alphagbm-*` origin 全失效；`anthropics/financial-services` 删除整个 `plugins/vertical-plugins/wealth-management`，6 个 `anthropic-fs-wealth-management-*` 里只有 `client-review` 迁到 `plugins/agent-plugins/meeting-prep-agent/skills/client-review`，其余 5 个上游已无对应。
- **治理盲区：prune 检测不到路径级删除**。`weekly_curation.py` 的出库第 1 条只请求 `/repos/{owner}/{repo}`，仓库存活即视为上游健康，因此上述 5 个孤儿技能与 3 个已被上游删除的 `alphagbm-*` 永远不会被自动出库。只有月度 `check_upstream_updates.py` 能发现，而它的结论目前没有任何流程消费（不进 prune、不进出库建议）。修法建议：让 prune 复用月度检查的 `source_path_missing` 结果，或把 origin 路径存在性纳入出库规则。
- 本轮 7 项卸载建议待用户确认（`reports/usage/pending-cleanup.json`，status=pending，绝不自动执行）。

## 2026-09-12（周度治理·网络故障与修复批次）

已解决：

- 周度流水线第 1 步连续两次失败（`RemoteDisconnected` / `SSLEOFError`），重试无效。根因：网络中间设备切断 Python OpenSSL 的 TLS 指纹（api.github.com 与 raw.githubusercontent.com 均中招）；curl（LibreSSL）与 gh（Go）指纹放行；本地代理 127.0.0.1:7890 对 GitHub 出口反而失效（分流节点问题）。已修复：`scripts/weekly_curation.py` 新增 curl 子进程回退（`_curl_fetch` / `_api_get_curl`，`raw_file_bytes` 同步回退），urllib 遇 SSL 切断/连接重置时自动降级，向后兼容，CI 等正常环境零影响。修复后全流程跑通。
- curl 回退首版漏了 `-L`：prune 检查上游时 `leecyno1/dasheng-media-workflow-skills` 返回 301（上游已改名）被误判为失败。已加 `-L` 跟随重定向，与 urllib 自动重定向行为对齐。
- 上游改名事实：`leecyno1/dasheng-media-workflow-skills` → `leecyno1/newma-media-studio`（301 重定向，上游存活，prune 未误判 404）。SOURCE.txt 与 origin 覆盖仍指旧名，GitHub 会重定向，暂不需改动；若后续 404 再更新。
- 已知残留：curl 子进程命令行携带 token（`ps aux` 可见），本机单用户环境风险可控；后续可改用 `--config -` 从 stdin 传 header 消除。

待观察：

- Python OpenSSL TLS 指纹切断是否为长期网络策略：若恢复，curl 回退自动闲置无害；若持续，后续脚本（如 `check_upstream_updates.py`）如遇同类失败可复用 `_curl_fetch` 模式。

## 2026-09-11（记忆恢复批次）

已解决（commit `2cdfd9f`，已推送 origin 与 gitee）：

- 远端 README 三张图裂：`assets/hero-v2.png`、`assets/weekly-pipeline.png`、`assets/bundles-duo.png` 被 README 引用但从未提交，GitHub/Gitee 上 404。根因是 `026c424`（2026-08-19）提交时 `scripts/publish_weekly.sh` 的白名单不含 `assets/`。三张图已入库，被取代的 `assets/hero.png` 已删除。
- 白名单已补 `assets/` 与 `.gitignore`（2026-09-08 修改，2026-09-11 随本次提交入库）。
- 记忆文件陈旧：本文件曾记录 318 个技能目录，`QODER_HANDOFF.md` 曾记录 403 个技能；实际为 `skills/default/` 560 个目录、注册表 424 个技能。两者已校正。
- 会话上下文丢失后，新会话未必挂载 `SearchMemory`/`UpdateMemory` 与 `schedule` MCP，记忆必须落在仓库文件里才可恢复（恢复顺序见 `QODER_HANDOFF.md`）。
- GitHub 仓库已改名为 `leecyno1/boutique-skills`：推送时远端返回 "This repository moved"。旧 URL 仍重定向，`git ls-remote` 新旧地址同指同一提交，推送不受影响。仓库大部分位置（`scripts/generate_assets.py`、`scripts/import_installer_default_skills.py`、`docs/generated/*`、`docs/tiers/*`、`docs/SKILL_MANUALS.md`）早已用新名，只有三处遗留已修正：`scripts/generate_finance_suite.py` 的硬编码 source/native_origin、`catalog/suites/finance-investment-standard.json`、`README.md` 套件表对应行。`origin` 远端地址已指向新名；Gitee 未改名，`GITEE_URL` 保持原值。本地目录名仍为 boutique-openclaw-skills，属目录名不是仓库名，不改。
- `scripts/publish_weekly.sh` 白名单原本不含 `findings.md` 与 `task_plan.md`，这两个记忆文件的改动永远不会被周度流程提交；已补入白名单。

未决：

- 周度治理 Quest 在 2026-08-29、2026-09-05 两次未触发，`reports/weekly-curation/` 与 `reports/usage/` 最新日期停在 2026-08-22。下次预期触发 2026-09-12（周六）09:00 Asia/Shanghai。
- `reports/usage/pending-cleanup.json` 的 `items` 为空，无待确认卸载项。

## 2026-08-09（已解决）

- `skills/default` 当时含 318 个技能目录。
- `catalog/default-skills.json` 当时有 320 条分层条目，但仅 179 个唯一技能 ID，因为 low/medium/high 是累积分层。
- 当时所有默认目录条目的 `source` 都指向 `leecyno1/auto-install-Openclaw`，是镜像/拷贝路径而非原生上游。
- `README.md` 声称包含原始仓库链接，但当时的默认目录并未提供。
- 当时工作流按周运行，需求是月度评审。

以上五项已在 enriched catalog 升级中解决：原生来源覆盖后 `needs_origin_review = 0`（418 个已核验或引用，6 个预设能力豁免），分层与索引由 `scripts/generate_enriched_catalog.py` 生成，周度治理保留并另加月度深度评审建议。
