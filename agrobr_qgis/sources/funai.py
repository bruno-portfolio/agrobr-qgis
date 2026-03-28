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

__all__ = ["TerrasIndigenasSource"]


@SourceRegistry.register
class TerrasIndigenasSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "funai_terras_indigenas"

    @classmethod
    def name(cls) -> str:
        return "Terras Indígenas (FUNAI)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.FUNDIARIO

    @classmethod
    def description(cls) -> str:
        return "Terras indígenas demarcadas no Brasil"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.GEO | SourceCapability.TABULAR | SourceCapability.BBOX_FILTER

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
            SourceParameter(
                name="fase",
                label="Fase",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="bbox",
                label="Bounding Box",
                param_type=ParamType.BBOX,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import funai  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            funai.terras_indigenas_geo(**kwargs) if geo else funai.terras_indigenas(**kwargs)
        )
        return result
