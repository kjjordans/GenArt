"""Tests for PaperSpace."""

import pytest

from plotter_art.py5_support.paperspace import PaperSpace, cm


class TestPreset:
    def test_a4_portrait(self):
        page = PaperSpace.preset("A4", orientation="portrait")
        assert page.width_mm == 210.0
        assert page.height_mm == 297.0
        assert page.name == "A4 portrait"

    def test_a4_landscape(self):
        page = PaperSpace.preset("A4", orientation="landscape")
        assert page.width_mm == 297.0
        assert page.height_mm == 210.0

    def test_a3_portrait(self):
        page = PaperSpace.preset("A3", orientation="portrait")
        assert page.width_mm == 297.0
        assert page.height_mm == 420.0

    def test_a0_largest(self):
        page = PaperSpace.preset("A0", orientation="portrait")
        assert page.width_mm == 841.0
        assert page.height_mm == 1189.0

    def test_a6_smallest(self):
        page = PaperSpace.preset("A6", orientation="portrait")
        assert page.width_mm == 105.0
        assert page.height_mm == 148.0

    def test_unknown_preset(self):
        with pytest.raises(ValueError, match="Unknown preset"):
            PaperSpace.preset("A10")

    def test_invalid_orientation(self):
        with pytest.raises(ValueError, match="orientation"):
            PaperSpace.preset("A4", orientation="square")


class TestCustom:
    def test_mm(self):
        page = PaperSpace.custom(200, 150, unit="mm")
        assert page.width_mm == 200.0
        assert page.height_mm == 150.0

    def test_cm(self):
        page = PaperSpace.custom(20, 15, unit="cm")
        assert page.width_mm == 200.0
        assert page.height_mm == 150.0

    def test_custom_name(self):
        page = PaperSpace.custom(100, 100, unit="mm", name="Square")
        assert page.name == "Square"

    def test_default_name(self):
        page = PaperSpace.custom(200, 100, unit="mm")
        assert "200" in page.name
        assert "100" in page.name

    def test_zero_width(self):
        with pytest.raises(ValueError, match="positive"):
            PaperSpace.custom(0, 100)

    def test_negative_height(self):
        with pytest.raises(ValueError, match="positive"):
            PaperSpace.custom(100, -10)

    def test_invalid_unit(self):
        with pytest.raises(ValueError, match="unit"):
            PaperSpace.custom(100, 100, unit="inches")


class TestCmHelper:
    def test_cm_conversion(self):
        assert cm(2) == 20.0
        assert cm(0.5) == 5.0


class TestAspectRatio:
    def test_portrait_less_than_one(self):
        page = PaperSpace.preset("A4", orientation="portrait")
        assert page.aspect_ratio == pytest.approx(210 / 297)

    def test_landscape_greater_than_one(self):
        page = PaperSpace.preset("A4", orientation="landscape")
        assert page.aspect_ratio == pytest.approx(297 / 210)

    def test_square(self):
        page = PaperSpace.custom(100, 100, unit="mm")
        assert page.aspect_ratio == 1.0
