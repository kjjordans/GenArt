"""py5 Hello World — using the py5 support library.

A dark canvas shows a Perlin-noise field thresholded into a dot grid.
Demonstrates PaperSpace, Viewport, ParameterState, and SVG export.

Run with:
    .venv-py5\\Scripts\\python sketches\\py5\\py5_hello_world\\py5_hello_world.py
"""

from __future__ import annotations

import math

import numpy as np
import opensimplex
import py5

from plotter_art.py5_support import (
    PaperSpace,
    ParamDef,
    ParameterState,
    export_sketch,
    get_page,
    get_state,
    get_viewport,
    run_sketch,
)

# ------------------------------------------------------------------ #
# Sketch-specific configuration
# ------------------------------------------------------------------ #
PAGE = PaperSpace.preset("A4", orientation="portrait")

PARAM_DEFS = [
    ParamDef("freq", "Frequency", 0.01, 0.5, 0.01, False),
    ParamDef("threshold", "Threshold", -1.0, 1.0, 0.05, False),
    ParamDef("seed", "Seed", 0, 100, 1, True),
]

STATE = ParameterState.from_defs(PARAM_DEFS)

# ------------------------------------------------------------------ #
# Display style
# ------------------------------------------------------------------ #
BACKGROUND = 30
STROKE_WEIGHT = 0.4
CELL_MM = 4.0  # grid cell size

# ------------------------------------------------------------------ #
# Noise cache
# ------------------------------------------------------------------ #
_noise_cache: dict = {"seed": None, "freq": None, "array": None}


def get_noise_field() -> np.ndarray:
    """Return a 2D opensimplex noise field for the current parameters."""
    state = get_state()
    assert state is not None

    freq = state.float("freq")
    seed = state.int("seed")
    page = get_page()

    n_cols = math.ceil(page.width_mm / CELL_MM)
    n_rows = math.ceil(page.height_mm / CELL_MM)

    if (
        _noise_cache["seed"] == seed
        and _noise_cache["freq"] == freq
        and _noise_cache["array"] is not None
    ):
        return _noise_cache["array"]

    simplex = opensimplex.OpenSimplex(seed=seed)
    arr = np.empty((n_rows, n_cols), dtype=np.float64)
    for r in range(n_rows):
        for c in range(n_cols):
            x = c * CELL_MM * freq
            y = r * CELL_MM * freq
            arr[r, c] = simplex.noise2(x, y)

    _noise_cache.update({"seed": seed, "freq": freq, "array": arr})
    return arr


def draw_art(target: py5.Py5Graphics) -> None:
    """Draw the noise-threshold dots into *target*."""
    state = get_state()
    assert state is not None
    threshold = state.float("threshold")

    field = get_noise_field()
    n_rows, n_cols = field.shape
    page = get_page()

    target.no_stroke()

    for r in range(n_rows):
        for c in range(n_cols):
            val = field[r, c]
            x = c * CELL_MM
            y = r * CELL_MM

            # Only draw if within page bounds
            if x > page.width_mm or y > page.height_mm:
                continue

            if val > threshold:
                intensity = (val - threshold) / (1.0 - threshold + 1e-6)
                grey = 120 + int(intensity * 120)
                target.fill(grey)
                radius = CELL_MM * 0.35 * (0.3 + 0.7 * intensity)
                target.ellipse(x, y, radius * 2, radius * 2)

    # boundary frame
    target.no_fill()
    target.stroke(180)
    target.stroke_weight(STROKE_WEIGHT)
    target.rect(0, 0, page.width_mm, page.height_mm)


def draw() -> None:
    """Main py5 draw loop."""
    viewport = get_viewport()

    py5.background(BACKGROUND)
    py5.push_matrix()
    viewport.push_transform(py5)
    draw_art(py5)
    py5.pop_matrix()


def do_export() -> None:
    """Export the current state to an SVG."""
    page = get_page()
    path = __file__.replace(".py", f"_{get_state().int('seed')}.svg")
    export_sketch(page, draw_art, path)


if __name__ == "__main__":
    run_sketch(
        page=PAGE,
        draw=draw,
        state=STATE,
        params=PARAM_DEFS,
        buttons={"Export SVG": do_export},
        controls_title="Hello World Parameters",
        window_title="py5 Hello World — Noise Field",
    )
