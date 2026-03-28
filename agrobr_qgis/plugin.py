from __future__ import annotations

from typing import Any


class AgroBRPlugin:
    def __init__(self, iface: Any) -> None:
        self.iface = iface

    def initGui(self) -> None:  # noqa: N802
        from .core.proxy import propagate_proxy

        propagate_proxy()

    def unload(self) -> None:
        try:
            from .core.layer_builder import LayerBuilder

            LayerBuilder.cleanup_temp()
        except ImportError:
            pass
