# agrobr QGIS Plugin
# Copyright (C) 2026 Bruno
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .core.dependency_doctor import DependencyStatus


class agrobrStub:
    def __init__(self, iface: Any, message: str | None = None) -> None:
        self.iface = iface
        self.message = message

    def initGui(self) -> None:  # noqa: N802
        from qgis.PyQt.QtWidgets import QMessageBox  # type: ignore[import-untyped]

        from .core.dependency_doctor import DependencyDoctor
        from .core.logger import Logger

        message = self.message or (
            "A biblioteca agrobr não está instalada. "
            f"Instale com: {DependencyDoctor.manual_install_hint()}"
        )
        Logger(self.iface).error(message)
        QMessageBox.warning(None, "agrobr", message)

    def unload(self) -> None:
        pass


def _offer_major_upgrade(iface: Any, status: DependencyStatus) -> str:
    from qgis.PyQt.QtWidgets import QMessageBox  # type: ignore[import-untyped]

    from .core.constants import SUPPORTED_AGROBR_MAJOR
    from .core.dependency_doctor import DependencyDoctor

    answer = QMessageBox.question(
        iface.mainWindow(),
        "agrobr",
        f"Este plugin usa a agrobr {SUPPORTED_AGROBR_MAJOR}.x; a instalada é a {status.version}. "
        f"Atualizar agora? Outros programas que usam a agrobr neste Python passam a usar a "
        f"{SUPPORTED_AGROBR_MAJOR}.x.",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if answer != QMessageBox.StandardButton.Yes:
        return status.message
    return DependencyDoctor.upgrade_major(status.version).message


def classFactory(iface: Any) -> Any:  # noqa: N802
    from .core.dependency_doctor import DependencyDoctor

    status = DependencyDoctor.check()
    if not status.installed:
        status = DependencyDoctor.auto_install()
        if not status.installed:
            return agrobrStub(iface)

    version_status = DependencyDoctor.check_version()
    if version_status.needs_major_upgrade:
        return agrobrStub(iface, _offer_major_upgrade(iface, version_status))
    if not version_status.compatible:
        return agrobrStub(iface, version_status.message)
    if "desatualizado" in version_status.message:
        DependencyDoctor.auto_install_async(lambda _: None)

    from .plugin import agrobrPlugin

    return agrobrPlugin(iface)
