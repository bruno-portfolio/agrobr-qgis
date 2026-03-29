from __future__ import annotations

import unicodedata

import pandas as pd
import pytest

from agrobr_qgis.core.data_contract import DataContract


@pytest.mark.edge
class TestEncoding:
    def test_nfd_column_normalized_to_nfc(self) -> None:
        nfd_col = unicodedata.normalize("NFD", "município")
        nfc_col = unicodedata.normalize("NFC", "município")
        assert nfd_col != nfc_col

        df = pd.DataFrame({nfd_col: ["Brasilia", "Goiania"]})
        result = DataContract.validate(df)

        assert nfc_col in result.df.columns
        assert nfd_col not in result.df.columns

    def test_nfc_values_normalized(self) -> None:
        nfd_value = unicodedata.normalize("NFD", "São Paulo")
        nfc_value = unicodedata.normalize("NFC", "São Paulo")
        assert nfd_value != nfc_value

        df = pd.DataFrame({"cidade": [nfd_value, nfd_value]})
        result = DataContract.validate(df)

        for val in result.df["cidade"]:
            assert val == nfc_value
            assert unicodedata.is_normalized("NFC", val)

    def test_mixed_encoding_in_column_values(self) -> None:
        nfd = unicodedata.normalize("NFD", "produção")
        nfc = unicodedata.normalize("NFC", "produção")
        assert nfd != nfc

        df = pd.DataFrame({"tipo": [nfc, nfd, nfc, nfd]})
        result = DataContract.validate(df)

        for val in result.df["tipo"]:
            assert unicodedata.is_normalized("NFC", val)
            assert val == nfc

    def test_non_ascii_column_names(self) -> None:
        df = pd.DataFrame(
            {
                "município": ["Uberaba", "Uberlandia"],
                "produção": [1000, 2000],
                "área_ha": [500.0, 700.0],
            }
        )
        result = DataContract.validate(df)

        assert "município" in result.df.columns
        assert "produção" in result.df.columns
        assert "área_ha" in result.df.columns
        assert result.row_count == 2
        assert result.col_count == 3
