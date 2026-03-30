from __future__ import annotations

from typing import Any

from agrobr_qgis.core.constants import DTYPE_FALLBACK, DTYPE_MAP, UF_LIST
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
        QgsCoordinateReferenceSystem,
        QgsFeature,
        QgsField,
        QgsFields,
        QgsGeometry,
        QgsProcessingAlgorithm,
        QgsProcessingParameterBoolean,
        QgsProcessingParameterEnum,
        QgsProcessingParameterExtent,
        QgsProcessingParameterFeatureSink,
        QgsProcessingParameterNumber,
        QgsProcessingParameterString,
        QgsWkbTypes,
    )
    from qgis.PyQt.QtCore import QVariant  # type: ignore[import-untyped]

    param_cls_map: dict[str, type[Any]] = {
        "QgsProcessingParameterString": QgsProcessingParameterString,
        "QgsProcessingParameterNumber": QgsProcessingParameterNumber,
        "QgsProcessingParameterEnum": QgsProcessingParameterEnum,
        "QgsProcessingParameterExtent": QgsProcessingParameterExtent,
    }

    GEOM_TYPE_MAP: dict[str, Any] = {
        "Point": QgsWkbTypes.Point,
        "MultiPoint": QgsWkbTypes.MultiPoint,
        "LineString": QgsWkbTypes.LineString,
        "MultiLineString": QgsWkbTypes.MultiLineString,
        "Polygon": QgsWkbTypes.Polygon,
        "MultiPolygon": QgsWkbTypes.MultiPolygon,
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

        def _collect_params(self, parameters: dict[str, Any], context: Any) -> dict[str, Any]:
            kwargs: dict[str, Any] = {}
            for param in self._adapter.parameters():
                if param.param_type == ParamType.INT:
                    val = self.parameterAsInt(parameters, param.name, context)
                    if val:
                        kwargs[param.name] = val
                elif param.param_type == ParamType.UF:
                    idx = self.parameterAsEnum(parameters, param.name, context)
                    if 0 <= idx < len(UF_LIST):
                        kwargs[param.name] = UF_LIST[idx]
                elif param.param_type == ParamType.CHOICE and param.choices:
                    idx = self.parameterAsEnum(parameters, param.name, context)
                    if 0 <= idx < len(param.choices):
                        kwargs[param.name] = param.choices[idx]
                elif param.param_type == ParamType.BBOX:
                    extent = self.parameterAsExtent(parameters, param.name, context)
                    if not extent.isNull():
                        kwargs[param.name] = (
                            extent.xMinimum(),
                            extent.yMinimum(),
                            extent.xMaximum(),
                            extent.yMaximum(),
                        )
                else:
                    val = self.parameterAsString(parameters, param.name, context).strip()
                    if val:
                        kwargs[param.name] = val
            return kwargs

        def processAlgorithm(  # noqa: N802
            self,
            parameters: dict[str, Any],
            context: Any,
            feedback: Any,
        ) -> dict[str, Any]:
            import geopandas as gpd
            import pandas as pd

            from agrobr_qgis.core.data_contract import DataContract

            kwargs = self._collect_params(parameters, context)
            geo = bool(
                self._adapter.capabilities() & SourceCapability.GEO
                and self.parameterAsBool(parameters, "GEO", context)
            )

            feedback.pushInfo(f"Buscando {self._adapter.name()}...")
            source = self._adapter()
            raw = source.fetch(geo=geo, **kwargs)
            result = DataContract.validate(raw)

            if result.row_count == 0:
                feedback.pushInfo("Resultado vazio")
                return {}

            df = result.df
            is_geo = isinstance(df, gpd.GeoDataFrame) and result.has_geometry
            attr_cols = [c for c in df.columns if c != "geometry"]

            fields = QgsFields()
            for col in attr_cols:
                qvariant_name = DTYPE_MAP.get(str(df[col].dtype), DTYPE_FALLBACK)
                fields.append(QgsField(col, getattr(QVariant, qvariant_name)))

            if is_geo:
                wkb_type = GEOM_TYPE_MAP.get(result.geometry_type or "", QgsWkbTypes.Unknown)
                crs = QgsCoordinateReferenceSystem(result.crs or "EPSG:4674")
            else:
                wkb_type = QgsWkbTypes.NoGeometry
                crs = QgsCoordinateReferenceSystem()

            (sink, dest_id) = self.parameterAsSink(
                parameters, "OUTPUT", context, fields, wkb_type, crs
            )

            feedback.pushInfo(f"Escrevendo {result.row_count} features...")
            for _idx, row in df.iterrows():
                if feedback.isCanceled():
                    break
                feat = QgsFeature(fields)
                for col in attr_cols:
                    feat[col] = None if pd.isna(row[col]) else row[col]
                if is_geo:
                    feat.setGeometry(QgsGeometry.fromWkt(row.geometry.wkt))
                sink.addFeature(feat)

            if dest_id:
                from agrobr_qgis.core.layer_builder import LayerBuilder

                style_path = LayerBuilder.resolve_style(result.geometry_type)
                if style_path:
                    layer = context.temporaryLayerStore().mapLayer(dest_id)
                    if layer:
                        layer.loadNamedStyle(style_path)

            return {"OUTPUT": dest_id}

    algo_name = adapter_cls.id().replace("_", " ").title().replace(" ", "")
    _Algorithm.__name__ = f"Fetch{algo_name}Algorithm"
    _Algorithm.__qualname__ = _Algorithm.__name__
    return _Algorithm
