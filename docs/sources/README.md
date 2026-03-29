# Fontes de Dados

O plugin agrobr disponibiliza 34 fontes de dados em 5 categorias.

## Resumo

| Fonte | Categoria | Geo | Auth | Guia |
|-------|-----------|:---:|:----:|------|
| Queimadas (INPE) | Ambiental | Sim | - | [queimadas.md](queimadas.md) |
| DETER (INPE) | Ambiental | Sim | - | [desmatamento.md](desmatamento.md) |
| PRODES (INPE) | Ambiental | Sim | - | [desmatamento.md](desmatamento.md) |
| Unidades de Conservacao (ICMBio) | Ambiental | Sim | - | [icmbio.md](icmbio.md) |
| Embargos (IBAMA) | Ambiental | Sim | - | [ibama.md](ibama.md) |
| Demanda de Irrigacao (ANA) | Ambiental | Sim | - | [ana.md](ana.md) |
| Disponibilidade Hidrica (ANA) | Ambiental | Sim | - | [ana.md](ana.md) |
| Hidrografia (ANA) | Ambiental | Sim | - | [ana.md](ana.md) |
| Pivos de Irrigacao (ANA) | Ambiental | Sim | - | [ana.md](ana.md) |
| CNFP (SFB) | Ambiental | Sim | - | [sfb.md](sfb.md) |
| Concessoes Florestais (SFB) | Ambiental | Sim | - | [sfb.md](sfb.md) |
| IFN Conglomerados (SFB) | Ambiental | Sim | - | [sfb.md](sfb.md) |
| Alertas (MapBiomas) | Ambiental | Sim | Sim | [mapbiomas.md](mapbiomas.md) |
| Terras Indigenas (FUNAI) | Fundiario | Sim | - | [funai.md](funai.md) |
| Quilombolas (INCRA) | Fundiario | Sim | - | [incra.md](incra.md) |
| Imoveis Rurais (SICAR) | Fundiario | Sim | - | [sicar.md](sicar.md) |
| Resumo CAR (SICAR) | Fundiario | - | - | [sicar.md](sicar.md) |
| PAM (IBGE) | Producao | Join | - | [ibge.md](ibge.md) |
| LSPA (IBGE) | Producao | - | - | [ibge.md](ibge.md) |
| PPM (IBGE) | Producao | Join | - | [ibge.md](ibge.md) |
| Safras (CONAB) | Producao | - | - | [conab.md](conab.md) |
| Serie Historica (CONAB) | Producao | - | - | [conab.md](conab.md) |
| CEASA Precos (CONAB) | Producao | - | - | [conab.md](conab.md) |
| Indicadores (CEPEA) | Mercado | - | - | [cepea.md](cepea.md) |
| PTAX (BCB) | Mercado | - | - | [bcb.md](bcb.md) |
| Focus (BCB) | Mercado | - | - | [bcb.md](bcb.md) |
| SGS (BCB) | Mercado | - | - | [bcb.md](bcb.md) |
| PSD (USDA) | Mercado | - | Sim | [usda.md](usda.md) |
| Ajustes Diarios (B3) | Mercado | - | - | [b3.md](b3.md) |
| Historico (B3) | Mercado | - | - | [b3.md](b3.md) |
| ZARC (MAPA) | Regulatorio | Join | - | [zarc.md](zarc.md) |
| Defensivos Formulados (MAPA) | Regulatorio | - | - | [defensivos.md](defensivos.md) |
| Autorizacoes de Defensivos (MAPA) | Regulatorio | - | - | [defensivos.md](defensivos.md) |
| Defensivos Tecnicos (MAPA) | Regulatorio | - | - | [defensivos.md](defensivos.md) |

**Legenda:**
- **Geo** = suporta saida geoespacial (marque "Saida geoespacial" no dock)
- **Join** = suporta join municipal (dados tabulares transformados em camada geoespacial via malha IBGE)
- **Auth** = requer token de autenticacao (configure em Configuracoes > Tokens)

## Por Categoria

### Ambiental (13 fontes)

Dados de meio ambiente, desmatamento, queimadas, areas protegidas e recursos hidricos.

- [Queimadas (INPE)](queimadas.md)
- [DETER e PRODES (INPE)](desmatamento.md)
- [Unidades de Conservacao (ICMBio)](icmbio.md)
- [Embargos (IBAMA)](ibama.md)
- [ANA — Irrigacao, Hidrografia, Pivos](ana.md)
- [SFB — CNFP, Concessoes, IFN](sfb.md)
- [Alertas (MapBiomas)](mapbiomas.md)

### Fundiario (4 fontes)

Dados de terras indigenas, quilombolas e cadastro ambiental rural.

- [Terras Indigenas (FUNAI)](funai.md)
- [Quilombolas (INCRA)](incra.md)
- [SICAR — Imoveis Rurais e Resumo CAR](sicar.md)

### Producao (6 fontes)

Dados de producao agricola e pecuaria.

- [IBGE — PAM, LSPA, PPM](ibge.md)
- [CONAB — Safras, Serie Historica, CEASA](conab.md)

### Mercado (7 fontes)

Dados de precos, cambio e expectativas de mercado.

- [Indicadores (CEPEA)](cepea.md)
- [BCB — PTAX, Focus, SGS](bcb.md)
- [PSD (USDA)](usda.md)
- [B3 — Ajustes e Historico](b3.md)

### Regulatorio (4 fontes)

Dados de zoneamento e defensivos agricolas.

- [ZARC (MAPA)](zarc.md)
- [Defensivos (MAPA)](defensivos.md)

## Fontes com Autenticacao

Duas fontes requerem token de API:

| Fonte | Variavel | Onde obter |
|-------|----------|------------|
| Alertas (MapBiomas) | `MAPBIOMAS_TOKEN` | [plataforma.alerta.mapbiomas.org](https://plataforma.alerta.mapbiomas.org) |
| PSD (USDA) | `USDA_API_KEY` | [apps.fas.usda.gov](https://apps.fas.usda.gov) |

Para configurar: dock agrobr > **Configuracoes** > aba **Tokens**.

## Join Municipal

Tres fontes suportam join municipal (dados tabulares -> camada geoespacial):

- **PAM (IBGE)** — coluna `codigo_municipio`
- **PPM (IBGE)** — coluna `codigo_municipio`
- **ZARC (MAPA)** — coluna `geocodigo`

Para usar: marque o checkbox **"Join municipal"** no painel de parametros. O plugin faz o join automatico com a malha municipal IBGE (SIRGAS 2000 / EPSG:4674).
