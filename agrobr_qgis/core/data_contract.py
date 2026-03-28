from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

import geopandas as gpd
import pandas as pd
from shapely import get_num_coordinates
from shapely.validation import make_valid

from .constants import DEFAULT_CRS


@dataclass
class ContractResult:
    df: pd.DataFrame | gpd.GeoDataFrame
    warnings: list[str] = field(default_factory=list)
    row_count: int = 0
    col_count: int = 0
    has_geometry: bool = False
    crs: str | None = None
    geometry_type: str | None = None
    estimated_vertices: int = 0


class DataContract:
    @classmethod
    def validate(cls, data: pd.DataFrame | gpd.GeoDataFrame | None) -> ContractResult:
        warnings: list[str] = []

        if data is None or (isinstance(data, pd.DataFrame) and data.empty):
            return ContractResult(
                df=data if data is not None else pd.DataFrame(),
                warnings=["Resultado vazio"],
            )

        data = data.copy()

        data.columns = pd.Index(
            [unicodedata.normalize("NFC", c) if isinstance(c, str) else c for c in data.columns]
        )

        if data.columns.duplicated().any():
            dupes = data.columns[data.columns.duplicated()].tolist()
            warnings.append(f"Colunas duplicadas renomeadas: {dupes}")
            seen: dict[str, int] = {}
            new_cols: list[str] = []
            for c in data.columns:
                if c in seen:
                    seen[c] += 1
                    new_cols.append(f"{c}_{seen[c]}")
                else:
                    seen[c] = 0
                    new_cols.append(c)
            data.columns = pd.Index(new_cols)

        str_cols = data.select_dtypes(include=["object", "string"]).columns
        for col in str_cols:
            data[col] = data[col].apply(
                lambda v: unicodedata.normalize("NFC", v) if isinstance(v, str) else v
            )

        tz_cols = data.select_dtypes(include=["datetimetz"]).columns
        if len(tz_cols) > 0:
            for col in tz_cols:
                data[col] = data[col].dt.tz_localize(None)
            warnings.append(f"Timezone removido das colunas: {list(tz_cols)}")

        has_geometry = isinstance(data, gpd.GeoDataFrame)
        crs = None
        geometry_type = None
        estimated_vertices = 0

        if has_geometry:
            assert isinstance(data, gpd.GeoDataFrame)
            if data.crs is None:
                data = data.set_crs(DEFAULT_CRS)
                warnings.append(f"CRS ausente, assumido {DEFAULT_CRS}")
            crs = str(data.crs)

            invalid_mask = ~data.geometry.is_valid & ~data.geometry.isna()
            if invalid_mask.any():
                n = int(invalid_mask.sum())
                data.loc[invalid_mask, "geometry"] = data.loc[  # type: ignore[call-overload]
                    invalid_mask, "geometry"
                ].apply(make_valid)
                warnings.append(f"{n} geometrias inválidas corrigidas via make_valid()")

            null_mask = data.geometry.is_empty | data.geometry.isna()
            if null_mask.any():
                n = int(null_mask.sum())
                data = data[~null_mask].copy()
                warnings.append(f"{n} geometrias nulas removidas")

            if len(data) > 0:
                geometry_type = data.geometry.geom_type.mode().iloc[0]
                sample = data.geometry.head(100)
                avg = float(get_num_coordinates(sample.values).mean())
                estimated_vertices = int(avg * len(data))

        return ContractResult(
            df=data,
            warnings=warnings,
            row_count=len(data),
            col_count=len(data.columns),
            has_geometry=has_geometry,
            crs=crs,
            geometry_type=geometry_type,
            estimated_vertices=estimated_vertices,
        )
