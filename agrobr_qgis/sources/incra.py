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

__all__ = ["QuilombolasSource"]


@SourceRegistry.register
class QuilombolasSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "incra_quilombolas"

    @classmethod
    def name(cls) -> str:
        return "Quilombolas (INCRA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.FUNDIARIO

    @classmethod
    def description(cls) -> str:
        return "Territórios quilombolas reconhecidos pelo INCRA"

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
        from agrobr.sync import incra  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            incra.quilombolas_geo(**kwargs) if geo else incra.quilombolas(**kwargs)
        )
        return result
