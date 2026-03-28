from __future__ import annotations

from agrobr_qgis.core.source_adapter import ParamType
from agrobr_qgis.processing.algorithms._factory import PARAM_MAP, UF_LIST


class TestParamMap:
    def test_all_param_types_mapped(self) -> None:
        for pt in ParamType:
            assert pt in PARAM_MAP, f"ParamType.{pt.name} not in PARAM_MAP"

    def test_no_extra_keys(self) -> None:
        for key in PARAM_MAP:
            assert isinstance(key, ParamType), f"Unknown key in PARAM_MAP: {key}"

    def test_all_values_are_strings(self) -> None:
        for pt, cls_name in PARAM_MAP.items():
            assert isinstance(cls_name, str), f"PARAM_MAP[{pt}] is not a string"

    def test_dynamic_types_fallback_to_string(self) -> None:
        dynamic_types = [ParamType.CHOICE_DYNAMIC, ParamType.MULTI_CHOICE, ParamType.PRODUTO]
        for pt in dynamic_types:
            assert PARAM_MAP[pt] == "QgsProcessingParameterString"


class TestUfList:
    def test_27_ufs(self) -> None:
        assert len(UF_LIST) == 27

    def test_sorted(self) -> None:
        assert sorted(UF_LIST) == UF_LIST

    def test_all_two_chars(self) -> None:
        for uf in UF_LIST:
            assert len(uf) == 2
