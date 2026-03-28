from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import DataContract
from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import SourceCapability, SourceCategory
from tests.mocks.mock_agrobr import MockConab


@pytest.fixture(autouse=True)
def _register_conab(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_module = MagicMock()
    mock_conab = MockConab()
    mock_module.conab = mock_conab
    monkeypatch.setitem(sys.modules, "agrobr", MagicMock())
    monkeypatch.setitem(sys.modules, "agrobr.sync", mock_module)
    monkeypatch.setitem(sys.modules, "agrobr.sync.conab", mock_conab)
    from agrobr_qgis.sources.conab import (
        ConabCeasaPrecosSource,
        ConabSafrasSource,
        ConabSerieHistoricaSource,
    )

    SourceRegistry.register(ConabSafrasSource)
    SourceRegistry.register(ConabSerieHistoricaSource)
    SourceRegistry.register(ConabCeasaPrecosSource)


class TestConabSafrasSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("conab_safras") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("conab_safras")
        assert src is not None
        assert src.id() == "conab_safras"

    def test_category(self) -> None:
        src = SourceRegistry.get("conab_safras")
        assert src is not None
        assert src.category() == SourceCategory.PRODUCAO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("conab_safras")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("conab_safras")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("conab_safras")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10


class TestConabSerieHistoricaSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("conab_serie_historica") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("conab_serie_historica")
        assert src is not None
        assert src.id() == "conab_serie_historica"

    def test_category(self) -> None:
        src = SourceRegistry.get("conab_serie_historica")
        assert src is not None
        assert src.category() == SourceCategory.PRODUCAO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("conab_serie_historica")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.TEMPORAL

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("conab_serie_historica")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("conab_serie_historica")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10


class TestConabCeasaPrecosSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("conab_ceasa_precos") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("conab_ceasa_precos")
        assert src is not None
        assert src.id() == "conab_ceasa_precos"

    def test_category(self) -> None:
        src = SourceRegistry.get("conab_ceasa_precos")
        assert src is not None
        assert src.category() == SourceCategory.PRODUCAO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("conab_ceasa_precos")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("conab_ceasa_precos")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("conab_ceasa_precos")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10
