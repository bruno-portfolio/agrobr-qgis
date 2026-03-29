from __future__ import annotations

import contextlib
from collections.abc import Callable
from functools import partial
from typing import Any

from qgis.core import QgsApplication  # type: ignore[import-untyped]

from .registry import SourceRegistry
from .task_runner import FetchTask


class FetchController:
    def __init__(
        self,
        on_result: Callable[[Any, Any], None],
        on_error: Callable[[Any, str], None],
    ) -> None:
        self._on_result = on_result
        self._on_error = on_error
        self._current_task: FetchTask | None = None
        self._connections: list[tuple[Any, Any]] = []

    def start_fetch(self, source_id: str, params: dict[str, Any], *, geo: bool, join: bool) -> bool:
        adapter_cls = SourceRegistry.get(source_id)
        if adapter_cls is None:
            return False
        self._disconnect_all()
        adapter = adapter_cls()
        task = FetchTask(adapter, params, geo=geo, join_municipal=join)
        self._current_task = task
        result_slot = partial(self._handle_result, task)
        error_slot = partial(self._handle_error, task)
        task.resultReady.connect(result_slot)
        task.errorOccurred.connect(error_slot)
        self._connections.append((task.resultReady, result_slot))
        self._connections.append((task.errorOccurred, error_slot))
        QgsApplication.taskManager().addTask(task)
        return True

    def cancel(self) -> None:
        if self._current_task:
            self._current_task.cancel()
            self._current_task = None

    @property
    def is_active(self) -> bool:
        return self._current_task is not None

    def _handle_result(self, task: FetchTask, result: Any) -> None:
        if task is not self._current_task:
            return
        self._current_task = None
        self._on_result(task, result)

    def _handle_error(self, task: FetchTask, msg: str) -> None:
        if task is not self._current_task:
            return
        self._current_task = None
        self._on_error(task, msg)

    def _disconnect_all(self) -> None:
        for signal, slot in self._connections:
            with contextlib.suppress(TypeError, RuntimeError):
                signal.disconnect(slot)
        self._connections.clear()
