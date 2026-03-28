from __future__ import annotations

from typing import Any


class AgroBRProvider:  # pragma: no cover
    def id(self) -> str:  # noqa: A003
        return "agrobr"

    def name(self) -> str:
        return "AgroBR"

    def loadAlgorithms(self) -> None:  # noqa: N802
        from agrobr_qgis import sources  # noqa: F401
        from agrobr_qgis.core.registry import SourceRegistry

        from .algorithms._factory import make_algorithm

        for source_cls in SourceRegistry.list_all():
            algo_cls = make_algorithm(source_cls)
            self.addAlgorithm(algo_cls())  # type: ignore[attr-defined]

    def addAlgorithm(self, algorithm: Any) -> None:  # noqa: N802
        pass
