from __future__ import annotations

from typing import Any

import pandas as pd

from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import (
    ParamType,
    SourceAdapter,
    SourceCapability,
    SourceCategory,
    SourceParameter,
)

__all__ = ["IbgeLspaSource", "IbgePamSource", "IbgePpmSource"]


@SourceRegistry.register
class IbgePamSource(SourceAdapter):
    @classmethod
    def source_url(cls) -> str | None:
        return "https://sidra.ibge.gov.br/tabela/5457"

    @classmethod
    def health_url(cls) -> str | None:
        return "https://servicodados.ibge.gov.br/api/v3/agregados"

    @classmethod
    def id(cls) -> str:
        return "ibge_pam"

    @classmethod
    def name(cls) -> str:
        return "PAM (IBGE)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.PRODUCAO

    @classmethod
    def description(cls) -> str:
        return "Produção Agrícola Municipal"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR | SourceCapability.MUNICIPAL_JOIN

    @classmethod
    def join_column(cls) -> str | None:
        return "codigo_municipio"

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="produto",
                label="Produto",
                param_type=ParamType.PRODUTO,
                required=True,
            ),
            SourceParameter(
                name="ano",
                label="Ano",
                param_type=ParamType.INT,
            ),
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
            SourceParameter(
                name="nivel",
                label="Nível",
                param_type=ParamType.CHOICE,
                choices=["brasil", "uf", "municipio"],
                default="uf",
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import ibge  # type: ignore[import-untyped]

        result: pd.DataFrame = ibge.pam(**kwargs)
        nivel = kwargs.get("nivel", "uf")
        if nivel == "municipio" and "localidade" in result.columns:
            from agrobr_qgis.core.spatial_join import SpatialJoin

            result["codigo_municipio"] = SpatialJoin.localidade_to_code(result["localidade"])
            result = result.dropna(subset=["codigo_municipio"])
        return result


@SourceRegistry.register
class IbgeLspaSource(SourceAdapter):
    @classmethod
    def health_url(cls) -> str | None:
        return "https://servicodados.ibge.gov.br/api/v3/agregados"

    @classmethod
    def id(cls) -> str:
        return "ibge_lspa"

    @classmethod
    def name(cls) -> str:
        return "LSPA (IBGE)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.PRODUCAO

    @classmethod
    def description(cls) -> str:
        return "Levantamento Sistemático da Produção Agrícola"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="produto",
                label="Produto",
                param_type=ParamType.PRODUTO,
                required=True,
            ),
            SourceParameter(
                name="ano",
                label="Ano",
                param_type=ParamType.INT,
            ),
            SourceParameter(
                name="mes",
                label="Mês",
                param_type=ParamType.INT,
            ),
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import ibge  # type: ignore[import-untyped]

        result: pd.DataFrame = ibge.lspa(**kwargs)
        return result


@SourceRegistry.register
class IbgePpmSource(SourceAdapter):
    @classmethod
    def health_url(cls) -> str | None:
        return "https://servicodados.ibge.gov.br/api/v3/agregados"

    @classmethod
    def id(cls) -> str:
        return "ibge_ppm"

    @classmethod
    def name(cls) -> str:
        return "PPM (IBGE)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.PRODUCAO

    @classmethod
    def description(cls) -> str:
        return "Pesquisa da Pecuária Municipal"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR | SourceCapability.MUNICIPAL_JOIN

    @classmethod
    def join_column(cls) -> str | None:
        return "codigo_municipio"

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="especie",
                label="Espécie",
                param_type=ParamType.STRING,
                required=True,
                help_text="Espécie pecuária",
            ),
            SourceParameter(
                name="ano",
                label="Ano",
                param_type=ParamType.INT,
            ),
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
            SourceParameter(
                name="nivel",
                label="Nível",
                param_type=ParamType.CHOICE,
                choices=["brasil", "uf", "municipio"],
                default="uf",
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import ibge  # type: ignore[import-untyped]

        result: pd.DataFrame = ibge.ppm(**kwargs)
        nivel = kwargs.get("nivel", "uf")
        if nivel == "municipio" and "localidade" in result.columns:
            from agrobr_qgis.core.spatial_join import SpatialJoin

            result["codigo_municipio"] = SpatialJoin.localidade_to_code(result["localidade"])
            result = result.dropna(subset=["codigo_municipio"])
        return result
