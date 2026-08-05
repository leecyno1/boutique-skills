---
name: westockdata
description: >-
  Query A-share, Hong Kong, and US stock, index, sector, and ETF data through
  the version-pinned westock-data-clawhub CLI. Use when one consistent command
  surface is more useful than writing data-fetching code: quotes, K-lines,
  financial statements, capital flow, technical indicators, shareholders,
  dividends, ETF holdings/NAV, market boards, calendars, or cross-market
  comparisons. Treat results as unverified market data, cite the command and
  retrieval time, and do not use this skill for trade execution or as the sole
  basis for an investment decision.
metadata:
  upstream-package: westock-data-clawhub@1.0.4
  reviewed: "2026-08-05"
---

# WeStock Data

This is a constrained adapter for the external `westock-data-clawhub` npm CLI.
The executable is not mirrored here: npm publishes an obfuscated single-file
program without a declared software license or public source repository. Always
run the exact reviewed version and keep the package cache outside this skill.

## Safety Rules

1. Use only `westock-data-clawhub@1.0.4`. Never use `@latest` and never install
   it globally.
2. Ask before the first execution in a sensitive or production environment.
   The package is executable third-party code and cannot be fully audited from
   readable source.
3. Do not pass credentials, private portfolio files, personal identifiers, or
   unpublished research to the CLI. Its documented commands require none.
4. Run read-only data commands only. Do not repurpose the package for order
   placement, account access, or unattended trading.
5. Label the market, currency, as-of time, command, and data limitations in the
   answer. Cross-check material figures against an independent source.
6. Never present technical indicators, flows, rankings, or generated analysis
   as personalized investment advice.

## Preflight

```bash
node --version
npm view westock-data-clawhub@1.0.4 version dist.integrity dist.shasum
```

Expected package identity:

- version: `1.0.4`
- shasum: `b434e6ca4b434455201f1d8af56da435f518b678`
- integrity: `sha512-Cr4IS69wJ6aFdaDv7Sh/Zwf1FEj+8BHxegIltjWg4bswjV2SfbG9VmM0YN4SwfaLJlP1INzM0Ed3LXP+3WpjSA==`

Stop if npm reports a different identity. Node.js 18 or newer is required.

## Command Routing

Run commands from a temporary or user-owned working directory:

```bash
npx -y westock-data-clawhub@1.0.4 search 腾讯控股
npx -y westock-data-clawhub@1.0.4 quote sh600519,hk00700,usAAPL
npx -y westock-data-clawhub@1.0.4 kline sh600519 --period day --limit 60 --fq qfq
npx -y westock-data-clawhub@1.0.4 minute hk00700 --days 5
npx -y westock-data-clawhub@1.0.4 finance hk00700 --num 4
npx -y westock-data-clawhub@1.0.4 profile usAAPL
npx -y westock-data-clawhub@1.0.4 technical sh600519 --group ma,macd,rsi
npx -y westock-data-clawhub@1.0.4 dividend sh600519 --years 5
npx -y westock-data-clawhub@1.0.4 etf sh510300
npx -y westock-data-clawhub@1.0.4 etf-holdings sh510300
npx -y westock-data-clawhub@1.0.4 etf-nav sh510300 --start 2026-01-01 --end 2026-06-30
```

Additional documented read-only commands include:

- A-share flow and trading context: `asfund`, `lhb`, `blocktrade`,
  `margintrade`, `chip`.
- Hong Kong and US context: `hkfund`, `usfund`.
- Ownership and corporate actions: `shareholder`, `exdiv`, `reserve`,
  `suspension`.
- Market context: `hot stock`, `hot board`, `hot etf`, `board`, `calendar`,
  `ipo`.

Use prefixed identifiers such as `sh600519`, `sz000001`, `bj920xxx`,
`hk00700`, and `usAAPL`. `search` and `minute` do not support comma-separated
batch input. Minute data, ownership fields, and market-specific flow commands
have narrower coverage than quotes and daily K-lines.

## Output Contract

For every result, provide:

1. `Request`: instruments, market, period, adjustment method, and requested
   fields.
2. `Retrieved`: local timestamp and the exact version-pinned command.
3. `Result`: a compact table with explicit currencies and units.
4. `Checks`: stale dates, missing fields, suspicious zeros, inconsistent
   currencies, and one independent corroboration for decision-critical data.
5. `Limits`: unofficial data provenance, possible delay or endpoint changes,
   and no investment recommendation.

Do not silently interpret missing values as zero. For cross-market financial
comparisons, normalize reporting periods and currencies before calculating
growth or ratios.

## Position In The Finance Stack

Use `a-stock-data` for the repository's deeper, auditable A-share research
endpoints and `global-stock-data` for the richer official-source-first US/HK
stack. Use `tushare-openclaw-skill` when a licensed structured A-share API and
repeatable dataset are required. `westockdata` is the optional lightweight
cross-market CLI, not a replacement for those standard data foundations.
