from __future__ import annotations

DEFAULT_CRS: str = "EPSG:4674"
FETCH_TIMEOUT_SECONDS: int = 60
MEMORY_LAYER_MAX_VERTICES: int = 2_000_000
MEMORY_LAYER_MAX_ROWS: int = 50_000
HEALTH_CHECK_TIMEOUT_SECONDS: int = 5

MUNICIPAL_MESH_URL: str = (
    "https://geoftp.ibge.gov.br/organizacao_do_territorio/"
    "malhas_territoriais/malhas_municipais/municipio_2022/"
    "Brasil/BR/BR_Municipios_2022.zip"
)
UF_MESH_URL: str = (
    "https://geoftp.ibge.gov.br/organizacao_do_territorio/"
    "malhas_territoriais/malhas_municipais/municipio_2022/"
    "Brasil/BR/BR_UF_2022.zip"
)
MUNICIPAL_MESH_SHA256: str = "9c904fa1feb978a89042bfecd7758e571266f285d6122a4ff02ffe37bffb76a2"
UF_MESH_SHA256: str = "282ec7f0f0beeeead45e6609f4ffffce161bda04cb8ee0afcad2316d1c841bcb"

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

UF_LIST: list[str] = [
    "AC",
    "AL",
    "AM",
    "AP",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MG",
    "MS",
    "MT",
    "PA",
    "PB",
    "PE",
    "PI",
    "PR",
    "RJ",
    "RN",
    "RO",
    "RR",
    "RS",
    "SC",
    "SE",
    "SP",
    "TO",
]
