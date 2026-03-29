from __future__ import annotations

from unittest.mock import MagicMock


class TestStubLifecycle:
    def test_stub_shows_warning(self, mock_qgis_full: MagicMock, mock_iface: MagicMock) -> None:
        from agrobr_qgis import agrobrStub

        stub = agrobrStub(mock_iface)
        stub.initGui()

        mock_qgis_full.QMessageBox.warning.assert_called_once()
        call_args = mock_qgis_full.QMessageBox.warning.call_args
        assert "agrobr" in call_args[0][2].lower()

        mock_iface.messageBar().pushMessage.assert_called_once()

    def test_stub_no_dock_no_actions(
        self, mock_qgis_full: MagicMock, mock_iface: MagicMock
    ) -> None:
        _ = mock_qgis_full
        from agrobr_qgis import agrobrStub

        stub = agrobrStub(mock_iface)
        stub.initGui()
        stub.unload()

        mock_iface.addDockWidget.assert_not_called()
        mock_iface.addToolBarIcon.assert_not_called()
