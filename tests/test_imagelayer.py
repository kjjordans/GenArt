"""Tests for ImageLayer's py5 preview conversion."""

import numpy as np

from plotter_art.py5_support.imagelayer import ImageLayer
from plotter_art.py5_support.paperspace import PaperSpace


class FakePy5:
    """Small py5 stand-in for testing the preview image conversion."""

    def __init__(self):
        self.converted_images = []
        self.drawn_images = []

    def create_image_from_numpy(self, array, bands):
        self.converted_images.append((array.copy(), bands))
        return object()

    def push_matrix(self):
        pass

    def pop_matrix(self):
        pass

    def image(self, image, x, y, width, height):
        self.drawn_images.append((image, x, y, width, height))

    def no_tint(self):
        pass


def test_draw_preview_converts_grayscale_array_once():
    """The preview converts to uint8 grayscale and reuses the cached image."""
    source = np.array([[0.0, 0.5], [1.0, 0.25]], dtype=np.float32)
    image_layer = ImageLayer(source, PaperSpace.preset("A4"))
    fake_py5 = FakePy5()

    image_layer.draw_preview(fake_py5)
    image_layer.draw_preview(fake_py5)

    converted, bands = fake_py5.converted_images[0]
    assert converted.dtype == np.uint8
    assert converted.tolist() == [[0, 128], [255, 64]]
    assert bands == "L"
    assert len(fake_py5.converted_images) == 1
    assert len(fake_py5.drawn_images) == 2
