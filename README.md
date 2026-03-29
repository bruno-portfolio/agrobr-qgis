# agrobr-qgis

> Brazilian agricultural data in QGIS with one click

[![Tests](https://github.com/bruno-portfolio/agrobr-qgis/actions/workflows/tests.yml/badge.svg)](https://github.com/bruno-portfolio/agrobr-qgis/actions/workflows/tests.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![QGIS 4.0+](https://img.shields.io/badge/QGIS-4.0+-93b023.svg)](https://qgis.org/)
[![License: GPL-2.0+](https://img.shields.io/badge/License-GPL--2.0+-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![agrobr](https://img.shields.io/badge/powered%20by-agrobr-orange.svg)](https://pypi.org/project/agrobr/)

**[Leia em Português](README.pt-BR.md)**

QGIS 4 plugin that exposes [agrobr](https://pypi.org/project/agrobr/) library data as geospatial and tabular layers, with native Qt6 GUI.

Centralizes 38+ Brazilian agricultural data sources (IBGE, CONAB, CEPEA, INPE, IBAMA, BCB, USDA, MapBiomas, etc.) in a single plugin, eliminating manual ETL, scattered downloads, and manual joins with municipal boundaries.

## Requirements

| Component | Version |
|-----------|---------|
| QGIS | 4.0+ |
| Python | 3.12+ |
| agrobr | >=1.0.0,<2.0.0 |

> **QGIS 3.x is not supported.** This plugin targets QGIS 4 / Qt6 exclusively.

## Installation

### Via Plugin Manager (recommended)

1. Open QGIS 4
2. Go to **Plugins → Manage and Install Plugins**
3. Search for **agrobr**
4. Click **Install Plugin**

The plugin auto-installs the `agrobr[geo]` dependency on first run.

### Manual

```bash
pip install agrobr[geo]
```

Copy the `agrobr_qgis/` folder to the QGIS plugins directory:

- **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
- **Windows:** `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
- **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

## Usage

1. Enable the plugin in Plugin Manager
2. The **agrobr** dock panel appears on the side
3. Browse source categories (Environmental, Production, Market, Credit, Climate)
4. Select a source, fill in parameters
5. Click **Fetch Data**
6. Review the summary (features, CRS, geometry type)
7. **Add to map** as a layer

### Geospatial Sources

Wildfire hotspots (INPE), Deforestation (PRODES/DETER), FUNAI, ICMBio, INCRA, IBAMA, SICAR, ANA, SFB, MapBiomas Alerts.

### Tabular Sources

CEPEA, CONAB, IBGE, BCB, USDA, B3, ZARC, Pesticides.

Tabular sources can be converted to geospatial layers via **automatic municipal join** with the IBGE boundary mesh.

### Processing Toolbox

Each source is also available as a Processing Toolbox algorithm, enabling use in models and scripts.

## Features

- **Background-first** — all fetches run in background, UI never blocks
- **Offline-first** — agrobr cache enables offline usage
- **Memory-first** — small layers in memory, automatic GPKG fallback for large datasets
- **Municipal join** — tabular data → IBGE mesh with a single checkbox
- **Auto-validation** — CRS, invalid geometries, encoding, timezone
- **Source search** — filter by name, description, or category
- **Health check** — online/offline status per source
- **Corporate proxy** — auto-propagates QGIS proxy settings

## Architecture

```
agrobr_qgis/
  core/          # Business logic (no Qt GUI)
  sources/       # 1 adapter per source (Registry pattern)
  gui/           # Qt6 interface (dock, panels, widgets)
  processing/    # Processing Provider (1 algorithm per source)
```

## Development

```bash
git clone https://github.com/bruno-portfolio/agrobr-qgis.git
cd agrobr-qgis

pip install ruff mypy pytest pytest-cov agrobr[geo]
pre-commit install
```

```bash
ruff check agrobr_qgis/ tests/       # Lint
mypy agrobr_qgis/                     # Type check
pytest tests/unit/ -v                 # Unit tests
pytest tests/edge_cases/ -v           # Edge cases
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## License

- **Plugin:** GPL-2.0-or-later — see [LICENSE](LICENSE)
- **agrobr:** MIT (compatible)
- **Data:** belongs to their respective public sources
