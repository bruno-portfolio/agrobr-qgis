from __future__ import annotations

import contextlib
import importlib

__all__ = [
    "queimadas",
    "desmatamento",
    "funai",
    "icmbio",
    "incra",
    "ibama",
    "ana",
    "sfb",
    "mapbiomas_alerta",
    "sicar",
    "conab",
    "ibge",
    "zarc",
]

for _name in __all__:
    with contextlib.suppress(ImportError):
        importlib.import_module(f".{_name}", __package__)
