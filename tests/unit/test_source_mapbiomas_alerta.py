from __future__ import annotations

import sys
from unittest.mock import MagicMock

import geopandas as gpd
import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import DataContract
from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import SourceCapability, SourceCategory
from tests.mocks.mock_agrobr import MockMapbiomasAlerta


@pytest.fixture(autouse=True)
def _register_mapbiomas_alerta(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_module = MagicMock()
    mock_mapbiomas_alerta = MockMapbiomasAlerta()
    mock_module.mapbiomas_alerta = mock_mapbiomas_alerta
    monkeypatch.setitem(sys.modules, "agrobr", MagicMock())
    monkeypatch.setitem(sys.modules, "agrobr.sync", mock_module)
    monkeypatch.setitem(sys.modules, "agrobr.sync.mapbiomas_alerta", mock_mapbiomas_alerta)
    from agrobr_qgis.sources.mapbiomas_alerta import AlertasSource

    SourceRegistry.register(AlertasSource)


class TestAlertasSource:
    def test_registered_in_registry(self) -> None:
        assert SourceRegistry.get("mapbiomas_alertas") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("mapbiomas_alertas")
        assert src is not None
        assert src.id() == "mapbiomas_alertas"

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("mapbiomas_alertas")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.GEO
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.BBOX_FILTER
        assert caps & SourceCapability.TEMPORAL
        assert caps & SourceCapability.AUTH
        assert caps & SourceCapability.PAGINATION

    def test_category(self) -> None:
        src = SourceRegistry.get("mapbiomas_alertas")
        assert src is not None
        assert src.category() == SourceCategory.AMBIENTAL

    def test_auth_env_var(self) -> None:
        src = SourceRegistry.get("mapbiomas_alertas")
        assert src is not None
        assert src.auth_env_var() == "MAPBIOMAS_TOKEN"

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("mapbiomas_alertas")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_fetch_geo_returns_geodataframe(self) -> None:
        src_cls = SourceRegistry.get("mapbiomas_alertas")
        assert src_cls is not None
        result = src_cls().fetch(geo=True)
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("mapbiomas_alertas")
        assert src_cls is not None
        raw = src_cls().fetch(geo=True)
        result = DataContract.validate(raw)
        assert result.has_geometry is True
        assert result.row_count > 0
        assert any("make_valid" in w for w in result.warnings)
        assert any("nulas" in w for w in result.warnings)
