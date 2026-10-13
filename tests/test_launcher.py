"""Tests for the py5 sketch launcher."""

import importlib
import sys
from types import ModuleType

import pytest

from plotter_art.py5_support.controls import ParamDef
from plotter_art.py5_support.paperspace import PaperSpace


@pytest.fixture
def launcher_module(monkeypatch):
    """Import the launcher with a lightweight py5 stub when py5 is unavailable."""
    module_name = "plotter_art.py5_support.launcher"
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
        if getattr(package, "launcher", None) is module:
            delattr(package, "launcher")


def test_run_sketch_requires_state_when_params_are_provided(monkeypatch, launcher_module):
    """Reject slider configuration before attempting to launch py5."""
    monkeypatch.setattr(
        launcher_module.py5,
        "run_sketch",
        lambda **kwargs: pytest.fail("py5 sketch should not launch for invalid arguments"),
        raising=False,
    )

    page = PaperSpace.preset("A4")
    params = [ParamDef("radius", "Radius", 1, 10, 1, True)]

    with pytest.raises(ValueError, match="state is required"):
        launcher_module.run_sketch(page=page, draw=lambda: None, params=params)
