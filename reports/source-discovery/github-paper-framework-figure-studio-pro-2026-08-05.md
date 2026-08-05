# GitHub Skill Review: Paper Framework Figure Studio Pro

- Review date: 2026-08-05
- Upstream: https://github.com/c-narcissus/paper-framework-figure-studio-pro
- Upstream snapshot: `77557418b4ca8c24fa8961206bf9b8f7f6d030e1`
- Popularity at review: 1,812 stars and 104 forks
- Imported version: `v3.2.15c`
- Upstream latest package: `v3.2.15f`
- License: MIT-0 inside both release packages and declared in the README; the repository root does not expose a standalone license file, so GitHub license metadata is empty.

## What It Does

`paper-framework-figure-studio-pro` turns a research paper into publication-oriented framework, architecture, pipeline, method-overview, system/data-flow, or mechanism figure candidates. Its S0-S5 workflow separates paper-grounded semantic extraction, figure strategy, first-round image exploration, human direction selection, formal candidate preparation, and terminal image generation.

The strongest parts are source-faithful node and edge contracts, symbol disambiguation, prompt audits before image generation, candidate lineage, preference carryover, and cumulative checkpoint recovery. It also includes a large computer-science visual vocabulary with reusable SVG assets and deterministic Python guards.

## Compatibility Decision

The imported package is `v3.2.15c`, not the current `v3.2.15f` package. The upstream README explicitly limits `v3.2.15f` to ChatGPT Web because S5 depends on using S2 images as reference inputs. The repository is intended to support general coding agents, and `v3.2.15c` retains the documented Codex route.

## Security And Quality Review

- Python sources compile successfully.
- No network clients, credential collection, shell execution, or arbitrary `eval`/`exec` calls were found.
- The one subprocess call invokes a sibling checkpoint-repair script with the current Python interpreter.
- Cleanup commands delete only paths resolved through the run-directory safe-path helper. They remain a medium operational risk because rewind and artifact-reset operations intentionally remove generated run artifacts.
- The upstream ZIP had an unreadable directory permission bit; the mirror normalizes permissions.
- Tabler (MIT) and Lucide (ISC/MIT) icon provenance is present in individual asset records; the mirror adds a consolidated third-party notice.
- Paper-derived motif records are treated as abstract design references, not permission to reproduce source-paper artwork.
- Both `v3.2.15c` and `v3.2.15f` ship an unreferenced `figure_studio_checkpoint_integrity.py` that imports four nonexistent symbols. It is omitted; the active state/checkpoint workflow already contains cumulative-integrity guards.
- The version-locked release architecture audit is also omitted because it expects `v3.2.15b` metadata and publishing files rather than runtime artifacts.
- The 50 KB, 373-line controller is below the 500-line structural ceiling but remains context-heavy.
- Fixed reply suffixes and an exact dedication block are unrelated to figure correctness and can intrude on normal assistant conversation.

## Overlap Review

The skill overlaps partially with `baoyu-infographic`, `canvas-design`, `alphaear-logic-visualizer`, and presentation tooling. It remains distinct because it focuses narrowly on paper-grounded method/framework figures, evidence-backed connector semantics, staged image candidates, and resumable checkpoint governance.

## Decision

**Import: yes. Standard bundle: no.**

It is a strong specialist skill for researchers and technical authors, but it is too domain-specific, context-heavy, slow, and image-route-sensitive for the general no-duplicate standard bundle. It belongs in the high tier as an optional research-figure tool.

Editorial capability assessment: **84/100, 4 stars**. The repository's generic automated registry score is **79/100, 4 stars** because this is an L3 specialist with medium operational risk. Main deductions are the oversized controller, conversational side effects, root-license metadata gap, and split compatibility between Codex and ChatGPT Web.
