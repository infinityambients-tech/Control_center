from __future__ import annotations

import importlib.util
import logging
from pathlib import Path
from types import ModuleType
from typing import Callable

from fastapi import FastAPI

logger = logging.getLogger(__name__)


def load_plugins(app: FastAPI, plugins_dir: Path) -> list[str]:
    """
    Loads plugins from a folder. Each plugin is a .py file exporting `register(app)`.
    Returns list of loaded plugin names.
    """
    loaded: list[str] = []
    if not plugins_dir.exists() or not plugins_dir.is_dir():
        return loaded

    for path in sorted(plugins_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue

        mod = _load_module_from_path(path)
        register = getattr(mod, "register", None)
        if callable(register):
            try:
                register(app)
                loaded.append(path.stem)
            except Exception:
                logger.exception("Plugin register() failed: %s", path.name)
        else:
            logger.warning("Plugin missing register(app): %s", path.name)
    return loaded


def _load_module_from_path(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"control_center_plugin_{path.stem}", path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot import plugin: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module

