"""Minimal py5 sketch using the GenArt support library.

Run from the project root with:
    .venv-py5\\Scripts\\python sketches\\py5\\minimal_example\\minimal_example.py
"""

import py5

from plotter_art.py5_support import (
    PaperSpace,
    ParamDef,
    ParameterState,
    get_page,
    get_state,
    get_viewport,
    run_sketch,
)

# Describe the physical page. Sketch coordinates below are in millimetres.
PAGE = PaperSpace.preset("A4", orientation="portrait")

# Define a slider and its initial value.
PARAMS = [ParamDef("radius", "Radius (mm)", 10, 80, 1, True, default=40)]
STATE = ParameterState.from_defs(PARAMS)


def draw() -> None:
    """Draw one adjustable circle in the centre of the page."""
    page = get_page()
    viewport = get_viewport()
    state = get_state()
    assert state is not None

    py5.background(35)
    py5.push_matrix()
    viewport.push_transform(py5)  # from page millimetres to preview pixels

    py5.no_fill()
    py5.stroke(235)
    py5.stroke_weight(0.5)  # mm in page space
    py5.rect(0, 0, page.width_mm, page.height_mm)  # page boundary
    py5.ellipse(
        page.width_mm / 2,
        page.height_mm / 2,
        state.float("radius") * 2,
        state.float("radius") * 2,
    )

    py5.pop_matrix()


if __name__ == "__main__":
    run_sketch(
        page=PAGE,
        draw=draw,
        state=STATE,
        params=PARAMS,
        window_title="Minimal py5 sketch",
        controls_title="Sketch parameters",
    )
