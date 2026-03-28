from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import DataContract
from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import SourceCapability, SourceCategory
from tests.mocks.mock_agrobr import MockBcb


@pytest.fixture(autouse=True)
def _register_bcb(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_module = MagicMock()
    mock_bcb = MockBcb()
    mock_module.bcb = mock_bcb
    monkeypatch.setitem(sys.modules, "agrobr", MagicMock())
    monkeypatch.setitem(sys.modules, "agrobr.sync", mock_module)
    monkeypatch.setitem(sys.modules, "agrobr.sync.bcb", mock_bcb)
    from agrobr_qgis.sources.bcb import BcbFocusSource, BcbPtaxSource, BcbSgsSource

    SourceRegistry.register(BcbPtaxSource)
    SourceRegistry.register(BcbFocusSource)
    SourceRegistry.register(BcbSgsSource)


class TestBcbPtaxSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("bcb_ptax") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("bcb_ptax")
        assert src is not None
        assert src.id() == "bcb_ptax"

    def test_category(self) -> None:
        src = SourceRegistry.get("bcb_ptax")
        assert src is not None
        assert src.category() == SourceCategory.MERCADO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("bcb_ptax")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.TEMPORAL

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("bcb_ptax")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("bcb_ptax")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10


class TestBcbFocusSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("bcb_focus") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("bcb_focus")
        assert src is not None
        assert src.id() == "bcb_focus"

    def test_category(self) -> None:
        src = SourceRegistry.get("bcb_focus")
        assert src is not None
        assert src.category() == SourceCategory.MERCADO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("bcb_focus")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("bcb_focus")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("bcb_focus")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10


class TestBcbSgsSource:
    def test_registered(self) -> None:
        assert SourceRegistry.get("bcb_sgs") is not None

    def test_id(self) -> None:
        src = SourceRegistry.get("bcb_sgs")
        assert src is not None
        assert src.id() == "bcb_sgs"

    def test_category(self) -> None:
        src = SourceRegistry.get("bcb_sgs")
        assert src is not None
        assert src.category() == SourceCategory.MERCADO

    def test_capabilities(self) -> None:
        src = SourceRegistry.get("bcb_sgs")
        assert src is not None
        caps = src.capabilities()
        assert caps & SourceCapability.TABULAR
        assert caps & SourceCapability.TEMPORAL

    def test_fetch_returns_dataframe(self) -> None:
        src_cls = SourceRegistry.get("bcb_sgs")
        assert src_cls is not None
        result = src_cls().fetch()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10

    def test_pipeline_fetch_to_contract(self) -> None:
        src_cls = SourceRegistry.get("bcb_sgs")
        assert src_cls is not None
        raw = src_cls().fetch()
        result = DataContract.validate(raw)
        assert result.has_geometry is False
        assert result.row_count == 10
