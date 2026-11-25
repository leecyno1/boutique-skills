# Boutique Skills 交接给 Qoder

更新时间：2026-11-25

接手先读 [AGENTS.md](AGENTS.md)（Agent 入口与硬规则）。换新机器读 [docs/MIGRATION.md](docs/MIGRATION.md)。

## 仓库信息

- 路径：/Volumes/PSSD/Projects/boutique-skills（2026-10-31 由 boutique-openclaw-skills 改名，与仓库名一致）
- 默认分支：main
- GitHub：https://github.com/leecyno1/boutique-skills（远端 origin；2026-09-11 由 boutique-openclaw-skills 改名，origin URL 已同步更新）
- Gitee：https://gitee.com/leecyno1/boutique-openclaw-skills（远端 gitee；未改名）
- 注意：字符串 `boutique-openclaw-skills` 现在只应出现在 Gitee 仓库地址与历史记录里（旧会话转录目录、RepoWiki 目录、早期报告中的绝对路径）。仓库名、本地目录名、GitHub 地址都已统一为 `boutique-skills`。
- 当前技能数：332（catalog/skills.enriched.json，生成于 2026-11-21；11-02 退役 132 个、11-07 周度发现补回 15 个到 319，11-11 设计去重出库 2 个到 317，11-14 发现入库 11 个到 327，11-21 发现入库 5 个到 332）；skills/default/ 目录 469 个（含未注册候选与套件成员）
- 横向分层：high 332 / medium 67 / low 52（累积分层，非互斥）；纵向 L1 12 / L2 127 / L3 193
- 星级分布：5★ 101 / 4★ 159 / 3★ 66 / 1★ 6
- 来源核验：326 已核验或引用，6 个预设能力豁免，needs_origin_review = 0
- 标准包：21 个 Skill（上限 40，零第三方 key；packs 为参考推荐不随包安装）。frontend 槽位 = `design-taste-frontend`（96，taste 为标准默认设计库）
- 金融投资标准组合：28 个 Skill（能力位去重，上限 40；同位优先无 key 候选）
- 退役登记：`catalog/retired-skills.json`（138 个 id + 9 个整库屏蔽 + 10 个共用不屏蔽），发现/导入阶段自动跳过；过时退役分析见 `reports/usage/obsolescence-analysis-2026-11-02.md`，设计流派裁定见同文件 `design_school_decision`。整库屏蔽只适用于“该库已无在库技能”的情况，`tests/test_retired_guard.py` 会断言屏蔽库不覆盖任何在库 origin
- 组合 API Key 政策：大模型 key 与 GitHub 工具 token 豁免；第三方注册 key 在标准组合硬过滤、在金融组合同位软惩罚（详见 docs/WEEKLY_CURATION.md）

本仓库收录经过搜索、去重、来源审计和评分的 Agent Skills。维护重点是来源可追溯、能力不重复、依赖透明、评分可复核、安装可用。

## 移交新机器（2026-11-25）

本仓库要整体搬到新 Mac 继续开发。迁移包已备好：`/Volumes/PSSD/123/boutique-skills-新机迁移/`，仓库副本在其下 `boutique-skills/`，含完整 `.git` 与双远端配置，工作区干净。**原目录 `/Volumes/PSSD/Projects/boutique-skills` 保留不动**，两边都是完整可用的仓库。

落地步骤、离线验收命令、硬编码路径清单、定时任务重建参数与禁止事项全部写在 [docs/MIGRATION.md](docs/MIGRATION.md)。三条最要紧的：

1. **同一时间只允许一台机器启用周度任务**，两台同时跑会重复发现、重复发布并互相覆盖。切换顺序：先停旧机 → 新机离线验收 → 再建新机任务。
2. 副本带着可用的远端配置，`git push` 是真会生效的。验收前不要自动推送或发布。
3. 未随盘的是机器状态与无关项目：本机技能安装目录与归档、钥匙串与 gh/git 凭据、`.qoder/repowiki` 缓存、遥测扫描缓存，以及 `boutique-skills.stale-*` 两个旧克隆、`OpenClawInstaller`、`公众号文章` 等同级项目。

## 当前待办（2026-11-25 更新）

