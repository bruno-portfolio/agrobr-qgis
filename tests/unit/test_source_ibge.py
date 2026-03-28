from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import DataContract
from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import SourceCapability, SourceCategory
from tests.mocks.mock_agrobr import MockIbge


@pytest.fixture(autouse=True)
def _register_ibge(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_module = MagicMock()
    mock_ibge = MockIbge()
    mock_module.ibge = mock_ibge
    monkeypatch.setitem(sys.modules, "agrobr", MagicMock())
    monkeypatch.setitem(sys.modules, "agrobr.sync", mock_module)
    monkeypatch.setitem(sys.modules, "agrobr.sync.ibge", mock_ibge)
    from agrobr_qgis.sources.ibge import IbgeLspaSource, IbgePamSource, IbgePpmSource

    SourceRegistry.register(IbgePamSource)
    SourceRegistry.register(IbgeLspaSource)
    SourceRegistry.register(IbgePpmSource)


class TestIbgePamSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("ibge_pam") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("ibge_pam")
        assert src is not None
        assert src.id() == "ibge_pam"

    def test_category(self) -> None:
        src = SourceRegistry.get("ibge_pam")
        assert src is not None
        assert src.category() == SourceCategory.PRODUCAO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("ibge_pam")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.MUNICIPAL_JOIN

    def test_join_column(self) -> None:
        src = SourceRegistry.get("ibge_pam")
        assert src is not None
        assert src.join_column() == "codigo_municipio"

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("ibge_pam")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("ibge_pam")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10


class TestIbgeLspaSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("ibge_lspa") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("ibge_lspa")
        assert src is not None
        assert src.id() == "ibge_lspa"

    def test_category(self) -> None:
        src = SourceRegistry.get("ibge_lspa")
        assert src is not None
        assert src.category() == SourceCategory.PRODUCAO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("ibge_lspa")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.TEMPORAL

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("ibge_lspa")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("ibge_lspa")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10


class TestIbgePpmSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("ibge_ppm") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("ibge_ppm")
        assert src is not None
        assert src.id() == "ibge_ppm"

    def test_category(self) -> None:
        src = SourceRegistry.get("ibge_ppm")
        assert src is not None
        assert src.category() == SourceCategory.PRODUCAO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("ibge_ppm")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.MUNICIPAL_JOIN

    def test_join_column(self) -> None:
        src = SourceRegistry.get("ibge_ppm")
        assert src is not None
        assert src.join_column() == "codigo_municipio"

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("ibge_ppm")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("ibge_ppm")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10
