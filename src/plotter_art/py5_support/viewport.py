"""Viewport - Screen preview fitting for PaperSpace.

Maps mm-based PaperSpace coordinates to py5 pixel coordinates
while preserving aspect ratio and keeping a configurable margin.
"""

from __future__ import annotations

from dataclasses import dataclass

from plotter_art.py5_support.paperspace import PaperSpace


@dataclass(frozen=True, slots=True)
class Viewport:
    """Screen viewport that fits a PaperSpace page into a window.

    Attributes:
        canvas_w: Window width in pixels.
        canvas_h: Window height in pixels.
        page: Associated PaperSpace.
        scale: Pixels per mm.
        offset_x: Horizontal offset in pixels to center the page.
        offset_y: Vertical offset in pixels to center the page.
    """

    canvas_w: int
    canvas_h: int
    page: PaperSpace
    scale: float
    offset_x: float
    offset_y: float

    @classmethod
    def fit(
        cls,
        page: PaperSpace,
        *,
        canvas_w: int = 900,
        canvas_h: int = 700,
        margin_pixels: int = 20,
    ) -> Viewport:
        """Create a viewport that fits *page* into an on-screen canvas.

                The fit preserves page aspect ratio and centres the page within
        the available canvas area.

                Args:
                    page: PaperSpace to preview.
                    canvas_w: Canvas width in pixels.
                    canvas_h: Canvas height in pixels.
                    margin_pixels: Empty margin around the page in pixels.

                Returns:
                    A ``Viewport`` instance for this fit.

                Example:
                    >>> page = PaperSpace.preset("A4", orientation="portrait")
                    >>> vp = Viewport.fit(page, canvas_w=900, canvas_h=700)
                    >>> vp.scale > 0
                    True
        """
        usable_w = max(canvas_w - 2 * margin_pixels, 1)
        usable_h = max(canvas_h - 2 * margin_pixels, 1)

        page_ratio = page.aspect_ratio
        view_ratio = usable_w / usable_h

        if page_ratio > view_ratio:
            # Page is wider relative to view -> width constrained
            scale = usable_w / page.width_mm
        else:
            # Page is taller relative to view -> height constrained
            scale = usable_h / page.height_mm

        draw_w = page.width_mm * scale
        draw_h = page.height_mm * scale

        offset_x = (canvas_w - draw_w) / 2.0
        offset_y = (canvas_h - draw_h) / 2.0

        return cls(
            canvas_w=canvas_w,
            canvas_h=canvas_h,
            page=page,
            scale=scale,
            offset_x=offset_x,
            offset_y=offset_y,
        )

    # ------------------------------------------------------------------ #
    # Coordinate transforms
    # ------------------------------------------------------------------ #

    def to_screen(self, x_mm: float, y_mm: float) -> tuple[float, float]:
        """Convert page-space (mm) to screen-space (pixels).

        Args:
            x_mm: X coordinate in millimetres.
            y_mm: Y coordinate in millimetres.

        Returns:
            ``(screen_x, screen_y)`` in pixel coordinates.
        """
        sx = x_mm * self.scale + self.offset_x
        sy = y_mm * self.scale + self.offset_y
        return sx, sy

    def to_page(self, screen_x: float, screen_y: float) -> tuple[float, float]:
        """Convert screen-space (pixels) to page-space (mm).

        Args:
            screen_x: Screen X coordinate in pixels.
            screen_y: Screen Y coordinate in pixels.

        Returns:
            ``(x_mm, y_mm)`` in millimetres.
        """
        x_mm = (screen_x - self.offset_x) / self.scale
        y_mm = (screen_y - self.offset_y) / self.scale
        return x_mm, y_mm

    # ------------------------------------------------------------------ #
    # py5 helpers
    # ------------------------------------------------------------------ #

    def push_transform(self, py5_module) -> None:
        """Apply the viewport transform so py5 drawing uses mm coordinates.

        Call ``py5.push_matrix()`` before this and ``py5.pop_matrix()`` after.
        """
        py5_module.translate(self.offset_x, self.offset_y)
        py5_module.scale(self.scale)

    def draw_page_outline(self, py5_module, *, colour: tuple = (180,), weight: float = 0.4) -> None:
        """Draw the paper page outline for preview.

        Args:
            py5_module: The py5 module.
            colour: ``(gray,)`` or ``(r, g, b)`` stroke colour.
            weight: Stroke weight in pixels.
        """
        py5_module.push_matrix()
        self.push_transform(py5_module)
        py5_module.no_fill()
        py5_module.stroke(*colour)
        py5_module.stroke_weight(weight / max(self.scale, 0.001))
        py5_module.rect(0, 0, self.page.width_mm, self.page.height_mm)
        py5_module.pop_matrix()

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"page={self.page.name}, "
            f"canvas={self.canvas_w}x{self.canvas_h}px, "
            f"scale={self.scale:.3f}px/mm)"
        )