工作区在本轮周度治理后干净，`main` 与 origin、gitee 三方同步（具体提交号以 `git log --oneline -1` 为准，不要在记忆文件里钉哈希）。持久结论：`publish_weekly.sh` 白名单已含 `assets/`、`.gitignore`、`findings.md`、`task_plan.md`，`.gitignore` 排除遥测缓存与 `.qoder/`；发布脚本内置 HTTPS→SSH 回退；周度流程共 11 步，第 2 步为上游同步（含 origin 路径迁移），第 3 步为出库（消费同步报告），第 9 步为审计 + 语法门禁 + 风险门禁 + 单元测试。

未决（按处理紧迫度）：

1. **97 项卸载建议待用户确认，应当轮处理**：`reports/usage/pending-cleanup.json` status=pending，96 个唯一技能（96 qoder + 1 codex）。跳升根因已取证：Qoder 活目录 132（11-07）→267（11-21），新增 135 个副本都不是仓库注册技能且零调用，mtime 仍是旧日期、与本地归档只 1 个重合，属客户端侧还原/重装。执行方式 `python3 scripts/uninstall_skills.py --confirm`（周度自动化不得带 `--include-active`）。**不要跨周悬挂**，理由见待办 2。
2. **归档式卸载对客户端重装不具持久性（2026-11-21 复核）**：`~/.qoder/skills-archive` 现有 183 个目录、`~/.codex/skills-archive` 186 个（11-12 记录 qoder 归档目录不存在，现已重新出现）。11-02 归档的技能被客户端还原过至少两次（2026-09-16 批量、11-07 之后再一次）。含义：卸载确认应当轮执行并复核活目录数，跨周悬挂会被还原抹掉。
3. **上游描述漂移会静默改分类（2026-11-21 新增，门禁盲区）**：`book-to-skill` 因上游新增 "remote MCP book search" 一句描述，被 search 关键词从 coding-devtools 挤成 search-research，已加覆盖归位。`tests/test_category_classifier.py` 只断言"目录与分类器实时一致"，**不断言"同步前后分类稳定"**，所以上游改一句描述就能静默改掉分类与评分而门禁全绿。周更后应 diff 同步前后的 `primary_category`，逐个核对变化项。
4. **新入库技能必须逐个核对分类（2026-11-21 实证）**：本轮 5 个新技能（Jeffallan/claude-skills）全部静默错分，且没有一个落进兜底桶，门禁不会拦。触发词分别是 writing / planning / trade（trade-offs 连字符复合词，词边界救不了）/ search / design+s。**入库后先跑分类探针，别等门禁。** 该库 5 个岗位不同，不是单一分类家族。
5. **84 个来源无法内容同步**：`metadata_only_root_no_skill_md` 84 + `metadata_only_root_too_large` 1，origin 指向仓库根目录且无 SKILL.md，只能核验存在性。要逐个补 origin 路径才能真正纳入周更。
6. **导入函数静默 0 落盘**：`collect_skill_files` 抓取为空或超限时静默 `continue`，`alchaincyf/nuwa-skill` 连续两轮（11-14、11-21）因此 0 落盘却无日志。补一条 warn 即可。
7. **治理链路已恢复，自动运行仍需盯**：Quest `436c5b6e-10c6-487b-b73a-1504e4cc89c0`，directory 域绑定本仓库，周六 09:00 Asia/Shanghai，Full Access，独立会话，`enabled=true`（2026-11-11 经 `qoder_cron list` 核对；**2026-11-21 会话未挂载 schedule MCP，无法复核，本轮由用户指令触发执行**）。2026-11-07 那次 `lastRunStatus=canceled`（发现阶段被 17MB 大响应截断，已修 `IncompleteRead` 回退）；2026-11-14 那次跑到第 9 步被兜底桶门禁拦下、本地修复后第 10-11 步未执行，改动悬挂到 11-21 才随本轮发布。旧的 chatOnly 任务（`70f2e60c`）与上一版 workspace 域任务（`d86c21e2`）已删除。**下次自动运行重点核对：第 9 步门禁是否拦下新技能分类、第 10-11 步是否真的跑完（看远端 SHA 是否前进）、上游同步 20–25 分钟是否跑完、发布是否走了 SSH 回退。**
8. **路径级失效已纳入周更治理（2026-10-31）**：`check_upstream_updates.py` 在 `source_path_missing` 时会自动迁移 origin——先按 SKILL.md 内容哈希，再按唯一同名目录，最后在版本/稳定分支（如 `taste-skill-v1.9`）里找原路径；迁移写回 `catalog/native-origin-overrides.json` 与 `SOURCE.txt`，并从新路径同步。`weekly_curation.py prune --upstream-report` 消费同一份报告，只对迁移失败、确认已删除的孤儿出库，并用 origin 是否已变动防止旧报告误删。10-31 那轮 52 个失效路径：30 个迁移成功、22 个确认删除并出库。**11-14 与 11-21 两轮迁移数均为 0，上游无重组。**
9. **过时退役已执行（2026-11-02）**：按“模型/harness 是否已覆盖”标准，本机归档 193 个技能（300 份副本），仓库出库 132 个（436→304），全部登记进 `catalog/retired-skills.json` 防再导入。其中 codex 侧 ecc 一族（tdd-workflow、e2e-testing、security-review 等 24 个）近 30 天引用量高，属归档观察：若 Codex 输出质量下降，`mv ~/.codex/skills-archive/<name> ~/.codex/skills/` 即可恢复。
10. **人工复核队列**：`alibaba/open-code-review`（54786 星，Apache-2.0）被 monorepo 门槛（`skill_subdirs=2 < 3`）挡下而非聚合商店规则，评估与入库条件见 `reports/source-discovery/open-code-review-review-2026-09-30.md`；同批 `pascalorg/editor` 建议维持不收。`Jeffallan/claude-skills` 有上百个工程专家技能，本轮只入库 5 个，是否继续收录需人工裁定。`computer-use`（qoder 历史 73 次调用、未收录）是本轮 discover 建议，收录前先确认 canonical 上游（可能由 Qoder 插件提供）。
11. **`~/.qoder/skills` 缺 agent-reach 副本**：`~/.claude/skills` 与 `~/.agents/skills` 有，CLI 在 `~/.local/bin/agent-reach`。仓库与标准包 `social-research` 槽位均已收录，周更会自动同步上游。
12. **设计流派已收敛完毕（2026-11-11 第二轮）**：taste-skill 是标准默认设计库，标准包 frontend 槽位已换成 `design-taste-frontend`(96)。其余设计技能按“优于 taste 或互补则留，否则按重复出库”筛完：出库 animation、impeccable、frontend-design、web-animation-design 4 个；保留 review-animations 98、pick-ui-library 92、scroll-world 93、generative-ui 92、huashu-design 81、gsap ×8 与 taste 家族 13 个（互补岗位，不重复）。裁定与保留理由记在 `catalog/retired-skills.json` 的 `design_school_decision`。**后续发现新的设计流派，先按这条规则判断，不要默认收录。**
13. **分类器兜底桶已清空（2026-11-11 第三轮）**：`commerce-ops` 是“关键词全不命中”的兜底桶，原有 16 个技能静默错分，现已逐个核对 SKILL.md 归位。`tests/test_category_classifier.py`（已接入周度第 9 步）断言兜底桶只能由显式覆盖产生、目录分类与分类器实时一致。**新技能落进兜底桶时，读它的 SKILL.md 后写进 `CATEGORY_OVERRIDES`，不要留着错分；加短关键词前先判断会不会嵌在别的英文单词里。**
14. **宽匹配已逐个核对完毕（2026-11-12 第四轮）**：`BOUNDARY_KEYWORDS` 现为 9 个 `ui/ios/media/vision/dev/market/compress/design/valuation`，每个都有具名实证误命中；`BOUNDARY_INFLECTION = (?:s|es|ed|ous)?` 保住 stocks/images/tasks/dangerous 这类合法屈折，**故意不放过 -ing 与 -er**。`search` 实测无危害不收。覆盖表 80→94 条（11-14 +2、11-21 +6，现 102 条），新增三个家族：tradermonty 交易 edge 流水线→finance-trading、Claude-BugHunter 漏洞赏金→security-audit、ECC Agent 工程→agent-orchestration。**改关键词表前先跑影响面模拟，改完必须重生成目录并跑 7 个分类器用例；同库同岗的家族核对完就加进 `test_reviewed_families_stay_in_one_category`。** 归位会联动掉星，那是评分模型既有设计，不是 bug。
15. **EGM 家族分类语义未裁定（11-14 遗留）**：egm-brainstorm/draft/drift-report/resolve/bootstrap 现全在 design-ui，但内容是软件设计文档/README 契约工作流，语义上更接近 docs-office 或 agent-orchestration。

