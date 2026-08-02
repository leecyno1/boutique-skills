# Changelog

## v2.0.3 — 2026-07-26

### 修复：EDGAR Frames 对资产负债表科目一直返回 404

`market_frame()` 一律拼 `CY{year}Q{q}` / `CY{year}`，但 SEC Frames 对**时点(instant)概念**
要求周期带 `I` 后缀，且不提供纯年度周期。`XBRL_TAGS` 里有 4 个属于此类，此前**全部取不到数**：

| 标签 | 修前 | 修后 |
|---|---|---|
| 总资产 `Assets` | `CY2025Q1` → 404 | `CY2025Q1I` → 5643 家 |
| 股东权益 `StockholdersEquity` | 404 | 5465 家 |
| 现金及等价物 `CashAndCashEquivalentsAtCarryingValue` | 404 | 4506 家 |
| 长期负债 `LongTermDebtNoncurrent` | 404 | 1532 家 |

年度请求同样受影响（`Assets/CY2024` → 404），现落到 `CY2024Q4I`。

新增 `_INSTANT_TAGS` 集合做区分；期间(duration)概念行为不变。

`market_frame()` 还支持传**任意原始 XBRL 标签**（`Liabilities` / `InventoryNet` /
`AssetsCurrent` …），这些不在内置别名表里、同样是时点概念。因此改为**自动回退**：
先按 `_INSTANT_TAGS` 猜一种周期形式，收到 404 再换另一种重试，无需穷举所有时点概念。
已知类型时可显式传 `instant=True/False` 省掉一次探测请求。
验证：13 个标签 × 季度/年度共 26 项请求全部返回有效数据（修前 8 项为 404）。

### 加固：OCC 合约代码允许调整后根符号

`_OSI` 的 root 由 `[A-Z]+` 放宽为 `[A-Z][A-Z0-9]*`。拆股/分拆等公司行为会产生带数字的
调整后合约根（如 `NVDA1`、`BRKB1`），原正则会直接拒绝、`options_chain_cboe()` 静默漏掉这些合约。
后续均为定宽组，正则回溯可正确对齐，标准合约解析结果不变。

验证：NVDA/AAPL/TSLA/T 共 14,424 份真实合约解析成功率 100%；合成的调整后代码亦能正确切分。
（说明：CBOE 按标的返回的链中当前只含标准根，未能实地复现漏解析，此项为防御性加固。）

## v2.0.2 — 2026-07-26

### 修复：腾讯行情字段下标错误 — 两个函数此前 100% 崩溃

