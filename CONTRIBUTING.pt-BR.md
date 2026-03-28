# Contribuindo para o agrobr-qgis

Contribuições são bem-vindas — bug reports, melhorias de documentação, novos adapters de fontes ou correções de código.

## Como contribuir

### Reportando bugs

1. Verifique se já não foi reportado nas [Issues](https://github.com/bruno-portfolio/agrobr-qgis/issues)
2. Abra uma nova issue usando o template de Bug Report
3. Inclua: versão do QGIS, OS, versão do agrobr, logs da aba "AgroBR" no QgsMessageLog

### Pull Requests

1. Fork o repositório e crie uma branch: `git checkout -b feat/descricao-curta`
2. Faça commits no formato `tipo: descrição curta`
3. Escreva testes para toda funcionalidade nova
4. Certifique-se que `ruff check`, `mypy` e `pytest` passam
5. Abra um Pull Request com descrição do que muda e por quê

Para mudanças grandes, abra uma issue primeiro para discussão.

## Setup de desenvolvimento

```bash
git clone https://github.com/bruno-portfolio/agrobr-qgis.git
cd agrobr-qgis

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

pip install ruff mypy pytest pytest-cov pandas-stubs agrobr[geo]
pre-commit install
```

## Rodando testes

```bash
pytest tests/unit/ -v                 # Unitários (sem QGIS)
pytest tests/edge_cases/ -v           # Edge cases (sem QGIS)
pytest tests/unit/ tests/edge_cases/ --cov=agrobr_qgis   # Com cobertura
```

Testes QGIS requerem Docker:

```bash
docker run --rm -v $(pwd):/workspace qgis/qgis:4.0-trixie bash -c \
  "pip install pytest pytest-qgis agrobr[geo] && xvfb-run pytest /workspace/tests/qgis/ -v"
```

O coverage gate é **85%** com branch coverage.

## Linting e formatação

```bash
ruff check agrobr_qgis/ tests/       # Lint
ruff format agrobr_qgis/ tests/      # Formatar
mypy agrobr_qgis/                     # Type check (strict)
pre-commit run --all-files            # Todos os hooks
```

## Padrões de código

- **Type hints obrigatórios** em todo código de produção
- **Sem comentários** — código autoexplicativo
- **Docstrings Google style** apenas quando assinatura + nome não bastam
- **Line length:** 100 caracteres
- **Python:** 3.12+
- Seguir padrões do [agrobr](https://github.com/bruno-portfolio/agrobr)

### Imports

```python
# Correto
from agrobr_qgis.core import registry
from agrobr_qgis.core.source_adapter import SourceAdapter

# Evitar
from agrobr_qgis.core.source_adapter import SourceAdapter, SourceCapability, ParamType
```

## Adicionando nova fonte de dados

Adicionar uma fonte = criar 1 arquivo em `agrobr_qgis/sources/`:

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
class MinhaFonteSource(SourceAdapter):

    @classmethod
    def id(cls) -> str:
        return "minha_fonte"

    @classmethod
    def name(cls) -> str:
        return "Minha Fonte (Órgão)"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        from agrobr.sync import minha_fonte  # type: ignore[import-untyped]

        return minha_fonte.dados(**kwargs)
```

Depois:

1. Adicionar import em `agrobr_qgis/sources/__init__.py`
2. Criar fixture em `tests/mocks/fixtures/minha_fonte.py` (schema real, 10 rows)
3. Adicionar testes em `tests/unit/test_source_minha_fonte.py`
4. Atualizar `CHANGELOG.md`

## Atualizando a malha municipal

Quando o IBGE publicar nova malha:

1. Baixar malha simplificada
2. Calcular SHA-256: `sha256sum municipios_simplificado.gpkg`
3. Atualizar `MUNICIPAL_MESH_SHA256` em `agrobr_qgis/core/constants.py`
4. Bump minor version

## Commits

- Formato: `tipo: descrição curta`
- Tipos: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`, `perf`, `security`
- Mensagens em português
- Referencie issues quando aplicável: `fix: corrige join vazio (#42)`

## Dúvidas?

Abra uma [issue](https://github.com/bruno-portfolio/agrobr-qgis/issues) com a label `question`.
