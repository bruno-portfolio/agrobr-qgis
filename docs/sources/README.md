# Fontes de Dados

O plugin agrobr disponibiliza 24 fontes de dados em 4 categorias.

## Resumo

| Fonte | Categoria | Geo | Auth | Guia |
|-------|-----------|:---:|:----:|------|
| Queimadas (INPE) | Ambiental | Sim | - | [queimadas.md](queimadas.md) |
| DETER (INPE) | Ambiental | Sim | - | [desmatamento.md](desmatamento.md) |
| PRODES (INPE) | Ambiental | Sim | - | [desmatamento.md](desmatamento.md) |
| Unidades de Conservação (ICMBio) | Ambiental | Sim | - | [icmbio.md](icmbio.md) |
| Embargos (IBAMA) | Ambiental | Sim | - | [ibama.md](ibama.md) |
| Demanda de Irrigação (ANA) | Ambiental | Sim | - | [ana.md](ana.md) |
| Disponibilidade Hídrica (ANA) | Ambiental | Sim | - | [ana.md](ana.md) |
| Hidrografia (ANA) | Ambiental | Sim | - | [ana.md](ana.md) |
| Pivôs de Irrigação (ANA) | Ambiental | Sim | - | [ana.md](ana.md) |
| CNFP (SFB) | Ambiental | Sim | - | [sfb.md](sfb.md) |
| Concessões Florestais (SFB) | Ambiental | Sim | - | [sfb.md](sfb.md) |
| IFN Conglomerados (SFB) | Ambiental | Sim | - | [sfb.md](sfb.md) |
| Alertas (MapBiomas) | Ambiental | Sim | Sim | [mapbiomas.md](mapbiomas.md) |
| Terras Indígenas (FUNAI) | Fundiário | Sim | - | [funai.md](funai.md) |
| Quilombolas (INCRA) | Fundiário | Sim | - | [incra.md](incra.md) |
| Imóveis Rurais (SICAR) | Fundiário | Sim | - | [sicar.md](sicar.md) |
| Resumo CAR (SICAR) | Fundiário | - | - | [sicar.md](sicar.md) |
| PAM (IBGE) | Produção | Join | - | [ibge.md](ibge.md) |
| LSPA (IBGE) | Produção | - | - | [ibge.md](ibge.md) |
| PPM (IBGE) | Produção | Join | - | [ibge.md](ibge.md) |
| Safras (CONAB) | Produção | - | - | [conab.md](conab.md) |
| Série Histórica (CONAB) | Produção | - | - | [conab.md](conab.md) |
| CEASA Preços (CONAB) | Produção | - | - | [conab.md](conab.md) |
| ZARC (MAPA) | Regulatório | Join | - | [zarc.md](zarc.md) |

**Legenda:**
- **Geo** = suporta saída geoespacial (marque "Saída geoespacial" no dock)
- **Join** = suporta join municipal (dados tabulares transformados em camada geoespacial via malha IBGE)
- **Auth** = requer token de autenticação (configure em Configurações > Tokens)

## Por Categoria

### Ambiental (13 fontes)

Dados de meio ambiente, desmatamento, queimadas, áreas protegidas e recursos hídricos.

- [Queimadas (INPE)](queimadas.md)
- [DETER e PRODES (INPE)](desmatamento.md)
- [Unidades de Conservação (ICMBio)](icmbio.md)
- [Embargos (IBAMA)](ibama.md)
- [ANA — Irrigação, Hidrografia, Pivôs](ana.md)
- [SFB — CNFP, Concessões, IFN](sfb.md)
- [Alertas (MapBiomas)](mapbiomas.md)

### Fundiário (4 fontes)

Dados de terras indígenas, quilombolas e cadastro ambiental rural.

- [Terras Indígenas (FUNAI)](funai.md)
- [Quilombolas (INCRA)](incra.md)
- [SICAR — Imóveis Rurais e Resumo CAR](sicar.md)

### Produção (6 fontes)

Dados de produção agrícola e pecuária.

- [IBGE — PAM, LSPA, PPM](ibge.md)
- [CONAB — Safras, Série Histórica, CEASA](conab.md)

### Regulatório (1 fonte)

Dados de zoneamento agrícola.

- [ZARC (MAPA)](zarc.md)

## Fontes com Autenticação

Uma fonte requer token de API:

| Fonte | Variável | Onde obter |
|-------|----------|------------|
| Alertas (MapBiomas) | `MAPBIOMAS_TOKEN` | [plataforma.alerta.mapbiomas.org](https://plataforma.alerta.mapbiomas.org) |

Para configurar: dock agrobr > **Configurações** > aba **Tokens**.

## Join Municipal

Três fontes suportam join municipal (dados tabulares -> camada geoespacial):

- **PAM (IBGE)** — coluna `codigo_municipio`
- **PPM (IBGE)** — coluna `codigo_municipio`
- **ZARC (MAPA)** — coluna `geocodigo`

Para usar: marque o checkbox **"Join municipal"** no painel de parâmetros. O plugin faz o join automático com a malha municipal IBGE (SIRGAS 2000 / EPSG:4674).
