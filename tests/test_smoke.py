"""Smoke tests verifying the package and its core import stack."""

import importlib

import plotter_art


def test_package_importable():
    assert plotter_art.__version__


def test_core_dependencies_importable():
    for name in ("numpy", "PIL", "vsketch", "vpype"):
        importlib.import_module(name)
