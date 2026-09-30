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

---

## 2026-09-30

### Completed
- Added code style preference to AGENTS.md and session log
- **Study 03: Harmonograph** — dual-pendulum damped harmonograph with frequency, phase, amplitude, damping, sample count, and dt parameters
  - Removed no-op `1.0 *` factors
  - Phases converted to degrees with `math.radians()`
  - Removed `reloop` from finalize (harmless but unnecessary for open spiral)
  - Ruff clean
- Decided against extracting `sample_parametric` helper — not enough utility yet (preference: no premature abstraction)

### Pending for next session
- **Study 04: Disturbed grid** (Vera Molnár–style)
  - Grid of squares with seeded jitter (position, rotation, scale)
  - Finalize shape choice (square/circle/diamond)
  - Decide whether to start with position-only jitter or all three