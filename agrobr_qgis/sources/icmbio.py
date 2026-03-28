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

__all__ = ["UcsSource"]


@SourceRegistry.register
class UcsSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "icmbio_ucs"

    @classmethod
    def name(cls) -> str:
        return "Unidades de Conservação (ICMBio)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Unidades de conservação federais"

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
                name="grupo",
                label="Grupo",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="bioma",
                label="Bioma",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="bbox",
                label="Bounding Box",
                param_type=ParamType.BBOX,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import icmbio  # type: ignore[import-untyped]

        result: pd.DataFrame = icmbio.ucs_geo(**kwargs) if geo else icmbio.ucs(**kwargs)
        return result
