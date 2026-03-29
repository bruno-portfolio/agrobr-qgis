from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock

import pandas as pd
import pytest

from agrobr_qgis.core.source_adapter import SourceAdapter, SourceCapability, SourceCategory


class _TimeoutAdapter(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "test_timeout"

    @classmethod
    def name(cls) -> str:
        return "Test"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        raise TimeoutError("timed out")


class _ConnectionErrorAdapter(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "test_conn_error"

    @classmethod
    def name(cls) -> str:
        return "Test"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        raise ConnectionError("connection refused")


class _StubQgsTask:
    CanCancel = 1

    def __init__(self, description: str = "", flags: int = 0) -> None:
        pass

    def isCanceled(self) -> bool:
        return False

    def setProgress(self, progress: float) -> None:
        pass


@pytest.fixture()
def _patch_qgis_task(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_core = MagicMock()
    mock_core.QgsTask = _StubQgsTask
    monkeypatch.setitem(sys.modules, "qgis", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.core", mock_core)
    monkeypatch.setitem(sys.modules, "qgis.PyQt", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.PyQt.QtCore", MagicMock())
    monkeypatch.delitem(sys.modules, "agrobr_qgis.core.task_runner", raising=False)


class _SlowAdapter(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "test_slow"

    @classmethod
    def name(cls) -> str:
        return "Test"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    @classmethod
    def capabilities(cls) -> SourceCapability:
        return SourceCapability.TABULAR

    def fetch(self, *, geo: bool = False, **kwargs: Any) -> pd.DataFrame:
        import time

        time.sleep(5)
        return pd.DataFrame()


@pytest.mark.edge
@pytest.mark.usefixtures("_patch_qgis_task")
class TestTimeout:
    def test_fetch_timeout_error(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _TimeoutAdapter()
        task = FetchTask(source, {})
        result = task.run()
        assert result is False
        assert task._error is not None
        assert isinstance(task._error, TimeoutError)
        assert "timed out" in str(task._error)

    def test_fetch_enforces_timeout(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _SlowAdapter()
        task = FetchTask(source, {}, timeout=1)
        result = task.run()
        assert result is False
        assert task._error is not None

    def test_fetch_connection_error(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _ConnectionErrorAdapter()
        task = FetchTask(source, {})
        result = task.run()
        assert result is False
        assert task._error is not None
        assert isinstance(task._error, ConnectionError)
        assert "connection refused" in str(task._error)
