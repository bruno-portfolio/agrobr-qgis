from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

__all__ = ["make_funai_df", "make_funai_gdf"]

_DATA = {
    "nome_ti": [
        "Yanomami",
        "Raposa Serra do Sol",
        "Vale do Javari",
        "Kayapó",
        "Munduruku",
        "Xingu",
        "Araribóia",
        "Waimiri-Atroari",
        "Alto Rio Negro",
        "Mangueirinha",
    ],
    "fase": [
        "Regularizada",
        "Homologada",
        "Regularizada",
        "Declarada",
        "Homologada",
        "Regularizada",
        "Declarada",
        "Regularizada",
        "Homologada",
        "Regularizada",
    ],
    "uf": ["RR", "RR", "AM", "PA", "PA", "MT", "MA", "AM", "AM", "PR"],
    "area_ha": [
        9664975.0,
        1747464.0,
        8544480.0,
        3284005.0,
        2381794.0,
        2642003.0,
        413288.0,
        2585911.0,
        7999381.0,
        16375.0,
    ],
    "etnia": [
        "Yanomami",
        "Macuxi",
        "Marubo",
        "Kayapó",
        "Munduruku",
        "Kuikuro",
        "Guajajara",
        "Waimiri-Atroari",
        "Tukano",
        "Kaingang",
    ],
    "municipio": [
        "Boa Vista",
        "Pacaraima",
        "Atalaia do Norte",
        "Ourilândia do Norte",
        "Jacareacanga",
        "Canarana",
        "Amarante do Maranhão",
        "Presidente Figueiredo",
        "São Gabriel da Cachoeira",
        "Mangueirinha",
    ],
}

_LATS = [
    2.8235,
    4.0700,
    -5.1200,
    -7.9500,
    -6.2800,
    -12.0100,
    -5.5600,
    -1.6500,
    -0.1300,
    -25.9400,
]
_LONS = [
    -63.5800,
    -60.4200,
    -72.7800,
    -51.5200,
    -57.0100,
    -53.0700,
    -46.7200,
    -59.9800,
    -67.0800,
    -52.1700,
]
_COORDS = list(zip(_LONS, _LATS))


def make_funai_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)


def make_funai_gdf() -> gpd.GeoDataFrame:
    geoms: list[Point | Polygon | None] = [Point(c) for c in _COORDS]
    geoms[7] = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])
    geoms[9] = None
    return gpd.GeoDataFrame(_DATA, geometry=geoms, crs="EPSG:4674")
