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
        return [
            sys.executable,
            "-m",
            "pip",
            "install",
            f"{cls.REQUIRED}[{cls.EXTRAS}]",
            "--user",
            "--quiet",
        ]

    @staticmethod
    def _refresh_imports() -> None:
        user_site = site.getusersitepackages()
        if user_site not in sys.path:
            sys.path.insert(0, user_site)
        importlib.invalidate_caches()
