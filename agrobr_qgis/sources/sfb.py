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

__all__ = ["CnfpSource", "ConcessoesSource", "IfnConglomeradosSource"]


@SourceRegistry.register
class CnfpSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "sfb_cnfp"

    @classmethod
    def name(cls) -> str:
        return "CNFP (SFB)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Cadastro Nacional de Florestas Públicas"

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
                name="bioma",
                label="Bioma",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="categoria",
                label="Categoria",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="bbox",
                label="Bounding Box",
                param_type=ParamType.BBOX,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import sfb  # type: ignore[import-untyped]

        result: pd.DataFrame = sfb.cnfp_geo(**kwargs) if geo else sfb.cnfp(**kwargs)
        return result


@SourceRegistry.register
class ConcessoesSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "sfb_concessoes"

    @classmethod
    def name(cls) -> str:
        return "Concessões Florestais (SFB)"

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
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import sfb  # type: ignore[import-untyped]

        result: pd.DataFrame = sfb.concessoes_geo(**kwargs) if geo else sfb.concessoes(**kwargs)
        return result


@SourceRegistry.register
class IfnConglomeradosSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "sfb_ifn_conglomerados"

    @classmethod
    def name(cls) -> str:
        return "IFN Conglomerados (SFB)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def description(cls) -> str:
        return "Inventário Florestal Nacional — conglomerados"

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
        from agrobr.sync import sfb  # type: ignore[import-untyped]

        result: pd.DataFrame = (
            sfb.ifn_conglomerados_geo(**kwargs) if geo else sfb.ifn_conglomerados(**kwargs)
        )
        return result
