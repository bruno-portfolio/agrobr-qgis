from __future__ import annotations

import hashlib
import threading
from pathlib import Path
from unittest.mock import MagicMock, patch

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Polygon

from agrobr_qgis.core.exceptions import ChecksumError
from agrobr_qgis.core.spatial_join import SpatialJoin


def _mock_mesh_municipal() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {
            "CD_MUN": ["3550308", "3304557", "5300108"],
            "NM_MUN": ["São Paulo", "Rio de Janeiro", "Brasília"],
        },
        geometry=[
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(1, 0), (2, 0), (2, 1), (1, 1)]),
            Polygon([(2, 0), (3, 0), (3, 1), (2, 1)]),
        ],
        crs="EPSG:4674",
    )


def _mock_mesh_uf() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"CD_UF": ["35", "33", "53"], "NM_UF": ["São Paulo", "Rio de Janeiro", "Distrito Federal"]},
        geometry=[
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(1, 0), (2, 0), (2, 1), (1, 1)]),
            Polygon([(2, 0), (3, 0), (3, 1), (2, 1)]),
        ],
        crs="EPSG:4674",
    )


class TestToMunicipal:
    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh_municipal())
    def test_valid_join(self, _mock: MagicMock) -> None:
        df = pd.DataFrame({"cod_mun": ["3550308", "3304557"], "valor": [100, 200]})
        result = SpatialJoin.to_municipal(df, "cod_mun")
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 2
        assert "geometry" in result.columns

    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh_municipal())
    def test_empty_join(self, _mock: MagicMock, mock_qgis_full: MagicMock) -> None:
        df = pd.DataFrame({"cod_mun": ["9999999"], "valor": [100]})
        result = SpatialJoin.to_municipal(df, "cod_mun")
        assert len(result) == 0

    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh_municipal())
    def test_int_key_normalized_to_str(self, _mock: MagicMock) -> None:
        df = pd.DataFrame({"cod_mun": [3550308, 3304557], "valor": [100, 200]})
        result = SpatialJoin.to_municipal(df, "cod_mun")
        assert len(result) == 2

    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh_municipal())
    def test_aggregation_sum(self, _mock: MagicMock) -> None:
        df = pd.DataFrame(
            {
                "cod_mun": ["3550308", "3550308", "3304557"],
                "valor": [100, 50, 200],
            }
        )
        result = SpatialJoin.to_municipal(df, "cod_mun", value_cols=["valor"], agg="sum")
        sp_row = result[result["CD_MUN"] == "3550308"]
        assert sp_row["valor"].iloc[0] == 150

    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh_municipal())
    def test_aggregation_mean(self, _mock: MagicMock) -> None:
        df = pd.DataFrame(
            {
                "cod_mun": ["3550308", "3550308"],
                "valor": [100, 200],
            }
        )
        result = SpatialJoin.to_municipal(df, "cod_mun", value_cols=["valor"], agg="mean")
        assert result["valor"].iloc[0] == 150.0


class TestToUf:
    @patch.object(SpatialJoin, "_get_mesh", return_value=_mock_mesh_uf())
    def test_valid_join(self, _mock: MagicMock) -> None:
        df = pd.DataFrame({"uf": ["35", "33"], "valor": [100, 200]})
        result = SpatialJoin.to_uf(df, "uf")
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 2


class TestValidateChecksum:
    def test_valid_checksum(self, tmp_path: Path) -> None:
        f = tmp_path / "test.gpkg"
        f.write_bytes(b"test data")
        expected = hashlib.sha256(b"test data").hexdigest()
        SpatialJoin._validate_checksum(f, expected)
        assert f.exists()

    def test_invalid_checksum_deletes_file(self, tmp_path: Path) -> None:
        f = tmp_path / "test.gpkg"
        f.write_bytes(b"test data")
        with pytest.raises(ChecksumError, match="inválido"):
            SpatialJoin._validate_checksum(f, "wrong_hash")
        assert not f.exists()


class TestClearCache:
    def test_clear_cache_empties_dict(self) -> None:
        SpatialJoin._mesh_cache["test"] = _mock_mesh_municipal()
        SpatialJoin.clear_cache()
        assert len(SpatialJoin._mesh_cache) == 0


class TestLockExists:
    def test_mesh_lock_is_threading_lock(self) -> None:
        assert type(SpatialJoin._mesh_lock) is type(threading.Lock())
