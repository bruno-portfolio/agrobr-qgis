from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def mock_qgis(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock_core = MagicMock()
    mock_core.Qgis.MessageLevel.Info = 0
    mock_core.Qgis.MessageLevel.Warning = 1
    mock_core.Qgis.MessageLevel.Critical = 2
    monkeypatch.setitem(sys.modules, "qgis", MagicMock())
    monkeypatch.setitem(sys.modules, "qgis.core", mock_core)
    return mock_core


class TestLogger:
    def test_user_without_iface_no_error(self) -> None:
        from agrobr_qgis.core.logger import Logger

        Logger().user("nenhum erro aqui")

    def test_user_with_iface_calls_message_bar(self, mock_qgis: MagicMock) -> None:
        from agrobr_qgis.core.logger import Logger

        _ = mock_qgis
        mock_iface = MagicMock()
        Logger(iface=mock_iface).user("teste")
        mock_iface.messageBar().pushMessage.assert_called_once_with("agrobr", "teste", 0, 5)

    def test_error_with_iface_calls_message_bar_critical(self, mock_qgis: MagicMock) -> None:
        from agrobr_qgis.core.logger import Logger

        mock_iface = MagicMock()
        Logger(iface=mock_iface).error("falha")
        mock_qgis.QgsMessageLog.logMessage.assert_called_once_with("falha", "agrobr", 2)
        mock_iface.messageBar().pushMessage.assert_called_once_with(
            "agrobr", "falha", 2, duration=0
        )

    def test_error_without_iface_logs_only(self, mock_qgis: MagicMock) -> None:
        from agrobr_qgis.core.logger import Logger

        Logger().error("falha sem iface")
        mock_qgis.QgsMessageLog.logMessage.assert_called_once_with("falha sem iface", "agrobr", 2)

    def test_audit_calls_log_message_info(self, mock_qgis: MagicMock) -> None:
        from agrobr_qgis.core.logger import Logger

        Logger().audit("operacao registrada")
        mock_qgis.QgsMessageLog.logMessage.assert_called_once_with(
            "operacao registrada", "agrobr", 0
        )

    def test_debug_uses_info_level(self, mock_qgis: MagicMock) -> None:
        from agrobr_qgis.core.logger import Logger

        Logger().debug("detalhe interno")
        mock_qgis.QgsMessageLog.logMessage.assert_called_once_with("detalhe interno", "agrobr", 0)
