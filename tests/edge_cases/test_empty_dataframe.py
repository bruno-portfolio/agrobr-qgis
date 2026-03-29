from __future__ import annotations

import geopandas as gpd
import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import ContractResult, DataContract


@pytest.mark.edge
class TestEmptyDataFrame:
    def test_validate_empty_geodataframe(self) -> None:
        gdf = gpd.GeoDataFrame(
            {"val": pd.Series(dtype="float64")},
            geometry=gpd.GeoSeries([], crs="EPSG:4326"),
        )
        assert len(gdf) == 0
        assert "geometry" in gdf.columns

        result = DataContract.validate(gdf)

        assert isinstance(result, ContractResult)
        assert "Resultado vazio" in result.warnings

    def test_validate_none_returns_empty(self) -> None:
        result = DataContract.validate(None)

        assert isinstance(result, ContractResult)
        assert isinstance(result.df, pd.DataFrame)
        assert result.df.empty
        assert result.row_count == 0
        assert result.col_count == 0
        assert result.has_geometry is False
        assert result.crs is None
        assert "Resultado vazio" in result.warnings

    def test_validate_single_column_no_rows(self) -> None:
        df = pd.DataFrame({"coluna_unica": pd.Series(dtype="int64")})
        assert len(df) == 0
        assert len(df.columns) == 1

        result = DataContract.validate(df)

        assert "Resultado vazio" in result.warnings
        assert result.df.empty

    def test_validate_many_columns_no_rows(self) -> None:
        cols = {f"col_{i:02d}": pd.Series(dtype="float64") for i in range(20)}
        df = pd.DataFrame(cols)
        assert len(df) == 0
        assert len(df.columns) == 20

        result = DataContract.validate(df)

        assert "Resultado vazio" in result.warnings
        assert result.df.empty
