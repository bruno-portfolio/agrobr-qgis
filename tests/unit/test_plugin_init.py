from __future__ import annotations

import importlib
import sys
from unittest.mock import MagicMock

import pytest


class TestClassFactory:
    def test_with_agrobr_returns_plugin(
        self, mock_qgis_full: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _ = mock_qgis_full
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "1.0.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)

        from agrobr_qgis import classFactory

        result = classFactory(MagicMock())
        assert type(result).__name__ == "agrobrPlugin"

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

    def test_stub_unload_no_raise(self, mock_iface: MagicMock) -> None:
        from agrobr_qgis import agrobrStub

        stub = agrobrStub(mock_iface)
        stub.unload()
