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
    compatible: bool = True
    needs_major_upgrade: bool = False


class DependencyDoctor:
    REQUIRED = "agrobr"
    EXTRAS = "geo"
    _ALLOWED_PACKAGES: frozenset[str] = frozenset({"agrobr"})

    @classmethod
    def requirement(cls) -> str:
        from .constants import MIN_AGROBR_VERSION, SUPPORTED_AGROBR_MAJOR

        return f"{cls.REQUIRED}[{cls.EXTRAS}]>={MIN_AGROBR_VERSION},<{SUPPORTED_AGROBR_MAJOR + 1}"

    @classmethod
    def manual_install_hint(cls) -> str:
        return f'pip install "{cls.requirement()}"'

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

        from .constants import MIN_AGROBR_VERSION, SUPPORTED_AGROBR_MAJOR

        status = cls.check()
        if not status.installed or status.version is None:
            return status
        try:
            if Version(status.version).major > SUPPORTED_AGROBR_MAJOR:
                return DependencyStatus(
                    installed=True,
                    version=status.version,
                    message=f"agrobr {status.version} não é compatível com esta versão do "
                    f"plugin, que usa a agrobr {SUPPORTED_AGROBR_MAJOR}.x. Atualize o plugin "
                    f"agrobr no gerenciador de plugins do QGIS ou instale a agrobr "
                    f"{SUPPORTED_AGROBR_MAJOR}.x: {cls.manual_install_hint()}",
                    compatible=False,
                )
            if Version(status.version).major < SUPPORTED_AGROBR_MAJOR:
                return DependencyStatus(
                    installed=True,
                    version=status.version,
                    message=f"agrobr {status.version} instalada; este plugin usa a agrobr "
                    f"{SUPPORTED_AGROBR_MAJOR}.x. Atualize com {cls.manual_install_hint()} e "
                    f"reinicie o QGIS, ou volte ao plugin agrobr 0.1.x, que usa a agrobr 1.x.",
                    compatible=False,
                    needs_major_upgrade=True,
                )
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
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.check_call(
                cls._pip_command(),
                timeout=120,
                startupinfo=startupinfo,
            )
            cls._refresh_imports()
            return cls.check()
        except FileNotFoundError:
            return DependencyStatus(
                installed=False,
                version=None,
                message=f"pip não encontrado. Instale manualmente: {cls.manual_install_hint()}",
            )
        except subprocess.CalledProcessError as e:
            return DependencyStatus(
                installed=False,
                version=None,
                message=f"Falha na instalação (código {e.returncode}). "
                f"Instale manualmente: {cls.manual_install_hint()}",
            )
        except subprocess.TimeoutExpired:
            return DependencyStatus(
                installed=False,
                version=None,
                message="Timeout na instalação. Verifique conexão e tente manualmente.",
            )

    @classmethod
    def upgrade_major(cls, installed_version: str | None) -> DependencyStatus:
        """Instala a major suportada sobre uma anterior já importada neste processo.

        O módulo antigo fica em ``sys.modules`` até o QGIS reiniciar; por isso a versão nova vem
        dos metadados da distribuição instalada, e não de ``agrobr.__version__``.
        """
        from importlib import metadata

        from packaging.version import Version

        from .constants import SUPPORTED_AGROBR_MAJOR

        status = cls.auto_install()
        if not status.installed:
            return status
        try:
            new_version = metadata.version(cls.REQUIRED)
        except metadata.PackageNotFoundError:
            new_version = None
        if new_version is None or Version(new_version).major != SUPPORTED_AGROBR_MAJOR:
            return DependencyStatus(
                installed=True,
                version=installed_version,
                message=f"A atualização da agrobr não pôde ser confirmada. Instale manualmente: "
                f"{cls.manual_install_hint()}",
                compatible=False,
            )
        return DependencyStatus(
            installed=True,
            version=new_version,
            message=f"agrobr atualizada de {installed_version} para {new_version}. "
            f"Reinicie o QGIS para usar o plugin.",
            compatible=False,
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
            cls._python_path(),
            "-m",
            "pip",
            "install",
            cls.requirement(),
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
