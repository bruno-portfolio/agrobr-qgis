from __future__ import annotations

import importlib
import subprocess
import sys
from importlib import metadata
from unittest.mock import MagicMock

import pytest


class TestClassFactory:
    def test_with_agrobr_returns_plugin(
        self, mock_qgis_full: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _ = mock_qgis_full
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "2.0.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)

        from agrobr_qgis import classFactory

        result = classFactory(MagicMock())
        assert type(result).__name__ == "agrobrPlugin"

    def test_with_agrobr_next_major_returns_stub_without_install(
        self, mock_qgis_full: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _ = mock_qgis_full
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "3.0.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        calls: list[object] = []
        monkeypatch.setattr(subprocess, "check_call", lambda *a, **_kw: calls.append(a))

        from agrobr_qgis import agrobrStub, classFactory

        result = classFactory(MagicMock())
        assert isinstance(result, agrobrStub)
        assert result.message is not None
        assert "agrobr 3.0.0 não é compatível" in result.message
        assert calls == []
        mock_qgis_full.QMessageBox.question.assert_not_called()

    def test_without_agrobr_returns_stub(
        self, mock_qgis_full: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _ = mock_qgis_full
        original = importlib.import_module

        def _raise_for_agrobr(name: str, *args: object, **kwargs: object) -> object:
            if name == "agrobr":
                raise ImportError("mocked")
            return original(name, *args, **kwargs)

        monkeypatch.setattr(importlib, "import_module", _raise_for_agrobr)

        from agrobr_qgis import agrobrStub, classFactory

        result = classFactory(MagicMock())
        assert isinstance(result, agrobrStub)

    def test_stub_initgui_no_raise(self, mock_qgis_full: MagicMock, mock_iface: MagicMock) -> None:
        _ = mock_qgis_full
        from agrobr_qgis import agrobrStub

        stub = agrobrStub(mock_iface)
        stub.initGui()

    def test_stub_initgui_default_message_caps_major(
        self, mock_qgis_full: MagicMock, mock_iface: MagicMock
    ) -> None:
        from agrobr_qgis import agrobrStub

        agrobrStub(mock_iface).initGui()
        message = mock_qgis_full.QMessageBox.warning.call_args.args[2]
        assert "não está instalada" in message
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in message

    def test_stub_initgui_shows_given_message(
        self, mock_qgis_full: MagicMock, mock_iface: MagicMock
    ) -> None:
        from agrobr_qgis import agrobrStub

        agrobrStub(mock_iface, "agrobr 2.0.0 não é compatível").initGui()
        mock_qgis_full.QMessageBox.warning.assert_called_once_with(
            None, "agrobr", "agrobr 2.0.0 não é compatível"
        )

    def test_stub_unload_no_raise(self, mock_iface: MagicMock) -> None:
        from agrobr_qgis import agrobrStub

        stub = agrobrStub(mock_iface)
        stub.unload()


class TestMajorUpgradeOffer:
    @pytest.fixture()
    def agrobr_1x(self, monkeypatch: pytest.MonkeyPatch) -> list[object]:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "1.1.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        calls: list[object] = []
        monkeypatch.setattr(subprocess, "check_call", lambda *a, **_kw: calls.append(a))
        monkeypatch.setattr(metadata, "version", lambda _name: "2.0.0")
        return calls

    def test_major_upgrade_accepted(
        self, mock_qgis_full: MagicMock, agrobr_1x: list[object]
    ) -> None:
        box = mock_qgis_full.QMessageBox
        box.question.return_value = box.StandardButton.Yes

        from agrobr_qgis import agrobrStub, classFactory

        iface = MagicMock()
        result = classFactory(iface)
        assert isinstance(result, agrobrStub)
        assert result.message == (
            "agrobr atualizada de 1.1.0 para 2.0.0. Reinicie o QGIS para usar o plugin."
        )
        assert len(agrobr_1x) == 1
        parent, title, text, _buttons = box.question.call_args.args
        assert parent is iface.mainWindow()
        assert title == "agrobr"
        assert "usa a agrobr 2.x; a instalada é a 1.1.0" in text
        assert "Outros programas" in text

    def test_major_upgrade_declined(
        self, mock_qgis_full: MagicMock, agrobr_1x: list[object]
    ) -> None:
        box = mock_qgis_full.QMessageBox
        box.question.return_value = box.StandardButton.No

        from agrobr_qgis import agrobrStub, classFactory

        result = classFactory(MagicMock())
        assert isinstance(result, agrobrStub)
        assert result.message is not None
        assert agrobr_1x == []
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in result.message
        assert "plugin agrobr 0.1.x" in result.message

    def test_major_upgrade_pip_failure(
        self, mock_qgis_full: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "1.1.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)

        def _raise_cpe(*_args: object, **_kwargs: object) -> None:
            raise subprocess.CalledProcessError(returncode=1, cmd="pip")

        monkeypatch.setattr(subprocess, "check_call", _raise_cpe)
        box = mock_qgis_full.QMessageBox
        box.question.return_value = box.StandardButton.Yes

        from agrobr_qgis import agrobrStub, classFactory

        result = classFactory(MagicMock())
        assert isinstance(result, agrobrStub)
        assert result.message is not None
        assert "Falha na instalação (código 1)" in result.message
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in result.message
