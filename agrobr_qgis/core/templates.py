from __future__ import annotations

from datetime import datetime

from .source_adapter import ParamType
from .template import (
    ParamBinding,
    SourceDefaults,
    Template,
    TemplateParam,
    TemplateRegistry,
)

_CURRENT_YEAR = datetime.now().year

TemplateRegistry.register(
    Template(
        id="raio_x_ambiental",
        name="Raio-X Ambiental",
        description=("Queimadas, desmatamento, embargos, imoveis rurais e UCs para uma UF"),
        category="Ambiental",
        source_ids=(
            "queimadas",
            "deter",
            "ibama_embargos",
            "sicar_imoveis",
            "icmbio_ucs",
        ),
        params=(
            TemplateParam(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
                required=True,
                bindings=(
                    ParamBinding("queimadas", "uf"),
                    ParamBinding("deter", "uf"),
                    ParamBinding("ibama_embargos", "uf"),
                    ParamBinding("sicar_imoveis", "uf"),
                    ParamBinding("icmbio_ucs", "uf"),
                ),
            ),
        ),
        source_defaults=(SourceDefaults("queimadas", {"ano": _CURRENT_YEAR, "mes": 1}),),
    )
)

TemplateRegistry.register(
    Template(
        id="analise_producao",
        name="Analise de Producao",
        description=("PAM, serie historica CONAB e indicadores CEPEA para um produto"),
        category="Producao",
        source_ids=("ibge_pam", "conab_serie_historica", "cepea_indicador"),
        params=(
            TemplateParam(
                name="produto",
                label="Produto",
                param_type=ParamType.STRING,
                required=True,
                help_text="Ex: Soja, Milho — nome comum",
                bindings=(
                    ParamBinding("ibge_pam", "produto"),
                    ParamBinding("conab_serie_historica", "produto"),
                    ParamBinding("cepea_indicador", "produto"),
                ),
            ),
            TemplateParam(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
                bindings=(
                    ParamBinding("ibge_pam", "uf"),
                    ParamBinding("conab_serie_historica", "uf"),
                ),
            ),
        ),
        source_defaults=(SourceDefaults("ibge_pam", {"ano": _CURRENT_YEAR, "nivel": "uf"}),),
    )
)

TemplateRegistry.register(
    Template(
        id="risco_climatico",
        name="Risco Climatico",
        description="ZARC e PAM para avaliar risco de uma cultura",
        category="Clima",
        source_ids=("zarc_zoneamento", "ibge_pam"),
        params=(
            TemplateParam(
                name="cultura",
                label="Cultura",
                param_type=ParamType.STRING,
                required=True,
                help_text="Ex: SOJA, MILHO",
                bindings=(
                    ParamBinding("zarc_zoneamento", "cultura"),
                    ParamBinding("ibge_pam", "produto", transform=str.capitalize),
                ),
            ),
            TemplateParam(
                name="uf",
                label="UF",
                param_type=ParamType.UF,
                bindings=(
                    ParamBinding("zarc_zoneamento", "uf"),
                    ParamBinding("ibge_pam", "uf"),
                ),
            ),
        ),
        source_defaults=(SourceDefaults("ibge_pam", {"ano": _CURRENT_YEAR, "nivel": "uf"}),),
    )
)
