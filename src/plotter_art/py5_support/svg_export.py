"""SVG export helper for py5 sketches with physical page dimensions.

Provides a reusable pattern to export sketch geometry at real
millimetre scale, with a matching viewBox so coordinates map
directly to mm.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections.abc import Callable
from pathlib import Path

import py5

from plotter_art.py5_support.paperspace import PaperSpace


class SVGExporter:
    """Export sketch geometry to a plotter-ready SVG.

    Usage:
        def draw_art(target):
            # Draw in page mm coordinates into target
            target.line(0, 0, 210, 297)

        exporter = SVGExporter(page)
        exporter.export(draw_art, "output/sketch.svg")
    """

    def __init__(self, page: PaperSpace) -> None:
        """Create an exporter for *page*.

        Args:
            page: PaperSpace defining physical dimensions.
        """
        self.page = page

    def export(
        self,
        draw_fn: Callable[[py5.Py5Graphics], None],
        path: str | Path,
        *,
        stroke_colour: tuple[int, ...] = (0,),
        stroke_width_mm: float = 0.4,
    ) -> Path:
        """Export geometry through *draw_fn* to an SVG file.

        Args:
            draw_fn: Callback that receives a ``Py5Graphics`` and draws
                the artwork in page mm coordinates.
            path: Output file path.
            stroke_colour: Default stroke colour for the SVG group.
                ``(gray,)`` or ``(r, g, b)``.
            stroke_width_mm: Default stroke width in mm.

        Returns:
            The output path.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        w = int(self.page.width_mm)
        h = int(self.page.height_mm)

        # py5 SVG renderer
        recorder = py5.create_graphics(w, h, py5.SVG, str(path))
        recorder.begin_draw()

        # Set default style
        recorder.no_fill()
        recorder.stroke(*stroke_colour)
        recorder.stroke_weight(stroke_width_mm)

        # Let the sketch draw
        draw_fn(recorder)

        recorder.end_draw()

        # Patch viewBox and physical dimensions on the generated SVG
        self._patch_svg(path)

        print(f"exported {path}")
        return path

    def _patch_svg(self, path: Path) -> None:
        """Inject viewBox and mm dimensions into the exported SVG.

        Args:
            path: Path to the SVG file to patch in place.
        """
        try:
            tree = ET.parse(path)
            root = tree.getroot()

            root.set("width", f"{self.page.width_mm:.1f}mm")
            root.set("height", f"{self.page.height_mm:.1f}mm")
            root.set(
                "viewBox",
                f"0 0 {self.page.width_mm:.1f} {self.page.height_mm:.1f}",
            )

            tree.write(path, encoding="utf-8", xml_declaration=True)
        except ET.ParseError as exc:
            raise ValueError(f"Could not parse generated SVG {path}: {exc}") from exc


def export_sketch(
    page: PaperSpace,
    draw_fn: Callable[[py5.Py5Graphics], None],
    path: str | Path,
    **kwargs,
) -> Path:
    """One-shot export convenience function.

    Args:
        page: Physical page dimensions.
        draw_fn: Drawing callback receiving ``Py5Graphics``.
        path: Output file path.
        **kwargs: Extra options forwarded to ``SVGExporter.export``.

    Returns:
        The output path.

    Example:
        >>> page = PaperSpace.preset("A4", orientation="portrait")
        >>> export_sketch(page, draw_art, "output/art.svg")
    """
    exporter = SVGExporter(page)
    return exporter.export(draw_fn, path, **kwargs)


def make_svg_export_callback(
    page: PaperSpace,
    draw_fn: Callable[[py5.Py5Graphics], None],
    output_dir: str | Path,
    *,
    initial_filename: str = "sketch.svg",
    title: str = "Export sketch as SVG",
) -> Callable[[], None]:
    """Create a button callback that asks for an SVG path and exports.

    Intended for use with ``run_sketch(buttons={...})``. The file dialog
    and output-directory creation are handled here so sketches only need
    to provide their drawing callback and output location.

    Args:
        page: Physical page dimensions.
        draw_fn: Callback that draws artwork in page mm coordinates.
        output_dir: Initial directory shown in the save dialog.
        initial_filename: Suggested output filename.
        title: File-dialog title.

    Returns:
        A no-argument callback suitable for a Tkinter button.
    """
    output_dir = Path(output_dir)

    def export_from_dialog() -> None:
        from tkinter import filedialog

        output_dir.mkdir(parents=True, exist_ok=True)
        path = filedialog.asksaveasfilename(
            title=title,
            initialdir=str(output_dir),
            initialfile=initial_filename,
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg")],
        )
        if path:
            export_sketch(page, draw_fn, path)

    return export_from_dialog
