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

__all__ = ["B3AjustesSource", "B3HistoricoSource"]


@SourceRegistry.register
class B3AjustesSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "b3_ajustes"

    @classmethod
    def name(cls) -> str:
        return "Ajustes Diários (B3)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.MERCADO

    @classmethod
    def description(cls) -> str:
        return "Ajustes diários de contratos futuros"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="data",
                label="Data",
                param_type=ParamType.DATE,
                required=True,
            ),
            SourceParameter(
                name="contrato",
                label="Contrato",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import b3  # type: ignore[import-untyped]

        result: pd.DataFrame = b3.ajustes(**kwargs)
        return result


@SourceRegistry.register
class B3HistoricoSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "b3_historico"

    @classmethod
    def name(cls) -> str:
        return "Histórico (B3)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.MERCADO

    @classmethod
    def description(cls) -> str:
        return "Histórico de preços de contratos futuros"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="contrato",
                label="Contrato",
                param_type=ParamType.STRING,
                required=True,
            ),
            SourceParameter(
                name="inicio",
                label="Data início",
                param_type=ParamType.DATE,
                required=True,
            ),
            SourceParameter(
                name="fim",
                label="Data fim",
                param_type=ParamType.DATE,
                required=True,
            ),
            SourceParameter(
                name="vencimento",
                label="Vencimento",
                param_type=ParamType.STRING,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import b3  # type: ignore[import-untyped]

        result: pd.DataFrame = b3.historico(**kwargs)
        return result
