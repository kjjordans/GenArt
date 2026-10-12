# Session Log

## 2026-10-09

### Completed
- **Study 05: Recursive subdivision** (`sketches/vsketch/recursive_subdivision/`)
  - Panels modelled as point lists so cuts can be angled; each slice runs from the
    longest edge into the panel at up to `max_tilt` degrees off perpendicular
  - `exit_point()` ray test locates where the cut leaves the panel
  - `stop_chance` lets sibling branches finish at different depths; `min_size` guards the
    longest edge
  - Moved the WIP from `sketches/recursive_subdivision/` into `sketches/vsketch/`
  - Committed as `0cd89b7`
- **Molnár hexagons** — nested-hexagon variant on an offset grid
  (`sketches/vsketch/molnar_hexagons/`)

### Decisions
- The rectilinear/angled BSP look isn't a keeper aesthetically; the study is kept for its
  reusable BSP + ray geometry, not as a finished piece
- Vary a sketch's own `seed` with `--param seed N`; `vsk save -s` only seeds vsketch's RNG
- p5.js hello-world left untracked as scratch; revisit only if p5js art makes sense

### Pending
- Next study: noise contour map (Stage 3) or the image track (Stage 4–5)

---

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

---

## 2026-10-12 (cont.)

### Completed
- **py5 Support Library** (`src/plotter_art/py5_support/`)
  - `PaperSpace` — physical page model with ISO A-series presets (A0–A6), portrait/landscape,
    custom sizes in mm or cm, `cm()` conversion helper
  - `Viewport` — screen preview fitting: page↔pixel transforms, page outline drawing,
    preserves aspect ratio with configurable margins
  - `ImageLayer` — raster image aligned to PaperSpace with `contain`/`cover`/`stretch` fit,
    bilinear/nearest pixel sampling in page mm coordinates, py5 preview rendering
  - `ParameterState` + `ParamDef` — typed parameter definitions, live slider state
  - `build_controls()` — Tkinter slider window with value labels and action buttons
  - `SVGExporter` / `export_sketch()` — plotter-ready SVG with mm dimensions and viewBox,
    raster images excluded by default
  - `run_sketch()` — two-window launcher: py5 canvas + Tkinter controls, clean lifecycle
  - Lazy py5 imports in `__init__` so the package imports without py5 installed
  - Tests: 33 passing (paperspace, viewport, controls)
  - **Refactored py5 Hello World** (`sketches/py5/py5_hello_world/`) to use the library
    demonstrating `ParameterState`, `PaperSpace`, `Viewport`, and `export_sketch()`
  - Fixed `run_sketch()` callback registration: explicitly pass py5 `settings`/`setup`/`draw`
    functions so the canvas uses its configured 900×700 size and the user draw callback runs
  - Removed background fill from shared artwork/export callback so SVG contains only artwork
  - Verified a py5 callback smoke test opens a 900×700 preview; Ruff clean, 33 tests pass
- **Minimal py5 example** (`sketches/py5/minimal_example/minimal_example.py`)
  - One PaperSpace, one radius slider, and one mm-based circle draw callback
  - Ruff and Python compile checks pass
- **py5 sketch template** (`sketches/py5/sketch_template.py`)
  - Copyable starter with KEEP/CUSTOMIZE/OPTIONAL blocks, one example slider,
    viewport-based mm drawing, shared launcher, and optional SVG export button
  - Ruff and Python compile checks pass
- Moved SVG save-dialog/button callback into `make_svg_export_callback()` in
  `plotter_art.py5_support.svg_export`; template now declares the button using the helper

### Decisions
- Library stays small and needs-driven: add features only when a sketch needs them
- py5 and vsketch environments remain separate (`.venv` / `.venv-py5`) to avoid dependency conflicts
- `genart` package installed editable (`pip install -e . --no-deps`) in `.venv-py5` so sketches
  can import `plotter_art` modules without manual path hacks

### Pending
- Image-processing/marching-squares sketch using `ImageLayer` to verify image↔geometry alignment
- Additional paper presets beyond ISO A series if needed
- Processing image track (Stage 4–5)
