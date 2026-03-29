from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from agrobr_qgis.core.spatial_join import SpatialJoin


class _StubQgsTask:
    CanCancel = 1

    def __init__(self, description: str = "", flags: int = 0) -> None:
        pass

    def isCanceled(self) -> bool:
        return False

    def setProgress(self, progress: float) -> None:
        pass


class _FailingSource:
    @classmethod
    def name(cls) -> str:
        return "failing_source"

    @classmethod
    def capabilities(cls) -> int:
        return 0

    @classmethod
    def join_column(cls) -> str | None:
        return None

    def fetch(self, **kwargs: Any) -> pd.DataFrame:
        raise ConnectionError("Sem conexão com a internet")


@pytest.fixture()
def _patch_qgis_task(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_core = MagicMock()
    mock_core.QgsTask = _StubQgsTask
    monkeypatch.setitem(sys.modules, "qgis", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.core", mock_core)
    monkeypatch.setitem(sys.modules, "qgis.PyQt", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.PyQt.QtCore", MagicMock())


@pytest.mark.edge
class TestOfflineDegradation:
    @pytest.mark.usefixtures("_patch_qgis_task")
    def test_fetch_connection_error_message(self) -> None:
        from agrobr_qgis.core.task_runner import FetchTask

        source = _FailingSource()
        task = FetchTask(source=source, params={})  # type: ignore[arg-type]

        result = task.run()

        assert result is False
        assert task._error is not None
        assert isinstance(task._error, ConnectionError)

    def test_mesh_download_connection_error(self) -> None:
        SpatialJoin._mesh_cache.clear()

        with (
            patch.object(
                SpatialJoin,
                "_download_and_verify",
                side_effect=ConnectionError("offline"),
            ),
            pytest.raises(ConnectionError, match="offline"),
        ):
            SpatialJoin._get_mesh("http://fake.url/mesh.gpkg", "fakehash")

    def test_mesh_download_url_error(self) -> None:
        SpatialJoin._mesh_cache.clear()

        with (
            patch.object(
                SpatialJoin,
                "_download_and_verify",
                side_effect=OSError("Name or service not known"),
            ),
            pytest.raises(OSError, match="Name or service not known"),
        ):
            SpatialJoin._get_mesh("http://unreachable.host/mesh.gpkg", "fakehash")

    def test_mesh_cache_not_populated_on_failure(self) -> None:
        SpatialJoin._mesh_cache.clear()

        with (
            patch.object(
                SpatialJoin,
                "_download_and_verify",
                side_effect=ConnectionError("offline"),
            ),
            pytest.raises(ConnectionError),
        ):
            SpatialJoin._get_mesh("http://fake.url/mesh_test.gpkg", "fakehash")

        assert "mesh_test.gpkg" not in SpatialJoin._mesh_cache
