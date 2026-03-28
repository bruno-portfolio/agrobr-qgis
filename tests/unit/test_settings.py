from __future__ import annotations

import json
import sys
from collections.abc import Callable
from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def mock_qgis_settings(monkeypatch: pytest.MonkeyPatch) -> Callable[..., None]:
    settings_data: dict[str, object] = {}
    mock_settings_instance = MagicMock()

    def _value(key: str, default: object = None, type: type | None = None) -> object:  # noqa: ARG001
        return settings_data.get(key, default)

    def _set_value(key: str, value: object) -> None:
        settings_data[key] = value

    mock_settings_instance.value = _value
    mock_settings_instance.setValue = _set_value

    mock_core = MagicMock()
    mock_core.QgsSettings.return_value = mock_settings_instance
    monkeypatch.setitem(sys.modules, "qgis", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.core", mock_core)

    def _set(**kwargs: object) -> None:
        prefix = "agrobr/"
        for k, v in kwargs.items():
            settings_data[f"{prefix}{k}"] = v

    return _set


class TestCacheEnabled:
    def test_default_true(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings()
        from agrobr_qgis.core.settings_manager import SettingsManager

        assert SettingsManager.is_cache_enabled() is True

    def test_set_and_get(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings()
        from agrobr_qgis.core.settings_manager import SettingsManager

        SettingsManager.set_cache_enabled(False)
        assert SettingsManager.is_cache_enabled() is False

    def test_explicit_true(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(cache_enabled=True)
        from agrobr_qgis.core.settings_manager import SettingsManager

        assert SettingsManager.is_cache_enabled() is True


class TestDefaultCrs:
    def test_default_epsg4674(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings()
        from agrobr_qgis.core.settings_manager import SettingsManager

        assert SettingsManager.get_default_crs() == "EPSG:4674"

    def test_set_and_get(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings()
        from agrobr_qgis.core.settings_manager import SettingsManager

        SettingsManager.set_default_crs("EPSG:4326")
        assert SettingsManager.get_default_crs() == "EPSG:4326"


class TestRecentSources:
    def test_default_empty(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings()
        from agrobr_qgis.core.settings_manager import SettingsManager

        assert SettingsManager.get_recent_sources() == []

    def test_add_source(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings()
        from agrobr_qgis.core.settings_manager import SettingsManager

        SettingsManager.add_recent_source("queimadas")
        assert SettingsManager.get_recent_sources() == ["queimadas"]

    def test_dedup_moves_to_front(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(recent_sources=json.dumps(["ibge_pam", "queimadas"]))
        from agrobr_qgis.core.settings_manager import SettingsManager

        SettingsManager.add_recent_source("queimadas")
        result = SettingsManager.get_recent_sources()
        assert result[0] == "queimadas"
        assert result.count("queimadas") == 1

    def test_max_10(self, mock_qgis_settings: Callable[..., None]) -> None:
        existing = json.dumps([f"source_{i}" for i in range(10)])
        mock_qgis_settings(recent_sources=existing)
        from agrobr_qgis.core.settings_manager import SettingsManager

        SettingsManager.add_recent_source("new_source")
        result = SettingsManager.get_recent_sources()
        assert len(result) == 10
        assert result[0] == "new_source"
