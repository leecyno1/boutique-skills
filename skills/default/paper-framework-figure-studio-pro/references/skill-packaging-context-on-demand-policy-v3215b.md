# Skill Packaging Context-On-Demand Policy v3.2.15b

Reusable skill packages should minimize always-loaded context while preserving all runtime rules.

## Packaging rules

- Keep `SKILL.md` as the compact controller and highest-priority rule index.
- Put detailed policies in `references/` and load them only when the current request needs that rule family.
- Put reusable helpers and validators in `scripts/`.
- Keep project-specific paper facts, module names, variables, datasets, candidate descriptions, generated images, and audit outputs out of the reusable skill package; they belong in run outputs and cumulative checkpoints.
- Preserve UTF-8 exact text for fixed Chinese reply/origin strings.

## Patch reports

Historical `PATCH_REPORT_*.md` files are not runtime dependencies. A clean release package may delete most or all historical patch reports as long as the runtime rules are fully represented in `SKILL.md`, `references/`, `scripts/`, `CHANGELOG.md`, and release validation files.

Recommended release-retained files:

- `SKILL.md`
- `README.md`
- `CHANGELOG.md`
- `VERSION`
- `RELEASE_VALIDATION_v3.2.15b.md`
- `RELEASE_VALIDATION_v3.2.15b.json`
- `SKILL_CREATOR_PACKAGE_REPORT.md`
- `references/`, `scripts/`, `templates/`, `assets/`, and `agents/` as applicable

Development archives may retain patch reports for provenance, but production/release archives should avoid carrying long patch-history files unless specifically needed for debugging.
