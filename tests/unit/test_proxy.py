from __future__ import annotations

import os
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

    mock_settings_instance.value = _value

    mock_core = MagicMock()
    mock_core.QgsSettings.return_value = mock_settings_instance
    monkeypatch.setitem(sys.modules, "qgis", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.core", mock_core)

    monkeypatch.delenv("HTTP_PROXY", raising=False)
    monkeypatch.delenv("HTTPS_PROXY", raising=False)

    def _set(**kwargs: object) -> None:
        mapping = {
            "enabled": "proxy/proxyEnabled",
            "host": "proxy/proxyHost",
            "port": "proxy/proxyPort",
            "user": "proxy/proxyUser",
            "password": "proxy/proxyPassword",
        }
        for k, v in kwargs.items():
            settings_data[mapping[k]] = v

    return _set


class TestPropagateProxy:
    def test_disabled_no_env(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(enabled=False, host="proxy.corp", port="8080")
        from agrobr_qgis.core.proxy import propagate_proxy

        propagate_proxy()
        assert "HTTP_PROXY" not in os.environ
        assert "HTTPS_PROXY" not in os.environ

    def test_no_host_no_env(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(enabled=True, host="", port="8080")
        from agrobr_qgis.core.proxy import propagate_proxy

        propagate_proxy()
        assert "HTTP_PROXY" not in os.environ

    def test_host_port(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(enabled=True, host="proxy.corp", port="8080", user="", password="")
        from agrobr_qgis.core.proxy import propagate_proxy

        propagate_proxy()
        assert os.environ["HTTP_PROXY"] == "http://proxy.corp:8080"
        assert os.environ["HTTPS_PROXY"] == "http://proxy.corp:8080"

    def test_user_password(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(
            enabled=True, host="proxy.corp", port="8080", user="admin", password="secret"
        )
        from agrobr_qgis.core.proxy import propagate_proxy

        propagate_proxy()
        assert os.environ["HTTP_PROXY"] == "http://admin:secret@proxy.corp:8080"

    def test_special_chars_password(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(
            enabled=True, host="proxy.corp", port="8080", user="admin", password="p@ss:w0rd/&"
        )
        from agrobr_qgis.core.proxy import propagate_proxy

        propagate_proxy()
        url = os.environ["HTTP_PROXY"]
        assert "p%40ss%3Aw0rd%2F%26" in url
        assert "admin" in url

    def test_user_without_password(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(enabled=True, host="proxy.corp", port="8080", user="admin", password="")
        from agrobr_qgis.core.proxy import propagate_proxy

        propagate_proxy()
        assert os.environ["HTTP_PROXY"] == "http://admin@proxy.corp:8080"

    def test_port_zero_omitted(self, mock_qgis_settings: Callable[..., None]) -> None:
        mock_qgis_settings(enabled=True, host="proxy.corp", port="0", user="", password="")
        from agrobr_qgis.core.proxy import propagate_proxy

        propagate_proxy()
        assert os.environ["HTTP_PROXY"] == "http://proxy.corp"

    def test_does_not_overwrite_existing_env(
        self, mock_qgis_settings: Callable[..., None], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("HTTP_PROXY", "http://existing:9999")
        monkeypatch.setenv("HTTPS_PROXY", "http://existing:9999")
        mock_qgis_settings(enabled=True, host="proxy.corp", port="8080", user="", password="")
        from agrobr_qgis.core.proxy import propagate_proxy

        propagate_proxy()
        assert os.environ["HTTP_PROXY"] == "http://existing:9999"
        assert os.environ["HTTPS_PROXY"] == "http://existing:9999"
