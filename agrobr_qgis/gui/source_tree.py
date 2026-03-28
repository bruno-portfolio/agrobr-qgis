from __future__ import annotations

from collections import defaultdict
from typing import Any

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
            QStandardItem,
            QStandardItemModel,
        )
        from qgis.PyQt.QtWidgets import QTreeView  # type: ignore[import-untyped]

        self._Qt = Qt
        self._QStandardItem = QStandardItem
        self._model = QStandardItemModel()
        self._filter = SourceFilterProxy()
        self._filter.proxy.setSourceModel(self._model)

        self._view = QTreeView(parent)
        self._view.setModel(self._filter.proxy)
        self._view.setHeaderHidden(True)
        self._view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

        self._build_model()
        self._view.expandAll()

    def _build_model(self) -> None:
        from agrobr_qgis.core.registry import SourceRegistry

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
                item.setToolTip(src.description() or src.name())
                parent.appendRow(item)

            self._model.appendRow(parent)

    def filter_text(self, text: str) -> None:
        from qgis.PyQt.QtCore import QRegularExpression  # type: ignore[import-untyped]

        pattern = QRegularExpression.escape(text.lower())
        self._filter.proxy.setFilterRegularExpression(pattern)
        if text:
            self._view.expandAll()

    def selected_source_id(self) -> str | None:
        indexes = self._view.selectionModel().selectedIndexes()
        if not indexes:
            return None
        source_index = self._filter.proxy.mapToSource(indexes[0])
        result: str | None = self._model.data(source_index, self._Qt.ItemDataRole.UserRole)
        return result

    def connect_selection_changed(self, slot: Any) -> None:
        self._view.selectionModel().selectionChanged.connect(slot)

    @property
    def view(self) -> Any:
        return self._view
