from __future__ import annotations

import importlib
import sys
from unittest.mock import MagicMock

import pandas as pd
import pytest

from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import SourceCapability, SourceCategory

_SOURCE_MODULES = [
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
    "cepea",
    "conab",
    "ibge",
    "bcb",
    "usda",
    "b3",
    "zarc",
    "defensivos",
]

_SYNC_MODULES = [m for m in _SOURCE_MODULES if m != "sicar"]


@pytest.fixture(autouse=True)
def _register_all_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    mock = MagicMock()
    monkeypatch.setitem(sys.modules, "agrobr", mock)
    monkeypatch.setitem(sys.modules, "agrobr.sync", mock)
    monkeypatch.setitem(sys.modules, "agrobr.alt", mock)

    for mod_name in _SYNC_MODULES:
        m = MagicMock()
        monkeypatch.setitem(sys.modules, f"agrobr.sync.{mod_name}", m)
        setattr(mock, mod_name, m)

    sicar_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "agrobr.alt.sicar", sicar_mock)
    mock.sicar = sicar_mock

    for mod_name in _SOURCE_MODULES:
        full = f"agrobr_qgis.sources.{mod_name}"
        if full in sys.modules:
            importlib.reload(sys.modules[full])
        else:
            importlib.import_module(full)


class TestAllSourcesStructural:
    def test_sources_registered(self) -> None:
        sources = SourceRegistry.list_all()
        assert len(sources) >= 30

    def test_no_duplicate_ids(self) -> None:
        sources = SourceRegistry.list_all()
        ids = [s.id() for s in sources]
        assert len(ids) == len(set(ids))

    def test_all_have_valid_id(self) -> None:
        for src in SourceRegistry.list_all():
            assert src.id()

    def test_all_have_valid_name(self) -> None:
        for src in SourceRegistry.list_all():
            assert src.name()

    def test_all_have_valid_category(self) -> None:
        for src in SourceRegistry.list_all():
            assert isinstance(src.category(), SourceCategory)

    def test_auth_sources_have_env_var(self) -> None:
        for src in SourceRegistry.list_all():
            if src.capabilities() & SourceCapability.AUTH:
                assert src.auth_env_var() is not None

    def test_municipal_join_sources_have_join_column(self) -> None:
        for src in SourceRegistry.list_all():
            if src.capabilities() & SourceCapability.MUNICIPAL_JOIN:
                assert src.join_column() is not None

    def test_all_fetch_callable(self) -> None:
        for src_cls in SourceRegistry.list_all():
            instance = src_cls()
            result = instance.fetch()
            assert isinstance(result, (pd.DataFrame, MagicMock))
