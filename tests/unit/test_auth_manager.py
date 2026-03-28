from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def mock_qgis_auth(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    store: dict[str, str] = {}

    mock_cfg_class = MagicMock()

    def _make_cfg() -> MagicMock:
        cfg = MagicMock()
        cfg_data: dict[str, str] = {}
        cfg.setId = MagicMock()
        cfg.setName = MagicMock()
        cfg.setMethod = MagicMock()
        cfg.setConfig = MagicMock(side_effect=lambda k, v: cfg_data.update({k: v}))
        cfg.config = MagicMock(side_effect=lambda k, d="": cfg_data.get(k, d))
        cfg._data = cfg_data
        return cfg

    mock_cfg_class.side_effect = lambda: _make_cfg()

    mock_auth_mgr = MagicMock()

    def _load(cfg_id: str, cfg: MagicMock, full: bool = True) -> bool:  # noqa: ARG001
        if cfg_id in store:
            cfg._data["token"] = store[cfg_id]
            cfg.config = MagicMock(side_effect=lambda k, d="": cfg._data.get(k, d))
            return True
        return False

    def _store(cfg: MagicMock) -> bool:
        cfg_id = cfg.setId.call_args[0][0]
        token = cfg._data.get("token", "")
        store[cfg_id] = token
        return True

    def _update(cfg: MagicMock) -> bool:
        return _store(cfg)

    def _exists(cfg_id: str) -> bool:
        return cfg_id in store

    def _remove(cfg_id: str) -> bool:
        return store.pop(cfg_id, None) is not None

    mock_auth_mgr.loadAuthenticationConfig = MagicMock(side_effect=_load)
    mock_auth_mgr.storeAuthenticationConfig = MagicMock(side_effect=_store)
    mock_auth_mgr.updateAuthenticationConfig = MagicMock(side_effect=_update)
    mock_auth_mgr.existsAuthenticationConfig = MagicMock(side_effect=_exists)
    mock_auth_mgr.removeAuthenticationConfig = MagicMock(side_effect=_remove)

    mock_core = MagicMock()
    mock_core.QgsApplication.authManager.return_value = mock_auth_mgr
    mock_core.QgsAuthMethodConfig = mock_cfg_class
    monkeypatch.setitem(sys.modules, "qgis", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.core", mock_core)

    return store


class TestAuthManager:
    def test_get_token_not_found(self, mock_qgis_auth: dict[str, str]) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        assert AuthManager.get_token("nonexistent") is None

    def test_set_and_get_token(self, mock_qgis_auth: dict[str, str]) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        assert AuthManager.set_token("usda", "my-api-key") is True
        assert AuthManager.get_token("usda") == "my-api-key"

    def test_has_token_false(self, mock_qgis_auth: dict[str, str]) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        assert AuthManager.has_token("usda") is False

    def test_has_token_true(self, mock_qgis_auth: dict[str, str]) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        AuthManager.set_token("usda", "key")
        assert AuthManager.has_token("usda") is True

    def test_remove_token(self, mock_qgis_auth: dict[str, str]) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        AuthManager.set_token("usda", "key")
        assert AuthManager.remove_token("usda") is True
        assert AuthManager.has_token("usda") is False

    def test_remove_nonexistent(self, mock_qgis_auth: dict[str, str]) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        assert AuthManager.remove_token("nonexistent") is False

    def test_update_existing_token(self, mock_qgis_auth: dict[str, str]) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        AuthManager.set_token("usda", "old-key")
        AuthManager.set_token("usda", "new-key")
        assert AuthManager.get_token("usda") == "new-key"
