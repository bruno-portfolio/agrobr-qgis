from __future__ import annotations

import sys
from unittest.mock import MagicMock

_mock_core = MagicMock()


class _StubQgsTask:
    CanCancel = 1

    def __init__(self, *a: object, **kw: object) -> None:
        pass

    def isCanceled(self) -> bool:  # noqa: N802
        return False

    def setProgress(self, p: float) -> None:  # noqa: N802
        pass


_mock_core.QgsTask = _StubQgsTask
sys.modules.setdefault("qgis", MagicMock())
sys.modules["qgis.core"] = _mock_core
sys.modules.setdefault("qgis.PyQt", MagicMock())
sys.modules.setdefault("qgis.PyQt.QtCore", MagicMock())

from typing import Any  # noqa: E402

import pandas as pd  # noqa: E402
import pytest  # noqa: E402

from agrobr_qgis.core.data_contract import ContractResult  # noqa: E402
from agrobr_qgis.core.registry import SourceRegistry  # noqa: E402
from agrobr_qgis.core.source_adapter import (  # noqa: E402
    ParamType,
    SourceAdapter,
    SourceCategory,
    SourceParameter,
)
from agrobr_qgis.core.template import (  # noqa: E402
    ParamBinding,
    SourceDefaults,
    Template,
    TemplateParam,
)
from agrobr_qgis.core.template_runner import TemplateFetchTask  # noqa: E402


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
        return pd.DataFrame({"uf": [kwargs.get("uf", "SP")], "valor": [100]})


class _SourceFail(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "src_fail"

    @classmethod
    def name(cls) -> str:
        return "Source Fail"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return []

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        msg = "conexao recusada"
        raise ConnectionError(msg)


class _SourceTimeout(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "src_timeout"

    @classmethod
    def name(cls) -> str:
        return "Source Timeout"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def parameters(cls) -> list[SourceParameter]:
        return []

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        raise TimeoutError


@pytest.fixture(autouse=True)
def _setup() -> None:
    SourceRegistry.register(_SourceA)
    SourceRegistry.register(_SourceFail)
    SourceRegistry.register(_SourceTimeout)
    yield  # type: ignore[misc]


def _make_single_source_template(
    source_id: str = "src_a",
    bindings: tuple[ParamBinding, ...] = (),
    source_defaults: tuple[SourceDefaults, ...] = (),
    params: tuple[TemplateParam, ...] | None = None,
) -> Template:
    if params is None:
        params = (
            TemplateParam(
                name="estado",
                label="Estado",
                param_type=ParamType.UF,
                bindings=bindings
                if bindings
                else (ParamBinding(source_id=source_id, source_param="uf"),),
            ),
        )
    return Template(
        id="tpl_runner",
        name="Runner Test",
        description="",
        category="ambiental",
        source_ids=(source_id,),
        params=params,
        source_defaults=source_defaults,
    )


class TestResolveParams:
    def test_binding_overrides_default(self) -> None:
        tpl = _make_single_source_template(
            bindings=(ParamBinding(source_id="src_a", source_param="uf"),),
        )
        task = TemplateFetchTask(tpl, {"estado": "MG"})
        resolved = task._resolve_params()
        assert resolved["src_a"]["uf"] == "MG"
        assert resolved["src_a"]["ano"] == 2026

    def test_source_defaults(self) -> None:
        tpl = _make_single_source_template(
            source_defaults=(SourceDefaults(source_id="src_a", defaults={"ano": 2020}),),
        )
        task = TemplateFetchTask(tpl, {"estado": "SP"})
        resolved = task._resolve_params()
        assert resolved["src_a"]["ano"] == 2020

    def test_transform(self) -> None:
        tpl = _make_single_source_template(
            bindings=(ParamBinding(source_id="src_a", source_param="uf", transform=str.upper),),
        )
        task = TemplateFetchTask(tpl, {"estado": "sp"})
        resolved = task._resolve_params()
        assert resolved["src_a"]["uf"] == "SP"

    def test_precedence(self) -> None:
        tpl = _make_single_source_template(
            bindings=(ParamBinding(source_id="src_a", source_param="ano"),),
            source_defaults=(SourceDefaults(source_id="src_a", defaults={"ano": 2020}),),
        )
        task = TemplateFetchTask(tpl, {"estado": 2024})
        resolved = task._resolve_params()
        assert resolved["src_a"]["ano"] == 2024


class TestFetchOne:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        tpl = _make_single_source_template()
        task = TemplateFetchTask(tpl, {"estado": "SP"})
        contract_result = ContractResult(df=pd.DataFrame({"v": [1]}), row_count=1, col_count=1)
        monkeypatch.setattr(
            "agrobr_qgis.core.template_runner.DataContract.validate",
            lambda _data: contract_result,
        )
        outcome = task._fetch_one("src_a", {"uf": "SP"})
        assert outcome.status == "ok"
        assert outcome.result is contract_result

    def test_error(self) -> None:
        tpl = _make_single_source_template(source_id="src_fail", params=())
        task = TemplateFetchTask(tpl, {})
        outcome = task._fetch_one("src_fail", {})
        assert outcome.status == "error"
        assert outcome.error_message == "conexao recusada"

    def test_timeout(self) -> None:
        tpl = _make_single_source_template(source_id="src_timeout", params=())
        task = TemplateFetchTask(tpl, {})
        outcome = task._fetch_one("src_timeout", {})
        assert outcome.status == "timeout"
        assert outcome.error_message == "Timeout"


class TestRun:
    def test_partial_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        tpl = Template(
            id="tpl_multi",
            name="Multi",
            description="",
            category="ambiental",
            source_ids=("src_a", "src_fail"),
            params=(
                TemplateParam(
                    name="estado",
                    label="Estado",
                    param_type=ParamType.UF,
                    bindings=(ParamBinding(source_id="src_a", source_param="uf"),),
                ),
            ),
            source_defaults=(),
        )
        contract_result = ContractResult(df=pd.DataFrame({"v": [1]}), row_count=1, col_count=1)
        monkeypatch.setattr(
            "agrobr_qgis.core.template_runner.DataContract.validate",
            lambda _data: contract_result,
        )
        task = TemplateFetchTask(tpl, {"estado": "SP"})
        returned = task.run()
        assert returned is True
        result = task._result
        assert result is not None
        assert len(result.succeeded) == 1
        assert result.succeeded[0].source_id == "src_a"
        assert len(result.failed) == 1
        assert result.failed[0].source_id == "src_fail"
        assert result.failed[0].status == "error"