## 最近完成（2026-11-25 整理项目 + 备好新机迁移包）

- 新建仓库根 `AGENTS.md`：Agent 入口、权威文档顺序、7 条硬规则（目录只能脚本生成、兜底桶必须为空、设计只认 taste 默认、出库走归档、4 个保护文件、发布只用 publish_weekly.sh、密钥只读键名）、验收命令、工具链。已加进 `publish_weekly.sh` 白名单。
- 新建 `docs/MIGRATION.md`：随盘/未随盘清单、新机 6 步落地、离线验收、硬编码与陈旧引用清单、周度任务重建参数、禁止事项。
- 迁移包 `/Volumes/PSSD/123/boutique-skills-新机迁移/`：完整仓库副本（含 `.git`、双远端配置）+ 根 AGENTS.md/README.md + `config/boutique-skills-cron.json`（周度任务定义，新机照抄只改 cwd）+ 文件清单。排除 `__pycache__`、`.DS_Store`、`.qoder/`、遥测扫描缓存，以及两个 stale 旧克隆、OpenClawInstaller、公众号文章等无关项目。原目录保留。
- 顺手查出一个门禁盲区：`scripts/build_skills_directory.py` 需要 PyYAML，**旧机没装，该脚本一直跑不起来**；它不在周度流程里所以门禁全绿也掩盖了。已写进 AGENTS.md 与 MIGRATION.md，新机补装。
- 基线核对：HEAD `50bff92`，工作区干净，HEAD=origin=gitee；332 技能 / 469 目录，L1 12 / L2 127 / L3 193，安装档 52/67/332，标准包 21、金融组合 28。audit/syntax/risk 全 0，6 个测试文件全过。

