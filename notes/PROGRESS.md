# Progress Memory

Living project memory. Updated as work happens. Keep entries short and factual.
Source of truth for the plan is `study_plan.md`; this file tracks **actual state**.

Last updated: 2026-10-03

## How to use this file

- **Status** — where the project is right now.
- **Works** — verified, don't re-litigate.
- **Doesn't work / gotchas** — failed attempts and traps. Add the error, not just "didn't work".
- **Decisions** — choices made and why, so we don't churn.
- **Next** — the immediate queue.
- **Session log** — append-only; newest at top.

## Status

- Stage 1–2 in progress. Studies 02, 03, 04 done. Study 01 (calibration) is out of scope here.
- `src/plotter_art/**` is still empty (`__init__.py` only) — extraction deliberately deferred.
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
- `vsk save <sketch-dir> -s <seed> -d <output-dir>` produces a plot-ready SVG
  (vpype cleanup via the sketch's `finalize`).
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

## Next

1. Study 05 — recursive subdivision (BSP/quadtree).
2. Processing image track — load / greyscale / threshold / contours in py5.

## Session log

- **2026-10-03** — Studies 02–04 built; py5 port + `py5-parameter-window` skill; repo
  split into `vsketch/` and `processing/`; docs Gallery live; harmonograph resampled.
  Notes refreshed.
- **2026-09-29** — Created this memory file. Inspected repo: scaffold + study plan only,
  studies not started. Ran `pytest` -> 2 passed.
