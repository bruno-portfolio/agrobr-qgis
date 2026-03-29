from __future__ import annotations

from typing import Any

import pandas as pd
import pytest

from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import (
    ParamType,
    SourceAdapter,
    SourceCategory,
    SourceParameter,
)
from agrobr_qgis.core.template import (
    ParamBinding,
    SourceDefaults,
    SourceOutcome,
    Template,
    TemplateParam,
    TemplateRegistry,
    TemplateResult,
)


class _SourceA(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "src_a"

    @classmethod
    def name(cls) -> str:
        return "Source A"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(name="uf", label="UF", param_type=ParamType.UF, required=True),
            SourceParameter(
                name="ano", label="Ano", param_type=ParamType.INT, required=True, default=2026
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        return pd.DataFrame()


class _SourceB(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "src_b"

    @classmethod
    def name(cls) -> str:
        return "Source B"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.PRODUCAO

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return [
            SourceParameter(
                name="produto", label="Produto", param_type=ParamType.STRING, required=True
            ),
        ]

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        return pd.DataFrame()


@pytest.fixture(autouse=True)
def _setup() -> None:
    SourceRegistry.register(_SourceA)
    SourceRegistry.register(_SourceB)
    yield  # type: ignore[misc]
    TemplateRegistry.clear()


def _make_template(**overrides: Any) -> Template:
    defaults = {
        "id": "tpl_test",
        "name": "Test Template",
        "description": "Template para testes",
        "category": "ambiental",
        "source_ids": ("src_a", "src_b"),
        "params": (
            TemplateParam(
                name="estado",
                label="Estado",
                param_type=ParamType.UF,
                required=True,
                bindings=(ParamBinding(source_id="src_a", source_param="uf"),),
            ),
            TemplateParam(
                name="cultura",
                label="Cultura",
                param_type=ParamType.STRING,
                required=True,
                bindings=(ParamBinding(source_id="src_b", source_param="produto"),),
            ),
        ),
        "source_defaults": (),
    }
    defaults.update(overrides)
    return Template(**defaults)


class TestTemplateRegistry:
    def test_register_valid_template(self) -> None:
        tpl = _make_template()
        TemplateRegistry.register(tpl)
        assert TemplateRegistry.get("tpl_test") is tpl

    def test_register_unknown_source_raises(self) -> None:
        tpl = _make_template(source_ids=("src_a", "nope"))
        with pytest.raises(ValueError, match="source 'nope' not registered"):
            TemplateRegistry.register(tpl)

    def test_register_uncovered_required_param_raises(self) -> None:
        tpl = _make_template(
            params=(
                TemplateParam(
                    name="estado",
                    label="Estado",
                    param_type=ParamType.UF,
                    required=True,
                    bindings=(ParamBinding(source_id="src_a", source_param="uf"),),
                ),
            ),
        )
        with pytest.raises(ValueError, match="required param 'produto' on source 'src_b'"):
            TemplateRegistry.register(tpl)

    def test_register_covered_by_binding(self) -> None:
        tpl = _make_template(
            params=(
                TemplateParam(
                    name="estado",
                    label="Estado",
                    param_type=ParamType.UF,
                    bindings=(ParamBinding(source_id="src_a", source_param="uf"),),
                ),
                TemplateParam(
                    name="cultura",
                    label="Cultura",
                    param_type=ParamType.STRING,
                    bindings=(ParamBinding(source_id="src_b", source_param="produto"),),
                ),
            ),
        )
        TemplateRegistry.register(tpl)
        assert TemplateRegistry.get("tpl_test") is not None

    def test_register_covered_by_source_defaults(self) -> None:
        tpl = _make_template(
            params=(
                TemplateParam(
                    name="estado",
                    label="Estado",
                    param_type=ParamType.UF,
                    bindings=(ParamBinding(source_id="src_a", source_param="uf"),),
                ),
            ),
            source_defaults=(SourceDefaults(source_id="src_b", defaults={"produto": "soja"}),),
        )
        TemplateRegistry.register(tpl)
        assert TemplateRegistry.get("tpl_test") is not None

    def test_register_covered_by_adapter_default(self) -> None:
        tpl = _make_template(source_ids=("src_a",), params=())
        with pytest.raises(ValueError, match="required param 'uf' on source 'src_a'"):
            TemplateRegistry.register(tpl)

        tpl_with_binding = _make_template(
            source_ids=("src_a",),
            params=(
                TemplateParam(
                    name="estado",
                    label="Estado",
                    param_type=ParamType.UF,
                    bindings=(ParamBinding(source_id="src_a", source_param="uf"),),
                ),
            ),
        )
        TemplateRegistry.register(tpl_with_binding)
        assert TemplateRegistry.get("tpl_test") is not None


class TestTemplateResult:
    @staticmethod
    def _make_outcomes() -> list[SourceOutcome]:
        return [
            SourceOutcome("src_a", "Source A", "ok", result="data_a"),
            SourceOutcome("src_b", "Source B", "error", error_message="falhou"),
            SourceOutcome("src_c", "Source C", "timeout", error_message="Timeout"),
        ]

    def test_succeeded(self) -> None:
        result = TemplateResult("t1", "T1", self._make_outcomes())
        assert len(result.succeeded) == 1
        assert result.succeeded[0].source_id == "src_a"

    def test_failed(self) -> None:
        result = TemplateResult("t1", "T1", self._make_outcomes())
        assert len(result.failed) == 2
        failed_ids = {o.source_id for o in result.failed}
        assert failed_ids == {"src_b", "src_c"}

    def test_all_ok(self) -> None:
        outcomes = [
            SourceOutcome("src_a", "Source A", "ok", result="data_a"),
            SourceOutcome("src_b", "Source B", "ok", result="data_b"),
        ]
        result = TemplateResult("t1", "T1", outcomes)
        assert result.all_ok is True

    def test_not_all_ok(self) -> None:
        result = TemplateResult("t1", "T1", self._make_outcomes())
        assert result.all_ok is False
