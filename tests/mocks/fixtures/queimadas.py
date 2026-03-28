from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

__all__ = ["make_queimadas_df", "make_queimadas_gdf"]

_DATA = {
    "data_hora_gmt": pd.to_datetime(
        [
            "2026-03-28 00:00:00",
            "2026-03-28 03:15:00",
            "2026-03-28 06:30:00",
            "2026-03-28 09:45:00",
            "2026-03-28 12:00:00",
            "2026-03-28 15:15:00",
            "2026-03-28 18:30:00",
            "2026-03-28 21:45:00",
            "2026-03-27 12:00:00",
            "2026-03-27 18:00:00",
        ]
    ),
    "satelite": [
        "AQUA_M-T",
        "TERRA_M-T",
        "NPP-375",
        "AQUA_M-T",
        "TERRA_M-T",
        "NPP-375",
        "AQUA_M-T",
        "TERRA_M-T",
        "NPP-375",
        "AQUA_M-T",
    ],
    "municipio": [
        "Brasília",
        "Goiânia",
        "Cuiabá",
        "Campo Grande",
        "Palmas",
        "Porto Velho",
        "Manaus",
        "Belém",
        "São Luís",
        "Teresina",
    ],
    "estado": ["DF", "GO", "MT", "MS", "TO", "RO", "AM", "PA", "MA", "PI"],
    "pais": ["Brasil"] * 10,
    "bioma": [
        "Cerrado",
        "Cerrado",
        "Cerrado",
        "Cerrado",
        "Cerrado",
        "Amazônia",
        "Amazônia",
        "Amazônia",
        "Cerrado",
        "Caatinga",
    ],
    "dias_sem_chuva": [15, 20, 30, 25, 10, 5, 3, 8, 12, 18],
    "precipitacao": [0.0, 0.0, 0.0, 0.0, 2.5, 5.0, 10.0, 1.0, 0.0, 0.0],
    "risco_fogo": [0.9, 0.85, 0.95, 0.88, 0.5, 0.3, 0.2, 0.6, 0.75, 0.82],
    "latitude": [
        -15.7801,
        -16.6869,
        -15.6014,
        -20.4697,
        -10.1689,
        -8.7612,
        -3.1190,
        -1.4558,
        -2.5297,
        -5.0892,
    ],
    "longitude": [
        -47.9292,
        -49.2648,
        -56.0974,
        -54.6201,
        -48.3317,
        -63.9004,
        -60.0217,
        -48.5024,
        -44.2825,
        -42.8019,
    ],
    "frp": [12.5, 45.2, 78.9, 23.1, 5.6, 34.7, 8.9, 56.3, 15.4, 67.8],
}

_COORDS = list(zip(_DATA["longitude"], _DATA["latitude"]))


def make_queimadas_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)


def make_queimadas_gdf() -> gpd.GeoDataFrame:
    geoms: list[Point | Polygon | None] = [Point(c) for c in _COORDS]
    geoms[7] = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])  # bowtie invalida
    geoms[9] = None  # nula
    return gpd.GeoDataFrame(_DATA, geometry=geoms, crs="EPSG:4674")
