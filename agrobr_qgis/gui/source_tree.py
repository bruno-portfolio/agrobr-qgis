from __future__ import annotations

from collections import defaultdict
from typing import Any

ITEM_TYPE_ROLE_OFFSET = 1

_CATEGORY_LABELS: dict[str, str] = {
    "ambiental": "Ambiental",
    "producao": "Producao",
    "mercado": "Mercado",
    "fundiario": "Fundiario",
    "regulatorio": "Regulatorio",
    "credito": "Credito",
    "clima": "Clima",
    "comercio_exterior": "Comercio Exterior",
}


class SourceFilterProxy:  # pragma: no cover
    def __init__(self) -> None:
        from qgis.PyQt.QtCore import (  # type: ignore[import-untyped]
            QSortFilterProxyModel,
            Qt,
        )

        class _Proxy(QSortFilterProxyModel):  # type: ignore[misc]
            def filterAcceptsRow(self, row: int, parent: Any) -> bool:  # noqa: N802
                model = self.sourceModel()
                index = model.index(row, 0, parent)
                if not parent.isValid():
                    for i in range(model.rowCount(index)):
                        child = model.index(i, 0, index)
                        text = model.data(child, Qt.ItemDataRole.DisplayRole) or ""
                        if self.filterRegularExpression().match(text.lower()).hasMatch():
                            return True
                    return False
                text = str(model.data(index, Qt.ItemDataRole.DisplayRole) or "")
                return bool(self.filterRegularExpression().match(text.lower()).hasMatch())

        self._proxy = _Proxy()
        self._proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._proxy.setRecursiveFilteringEnabled(False)

    @property
    def proxy(self) -> Any:
        return self._proxy


class SourceTreeWidget:  # pragma: no cover
    def __init__(self, parent: Any = None) -> None:
        from qgis.PyQt.QtCore import Qt  # type: ignore[import-untyped]
        from qgis.PyQt.QtGui import (  # type: ignore[import-untyped]
            QColor,
            QIcon,
            QPainter,
            QPixmap,
            QStandardItem,
            QStandardItemModel,
        )
        from qgis.PyQt.QtWidgets import QTreeView  # type: ignore[import-untyped]

        self._Qt = Qt
        self._QStandardItem = QStandardItem
        self._QColor = QColor
        self._QIcon = QIcon
        self._QPainter = QPainter
        self._QPixmap = QPixmap
        self._model = QStandardItemModel()
        self._filter = SourceFilterProxy()
        self._filter.proxy.setSourceModel(self._model)
        self._source_items: dict[str, Any] = {}

        self._view = QTreeView(parent)
        self._view.setModel(self._filter.proxy)
        self._view.setHeaderHidden(True)
        self._view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

        self._build_model()
        self._view.expanded.connect(self._on_category_expanded)

    def _build_model(self) -> None:
        from agrobr_qgis.core.registry import SourceRegistry

        item_type_role = self._Qt.ItemDataRole.UserRole + ITEM_TYPE_ROLE_OFFSET

        from agrobr_qgis.core.template import TemplateRegistry

        templates = TemplateRegistry.list_all()
        if templates:
            tmpl_parent = self._QStandardItem(f"Templates ({len(templates)})")
            tmpl_parent.setSelectable(False)
            tmpl_parent.setToolTip("Templates multi-fonte")
            for tmpl in templates:
                item = self._QStandardItem(tmpl.name)
                item.setData(tmpl.id, self._Qt.ItemDataRole.UserRole)
                item.setData("template", item_type_role)
                item.setToolTip(tmpl.description)
                tmpl_parent.appendRow(item)
            self._model.appendRow(tmpl_parent)

        sources = SourceRegistry.list_all()
        grouped: dict[str, list[type[Any]]] = defaultdict(list)
        for src in sources:
            grouped[src.category().value].append(src)

        for cat_value, cat_sources in sorted(grouped.items()):
            label = _CATEGORY_LABELS.get(cat_value, cat_value.title())
            parent = self._QStandardItem(f"{label} ({len(cat_sources)})")
            parent.setSelectable(False)
            parent.setToolTip(f"{label} — {len(cat_sources)} fontes")

            for src in sorted(cat_sources, key=lambda s: s.name()):
                item = self._QStandardItem(src.name())
                item.setData(src.id(), self._Qt.ItemDataRole.UserRole)
                item.setData("source", item_type_role)
                item.setToolTip(src.description() or src.name())
                parent.appendRow(item)
                self._source_items[src.id()] = item

            self._model.appendRow(parent)

    def filter_text(self, text: str) -> None:
        from qgis.PyQt.QtCore import QRegularExpression  # type: ignore[import-untyped]

        pattern = QRegularExpression.escape(text.lower())
        self._filter.proxy.setFilterRegularExpression(pattern)
        if text:
            self._view.expanded.disconnect(self._on_category_expanded)
            self._view.expandAll()
            self._view.expanded.connect(self._on_category_expanded)

    def selected_item(self) -> tuple[str, str] | None:
        indexes = self._view.selectionModel().selectedIndexes()
        if not indexes:
            return None
        source_index = self._filter.proxy.mapToSource(indexes[0])
        item_id: str | None = self._model.data(source_index, self._Qt.ItemDataRole.UserRole)
        item_type_role = self._Qt.ItemDataRole.UserRole + ITEM_TYPE_ROLE_OFFSET
        item_type: str = self._model.data(source_index, item_type_role) or "source"
        return (item_id, item_type) if item_id else None

    def selected_source_id(self) -> str | None:
        item = self.selected_item()
        if item and item[1] == "source":
            return item[0]
        return None

    def connect_selection_changed(self, slot: Any) -> None:
        self._view.selectionModel().selectionChanged.connect(slot)

    def _on_category_expanded(self, proxy_index: Any) -> None:
        source_index = self._filter.proxy.mapToSource(proxy_index)
        parent_item = self._model.itemFromIndex(source_index)
        if parent_item is None:
            return
        source_ids: list[str] = []
        for i in range(parent_item.rowCount()):
            child = parent_item.child(i)
            sid = child.data(self._Qt.ItemDataRole.UserRole) if child else None
            if sid:
                source_ids.append(sid)
        if not source_ids:
            return
        from agrobr_qgis.core.health_check import check_sources

        task = check_sources(source_ids)
        if task is None:
            return
        task.allChecked.connect(self._on_health_results)
        from qgis.core import QgsApplication  # type: ignore[import-untyped]

        QgsApplication.taskManager().addTask(task)

    def _on_health_results(self, statuses: list[Any]) -> None:
        for status in statuses:
            self._update_health_icon(status.source_id, status.status)

    def _update_health_icon(self, source_id: str, status: str) -> None:
        item = self._source_items.get(source_id)
        if item:
            item.setIcon(self._status_icon(status))

    def _status_icon(self, status: str) -> Any:
        if status == "unchecked":
            return self._QIcon()
        color = self._QColor(76, 175, 80) if status == "online" else self._QColor(189, 189, 189)
        px = self._QPixmap(12, 12)
        px.fill(self._Qt.GlobalColor.transparent)
        painter = self._QPainter(px)
        painter.setRenderHint(self._QPainter.RenderHint.Antialiasing)
        painter.setBrush(color)
        painter.setPen(self._Qt.PenStyle.NoPen)
        painter.drawEllipse(1, 1, 10, 10)
        painter.end()
        return self._QIcon(px)

    @property
    def view(self) -> Any:
        return self._view
