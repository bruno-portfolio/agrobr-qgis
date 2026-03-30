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
    "ConabCeasaPrecosSource",
    "ConabSafrasSource",
    "ConabSerieHistoricaSource",
]


@SourceRegistry.register
class ConabSafrasSource(SourceAdapter):
    @classmethod
    def source_url(cls) -> str | None:
        return "https://portaldeinformacoes.conab.gov.br/safra-serie-historica-graos.html"

    @classmethod
    def id(cls) -> str:
        return "conab_safras"

    @classmethod
    def name(cls) -> str:
        return "Safras (CONAB)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.PRODUCAO

    @classmethod
    def description(cls) -> str:
        return "Levantamento de safras CONAB"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return []

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import conab  # type: ignore[import-untyped]

        result: pd.DataFrame = pd.DataFrame(conab.levantamentos())
        return result


@SourceRegistry.register
class ConabSerieHistoricaSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "conab_serie_historica"

    @classmethod
    def name(cls) -> str:
        return "Série Histórica (CONAB)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.PRODUCAO

    @classmethod
    def description(cls) -> str:
        return "Série histórica de produção agrícola"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="produto",
                label="Produto",
                param_type=ParamType.STRING,
                required=True,
            ),
            SourceParameter(
                name="inicio",
                label="Ano inicial",
                param_type=ParamType.INT,
                help_text="Ano inicial",
            ),
            SourceParameter(
                name="fim",
                label="Ano final",
                param_type=ParamType.INT,
                help_text="Ano final",
            ),
            SourceParameter(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import conab  # type: ignore[import-untyped]

        result: pd.DataFrame = conab.serie_historica(**kwargs)
        return result


@SourceRegistry.register
class ConabCeasaPrecosSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "conab_ceasa_precos"

    @classmethod
    def name(cls) -> str:
        return "CEASA Preços (CONAB)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.PRODUCAO

    @classmethod
    def description(cls) -> str:
        return "Preços praticados nas CEASAs"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="produto",
                label="Produto",
                param_type=ParamType.STRING,
            ),
            SourceParameter(
                name="ceasa",
                label="CEASA",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import conab  # type: ignore[import-untyped]

        result: pd.DataFrame = conab.ceasa_precos(**kwargs)
        return result
