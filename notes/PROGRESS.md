# Progress Memory

Living project memory. Updated as work happens. Keep entries short and factual.
Source of truth for the plan is `study_plan.md`; this file tracks **actual state**.

Last updated: 2026-10-12

## How to use this file

- **Status** — where the project is right now.
- **Works** — verified, don't re-litigate.
- **Doesn't work / gotchas** — failed attempts and traps. Add the error, not just "didn't work".
- **Decisions** — choices made and why, so we don't churn.
- **Next** — the immediate queue.
- **Session log** — append-only; newest at top.

## Status

- Stage 1–3 in progress. Studies 02–06 done. Study 01 (calibration) is out of scope here.
- First reusable module extracted: `plotter_art.geometry.contours` (marching squares).
- Sketches are split by tool: `sketches/vsketch/` (vsketch, `.venv`) and
  `sketches/processing/` (py5, `.venv-py5`).
- Docs site (MkDocs Material) is live at https://kjjordans.github.io/GenArt/ with a Gallery.

## Works

- `.venv` (Python 3.13) with vsketch 1.2, vpype, matplotlib, pytest, ruff.
- `.venv-py5` with py5 0.10.11a0 and Java 21 (installed to `~/.jdk`).
- `pytest` baseline (`tests/test_smoke.py`) passes.
- Studies:
  - 02 Rosette — `sketches/vsketch/rosette/`
  - 03 Harmonograph — `sketches/vsketch/harmonograph/` (20k samples, smooth)
  - 04 Molnár squares — `sketches/vsketch/molnar_squares/` plus the py5 port in
    `sketches/processing/molnar_squares/`
  - 04b Molnár hexagons — `sketches/vsketch/molnar_hexagons/` (nested hexagons on an
    offset/honeycomb grid)
  - 05 Recursive subdivision — `sketches/vsketch/recursive_subdivision/` (angled BSP cuts
    with uneven stopping)
  - 06 Marching squares — `sketches/vsketch/marching_squares/`; reusable module
    `src/plotter_art/geometry/contours.py`
- `vsk save <sketch-dir> -d <output-dir>` produces a plot-ready SVG (vpype cleanup via the
  sketch's `finalize`). Vary a sketch's own `seed` Param with `--param seed N`;
  `-s/--seed` only seeds vsketch's built-in RNG, which this project's sketches don't use.
- Docs deploy automatically from `docs/**` via `.github/workflows/deploy.yml`.

## Doesn't work / gotchas

- `vsk.width` / `vsk.height` are always CSS pixels (793.7 x 1122.5 for A4) and are
  **not** affected by `vsk.scale("cm")`. Convert with `* 2.54 / 96` before using as cm.
- The vsketch viewer watches the sketch folder and locks it, so `git mv` of a running
  sketch's folder fails with "Permission denied". Stop the viewer first.
- `vsketch.Param` has no help/description field; the viewer shows only the name and unit.
- py5 `pixel_density(2)` warns "not available for this display" on many monitors.
- Windows environment variables set via `SetEnvironmentVariable` do not affect
  already-open terminals.

## Decisions

- Package/project name is `genart` (dir `GenArt`); import package is `plotter_art`.
- Millimetres are the project-level physical unit.
- "Start lightly": only add a module once two or more sketches need it. The grid/jitter
  extraction is deferred until a second sketch needs it.
- Randomness must come from an explicit seed; no hidden module-level random state.
- vsketch studies live in `sketches/vsketch/` (`.venv`); py5 studies live in
  `sketches/processing/` (`.venv-py5`).
- The on-screen canvas may be magnified for display; SVG export stays exact page size.
- Study 01 (plotter calibration) is out of scope for this environment; the user handles
  physical calibration and plotting separately.
- Recursive subdivision models panels as point lists (not rectangles) so cuts can be
  angled; a straight chord of a convex panel yields two convex panels, which keeps the
  inward-normal test simple.
- Deferred extracting the BSP/ray helpers into `src/plotter_art/` — only one sketch uses
  them so far.
- The rectilinear/angled BSP look isn't a keeper aesthetically; the study is committed for
  its reusable geometry, not as a finished piece.

## Next

1. Study 07 — streamline field (vector fields and integration).
2. Processing image track — load / greyscale / threshold / contours in py5.

## Session log

- **2026-10-12** — Study 06 marching squares: smooth scalar field + marching-squares
  contour extraction into `src/plotter_art/geometry/contours.py`; vsketch sketch with
  per-layer contour levels, seed control, and configurable grid resolution. 5 tests pass.
- **2026-10-09** — Study 05 recursive subdivision built (angled slices, uneven stopping)
  and committed; Molnár hexagons variant noted; `vsk save -s` vs `--param seed` gotcha
  documented; recursive-subdivision style parked (not a keeper).
- **2026-10-03** — Studies 02–04 built; py5 port + `py5-parameter-window` skill; repo
  split into `vsketch/` and `processing/`; docs Gallery live; harmonograph resampled.
  Notes refreshed.
- **2026-09-29** — Created this memory file. Inspected repo: scaffold + study plan only,
  studies not started. Ran `pytest` -> 2 passed.
