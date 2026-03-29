from __future__ import annotations

import pytest

from agrobr_qgis.core.constants import (
    DTYPE_FALLBACK,
    DTYPE_MAP,
    MEMORY_LAYER_MAX_ROWS,
    MEMORY_LAYER_MAX_VERTICES,
)
from agrobr_qgis.core.data_contract import ContractResult, DataContract
from agrobr_qgis.core.layer_builder import LayerBuilder
from tests.mocks.fixtures.queimadas import make_queimadas_gdf


class TestShouldUseGpkg:
    def test_below_thresholds_returns_false(self) -> None:
        result = ContractResult(
            df=None,  # type: ignore[arg-type]
            row_count=100,
            estimated_vertices=1000,
        )
        assert LayerBuilder._should_use_gpkg(result) is False

    def test_above_max_rows_returns_true(self) -> None:
        result = ContractResult(
            df=None,  # type: ignore[arg-type]
            row_count=MEMORY_LAYER_MAX_ROWS + 1,
            estimated_vertices=0,
        )
        assert LayerBuilder._should_use_gpkg(result) is True

    def test_above_max_vertices_returns_true(self) -> None:
        result = ContractResult(
            df=None,  # type: ignore[arg-type]
            row_count=100,
            estimated_vertices=MEMORY_LAYER_MAX_VERTICES + 1,
        )
        assert LayerBuilder._should_use_gpkg(result) is True


class TestMapDtype:
    @pytest.mark.parametrize("dtype_str,expected", list(DTYPE_MAP.items()))
    def test_known_dtypes(self, dtype_str: str, expected: str) -> None:
        assert LayerBuilder._map_dtype(dtype_str) == expected

    def test_unknown_dtype_returns_fallback(self) -> None:
        assert LayerBuilder._map_dtype("complex128") == DTYPE_FALLBACK


class TestResolveStyle:
    def test_polygon(self) -> None:
        result = LayerBuilder.resolve_style("Polygon")
        assert result is not None
        assert result.endswith("polygon.qml")

    def test_multipolygon(self) -> None:
        result = LayerBuilder.resolve_style("MultiPolygon")
        assert result is not None
        assert result.endswith("polygon.qml")

    def test_point(self) -> None:
        result = LayerBuilder.resolve_style("Point")
        assert result is not None
        assert result.endswith("point.qml")

    def test_line(self) -> None:
        result = LayerBuilder.resolve_style("LineString")
        assert result is not None
        assert result.endswith("line.qml")

    def test_none_returns_none(self) -> None:
        assert LayerBuilder.resolve_style(None) is None

    def test_unknown_returns_none(self) -> None:
        assert LayerBuilder.resolve_style("GeometryCollection") is None


class TestPipelineIntegration:
    def test_fixture_through_contract_to_decision(self) -> None:
        gdf = make_queimadas_gdf()
        result = DataContract.validate(gdf)
        assert result.has_geometry is True
        assert LayerBuilder._should_use_gpkg(result) is False
