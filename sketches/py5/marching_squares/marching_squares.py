"""Starter template for a new py5 sketch.

Copy this file into a new folder under ``sketches/py5/`` and rename it.
Run from the project root with:
    .venv-py5\\Scripts\\python sketches\\py5\\<your_sketch>\\<your_sketch>.py
"""

# ---------------------------------------------------------------------------
# KEEP: Imports needed by the standard py5 sketch setup.
# Add algorithm-specific imports below this block.
# ---------------------------------------------------------------------------
from collections.abc import Sequence
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
from plotter_art.renderers import ContourStyle, DEFAULT_CONTOUR_STYLES

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
    ParamDef("cols", "Columns", 1, 400, 1, True, default=100),
]
STATE = ParameterState.from_defs(PARAMS)
STATE.update("show_ellipses", 1)

# Override this with a tuple of ContourStyle entries to customize this sketch.
CONTOUR_STYLES = DEFAULT_CONTOUR_STYLES


# ---------------------------------------------------------------------------
# CUSTOMIZE: Put your artwork here.
# Keep this function free of background/window setup so it can draw both
# in the preview and in the SVG. `target` is py5 or an SVG graphics target;
# all drawing coordinates and sizes are in millimetres.
# ---------------------------------------------------------------------------

def edge_crossing(x1, y1, x2, y2, v1, v2, level):
    """Calculate the crossing point of the edge between (x1, y1) and (x2, y2)
    where the values v1 and v2 cross the given level."""
    if (v1 >= level) == (v2 >= level):
        return None

    t = (level - v1) / (v2 - v1)
    x_cross = x1 + t * (x2 - x1)
    y_cross = y1 + t * (y2 - y1)
    return x_cross, y_cross


def draw_contours(sketch, xs, ys, values, level: float) -> None:
    """Draw one marching-squares contour at *level*.

    The caller sets the stroke colour before calling this function.
    """
    rows = values.shape[0] - 1
    cols = values.shape[1] - 1

    for row in range(rows):
        for col in range(cols):
            x0, y0 = xs[col], ys[row]
            x1, y1 = xs[col + 1], ys[row + 1]

            tl = values[row, col]
            tr = values[row, col + 1]
            br = values[row + 1, col + 1]
            bl = values[row + 1, col]

            case = (
                int(tl >= level)
                | (int(tr >= level) << 1)
                | (int(br >= level) << 2)
                | (int(bl >= level) << 3)
            )

            if case in (0, 15):
                continue

            crossings = []
            p_top = edge_crossing(x0, y0, x1, y0, tl, tr, level)
            p_right = edge_crossing(x1, y0, x1, y1, tr, br, level)
            p_bottom = edge_crossing(x0, y1, x1, y1, bl, br, level)
            p_left = edge_crossing(x0, y0, x0, y1, tl, bl, level)

            if p_top is not None:
                crossings.append(p_top)
            if p_right is not None:
                crossings.append(p_right)
            if p_bottom is not None:
                crossings.append(p_bottom)
            if p_left is not None:
                crossings.append(p_left)

            if len(crossings) == 2:
                p1, p2 = crossings
                sketch.line(p1[0], p1[1], p2[0], p2[1])
            elif len(crossings) == 4:
                center_high = (tl + tr + br + bl) / 4 >= level

                if case == 5:
                    pairs = (
                        ((0, 1), (2, 3))
                        if center_high
                        else ((0, 3), (1, 2))
                    )
                else:  # case == 10
                    pairs = (
                        ((0, 3), (1, 2))
                        if center_high
                        else ((0, 1), (2, 3))
                    )

                for first, second in pairs:
                    p1 = crossings[first]
                    p2 = crossings[second]
                    sketch.line(p1[0], p1[1], p2[0], p2[1])


def draw_sketch(
    sketch,
    page: PaperSpace,
    state: ParameterState,
    contour_styles: Sequence[ContourStyle] = DEFAULT_CONTOUR_STYLES,
) -> None:
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

    xs = [margin + col * cell_width for col in range(cols + 1)]
    ys = [margin + row * cell_height for row in range(rows + 1)]

    values = np.empty((rows + 1, cols + 1), dtype=float)

    # get the noise values for each grid point
    for row, y in enumerate(ys):
        for col, x in enumerate(xs):
            values[row, col] = py5.noise(x * freq, y * freq)

    if state.int("show_ellipses"):
        sketch.no_stroke()
        for row in range(rows + 1):
            for col in range(cols + 1):

                sketch.fill(255 * values[row, col])
                sketch.ellipse(xs[col], ys[row], 1, 1)  
    
    
    
    for style in contour_styles:
        sketch.stroke(*style.stroke_rgb)
        sketch.stroke_weight(style.stroke_width_mm)
        draw_contours(sketch, xs, ys, values, style.level)

    # Display the grid points as small circles when the debug toggle is on.



# ---------------------------------------------------------------------------
# KEEP or CUSTOMIZE: Default SVG export button.
# The library provides the file dialog and writes the SVG. The sketch only
# supplies its artwork callback, page, and output location.
# ---------------------------------------------------------------------------
def toggle_ellipses() -> None:
    """Toggle the temporary grid-point circles on or off."""
    STATE.update("show_ellipses", 1 - STATE.int("show_ellipses"))


def export_metadata() -> dict[str, object]:
    """Return the current sketch configuration for its SVG sidecar."""
    return {
        "schema_version": 1,
        "sketch_name": SKETCH_NAME,
        "page": {
            "name": PAGE.name,
            "width_mm": PAGE.width_mm,
            "height_mm": PAGE.height_mm,
        },
        "parameters": {
            "margin_mm": STATE.float("margin"),
            "seed": STATE.int("seed"),
            "noise_coordinate_scale_per_mm": STATE.float("freq"),
            "columns": STATE.int("cols"),
            "show_ellipses": bool(STATE.int("show_ellipses")),
        },
        "contour_styles": [
            {
                "level": style.level,
                "stroke_rgb": list(style.stroke_rgb),
                "stroke_width_mm": style.stroke_width_mm,
            }
            for style in CONTOUR_STYLES
        ],
    }


BUTTONS = {
    "Toggle ellipses": toggle_ellipses,
    "Export SVG": make_svg_export_callback(
        PAGE,
        lambda sketch: draw_sketch(sketch, PAGE, STATE, CONTOUR_STYLES),
        OUTPUT_DIR,
        initial_filename=f"{SKETCH_NAME}.svg",
        metadata_fn=export_metadata,
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

    draw_sketch(py5, page, state, CONTOUR_STYLES)
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
