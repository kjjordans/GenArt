"""PaperSpace - Physical page model for py5 sketches.

Defines a physical page in millimetres with standard ISO presets,
available in portrait or landscape orientation. Coordinates and
dimensions within a PaperSpace are always in mm, independent of
on-screen pixel display.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# ISO A-series dimensions in mm (width × height for portrait)
_ISO_A_PRESETS: dict[str, tuple[float, float]] = {
    "A6": (105.0, 148.0),
    "A5": (148.0, 210.0),
    "A4": (210.0, 297.0),
    "A3": (297.0, 420.0),
    "A2": (420.0, 594.0),
    "A1": (594.0, 841.0),
    "A0": (841.0, 1189.0),
}

# Valid orientations
Orientation = Literal["portrait", "landscape"]
# Valid units
Unit = Literal["mm", "cm"]


def cm(value: float) -> float:
    """Convert centimetres to millimetres.

    Args:
        value: Length in centimetres.

    Returns:
        Equivalent length in millimetres.
    """
    return float(value) * 10.0


@dataclass(frozen=True, slots=True)
class PaperSpace:
    """A physical page in millimetres.

    Attributes:
        width_mm: Page width in millimetres.
        height_mm: Page height in millimetres.
        name: Human-readable name for this page.
    """

    width_mm: float
    height_mm: float
    name: str

    # ------------------------------------------------------------------ #
    # Constructors
    # ------------------------------------------------------------------ #

    @classmethod
    def preset(
        cls,
        name: str,
        *,
        orientation: Orientation = "portrait",
    ) -> PaperSpace:
        """Create a PaperSpace from a standard ISO A-series preset.

        Supported presets: A0 through A6.

        Args:
            name: Preset name such as "A4", "A3", or "A2".
            orientation: Page orientation. ``portrait`` keeps the
                original width < height, while ``landscape`` swaps them.
                Square presets are unaffected.

        Returns:
            A new ``PaperSpace`` configured for the preset and orientation.

        Raises:
            ValueError: If *name* is not a known ISO preset or *orientation*
                is not ``"portrait"`` or ``"landscape"``.

        Example:
            >>> page = PaperSpace.preset("A4", orientation="landscape")
            >>> page.width_mm
            297.0
        """
        if orientation not in ("portrait", "landscape"):
            raise ValueError(f"orientation must be 'portrait' or 'landscape', got {orientation!r}")

        key = name.upper()
        if key not in _ISO_A_PRESETS:
            valid = ", ".join(sorted(_ISO_A_PRESETS))
            raise ValueError(f"Unknown preset {name!r}. Valid: {valid}")

        w, h = _ISO_A_PRESETS[key]
        if orientation == "landscape":
            w, h = h, w
        return cls(width_mm=w, height_mm=h, name=f"{key} {orientation}")

    @classmethod
    def custom(
        cls,
        width: float,
        height: float,
        *,
        unit: Unit = "mm",
        name: str | None = None,
    ) -> PaperSpace:
        """Create a PaperSpace from arbitrary dimensions.

        Args:
            width: Page width.
            height: Page height.
            unit: ``"mm"`` or ``"cm"``.
            name: Optional display name. If omitted, a default is generated.

        Returns:
            A new ``PaperSpace`` with the requested dimensions.

        Raises:
            ValueError: If *width* or *height* is non-positive, or *unit* is
                not ``"mm"`` or ``"cm"``.

        Example:
            >>> page = PaperSpace.custom(20, 20, unit="cm", name="Square20")
            >>> page.width_mm
            200.0
        """
        if unit not in ("mm", "cm"):
            raise ValueError(f"unit must be 'mm' or 'cm', got {unit!r}")
        if width <= 0 or height <= 0:
            raise ValueError(f"width and height must be positive, got {width!r}×{height!r}")

        factor = 1.0 if unit == "mm" else 10.0
        w = float(width) * factor
        h = float(height) * factor

        auto_name = name or f"{width:g}×{height:g}{unit}"
        return cls(width_mm=w, height_mm=h, name=auto_name)

    # ------------------------------------------------------------------ #
    # Convenience
    # ------------------------------------------------------------------ #

    @property
    def aspect_ratio(self) -> float:
        """Page aspect ratio (width_mm / height_mm)."""
        return self.width_mm / self.height_mm if self.height_mm else 1.0

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"width={self.width_mm:.1f}mm, "
            f"height={self.height_mm:.1f}mm, "
            f"name={self.name!r})"
        )