## 最近完成（2026-11-21 周度治理 11 步跑通）

- 完整执行 `weekly_cycle.sh`，把 11-14 悬挂的 378 项改动与本轮成果一并发布。发现 29 候选 / 3 import / 5 入库（Jeffallan/claude-skills 首次入库）；出库 0。
- 上游同步 311 个来源、0 error、28 个技能更新、227 个文件变更（133 改 + 94 增）；origin 迁移 0、路径失效 0、404 0。
- 两处分类归位（详见 findings.md 2026-11-21）：5 个新技能静默错分逐个取证后加覆盖；`book-to-skill` 因上游描述漂移被挤成 search-research，已归位。覆盖表 96→102，未动关键词表。
- 门禁全绿：audit 332/326（missing / duplicate / missing_native_origins / standard_bundle_issues 全 0）、syntax 1372 py + 397 js errors 0、risk 15=15 new 0、6 个测试文件 27 用例 OK。标准包 21 位、金融组合 28 位未变。
- 发布 `e4d946a`（750 文件），三方 SHA 一致，HTTPS 直连未回退 SSH，4 个受保护文件未提交。
- 调整建议 remove 97 / consider 184 / keep 88 / discover 1，全部 pending 未执行；remove 跳升根因取证为客户端还原（见待办 1）。

## 最近完成（2026-11-12 逐个核对宽匹配）

- 探针枚举 24 个"关键词只以嵌词形式命中"的技能，逐个读 SKILL.md 判定：合法屈折与站得住的分类不动，14 个错分按家族归位（tradermonty edge 流水线 6 个→finance-trading、Claude-BugHunter 5 个→security-audit、ECC 3 个→agent-orchestration）。
- 词边界集合 4→9（新增 dev/market/compress/design/valuation），屈折白名单 `(?:s|es|ed|ous)?`；`search`/`task`/`mcp` 经实测无危害，不收，避免集合虚胖。
- 分类器测试 6→7 用例：新增 6 条跨词回归、7 条屈折回归，以及 `test_reviewed_families_stay_in_one_category`（断言三个库各自单一分类，成员 41/5/4）。
- 影响面精确 14 个技能，其余 303 个零变化：finance-trading 73→79、security-audit 5→10、agent-orchestration 12→15、design-ui 34→30、coding-devtools 27→24、search-research 29→25；L2 128→115 / L3 177→190；5★ 100→91。安装档 53/68/317、标准包 21 位、金融组合 28 位逐字节未变，兜底桶仍 0。
- 门禁全绿：audit 317/311（missing 0、duplicate 0、bundle issues 0）、syntax 1266 py + 394 js errors 0、risk 15=15 new 0、6 个测试文件 27 用例 OK。

