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
- 124 testes unitários cobrindo 99.5% do core
