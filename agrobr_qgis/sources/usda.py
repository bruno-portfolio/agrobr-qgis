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

__all__ = ["UsdaPsdSource"]


@SourceRegistry.register
class UsdaPsdSource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "usda_psd"

    @classmethod
    def name(cls) -> str:
        return "PSD (USDA)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.MERCADO

    @classmethod
    def description(cls) -> str:
        return "Production, Supply & Distribution (USDA)"

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR | SourceCapability.AUTH

    @classmethod
    def auth_env_var(cls) -> str | None:
        return "USDA_API_KEY"

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="commodity",
                label="Commodity",
                param_type=ParamType.STRING,
                required=True,
            ),
            SourceParameter(
                name="country",
                label="Country",
                param_type=ParamType.STRING,
                default="BR",
            ),
            SourceParameter(
                name="market_year",
                label="Market Year",
                param_type=ParamType.INT,
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:  # noqa: ARG002
        from agrobr.sync import usda  # type: ignore[import-untyped]

        result: pd.DataFrame = usda.psd(**kwargs)
        return result
