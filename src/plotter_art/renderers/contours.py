"""Reusable styles for drawing scalar-field contours."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContourStyle:
    """Style for one contour level.

    Attributes:
        level: Scalar-field value at which to draw the contour.
        stroke_rgb: RGB stroke colour, with each channel from 0 to 255.
        stroke_width_mm: Stroke width in millimetres.
    """

    level: float
    stroke_rgb: tuple[int, int, int]
    stroke_width_mm: float = 0.5


DEFAULT_CONTOUR_STYLES = (
    ContourStyle(0.2, (230, 70, 70)),
    ContourStyle(0.35, (230, 150, 50)),
    ContourStyle(0.5, (70, 170, 100)),
    ContourStyle(0.65, (60, 130, 220)),
    ContourStyle(0.8, (170, 90, 200)),
)
