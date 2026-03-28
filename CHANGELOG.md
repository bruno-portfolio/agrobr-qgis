# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- Setup inicial do projeto (Fase 0)
- Estrutura de diretórios, pyproject.toml, pre-commit, CI/CD
- Configuração ruff, mypy strict, pytest com 85% coverage threshold
- GitHub Actions: lint, typecheck, unit tests, QGIS Docker tests
- Release workflow via qgis-plugin-ci
- Core puro sem Qt (Fase 1): constants, exceptions, logger, source_adapter, registry, data_contract
- SourceAdapter ABC com SourceCategory, SourceCapability (Flag), ParamType (StrEnum)
- SourceRegistry com register/get/list/clear e suporte a decorator
- DataContract com validação NFC, duplicatas, timezone strip, CRS default, make_valid, vertex estimation
- Logger com lazy imports para qgis.* (testável sem QGIS)
- Hierarquia de exceções: AgroBRError → FetchError, ContractError, JoinError, AuthError, DependencyError, ChecksumError
- Primeiro adapter + pipeline (Fase 2): queimadas (INPE) como fonte piloto
- QueimadasSource: GEO | TABULAR | TEMPORAL, fetch via agrobr.sync com lazy import
- LayerBuilder: memory-first com GPKG fallback (threshold 50k rows / 2M vértices), TemporaryDirectory gerenciado
- FetchTask (QgsTask): fetch → validate → join opcional em background, cancelamento cooperativo
- Mock router e fixture queimadas (schema real INPE, 10 rows, inclui geom inválida + nula)
- 151 testes unitários (Fase 1 + Fase 2)
- Plugin lifecycle (Fase 3): classFactory, AgroBRStub, AgroBRPlugin
- DependencyDoctor: check() via importlib + auto_install() com allowlist e sys.path fix (OSGeo4W)
- Proxy corporativo: propagate_proxy() lê QgsSettings e seta HTTP_PROXY/HTTPS_PROXY
- AgroBRPlugin skeleton: initGui() chama propagate_proxy(), unload() chama cleanup_temp()
- AgroBRStub: QMessageBox.warning + Logger.error quando agrobr não está instalado
- 170 testes unitários (Fase 1 + Fase 2 + Fase 3)
- GUI completa (Fase 4): dock principal, árvore de fontes, painel de parâmetros, resultado, settings dialog
- DockState (5 estados) com STATE_CONFIG centralizado e ParamCache in-memory
- SourceTreeWidget: QTreeView + QSortFilterProxyModel, 34 fontes em 5 categorias com busca
- ParamPanel: construtor dinâmico por ParamType, checkboxes GEO/JOIN, auth check
- ResultPanel: resumo ContractResult + ações (Adicionar ao Mapa, Zoom, Buscar Novamente)
- SettingsDialog: cache, CRS padrão, gerenciamento de tokens para fontes AUTH
- MainDock: orchestrador com signal cleanup Qt6, task identity check, progress bar
- FetchTask: progresso granular (10/60/80/100%) via setProgress()
- UF_LIST centralizado em constants.py
- 338 testes unitários, 91% coverage
