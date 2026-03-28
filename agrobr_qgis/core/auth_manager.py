from __future__ import annotations


class AuthManager:
    PREFIX = "agrobr_"
    METHOD = "Basic"

    @classmethod
    def get_token(cls, source_id: str) -> str | None:
        from qgis.core import QgsApplication, QgsAuthMethodConfig  # type: ignore[import-untyped]

        auth_mgr = QgsApplication.authManager()
        cfg = QgsAuthMethodConfig()
        cfg_id = f"{cls.PREFIX}{source_id}"
        if auth_mgr.loadAuthenticationConfig(cfg_id, cfg, True):
            token: str = cfg.config("token", "")
            return token or None
        return None

    @classmethod
    def set_token(cls, source_id: str, token: str) -> bool:
        from qgis.core import QgsApplication, QgsAuthMethodConfig  # type: ignore[import-untyped]

        auth_mgr = QgsApplication.authManager()
        cfg_id = f"{cls.PREFIX}{source_id}"
        cfg = QgsAuthMethodConfig()
        cfg.setId(cfg_id)
        cfg.setName(f"AgroBR - {source_id}")
        cfg.setMethod(cls.METHOD)
        cfg.setConfig("token", token)
        if auth_mgr.existsAuthenticationConfig(cfg_id):
            result: bool = auth_mgr.updateAuthenticationConfig(cfg)
            return result
        result = auth_mgr.storeAuthenticationConfig(cfg)
        return result

    @classmethod
    def remove_token(cls, source_id: str) -> bool:
        from qgis.core import QgsApplication  # type: ignore[import-untyped]

        result: bool = QgsApplication.authManager().removeAuthenticationConfig(
            f"{cls.PREFIX}{source_id}"
        )
        return result

    @classmethod
    def has_token(cls, source_id: str) -> bool:
        return cls.get_token(source_id) is not None
