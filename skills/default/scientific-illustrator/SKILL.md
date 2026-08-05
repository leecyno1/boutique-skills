---
name: scientific-illustrator
description: Design, recreate, audit, and correct scientific figures as editable objects in draw.io Desktop, Microsoft PowerPoint, or WPS Presentation using the bundled Scientific Illustrator Codex plugin and local MCP servers. Trigger on Scientific Illustrator, drawio-scientific-illustrator, editable scientific illustration, reference-image reconstruction, graphical abstract, research workflow diagram, Draw.io figure, or editable PPTX figure. Use paper-framework-figure-studio-pro first when the user needs paper-grounded concept exploration rather than editable reconstruction.
license: MIT
metadata:
  upstream-version: "1.5.3"
---

# Scientific Illustrator

Use the directory containing this file as `<skill-root>`. The complete upstream
Codex plugin is mirrored here, including six specialist skills and three local
MCP servers.

## Preflight

1. Ask which backend the user wants: draw.io Desktop, Microsoft PowerPoint, or
   WPS Presentation.
2. Confirm that the selected desktop application is installed and open.
3. Check that the plugin and its MCP tools are available. Expected servers are
   `drawio-live`, `drawio-file-utils`, and `powerpoint-live`.
4. If those tools are unavailable, stop before editing and register this local
   mirror:

```bash
codex plugin marketplace add <skill-root>
codex plugin add scientific-illustrator@scientific-illustrator-tools
```

After registration, ask the user to restart Codex and start a new task. Do not
run the upstream network installer or modify certificate trust automatically.

## Route The Request

The plugin exposes these native skills under
`plugins/scientific-illustrator/skills/`:

| Request | Native skill |
|---|---|
| Design a new scientific figure from a brief | `design-scientific-figure` |
| Recreate a reference figure, backend-neutral | `recreate-scientific-figure` |
| Draw or recreate in live draw.io | `recreate-scientific-figure-in-drawio` |
| Draw or edit in PowerPoint or WPS | `edit-powerpoint-live` |
| Review structure, rendering, and editability | `audit-scientific-figure` |
| Turn review findings into object-level repairs | `correct-scientific-figure` |

Read the selected native `SKILL.md` before operating. Use its
Designer-Drawer-Reviewer-Corrector loop rather than improvising backend calls.

## Operating Rules

- Prefer editable text, shapes, connectors, tables, charts, groups, and native
  objects. Insert images only for irreducible raster regions such as microscopy
  fields or complex textures.
- Build and review one logical region at a time. Require fresh structural and
  rendered evidence after every correction and again for the complete figure.
- A successful MCP call is not proof of visual correctness.
- Preserve the user's source image and document. Save to an explicit target and
  keep a recoverable copy before modifying an existing presentation or diagram.
- Report the actual backend. COM and connected Office.js may edit a current
  PowerPoint window; OOXML and WPS paths may operate on an editable working copy.
  Never describe a dispatched open request as a verified live connection.
- Keep the selected application in the background unless the user requests
  foreground drawing.

## Related Skills

- Use `paper-framework-figure-studio-pro` for paper-grounded semantic extraction,
  candidate concepts, and a staged human decision workflow.
- Use this skill to turn a chosen design or reference into editable Draw.io or
  PPTX objects and run deterministic review/correction loops.
- Use `alphaear-logic-visualizer` for lightweight financial logic diagrams when
  a full desktop-plugin workflow is unnecessary.

## Completion Gate

Deliver only after the native Reviewer passes the whole figure. Report the
editable source path, exported preview path, backend and connection mode,
remaining source ambiguities, raster regions retained, and any unavailable
desktop-specific verification.
