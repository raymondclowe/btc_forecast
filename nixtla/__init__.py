"""Minimal shim package to satisfy editable build during `uv sync`.

This repo's pyproject.toml expects a package named `nixtla` and
reads `nixtla.__version__` dynamically when building in editable mode.
Some cleanup removed the original package; create a tiny shim that
exposes a version so `uv sync` can succeed. This file is intentionally
small and safe; it can be replaced by the real package later.
"""
__version__ = "0.0.0"
