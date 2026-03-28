from __future__ import annotations

import hashlib
import threading
import urllib.request
from pathlib import Path
from typing import ClassVar

import geopandas as gpd
import pandas as pd

from .constants import MUNICIPAL_MESH_SHA256, MUNICIPAL_MESH_URL, UF_MESH_URL
from .exceptions import ChecksumError
from .logger import Logger


class SpatialJoin:
    CACHE_DIR: ClassVar[Path] = Path.home() / ".agrobr" / "meshes"
    MUNICIPAL_FILENAME: ClassVar[str] = "municipios_simplificado.gpkg"
    UF_FILENAME: ClassVar[str] = "ufs_simplificado.gpkg"
    _mesh_lock: ClassVar[threading.Lock] = threading.Lock()
    _mesh_cache: ClassVar[dict[str, gpd.GeoDataFrame]] = {}

    @classmethod
    def to_municipal(
        cls,
        df: pd.DataFrame,
        join_col: str,
        value_cols: list[str] | None = None,
        agg: str = "sum",
    ) -> gpd.GeoDataFrame:
        mesh = cls._get_mesh(cls.MUNICIPAL_FILENAME, MUNICIPAL_MESH_URL, MUNICIPAL_MESH_SHA256)

        if value_cols and df[join_col].duplicated().any():
            df = df.groupby(join_col, as_index=False)[value_cols].agg(agg)

        df = df.copy()
        df[join_col] = df[join_col].astype(str)

        merged: gpd.GeoDataFrame = mesh.merge(df, left_on="CD_MUN", right_on=join_col, how="inner")

        if len(merged) == 0:
            Logger().audit(
                f"SpatialJoin.to_municipal: join vazio. "
                f"df[{join_col}] sample: {df[join_col].head(3).tolist()}, "
                f"mesh CD_MUN sample: {mesh['CD_MUN'].head(3).tolist()}"
            )

        return merged

    @classmethod
    def to_uf(cls, df: pd.DataFrame, join_col: str) -> gpd.GeoDataFrame:
        mesh = cls._get_mesh(cls.UF_FILENAME, UF_MESH_URL, expected_sha256=None)

        df = df.copy()
        df[join_col] = df[join_col].astype(str)

        result: gpd.GeoDataFrame = mesh.merge(df, left_on="CD_UF", right_on=join_col, how="inner")
        return result

    @classmethod
    def _get_mesh(cls, filename: str, url: str, expected_sha256: str | None) -> gpd.GeoDataFrame:
        with cls._mesh_lock:
            if filename in cls._mesh_cache:
                return cls._mesh_cache[filename]

            cache_path = cls.CACHE_DIR / filename
            if not cache_path.exists():
                cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
                cls._download(url, cache_path)
                if expected_sha256:
                    cls._validate_checksum(cache_path, expected_sha256)

            gdf: gpd.GeoDataFrame = gpd.read_file(cache_path)
            for col in ["CD_MUN", "CD_UF"]:
                if col in gdf.columns:
                    gdf[col] = gdf[col].astype(str)
            cls._mesh_cache[filename] = gdf
            return gdf

    @classmethod
    def _download(cls, url: str, dest: Path) -> None:
        with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310
            dest.write_bytes(response.read())

    @staticmethod
    def _validate_checksum(path: Path, expected: str) -> None:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            path.unlink()
            raise ChecksumError(f"Checksum da malha inválido: {actual} (esperado: {expected})")
