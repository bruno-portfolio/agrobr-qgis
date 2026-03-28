from __future__ import annotations

import pandas as pd

__all__ = ["make_zarc_df"]

_DATA = {
    "cultura": [
        "Soja",
        "Soja",
        "Milho",
        "Milho",
        "Arroz",
        "Feijão",
        "Feijão",
        "Trigo",
        "Soja",
        "Milho",
    ],
    "municipio": [
        "Sorriso",
        "Londrina",
        "Cascavel",
        "Rio Verde",
        "Alegrete",
        "Unaí",
        "Irecê",
        "Passo Fundo",
        "Dourados",
        "Jataí",
    ],
    "codigo_municipio": [
        "5107925",
        "4113700",
        "4106902",
        "5218805",
        "4300604",
        "3170404",
        "2914109",
        "4314100",
        "5003702",
        "5211909",
    ],
    "solo": [
        "Tipo 1",
        "Tipo 2",
        "Tipo 3",
        "Tipo 1",
        "Tipo 2",
        "Tipo 3",
        "Tipo 1",
        "Tipo 2",
        "Tipo 3",
        "Tipo 1",
    ],
    "risco": [
        "Baixo",
        "Baixo",
        "Médio",
        "Baixo",
        "Médio",
        "Alto",
        "Alto",
        "Médio",
        "Baixo",
        "Baixo",
    ],
    "ciclo": [
        "Precoce",
        "Médio",
        "Tardio",
        "Precoce",
        "Médio",
        "Precoce",
        "Médio",
        "Tardio",
        "Precoce",
        "Médio",
    ],
}


def make_zarc_df() -> pd.DataFrame:
    return pd.DataFrame(_DATA)
