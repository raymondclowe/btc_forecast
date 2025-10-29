Agent guidelines — concise and actionable

- Be concise: prefer short bullets over long prose.
- Save important learnings to `LEARNINGS.md` and check it before asking for help or searching online.

Environment & virtualenv (uv)

- Use the project-managed virtual environment. This repository uses the `uv` workflow by default.
- Run Python commands inside the project environment with `uv run <command>` to ensure correct dependencies and imports.
	- Examples: `uv run pytest -q`, `uv run python -c "import pkg; print(pkg.__version__)"`
- To add or sync dependencies: `uv add <package>` then `uv sync`.

Testing

- Use `pytest` for tests. Run tests with `uv run pytest` (or `uv run pytest -q` for quiet output).

Quick debugging tips

- Print raw API responses to inspect all keys and variations.
- Try multiple key formats or input variants when searching or when APIs return inconsistent shapes.

Troubleshooting

- ModuleNotFoundError under `uv run`: install the package into the project venv (`uv add <pkg>` → `uv sync`).
- If tests fail due to missing deps, ensure you're running them with `uv run pytest` so the project's venv is used.

Why this matters

- Running under the project's environment (via `uv run`) reproduces CI/dev expectations and avoids system-vs-project dependency mismatch.

Keep it short — update `LEARNINGS.md` frequently so the next person (or agent) doesn't repeat work.

