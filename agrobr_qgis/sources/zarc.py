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

__all__ = ["ZarcZoneamentoSource"]


@SourceRegistry.register
class ZarcZoneamentoSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "zarc_zoneamento"

    @classmethod
    def name(cls) -> str:
        return "ZARC (MAPA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.REGULATORIO

    @classmethod
    def description(cls) -> str:
        return "Zoneamento Agrícola de Risco Climático"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR | SourceCapability.MUNICIPAL_JOIN

    @classmethod
    def join_column(cls) -> str | None:
        return "geocodigo"

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="cultura",
                label="Cultura",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
            SourceParameter(
                name="municipio",
                label="Município",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="safra",
                label="Safra",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import zarc  # type: ignore[import-untyped]

        result: pd.DataFrame = zarc.zoneamento(**kwargs)
        return result