感谢 [@HoRiZonn0](https://github.com/HoRiZonn0)（issue #2）提供完整字段对照。逐条实测复现后确认其报告**全部正确**，并发现比报告更严重的后果：

- **`us_stock_quote_tencent` 每次调用必抛 `ValueError`** —— `high_52w` 读 `fields[35]`，而下标 35 实为币种字符串 `"USD"`，`float("USD")` 直接崩。
- **`hk_stock_quote_tencent` 同样必崩** —— `volume` 读 `fields[6]`，港股该字段带小数位（`"22959603.0"`），`int()` 解析失败。此项非 issue 所报，为本次复测新发现。

即：**这两个函数在 v2.0.1 及更早版本中从未真正可用过。**

修正的下标（美股 71 字段 / 港股 78 字段，布局不同，此前误共用一套）：

| 字段 | 原值 | 修正为 | 实测依据 |
|---|---|---|---|
| 英文名 | 美 27 / 港 2 | 美港统一 **46** | `Apple Inc.` / `TENCENT` |
| PE | 美 53 / 港 39 | 美港统一 **39** | 40.32 / 15.87（原 53 实为总市值） |
| PB | 统一 56 | 美 **51** / 港 **58** | 45.93 / 3.14（原 56 美股为 `"GP"`、港股为 0） |
| 52 周高 / 低 | 35 / 36 | **48 / 49** | 334.99·200.72 / 677.7·411.0 |
| 市值 | 44 标注为总市值 | **44=流通 / 45=总** | AAPL 48881 vs 48911 亿，与总股本 `fields[62]` 反算一致 |
| 币种 | 未提供 | 美 **35** / 港 **75** | `USD` / `HKD` |

其他改动：

- 新增 `currency` 字段；美股新增 `eps`（下标 47，`price ÷ eps = pe` 自洽验证）；港股 `fields[2]` 正名为 `code`
- `volume` 统一改用 `int(float(x))`，消除小数位崩溃这一类隐患
- 长度守卫由笼统的 `< 50` 收紧为按实际读取深度判定（美股 52 / 港股 76）
- §1.2 新增**腾讯行情字段对照表**，美港分列、标注「亿本币」单位，并附自行复现命令

验证：`usAAPL` / `usNVDA` / `hk00700` / `hk09988` 四例全部取数正常，数值与腾讯页面一致。

## v2.0.1 — 2026-07-24

### 修复：错误处理把「没数据」和「出故障」混为一谈

v2.0.0 的 Layer 9/10 用 `except Exception: continue` 做日期回退，会**吞掉一切异常**。
后果是 `SEC_CONTACT` 没配置时，用户看到的是"未找到近 7 个工作日的 EDGAR 每日索引"，
而不是"请先配置 SEC_CONTACT"——v2.0.0 特意加的 fail-fast 提示因此永远不会显示。

本版引入明确的异常语义：

- **新增 `DataNotAvailable(RuntimeError)`**：该日/该资源确实没有数据（非交易日、文件尚未发布、标的无期权），调用方可安全回退
- **`RuntimeError`**：配置错误、限流、网络故障 —— 必须冒泡，不得伪装成"没数据"
- **`ValueError`**：参数错误（如把港股代码传给仅支持美股的层）

三处日期回退循环改为只捕获 `DataNotAvailable`；`short_volume_all` / `daily_filings` /
`options_chain_cboe` 的"找不到数据"改抛 `DataNotAvailable`，与调用方的捕获类型对齐。

### 修复：403 的三种含义现在能精确区分

**根因**：SEC Archives 与 FINRA CDN 都托管在 S3 上，而 S3 在调用方没有 `ListBucket`
权限时，对**不存在的对象返回 `403 AccessDenied`（XML）而非 `404 NoSuchKey`**。
两个源实测行为一致。这意味着"当日文件尚未发布"和"被拒绝"共用同一个状态码。

现按响应内容**正向识别**（而非用排除法，否则限流/封禁会被当成"没数据"）：

| 情况 | HTTP | Content-Type | 判定 |
|---|---|---|---|
| 对象不存在 | 403 | `application/xml` + `<Code>AccessDenied</Code>` | `DataNotAvailable`，可回退 |
| SEC UA 未声明 | 403 | `text/html` + `Undeclared Automated Tool` | `RuntimeError`，提示 UA 格式 |
| 限流 / 封禁 / 其他 | 403 | 其他 | `RuntimeError`，冒泡 |

`official_get()` 的 `missing_codes` 参数因此移除——判据改为内容驱动，调用方无需传参。

### 修复：0DTE 日期在冬令时会算错一天

`_et_today()` 原先硬编码 UTC-4（EDT）。冬令时美东是 UTC-5，导致 UTC 04:00–05:00
这一小时被算成次日，`filter_expiry(chain, "0DTE")` 与 `dte_max` 会选错到期日。

改用 `zoneinfo.ZoneInfo("America/New_York")`；无 tzdata 的环境（部分 Windows）
回退到自算 DST，切换时刻按纽约当地 2:00 换算为 UTC（开始 07:00 UTC / 结束 06:00 UTC），
而非笼统用 00:00 UTC。

### 说明

十三层架构 / 30+ 端点 / 11 数据源不变；本版为错误处理与时区正确性补丁。
问题由 Codex CLI 独立审计发现，三轮审计—修复—复审后确认无回归。


## v2.0.0 — 2026-07-24

### 新增：官方源优先架构（八层 → 十三层，18 → 30+ 端点，5 → 11 数据源）

新增层的主力数据全部取自**美国政府 / 自律组织 / 交易所**的公开端点：

- **Layer 6.1 · CBOE 官方期权链**（新增，Yahoo 期权降为 6.2 后备）
  - 全链含 `iv / delta / gamma / vega / theta / rho`——**Yahoo 期权链没有希腊字母**
  - `filter_expiry(chain, "0DTE")` 取当日到期合约；`unusual_activity()` 用 **vol/OI > 1**（当日成交超存量持仓＝新建仓）识别 flow
  - `chain_summary()` 输出 put/call 量比与持仓比、**成交量加权 IV**、**净 delta 敞口**
  - 实测：NVDA 全链 3,908 / 0DTE 168；TSLA 全链 6,200 / 0DTE 326
- **Layer 9 · FINRA Reg SHO 做空层**：全市场每日空头成交量，单文件覆盖 **12,112 只**；含个股时序与占比排行
- **Layer 10 · EDGAR 申报事件流**：每日索引（实测单日 **Form 4 内部人 547 / 8-K 370 / 13F-HR 261 / 144 118**）+ 全文检索（2001 至今所有申报正文）
- **Layer 11 · EDGAR frames 全市场横截面**：任意 XBRL 标签一次拿全市场＝**免费 screener**（净利润 CY2025Q1 覆盖 5,309 家，研发费用覆盖 1,842 家）
- **Layer 12 · 宏观/日历**：美债收益率曲线（1M~30Y）、CFTC COT 持仓报告、Nasdaq 财报日历

### 新增：合规分级（每个源标注级别 + 条款原文）

逐家实读各源条款后分级，**"官方"不等于"可自由使用"**：

- **S 级**（可商用可再分发）：SEC EDGAR / Treasury / CFTC
- **B 级**（商用需自行确认）：FINRA
- **C 级**（需事先授权或条款未核实）：CBOE / Nasdaq / Yahoo / 东财 / 新浪 / 腾讯
- **⛔ 已排除**：HKEX CCASS——其条款明文禁止 robot/bot/spider/scraper 且适用于"whether or not for gain"，**故本工具不提供该抓取代码**

README 与 SKILL.md 均给出条款原文摘录。**本工具只分发代码，不分发任何市场数据。**

### 新增：统一 HTTP 出口（限流 + UA 声明 + 友好错误）

- `_RateLimiter` **线程安全**节流器（用锁，避免并发下被击穿）
- 按源限速：**SEC 官方硬上限 10 req/s，此处设 8 req/s** 留余量；FINRA/CBOE 4/s、Nasdaq 2/s
- `SEC_CONTACT` 未改为真实邮箱时**直接报错**并说明原因（SEC 要求声明 User-Agent，否则返回 Undeclared Automated Tool）
- `assert_us_ticker()` 拦截把港股代码传给仅支持美股的层
- HTTP 403/404/429 给出针对性提示

### 其他

- 顶部新增**端点路由速查表**（按需定位，不必通读全文）
- 架构图、数据源优先级表、数据源汇总表同步更新，汇总表增加"合规级"列
- 原 Layer 1–8（含技术指标层）编号与内容不变，**向后兼容**

### 注意

- ⚠️ 使用前必须把 `SEC_CONTACT` 改成你自己的真实姓名与邮箱
- ⚠️ 若自行改用 `urllib` 实现，**必须手动 `gzip.decompress`**（`requests` 会自动解压，`urllib` 不会）——否则 SEC 返回内容解析失败、表现为"数据莫名变少"


## v1.0.1 — 2026-06-20

### 修复（PR #1 @APTX4869-maker + 连带 bug）
- **5 个函数漏传 `params` 导致始终拿不到数据（PR #1）**：`stock_quote_eastmoney` / `stock_kline_yahoo` / `fund_flow_daily` / `stock_search` / `market_stock_list` 都构造了 `params` dict，但 `requests.get(url, ...)` 时漏了 `params=params`，请求实际是裸 URL → 服务端返回空（东财 push2 返回 `rc:102`/`data:null`）。一次性补齐 5 处。**实测确认**：漏传时 `data=None`，补齐后 `market_stock_list` 返回 `total=5990`。致谢 @APTX4869-maker 的排查与验证。
- **连带 bug：`market_stock_list` 在 `diff` 为 dict 时崩溃（本次一并修）**：补齐 params 后该函数能拿到响应，但东财 push2 的 `diff` 字段**有时是 list、有时是按序号为键的 dict**（如 `{"0":{...},"1":{...}}`）。旧代码 `for item in diff` 遇 dict 会拿到字符串键 → `AttributeError: 'str' object has no attribute 'get'`。新增 `if isinstance(diff, dict): diff = list(diff.values())` 归一化。**实测确认**：当前返回的 `diff` 正是 dict 结构，归一化后正常遍历。

### 说明
- 八层架构 / 18 端点 / 5 数据源不变；纯 bug 修复补丁。这 5 个端点此前**始终返回空数据**，升级强烈建议。

## v1.0 — 2026-05-20

### 首次开源发布

- **八层数据架构**：行情 / K线 / 技术指标 / 基本面 / 资金面 / 期权 / SEC Filing / 工具
- **18 个端点**覆盖美股 + 港股全品类数据
- **5 个数据源**：东财（push2 + push2his + datacenter + search）、Yahoo Finance（crumb 自动管理）、新浪财经、腾讯财经、SEC EDGAR
- 全部零鉴权（Yahoo crumb 自动获取，SEC 仅需 User-Agent）
- 仅依赖 `requests`，零第三方数据封装
- 内嵌完整 Python 代码，AI 编程助手直接可用
- 2026-05-20 全部端点实测验证

### 端点清单

| 层 | 端点 | 数据源 |
|----|------|--------|
| 行情 | 美股/港股实时报价 × 3 | 新浪 + 腾讯 + 东财push2 |
| K线 | 日/周/月/分钟 × 2 | 新浪 + Yahoo chart |
| 技术指标 | MA/EMA + MACD + RSI + KDJ + 布林带 × 1 | 纯Python计算（基于K线OHLCV） |
| 基本面 | 财报三表 + GMAININDICATOR + Yahoo 23模块 + SEC XBRL | 东财datacenter + Yahoo + EDGAR |
| 资金面 | 日级资金流 × 1 | 东财push2his |
| 期权 | 期权链 × 1 | Yahoo |
| SEC Filing | Filing列表 + XBRL × 2 | EDGAR |
| 工具 | 搜索 + 全市场列表 + 新闻 + CIK映射 × 4 | 东财search + 东财push2 + Yahoo + SEC |

### 实测发现与修正

- **东财 push2his K线不覆盖美股/港股**：kline/get 端点对美股(105.AAPL)/港股(116.00700) secid 返回空数据，仅资金流(fflow/daykline/get)正常。K线层改为新浪(美股) + Yahoo chart(美股+港股)
- **Yahoo 新闻需要 cookie**：v1/finance/search 裸请求返回 400，需先访问 fc.yahoo.com 获取 cookie
- **东财 push2 实时行情已验证**：push2.eastmoney.com/api/qt/stock/get 对美股(105.AAPL)和港股(116.00700)均返回完整数据
- **东财 GMAININDICATOR 已验证**：美股(RPT_USF10)返回49字段，港股(RPT_HKF10)返回75字段
- **东财 push2 全市场列表已验证**：美股(m:105)返回5925只，港股(m:116)返回18000+只
