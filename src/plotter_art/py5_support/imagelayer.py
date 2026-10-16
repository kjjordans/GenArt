"""ImageLayer - Raster image positioned and sampled relative to PaperSpace.

Loads a raster image (file, Pillow image, or array) and aligns it with
a PaperSpace page using a chosen fit mode. Provides drawing for py5
preview and sampling for algorithms such as marching squares.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np
from PIL import Image

from plotter_art.py5_support.paperspace import PaperSpace

FitMode = Literal["contain", "cover", "stretch"]


@dataclass(frozen=True, slots=True)
class ImagePlacement:
    """Computed placement of a source image on a PaperSpace page.

    Attributes:
        page: The associated PaperSpace.
        src_w: Source image width in pixels.
        src_h: Source image height in pixels.
        page_x: Top-left X in mm on the page.
        page_y: Top-left Y in mm on the page.
        page_w: Display width in mm on the page.
        page_h: Display height in mm on the page.
        fit: Fit mode used.
    """

    page: PaperSpace
    src_w: int
    src_h: int
    page_x: float
    page_y: float
    page_w: float
    page_h: float
    fit: FitMode

    @property
    def sample_scale_x(self) -> float:
        """Pixels per mm when sampling.

        Returns:
            Scale factor for mapping page X to source pixel X.
        """
        return self.src_w / self.page_w if self.page_w > 0 else 0.0

    @property
    def sample_scale_y(self) -> float:
        """Pixels per mm when sampling.

        Returns:
            Scale factor for mapping page Y to source pixel Y.
        """
        return self.src_h / self.page_h if self.page_h > 0 else 0.0

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"src={self.src_w}x{self.src_h}px, "
            f"page={self.page_w:.1f}x{self.page_h:.1f}mm @ "
            f"({self.page_x:.1f}, {self.page_y:.1f}), "
            f"fit={self.fit})"
        )


class ImageLayer:
    """Raster image aligned to a PaperSpace for preview and sampling.

    Attributes:
        placement: Computed placement transform.
        array: Source image as a grayscale numpy array (0..1 float).
    """

    def __init__(
        self,
        source: str | Path | Image.Image | np.ndarray,
        page: PaperSpace,
        *,
        fit: FitMode = "contain",
        opacity: float = 1.0,
        crop: tuple[float, float, float, float] | None = None,
    ):
        """Create an ImageLayer aligned to *page*.

        Args:
            source: Image file path, Pillow image, or ``(H, W)`` or
                ``(H, W, C)`` numpy array.
            page: The PaperSpace page to align to.
            fit: ``"contain"`` (fit within page, preserve ratio),
                ``"cover"`` (fill page, crop excess), or
                ``"stretch"`` (fill page exactly, allow distortion).
            opacity: Preview opacity (0..1).
            crop: Optional crop region as ``(x0, y0, x1, y1)``
                in page mm before fit. If omitted, the whole image is used.

        Raises:
            ValueError: If *fit* is not a valid mode or *source* is not
                recognisable as an image.
        """
        if fit not in ("contain", "cover", "stretch"):
            raise ValueError(f"fit must be 'contain', 'cover', or 'stretch', got {fit!r}")

        self.page = page
        self.fit = fit
        self.opacity = float(opacity)
        self.crop = crop

        # Load into a (H, W) float32 array in range [0, 1]
        self._array = self._load_array(source)
        self._h, self._w = self._array.shape

        # Compute placement on the page
        self.placement = self._compute_placement()
        self._buffered = False
        self._py5_image = None

    # ------------------------------------------------------------------ #
    # Loading
    # ------------------------------------------------------------------ #

    @staticmethod
    def _load_array(source: str | Path | Image.Image | np.ndarray) -> np.ndarray:
        if isinstance(source, (str, Path)):
            img = Image.open(str(source)).convert("L")
            return np.array(img, dtype=np.float32) / 255.0

        if isinstance(source, Image.Image):
            return np.array(source.convert("L"), dtype=np.float32) / 255.0

        if isinstance(source, np.ndarray):
            arr = np.asarray(source, dtype=np.float32)
            if arr.ndim == 3:
                arr = arr[..., 0] if arr.shape[2] <= 4 else arr
            if arr.ndim == 2:
                if arr.max() > 1.0:
                    arr = arr / arr.max()
                return arr
            raise ValueError(f"Unsupported array shape: {arr.shape}")

        raise ValueError(f"Cannot load image from type {type(source)}")

    # ------------------------------------------------------------------ #
    # Placement computation
    # ------------------------------------------------------------------ #

    def _compute_placement(self) -> ImagePlacement:
        src_w, src_h = self._w, self._h
        page_w = self.page.width_mm
        page_h = self.page.height_mm

        if self.fit == "stretch":
            return ImagePlacement(
                page=self.page,
                src_w=src_w,
                src_h=src_h,
                page_x=0.0,
                page_y=0.0,
                page_w=page_w,
                page_h=page_h,
                fit="stretch",
            )

        src_ratio = src_w / src_h
        page_ratio = page_w / page_h if page_h > 0 else 1.0

        if self.fit == "contain":
            if src_ratio > page_ratio:
                # Source wider relative to page -> width constrained
                pw = page_w
                ph = pw / src_ratio
                px = 0.0
                py = (page_h - ph) / 2.0
            else:
                # Source taller relative to page -> height constrained
                ph = page_h
                pw = ph * src_ratio
                px = (page_w - pw) / 2.0
                py = 0.0
            return ImagePlacement(
                page=self.page,
                src_w=src_w,
                src_h=src_h,
                page_x=px,
                page_y=py,
                page_w=pw,
                page_h=ph,
                fit="contain",
            )

        # "cover"
        if src_ratio > page_ratio:
            # Source wider -> height constrained, width crops
            ph = page_h
            pw = ph * src_ratio
            px = (page_w - pw) / 2.0
            py = 0.0
        else:
            # Source taller -> width constrained, height crops
            pw = page_w
            ph = pw / src_ratio
            px = 0.0
            py = (page_h - ph) / 2.0
        return ImagePlacement(
            page=self.page,
            src_w=src_w,
            src_h=src_h,
            page_x=px,
            page_y=py,
            page_w=pw,
            page_h=ph,
            fit="cover",
        )

    # ------------------------------------------------------------------ #
    # Sampling
    # ------------------------------------------------------------------ #

    def sample(
        self,
        x_mm: float,
        y_mm: float,
        *,
        method: Literal["nearest", "bilinear"] = "bilinear",
        outside_value: float | None = 0.0,
    ) -> float | None:
        """Sample the image at a page-space mm location.

        Args:
            x_mm: Page X coordinate in mm.
            y_mm: Page Y coordinate in mm.
            method: ``"nearest"`` for exact-pixel sampling, ``"bilinear"``
                for interpolated sampling.
            outside_value: Value returned when the point lies outside
                the placed image bounds. ``None`` means return ``None``.

        Returns:
            Grayscale intensity in range ``[0, 1]``, or *outside_value* / ``None``.
        """
        placement = self.placement

        # Check bounds
        if x_mm < placement.page_x or x_mm > placement.page_x + placement.page_w:
            return outside_value
        if y_mm < placement.page_y or y_mm > placement.page_y + placement.page_h:
            return outside_value

        # Map to source pixels
        src_x = (x_mm - placement.page_x) * placement.sample_scale_x
        src_y = (y_mm - placement.page_y) * placement.sample_scale_y

        if method == "nearest":
            ix = round(src_x)
            iy = round(src_y)
            if ix < 0 or ix >= self._w or iy < 0 or iy >= self._h:
                return outside_value
            return float(self._array[iy, ix])

        # Bilinear
        ix0 = int(np.floor(src_x))
        iy0 = int(np.floor(src_y))
        ix1 = ix0 + 1
        iy1 = iy0 + 1

        # Clamp
        ix0 = max(0, min(ix0, self._w - 1))
        ix1 = max(0, min(ix1, self._w - 1))
        iy0 = max(0, min(iy0, self._h - 1))
        iy1 = max(0, min(iy1, self._h - 1))

        fx = src_x - ix0
        fy = src_y - iy0

        v00 = self._array[iy0, ix0]
        v10 = self._array[iy0, ix1]
        v01 = self._array[iy1, ix0]
        v11 = self._array[iy1, ix1]

        top = v00 * (1 - fx) + v10 * fx
        bot = v01 * (1 - fx) + v11 * fx
        return float(top * (1 - fy) + bot * fy)

    # ------------------------------------------------------------------ #
    # py5 preview drawing
    # ------------------------------------------------------------------ #

    def draw_preview(
        self,
        py5_module,
        *,
        viewport=None,
        tint: tuple[int, ...] | None = None,
    ) -> None:
        """Draw the image onto the py5 canvas.

        If a Viewport is provided, the image is drawn through the
        page-to-screen transform. Otherwise it is drawn in page mm
        coordinates directly (use with an active viewport transform).

        Args:
            py5_module: The py5 module.
            viewport: Optional Viewport for screen-space fitting.
            tint: Optional ``(gray,)`` or ``(r, g, b)`` tint colour.
        """
        # Build/update cached py5 image if needed
        if self._py5_image is None or not self._buffered:
            arr_u8 = np.rint(np.clip(self._array, 0.0, 1.0) * 255).astype(np.uint8)
            self._py5_image = py5_module.create_image_from_numpy(arr_u8, "L")
            self._buffered = True

        py5_module.push_matrix()
        if viewport is not None:
            viewport.push_transform(py5_module)

        # Draw at placement position in page coordinates
        placement = self.placement
        if self.opacity < 1.0:
            py5_module.tint(255, int(self.opacity * 255))
        elif tint is not None:
            if len(tint) == 1:
                py5_module.tint(tint[0])
            else:
                py5_module.tint(*tint)

        py5_module.image(
            self._py5_image,
            placement.page_x,
            placement.page_y,
            placement.page_w,
            placement.page_h,
        )

        py5_module.no_tint()
        py5_module.pop_matrix()

    # ------------------------------------------------------------------ #
    # Access
    # ------------------------------------------------------------------ #

    @property
    def array(self) -> np.ndarray:
        """Grayscale source array in range ``[0, 1]``."""
        return self._array

    @property
    def shape(self) -> tuple[int, int]:
        """Shape (height, width) of the source array in pixels."""
        return self._h, self._w

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"page={self.placement.page.name}, "
            f"fit={self.fit}, "
            f"src={self._w}x{self._h}px, "
            f"opacity={self.opacity})"
        )
