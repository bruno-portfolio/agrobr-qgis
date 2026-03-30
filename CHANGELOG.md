# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.1.0] - 2026-03-29

### Added
- Plugin QGIS 4 completo com GUI nativa Qt6 (dock, árvore de fontes, painel de parâmetros, resultado)
- 24 fontes de dados agrícolas brasileiros via biblioteca agrobr
- Fontes geoespaciais: Queimadas (INPE), DETER, PRODES, FUNAI, ICMBio, INCRA, IBAMA, SICAR, ANA (4), SFB (3), MapBiomas Alerta
- Fontes tabulares: CONAB (3), IBGE (3), ZARC
- Processing Toolbox: cada fonte disponível como algoritmo (tipo coercion, FeatureSink, estilo QML)
- Templates multi-fonte: Raio-X Ambiental, Análise de Produção, Risco Climático
- SourceAdapter ABC com SourceCategory, SourceCapability (Flag), ParamType (StrEnum)
- SourceRegistry thread-safe com decorator `@register`
- DataContract: validação NFC, duplicatas, timezone strip, CRS default, make_valid, vertex estimation
- LayerBuilder: memory-first com GPKG fallback (50k rows / 2M vértices)
- FetchTask (QgsTask): fetch com timeout enforcement, cancelamento cooperativo, join municipal opcional
- FetchController: encapsula lookup → task → signals
- Estilos QML automáticos por tipo de geometria (point, polygon, line)
- Animação temporal em 3 fontes (queimadas, deter, mapbiomas)
- Post-fetch actions: Adicionar ao Mapa, Zoom, Abrir Tabela, Salvar como, Ver Origem
- Persistência de parâmetros via QgsProject
- Health check: probe HTTP HEAD com fallback GET, cache TTL 30min, ícones na árvore
- DependencyDoctor: auto-install agrobr[geo] com detecção de versão
- Proxy corporativo: propaga configuração do QGIS automaticamente
- DockState (6 estados) com STATE_CONFIG centralizado e ParamCache in-memory
- Thread-safety: locks em SourceRegistry, HealthCache, LayerBuilder
- 392 testes (unit + edge cases), ruff + mypy strict clean
- CI/CD: GitHub Actions (lint, typecheck, unit tests, QGIS Docker tests, release)
- Documentação: guia de instalação, guia por fonte (14 docs), troubleshooting
