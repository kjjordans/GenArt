"""Launcher - Py5 sketch lifecycle with parameter controls.

Manages the two-window pattern: py5 canvas running non-blocking
plus a Tkinter controls window. Shuts down cleanly when the user
closes the controls.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import py5

from plotter_art.py5_support.controls import ParamDef, ParameterState, build_controls
from plotter_art.py5_support.paperspace import PaperSpace
from plotter_art.py5_support.viewport import Viewport

SketchDrawFn = Callable[[], None]


def run_sketch(
    *,
    page: PaperSpace,
    draw: SketchDrawFn,
    setup: SketchDrawFn | None = None,
    state: ParameterState | None = None,
    params: list[ParamDef] | None = None,
    buttons: dict[str, Callable[[], Any]] | None = None,
    controls_title: str = "Parameters",
    canvas_w: int = 900,
    canvas_h: int = 700,
    window_title: str = "py5 Sketch",
) -> None:
    """Launch a py5 sketch with a Tkinter parameter window.

    This is the recommended entry point for py5 sketches in this project.
    It sets up the canvas, wires the draw callback, builds sliders, and
    keeps both windows alive until the user closes the controls.

    Args:
        page: Physical page being drawn.
        draw: Callable invoked every frame. Should draw into ``py5``
            using the current page/viewport transform.
        setup: Optional callable invoked once after ``py5.setup()``.
        state: Live parameter state. Required if sliders are used.
        params: Parameter definitions for the Tkinter sliders.
            Required if sliders are used.
        buttons: Optional button label -> callback mapping.
        controls_title: Tkinter window title.
        canvas_w: Canvas width in pixels.
        canvas_h: Canvas height in pixels.
        window_title: Py5 window title.

    Example:
        >>> page = PaperSpace.preset("A4", orientation="portrait")
        >>> state = ParameterState.from_defs(params)
        >>>
        >>> def draw():
        ...     viewport = get_viewport()
        ...     py5.background(30)
        ...     py5.push_matrix()
        ...     viewport.push_transform(py5)
        ...     py5.rect(0, 0, 100, 100)
        ...     py5.pop_matrix()
        ...
        >>> run_sketch(page=page, draw=draw, state=state, params=params)
    """
    if params and state is None:
        raise ValueError("state is required when params are provided")

    viewport = Viewport.fit(page, canvas_w=canvas_w, canvas_h=canvas_h)

    # Store on the module for draw/setup access
    _SKETCH_DATA["page"] = page
    _SKETCH_DATA["viewport"] = viewport
    _SKETCH_DATA["user_draw"] = draw
    _SKETCH_DATA["user_setup"] = setup
    _SKETCH_DATA["state"] = state
    _SKETCH_DATA["canvas_w"] = canvas_w
    _SKETCH_DATA["canvas_h"] = canvas_h
    _SKETCH_DATA["window_title"] = window_title

    sketch_functions = _make_py5_functions()
    py5.run_sketch(block=False, sketch_functions=sketch_functions)

    if params:
        root = build_controls(
            state,  # type: ignore[arg-type]
            params,
            buttons=buttons,
            title=controls_title,
        )
    else:
        root = _minimal_controls(buttons)

    root.mainloop()
    py5.exit_sketch()


def _minimal_controls(
    buttons: dict[str, Callable[[], Any]] | None = None,
) -> Any:
    """Make a minimal placeholder controls window when no sliders are needed."""
    import tkinter as tk

    root = tk.Tk()
    root.title("Controls")
    if buttons:
        frame = tk.Frame(root)
        frame.pack(padx=8, pady=6)
        for label, cb in buttons.items():
            tk.Button(frame, text=label, command=cb).pack(side="left", padx=4)
    return root


def _make_py5_functions() -> dict[str, SketchDrawFn]:
    """Build the py5 callbacks explicitly for ``run_sketch``.

    Passing callbacks through ``sketch_functions`` avoids relying on py5's
    caller-frame discovery, which does not work when the launcher is the
    direct caller of ``run_sketch``.
    """
    canvas_w = _SKETCH_DATA["canvas_w"]
    canvas_h = _SKETCH_DATA["canvas_h"]

    def _settings() -> None:
        py5.size(canvas_w, canvas_h)

    def _setup() -> None:
        py5.frame_rate(30)
        py5.window_title(_SKETCH_DATA["window_title"])
        user_setup = _SKETCH_DATA.get("user_setup")
        if user_setup:
            user_setup()

    def _draw() -> None:
        user_draw = _SKETCH_DATA["user_draw"]
        if user_draw:
            user_draw()

    return {"settings": _settings, "setup": _setup, "draw": _draw}


# Module-level storage so py5 callbacks can access sketch configuration
_SKETCH_DATA: dict[str, Any] = {}


def get_page() -> PaperSpace:
    """Return the current sketch's PaperSpace.

    Call from within ``draw`` or ``setup``.
    """
    return _SKETCH_DATA["page"]


def get_viewport() -> Viewport:
    """Return the current sketch's Viewport.

    Call from within ``draw`` or ``setup``.
    """
    return _SKETCH_DATA["viewport"]


def get_state() -> ParameterState | None:
    """Return the current sketch's ParameterState, or ``None``."""
    return _SKETCH_DATA.get("state")
