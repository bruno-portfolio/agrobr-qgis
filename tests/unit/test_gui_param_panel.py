from __future__ import annotations

from unittest.mock import MagicMock

from agrobr_qgis.core.source_adapter import ParamType, SourceParameter


class _SpinBox:
    def __init__(self, value: int) -> None:
        self._value = value

    def value(self) -> int:
        return self._value


class _Unused:
    pass


def test_collect_params_omits_unset_optional_int(mock_qgis_full: MagicMock) -> None:
    mock_qgis_full.QSpinBox = _SpinBox
    mock_qgis_full.QDateEdit = _Unused
    mock_qgis_full.QComboBox = _Unused
    mock_qgis_full.QLineEdit = _Unused
    from agrobr_qgis.gui.param_panel import ParamPanel

    panel = ParamPanel(MagicMock())
    panel._widgets = {
        "ano": (SourceParameter("ano", "Ano", ParamType.INT), _SpinBox(0)),
        "mes": (SourceParameter("mes", "Mês", ParamType.INT, required=True), _SpinBox(0)),
        "max_registros": (
            SourceParameter("max_registros", "Máx. registros", ParamType.INT),
            _SpinBox(100),
        ),
    }

    assert panel.collect_params() == {"mes": 0, "max_registros": 100}
