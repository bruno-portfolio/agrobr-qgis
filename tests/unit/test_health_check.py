from __future__ import annotations

import sys
import time
from unittest.mock import MagicMock, patch

_mock_core = MagicMock()


class _StubQgsTask:
    CanCancel = 1

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def isCanceled(self) -> bool:  # noqa: N802
        return False

    def setProgress(self, p: float) -> None:  # noqa: N802
        pass


_mock_core.QgsTask = _StubQgsTask
sys.modules.setdefault("qgis", MagicMock())
sys.modules["qgis.core"] = _mock_core
sys.modules.setdefault("qgis.PyQt", MagicMock())
sys.modules.setdefault("qgis.PyQt.QtCore", MagicMock())

from agrobr_qgis.core.health_check import HealthCache, HealthCheckTask, HealthStatus  # noqa: E402


class TestHealthCache:
    def setup_method(self) -> None:
        HealthCache.clear()

    def test_get_uncached_returns_unchecked(self) -> None:
        result = HealthCache.get("some_source")
        assert result.status == "unchecked"
        assert result.checked_at is None

    def test_set_and_get_within_ttl(self) -> None:
        status = HealthStatus("src", "online", time.monotonic(), 42)
        HealthCache.set(status)
        result = HealthCache.get("src")
        assert result.status == "online"
        assert result.response_ms == 42

    def test_stale_after_ttl(self) -> None:
        old_time = time.monotonic() - HealthCache.TTL_SECONDS - 1
        status = HealthStatus("src", "online", old_time, 10)
        HealthCache.set(status)
        assert HealthCache.is_stale("src") is True
        result = HealthCache.get("src")
        assert result.status == "unchecked"

    def test_not_stale_within_ttl(self) -> None:
        status = HealthStatus("src", "online", time.monotonic(), 10)
        HealthCache.set(status)
        assert HealthCache.is_stale("src") is False

    def test_is_stale_when_never_checked(self) -> None:
        assert HealthCache.is_stale("never_seen") is True

    def test_clear_removes_all(self) -> None:
        HealthCache.set(HealthStatus("a", "online", time.monotonic()))
        HealthCache.set(HealthStatus("b", "offline", time.monotonic()))
        HealthCache.clear()
        assert HealthCache.get("a").status == "unchecked"
        assert HealthCache.get("b").status == "unchecked"


class TestProbe:
    def test_probe_head_success(self) -> None:
        mock_httpx = MagicMock()
        mock_httpx.head.return_value = MagicMock(status_code=200)
        with patch.dict("sys.modules", {"httpx": mock_httpx}):
            result = HealthCheckTask._probe("test", "http://example.com")
        assert result.status == "online"
        assert result.response_ms is not None

    def test_probe_head_405_fallback_get(self) -> None:
        mock_httpx = MagicMock()
        mock_httpx.head.return_value = MagicMock(status_code=405)
        stream_response = MagicMock(status_code=200)
        stream_ctx = MagicMock()
        stream_ctx.__enter__ = MagicMock(return_value=stream_response)
        stream_ctx.__exit__ = MagicMock(return_value=False)
        mock_httpx.stream.return_value = stream_ctx
        with patch.dict("sys.modules", {"httpx": mock_httpx}):
            result = HealthCheckTask._probe("test", "http://example.com")
        assert result.status == "online"

    def test_probe_timeout_returns_offline(self) -> None:
        mock_httpx = MagicMock()
        mock_httpx.head.side_effect = Exception("timeout")
        with patch.dict("sys.modules", {"httpx": mock_httpx}):
            result = HealthCheckTask._probe("test", "http://example.com")
        assert result.status == "offline"

    def test_no_health_url_returns_unchecked(self) -> None:
        status = HealthStatus("no_url", "unchecked")
        assert status.status == "unchecked"

    def test_httpx_import_error_returns_unchecked(self) -> None:
        with patch.dict("sys.modules", {"httpx": None}):
            result = HealthCheckTask._probe("test", "http://example.com")
        assert result.status == "unchecked"
