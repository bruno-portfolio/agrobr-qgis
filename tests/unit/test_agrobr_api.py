from __future__ import annotations

import importlib
import inspect
from collections.abc import Callable
from typing import Any

import geopandas as gpd
import pandas as pd
import pytest
from agrobr import contracts
from agrobr.desmatamento import models as desmatamento_models
from agrobr.mapbiomas_alerta import models as alerta_models

from agrobr_qgis.core.auth_manager import AuthManager
from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import ParamType, SourceAdapter, SourceParameter
from agrobr_qgis.core.template import TemplateRegistry
from agrobr_qgis.sources import (
    ana,
    conab,
    desmatamento,
    funai,
    ibama,
    ibge,
    icmbio,
    incra,
    mapbiomas_alerta,
    queimadas,
    sfb,
    sicar,
    zarc,
)

CALLS: list[tuple[type[SourceAdapter], bool, str, str]] = [
    (ana.DemandaIrrigacaoSource, False, "agrobr.ana", "demanda_irrigacao"),
    (ana.DemandaIrrigacaoSource, True, "agrobr.ana", "demanda_irrigacao_geo"),
    (ana.DisponibilidadeHidricaSource, False, "agrobr.ana", "disponibilidade_hidrica"),
    (ana.DisponibilidadeHidricaSource, True, "agrobr.ana", "disponibilidade_hidrica_geo"),
    (ana.HidrografiaSource, False, "agrobr.ana", "hidrografia"),
    (ana.HidrografiaSource, True, "agrobr.ana", "hidrografia_geo"),
    (ana.PivosIrrigacaoSource, False, "agrobr.ana", "pivos_irrigacao"),
    (ana.PivosIrrigacaoSource, True, "agrobr.ana", "pivos_irrigacao_geo"),
    (conab.ConabSafrasSource, False, "agrobr.conab", "levantamentos"),
    (conab.ConabSerieHistoricaSource, False, "agrobr.conab", "serie_historica"),
    (conab.ConabCeasaPrecosSource, False, "agrobr.conab", "ceasa_precos"),
    (desmatamento.DeterSource, False, "agrobr.desmatamento", "deter"),
    (desmatamento.DeterSource, True, "agrobr.desmatamento", "deter_geo"),
    (desmatamento.ProdesSource, False, "agrobr.desmatamento", "prodes"),
    (desmatamento.ProdesSource, True, "agrobr.desmatamento", "prodes_geo"),
    (funai.TerrasIndigenasSource, False, "agrobr.funai", "terras_indigenas"),
    (funai.TerrasIndigenasSource, True, "agrobr.funai", "terras_indigenas_geo"),
    (ibama.EmbargosSource, False, "agrobr.ibama", "embargos"),
    (ibama.EmbargosSource, True, "agrobr.ibama", "embargos_geo"),
    (ibge.IbgePamSource, False, "agrobr.ibge", "pam"),
    (ibge.IbgeLspaSource, False, "agrobr.ibge", "lspa"),
    (ibge.IbgePpmSource, False, "agrobr.ibge", "ppm"),
    (icmbio.UcsSource, False, "agrobr.icmbio", "ucs"),
    (icmbio.UcsSource, True, "agrobr.icmbio", "ucs_geo"),
    (incra.QuilombolasSource, False, "agrobr.incra", "quilombolas"),
    (incra.QuilombolasSource, True, "agrobr.incra", "quilombolas_geo"),
    (mapbiomas_alerta.AlertasSource, False, "agrobr.mapbiomas_alerta", "alertas"),
    (mapbiomas_alerta.AlertasSource, True, "agrobr.mapbiomas_alerta", "alertas_geo"),
    (queimadas.QueimadasSource, False, "agrobr.queimadas", "focos"),
    (queimadas.QueimadasSource, True, "agrobr.queimadas", "focos_geo"),
    (sfb.CnfpSource, False, "agrobr.sfb", "cnfp"),
    (sfb.CnfpSource, True, "agrobr.sfb", "cnfp_geo"),
    (sfb.ConcessoesSource, False, "agrobr.sfb", "concessoes"),
    (sfb.ConcessoesSource, True, "agrobr.sfb", "concessoes_geo"),
    (sfb.IfnConglomeradosSource, False, "agrobr.sfb", "ifn_conglomerados"),
    (sfb.IfnConglomeradosSource, True, "agrobr.sfb", "ifn_conglomerados_geo"),
    (sicar.SicarImoveisSource, False, "agrobr.alt.sicar", "imoveis"),
    (sicar.SicarImoveisSource, True, "agrobr.alt.sicar", "imoveis_geo"),
    (sicar.SicarResumoSource, False, "agrobr.alt.sicar", "resumo"),
    (zarc.ZarcZoneamentoSource, False, "agrobr.zarc", "zoneamento"),
]

ADAPTERS: dict[str, type[SourceAdapter]] = {adapter.id(): adapter for adapter, *_ in CALLS}

_SAMPLES: dict[ParamType, Any] = {
    ParamType.STRING: "x",
    ParamType.PRODUTO: "soja",
    ParamType.INT: 2023,
    ParamType.DATE: "2024-01-31",
    ParamType.UF: "MT",
    ParamType.BBOX: (-48.0, -16.0, -47.0, -15.0),
    ParamType.CHOICE_DYNAMIC: "x",
    ParamType.MULTI_CHOICE: "x",
}

_SAVED_TOKEN = "token-salvo"

_EXPLICIT_KINDS = (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)


def _sample(param: SourceParameter) -> Any:
    if param.default is not None:
        return param.default
    if param.choices:
        return param.choices[0]
    return _SAMPLES[param.param_type]


