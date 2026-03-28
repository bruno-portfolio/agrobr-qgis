from __future__ import annotations

import contextlib

__all__ = ["queimadas"]

with contextlib.suppress(ImportError):
    from . import queimadas  # noqa: F401
