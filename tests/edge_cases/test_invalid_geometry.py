from __future__ import annotations

import geopandas as gpd
import pytest
from shapely.geometry import LineString, Point, Polygon

from agrobr_qgis.core.data_contract import DataContract


@pytest.mark.edge
class TestInvalidGeometry:
    def test_bowtie_polygon_fixed(self) -> None:
        bowtie = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])
        assert not bowtie.is_valid

        gdf = gpd.GeoDataFrame(
            {"nome": ["fazenda"]},
            geometry=[bowtie],
            crs="EPSG:4326",
        )
        result = DataContract.validate(gdf)

        assert any("make_valid" in w for w in result.warnings)
        assert result.df.geometry.is_valid.all()
        assert result.row_count == 1

    def test_mixed_geometry_types(self) -> None:
        geoms = [
            Point(0, 0),
            Point(1, 1),
            Point(2, 2),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 0)]),
            LineString([(0, 0), (5, 5)]),
        ]
        gdf = gpd.GeoDataFrame(
            {"val": range(5)},
            geometry=geoms,
            crs="EPSG:4674",
        )
        result = DataContract.validate(gdf)

        assert result.geometry_type == "Point"
        assert result.row_count == 5

    def test_empty_geometry_removed(self) -> None:
        empty_point = Point()
        assert empty_point.is_empty

        gdf = gpd.GeoDataFrame(
            {"val": [1, 2, 3]},
            geometry=[Point(10, -20), empty_point, Point(30, -40)],
            crs="EPSG:4674",
        )
        result = DataContract.validate(gdf)

        assert result.row_count == 2
        assert any("nulas" in w for w in result.warnings)
        assert not result.df.geometry.is_empty.any()

    def test_nan_coordinates_raises(self) -> None:
        nan_point = Point(float("nan"), float("nan"))
        valid_point = Point(-47.9, -15.8)

        gdf = gpd.GeoDataFrame(
            {"val": [1, 2]},
            geometry=[valid_point, nan_point],
            crs="EPSG:4674",
        )

        from shapely.errors import GEOSException

        with pytest.raises(GEOSException):
            DataContract.validate(gdf)
