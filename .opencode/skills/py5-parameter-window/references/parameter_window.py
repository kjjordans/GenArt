"""Copy-paste building blocks for a py5 sketch with a Tkinter parameter window.

These pieces live in the SAME module as the sketch so that `globals()` in the
slider callbacks refers to the sketch parameters. See
`sketches/processing/molnar_squares/molnar_squares.py` for a complete example.

Adjust PARAMS and the drawing code for your own sketch.
"""

import math
import random
from pathlib import Path

import py5

# --- Sketch parameters: plain module globals the sketch reads each frame ---
N_COLS = 6
SIZE_MM = 30.0
JITTER = 0.1
SPREAD = 0.5
SEED_INITIAL = 42

# --- Controls: (global name, label, min, max, step, is_int) ---
PARAMS = [
    ("N_COLS", "Columns", 1, 12, 1, True),
    ("SIZE_MM", "Size (mm)", 1.0, 60.0, 1.0, False),
    ("JITTER", "Jitter", 0.0, 1.0, 0.01, False),
    ("SPREAD", "Spread", 0.05, 2.0, 0.05, False),
]

# --- Look & page ---
BACKGROUND = 45
STROKE_WEIGHT = 0.6
VIEW_SCALE = 2.5  # magnification for the display only
PAGE_W_MM = 210.0
PAGE_H_MM = 297.0
DISPLAY_COLORS = [(225,), (235, 120, 120), (130, 170, 245), (140, 225, 150)]
EXPORT_COLORS = [(0,), (180, 30, 30), (30, 60, 180), (30, 120, 50)]
OUTPUT_DIR = Path(__file__).parent / "output"

# --- Mutable state ---
seed = SEED_INITIAL
focus_x = 0.5
focus_y = 0.5
_save_requested = False


def randomize_seed() -> None:
    global seed
    seed = random.randint(0, 9999)


def request_save() -> None:
    global _save_requested
    _save_requested = True


def build_controls():
    """Create a Tkinter window with a slider per parameter and two buttons."""
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

        scale = tk.Scale(
            row,
            from_=lo,
            to=hi,
            resolution=step,
            orient="horizontal",
            showvalue=False,
            command=on_change,
            length=200,
        )
        scale.set(globals()[name])
        scale.pack(side="left", fill="x", expand=True)
        value_label.config(text=f"{globals()[name]:g}")
        value_label.pack(side="right")

    buttons = tk.Frame(root)
    buttons.pack(fill="x", padx=8, pady=6)
    tk.Button(buttons, text="Random seed", command=randomize_seed).pack(side="left")
    tk.Button(buttons, text="Export SVG", command=request_save).pack(side="left", padx=6)

    return root


# --- Sketch ---
def draw_scene(target, colors=DISPLAY_COLORS) -> None:
    """Draw into either the sketch (py5) or an offscreen Py5Graphics."""
    target.no_fill()
    target.stroke_weight(STROKE_WEIGHT)
    rng = random.Random(seed)  # re-seed each frame so jitter is stable
    for i in range(N_COLS):
        x = 20.0 + i * SIZE_MM
        y = 20.0 + i * SIZE_MM
        angle = rng.uniform(-5.0, 5.0)
        target.stroke(*colors[i % len(colors)])
        target.push_matrix()
        target.translate(x, y)
        target.rotate(math.radians(angle))
        target.rect(-SIZE_MM / 2, -SIZE_MM / 2, SIZE_MM, SIZE_MM)
        target.pop_matrix()


def export_svg() -> None:
    """Write an exact page-size SVG, independent of the view scale."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / f"sketch_{seed}.svg"
    recorder = py5.create_graphics(int(PAGE_W_MM), int(PAGE_H_MM), py5.SVG, str(path))
    recorder.begin_draw()
    draw_scene(recorder, EXPORT_COLORS)
    recorder.end_draw()
    print(f"saved {path}")


def setup() -> None:
    py5.size(int(PAGE_W_MM * VIEW_SCALE), int(PAGE_H_MM * VIEW_SCALE))
    py5.no_fill()
    py5.frame_rate(30)
    py5.window_title("py5 - parameter window example")


def draw() -> None:
    global _save_requested
    py5.background(BACKGROUND)
    if _save_requested:
        export_svg()
        _save_requested = False
    py5.push_matrix()
    py5.scale(VIEW_SCALE)
    draw_scene(py5, DISPLAY_COLORS)
    py5.pop_matrix()


# --- Interaction ---
def _set_focus() -> None:
    global focus_x, focus_y
    focus_x = min(max(py5.mouse_x / py5.width, 0.0), 1.0)
    focus_y = min(max(py5.mouse_y / py5.height, 0.0), 1.0)


def mouse_pressed() -> None:
    _set_focus()


def mouse_dragged() -> None:
    _set_focus()


def mouse_wheel(event) -> None:
    global SPREAD
    count = event.get_count()  # +1 wheel down, -1 wheel up
    if count:
        SPREAD = min(max(SPREAD * 1.1**count, 0.05), 2.0)


def key_pressed() -> None:
    key = py5.key.lower()
    if key == "r":
        randomize_seed()
    elif key == "s":
        request_save()


if __name__ == "__main__":
    py5.run_sketch(block=False)
    build_controls().mainloop()
    py5.exit_sketch()
