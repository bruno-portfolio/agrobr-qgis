from __future__ import annotations

import pandas as pd

__all__ = ["make_bcb_df"]

_DATA = {
    "data": pd.to_datetime(
        [
            "2026-03-20",
            "2026-03-20",
            "2026-03-21",
            "2026-03-21",
            "2026-03-24",
            "2026-03-24",
            "2026-03-25",
            "2026-03-25",
            "2026-03-26",
            "2026-03-26",
        ]
    ),
    "moeda": ["USD"] * 10,
    "tipo": [
        "Compra",
        "Venda",
        "Compra",
        "Venda",
        "Compra",
        "Venda",
        "Compra",
        "Venda",
        "Compra",
        "Venda",
    ],
    "cotacao": [
        5.05,
        5.07,
        5.03,
        5.05,
        5.08,
        5.10,
        5.06,
        5.08,
        5.04,
        5.06,
    ],
}


def make_bcb_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)
