from __future__ import annotations

from qgis.core import QgsProcessingProvider  # type: ignore[import-untyped]


class agrobrProvider(QgsProcessingProvider):  # type: ignore[misc]  # pragma: no cover
    def id(self) -> str:  # noqa: A003
        return "agrobr"

    def name(self) -> str:
        return "agrobr"

    def loadAlgorithms(self) -> None:  # noqa: N802
        from agrobr_qgis import sources  # noqa: F401
        from agrobr_qgis.core.registry import SourceRegistry

        from .algorithms._factory import make_algorithm

        for source_cls in SourceRegistry.list_all():
            algo_cls = make_algorithm(source_cls)
            self.addAlgorithm(algo_cls())
