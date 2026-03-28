from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

__all__ = ["make_desmatamento_df", "make_desmatamento_gdf"]

_DATA = {
    "data_deteccao": pd.to_datetime(
        [
            "2026-03-01",
            "2026-03-03",
            "2026-03-05",
            "2026-03-08",
            "2026-03-10",
            "2026-03-12",
            "2026-03-15",
            "2026-03-18",
            "2026-03-22",
            "2026-03-25",
        ]
    ),
    "area_km2": [0.45, 1.23, 0.78, 3.56, 0.12, 2.34, 0.67, 5.89, 1.01, 0.33],
    "classe": [
        "DESMATAMENTO",
        "DEGRADACAO",
        "DESMATAMENTO",
        "DESMATAMENTO",
        "DEGRADACAO",
        "DESMATAMENTO",
        "DEGRADACAO",
        "DESMATAMENTO",
        "DESMATAMENTO",
        "DEGRADACAO",
    ],
    "uf": ["PA", "MT", "RO", "AM", "MA", "TO", "PA", "MT", "RO", "AM"],
    "bioma": [
        "Amazônia",
        "Amazônia",
        "Amazônia",
        "Amazônia",
        "Amazônia",
        "Cerrado",
        "Amazônia",
        "Amazônia",
        "Amazônia",
        "Amazônia",
    ],
    "satelite": [
        "CBERS-4A",
        "LANDSAT-8",
        "CBERS-4A",
        "SENTINEL-2",
        "LANDSAT-8",
        "CBERS-4A",
        "SENTINEL-2",
        "LANDSAT-8",
        "CBERS-4A",
        "SENTINEL-2",
    ],
    "municipio": [
        "Altamira",
        "Colniza",
        "Porto Velho",
        "Lábrea",
        "Amarante do Maranhão",
        "Formosa do Rio Preto",
        "São Félix do Xingu",
        "Juara",
        "Candeias do Jamari",
        "Apuí",
    ],
}

_LATS = [
    -3.2100,
    -9.3700,
    -8.7612,
    -7.2600,
    -5.5700,
    -11.0500,
    -6.6400,
    -11.2600,
    -8.7900,
    -7.2100,
]
_LONS = [
    -52.2100,
    -59.2300,
    -63.9004,
    -64.8000,
    -46.7400,
    -45.1600,
    -51.9700,
    -57.5200,
    -63.7000,
    -59.8900,
]
_COORDS = list(zip(_LONS, _LATS))


def make_desmatamento_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)


def make_desmatamento_gdf() -> gpd.GeoDataFrame:
    geoms: list[Point | Polygon | None] = [Point(c) for c in _COORDS]
    geoms[7] = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])
    geoms[9] = None
    return gpd.GeoDataFrame(_DATA, geometry=geoms, crs="EPSG:4674")
