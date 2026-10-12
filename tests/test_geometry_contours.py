"""Tests for contour extraction."""

from plotter_art.geometry.contours import marching_squares


def test_flat_field_returns_empty():
    """A constant field should create no contour segments."""
    def flat(x: float, y: float) -> float:
        return 1.0

    result = marching_squares(flat, 0.0, 10.0, 0.0, 10.0, 4, 4, [0.5, 1.5, 2.5])
    assert all(len(segs) == 0 for segs in result.values())


def test_ramp_field_produces_segments():
    """A linear ramp should create at least one segment for a level in range."""
    def ramp(x: float, y: float) -> float:
        return x + y

    result = marching_squares(ramp, 0.0, 10.0, 0.0, 10.0, 8, 8, [5.0])
    assert len(result[5.0]) > 0


def test_multiple_levels():
    """Output should contain an entry for every requested level."""
    def ramp(x: float, y: float) -> float:
        return x

    levels = [2.0, 4.0, 6.0]
    result = marching_squares(ramp, 0.0, 10.0, 0.0, 10.0, 5, 5, levels)
    assert set(result.keys()) == set(levels)
