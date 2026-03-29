# Contributing to agrobr-qgis

**[Leia em Português](CONTRIBUTING.pt-BR.md)**

Contributions are welcome — bug reports, documentation improvements, new source adapters, or code fixes.

## How to contribute

### Reporting bugs

1. Check if it's already reported in [Issues](https://github.com/bruno-portfolio/agrobr-qgis/issues)
2. Open a new issue using the Bug Report template
3. Include: QGIS version, OS, agrobr version, logs from the "agrobr" tab in QgsMessageLog

### Pull Requests

1. Fork the repo and create a branch: `git checkout -b feat/short-description`
2. Write commits in the format `type: short description`
3. Write tests for all new functionality
4. Make sure `ruff check`, `mypy`, and `pytest` pass
5. Open a Pull Request describing what changed and why

For large changes, open an issue first for discussion.

## Development setup

```bash
git clone https://github.com/bruno-portfolio/agrobr-qgis.git
cd agrobr-qgis

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

pip install ruff mypy pytest pytest-cov pandas-stubs agrobr[geo]
pre-commit install
```

## Running tests

```bash
pytest tests/unit/ -v                 # Unit tests (no QGIS needed)
pytest tests/edge_cases/ -v           # Edge cases (no QGIS needed)
pytest tests/unit/ tests/edge_cases/ --cov=agrobr_qgis   # With coverage
```

QGIS tests require Docker:

```bash
docker run --rm -v $(pwd):/workspace qgis/qgis:4.0-trixie bash -c \
  "pip install pytest pytest-qgis agrobr[geo] && xvfb-run pytest /workspace/tests/qgis/ -v"
```

Coverage gate is **85%** with branch coverage.

## Linting and formatting

```bash
ruff check agrobr_qgis/ tests/       # Lint
ruff format agrobr_qgis/ tests/      # Format
mypy agrobr_qgis/                     # Type check (strict)
pre-commit run --all-files            # All hooks
```

## Code standards

- **Type hints required** on all production code
- **No comments** — code should be self-explanatory
- **Google style docstrings** only when signature + name aren't enough
- **Line length:** 100 characters
- **Python:** 3.12+
- Follow [agrobr](https://github.com/bruno-portfolio/agrobr) conventions

### Imports

```python
# Correct
from agrobr_qgis.core import registry
from agrobr_qgis.core.source_adapter import SourceAdapter

# Avoid
from agrobr_qgis.core.source_adapter import SourceAdapter, SourceCapability, ParamType
```

## Adding a new data source

Adding a source = creating 1 file in `agrobr_qgis/sources/`:

```python
from __future__ import annotations

from typing import Any

import pandas as pd

from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import (
    SourceAdapter,
    SourceCapability,
    SourceCategory,
)


@SourceRegistry.register
class MySourceSource(SourceAdapter):

    @classmethod
    def id(cls) -> str:
        return "my_source"

    @classmethod
    def name(cls) -> str:
        return "My Source (Agency)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import my_source  # type: ignore[import-untyped]

        return my_source.data(**kwargs)
```

Then:

1. Add the import in `agrobr_qgis/sources/__init__.py`
2. Create a fixture in `tests/mocks/fixtures/my_source.py` (real schema, 10 rows)
3. Add tests in `tests/unit/test_source_my_source.py`
4. Update `CHANGELOG.md`

## Updating the municipal mesh

When IBGE publishes a new mesh:

1. Download the simplified mesh
2. Compute SHA-256: `sha256sum municipios_simplificado.gpkg`
3. Update `MUNICIPAL_MESH_SHA256` in `agrobr_qgis/core/constants.py`
4. Bump minor version

## Commits

- Format: `type: short description`
- Types: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`, `perf`, `security`
- Messages in Portuguese (project convention)
- Reference issues when applicable: `fix: corrige join vazio (#42)`

## Questions?

Open an [issue](https://github.com/bruno-portfolio/agrobr-qgis/issues) with the `question` label.
