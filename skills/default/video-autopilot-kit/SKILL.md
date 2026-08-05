---
name: video-autopilot-kit
description: Build, inspect, quality-gate, and operate YouTube and short-form video pipelines with the bundled Video Autopilot Kit. Use for ffmpeg-first vertical Shorts/Reels, teaching long-form videos, CapCut draft JSON automation, subtitle and B-roll alignment, delivery QA, competitor-video teardown, interview-show packages, channel D2/D7/D28 tracking, or AI creator-compliance checks. Trigger on Video Autopilot Kit, CapCut JSON, shorts_autopilot, vertical teardown, or video delivery QA. Not for cinematic Remotion product promos; use video-shotcraft for those.
license: MIT
metadata:
  upstream-version: "0.11.0"
---

# Video Autopilot Kit

Use the directory containing this `SKILL.md` as `<skill-root>`. The bundled
upstream project is self-contained under that directory; invoke scripts with
absolute paths so the user's working directory remains their project.

## Operating Rules

1. Default to the programmatic ffmpeg path. Use the CapCut-assisted path only
   when the user explicitly needs CapCut effects, templates, or draft editing.
2. Never use `<skill-root>` as the user's project or media workspace. Set
   `VIDEO_KIT_PROJECT_ROOT` and the relevant input/output variables to paths in
   the user's project.
3. Preserve source media. Write normalized clips, plans, reports, and renders to
   separate work/output directories. Do not overwrite a CapCut draft without a
   timestamped backup and explicit user approval.
4. Treat shipped duration, caption, pacing, and KPI thresholds as calibration
   examples. Recalculate them from 3-5 representative videos before using them
   as hard production gates.
5. Captions, prices, names, addresses, performance claims, and guest metrics
   must come from visible frames or cited evidence. Do not invent unreadable or
   missing facts.
6. Do not describe a render as deliverable until ffprobe checks, the relevant
   quality gates, and a visual frame review all pass.

## Preflight

Run before the first operation in a project:

```bash
python3 <skill-root>/src/system_health.py --quick
command -v ffmpeg
command -v ffprobe
ffmpeg -hide_banner -filters 2>/dev/null | rg '(^| )ass( |$)'
```

Requirements:

- Core gates and interview planning: Python 3.9+.
- Programmatic video builds: `ffmpeg` and `ffprobe`.
- Subtitle burning: an ffmpeg build with the `ass`/libass filter. Stop and tell
  the user when the filter check is empty; do not silently ship without captions.
- `shorts_autopilot.py`: Pillow and NumPy.
- Competitor-caption OCR: optional `rapidocr-onnxruntime` and
  `opencc-python-reimplemented`. Without them, rhythm analysis still works.
- CapCut draft automation: Windows-first and version-sensitive. Read
  `TROUBLESHOOTING.md` before touching a draft.

No API key is required by the bundled tools.

## Route the Request

| Request | Route | Read first |
|---|---|---|
| Turn clips into Shorts/Reels | `src/shorts_autopilot.py` | `SETUP.md`, `knowledge/shorts-mastery-2026.md` |
| Validate a short before publishing | `src/longform_maker/shorts_gate.py` | `knowledge/shorts-mastery-2026.md` |
| Build teaching long-form video | `src/longform_maker/` | `knowledge/programmatic-video-build.md`, `knowledge/premium-motion-fx.md` |
| Edit or audit CapCut drafts | `src/capcut_helpers/` | `knowledge/capcut-automation-sop.md`, `TROUBLESHOOTING.md` |
| Check a finished export | `src/capcut_helpers/delivery_qa.py` | `knowledge/video-craft-playbook.md` |
| Analyze competitor vertical videos | `src/teardown.py` | `knowledge/vertical-teardown-method.md` |
| Prepare an interview series | `src/interview_autopilot.py` | `knowledge/interview-show-playbook.md` |
| Review channel follow-ups | `src/channel_tracker.py` | `knowledge/ops-automation.md` |
| Review AI-content policy exposure | knowledge workflow | `knowledge/ai-content-compliance.md` and its sources appendix |

Use `video-shotcraft` instead when the request is specifically a cinematic
product promo based on real product screenshots and Remotion shot recipes. Use
a lightweight trimming/subtitle skill for a single simple edit that does not
need this kit's planning, gates, or operational layer.

## Vertical Shorts Workflow

1. Create a user-owned project and fill the relevant templates from `SETUP.md`.
2. Set explicit paths:

```bash
export VIDEO_KIT_PROJECT_ROOT="/absolute/path/to/project"
export VIDEO_KIT_SHORTS_INBOX="$VIDEO_KIT_PROJECT_ROOT/videos/_INBOX/shorts"
export VIDEO_KIT_BGM_ROOT="$VIDEO_KIT_PROJECT_ROOT/assets/bgm"
```

3. Put source clips in `<inbox>/<folder-id>/` and scan:

```bash
python3 <skill-root>/src/shorts_autopilot.py scan <folder-id> --platform yt_shorts
```

4. Inspect `_work/SHEET.jpg` and `_work/_signs/`. Fill the generated `_plan.py`
   only with facts visible in those frames. Remove every `TODO`.
5. Build with the platform already recorded in the plan:

```bash
python3 <skill-root>/src/shorts_autopilot.py build <folder-id>
```

6. Review the generated report and QA frames. Re-run the shorts gate with the
   user's calibrated rules when shipped defaults are not representative.

Supported platform bands are `yt_shorts`, `ig_reels`, and `fb_reels`.

## Competitor Teardown

Run the tool on one video or a folder:

```bash
python3 <skill-root>/src/teardown.py /path/to/video-or-folder --band wide --thresh 0.25
```

Before interpreting results, manually count cuts in a 10-second sample and
calibrate `--thresh`. Report cut rate, gap median and spread, caption-change
rate, captions-to-cuts ratio, and loudness as observations, not causal claims.
Treat OCR text as provisional; it is unreliable for signs, prices, and product
names even when confidence appears high.

## Interview Workflow

The sequence is `invite -> plan -> build`:

```bash
python3 <skill-root>/src/interview_autopilot.py invite 01 --name "Guest" --hint "Verified achievement"
python3 <skill-root>/src/interview_autopilot.py plan 01
python3 <skill-root>/src/interview_autopilot.py build 01 --compliance-ok
```

Do not pass `--compliance-ok` on the user's behalf. It is a human sign-off after
the platform AI-content checklist has actually been reviewed. Guest metrics
without a source must remain blocked by `interview_gate.py`.

## CapCut Safety

- Confirm the installed CapCut version against `TROUBLESHOOTING.md`.
- Close CapCut before direct draft JSON edits.
- Resolve draft paths through `src/capcut_helpers/paths.py`; do not hard-code a
  Windows username or assume macOS automation support.
- Use `draft_io.py` backup behavior and retain the backup until the edited draft
  opens and exports successfully.
- Prefer programmatic QA modules even when the edit itself used CapCut.

## Completion Gate

Before handoff, report:

- output path, dimensions, frame rate, duration, codecs, and file size;
- which mechanical gates passed, warned, or were unavailable;
- caption/libass status and any optional dependency skipped;
- visual checks from representative beginning, middle, ending, and transition
  frames;
- calibrated assumptions that still need real-channel data;
- source-media and CapCut-backup preservation status.

Warnings are not failures, but they must remain visible. A missing required
check is not a pass.
