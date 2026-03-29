from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pandas as pd

_mock_core = MagicMock()


class _StubQgsTask:
    CanCancel = 1

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def isCanceled(self) -> bool:  # noqa: N802
        return False

    def setProgress(self, p: float) -> None:  # noqa: N802
        pass

    def cancel(self) -> None:
        pass


_mock_core.QgsTask = _StubQgsTask
_mock_core.QgsApplication.taskManager.return_value = MagicMock()
sys.modules.setdefault("qgis", MagicMock())
sys.modules.setdefault("qgis.core", _mock_core)
sys.modules.setdefault("qgis.PyQt", MagicMock())
sys.modules.setdefault("qgis.PyQt.QtCore", MagicMock())

from agrobr_qgis.core.fetch_controller import FetchController  # noqa: E402
from agrobr_qgis.core.registry import SourceRegistry  # noqa: E402
from agrobr_qgis.core.source_adapter import (  # noqa: E402
    SourceAdapter,
    SourceCategory,
)


class _DummySource(SourceAdapter):
    @classmethod
    def id(cls) -> str:
        return "dummy"

    @classmethod
    def name(cls) -> str:
        return "Dummy"

    @classmethod
    def category(cls) -> SourceCategory:
        return SourceCategory.AMBIENTAL

    def fetch(self, *, geo: bool = False, **kwargs: object) -> pd.DataFrame:
        return pd.DataFrame({"v": [1]})


class TestFetchController:
    def setup_method(self) -> None:
        SourceRegistry.register(_DummySource)

    def teardown_method(self) -> None:
        SourceRegistry.clear()

    def test_start_fetch_unknown_source_returns_false(self) -> None:
        ctrl = FetchController(on_result=MagicMock(), on_error=MagicMock())
        assert ctrl.start_fetch("nonexistent", {}, geo=False, join=False) is False

    def test_start_fetch_known_source_returns_true(self) -> None:
        ctrl = FetchController(on_result=MagicMock(), on_error=MagicMock())
        with patch("agrobr_qgis.core.fetch_controller.QgsApplication") as mock_app:
            mock_app.taskManager.return_value = MagicMock()
            result = ctrl.start_fetch("dummy", {}, geo=False, join=False)
        assert result is True
        assert ctrl.is_active is True

    def test_cancel_clears_task(self) -> None:
        ctrl = FetchController(on_result=MagicMock(), on_error=MagicMock())
        with patch("agrobr_qgis.core.fetch_controller.QgsApplication") as mock_app:
            mock_app.taskManager.return_value = MagicMock()
            ctrl.start_fetch("dummy", {}, geo=False, join=False)
        ctrl.cancel()
        assert ctrl.is_active is False

    def test_connections_tracked(self) -> None:
        ctrl = FetchController(on_result=MagicMock(), on_error=MagicMock())
        with patch("agrobr_qgis.core.fetch_controller.QgsApplication") as mock_app:
            mock_app.taskManager.return_value = MagicMock()
            ctrl.start_fetch("dummy", {}, geo=False, join=False)
        assert len(ctrl._connections) == 2