## 最近完成（2026-11-11 分类器完善）

- 兜底桶 `commerce-ops` 从 16 个技能清到 0：逐个读 SKILL.md，按同家族惯例归类（课程家族→coding-devtools、OmniRoute CLI→coding-devtools、ponytail→coding-devtools、story 网文→writing-content、SEO→marketing-growth、论文套件→search-research、套件路由→agent-orchestration）。
- 跨词误命中：`BOUNDARY_KEYWORDS` 扩到 `ui/ios/media/vision`，reflection、baoyu-image-gen 自动归位；另修正 cli-a2a/cli-backup-sync/cli-compression、cavecrew/caveman-commit/caveman-compress、seo-agentic/seo-cluster、agentmail、build-project、analytical-method-validation 共 11 个核对过的误判。
- `classify_category` 的局部 `explicit` 字典提升为模块级 `CATEGORY_OVERRIDES`（52→80 条，按家族分组写理由）。
- 新增 `tests/test_category_classifier.py`（6 用例：兜底桶必须显式覆盖、目录与分类器一致、覆盖表分类名合法、跨词回归、真实术语仍命中、块标量头解析），接入 `weekly_cycle.sh` 第 9 步，周度测试 5→6 个。
- 影响面：30 个技能分类变化，5★ 89→100、L2 118→128 / L3 187→177；安装档 53/68/317 未变，标准包 21 位（frontend 仍 design-taste-frontend）、金融组合 28 位未变。门禁全绿（audit 0/0/0、syntax 0 errors、risk 15=15 new 0、6 测试 OK）。

## 最近完成（2026-11-11 设计去重 + taste 设为标准默认）

- 重定位：`frontend-design` 来源已定位 = `anthropics/skills@00756142`（2025-12-04，SKILL.md 逐字 94.67% 相同）；`web-animation-design` canonical 上游查不到（只有聚合/镜像，无 license 无署名），内容与在库 `review-animations`(98) 同源重复。
- 出库 4 个：animation（bytesagain，shell 包 CSS keyframes，模型原生已覆盖）、impeccable（pbakaus，竞争流派，taste 96 > 92）、frontend-design、web-animation-design。仓库 319 → 317，目录 458 → 454。
- 本机归档 4 份副本（frontend-design、web-animation-design 各 Qoder + Codex）。两者近期都有调用，dry-run 全被安全网拒绝，按人工裁定用 `--include-active --confirm`。**frontend-design 是高频技能（833 次 / 近 30 天 363 次），归档会改变日常行为**，同岗位由 design-taste-frontend 承担；回退 `mv ~/.{qoder,codex}/skills-archive/<name> ~/.{qoder,codex}/skills/`。
- taste 成为默认：`CAPABILITY_RULES` 的 frontend 候选加 `design-taste-frontend`，标准包 frontend 槽位由 generative-ui(92) 换成 design-taste-frontend(96)。generative-ui 留在库里做对话内联 widget。
- 修两个生成器 bug：`parse_frontmatter` 不认 `>-` 块标量头（4 个技能 description 变成字面 ">-"）；分类器 `ui` 裸子串匹配把 "quick" 判成 design-ui（加词边界后 11 个技能回到正确分类，design-ui 45→34）。
- 门禁全绿：audit 317/311、missing_skills 0、standard_bundle_issues 0；syntax errors 0；risk 15/15 new 0；5 个测试 OK。

## 最近完成（2026-11-11 设计流派只留 taste 一家）

