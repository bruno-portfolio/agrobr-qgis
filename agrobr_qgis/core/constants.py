from __future__ import annotations

DEFAULT_CRS: str = "EPSG:4674"
FETCH_TIMEOUT_SECONDS: int = 60
MEMORY_LAYER_MAX_VERTICES: int = 2_000_000
MEMORY_LAYER_MAX_ROWS: int = 50_000
HEALTH_CHECK_TIMEOUT_SECONDS: int = 5

MUNICIPAL_MESH_SHA256: str = "TODO"

DTYPE_MAP: dict[str, str] = {
    "int64": "LongLong",
    "Int64": "LongLong",
    "int32": "Int",
    "Int32": "Int",
    "float64": "Double",
    "Float64": "Double",
    "float32": "Double",
    "bool": "Bool",
    "boolean": "Bool",
    "object": "String",
    "string": "String",
    "datetime64[ns]": "DateTime",
    "datetime64[ns, UTC]": "DateTime",
    "category": "String",
}

DTYPE_FALLBACK: str = "String"
