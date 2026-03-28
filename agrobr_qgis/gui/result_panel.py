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
        self._zoom_btn.setEnabled(False)

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

        self._layout.addWidget(container)

    def _clear_content(self) -> None:
        old = self._layout.takeAt(0)
        while old:
            if old.widget():
                old.widget().deleteLater()
            old = self._layout.takeAt(0)

    def enable_zoom(self) -> None:
        self._zoom_btn.setEnabled(True)

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
    def widget(self) -> Any:
        return self._widget
