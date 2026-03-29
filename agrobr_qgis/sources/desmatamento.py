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

__all__ = ["DeterSource", "ProdesSource"]

_BIOMAS = [
    "Amazônia",
    "Cerrado",
    "Mata Atlântica",
    "Caatinga",
    "Pampa",
    "Pantanal",
]


@SourceRegistry.register
class DeterSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "deter"

    @classmethod
    def temporal_column(cls) -> str | None:
        return "data_deteccao"

    @classmethod
    def source_url(cls) -> str | None:
        return "https://terrabrasilis.dpi.inpe.br/"

    @classmethod
    def health_url(cls) -> str | None:
        return "https://terrabrasilis.dpi.inpe.br/geoserver/web/"

    @classmethod
    def name(cls) -> str:
        return "DETER (INPE)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Alertas de desmatamento em tempo real (INPE/DETER)"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return (
            SourceCapability.GEO
            | SourceCapability.TABULAR
            | SourceCapability.TEMPORAL
            | SourceCapability.BBOX_FILTER
        )

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="bioma",
                label="Bioma",
                param_type=ParamType.CHOICE,
                choices=_BIOMAS,
            ),
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
            SourceParameter(
                name="data_inicio",
                label="Data início",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="data_fim",
                label="Data fim",
                param_type=ParamType.DATE,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import desmatamento  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            desmatamento.deter_geo(**kwargs) if geo else desmatamento.deter(**kwargs)
        )
        return result


@SourceRegistry.register
class ProdesSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "prodes"

    @classmethod
    def name(cls) -> str:
        return "PRODES (INPE)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Desmatamento anual por corte raso (INPE/PRODES)"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.GEO | SourceCapability.TABULAR | SourceCapability.BBOX_FILTER

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="bioma",
                label="Bioma",
                param_type=ParamType.CHOICE,
                choices=_BIOMAS,
            ),
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
            SourceParameter(
                name="data_inicio",
                label="Data início",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="data_fim",
                label="Data fim",
                param_type=ParamType.DATE,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import desmatamento  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            desmatamento.prodes_geo(**kwargs) if geo else desmatamento.prodes(**kwargs)
        )
        return result
