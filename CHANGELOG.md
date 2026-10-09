# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.2.0] - 2026-10-09

### Changed
- Requer a agrobr 2.x (`agrobr[geo]>=2.0.0,<3`): auto-instalação, `requirements.txt`, CI e instruções de
  instalação usam o mesmo intervalo, com o comando manual entre aspas
- Parâmetros com os nomes da agrobr 2.0, na GUI e no Processing (modelos e scripts com os nomes antigos
  precisam trocá-los):
  - ANA (demanda, disponibilidade, hidrografia, pivôs): `max_features` → `max_registros`
  - CONAB Série Histórica: `inicio`/`fim` → `ano_inicio`/`ano_fim`
  - DETER: `data_inicio`/`data_fim` → `inicio`/`fim`
  - MapBiomas Alertas: `start_date`/`end_date`/`limit` → `inicio`/`fim`/`max_registros` (teto total de
    registros, não por página)
  - ZARC: `cultura` → `produto` (a coluna de saída continua `cultura`)
  - PRODES: `data_inicio`/`data_fim` → `ano`; a agrobr nunca leu datas no PRODES
- `municipio` no SICAR e no ZARC aceita o nome inteiro ou o código IBGE; pedaço do nome é recusado
- DETER oferece só Amazônia e Cerrado, os biomas que o DETER publica

### Added
- Com a agrobr 1.x instalada, o plugin pergunta antes de atualizá-la para a 2.x: sim atualiza e pede para
  reiniciar o QGIS; não mostra o comando manual. Com uma agrobr de major mais nova, mostra uma mensagem e não a
  rebaixa
- Testes que conferem cada chamada à agrobr contra a assinatura real da 2.0

### Fixed
- GUI: campo inteiro opcional vazio deixa de ir como `0` (a agrobr 2.0 recusa `ano=0`, `mes=0` e
  `max_registros=0`)
- MapBiomas Alertas: o token salvo nas configurações chega à agrobr; antes, só a variável de ambiente valia
- Animação temporal do DETER (coluna `data`) e do MapBiomas Alertas (coluna `data_deteccao`), que procurava
  colunas que a agrobr não publica

## [0.1.1] - 2026-04-11

### Added
- MapBiomas Cobertura: tile service WMS (Collection 10, 1985-2024)

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
