# free-stockdb Review - 2026-08-05

## Source

- Repository: [hello245m/free-stockdb](https://github.com/hello245m/free-stockdb)
- Snapshot: `f4b54e65e0b05ba6f0f8a990f4c68dd930f763fd`
- Activity: 1,750 stars, 251 forks, latest push 2026-08-05
- Release: `v0.2.1` test build, Windows only
- License: MIT for repository code; market-data rights remain unspecified by source
- Upstream format: database project, not a native Agent Skill

## Decision

**Do not import in the current state. Score: 52/100, 2 stars.**

The local-first A-share data-engine concept is useful and would complement
`a-stock-data`: the latter focuses on live multi-source research endpoints,
while free-stockdb aims to provide reusable local historical bars for bulk
research and backtesting. The current repository, however, does not reproduce
the capabilities advertised by its release package and does not meet this
repository's provenance and execution-safety threshold.

| Dimension | Score | Reason |
|---|---:|---|
| Functional coverage | 18/20 | Ambitious daily/minute/tick storage, adjustment, indicators, boards, HTTP, Python, Excel, HTML, and MCP surface. |
| Actionability | 8/20 | The public repository contains no data mirror and no usable default source; the Python and MCP paths cannot import from source. |
| Implementation and tests | 7/20 | The C++ project builds and the manifest updater works, but core C++ client methods return empty results, the open indicator endpoint only calculates MA5, and there are no tests or CI workflows. |
| Portability | 5/15 | Source builds on macOS with local dependencies, but the only published runtime is a Windows test package and the required Python extension modules are Windows binaries. |
| Safety and provenance | 6/15 | The updater checks size and SHA-256, but the release defaults to plain HTTP, data provenance is not auditable, the open server permits unauthenticated writes with wildcard CORS, and the supplied checksum file does not identify or match the release archive. |
| Uniqueness and maintenance | 8/10 | The local A-share data-engine niche is valuable and development is active, but the project is still early and release/source parity is weak. |

## Verified Findings

### What worked

- CMake configuration and compilation passed on macOS after building LevelDB in
  a temporary prefix; no system package was installed.
- The open-source updater successfully synchronized and verified a synthetic
  local manifest using size and SHA-256 checks.
- The C++ server started on loopback and handled basic LevelDB set/get requests.
- Python files passed bytecode compilation, and the repository contains a real
  stdio MCP protocol implementation rather than only a prompt document.

### Release and source do not match

- `pybao/stock_sdk.py` imports `stockdb`, and `pybao/zhibiao.py` imports
  `zb_core`; neither extension module nor its build source exists in the Git
  repository. Both imports fail from a clean checkout.
- The Windows release contains opaque `stockdb.pyd`, `zb_core.pyd`,
  `stockdb.exe`, and updater binaries. Those binaries implement the production
  path described in the README, not the open C++ client in the repository.
- `StockDbClient::get_stock_list`, `get_kdata`, and `get_factors` return empty
  vectors in the public C++ implementation.
- The public `zb.get` HTTP route ignores the requested indicator and always
  emits a five-period moving average. This does not reproduce the advertised 39
  indicators.
- The release is Windows-only despite README and commit messages claiming
  completed macOS and Linux versions.

### Data and integrity claims are not independently verifiable

- The repository's `sync_url.txt` is intentionally empty. The Windows release
  instead defaults to `http://a.123128.xyz`, so initial acquisition is online
  and relies on an external, unencrypted mirror.
- No public data manifest was available in the repository for validating the
  claimed 26-year span, 7,400+ instruments, approximately 110 million records,
  corporate-action coverage, or update cadence.
- The repository does not identify the constituent market-data providers or
  provide source-by-source licensing and redistribution terms.
- GitHub's release-asset digest matches the downloaded ZIP, but the separately
  published `SHA256.txt` contains a different hash labelled only `lg`; it does
  not match the ZIP or any contained EXE/PYD file.
- Binary strings include a fixed external service URL and what appears to be a
  static authentication value. The opaque binaries were inspected but not run.

### Open-source server safety gaps

- The server exposes an unauthenticated `cmd=set` mutation over HTTP and emits
  `Access-Control-Allow-Origin: *` on every response.
- `stockdb.conf` shows an optional auth setting, but the public server entry
  point does not parse that file and the `password` field is not enforced.
- Query parameters are not URL-decoded. A standards-compliant encoded JSON
  value was stored and returned as literal percent-encoded text in the smoke
  test.
- Loopback is the default and limits exposure, but the CLI supports arbitrary
  bind addresses without adding authentication or read-only enforcement.

## Reconsideration Gate

Re-evaluate for import when upstream provides all of the following:

1. Reproducible source and build instructions for the `stockdb` and `zb_core`
   Python modules, or removes them in favor of the open C++ implementation.
2. Tested macOS and Linux releases, versioned together with the source snapshot
   and correctly labelled SHA-256 files.
3. HTTPS-only default mirrors, an authenticated or signed manifest, and a
   documented source-by-source data provenance and licensing matrix.
4. Enforced authentication or read-only mode for all non-loopback listeners,
   restricted CORS, URL decoding, input bounds, and failure-safe request parsing.
5. Tests and CI covering synchronization, adjustment factors, daily/minute
   queries, all advertised indicators, Python SDK behavior, and MCP calls.
6. Documentation that clearly separates verified open-source capabilities from
   closed release-only behavior and independently validates the coverage claims.

Until those conditions are met, retain `a-stock-data`, `tushare-api`, and the
existing backtest stack for production use. Do not install or execute the
Windows release as part of the Boutique Skills distribution.
