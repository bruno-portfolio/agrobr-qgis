from __future__ import annotations

import importlib
import subprocess
import sys
from unittest.mock import MagicMock

import pytest

from agrobr_qgis.core.dependency_doctor import DependencyDoctor


class TestDependencyDoctorCheck:
    def test_check_installed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "1.0.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        status = DependencyDoctor.check()
        assert status.installed is True
        assert status.version == "1.0.0"
        assert status.message == "OK"

    def test_check_absent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        original = importlib.import_module

        def _raise_for_agrobr(name: str, *args: object, **kwargs: object) -> object:
            if name == "agrobr":
                raise ImportError("mocked")
            return original(name, *args, **kwargs)

        monkeypatch.setattr(importlib, "import_module", _raise_for_agrobr)
        status = DependencyDoctor.check()
        assert status.installed is False
        assert status.version is None
        assert "não encontrado" in status.message


class TestDependencyDoctorAutoInstall:
    def test_allowlist_rejects_unknown(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(DependencyDoctor, "REQUIRED", "evil-package")
        result = DependencyDoctor.auto_install()
        assert result.installed is False
        assert "não permitido" in result.message

    def test_pip_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _raise_fnf(*_args: object, **_kwargs: object) -> None:
            raise FileNotFoundError

        monkeypatch.setattr(subprocess, "check_call", _raise_fnf)
        result = DependencyDoctor.auto_install()
        assert result.installed is False
        assert "pip não encontrado" in result.message

    def test_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _raise_timeout(*_args: object, **_kwargs: object) -> None:
            raise subprocess.TimeoutExpired(cmd="pip", timeout=120)

        monkeypatch.setattr(subprocess, "check_call", _raise_timeout)
        result = DependencyDoctor.auto_install()
        assert result.installed is False
        assert "Timeout" in result.message

    def test_called_process_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _raise_cpe(*_args: object, **_kwargs: object) -> None:
            raise subprocess.CalledProcessError(returncode=1, cmd="pip")

        monkeypatch.setattr(subprocess, "check_call", _raise_cpe)
        result = DependencyDoctor.auto_install()
        assert result.installed is False
        assert "código 1" in result.message
