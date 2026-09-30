# Session Log

## 2026-09-26

### Completed
- Project review and architecture overview
- Created AGENTS.md with conventions
- Installed vsketch (1.2.0) and vpype (1.15.0) via pipx
- Set up `.venv` with `pip install -e ".[dev]"`
- Created `.python-version` (3.11.15)
- **Hello World sketch** — circle + cross through center
- **Study 02: Rosette** — working multi-layer parametric rose curve with sliders for amplitude, frequency, phase, layers, layer_scale, layer_rotation
- Learned: `vsk.translate()`, `vsk.scale("mm")`, `vsk.line()`, separating geometry functions from drawing code

### Preferences
- **Code style:** Keep code readable by an intermediate programmer. Avoid premature abstraction and clever patterns unless they add clear utility.

### Pending for next session
- Run ruff check on rosette sketch
- Next study: Study 04 — disturbed grid