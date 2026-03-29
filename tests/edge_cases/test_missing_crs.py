from __future__ import annotations

import geopandas as gpd
import pytest
from shapely.geometry import Point

from agrobr_qgis.core.data_contract import DataContract


@pytest.mark.edge
class TestMissingCrs:
    def test_no_crs_defaults_to_4674(self) -> None:
        gdf = gpd.GeoDataFrame(
            {"municipio": ["Brasilia"], "area_ha": [580.0]},
            geometry=[Point(-47.9, -15.8)],
        )
        gdf = gdf.set_crs(None)  # type: ignore[arg-type]
        assert gdf.crs is None

        result = DataContract.validate(gdf)

        assert "4674" in (result.crs or "")
        assert any("CRS ausente" in w for w in result.warnings)
        assert any("4674" in w for w in result.warnings)

    def test_non_standard_crs_preserved(self) -> None:
        gdf = gpd.GeoDataFrame(
            {"estacao": ["INMET-A001"], "temp_c": [28.5]},
            geometry=[Point(-47.9, -15.8)],
            crs="EPSG:4326",
        )
        result = DataContract.validate(gdf)

        assert "4326" in (result.crs or "")
        assert not any("CRS ausente" in w for w in result.warnings)

    def test_crs_in_result_metadata(self) -> None:
        gdf = gpd.GeoDataFrame(
            {"val": [1, 2, 3]},
            geometry=[Point(i, -i) for i in range(3)],
            crs="EPSG:4674",
        )
        result = DataContract.validate(gdf)

        assert result.crs is not None
        assert "4674" in result.crs
        assert result.has_geometry is True
