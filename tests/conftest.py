from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _reset_registry():
    yield
    try:
        from agrobr_qgis.core.registry import SourceRegistry

        SourceRegistry.clear()
    except ImportError:
        pass
