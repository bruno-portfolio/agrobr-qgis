from __future__ import annotations

from typing import Any

from agrobr_qgis.core.constants import UF_LIST
from agrobr_qgis.core.source_adapter import ParamType, SourceCapability

PARAM_MAP: dict[ParamType, str] = {
    ParamType.STRING: "QgsProcessingParameterString",
    ParamType.INT: "QgsProcessingParameterNumber",
    ParamType.DATE: "QgsProcessingParameterString",
    ParamType.CHOICE: "QgsProcessingParameterEnum",
    ParamType.CHOICE_DYNAMIC: "QgsProcessingParameterString",
    ParamType.MULTI_CHOICE: "QgsProcessingParameterString",
    ParamType.BBOX: "QgsProcessingParameterExtent",
    ParamType.UF: "QgsProcessingParameterEnum",
    ParamType.PRODUTO: "QgsProcessingParameterString",
}


def make_algorithm(adapter_cls: type[Any]) -> type[Any]:  # pragma: no cover
    from qgis.core import (  # type: ignore[import-untyped]
        QgsProcessingAlgorithm,
        QgsProcessingParameterBoolean,
        QgsProcessingParameterEnum,
        QgsProcessingParameterExtent,
        QgsProcessingParameterFeatureSink,
        QgsProcessingParameterNumber,
        QgsProcessingParameterString,
    )

    param_cls_map: dict[str, type[Any]] = {
        "QgsProcessingParameterString": QgsProcessingParameterString,
        "QgsProcessingParameterNumber": QgsProcessingParameterNumber,
        "QgsProcessingParameterEnum": QgsProcessingParameterEnum,
        "QgsProcessingParameterExtent": QgsProcessingParameterExtent,
    }

    class _Algorithm(QgsProcessingAlgorithm):  # type: ignore[misc]
        _adapter = adapter_cls

        def name(self) -> str:
            result: str = f"agrobr_{self._adapter.id()}"
            return result

        def displayName(self) -> str:  # noqa: N802
            result: str = self._adapter.name()
            return result

        def group(self) -> str:
            result: str = self._adapter.category().value.title()
            return result

        def groupId(self) -> str:  # noqa: N802
            result: str = self._adapter.category().value
            return result

        def shortHelpString(self) -> str:  # noqa: N802
            result: str = self._adapter.description()
            return result

        def createInstance(self) -> _Algorithm:  # noqa: N802
            return self.__class__()

        def initAlgorithm(self, config: dict[str, Any] | None = None) -> None:  # noqa: N802, ARG002
            for param in self._adapter.parameters():
                qgs_cls_name = PARAM_MAP.get(param.param_type, "QgsProcessingParameterString")
                qgs_cls = param_cls_map.get(qgs_cls_name, QgsProcessingParameterString)

                if param.param_type == ParamType.UF:
                    self.addParameter(
                        QgsProcessingParameterEnum(
                            param.name,
                            param.label,
                            options=UF_LIST,
                            optional=not param.required,
                        )
                    )
                elif param.param_type == ParamType.CHOICE and param.choices:
                    self.addParameter(
                        QgsProcessingParameterEnum(
                            param.name,
                            param.label,
                            options=param.choices,
                            optional=not param.required,
                        )
                    )
                else:
                    self.addParameter(
                        qgs_cls(
                            param.name,
                            param.label,
                            optional=not param.required,
                        )
                    )

            if self._adapter.capabilities() & SourceCapability.GEO:
                self.addParameter(
                    QgsProcessingParameterBoolean(
                        "GEO",
                        "Saída geoespacial",
                        defaultValue=True,
                    )
                )

            self.addParameter(QgsProcessingParameterFeatureSink("OUTPUT", "Camada de saída"))

        def processAlgorithm(  # noqa: N802
            self,
            parameters: dict[str, Any],
            context: Any,
            feedback: Any,  # noqa: ARG002
        ) -> dict[str, Any]:
            from agrobr_qgis.core.data_contract import DataContract

            kwargs: dict[str, Any] = {}
            for param in self._adapter.parameters():
                val = self.parameterAsString(parameters, param.name, context).strip()
                if val:
                    kwargs[param.name] = val

            geo = bool(
                self._adapter.capabilities() & SourceCapability.GEO
                and self.parameterAsBool(parameters, "GEO", context)
            )

            source = self._adapter()
            raw = source.fetch(geo=geo, **kwargs)
            result = DataContract.validate(raw)

            return {"OUTPUT": result.df}

    algo_name = adapter_cls.id().replace("_", " ").title().replace(" ", "")
    _Algorithm.__name__ = f"Fetch{algo_name}Algorithm"
    _Algorithm.__qualname__ = _Algorithm.__name__
    return _Algorithm
