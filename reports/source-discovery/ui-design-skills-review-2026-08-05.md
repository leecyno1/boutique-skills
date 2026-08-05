# UI Design Skills Review - 2026-08-05

Source note: [How to improve an AI coding assistant's UI design taste](https://www.xiaohongshu.com/explore/6a69f62f0000000010026597)

The note points to two first-party GitHub projects. Both have explicit redistribution licenses and both were already represented in the repository, so this review avoids duplicate skill IDs and refreshes the one stale mirror.

| Project | Upstream snapshot | License | Score | Decision |
|---|---|---|---:|---|
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | `e988add20dab0fa97d7a76781c48961c8184288e` | MIT | 92/100, 5 stars | Keep the existing full multi-skill mirror; no duplicate import and no upstream delta. |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `ae5e95101a6979e7f7973a4ff57680b3c7adc1ec` | Apache-2.0 | 92/100, 5 stars | Keep and refresh `impeccable` from the latest upstream skill bundle. |

## Taste Skill

Taste Skill is strongest as an anti-template design rulebook. Its pack covers frontend taste, redesign, visual styles, image-to-code, brand systems, and output discipline. It is portable and low-risk because the core skills are instruction-driven and can run offline.

Its main limitation is fragmentation: the pack contains several overlapping style and compatibility skills, and it provides less executable design-system machinery than Impeccable. It remains valuable when a task needs a fast aesthetic correction or a specific visual vocabulary.

Score basis: design judgment 19/20, actionability 17/20, implementation completeness 17/20, portability 15/15, operational safety 15/15, uniqueness and maintenance 9/10.

## Impeccable

Impeccable is the stronger end-to-end design engineering workflow. It routes work across critique, audit, layout, typography, motion, responsive adaptation, hardening, design-system extraction, and live browser iteration. The mirrored bundle includes executable detectors and framework-aware edit flows rather than prompt guidance alone.

The 2026-08-04 upstream update materially improves the mirror:

- reduces false positives in JavaScript, JSX, and CSS-in-JS comment handling;
- expands DESIGN.md parsing for layout and shape decisions;
- adds `.blade.php` scanning;
- checks project and symlink boundaries before scanning files;
- centralizes cross-platform browser launching;
- improves hook lifecycle management and native browser-surface checks.

The main tradeoff is operational scope. Some commands open a local browser, run a loopback server, edit project files, or start child processes. Optional image generation uses `OPENAI_API_KEY`, and concept selection may contact `impeccable.style`; these are visible feature paths rather than hidden install behavior. Local servers bind to `127.0.0.1`, and the new path-boundary checks improve safety.

Score basis: workflow depth 20/20, actionability 20/20, implementation and test quality 19/20, platform compatibility 13/15, operational safety 11/15, uniqueness and maintenance 9/10.

## Recommendation

Keep both because their best uses are different: use Taste Skill for concise aesthetic rules and anti-slop correction; use Impeccable for a complete review-to-implementation workflow. Impeccable is the preferred default when only one comprehensive UI design skill should be selected.

## Verification

- Codex Agent Skill validation passed after moving upstream extension fields under standard `metadata`.
- The repository audit resolved all 353 auditable skills with no missing skills, missing origins, duplicate capabilities, or standard-bundle issues.
- Repository tests passed: 7/7.
- Impeccable upstream core and detector suites passed after pointing Puppeteer at the installed system Chrome; the browser detector group passed 121/121.
- Standard and high-tier installation dry runs completed successfully.
