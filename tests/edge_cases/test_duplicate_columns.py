from __future__ import annotations

import unicodedata

import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import DataContract


@pytest.mark.edge
class TestDuplicateColumns:
    def test_triple_duplicate_renamed(self) -> None:
        df = pd.DataFrame([[10, 20, 30]], columns=["a", "a", "a"])
        result = DataContract.validate(df)

        cols = list(result.df.columns)
        assert cols == ["a", "a_1", "a_2"]
        assert any("duplicadas" in w for w in result.warnings)
        assert result.col_count == 3

    def test_duplicate_after_nfc(self) -> None:
        nfd_col = unicodedata.normalize("NFD", "produção")
        nfc_col = unicodedata.normalize("NFC", "produção")
        assert nfd_col != nfc_col
        assert unicodedata.normalize("NFC", nfd_col) == nfc_col

        df = pd.DataFrame({nfd_col: [100], nfc_col: [200]})
        result = DataContract.validate(df)

        assert any("duplicadas" in w for w in result.warnings)
        cols = list(result.df.columns)
        assert len(cols) == len(set(cols))

    def test_no_duplicates_untouched(self) -> None:
        df = pd.DataFrame({"municipio": ["Goiania"], "uf": ["GO"], "valor": [42.0]})
        result = DataContract.validate(df)

        cols = list(result.df.columns)
        assert cols == ["municipio", "uf", "valor"]
        assert not any("duplicadas" in w for w in result.warnings)
