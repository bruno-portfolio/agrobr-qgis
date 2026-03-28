from __future__ import annotations

import hashlib
import tempfile
import time
from pathlib import Path
from typing import Any, ClassVar

import geopandas as gpd
import pandas as pd

from .constants import (
    DEFAULT_CRS,
    DTYPE_FALLBACK,
    DTYPE_MAP,
    MEMORY_LAYER_MAX_ROWS,
    MEMORY_LAYER_MAX_VERTICES,
)
from .data_contract import ContractResult


class LayerBuilder:
    _temp_dir: ClassVar[tempfile.TemporaryDirectory[str] | None] = None

    @classmethod
    def from_contract_result(
        cls,
        result: ContractResult,
        layer_name: str,
        style_path: str | None = None,
    ) -> Any:
        if result.has_geometry:
            assert isinstance(result.df, gpd.GeoDataFrame)
            if cls._should_use_gpkg(result):
                return cls._via_gpkg(result.df, layer_name, style_path)
            return cls._via_memory(result.df, layer_name, style_path, result.geometry_type)
        return cls._table_layer(result.df, layer_name)

    @staticmethod
    def _should_use_gpkg(result: ContractResult) -> bool:
        return (
            result.row_count > MEMORY_LAYER_MAX_ROWS
            or result.estimated_vertices > MEMORY_LAYER_MAX_VERTICES
        )

    @classmethod
    def _get_temp_dir(cls) -> Path:
        if cls._temp_dir is None:
            cls._temp_dir = tempfile.TemporaryDirectory(prefix="agrobr_")
        return Path(cls._temp_dir.name)

    @classmethod
    def _via_memory(
        cls,
        gdf: gpd.GeoDataFrame,
        layer_name: str,
        style_path: str | None,
        geometry_type: str | None = None,
    ) -> Any:
        from qgis.core import QgsFeature, QgsField, QgsFields, QgsGeometry, QgsVectorLayer
        from qgis.PyQt.QtCore import QVariant

        geom_type = geometry_type or gdf.geometry.geom_type.mode().iloc[0]
        crs = str(gdf.crs) if gdf.crs else DEFAULT_CRS
        uri = f"{geom_type}?crs={crs}"
        layer = QgsVectorLayer(uri, layer_name, "memory")

        attr_cols = gdf.columns.drop("geometry")
        fields = QgsFields()
        for col in attr_cols:
            qvariant_name = cls._map_dtype(str(gdf[col].dtype))
            fields.append(QgsField(col, getattr(QVariant, qvariant_name)))
        layer.dataProvider().addAttributes(fields)
        layer.updateFields()

        features = []
        for _, row in gdf.iterrows():
            feat = QgsFeature(layer.fields())
            feat.setGeometry(QgsGeometry.fromWkt(row.geometry.wkt))
            for col in attr_cols:
                feat[col] = None if pd.isna(row[col]) else row[col]
            features.append(feat)
        layer.dataProvider().addFeatures(features)

        if style_path:
            layer.loadNamedStyle(style_path)
        return layer

    @classmethod
    def _via_gpkg(
        cls,
        gdf: gpd.GeoDataFrame,
        layer_name: str,
        style_path: str | None,
    ) -> Any:
        from qgis.core import QgsVectorLayer

        tmp_dir = cls._get_temp_dir()
        name_seed = f"{layer_name}_{time.time()}"
        suffix = f"_agrobr_{hashlib.md5(name_seed.encode()).hexdigest()[:8]}.gpkg"  # noqa: S324
        tmp_path = tmp_dir / f"{layer_name}{suffix}"
        gdf.to_file(tmp_path, driver="GPKG")
        layer = QgsVectorLayer(str(tmp_path), layer_name, "ogr")
        if style_path:
            layer.loadNamedStyle(style_path)
        return layer

    @classmethod
    def _table_layer(cls, df: pd.DataFrame, layer_name: str) -> Any:
        from qgis.core import QgsFeature, QgsField, QgsFields, QgsVectorLayer
        from qgis.PyQt.QtCore import QVariant

        layer = QgsVectorLayer("None", layer_name, "memory")
        fields = QgsFields()
        for col in df.columns:
            qvariant_name = cls._map_dtype(str(df[col].dtype))
            fields.append(QgsField(col, getattr(QVariant, qvariant_name)))
        layer.dataProvider().addAttributes(fields)
        layer.updateFields()

        features = []
        for _, row in df.iterrows():
            feat = QgsFeature(layer.fields())
            for col in df.columns:
                feat[col] = None if pd.isna(row[col]) else row[col]
            features.append(feat)
        layer.dataProvider().addFeatures(features)
        return layer

    @staticmethod
    def _map_dtype(dtype_str: str) -> str:
        return DTYPE_MAP.get(str(dtype_str), DTYPE_FALLBACK)

    @classmethod
    def cleanup_temp(cls) -> None:
        if cls._temp_dir is not None:
            cls._temp_dir.cleanup()
            cls._temp_dir = None
