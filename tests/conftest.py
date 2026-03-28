from __future__ import annotations

from unittest.mock import MagicMock

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point


@pytest.fixture(autouse=True)
def _reset_registry():
    yield
    try:
        from agrobr_qgis.core.registry import SourceRegistry

        SourceRegistry.clear()
    except ImportError:
        pass


@pytest.fixture()
def mock_iface() -> MagicMock:
    iface = MagicMock()
    bar = MagicMock()
    bar.pushMessage = MagicMock()
    iface.messageBar.return_value = bar
    return iface


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "nome": ["A", "B", "C", "D", "E"],
            "valor": [1.0, 2.0, 3.0, 4.0, 5.0],
        }
    )


@pytest.fixture()
def sample_gdf() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"nome": ["A", "B", "C", "D", "E"], "valor": [1.0, 2.0, 3.0, 4.0, 5.0]},
        geometry=[Point(i, -i) for i in range(5)],
        crs="EPSG:4674",
    )
