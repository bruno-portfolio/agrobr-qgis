from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class DockState(StrEnum):
    IDLE = "idle"
    SELECTED = "selected"
    LOADING = "loading"
    RESULT = "result"
    ERROR = "error"


@dataclass(frozen=True)
class WidgetVisibility:
    search_bar: bool = False
    source_tree: bool = False
    param_panel: bool = False
    fetch_button: bool = False
    progress_bar: bool = False
    result_panel: bool = False
    error_label: bool = False
    add_button: bool = False
    zoom_button: bool = False


STATE_CONFIG: dict[DockState, WidgetVisibility] = {
    DockState.IDLE: WidgetVisibility(
        search_bar=True,
        source_tree=True,
    ),
    DockState.SELECTED: WidgetVisibility(
        search_bar=True,
        source_tree=True,
        param_panel=True,
        fetch_button=True,
    ),
    DockState.LOADING: WidgetVisibility(
        search_bar=True,
        source_tree=True,
        progress_bar=True,
    ),
    DockState.RESULT: WidgetVisibility(
        search_bar=True,
        source_tree=True,
        result_panel=True,
        add_button=True,
        zoom_button=True,
    ),
    DockState.ERROR: WidgetVisibility(
        search_bar=True,
        source_tree=True,
        error_label=True,
    ),
}


class ParamCache:
    def __init__(self) -> None:
        self._cache: dict[str, dict[str, Any]] = {}

    def save(self, source_id: str, params: dict[str, Any]) -> None:
        self._cache[source_id] = dict(params)

    def load(self, source_id: str) -> dict[str, Any]:
        return dict(self._cache.get(source_id, {}))

    def clear(self, source_id: str | None = None) -> None:
        if source_id is None:
            self._cache.clear()
        else:
            self._cache.pop(source_id, None)
