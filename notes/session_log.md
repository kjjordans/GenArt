# Session Log

## 2026-09-26

### Completed
- Project review and architecture overview
- Created AGENTS.md with conventions
- Installed vsketch (1.2.0) and vpype (1.15.0) via pipx
- Set up `.venv` with `pip install -e ".[dev]"`
- Created `.python-version` (3.11.15)
- **Hello World sketch** — circle + cross through center
- **Study 02: Rosette** — working multi-layer parametric rose curve with sliders for amplitude, frequency, phase, layers, layer_scale, layer_rotation
- Learned: `vsk.translate()`, `vsk.scale("mm")`, `vsk.line()`, separating geometry functions from drawing code

### Preferences
- **Code style:** Keep code readable by an intermediate programmer. Avoid premature abstraction and clever patterns unless they add clear utility.

---

## 2026-09-30

### Completed
- Added code style preference to AGENTS.md and session log
- **Study 03: Harmonograph** — dual-pendulum damped harmonograph with frequency, phase, amplitude, damping, sample count, and dt parameters
  - Removed no-op `1.0 *` factors
  - Phases converted to degrees with `math.radians()`
  - Removed `reloop` from finalize (harmless but unnecessary for open spiral)
  - Ruff clean
- Decided against extracting `sample_parametric` helper — not enough utility yet (preference: no premature abstraction)

### Pending for next session
- **Study 04: Disturbed grid** (Vera Molnár–style)
  - Grid of squares with seeded jitter (position, rotation, scale)
  - Finalize shape choice (square/circle/diamond)
  - Decide whether to start with position-only jitter or all three

---

## 2026-10-03

### Completed
- **Study 04: Molnár squares** (`sketches/vsketch/molnar_squares/`)
  - Grid of concentric squares with seeded, bell-weighted disorder peaking at a focus point
  - Per-ring off-register jitter, random layers, omission chance
  - Size jitter now scales the whole nested block per cell, so every ring reacts
  - Defaults tuned toward *(Dés)Ordres* (subtle disorder)
  - Plot-ready SVG via `vsk save sketches/vsketch/molnar_squares -s 42`
- **py5 (Processing) port** (`sketches/processing/molnar_squares/`) — Tkinter parameter
  window, dark canvas, mouse-drag focus, scroll spread, exact-A4 SVG export
- **Skill** `py5-parameter-window` capturing the py5 + Tkinter pattern
- **Repo reorg** — sketches split into `sketches/vsketch/` and `sketches/processing/`
- **Docs** — `docs/Gallery/` grid-card gallery; live at https://kjjordans.github.io/GenArt/
- **Harmonograph** resampled to 20k points for smooth curves

### Decisions
- Deferred extracting grid/jitter helpers into `src/plotter_art/` — only one sketch uses
  them; wait for a second (per "no premature abstraction")
- vsketch studies run in `.venv`; py5 studies in `.venv-py5`
- The focus is a page fraction so the mouse maps directly; display magnification is
  display-only and the export stays exact page size

## 2026-10-12

### Completed
- **Study 06: Marching squares** (`sketches/vsketch/marching_squares/`)
  - Smooth scalar field built from seeded random sine waves (no extra dependencies)
  - Classic marching-squares algorithm with linear edge interpolation
  - Ambiguous saddle cases resolved via cell-centre average
  - Extracted into reusable `src/plotter_art/geometry/contours.py`
  - Sketch parameters: grid cols/rows, number of contour levels, seed, field scale, margin
  - Contours drawn on separate vsketch layers for multi-pen plotting
  - 5 tests pass (3 new + 2 smoke); ruff clean

### Decisions
- Extraction justified: Study 06 explicitly calls for "Scalar field + contours" as a
  reusable module. Kept API minimal: one function, plain types.
- Field generator stays in the sketch (not extracted) — only one sketch uses it and
  sum-of-sines is easy to re-implement for different aesthetics.

### Pending
- Study 05 — recursive subdivision
- Study 07 — streamline field
- Processing image track (Stage 4–5)
