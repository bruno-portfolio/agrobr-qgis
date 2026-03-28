from __future__ import annotations

from typing import Any

import geopandas as gpd
import pandas as pd

from tests.mocks.fixtures.bcb import make_bcb_df
from tests.mocks.fixtures.cepea import make_cepea_df
from tests.mocks.fixtures.conab_safras import make_conab_safras_df
from tests.mocks.fixtures.desmatamento import make_desmatamento_df, make_desmatamento_gdf
from tests.mocks.fixtures.funai import make_funai_df, make_funai_gdf
from tests.mocks.fixtures.ibama_embargos import make_ibama_embargos_df, make_ibama_embargos_gdf
from tests.mocks.fixtures.ibge_pam import make_ibge_pam_df
from tests.mocks.fixtures.icmbio import make_icmbio_df, make_icmbio_gdf
from tests.mocks.fixtures.mapbiomas_alerta import (
    make_mapbiomas_alerta_df,
    make_mapbiomas_alerta_gdf,
)
from tests.mocks.fixtures.queimadas import make_queimadas_df, make_queimadas_gdf
from tests.mocks.fixtures.zarc import make_zarc_df

__all__ = [
    "MockBcb",
    "MockCepea",
    "MockConab",
    "MockDesmatamento",
    "MockFunai",
    "MockIbama",
    "MockIbge",
    "MockIcmbio",
    "MockMapbiomasAlerta",
    "MockQueimadas",
    "MockZarc",
]


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


class MockDesmatamento:
    def deter(self, **kwargs: Any) -> pd.DataFrame:
        return make_desmatamento_df()

    def deter_geo(self, **kwargs: Any) -> gpd.GeoDataFrame:
        return make_desmatamento_gdf()

    def prodes(self, **kwargs: Any) -> pd.DataFrame:
        return make_desmatamento_df()

    def prodes_geo(self, **kwargs: Any) -> gpd.GeoDataFrame:
        return make_desmatamento_gdf()


class MockFunai:
    def terras_indigenas(self, **kwargs: Any) -> pd.DataFrame:
        return make_funai_df()

    def terras_indigenas_geo(self, **kwargs: Any) -> gpd.GeoDataFrame:
        return make_funai_gdf()


class MockIcmbio:
    def ucs(self, **kwargs: Any) -> pd.DataFrame:
        return make_icmbio_df()

    def ucs_geo(self, **kwargs: Any) -> gpd.GeoDataFrame:
        return make_icmbio_gdf()


class MockIbama:
    def embargos(self, **kwargs: Any) -> pd.DataFrame:
        return make_ibama_embargos_df()

    def embargos_geo(self, **kwargs: Any) -> gpd.GeoDataFrame:
        return make_ibama_embargos_gdf()


class MockMapbiomasAlerta:
    def alertas(self, **kwargs: Any) -> pd.DataFrame:
        return make_mapbiomas_alerta_df()

    def alertas_geo(self, **kwargs: Any) -> gpd.GeoDataFrame:
        return make_mapbiomas_alerta_gdf()


class MockConab:
    def levantamentos(self, **kwargs: Any) -> pd.DataFrame:
        return make_conab_safras_df()

    def serie_historica(self, **kwargs: Any) -> pd.DataFrame:
        return make_conab_safras_df()

    def ceasa_precos(self, **kwargs: Any) -> pd.DataFrame:
        return make_conab_safras_df()


class MockIbge:
    def pam(self, **kwargs: Any) -> pd.DataFrame:
        return make_ibge_pam_df()

    def lspa(self, **kwargs: Any) -> pd.DataFrame:
        return make_ibge_pam_df()

    def ppm(self, **kwargs: Any) -> pd.DataFrame:
        return make_ibge_pam_df()


class MockCepea:
    def indicador(self, **kwargs: Any) -> pd.DataFrame:
        return make_cepea_df()


class MockBcb:
    def ptax(self, **kwargs: Any) -> pd.DataFrame:
        return make_bcb_df()

    def focus(self, **kwargs: Any) -> pd.DataFrame:
        return make_bcb_df()

    def sgs(self, **kwargs: Any) -> pd.DataFrame:
        return make_bcb_df()


class MockZarc:
    def zoneamento(self, **kwargs: Any) -> pd.DataFrame:
        return make_zarc_df()
