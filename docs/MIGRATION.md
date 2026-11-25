# 换新机器接手指南

本仓库要整体搬到新 Mac 继续开发。这份文档讲怎么落地、怎么验收、哪些东西必须在新机复核。仓库自身的规则见 [AGENTS.md](../AGENTS.md)，当前状态见 [QODER_HANDOFF.md](../QODER_HANDOFF.md)。

迁移包位置：`/Volumes/PSSD/123/boutique-skills-新机迁移/`，仓库副本在其下 `boutique-skills/`。原目录 `/Volumes/PSSD/Projects/boutique-skills` 保留不动，两边都是完整可用的仓库。

## 随盘与未随盘

随盘：全部已跟踪文件（含 `skills/` 内容与资产、`catalog/`、`scripts/`、`tests/`、`docs/`、`reports/`、`categories/`、`tiers/`、`profiles/`、`optimization/`、`assets/`、`.github/workflows/`），以及完整 `.git`（历史、`origin` 与 `gitee` 双远端配置、本地 git config）。副本是干净工作区，HEAD 与双远端一致。

未随盘：

| 排除项 | 原因 |
|---|---|
| `__pycache__/`、`.DS_Store` | 可再生缓存 |
| `.qoder/repowiki/` | 本机生成的 RepoWiki 知识缓存，已 gitignore，镜像在 `~/.qoder/knowledges/`，新机可重新生成 |
| `reports/usage/.scan-state.json`、`.scan-uses.json` | 遥测扫描增量缓存，新机重扫即可 |
| `Projects/boutique-skills.stale-2026-08-16`（291M） | 旧备份克隆 |
| `Projects/boutique-skills.stale-desktop-2026-10-31`（521M） | 桌面旧克隆，有用依赖已并入主仓库 |
| `Projects/OpenClawInstaller`（1.2G） | 另一个项目，只被一个离线导入脚本引用 |
| `Projects/公众号文章` 等同级业务项目 | 无关项目，仅被 SOURCE.txt 的历史来源记录引用 |
| 本机 `~/.qoder/skills`、`~/.codex/skills` 安装副本与归档 | 属于机器状态，不属于仓库；新机按需重新安装 |
| 钥匙串、gh/git 凭据、环境变量值 | 不随盘传递，新机重新授权 |

## 新机落地步骤

1. **放仓库。** 把 `boutique-skills/` 复制到新机工作区。路径不必与旧机相同——周度脚本全部用 `SCRIPT_DIR/..` 定位仓库根，不依赖绝对路径。唯一例外见下面的硬编码清单。
2. **装工具链。** Python >= 3.12、Node、git、gh CLI。旧机实测 Python 3.14.4 / Node v26.7.0 全门禁通过。周度 11 步与门禁只用标准库；两个离线工具额外需要 `PyYAML`（`build_skills_directory.py`）与 `Pillow`（`generate_assets.py`）。**旧机缺 PyYAML，前者一直跑不起来**，新机顺手补上：`python3 -m pip install PyYAML Pillow`。
3. **配凭据。** `gh auth login`（发现阶段用），git 推送凭据（GitHub + Gitee）。发布脚本内置 HTTPS→SSH 回退，两条路至少通一条。环境变量只认键名：`GITHUB_TOKEN` 或 `GH_TOKEN`（发现/上游同步），`TUSHARE_TOKEN`（仅金融评测报告，周度不需要）。值不写进任何文件或输出。
4. **先离线验收**（下一节），确认副本自身完整，再考虑联网。
5. **重建定时任务。** 见下面"周度自动化"。先停旧机任务，再建新机任务。
6. **按需重装本机技能。** 仓库是源，本机 `~/.qoder/skills` 等安装目录是消费端。用 `make install-standard`（默认 dry-run）或 `scripts/install-tier.sh` 安装，不要从旧机拷安装目录。

## 离线验收

不联网、不推送、不安装，全部要过：

