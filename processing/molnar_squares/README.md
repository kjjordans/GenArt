# Molnár Squares — py5 (Processing) port

An interactive port of `sketches/molnar_squares/` to [py5](https://py5coding.org/)
(Processing for Python 3). A grid of squares with concentric rings and seeded,
focus-weighted disorder.

## Setup

py5 needs **Java 17+** and lives in its own virtual environment so its
`numpy`/`pillow` requirements can't disturb the main vsketch/vpype toolchain.

From the repository root:

```powershell
python -m venv .venv-py5
.venv-py5\Scripts\python -m pip install -r processing\requirements.txt
.venv-py5\Scripts\python -c "import jdk; print(jdk.install('21'))"
```

Java is installed to `~/.jdk`, which py5 detects automatically. You only need
this once.

## Run

```powershell
.venv-py5\Scripts\python processing\molnar_squares\molnar_squares.py
```

## Controls

A **parameter window** (Tkinter) opens alongside the sketch with a slider for
each value: columns, rows, rings, layers, margin, padding, ring scale, jitter
position/angle/scale, spread, and omit. It also has **Random seed** and
**Export SVG** buttons. Changes apply live.

| Input | Action |
| --- | --- |
| Left-drag (sketch) | Move the bell focus point (peak disorder) |
| Scroll wheel (sketch) | Widen / narrow the bell spread |
| `R` | New random seed |
| `S` | Export `output/molnar_<seed>.svg` |
| `O` | Toggle omission (0 ↔ 0.2) |

Closing the parameter window ends the program.

## Notes

- The sketch is drawn in **millimetres** at A4. The window shows it magnified
  (`VIEW_SCALE = 2.5`), while `S` writes an **exact A4 SVG** (real page size) via
  an offscreen renderer, so the export is plot-accurate.
- Layers are mapped to stroke colours for on-screen preview; for multi-pen
  plotting you would split the SVG by colour/layer in your pipeline.
- Jitter is re-seeded every frame, so squares stay put while the focus moves;
  only the amount of jitter changes.
