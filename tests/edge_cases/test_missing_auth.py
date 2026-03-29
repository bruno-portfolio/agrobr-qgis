from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest


@pytest.mark.edge
class TestMissingAuth:
    def test_get_token_unconfigured(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_auth_mgr = MagicMock()
        mock_auth_mgr.loadAuthenticationConfig = MagicMock(return_value=False)

        mock_core = MagicMock()
        mock_core.QgsApplication.authManager.return_value = mock_auth_mgr

        monkeypatch.setitem(sys.modules, "qgis", MagicMock())
        monkeypatch.setitem(sys.modules, "qgis.core", mock_core)

        from agrobr_qgis.core.auth_manager import AuthManager

        result = AuthManager.get_token("nonexistent_source")
        assert result is None

    def test_has_token_false_when_unconfigured(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_auth_mgr = MagicMock()
        mock_auth_mgr.loadAuthenticationConfig = MagicMock(return_value=False)

        mock_core = MagicMock()
        mock_core.QgsApplication.authManager.return_value = mock_auth_mgr

        monkeypatch.setitem(sys.modules, "qgis", MagicMock())
        monkeypatch.setitem(sys.modules, "qgis.core", mock_core)

        from agrobr_qgis.core.auth_manager import AuthManager

        assert AuthManager.has_token("nonexistent_source") is False
