# UZI Skill Source Review

- Review date: 2026-08-06
- Decision: import as an optional high-tier finance application
- Editorial score: **86/100 (4/5 stars)**
- Upstream: <https://github.com/wbh604/UZI-Skill>
- Snapshot: `fce996c33e70eddce8e375f53cd252b549eb3d7c`
- License: MIT
- Verified GitHub metadata: 6,004 stars, 853 forks, pushed 2026-07-18 12:32:23 UTC
- Snapshot commit date: 2026-07-07 16:47:43 +08:00

## Score

| Dimension | Score | Notes |
|---|---:|---|
| Capability depth | 19/20 | A/HK/US research, 20 command workflows, valuation, screening, portfolio comparison, LHB and report generation. |
| Engineering and tests | 18/20 | Roughly 45K lines, 434 tracked files, 63 Python test modules, real runtime code and validation gates. |
| Data provenance and reproducibility | 15/20 | Multiple fallback providers and data-integrity checks, but public scraping and fallback behavior remain fragile. |
| Safety and reliability | 14/20 | No broker execution found; points deducted for action-oriented labels, persistent browser state, tunnels and rough valuation proxies. |
| Maintenance and provenance | 12/15 | MIT, recent fixes and substantial adoption; documentation has version and count drift. |
| Incremental repository value | 8/15 | Strong A-share application workflow, but overlaps existing finance, data, modeling and Serenity skills. |
| **Total** | **86/100** | **Import** |

## What It Adds

The project is a functioning research application rather than prompt-only packaging. It combines data collection and fallbacks, 22 research dimensions, institutional valuation and memo workflows, report rendering, A-share hot-money/LHB analysis, and risk-signal detection. Its strongest incremental value is the integrated A-share workflow and the ability to produce a coherent local report from several specialist paths.

The 66 investor/public-figure personas are retained inside one application package. They are not separate catalog skills because they share one runtime and many are simulated or generated framework stubs. Splitting them would inflate the catalog and falsely imply independent capability or endorsement.

## Risks And Hardening

- Persona outputs can create false authority. Boutique labels them as simulated frameworks, not endorsements, quotations, or current opinions.
- Deep mode advertises 5-8 minute runs with multiple agents and high token use. The agent must disclose this and choose the narrowest workflow.
- Public-data scraping may break or conflict with source expectations. Prefer filings, exchange disclosures, structured APIs, rate limits and explicit provenance.
- Playwright can persist Xueqiu cookies under `~/.uzi-skill/playwright-xueqiu/`; remote reports can use Cloudflare Tunnel; installers can add browsers or system software. None may be enabled without explicit consent.
- Some valuation paths use rough fallbacks such as FCF from net income or market cap and EBITDA from net income. Proxy-derived values must be labeled and cannot support confident target prices.
- Buy/sell labels, buy zones, ideal prices, stops and position sizes are hypothetical research outputs. No broker connectivity, order placement or unattended trading is permitted.
- Trap detection reports risk signals, not a fraud finding, unless supported by adequate primary evidence.

## Known Upstream Drift

- Root metadata says version 3.9.1 while README, package metadata and internal skills say 3.9.2.
- Documentation contains older counts for investors and methods (50/51/65 versus 66; 17 versus 22).
- Root and nested requirements disagree on the minimum BaoStock version.
- The optional hosted `MX_APIKEY` path exists even though the project can run without it and advertises a zero-key default.

## Verification Scope

Static review found no `shell=True`, `os.system`, dynamic `eval`/`exec`, or pickle-loading pattern in the reviewed runtime scan. Runtime code does use subprocesses, file-tree deletion in controlled paths, browser automation, and optional installation flows, so the imported safety contract is mandatory.

Import verification used an isolated Python 3.12 environment and did not modify the system Python or install a browser. The complete collected suite passed: **657 passed in 9.47s**. JSON validation, Python bytecode compilation, repository audit, and both suite dry-runs also passed. The 657-test result supersedes the upstream documentation's older claim of 649 tests for this snapshot.
