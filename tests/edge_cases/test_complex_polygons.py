from __future__ import annotations

import geopandas as gpd
import numpy as np
import pytest
from shapely.geometry import MultiPolygon, Polygon

from agrobr_qgis.core.data_contract import DataContract


@pytest.mark.edge
class TestComplexPolygons:
    def test_polygon_with_many_vertices(self) -> None:
        angles = np.linspace(0, 2 * np.pi, 1000, endpoint=False)
        coords = [(np.cos(a), np.sin(a)) for a in angles]
        big_polygon = Polygon(coords)
        assert big_polygon.is_valid

        gdf = gpd.GeoDataFrame(
            {"nome": ["circulo"]},
            geometry=[big_polygon],
            crs="EPSG:4674",
        )
        result = DataContract.validate(gdf)

        assert result.row_count == 1
        assert result.has_geometry is True
        assert result.geometry_type == "Polygon"
        assert result.estimated_vertices >= 1000

    def test_polygon_with_holes(self) -> None:
        outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
        hole = [(3, 3), (7, 3), (7, 7), (3, 7)]
        holed_polygon = Polygon(outer, [hole])
        assert holed_polygon.is_valid

        gdf = gpd.GeoDataFrame(
            {"nome": ["fazenda_com_reserva"]},
            geometry=[holed_polygon],
            crs="EPSG:4674",
        )
        result = DataContract.validate(gdf)

        assert result.row_count == 1
        assert result.has_geometry is True
        assert result.geometry_type == "Polygon"
        assert result.estimated_vertices > 0
        assert len(result.warnings) == 0

    def test_multipolygon(self) -> None:
        p1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        p2 = Polygon([(2, 2), (3, 2), (3, 3), (2, 3)])
        p3 = Polygon([(5, 5), (6, 5), (6, 6), (5, 6)])
        multi = MultiPolygon([p1, p2, p3])
        assert multi.is_valid

        gdf = gpd.GeoDataFrame(
            {"regiao": ["arquipelago"]},
            geometry=[multi],
            crs="EPSG:4674",
        )
        result = DataContract.validate(gdf)

        assert result.row_count == 1
        assert result.has_geometry is True
        assert result.geometry_type == "MultiPolygon"
        assert result.estimated_vertices > 0
