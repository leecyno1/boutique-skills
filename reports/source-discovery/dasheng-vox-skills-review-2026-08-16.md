# Dasheng VOX Skills Review - 2026-08-16

## Scope

The referenced Codex task most recently introduced two media-production Skills that were not already present in this catalog:

- `dasheng-vox-skills`
- `dasheng-video-omni-browser`

`video-shotcraft`, `frontend-design`, and `dasheng-video-director` were already cataloged and were not duplicated. General coding helpers mentioned in the task were not imported as media workflow output.

## Decision

**Import both into the high-tier Dasheng media suite.**

| Skill | Score | Stars | Decision |
|---|---:|---:|---|
| `dasheng-vox-skills` | 90/100 | 5 | Import as the primary VOX orchestration layer |
| `dasheng-video-omni-browser` | 82/100 | 4 | Import as an optional browser executor |

## dasheng-vox-skills

| Dimension | Score | Reason |
|---|---:|---|
| Workflow coverage | 19/20 | Covers script rewriting, storyboard approval, shot routing, generation, Remotion handoff, subtitles, and QC. |
| Implementation depth | 19/20 | Includes a resumable manifest, attempt history, Gemini API client, Shotcraft adapter, and ffmpeg-based shot inspection. |
| Quality and evidence controls | 19/20 | Separates real evidence and deterministic local motion from generated B-roll; approval gates are explicit. |
| Portability | 15/20 | Core files are bundled and Shotcraft discovery was adapted for installed siblings; the full director CLI and final Remotion project still live in the source media repository. |
| Safety and provenance | 10/10 | MIT source, no bundled secrets, official Google API route, Google-host validation before forwarding the API key, no third-party aggregator, and generated media stays outside the Skill. |
| Maintenance value | 8/10 | Strong integration value with existing `video-shotcraft`; latest source changes were still in a local working tree at review time. |

**Total: 90/100.**

## dasheng-video-omni-browser

| Dimension | Score | Reason |
|---|---:|---|
| Functional value | 18/20 | Provides a practical fallback when Gemini API access is unavailable. |
| Actionability | 17/20 | Bundled packet builder creates per-shot prompts, paths, and status records. |
| Reliability | 13/20 | Depends on a signed-in Chrome session and changing Gemini web UI; CAPTCHA requires user action. |
| Quality controls | 17/20 | Clear reference-frame contract and opening/middle/final-frame rejection rules. |
| Safety and privacy | 10/10 | Explicitly forbids reading cookies, local storage, passwords, or profile files. |
| Portability and maintenance | 7/10 | Browser automation is environment-specific and has no stable API contract. |

**Total: 82/100.**

## Verification

- All five bundled Python files compile with Python 3.14.
- Standard-library smoke tests covered Omni packet creation and refresh, mixed Shotcraft/Gemini Manifest routing, attempt recording and resume, Gemini dry-run routing, and Shotcraft catalog discovery.
- The source repository's pytest suite could not run because `pytest` is not installed in the active Python environment.
- Live Gemini generation and signed-in Chrome download were not executed because they consume external service quota and depend on the user's active account session.

## Import Notes

- Runtime media and `__pycache__` were excluded.
- `director-workflow.md` and `visual-grammar.md` were bundled so the orchestration Skill retains its content and visual gates without requiring `dasheng-video-vox`.
- The optional full director CLI remains an external capability of the source media project and the existing `dasheng-video-director` Skill.
