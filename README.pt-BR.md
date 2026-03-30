# agrobr-qgis

> Dados agrícolas brasileiros no QGIS em um clique

[![Tests](https://github.com/bruno-portfolio/agrobr-qgis/actions/workflows/tests.yml/badge.svg)](https://github.com/bruno-portfolio/agrobr-qgis/actions/workflows/tests.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![QGIS 4.0+](https://img.shields.io/badge/QGIS-4.0+-93b023.svg)](https://qgis.org/)
[![License: GPL-2.0+](https://img.shields.io/badge/License-GPL--2.0+-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![agrobr](https://img.shields.io/badge/powered%20by-agrobr-orange.svg)](https://pypi.org/project/agrobr/)

**[Read in English](README.md)**

Plugin QGIS 4 que expõe os dados da biblioteca [agrobr](https://pypi.org/project/agrobr/) como camadas geoespaciais e tabulares, com interface gráfica nativa Qt6.

Centraliza 24 fontes de dados agrícolas brasileiros (IBGE, CONAB, INPE, IBAMA, MapBiomas, etc.) em um único plugin, eliminando ETL manual, downloads dispersos e joins manuais com malha municipal.

## Requisitos

| Componente | Versão |
|------------|--------|
| QGIS | 4.0+ |
| Python | 3.12+ |
| agrobr | >=1.0.0,<2.0.0 |

> **QGIS 3.x não é suportado.** O plugin targeta exclusivamente QGIS 4 / Qt6.

## Instalação

### Via Plugin Manager (recomendado)

1. Abra QGIS 4
2. Menu **Plugins → Manage and Install Plugins**
3. Busque por **agrobr**
4. Clique **Install Plugin**

O plugin instala a dependência `agrobr[geo]` automaticamente na primeira execução.

### Manual

```bash
pip install agrobr[geo]
```

Copie a pasta `agrobr_qgis/` para o diretório de plugins do QGIS:

- **Linux:** `~/.local/share/QGIS/QGIS4/profiles/default/python/plugins/`
- **Windows:** `%APPDATA%\QGIS\QGIS4\profiles\default\python\plugins\`
- **macOS:** `~/Library/Application Support/QGIS/QGIS4/profiles/default/python/plugins/`

## Uso

1. Ative o plugin no Plugin Manager
2. O dock **agrobr** aparece na lateral
3. Navegue pelas categorias de fontes (Ambiental, Produção, Fundiário, Regulatório)
4. Selecione uma fonte, preencha os parâmetros
5. Clique **Buscar Dados**
6. Visualize o resumo (feições, CRS, tipo de geometria)
7. **Adicionar ao mapa** como camada

### Fontes Geoespaciais

Queimadas (INPE), Desmatamento (PRODES/DETER), FUNAI, ICMBio, INCRA, IBAMA, SICAR, ANA, SFB, MapBiomas Alerta.

### Fontes Tabulares

CONAB, IBGE, ZARC.

Fontes tabulares podem ser convertidas em camadas geoespaciais via **join municipal automático** com a malha IBGE.

### Templates

Workflows pré-configurados que combinam múltiplas fontes em um clique:

- **Raio-X Ambiental** — Queimadas, DETER, Embargos, SICAR e UCs para uma UF
- **Análise de Produção** — PAM (IBGE) e Série Histórica (CONAB) para um produto
- **Risco Climático** — ZARC e PAM para avaliar risco de uma cultura

### Processing Toolbox

Cada fonte também está disponível como algoritmo no Processing Toolbox do QGIS, permitindo uso em modelos, batch processing e scripts.

## Funcionalidades

- **Background-first** — todo fetch roda em background, UI nunca bloqueia
- **Offline-first** — cache do agrobr permite uso sem internet
- **Memory-first** — camadas pequenas em memória, GPKG automático para grandes volumes
- **Join municipal** — dados tabulares → malha IBGE com um checkbox
- **Validação automática** — CRS, geometrias inválidas, encoding, timezone
- **Busca de fontes** — filtro por nome, descrição ou categoria
- **Health check** — status online/offline por fonte
- **Proxy corporativo** — propaga configuração de proxy do QGIS automaticamente
- **Animação temporal** — fontes com dimensão temporal (queimadas, DETER, MapBiomas)
- **Estilos automáticos** — simbologia QML por tipo de geometria
- **Templates** — workflows multi-fonte pré-configurados
- **Persistência** — parâmetros salvos junto com o projeto QGIS
- **Post-fetch** — abrir tabela, salvar como (GPKG/GeoJSON/SHP), ver origem

## Arquitetura

```
agrobr_qgis/
  core/          # Lógica de negócio (sem Qt GUI)
  sources/       # 1 adapter por fonte (Registry pattern)
  gui/           # Interface Qt6 (dock, painéis, widgets)
  processing/    # Processing Provider (1 algoritmo por fonte)
```

## Desenvolvimento

```bash
git clone https://github.com/bruno-portfolio/agrobr-qgis.git
cd agrobr-qgis

pip install ruff mypy pytest pytest-cov agrobr[geo]
pre-commit install
```

```bash
ruff check agrobr_qgis/ tests/       # Lint
mypy agrobr_qgis/                     # Type check
pytest tests/unit/ -v                 # Testes unitários
pytest tests/edge_cases/ -v           # Edge cases
```

Veja [CONTRIBUTING.pt-BR.md](CONTRIBUTING.pt-BR.md) para o guia completo.

## Licença

- **Plugin:** GPL-2.0-or-later — veja [LICENSE](LICENSE)
- **agrobr:** MIT (compatível)
- **Dados:** pertencem às respectivas fontes públicas
