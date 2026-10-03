"""Molnár squares - py5 (Processing) port.

Grid of squares with concentric rings and seeded, focus-weighted disorder.
Interactive: drag to move the bell focus; keyboard shortcuts for reseed,
SVG export and toggling omission.

Run with:
    .venv-py5\\Scripts\\python processing\\molnar_squares\\molnar_squares.py
"""

import math
import random
from pathlib import Path

import py5

# --- Parameters (mirrors sketches/molnar_squares/sketch_molnar_squares.py) ---
MARGIN_MM = 20.0  # vsketch used 2.0 cm
N_COLS = 6
N_ROWS = 6
PADDING_MM = 5.0  # vsketch used 0.5 cm
NESTS = 3
NEST_SCALE = 0.75
JITTER_POS = 0.1  # fraction of the cell pitch
JITTER_ANGLE = 1.0  # degrees
JITTER_SCALE = 1.0  # 1 = none, 1.1 or 0.9 = +/-10%
SPREAD = 0.5  # bell width, as a fraction of the grid reach
LAYERS = 1  # squares are assigned a random layer

OMIT_STEP = 0.2  # value the O key toggles between 0 and this
SEED_INITIAL = 42

PAGE_W_MM = 210.0
PAGE_H_MM = 297.0
VIEW_SCALE = 2.5  # on-screen magnification; the export stays at real A4 size

BACKGROUND = 45  # dark grey canvas
STROKE_WEIGHT = 0.6  # thinner lines

# layer -> stroke colour; light on the dark canvas for the display...
DISPLAY_COLORS = [(225,), (235, 120, 120), (130, 170, 245), (140, 225, 150)]
# ...and dark, distinguishable colours for the SVG (previewed on white paper)
EXPORT_COLORS = [(0,), (180, 30, 30), (30, 60, 180), (30, 120, 50)]

OUTPUT_DIR = Path(__file__).parent / "output"

# --- Mutable interaction state ---
focus_x = 0.5  # 0 = left edge, 1 = right
focus_y = 0.5  # 0 = top edge, 1 = bottom
seed = SEED_INITIAL
omit = 0.0
_save_requested = False

# --- Controls window: (global name, label, min, max, step, is_int) ---
PARAMS = [
    ("N_COLS", "Columns", 1, 12, 1, True),
    ("N_ROWS", "Rows", 1, 12, 1, True),
    ("NESTS", "Rings", 1, 8, 1, True),
    ("LAYERS", "Layers", 1, 4, 1, True),
    ("MARGIN_MM", "Margin (mm)", 0.0, 40.0, 1.0, False),
    ("PADDING_MM", "Padding (mm)", 0.0, 15.0, 0.5, False),
    ("NEST_SCALE", "Ring scale", 0.1, 1.0, 0.01, False),
    ("JITTER_POS", "Jitter pos", 0.0, 1.0, 0.01, False),
    ("JITTER_ANGLE", "Jitter angle", 0.0, 20.0, 0.5, False),
    ("JITTER_SCALE", "Jitter scale", 0.5, 1.5, 0.01, False),
    ("SPREAD", "Spread", 0.05, 2.0, 0.05, False),
    ("omit", "Omit", 0.0, 1.0, 0.01, False),
]


