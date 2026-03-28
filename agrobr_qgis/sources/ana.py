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

__all__ = [
    "DemandaIrrigacaoSource",
    "DisponibilidadeHidricaSource",
    "HidrografiaSource",
    "PivosIrrigacaoSource",
]


@SourceRegistry.register
class DemandaIrrigacaoSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "ana_demanda_irrigacao"

    @classmethod
    def name(cls) -> str:
        return "Demanda de Irrigação (ANA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.GEO | SourceCapability.TABULAR | SourceCapability.BBOX_FILTER

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="bbox",
                label="Bounding Box",
                param_type=ParamType.BBOX,
                required=True,
            ),
            SourceParameter(
                name="max_features",
                label="Max features",
                param_type=ParamType.INT,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import ana  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            ana.demanda_irrigacao_geo(**kwargs) if geo else ana.demanda_irrigacao(**kwargs)
        )
        return result


@SourceRegistry.register
class DisponibilidadeHidricaSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "ana_disponibilidade_hidrica"

    @classmethod
    def name(cls) -> str:
        return "Disponibilidade Hídrica (ANA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.GEO | SourceCapability.TABULAR | SourceCapability.BBOX_FILTER

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="bbox",
                label="Bounding Box",
                param_type=ParamType.BBOX,
            ),
            SourceParameter(
                name="max_features",
                label="Max features",
                param_type=ParamType.INT,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import ana  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            ana.disponibilidade_hidrica_geo(**kwargs)
            if geo
            else ana.disponibilidade_hidrica(**kwargs)
        )
        return result


@SourceRegistry.register
class HidrografiaSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "ana_hidrografia"

    @classmethod
    def name(cls) -> str:
        return "Hidrografia (ANA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.GEO | SourceCapability.TABULAR | SourceCapability.BBOX_FILTER

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="bbox",
                label="Bounding Box",
                param_type=ParamType.BBOX,
                required=True,
            ),
            SourceParameter(
                name="max_features",
                label="Max features",
                param_type=ParamType.INT,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import ana  # type: ignore[import-untyped]

        result: pd.DataFrame = ana.hidrografia_geo(**kwargs) if geo else ana.hidrografia(**kwargs)
        return result


@SourceRegistry.register
class PivosIrrigacaoSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "ana_pivos_irrigacao"

    @classmethod
    def name(cls) -> str:
        return "Pivôs de Irrigação (ANA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

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
            SourceParameter(
                name="max_features",
                label="Max features",
                param_type=ParamType.INT,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import ana  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            ana.pivos_irrigacao_geo(**kwargs) if geo else ana.pivos_irrigacao(**kwargs)
        )
        return result
