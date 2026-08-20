# 评分体系

五星标签由 100 分综合评分映射而来：

| 分数 | 星级 |
|---:|---:|
| 90-100 | 5★ |
| 75-89 | 4★ |
| 60-74 | 3★ |
| 40-59 | 2★ |
| 0-39 | 1★ |

## 当前评分因子

| 因子 | 权重/规则 |
|---|---|
| 原生来源可信度 | verified override +25，本地引用 +15，缺失 -20 |
| 横向通用性 | L1 +20，L2 +12，L3 +5 |
| 风险 | low +10，medium +4，high -8 |
| 使用门槛 | direct +8，browser/mcp +3 |
| 文档描述 | 有描述 +7 |
| 本地使用频率 | +0~8（log₂ 调用次数 × 时间衰减，来自 scripts/telemetry_collect.py 本地遥测；无数据时为 0） |
| 预置排除 | Open/Hermes 已预置的 skill 不进入标准配置组 |

## 后续月评增强

月评任务应补充 GitHub stars/forks/release、ClawHub/CL.Up rating/downloads、skills.h 热度与更新时间。没有可验证原生来源的 skill，即使本地可用，最高只能评为 2★。
