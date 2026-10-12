"""Controls - Tkinter parameter window for py5 sketches.

Provides a reusable slider panel and button bar for live parameter control.
State is managed through a small mapping object that the sketch reads each frame.
"""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ParamDef:
    """Definition of a single numeric parameter.

    Attributes:
        key: Machine identifier used in the state dict.
        label: Human-readable label for the slider.
        lo: Minimum value.
        hi: Maximum value.
        step: Slider resolution.
        is_int: Whether the value is an integer.
        default: Starting value. If omitted, ``lo`` is used.
    """

    key: str
    label: str
    lo: float
    hi: float
    step: float
    is_int: bool
    default: float | None = None


class ParameterState(dict):
    """Live parameter state backed by a dictionary.

    Provides convenience construction from ``ParamDef``
    objects and typed accessors.

    Example:
        >>> defs = [ParamDef("freq", "Frequency", 0.0, 1.0, 0.01, False)]
        >>> state = ParameterState.from_defs(defs, initial={"freq": 0.15})
        >>> state.float("freq")
        0.15
    """

    @classmethod
    def from_defs(
        cls,
        definitions: list[ParamDef],
        *,
        initial: dict[str, Any] | None = None,
    ) -> ParameterState:
        """Build a state from parameter definitions.

        Args:
            definitions: List of ``ParamDef`` values.
            initial: Optional overrides for starting values.

        Returns:
            A ``ParameterState`` with all defaults set.
        """
        state = cls()
        for d in definitions:
            val = initial.get(d.key) if initial and d.key in initial else d.default
            if val is None:
                val = d.lo
            state[d.key] = int(val) if d.is_int else float(val)
        return state

    def int(self, key: str) -> int:
        """Return *key* as an int."""
        return int(self[key])

    def float(self, key: str) -> float:
        """Return *key* as a float."""
        return float(self[key])

    def update(self, key: str, value: float | int) -> None:  # type: ignore[override]
        """Update a parameter value in-place."""
        self[key] = value


def build_controls(
    state: ParameterState,
    params: list[ParamDef],
    *,
    buttons: dict[str, Callable[[], Any]] | None = None,
    title: str = "Parameters",
) -> tk.Tk:
    """Create a Tkinter window with a slider per parameter.

    Args:
        state: Live parameter state to update as sliders move.
        params: Parameter definitions (order determines display order).
        buttons: Optional mapping of button label to callback.
            ``{"Export SVG": do_export}`` renders one button per entry.
        title: Window title.

    Returns:
        The root ``tk.Tk`` widget. Call ``root.mainloop()`` to run.
    """
    root = tk.Tk()
    root.title(title)

    for p in params:
        row = tk.Frame(root)
        row.pack(fill="x", padx=8, pady=2)

        tk.Label(row, text=p.label, width=12, anchor="w").pack(side="left")
        value_label = tk.Label(row, width=6, anchor="e")

        def on_change(val, key=p.key, is_int=p.is_int, vl=value_label):
            value = round(float(val)) if is_int else round(float(val), 3)
            state.update(key, value)
            vl.config(text=f"{value:g}")

        scale = tk.Scale(
            row,
            from_=p.lo,
            to=p.hi,
            resolution=p.step,
            orient="horizontal",
            showvalue=False,
            command=on_change,
            length=200,
        )
        scale.set(state.get(p.key, p.default if p.default is not None else p.lo))
        scale.pack(side="left", fill="x", expand=True)

        current = state.get(p.key, p.default if p.default is not None else p.lo)
        fmt = "{:.0f}" if p.is_int else "{:g}"
        value_label.config(text=fmt.format(current))
        value_label.pack(side="right")

    if buttons:
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=8, pady=6)
        for label, cb in buttons.items():
            tk.Button(btn_frame, text=label, command=cb).pack(side="left", padx=4)

    return root
