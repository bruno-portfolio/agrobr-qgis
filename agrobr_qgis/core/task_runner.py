from __future__ import annotations

from typing import Any

from qgis.core import QgsTask  # type: ignore[import-untyped]
from qgis.PyQt.QtCore import pyqtSignal  # type: ignore[import-untyped]

from .constants import FETCH_TIMEOUT_SECONDS
from .data_contract import ContractResult, DataContract
from .source_adapter import SourceAdapter, SourceCapability


class FetchTask(QgsTask):  # type: ignore[misc]
    resultReady = pyqtSignal(object)
    errorOccurred = pyqtSignal(str)

    def __init__(
        self,
        source: SourceAdapter,
        params: dict[str, Any],
        *,
        geo: bool = False,
        join_municipal: bool = False,
        timeout: int = FETCH_TIMEOUT_SECONDS,
        description: str = "",
    ) -> None:
        super().__init__(
            description or f"Buscando {source.name()}...",
            QgsTask.CanCancel,
        )
        self.source = source
        self.params = params
        self.geo = geo
        self.join_municipal = join_municipal
        self.timeout = timeout
        self._contract_result: ContractResult | None = None
        self._error: Exception | None = None

    def run(self) -> bool:
        try:
            if self.isCanceled():
                return False

            self.setProgress(10)
            raw = self.source.fetch(geo=self.geo, **self.params)

            if self.isCanceled():
                return False

            self.setProgress(60)
            self._contract_result = DataContract.validate(raw)

            if self.isCanceled():
                return False

            self.setProgress(80)
            if (
                self.join_municipal
                and not self._contract_result.has_geometry
                and self.source.capabilities() & SourceCapability.MUNICIPAL_JOIN
            ):
                join_col = self.source.join_column()
                if join_col and join_col in self._contract_result.df.columns:
                    from .spatial_join import SpatialJoin  # type: ignore[import-not-found]

                    geo_df = SpatialJoin.to_municipal(self._contract_result.df, join_col)
                    self._contract_result = DataContract.validate(geo_df)

            self.setProgress(100)
            return True

        except Exception as e:
            self._error = e
            return False

    def finished(self, result: bool) -> None:
        if result and self._contract_result:
            self.resultReady.emit(self._contract_result)
        elif self._error:
            self.errorOccurred.emit(str(self._error))
        else:
            self.errorOccurred.emit("Operação cancelada")
