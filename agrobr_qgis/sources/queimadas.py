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
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="data",
                label="Data",
                param_type=ParamType.DATE,
                required=False,
                help_text="Data dos focos (default: hoje)",
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import queimadas  # type: ignore[import-untyped]

        result: pd.DataFrame = queimadas.focos_geo(**kwargs) if geo else queimadas.focos(**kwargs)
        return result
