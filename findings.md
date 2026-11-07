# Findings

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
