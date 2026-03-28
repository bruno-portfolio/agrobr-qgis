from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Flag, StrEnum, auto
from typing import Any

import pandas as pd


class SourceCategory(StrEnum):
    AMBIENTAL = "ambiental"
    PRODUCAO = "producao"
    MERCADO = "mercado"
    CREDITO = "credito"
    CLIMA = "clima"
    COMERCIO_EXTERIOR = "comercio_exterior"
    FUNDIARIO = "fundiario"
    REGULATORIO = "regulatorio"


class SourceCapability(Flag):
    GEO = auto()
    TABULAR = auto()
    BBOX_FILTER = auto()
    TEMPORAL = auto()
    AUTH = auto()
    PREVIEW = auto()
    PAGINATION = auto()
    MUNICIPAL_JOIN = auto()


class ParamType(StrEnum):
    STRING = "string"
    INT = "int"
    DATE = "date"
    CHOICE = "choice"
    CHOICE_DYNAMIC = "choice_dynamic"
    MULTI_CHOICE = "multi_choice"
    BBOX = "bbox"
    UF = "uf"
    PRODUTO = "produto"


@dataclass
class SourceParameter:
    name: str
    label: str
    param_type: ParamType
    required: bool = False
    default: Any = None
    choices: list[str] | None = None
    help_text: str = ""
    depends_on: str | None = None

    @property
    def processing_safe(self) -> bool:
        return self.param_type not in (
            ParamType.CHOICE_DYNAMIC,
            ParamType.MULTI_CHOICE,
            ParamType.PRODUTO,
        )


class SourceAdapter(ABC):
    @classmethod
    @abstractmethod
    def id(cls) -> str: ...

    @classmethod
    @abstractmethod
    def name(cls) -> str: ...

    @classmethod
    @abstractmethod
    def category(cls) -> SourceCategory: ...

    @classmethod
    def description(cls) -> str:
        return ""

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return []

    @classmethod
    def auth_env_var(cls) -> str | None:
        return None

    @classmethod
    def join_column(cls) -> str | None:
        return None

    @abstractmethod
    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame: ...
