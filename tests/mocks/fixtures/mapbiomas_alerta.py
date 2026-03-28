from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

__all__ = ["make_mapbiomas_alerta_df", "make_mapbiomas_alerta_gdf"]

_DATA = {
    "alert_code": [
        "MBA-2026-00001",
        "MBA-2026-00042",
        "MBA-2026-00105",
        "MBA-2026-00178",
        "MBA-2026-00256",
        "MBA-2026-00312",
        "MBA-2026-00489",
        "MBA-2026-00534",
        "MBA-2026-00601",
        "MBA-2026-00720",
    ],
    "source": [
        "DETER",
        "SAD",
        "SIRAD",
        "DETER",
        "SAD",
        "DETER",
        "SIRAD",
        "SAD",
        "DETER",
        "SIRAD",
    ],
    "detected_at": pd.to_datetime(
        [
            "2026-03-01 08:30:00",
            "2026-03-03 14:15:00",
            "2026-03-06 10:00:00",
            "2026-03-09 16:45:00",
            "2026-03-11 09:20:00",
            "2026-03-14 13:00:00",
            "2026-03-17 11:30:00",
            "2026-03-20 07:50:00",
            "2026-03-23 15:10:00",
            "2026-03-26 12:00:00",
        ]
    ),
    "area_ha": [
        25.3,
        142.7,
        8.9,
        310.5,
        56.1,
        87.4,
        15.2,
        203.6,
        44.8,
        99.0,
    ],
    "bioma": [
        "Amazônia",
        "Amazônia",
        "Cerrado",
        "Amazônia",
        "Amazônia",
        "Cerrado",
        "Amazônia",
        "Amazônia",
        "Cerrado",
        "Amazônia",
    ],
    "uf": ["PA", "MT", "GO", "AM", "RO", "MA", "PA", "MT", "TO", "AC"],
}

_LATS = [
    -3.8500,
    -10.1200,
    -14.0900,
    -5.7800,
    -9.8100,
    -4.3200,
    -6.4100,
    -12.6700,
    -9.3200,
    -9.0200,
]
_LONS = [
    -52.4300,
    -56.7800,
    -49.3200,
    -63.1500,
    -63.3400,
    -45.8900,
    -51.2800,
    -55.4200,
    -48.1700,
    -70.8100,
]
_COORDS = list(zip(_LONS, _LATS))


def make_mapbiomas_alerta_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)


def make_mapbiomas_alerta_gdf() -> gpd.GeoDataFrame:
    geoms: list[Point | Polygon | None] = [Point(c) for c in _COORDS]
    geoms[7] = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])
    geoms[9] = None
    return gpd.GeoDataFrame(_DATA, geometry=geoms, crs="EPSG:4674")
