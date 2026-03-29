from __future__ import annotations

import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .source_adapter import SourceAdapter, SourceCapability, SourceCategory


class SourceRegistry:
    _sources: dict[str, type[SourceAdapter]] = {}
    _lock: threading.Lock = threading.Lock()

    @classmethod
    def register(cls, source_class: type[SourceAdapter]) -> type[SourceAdapter]:
        with cls._lock:
            cls._sources[source_class.id()] = source_class
        return source_class

    @classmethod
    def get(cls, source_id: str) -> type[SourceAdapter] | None:
        with cls._lock:
            return cls._sources.get(source_id)

    @classmethod
    def list_all(cls) -> list[type[SourceAdapter]]:
        with cls._lock:
            return list(cls._sources.values())

    @classmethod
    def list_by_category(cls, category: SourceCategory) -> list[type[SourceAdapter]]:
        with cls._lock:
            return [s for s in cls._sources.values() if s.category() == category]

    @classmethod
    def list_by_capability(cls, cap: SourceCapability) -> list[type[SourceAdapter]]:
        with cls._lock:
            return [s for s in cls._sources.values() if s.capabilities() & cap]

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            cls._sources.clear()
