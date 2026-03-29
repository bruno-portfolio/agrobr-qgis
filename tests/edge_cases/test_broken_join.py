from __future__ import annotations

from unittest.mock import MagicMock, patch

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely.geometry import Point

from agrobr_qgis.core.spatial_join import SpatialJoin


def _mock_mesh() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"CD_MUN": ["3550308", "3304557"], "NM_MUN": ["São Paulo", "Rio de Janeiro"]},
        geometry=[Point(-46.6, -23.5), Point(-43.2, -22.9)],
        crs="EPSG:4674",
    )


@pytest.mark.edge
class TestBrokenJoin:
    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh())
    def test_join_nonexistent_codes(self, _mock: MagicMock, mock_qgis_full: MagicMock) -> None:
        df = pd.DataFrame({"cod_mun": ["0000000", "1111111"], "valor": [10, 20]})
        result = SpatialJoin.to_municipal(df, "cod_mun")
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 0

    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh())
    def test_join_empty_dataframe(self, _mock: MagicMock, mock_qgis_full: MagicMock) -> None:
        df = pd.DataFrame({"cod_mun": pd.Series(dtype="str"), "valor": pd.Series(dtype="float64")})
        result = SpatialJoin.to_municipal(df, "cod_mun")
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 0

    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh())
    def test_join_nan_in_join_column(self, _mock: MagicMock, mock_qgis_full: MagicMock) -> None:
        df = pd.DataFrame({"cod_mun": ["3550308", np.nan, None], "valor": [10, 20, 30]})
        result = SpatialJoin.to_municipal(df, "cod_mun")
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 1
        assert result.iloc[0]["CD_MUN"] == "3550308"
