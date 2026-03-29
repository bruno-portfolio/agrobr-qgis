from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock

import pandas as pd
import pytest


class _StubQgsTask:
    CanCancel = 1

    def __init__(self, description: str = "", flags: int = 0) -> None:
        pass

    def isCanceled(self) -> bool:
        return False

    def setProgress(self, progress: float) -> None:
        pass


class _CancelCounter:
    def __init__(self, cancel_at: int) -> None:
        self._call_count = 0
        self._cancel_at = cancel_at

    def __call__(self) -> bool:
        self._call_count += 1
        return self._call_count >= self._cancel_at


class _TrackingSource:
    def __init__(self) -> None:
        self.fetch_called = False

    @classmethod
    def name(cls) -> str:
        return "test_source"

    @classmethod
    def capabilities(cls) -> int:
        return 0

    @classmethod
    def join_column(cls) -> str | None:
        return None

    def fetch(self, **kwargs: Any) -> pd.DataFrame:
        self.fetch_called = True
        return pd.DataFrame({"col": [1, 2, 3]})


@pytest.fixture()
def _patch_qgis_task(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_core = MagicMock()
    mock_core.QgsTask = _StubQgsTask
    monkeypatch.setitem(sys.modules, "qgis", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.core", mock_core)
    monkeypatch.setitem(sys.modules, "qgis.PyQt", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.PyQt.QtCore", MagicMock())


@pytest.mark.edge
@pytest.mark.usefixtures("_patch_qgis_task")
class TestCancelledTask:
    def test_cancel_before_fetch(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _TrackingSource()
        task = FetchTask(source=source, params={})  # type: ignore[arg-type]
        task.isCanceled = _CancelCounter(cancel_at=1)

        result = task.run()

        assert result is False
        assert not source.fetch_called

    def test_cancel_after_fetch(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _TrackingSource()
        task = FetchTask(source=source, params={})  # type: ignore[arg-type]
        task.isCanceled = _CancelCounter(cancel_at=2)

        result = task.run()

        assert result is False
        assert source.fetch_called
        assert task._contract_result is None

    def test_cancel_after_validate(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _TrackingSource()
        task = FetchTask(source=source, params={})  # type: ignore[arg-type]
        task.isCanceled = _CancelCounter(cancel_at=3)

        result = task.run()

        assert result is False
        assert source.fetch_called
        assert task._contract_result is not None