- 用户给的小红书帖子指向 `elayadesign/ai-design-skills`（15242 星，MIT）。核查后不入库：与在库 taste-skill 规则互斥（elaya 禁渐变+封闭 token 集，taste 允许 shader/WebGL），同库 `figma-designer` 依赖 Figma MCP 而本机 0 个 Figma 工具，且仓库评分器给 70 分进 review、`skill_subdirs=2 < 3` 自动入库分被抬到 101。
- 本机：`landing-page-design` 两份旧副本归档（`uninstall_skills.py --include-active --confirm`，回执 archived=2）；`redesign-existing-projects` 原为 elaya 版（`6558d92fdeb2`），备份到 `~/.{qoder,codex}/skills-archive/redesign-existing-projects-elaya-20261111/` 后替换为仓库 taste 版（`0713bbfa0337`）。两个运行时现存 8 个设计技能一致。
- 仓库：`catalog/retired-skills.json` 加 `design-school` 分组 2 个 id + 2 个整库屏蔽（`elayadesign/ai-design-skills`、`elayadesign/redesign-skill`）+ `design_school_decision` 裁定记录。在库 `redesign-existing-projects` 的 origin 是 `Leonxlnx/taste-skill`，不受屏蔽影响。
- 文档校正：`docs/WEEKLY_CURATION.md` 的组合数（30/34 → 21/28）、金融组合带 key 位数（13/34 → 10/28）、标准包跳过位（去掉已不跳过的 finance-data），并补写 `--include-active` 只用于人工裁定、周度自动化不得带。

## 最近完成（2026-10-31 修复周度治理 + 首次自动上游同步 + 路径级治理）

- 周度流程扩为 11 步：第 2 步上游同步、第 3 步出库（消费同步报告）、第 9 步审计 + 两道发布门禁（`scripts/check_skill_syntax.py`、`scripts/check_new_risks.py` + `catalog/risky-baseline.json`）。
- 首次同步：436 个来源 → 118 个技能更新（468 改 + 227 新增文件），`current` 171、`source_path_missing` 52、`metadata_only_root_no_skill_md` 59、`wrapper_origin` 35。门禁拦下 `huashu-design` 的 `eval` 用法，复核后带理由放行。
- 路径级治理首次运行：30 个 origin 自动迁移（AlphaGBM 15、taste-skill 12、anthropics 3），22 个确认删除的孤儿出库；剩余 `source_path_missing` 清零。新增 `tests/test_upstream_relocation.py`。
- 本地目录改名为 `boutique-skills`，同名陈旧检出归档为 `boutique-skills.stale-2026-08-16`。桌面旧克隆 `~/Desktop/Projects/boutique-skills` 的依赖清单（wechat-multi-publisher）已并入主仓库后，整体归档为 `/Volumes/PSSD/Projects/boutique-skills.stale-desktop-2026-10-31`。
- `~/.qoder/skills/agent-reach` 软链到本仓库 `skills/default/agent-reach`，Qoder 侧可直接调用并随周更同步。


## 最近完成（2026-09-30 补漏周度治理）

发现阶段评估 41 个候选仓库，自动入库 5 个仓库共 21 个 Skill；出库检查 415 个上游，0 项移除。

| 上游仓库 | 星数 | 评分 | 入库 Skill |
|---|---:|---:|---|
| agricidaniel/claude-seo | 18000 | 80 | seo-agentic、seo-audit、seo-backlinks、seo-cluster、seo-competitor-pages |
| wanshuiyin/auto-claude-code-research-in-sleep | 16852 | 80 | ablation-planner、alphaxiv、analyze-results、arxiv、auto-paper-improvement-loop、browser-cdp |
| zenstory-ai/oh-story-claudecode | 7186 | 80 | story-cover、story-deslop、story-import、story-long-analyze |
| elementalsouls/claude-bughunter | 4731 | 80 | apk-redteam-pipeline、bb-local-toolkit、bb-methodology、bug-bounty、bugcrowd-reporting |
| nevamind-ai/memu | 14495 | 75 | memu（NOASSERTION 已核验为逐字 Apache-2.0，见其 SOURCE.txt） |

本轮另修复 `scripts/weekly_curation.py` 的 curl 回退把 token 暴露在 `ps aux` 的问题（改为 `curl --config -` 走 stdin），新增 `tests/test_curl_token_hygiene.py` 并接入 `weekly_cycle.sh` 第 8 步。

