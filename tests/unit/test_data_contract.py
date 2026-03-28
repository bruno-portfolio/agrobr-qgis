from __future__ import annotations

import unicodedata

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point, Polygon

from agrobr_qgis.core.data_contract import ContractResult, DataContract


class TestDataContract:
    def test_none_returns_empty_with_warning(self) -> None:
        result = DataContract.validate(None)
        assert isinstance(result, ContractResult)
        assert result.df.empty
        assert "Resultado vazio" in result.warnings

    def test_empty_dataframe_returns_warning(self) -> None:
        result = DataContract.validate(pd.DataFrame())
        assert "Resultado vazio" in result.warnings

    def test_duplicate_columns_renamed(self) -> None:
        df = pd.DataFrame([[1, 2, 3]], columns=["a", "a", "b"])
        result = DataContract.validate(df)
        cols = list(result.df.columns)
        assert cols == ["a", "a_1", "b"]
        assert any("duplicadas" in w for w in result.warnings)

    def test_nfc_normalization_columns(self) -> None:
        nfd_name = unicodedata.normalize("NFD", "município")
        df = pd.DataFrame({nfd_name: [1]})
        result = DataContract.validate(df)
        assert result.df.columns[0] == unicodedata.normalize("NFC", "município")

    def test_nfc_normalization_values(self) -> None:
        nfd_value = unicodedata.normalize("NFD", "São Paulo")
        df = pd.DataFrame({"cidade": [nfd_value]})
        result = DataContract.validate(df)
        assert result.df["cidade"].iloc[0] == unicodedata.normalize("NFC", "São Paulo")

    def test_timezone_strip(self) -> None:
        dates = pd.to_datetime(["2026-01-01", "2026-01-02"]).tz_localize("UTC")
        df = pd.DataFrame({"ts": dates})
        result = DataContract.validate(df)
        assert result.df["ts"].dt.tz is None
        assert any("Timezone" in w for w in result.warnings)

    def test_timezone_strip_single_warning(self) -> None:
        dates_a = pd.to_datetime(["2026-01-01"]).tz_localize("UTC")
        dates_b = pd.to_datetime(["2026-06-01"]).tz_localize("US/Eastern")
        df = pd.DataFrame({"ts_a": dates_a, "ts_b": dates_b})
        result = DataContract.validate(df)
        tz_warnings = [w for w in result.warnings if "Timezone" in w]
        assert len(tz_warnings) == 1

    def test_geodataframe_no_crs_assumes_default(self) -> None:
        gdf = gpd.GeoDataFrame({"val": [1]}, geometry=[Point(0, 0)])
        gdf = gdf.set_crs(None)  # type: ignore[arg-type]
        result = DataContract.validate(gdf)
        assert "EPSG:4674" in (result.crs or "")
        assert any("CRS ausente" in w for w in result.warnings)

    def test_geodataframe_with_crs_keeps_original(self) -> None:
        gdf = gpd.GeoDataFrame({"val": [1]}, geometry=[Point(0, 0)], crs="EPSG:4326")
        result = DataContract.validate(gdf)
        assert "4326" in (result.crs or "")
        assert not any("CRS ausente" in w for w in result.warnings)

    def test_invalid_geometry_make_valid(self) -> None:
        bowtie = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])
        gdf = gpd.GeoDataFrame({"val": [1]}, geometry=[bowtie], crs="EPSG:4326")
        result = DataContract.validate(gdf)
        assert any("make_valid" in w for w in result.warnings)
        assert result.df.geometry.is_valid.all()

    def test_null_geometry_removed(self) -> None:
        gdf = gpd.GeoDataFrame({"val": [1, 2]}, geometry=[Point(0, 0), None], crs="EPSG:4326")
        result = DataContract.validate(gdf)
        assert result.row_count == 1
        assert any("nulas" in w for w in result.warnings)

    def test_all_null_geometry_returns_zero_vertices(self) -> None:
        gdf = gpd.GeoDataFrame({"val": [1]}, geometry=[None], crs="EPSG:4326")
        result = DataContract.validate(gdf)
        assert result.estimated_vertices == 0
        assert result.row_count == 0

    def test_geometry_type_is_mode(self) -> None:
        geoms = [Point(0, 0), Point(1, 1), LineString([(0, 0), (1, 1)])]
        gdf = gpd.GeoDataFrame({"val": [1, 2, 3]}, geometry=geoms, crs="EPSG:4326")
        result = DataContract.validate(gdf)
        assert result.geometry_type == "Point"

    def test_estimated_vertices(self) -> None:
        geoms = [Point(i, i) for i in range(5)]
        gdf = gpd.GeoDataFrame({"val": range(5)}, geometry=geoms, crs="EPSG:4326")
        result = DataContract.validate(gdf)
        assert result.estimated_vertices == 5

    def test_row_count_col_count(self) -> None:
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        result = DataContract.validate(df)
        assert result.row_count == 3
        assert result.col_count == 2

    def test_has_geometry_true_for_geodataframe(self) -> None:
        gdf = gpd.GeoDataFrame({"val": [1]}, geometry=[Point(0, 0)], crs="EPSG:4326")
        result = DataContract.validate(gdf)
        assert result.has_geometry is True

    def test_has_geometry_false_for_dataframe(self) -> None:
        df = pd.DataFrame({"val": [1]})
        result = DataContract.validate(df)
        assert result.has_geometry is False
