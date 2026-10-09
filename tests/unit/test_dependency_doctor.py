from __future__ import annotations

import importlib
import subprocess
import sys
import threading
from importlib import metadata
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
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in result.message

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
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in result.message


class TestCheckVersion:
    @pytest.mark.parametrize("version", ["3.0.0", "3.0.0rc1", "4.1.0"])
    def test_check_version_next_major_incompatible(
        self, monkeypatch: pytest.MonkeyPatch, version: str
    ) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = version
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        status = DependencyDoctor.check_version()
        assert status.installed is True
        assert status.version == version
        assert status.compatible is False
        assert status.needs_major_upgrade is False
        assert "usa a agrobr 2.x" in status.message
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in status.message

    @pytest.mark.parametrize("version", ["1.1.0", "1.0.5", "0.9.0"])
    def test_check_version_previous_major_needs_upgrade(
        self, monkeypatch: pytest.MonkeyPatch, version: str
    ) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = version
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        status = DependencyDoctor.check_version()
        assert status.compatible is False
        assert status.needs_major_upgrade is True
        assert f"agrobr {version} instalada" in status.message
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in status.message
        assert "plugin agrobr 0.1.x" in status.message

    def test_check_version_supported_major(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "2.0.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        status = DependencyDoctor.check_version()
        assert status.compatible is True
        assert status.needs_major_upgrade is False
        assert status.message == "OK"

    def test_check_version_below_minimum(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "2.0.0rc1"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        status = DependencyDoctor.check_version()
        assert status.compatible is True
        assert "desatualizado" in status.message


class TestEnsureVersion:
    @pytest.mark.parametrize("version", ["3.0.0", "1.1.0"])
    def test_ensure_version_other_major_does_not_install(
        self, monkeypatch: pytest.MonkeyPatch, version: str
    ) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = version
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        calls: list[object] = []
        monkeypatch.setattr(subprocess, "check_call", lambda *a, **_kw: calls.append(a))
        status = DependencyDoctor.ensure_version()
        assert calls == []
        assert status.compatible is False
        assert status.version == version


class TestUpgradeMajor:
    def test_upgrade_major_reports_installed_distribution(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "1.1.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        calls: list[object] = []
        monkeypatch.setattr(subprocess, "check_call", lambda *a, **_kw: calls.append(a))
        monkeypatch.setattr(metadata, "version", lambda _name: "2.0.1")
        status = DependencyDoctor.upgrade_major("1.1.0")
        assert len(calls) == 1
        assert status.version == "2.0.1"
        assert status.compatible is False
        assert "agrobr atualizada de 1.1.0 para 2.0.1" in status.message
        assert "Reinicie o QGIS" in status.message

    def test_upgrade_major_unconfirmed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "1.1.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        monkeypatch.setattr(subprocess, "check_call", lambda *_a, **_kw: None)
        monkeypatch.setattr(metadata, "version", lambda _name: "1.1.0")
        status = DependencyDoctor.upgrade_major("1.1.0")
        assert status.compatible is False
        assert "não pôde ser confirmada" in status.message
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in status.message

    def test_upgrade_major_pip_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _raise_cpe(*_args: object, **_kwargs: object) -> None:
            raise subprocess.CalledProcessError(returncode=1, cmd="pip")

        monkeypatch.setattr(subprocess, "check_call", _raise_cpe)
        status = DependencyDoctor.upgrade_major("1.1.0")
        assert status.installed is False
        assert "código 1" in status.message
        assert 'pip install "agrobr[geo]>=2.0.0,<3"' in status.message


class TestAutoInstallAsync:
    def test_callback_receives_status(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_agrobr = MagicMock()
        mock_agrobr.__version__ = "1.0.0"
        monkeypatch.setitem(sys.modules, "agrobr", mock_agrobr)
        monkeypatch.setattr(subprocess, "check_call", lambda *_a, **_kw: None)

        received: list[object] = []
        done = threading.Event()

        def _cb(status: object) -> None:
            received.append(status)
            done.set()

        DependencyDoctor.auto_install_async(_cb)
        assert done.wait(timeout=5)
        assert len(received) == 1
        assert received[0].installed is True  # type: ignore[union-attr]


class TestPipCommand:
    def test_contains_package_and_extras(self) -> None:
        cmd = DependencyDoctor._pip_command()
        pkg_arg = [c for c in cmd if "agrobr[geo]" in c]
        assert len(pkg_arg) == 1
        assert "--user" in cmd
        assert "--quiet" in cmd
        assert "--upgrade" in cmd

    def test_caps_supported_major(self) -> None:
        cmd = DependencyDoctor._pip_command()
        assert "agrobr[geo]>=2.0.0,<3" in cmd
