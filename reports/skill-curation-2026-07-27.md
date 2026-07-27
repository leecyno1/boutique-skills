# Skill Curation — 2026-07-27

## Decision

- Imported: `behavior-validator`.
- Exported from the active catalog: `baoyu-danger-gemini-web`, `baoyu-danger-x-to-markdown`.
- Net catalog change: 344 → 343 skills.

## Imported skill

### `behavior-validator` — 5★ / 92

- Upstream: `openclaw/agent-skills`, commit `fe588b1a6267eb47f785d0c748db9f6f3e9a3b4f`.
- License: MIT, copied into the skill directory.
- Completeness: `SKILL.md`, OpenAI interface metadata, behavior-contract template, report schema, source record, and license.
- Maintenance: official OpenClaw repository with recent activity.
- Distinct value: source-blind black-box validation against an explicit behavior contract, including anti-cheat probes and evidence requirements.
- Overlap review: complements source-aware code review, unit tests, and verification skills; it does not replace them.
- Safety: no bundled executable script, no API key, no automatic network action, explicit credential and evidence-redaction rules.
- Compatibility: standard `SKILL.md` structure; installed in medium and high tiers.

## Exported skills

### `baoyu-danger-gemini-web` — 2★ / 49

- Uses a reverse-engineered Gemini Web API and browser-cookie authentication state.
- High risk classification and brittle unofficial interface.
- Function is covered more safely by maintained official/API-backed image-generation skills.
- Removed from the active directory, high tier, catalog, README, and generated indexes.

### `baoyu-danger-x-to-markdown` — 2★ / 56

- Uses a reverse-engineered X API and requires authentication cookies/tokens.
- High risk classification and platform-breakage/account-restriction risk.
- URL extraction and social research remain covered by `url-to-markdown`, `agent-reach`, and browser-based workflows.
- Removed from the active directory, high tier, catalog, README, and generated indexes.

Both removals remain recoverable from Git history.

## Validation

- Catalog generation: passed.
- Catalog skills: 343.
- Missing skills: 0.
- Missing native origins: 0.
- Duplicate capabilities: 0.
- Standard bundle issues: 0.
- Repository tests: 7/7 passed.
- Python compile check: passed.
- Audit remains WARN because of 74 optional missing environment variables and 11 unrelated risk-pattern findings.
- Standard bundle membership remains 34 skills plus 2 packs; finance suite membership is unchanged.

## Protected worktree changes

The four pre-existing Tushare evaluation files remained unstaged and are excluded from this curation commit.
