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

__all__ = ["MapBiomasCoberturaSource"]

_WMS_BASE = "http://azure.solved.eco.br:8080/geoserver/solved/wms"
_FIRST_YEAR = 1985
_LAST_YEAR = 2024


@SourceRegistry.register
class MapBiomasCoberturaSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "mapbiomas_cobertura"

    @classmethod
    def name(cls) -> str:
        return "Cobertura (MapBiomas)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Uso e cobertura do solo \u2014 MapBiomas Collection 10 (1985-2024)"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TILE_SERVICE

    @classmethod
    def source_url(cls) -> str | None:
        return "https://mapbiomas.org/"

    @classmethod
    def health_url(cls) -> str | None:
        return f"{_WMS_BASE}?service=WMS&request=GetCapabilities"

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="ano",
                label="Ano",
                param_type=ParamType.CHOICE,
                required=True,
                choices=[str(y) for y in range(_FIRST_YEAR, _LAST_YEAR + 1)],
                default=str(_LAST_YEAR),
            ),
        ]

    @classmethod
    def tile_uri(cls, **kwargs: Any) -> str | None:
        ano = kwargs.get("ano", str(_LAST_YEAR))
        return (
            f"contextualWMSLegend=0"
            f"&crs=EPSG:4326"
            f"&dpiMode=7"
            f"&featureCount=10"
            f"&format=image/png"
            f"&layers=mapbiomas_brazil_{ano}"
            f"&styles=solved:mapbiomas_legend"
            f"&url={_WMS_BASE}"
        )

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        return pd.DataFrame()
