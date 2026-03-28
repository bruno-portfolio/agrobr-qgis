from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

__all__ = ["make_ibama_embargos_df", "make_ibama_embargos_gdf"]

_DATA = {
    "auto_infracao": [
        "AI-2026-000101",
        "AI-2026-000234",
        "AI-2026-000389",
        "AI-2026-000412",
        "AI-2026-000567",
        "AI-2026-000678",
        "AI-2026-000790",
        "AI-2026-000845",
        "AI-2026-000923",
        "AI-2026-001001",
    ],
    "data_embargo": pd.to_datetime(
        [
            "2026-01-10",
            "2026-01-18",
            "2026-02-03",
            "2026-02-14",
            "2026-02-22",
            "2026-03-01",
            "2026-03-08",
            "2026-03-14",
            "2026-03-20",
            "2026-03-26",
        ]
    ),
    "area_ha": [
        120.5,
        45.3,
        230.8,
        78.2,
        15.6,
        340.1,
        92.7,
        560.4,
        33.9,
        180.0,
    ],
    "uf": ["PA", "MT", "RO", "AM", "MA", "TO", "PA", "MT", "RO", "AM"],
    "municipio": [
        "Novo Progresso",
        "Colniza",
        "Porto Velho",
        "Humaitá",
        "Grajaú",
        "Lagoa da Confusão",
        "Itaituba",
        "Juara",
        "Machadinho D'Oeste",
        "Manicoré",
    ],
    "tipo_infracao": [
        "Desmatamento ilegal",
        "Exploração florestal sem autorização",
        "Desmatamento ilegal",
        "Queimada sem autorização",
        "Desmatamento ilegal",
        "Exploração florestal sem autorização",
        "Queimada sem autorização",
        "Desmatamento ilegal",
        "Exploração florestal sem autorização",
        "Desmatamento ilegal",
    ],
}

_LATS = [
    -7.0800,
    -9.3700,
    -8.7600,
    -7.5100,
    -5.8200,
    -10.7900,
    -4.2800,
    -11.2600,
    -9.3400,
    -5.8100,
]
_LONS = [
    -55.3800,
    -59.2300,
    -63.9000,
    -63.0200,
    -46.1300,
    -49.7300,
    -55.9800,
    -57.5200,
    -62.0500,
    -61.3000,
]
_COORDS = list(zip(_LONS, _LATS))


def make_ibama_embargos_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)


def make_ibama_embargos_gdf() -> gpd.GeoDataFrame:
    geoms: list[Point | Polygon | None] = [Point(c) for c in _COORDS]
    geoms[7] = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])
    geoms[9] = None
    return gpd.GeoDataFrame(_DATA, geometry=geoms, crs="EPSG:4674")
