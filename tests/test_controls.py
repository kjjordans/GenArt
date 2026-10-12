"""Tests for ParameterState and ParamDef."""

from plotter_art.py5_support.controls import ParamDef, ParameterState


class TestParamDef:
    def test_creation(self):
        p = ParamDef("freq", "Frequency", 0.0, 1.0, 0.01, False)
        assert p.key == "freq"
        assert p.label == "Frequency"
        assert p.default is None


class TestParameterStateFromDefs:
    def test_defaults_from_lo(self):
        defs = [
            ParamDef("freq", "Frequency", 0.0, 1.0, 0.01, False),
            ParamDef("seed", "Seed", 0, 100, 1, True),
        ]
        state = ParameterState.from_defs(defs)
        assert state.float("freq") == 0.0
        assert state.int("seed") == 0

    def test_initial_overrides(self):
        defs = [ParamDef("freq", "Frequency", 0.0, 1.0, 0.01, False, default=0.15)]
        state = ParameterState.from_defs(defs, initial={"freq": 0.5})
        assert state.float("freq") == 0.5

    def test_default_from_def(self):
        defs = [ParamDef("freq", "Frequency", 0.0, 1.0, 0.01, False, default=0.15)]
        state = ParameterState.from_defs(defs)
        assert state.float("freq") == 0.15


class TestParameterStateAccessors:
    def test_float(self):
        state = ParameterState()
        state["val"] = 0.75
        assert state.float("val") == 0.75

    def test_int(self):
        state = ParameterState()
        state["val"] = 42
        assert state.int("val") == 42

    def test_int_from_float(self):
        state = ParameterState()
        state["val"] = 3.7
        assert state.int("val") == 3

    def test_update(self):
        state = ParameterState()
        state.update("key", 123)
        assert state["key"] == 123
