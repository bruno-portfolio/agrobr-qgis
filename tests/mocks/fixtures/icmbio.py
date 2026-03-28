from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

__all__ = ["make_icmbio_df", "make_icmbio_gdf"]

_DATA = {
    "nome_uc": [
        "PARNA da Amazônia",
        "REBIO do Tapirapé",
        "FLONA do Tapajós",
        "PARNA do Iguaçu",
        "ESEC de Maracá",
        "RESEX Chico Mendes",
        "APA do Xingu",
        "PARNA da Chapada Diamantina",
        "FLONA de Carajás",
        "REBIO de Sooretama",
    ],
    "grupo": [
        "Proteção Integral",
        "Proteção Integral",
        "Uso Sustentável",
        "Proteção Integral",
        "Proteção Integral",
        "Uso Sustentável",
        "Uso Sustentável",
        "Proteção Integral",
        "Uso Sustentável",
        "Proteção Integral",
    ],
    "categoria": [
        "PARNA",
        "REBIO",
        "FLONA",
        "PARNA",
        "ESEC",
        "RESEX",
        "APA",
        "PARNA",
        "FLONA",
        "REBIO",
    ],
    "uf": ["PA", "PA", "PA", "PR", "RR", "AC", "MT", "BA", "PA", "ES"],
    "bioma": [
        "Amazônia",
        "Amazônia",
        "Amazônia",
        "Mata Atlântica",
        "Amazônia",
        "Amazônia",
        "Amazônia",
        "Caatinga",
        "Amazônia",
        "Mata Atlântica",
    ],
    "area_ha": [
        994000.0,
        103000.0,
        527319.0,
        185262.0,
        101312.0,
        970570.0,
        2816000.0,
        152141.0,
        411948.0,
        27858.0,
    ],
}

_LATS = [
    -4.5600,
    -5.4200,
    -3.3500,
    -25.6100,
    3.3600,
    -10.9700,
    -10.4500,
    -12.5300,
    -6.0600,
    -19.0500,
]
_LONS = [
    -56.2700,
    -50.6700,
    -55.0100,
    -54.3500,
    -61.4500,
    -68.5800,
    -52.3800,
    -41.4200,
    -50.1800,
    -40.1200,
]
_COORDS = list(zip(_LONS, _LATS))


def make_icmbio_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)


def make_icmbio_gdf() -> gpd.GeoDataFrame:
    geoms: list[Point | Polygon | None] = [Point(c) for c in _COORDS]
    geoms[7] = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])
    geoms[9] = None
    return gpd.GeoDataFrame(_DATA, geometry=geoms, crs="EPSG:4674")
