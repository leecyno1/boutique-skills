# AlphaGBM Skills Review

- Review date: 2026-08-06
- Upstream: https://github.com/AlphaGBM/skills
- Snapshot: `6ecea742ed80b50c2b8789e1f4b709d8db8fef19`
- Upstream activity: 1,703 stars, 220 forks, last push 2026-07-09
- License: MIT
- Decision: import all 30 skills as an optional high-tier finance suite
- Editorial score: **82/100 (4/5 stars)**

## Identification

The screenshot refers to AlphaGBM. Despite the wording around "quant", this is
not a LightGBM training framework. It is an Agent Skill collection backed by the
AlphaGBM stock and options research API.

## Score

| Dimension | Score | Reason |
|---|---:|---|
| Capability depth | 18/20 | Strong options coverage: IV rank, smile/surface, Greeks, P&L, earnings crush, unusual activity, hedges, and BPS backtests. |
| Workflow quality | 17/20 | Clear triggers, output structures, related-skill routing, and usable research frameworks. |
| Data and reproducibility | 13/20 | Live results depend on a hosted proprietary API; the public repository mostly contains instructions and a small set of mock snapshots. |
| Safety and reliability | 14/20 | No broker integration was found, but upstream wording includes action-oriented labels and concrete order suggestions. Boutique hardening is required. |
| Maintenance and provenance | 12/15 | Recent MIT project with meaningful adoption, but README skill counts and some endpoint/mock-file references have drifted. |
| Incremental repository value | 8/15 | Useful second provider and good hedge/exit disciplines, but options coverage overlaps heavily with `llmquant-options`. |
| **Total** | **82/100** | **Good optional suite; not a core replacement.** |

## What It Adds

- A second real-data provider for options and stock research.
- Practical hedge, take-profit, fear, VIX, Marks-cycle, Tepper, and Buffett lenses.
- Persistent company profiles, theses, themes, alerts, and watchlists.
- A specialized AI supply-chain chokepoint framework.

## Limitations

- Live endpoints require `ALPHAGBM_API_KEY`; unauthenticated endpoint tests returned HTTP 401.
- Bundled mock data is illustrative and cannot support current-market claims.
- Many skills reference mock-data paths that are absent upstream.
- The README reports inconsistent suite counts (26/29) while the repository contains 30 skill directories.
- CLI and documentation endpoint details show some drift, and the CLI stores its key in plaintext under `~/.alphagbm/config.json`.
- Most analytical implementation is server-side and therefore cannot be independently audited from this repository.
- `STRONG_BUY`, panic-buy, active-position, and concrete GTC-order wording needs to be treated as framework output rather than personalized advice.

## Overlap Decision

`llmquant-options` already covers IV Rank, contract scoring, strategy design,
Greeks, P&L, smile/surface, unusual activity, earnings IV crush, and BPS
backtests. AlphaGBM therefore does not replace `llmquant-options` or
`options-strategy-advisor`. It enters the finance standard suite as an optional
source family, preserving provider choice without creating a duplicate named
standard slot.

## Import Hardening

Every imported skill includes a shared contract that:

- labels mock snapshots as illustrative and potentially stale;
- requires timestamp, symbol, market, currency, data window, and option contract metadata;
- requires independent corroboration for decision-critical data;
- separates source facts, calculations, assumptions, and interpretation;
- treats directional labels as research outputs rather than instructions; and
- prohibits broker connectivity, order placement, and unattended trading.

## Imported Skills

The suite contains 30 skills covering alerts, Bull Put Spread backtests,
Buffett and Duan lenses, chokepoint research, company profiles, comparisons,
earnings IV crush, fear scoring, Greeks, research health, hedging, theses, IV
rank, macro and sentiment, market-cycle signals, option scoring and strategies,
P&L simulation, prediction markets, stock analysis, take-profit analysis,
Tepper signals, themes, unusual activity, VIX, volatility smile/surface, and
watchlists.
