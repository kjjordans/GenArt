"""Contour extraction from scalar fields using the marching-squares algorithm."""

from collections.abc import Callable, Sequence


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between *a* and *b*."""
    return a + t * (b - a)


def _interp_edge(
    low_pos: float,
    high_pos: float,
    low_val: float,
    high_val: float,
    threshold: float,
) -> float:
    """Return the interpolated position where the field crosses *threshold*.

    The result lies between *low_pos* and *high_pos*.  If both values are
    equal, the midpoint is returned as a safe fallback.
    """
    if high_val == low_val:
        return (low_pos + high_pos) / 2.0
    t = (threshold - low_val) / (high_val - low_val)
    return _lerp(low_pos, high_pos, t)


def marching_squares(
    field: Callable[[float, float], float],
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    cols: int,
    rows: int,
    levels: Sequence[float],
) -> dict[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """Extract contour line segments from a scalar field.

    For each level in *levels*, the field is evaluated on a regular grid
    and the classic marching-squares cases are used to generate line
    segments where the field crosses the level.

    Ambiguous saddle cases (cases 5 and 10) are resolved by comparing the
    average of the four corner values to the threshold.

    Args:
        field: Function ``f(x, y) -> float``.
        x_min, x_max: Horizontal extents of the sampled region.
        y_min, y_max: Vertical extents of the sampled region.
        cols: Number of grid columns (cells).
        rows: Number of grid rows (cells).
        levels: Contour levels to extract.

    Returns:
        A dict mapping each level to a list of line segments.  Each
        segment is ``((x1, y1), (x2, y2))``.
    """
    dx = (x_max - x_min) / cols
    dy = (y_max - y_min) / rows

    # Pre-sample corner values on a (cols+1) x (rows+1) grid.
    values: list[list[float]] = []
    for j in range(rows + 1):
        row_vals: list[float] = []
        y = y_min + j * dy
        for i in range(cols + 1):
            x = x_min + i * dx
            row_vals.append(field(x, y))
        values.append(row_vals)

    result: dict[float, list[tuple[tuple[float, float], tuple[float, float]]]] = {
        level: [] for level in levels
    }

    for j in range(rows):
        y_bot = y_min + j * dy
        y_top = y_bot + dy
        for i in range(cols):
            x_left = x_min + i * dx
            x_right = x_left + dx

            v0 = values[j][i]  # bottom-left
            v1 = values[j][i + 1]  # bottom-right
            v2 = values[j + 1][i + 1]  # top-right
            v3 = values[j + 1][i]  # top-left

            for level in levels:
                b0 = 1 if v0 > level else 0
                b1 = 1 if v1 > level else 0
                b2 = 1 if v2 > level else 0
                b3 = 1 if v3 > level else 0
                case = (b3 << 3) | (b2 << 2) | (b1 << 1) | b0

                if case in (0, 15):
                    continue

                # Edge crossing points (computed on demand per case).
                # Bottom edge: between v0 and v1.
                bottom = _interp_edge(x_left, x_right, v0, v1, level)
                # Right edge: between v1 and v2.
                right = _interp_edge(y_bot, y_top, v1, v2, level)
                # Top edge: between v3 and v2.
                top = _interp_edge(x_left, x_right, v3, v2, level)
                # Left edge: between v0 and v3.
                left = _interp_edge(y_bot, y_top, v0, v3, level)

                # Resolve ambiguous saddle cases using the cell-centre average.
                if case in (5, 10):
                    centre = (v0 + v1 + v2 + v3) / 4.0
                    if centre > level:
                        case = 5 if case == 5 else 10
                    else:
                        case = 10 if case == 5 else 5

                segs: list[tuple[tuple[float, float], tuple[float, float]]] = []
                if case == 1:
                    segs.append(((x_left, left), (bottom, y_bot)))
                elif case == 2:
                    segs.append(((bottom, y_bot), (x_right, right)))
                elif case == 3:
                    segs.append(((x_left, left), (x_right, right)))
                elif case == 4:
                    segs.append(((top, y_top), (x_right, right)))
                elif case == 5:
                    segs.append(((x_left, left), (top, y_top)))
                    segs.append(((bottom, y_bot), (x_right, right)))
                elif case == 6:
                    segs.append(((bottom, y_bot), (top, y_top)))
                elif case in (7, 8):
                    segs.append(((x_left, left), (top, y_top)))
                elif case == 9:
                    segs.append(((bottom, y_bot), (top, y_top)))
                elif case == 10:
                    segs.append(((x_left, left), (bottom, y_bot)))
                    segs.append(((top, y_top), (x_right, right)))
                elif case == 11:
                    segs.append(((top, y_top), (x_right, right)))
                elif case == 12:
                    segs.append(((x_left, left), (top, y_top)))
                elif case == 13:
                    segs.append(((bottom, y_bot), (x_right, right)))
                elif case == 14:
                    segs.append(((x_left, left), (bottom, y_bot)))

                result[level].extend(segs)

    return result
