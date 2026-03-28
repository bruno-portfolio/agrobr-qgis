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

__all__ = ["SicarImoveisSource", "SicarResumoSource"]


@SourceRegistry.register
class SicarImoveisSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "sicar_imoveis"

    @classmethod
    def name(cls) -> str:
        return "Imóveis Rurais (SICAR)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.FUNDIARIO

    @classmethod
    def description(cls) -> str:
        return "Imóveis rurais do Cadastro Ambiental Rural"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.GEO | SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
                required=True,
            ),
            SourceParameter(
                name="municipio",
                label="Município",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="status",
                label="Status",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="tipo",
                label="Tipo",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.alt import sicar  # type: ignore[import-untyped]

        if geo:
            result: pd.DataFrame = sicar.imoveis_geo(**kwargs)  # type: ignore[assignment]
        else:
            result = sicar.imoveis(**kwargs)  # type: ignore[assignment]
        return result


@SourceRegistry.register
class SicarResumoSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "sicar_resumo"

    @classmethod
    def name(cls) -> str:
        return "Resumo CAR (SICAR)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.FUNDIARIO

    @classmethod
    def description(cls) -> str:
        return "Resumo estatístico do CAR por município/UF"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
                required=True,
            ),
            SourceParameter(
                name="municipio",
                label="Município",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.alt import sicar  # type: ignore[import-untyped]

        result: pd.DataFrame = sicar.resumo(**kwargs)  # type: ignore[assignment]
        return result
