"""Tests for Viewport."""

import pytest

from plotter_art.py5_support.paperspace import PaperSpace
from plotter_art.py5_support.viewport import Viewport


class TestFit:
    def test_a4_portrait_in_900x700(self):
        page = PaperSpace.preset("A4", orientation="portrait")
        vp = Viewport.fit(page, canvas_w=900, canvas_h=700)
        assert vp.page is page
        assert vp.canvas_w == 900
        assert vp.canvas_h == 700
        # A4 is tall; should be height-constrained
        expected_scale = (700 - 40) / 297.0
        assert vp.scale == pytest.approx(expected_scale)

    def test_a4_landscape_in_900x700(self):
        page = PaperSpace.preset("A4", orientation="landscape")
        vp = Viewport.fit(page, canvas_w=900, canvas_h=700)
        # A4 landscape is wide; should be width-constrained
        expected_scale = (900 - 40) / 297.0
        assert vp.scale == pytest.approx(expected_scale)

    def test_viewport_has_offsets(self):
        page = PaperSpace.custom(100, 100, unit="mm")
        vp = Viewport.fit(page, canvas_w=200, canvas_h=200)
        assert vp.offset_x > 0
        assert vp.offset_y > 0


class TestToScreen:
    def test_origin(self):
        page = PaperSpace.custom(100, 100, unit="mm")
        vp = Viewport.fit(page, canvas_w=200, canvas_h=200, margin_pixels=0)
        sx, sy = vp.to_screen(0, 0)
        assert sx == pytest.approx(vp.offset_x)
        assert sy == pytest.approx(vp.offset_y)

    def test_page_corner(self):
        page = PaperSpace.custom(100, 100, unit="mm")
        vp = Viewport.fit(page, canvas_w=200, canvas_h=200, margin_pixels=0)
        sx, sy = vp.to_screen(100, 100)
        assert sx == pytest.approx(vp.offset_x + 100 * vp.scale)
        assert sy == pytest.approx(vp.offset_y + 100 * vp.scale)


class TestToPage:
    def test_roundtrip(self):
        page = PaperSpace.custom(100, 100, unit="mm")
        vp = Viewport.fit(page, canvas_w=200, canvas_h=200, margin_pixels=10)
        x_mm, y_mm = 33.3, 66.7
        sx, sy = vp.to_screen(x_mm, y_mm)
        px, py = vp.to_page(sx, sy)
        assert px == pytest.approx(x_mm)
        assert py == pytest.approx(y_mm)


class TestMargin:
    def test_margin_affects_scale(self):
        page = PaperSpace.custom(100, 100, unit="mm")
        vp0 = Viewport.fit(page, canvas_w=300, canvas_h=300, margin_pixels=0)
        vp20 = Viewport.fit(page, canvas_w=300, canvas_h=300, margin_pixels=20)
        assert vp20.scale < vp0.scale
