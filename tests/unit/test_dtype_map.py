from __future__ import annotations

import pytest

from agrobr_qgis.core.constants import DTYPE_FALLBACK, DTYPE_MAP


class TestDtypeMap:
    @pytest.mark.parametrize("dtype", list(DTYPE_MAP.keys()))
    def test_all_dtypes_resolve(self, dtype: str) -> None:
        assert dtype in DTYPE_MAP
        assert isinstance(DTYPE_MAP[dtype], str)

    def test_unknown_dtype_falls_back(self) -> None:
        assert DTYPE_MAP.get("unknown_dtype_xyz", DTYPE_FALLBACK) == DTYPE_FALLBACK

    def test_dtype_fallback_is_string(self) -> None:
        assert DTYPE_FALLBACK == "String"

    def test_nullable_int_maps_same_as_int(self) -> None:
        assert DTYPE_MAP["Int64"] == DTYPE_MAP["int64"]
        assert DTYPE_MAP["Int32"] == DTYPE_MAP["int32"]

    @pytest.mark.parametrize("dtype", list(DTYPE_MAP.keys()))
    def test_all_values_are_nonempty_capitalized_strings(self, dtype: str) -> None:
        value = DTYPE_MAP[dtype]
        assert len(value) > 0
        assert value[0].isupper()