```bash
cd <新机仓库路径>
git status --short                 # 必须为空
git log --oneline -1               # 记下 HEAD
git remote -v                      # origin=github leecyno1/boutique-skills, gitee=leecyno1/boutique-openclaw-skills
python3 scripts/audit_skills.py
python3 scripts/check_skill_syntax.py
python3 scripts/check_new_risks.py
for t in tests/test_*.py; do python3 "$t"; done
```

判定标准：audit 的 `missing_skills`、`duplicate_capabilities`、`missing_native_origins`、`standard_bundle_issues` 全为 0；syntax `errors` 为 0；risk `new` 为 0；6 个测试文件全 OK。任一非零就先查原因，不要改基线或跳过测试。

联网后再核对 `git rev-parse HEAD origin/main gitee/main` 三者一致（需先 `git fetch`）。

## 需要在新机复核的硬编码与陈旧引用

这些不影响周度流程，但用到就会踩：

- `scripts/import_installer_default_skills.py:7` 写死 `DEFAULT_INSTALLER = Path('/Volumes/PSSD/Projects/OpenClawInstaller')`。离线导入工具，不在周度流程与 Makefile 里。新机要用先改成实际路径，该项目未随盘。
- 21 个 `skills/default/dasheng-*/SOURCE.txt` 的来源记录指向 `/Volumes/PSSD/Projects/公众号文章`。这是历史 provenance 文本，不是运行依赖，保留原样即可；`公众号文章` 项目未随盘，由它自己的迁移包维护。
- `progress.md` 是 2026-08-09 的早期进度快照，已跟踪但无脚本引用，内容早被 findings.md 与 task_plan.md 取代。当历史文件看，不要当现状。
- `docs/OPENCLAW_SKILLS_FULL.md`、`docs/SKILL_MANUALS.md` 等早期文档里的绝对路径与技能数量可能过期。现状一律以 `catalog/` 与 QODER_HANDOFF.md 为准。
- `optimization/skillopt/` 是 vendored 子项目，自带 `.env.example`、`requirements.txt`、独立 `.gitignore`。不参与周度流程，要用单独按它的 README 装环境。

## 周度自动化

旧机任务（Quest / `qoder_cron`）：

| 字段 | 值 |
|---|---|
| id | `436c5b6e-10c6-487b-b73a-1504e4cc89c0` |
| name | Boutique Skills 周度治理 |
| schedule | cron `0 9 * * 6`，Asia/Shanghai（每周六 09:00） |
| executionScope | `directory`，cwd = 仓库绝对路径 |
| permissionMode | `bypassPermissions`（Full Access） |
| outputMode | `independent`（独立会话） |
| model | `qmodel_latest` |
| 最近一次 | 2026-11-21 09:00 succeeded，耗时约 37 分钟 |

instruction 全文随盘放在迁移包 `config/boutique-skills-cron.json`，新机照抄、只改 cwd 与仓库路径两处。**同一时间只允许一台机器启用**：两台同时跑会重复发现、重复发布并互相覆盖。切换顺序是先停旧机、验收新机、再建新机任务。

任务跑完的汇报口径与监督要点写在 instruction 里，也见 docs/WEEKLY_CURATION.md。任何一步失败就停下写 findings.md 再报告，不要跳过审计或测试强行发布。

## 禁止事项

- 不要两台机器同时启用周度任务。
- 不要在验收前自动推送、发布或重建远端。副本带着完整 `.git` 与远端配置，`git push` 是真会生效的。
- 不要 `git reset --hard`、`git clean`、`git checkout --` 覆盖工作区，不要 force-push 或 squash 已发布历史。
- 不要提交 `reports/finance-skill-eval/tushare-eval/` 下那 4 个保护文件。
- 不要把密钥值写进文件、提交、报告或回复。
- 卸载建议只写 `reports/usage/pending-cleanup.json`，等用户当场确认再执行；Qoder 客户端重装会还原已归档技能，确认不要跨周悬挂。