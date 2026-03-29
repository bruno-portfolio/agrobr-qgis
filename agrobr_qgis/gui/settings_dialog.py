from __future__ import annotations

from typing import Any

from agrobr_qgis.core.source_adapter import SourceCapability


class SettingsDialog:  # pragma: no cover
    def __init__(self, parent: Any = None) -> None:
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QCheckBox,
            QDialog,
            QDialogButtonBox,
            QFormLayout,
            QLabel,
            QLineEdit,
            QTabWidget,
            QVBoxLayout,
            QWidget,
        )

        self._dialog = QDialog(parent)
        self._dialog.setWindowTitle(self._dialog.tr("agrobr — Configuracoes"))
        self._dialog.setMinimumWidth(400)

        layout = QVBoxLayout(self._dialog)
        tabs = QTabWidget()

        general_tab = QWidget()
        general_form = QFormLayout(general_tab)

        from agrobr_qgis.core.settings_manager import SettingsManager

        self._cache_check = QCheckBox()
        self._cache_check.setChecked(SettingsManager.is_cache_enabled())
        general_form.addRow(self._dialog.tr("Cache habilitado:"), self._cache_check)

        self._crs_edit = QLineEdit(SettingsManager.get_default_crs())
        general_form.addRow(self._dialog.tr("CRS padrao:"), self._crs_edit)

        tabs.addTab(general_tab, self._dialog.tr("Geral"))

        tokens_tab = QWidget()
        tokens_layout = QVBoxLayout(tokens_tab)
        self._token_widgets: dict[str, QLineEdit] = {}

        from agrobr_qgis.core.auth_manager import AuthManager
        from agrobr_qgis.core.registry import SourceRegistry

        auth_sources = SourceRegistry.list_by_capability(SourceCapability.AUTH)

        if not auth_sources:
            tokens_layout.addWidget(QLabel(self._dialog.tr("Nenhuma fonte requer autenticacao")))
        else:
            from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
                QHBoxLayout,
                QPushButton,
            )

            for src in auth_sources:
                row = QHBoxLayout()
                row.addWidget(QLabel(src.name()))
                token_edit = QLineEdit()
                token_edit.setEchoMode(QLineEdit.EchoMode.Password)
                existing = AuthManager.get_token(src.id())
                if existing:
                    token_edit.setText(existing)
                self._token_widgets[src.id()] = token_edit
                row.addWidget(token_edit)

                save_btn = QPushButton(self._dialog.tr("Salvar"))
                save_btn.clicked.connect(lambda _checked, sid=src.id(): self._save_token(sid))
                row.addWidget(save_btn)

                remove_btn = QPushButton(self._dialog.tr("Remover"))
                remove_btn.clicked.connect(lambda _checked, sid=src.id(): self._remove_token(sid))
                row.addWidget(remove_btn)
                tokens_layout.addLayout(row)

        tokens_layout.addStretch()
        tabs.addTab(tokens_tab, self._dialog.tr("Tokens"))

        layout.addWidget(tabs)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._accept)
        buttons.rejected.connect(self._dialog.reject)
        layout.addWidget(buttons)

    def _save_token(self, source_id: str) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        token_edit = self._token_widgets.get(source_id)
        if token_edit and token_edit.text().strip():
            AuthManager.set_token(source_id, token_edit.text().strip())

    def _remove_token(self, source_id: str) -> None:
        from agrobr_qgis.core.auth_manager import AuthManager

        AuthManager.remove_token(source_id)
        token_edit = self._token_widgets.get(source_id)
        if token_edit:
            token_edit.clear()

    def _accept(self) -> None:
        from agrobr_qgis.core.settings_manager import SettingsManager

        SettingsManager.set_cache_enabled(self._cache_check.isChecked())
        crs = self._crs_edit.text().strip()
        if crs:
            SettingsManager.set_default_crs(crs)
        self._dialog.accept()

    def exec(self) -> int:
        result: int = self._dialog.exec()
        return result
