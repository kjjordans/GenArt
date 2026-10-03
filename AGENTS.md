# GenArt -- Agent Notes

## Project

Generative pen-plotter art toolbox (Python 3.11+, hatchling build).
Core deps: numpy, vsketch, vpype, pillow.
Lint: ruff (line-length=100). Test: pytest.

## Conventions

- **Naming**: snake_case (functions, variables, files)
- **Docstrings**: Google style (Args:, Returns:, Raises:)
- **Testing**: pytest functions with plain asserts
- **Commits**: Conventional commits (feat:, fix:, docs:, refactor:, etc.)
- **Code style**: Keep code readable by an intermediate programmer. Avoid premature abstraction or clever patterns unless they add clear utility.
- Python: follow pyproject.toml settings (ruff format, mypy typing)
- Git commits: descriptive messages, one logical change per commit
- Keep output files under 10 MB; use Git LFS for large assets if needed
- `docs/` is built with MkDocs Material and auto-deploys to GitHub Pages

## Session Log

Session notes are kept in `notes/session_log.md`.


## Agent-specific notes

- **Hermes art bot:** research and documentation only. Writing goes in `docs/`.
- **OpenCode:** Focus on Coding. Focus on `src/`, `sketches/`, and `tests/`.
- **Sketch layout:** vsketch studies live in `sketches/vsketch/<name>/` and run
  from `.venv`; py5/Processing studies live in `sketches/processing/<name>/` and
  run from `.venv-py5`. Each sketch folder is self-contained with its own
  `config/` and `output/`. 
