# WorkBuddy Investment Skills Review - 2026-08-05

## Source

- Xiaohongshu note: [workbuddy必装！投资行业6大王炸Skill！](https://www.xiaohongshu.com/user/profile/6874b3410000000007031f43/6a630734000000001101b791)
- Publisher: 启畅信息
- Observed engagement: 190 likes and 685 collections
- Public market archive: [infometa/workbuddyskills](https://github.com/infometa/workbuddyskills), snapshot `2bd6db6fe5678650e8272adafabbdceba61c3544`
- Archive status: 175 stars, 54 forks, no repository-level license; described by its maintainer as an offline study archive of public WorkBuddy CDN/market bundles

The six names were extracted from the original 720x1280 video rather than
inferred from the low-resolution screenshot: `neodata-financial-search`,
`westockdata`, `fund-analysis`, `research-report-writer`, `etf-filter`, and
`a-share-daily-review`.

## Decision

**Import only a constrained `westockdata` adapter. Group score: 58/100, 3 stars.**

The poster is a useful WorkBuddy marketplace shortlist, but it is not a single
open-source suite. Two entries are platform services, one invokes a protected
runtime, and three have no attributable public source matching the advertised
capability. Copying all six would turn private/platform dependencies into
apparently portable skills and duplicate stronger components already in the
Boutique Skills finance stack.

| Skill | Score | Decision | Reason |
|---|---:|---|---|
| `westockdata` | 76 | Import constrained adapter; optional only | The version-pinned npm CLI successfully returned cross-market search, A/H/US quotes, Hong Kong financial statements, and ETF details/holdings. It provides a convenient unified command surface. The two-file npm package has no declared license or source repository and ships a 2.6 MB obfuscated executable, so only a locally written adapter is redistributed. |
| `neodata-financial-search` | 61 | Do not import | Broad natural-language coverage, but the public package calls `copilot.tencent.com/agenttool/v1/neodata` and depends on a WorkBuddy `connect_cloud_service` temporary token. The archive has no license and the skill directs the model to prohibit alternative data sources, which conflicts with independent verification. It is not portable outside the WorkBuddy account/runtime. |
| `a-share-daily-review` | 59 | Do not import this advertised item | No attributable public source was present in the WorkBuddy archive. Public same-name repositories are unrelated third-party reimplementations: one licensed prompt-only framework scores lower than the installed `stock-daily-analysis-skill`; a more capable Codex implementation has no license. Existing daily review, AlphaEar, market breadth, policy, and reporting skills already cover this slot. |
| `research-report-writer` | 55 | Do not import | The advertised pipeline has no matching source in the WorkBuddy archive. Generic public skills with the same name are not evidence of provenance. Existing Anthropic equity research, `buy-side-equity-research-memo`, `stock-analysis`, `alphaear-reporter`, and Day1Global earnings workflows provide stronger, attributable report generation. |
| `fund-analysis` | 51 | Do not import | The discoverable package is a signed `runtime-mode: agent` proxy that requires the unavailable `skill_runtime_run` service and forbids independent execution. It contains no auditable analysis logic or data connectors. Public fund-analysis projects with the same generic name are not its upstream. |
| `etf-filter` | 44 | Do not import | No matching public `SKILL.md`, repository, or WorkBuddy archive package was found. The poster describes only a capability claim. `llmquant-etfs`, `westockdata` ETF commands, the existing data stack, and screeners already cover holdings, NAV, exposure, liquidity, and filtering inputs. |

## Verification

`westock-data-clawhub@1.0.4` was executed in a temporary directory with no
credentials. These commands returned non-empty data on 2026-08-05:

```bash
npx -y westock-data-clawhub@1.0.4 search 腾讯控股
npx -y westock-data-clawhub@1.0.4 quote sh600519,hk00700,usAAPL
npx -y westock-data-clawhub@1.0.4 finance hk00700 --num 2
npx -y westock-data-clawhub@1.0.4 etf sh510300
```

The runtime identity was fixed to shasum
`b434e6ca4b434455201f1d8af56da435f518b678` and npm integrity
`sha512-Cr4IS69wJ6aFdaDv7Sh/Zwf1FEj+8BHxegIltjWg4bswjV2SfbG9VmM0YN4SwfaLJlP1INzM0Ed3LXP+3WpjSA==`.
The npm metadata provides neither `license` nor `repository`; its archive
contains only `package.json` and an obfuscated `scripts/index.js`. Successful
output therefore establishes utility, not open-source status or full safety.

## Overlap And Placement

`westockdata` overlaps `a-stock-data`, `global-stock-data`,
`tushare-openclaw-skill`, and `yfinance-data`. Its incremental value is a single
A/H/US CLI with broad ETF, flow, financial, shareholder, and calendar commands.
That convenience merits optional high-tier catalog placement, but does not
justify replacing the existing standard data foundations, whose source,
license, methodology, and fallbacks are more auditable.

Do not add any of the six poster entries to the general standard bundle or the
finance standard suite in this review. Reconsider `neodata-financial-search`
when Tencent publishes a portable authentication path and an explicit license;
reconsider the other four when their exact market packages have attributable
source, license, execution requirements, and reproducible tests.
