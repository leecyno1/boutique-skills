# Video Autopilot Kit Review - 2026-08-05

## Source

- Repository: [Hao0321/video-autopilot-kit](https://github.com/Hao0321/video-autopilot-kit)
- Snapshot: `f081e99ed169b5aba1156a2aa6a80b748c39fbc9` (`v0.11.0`)
- Activity: 1,728 stars, 284 forks, latest code push 2026-07-28
- License: MIT
- Upstream format: runnable Python project, not a native Agent Skill

## Decision

**Import with a local Agent Skill wrapper. Score: 88/100, 4 stars.**

The project has enough executable depth and non-overlapping value to justify inclusion. Its strongest capability is an ffmpeg-first production and QA system for vertical Shorts, teaching long-form videos, and interview content. CapCut draft automation is a secondary, Windows-first path rather than the only way to use the kit.

| Dimension | Score | Reason |
|---|---:|---|
| Functional coverage | 19/20 | Shorts, long-form, interviews, CapCut draft operations, QA, competitor teardown, channel follow-up, and creator compliance. |
| Actionability | 18/20 | Runnable examples, setup templates, CLI entry points, and fail-closed gates; some workflows still require manual profile and plan filling. |
| Implementation and tests | 17/20 | 12,890 lines of Python, self-tests, import-sanity checks, and synthetic-media examples; full health exposed one undocumented libass dependency. |
| Portability and dependencies | 11/15 | Programmatic path supports Windows/macOS/Linux, but CapCut automation is Windows-first and subtitle builds need a libass-enabled ffmpeg. |
| Safety and provenance | 14/15 | MIT license, no bundled secrets or private data, no required API keys, subprocess argument arrays, explicit citation and compliance rules, and CapCut backups. |
| Uniqueness and maintenance | 9/10 | Distinct from Remotion promo-video skills and actively versioned, but overlaps lighter trimming, subtitle, and publishing tools. |

## Security Review

The executable surface uses local Python and ffmpeg/ffprobe. No production API endpoint, credential reader, shell-evaluated command, or required network service was found. Optional OCR packages are isolated and degrade cleanly when absent. File deletion is limited to generated temporary artifacts and test workspaces; draft editing has timestamped backup support.

Operational risks remain visible: scripts can create and move media files, CapCut draft JSON is version-sensitive, and user-provided output paths determine the write scope. The wrapper therefore requires a user-owned project root, preserves source media, and requires approval before CapCut draft changes.

## Verification

- Python compile check passed for `src/` and `examples/`.
- Quick system health passed all runnable checks and core-file checks.
- Zero-media examples for the Shorts gate, interview gate, and competitor teardown passed.
- Full system health passed 13 of 14 executable modules. `word_captions` failed because the installed Homebrew ffmpeg 8.1 lacks the `ass`/libass filter; the end-to-end vertical example failed at the same dependency boundary.
- The local skill wrapper turns the libass filter into an explicit preflight requirement rather than allowing a late render failure.

## Placement

Add to the high tier only. Do not add to the general standard bundle: its 2 MB source mirror and Python/ffmpeg/optional CapCut dependencies are appropriate for creators who need the complete workflow, not every installation.
