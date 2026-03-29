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

__all__ = ["QueimadasSource"]


@SourceRegistry.register
class QueimadasSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "queimadas"

    @classmethod
    def name(cls) -> str:
        return "Queimadas (INPE)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Focos de incêndio detectados por satélite (INPE/Programa Queimadas)"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.GEO | SourceCapability.TABULAR | SourceCapability.TEMPORAL

    @classmethod
    def temporal_column(cls) -> str | None:
        return "data"

    @classmethod
    def source_url(cls) -> str | None:
        return "https://terrabrasilis.dpi.inpe.br/queimadas/portal/"

    @classmethod
    def health_url(cls) -> str | None:
        return "https://terrabrasilis.dpi.inpe.br/geoserver/web/"

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="ano",
                label="Ano",
                param_type=ParamType.INT,
                required=True,
                default=2026,
            ),
            SourceParameter(
                name="mes",
                label="Mês",
                param_type=ParamType.INT,
                required=True,
                default=1,
            ),
            SourceParameter(
                name="dia",
                label="Dia",
                param_type=ParamType.INT,
                help_text="Opcional — deixe 0 para o mês inteiro",
            ),
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import queimadas  # type: ignore[import-untyped]

        if not kwargs.get("dia"):
            kwargs.pop("dia", None)
        result: pd.DataFrame = queimadas.focos_geo(**kwargs) if geo else queimadas.focos(**kwargs)
        return result
