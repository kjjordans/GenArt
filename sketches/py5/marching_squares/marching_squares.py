"""Starter template for a new py5 sketch.

Copy this file into a new folder under ``sketches/py5/`` and rename it.
Run from the project root with:
    .venv-py5\\Scripts\\python sketches\\py5\\<your_sketch>\\<your_sketch>.py
"""

# ---------------------------------------------------------------------------
# KEEP: Imports needed by the standard py5 sketch setup.
# Add algorithm-specific imports below this block.
# ---------------------------------------------------------------------------
from pathlib import Path
import numpy as np
import py5

from plotter_art.py5_support import (
    PaperSpace,
    ParamDef,
    ParameterState,
    get_page,
    get_state,
    get_viewport,
    make_svg_export_callback,
    run_sketch,
)

# ---------------------------------------------------------------------------
# CUSTOMIZE: Choose a paper size and orientation.
# Coordinates used by the artwork below are millimetres.
# ---------------------------------------------------------------------------
SKETCH_NAME = "my_sketch"
PAGE = PaperSpace.preset("A4", orientation="portrait")
OUTPUT_DIR = Path(__file__).parent / "output"


# ---------------------------------------------------------------------------
# CUSTOMIZE: Define the sliders your sketch needs.
# Remove the example slider and add/edit ParamDef entries as needed.
# If you change these definitions, keep STATE initialized from PARAMS.
# ---------------------------------------------------------------------------
PARAMS = [
   #ParamDef(key, label, lo, hi, step, is_int, default=None)
    ParamDef("margin", "Margin (mm)", 0, 80, 1, True, default=35),
    ParamDef("seed", "Seed", 0, 1000, 1, True, default=42),
    ParamDef("freq", "Noise Frequency", 0.01, 0.5, 0.01, False, default=0.1),
    ParamDef("cols", "Columns", 1, 50, 1, True, default=10),
]
STATE = ParameterState.from_defs(PARAMS)


# ---------------------------------------------------------------------------
# CUSTOMIZE: Put your artwork here.
# Keep this function free of background/window setup so it can draw both
# in the preview and in the SVG. `target` is py5 or an SVG graphics target;
# all drawing coordinates and sizes are in millimetres.
# ---------------------------------------------------------------------------
def draw_sketch(sketch, page: PaperSpace, state: ParameterState) -> None:
    """Draw the artwork in page-space millimetres."""
    sketch.no_fill()
    sketch.stroke(235)
    sketch.stroke_weight(0.5)

    # get parameters from the state
    margin = state.float("margin")
    seed = state.int("seed")
    freq = state.float("freq")
    cols = state.int("cols")


    py5.noise_seed(seed)
    #calculate the number of rows to keep the same margin at the top and bottom
    rows = int((page.height_mm - 2 * margin) / ((page.width_mm - 2 * margin) / cols))



    # cell size
    cell_width = (page.width_mm - 2 * margin) / (cols)
    cell_height = cell_width

    

    for row in range (rows + 1):
        for col in range(cols + 1):
            
            x = margin + col * cell_width
            y = margin + row * cell_height
            val = py5.noise(x * freq, y * freq)
            sketch.fill(255 * val)
            sketch.ellipse(x, y, 3, 3)


# ---------------------------------------------------------------------------
# KEEP or CUSTOMIZE: Default SVG export button.
# The library provides the file dialog and writes the SVG. The sketch only
# supplies its artwork callback, page, and output location.
# ---------------------------------------------------------------------------
BUTTONS = {
    "Export SVG": make_svg_export_callback(
        PAGE,
        lambda sketch: draw_sketch(sketch, PAGE, STATE),
        OUTPUT_DIR,
        initial_filename=f"{SKETCH_NAME}.svg",
    ),
}


# ---------------------------------------------------------------------------
# KEEP: Preview callback structure.
# Clear the screen, apply the page-to-screen transform, draw the artwork,
# then restore the transform. Put preview-only backgrounds/images here.
# ---------------------------------------------------------------------------
def draw() -> None:
    page = get_page()
    state = get_state()
    viewport = get_viewport()
    assert state is not None

    py5.background(126)
    py5.push_matrix()
    viewport.push_transform(py5)

    # Optional page boundary, visible in preview and included in SVG only if
    # you also add it to draw_sketch().
    py5.no_fill()
    py5.stroke(100)
    py5.stroke_weight(0.4)
    py5.rect(0, 0, page.width_mm, page.height_mm)

    draw_sketch(py5, page, state)
    py5.pop_matrix()


# ---------------------------------------------------------------------------
# KEEP: Entry point and shared launcher.
# Pass your page, draw callback, and slider definitions/state here.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_sketch(
        page=PAGE,
        draw=draw,
        state=STATE,
        params=PARAMS,
        buttons=BUTTONS,
        controls_title=f"{SKETCH_NAME} parameters",
        window_title=SKETCH_NAME,
        canvas_w=1200,
        canvas_h=1200
    )
