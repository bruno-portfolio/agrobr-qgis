from __future__ import annotations

import sys
from unittest.mock import MagicMock

import geopandas as gpd
import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import DataContract
from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import SourceCapability, SourceCategory
from tests.mocks.mock_agrobr import MockFunai


@pytest.fixture(autouse=True)
def _register_funai(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_module = MagicMock()
    mock_funai = MockFunai()
    mock_module.funai = mock_funai
    monkeypatch.setitem(sys.modules, "agrobr", MagicMock())
    monkeypatch.setitem(sys.modules, "agrobr.sync", mock_module)
    monkeypatch.setitem(sys.modules, "agrobr.sync.funai", mock_funai)
    from agrobr_qgis.sources.funai import TerrasIndigenasSource

    SourceRegistry.register(TerrasIndigenasSource)


class TestTerrasIndigenasSource:
    def test_registered_in_registry(self) -> None:
        assert SourceRegistry.get("funai_terras_indigenas") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("funai_terras_indigenas")
        assert src is not None
        assert src.id() == "funai_terras_indigenas"

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("funai_terras_indigenas")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.GEO
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.BBOX_FILTER

    def test_category(self) -> None:
        src = SourceRegistry.get("funai_terras_indigenas")
        assert src is not None
        assert src.category() == SourceCategory.FUNDIARIO

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("funai_terras_indigenas")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_fetch_geo_returns_geodataframe(self) -> None:
        src_cls = SourceRegistry.get("funai_terras_indigenas")
        assert src_cls is not None
        result = src_cls().fetch(geo=True)
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("funai_terras_indigenas")
        assert src_cls is not None
        raw = src_cls().fetch(geo=True)
        result = DataContract.validate(raw)
        assert result.has_geometry is True
        assert result.row_count > 0
        assert any("make_valid" in w for w in result.warnings)
        assert any("nulas" in w for w in result.warnings)
