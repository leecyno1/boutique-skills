# SkillOpt Usage Guide

SkillOpt is an optional optimization layer for improving selected skills with repeatable evaluations. It should be used as a controlled experiment loop, not as an automatic rewrite tool for the whole registry.

## Best Fit

Use SkillOpt when the target skill has measurable outputs and repeatable examples:

| Skill type | Good benchmark shape | Example candidates |
|---|---|---|
| Search / research QA | question, context, expected answer | `url-to-markdown`, `yc-reader`, `news-radar` |
| Data / finance analysis | scenario, data context, expected judgment | `a-stock-data`, `funda-data`, `yfinance-data` |
| Document / spreadsheet workflows | file/task description, expected output or rubric | `minimax-docx`, `minimax-xlsx`, `nano-pdf` |
| Coding helpers | issue, repo context, expected patch rubric | `frontend-dev` |
| Content workflows | brief, constraints, reference answer/rubric | `baoyu-format-markdown`, `baoyu-xhs-images` |

## Poor Fit

Do not use SkillOpt for:

- Metadata-only changes such as category, rating, upstream URL, or README table edits.
- Skills without a stable evaluation set.
- Broad creative skills where there is no clear pass/fail or rubric.
- Imported upstream skills before reviewing license and attribution implications.
- Bulk rewriting many skills in one run.

## Recommended Process

1. Pick one skill and one narrow failure mode.
2. Create a small dataset with `train`, `val`, and `test` splits.
3. Run SkillOpt and inspect `best_skill.md` as a candidate only.
4. Manually compare the candidate against the upstream skill and local guide.
5. Accept only the smallest useful changes into `skills/default/<skill-id>/SKILL.md`.
6. Regenerate catalog/docs and run audit/tests.
7. Record the optimization result in the skill guide or a short changelog note.

## Quality Gates

Before accepting an optimized skill:

- The candidate must improve the validation/test score or fix a named failure mode.
- The candidate must preserve native upstream origin and license notes.
- The candidate must not add hidden API-key requirements.
- The candidate must keep the skill trigger description concise and accurate.
- The candidate must not make a specialist skill pretend to be a foundation skill.
- The accepted diff should be reviewed by a human, not copied wholesale.

## Suggested First Targets

The tracked candidate queue lives in `optimization/skillopt-candidates.json`.

| Priority | Skill | Template | Why |
|---|---|---|---|
| 1 | `url-to-markdown` | `qa` | Clear QA/extraction outcomes and many edge cases. |
| 2 | `a-stock-data` | `finance-analysis` | High-value standard bundle skill with measurable finance queries. |
| 4 | `baoyu-format-markdown` | `content-rubric` | Content formatting can be tested with rubric-based examples. |
| 5 | `frontend-dev` | `coding-rubric` | Can use visual/spec compliance rubrics, but needs careful datasets. |

## Commands

Scaffold a dataset:

```bash
python3 optimization/scripts/create_skillopt_dataset.py <skill-id> --template qa
```

Supported templates: `qa`, `finance-analysis`, `content-rubric`, `coding-rubric`.

Run SearchQA-style optimization:

```bash
export SKILLOPT_OPTIMIZER_MODEL=<optimizer-model>
export SKILLOPT_TARGET_MODEL=<target-model>
python3 optimization/scripts/check_skillopt_ready.py <skill-id> --require-models
./optimization/scripts/run_skillopt_searchqa.sh <skill-id>
```

Review candidate output:

```bash
python3 optimization/scripts/review_skillopt_candidate.py <skill-id>
open optimization/skillopt-runs/<skill-id>/review.md
```

## Repository Policy

SkillOpt outputs under `optimization/skillopt-runs/` are local artifacts and must not be committed. Only reviewed, minimal changes to the actual skill files should enter the repository.
