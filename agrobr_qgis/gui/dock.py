from __future__ import annotations

from configparser import ConfigParser
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
    DockState.TEMPLATE_RESULT: 3,
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
        self._current_template: Any = None
        self._current_template_result: Any = None
        self._current_result: ContractResult | None = None
        self._current_template_task: Any = None
        self._added_layer: Any = None
        self._connections: list[tuple[Any, Any]] = []

        from agrobr_qgis.core.fetch_controller import FetchController

        self._fetch_controller = FetchController(self._on_result, self._on_error)

        self._dock = QDockWidget("agrobr")
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

        from qgis.PyQt.QtWidgets import QScrollArea  # type: ignore[import-untyped]

        self._stacked = QStackedWidget()
        self._idle_label = QLabel(self._dock_tr("Selecione uma fonte de dados para comecar"))
        self._idle_label.setWordWrap(True)
        self._stacked.addWidget(self._idle_label)

        self._param_container = QWidget()
        self._param_layout = QVBoxLayout(self._param_container)
        self._param_layout.setContentsMargins(0, 0, 0, 0)
        self._param_panel = ParamPanel(iface)
        self._param_layout.addWidget(self._param_panel.widget)
        param_scroll = QScrollArea()
        param_scroll.setWidget(self._param_container)
        param_scroll.setWidgetResizable(True)
        param_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self._stacked.addWidget(param_scroll)

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
        self._result_panel.open_table_button.clicked.connect(self._on_open_table)
        self._result_panel.save_as_button.clicked.connect(self._on_save_as)
        self._result_panel.view_origin_button.clicked.connect(self._on_view_origin)

        from qgis.PyQt.QtGui import QKeySequence, QShortcut  # type: ignore[import-untyped]

        self._sc_search = QShortcut(QKeySequence("Ctrl+F"), self._dock)
        self._sc_search.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        self._sc_search.activated.connect(self._search_bar.setFocus)

        self._sc_fetch = QShortcut(QKeySequence(Qt.Key.Key_Return), self._dock)
        self._sc_fetch.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        self._sc_fetch.activated.connect(self._on_fetch_shortcut)

        self._sc_cancel = QShortcut(QKeySequence(Qt.Key.Key_Escape), self._dock)
        self._sc_cancel.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        self._sc_cancel.activated.connect(self._on_cancel)

        self._apply_state(DockState.IDLE)

        from qgis.core import QgsProject  # type: ignore[import-untyped]

        self._project = QgsProject.instance()
        self._project.writeProject.connect(self._save_to_project)
        self._project.readProject.connect(self._restore_from_project)
        self._project.cleared.connect(self._param_cache.clear)

    def _dock_tr(self, text: str) -> str:
        result: str = self._dock.tr(text)
        return result

    def _on_selection_changed(self) -> None:
        item = self._source_tree.selected_item()
        if item is None:
            return
        item_id, item_type = item
        if item_type == "template":
            self._on_template_selected(item_id)
        else:
            self._on_source_selected(item_id)

    def _on_source_selected(self, source_id: str) -> None:
        if self._current_source_id and self._state == DockState.SELECTED:
            self._param_cache.save(self._current_source_id, self._param_panel.collect_params())
        self._current_source_id = source_id
        self._current_template = None
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

    def _on_template_selected(self, template_id: str) -> None:
        from agrobr_qgis.core.source_adapter import SourceCapability
        from agrobr_qgis.core.template import TemplateRegistry

        template = TemplateRegistry.get(template_id)
        if template is None:
            return
        self._current_template = template
        self._current_source_id = None
        self._added_layer = None
        self._param_panel.build(list(template.params), SourceCapability(0), template_id)
        self._apply_state(DockState.SELECTED)
        self._fetch_button.setEnabled(True)

    def _on_fetch(self) -> None:
        if self._current_template:
            self._on_template_fetch()
            return
        if not self._current_source_id:
            return

        params = self._param_panel.collect_params()
        self._param_cache.save(self._current_source_id, params)

        if not self._fetch_controller.start_fetch(
            self._current_source_id,
            params,
            geo=self._param_panel.is_geo_checked(),
            join=self._param_panel.is_join_checked(),
        ):
            self._on_error_internal(self._dock_tr("Fonte nao encontrada"))
            return

        from agrobr_qgis.core.registry import SourceRegistry

        adapter_cls = SourceRegistry.get(self._current_source_id)
        self._apply_state(DockState.LOADING)
        name = adapter_cls.name() if adapter_cls else self._current_source_id
        self._status_label.setText(self._dock_tr("Buscando {}...").format(name))

    def _on_template_fetch(self) -> None:
        if not self._current_template:
            return
        from qgis.core import QgsApplication  # type: ignore[import-untyped]

        from agrobr_qgis.core.template_runner import TemplateFetchTask

        params = self._param_panel.collect_params()
        task = TemplateFetchTask(
            self._current_template, params, geo=self._param_panel.is_geo_checked()
        )
        self._current_template_task = task
        task.allCompleted.connect(self._on_template_result)
        task.errorOccurred.connect(lambda msg: self._on_error(None, msg))
        QgsApplication.taskManager().addTask(task)
        self._apply_state(DockState.LOADING)
        self._status_label.setText(
            self._dock_tr("Template: {}...").format(self._current_template.name)
        )

    def _on_template_result(self, result: Any) -> None:
        self._current_template_task = None
        self._current_template_result = result
        self._result_panel.show_template_result(result)
        if self._result_panel.add_all_button:
            self._result_panel.add_all_button.clicked.connect(self._on_template_add_all)
        self._apply_state(DockState.TEMPLATE_RESULT)
        ok = len(result.succeeded)
        fail = len(result.failed)
        self._status_label.setText(self._dock_tr(f"Template: {ok} OK, {fail} falhas"))

    def _on_template_add_all(self) -> None:
        if not self._current_template_result:
            return
        from qgis.core import QgsProject  # type: ignore[import-untyped]

        from agrobr_qgis.core.layer_builder import LayerBuilder

        root = QgsProject.instance().layerTreeRoot()
        group = root.insertGroup(0, f"agrobr — {self._current_template_result.template_name}")
        for outcome in self._current_template_result.succeeded:
            layer_name = f"agrobr — {outcome.source_name}"
            layer = LayerBuilder.from_contract_result(outcome.result, layer_name)
            QgsProject.instance().addMapLayer(layer, False)
            group.addLayer(layer)
        self._logger.user(f"{len(self._current_template_result.succeeded)} camadas adicionadas")

    def _on_result(self, _task: Any, result: ContractResult) -> None:
        self._current_result = result
        self._result_panel.show_result(result)
        self._apply_state(DockState.RESULT)
        self._status_label.setText(self._dock_tr("Pronto"))

        from agrobr_qgis.core.registry import SourceRegistry
        from agrobr_qgis.core.settings_manager import SettingsManager

        if self._current_source_id:
            SettingsManager.add_recent_source(self._current_source_id)
            self._logger.audit(f"Fetch OK: {self._current_source_id} — {result.row_count} rows")
            adapter_cls = SourceRegistry.get(self._current_source_id)
            if adapter_cls and adapter_cls.source_url():
                self._result_panel.enable_origin()

    def _on_error(self, _task: Any, msg: str) -> None:
        self._error_label.setText(msg)
        self._logger.error(msg)
        self._apply_state(DockState.ERROR)
        self._status_label.setText(self._dock_tr("Erro ao buscar dados"))

    def _on_error_internal(self, msg: str) -> None:
        self._on_error(None, msg)

    def _on_add_to_map(self) -> None:
        if not self._current_result or not self._current_source_id:
            return

        from qgis.core import QgsProject  # type: ignore[import-untyped]

        from agrobr_qgis.core.layer_builder import LayerBuilder
        from agrobr_qgis.core.registry import SourceRegistry

        adapter_cls = SourceRegistry.get(self._current_source_id)
        name = adapter_cls.name() if adapter_cls else self._current_source_id
        layer_name = f"agrobr — {name}"

        result = self._current_result
        style_path = LayerBuilder.resolve_style(result.geometry_type)
        temporal_col = adapter_cls.temporal_column() if adapter_cls else None
        layer = LayerBuilder.from_contract_result(result, layer_name, style_path, temporal_col)
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

    def _on_open_table(self) -> None:
        if self._added_layer:
            self._iface.showAttributeTable(self._added_layer)

    def _on_save_as(self) -> None:
        if not self._added_layer:
            return
        from qgis.core import QgsVectorFileWriter  # type: ignore[import-untyped]
        from qgis.PyQt.QtWidgets import QFileDialog  # type: ignore[import-untyped]

        path, selected_filter = QFileDialog.getSaveFileName(
            self._dock,
            self._dock_tr("Salvar camada como..."),
            "",
            "GeoPackage (*.gpkg);;GeoJSON (*.geojson);;Shapefile (*.shp)",
        )
        if path:
            QgsVectorFileWriter.writeAsVectorFormat(self._added_layer, path, "UTF-8")
            self._logger.user(f"Camada exportada para {path}")

    def _on_view_origin(self) -> None:
        if not self._current_source_id:
            return
        from qgis.PyQt.QtCore import QUrl  # type: ignore[import-untyped]
        from qgis.PyQt.QtGui import QDesktopServices  # type: ignore[import-untyped]

        from agrobr_qgis.core.registry import SourceRegistry

        adapter_cls = SourceRegistry.get(self._current_source_id)
        url = adapter_cls.source_url() if adapter_cls else None
        if url:
            QDesktopServices.openUrl(QUrl(url))

    def _on_fetch_again(self) -> None:
        if self._current_source_id:
            self._apply_state(DockState.SELECTED)
            self._fetch_button.setEnabled(not self._param_panel.has_auth_warning())

    def _on_fetch_shortcut(self) -> None:
        if self._state == DockState.SELECTED:
            self._on_fetch()

    def _on_cancel(self) -> None:
        if self._state != DockState.LOADING:
            return
        if self._fetch_controller.is_active:
            self._fetch_controller.cancel()
        elif self._current_template_task:
            self._current_template_task.cancel()
            self._current_template_task = None
        self._apply_state(DockState.SELECTED)
        self._status_label.setText(self._dock_tr("Cancelado"))

    def _on_settings(self) -> None:
        from .settings_dialog import SettingsDialog

        dialog = SettingsDialog(self._dock)
        dialog.exec()

    def _save_to_project(self) -> None:
        import json

        if self._current_source_id:
            self._project.writeEntry("agrobr", "last_source", self._current_source_id)
        self._project.writeEntry("agrobr", "param_cache", json.dumps(self._param_cache.to_dict()))

    def _restore_from_project(self) -> None:
        import contextlib
        import json

        self._param_cache.clear()
        cache_json, ok = self._project.readEntry("agrobr", "param_cache", "")
        if ok and cache_json:
            with contextlib.suppress(json.JSONDecodeError, TypeError):
                self._param_cache.from_dict(json.loads(cache_json))

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
        self._fetch_controller.cancel()
        self._disconnect_all()
        import contextlib

        with contextlib.suppress(TypeError, RuntimeError):
            self._project.writeProject.disconnect(self._save_to_project)
            self._project.readProject.disconnect(self._restore_from_project)
            self._project.cleared.disconnect(self._param_cache.clear)
        self._dock.close()

    @property
    def dock_widget(self) -> Any:
        return self._dock

    def setVisible(self, visible: bool) -> None:  # noqa: N802
        self._dock.setVisible(visible)
