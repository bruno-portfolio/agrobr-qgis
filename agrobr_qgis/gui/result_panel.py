from __future__ import annotations

from typing import Any

from agrobr_qgis.core.data_contract import ContractResult


class ResultPanel:  # pragma: no cover
    def __init__(self, parent: Any = None) -> None:
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QPushButton,
            QVBoxLayout,
            QWidget,
        )

        self._widget = QWidget(parent)
        self._layout = QVBoxLayout(self._widget)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._add_btn = QPushButton(self._widget.tr("Adicionar ao Mapa"))
        self._zoom_btn = QPushButton(self._widget.tr("Zoom na Camada"))
        self._again_btn = QPushButton(self._widget.tr("Buscar Novamente"))
        self._open_table_btn = QPushButton(self._widget.tr("Abrir Tabela"))
        self._save_as_btn = QPushButton(self._widget.tr("Salvar como..."))
        self._view_origin_btn = QPushButton(self._widget.tr("Ver Origem"))
        self._zoom_btn.setEnabled(False)
        self._open_table_btn.setEnabled(False)
        self._save_as_btn.setEnabled(False)
        self._view_origin_btn.setEnabled(False)

    def show_result(self, result: ContractResult) -> None:
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QFormLayout,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QVBoxLayout,
            QWidget,
        )

        self._clear_content()

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)

        if result.row_count == 0:
            layout.addWidget(QLabel(self._widget.tr("Nenhum registro encontrado")))
            self._add_btn.setEnabled(False)
            self._zoom_btn.setEnabled(False)
        else:
            group = QGroupBox(self._widget.tr("Resultado"))
            form = QFormLayout(group)
            form.addRow(self._widget.tr("Registros:"), QLabel(str(result.row_count)))
            form.addRow(self._widget.tr("Colunas:"), QLabel(str(result.col_count)))
            form.addRow(
                self._widget.tr("Geometria:"),
                QLabel(result.geometry_type or self._widget.tr("Nenhuma")),
            )
            form.addRow(self._widget.tr("CRS:"), QLabel(result.crs or "N/A"))
            if result.estimated_vertices > 0:
                form.addRow(
                    self._widget.tr("Vertices estimados:"),
                    QLabel(f"~{result.estimated_vertices:,}"),
                )
            layout.addWidget(group)
            self._add_btn.setEnabled(True)
            self._zoom_btn.setEnabled(False)

        if result.warnings:
            warn_text = "\n".join(f"  - {w}" for w in result.warnings)
            warn_label = QLabel(f"Avisos:\n{warn_text}")
            warn_label.setWordWrap(True)
            warn_label.setStyleSheet("color: #cc6600;")
            layout.addWidget(warn_label)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self._add_btn)
        btn_layout.addWidget(self._zoom_btn)
        btn_layout.addWidget(self._again_btn)
        layout.addLayout(btn_layout)

        btn_layout2 = QHBoxLayout()
        btn_layout2.addWidget(self._open_table_btn)
        btn_layout2.addWidget(self._save_as_btn)
        btn_layout2.addWidget(self._view_origin_btn)
        layout.addLayout(btn_layout2)

        self._layout.addWidget(container)

    def show_template_result(self, result: Any) -> None:
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QVBoxLayout,
            QWidget,
        )

        self._clear_content()
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)

        ok_count = len(result.succeeded)
        fail_count = len(result.failed)
        header = QLabel(f"{result.template_name} — {ok_count}/{ok_count + fail_count} fontes OK")
        header.setStyleSheet("font-weight: bold;")
        layout.addWidget(header)

        for outcome in result.outcomes:
            group = QGroupBox()
            gl = QVBoxLayout(group)
            if outcome.status == "ok":
                gl.addWidget(
                    QLabel(f"\u2713 {outcome.source_name} — {outcome.result.row_count} registros")
                )
            else:
                lbl = QLabel(
                    f"\u2717 {outcome.source_name} — {outcome.error_message or outcome.status}"
                )
                lbl.setStyleSheet("color: #cc0000;")
                gl.addWidget(lbl)
            layout.addWidget(group)

        btn_layout = QHBoxLayout()
        add_all = QPushButton(self._widget.tr("Adicionar Todos OK"))
        add_all.setEnabled(ok_count > 0)
        btn_layout.addWidget(add_all)
        btn_layout.addWidget(self._again_btn)
        layout.addLayout(btn_layout)

        self._add_all_btn = add_all
        self._layout.addWidget(container)

    @property
    def add_all_button(self) -> Any:
        return getattr(self, "_add_all_btn", None)

    def _clear_content(self) -> None:
        old = self._layout.takeAt(0)
        while old:
            if old.widget():
                old.widget().deleteLater()
            old = self._layout.takeAt(0)

    def enable_zoom(self) -> None:
        self._zoom_btn.setEnabled(True)
        self._open_table_btn.setEnabled(True)
        self._save_as_btn.setEnabled(True)

    def enable_origin(self) -> None:
        self._view_origin_btn.setEnabled(True)

    def clear(self) -> None:
        self._clear_content()

    @property
    def add_button(self) -> Any:
        return self._add_btn

    @property
    def zoom_button(self) -> Any:
        return self._zoom_btn

    @property
    def fetch_again_button(self) -> Any:
        return self._again_btn

    @property
    def open_table_button(self) -> Any:
        return self._open_table_btn

    @property
    def save_as_button(self) -> Any:
        return self._save_as_btn

    @property
    def view_origin_button(self) -> Any:
        return self._view_origin_btn

    @property
    def widget(self) -> Any:
        return self._widget
