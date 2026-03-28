from __future__ import annotations

from typing import Any


class Logger:
    TAG = "AgroBR"

    def __init__(self, iface: Any = None) -> None:
        self._iface = iface

    def user(self, msg: str, level: Any = None, duration: int = 5) -> None:
        if self._iface:
            if level is None:
                from qgis.core import Qgis

                level = Qgis.MessageLevel.Info
            self._iface.messageBar().pushMessage(self.TAG, msg, level, duration)

    def audit(self, msg: str) -> None:
        from qgis.core import Qgis, QgsMessageLog

        QgsMessageLog.logMessage(msg, self.TAG, Qgis.MessageLevel.Info)

    def debug(self, msg: str) -> None:
        from qgis.core import Qgis, QgsMessageLog

        QgsMessageLog.logMessage(msg, self.TAG, Qgis.MessageLevel.Warning)

    def error(self, msg: str) -> None:
        from qgis.core import Qgis, QgsMessageLog

        QgsMessageLog.logMessage(msg, self.TAG, Qgis.MessageLevel.Critical)
        if self._iface:
            self._iface.messageBar().pushMessage(
                self.TAG, msg, Qgis.MessageLevel.Critical, duration=0
            )
