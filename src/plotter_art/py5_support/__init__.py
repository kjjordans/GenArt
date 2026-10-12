"""py5 sketch support library for GenArt.

Reusable building blocks for py5 sketches: physical page model,
preview viewport, image display and sampling, parameter controls,
plotter-ready SVG export, and application lifecycle.

This module can be imported without py5 installed. py5-dependent
components are loaded on first use or explicit import.

Example:
    >>> from plotter_art.py5_support.paperspace import PaperSpace, cm
    >>> from plotter_art.py5_support.controls import ParameterState, ParamDef
"""

import importlib.util

# Core non-py5 modules (always available)
from plotter_art.py5_support.controls import ParamDef, ParameterState, build_controls
from plotter_art.py5_support.imagelayer import ImageLayer
from plotter_art.py5_support.paperspace import PaperSpace, cm
from plotter_art.py5_support.viewport import Viewport

__all__ = [
    "ImageLayer",
    "PaperSpace",
    "ParamDef",
    "ParameterState",
    "Viewport",
    "build_controls",
    "cm",
]

# Lazy py5-dependent imports
_py5_available = importlib.util.find_spec("py5") is not None

if _py5_available:
    from plotter_art.py5_support import launcher as _launcher
    from plotter_art.py5_support import svg_export as _svg_export

    get_page = _launcher.get_page
    get_state = _launcher.get_state
    get_viewport = _launcher.get_viewport
    run_sketch = _launcher.run_sketch
    SVGExporter = _svg_export.SVGExporter
    export_sketch = _svg_export.export_sketch
    make_svg_export_callback = _svg_export.make_svg_export_callback

    __all__.extend(
        [
            "SVGExporter",
            "export_sketch",
            "get_page",
            "get_state",
            "get_viewport",
            "make_svg_export_callback",
            "run_sketch",
        ]
    )
