from __future__ import annotations

from typing import Any

from agrobr_qgis.core.constants import UF_LIST
from agrobr_qgis.core.source_adapter import ParamType, SourceCapability, SourceParameter


class ParamPanel:  # pragma: no cover
    def __init__(self, iface: Any) -> None:
        from qgis.PyQt.QtWidgets import QVBoxLayout, QWidget  # type: ignore[import-untyped]

        self._iface = iface
        self._widget = QWidget()
        self._layout = QVBoxLayout(self._widget)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._widgets: dict[str, Any] = {}
        self._geo_checkbox: Any = None
        self._join_checkbox: Any = None
        self._auth_warning = False

    def build(
        self,
        parameters: list[Any],
        capabilities: SourceCapability,
        source_id: str,
    ) -> None:
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QCheckBox,
            QFormLayout,
            QLabel,
            QWidget,
        )

        self._widgets.clear()
        self._geo_checkbox = None
        self._join_checkbox = None
        self._auth_warning = False

        old = self._layout.takeAt(0)
        while old:
            if old.widget():
                old.widget().deleteLater()
            old = self._layout.takeAt(0)

        container = QWidget()
        form = QFormLayout(container)
        form.setContentsMargins(4, 4, 4, 4)

        for param in parameters:
            w = self._create_widget(param)
            self._widgets[param.name] = (param, w)
            label = QLabel(param.label)
            if param.help_text:
                label.setToolTip(param.help_text)
            form.addRow(label, w)

        if capabilities & SourceCapability.GEO:
            self._geo_checkbox = QCheckBox(self._widget.tr("Saida geoespacial"))
            form.addRow(self._geo_checkbox)
            self._geo_checkbox.stateChanged.connect(self._on_geo_changed)

        if capabilities & SourceCapability.MUNICIPAL_JOIN:
            self._join_checkbox = QCheckBox(self._widget.tr("Join municipal"))
            form.addRow(self._join_checkbox)
            if self._geo_checkbox:
                self._join_checkbox.setVisible(not self._geo_checkbox.isChecked())

        if capabilities & SourceCapability.AUTH:
            from agrobr_qgis.core.auth_manager import AuthManager

            if not AuthManager.has_token(source_id):
                self._auth_warning = True
                warn = QLabel(self._widget.tr("Token nao configurado — veja Configuracoes"))
                warn.setStyleSheet("color: #cc6600; font-weight: bold;")
                form.addRow(warn)

        self._layout.addWidget(container)

    def _on_geo_changed(self, state: int) -> None:
        if self._join_checkbox:
            self._join_checkbox.setVisible(state == 0)

    def _create_widget(self, param: SourceParameter) -> Any:
        from qgis.PyQt.QtCore import QDate  # type: ignore[import-untyped]
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QComboBox,
            QDateEdit,
            QLineEdit,
            QSpinBox,
        )

        t = param.param_type
        if t == ParamType.STRING:
            w = QLineEdit()
            if param.default:
                w.setText(str(param.default))
            if param.help_text:
                w.setPlaceholderText(param.help_text)
            return w
        if t == ParamType.INT:
            w = QSpinBox()
            w.setRange(0, 999_999)
            if param.default is not None:
                w.setValue(int(param.default))
            return w
        if t == ParamType.DATE:
            w = QDateEdit()
            w.setDisplayFormat("dd/MM/yyyy")
            w.setCalendarPopup(True)
            w.setDate(QDate.currentDate())
            return w
        if t == ParamType.CHOICE:
            w = QComboBox()
            w.addItem("")
            if param.choices:
                w.addItems(param.choices)
            if param.default:
                idx = w.findText(str(param.default))
                if idx >= 0:
                    w.setCurrentIndex(idx)
            return w
        if t == ParamType.CHOICE_DYNAMIC:
            w = QComboBox()
            w.setEditable(True)
            return w
        if t == ParamType.MULTI_CHOICE:
            w = QLineEdit()
            w.setPlaceholderText(self._widget.tr("valores separados por virgula"))
            return w
        if t == ParamType.BBOX:
            try:
                from qgis.gui import QgsExtentGroupBox  # type: ignore[import-untyped]

                w = QgsExtentGroupBox()
                w.setMapCanvas(self._iface.mapCanvas())
                return w
            except ImportError:
                w = QLineEdit()
                w.setPlaceholderText("xmin, ymin, xmax, ymax")
                return w
        if t == ParamType.UF:
            w = QComboBox()
            w.addItem("")
            w.addItems(UF_LIST)
            return w
        if t == ParamType.PRODUTO:
            w = QLineEdit()
            w.setPlaceholderText(self._widget.tr("Ex: Soja, Milho"))
            return w
        w = QLineEdit()
        return w

    def collect_params(self) -> dict[str, Any]:
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QComboBox,
            QDateEdit,
            QLineEdit,
            QSpinBox,
        )

        result: dict[str, Any] = {}
        for name, (_param, widget) in self._widgets.items():
            if isinstance(widget, QSpinBox):
                result[name] = widget.value()
            elif isinstance(widget, QDateEdit):
                result[name] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QComboBox):
                val = widget.currentText()
                if val:
                    result[name] = val
            elif isinstance(widget, QLineEdit):
                val = widget.text().strip()
                if val:
                    result[name] = val
            else:
                try:
                    extent = widget.outputExtent()
                    if not extent.isNull():
                        result[name] = (
                            extent.xMinimum(),
                            extent.yMinimum(),
                            extent.xMaximum(),
                            extent.yMaximum(),
                        )
                except AttributeError:
                    pass
        return {k: v.strip() if isinstance(v, str) else v for k, v in result.items()}

    def restore_params(self, cached: dict[str, Any]) -> None:
        from qgis.PyQt.QtCore import QDate  # type: ignore[import-untyped]
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QComboBox,
            QDateEdit,
            QLineEdit,
            QSpinBox,
        )

        for name, val in cached.items():
            if name not in self._widgets:
                continue
            _, widget = self._widgets[name]
            if isinstance(widget, QSpinBox):
                widget.setValue(int(val))
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.fromString(str(val), "yyyy-MM-dd"))
            elif isinstance(widget, QComboBox):
                idx = widget.findText(str(val))
                if idx >= 0:
                    widget.setCurrentIndex(idx)
                elif widget.isEditable():
                    widget.setEditText(str(val))
            elif isinstance(widget, QLineEdit):
                widget.setText(str(val))

    def is_geo_checked(self) -> bool:
        return bool(self._geo_checkbox and self._geo_checkbox.isChecked())

    def is_join_checked(self) -> bool:
        return bool(self._join_checkbox and self._join_checkbox.isChecked())

    def has_auth_warning(self) -> bool:
        return self._auth_warning

    @property
    def widget(self) -> Any:
        return self._widget
