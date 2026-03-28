from __future__ import annotations

from configparser import ConfigParser
from functools import partial
from pathlib import Path
from typing import Any

from agrobr_qgis.core.data_contract import ContractResult
from agrobr_qgis.gui.state import STATE_CONFIG, DockState, ParamCache

_PAGE_MAP: dict[DockState, int] = {
    DockState.IDLE: 0,
    DockState.SELECTED: 1,
    DockState.LOADING: 2,
    DockState.RESULT: 3,
    DockState.ERROR: 4,
}


class MainDock:  # pragma: no cover
    def __init__(self, iface: Any) -> None:
        from qgis.PyQt.QtCore import Qt  # type: ignore[import-untyped]
        from qgis.PyQt.QtWidgets import (  # type: ignore[import-untyped]
            QDockWidget,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QSplitter,
            QStackedWidget,
            QVBoxLayout,
            QWidget,
        )

        from agrobr_qgis.core.logger import Logger

        from .param_panel import ParamPanel
        from .result_panel import ResultPanel
        from .source_tree import SourceTreeWidget

        self._iface = iface
        self._logger = Logger(iface)
        self._state = DockState.IDLE
        self._param_cache = ParamCache()
        self._current_source_id: str | None = None
        self._current_task: Any = None
        self._current_result: ContractResult | None = None
        self._added_layer: Any = None
        self._connections: list[tuple[Any, Any]] = []

        self._dock = QDockWidget("AgroBR")
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)

        self._search_bar = QLineEdit()
        self._search_bar.setPlaceholderText(self._dock_tr("Buscar fonte..."))
        self._search_bar.setClearButtonEnabled(True)
        main_layout.addWidget(self._search_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self._source_tree = SourceTreeWidget()
        splitter.addWidget(self._source_tree.view)

        self._stacked = QStackedWidget()
        self._idle_label = QLabel(self._dock_tr("Selecione uma fonte de dados para comecar"))
        self._idle_label.setWordWrap(True)
        self._stacked.addWidget(self._idle_label)

        self._param_container = QWidget()
        self._param_layout = QVBoxLayout(self._param_container)
        self._param_layout.setContentsMargins(0, 0, 0, 0)
        self._param_panel = ParamPanel(iface)
        self._param_layout.addWidget(self._param_panel.widget)
        self._stacked.addWidget(self._param_container)

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 0)
        self._stacked.addWidget(self._progress_bar)

        self._result_panel = ResultPanel()
        self._stacked.addWidget(self._result_panel.widget)

        self._error_label = QLabel()
        self._error_label.setWordWrap(True)
        self._error_label.setStyleSheet("color: #cc0000; font-weight: bold;")
        self._stacked.addWidget(self._error_label)

        splitter.addWidget(self._stacked)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([200, 350])
        main_layout.addWidget(splitter, 1)

        bottom_bar = QHBoxLayout()
        self._fetch_button = QPushButton(self._dock_tr("Buscar Dados"))
        self._settings_button = QPushButton(self._dock_tr("Configuracoes"))
        bottom_bar.addWidget(self._fetch_button)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self._settings_button)
        main_layout.addLayout(bottom_bar)

        status_bar = QHBoxLayout()
        self._status_label = QLabel(self._dock_tr("Pronto"))
        self._version_label = QLabel(self._read_version())
        status_bar.addWidget(self._status_label)
        status_bar.addStretch()
        status_bar.addWidget(self._version_label)
        main_layout.addLayout(status_bar)

        self._dock.setWidget(main_widget)

        self._search_bar.textChanged.connect(self._source_tree.filter_text)
        self._source_tree.connect_selection_changed(self._on_selection_changed)
        self._fetch_button.clicked.connect(self._on_fetch)
        self._settings_button.clicked.connect(self._on_settings)
        self._result_panel.add_button.clicked.connect(self._on_add_to_map)
        self._result_panel.zoom_button.clicked.connect(self._on_zoom)
        self._result_panel.fetch_again_button.clicked.connect(self._on_fetch_again)

        from qgis.PyQt.QtGui import QKeySequence, QShortcut  # type: ignore[import-untyped]

        sc_search = QShortcut(QKeySequence("Ctrl+F"), self._dock)
        sc_search.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        sc_search.activated.connect(self._search_bar.setFocus)

        sc_fetch = QShortcut(QKeySequence(Qt.Key.Key_Return), self._dock)
        sc_fetch.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        sc_fetch.activated.connect(self._on_fetch_shortcut)

        sc_cancel = QShortcut(QKeySequence(Qt.Key.Key_Escape), self._dock)
        sc_cancel.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        sc_cancel.activated.connect(self._on_cancel)

        self._apply_state(DockState.IDLE)

    def _dock_tr(self, text: str) -> str:
        result: str = self._dock.tr(text)
        return result

    def _on_selection_changed(self) -> None:
        source_id = self._source_tree.selected_source_id()
        if source_id is None:
            return
        self._current_source_id = source_id
        self._added_layer = None

        from agrobr_qgis.core.registry import SourceRegistry

        adapter_cls = SourceRegistry.get(source_id)
        if adapter_cls is None:
            return

        self._param_panel.build(adapter_cls.parameters(), adapter_cls.capabilities(), source_id)
        cached = self._param_cache.load(source_id)
        if cached:
            self._param_panel.restore_params(cached)

        self._apply_state(DockState.SELECTED)
        self._fetch_button.setEnabled(not self._param_panel.has_auth_warning())

    def _on_fetch(self) -> None:
        if not self._current_source_id:
            return

        from qgis.core import QgsApplication  # type: ignore[import-untyped]

        from agrobr_qgis.core.registry import SourceRegistry
        from agrobr_qgis.core.task_runner import FetchTask

        adapter_cls = SourceRegistry.get(self._current_source_id)
        if adapter_cls is None:
            self._on_error_internal(self._dock_tr("Fonte nao encontrada"))
            return

        self._disconnect_all()

        params = self._param_panel.collect_params()
        self._param_cache.save(self._current_source_id, params)

        adapter = adapter_cls()
        task = FetchTask(
            adapter,
            params,
            geo=self._param_panel.is_geo_checked(),
            join_municipal=self._param_panel.is_join_checked(),
        )
        self._current_task = task

        self._connect(task.resultReady, partial(self._on_result, task))
        self._connect(task.errorOccurred, partial(self._on_error, task))

        QgsApplication.taskManager().addTask(task)
        self._apply_state(DockState.LOADING)
        self._status_label.setText(self._dock_tr("Buscando {}...").format(adapter_cls.name()))

    def _on_result(self, task: Any, result: ContractResult) -> None:
        if task is not self._current_task:
            return
        self._current_task = None
        self._current_result = result
        self._result_panel.show_result(result)
        self._apply_state(DockState.RESULT)
        self._status_label.setText(self._dock_tr("Pronto"))

        from agrobr_qgis.core.settings_manager import SettingsManager

        if self._current_source_id:
            SettingsManager.add_recent_source(self._current_source_id)
            self._logger.audit(f"Fetch OK: {self._current_source_id} — {result.row_count} rows")

    def _on_error(self, task: Any, msg: str) -> None:
        if task is not self._current_task:
            return
        self._current_task = None
        self._error_label.setText(msg)
        self._logger.error(msg)
        self._apply_state(DockState.ERROR)
        self._status_label.setText(self._dock_tr("Erro ao buscar dados"))

    def _on_error_internal(self, msg: str) -> None:
        self._error_label.setText(msg)
        self._logger.error(msg)
        self._apply_state(DockState.ERROR)

    def _on_add_to_map(self) -> None:
        if not self._current_result or not self._current_source_id:
            return

        from qgis.core import QgsProject  # type: ignore[import-untyped]

        from agrobr_qgis.core.layer_builder import LayerBuilder
        from agrobr_qgis.core.registry import SourceRegistry

        adapter_cls = SourceRegistry.get(self._current_source_id)
        name = adapter_cls.name() if adapter_cls else self._current_source_id
        layer_name = f"AgroBR — {name}"

        result = self._current_result
        layer = LayerBuilder.from_contract_result(result, layer_name)
        QgsProject.instance().addMapLayer(layer)
        self._added_layer = layer
        self._current_result = None
        self._result_panel.enable_zoom()
        self._logger.user(f"{result.row_count} registros adicionados como '{layer_name}'")

    def _on_zoom(self) -> None:
        if self._added_layer:
            canvas = self._iface.mapCanvas()
            canvas.setExtent(self._added_layer.extent())
            canvas.refresh()

    def _on_fetch_again(self) -> None:
        if self._current_source_id:
            self._apply_state(DockState.SELECTED)
            self._fetch_button.setEnabled(not self._param_panel.has_auth_warning())

    def _on_fetch_shortcut(self) -> None:
        if self._state == DockState.SELECTED:
            self._on_fetch()

    def _on_cancel(self) -> None:
        if self._state == DockState.LOADING and self._current_task:
            self._current_task.cancel()
            self._current_task = None
            self._apply_state(DockState.SELECTED)
            self._status_label.setText(self._dock_tr("Cancelado"))

    def _on_settings(self) -> None:
        from .settings_dialog import SettingsDialog

        dialog = SettingsDialog(self._dock)
        dialog.exec()

    def _apply_state(self, state: DockState) -> None:
        self._state = state
        vis = STATE_CONFIG[state]

        self._stacked.setCurrentIndex(_PAGE_MAP.get(state, 0))

        self._search_bar.setVisible(vis.search_bar)
        self._source_tree.view.setVisible(vis.source_tree)
        self._fetch_button.setVisible(vis.fetch_button)
        self._settings_button.setVisible(True)

    def _read_version(self) -> str:
        try:
            parser = ConfigParser()
            parser.read(str(Path(__file__).parent.parent / "metadata.txt"))
            return parser.get("general", "version", fallback="")
        except Exception:
            return ""

    def _connect(self, signal: Any, slot: Any) -> None:
        signal.connect(slot)
        self._connections.append((signal, slot))

    def _disconnect_all(self) -> None:
        import contextlib

        for signal, slot in self._connections:
            with contextlib.suppress(TypeError, RuntimeError):
                signal.disconnect(slot)
        self._connections.clear()

    def close(self) -> None:
        if self._current_task:
            self._current_task.cancel()
            self._current_task = None
        self._disconnect_all()
        self._dock.close()

    @property
    def dock_widget(self) -> Any:
        return self._dock

    def setVisible(self, visible: bool) -> None:  # noqa: N802
        self._dock.setVisible(visible)
