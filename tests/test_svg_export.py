"""Tests for SVG export metadata sidecars."""

import importlib
import json
import sys
from types import ModuleType

import pytest

from plotter_art.py5_support.paperspace import PaperSpace


@pytest.fixture
def svg_export_module(monkeypatch):
    """Import the exporter with a lightweight py5 stub when needed."""
    module_name = "plotter_art.py5_support.svg_export"
    package = sys.modules["plotter_art.py5_support"]
    existing = sys.modules.get(module_name)
    if existing is not None:
        yield existing
        return

    monkeypatch.setitem(sys.modules, "py5", ModuleType("py5"))
    module = importlib.import_module(module_name)
    try:
        yield module
    finally:
        sys.modules.pop(module_name, None)
        if getattr(package, "svg_export", None) is module:
            delattr(package, "svg_export")


def test_metadata_is_written_to_same_basename_json(svg_export_module, tmp_path):
    """The sidecar pairs with the SVG and records its filename."""
    exporter = svg_export_module.SVGExporter(PaperSpace.preset("A4"))
    svg_path = tmp_path / "contours.svg"
    metadata = {
        "schema_version": 1,
        "sketch_name": "marching_squares",
        "parameters": {"seed": 42},
    }

    metadata_path = exporter._write_metadata(svg_path, metadata)

    assert metadata_path == tmp_path / "contours.json"
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == {
        **metadata,
        "svg_filename": "contours.svg",
    }
