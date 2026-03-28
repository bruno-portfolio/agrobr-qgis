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
    "DefensivosAutorizacoesSource",
    "DefensivosFormuladosSource",
    "DefensivosTecnicosSource",
]


@SourceRegistry.register
class DefensivosFormuladosSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "defensivos_formulados"

    @classmethod
    def name(cls) -> str:
        return "Defensivos Formulados (MAPA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.REGULATORIO

    @classmethod
    def description(cls) -> str:
        return "Produtos formulados registrados no MAPA"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="ingrediente_ativo",
                label="Ingrediente ativo",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="classe",
                label="Classe",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="titular",
                label="Titular",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="marca",
                label="Marca",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import defensivos  # type: ignore[import-untyped]

        result: pd.DataFrame = defensivos.formulados(**kwargs)
        return result


@SourceRegistry.register
class DefensivosAutorizacoesSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "defensivos_autorizacoes"

    @classmethod
    def name(cls) -> str:
        return "Autorizações de Defensivos (MAPA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.REGULATORIO

    @classmethod
    def description(cls) -> str:
        return "Autorizações de uso de defensivos por cultura"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="cultura",
                label="Cultura",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="ingrediente_ativo",
                label="Ingrediente ativo",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="nr_registro",
                label="Nº registro",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import defensivos  # type: ignore[import-untyped]

        result: pd.DataFrame = defensivos.autorizacoes(**kwargs)
        return result


@SourceRegistry.register
class DefensivosTecnicosSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "defensivos_tecnicos"

    @classmethod
    def name(cls) -> str:
        return "Defensivos Técnicos (MAPA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.REGULATORIO

    @classmethod
    def description(cls) -> str:
        return "Produtos técnicos de defensivos registrados"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="ingrediente_ativo",
                label="Ingrediente ativo",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="titular",
                label="Titular",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="classe",
                label="Classe",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import defensivos  # type: ignore[import-untyped]

        result: pd.DataFrame = defensivos.tecnicos(**kwargs)
        return result
