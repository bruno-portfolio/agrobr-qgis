from __future__ import annotations

import importlib
import site
import subprocess
import sys
import threading
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DependencyStatus:
    installed: bool
    version: str | None
    message: str


class DependencyDoctor:
    REQUIRED = "agrobr"
    EXTRAS = "geo"
    _ALLOWED_PACKAGES: frozenset[str] = frozenset({"agrobr"})

    @staticmethod
    def check() -> DependencyStatus:
        try:
            mod = importlib.import_module("agrobr")
            version = getattr(mod, "__version__", "desconhecida")
            return DependencyStatus(installed=True, version=version, message="OK")
        except ImportError:
            return DependencyStatus(installed=False, version=None, message="agrobr não encontrado")

    @classmethod
    def check_version(cls) -> DependencyStatus:
        from packaging.version import Version

        from .constants import MIN_AGROBR_VERSION

        status = cls.check()
        if not status.installed or status.version is None:
            return status
        try:
            if Version(status.version) < Version(MIN_AGROBR_VERSION):
                return DependencyStatus(
                    installed=True,
                    version=status.version,
                    message=f"agrobr {status.version} desatualizado (mínimo {MIN_AGROBR_VERSION})",
                )
        except Exception:
            pass
        return status

    @classmethod
    def ensure_version(cls) -> DependencyStatus:
        status = cls.check_version()
        if status.installed and "desatualizado" in status.message:
            return cls.auto_install()
        if not status.installed:
            return cls.auto_install()
        return status

    @classmethod
    def auto_install(cls) -> DependencyStatus:
        if cls.REQUIRED not in cls._ALLOWED_PACKAGES:
            return DependencyStatus(
                installed=False,
                version=None,
                message=f"Pacote '{cls.REQUIRED}' não permitido",
            )

        try:
            subprocess.check_call(
                cls._pip_command(),
                timeout=120,
            )
            cls._refresh_imports()
            return cls.check()
        except FileNotFoundError:
            return DependencyStatus(
                installed=False,
                version=None,
                message="pip não encontrado. Instale manualmente: pip install agrobr[geo]",
            )
        except subprocess.CalledProcessError as e:
            return DependencyStatus(
                installed=False,
                version=None,
                message=f"Falha na instalação (código {e.returncode}). "
                f"Instale manualmente: pip install agrobr[geo]",
            )
        except subprocess.TimeoutExpired:
            return DependencyStatus(
                installed=False,
                version=None,
                message="Timeout na instalação. Verifique conexão e tente manualmente.",
            )

    @classmethod
    def auto_install_async(
        cls,
        callback: Callable[[DependencyStatus], None],
    ) -> None:
        def _run() -> None:
            status = cls.auto_install()
            callback(status)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()

    @classmethod
    def _pip_command(cls) -> list[str]:
        from .constants import MIN_AGROBR_VERSION

        return [
            cls._python_path(),
            "-m",
            "pip",
            "install",
            f"{cls.REQUIRED}[{cls.EXTRAS}]>={MIN_AGROBR_VERSION}",
            "--upgrade",
            "--user",
            "--quiet",
        ]

    @staticmethod
    def _python_path() -> str:
        if "python" in sys.executable.lower():
            return sys.executable
        import shutil

        for name in ("python3", "python"):
            path = shutil.which(name)
            if path:
                return path
        return sys.executable

    @staticmethod
    def _refresh_imports() -> None:
        user_site = site.getusersitepackages()
        if user_site not in sys.path:
            sys.path.insert(0, user_site)
        importlib.invalidate_caches()
