from __future__ import annotations

from typing import Any


class AgroBRPlugin:
    def __init__(self, iface: Any) -> None:
        self.iface = iface

    def initGui(self) -> None:  # noqa: N802
        from .core.proxy import propagate_proxy

        propagate_proxy()

        from qgis.core import QgsApplication  # type: ignore[import-untyped]

        from . import sources  # noqa: F401
        from .processing.provider import AgroBRProvider

        self._provider = AgroBRProvider()
        QgsApplication.processingRegistry().addProvider(self._provider)  # pragma: no cover

        from qgis.PyQt.QtWidgets import QAction  # type: ignore[import-untyped]

        from .core.logger import Logger
        from .gui.dock import MainDock

        self._logger = Logger(self.iface)
        self._dock = MainDock(self.iface)

        from qgis.PyQt.QtCore import Qt  # type: ignore[import-untyped]

        self.iface.addDockWidget(  # pragma: no cover
            Qt.DockWidgetArea.RightDockWidgetArea, self._dock.dock_widget
        )

        icon = QgsApplication.getThemeIcon("/mIconRaster.svg")
        self._action = QAction(icon, "AgroBR", self.iface.mainWindow())
        self._action.triggered.connect(lambda: self._dock.setVisible(True))
        self.iface.addToolBarIcon(self._action)  # pragma: no cover
        self.iface.addPluginToMenu("&AgroBR", self._action)  # pragma: no cover

    def unload(self) -> None:
        if hasattr(self, "_dock"):
            self._dock.close()
            self.iface.removeDockWidget(self._dock.dock_widget)  # pragma: no cover
            self._dock.dock_widget.deleteLater()
        if hasattr(self, "_action"):
            self.iface.removeToolBarIcon(self._action)  # pragma: no cover
            self.iface.removePluginFromMenu("&AgroBR", self._action)  # pragma: no cover
        try:
            from qgis.core import QgsApplication  # type: ignore[import-untyped]

            if hasattr(self, "_provider"):
                QgsApplication.processingRegistry().removeProvider(self._provider)
        except ImportError:
            pass
        try:
            from .core.layer_builder import LayerBuilder

            LayerBuilder.cleanup_temp()
        except ImportError:
            pass
        try:
            from .core.spatial_join import SpatialJoin

            SpatialJoin.clear_cache()
        except ImportError:
            pass
