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

__all__ = ["EmbargosSource"]


@SourceRegistry.register
class EmbargosSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "ibama_embargos"

    @classmethod
    def name(cls) -> str:
        return "Embargos (IBAMA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Áreas embargadas por infrações ambientais"

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
                name="bbox",
                label="Bounding Box",
                param_type=ParamType.BBOX,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import ibama  # type: ignore[import-untyped]

        result: pd.DataFrame = ibama.embargos_geo(**kwargs) if geo else ibama.embargos(**kwargs)
        return result
