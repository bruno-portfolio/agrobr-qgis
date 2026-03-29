from __future__ import annotations

from typing import Any

import pandas as pd

from agrobr_qgis.core.registry import SourceRegistry
from agrobr_qgis.core.source_adapter import (
    SourceAdapter,
    SourceCapability,
    SourceCategory,
)


def _make_source(
    source_id: str,
    cat: SourceCategory = SourceCategory.AMBIENTAL,
    caps: SourceCapability = SourceCapability.TABULAR,
) -> type[SourceAdapter]:
    class _Source(SourceAdapter):
        @classmethod
        def id(cls) -> str:
            return source_id

        @classmethod
        def name(cls) -> str:
            return source_id.title()

        @classmethod
        def category(cls) -> SourceCategory:
            return cat

        @classmethod
        def capabilities(cls) -> SourceCapability:
            return caps

        def fetch(self, *, geo: bool = False, **_kwargs: Any) -> pd.DataFrame:
            _ = geo
            return pd.DataFrame()

    return _Source


class TestSourceRegistry:
    def test_register_and_get_roundtrip(self) -> None:
        src = _make_source("alpha")
        SourceRegistry.register(src)
        assert SourceRegistry.get("alpha") is src

    def test_list_all(self) -> None:
        SourceRegistry.register(_make_source("a"))
        SourceRegistry.register(_make_source("b"))
        assert len(SourceRegistry.list_all()) == 2

    def test_list_by_category(self) -> None:
        SourceRegistry.register(_make_source("env1", cat=SourceCategory.AMBIENTAL))
        SourceRegistry.register(_make_source("reg1", cat=SourceCategory.REGULATORIO))
        result = SourceRegistry.list_by_category(SourceCategory.AMBIENTAL)
        assert len(result) == 1
        assert result[0].id() == "env1"

    def test_list_by_capability_bitwise(self) -> None:
        SourceRegistry.register(
            _make_source("geo1", caps=SourceCapability.GEO | SourceCapability.TABULAR)
        )
        SourceRegistry.register(_make_source("tab1", caps=SourceCapability.TABULAR))
        geo_sources = SourceRegistry.list_by_capability(SourceCapability.GEO)
        assert len(geo_sources) == 1
        assert geo_sources[0].id() == "geo1"

    def test_clear(self) -> None:
        SourceRegistry.register(_make_source("x"))
        assert len(SourceRegistry.list_all()) == 1
        SourceRegistry.clear()
        assert len(SourceRegistry.list_all()) == 0

    def test_duplicate_id_overwrites(self) -> None:
        src1 = _make_source("dup")
        src2 = _make_source("dup")
        SourceRegistry.register(src1)
        SourceRegistry.register(src2)
        assert SourceRegistry.get("dup") is src2

    def test_get_nonexistent_returns_none(self) -> None:
        assert SourceRegistry.get("nonexistent") is None

    def test_register_as_decorator(self) -> None:
        @SourceRegistry.register
        class _Decorated(SourceAdapter):
            @classmethod
            def id(cls) -> str:
                return "decorated"

            @classmethod
            def name(cls) -> str:
                return "Decorated"

            @classmethod
            def category(cls) -> SourceCategory:
                return SourceCategory.PRODUCAO

            def fetch(self, *, geo: bool = False, **_kwargs: Any) -> pd.DataFrame:
                _ = geo
                return pd.DataFrame()

        assert SourceRegistry.get("decorated") is _Decorated