def compute_squares() -> list[tuple[float, float, float, float, float, int]]:
    """Return the squares to draw as (x, y, angle_deg, scale, size, layer)."""
    usable_w = PAGE_W_MM - 2 * MARGIN_MM
    cell_w = (usable_w - (N_COLS - 1) * PADDING_MM) / N_COLS
    pitch = cell_w + PADDING_MM

    # grid extents
    grid_w = (N_COLS - 1) * pitch + cell_w
    grid_h = (N_ROWS - 1) * pitch + cell_w
    x0, y0 = MARGIN_MM, MARGIN_MM

    # the focus is a point on the page, so the mouse cursor maps to it directly
    ref = (focus_x * PAGE_W_MM, focus_y * PAGE_H_MM)

    # the farthest cell from the focus is always a corner cell
    corner_cells = [
        (x0 + cell_w / 2, y0 + cell_w / 2),
        (x0 + grid_w - cell_w / 2, y0 + cell_w / 2),
        (x0 + cell_w / 2, y0 + grid_h - cell_w / 2),
        (x0 + grid_w - cell_w / 2, y0 + grid_h - cell_w / 2),
    ]
    max_dist = max(math.dist(ref, c) for c in corner_cells)
    sigma = max(SPREAD * max_dist, 1e-6)

    rng = random.Random(seed)
    offset = JITTER_POS * pitch
    amplitude = abs(JITTER_SCALE - 1.0)

    squares = []
    for row in range(N_ROWS):
        for col in range(N_COLS):
            cx = MARGIN_MM + col * pitch + cell_w / 2
            cy = MARGIN_MM + row * pitch + cell_w / 2

            # bell weight: 1 at the focus, falling off with distance
            w = math.exp(-((math.dist((cx, cy), ref) / sigma) ** 2))

            for i in range(NESTS):
                # draw all randoms before the omit roll, so changing `omit`
                # only removes squares without moving the others
                dx = rng.uniform(-offset * w, offset * w)
                dy = rng.uniform(-offset * w, offset * w)
                angle = rng.uniform(-JITTER_ANGLE * w, JITTER_ANGLE * w)
                scale = 1.0 + rng.uniform(-amplitude * w, amplitude * w)
                layer = rng.randint(1, LAYERS)

                if rng.random() < omit:
                    continue

                size = cell_w * NEST_SCALE**i
                squares.append((cx + dx, cy + dy, angle, scale, size, layer))

    return squares


def draw_scene(target, colors=DISPLAY_COLORS) -> None:
    """Draw every square, each with its own transform (off-register rings).

    `target` is either the main sketch (py5) or an offscreen Py5Graphics, so the
    same code renders both the display and the exported SVG.
    """
    target.no_fill()
    target.stroke_weight(STROKE_WEIGHT)
    for x, y, angle, scale, size, layer in compute_squares():
        target.stroke(*colors[(layer - 1) % len(colors)])
        target.push_matrix()
        target.translate(x, y)
        target.rotate(math.radians(angle))
        target.scale(scale)
        target.rect(-size / 2, -size / 2, size, size)
        target.pop_matrix()


def export_svg() -> None:
    """Write an exact A4 SVG (real page size), independent of the view scale."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / f"molnar_{seed}.svg"
    recorder = py5.create_graphics(int(PAGE_W_MM), int(PAGE_H_MM), py5.SVG, str(path))
    recorder.begin_draw()
    draw_scene(recorder, EXPORT_COLORS)
    recorder.end_draw()
    print(f"saved {path}")


def setup() -> None:
    py5.size(int(PAGE_W_MM * VIEW_SCALE), int(PAGE_H_MM * VIEW_SCALE))
    py5.no_fill()
    py5.frame_rate(30)
    py5.window_title("Molnar Squares - py5")


def draw() -> None:
    global _save_requested
    py5.background(BACKGROUND)
    if _save_requested:
        export_svg()
        _save_requested = False

    # magnify for the display only; the export uses real A4 coordinates
    py5.push_matrix()
    py5.scale(VIEW_SCALE)
    draw_scene(py5)
    py5.pop_matrix()


def randomize_seed() -> None:
    global seed
    seed = random.randint(0, 9999)


def request_save() -> None:
    global _save_requested
    _save_requested = True


def build_controls():
    """Create a Tkinter window with a slider per parameter."""
    import tkinter as tk

    root = tk.Tk()
    root.title("Molnar parameters")

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


def _set_focus() -> None:
    global focus_x, focus_y
    focus_x = min(max(py5.mouse_x / py5.width, 0.0), 1.0)
    focus_y = min(max(py5.mouse_y / py5.height, 0.0), 1.0)


def mouse_pressed() -> None:
    _set_focus()


def mouse_dragged() -> None:
    _set_focus()


def mouse_wheel(event) -> None:
    """Scroll to widen/narrow the bell spread."""
    global SPREAD
    count = event.get_count()
    if count:
        SPREAD = min(max(SPREAD * 1.1**count, 0.05), 2.0)


def key_pressed() -> None:
    global omit
    key = py5.key.lower()
    if key == "r":
        randomize_seed()
    elif key == "s":
        request_save()
    elif key == "o":
        omit = 0.0 if omit > 0.0 else OMIT_STEP


if __name__ == "__main__":
    py5.run_sketch(block=False)
    controls = build_controls()
    controls.mainloop()
    py5.exit_sketch()
