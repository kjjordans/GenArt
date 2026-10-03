---
name: py5 Parameter Window
description: Build interactive py5 (Processing for Python) sketches that pair the canvas with a separate Tkinter parameter window, a dark styled canvas with thin lines, mouse-driven controls, and exact-size SVG export for plotting. Use when creating or extending a py5/Processing sketch that needs live parameter tweaking, mouse interaction, custom styling, or plotter-ready SVG output.
---

# py5 Parameter Window

## What this covers

A repeatable pattern for a py5 sketch with:

- a separate Tkinter window of sliders and buttons that drives the sketch live,
- mouse interaction in the sketch canvas (drag, wheel),
- custom styling (dark background, thin light strokes on screen; dark strokes in the SVG),
- exact-size SVG export, independent of the on-screen magnification.

Full working example: `sketches/processing/molnar_squares/molnar_squares.py`.

## Environment (once per machine/project)

py5 needs Python 3.10+ and Java 17+ (prefer 21). Keep it in its own venv so its
`numpy>=2.2` / `pillow>=11` requirements cannot disturb other toolchains:

```sh
python -m venv .venv-py5
.venv-py5/Scripts/pip install py5 install-jdk
.venv-py5/Scripts/python -c "import jdk; print(jdk.install('21'))"
```

On non-Windows use `bin/pip` and `bin/python`. Java lands in `~/.jdk`, which py5
detects automatically. Importing `py5` starts the JVM but opens no window;
`py5.run_sketch()` opens the window.

## The two-window pattern

py5/Processing has no built-in parameter panel. Run the sketch non-blocking and
let Tkinter own the main thread:

```python
if __name__ == "__main__":
    py5.run_sketch(block=False)   # sketch runs on its own animation thread
    build_controls().mainloop()   # Tkinter owns the main thread
    py5.exit_sketch()
```

Closing the Tkinter window ends the program.

## Parameter window

Put `PARAMS` and `build_controls()` in the **same module as the sketch globals**
so the callbacks can write them:

```python
# (global name, label, min, max, step, is_int)
PARAMS = [("N_COLS", "Columns", 1, 12, 1, True), ("SPREAD", "Spread", 0.05, 2.0, 0.05, False)]


def build_controls():
    import tkinter as tk

    root = tk.Tk()
    root.title("Parameters")
    for name, label, lo, hi, step, is_int in PARAMS:
        row = tk.Frame(root)
        row.pack(fill="x", padx=8, pady=1)
        tk.Label(row, text=label, width=12, anchor="w").pack(side="left")
        value_label = tk.Label(row, width=6, anchor="e")

        def on_change(val, n=name, i=is_int, vl=value_label):
            value = round(float(val)) if i else round(float(val), 3)
            globals()[n] = value
            vl.config(text=f"{value:g}")

        scale = tk.Scale(row, from_=lo, to=hi, resolution=step, orient="horizontal",
                         showvalue=False, command=on_change, length=200)
        scale.set(globals()[name])
        scale.pack(side="left", fill="x", expand=True)
        value_label.config(text=f"{globals()[name]:g}")
        value_label.pack(side="right")
    return root
```

Key points:

- The callback's default arguments (`n=name`, `i=is_int`, `vl=value_label`) capture
  the per-slider values in the loop. Without them, every slider writes the last name.
- `round(float(val))` already returns an int; do not wrap it in `int()` (ruff RUF046).
- Sliders write module globals; the sketch reads them each frame, so updates are live.
- Re-seed the RNG every frame so jitter stays stable while values change.
- A slider cannot track mouse/wheel-driven changes without thread-unsafe cross-window
  updates; let the last input win.

## Mouse interaction

Register top-level functions named exactly `mouse_pressed`, `mouse_dragged`,
`mouse_wheel`, `key_pressed`.

```python
def mouse_pressed(): _set_focus()
def mouse_dragged(): _set_focus()


def mouse_wheel(event):
    global SPREAD
    count = event.get_count()   # +1 wheel down, -1 wheel up
    if count:
        SPREAD = min(max(SPREAD * 1.1**count, 0.05), 2.0)
```

## Coordinate mapping (common bug)

`py5.mouse_x` / `py5.mouse_y` are window pixels. If the page is magnified by
`VIEW_SCALE`, convert to page coordinates first:

```python
focus_x = min(max(py5.mouse_x / py5.width, 0.0), 1.0)   # fraction of the page
focus_y = min(max(py5.mouse_y / py5.height, 0.0), 1.0)
```

Then place something at `focus * PAGE_SIZE`. Do **not** normalise over the page
and then apply over an inset sub-rectangle - the point shifts and appears offset
from the cursor.

## Styling

```python
BACKGROUND = 45        # dark grey canvas
STROKE_WEIGHT = 0.6    # thin lines
DISPLAY_COLORS = [(225,), (235, 120, 120), (130, 170, 245)]   # light, on dark
EXPORT_COLORS = [(0,), (180, 30, 30), (30, 60, 180)]          # dark, on white
```

Draw with `py5.background(BACKGROUND)`, `target.no_fill()`,
`target.stroke_weight(STROKE_WEIGHT)`, and select the palette per target. Keeping
display and export palettes separate means styling the screen never ruins the
plot file.

## Display vs export size

Magnify for the display only; export at the real page size via an offscreen
graphics:

```python
def draw():
    py5.background(BACKGROUND)
    py5.push_matrix()
    py5.scale(VIEW_SCALE)
    draw_scene(py5, DISPLAY_COLORS)
    py5.pop_matrix()


def export_svg():
    pg = py5.create_graphics(PAGE_W, PAGE_H, py5.SVG, str(path))
    pg.begin_draw()
    draw_scene(pg, EXPORT_COLORS)
    pg.end_draw()
```

`draw_scene(target, colors)` draws into either the sketch or the recorder, so the
same code renders the screen and the SVG. `Py5Graphics.end_draw()` writes the SVG;
py5 does not expose `dispose()`.

## Gotchas

- A4 in millimetres is 210x297. Mixing centimetre values into `*_MM` constants
  silently scales the work by 10.
- `py5.pixel_density(2)` warns "not available for this display" on many monitors;
  omit it unless the display is known to support it.
- Rotations are radians in py5: wrap degrees in `math.radians`.
- Seed the RNG every frame (`random.Random(seed)`) so jitter is stable, not flickering.
- py5 runs a parent and child process, so two `python.exe` entries is normal.

## Reference

- `references/parameter_window.py` - copy-paste building blocks.
- `sketches/processing/molnar_squares/molnar_squares.py` - the full working example.
