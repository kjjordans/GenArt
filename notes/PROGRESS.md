# Progress Memory

Living project memory. Updated as work happens. Keep entries short and factual.
Source of truth for the plan is `study_plan.md`; this file tracks **actual state**.

Last updated: 2026-09-29

## How to use this file

- **Status** — where the project is right now.
- **Works** — verified, don't re-litigate.
- **Doesn't work / gotchas** — failed attempts and traps. Add the error, not just "didn't work".
- **Decisions** — choices made and why, so we don't churn.
- **Next** — the immediate queue.
- **Session log** — append-only; newest at top.

When something is resolved, move it out of "Doesn't work" and note the fix in the session log.

## Status

- Phase: **Stage 0 — Foundation**. Scaffolding complete, no studies started.
- Studies 01–12: **all pending**.
- Package `plotter_art` imports; module subpackages exist but are empty (`__init__.py` only).
- No sketches, outputs, or algorithm notes yet.

## Works

- `pip`/venv setup via `.venv`.
- `pytest` baseline: **2 passed** (`tests/test_smoke.py`) — verifies `plotter_art` imports and core deps (`numpy`, `PIL`, `vsketch`, `vpype`) import. (Verified 2026-09-29.)
- Package layout scaffolded under `src/plotter_art/{geometry,transforms,fields,samplers,image,systems,renderers,utils}`.
- Tooling declared in `pyproject.toml`: dependencies `numpy`, `vsketch`, `vpype`, `pillow`; dev extras `pytest`, `ruff`; pytest `testpaths=["tests"]`; ruff line-length 100.

## Doesn't work / gotchas

- Nothing broken yet. Add failures here as they happen, with the exact error and command.

## Decisions

- Package/project name is `genart` (dir `GenArt`); import package is `plotter_art`.
- Millimetres are the project-level physical unit (per `study_plan.md`).
- Follow the "start lightly" rule: only add a module once two or more sketches need it.
- Randomness must come from an explicit seed; no hidden module-level random state.

## Next

1. Study 01 — plotter calibration sheet: page border, safe plotting rectangle, spacing ladder, pen/speed test; one known-good SVG + GRBL G-code; document machine origin/placement/sender settings.
2. Study 02 — parameterised rosette per `study_plan.md` §9 acceptance criteria.
3. Add the first real modules only as studies need them (likely `utils` for seeding/page bounds, `geometry` for curve sampling).

## Session log

- **2026-09-29** — Created this memory file. Inspected repo: scaffold + study plan only, studies not started. Ran `pytest` → 2 passed. No code changes other than adding this file.