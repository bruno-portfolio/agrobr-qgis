from __future__ import annotations

import pandas as pd

__all__ = ["make_conab_safras_df"]

_DATA = {
    "produto": [
        "Soja",
        "Milho",
        "Arroz",
        "Feijão",
        "Algodão",
        "Soja",
        "Milho",
        "Trigo",
        "Café",
        "Cana-de-açúcar",
    ],
    "safra": [
        "2025/26",
        "2025/26",
        "2025/26",
        "2025/26",
        "2025/26",
        "2024/25",
        "2024/25",
        "2025/26",
        "2025/26",
        "2025/26",
    ],
    "area_plantada": [
        46200.0,
        22800.0,
        1650.0,
        2890.0,
        1780.0,
        45100.0,
        21500.0,
        3100.0,
        1920.0,
        8500.0,
    ],
    "producao": [
        168500.0,
        130200.0,
        10800.0,
        3050.0,
        3520.0,
        155300.0,
        119800.0,
        10500.0,
        3480.0,
        620000.0,
    ],
    "produtividade": [
        3647.0,
        5710.0,
        6545.0,
        1055.0,
        1978.0,
        3443.0,
        5572.0,
        3387.0,
        1812.0,
        72941.0,
    ],
    "uf": ["MT", "PR", "RS", "MG", "BA", "MT", "GO", "RS", "MG", "SP"],
}


def make_conab_safras_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)
