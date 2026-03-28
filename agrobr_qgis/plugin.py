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

    def unload(self) -> None:
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
