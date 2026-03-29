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

__all__ = ["CepeaIndicadorSource"]


@SourceRegistry.register
class CepeaIndicadorSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "cepea_indicador"

    @classmethod
    def temporal_column(cls) -> str | None:
        return "data"

    @classmethod
    def source_url(cls) -> str | None:
        return "https://www.cepea.esalq.usp.br/br/indicador/soja.aspx"

    @classmethod
    def health_url(cls) -> str | None:
        return "https://www.cepea.esalq.usp.br/br"

    @classmethod
    def name(cls) -> str:
        return "Indicadores (CEPEA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.MERCADO

    @classmethod
    def description(cls) -> str:
        return "Indicadores de preços agropecuários CEPEA/ESALQ"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR | SourceCapability.TEMPORAL

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="produto",
                label="Produto",
                param_type=ParamType.PRODUTO,
                required=True,
                help_text="Produto (ex: Soja, Boi Gordo)",
            ),
            SourceParameter(
                name="praca",
                label="Praça",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="inicio",
                label="Data início",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="fim",
                label="Data fim",
                param_type=ParamType.DATE,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import cepea  # type: ignore[import-untyped]

        result: pd.DataFrame = cepea.indicador(**kwargs)
        return result
