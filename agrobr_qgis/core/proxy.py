from __future__ import annotations

import os
from urllib.parse import quote


def propagate_proxy() -> None:
    from qgis.core import QgsSettings  # type: ignore[import-untyped]

    settings = QgsSettings()
    if not settings.value("proxy/proxyEnabled", False, type=bool):
        return

    host: str = settings.value("proxy/proxyHost", "", type=str)
    if not host:
        return

    port: str = settings.value("proxy/proxyPort", "", type=str)
    user: str = settings.value("proxy/proxyUser", "", type=str)
    password: str = settings.value("proxy/proxyPassword", "", type=str)

    auth = ""
    if user:
        auth = quote(user, safe="")
        if password:
            auth += ":" + quote(password, safe="")
        auth += "@"

    url = f"http://{auth}{host}"
    if port and port != "0":
        url += f":{port}"

    if "HTTP_PROXY" not in os.environ:
        os.environ["HTTP_PROXY"] = url
    if "HTTPS_PROXY" not in os.environ:
        os.environ["HTTPS_PROXY"] = url
