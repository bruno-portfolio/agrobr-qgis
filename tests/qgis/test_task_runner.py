from __future__ import annotations

import os
import sys
from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from agrobr_qgis.core.source_adapter import (
    SourceAdapter,
    SourceCapability,
    SourceCategory,
)

pytestmark = pytest.mark.qgis


class _TabularJoinSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "tabular_join"

    @classmethod
    def name(cls) -> str:
        return "Tabular Join"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.PRODUCAO

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR | SourceCapability.MUNICIPAL_JOIN

    @classmethod
    def join_column(cls) -> str | None:
        return "cod_ibge"

    def fetch(self, *, geo: bool = False, **_kwargs: Any) -> pd.DataFrame:
        _ = geo
        return pd.DataFrame({"cod_ibge": ["3550308"], "valor": [100.0]})


class _GeoSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "geo_src"

    @classmethod
    def name(cls) -> str:
        return "Geo Source"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.GEO | SourceCapability.TABULAR

    def fetch(self, *, geo: bool = False, **_kwargs: Any) -> pd.DataFrame:
        _ = geo
        import geopandas as gpd
        from shapely.geometry import Point

        return gpd.GeoDataFrame({"val": [1]}, geometry=[Point(0, 0)], crs="EPSG:4674")


class _FailingSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "fail"

    @classmethod
    def name(cls) -> str:
        return "Failing"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    def fetch(self, *, geo: bool = False, **_kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        raise RuntimeError("fetch explodiu")


class TestFetchTask:
    def test_fetch_ok_emits_result(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _GeoSource()
        task = FetchTask(source, {}, geo=True)
        assert task.run() is True
        assert task._contract_result is not None
        assert task._contract_result.has_geometry is True

    def test_fetch_error_sets_error(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _FailingSource()
        task = FetchTask(source, {})
        assert task.run() is False
        assert task._error is not None
        assert "fetch explodiu" in str(task._error)

    def test_cancelled_returns_false(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _GeoSource()
        task = FetchTask(source, {})
        with patch.object(task, "isCanceled", return_value=True):
            assert task.run() is False
        assert task._contract_result is None
        assert task._error is None

    def test_join_municipal_called_when_conditions_met(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        mock_spatial_join = MagicMock()
        mock_spatial_join.SpatialJoin.to_municipal.return_value = pd.DataFrame(
            {"cod_ibge": ["3550308"], "valor": [100.0]}
        )
        mock_module = MagicMock()
        mock_module.SpatialJoin = mock_spatial_join.SpatialJoin

        source = _TabularJoinSource()
        task = FetchTask(source, {}, join_municipal=True)

        with patch.dict(sys.modules, {"agrobr_qgis.core.spatial_join": mock_module}):
            assert task.run() is True

        mock_spatial_join.SpatialJoin.to_municipal.assert_called_once()

    def test_join_not_called_when_data_is_geo(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        mock_spatial_join = MagicMock()
        source = _GeoSource()
        task = FetchTask(source, {}, geo=True, join_municipal=True)

        with patch.dict(sys.modules, {"agrobr_qgis.core.spatial_join": mock_spatial_join}):
            assert task.run() is True

        mock_spatial_join.SpatialJoin.to_municipal.assert_not_called()

    def test_agrobr_log_level_set_during_run(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        original = os.environ.get("AGROBR_LOG_LEVEL")
        source = _GeoSource()
        task = FetchTask(source, {})
        task.run()
        assert os.environ.get("AGROBR_LOG_LEVEL") == "WARNING"
        if original is None:
            os.environ.pop("AGROBR_LOG_LEVEL", None)
        else:
            os.environ["AGROBR_LOG_LEVEL"] = original
