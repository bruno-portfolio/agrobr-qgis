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

__all__ = ["AlertasSource"]


@SourceRegistry.register
class AlertasSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "mapbiomas_alertas"

    @classmethod
    def temporal_column(cls) -> str | None:
        return "detected_at"

    @classmethod
    def source_url(cls) -> str | None:
        return "https://plataforma.alerta.mapbiomas.org/"

    @classmethod
    def name(cls) -> str:
        return "Alertas (MapBiomas)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Alertas de desmatamento validados pelo MapBiomas"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return (
            SourceCapability.GEO
            | SourceCapability.TABULAR
            | SourceCapability.BBOX_FILTER
            | SourceCapability.TEMPORAL
            | SourceCapability.AUTH
            | SourceCapability.PAGINATION
        )

    @classmethod
    def auth_env_var(cls) -> str | None:
        return "MAPBIOMAS_TOKEN"

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="start_date",
                label="Data início",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="end_date",
                label="Data fim",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="bbox",
                label="Bounding Box",
                param_type=ParamType.BBOX,
            ),
            SourceParameter(
                name="limit",
                label="Limite",
                param_type=ParamType.INT,
                default=100,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import mapbiomas_alerta  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            mapbiomas_alerta.alertas_geo(**kwargs) if geo else mapbiomas_alerta.alertas(**kwargs)
        )
        return result
