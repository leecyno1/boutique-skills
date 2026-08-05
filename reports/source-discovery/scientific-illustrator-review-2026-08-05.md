# Scientific Illustrator Review - 2026-08-05

## Source

- Requested repository: [icebird1998/drawio-scientific-illustrator](https://github.com/icebird1998/drawio-scientific-illustrator)
- Current upstream: [icebird1998/scientific-illustrator](https://github.com/icebird1998/scientific-illustrator)
- Snapshot: `e0d2a44ad8a686cf5859f286d78df4879ff86c30` (`v1.5.3`)
- Popularity at review: legacy repository 1,269 stars and 89 forks; successor 371 stars and 30 forks
- License: MIT

The requested project is real, but its author marks it as superseded. The imported source is the actively maintained integrated successor; the old name is retained as a trigger alias and migration record.

## Decision

**Import the successor plugin. Score: 93/100, 5 stars.**

| Dimension | Score | Reason |
|---|---:|---|
| Functional coverage | 20/20 | Six native skills cover design, reference reconstruction, Draw.io and presentation drawing, structural/visual review, and object-level correction. |
| Actionability | 18/20 | The plugin ships 69 Draw.io/PowerPoint/WPS tools and explicit region-by-region workflows; first use still requires plugin registration and a desktop application. |
| Implementation and tests | 19/20 | Repository validation and all MCP/platform smoke tests pass, with Ubuntu, macOS, and Windows CI definitions. Commercial Office/WPS behavior still needs real-host verification. |
| Portability and dependencies | 13/15 | Supports Windows and macOS across Draw.io, PowerPoint, and WPS, but depends on Node.js, local MCP registration, and desktop software. |
| Safety and provenance | 14/15 | MIT, local-only bridges, no telemetry, random Office.js session token, no automatic certificate trust, and argument-array subprocesses. Document write capability remains medium risk. |
| Uniqueness and maintenance | 9/10 | Editable reconstruction and deterministic correction are distinct from image-only figure generation; the successor is versioned and explicitly replaces the popular legacy project. |

## Capability Review

The plugin implements one Designer-Drawer-Reviewer-Corrector protocol across three applications. It preserves editable text, shapes, connectors, tables, charts, grouping, and z-order, while requiring broad raster crops to be decomposed into atomic image regions plus editable overlays. Each completed region and the final figure receive both a structure audit and a rendered-image review.

The PowerPoint route distinguishes COM, connected Office.js, and OOXML fallback instead of claiming every file operation controls the foreground document. WPS likewise reports dispatched-open, verified-open, and refresh states separately. Draw.io rejects unknown shapes instead of silently replacing them with rectangles.

## Security Review

All three MCP servers run locally. Draw.io debugging and the Office.js bridge bind to `127.0.0.1`; the latter requires a random session token. The setup process generates a localhost certificate but leaves trust decisions to the user. JavaScript launch points use `execFile` or argument arrays, and no shell-string execution, telemetry, credential collection, or remote production API was found.

The remaining risk is operational: the plugin can create, update, delete, and save objects in Draw.io and presentation files. The local wrapper therefore requires an explicit backend, source preservation, truthful connection-state reporting, and a review gate before delivery.

## Verification

`npm test` passed the repository validator and all smoke suites:

- Draw.io live MCP: 26 tools
- Draw.io file utilities: 9 tools
- PowerPoint/WPS MCP: 34 tools
- Office.js HTTPS bridge and session handling
- Cross-platform focus policy and path discovery
- WPS state/refresh reliability
- Enabled Ubuntu, macOS, and Windows CI jobs

## Overlap And Placement

This skill does not replace `paper-framework-figure-studio-pro`. That skill extracts paper semantics and explores candidate figure concepts; Scientific Illustrator reconstructs or implements a selected concept as editable Draw.io/PPTX objects. `alphaear-logic-visualizer` remains the lighter route for simple financial diagrams.

Add to the high tier only. Do not add to the general standard bundle because every useful route requires local MCP registration plus Draw.io, PowerPoint, or WPS. The specialist value is high, but the dependency footprint is inappropriate for a default no-duplicate installation.
