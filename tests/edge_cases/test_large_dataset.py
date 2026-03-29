from __future__ import annotations

import pytest

from agrobr_qgis.core.constants import MEMORY_LAYER_MAX_ROWS, MEMORY_LAYER_MAX_VERTICES
from agrobr_qgis.core.data_contract import ContractResult
from agrobr_qgis.core.layer_builder import LayerBuilder


@pytest.mark.edge
class TestLargeDataset:
    def test_should_use_gpkg_above_row_threshold(self) -> None:
        result = ContractResult(
            df=None,  # type: ignore[arg-type]
            row_count=MEMORY_LAYER_MAX_ROWS + 1,
            estimated_vertices=0,
        )
        assert LayerBuilder._should_use_gpkg(result) is True

    def test_should_use_gpkg_above_vertex_threshold(self) -> None:
        result = ContractResult(
            df=None,  # type: ignore[arg-type]
            row_count=100,
            estimated_vertices=MEMORY_LAYER_MAX_VERTICES + 1,
        )
        assert LayerBuilder._should_use_gpkg(result) is True

    def test_should_use_gpkg_below_thresholds(self) -> None:
        result = ContractResult(
            df=None,  # type: ignore[arg-type]
            row_count=100,
            estimated_vertices=1000,
        )
        assert LayerBuilder._should_use_gpkg(result) is False

    def test_should_use_gpkg_at_exact_threshold(self) -> None:
        result = ContractResult(
            df=None,  # type: ignore[arg-type]
            row_count=MEMORY_LAYER_MAX_ROWS,
            estimated_vertices=MEMORY_LAYER_MAX_VERTICES,
        )
        assert LayerBuilder._should_use_gpkg(result) is False
