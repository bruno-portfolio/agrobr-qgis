# agrobr QGIS Plugin
# Copyright (C) 2026 Bruno
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from typing import Any


class agrobrStub:
    def __init__(self, iface: Any) -> None:
        self.iface = iface

    def initGui(self) -> None:  # noqa: N802
        from qgis.PyQt.QtWidgets import QMessageBox  # type: ignore[import-untyped]

        from .core.logger import Logger

        Logger(self.iface).error("agrobr não encontrado. Instale com: pip install agrobr[geo]")
        QMessageBox.warning(
            None,
            "agrobr",
            "A biblioteca agrobr não está instalada.\n\nInstale com:\n  pip install agrobr[geo]",
        )

    def unload(self) -> None:
        pass


def classFactory(iface: Any) -> Any:  # noqa: N802
    from .core.dependency_doctor import DependencyDoctor

    status = DependencyDoctor.check()
    if not status.installed:
        return agrobrStub(iface)

    from .plugin import agrobrPlugin

    return agrobrPlugin(iface)
