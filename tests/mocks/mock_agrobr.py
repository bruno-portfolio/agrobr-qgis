from __future__ import annotations

from typing import Any

import geopandas as gpd
import pandas as pd

from tests.mocks.fixtures.queimadas import make_queimadas_df, make_queimadas_gdf

__all__ = ["MockQueimadas"]


class MockQueimadas:
    def focos(self, **kwargs: Any) -> pd.DataFrame:
        df = make_queimadas_df()
        data = kwargs.get("data")
        if data is not None:
            mask = df["data_hora_gmt"].dt.date == pd.Timestamp(data).date()
            return df[mask].reset_index(drop=True)
        return df

    def focos_geo(self, **kwargs: Any) -> gpd.GeoDataFrame:
        gdf = make_queimadas_gdf()
        data = kwargs.get("data")
        if data is not None:
            mask = gdf["data_hora_gmt"].dt.date == pd.Timestamp(data).date()
            return gdf[mask].reset_index(drop=True)
        return gdf
