from __future__ import annotations

import time
from dataclasses import dataclass
from typing import ClassVar, Literal

from qgis.core import QgsTask  # type: ignore[import-untyped]
from qgis.PyQt.QtCore import pyqtSignal  # type: ignore[import-untyped]

from .constants import HEALTH_CHECK_TIMEOUT_SECONDS
from .registry import SourceRegistry


@dataclass
class HealthStatus:
    source_id: str
    status: Literal["online", "offline", "unchecked"]
    checked_at: float | None = None
    response_ms: int | None = None


class HealthCache:
    TTL_SECONDS: ClassVar[int] = 1800
    _cache: ClassVar[dict[str, HealthStatus]] = {}

    @classmethod
    def get(cls, source_id: str) -> HealthStatus:
        cached = cls._cache.get(source_id)
        if (
            cached
            and cached.checked_at is not None
            and (time.monotonic() - cached.checked_at) < cls.TTL_SECONDS
        ):
            return cached
        return HealthStatus(source_id, "unchecked")

    @classmethod
    def set(cls, status: HealthStatus) -> None:
        cls._cache[status.source_id] = status

    @classmethod
    def is_stale(cls, source_id: str) -> bool:
        cached = cls._cache.get(source_id)
        if cached is None or cached.checked_at is None:
            return True
        return (time.monotonic() - cached.checked_at) >= cls.TTL_SECONDS

    @classmethod
    def clear(cls) -> None:
        cls._cache.clear()


class HealthCheckTask(QgsTask):  # type: ignore[misc]
    allChecked = pyqtSignal(list)

    def __init__(self, source_ids: list[str]) -> None:
        super().__init__("Health check", QgsTask.CanCancel)
        self._source_ids = source_ids
        self._statuses: list[HealthStatus] = []

    def run(self) -> bool:
        for sid in self._source_ids:
            if self.isCanceled():
                return False
            adapter_cls = SourceRegistry.get(sid)
            if not adapter_cls:
                continue
            url = adapter_cls.health_url()
            status = HealthStatus(sid, "unchecked") if url is None else self._probe(sid, url)
            HealthCache.set(status)
            self._statuses.append(status)
        return True

    def finished(self, result: bool) -> None:
        if result:
            self.allChecked.emit(self._statuses)

    @staticmethod
    def _probe(source_id: str, url: str) -> HealthStatus:
        try:
            import httpx
        except ImportError:
            return HealthStatus(source_id, "unchecked")

        t0 = time.monotonic()
        try:
            r = httpx.head(url, timeout=HEALTH_CHECK_TIMEOUT_SECONDS, follow_redirects=True)
            if r.status_code in (405, 501):
                with httpx.stream("GET", url, timeout=HEALTH_CHECK_TIMEOUT_SECONDS) as r:
                    pass
            ms = int((time.monotonic() - t0) * 1000)
            online = r.status_code < 500
            return HealthStatus(source_id, "online" if online else "offline", time.monotonic(), ms)
        except Exception:
            return HealthStatus(source_id, "offline", time.monotonic(), None)


def check_sources(source_ids: list[str]) -> HealthCheckTask | None:
    stale = [sid for sid in source_ids if HealthCache.is_stale(sid)]
    if not stale:
        return None
    return HealthCheckTask(stale)
