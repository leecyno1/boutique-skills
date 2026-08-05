# GitHub Skill Review: Day1Global-Skills

- Review date: 2026-08-05
- Xiaohongshu lead: https://www.xiaohongshu.com/explore/6a71792a000000002701ecc5
- Upstream: https://github.com/star23/Day1Global-Skills
- Snapshot: `562c14b0c0bc84abff755181ead30ebea613d063`
- Popularity at review: 1,015 stars and 157 forks
- Last code push: 2026-04-15
- License: MIT
- Suite decision: **import, 79/100, 4 stars**

## Scorecard

| Skill | Score | Decision | Main reason |
|---|---:|---|---|
| `tech-earnings-deepdive` | 85 | Import + finance standard slot | Strongest item: 16-module earnings workflow, primary-source hierarchy, multi-method valuation, variant view, pre-mortem, and explicit action triggers. Upstream omitted three referenced files; the mirror replaces those broken references with self-contained checks. |
| `macro-liquidity` | 82 | Import + finance standard slot | Compact and useful Fed net-liquidity, SOFR, MOVE, and yen-carry dashboard. It adds a practical liquidity-specific view beside the broader `llmquant-macro` and policy tools. |
| `btc-bottom-model` | 78 | Import as optional specialist | The 13-indicator weighting is transparent and the live endpoint works, but field-level provenance and historical calibration are not independently published. The mirror requires corroboration and score recomputation. |
| `us-market-sentiment` | 76 | Import as optional specialist | Clear five-indicator dashboard, but institutional allocation, retail-flow, and prime-broker leverage data are often delayed, paywalled, or available only through secondary reporting. |
| `us-value-investing` | 72 | Import only as part of the suite | Easy to use, but the four-factor 12-point model is too coarse across sectors and overlaps `stock-analysis`, `us-stock-analysis`, DCF, and investor-lens skills. It is not a standard recommendation. |

## Method

The editorial score uses six dimensions: investment-method depth (25), data and evidence reproducibility (20), risk controls and disclaimers (15), Skill engineering quality (15), executability and dependencies (15), and license and maintenance (10).

## Security And Reliability Review

- All five packages contain instruction-only `SKILL.md` files; there are no executable scripts, shell commands, credential collectors, or local file mutations.
- The MIT license is present at repository root and copied into each mirrored skill.
- `btc-bottom-model` calls `https://brief.day1global.xyz/api/btc-score`. The endpoint returned fresh JSON during review, but it does not provide field-level source provenance and its schema differed from the instructions: the live fields are `score` and root `fearGreed`, not `totalScore` and `sentiment.cryptoFearGreed`.
- The mirror removes a mandatory promotional footer from all five skills.
- The upstream `tech-earnings-deepdive` refers to `references/valuation-models.md`, `references/investing-philosophies.md`, and `references/bias-checklist.md`, but none exists in the repository. The mirror removes the first two false dependencies and embeds the missing anti-bias checklist.
- No examples or prebuilt `.skill` archives are mirrored because they add no runtime capability and would duplicate the source documents.

## Overlap And Standard-Suite Decision

`tech-earnings-deepdive` overlaps with Anthropic earnings research, `earnings-recap`, `stock-analysis`, and DCF tooling, but its technology-specific A-P structure, six-lens confrontation, variant view, and action-trigger design provide meaningful incremental depth.

`macro-liquidity` overlaps with `llmquant-macro`, `macro-regime-detector`, and `policy-monitor`; its narrower four-indicator liquidity dashboard is distinct enough to keep.

The remaining three skills are useful optional views, not replacements for the current standard components. The full five-skill upstream is represented as the `day1global-skills` suite and included source family, while only the two strongest incremental skills receive named finance standard slots.

## Decision

**Import all five as an audited source suite. Add `tech-earnings-deepdive` and `macro-liquidity` to the finance standard slots. Do not add any of the five to the general no-duplicate standard bundle.**
