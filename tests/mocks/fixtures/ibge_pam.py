from __future__ import annotations

import pandas as pd

__all__ = ["make_ibge_pam_df"]

_DATA = {
    "produto": [
        "Soja",
        "Milho",
        "Cana-de-açúcar",
        "Café",
        "Laranja",
        "Arroz",
        "Feijão",
        "Algodão herbáceo",
        "Mandioca",
        "Banana",
    ],
    "ano": [2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025],
    "valor_producao": [
        285000.0,
        98500.0,
        72300.0,
        45200.0,
        18700.0,
        12400.0,
        8900.0,
        21300.0,
        6800.0,
        9100.0,
    ],
    "area_colhida": [
        45800.0,
        22100.0,
        8400.0,
        1850.0,
        560.0,
        1620.0,
        2780.0,
        1690.0,
        1120.0,
        470.0,
    ],
    "codigo_municipio": [
        "5103403",
        "4106902",
        "3548500",
        "3170701",
        "3549805",
        "4300604",
        "3136702",
        "2904902",
        "1500602",
        "2919553",
    ],
    "municipio": [
        "Sorriso",
        "Cascavel",
        "Ribeirão Preto",
        "Patrocínio",
        "São José do Rio Preto",
        "Alegrete",
        "Unaí",
        "Barreiras",
        "Acará",
        "Bom Jesus da Lapa",
    ],
}


def make_ibge_pam_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)
