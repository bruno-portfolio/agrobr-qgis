from __future__ import annotations

import dataclasses

from agrobr_qgis.gui.state import STATE_CONFIG, DockState, ParamCache, WidgetVisibility


class TestDockState:
    def test_all_states_in_config(self) -> None:
        for state in DockState:
            assert state in STATE_CONFIG

    def test_idle_shows_tree_and_search(self) -> None:
        v = STATE_CONFIG[DockState.IDLE]
        assert v.search_bar is True
        assert v.source_tree is True
        assert v.param_panel is False
        assert v.result_panel is False
        assert v.error_label is False
        assert v.fetch_button is False

    def test_selected_shows_params_and_fetch(self) -> None:
        v = STATE_CONFIG[DockState.SELECTED]
        assert v.param_panel is True
        assert v.fetch_button is True
        assert v.progress_bar is False

    def test_loading_shows_progress_hides_fetch(self) -> None:
        v = STATE_CONFIG[DockState.LOADING]
        assert v.progress_bar is True
        assert v.fetch_button is False
        assert v.param_panel is False

    def test_result_shows_add_and_zoom(self) -> None:
        v = STATE_CONFIG[DockState.RESULT]
        assert v.result_panel is True
        assert v.add_button is True
        assert v.zoom_button is True
        assert v.error_label is False

    def test_error_shows_label_and_keeps_tree(self) -> None:
        v = STATE_CONFIG[DockState.ERROR]
        assert v.error_label is True
        assert v.search_bar is True
        assert v.source_tree is True
        assert v.param_panel is False
        assert v.result_panel is False


class TestParamCache:
    def test_save_and_load(self) -> None:
        cache = ParamCache()
        cache.save("queimadas", {"data": "2026-01-01"})
        assert cache.load("queimadas") == {"data": "2026-01-01"}

    def test_load_missing_returns_empty_dict(self) -> None:
        cache = ParamCache()
        assert cache.load("nonexistent") == {}

    def test_clear_specific(self) -> None:
        cache = ParamCache()
        cache.save("a", {"x": 1})
        cache.save("b", {"y": 2})
        cache.clear("a")
        assert cache.load("a") == {}
        assert cache.load("b") == {"y": 2}

    def test_clear_all(self) -> None:
        cache = ParamCache()
        cache.save("a", {"x": 1})
        cache.save("b", {"y": 2})
        cache.clear()
        assert cache.load("a") == {}
        assert cache.load("b") == {}

    def test_overwrite(self) -> None:
        cache = ParamCache()
        cache.save("src", {"v": 1})
        cache.save("src", {"v": 2})
        assert cache.load("src") == {"v": 2}


class TestWidgetVisibility:
    def test_is_frozen_dataclass(self) -> None:
        assert dataclasses.is_dataclass(WidgetVisibility)
        v = WidgetVisibility(search_bar=True)
        assert v.search_bar is True
