from __future__ import annotations

from typing import Any

import pandas as pd
import pytest

from agrobr_qgis.core.source_adapter import (
    ParamType,
    SourceAdapter,
    SourceCapability,
    SourceCategory,
    SourceParameter,
)


class _DummySource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "dummy"

    @classmethod
    def name(cls) -> str:
        return "Dummy"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    def fetch(self, *, geo: bool = False, **_kwargs: Any) -> pd.DataFrame:
        _ = geo
        return pd.DataFrame()


class TestSourceCategory:
    @pytest.mark.parametrize("cat", list(SourceCategory))
    def test_values_are_valid_strings(self, cat: SourceCategory) -> None:
        assert isinstance(cat, str)
        assert len(cat) > 0

    def test_all_categories_exist(self) -> None:
        assert len(SourceCategory) == 8


class TestSourceCapability:
    def test_bitwise_or(self) -> None:
        combined = SourceCapability.GEO | SourceCapability.TABULAR
        assert SourceCapability.GEO in combined
        assert SourceCapability.TABULAR in combined

    def test_bitwise_and_match(self) -> None:
        combined = SourceCapability.GEO | SourceCapability.TABULAR
        assert combined & SourceCapability.GEO

    def test_bitwise_and_no_match(self) -> None:
        combined = SourceCapability.GEO | SourceCapability.TABULAR
        assert not (combined & SourceCapability.AUTH)

    def test_all_capabilities_distinct(self) -> None:
        values = [c.value for c in SourceCapability if c.name != ""]
        assert len(values) == len(set(values))


PROCESSING_SAFE_TYPES = [
    ParamType.STRING,
    ParamType.INT,
    ParamType.DATE,
    ParamType.CHOICE,
    ParamType.BBOX,
    ParamType.UF,
]
PROCESSING_UNSAFE_TYPES = [
    ParamType.CHOICE_DYNAMIC,
    ParamType.MULTI_CHOICE,
    ParamType.PRODUTO,
]


class TestParamType:
    @pytest.mark.parametrize("pt", list(ParamType))
    def test_values_are_valid_strings(self, pt: ParamType) -> None:
        assert isinstance(pt, str)
        assert len(pt) > 0

    def test_all_param_types_exist(self) -> None:
        assert len(ParamType) == 9


class TestSourceParameter:
    @pytest.mark.parametrize("pt", PROCESSING_SAFE_TYPES)
    def test_processing_safe_true(self, pt: ParamType) -> None:
        param = SourceParameter(name="x", label="X", param_type=pt)
        assert param.processing_safe is True

    @pytest.mark.parametrize("pt", PROCESSING_UNSAFE_TYPES)
    def test_processing_safe_false(self, pt: ParamType) -> None:
        param = SourceParameter(name="x", label="X", param_type=pt)
        assert param.processing_safe is False

    def test_defaults(self) -> None:
        param = SourceParameter(name="x", label="X", param_type=ParamType.STRING)
        assert param.required is False
        assert param.default is None
        assert param.choices is None
        assert param.help_text == ""
        assert param.depends_on is None


class TestSourceAdapter:
    def test_cannot_instantiate_abc(self) -> None:
        with pytest.raises(TypeError):
            SourceAdapter()  # type: ignore[abstract]

    def test_concrete_subclass_works(self) -> None:
        source = _DummySource()
        assert source.id() == "dummy"
        assert source.name() == "Dummy"
        assert source.category() == SourceCategory.AMBIENTAL

    def test_default_capabilities(self) -> None:
        assert _DummySource.capabilities() == SourceCapability.TABULAR

    def test_default_parameters(self) -> None:
        assert _DummySource.parameters() == []

    def test_default_description(self) -> None:
        assert _DummySource.description() == ""

    def test_default_auth_env_var(self) -> None:
        assert _DummySource.auth_env_var() is None

    def test_default_join_column(self) -> None:
        assert _DummySource.join_column() is None

    def test_fetch_returns_dataframe(self) -> None:
        result = _DummySource().fetch()
        assert isinstance(result, pd.DataFrame)