def _kwargs(adapter: type[SourceAdapter], *, only_required: bool) -> dict[str, Any]:
    return {
        p.name: _sample(p)
        for p in adapter.parameters()
        if not only_required or p.required or p.default is not None
    }


def _explicit_names(func: Callable[..., Any]) -> set[str]:
    return {
        name
        for name, param in inspect.signature(func).parameters.items()
        if param.kind in _EXPLICIT_KINDS
    }


@pytest.fixture()
def record_call(
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[str, str, bool], tuple[Callable[..., Any], dict[str, Any]]]:
    def _install(
        module_path: str, func_name: str, geo: bool
    ) -> tuple[Callable[..., Any], dict[str, Any]]:
        module = importlib.import_module(module_path)
        real = getattr(module, func_name)
        recorded: dict[str, Any] = {}

        def _fake(*args: Any, **kwargs: Any) -> Any:
            recorded["args"] = args
            recorded["kwargs"] = kwargs
            if func_name == "levantamentos":
                return []
            return gpd.GeoDataFrame() if geo else pd.DataFrame()

        monkeypatch.setattr(module, func_name, _fake)
        monkeypatch.setattr(AuthManager, "get_token", lambda _source_id: _SAVED_TOKEN)
        return real, recorded

    return _install


@pytest.mark.parametrize("only_required", [False, True], ids=["todos", "obrigatorios"])
@pytest.mark.parametrize(
    ("adapter", "geo", "module_path", "func_name"),
    CALLS,
    ids=[f"{m.rsplit('.', 1)[-1]}.{f}" for _a, _g, m, f in CALLS],
)
def test_fetch_binds_agrobr_signature(
    record_call: Callable[[str, str, bool], tuple[Callable[..., Any], dict[str, Any]]],
    adapter: type[SourceAdapter],
    geo: bool,
    module_path: str,
    func_name: str,
    only_required: bool,
) -> None:
    real, recorded = record_call(module_path, func_name, geo)
    kwargs = _kwargs(adapter, only_required=only_required)

    adapter().fetch(geo=geo, **kwargs)

    expected = set(kwargs) | ({"token"} if adapter.auth_env_var() else set())
    assert recorded["args"] == ()
    assert set(recorded["kwargs"]) == expected
    assert set(recorded["kwargs"]) <= _explicit_names(real)
    inspect.signature(real).bind(*recorded["args"], **recorded["kwargs"])


@pytest.mark.parametrize("geo", [False, True])
@pytest.mark.parametrize(("saved", "expected"), [("token-salvo", "token-salvo"), (None, None)])
def test_alertas_forwards_saved_token(
    record_call: Callable[[str, str, bool], tuple[Callable[..., Any], dict[str, Any]]],
    monkeypatch: pytest.MonkeyPatch,
    geo: bool,
    saved: str | None,
    expected: str | None,
) -> None:
    func_name = "alertas_geo" if geo else "alertas"
    _real, recorded = record_call("agrobr.mapbiomas_alerta", func_name, geo)
    monkeypatch.setattr(AuthManager, "get_token", lambda _source_id: saved)

    mapbiomas_alerta.AlertasSource().fetch(geo=geo)

    assert recorded["kwargs"].get("token") == expected


@pytest.mark.parametrize(
    ("adapter", "published"),
    [
        (desmatamento.DeterSource, desmatamento_models.DETER_WORKSPACES),
        (desmatamento.ProdesSource, desmatamento_models.PRODES_LAYERS),
    ],
    ids=["deter", "prodes"],
)
def test_bioma_choices_published_by_agrobr(
    adapter: type[SourceAdapter], published: dict[str, str]
) -> None:
    choices = next(p.choices for p in adapter.parameters() if p.name == "bioma")
    assert choices
    assert set(choices) <= set(published)


def test_template_bindings_target_source_parameters() -> None:
    for adapter in ADAPTERS.values():
        SourceRegistry.register(adapter)
    importlib.reload(importlib.import_module("agrobr_qgis.core.templates"))
    for template in TemplateRegistry.list_all():
        for tparam in template.params:
            for binding in tparam.bindings:
                names = {p.name for p in ADAPTERS[binding.source_id].parameters()}
                assert binding.source_param in names, (template.id, binding)
        for source_defaults in template.source_defaults:
            names = {p.name for p in ADAPTERS[source_defaults.source_id].parameters()}
            assert set(source_defaults.defaults) <= names, (template.id, source_defaults)


@pytest.mark.parametrize(
    ("adapter", "columns"),
    [
        (
            desmatamento.DeterSource,
            [c.name for c in contracts.get_contract("desmatamento_deter").columns],
        ),
        (
            desmatamento.DeterSource,
            [c.name for c in contracts.get_contract("desmatamento_deter_feicoes").columns],
        ),
        (
            queimadas.QueimadasSource,
            [c.name for c in contracts.get_contract("focos_queimadas").columns],
        ),
        (mapbiomas_alerta.AlertasSource, alerta_models.COLUNAS_SAIDA),
        (
            zarc.ZarcZoneamentoSource,
            [c.name for c in contracts.get_contract("zoneamento_agricola").columns],
        ),
    ],
    ids=["deter", "deter_geo", "queimadas", "mapbiomas_alertas", "zarc"],
)
def test_output_columns_exist_in_agrobr_contract(
    adapter: type[SourceAdapter], columns: list[str]
) -> None:
    used = {adapter.temporal_column(), adapter.join_column()} - {None}
    assert used
    assert used <= set(columns)
