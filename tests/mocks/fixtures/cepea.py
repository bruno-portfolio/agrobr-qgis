from __future__ import annotations

import pandas as pd

__all__ = ["make_cepea_df"]

_DATA = {
    "data": pd.to_datetime(
        [
            "2026-03-20",
            "2026-03-20",
            "2026-03-20",
            "2026-03-21",
            "2026-03-21",
            "2026-03-21",
            "2026-03-24",
            "2026-03-24",
            "2026-03-25",
            "2026-03-25",
        ]
    ),
    "produto": [
        "Soja",
        "Boi Gordo",
        "Café",
        "Soja",
        "Boi Gordo",
        "Café",
        "Milho",
        "Etanol",
        "Soja",
        "Boi Gordo",
    ],
    "praca": [
        "Paranaguá",
        "SP",
        "SP",
        "Paranaguá",
        "SP",
        "SP",
        "Campinas",
        "SP",
        "Paranaguá",
        "SP",
    ],
    "valor": [
        138.50,
        312.75,
        1245.00,
        139.20,
        314.10,
        1248.50,
        72.30,
        2.85,
        140.00,
        315.50,
    ],
    "variacao": [
        0.32,
        -0.15,
        1.20,
        0.51,
        0.43,
        0.28,
        -0.68,
        0.71,
        0.57,
        0.45,
    ],
}


def make_cepea_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)
