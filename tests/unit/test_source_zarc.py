from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import DataContract
from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import SourceCapability, SourceCategory
from tests.mocks.mock_agrobr import MockZarc


@pytest.fixture(autouse=True)
def _register_zarc(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_module = MagicMock()
    mock_zarc = MockZarc()
    mock_module.zarc = mock_zarc
    monkeypatch.setitem(sys.modules, "agrobr", MagicMock())
    monkeypatch.setitem(sys.modules, "agrobr.sync", mock_module)
    monkeypatch.setitem(sys.modules, "agrobr.sync.zarc", mock_zarc)
    from agrobr_qgis.sources.zarc import ZarcZoneamentoSource

    SourceRegistry.register(ZarcZoneamentoSource)


class TestZarcZoneamentoSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("zarc_zoneamento") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("zarc_zoneamento")
        assert src is not None
        assert src.id() == "zarc_zoneamento"

    def test_category(self) -> None:
        src = SourceRegistry.get("zarc_zoneamento")
        assert src is not None
        assert src.category() == SourceCategory.REGULATORIO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("zarc_zoneamento")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.MUNICIPAL_JOIN

    def test_join_column(self) -> None:
        src = SourceRegistry.get("zarc_zoneamento")
        assert src is not None
        assert src.join_column() == "geocodigo"

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("zarc_zoneamento")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("zarc_zoneamento")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10
