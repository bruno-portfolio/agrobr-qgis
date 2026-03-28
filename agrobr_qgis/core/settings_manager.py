from __future__ import annotations

import json

from .constants import DEFAULT_CRS


class SettingsManager:
    PREFIX = "agrobr/"

    @classmethod
    def is_cache_enabled(cls) -> bool:
        from qgis.core import QgsSettings  # type: ignore[import-untyped]

        result: bool = QgsSettings().value(f"{cls.PREFIX}cache_enabled", True, type=bool)
        return result

    @classmethod
    def set_cache_enabled(cls, enabled: bool) -> None:
        from qgis.core import QgsSettings  # type: ignore[import-untyped]

        QgsSettings().setValue(f"{cls.PREFIX}cache_enabled", enabled)

    @classmethod
    def get_default_crs(cls) -> str:
        from qgis.core import QgsSettings  # type: ignore[import-untyped]

        result: str = QgsSettings().value(f"{cls.PREFIX}default_crs", DEFAULT_CRS)
        return result

    @classmethod
    def set_default_crs(cls, crs: str) -> None:
        from qgis.core import QgsSettings  # type: ignore[import-untyped]

        QgsSettings().setValue(f"{cls.PREFIX}default_crs", crs)

    @classmethod
    def get_recent_sources(cls) -> list[str]:
        from qgis.core import QgsSettings  # type: ignore[import-untyped]

        raw: str = QgsSettings().value(f"{cls.PREFIX}recent_sources", "[]")
        result: list[str] = json.loads(raw) if raw else []
        return result

    @classmethod
    def add_recent_source(cls, source_id: str) -> None:
        from qgis.core import QgsSettings  # type: ignore[import-untyped]

        recent = cls.get_recent_sources()
        if source_id in recent:
            recent.remove(source_id)
        recent.insert(0, source_id)
        QgsSettings().setValue(f"{cls.PREFIX}recent_sources", json.dumps(recent[:10]))
