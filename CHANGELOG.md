# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.2.0] - 2026-03-29

### Added
- Thread-safety: `RLock` em `LayerBuilder._temp_dir` e `cleanup_temp()`, `os.environ.setdefault` para `AGROBR_LOG_LEVEL`
- Ícone customizado do plugin (substitui ícone genérico do QGIS)
- Estilos QML automáticos por tipo de geometria (point, polygon, line) em `styles/`
- Animação temporal: `temporal_column()` em 6 fontes (queimadas, deter, mapbiomas, cepea, bcb_ptax, bcb_sgs)
- Post-fetch actions: 3 novos botões — "Abrir Tabela", "Salvar como...", "Ver Origem"
- `source_url()` em 9 fontes com URL pública conhecida
- Persistência de parâmetros via `QgsProject` (save/restore ao abrir projeto)
- Health check: probe HTTP HEAD com fallback GET, ícones verde/cinza na árvore de fontes
- `health_url()` em 5 fontes (IBGE, BCB, INPE, CEPEA)
- Templates multi-fonte: `ParamBinding` explícito, `TemplateRegistry` com validação em tempo de registro
- 3 templates built-in: Raio-X Ambiental, Análise de Produção, Risco Climático
- `TemplateFetchTask`: execução sequencial, signals só em `finished()` (thread-safe)
- `FetchController`: extração do pipeline fetch do dock (encapsula lookup → task → signals)
- `DockState.TEMPLATE_RESULT` e UI de resultado parcial (por fonte, com ✓/✗)
- `ITEM_TYPE_ROLE` na árvore para discriminar source vs template (type-safe, sem string prefix)
- 39 edge case tests (12 arquivos): empty data, geometrias inválidas, CRS, encoding, timeout, cancelamento, auth, thresholds
- 18 testes de template (registry, resolve_params, partial failure)
- 11 testes de health check (cache TTL, probe HEAD/GET/timeout, httpx import seguro)
- Input strip inline em `collect_params()` e `processAlgorithm()` (contra whitespace via copy-paste)
- 406 testes totais, ruff + mypy clean em 52 arquivos

### Fixed
- Race condition: `AGROBR_LOG_LEVEL` setado/restaurado por task removido, agora único no `initGui()`
- Race condition: `_get_temp_dir()` check-then-act sem lock corrigido com `RLock`
- `_via_gpkg()`: `gdf.to_file()` movido para fora do lock (evita bloqueio de I/O em disco)
- Cancel (Escape) agora funciona para template fetches (não só fetches individuais)
- `FetchController._connections` agora corretamente populada (antes era no-op)
- `templates.py` importado em `plugin.py` (antes era dead code — templates nunca registrados)
- `expandAll()` no filtro de busca desconecta `expanded` signal antes (evita burst de health checks)
- `_on_error_internal` delegado para `_on_error` (eliminada duplicação)
- `ParamCache._cache` não mais acessado diretamente — adicionados `to_dict()`/`from_dict()`

### Changed
- `dock.py`: refatorado com `FetchController` + dispatch template/source (454 linhas, era 329)
- `SourceAdapter`: +3 classmethods (`temporal_column`, `source_url`, `health_url`) com TODO para SourceMeta
- `param_panel.build()`: aceita `list[Any]` para compatibilidade com `TemplateParam`
- `source_tree.py`: categorias começam colapsadas (antes `expandAll()` no init)

## [0.1.0] - 2026-03-29

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
- Hierarquia de exceções: agrobrError → FetchError, ContractError, JoinError, AuthError, DependencyError, ChecksumError
- Primeiro adapter + pipeline (Fase 2): queimadas (INPE) como fonte piloto
- QueimadasSource: GEO | TABULAR | TEMPORAL, fetch via agrobr.sync com lazy import
- LayerBuilder: memory-first com GPKG fallback (threshold 50k rows / 2M vértices), TemporaryDirectory gerenciado
- FetchTask (QgsTask): fetch → validate → join opcional em background, cancelamento cooperativo
- Mock router e fixture queimadas (schema real INPE, 10 rows, inclui geom inválida + nula)
- 151 testes unitários (Fase 1 + Fase 2)
- Plugin lifecycle (Fase 3): classFactory, agrobrStub, agrobrPlugin
- DependencyDoctor: check() via importlib + auto_install() com allowlist e sys.path fix (OSGeo4W)
- Proxy corporativo: propagate_proxy() lê QgsSettings e seta HTTP_PROXY/HTTPS_PROXY
- agrobrPlugin skeleton: initGui() chama propagate_proxy(), unload() chama cleanup_temp()
- agrobrStub: QMessageBox.warning + Logger.error quando agrobr não está instalado
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

### Fixed
- Provider: agrobrProvider herda de QgsProcessingProvider (era stub sem herança)
- Queimadas adapter: params corrigidos pra `ano`, `mes`, `dia`, `uf` (API espera int, não DATE)
- PAM/PPM adapters: `localidade_to_code()` mapeia "Municipio - UF" → CD_MUN via malha IBGE
- ZARC adapter: `join_column` corrigido pra `geocodigo` (nome real da coluna)
- FetchTask: join só executado se coluna existe no DataFrame (previne KeyError com dados vazios)
- Dock: QShortcuts armazenados como atributos (previne garbage collection do PyQt6)
- Dock: ParamCache salva params ao trocar de fonte (não só no fetch)
- Dock: QScrollArea no painel de params (QgsExtentGroupBox não trava mais o splitter)
- Dock: `_dock_tr()` crash corrigido (brand name hardcoded, não precisa de tr)

### Changed
- Branding: AgroBR → agrobr em todas as strings de UI, logger TAG, auth config, metadata
- Classes renomeadas: agrobrPlugin, agrobrStub, agrobrProvider, agrobrError
- SpatialJoin: novo método público `localidade_to_code()` para mapear nomes IBGE → códigos
- Autor: "Bruno" → "Bruno Escalhão" em metadata.txt e pyproject.toml
- Documentação: guia de instalação, guia por fonte (18 docs), troubleshooting
- Contagem de fontes corrigida: 38+ → 34 (READMEs e metadata)
- Paths de instalação corrigidos: QGIS3 → QGIS4 (READMEs)