上一轮（2026-08-16）入库：

| Skill | 评分 | 定位 |
|---|---:|---|
| dasheng-vox-skills | 90/100，5 星 | VOX 视频统一编排、Manifest、Provider 路由、Shotcraft、Gemini、Remotion、QC |
| dasheng-video-omni-browser | 82/100，4 星 | 使用已登录 Chrome Gemini Omni 逐镜生成约 10 秒视频 |

## 关键目录

- AGENTS.md：Agent 接手入口与硬规则（任何机器都先读这份）。
- docs/MIGRATION.md：换新机器的落地、验收与复核清单。
- skills/default/<name>/：Skill 主文件、配置、Agent 展示信息和来源说明。
- catalog/default-skills.json：基础注册表。
- catalog/native-origin-overrides.json：来源核验覆盖。
- catalog/suites/：组合套件（含金融投资标准组合）。
- scripts/generate_enriched_catalog.py：生成评分、依赖和文档索引。
- scripts/generate_finance_suite.py：生成金融组合（能力位去重，<= 40）。
- scripts/weekly_curation.py：周度发现/评分/入库/出库。
- scripts/telemetry_collect.py：本地使用频率遥测（扫描 Qoder/Claude Code/Codex/Kimi Code 会话日志，输出 reports/usage/ 周报与 usage-scores.json，评分联动 +0~8 分；仅本地聚合不读取消息内容）。
- scripts/usage_recommendations.py：skills 调整建议（keep/remove/consider/discover 四级，remove 写入 pending-cleanup.json 待确认）。
- scripts/uninstall_skills.py：确认后的归档式卸载（默认 dry-run，--confirm 执行，移入 *-archive/ 可恢复，活跃技能强制拒绝）。
- scripts/weekly_cycle.sh：周度全流程编排（11 步：发现→上游同步（含路径迁移）→出库→遥测→目录→组合→README→报告→审计测试→建议→发布）。
- tests/test_upstream_relocation.py：origin 迁移的单元测试（内容哈希优先、同名目录唯一才用、歧义不猜、版本分支原路径）。
- scripts/publish_weekly.sh：白名单提交并推送 GitHub+Gitee。
- scripts/audit_skills.py：全库审计。
- scripts/install-suite.sh：套件安装和 dry-run。
- reports/source-discovery/：评审报告。
- reports/weekly-curation/：周度发现/出库报告。

## 新 Skill 更新流程

1. 先在本地搜索同名和同能力 Skill，避免重复。
2. 再检查来源仓库、SKILL.md、脚本、依赖、许可证和最近提交。
3. 评估功能覆盖、可执行性、质量控制、移植性、安全、来源和维护价值。
4. 评分建议：90 分以上 5 星；75–89 分 4 星；60–74 分 3 星；低于 60 分不入库。
5. 每个候选添加 reports/source-discovery/<name>-review-YYYY-MM-DD.md。
6. 将文件放入 skills/default/<name>/，删除 __pycache__、临时文件、运行媒体和凭证。
7. 添加 SOURCE.txt，记录来源、许可证、快照提交和移植修正。
8. 更新基础目录、来源覆盖、评分覆盖和相关套件。
9. 重新生成目录：

   python3 scripts/generate_enriched_catalog.py

10. 检查安装预览：

   ./scripts/install-suite.sh <suite-id> --dry-run

