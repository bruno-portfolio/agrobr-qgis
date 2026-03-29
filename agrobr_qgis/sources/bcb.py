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

__all__ = ["BcbFocusSource", "BcbPtaxSource", "BcbSgsSource"]


@SourceRegistry.register
class BcbPtaxSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "bcb_ptax"

    @classmethod
    def temporal_column(cls) -> str | None:
        return "data"

    @classmethod
    def source_url(cls) -> str | None:
        return "https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes"

    @classmethod
    def health_url(cls) -> str | None:
        return "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json"

    @classmethod
    def name(cls) -> str:
        return "PTAX (BCB)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.MERCADO

    @classmethod
    def description(cls) -> str:
        return "Taxa de câmbio PTAX do Banco Central"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR | SourceCapability.TEMPORAL

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="data",
                label="Data",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="data_inicial",
                label="Data inicial",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="data_final",
                label="Data final",
                param_type=ParamType.DATE,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import bcb  # type: ignore[import-untyped]

        result: pd.DataFrame = bcb.ptax(**kwargs)
        return result


@SourceRegistry.register
class BcbFocusSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "bcb_focus"

    @classmethod
    def name(cls) -> str:
        return "Focus (BCB)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.MERCADO

    @classmethod
    def description(cls) -> str:
        return "Relatório Focus — expectativas de mercado"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="indicador",
                label="Indicador",
                param_type=ParamType.STRING,
                default="PIB Agropecuário",
            ),
            SourceParameter(
                name="top",
                label="Top N",
                param_type=ParamType.INT,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import bcb  # type: ignore[import-untyped]

        result: pd.DataFrame = bcb.focus(**kwargs)
        return result


@SourceRegistry.register
class BcbSgsSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "bcb_sgs"

    @classmethod
    def temporal_column(cls) -> str | None:
        return "data"

    @classmethod
    def name(cls) -> str:
        return "SGS (BCB)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.MERCADO

    @classmethod
    def description(cls) -> str:
        return "Séries temporais do Sistema Gerenciador de Séries"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR | SourceCapability.TEMPORAL

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="codigo",
                label="Código",
                param_type=ParamType.INT,
                required=True,
                help_text="Código da série SGS",
            ),
            SourceParameter(
                name="data_inicial",
                label="Data inicial",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="data_final",
                label="Data final",
                param_type=ParamType.DATE,
            ),
            SourceParameter(
                name="ultimos",
                label="Últimos N",
                param_type=ParamType.INT,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import bcb  # type: ignore[import-untyped]

        result: pd.DataFrame = bcb.sgs(**kwargs)
        return result