## 验证命令

    python3 -m json.tool catalog/default-skills.json >/dev/null
    python3 -m json.tool catalog/native-origin-overrides.json >/dev/null
    python3 -m py_compile skills/default/<name>/scripts/*.py
    python3 scripts/audit_skills.py --report /tmp/boutique-audit.md --json /tmp/boutique-audit.json
    git diff --check

有对应测试时运行对应 pytest。若 pytest 未安装，应明确记录为测试环境缺失，不要误报成代码失败。

## Git 规则

- 禁止使用 git reset --hard、git clean、git checkout -- 覆盖工作区。
- 提交前使用白名单 git add（scripts/publish_weekly.sh 已内置）。
- 当前以下四个文件已有用户改动，不能回滚、覆盖或代提交：

    reports/finance-skill-eval/tushare-eval/standard-finance-skills-recommendation.json
    reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.html
    reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.json
    reports/finance-skill-eval/tushare-eval/tushare-finance-skill-evaluation.md

- 提交前确认 git diff --cached --name-only 不含以上文件。
- 提交后同步两个远端（publish_weekly.sh 自动完成）：

    git push origin main
    git push gitee main
    git fetch origin main --quiet
    git fetch gitee main --quiet
    git rev-parse HEAD origin/main gitee/main

## 周度自动治理（2026-08-19 新增）

每周定时任务（Qoder 会话 schedule，周六 09:00 Asia/Shanghai）执行：

    ./scripts/weekly_cycle.sh

流程：发现（GitHub 搜索+评分+高分入库）→ 出库（上游失效/低分/被支配）→ 重建目录 → 刷新金融组合 → 审计 → 测试 → 双远端发布。

- 入库门槛：候选 >= 75 分且含 SKILL.md 且 >= 20 星且一年内活跃且无能力重叠；60-74 分进人工复核清单。
- 出库规则：上游 404 / 内部评分 < 60 / 同冲突组内被高出 >= 15 分的同类支配且自身 <= 70 分。
- 标准组合 <= 40 base skills（一能力一技能）；金融组合 <= 40（能力位取最高分）。
- 详见 docs/WEEKLY_CURATION.md。

## 定时维护建议（月度深度评审，可与周度自动流程互补）

每周或每两周：

1. 扫描新候选和上游更新。
2. 检查已入库 Skill 的来源仓库是否有新提交。
3. 对最近更新或高使用频率 Skill 重跑评分。
4. 清理重复能力和失效来源。
5. 运行目录生成、安装 dry-run 和全库审计。
6. 只提交本轮变更，并同步 GitHub/Gitee。

记录位置：新增候选和评分报告放在 reports/source-discovery/；问题放在 findings.md；来源和版本变化写入 SOURCE.txt 与提交记录。

## 已知限制

- dasheng-video-omni-browser 依赖用户已有 Chrome 登录态和 Gemini 网页 UI，不是稳定 API。
- dasheng-vox-skills 的完整导演 CLI、Remotion 工程和实际媒体产物仍在 /Volumes/PSSD/Projects/公众号文章；本仓库收录的是可复用编排核心和必要参考文件。
- 全库审计可能报告其他 Skill 的环境变量或风险扫描提示，先确认是否属于本轮改动。
- 真实 Gemini 在线生成、Chrome 下载和平台登录不在静态验证范围内。

## 接手完成标准

Qoder 接手后应能根据来源链接或本地 Skill 目录完成搜索、评分、去重、入库、目录生成、安装 dry-run、全库审计，并在保留用户改动的前提下同步 GitHub 和 Gitee。

## 记忆位置与上下文恢复（2026-09-11 补记）

会话上下文可能整体丢失，且新会话不一定挂载 `SearchMemory`/`UpdateMemory` 或 `schedule` MCP 工具。此时按下列顺序从磁盘恢复，不要凭印象作答：

1. 本文件（仓库根 `QODER_HANDOFF.md`）：流程、规则、待办，是唯一的权威长期记忆。
2. `task_plan.md` / `progress.md`：历史阶段与验证结论（origin/index/scoring 升级已于 2026-08 完成，needs_origin_review = 0）。
3. `findings.md`：问题清单，按日期分批记录。
4. 会话转录：`~/.qoder/projects/-Volumes-PSSD-Projects-boutique-openclaw-skills/transcript/*.jsonl`，可解析出历次用户指令、工具调用与结论。
5. 结构化仓库知识（RepoWiki）：`~/.qoder/knowledges/boutique-openclaw-skills/main__zh-CN/` 与仓库内 `.qoder/repowiki/`（2026-09-09 生成，完好）。
6. 客观事实以 `git log` / `git status` / `catalog/skills.enriched.json` 的 `summary` 为准，记忆文件与它们冲突时以仓库为准并回写记忆。

Quest（定时任务）由 `schedule` MCP 服务管理，不在本仓库内，也不等于本地 cron。该工具未挂载时无法查询或重建 Quest，只能从 `reports/weekly-curation/` 的最新日期推断是否真的触发过，并在本文件登记预期触发时间。
